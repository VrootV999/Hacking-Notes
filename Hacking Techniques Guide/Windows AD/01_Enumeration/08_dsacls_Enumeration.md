# Enumerating AD Object Permissions with dsacls

## Overview

`dsacls` is a native Windows command-line tool for viewing and managing Active Directory ACLs (Access Control Lists). It is part of the AD DS Tools (RSAT) and provides granular visibility into who has what permissions on AD objects. Unlike PowerView or the AD PowerShell module, `dsacls` is a native Microsoft tool that is less likely to be flagged by EDR/AV.

### Why Use dsacls

- **Native** — Ships with Windows (with RSAT installed)
- **Stealthy** — Less suspicious than PowerView or third-party tools
- **Detailed** — Shows ACE types, inheritance flags, and GUIDs
- **Scriptable** — Can be automated in batch scripts
- **Available** — Works on any Windows system with AD DS Tools installed

## Installation

### Via PowerShell (Windows Server 2012+)

```powershell
# Install AD DS Tools (includes dsacls)
Install-WindowsFeature RSAT-ADDS

# For Windows 10/11
Add-WindowsCapability -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0 -Online
```

### Via GUI

```
Control Panel → Programs → Turn Windows features on or off
→ Remote Server Administration Tools → Role Administration Tools
→ AD DS and AD LDS Tools → AD DS Tools
```

## Basic Syntax

```cmd
dsacls "DN_of_Object"
```

The Distinguished Name (DN) is the LDAP path to the object:

```
dsacls "CN=User1,CN=Users,DC=domain,DC=local"
dsacls "OU=Servers,DC=domain,DC=local"
dsacls "DC=domain,DC=local"
```

## Common Usage Examples

### Enumerate Domain Root ACL

```cmd
dsacls "DC=domain,DC=local"
```

Output example:
```
Access list:
Allow BUILTIN\Administrators SPECIAL ACCESS
  READ PROPERTY
  WRITE PROPERTY
  LIST CONTENTS
  LIST OBJECT
  CREATE CHILD
  DELETE CHILD
  DELETE
  WRITE DACL
  WRITE OWNER
  CONTROL ACCESS

Allow NT AUTHORITY\ENTERPRISE DOMAIN CONTROLLERS SPECIAL ACCESS
  READ PROPERTY
  LIST CONTENTS
  LIST OBJECT
  CONTROL ACCESS

Allow NT AUTHORITY\Authenticated Users SPECIAL ACCESS
  READ PROPERTY
  LIST CONTENTS
  LIST OBJECT

Allow Everyone SPECIAL ACCESS
  READ PROPERTY
  LIST CONTENTS
  LIST OBJECT
```

### Enumerate Specific Object ACL

```cmd
dsacls "CN=Administrator,CN=Users,DC=domain,DC=local"
```

```
Access list:
Allow BUILTIN\Administrators FULL CONTROL
Allow DOMAIN\Domain Admins FULL CONTROL
Allow DOMAIN\Enterprise Admins FULL CONTROL
Allow NT AUTHORITY\SYSTEM FULL CONTROL
Allow NT AUTHORITY\SELF SPECIAL ACCESS
  READ PROPERTY
  WRITE PROPERTY
  ...
```

### Enumerate an Organizational Unit

```cmd
dsacls "OU=Servers,DC=domain,DC=local"
```

### Enumerate Group ACL

```cmd
dsacls "CN=Domain Admins,CN=Users,DC=domain,DC=local"
```

### Enumerate AdminSDHolder

```cmd
dsacls "CN=AdminSDHolder,CN=System,DC=domain,DC=local"
```

AdminSDHolder is critical — its ACL propagates to all protected accounts:

```
Access list:
Allow BUILTIN\Administrators FULL CONTROL
Allow DOMAIN\Domain Admins FULL CONTROL
Allow DOMAIN\Enterprise Admins FULL CONTROL
Allow NT AUTHORITY\SYSTEM FULL CONTROL
-- Additional ACEs added by attackers for persistence --
```

## Output Interpretation

### ACE Types

| Ace Type | Meaning |
|----------|---------|
| `ALLOW` | Allow access with specified rights |
| `DENY` | Deny access (takes precedence over ALLOW) |
| `ALLOWED` | Explicitly allowed (synonym) |
| `DENIED` | Explicitly denied (synonym) |

### Rights

| Right | Hex | Description |
|-------|-----|-------------|
| `FULL CONTROL` | 0xF01FF | All operations |
| `GENERIC_ALL` | 0x10000000 | Full access |
| `GENERIC_READ` | 0x20000000 | Read access |
| `GENERIC_WRITE` | 0x40000000 | Write access |
| `GENERIC_EXECUTE` | 0x80000000 | Execute access |
| `SPECIAL ACCESS` | Varies | Custom rights (listed individually) |
| `READ PROPERTY` | 0x00000010 | Read attribute values |
| `WRITE PROPERTY` | 0x00000020 | Write attribute values |
| `LIST CONTENTS` | 0x00000004 | List child objects |
| `LIST OBJECT` | 0x00000008 | List object in directory |
| `CREATE CHILD` | 0x00000001 | Create child objects |
| `DELETE CHILD` | 0x00000002 | Delete child objects |
| `DELETE` | 0x00010000 | Delete the object |
| `WRITE DACL` | 0x00040000 | Modify permissions |
| `WRITE OWNER` | 0x00080000 | Take ownership |
| `CONTROL ACCESS` | 0x00000100 | Extended rights |

### Inheritance Flags

| Flag | Meaning |
|------|---------|
| `CONTAINER_INHERIT_ACE` | Inherited by child containers |
| `OBJECT_INHERIT_ACE` | Inherited by child leaf objects |
| `INHERITED_ACE` | Inherited from parent |
| `INHERIT_ONLY_ACE` | Does not apply to this object, only children |
| `NO_PROPAGATE_INHERIT_ACE` | Prevent further inheritance propagation |

### Extended Rights (Control Access Rights)

| Right | GUID | Purpose |
|-------|------|---------|
| `DS-Replication-Get-Changes` | 1131f6ad-9c07-11d1-f79f-00c04fc2dcd2 | DCSync (with other right) |
| `DS-Replication-Get-Changes-All` | 1131f6ae-9c07-11d1-f79f-00c04fc2dcd2 | DCSync (all data) |
| `DS-Replication-Get-Changes-In-Filtered-Set` | 89e95b76-444d-4c62-991a-0facbeda640c | DCSync (filtered) |
| `User-Force-Change-Password` | 00299570-246d-11d0-a768-00aa006e0529 | Force password change |
| `Send-As` | ab721a56-1e2f-11d0-9819-00aa0040529b | Send as another user |

## vs Other ACL Enumeration Tools

| Tool | Native? | Granularity | Output | Stealth |
|------|:-------:|:-----------:|:------:|:-------:|
| **dsacls** | Yes | High | Text | High |
| **PowerView Get-DomainObjectAcl** | No | High | Objects | Medium |
| **AD Module Get-Acl** | Yes (RSAT) | High | Objects | Medium |
| **ADSI Edit** | Yes | Very High | GUI | N/A |
| **ADExplorer** | No | Very High | GUI | Low |

### PowerView Equivalent

```powershell
# PowerView — More parsing-friendly
Get-DomainObjectAcl -Identity "CN=AdminSDHolder,CN=System,DC=domain,DC=local" -ResolveGUIDs
```

### AD Module Equivalent

```powershell
# AD PowerShell module
Get-Acl -Path "AD:CN=AdminSDHolder,CN=System,DC=domain,DC=local" | Format-List
```

### DSACLs Advantages

- Works in cmd.exe without PowerShell
- Native tool — not blocked by AppLocker/SCR
- Lower detection risk for EDR
- Available on Server Core installations with RSAT

### DSACLs Disadvantages

- Text output — harder to parse programmatically
- No GUID resolution for extended rights
- No recursive enumeration built-in
- Requires RSAT installation (not always present)

## Scripting dsacls for Bulk Enumeration

### Batch Script — Dump All OU ACLs

```batch
@echo off
REM Dump ACLs for all OUs in the domain
for /f "tokens=*" %%i in ('dsquery ou -limit 10000') do (
    echo ========================================
    echo %%i
    echo ========================================
    dsacls "%%i" > "ou_%%~nxi.txt"
)
```

### Batch Script — Dump All User ACLs

```batch
@echo off
REM Dump ACLs for all users
for /f "tokens=*" %%i in ('dsquery user -limit 10000') do (
    dsacls "%%i" > "user_%%~nxi_acl.txt"
)
```

### Batch Script — Find DELEGATE Permissions

```batch
@echo off
REM Find objects with non-default permissions
REM Good starting point for finding privilege escalation paths
dsacls "DC=domain,DC=local" | findstr /i "allow" > domain_aces.txt
```

### PowerShell Wrapper for dsacls

```powershell
# PowerShell function to wrap dsacls
function Get-DsaclsACL {
    param($DN)
    $output = dsacls $DN
    $result = [PSCustomObject]@{
        DistinguishedName = $DN
        RawACL = $output
    }
    return $result
}

# Use it
Get-DsaclsACL "CN=AdminSDHolder,CN=System,DC=domain,DC=local"
```

### Recursive Enumeration with dsacls and dsquery

```batch
@echo off
REM Step 1: Dump all objects in the domain
dsquery * "DC=domain,DC=local" -limit 10000 > all_objects.txt

REM Step 2: Get ACLs for each object
for /f "tokens=*" %%i in (all_objects.txt) do (
    dsacls "%%i" >> all_acl_output.txt
)

REM Step 3: Search for interesting permissions
findstr /i "generic_all generic_write full_control" all_acl_output.txt
```

## Use Cases

### 1. Find Who Has GenericWrite on High-Value Objects

```cmd
dsacls "CN=Domain Admins,CN=Users,DC=domain,DC=local" | findstr /i "generic_all full_control write"
```

### 2. Check AdminSDHolder for Persistence

```cmd
dsacls "CN=AdminSDHolder,CN=System,DC=domain,DC=local"
```

Look for:
- Non-standard principals (not Domain Admins, Enterprise Admins, SYSTEM)
- Any user with FULL CONTROL or WRITE PROPERTY
- ACEs that seem out of place

### 3. Audit DCSync Rights

```cmd
dsacls "DC=domain,DC=local" | findstr /i "replication"
```

Look for `DS-Replication-Get-Changes` and `DS-Replication-Get-Changes-All` rights. Any principal with both can DCSync.

### 4. Check If a Specific User Has Privileges

```cmd
dsacls "CN=TargetUser,CN=Users,DC=domain,DC=local" | findstr /i "DOMAIN\AttackerUser"
```

### 5. Find Objects with Non-Default ACLs

```cmd
REM Compare AdminSDHolder ACL against default
dsacls "CN=AdminSDHolder,CN=System,DC=domain,DC=local" > adminsdholder_acl.txt

REM Compare with a known-good backup to find modifications
```

## Detection Considerations

### dsacls Usage Detection

- `dsacls.exe` is a legitimate administrative tool
- Bulk enumeration may be detected as anomalous
- Event ID 4662 — Directory Service Access will fire for each object read
- High volumes of 4662 events in a short window indicate enumeration

```powershell
# Detect bulk AD object reads
Get-WinEvent -FilterHashtable @{LogName="Security"; ID=4662} |
    Group-Object @{e={$_.Properties[1].Value}} |
    Where-Object Count -gt 100
```

### dsacls vs PowerView Detection

| Tool | Detection Risk | Reason |
|------|:--------------:|--------|
| dsacls | Low | Native Microsoft tool |
| PowerView | Medium-High | Known malicious tool |
| AD Module Get-Acl | Low-Medium | PowerShell but legitimate |
| ADSI Edit | Low | Native MMC snap-in |

## Alternative: Get-Acl PowerShell Cmdlet

If PowerShell is available, `Get-Acl` can be used with the AD provider:

```powershell
# Requires AD PowerShell module (RSAT)
Import-Module ActiveDirectory

# Get ACL for a specific object
Get-Acl -Path "AD:CN=User1,CN=Users,DC=domain,DC=local" | Format-List

# Get ACL for domain root
Get-Acl -Path "AD:DC=domain,DC=local" | Format-List

# Parse ACEs
$acl = Get-Acl -Path "AD:CN=User1,CN=Users,DC=domain,DC=local"
$acl.Access | ForEach-Object {
    [PSCustomObject]@{
        Identity = $_.IdentityReference
        Rights = $_.ActiveDirectoryRights
        Type = $_.AccessControlType
        Inherited = $_.IsInherited
    }
}
```

### Advantages of Get-Acl

- Structured output (objects, not text)
- Better for scripting and parsing
- Can filter and sort programmatically
- Supports recursive enumeration

### Disadvantages

- Requires AD PowerShell module (RSAT)
- More likely to be logged by PowerShell logging
- Blocked by some AppLocker/SCR policies

## Cross-References

- [ACL Enumeration](./03_ACL_Enumeration.md)
- [BloodHound / SharpHound](./06_BloodHound_SharpHound.md)
- [LDAP Queries](./07_LDAP_Queries.md)
- [AdminSDHolder Attack](../05_Privilege_Escalation/03_AdminSDHolder.md)
- [DCSync Attack](../03_Credential_Access/01_DCSync.md)
- [Tools Reference](../09_Tools_Reference/README.md)
