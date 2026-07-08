# Windows Active Directory Persistence Techniques

## Overview

Once an attacker gains privileged access to an Active Directory environment (Domain Admin, Enterprise Admin, or local admin on a Domain Controller), establishing persistent access is critical to maintain a foothold even after the initial compromise vector is closed.

This section covers **10 major persistence techniques** in Windows AD environments, ranging from Kerberos ticket manipulation to Group Policy backdoors.

## Techniques Matrix

| # | Technique | Privilege Required | Interacts With DC | Persistence Type | Stealth |
|---|-----------|-------------------|-------------------|-----------------|---------|
| 1 | Golden Ticket | Domain Admin / KRBTGT hash | No (forged offline) | Kerberos ticket | Low - forged TGTs detectable |
| 2 | Silver Ticket | Service account hash | No (forged offline) | Kerberos ticket | Medium - no DC traffic |
| 3 | DSRM Backdoor | Domain Admin (DC local admin) | Yes (registry on DC) | Local/Registry | Medium - local to DC |
| 4 | Skeleton Key | Domain Admin (on DC) | Yes (on DC memory) | In-memory | Low - reboot clears |
| 5 | DCShadow | Enterprise Admin | Yes (push objects) | AD object replication | Low - mimics DC replication |
| 6 | AdminSDHolder | Domain Admin | Yes (ACL modification) | AD ACL | High - propagates to protected groups |
| 7 | SSP Backdoor | System on DC | Yes (DLL + registry) | DLL + Registry | Low - persists reboots |
| 8 | Certificate Forging | CA Admin / Enterprise Admin | Yes (CA abuse) | PKI trust chain | High - trusted by everything |
| 9 | Group Policy | Domain Admin | Yes (GPO creation) | GPO/SYSVOL | High - domain-wide execution |
| 10 | Shadow Credentials | Domain Admin / AD CS access | Yes (CA or cert auth) | Certificate-based | High - no hash required |

## General Prerequisites

- **Domain Admin** or **Enterprise Admin** privileges for most techniques
- Network access to Domain Controllers
- Tools: Mimikatz, Impacket, Rubeus, PowerView, Active Directory module, Certify
- Execution context: **Elevated command prompt / PowerShell** on a Domain Controller or domain-joined machine

## Detection & Response Summary

| Technique | Key Event IDs | Primary Artifacts |
|-----------|--------------|-------------------|
| Golden Ticket | 4768, 4769 (anomalous) | Kerberos TGT with forged timestamps |
| Silver Ticket | 4769 (no preceding 4768) | TGS request without TGT |
| DSRM Backdoor | 4657 (registry change) | DsrmAdminLogonBehavior registry key |
| Skeleton Key | No specific event | Mimikatz DLL in LSASS, failed logins |
| DCShadow | 4742, 5136, 4928-4933 | Abnormal replication from non-DC |
| AdminSDHolder | 5136, 5141 | Modified ACL on AdminSDHolder object |
| SSP Backdoor | 4657 (registry), new DLL | SSP DLL in System32, LSA registry keys |
| Certificate | 4886-4899 | Forged/unauthorized certs in AD CS |
| Group Policy | 5136, 5141 | Modified GPO files in SYSVOL |
| Shadow Credentials | 5136, 4662 | KeyCredentialLink attribute modification |

## Tooling Reference

### Mimikatz
```
mimikatz.exe
privilege::debug
```

### Impacket
```bash
# ticketer.py - part of Impacket
python3 ticketer.py ...
```

### Rubeus
```
Rubeus.exe golden ...
Rubeus.exe silver ...
```

### PowerView / ActiveDirectory Module
```powershell
# PowerView (part of PowerSploit / Empire)
Get-DomainUser
Add-DomainObjectAcl

# Active Directory PowerShell Module
Import-Module ActiveDirectory
Get-ADUser
```

### Certify
```
Certify.exe find ...
Certify.exe request ...
```

## Cleanup General Notes

- Restore modified ACLs, registry keys, and GPOs to original state
- Reset KRBTGT password twice to invalidate Golden Tickets
- Rotate all service account passwords after Silver Ticket use
- Remove rogue SSP DLLs from `C:\Windows\System32`
- Delete malicious GPOs and force `gpupdate /force`
- Revoke forged certificates from CA
- Restart Domain Controllers after in-memory changes (skeleton key)

---

**Next:** [01 - Golden Ticket](01_Golden_Ticket_Persistence.md)
