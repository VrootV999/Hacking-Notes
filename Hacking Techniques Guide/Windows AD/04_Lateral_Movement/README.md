# Lateral Movement in Active Directory

Lateral movement refers to techniques used to move from one compromised host to another within a network. After gaining initial access and harvesting credentials, lateral movement expands the foothold and enables privilege escalation toward domain dominance.

## Core Concepts

- **Credential Reuse** — Most lateral movement relies on password hashes, tickets, or keys captured from one machine being replayed on another
- **Protocol Dependencies** — Each technique leverages a different protocol (SMB, WinRM, RPC, WMI, RDP) affecting what ports need to be open and what tools can be used
- **Authentication Model** — NTLM vs Kerberos determines which forms of credentials (hash vs ticket) are viable
- **Local Admin Required** — Almost all lateral movement techniques require administrative privileges on the target machine

## Technique Selection Matrix

| Technique | Protocol | Port | Auth Required | Tool Examples |
|-----------|----------|------|---------------|--------------|
| Pass-the-Hash | SMB/WinRM | 445/5985 | Local admin | Impacket, Mimikatz, NetExec |
| Overpass-the-Hash | Kerberos | 88 | Domain user w/ hash | Rubeus |
| Pass-the-Ticket | Kerberos | 88 | Domain user w/ ticket | Rubeus, Mimikatz |
| PsExec | SVCCTL | 445 | Local admin | Impacket, Sysinternals, NetExec |
| WMI Exec | RPC | 135/49152+ | Local admin | Impacket, wmic |
| SMB Exec | SVCCTL | 445 | Local admin | Impacket |
| PowerShell Remoting | WinRM | 5985/5986 | Local admin / WinRM group | evil-winrm, PowerShell |
| Scheduled Tasks | RPC | 135/445 | Local admin | schtasks, SharpSC |
| RDP | RDP | 3389 | RDP access / local admin | xfreerdp, SharpRDP |
| DPAPI | SMB | 445 | Local admin (SYSTEM) | SharpDPAPI, robocopy |
| DCOM | RPC/DCOM | 135/49152+ | Local admin | dcomexec.py, MMC20.Application |

## General OPSEC Principles

1. **Minimize touch** — Each connection leaves Event Log traces; fewer connections = less detection
2. **Use existing sessions** — Reusing cached tickets or existing WinRM sessions is stealthier than creating new processes
3. **Avoid PsExec** — PsExec creates a service, is heavily monitored, and triggers 4697/7045 alerts
4. **Prefer WinRM/WMI** — These run in-process without dropping binaries when done correctly
5. **Clean up** — Remove created services, scheduled tasks, and dumped artifacts
6. **Use hostnames not IPs** — Kerberos authentication requires hostnames; IPs force NTLM fallback
7. **Target selection** — Attack workstations (users have sessions, cached credentials) before servers

## Detection Overview

| Event ID | Description |
|----------|-------------|
| 4624 | Logon — check LogonType (3=Network, 9=NewCreds, 10=RemoteInteractive) |
| 4625 | Failed logon |
| 4648 | Explicit credential logon |
| 4672 | Admin logon (SeTcbPrivilege, SeDebugPrivilege) |
| 4697 | Service creation (PsExec, service exe) |
| 5140 | SMB share access |
| 5145 | SMB file access (check IPC$, ADMIN$) |
| 7036 | Service start/stop |
| 7045 | Service install (SCM event) |

## Pre-requisite Verifications

```powershell
# Test SMB connectivity
Test-NetConnection -ComputerName target -Port 445

# Test WinRM connectivity
Test-WSMan -ComputerName target

# Test RDP connectivity
Test-NetConnection -ComputerName target -Port 3389

# Check if local admin on target (from Domain Controller)
net localgroup "Administrators" /domain

# From a compromised machine — test WMI
wmic /node:target process call create "cmd /c whoami"
```

## Technique Files

| # | File | Description |
|---|------|-------------|
| 01 | [Pass-the-Hash](01_Pass_The_Hash.md) | PtH with SMB/WinRM using NTLM hashes |
| 02 | [Overpass-the-Hash](02_Overpass_The_Hash.md) | Convert NTLM hash to Kerberos TGT |
| 03 | [Pass-the-Ticket](03_Pass_The_Ticket.md) | Reuse Kerberos tickets for authentication |
| 04 | [PsExec](04_PsExec.md) | Service control manager remote execution |
| 05 | [WMI Exec](05_WMI_Exec.md) | WMI-based remote execution |
| 06 | [SMB Exec](06_SMB_Exec.md) | SMB-based remote command execution |
| 07 | [PowerShell Remoting](07_PowerShell_Remoting.md) | WinRM-based PowerShell remoting |
| 08 | [Scheduled Tasks](08_Scheduled_Tasks.md) | Remote task scheduling for execution |
| 09 | [RDP](09_RDP.md) | Remote Desktop Protocol lateral movement |
| 10 | [DPAPI](10_DPAPI_Lateral.md) | DPAPI credential theft and lateral movement |
| 11 | [DCOM Lateral Movement](11_DCOM_Lateral_Movement.md) | DCOM-based remote execution |
| 12 | [PtH with Machine Accounts](12_Pass_The_Hash_Machine_Accounts.md) | Pass-the-Hash using Machine$ accounts |
