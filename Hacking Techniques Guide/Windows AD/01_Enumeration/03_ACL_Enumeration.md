# ACL/ACE Enumeration

## Overview

Active Directory Access Control Lists (ACLs) define who can do what to which objects. Misconfigured ACLs are one of the most common paths to privilege escalation in AD. An ACL is composed of Access Control Entries (ACEs) that grant or deny permissions. Finding interesting ACEs (GenericAll, GenericWrite, WriteOwner, WriteDACL, ForceChangePassword, WriteSPN, DCSync) can reveal direct paths to Domain Admin or other high-value targets.

## Key Permissions to Look For

| Permission | Description | Abuse Path |
|------------|-------------|------------|
| GenericAll | Full control over object | Modify object properties, reset password, add to group |
| GenericWrite | Write any properties | Set SPN, modify script path, update attributes |
| WriteOwner | Change object owner | Take ownership, then modify DACL |
| WriteDACL | Modify object DACL | Grant yourself additional rights (DCSync, etc.) |
| AllExtendedRights | All extended rights | Includes ForceChangePassword, etc. |
| ForceChangePassword | Reset user password | Change password and authenticate as victim |
| Self-Membership | Add self to group | Become member of privileged group |
| WriteSPN | Modify SPN attribute | Target for Kerberoast after setting arbitrary SPN |
| DCSync | Replicate directory changes | Dump password hashes from DC |
| AddMember | Add members to group | Escalate via group membership |
| ResetPassword | Reset user's password | Same as ForceChangePassword |

## PowerView ACL Enumeration

### Get Object ACLs

```powershell
# Get ACL for a specific user
Get-DomainObjectAcl -Identity <username>

# Get ACL for a specific group
Get-DomainObjectAcl -Identity "Domain Admins"

# Get ACL for a specific computer
Get-DomainObjectAcl -Identity <computer-name>$

# Get ACL for a specific OU
Get-DomainObjectAcl -Identity "OU=Admins,DC=domain,DC=local"

# Get ACL for the domain object itself
Get-DomainObjectAcl -Identity "DC=domain,DC=local"

# Resolve GUIDs to human-readable names
Get-DomainObjectAcl -Identity <username> -ResolveGUIDs

# Get ACLs for all objects in domain (very large output)
Get-DomainObjectAcl -Domain domain.local -ResolveGUIDs
```

### Finding Interesting ACLs

```powershell
# Find all interesting ACLs (built-in PowerView function)
Find-InterestingDomainAcl

# Interesting ACLs with resolved GUIDs
Find-InterestingDomainAcl -ResolveGUIDs

# Search for DCSync rights
Find-InterestingDomainAcl -ResolveGUIDs -Verbose | Where-Object {$_.ObjectType -match "Replication-Get-Changes" -or $_.ObjectType -match "DS-Replication-Get-Changes"}

# Search for GenericAll rights
Find-InterestingDomainAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll"}

# Find ACLs where specific user has interesting rights
$userSID = (Get-DomainUser -Identity <username>).objectsid
Find-InterestingDomainAcl -ResolveGUIDs | Where-Object {$_.SecurityIdentifier -eq $userSID}
```

### Access Control for Specific Permission Types

```powershell
# GenericAll - full control
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll"}

# GenericWrite - write access
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericWrite"}

# WriteOwner - can change owner
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "WriteOwner"}

# WriteDACL - can modify permissions
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "WriteDACL"}

# Extended rights specific
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "ExtendedRight"}

# ForceChangePassword (User-Force-Change-Password = 00299570-246d-11d0-a768-00aa006e0529)
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ObjectAceType -eq "00299570-246d-11d0-a768-00aa006e0529"}

# AllExtendedRights
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ObjectAceType -eq "00000000-0000-0000-0000-000000000000" -and $_.ActiveDirectoryRights -match "ExtendedRight"}

# DCSync (DS-Replication-Get-Changes = 1131f6aa-9c07-11d1-f79f-00c04fc2dcd2)
# DS-Replication-Get-Changes-All = 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2
Get-DomainObjectAcl -Identity "DC=domain,DC=local" -ResolveGUIDs | Where-Object {
    $_.ObjectAceType -eq "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2" -or
    $_.ObjectAceType -eq "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2"
}
```

### Format ACL Output with Resolved SIDs

```powershell
# Get ACLs with resolved trustee identities
Get-DomainObjectAcl -Identity "Domain Admins" -ResolveGUIDs | ForEach-Object {
    [PSCustomObject]@{
        ObjectDN = $_.ObjectDN
        Trustee = ConvertFrom-SID $_.SecurityIdentifier
        Rights = $_.ActiveDirectoryRights
        ObjectType = $_.ObjectAceType
        AceType = $_.AceType
    }
}

# Get ACLs where specific user/group has rights
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.SecurityIdentifier -eq (Get-DomainUser -Identity <victim-user>).objectsid}
```

### Enumerate ACLs for All Privileged Objects

```powershell
# Check ACLs on Domain Admins group
Get-DomainObjectAcl -Identity "Domain Admins" -ResolveGUIDs

# Check ACLs on Enterprise Admins group (if in root domain)
Get-DomainObjectAcl -Identity "Enterprise Admins" -ResolveGUIDs

# Check ACLs on AdminSDHolder
Get-DomainObjectAcl -Identity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -ResolveGUIDs

# Check ACLs on all Domain Controllers
Get-DomainObjectAcl -Identity "Domain Controllers" -ResolveGUIDs

# Check ACLs on Schema Admins
Get-DomainObjectAcl -Identity "Schema Admins" -ResolveGUIDs

# Check ACLs on domain root
Get-DomainObjectAcl -Identity "DC=domain,DC=local" -ResolveGUIDs
```

## AD Module ACL Enumeration

```powershell
# Get ACL on specific AD object
Get-Acl -Path "AD:\CN=<user>,CN=Users,DC=domain,DC=local" | Format-List

# Get ACL on Domain Admins
Get-Acl -Path "AD:CN=Domain Admins,CN=Users,DC=domain,DC=local" | Format-List

# Get ACL on domain object
Get-Acl -Path "AD:DC=domain,DC=local" | Format-List

# Get ACLs via ADSI
$domain = [ADSI]"LDAP://CN=Domain Admins,CN=Users,DC=domain,DC=local"
$domain.PsBase.ObjectSecurity | Format-List

# Get ACEs for specific trustee
$acl = Get-Acl -Path "AD:DC=domain,DC=local"
$acl.Access | Where-Object {$_.IdentityReference -match "DOMAIN\\user"}
```

## NetExec ACL Enumeration

```bash
# DCSync rights enumeration
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o DCSYNC=1

# Admin ACL enumeration
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o ADMIN_ACL=1

# All ACLs
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o ACL=1
```

## Manual LDAP ACL Enumeration

```powershell
# Use ADSI to query ACLs
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]'LDAP://domain.local')
$searcher.Filter = "(&(objectClass=user)(samAccountName=<username>))"
$user = $searcher.FindOne().GetDirectoryEntry()
$user.PsBase.ObjectSecurity | Format-List

# Enumerate who has rights to a specific object
$obj = [ADSI]"LDAP://CN=Domain Admins,CN=Users,DC=domain,DC=local"
$acl = $obj.PsBase.ObjectSecurity
foreach($ace in $acl.Access) {
    Write-Host "Trustee: $($ace.IdentityReference), Rights: $($ace.ActiveDirectoryRights)"
}
```

## AD ACLScanner (Alternative Tool)

```powershell
# AD ACLScanner - finds dangerous ACLs
# Download from GitHub and run
Import-Module .\ADACLScan.ps1
Invoke-ACLScan -Base "DC=domain,DC=local"

# Output to CSV
Invoke-ACLScan -Base "DC=domain,DC=local" -OutputFile acl_scan.csv
```

## dsacls (Command-Line)

```cmd
# From Windows with RSAT
dsacls "CN=Domain Admins,CN=Users,DC=domain,DC=local"
dsacls "DC=domain,DC=local"
dsacls "CN=AdminSDHolder,CN=System,DC=domain,DC=local"

# Pipe output
dsacls "DC=domain,DC=local" > domain_acl.txt
```

## Python ACL Enumeration (Impacket)

```bash
# Dump domain ACLs with impacket
owneredit.py -action read <domain>/<user>:<pass>@<dc-ip>

# Get object ACLs via dacledit
dacledit.py <domain>/<user>:<pass>@<dc-ip> -target "CN=User,CN=Users,DC=domain,DC=local" -action read

# Compute security descriptor
python3 -c "
from impacket.examples import findDelegation
# use findDelegation to enumerate delegation + ACL info
"
```

## Resolving GUIDs to Permission Names

### Extended Rights GUIDs

| GUID | Name | Abuse |
|------|------|-------|
| `00299570-246d-11d0-a768-00aa006e0529` | User-Force-Change-Password | Reset user password |
| `91e647de-d96f-4a70-9557-d63ff4f3ccd1` | DS-Replication-Get-Changes | DCSync |
| `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes-All | DCSync (extended) |
| `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` | DS-Replication-Get-Changes-In-Filtered-Set | DCSync (filtered) |
| `72e39547-7b18-11d1-adef-00c04fd8d5cd` | Add/Remove self as member | Self-Membership |
| `ffa6f046-ca8b-4b0d-b1f5-ca59e62a4d0b` | Write SPN | Target for Kerberoast |
| `bf9679c0-0de6-11d0-a285-00aa003049e2` | Write Account Restrictions | Modify UAC flags |
| `f3a64788-5306-11d1-a9c5-0000f80367c1` | DS-Read-Password | Read password (rare) |
| `2f740136-a9cf-4a5a-a5e3-0eb6e6e2b2f0` | DS-Execute-Intentions | MS-TS evaluation |
| `ab721a53-1e2f-11d0-9819-00aa0040529b` | DS-Install-Replica | Install DC |
| `e45795b2-9455-11d1-aebd-0000f80367c1` | Change Domain Configuration | Modify domain |

### Property Set GUIDs

| GUID | Name |
|------|------|
| `72e39547-7b18-11d1-adef-00c04fd8d5cd` | Personal Information |
| `e45795b2-9455-11d1-aebd-0000f80367c1` | Public Information |
| `77b5b886-944a-11d1-aebd-0000f80367c1` | General Information |
| `4c164200-20c0-11d0-a768-00aa006e0529` | User Account Restrictions |
| `5f202010-79a5-11d0-9020-00c04fc2d4cf` | Logon Information |
| `bc0ac240-79a9-11d0-9020-00c04fc2d4cf` | Group Membership |

### Validated Writes GUIDs

| GUID | Name |
|------|------|
| `bf9679c0-0de6-11d0-a285-00aa003049e2` | Validated write to DNS host name |
| `f3a64788-5306-11d1-a9c5-0000f80367c1` | Validated write to service principal name |
| `5f202010-79a5-11d0-9020-00c04fc2d4cf` | Validated write to user principal name |
| `2f740136-a9cf-4a5a-a5e3-0eb6e6e2b2f0` | Validated write to group |

## Full ACL Enumeration Script

```powershell
# Comprehensive ACL dump
$domainDN = (Get-Domain).DistinguishedName
$report = @()

# DCSync rights
Write-Host "[*] Checking DCSync rights on $domainDN"
Get-DomainObjectAcl -Identity $domainDN -ResolveGUIDs | Where-Object {
    $_.ObjectAceType -eq "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2" -or
    $_.ObjectAceType -eq "1131f6ad-9c07-11d1-f79f-00c04fc2dcd2"
} | ForEach-Object {
    $report += [PSCustomObject]@{
        ObjectType = "DCSync"
        Trustee = ConvertFrom-SID $_.SecurityIdentifier
        Rights = $_.ActiveDirectoryRights
    }
}

# AdminSDHolder ACLs
Write-Host "[*] Checking AdminSDHolder ACLs"
Get-DomainObjectAcl -Identity "CN=AdminSDHolder,CN=System,$domainDN" -ResolveGUIDs | ForEach-Object {
    $report += [PSCustomObject]@{
        ObjectType = "AdminSDHolder"
        Trustee = ConvertFrom-SID $_.SecurityIdentifier
        Rights = $_.ActiveDirectoryRights
        ObjectAceType = $_.ObjectAceType
    }
}

# Privileged groups ACLs
$privilegedGroups = @("Domain Admins", "Enterprise Admins", "Schema Admins", "Administrators", "Account Operators", "Backup Operators", "Server Operators", "Print Operators")
foreach ($group in $privilegedGroups) {
    Write-Host "[*] Checking $group ACLs"
    Get-DomainObjectAcl -Identity $group -ResolveGUIDs -ErrorAction SilentlyContinue | ForEach-Object {
        $report += [PSCustomObject]@{
            ObjectType = "Group:$group"
            Trustee = ConvertFrom-SID $_.SecurityIdentifier
            Rights = $_.ActiveDirectoryRights
            ObjectAceType = $_.ObjectAceType
        }
    }
}

$report | Export-CSV domain_acls.csv -NoTypeInformation
```

## Stealth / OPSEC Considerations

- **ACL queries are logged**: Each LDAP ACL read can trigger Event ID 4662 (AUDIT_DS_ACCESS) if Directory Service Access auditing is enabled
- **ResolveGUIDs**: Avoid `-ResolveGUIDs` on all objects in large domains - it generates many LDAP queries; use targeted objects
- **Find-InterestingDomainAcl**: This is a heavy function that enumerates many ACLs; use sparingly
- **AdminSDHolder**: Querying AdminSDHolder specifically may trigger alerts on hardened systems
- **DCSync right enumeration**: Checking for DS-Replication-Get-Changes is a precursor to DCSync; blue teams monitor for these checks
- **LDAP query volume**: Each ACL check is an LDAP query; batch queries or reduce scope

## Detection Notes

| Activity | Event ID | What Blue Team Sees |
|----------|----------|---------------------|
| ACL read on privileged group | 4662 | Object Access > Directory Service Access; AccessMask = 0x20014 |
| ACL read for DCSync check | 4662 | ObjectType = DS-Replication-Get-Changes; suspicious if from non-DC |
| AdminSDHolder read | 4662 | ObjectDN contains AdminSDHolder; immediate alert in some orgs |
| Bulk ACL enumeration | 4662 | High volume of 4662 events from same source |
| PowerView ACL functions | 4104 | PowerShell script block logging |
| Find-InterestingDomainAcl | 4662, 4104 | Both LDAP and PowerShell logs |

## Quick Reference

```powershell
# Basic ACL checks
Get-DomainObjectAcl -Identity <target-object> -ResolveGUIDs

# Interesting ACLs (built-in)
Find-InterestingDomainAcl -ResolveGUIDs

# DCSync rights
Get-DomainObjectAcl -Identity "DC=domain,DC=local" -ResolveGUIDs | Where-Object {$_.ObjectAceType -match "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2"}

# ForceChangePassword
Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ObjectAceType -eq "00299570-246d-11d0-a768-00aa006e0529"}

# GenericAll on groups
Get-DomainObjectAcl -Identity "Domain Admins" -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll"}

# OUs with delegation
Get-DomainOU -FullData | ForEach-Object {
    $ou = $_
    Get-DomainObjectAcl -Identity $_.DistinguishedName -ResolveGUIDs | Select @{N='OU';E={$ou.Name}}, Trustee, Rights
}

# AdminSDHolder
Get-DomainObjectAcl -Identity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -ResolveGUIDs

# Check user's actual effective rights
$userSID = (Get-DomainUser -Identity <user>).objectsid
Get-DomainObjectAcl -Identity "Domain Admins" -ResolveGUIDs | Where-Object {$_.SecurityIdentifier -eq $userSID}
```
