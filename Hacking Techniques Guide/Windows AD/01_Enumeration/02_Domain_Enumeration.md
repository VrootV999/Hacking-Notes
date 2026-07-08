# Domain Enumeration (Authenticated)

## Overview

Once you have domain credentials (low-priv or otherwise), the entire AD environment opens up. Authenticated enumeration reveals users, groups, computers, GPOs, OUs, trusts, ACLs, and more. This file covers enumeration using PowerView, Active Directory Module, NetExec, and manual LDAP queries.

## Initial Setup

```powershell
# Load PowerView
powershell -ep bypass
Import-Module .\PowerView.ps1

# Load AD Module (on domain-joined system with RSAT)
Import-Module ActiveDirectory

# Remote AD Module from Linux (Impacket)
python3 -c "from impacket.examples import findDelegation; ..."
```

## Domain & Forest Information

### PowerView

```powershell
# Get domain object
Get-Domain
Get-NetDomain

# Get domain SID
Get-DomainSID

# Get domain policy
Get-DomainPolicy
(Get-DomainPolicy)."System Access"
(Get-DomainPolicy)."Kerberos Policy"

# Get domain controller info
Get-DomainController
Get-NetDomainController -Domain domain.local
Get-DomainController -Server <dc-name> | Select Name, OSVersion, SiteName, IPAddress

# Get forest info
Get-Forest
Get-ForestDomain
Get-ForestGlobalCatalog
Get-ForestSite
Get-ForestServer

# Domain functional level
(Get-Domain).DomainMode
```

### AD Module

```powershell
# Domain info
Get-ADDomain
Get-ADDomain | Format-List *
Get-ADDomain | Select DNSRoot, NetBIOSName, DomainMode

# Domain controller info
Get-ADDomainController
Get-ADDomainController -Filter * | Select Name, IPv4Address, Site, OperatingSystem

# Forest info
Get-ADForest
Get-ADForest | Select RootDomain, Domains, GlobalCatalogs, Sites, ForestMode

# Functional levels
Get-ADDomain | fl DomainMode
Get-ADForest | fl ForestMode
```

### NetExec

```bash
# Domain info
nxc smb <dc-ip> -u 'user' -p 'pass' --os
nxc ldap <dc-ip> -u 'domain\user' -p 'pass' -M ad_enum

# Get domain SID
nxc smb <dc-ip> -u 'user' -p 'pass' --get-sid
```

## User Enumeration

### PowerView

```powershell
# ALL domain users
Get-DomainUser
Get-NetUser

# All user properties
Get-DomainUser -Identity * | Select *

# Specific user
Get-DomainUser -Identity <username>
Get-NetUser -Username <username>

# Key properties filter
Get-DomainUser | Select samaccountname, objectsid, pwdlastset, lastlogontimestamp, badpwdcount, admincount, memberof, description, whencreated, useraccountcontrol

# Enabled users only
Get-DomainUser -LDAPFilter "(!(userAccountControl:1.2.840.113556.1.4.803:=2))"

# Users with SPN (Kerberoastable)
Get-DomainUser -SPN
Get-DomainUser -SPN | Select samaccountname, serviceprincipalname

# Users with Pre-Auth Not Required (AS-REP Roastable)
Get-DomainUser -PreauthNotRequired
Get-DomainUser -PreauthNotRequired | Select samaccountname

# AdminCount >= 1 (privileged users)
Get-DomainUser -AdminCount
Get-DomainUser -AdminCount | Select samaccountname, admincount

# Users with sidHistory set
Get-DomainUser -LDAPFilter "(sidHistory=*)"

# Users with PasswordNeverExpires
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=65536)"

# Users with PasswordNotRequired
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=32)"

# Users by logon count (stale accounts)
Get-DomainUser -LDAPFilter "(logonCount=0)" | select samaccountname

# Users with trust attributes
Get-DomainUser -TrustedToAuth
Get-DomainUser -TrustedForDelegation

# Users created recently
Get-DomainUser -LDAPFilter "(whenCreated>=20240101000000.0Z)"

# Find users in specific OU
Get-DomainUser -SearchBase "OU=Admins,DC=domain,DC=local"

# Domain admin group members
Get-DomainGroupMember -Identity "Domain Admins" -Recurse
Get-DomainGroupMember -Identity "Enterprise Admins" -Recurse

# Users with description (potential secrets)
Get-DomainUser | Where-Object {$_.Description -ne $null} | Select samaccountname, description

# Users by department/city/title
Get-DomainUser -LDAPFilter "(department=IT)"
Get-DomainUser -LDAPFilter "(title=admin)" | Select samaccountname, title
```

### AD Module

```powershell
# All users
Get-ADUser -Filter *

# All users with all properties
Get-ADUser -Filter * -Properties *

# Specific user
Get-ADUser <username> -Properties *

# Filtered
Get-ADUser -Filter "Enabled -eq 'True'" -Properties *

# Users with SPN
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName, samaccountname
Get-ADUser -Filter * -Properties ServicePrincipalName | Where-Object {$_.ServicePrincipalName}

# Users with PreAuth not required
Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true} -Properties DoesNotRequirePreAuth

# Users by last logon
Get-ADUser -Filter "lastLogonTimestamp -gt 0" -Properties lastLogonTimestamp | Sort lastLogonTimestamp

# AdminCount users
Get-ADUser -LDAPFilter "(adminCount=1)" | Select Name

# User with sidHistory
Get-ADUser -LDAPFilter "(sidHistory=*)"

# Password last set
Get-ADUser -Filter * -Properties PasswordLastSet | Select Name, PasswordLastSet

# Group membership
Get-ADUser <username> -Properties MemberOf | Select -ExpandProperty MemberOf
```

### NetExec LDAP

```bash
# User enumeration
nxc ldap <dc-ip> -u 'user' -p 'pass' --users
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o USER=1

# All user attributes
nxc ldap <dc-ip> -u 'user' -p 'pass' --users -o ATTRIBUTES=sAMAccountName,cn,userPrincipalName,adminCount,servicePrincipalName,userAccountControl

# Kerberoastable users
nxc ldap <dc-ip> -u 'user' -p 'pass' --kerberoast
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o KERBEROAST=1

# ASREPRoastable users
nxc ldap <dc-ip> -u 'user' -p 'pass' --asreproast
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o ASREPROAST=1

# AdminCount users
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o ADMINCOUNT=1

# Dump all users to file
nxc ldap <dc-ip> -u 'user' -p 'pass' --users > users.txt
```

## Group Enumeration

### PowerView

```powershell
# All groups
Get-DomainGroup
Get-NetGroup

# Specific group
Get-DomainGroup -Identity "Domain Admins"

# Admin groups (adminCount > 0)
Get-DomainGroup -AdminCount

# Groups with specific filter
Get-DomainGroup -LDAPFilter "(groupType:1.2.840.113556.1.4.803:=2147483648)"  # Security groups

# Group membership (members)
Get-DomainGroupMember -Identity "Domain Admins"
Get-DomainGroupMember -Identity "Domain Admins" -Recurse

# Group membership (user is member of)
Get-DomainGroup -MemberIdentity <username>
Get-NetGroup -UserName <username>

# Nested group membership
Get-DomainGroupMember -Identity "Domain Admins" -Recurse | Select MemberName

# Foreign group membership (external domain groups)
Get-DomainForeignGroupMember -Domain domain.local

# Group Managed Service Accounts group
Get-DomainGroup -Identity "Group Policy Creator Owners"

# Bulk group member enumeration
Get-DomainGroup | ForEach-Object {Get-DomainGroupMember -Identity $_.DistinguishedName | Select @{N='Group';E={$_.GroupName}}, MemberName} | Export-CSV group_members.csv

# Local groups on machines
Get-DomainLocalGroup -ComputerName <server>
Get-DomainLocalGroupMember -ComputerName <server> -GroupName "Administrators"
```

### AD Module

```powershell
# All groups
Get-ADGroup -Filter *

# Specific group with members
Get-ADGroup "Domain Admins" -Properties Member
Get-ADGroupMember "Domain Admins" -Recursive

# Security groups
Get-ADGroup -Filter "GroupCategory -eq 'Security'"

# Group with LDAP filter  
Get-ADGroup -LDAPFilter "(adminCount=1)"

# Groups a user is member of
Get-ADPrincipalGroupMembership <username>

# Group members
Get-ADGroupMember "Domain Admins" | Select Name, SamAccountName, ObjectClass
```

### NetExec

```bash
# Group enumeration
nxc ldap <dc-ip> -u 'user' -p 'pass' --groups
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o GROUP=1

# Group members of specific group
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o GROUP_MEMBER="Domain Admins"
```

## Computer Enumeration

### PowerView

```powershell
# All computers
Get-DomainComputer
Get-NetComputer

# All properties
Get-DomainComputer | Select *

# Computers with full data (OS, version, SID, etc.)
Get-DomainComputer -FullData

# Computers by OS
Get-DomainComputer -OperatingSystem "Windows 10*"
Get-DomainComputer -OperatingSystem "*Server*"

# Computers with unconstrained delegation
Get-DomainComputer -Unconstrained
Get-DomainComputer -TrustedForDelegation

# Computers with constrained delegation
Get-DomainComputer -TrustedToAuth
Get-DomainComputer -LDAPFilter "(msDS-AllowedToDelegateTo=*)"

# Computers with LAPS
Get-DomainComputer -LDAPFilter "(ms-Mcs-AdmPwdExpirationTime=*)"

# Computers in specific OU
Get-DomainComputer -SearchBase "OU=Workstations,DC=domain,DC=local"

# Computers that are alive (PING)
Get-DomainComputer -Ping

# DCs
Get-DomainComputer -DomainController
Get-NetDomainController

# Find SQL servers via SPN
Get-DomainComputer -LDAPFilter "(servicePrincipalName=MSSQLSvc/*)"

# Computers by last logon timestamp
Get-DomainComputer -LDAPFilter "(lastLogonTimestamp>=133000000000000000)"
```

### AD Module

```powershell
# All computers
Get-ADComputer -Filter *

# All properties
Get-ADComputer -Filter * -Properties *

# Computers with OS filter
Get-ADComputer -Filter "OperatingSystem -like '*Server*'" -Properties OperatingSystem

# Unconstrained delegation
Get-ADComputer -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation

# LAPS enabled
Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwdExpirationTime | Where-Object {$_.'ms-Mcs-AdmPwdExpirationTime'}

# Computers by last logon
Get-ADComputer -Filter "LastLogonDate -gt (Get-Date).AddDays(-90)" -Properties LastLogonDate

# Find disabled computers
Get-ADComputer -Filter "Enabled -eq 'False'"

# Specific computer
Get-ADComputer <computer-name> -Properties *
```

### NetExec

```bash
# Computer enumeration (via LDAP)
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o COMPUTER=1

# Find Domain Controllers
nxc smb <dc-ip> -u 'user' -p 'pass' -M ad_enum -o DC=1

# OS version of all computers (via SMB on each host)
nxc smb <target-list> -u 'user' -p 'pass' --os
```

## Service Principal Names (SPN) Enumeration

### PowerView

```powershell
# Find SPNs (Kerberoastable accounts)
Get-DomainUser -SPN
Get-DomainUser -SPN | Get-DomainSPNTicket

# Find computers with SPNs
Get-DomainComputer -SPN

# Find all registered SPNs in domain
Get-DomainObject -LDAPFilter "(servicePrincipalName=*)" -Properties servicePrincipalName, name

# Find specific service SPN
Get-DomainUser -LDAPFilter "(servicePrincipalName=MSSQLSvc/*)"
Get-DomainUser -LDAPFilter "(servicePrincipalName=http/*)"
Get-DomainUser -LDAPFilter "(servicePrincipalName=cifs/*)"

# Export SPN list
Get-DomainUser -SPN | Select samaccountname, serviceprincipalname | Export-CSV spn_accounts.csv
```

### AD Module

```powershell
# Kerberoastable users
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName, samaccountname

# Find computers with specific SPN
Get-ADComputer -Filter "ServicePrincipalName -like 'MSSQLSvc/*'" -Properties ServicePrincipalName

# All objects with SPN
Get-ADObject -LDAPFilter "(servicePrincipalName=*)" -Properties servicePrincipalName, name
```

### NetExec

```bash
# Get Kerberoastable accounts (SPN)
nxc ldap <dc-ip> -u 'user' -p 'pass' --kerberoast
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o KERBEROAST=1
```

## User Account Control Flags

### PowerView

```powershell
# Accounts with specific UAC flags:
# ACCOUNTDISABLE      = 2
# PASSWD_NOTREQD      = 32
# PASSWD_CANT_CHANGE  = 64
# DONT_EXPIRE_PASSWD  = 65536
# TRUSTED_FOR_DELEGATION = 524288
# NOT_DELEGATED       = 1048576
# TRUSTED_TO_AUTH_FOR_DELEGATION = 16777216

# Password not required
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=32)"

# Password never expires
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=65536)"

# Disabled accounts
Get-DomainUser -LDAPFilter "(userAccountControl:1.2.840.113556.1.4.803:=2)"

# Check UAC flags
Get-DomainUser | Select samaccountname, useraccountcontrol
```

### AD Module

```powershell
# UserAccountControl enum values
Get-ADUser -Filter * -Properties UserAccountControl | Select Name, UserAccountControl

# Individual checks  
Get-ADUser -Filter {Enabled -eq $false}
Get-ADUser -Filter {PasswordNeverExpires -eq $true} -Properties PasswordNeverExpires
Get-ADUser -Filter {$_.PasswordNotRequired -eq $true} -Properties PasswordNotRequired
```

## OU Enumeration

### PowerView

```powershell
# All OUs
Get-DomainOU
Get-NetOU

# Specific OU properties
Get-DomainOU | Select name, distinguishedName, gplink

# OUs with GPO links
Get-DomainOU -LDAPFilter "(gPLink=*)"

# OUs in specific path
Get-DomainOU -SearchBase "DC=domain,DC=local"

# Objects in an OU
Get-DomainUser -SearchBase "OU=Admins,DC=domain,DC=local"
Get-DomainComputer -SearchBase "OU=Workstations,DC=domain,DC=local"
```

### AD Module

```powershell
# All OUs
Get-ADOrganizationalUnit -Filter *

# With linked GPOs
Get-ADOrganizationalUnit -Filter * -Properties gplink, gpoptions, linkedGroupPolicyObjects

# Objects in specific OU
Get-ADObject -Filter * -SearchBase "OU=Admins,DC=domain,DC=local"

# OUs with protection
Get-ADOrganizationalUnit -Filter "ProtectedFromAccidentalDeletion -eq $true"
```

## Delegation Enumeration

### PowerView

```powershell
# Unconstrained delegation
Get-DomainComputer -Unconstrained
Get-DomainComputer -TrustedForDelegation

# Constrained delegation (users)
Get-DomainUser -TrustedToAuth
Get-DomainUser -LDAPFilter "(msDS-AllowedToDelegateTo=*)"
Get-DomainUser -LDAPFilter "(msDS-AllowedToDelegateTo=*)" | Select samaccountname, msds-allowedtodelegateto, useraccountcontrol

# Constrained delegation (computers)
Get-DomainComputer -TrustedToAuth
Get-DomainComputer -LDAPFilter "(msDS-AllowedToDelegateTo=*)"

# RBCD (resource-based constrained delegation)
Get-DomainComputer -LDAPFilter "(msDS-AllowedToActOnBehalfOfOtherIdentity=*)"
Get-DomainUser -LDAPFilter "(msDS-AllowedToActOnBehalfOfOtherIdentity=*)"

# Find all delegation relationships
Get-DomainObject -LDAPFilter "(&(|(userAccountControl:1.2.840.113556.1.4.803:=524288)(userAccountControl:1.2.840.113556.1.4.803:=16777216))(objectCategory=person))" | Select name, useraccountcontrol

# Find delegation for all non-DC computers
Get-DomainComputer -LDAPFilter "(!(primaryGroupId=516))" | Where-Object {$_.TrustedForDelegation -or $_.TrustedToAuthForDelegation}
```

### AD Module

```powershell
# Unconstrained delegation
Get-ADUser -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation, ServicePrincipalName
Get-ADComputer -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation

# Constrained delegation (all objects)
Get-ADObject -LDAPFilter "(msDS-AllowedToDelegateTo=*)" -Properties msDS-AllowedToDelegateTo, Name

# RBCD
Get-ADComputer -LDAPFilter "(msDS-AllowedToActOnBehalfOfOtherIdentity=*)" -Properties msDS-AllowedToActOnBehalfOfOtherIdentity
```

### NetExec

```bash
# Delegation enumeration
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o DELEGATION=1

# Find unconstrained delegation
nxc ldap <dc-ip> -u 'user' -p 'pass' --unconstrained-delegation

# Find constrained delegation
nxc ldap <dc-ip> -u 'user' -p 'pass' --constrained-delegation
```

## Password Policy Enumeration

### PowerView

```powershell
# Domain password policy
Get-DomainPolicy
(Get-DomainPolicy)."System Access"
(Get-DomainPolicy)."Kerberos Policy"

# Fine-grained password policies
Get-DomainObject -LDAPFilter "(objectClass=msDS-PasswordSettings)"
Get-DomainObject -LDAPFilter "(objectClass=msDS-PasswordSettings)" | Select name, msDS-MinimumPasswordLength, msDS-PasswordHistoryLength, msDS-LockoutThreshold, msDS-LockoutDuration
```

### AD Module

```powershell
# Default domain policy
Get-ADDefaultDomainPasswordPolicy

# Fine-grained password policies
Get-ADFineGrainedPasswordPolicy -Filter *

# Password policy for specific user
Get-ADUserResultantPasswordPolicy <username>
```

### NetExec

```bash
# Password policy via SMB
nxc smb <dc-ip> -u 'user' -p 'pass' --pass-pol

# Password policy via LDAP
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o PASSWORD_POLICY=1
```

## Share Enumeration

### PowerView

```powershell
# Find shares on all domain machines
Invoke-ShareFinder
Invoke-ShareFinder -Verbose

# Filter to only writeable shares
Invoke-ShareFinder -CheckShareAccess | Where-Object {$_.Access -match "Write"}

# Share finder with specific domain
Invoke-ShareFinder -Domain domain.local

# Find sensitive shares
Invoke-ShareFinder -ExcludeIPC -ExcludeADMIN -ExcludeC | Export-CSV shares.csv
```

### NetExec

```bash
# Share enumeration
nxc smb <target-ip> -u 'user' -p 'pass' --shares

# Recursive share listing
nxc smb <target-ip> -u 'user' -p 'pass' -M spider_plus -o READ_ONLY=false

# Find file with specific extension on shares
nxc smb <target-ip> -u 'user' -p 'pass' -M spider_plus -o PATTERN="txt,conf,ini,xml,ps1,py,sh,kdbx"
```

## Local Admin & Session Enumeration

### PowerView

```powershell
# Find machines where current user has local admin
Find-LocalAdminAccess

# Enumerate local admins on machines
Invoke-EnumerateLocalAdmin

# Find logged-on users
Get-NetLoggedon -ComputerName <server>

# Find last logged-on user
Get-LastLoggedOn -ComputerName <server>

# RDP sessions
Get-NetRDPSession -ComputerName <server>

# WinRM access check
Test-WSMAN -ComputerName <server>

# PS remoting availability
Invoke-Command -ComputerName <server> -ScriptBlock {Get-Process} -Credential $creds

# Find user sessions across domain
Invoke-UserHunter
Invoke-UserHunter -Stealth
Invoke-UserHunter -GroupName "Domain Admins"
```

## User Account Control (UAC) / Domain Admins

### PowerView

```powershell
# List all privileged accounts (adminCount=1)
Get-DomainUser -AdminCount
Get-DomainUser -LDAPFilter "(adminCount=1)" | Select samaccountname, memberof

# Direct DA list
Get-DomainGroupMember -Identity "Domain Admins" -Recurse
Get-DomainGroupMember -Identity "Enterprise Admins" -Recurse
Get-DomainGroupMember -Identity "Schema Admins" -Recurse

# Builtin admin group
Get-DomainGroupMember -Identity "Administrators" -Recurse

# Account Operators
Get-DomainGroupMember -Identity "Account Operators"
Get-DomainGroupMember -Identity "Backup Operators"
Get-DomainGroupMember -Identity "Print Operators"
Get-DomainGroupMember -Identity "Server Operators"

# List all protected users
Get-DomainGroupMember -Identity "Protected Users"
```

## Service & Application Enumeration

### PowerView

```powershell
# Find domain controllers
Get-DomainController | Select Name, SiteName, IPAddress, OSVersion

# Find SQL servers via SPN
Get-DomainComputer -LDAPFilter "(servicePrincipalName=MSSQLSvc*)"
Get-DomainUser -LDAPFilter "(servicePrincipalName=MSSQLSvc*)"

# Find Exchange servers
Get-DomainComputer -LDAPFilter "(servicePrincipalName=exchangeMDB/*)"

# Find web servers
Get-DomainComputer -LDAPFilter "(servicePrincipalName=http/*)"
Get-DomainComputer -LDAPFilter "(servicePrincipalName=wsman/*)"

# Find file servers (via SPN)
Get-DomainComputer -LDAPFilter "(servicePrincipalName=cifs/*)"
```

## Bulk Data Export

```powershell
# Export all users to CSV
Get-DomainUser | Select samaccountname, objectsid, pwdlastset, lastlogontimestamp, admincount, memberof, description, useraccountcontrol | Export-CSV domain_users.csv -NoTypeInformation

# Export all computers
Get-DomainComputer -FullData | Select dNSHostName, OperatingSystem, whenCreated, TrustedForDelegation | Export-CSV domain_computers.csv -NoTypeInformation

# Export all groups with members
Get-DomainGroup | ForEach-Object {
    $group = $_
    Get-DomainGroupMember -Identity $_.DistinguishedName | Select @{N='GroupName';E={$group.Name}}, MemberName, MemberDistinguishedName
} | Export-CSV group_members_full.csv -NoTypeInformation
```

## OPSEC Considerations

- **PowerView logs**: `Get-DomainUser` triggers LDAP queries; PowerShell ScriptBlock logging (Event 4104) may capture commands
- **NetExec SMB scans**: Hitting every host with `--shares` is noisy; target suspicious machines only
- **Ping sweeps**: ICMP traffic is often monitored
- **Large queries**: `Get-DomainUser -LDAPFilter "(objectClass=*)"` will page all objects; use targeted filters
- **Replication operations**: Queries that simulate replication (for DCSync enumeration) may trigger honeytoken accounts
- **Scan throttling**: Use `-ThrottleLimit` in PowerView bulk operations
- **Remote execution**: Using Invoke-Command or WinRM creates a 4624 logon event and PowerShell 4104 events on the target

## Detection Notes

| Activity | Event ID | Notes |
|----------|----------|-------|
| LDAP query for all users | 4662 | Directory Service Access audit; object type user |
| Group membership read | 4799 | Security group enumeration |
| PowerShell script block | 4104 | Captures PowerView commands |
| NetExec SMB connection | 5140, 5145 | SMB share access events |
| Bulk AD object read | 4662 | Many queries in short window |
| Remote WinRM | 4624, 4104 | Logon + PowerShell events on target |
| SharpHound data collection | 4688, 4104 | Process creation + script block |

## Quick Reference

```powershell
# Domain Info
Get-Domain | fl
Get-DomainSID
Get-DomainPolicy

# All Users
Get-DomainUser | Select samaccountname, objectclass
Get-DomainUser -SPN                         # Kerberoast
Get-DomainUser -PreauthNotRequired          # AS-REP Roast
Get-DomainUser -AdminCount                  # Privileged

# All Groups
Get-DomainGroup -AdminCount
Get-DomainGroupMember "Domain Admins" -Recurse
Get-DomainForeignGroupMember

# All Computers
Get-DomainComputer -FullData
Get-DomainComputer -Unconstrained            # Delegation
Get-DomainComputer -TrustedToAuth
Get-DomainComputer -OperatingSystem "*Server*" # Servers

# OUs
Get-DomainOU -FullData

# GPOs
Get-DomainGPO | Select displayname, gpcfilesyspath

# Shares
Invoke-ShareFinder

# Local Admin
Find-LocalAdminAccess
Invoke-EnumerateLocalAdmin

# Sessions
Get-NetLoggedon -ComputerName <server>
Get-NetRDPSession -ComputerName <server>
Invoke-UserHunter

# SPN / Delegation
Get-DomainUser -SPN
Get-DomainUser -TrustedToAuth
Get-DomainComputer -TrustedForDelegation
Get-DomainComputer -TrustedToAuth
```
