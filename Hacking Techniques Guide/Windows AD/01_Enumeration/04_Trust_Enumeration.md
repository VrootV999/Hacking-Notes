# Trust Enumeration

## Overview

Domain and forest trusts define authentication boundaries. Attackers can abuse trust relationships to move laterally across domains/forests, perform SID history abuse (extraSID), cross-kerberos attacks, and trust ticket (TGT) delegation attacks. Understanding trust direction, type, transitivity, and SID filtering is critical for escalation.

## Trust Types

| Trust Type | Description | Attack Potential |
|------------|-------------|------------------|
| Parent-Child | Automatically created between parent and child domains | SID History abuse, Kerberos across domains |
| Tree-Root | Between domains in same forest | Same as parent-child |
| Forest | Between two forests (transitive or non-transitive) | Forest-to-forest escalation, SID history |
| External | Between AD domain and non-AD realm or external AD domain | Usually less dangerous |
| Realm | Between AD and non-Windows Kerberos realm | Limited |
| Shortcut | Manually created to optimize trust path | Same as parent-child |

## Trust Direction

| Direction | Meaning | Attack Path |
|-----------|---------|-------------|
| Outbound | This domain trusts the target domain | Trust tickets flow from target to this domain |
| Inbound | Target domain trusts this domain | Can attempt to use this domain's resources from target |
| Bidirectional | Mutual trust | Full cross-authentication |
| Disabled | Trust exists but not active | No crossing possible |

## PowerView Trust Enumeration

### Domain Trusts

```powershell
# All domain trusts
Get-DomainTrust
Get-NetDomainTrust

# Trusts for specific domain
Get-DomainTrust -Domain domain.local

# Trusts with all properties
Get-DomainTrust | Select SourceName, TargetName, TrustType, TrustDirection, TrustAttributes, TrustTransitive, sid

# Filter by trust type
Get-DomainTrust | Where-Object {$_.TrustType -eq "ParentChild"}
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"}
Get-DomainTrust | Where-Object {$_.TrustType -eq "External"}

# Filter by direction
Get-DomainTrust | Where-Object {$_.TrustDirection -eq "Bidirectional"}
Get-DomainTrust | Where-Object {$_.TrustDirection -eq "Outbound"}
Get-DomainTrust | Where-Object {$_.TrustDirection -eq "Inbound"}

# Check SID filtering status
Get-DomainTrust | Select SourceName, TargetName, TrustAttributes

# TrustAttributes values:
#   0x00000001 = Non-transitive
#   0x00000002 = Uplevel only
#   0x00000004 = Quarantined domain (SID filtering enabled)
#   0x00000008 = Forest trust
#   0x00000010 = Cross-org
#   0x00000020 = Intra-org
#   0x00000040 = Inter-org (external)
#   0x00000400 = SID filtering disabled (vulnerable!)
```

### Forest Trusts

```powershell
# Get forest trusts
Get-ForestTrust
Get-ForestTrust -Forest domain.local

# Forest trust details
Get-ForestTrust | Format-List *

# Forest trust with all properties
Get-ForestTrust | Select SourceName, TargetName, TrustType, TrustAttributes, TrustDirection

# Forest trust status
Get-ForestTrust | ForEach-Object {
    [PSCustomObject]@{
        Source = $_.SourceName
        Target = $_.TargetName
        Type = $_.TrustType
        Direction = $_.TrustDirection
        Transitive = if ($_.TrustAttributes -band 0x20) {"Intra-org"} else {"Inter-org"}
        SIDFiltering = if ($_.TrustAttributes -band 0x4) {"Enabled"} else {"Disabled"}
    }
}
```

### Trust Mapping

```powershell
# Map all domain trusts recursively
Get-DomainTrust -API | ForEach-Object {
    $source = $_.SourceName
    $target = $_.TargetName
    Write-Host "$source -> $target ($($_.TrustDirection))"
    # Recursively enumerate child trusts
    try {
        Get-DomainTrust -Domain $target -API -ErrorAction Stop | ForEach-Object {
            Write-Host "  -> $_($_.TargetName) ($($_.TrustDirection))"
        }
    } catch {}
}

# Find all reachable domains
$domains = @()
$domains += (Get-Domain).Name
Get-DomainTrust | ForEach-Object {
    $domains += $_.TargetName
}
$domains = $domains | Select -Unique
Write-Host "Reachable domains:"
$domains
```

### Trust Users & Groups

```powershell
# Find users from external/trusted domains
Get-DomainUser -LDAPFilter "(objectSid=*)"
Get-DomainForeignUser
Get-NetForeignUser

# Find groups with members from other domains
Get-DomainForeignGroupMember
Get-NetForeignGroupMember

# Find foreign group members with resolved names
Get-DomainForeignGroupMember -Domain domain.local | Select GroupName, MemberName, MemberDistinguishedName

# Find groups that contain foreign security principals
Get-DomainGroup -LDAPFilter "(|(member=S-1-*)(member=CN=ForeignSecurityPrincipals*))"

# Foreign security principals
Get-DomainObject -LDAPFilter "(objectClass=foreignSecurityPrincipal)" | Select cn, objectSid

# Resolve foreign SIDs
Get-DomainObject -LDAPFilter "(objectClass=foreignSecurityPrincipal)" | ForEach-Object {
    $obj = $_
    $sid = $_.cn
    try {
        $resolved = ConvertFrom-SID $sid
        [PSCustomObject]@{
            SID = $sid
            ResolvedName = $resolved
            DistinguishedName = $_.DistinguishedName
        }
    } catch {
        [PSCustomObject]@{
            SID = $sid
            ResolvedName = "UNRESOLVED"
            DistinguishedName = $_.DistinguishedName
        }
    }
}
```

## AD Module Trust Enumeration

```powershell
# Get all domain trusts
Get-ADTrust -Filter *

# Filter by type
Get-ADTrust -Filter "TrustType -eq 'ParentChild'"
Get-ADTrust -Filter "TrustType -eq 'Forest'"
Get-ADTrust -Filter "TrustType -eq 'External'"

# Specific trust details
Get-ADTrust -Identity "target.domain.local"
Get-ADTrust -Identity domain.local

# Trust properties
Get-ADTrust -Filter * | Format-List Name, Target, TrustType, TrustDirection, TrustAttributes, SIDFilteringForestAware, Intrasite, IsTreeParent, IsTreeRoot

# Get forest info
Get-ADForest
Get-ADForest | Select Domains, UPNSuffixes, SPNSuffixes

# List all domains in forest
(Get-ADForest).Domains

# Forest trust enumeration
Get-ADTrust -Filter "TrustType -eq 'Forest'"
```

## NetExec Trust Enumeration

```bash
# Trust enumeration via LDAP
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o TRUST=1

# Domain trust enumeration module
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o TRUST_ALL=1

# SMB-based trust info
nxc smb <dc-ip> -u 'user' -p 'pass' -M trust_enum

# Find domains in same forest
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o DOMAIN_LIST=1
```

## netdom (Windows Native)

```cmd
# List all trusts (from cmd)
netdom query trust
netdom query /domain:domain.local trust

# Query domain controller for trusts
netdom query /d:domain.local dc

# Specific trust query
netdom trust domain.local /d:target.local /verbose

# Verify trust health
netdom verify domain.local /d:target.local

# Reset trust
netdom reset domain.local /d:target.local

# Show trust relationship details
netdom trust domain.local /d:target.local /show
```

## nltest (Windows Native)

```cmd
# List all domain trusts
nltest /domain_trusts

# Detailed trust list
nltest /domain_trusts /all_trusts

# List DCs in domain
nltest /dclist:domain.local

# Query trust with specific domain
nltest /dsgetdc:target.domain.local

# List trusted domains
nltest /trusted_domains

# Forest trust info
nltest /dsgetforestinfo
```

## Active Directory Domains and Trusts (GUI)

```
1. Open "Active Directory Domains and Trusts" MMC
2. Right-click domain name -> Properties
3. Click "Trusts" tab
4. View "Domains trusted by this domain" and "Domains that trust this domain"
5. Select each trust -> Properties -> Validate trust status
```

## SID History / SID Filtering Enumeration

### PowerView

```powershell
# Find users with sidHistory
Get-DomainUser -LDAPFilter "(sidHistory=*)"
Get-DomainUser -LDAPFilter "(sidHistory=*)" | Select samaccountname, sidhistory, memberof

# Check if SID filtering is disabled on a trust
Get-DomainTrust | Select SourceName, TargetName, @{N='SIDFiltering';E={if($_.TrustAttributes -band 0x4){"Enabled"}else{"Disabled"}}}

# Trusts without SID filtering (vulnerable)
Get-DomainTrust | Where-Object {!($_.TrustAttributes -band 0x4)}

# Find ForeignSecurityPrincipal objects
Get-DomainObject -LDAPFilter "(objectClass=foreignSecurityPrincipal)" | Select @{N='ForeignSID';E={$_.cn}}

# SID history for extraSID attack
# First, get child domain SID
$childSID = (Get-Domain -Domain child.domain.local).DomainSID

# Get enterprise admin group SID
$enterpriseAdminSID = (Get-DomainGroup -Identity "Enterprise Admins" -Domain root.domain.local).objectsid

# SID history inclusion check (pre-attack)
# From child: golden ticket with extra SID
```

### AD Module

```powershell
# SID history accounts
Get-ADUser -LDAPFilter "(sidHistory=*)"
Get-ADUser -LDAPFilter "(sidHistory=*)" -Properties sidHistory, samaccountname

# SID filtering status via AD module
Get-ADTrust -Filter * | Select Name, Target, SIDFilteringForestAware
```

## Trust Key Enumeration

### PowerView

```powershell
# Dump trust keys (requires Domain Admin or equivalent)
Get-DomainTrust | ForEach-Object {
    $trust = $_
    Write-Host "[*] Trust: $($trust.SourceName) -> $($trust.TargetName)"
    Write-Host "    Direction: $($trust.TrustDirection)"
    Write-Host "    Type: $($trust.TrustType)"
    Write-Host "    Transitive: $($trust.TrustTransitive)"
}
```

### ntdsutil (Trust Keys - for inter-realm TGT forging)

```cmd
# Requires NTDS.dit access + SYSTEM/SYSTEM hives
ntdsutil "ac i ntds" "list trusts" q q
```

### Mimikatz Trust Key Extraction

```cmd
# Extract trust keys (requires DA)
mimikatz # lsadump::trust /patch
mimikatz # lsadump::domain /trust

# Extract trust auth info for specific trust
mimikatz # lsadump::lsa /patch /id:1
```

## ExtraSID / SIDHistory Abuse Recon

### Pre-requisites Enumeration

```powershell
# Check if target domain has SID filtering disabled on trust to parent
Get-DomainTrust -Domain child.domain.local | Where-Object {$_.TargetName -eq "domain.local"} | fl

# Find Enterprise Admins SID
$eaSID = (Get-DomainGroup -Identity "Enterprise Admins" -Domain root.domain.local).objectsid
Write-Host "Enterprise Admins SID: $eaSID"

# Find all domains in forest
Get-DomainTrust | Select TargetName | Sort -Unique

# Check if child domain can authenticate to parent
nxc smb <root-dc> -u 'child\user' -p 'pass' --shares
```

## Cross-Forest Attacks Enumeration

### SIDHistory Across Forests

```powershell
# Find users from other forests
Get-DomainForeignUser
Get-DomainForeignUser -Domain domain.local

# Find groups from other forests in domain groups
Get-DomainForeignGroupMember

# Check for forest trust bindings
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"}

# SID filtering on forest trusts (usually enabled for inter-org)
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"} | Select TargetName, @{N='SIDFiltering';E={if($_.TrustAttributes -band 0x4){"Enabled"}else{"Disabled"}}}
```

## Trust Enumeration via LDAP

```powershell
# LDAP query for trusted domain objects
Get-DomainObject -LDAPFilter "(objectClass=trustedDomain)" | Select name, trustDirection, trustType, trustAttributes, flatName, securityIdentifier

# LDAP filter for inter-domain trust objects
ldapsearch -x -H ldap://<dc-ip> -D "<user>@<domain>" -w '<pass>' -b "CN=System,DC=domain,DC=local" "(objectClass=trustedDomain)"

# All domain trust objects
Get-DomainObject -LDAPFilter "(objectClass=trustedDomain)" | Format-List *
```

## NetExec Cross-Domain Checks

```bash
# Test credentials across domains
nxc smb <target-dc> -u 'domain\user' -p 'pass' --shares

# LDAP recon on another domain in forest
nxc ldap <target-dc> -u 'domain\user' -p 'pass' --users

# Check if cross-domain authentication is possible
nxc smb <target-dc> -u 'currentdomain\user' -p 'pass'

# MSP / Managed Services cross-forest
nxc smb <target-dc> -u 'currentdomain\user' -p 'pass' -d 'target.domain.local'
```

## Trust Abuse Recon Summary

```powershell
# Full trust enum script
$domainDN = (Get-Domain).DistinguishedName
$report = @()

# 1. Get all trusts
Write-Host "[*] Enumerating trusts..."
Get-DomainTrust | ForEach-Object {
    $report += [PSCustomObject]@{
        Category = "Trust"
        Source = $_.SourceName
        Target = $_.TargetName
        Direction = $_.TrustDirection
        Type = $_.TrustType
        Transitive = $_.TrustTransitive
        SIDFiltering = if ($_.TrustAttributes -band 0x4) {"Disabled (VULN)"} else {"Enabled"}
    }
}

# 2. Foreign users
Write-Host "[*] Checking foreign users..."
Get-DomainForeignUser | ForEach-Object {
    $report += [PSCustomObject]@{
        Category = "ForeignUser"
        Source = ""
        Target = $_.MemberName
        Direction = ""
        Type = ""
        Transitive = ""
        SIDFiltering = ""
    }
}

# 3. Foreign group members
Write-Host "[*] Checking foreign group members..."
Get-DomainForeignGroupMember | ForEach-Object {
    $report += [PSCustomObject]@{
        Category = "ForeignGroupMember"
        Source = $_.GroupName
        Target = $_.MemberName
        Direction = ""
        Type = ""
        Transitive = ""
        SIDFiltering = ""
    }
}

# 4. Forest info
Write-Host "[*] Checking forest..."
$forest = Get-Forest
Write-Host "Forest: $($forest.Name)" -ForegroundColor Green
$forest.Domains

# 5. Trusts with SID history
Write-Host "[*] Checking SID history users..."
Get-DomainUser -LDAPFilter "(sidHistory=*)" | ForEach-Object {
    Write-Host "SID History found on: $($_.samaccountname)" -ForegroundColor Yellow
}

$report | Format-Table -AutoSize
```

## Stealth / OPSEC Considerations

- **Trust enumeration via netdom/nltest**: These tools run locally and generate Event ID 4662 for AD queries
- **Get-DomainTrust**: LDAP query to System container; may be monitored via Directory Service Access
- **SIDHistory enumeration**: Searching for sidHistory attribute is a specific LDAP filter that can be alerted on
- **Cross-domain authentication**: Logs on target domain when making authentication checks
- **Trust key extraction** (lsadump::trust): Requires Domain Admin and is extremely noisy
- **Foreign principals enumeration**: LDAP query against ForeignSecurityPrincipals container may be monitored

## Detection Notes

| Activity | Event ID | Notes |
|----------|----------|-------|
| Trust read (LDAP query) | 4662 | TrustedDomain object access |
| Trust retrieval (LSA) | 4618 | LSA trusted domain enumeration |
| Cross-domain auth | 4624 | Kerberos service ticket across domains |
| Trust validation (nltest) | 5663 | Application operation |
| sidHistory search | 4662 | Specific LDAP filter |
| ForeignSecurityPrincipal query | 4662 | Container access |
| ntdsutil trust listing | Various | Requires high privilege |

## Quick Reference

```powershell
# List all domain trusts
Get-DomainTrust
Get-ADTrust -Filter *

# Check for trusts without SID filtering
Get-DomainTrust | Where-Object {!($_.TrustAttributes -band 0x4)}

# Check for forest trusts
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"}
Get-ADTrust -Filter "TrustType -eq 'Forest'"

# Forest info
Get-Forest
Get-ADForest

# Foreign users/groups
Get-DomainForeignUser
Get-DomainForeignGroupMember

# SID history holders
Get-DomainUser -LDAPFilter "(sidHistory=*)"
Get-ADUser -LDAPFilter "(sidHistory=*)" -Properties sidHistory

# All accessible domains
(Get-ADForest).Domains
Get-DomainTrust | Select TargetName | Sort -Unique

# NetExec trust enumeration
nxc ldap <dc> -u 'user' -p 'pass' -M ad_enum -o TRUST=1

# Cross-domain command execution
nxc smb <dc> -u 'domain\user' -p 'pass' -d 'otherdomain.local' --shares
```
