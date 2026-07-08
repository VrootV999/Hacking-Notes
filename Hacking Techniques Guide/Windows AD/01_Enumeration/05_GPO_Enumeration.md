# GPO Enumeration

## Overview

Group Policy Objects (GPOs) are a core AD feature for centrally managing security and configuration settings across domain-joined computers and users. Misconfigured GPOs can be abused for privilege escalation, lateral movement, and persistence. GPO abuse typically involves identifying writable GPOs, GPOs with apply group policy to non-privileged users, or vulnerable settings like AlwaysInstallElevated, scheduled tasks, logon scripts, and unrestricted delegation via GPO.

## PowerView GPO Enumeration

### Basic GPO Enumeration

```powershell
# List all GPOs
Get-DomainGPO
Get-NetGPO

# Detailed GPO info
Get-DomainGPO | Select displayname, gpcfilesyspath, versionNumber, whenChanged

# All GPO properties
Get-DomainGPO | Format-List *
Get-DomainGPO -FullData

# GPOs in specific domain
Get-DomainGPO -Domain domain.local

# GPOs by display name
Get-DomainGPO -Identity "Default Domain Policy"
Get-DomainGPO -Identity "Default Domain Controllers Policy"
```

### GPO Links to OUs

```powershell
# Get all GPO links (which OUs each GPO applies to)
Get-DomainGPO | Select displayname, @{N='LinkedOUs';E={$_.gpcfilesyspath}}

# Get GPOs linked to specific OU
Get-DomainGPO -LinkedOU "OU=Workstations,DC=domain,DC=local"

# OUs with their linked GPOs
Get-DomainOU -FullData | Select name, distinguishedName, @{N='GPOs';E={$_.gplink}}

# Resolve GPO links from OU
Get-DomainOU -Identity "OU=Workstations,DC=domain,DC=local" | Select-Object -ExpandProperty gplink

# Find OUs with no GPO linked (potentially unmanaged)
Get-DomainOU | Where-Object {$_.gplink -eq $null -or $_.gplink -eq ""}
```

### GPO Permissions

```powershell
# Get GPO ACLs (who can modify GPOs)
Get-DomainObjectAcl -Identity "CN=Policies,CN=System,DC=domain,DC=local" -ResolveGUIDs

# Get ACL for specific GPO
Get-DomainGPO -Identity "Default Domain Policy" | ForEach-Object {
    Get-DomainObjectAcl -Identity $_.DistinguishedName -ResolveGUIDs
}

# Find GPOs where non-privileged users have write access
Get-DomainGPO | ForEach-Object {
    $gpo = $_
    Get-DomainObjectAcl -Identity $_.DistinguishedName -ResolveGUIDs | Where-Object {
        $_.ActiveDirectoryRights -match "Write" -or
        $_.ActiveDirectoryRights -match "GenericAll" -or
        $_.ActiveDirectoryRights -match "WriteProperty" -or
        $_.ActiveDirectoryRights -match "WriteDACL"
    } | Select @{N='GPO';E={$gpo.DisplayName}}, @{N='Trustee';E={ConvertFrom-SID $_.SecurityIdentifier}}, Rights
}

# Find GPOs with GenericWrite/GenericAll for current user
$userSID = (Get-DomainUser -Identity <username>).objectsid
Get-DomainGPO | ForEach-Object {
    $gpo = $_
    Get-DomainObjectAcl -Identity $_.DistinguishedName -ResolveGUIDs | Where-Object {
        $_.SecurityIdentifier -eq $userSID -and
        ($_.ActiveDirectoryRights -match "Write" -or $_.ActiveDirectoryRights -match "GenericAll")
    } | Select @{N='GPO';E={$gpo.DisplayName}}, Rights
}
```

### GPO Application to Users/Computers

```powershell
# Find GPOs that apply to specific computer
Get-DomainComputer -Identity <computer-name>$ | ForEach-Object {
    $comp = $_
    Get-DomainGPO -ComputerIdentity $_.DistinguishedName | Select DisplayName
}

# Find GPOs that apply to specific user
Get-DomainUser -Identity <username> | ForEach-Object {
    $user = $_
    Get-DomainGPO -UserIdentity $_.DistinguishedName | Select DisplayName
}

# Find computers where a specific GPO applies
Get-DomainGPO -Identity "Workstation Policy" | ForEach-Object {
    $gpo = $_
    Get-DomainComputer -LDAPFilter "(distinguishedName=*$($gpo.displayName)*)" -ErrorAction SilentlyContinue
}

# Get resultant GPOs for a specific OU and its parents
Get-DomainGPO -LinkedOU "OU=Admins,OU=Corp,DC=domain,DC=local" | Select DisplayName
```

## Interesting GPO Settings

### Finding GPOs with Specific Settings

```powershell
# Find GPOs that modify local groups (Restricted Groups)
Get-DomainGPO -FullData | Where-Object {$_.restrictedGroups -ne $null}
Get-DomainGPO -FullData | Where-Object {$_.restrictedGroups -match "Administrators"}

# Find GPOs with logon/logoff scripts
Get-DomainGPO -FullData | Where-Object {$_.scripts -ne $null}
Get-DomainGPO -FullData | Where-Object {$_.scripts -match "script" -or $_.startupScripts -ne $null -or $_.shutdownScripts -ne $null}

# Find GPOs with scheduled tasks
Get-DomainGPO -FullData | Where-Object {$_.scheduledTasks -ne $null}

# Find GPOs with registry settings
Get-DomainGPO -FullData | Where-Object {$_.registrySettings -ne $null}

# Find GPOs with files deployed
Get-DomainGPO -FullData | Where-Object {$_.files -ne $null}
```

### Common Vulnerable GPO Configurations

```powershell
# Find GPOs with AlwaysInstallElevated enabled
# ADM template: EnableUserControl = 1
Get-DomainGPO | Get-DomainObjectAcl -ResolveGUIDs | Where-Object {$_.ObjectDN -match "AlwaysInstallElevated" -or $_.ObjectAceType -match "AlwaysInstallElevated"}

# Find GPOs allowing unconstrained delegation
# ADM template: Microsoft Network Server - LDAP signing / Channel binding
# Security Template: SeMachineAccountPrivilege

# GPOs that add domain users to local admin group
Get-DomainGPO -FullData | Where-Object {$_.restrictedGroups -match "S-1-5-21" -and $_.restrictedGroups -match "Administrators"}

# Find GPOs with AutoAdminLogon setting
# Registry: HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon\AutoAdminLogon
```

### Checking GPO File System Paths

```powershell
# Find GPO file system paths (SYSVOL)
Get-DomainGPO | Select displayname, gpcfilesyspath

# Check access to GPO file system
Get-DomainGPO | ForEach-Object {
    $path = $_.gpcfilesyspath
    if (Test-Path $path) {
        Write-Host "[+] Accessible: $path"
        Get-ChildItem $path -Recurse -ErrorAction SilentlyContinue | Select FullName
    }
}

# Check if we can write to GPO folders
Get-DomainGPO | ForEach-Object {
    $path = $_.gpcfilesyspath
    if (Test-Path $path) {
        $acl = Get-Acl -Path $path
        $acl.Access | Where-Object {$_.IdentityReference -match "DOMAIN\\user" -and $_.FileSystemRights -match "Write"} | Select @{N='GPO';E={$_.DisplayName}}, FileSystemRights
    }
}
```

## GPO Enumeration via SYSVOL

```powershell
# List GPO folders in SYSVOL
Get-ChildItem "\\<dc>\SYSVOL\domain.local\Policies" | Select FullName, Name
Get-ChildItem "\\<dc>\SYSVOL\domain.local\Policies\{GPO-GUID}\Machine" -Recurse
Get-ChildItem "\\<dc>\SYSVOL\domain.local\Policies\{GPO-GUID}\User" -Recurse

# Search SYSVOL for interesting files
Get-ChildItem "\\<dc>\SYSVOL\domain.local" -Recurse -Include "*.ps1", "*.bat", "*.cmd", "*.vbs", "*.xml", "*.inf", "*.pol", "*.ini"

# Find GptTmpl.inf (security settings)
Get-ChildItem "\\<dc>\SYSVOL\domain.local\Policies" -Recurse -Filter "GptTmpl.inf" | ForEach-Object {
    Write-Host "[*] Found: $($_.FullName)"
    Get-Content $_.FullName
}

# Find Registry.pol (registry settings)
Get-ChildItem "\\<dc>\SYSVOL\domain.local\Policies" -Recurse -Filter "Registry.pol" | ForEach-Object {
    Write-Host "[*] Found: $($_.FullName)"
}

# Find scripts
Get-ChildItem "\\<dc>\SYSVOL\domain.local\Policies" -Recurse -Include "*.ps1", "*.bat", "*.vbs", "*.cmd"
```

## AD Module GPO Enumeration

```powershell
# List all GPOs
Get-GPO -All
Get-GPO -All | Select DisplayName, Owner, CreationTime, ModificationTime, GpoStatus

# Specific GPO
Get-GPO -Name "Default Domain Policy"
Get-GPO -Guid "{GPO-GUID}"

# GPO permissions
Get-GPPermissions -Guid "{GPO-GUID}" -All

# GPOs linked to specific OU
Get-GPInheritance -TargetOU "OU=Workstations,DC=domain,DC=local"
Get-GPInheritance -TargetOU "OU=Admins,DC=domain,DC=local" | Select -ExpandProperty GpoLinks

# GPO report (export to XML/HTML)
Get-GPOReport -Name "Default Domain Policy" -ReportType XML
Get-GPOReport -Guid "{GPO-GUID}" -ReportType HTML -Path .\gpo_report.html

# Get GPOs via AD module
Get-ADObject -LDAPFilter "(objectClass=groupPolicyContainer)" -Properties displayName, gPCFileSysPath, gPFunctionalityVersion, versionNumber

# Resultant Set of Policy (RSoP)
gpresult /r
gpresult /r /scope:computer
gpresult /h gpresult.html
```

### AD Module Cmdlets (Requires GPMC)

```powershell
# Requires Group Policy Management Console
Import-Module GroupPolicy

# Get all GPOs
Get-GPO -All

# Backup GPO
Backup-GPO -Name "Workstation Policy" -Path .\GPOBackups

# Copy GPO
Copy-GPO -SourceName "Workstation Policy" -TargetName "New Policy"

# Get GPO report
Get-GPOReport -Name "Default Domain Policy" -ReportType XML -Path .\policy.xml
```

## NetExec GPO Enumeration

```bash
# GPO enumeration via LDAP
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o GPO=1

# GPO interesting permissions
nxc ldap <dc-ip> -u 'user' -p 'pass' -M gpo_info
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o GPO_PERM=1

# Check GPO for vulnerable settings  
nxc ldap <dc-ip> -u 'user' -p 'pass' -M ad_enum -o GPO_VULN=1
```

## GPO Abuse Enumeration Checklist

```powershell
# 1. Enumerate all GPOs
Get-DomainGPO | Select DisplayName, gpcfilesyspath

# 2. Find writable GPOs
$userSID = (Get-DomainUser -Identity <username>).objectsid
Get-DomainGPO | ForEach-Object {
    $gpo = $_
    $acl = Get-DomainObjectAcl -Identity $_.DistinguishedName -ResolveGUIDs
    if ($acl.SecurityIdentifier -contains $userSID -or $acl | Where-Object {$_.ActiveDirectoryRights -match "Write" -or $_.ActiveDirectoryRights -match "GenericAll"}) {
        Write-Host "[VULN] $($gpo.DisplayName) is writable by you!" -ForegroundColor Red
        $gpo | Select DisplayName, gpcfilesyspath
    }
}

# 3. Find GPOs with Apply Group Policy to non-privileged users
Get-DomainGPO | ForEach-Object {
    $gpo = $_
    $path = $_.gpcfilesyspath
    if ($path -and (Test-Path $path)) {
        $gpreport = [xml](Get-Content "$path\gpreport.xml" -ErrorAction SilentlyContinue)
        if ($gpreport) {
            # Check for vulnerable settings
            $gpreport
        }
    }
}

# 4. Find GPOs linked to critical OUs (Domain Controllers, Admins)
Get-DomainOU | Where-Object {$_.distinguishedName -match "Domain Controllers|Admins|Servers|Privileged"} | ForEach-Object {
    $ou = $_
    Write-Host "[*] OU: $($ou.Name)"
    Get-DomainGPO -LinkedOU $_.distinguishedName | Select DisplayName
}

# 5. Check GPO file paths for writeable content
Get-DomainGPO | ForEach-Object {
    $gpo = $_
    $path = $_.gpcfilesyspath
    if ($path -and (Test-Path $path)) {
        $canwrite = (Get-Acl "$path\*" -ErrorAction SilentlyContinue).Access | Where-Object {
            $_.IdentityReference -match "DOMAIN\\" -and
            $_.FileSystemRights -match "Write" -and
            $_.AccessControlType -eq "Allow"
        }
        if ($canwrite) {
            Write-Host "[+] Writeable GPO files: $path" -ForegroundColor Yellow
        }
    }
}
```

## GPO Enumeration via LDAP

```powershell
# LDAP search for all GPOs
$gpoSearch = New-Object DirectoryServices.DirectorySearcher([ADSI]"LDAP://domain.local")
$gpoSearch.Filter = "(objectClass=groupPolicyContainer)"
$gpoSearch.PropertiesToLoad.AddRange(@("displayName", "gPCFileSysPath", "versionNumber", "flags"))
$gpResults = $gpoSearch.FindAll()

foreach ($gpo in $gpResults) {
    Write-Host "GPO: $($gpo.Properties.displayname)"
    Write-Host "  Path: $($gpo.Properties.gpcfilesyspath)"
    Write-Host "  Version: $($gpo.Properties.versionnumber)"
    Write-Host ""
}
```

## GPO Enumeration Script (Complete)

```powershell
# Comprehensive GPO enumeration script
$report = @()

# All GPOs
Write-Host "[*] Enumerating all GPOs..."
Get-DomainGPO -FullData | ForEach-Object {
    $gpo = $_
    $report += [PSCustomObject]@{
        GPO = $gpo.DisplayName
        Path = $gpo.gpcfilesyspath
        Version = $gpo.versionNumber
        Created = $gpo.whenCreated
        Modified = $gpo.whenChanged
    }
}

# Writable GPOs for low-priv users
Write-Host "[*] Checking writable GPOs..."
Get-DomainGPO | ForEach-Object {
    $gpo = $_
    Get-DomainObjectAcl -Identity $_.DistinguishedName -ResolveGUIDs | Where-Object {
        $_.ActiveDirectoryRights -match "Write|GenericAll|WriteProperty|WriteDACL"
    } | ForEach-Object {
        $report += [PSCustomObject]@{
            GPO = $gpo.DisplayName
            Path = $gpo.gpcfilesyspath
            Note = "Writable by $((ConvertFrom-SID $_.SecurityIdentifier))"
        }
    }
}

# Vulnerable settings
Write-Host "[*] Checking vulnerable GPO settings..."
Get-DomainGPO -FullData | Where-Object {$_.restrictedGroups -ne $null -or $_.scripts -ne $null -or $_.scheduledTasks -ne $null -or $_.registrySettings -ne $null} | ForEach-Object {
    $report += [PSCustomObject]@{
        GPO = $_.DisplayName
        Path = $_.gpcfilesyspath
        Note = "Contains scripts/tasks/reg settings"
    }
}

$report | Format-Table -AutoSize
$report | Export-CSV gpo_enumeration.csv -NoTypeInformation
```

## GPO Abuse Techniques (Enumeration Phase)

### Identifying GPO for Abuse

```powershell
# 1. Find writable GPO
# If you can write to a GPO, you can add logon scripts, scheduled tasks, or modify security settings
Get-DomainGPO | ForEach-Object {
    $gpo = $_
    $gpoPath = $_.gpcfilesyspath
    # Check if you can write to the GPO folder
    $canWrite = Test-Path $gpoPath -ErrorAction SilentlyContinue
    if ($canWrite) {
        try {
            $testFile = "$gpoPath\test_write_$(Get-Random).txt"
            [System.IO.File]::WriteAllText($testFile, "test")
            Remove-Item $testFile -Force
            Write-Host "[VULNERABLE] Write access to: $($gpo.DisplayName) ($gpoPath)" -ForegroundColor Red
        } catch {
            Write-Host "[?] No write access to: $($gpo.DisplayName)"
        }
    }
}

# 2. Find GPO that applies to Domain Controllers or Admin workstations
Get-DomainGPO -LinkedOU "OU=Domain Controllers,DC=domain,DC=local" | Select DisplayName

# 3. Find GPO with logon scripts (can replace)
Get-DomainGPO -FullData | Where-Object {$_.scripts -ne $null} | Select DisplayName, gpcfilesyspath
```

## Stealth / OPSEC Considerations

- **GPO enumeration triggers LDAP queries**: Each GPO query can generate Event 4662 on the DC
- **SYSVOL access**: Browsing SYSVOL shares generates Event 5140/5145 (SMB share access)
- **gpresult**: Running locally is quiet but only shows applied GPOs; requires no network queries
- **GPMC queries**: Using Group Policy Management Console generates many LDAP queries and logs
- **Write testing**: Writing test files to SYSVOL/GPO folders generates Event 4663 (file write)
- **Large domains**: Full GPO enumeration can be heavy; scope to interesting OUs first
- **GPO script modification**: If you modify a script in SYSVOL, it will execute across all target systems when Group Policy refreshes (every 90-120 min by default, or at reboot)

## Detection Notes

| Activity | Event ID | Notes |
|----------|----------|-------|
| GPO read (LDAP) | 4662 | Directory Service Access on groupPolicyContainer |
| SYSVOL file read | 5140, 5145 | SMB share access to \\\\DC\\SYSVOL |
| Write to SYSVOL | 4663, 5145 | File write to SYSVOL share |
| GPO refresh (from DC) | 8000+ | Group Policy application events on clients |
| GPO permission change | 5136 | Directory Service Change on GPO |
| PowerShell GPO cmdlets | 4104 | ScriptBlock logging captures GPO operations |
| gpresult execution | 4688 | Process creation (can be low severity) |
| GPUpdate execution | 4688 | Manual group policy update |

## Quick Reference

```powershell
# All GPOs
Get-DomainGPO | Select DisplayName, gpcfilesyspath

# GPOs linked to critical OUs
Get-DomainGPO -LinkedOU "OU=Domain Controllers,DC=domain,DC=local"
Get-DomainGPO -LinkedOU "OU=Servers,DC=domain,DC=local"

# Check GPO permissions
Get-DomainGPO | ForEach-Object { Get-DomainObjectAcl -Identity $_.DistinguishedName -ResolveGUIDs | Where-Object {$_.ActiveDirectoryRights -match "Write"} } | Format-Table

# GPOs with restricted groups
Get-DomainGPO -FullData | Where-Object {$_.restrictedGroups -ne $null}

# GPOs with scripts
Get-DomainGPO -FullData | Where-Object {$_.scripts -ne $null}

# SYSVOL browsing
dir \\<dc>\SYSVOL\domain.local\Policies

# Search for scripts in SYSVOL
Get-ChildItem "\\<dc>\SYSVOL\domain.local" -Recurse -Include *.ps1, *.bat, *.vbs, *.cmd

# GPO report (AD Module)
Get-GPOReport -Name "Default Domain Policy" -ReportType HTML

# NetExec GPO
nxc ldap <dc> -u 'user' -p 'pass' -M ad_enum -o GPO=1

# GPO permission check
nxc ldap <dc> -u 'user' -p 'pass' -M gpo_info

# Writable GPOs for current user
$sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User.Value
Get-DomainObjectAcl -ResolveGUIDs -LDAPFilter "(objectClass=groupPolicyContainer)" | Where-Object {$_.SecurityIdentifier -eq $sid -and $_.ActiveDirectoryRights -match "Write|GenericAll"} | Format-Table
```
