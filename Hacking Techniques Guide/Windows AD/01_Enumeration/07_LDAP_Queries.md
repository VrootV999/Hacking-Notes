# LDAP Queries

## Overview

Manual LDAP queries provide granular control over AD enumeration. Unlike bulk tools, LDAP queries allow specific attribute retrieval, filtering, and paging. This is useful for stealth (targeted queries) and for environments where PowerView or SharpHound are blocked. Tools include `ldapsearch` (Linux), ADSI (PowerShell), AdFind (Windows), and Python ldap3.

## ldapsearch (Linux)

### Basic Connection

```bash
# Anonymous bind (if allowed)
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local"

# Authenticated bind
ldapsearch -x -H ldap://<dc-ip> -D "DOMAIN\\<user>" -w '<password>' -b "DC=domain,DC=local"

# UPN format
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local"

# LDAPS (port 636)
ldapsearch -x -H ldaps://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" -Z

# Global Catalog (port 3268)
ldapsearch -x -H ldap://<dc-ip>:3268 -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local"

# With TLS
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" -ZZ
```

### Domain Info

```bash
# Root DSE (domain/forest info, capabilities, naming contexts)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "" -s base "(objectClass=*)"

# Domain info
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" -s base "(objectClass=domain)" *

# Naming contexts
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "" -s base "(objectClass=*)" namingContexts

# Supported capabilities
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "" -s base "(objectClass=*)" supportedCapabilities
```

### User Queries

```bash
# All users (base attributes)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person))" sAMAccountName cn userPrincipalName

# All users with all attributes
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person))"

# Enabled users
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(!userAccountControl:1.2.840.113556.1.4.803:=2))" sAMAccountName

# Disabled users
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(userAccountControl:1.2.840.113556.1.4.803:=2))" sAMAccountName

# Users with SPN (Kerberoastable)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(servicePrincipalName=*))" sAMAccountName servicePrincipalName

# Users without Kerberos Pre-Auth (AS-REP Roastable)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" sAMAccountName

# AdminCount users
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(adminCount=1))" sAMAccountName adminCount

# SID History users
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(sidHistory=*))" sAMAccountName sidHistory

# Password never expires users
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(userAccountControl:1.2.840.113556.1.4.803:=65536))" sAMAccountName

# Password not required users
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(userAccountControl:1.2.840.113556.1.4.803:=32))" sAMAccountName

# Users with description field
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(description=*))" sAMAccountName description

# Locked out users
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(lockoutTime>=1))" sAMAccountName lockoutTime

# Users with trusted for delegation
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(userAccountControl:1.2.840.113556.1.4.803:=524288))" sAMAccountName

# Users with constrained delegation
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(msDS-AllowedToDelegateTo=*))" sAMAccountName msDS-AllowedToDelegateTo

# Created in last 30 days
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person)(whenCreated>=20240601000000.0Z))" sAMAccountName whenCreated

# Specific user
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(sAMAccountName=<username>)" *

# Users in specific OU
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "OU=Admins,DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person))" sAMAccountName

# Users with specific department/title/city
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(department=IT)" sAMAccountName department
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(title=admin*)" sAMAccountName title
```

### Group Queries

```bash
# All groups
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(objectClass=group)" sAMAccountName

# Specific group with members
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(sAMAccountName=Domain Admins)" member

# AdminCount groups (privileged)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=group)(adminCount=1))" sAMAccountName member

# Security groups vs distribution groups
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=2147483648))" sAMAccountName groupType

# Groups in specific OU
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "OU=Groups,DC=domain,DC=local" "(objectClass=group)" sAMAccountName

# Groups where a specific user is member
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=group)(member=CN=<username>,CN=Users,DC=domain,DC=local))" sAMAccountName

# Groups with foreign security principals
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=group)(member=CN=S-1-*))" sAMAccountName member

# Recursive group membership (LDAP_MATCHING_RULE_IN_CHAIN)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(member:1.2.840.113556.1.4.1941:=CN=<username>,CN=Users,DC=domain,DC=local)" sAMAccountName

# Domain local groups
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=4))" sAMAccountName

# Global groups
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=2))" sAMAccountName

# Universal groups
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=group)(groupType:1.2.840.113556.1.4.803:=8))" sAMAccountName
```

### Computer Queries

```bash
# All computers
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(objectClass=computer)" dNSHostName operatingSystem

# Computers with unconstrained delegation
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))" dNSHostName

# Computers with constrained delegation
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(msDS-AllowedToDelegateTo=*))" dNSHostName msDS-AllowedToDelegateTo

# Computers with LAPS
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(ms-Mcs-AdmPwdExpirationTime=*))" dNSHostName ms-Mcs-AdmPwdExpirationTime

# Domain Controllers
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(primaryGroupID=516))" dNSHostName operatingSystem

# Servers (non-DC)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(operatingSystem=*Server*)(!(primaryGroupID=516)))" dNSHostName operatingSystem

# Workstations
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(operatingSystem=*Windows 10*))" dNSHostName operatingSystem

# Computers with specific SPN
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(servicePrincipalName=MSSQLSvc/*))" dNSHostName servicePrincipalName

# Computers with RBCD
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(msDS-AllowedToActOnBehalfOfOtherIdentity=*))" dNSHostName

# Stale computers (last logon > 90 days)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=computer)(lastLogonTimestamp<=133000000000000000))" dNSHostName lastLogonTimestamp
```

### GPO Queries

```bash
# All GPOs
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=Policies,CN=System,DC=domain,DC=local" "(objectClass=groupPolicyContainer)" displayName gPCFileSysPath

# Specific GPO
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=Policies,CN=System,DC=domain,DC=local" "(displayName=Default Domain Policy)" *

# GPOs created recently
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=Policies,CN=System,DC=domain,DC=local" "(&(objectClass=groupPolicyContainer)(whenCreated>=20240101000000.0Z))" displayName whenCreated
```

### OU Queries

```bash
# All OUs
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(objectClass=organizationalUnit)" name distinguishedName

# OUs with GPO links
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=organizationalUnit)(gPLink=*))" name gPLink

# OUs with delegation (interesting ACLs)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(objectClass=organizationalUnit)" name
```

### Trust Queries

```bash
# All trusted domain objects
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=System,DC=domain,DC=local" "(objectClass=trustedDomain)" name trustDirection trustType trustAttributes flatName securityIdentifier

# Specific trust
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=System,DC=domain,DC=local" "(name=target.domain.local)" *
```

### ACL Queries

```bash
# Direct ACL queries are difficult via ldapsearch (requires nTSecurityDescriptor processing)
# However, you can find objects and their security descriptors
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(sAMAccountName=Domain Admins)" nTSecurityDescriptor

# Objects with adminCount=1 (privileged objects)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(adminCount=1)" sAMAccountName distinguishedName adminCount
```

### Service Specific Queries

```bash
# Find all registered SPNs
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=*)" sAMAccountName servicePrincipalName

# MSSQL services
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=MSSQLSvc/*)" sAMAccountName servicePrincipalName

# HTTP services
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=http/*)" sAMAccountName servicePrincipalName

# CIFS services
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=cifs/*)" sAMAccountName servicePrincipalName

# LDAP services
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=ldap/*)" sAMAccountName servicePrincipalName

# HOST services (equivalent to full control in Kerberos)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=HOST/*)" sAMAccountName servicePrincipalName

# WSMan/WinRM services
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=WSMAN/*)" sAMAccountName servicePrincipalName

# RDP services
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(servicePrincipalName=TERMSRV/*)" sAMAccountName servicePrincipalName
```

### Password Policy

```bash
# Domain password policy
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" -s base "(objectClass=domain)" minPwdLength lockoutThreshold lockoutDuration pwdHistoryLength

# Fine-grained password policies
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=Password Settings Container,CN=System,DC=domain,DC=local" "(objectClass=msDS-PasswordSettings)" *
```

### Foreign Security Principals

```bash
# All foreign security principals
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=ForeignSecurityPrincipals,DC=domain,DC=local" "(objectClass=foreignSecurityPrincipal)" cn

# Resolve foreign SIDs
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "CN=ForeignSecurityPrincipals,DC=domain,DC=local" "(objectClass=foreignSecurityPrincipal)" cn
```

### Output Formatting

```bash
# Output specific attributes only
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(sAMAccountName=<user>)" sAMAccountName cn memberOf distinguishedName

# Save to file
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person))" sAMAccountName > domain_users.ldap

# LDIF format output
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(sAMAccountName=*)" -L

# Size limit (default is 1000 for ldapsearch)
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(objectClass=user)" -E pr=1000/prompt

# Page size control
ldapsearch -x -H ldap://<dc-ip> -D "<user>@domain.local" -w '<password>' -b "DC=domain,DC=local" "(objectClass=user)" -E 'pagesize=500'
```

## ADSI (PowerShell - Windows)

### Basic ADSI Connection

```powershell
# Connect to LDAP
$domainDN = "DC=domain,DC=local"
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://$domainDN")

# Authenticated connection
$de = [ADSI]"LDAP://$domainDN"
$de.PsBase.Properties

# With alternate credentials
$username = "domain\user"
$password = "password"
$de = New-Object DirectoryServices.DirectoryEntry("LDAP://$domainDN", $username, $password)
```

### User Enumeration with ADSI

```powershell
# All users
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://DC=domain,DC=local")
$searcher.Filter = "(&(objectClass=user)(objectCategory=person))"
$searcher.FindAll() | ForEach-Object {
    [PSCustomObject]@{
        User = $_.Properties.samaccountname
        CN = $_.Properties.cn
        Enabled = -not ($_.Properties.useraccountcontrol[0] -band 2)
        LastLogon = [datetime]::FromFileTime($_.Properties.lastlogontimestamp[0])
    }
}

# Users with SPN
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://DC=domain,DC=local")
$searcher.Filter = "(&(objectClass=user)(objectCategory=person)(servicePrincipalName=*))"
$searcher.FindAll() | ForEach-Object {
    [PSCustomObject]@{
        User = $_.Properties.samaccountname
        SPN = $_.Properties.serviceprincipalname
    }
}

# Users without preauth
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://DC=domain,DC=local")
$searcher.Filter = "(&(objectClass=user)(objectCategory=person)(userAccountControl:1.2.840.113556.1.4.803:=4194304))"
$searcher.FindAll() | ForEach-Object {
    $_.Properties.samaccountname
}

# Users with adminCount
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://DC=domain,DC=local")
$searcher.Filter = "(&(objectClass=user)(objectCategory=person)(adminCount=1))"
$results = $searcher.FindAll()
$results | ForEach-Object { $_.Properties.samaccountname }

# Users with description
$searcher.Filter = "(&(objectClass=user)(objectCategory=person)(description=*))"
$searcher.FindAll() | ForEach-Object {
    [PSCustomObject]@{
        User = $_.Properties.samaccountname
        Description = $_.Properties.description
    }
}
```

### Group Enumeration with ADSI

```powershell
# All groups
$searcher.Filter = "(objectClass=group)"
$searcher.FindAll() | ForEach-Object { $_.Properties.samaccountname }

# Domain Admins members
$searcher.Filter = "(sAMAccountName=Domain Admins)"
$searcher.FindAll() | ForEach-Object {
    $_.Properties.member
}

# Groups with adminCount
$searcher.Filter = "(&(objectClass=group)(adminCount=1))"
$searcher.FindAll() | ForEach-Object { $_.Properties.samaccountname }

# Recursive group membership for user
$searcher.Filter = "(member:1.2.840.113556.1.4.1941:=CN=<username>,CN=Users,DC=domain,DC=local)"
$searcher.FindAll() | ForEach-Object { $_.Properties.samaccountname }
```

### Computer Enumeration with ADSI

```powershell
# All computers
$searcher.Filter = "(objectClass=computer)"
$searcher.FindAll() | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Properties.dnshostname
        OS = $_.Properties.operatingsystem
        Enabled = -not ($_.Properties.useraccountcontrol[0] -band 2)
    }
}

# Unconstrained delegation
$searcher.Filter = "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))"
$searcher.FindAll() | ForEach-Object { $_.Properties.dnshostname }

# With LAPS
$searcher.Filter = "(&(objectClass=computer)(ms-Mcs-AdmPwdExpirationTime=*))"
$searcher.FindAll() | ForEach-Object { $_.Properties.dnshostname }

# Domain Controllers
$searcher.Filter = "(&(objectClass=computer)(primaryGroupID=516))"
$searcher.FindAll() | ForEach-Object { $_.Properties.dnshostname }
```

### GPO Enumeration with ADSI

```powershell
# All GPOs
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://CN=Policies,CN=System,DC=domain,DC=local")
$searcher.Filter = "(objectClass=groupPolicyContainer)"
$searcher.FindAll() | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Properties.displayname
        Path = $_.Properties.gpcfilesyspath
        Version = $_.Properties.versionnumber
    }
}
```

### Trust Enumeration with ADSI

```powershell
# All trusts
$searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://CN=System,DC=domain,DC=local")
$searcher.Filter = "(objectClass=trustedDomain)"
$searcher.FindAll() | ForEach-Object {
    [PSCustomObject]@{
        Name = $_.Properties.name
        Direction = $_.Properties.trustdirection
        Type = $_.Properties.trusttype
        Attributes = $_.Properties.trustattributes
        FlatName = $_.Properties.flatname
    }
}
```

### ADSI Utility Functions

```powershell
# Resolve SID to name
Function ConvertFrom-ADSID {
    param([string]$SID)
    try {
        $obj = [System.Security.Principal.SecurityIdentifier]::new($SID)
        $obj.Translate([System.Security.Principal.NTAccount]).Value
    } catch {
        $SID
    }
}

# Get user's group membership
Function Get-ADSIGroupMembership {
    param([string]$Username)
    $searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://DC=domain,DC=local")
    $searcher.Filter = "(sAMAccountName=$Username)"
    $user = $searcher.FindOne()
    if ($user) {
        # Recursive membership
        $searcher.Filter = "(member:1.2.840.113556.1.4.1941:=$($user.Properties.distinguishedname))"
        $searcher.FindAll() | ForEach-Object { $_.Properties.samaccountname }
    }
}

# Get all SPNs
Function Get-ADSIAllSPNs {
    $searcher = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://DC=domain,DC=local")
    $searcher.Filter = "(servicePrincipalName=*)"
    $searcher.PropertiesToLoad.AddRange(@("sAMAccountName","servicePrincipalName"))
    $searcher.FindAll() | ForEach-Object {
        foreach ($spn in $_.Properties.serviceprincipalname) {
            [PSCustomObject]@{
                User = $_.Properties.samaccountname
                SPN = $spn
            }
        }
    }
}
```

## AdFind (Windows Binary)

### Installation

```cmd
# Download from https://www.joeware.net/freetools/tools/adfind/
# No installation required - standalone binary
adfind.exe -h
```

### Basic Queries

```cmd
# Default domain query
AdFind -default -f (objectClass=*)

# Specific server
AdFind -s <dc-ip> -b dc=domain,dc=local -f (objectClass=user)

# With credentials
AdFind -s <dc-ip> -u <user> -up <password> -b dc=domain,dc=local -f (objectClass=*)
```

### User Queries with AdFind

```cmd
# All users
AdFind -f "(&(objectCategory=person)(objectClass=user))" sAMAccountName

# All user attributes
AdFind -f "(&(objectCategory=person)(objectClass=user))" -list

# Enabled users
AdFind -f "(&(objectCategory=person)(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))" sAMAccountName

# Users with SPN (Kerberoastable)
AdFind -f "(&(objectCategory=person)(objectClass=user)(servicePrincipalName=*))" sAMAccountName servicePrincipalName

# Users without Kerberos Pre-Auth
AdFind -f "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" sAMAccountName

# AdminCount users
AdFind -f "(&(objectCategory=person)(objectClass=user)(adminCount=1))" sAMAccountName adminCount

# Users with SID history
AdFind -f "(&(objectCategory=person)(objectClass=user)(sidHistory=*))" sAMAccountName sidHistory

# Users with description
AdFind -f "(&(objectCategory=person)(objectClass=user)(description=*))" sAMAccountName description

# Users with passwords never expire
AdFind -f "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=65536))" sAMAccountName

# Users created in last 30 days (bit date conversion)
AdFind -f "(&(objectCategory=person)(objectClass=user)(whenCreated>=20240601000000.0Z))" sAMAccountName whenCreated
```

### Group Queries with AdFind

```cmd
# All groups
AdFind -f "(objectClass=group)" sAMAccountName

# Domain Admins with members
AdFind -f "(sAMAccountName=Domain Admins)" member -list

# Groups with adminCount
AdFind -f "(&(objectClass=group)(adminCount=1))" sAMAccountName

# Groups with members
AdFind -f "(objectClass=group)" sAMAccountName member -list

# Recursive user membership
AdFind -f "(member:1.2.840.113556.1.4.1941:=CN=<username>,CN=Users,DC=domain,DC=local)" sAMAccountName
```

### Computer Queries with AdFind

```cmd
# All computers
AdFind -f "(objectClass=computer)" dNSHostName operatingSystem

# Unconstrained delegation computers
AdFind -f "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))" dNSHostName

# Domain Controllers
AdFind -f "(&(objectClass=computer)(primaryGroupID=516))" dNSHostName operatingSystem

# Server OS
AdFind -f "(&(objectClass=computer)(operatingSystem=*Server*))" dNSHostName operatingSystem

# LAPS enabled
AdFind -f "(&(objectClass=computer)(ms-Mcs-AdmPwdExpirationTime=*))" dNSHostName ms-Mcs-AdmPwdExpirationTime

# Stale computers (last logon > 90 days)
AdFind -f "(&(objectClass=computer)(lastLogonTimestamp<=133000000000000000))" dNSHostName lastLogonTimestamp
```

### GPO Queries with AdFind

```cmd
# All GPOs
AdFind -subnodes -b CN=Policies,CN=System,DC=domain,DC=local -f "(objectClass=groupPolicyContainer)" displayName gPCFileSysPath

# GPO details
AdFind -subnodes -b CN=Policies,CN=System,DC=domain,DC=local -f "(displayName=Default Domain Policy)" -list
```

### Trust Queries with AdFind

```cmd
# All trusts
AdFind -subnodes -b CN=System,DC=domain,DC=local -f "(objectClass=trustedDomain)" name trustDirection trustType trustAttributes

# Specific trust
AdFind -subnodes -b CN=System,DC=domain,DC=local -f "(name=target.domain.local)" -list
```

### OU Queries with AdFind

```cmd
# All OUs
AdFind -f "(objectClass=organizationalUnit)" name distinguishedName

# OUs with GPO links
AdFind -f "(&(objectClass=organizationalUnit)(gPLink=*))" name gPLink

# OUs with protection
AdFind -f "(&(objectClass=organizationalUnit)(protected?=TRUE))" name
```

### Service and SPN Queries with AdFind

```cmd
# All SPNs
AdFind -f "(servicePrincipalName=*)" sAMAccountName servicePrincipalName

# Specific service types
AdFind -f "(servicePrincipalName=MSSQLSvc/*)" sAMAccountName servicePrincipalName
AdFind -f "(servicePrincipalName=http/*)" sAMAccountName servicePrincipalName
AdFind -f "(servicePrincipalName=cifs/*)" sAMAccountName servicePrincipalName
AdFind -f "(servicePrincipalName=TERMSRV/*)" sAMAccountName servicePrincipalName
```

### Object Counts with AdFind

```cmd
# Count users
AdFind -f "(&(objectCategory=person)(objectClass=user))" -count

# Count computers
AdFind -f "(objectClass=computer)" -count

# Count groups
AdFind -f "(objectClass=group)" -count

# Count GPOs
AdFind -subnodes -b CN=Policies,CN=System,DC=domain,DC=local -f "(objectClass=groupPolicyContainer)" -count
```

## Python LDAP Queries (ldap3)

```python
#!/usr/bin/env python3
import ldap3
from ldap3 import Server, Connection, ALL, NTLM

# Server info
server = Server('dc.domain.local', get_info=ALL)

# Authenticated connection (NTLM)
conn = Connection(server, user='DOMAIN\\user', password='password', authentication=NTLM)
conn.bind()

# Basic search
conn.search('DC=domain,DC=local', '(objectClass=user)', attributes=['sAMAccountName', 'cn'])
for entry in conn.entries:
    print(entry)

# Users with SPN
conn.search('DC=domain,DC=local', '(&(objectClass=user)(servicePrincipalName=*))',
            attributes=['sAMAccountName', 'servicePrincipalName'])

# Users without preauth
conn.search('DC=domain,DC=local',
            '(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))',
            attributes=['sAMAccountName'])

# AdminCount users
conn.search('DC=domain,DC=local', '(&(objectClass=user)(adminCount=1))',
            attributes=['sAMAccountName'])

# All groups
conn.search('DC=domain,DC=local', '(objectClass=group)',
            attributes=['sAMAccountName', 'member'])

# Domain Admins members
conn.search('DC=domain,DC=local', '(sAMAccountName=Domain Admins)',
            attributes=['member'])

# All computers
conn.search('DC=domain,DC=local', '(objectClass=computer)',
            attributes=['dNSHostName', 'operatingSystem'])

# Unconstrained delegation computers
conn.search('DC=domain,DC=local',
            '(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))',
            attributes=['dNSHostName'])

# GPOs
conn.search('CN=Policies,CN=System,DC=domain,DC=local', '(objectClass=groupPolicyContainer)',
            attributes=['displayName', 'gPCFileSysPath'])

# Trusts
conn.search('CN=System,DC=domain,DC=local', '(objectClass=trustedDomain)',
            attributes=['name', 'trustDirection', 'trustType', 'trustAttributes'])

# Search all objects (careful - large results)
conn.search('DC=domain,DC=local', '(objectClass=*)', attributes=['distinguishedName'], size_limit=10)

# Unbind
conn.unbind()
```

## Python LDAP Queries (Impacket)

```python
#!/usr/bin/env python3
from impacket.ldap import ldapasn1 as ldap
from impacket.ldap import ldaptypes
from impacket.examples.utils import parse_credentials

# Using impacket's LDAP library
domain, username, password, dc_ip = "domain.local", "user", "password", "192.168.1.10"

ldap_conn = ldap.LDAPConnection(f"ldap://{dc_ip}", baseDN=f"DC={domain.replace('.', ',DC=')}")
ldap_conn.login(username, password, domain, "", lmhash="", nthash="")

# Search users
results = ldap_conn.search(searchFilter="(&(objectClass=user)(objectCategory=person))",
                           attributes=['sAMAccountName', 'cn'])
for r in results:
    print(r['attributes'])

# Search computers
results = ldap_conn.search(searchFilter="(objectClass=computer)",
                           attributes=['dNSHostName'])
```

## Stealth / OPSEC Considerations

- **Size Limits**: ldapsearch defaults to 1000 results; use paging or specific filters to avoid incomplete data
- **LDAP Query Logging**: Event ID 4662 logs LDAP queries when Directory Service Access auditing is enabled
- **Anonymous LDAP**: Often blocked in modern environments; authenticated queries are more reliable
- **Global Catalog**: Port 3268 queries may be less monitored than port 389 in some environments
- **LDAPS**: Port 636 queries are encrypted but may be monitored at the DC
- **Time-based detection**: Rapid consecutive queries can indicate scanning; add delays between queries
- **Filter specificity**: Use targeted filters (e.g., specific user search) instead of wildcard for stealth
- **UserAccountControl bitwise**: The `LDAP_MATCHING_RULE_BIT_AND` (1.2.840.113556.1.4.803) syntax is best for UAC queries
- **Recursive membership**: `LDAP_MATCHING_RULE_IN_CHAIN` (1.2.840.113556.1.4.1941) is a server-side operation that can be expensive on large domains

## Detection Notes

| Activity | Event ID | Notes |
|----------|----------|-------|
| LDAP query (any) | 4662 | Directory Service Access; AccessMask indicates read |
| ldapsearch auth | 4776 | Credential validation for ldapsearch bind |
| Anonymous LDAP bind | 4625 (if fails) | May be logged as anonymous logon failure |
| Large result set | 4662 | Multiple 4662 events in short window |
| Paged search | 4662 | Paged LDAP queries |
| AdFind execution | 4688 | Process creation (adfind.exe) |
| ADSI/PowerShell LDAP | 4104 | Script block logging captures LDAP queries |
| Python ldap3 | 4688 | Python process running LDAP queries |

## Quick Reference

```bash
# Domain info
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "" -s base "(objectClass=*)"

# All users
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(&(objectClass=user)(objectCategory=person))" sAMAccountName

# Kerberoastable users
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(&(objectClass=user)(servicePrincipalName=*))" sAMAccountName servicePrincipalName

# AS-REP Roastable users
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))" sAMAccountName

# AdminCount users
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(&(objectClass=user)(adminCount=1))" sAMAccountName

# SID History users
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(&(objectClass=user)(sidHistory=*))" sAMAccountName

# All computers
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(objectClass=computer)" dNSHostName operatingSystem

# Unconstrained delegation computers
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(&(objectClass=computer)(userAccountControl:1.2.840.113556.1.4.803:=524288))" dNSHostName

# Domain Controllers
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(&(objectClass=computer)(primaryGroupID=516))" dNSHostName

# All groups
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(objectClass=group)" sAMAccountName

# Domain Admins members
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" "(sAMAccountName=Domain Admins)" member

# All trusts
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "CN=System,DC=domain,DC=local" "(objectClass=trustedDomain)" name trustDirection

# All GPOs
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "CN=Policies,CN=System,DC=domain,DC=local" "(objectClass=groupPolicyContainer)" displayName

# Password policy
ldapsearch -x -H ldap://<dc> -D "u@d" -w 'p' -b "DC=domain,DC=local" -s base "(objectClass=domain)" minPwdLength lockoutThreshold
```
