# NetBIOS and Name Resolution Protocol

## What it is

Name resolution in Windows networks involves multiple protocols that work together (and sometimes conflict). Understanding each is critical because **name resolution attacks are among the easiest and most common ways to compromise an Active Directory environment**.

The key protocols are:
- **DNS** — Domain Name System (primary, modern)
- **NBT-NS** — NetBIOS over TCP/IP Name Service (NetBIOS name resolution)
- **LLMNR** — Link-Local Multicast Name Resolution (DNS-like for local links)
- **mDNS** — Multicast DNS (Apple/Bonjour, also used by some Windows features)
- **WINS** — Windows Internet Name Service (centralized NetBIOS name server)

## NetBIOS over TCP/IP (NBT)

### What is NetBIOS

NetBIOS (Network Basic Input/Output System) was originally developed by IBM and Sytek in 1983. It provides three services:

1. **Name service** — Name registration and resolution (port 137)
2. **Datagram service** — Connectionless communication (port 138)
3. **Session service** — Connection-oriented communication (port 139)

NetBIOS names are **16 bytes** (15 characters + 1 byte suffix).

### NetBIOS name types

| Type | Suffix byte | Suffix (hex) | Description |
|------|-------------|--------------|-------------|
| Unique | 0x00 | Workstation Service | Workstation service name |
| Group | 0x00 | Workstation Service | Domain name |
| Unique | 0x03 | Messenger Service | Messenger service (used for net send) |
| Unique | 0x06 | RAS Server Service | Remote Access Server |
| Unique | 0x1B | Domain Master Browser | Domain master browser (PDC) |
| Unique | 0x1D | Master Browser | Local master browser |
| Group | 0x1E | Browser Service Elections | Browser election service |
| Unique | 0x20 | Server Service | File server / SMB listener |
| Unique | 0x21 | RAS Client Service | Remote Access Client |
| Group | 0x2B | Lotus Notes | Lotus Notes Server |
| Unique | 0x6A | DCA IRMALAN | Gateway service |

**Notable:** `0x20` (Server Service) is the most commonly resolved — it's what maps to a computer's SMB server.

### NetBIOS name registration

When a NetBIOS-enabled computer boots:

```
1. Client sends a NetBIOS Name Registration request (broadcast)
2. If no other computer responds with "NAME CONFLICT", the name is registered
3. If a WINS server is configured, the client registers with WINS instead
4. Names are cached locally (NetBIOS name cache)
```

### NetBIOS name resolution

```
Client needs to resolve "FILESERVER"
         │
         ├── 1. Check local NetBIOS name cache
         │    └── if found → done
         │
         ├── 2. Send NBNS broadcast (UDP port 137)
         │    └── Target responds with its IP
         │    └── Timeout: 3 broadcasts, 0.75s apart
         │
         ├── 3. Check LMHOSTS file (if configured)
         │    └── %SystemRoot%\System32\drivers\etc\lmhosts
         │
         ├── 4. Query WINS server (if configured, port 137 TCP/UDP)
         │    └── WINS responds with IP
         │
         └── 5. Try HOSTS file / DNS as final fallback
              └── order depends on NetbiosNodeType
```

### NetBIOS node types

The **NetbiosNodeType** registry value (`HKLM\SYSTEM\CurrentControlSet\Services\Netbt\Parameters\NodeType`) determines name resolution order:

| Node type | Value | Resolution order |
|-----------|-------|------------------|
| B-node (Broadcast) | 1 | Broadcast only |
| P-node (Peer) | 2 | WINS only |
| M-node (Mixed) | 4 | Broadcast, then WINS |
| H-node (Hybrid) | 8 | **WINS, then broadcast** (default for DHCP clients) |

## NetBIOS suffixes

The 16th byte of a NetBIOS name indicates the service type. The suffix is encoded in the name query/registration packets.

```
Example: FILESERVER<00> vs FILESERVER<20>
  <00> = Workstation Service
  <20> = Server Service (SMB)

COMPUTER1     <00>  Unique  Workstation
COMPUTER1     <03>  Unique  Messenger
COMPUTER1     <20>  Unique  Server
CORP          <00>  Group   Domain Name
CORP          <1C>  Group   Domain Controllers
CORP          <1E>  Group   Browser Elections
CORP          <1D>  Unique  Master Browser
```

## NBSTAT (nbtstat)

```cmd
# View local NetBIOS name table
nbtstat -n

# Look up a remote NetBIOS name table
nbtstat -A 10.10.10.50   (by IP)
nbtstat -a FILESERVER    (by name)

# View NetBIOS name cache
nbtstat -c

# Purge cache and reload LMHOSTS
nbtstat -R

# List statistics by protocol
nbtstat -s
```

**NBSTAT output example:**
```
Local Area Connection:
Node IpAddress: [10.10.10.50] Scope Id: []

           NetBIOS Remote Machine Name Table

    Name               Type         Status
    ---------------------------------------------
    FILESERVER    <00>  UNIQUE      Registered
    CORP          <00>  GROUP       Registered
    FILESERVER    <20>  UNIQUE      Registered
    CORP          <1C>  GROUP       Registered
    CORP          <1E>  GROUP       Registered
    CORP          <1D>  UNIQUE      Registered
    ..._MSBROWSE_.<01>  GROUP       Registered

    MAC Address = 00-11-22-33-44-55
```

**Attackers use nbtstat** to discover servers, domain controllers, and domain names during reconnaissance.

## LLMNR (Link-Local Multicast Name Resolution)

### What is LLMNR

LLMNR (RFC 4795) is a protocol based on DNS packet format that enables name resolution for peers on a local link. It is used when DNS queries fail.

- **Port:** 5355/UDP
- **Multicast address:** 224.0.0.252 (IPv4), FF02:0:0:0:0:0:1:3 (IPv6)
- **Enabled by default** on Windows Vista and later

### LLMNR flow

```
1. Client tries DNS first
2. If DNS fails → sends LLMNR multicast query:
   "Who has FILESERVER?"
   (Multicast to all LLMNR-enabled systems on the local link)

3. The owner of FILESERVER responds unicast with its IP
4. Client connects to the responder
```

### LLMNR security problems

LLMNR has **no authentication** — any host on the local link can respond to any query. This is the core of the **Responder attack**.

## mDNS (Multicast DNS)

### What is mDNS

mDNS (RFC 6762) is used by Apple Bonjour and some Linux/Windows services. It resolves hostnames ending in `.local`.

- **Port:** 5353/UDP
- **Multicast address:** 224.0.0.251 (IPv4)
- **Primarily used by:** Apple devices, printer discovery, some IoT

Windows supports mDNS starting with Windows 10, primarily for printing and device discovery.

## WINS (Windows Internet Name Service)

WINS is a centralized **NetBIOS Name Server** (NBNS). It maps NetBIOS names to IP addresses.

### How WINS works

```
1. Clients register their NetBIOS name + IP with the WINS server
2. When resolving names, clients query the WINS server (unicast)
3. WINS servers can replicate with each other
4. If WINS is unavailable, clients fall back to broadcast
```

**WINS limitations:**
- No security (no authentication of registrations)
- Flat namespace (no hierarchy)
- NetBIOS names are limited to 15 characters
- Deprecated in favor of DNS (removed from Windows Server 2025+)

### WINS port

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| 42/TCP, UDP | WINS replication | WINS ↔ WINS | Server replication |
| 137/TCP, UDP | NBNS | Client ↔ WINS | Name registration/resolution |

## WPAD (Web Proxy Auto-Discovery Protocol)

WPAD allows clients to automatically discover web proxy settings. It is significant in name resolution attacks.

### WPAD discovery

Clients look for a proxy configuration file (`wpad.dat`) by trying:

1. **DNS:** Query for `wpad.<domain>` (A record)
2. **DHCP:** DHCP option 252 provides the WPAD URL
3. **LLMNR/NBT-NS:** If DNS fails, multicast/broadcast for "WPAD"

**Attack:** An attacker responds to LLMNR/NBT-NS queries for "WPAD" with their own IP, hosts a `wpad.dat` file that proxies all traffic through the attacker, capturing all HTTP traffic (including NTLM hashes).

## Name resolution order on Windows

The default order for hostname resolution:

```
1. Local HOSTS file       (%SystemRoot%\System32\drivers\etc\hosts)
2. DNS                    (primary, according to adapter DNS servers)
3. LLMNR                  (multicast, if DNS fails)
4. NetBIOS                (broadcast + WINS, if LLMNR fails)
   ├── Local NetBIOS cache
   ├── Broadcast (NBNS)
   ├── LMHOSTS file
   └── WINS server
```

The exact order depends on:
- DNS suffix search list
- NetbiosNodeType value
- Link-local multicast settings
- LLMNR enabled/disabled

## Comparison: LLMNR vs NBT-NS vs mDNS vs DNS

| Feature | DNS | LLMNR | NBT-NS | mDNS |
|---------|-----|-------|--------|------|
| RFC | 1034, 1035 | 4795 | 1001, 1002 | 6762 |
| Port | 53/UDP, TCP | 5355/UDP | 137/UDP | 5353/UDP |
| Scope | Global / enterprise | Local link | Local link (or WINS) | Local link |
| Multicast | No | 224.0.0.252 | Broadcast (255.255.255.255) | 224.0.0.251 |
| Authentication | Optional (DNSSEC) | None | None | None |
| Namespace | Hierarchical | Flat | Flat (15 chars) | .local |
| Security | DNSSEC | No security | No security | No security |
| Windows default | Always enabled | Enabled (Vista+) | Enabled (legacy) | Partial (Win 10+) |
| Attack vector | Poisoning | Responder | Responder | Responder |

## How attackers abuse name resolution

| Attack | Protocol | Description |
|--------|----------|-------------|
| **Responder** | LLMNR, NBT-NS, mDNS | Listen for name resolution queries and respond with the attacker's IP to capture Net-NTLM hashes |
| **Inveigh** | LLMNR, NBT-NS, mDNS, DNS | PowerShell-based version of Responder with more features |
| **MITM6** | DHCPv6 + DNS | Advertise rogue DNS server via DHCPv6 to redirect name resolution |
| **WPAD poisoning** | DNS, LLMNR, NBT-NS | Respond to WPAD queries; host malicious proxy config to capture traffic |
| **DNS spoofing** | DNS | Send forged DNS responses to redirect traffic |
| **SMB relay + Responder** | LLMNR/NBT-NS | Capture hashes via Responder and relay them to target servers |
| **NBNS spoofing** | NBT-NS | Forge NetBIOS name resolution responses |
| **WINS poisoning** | WINS | Register rogue entries on WINS server to redirect traffic |
| **HOSTS file modification** | File | Modify local HOSTS file to redirect specific names |
| **DNS search list poisoning** | DNS | Add malicious domains to search list via DHCP to capture traffic |

### The Responder attack chain

```
1. Attacker runs Responder on the local subnet:
   python Responder.py -I eth0

2. User tries to access a resource by name (e.g., "\\FILESERVER\share")
   But FILESERVER is not in DNS → client falls back to LLMNR

3. Client broadcasts LLMNR query for "FILESERVER"

4. Responder answers: "FILESERVER is at 10.10.10.50" (attacker's IP)

5. Client connects to attacker's SMB server, sending NTLMSSP NEGOTIATE

6. Attacker challenges the client (8-byte random challenge)

7. Client responds with Net-NTLMv2 hash

8. Attacker now has the hash, which can be:
   - Cracked offline (hashcat mode 5600 for Net-NTLMv2)
   - Relayed to another server (if SMB signing is not enforced)
```

### MITM6 (Man-in-the-Middle via DHCPv6)

```
1. Attacker runs mitm6:
   mitm6 -d corp.com

2. Attacker's fake DHCPv6 server responds to DHCPv6 Solicit
   Offering: DNS server = attacker's IP

3. Windows clients prefer IPv6 over IPv4 in default configuration
   
4. Client queries DNS for resources → attacker controls resolution

5. Attacker redirects queries to their own servers
   → Captures NTLM hashes
```

## Defender recommendations

1. **Disable LLMNR** via Group Policy:
   - Computer Configuration → Administrative Templates → Network → DNS Client
   - "Turn off LLMNR" → **Enabled**

2. **Disable NBT-NS** on network adapters:
   - Network adapter properties → IPv4 → Advanced → WINS → Disable NetBIOS over TCP/IP
   - Or via Group Policy / PowerShell:
     ```powershell
     Get-NetAdapter | Set-DNSClient -RegisterThisConnectionsAddress $false
     Disable-NetAdapterBinding -Name "*" -ComponentID "ms_netbt"
     ```

3. **Use secure DNS** — ensure all clients use DNS for resolution; remove dependency on NetBIOS/WINS.

4. **Remove WINS** — migrate from WINS to DNS for all name resolution.

5. **Disable WPAD** via Group Policy:
   - "Turn off automatic proxy detection" → **Enabled**
   - Configure proxy settings manually if needed.

6. **Prefer IPv4 or secure IPv6** — configure DHCPv6 with authenticated DHCP servers.

7. **Enable SMB signing** — prevents relay of captured hashes even if hash capture occurs.

8. **Enable LDAP signing + channel binding** — prevents relay to LDAP.

9. **Monitor for Responder activity**:
   - Event ID 4698: Windows event log for LLMNR activity (limited)
   - Network monitoring for:
     - Sudden increase in NBT-NS broadcasts
     - LLMNR queries for "WPAD" or "ISATAP"
     - Multiple LLMNR responses for the same query
     - NBNS responses from unexpected hosts

10. **Enable Link-Layer Topology Discovery (LLTD)** responder blocking via firewall.

11. **Use Windows Defender Firewall** — block inbound ports 137, 138, 139, 5355 from untrusted networks.

12. **Network segmentation** — limit exposure of sensitive servers to broadcast domains.

## Relevant RFCs

| Document | Description |
|----------|-------------|
| RFC 1001 | Protocol Standard for NetBIOS Service on TCP/UDP |
| RFC 1002 | NetBIOS Working Group Detailed Specifications |
| RFC 4795 | Link-Local Multicast Name Resolution (LLMNR) |
| RFC 6762 | Multicast DNS (mDNS) |
| RFC 6763 | DNS-Based Service Discovery (DNS-SD) |
| RFC 2131 | Dynamic Host Configuration Protocol (DHCP) |
| RFC 3315 | DHCPv6 |
| RFC 6106 | IPv6 Router Advertisement Options for DNS Configuration |
