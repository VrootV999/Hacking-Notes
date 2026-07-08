# LDAP Protocol in Active Directory

## What it is

Lightweight Directory Access Protocol (LDAP) is an open, vendor-neutral protocol for accessing and maintaining distributed directory information services over an IP network. In Active Directory, LDAP is the **primary protocol for querying and modifying** directory objects.

AD implements LDAPv3 (RFC 4511) with Microsoft-specific extensions and schema.

## LDAP directory structure

An LDAP directory is organized as a **tree hierarchy** (DIT — Directory Information Tree). Each node is an **entry** (object) with a set of **attributes**.

### Distinguished Names (DN)

Every object in AD has a unique Distinguished Name that describes its exact position in the LDAP tree.

```
DN: CN=John Smith,CN=Users,DC=corp,DC=example,DC=com

Components:
  CN=John Smith       Common Name (the object itself)
  CN=Users            Common Name (container)
  DC=corp             Domain Component
  DC=example          Domain Component
  DC=com              Domain Component
```

### Relative Distinguished Names (RDN)

The leftmost component of the DN is the RDN — it uniquely identifies the entry within its immediate container.

- RDN: `CN=John Smith`
- Container: `CN=Users,DC=corp,DC=example,DC=com`

### LDAP naming contexts

AD has several naming contexts (partitions):

| Naming context | DN example | Contents |
|---------------|------------|----------|
| Domain | `DC=corp,DC=example,DC=com` | Domain objects (users, groups, computers, OUs) |
| Configuration | `CN=Configuration,DC=corp,DC=example,DC=com` | Topology, services, sites |
| Schema | `CN=Schema,CN=Configuration,DC=corp,DC=example,DC=com` | Object classes and attributes |
| DNS zones | `DC=DomainDnsZones,DC=corp,DC=example,DC=com` | AD-integrated DNS zone data |

## LDAP operations

### Bind (authentication)

Clients must bind (authenticate) to the LDAP server before performing queries/modifications.

```
Client                              LDAP Server (DC)
  │                                        │
  │  BindRequest                           │
  │  ──────────────────────────────────→   │
  │  • LDAP version (3)                    │
  │  • Authentication type:                │
  │    - Simple (cleartext password)       │
  │    - SASL (NTLM, Kerberos, GSSAPI)     │
  │                                        │
  │  BindResponse                          │
  │  ←──────────────────────────────────  │
  │  • Result code (0 = success)           │
  │                                        │
```

**Authentication options:**

| Method | Security | Usage |
|--------|----------|-------|
| Simple bind | None (cleartext) | Usually disabled; uses SSL/TLS |
| SASL NTLM | Medium | NTLM-based bind |
| SASL Kerberos (GSSAPI) | High | Kerberos-based bind; preferred |
| SASL GSS-SPNEGO | Negotiates Kerberos or NTLM | Default for many tools |
| Simple bind + LDAPS | High | Simple bind over SSL |

### Search

The most common LDAP operation. Queries the directory with a specific scope, filter, and attribute list.

```
SearchRequest:
  baseObject: OU=Users,DC=corp,DC=example,DC=com
  scope: subtree
  filter: (&(objectCategory=person)(objectClass=user))
  attributes: ["sAMAccountName", "displayName", "mail"]
  sizeLimit: 1000
  timeLimit: 120
```

**Search scopes:**

- **base** — only the base object itself
- **oneLevel** — immediate children of the base object
- **subtree** — entire subtree including the base object

### LDAP search filters

Filters use prefix notation (operators before operands).

| Filter | Meaning |
|--------|---------|
| `(objectClass=user)` | All user objects |
| `(&(objectClass=user)(department=IT))` | Users in IT department (AND) |
| `(|(objectClass=user)(objectClass=group))` | Users OR groups (OR) |
| `(!(objectClass=computer))` | All non-computer objects (NOT) |
| `(sAMAccountName=jsmith*)` | sAMAccountName starting with "jsmith" |
| `(sAMAccountName=jsmith)` | Exact match |
| `(memberOf=CN=Domain Admins,CN=Users,DC=corp,DC=com)` | Members of Domain Admins group |
| `(objectCategory=person)` | All person objects (includes contacts and users) |
| `(userAccountControl:1.2.840.113556.1.4.803:=2)` | Users with ACCOUNTDISABLE bit set |
| `(objectSid=S-1-5-21-...-500)` | Find object by SID |

**Bitwise matching rules:**

- `1.2.840.113556.1.4.803` = LDAP_MATCHING_RULE_BIT_AND (AND — all bits must match)
- `1.2.840.113556.1.4.804` = LDAP_MATCHING_RULE_BIT_OR (OR — any bit must match)

### Compare

Checks whether an entry has a specific attribute value. Returns TRUE/FALSE. Used internally for access checks.

### Add

Creates a new entry. Must specify all mandatory attributes for the object class.

```
AddRequest:
  entry: CN=jdoe,CN=Users,DC=corp,DC=example,DC=com
  attributes:
    objectClass: user
    sAMAccountName: jdoe
    userPrincipalName: jdoe@corp.example.com
    displayName: Jane Doe
```

### Modify

Changes attributes on an existing entry. Operations: `add`, `delete`, `replace`.

```
ModifyRequest:
  entry: CN=jdoe,CN=Users,DC=corp,DC=example,DC=com
  changes:
    - operation: replace
      attribute: telephoneNumber
      values: ["+1-555-0123"]
    - operation: add
      attribute: memberOf
      values: ["CN=VPN Users,CN=Groups,DC=corp,DC=com"]
```

### Delete

Removes an entry. Can only delete leaf objects (containers must be emptied first).

### Modify DN

Moves or renames an entry within the directory tree.

```
ModifyDNRequest:
  entry: CN=jdoe,CN=Users,DC=corp,DC=example,DC=com
  newrdn: CN=john.doe
  deleteoldrdn: TRUE
  newSuperior: OU=Managers,DC=corp,DC=example,DC=com
```

## LDAP controls

Controls extend LDAP operations. They are sent alongside requests.

### Paged Results (1.2.840.113556.1.4.319)

Controls result set size. Without paging, AD limits search results to 1000 entries (or 5000 in newer versions). Paged results allow retrieving large result sets in chunks.

```
Control: 1.2.840.113556.1.4.319
  size: 500 (entries per page)
  cookie: "" (empty on first request; server returns cookie for subsequent)
```

### Server-side Sort (1.2.840.113556.1.4.473)

Allows sorting results on the server side before returning them.

### Security Descriptor Flags (1.2.840.113556.1.4.801)

Controls which parts of a security descriptor are returned in `nTSecurityDescriptor`.

### SD Rights (1.2.840.113556.1.4.801)

DACL/SACL owner/group rights control.

### Permissive Modify (1.2.840.113556.1.4.1413)

If set, a modify operation that tries to add a value that already exists (or delete one that doesn't) does not cause an error.

### Fast Bind (1.2.840.113556.1.4.1781)

Allows SChannel-based bind without requiring a full Kerberos exchange.

## LDAP referrals

When an LDAP query targets objects stored on a different server or domain, the server may return a **referral** — a pointer to the server that holds the requested data.

```
Client → DC1: "Find user jdoe"
DC1 → Client: Referral to DC2.corp.example.com (if jdoe is on DC2)
```

## LDAP over SSL (LDAPS)

- Port: **636/TCP** (LDAPS)
- Port: **3269/TCP** (Global Catalog LDAPS)
- Requires a valid server certificate on the DC
- Encrypts all LDAP traffic (bind, search, modify)
- Auto-enrolled certificate on DCs via AD CS if the enterprise CA is deployed

## Global Catalog (GC)

The Global Catalog is accessed via LDAP on separate ports:

- **3268/TCP** — GC LDAP (non-SSL)
- **3269/TCP** — GC LDAP (SSL)

The GC contains all objects from all domains in the forest, but only a subset of attributes (the **Partial Attribute Set** or PAS).

### Use cases:
- Forest-wide searches (find a user by name in any domain)
- Universal group membership resolution at logon
- Exchange address book lookups

## AD-specific LDAP attributes

### User attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `sAMAccountName` | Pre-Windows 2000 logon name | `jdoe` |
| `userPrincipalName` | UPN logon | `jdoe@corp.com` |
| `objectSid` | Security Identifier | `S-1-5-21-...` |
| `objectGUID` | Immutable identifier | `{GUID}` |
| `userAccountControl` | Bitmask of account flags | `512` (normal), `514` (disabled), `66048` (password never expires) |
| `pwdLastSet` | Date/time of last password change | Filetime |
| `badPwdCount` | Bad password attempts | Integer |
| `lastLogonTimestamp` | Approximate last logon | Filetime |
| `memberOf` | DN of groups the user belongs to | Multi-valued |
| `unicodePwd` | Password (for set operations) | Special (cleartext, only over LDAPS) |
| `dBCSPwd` | LM hash (legacy) | Binary |
| `ntPwdHistory` | NTLM password history | Binary |
| `supplementalCredentials` | Kerberos keys + wDigest | Binary |
| `adminCount` | Set to 1 if user is a privileged account | Integer |
| `servicePrincipalName` | SPNs registered for the account | `HTTP/webserver.corp.com` |
| `msDS-SupportedEncryptionTypes` | Bitmask of supported Kerberos enctypes | Integer |

### Computer attributes

| Attribute | Description | Example |
|-----------|-------------|---------|
| `sAMAccountName` | Computer name with `$` | `WS001$` |
| `operatingSystem` | OS name string | `Windows 10 Enterprise` |
| `operatingSystemVersion` | Version number | `10.0 (19041)` |
| `dNSHostName` | Full DNS hostname | `ws001.corp.com` |
| `userAccountControl` | Bitmask (including `WORKSTATION_TRUST_ACCOUNT`) | Integer |

### Group attributes

| Attribute | Description |
|-----------|-------------|
| `groupType` | Bitmask: `GLOBAL(2)`, `DOMAIN_LOCAL(4)`, `UNIVERSAL(8)`, `SECURITY(2147483648)` |
| `member` | Multi-valued DN list of members |
| `memberOf` | Parent groups |

## Common enumeration LDAP queries

### All enabled users
```
(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))
```

### Domain admins group members
```
(&(objectClass=group)(sAMAccountName=Domain Admins))
```
Then read the `member` attribute, or:
```
(&(objectClass=user)(memberOf=CN=Domain Admins,CN=Users,DC=corp,DC=com))
```

### Users with SPNs (Kerberoasting targets)
```
(&(objectCategory=person)(objectClass=user)(servicePrincipalName=*)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))
```

### Users without Kerberos pre-authentication (AS-REP roasting targets)
```
(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))
```

### All domain controllers
```
(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))
```

### Computers with operating system info
```
(&(objectCategory=computer)(operatingSystem=*))
```

### Find all GPOs in the domain
```
(objectCategory=groupPolicyContainer)
```

### All organizational units
```
(objectCategory=organizationalUnit)
```

### Users with old passwords (>90 days)
```
(&(objectCategory=person)(objectClass=user)(pwdLastSet<=131657760000000000))
```
(Convert days to filetime: 90 days = 7776000 seconds × 10000000 = 77760000000000 100-ns intervals)

### Accounts with constrained delegation
```
(&(objectCategory=computer)(msDS-AllowedToDelegateTo=*))
```

### Accounts with RBCD set
```
(&(objectCategory=computer)(msDS-AllowedToActOnBehalfOfOtherIdentity=*))
```

## LDAP injection

LDAP injection occurs when user input is incorporated into LDAP search filters without proper sanitization.

### Vulnerable example (web app)

```python
# VULNERABLE
filter = f"(sAMAccountName={username})"
results = ldap_search(base_dn, filter)
```

If username = `*)(samAccountName=*)(|(samAccountName=*`, the filter becomes:

```
(sAMAccountName=*)(samAccountName=*)(|(samAccountName=*)
```

This returns all users instead of just the target.

### Mitigations

- Whitelist allowed characters for input
- Use parameterized LDAP queries (SDK-provided helpers)
- Escape special characters: `* ( ) \ NUL /`
- Never concatenate user input directly into filters

## PowerShell and LDAP

### ADSI (Active Directory Service Interfaces)

```powershell
# Basic LDAP search using ADSI
$searcher = [ADSISearcher]"(&(objectCategory=user)(sAMAccountName=jsmith*))"
$searcher.PageSize = 1000
$results = $searcher.FindAll()
```

### AD module cmdlets

```powershell
# Using ActiveDirectory module
Get-ADUser -Filter 'Department -eq "IT"' -Properties Department, Title
Get-ADGroupMember -Identity "Domain Admins"
Get-ADComputer -Filter 'OperatingSystem -like "*Windows 10*"' -Properties OperatingSystem
```

### ADSI LDAP paths

```
LDAP://DC=corp,DC=example,DC=com                   (domain root)
LDAP://CN=Users,DC=corp,DC=example,DC=com          (Users container)
LDAP://GC://DC=corp,DC=example,DC=com              (Global Catalog)
LDAP://CN=Schema,CN=Configuration,DC=corp,DC=com   (Schema partition)
```

## LDAP over TLS vs LDAPS

| Aspect | LDAP + STARTTLS | LDAPS |
|--------|-----------------|-------|
| Port | Dynamic (uses 389) | 636 |
| Negotiation | STARTTLS extended operation after LDAP bind | TLS immediately on connection |
| Support | RFC 2830 | Pre-RFC (standardized as useLDAPS) |
| AD Support | Supported (Windows 2000+) | Supported |

## Ports used

| Port | Protocol | Purpose |
|------|----------|---------|
| 389/TCP, UDP | LDAP | Standard LDAP (including STARTTLS) |
| 636/TCP | LDAPS | LDAP over SSL |
| 3268/TCP | GC LDAP | Global Catalog non-SSL |
| 3269/TCP | GC LDAPS | Global Catalog SSL |
| 9389/TCP | ADWS | Active Directory Web Services (SOAP over HTTP) |

## How attackers abuse LDAP

| Attack | Description |
|--------|-------------|
| **LDAP enumeration** | Use unauthenticated or low-privileged LDAP queries to map the domain (users, groups, computers, trusts) |
| **LDAP injection** | Manipulate LDAP search filters in vulnerable applications to bypass auth or extract data |
| **AdminSDHolder abuse** | Modify the ACL on AdminSDHolder via LDAP to grant persistence on privileged accounts |
| **Attribute modification** | Modify `msDS-AllowedToActOnBehalfOfOtherIdentity` via LDAP to set up RBCD abuse |
| **Weak ACL discovery** | Query LDAP for objects with weak permissions (e.g., `GenericAll` for the "Authenticated Users" group) |
| **Password change via LDAP** | Change a user's password via `unicodePwd` attribute if the attacker has the necessary rights |
| **Directory scavenging** | Extract all `description` and `info` fields for passwords stored in clear text |
| **Shadow credentials** | Add `msDS-KeyCredentialLink` to a user/computer object via LDAP to create Kerberos PKINIT pre-auth keys |

## Defender recommendations

1. **Enable LDAP channel binding** — prevents LDAP relay attacks. Enforce via Group Policy: `Domain controller: LDAP server channel binding token requirements`.

2. **Enable LDAP signing** — prevents LDAP tampering. Set `Domain controller: LDAP server signing requirements` to `Require signing`.

3. **Restrict anonymous LDAP access** — configure `dsHeuristics` to block anonymous queries.

4. **Disable LDAP over unsigned/clear-text** — use LDAPS (636) only if possible.

5. **Audit LDAP queries** — monitor for unusual search patterns:
   - Event ID 4662: An operation was performed on an object
   - Event ID 5136: A directory service object was modified

6. **Sanitize all LDAP queries in applications** — guard against LDAP injection.

7. **Limit query size** — use paged results (1000 entries per page) instead of allowing massive result sets.

8. **Monitor for attribute modifications** — especially `msDS-AllowedToActOnBehalfOfOtherIdentity`, `msDS-KeyCredentialLink`, `adminCount`, and `nTSecurityDescriptor`.

9. **Enable extended protection on AD FS and web apps** using LDAP.

## Relevant RFCs and MS protocols

| Document | Description |
|----------|-------------|
| RFC 4511 | LDAPv3 Protocol |
| RFC 4512 | LDAP Directory Information Models |
| RFC 4513 | LDAP Authentication Methods and SASL |
| RFC 4514 | LDAP String Representation of Distinguished Names |
| RFC 4515 | LDAP String Representation of Search Filters |
| RFC 4516 | LDAP URL Format |
| RFC 4517 | LDAP Syntaxes and Matching Rules |
| RFC 2830 | LDAP Extension for Transport Layer Security (STARTTLS) |
| RFC 2696 | LDAP Paged Results Control |
| RFC 2891 | LDAP Server Side Sort Control |
| [MS-ADTS] | Active Directory Technical Specification |
| [MS-LDAP] | LDAP Protocol Extensions (Microsoft) |
| [MS-ADSC] | Active Directory Schema Classes and Attributes |
