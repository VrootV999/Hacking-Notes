# AD CS Attack Surface Overview

## What is AD CS?

Active Directory Certificate Services (AD CS) is Microsoft's PKI implementation that issues, manages, and validates certificates in an Active Directory environment. It enables domain-joined machines to enroll for certificates used for authentication (smartcards, VPN, 802.1x, SSL/TLS), code signing, encryption, and more.

AD CS is **not installed by default** but is widely deployed in enterprise environments.

## Why AD CS is a Prime Attack Target

Certificates are **trusted** — a certificate issued by an enterprise CA is trusted by every domain-joined machine. If an attacker can abuse AD CS to:
- Issue a certificate for a privileged user (e.g. Domain Admin)
- Request a certificate with improper validation
- Relay NTLM to the certificate enrollment endpoint

...they can authenticate as that user using PKINIT (Kerberos authentication via证书), bypassing password requirements, MFA (in some cases), and often avoiding detection.

## Attack Flow Summary

```
1. ENUMERATE AD CS        → certipy find, Certify.exe, BloodHound
2. IDENTIFY VULNERABILITY  → ESC1–ESC13, misconfigured templates, CA ACLs
3. EXPLOIT                → Request/generate certificate for privileged user
4. AUTHENTICATE           → Use PKINIT with certificate (certipy auth, kekeo)
5. ESCALATE / PERSIST     → DCSync, lateral movement, golden certificate
```

## ESC Vulnerability Reference Table

| ESC # | Name | Root Cause | Difficulty | Fix |
|-------|------|-----------|------------|-----|
| **ESC1** | SAN Misconfiguration | CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT + Manager Approval OFF + Authorized Signatures N/A | Low | Disable enrollee-supplies-subject or enable Manager Approval |
| **ESC2** | Any Purpose EKU | Certificate template has "Any Purpose" EKU (2.5.29.37.0) or no EKU | Low | Remove Any Purpose EKU, restrict EKU list |
| **ESC3** | Enrollment Agent | Template allows enrollment agent (Certificate Request Agent EKU) on behalf of others | Low | Restrict who can enroll for enrollment agent templates |
| **ESC4** | Template ACL Abuse | Low-privilege user has Write access to certificate template | Medium | Audit template ACLs, remove excessive Write/Full Control |
| **ESC5** | PKI Object ACL Abuse | Weak ACLs on the CA server's AD object or container | Medium | Harden ACLs on PKI-related AD objects |
| **ESC6** | EDITF_ATTRIBUTESUBJECTALTNAME2 | CA has `EDITF_ATTRIBUTESUBJECTALTNAME2` flag set — allows SAN specification via Subject Attributes | Low | Disable the flag on CA |
| **ESC7** | CA ACL Abuse | Low-privilege user has ManageCA or ManageCertificates rights on CA | Medium | Remove excessive CA ACL privileges |
| **ESC8** | NTLM Relay to HTTP Enrollment | AD CS Web Enrollment endpoint accepts NTLM auth, allowing relay from SMB | Low | Disable NTLM on CA, enable HTTPS, use Extended Protection for Authentication |
| **ESC9** | No Security Extension | Weak issuance policies — No Security Extension in certificate template | Medium | Enable Security Extension in templates |
| **ESC10** | Weak StrongCertificateBindingEnforcement | Registry `StrongCertificateBindingEnforcement` = 0 (disabled) or 1 (audit only) | Medium | Set to 2 (enforce) on domain controllers |
| **ESC11** | NTLM Relay to ICERTPASS | ICERTPASS RPC interface allows NTLM relay to certificate enrollment | Low | Enable EPA on CA, restrict NTLM |
| **ESC12** | CA Properties NDC Security | Attacker with Write access to CA's AD object can modify `ndC` attributes for persistence | High | Harden CA object ACL |
| **ESC13** | OID Group Link Abuse | Certificate template linked to security group via OID — gaining cert gives group membership | Medium | Audit OID-to-group mappings |

## Prerequisites for Attack

- Domain credentials (user account, computer account, or NTLM hash)
- Network connectivity to the CA server or Domain Controller
- Certipy (Linux) or Certify / ForgeCert (Windows)
- For ESC8: ability to trigger NTLM auth from victim to attacker (mitm6, responder, dropbox)

## Tools

| Tool | Platform | Purpose |
|------|----------|---------|
| [Certipy](https://github.com/ly4k/Certipy) | Linux | Enumeration, exploitation, authentication (the primary tool) |
| [Certify](https://github.com/GhostPack/Certify) | Windows | Enumeration + exploitation from Windows hosts |
| [ForgeCert](https://github.com/GhostPack/ForgeCert) | Windows | Forge certificates from existing CA certificates |
| [Kekeo](https://github.com/gentilkiwi/kekeo) | Windows | PKINIT authentication with certificates |
| [Rubeus](https://github.com/GhostPack/Rubeus) | Windows | PKINIT + Kerberos ticket requests with certificates |
| [Impacket ntlmrelayx](https://github.com/fortra/impacket) | Linux | NTLM relaying for ESC8, ESC11 |
| [BloodHound](https://github.com/BloodHoundAD/BloodHound) | Linux/Win | AD CS attack path mapping (v4+) |

## Technique Files

| # | File | Description |
|---|------|-------------|
| 01 | [Certipy Enumeration](01_Certipy_Enumeration.md) | AD CS enumeration with Certipy |
| 02 | [ESC1 / ESC2 / ESC3](02_ESC1_ESC2_ESC3.md) | SAN misconfiguration, Any Purpose EKU, Enrollment Agent |
| 03 | [ESC4 / ESC5 / ESC6](03_ESC4_ESC5_ESC6.md) | Template ACL, PKI object ACL, EDITF_ATTRIBUTESUBJECTALTNAME2 |
| 04 | [ESC7 / ESC8](04_ESC7_ESC8.md) | CA ACL abuse, NTLM relay to HTTP enrollment |
| 05 | [ESC9 / ESC10 / ESC11](05_ESC9_ESC10_ESC11.md) | No Security Extension, weak binding, NTLM relay to ICERTPASS |
| 06 | [ESC12 / ESC13](06_ESC12_ESC13.md) | CA ndC properties, OID group link abuse |
| 07 | [Certify / ForgeCert](07_Certify_ForgeCert.md) | Windows-based AD CS exploitation toolkit |
| 08 | [ESC8 + PetitPotam → krbtgt](08_ESC8_PetitPotam_krbtgt.md) | AD CS relay + PetitPotam to capture krbtgt hash |
