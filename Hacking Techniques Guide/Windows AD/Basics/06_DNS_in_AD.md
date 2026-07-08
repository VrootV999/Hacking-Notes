# DNS in Active Directory

## What it is

Active Directory Domain Services **requires** DNS. It uses DNS for:

- **Service location** — domain controllers register SRV records so clients can find them
- **Domain naming** — each AD domain corresponds to a DNS domain name
- **Global Catalog location** — GC servers register SRV records
- **Kerberos (KDC) location** — clients find KDCs via DNS SRV records
- **Domain join** — during domain join, the client discovers DCs via DNS
- **Site awareness** — clients find DCs in their own site via site-specific DNS records

**Without DNS, AD does not function.** This is why AD-integrated DNS is the most common deployment.

## SRV records — Service location

SRV (Service) records (RFC 2782) map services to servers.

### SRV record format

```
_service._proto.name TTL class SRV priority weight port target
```

### AD-specific SRV records

| SRV record | Purpose |
|------------|---------|
| `_ldap._tcp.dc._msdcs.<domain>` | Domain Controllers offering LDAP |
| `_kerberos._tcp.dc._msdcs.<domain>` | KDC (Domain Controllers) |
| `_kerberos._udp.<domain>` | KDC (UDP) |
| `_kpasswd._tcp.<domain>` | Kerberos password change (TCP) |
| `_kpasswd._udp.<domain>` | Kerberos password change (UDP) |
| `_gc._tcp.<forest>` | Global Catalog servers |
| `_ldap._tcp.<SiteName>._sites.dc._msdcs.<domain>` | DCs in a specific site |
| `_kerberos._tcp.<SiteName>._sites.dc._msdcs.<domain>` | KDCs in a specific site |
| `_ldap._tcp.gc._msdcs.<forest>` | Global Catalog servers (alternative) |
| `_ldap._tcp.<SiteName>._sites.gc._msdcs.<forest>` | GC servers in a specific site |
| `_ldap._tcp.pdc._msdcs.<domain>` | PDC Emulator |
| `_ldap._tcp.<DomainGUID>.domains._msdcs.<forest>` | Domain lookup by GUID |
| `_kerberos._tcp.dc._msdcs.<forest>` | Domain-agnostic DC lookup |

### DC locator process

When a domain-joined client needs to find a DC:

```
1. Client's Netlogon service queries DNS for:
   _ldap._tcp.<SiteName>._sites.dc._msdcs.<domain>

2. If no site-specific records found:
   _ldap._tcp.dc._msdcs.<domain>

3. Returns SRV records with:
   - Priority (lower = preferred)
   - Weight (relative load balancing)
   - Target hostname (DNS A record)

4. Client resolves the target hostname via A/AAAA record

5. Client sends LDAP ping to the DC (CLDAP, port 389 UDP)

6. DC responds with:
   - Whether it's a GC
   - Whether it's the PDC
   - The client's site name
   - Domain GUID
   - Forest and domain name

7. Client caches the DC info and uses it for authentication
```

## DNS zones

### Zone types

| Zone type | Description |
|-----------|-------------|
| **Primary** | Master copy of zone data; writable |
| **Secondary** | Read-only copy transferred from a primary |
| **Stub** | Contains only SOA, NS, and glue records; used for delegation |
| **AD-integrated** | Zone data stored in AD DS (NTDS.dit); replicated via AD replication |

### AD-integrated DNS zones

AD-integrated zones store DNS data in the AD database (in application partitions). This provides:

- **Multi-master updates** — any DC can update DNS records
- **Secure dynamic updates** — only authenticated computers can update their own records
- **Automatic replication** — zone data replicates via AD replication (no need for zone transfers)
- **Integrated with AD security** — DNS records have ACLs like AD objects

**Application partitions for DNS:**

| Partition | Contents | Replication scope |
|-----------|----------|-------------------|
| `DomainDnsZones` | Domain's DNS zones | All DCs in the domain |
| `ForestDnsZones` | Forest-wide DNS zones | All DCs in the forest |

## Dynamic DNS updates

Domain-joined computers automatically register and update their DNS records.

### A/AAAA record registration

1. When a computer boots, its `netlogon` service sends a DHCP request
2. If DHCP is used, the DHCP server can register the client's PTR record
3. The client attempts to update its A/AAAA record in DNS
4. The client also registers its PTR record (reverse lookup)

### SRV record registration

Domain Controllers register SRV records when the `netlogon` service starts:

```powershell
# Force registration
net stop netlogon && net start netlogon

# Or via nltest
nltest /dsregdns
```

### Secure dynamic updates

When a zone is configured for **Secure Dynamic Updates**:

- The client must authenticate to the DC
- The client may only update records for which it has ownership
- Ownership is based on the machine account's SID in AD

**Attack angle:** If a zone allows non-secure updates, an attacker can create arbitrary DNS records without authentication.

## DNS scavenging

Scavenging removes stale DNS records automatically.

| Setting | Description |
|---------|-------------|
| **No-refresh interval** | Time during which a record owner cannot refresh its timestamp (default 7 days) |
| **Refresh interval** | Time after which the record owner can refresh (default 7 days) |
| **Scavenging period** | How often the DNS server scans for stale records (default 7 days) |
| **Enable scavenging** | Must be enabled at the server and zone levels |

If scavenging is disabled, stale records accumulate, including records of decommissioned servers. Attackers can exploit stale records for **DNS hijacking**.

## Dnscmd and dnscache

### dnscmd (command-line DNS management)

```cmd
# View zones on a DNS server
dnscmd DC01 /zoneprint corp.example.com

# Show record details
dnscmd DC01 /enumrecords corp.example.com.

# Force zone transfer
dnscmd DC01 /zonerefresh corp.example.com

# Add a record
dnscmd DC01 /recordadd corp.example.com evil A 10.10.10.50

# Delete a record
dnscmd DC01 /recorddelete corp.example.com evilsrv A

# Configure scavenging
dnscmd DC01 /config /scavenginginterval 1440
dnscmd DC01 /config /defaultrefreshinterval 1440
```

### dnscache (client-side)

```powershell
# View DNS cache
ipconfig /displaydns

# Flush DNS cache
ipconfig /flushdns

# Register DNS records
ipconfig /registerdns
```

## AD DNS records enumeration

### Using PowerShell

```powershell
# Retrieve all DNS records from AD
Get-DnsServerResourceRecord -ZoneName "corp.example.com"

# All A records
Get-DnsServerResourceRecord -ZoneName "corp.example.com" -RRType A

# All SRV records
Get-DnsServerResourceRecord -ZoneName "corp.example.com" -RRType SRV

# All DC SRV records
Resolve-DnsName -Type SRV _ldap._tcp.dc._msdcs.corp.example.com

# Using nslookup
nslookup -type=SRV _ldap._tcp.dc._msdcs.corp.example.com
```

### Using adidnsdump (attacker tool)

```bash
# Dump all AD DNS records
adidnsdump -u corp\\jsmith corp-dc.corp.com
```

## How attackers abuse AD DNS

| Attack | Description |
|--------|-------------|
| **adidnsdump** | Dump all DNS records from AD-integrated zones via LDAP — reveals all machines, servers, and their roles |
| **DNSTool (Krbtgt delegation)** | Add/modify DNS ACLs to grant a compromised account write access to DNS records; used in the Krbtgt delegation attack to redirect authentication |
| **DNS poisoning** | Modify DNS records to redirect traffic to attacker's server (e.g., replace a server's A record to intercept Net-NTLM hashes) |
| **Non-secure dynamic updates** | Register arbitrary records if the zone allows non-secure updates — enables man-in-the-middle |
| **DNS spoofing** | Spoof DNS responses to redirect the client to an attacker-controlled machine |
| **Stale record abuse** | Register a machine with the same hostname as a defunct server; take over services via name collision |
| **DNS hijacking via WPAD** | Register a WPAD record to proxy all client HTTP traffic |
| **DNS zone transfer** | If a zone allows unrestricted AXFR, dump the entire zone for reconnaissance |
| **DNS tunneling** | Encapsulate data in DNS queries/responses for C2 communication (e.g., dnscat2) |
| **DNS cache poisoning** | Poison the DNS resolver cache to redirect future lookups |
| **DnsAdmins abuse** | The DnsAdmins group has privileges to load DLLs into the DNS process — can be used for code execution as SYSTEM on the DNS server |

### DnsAdmins to Domain Admin path

1. A member of DnsAdmins on a DC (or DNS server) can run:
   ```cmd
   dnscmd DC01 /config /serverlevelplugindll C:\path\to\malicious.dll
   ```
2. This forces the DNS service to load the DLL
3. The DLL executes as `SYSTEM` on the DNS server (often a Domain Controller)
4. Result: **Domain Admin** from DnsAdmins membership

### Krbtgt delegation attack (DNSTool)

1. An attacker with `GenericWrite` on a DNS zone can modify ACLs
2. Grant a controlled computer account `AllowedToActOnBehalfOfOtherIdentity`
3. Use RBCD to impersonate any user to that computer
4. This effectively gives the attacker domain admin if they can control a DC

## Defender recommendations

1. **Enable secure dynamic updates** for all AD-integrated zones.

2. **Enable DNS scavenging** to remove stale records — reduces the attack surface for name collisions.

3. **Restrict zone transfers** — only allow to secondary DNS servers; never to any server.

4. **Audit DnsAdmins membership** — no normal users should be in this group.

5. **Monitor DNS changes:**
   - Event ID 770: DNS zone modified
   - Event ID 771: DNS record updated
   - Event ID 772: DNS zone transfer
   - Event ID 773: DNS record added
   - Event ID 774: DNS record deleted

6. **Use DNS logging** — enable audit logging for DNS queries if possible.

7. **Disable non-secure dynamic updates** — every zone should require authentication.

8. **Register DC service records** — use `nltest /dsregdns` to verify DC registration.

9. **Monitor for unusual SRV records** — especially `_vlmcs`, `_wpad`, or unknown service records.

10. **Implement DNS over HTTPS (DoH) or DNS over TLS (DoT)** if available — prevents DNS spoofing at the network level.

11. **Use DomainDnsZones and ForestDnsZones application partitions** — do not use primary zones for AD DNS.

12. **Protect the DnsAdmins group** — restrict membership and monitor for modifications.

## Relevant RFCs and MS protocols

| Document | Description |
|----------|-------------|
| RFC 1034 | Domain Names — Concepts and Facilities |
| RFC 1035 | Domain Names — Implementation and Specification |
| RFC 2782 | A DNS RR for Specifying the Location of Services (SRV) |
| RFC 2136 | Dynamic Updates in the Domain Name System |
| RFC 3007 | Secure Domain Name System (DNS) Dynamic Update |
| RFC 3645 | Generic Security Service Algorithm for Secret Key Transaction Authentication for DNS (GSS-TSIG) |
| [MS-ADTS] | AD Technical Specification (DNS requirements) |
| [MS-DNSP] | DNS Server Management Protocol |
| [MS-NLMP] | Netlogon Remote Protocol (includes DC locator DNS) |
