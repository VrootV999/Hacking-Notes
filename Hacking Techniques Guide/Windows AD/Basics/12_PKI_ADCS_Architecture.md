# PKI / Active Directory Certificate Services (AD CS)

## What it is

Active Directory Certificate Services (AD CS) is Microsoft's Public Key Infrastructure (PKI) implementation for Windows. It provides:

- Certificate issuance and management
- Certificate lifecycle management (enrollment, renewal, revocation)
- Smart card and virtual smart card authentication
- Secure email (S/MIME)
- Code signing
- IPsec authentication
- Network Policy Server (NPS) / RADIUS authentication
- SSL/TLS certificates for internal services
- **Kerberos PKINIT** — certificate-based Kerberos authentication

## CA hierarchy

### CA types

| CA Type | Description |
|---------|-------------|
| **Root CA** | Top of the CA hierarchy; self-signed; offline (disconnected from network) in best practice; issues only subordinate CA certificates |
| **Issuing CA** | (Subordinate CA) Issues end-entity certificates; online; can be enterprise or standalone |
| **Enterprise CA** | Integrated with AD; auto-enrollment supported; certificate templates used; certificate auto-published to AD |
| **Standalone CA** | Not AD-integrated; manual enrollment; no certificate templates; no auto-enrollment |

### Recommended hierarchy

```
                    +----------+
                    | Root CA  |  (Offline, self-signed, air-gapped)
                    +----------+
                         |
                    Issues CA cert
                         |
                    +----------+
                    | Issuing  |  (Online, AD-integrated, issues all end-user certs)
                    | CA       |
                    +----------+
                    /    |    \
                   /     |     \
          Web Servers  Users  Computers
```

### Enterprise CA architecture

An Enterprise CA publishes its information to Active Directory:

```
CN=<CA-Name>, CN=Certification Authorities, CN=Public Key Services,
  CN=Services, CN=Configuration, DC=corp, DC=example, DC=com
```

It also creates:
- **NTAuthCertificates** — trusted root certification authorities object in AD
- **AIA (Authority Information Access)** — location of CA certificate and CRL
- **CDP (CRL Distribution Point)** — location of certificate revocation lists

## Certificate templates

Certificate templates define the properties and issuance policies for certificates. They are stored in AD:

```
CN=Certificate Templates, CN=Public Key Services, CN=Services,
  CN=Configuration, DC=corp, DC=example, DC=com
```

### Template properties

| Property | Description |
|----------|-------------|
| **Template Name** | Display name (e.g., "Web Server", "User") |
| **Template Schema Version** | 1 (Windows 2000), 2 (Windows 2003+), 3 (Windows 2008 R2+) |
| **pKIExtendedKeyUsage** | EKU (Extended Key Usage) OIDs — what the cert is valid for |
| **msPKI-Certificate-Name-Flag** | How the subject name is built (from AD attributes) |
| **msPKI-Enrollment-Flag** | Enrollment behavior flags |
| **msPKI-RA-Signature** | Number of required CA manager signatures |
| **Security Descriptor** | Who can read, enroll, auto-enroll on this template |
| **Validity Period** | How long issued certificates are valid |
| **Renewal Period** | How long before expiry renewal is allowed |
| **Key Size** | RSA key length (1024, 2048, 4096) |

### Key template schema attributes

#### pKIExtendedKeyUsage (EKU)

| EKU OID | Purpose |
|---------|---------|
| `1.3.6.1.5.5.7.3.1` | Server Authentication |
| `1.3.6.1.5.5.7.3.2` | Client Authentication |
| `1.3.6.1.5.5.7.3.3` | Code Signing |
| `1.3.6.1.5.5.7.3.4` | Secure Email |
| `1.3.6.1.5.5.7.3.9` | Smart Card Logon |
| `1.3.6.1.4.1.311.10.3.1` | Certificate Trust List |
| `1.3.6.1.4.1.311.10.3.4` | Encrypting File System |
| `1.3.6.1.4.1.311.20.2.2` | Smart Card Logon / PKINIT |
| `1.3.6.1.4.1.311.21.5` | KDC Authentication (Kerberos) |
| `1.3.6.1.4.1.311.61.4.1` | Certificate Request Agent (for enrollment agents) |
| `2.5.29.37.0` | **Any Purpose** (allows any usage — dangerous) |
| (none) | **All purposes** (same as Any Purpose) |

#### msPKI-Certificate-Name-Flag

| Flag | Value | Description |
|------|-------|-------------|
| CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT | 1 | **Attacker's favorite** — the requester supplies the subject name |
| CT_FLAG_SUBJECT_ALT_REQUIRE_UPN | 0x100000 | Require UPN in SAN |
| CT_FLAG_SUBJECT_ALT_REQUIRE_EMAIL | 0x200000 | Require email in SAN |
| CT_FLAG_SUBJECT_ALT_REQUIRE_DNS | 0x400000 | Require DNS in SAN |
| CT_FLAG_SUBJECT_ALT_REQUIRE_DIRECTORY_GUID | 0x1000000 | Require directory GUID in SAN |

**CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT** is the most dangerous flag — it allows the requester to specify **any** subject name, enabling domain escalation.

#### msPKI-Enrollment-Flag

| Flag | Value | Description |
|------|-------|-------------|
| CT_FLAG_INCLUDE_SYMMETRIC_ALGORITHMS | 0x1 | Include symmetric algorithms |
| CT_FLAG_PUBLISH_TO_DS | 0x2 | Publish certificate to AD |
| CT_FLAG_PUBLISH_TO_FRS | 0x4 | Publish to file replication |
| CT_FLAG_INCLUDE_SYMMETRIC_ALGORITHMS | 0x8 | Include symmetric algorithms |
| CT_FLAG_NO_DIRECTORY_SD_ACL | 0x20 | No security descriptor in directory |
| CT_FLAG_ADD_EMAIL | 0x2000 | Add email to certificate |
| CT_FLAG_AUTO_ENROLLMENT_CHECK_USER_DS_CERTIFICATE | 0x40 | Check user DS cert |
| CT_FLAG_PREVIOUS_APPROVAL_VALIDATE_REENROLLMENT | 0x80 | Validate reenrollment |

## Certificate enrollment

### Enrollment methods

| Method | Description |
|--------|-------------|
| **Auto-enrollment** | Domain-joined users/computers automatically enroll for certificates (GPO-configured). Only Enterprise CA |
| **Manual (Certificates MMC)** | User requests a certificate via `certlm.msc` or `certmgr.msc` |
| **Web Enrollment** | Web-based enrollment via `http://<CA>/certsrv` |
| **CEP/CES** | Certificate Enrollment Policy / Certificate Enrollment Service (Windows Server 2012+) |
| **NDES** | Network Device Enrollment Service (SCEP) for non-Windows devices |
| **PowerShell** | `Get-Certificate`, `New-SelfSignedCertificate` cmdlets |
| **certreq** | Command-line certificate request tool |

### Web Enrollment flow

```
Client                                      CA Server
  │                                            │
  │  1. HTTP GET /certsrv                      │
  │  ←───────── Logon page ────────────────── │
  │                                            │
  │  2. Authenticates (Kerberos/NTLM)          │
  │  ──────────────────────────────────────→  │
  │                                            │
  │  3. Request certificate via web form       │
  │     (selects template, provides subject)   │
  │  ──────────────────────────────────────→  │
  │                                            │
  │  4. CA checks permissions on template      │
  │     Generates certificate                  │
  │  ←───────── Certificate issued ─────────── │
  │                                            │
```

### CEP/CES flow (Windows 2012+)

```
1. Client contacts CEP service to get certificate enrollment policy
   (HTTPS to https://<server>/PolicyService)
2. CEP returns available templates and enrollment requirements
3. Client contacts CES service to enroll
   (HTTPS to https://<server>/CertificateService)
4. CES validates, contacts CA, returns issued certificate
```

## Certificate revocation

### CRL (Certificate Revocation List)

- Published by CA at regular intervals
- Contains serial numbers of revoked certificates
- Distributed via CDP (CRL Distribution Point) URLs in issued certificates
- **Base CRL** — full list; **Delta CRL** — only changes since last base CRL

### CRL path

Certificates contain CDP extensions:

```
CDP Extension:
  [1]CRL Distribution Point
       Distribution Point Name:
            Full Name:
                 URL=http://pki.corp.com/CertData/CRL/CORP-CA.crl
                 URL=ldap:///CN=CORP-CA,CN=CA,CN=CDP,...?certificateRevocationList
```

### OCSP (Online Certificate Status Protocol)

- Real-time certificate status check
- More current than CRLs
- Responder must be online
- AD CS includes the Online Responder role

```
Client → OCSP Responder → "Is this certificate valid?"
OCSP Responder → Client → "Good / Revoked / Unknown"
```

## Certificate trust

### Trust hierarchy

```
Root CA Certificate
  (in Trusted Root Certification Authorities store)
       |
Intermediate CA Certificate
  (in Intermediate Certification Authorities store)
       |
End-Entity Certificate
  (the actual certificate used by the client/service)
```

### NTAuthCertificates

The `NTAuthCertificates` AD object tells the Kerberos KDC which CAs are trusted to issue authentication certificates:

```
CN=NTAuthCertificates, CN=Public Key Services, CN=Services,
  CN=Configuration, DC=corp, DC=example, DC=com
```

If a CA issues a certificate for "Smart Card Logon" or "Client Authentication" EKU, and the CA is listed in NTAuthCertificates, that certificate can be used for domain authentication (PKINIT).

## AD CS attack surface

AD CS is one of the **most dangerous attack surfaces** in Active Directory. The research by SpecterOps (Will Schroeder, Lee Christensen — "Certified Pre-Owned", 2021) identified multiple escalation paths.

### ESC1 — Misconfigured Template (Enrollee Supplies Subject)

**Requirements:**
1. Template allows enrollee to supply subject name (`CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`)
2. Template grants `Enroll` to a low-privileged group
3. Template has either:
   - No EKU (`Any Purpose`), OR
   - `Client Authentication` + `Smart Card Logon` EKU (allows domain auth)
4. CA is trusted for NT Authentication (in NTAuthCertificates)

**Attack:**
```bash
# Request a certificate as Domain Admin
certipy req -u jsmith@corp.com -p password -ca CORP-CA \
    -template "VulnTemplate" -upn administrator@corp.com

# Use certificate for Kerberos PKINIT authentication
certipy auth -pfx administrator.pfx -dc-ip 10.10.10.10
```

### ESC2 — Misconfigured Template (Any Purpose EKU)

**Requirements:**
1. Template has **Any Purpose** EKU (or no EKU)
2. Enroll permission for attacker
3. CA trusted for NT Authentication

**Attack:** Certificate can be used for any purpose, including client authentication.

### ESC3 — Enrollment Agent Certificate Abuse

**Requirements:**
1. Template has **Certificate Request Agent** EKU (`1.3.6.1.4.1.311.61.4.1`)
2. Another template allows enrollment on behalf of others
3. Enroll permission for attacker

**Attack:** Request a certificate as any user on behalf of the certificate agent.

### ESC4 — Template ACL Misconfiguration

**Requirements:**
1. Attacker has `Write` privileges on a certificate template
2. Attacker modifies the template to enable `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT`

**Attack:** Change the template's security descriptor, modify the flags, then enroll with any subject name.

### ESC5 — CA ACL Misconfiguration

**Requirements:**
1. Attacker has `Write` or `ManageCA` privileges on the CA object

**Attack:** Modify CA settings, grant enrollment rights, or modify NTAuthCertificates.

### ESC6 — CAEDITF_EDITF_ATTRIBUTESUBJECTALTNAME2

**Requirements:**
1. CA has `EDITF_ATTRIBUTESUBJECTALTNAME2` flag set
2. Enroll permission on any template

**Attack:** Specify SAN in certificate request attributes, allowing domain authentication.

```bash
# Check if CA has vulnerable flag
certipy find -u jsmith@corp.com -p password -dc-ip 10.10.10.10
```

### ESC7 — CA Manager Approval + CA Manager Rights

**Requirements:**
1. Template requires CA Manager Approval
2. Attacker has `ManageCA` or `Issue and Manage Certificates` rights

**Attack:**
1. Request certificate → pending approval
2. As CA manager, approve the pending request

### ESC8 — NTLM Relay to AD CS Web Enrollment

**Requirements:**
1. Web Enrollment enabled (Web Service — `/certsrv`)
2. HTTP enabled (not HTTPS, or certificate errors ignored)
3. Attacker can capture NTLM auth and relay to the CA

**Attack:**
```bash
# Relay NTLM to AD CS Web Enrollment
ntlmrelayx.py -t http://CA01.corp.com/certsrv/certfnsh.asp \
    -smb2support --adcs --template DomainController

# Start Responder to capture NTLM
python Responder.py -I eth0
```

When a client authenticates to the attacker's fake SMB server, the NTLM hash is relayed to the CA web enrollment to request a certificate as that client.

### ESC9 — No Security Extension (NTAuthCertificates bypass)

If the `msPKI-Enrollment-Flag` has `CT_FLAG_NO_DIRECTORY_SD_ACL`, the CA doesn't check AD security descriptors for the certificate.

### ESC10 — Weak certificate chain

**Requirements:**
1. Weak CA certificate key (e.g., SHA1, short RSA key)
2. Weak cross-signing certificates

### ESC11 — NTLM Relay to CEP/CES

Same as ESC8 but targeting CEP/CES (Kerberos-based enrollment policy).

## How attackers abuse AD CS

| Attack | ESC # | Description |
|--------|-------|-------------|
| **Certified Pre-Owned** | ESC1-8 | Multiple paths to escalate from domain user to Domain Admin via PKI misconfigurations |
| **Golden Certificate** | N/A | Forge a certificate using the CA's private key (analogous to Golden Ticket) |
| **CA compromise** | N/A | Steal CA private key from the CA server (file system or HSM) |
| **DPAPI backup key theft** | N/A | AD CS stores DPAPI backup keys that can decrypt domain user secrets |
| **Certificate private key theft** | N/A | Extract private keys from machines (DPAPI-protected, or from LSASS) |
| **PKINIT abuse** | N/A | Use stolen certificates for Kerberos authentication (no password needed) |
| **Shadow Credentials** | N/A | Add `msDS-KeyCredentialLink` to user/computer for PKINIT authentication |
| **Theft of machine certificate** | N/A | Machine certificate can authenticate as the computer account |
| **Web Enrollment CSRF** | N/A | Cross-site request forgery on `/certsrv` to make privileged users enroll certificates |

## Defender recommendations

1. **Audit certificate templates** — regularly review all templates for dangerous configurations:
   - `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` should not be combined with `Client Authentication` EKU
   - No template should have `Any Purpose` EKU unless absolutely required
   - Restrict enrollment permissions to only those who need certificates

2. **Disable Web Enrollment** if not needed — or enforce HTTPS with strong certificates.

3. **Enable CA auditing:**
   - Event ID 4886: Certificate issued
   - Event ID 4887: Certificate approval
   - Event ID 4888: Certificate revocation
   - Event ID 4898: Certificate template loaded

4. **Use certipy for auditing:**
   ```bash
   certipy find -u auditor@corp.com -p password -dc-ip 10.10.10.10 -stdout
   ```

5. **Restrict CA access** — only authorized administrators should have `ManageCA` and `Issue and Manage Certificates` rights.

6. **Secure the CA server** — it is the most sensitive server in the domain:
   - Dedicated server, not a DC
   - Enforce Credential Guard
   - Use HSM for CA key protection
   - Enable Windows Defender Firewall
   - Block internet access

7. **Use Key Based Renewal** — prevents renewal of stolen certificates.

8. **Enable certificate revocation** — ensure CRLs and OCSP are available and trusted by all clients.

9. **Set appropriate certificate lifetimes** — shorter is better (e.g., 1-2 years for user certs).

10. **Monitor for anomalous certificate requests** — especially for sensitive templates (Domain Controller, Enrollment Agent).

11. **Use modern cryptography** — RSA 2048+ keys, SHA256+ signatures. Disable SHA1.

12. **Implement certificate pinning/pinning** for critical services.

## Relevant RFCs and MS protocols

| Document | Description |
|----------|-------------|
| RFC 5280 | Internet X.509 PKI Certificate and CRL Profile |
| RFC 6960 | Online Certificate Status Protocol (OCSP) |
| RFC 4210 | CMP (Certificate Management Protocol) |
| RFC 3647 | PKI Certificate Policy/Certification Practices Framework |
| [MS-CERT] | Certificate Services Protocol |
| [MS-CCE] | Certificate Services: Client Extensions |
| [MS-WCCE] | Windows Client Certificate Enrollment Protocol |
| [MS-XCEP] | Certificate Enrollment Policy Protocol |
| [MS-XCEP] | X.509 Certificate Enrollment Policy Protocol |
| [MS-CMP] | Certificate Management Protocol (Microsoft) |
| "Certified Pre-Owned" | SpecterOps whitepaper on AD CS abuse |

## Key tools

| Tool | Purpose |
|------|---------|
| **certipy** | Python tool for AD CS enumeration and exploitation |
| **Certify** | .NET tool for AD CS enumeration (part of GhostPack) |
| **PSPKI** | PowerShell module for PKI management |
| **PKIView** | Microsoft tool to view CA configuration |
| **certutil** | Built-in CA management tool |
| **ForgeCert** | Tool to forge certificates from CA key |
| **Coercer** | Tool to coerce authentication (useful for ESC8 relay) |
