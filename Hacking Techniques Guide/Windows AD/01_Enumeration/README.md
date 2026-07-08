# Windows AD Enumeration Phase

## Overview

Enumeration is the most critical phase of any Active Directory assessment. The goal is to map the AD environment, identify misconfigurations, and find attack paths that lead to privilege escalation or credential access. This phase spans pre-compromise (unauthenticated) and post-compromise (authenticated) techniques.

## General Methodology

```
1. Initial Recon (no creds)     → DNS, SMB null, anonymous LDAP, RID cycling
2. Domain Enum (with creds)     → Users, Groups, Computers, GPOs, OUs, trusts
3. ACL/ACE Enum                 → Interesting permissions, delegation, GenericAll/Write
4. Trust Enum                   → Domain/forest trusts, SID filtering, trust keys
5. GPO Enum                     → Misconfigurations, vulnerable GPOs
6. BloodHound/SharpHound        → Graph-based analysis, attack path mapping
7. LDAP Queries                 → Deep-dive manual LDAP searches
```

## Enumeration Targets Checklist

### Users
- [ ] All domain users (samaccountname, cn, upn, sid, enabled/disabled)
- [ ] Kerberoastable accounts (ServicePrincipalName set)
- [ ] AS-REP roastable accounts (DoesNotRequirePreAuth)
- [ ] Accounts with adminCount > 0 (protected/privileged users)
- [ ] Accounts with sidHistory set
- [ ] Accounts with unconventionally high badPwdCount
- [ ] Accounts with password not required (PasswordNotRequired)
- [ ] Accounts with reversible encryption
- [ ] Accounts without Kerberos pre-auth
- [ ] Accounts with TrustedForDelegation / TrustedToAuthForDelegation
- [ ] Accounts with constrained/unconstrained delegation
- [ ] Service accounts (managed service accounts, gMSA)
- [ ] Domain Admin & Enterprise Admin group members
- [ ] Highly privileged group memberships
- [ ] Account descriptions containing potential secrets

### Groups
- [ ] All security/distribution groups
- [ ] Nested group memberships
- [ ] Admin groups (Domain Admins, Enterprise Admins, Schema Admins)
- [ ] Builtin privileged groups (Account Operators, Backup Operators, Server Operators)
- [ ] Group Managed Service Accounts group
- [ ] "Foreign" security principals (trust-linked groups)
- [ ] ACL-enabled groups with special permissions

### Computers
- [ ] All domain-joined computers (name, OS, version, last logon)
- [ ] Domain Controllers
- [ ] SQL servers, web servers, file servers
- [ ] Systems with unconstrained delegation
- [ ] Systems with constrained delegation (allowed-to-delegate-to)
- [ ] Systems with LAPS enabled (ms-Mcs-AdmPwdExpirationTime present)
- [ ] Systems with adminCount > 0
- [ ] Systems with operating system versions (find legacy/outdated)
- [ ] Systems with IPv4/IPv6 addresses

### Domain Controllers
- [ ] DC names and IP addresses
- [ ] Functional levels (domain/forest)
- [ ] DC OS versions
- [ ] DC site/subnet information
- [ ] DC services (DNS, KDC, LDAP, GC)

### GPOs
- [ ] All GPOs and their linked OUs
- [ ] GPOs with interesting permissions (ApplyGroupPolicy to non-privileged users)
- [ ] GPOs that modify local admin groups (Restricted Groups)
- [ ] GPOs with scheduled tasks
- [ ] GPOs with logon scripts
- [ ] GPOs with registry settings for AutoAdminLogon
- [ ] GPOs allowing unconstrained delegation
- [ ] GPOs with vulnerable settings (AlwaysInstallElevated, etc.)

### OUs
- [ ] All Organizational Units
- [ ] OUs with delegation (ACLs granting users control over OUs)
- [ ] OUs containing privileged/workstation/servers
- [ ] OUs with GPO links

### Trusts
- [ ] Domain trusts (direction, type, SID filtering)
- [ ] Forest trusts (direction, transitive)
- [ ] Trust relationships with non-AD Kerberos realms
- [ ] SIDHistory on trust relationships
- [ ] Trust keys (rc4/aes)
- [ ] External trusts to third-party domains

### ACLs / Delegation
- [ ] GenericAll on users/groups/computers/domains
- [ ] GenericWrite on users/groups/computers
- [ ] WriteOwner on objects
- [ ] WriteDACL on objects
- [ ] AllExtendedRights
- [ ] ForceChangePassword (User-Force-Change-Password)
- [ ] Self-Membership (Self writes to group memberships)
- [ ] DS-Replication-Get-Changes (DCSync rights)
- [ ] DS-Replication-Get-Changes-All (DCSync extended rights)
- [ ] Write to SPN (allows Kerberoastable attacks)
- [ ] WriteServicePrincipalName
- [ ] Validated-SPN
- [ ] Allowing logon scripts to be modified
- [ ] Group delegation (control over groups granting access)

### Delegations
- [ ] Unconstrained delegation (trusted for delegation)
- [ ] Constrained delegation (allowed-to-delegate-to)
- [ ] Resource-based constrained delegation
- [ ] Protocol transition enabled (TrustedToAuthForDelegation)

### SPNs
- [ ] All registered SPNs (service/MSSQLSvc, http, cifs, ldap, host, etc.)
- [ ] Duplicate SPNs
- [ ] SPNs linked to user accounts (potential Kerberoast)
- [ ] SPNs for high-value services

### Certificates (ADCS)
- [ ] CA servers
- [ ] Certificate templates with vulnerable settings
- [ ] ESC1-ESC13 vulnerabilities
- [ ] CA security settings (ACLs on CA object)

## Tool Categories

| Category | Tools |
|----------|-------|
| No-Creds Recon | nmap, enum4linux-ng, ldapsearch, nxc smb/ldap (null auth) |
| Command-line Enum | PowerView, AD Module, NetExec |
| Graph Analysis | BloodHound + SharpHound |
| LDAP Queries | ldapsearch, ADSI, AdFind, pyldapsearch |
| ACL Specific | PowerView (Get-DomainObjectAcl), BloodHound, AD ACLScanner |
| Trust Enum | PowerView, ntdsutil, netdom |
| GPO Enum | PowerView, GPMC (Group Policy Management Console) |
| Proxy/Relay | Responder, Inveigh, mitm6 |

## OPSEC Considerations

- **Stealthy enumeration**: Use LDAP queries with filters instead of dumping everything; avoid creating noisy event logs (Event ID 4625 for failed logins, 4662 for ACL access)
- **Timing**: Space out queries to avoid triggering threshold-based detections
- **Tool selection**: AD Module cmdlets may be logged via PowerShell ScriptBlock Logging; PowerView may be flagged by AV/EDR
- **Network**: Unauthenticated scans from external IPs will be logged; SMB null sessions often blocked in modern environments
- **BloodHound**: SharpHound with `-c DCOnly` is quieter than `-c All` (avoids connecting to every workstation)
- **LDAP queries**: Use filters to limit results; avoid `(objectClass=*)` wildcards on large domains

## Detection Notes for Blue Teams

| Activity | Event ID | Source |
|----------|----------|--------|
| Account enumeration (bad pw count) | 4625, 4771 | Security Log |
| LDAP query | 4662 | Security Log (Audit DS Access) |
| Group membership enumeration | 4799 | Security Log |
| Nmap scan | 5152, 5154 | Windows Filtering Platform |
| Anonymous SMB connection | 5140 | Security Log |
| PowerShell module load | 4104 | PowerShell ScriptBlock Logging |
| SharpHound execution | 4104, 4688 | PowerShell/Security |
| RID cycling | 4625 | Security Log |
| Kerberos TGS-REQ (Kerberoast listen) | 4769 | Security Log |
| AS-REP (ASREPRoast) | 4768 | Security Log |
| BloodHound ingestion | 4688, 4104 | Security/PowerShell |

## Command Reference Map

| Goal | Tool | Syntax |
|------|------|--------|
| All Users | PowerView | `Get-DomainUser` |
| All Users | AD Module | `Get-ADUser -Filter *` |
| All Users | NetExec | `nxc ldap dc -u user -p pass --users` |
| SPN Users (Kerberoast) | PowerView | `Get-DomainUser -SPN` |
| No-Preauth (ASREPRoast) | PowerView | `Get-DomainUser -PreauthNotRequired` |
| All Groups | PowerView | `Get-DomainGroup` |
| All Computers | PowerView | `Get-DomainComputer` |
| Domain Trusts | PowerView | `Get-DomainTrust` |
| All GPOs | PowerView | `Get-DomainGPO` |
| OUs | PowerView | `Get-DomainOU` |
| Object ACLs | PowerView | `Get-DomainObjectAcl` |
| Interesting ACLs | PowerView | `Find-InterestingDomainAcl` |
| Unconstrained Delegation | PowerView | `Get-DomainComputer -Unconstrained` |
| Constrained Delegation | PowerView | `Get-DomainUser -TrustedToAuth` |
| DCSync Rights | PowerView | `Get-DomainObjectAcl -ResolveGUIDs` |
| AdminCount Objects | PowerView | `Get-DomainUser -AdminCount` |
| Share Find | PowerView | `Invoke-ShareFinder` |
| Local Admins | PowerView | `Invoke-EnumerateLocalAdmin` |
| Logged On Users | PowerView | `Get-NetLoggedon` |
| RDP Sessions | PowerView | `Get-NetRDPSession` |
| Domain Admin list | PowerView | `Get-DomainGroupMember "Domain Admins"` |
| Forest Trusts | PowerView | `Get-ForestTrust` |

## Technique Files

| # | File | Description |
|---|------|-------------|
| 01 | [Initial Recon (No Creds)](01_Initial_Recon_No_Creds.md) | Unauthenticated AD reconnaissance |
| 02 | [Domain Enumeration](02_Domain_Enumeration.md) | Authenticated domain user/group/computer enumeration |
| 03 | [ACL Enumeration](03_ACL_Enumeration.md) | Access control list and ACE analysis |
| 04 | [Trust Enumeration](04_Trust_Enumeration.md) | Domain and forest trust relationship enumeration |
| 05 | [GPO Enumeration](05_GPO_Enumeration.md) | Group Policy Object enumeration and analysis |
| 06 | [BloodHound / SharpHound](06_BloodHound_SharpHound.md) | Graph-based attack path mapping |
| 07 | [LDAP Queries](07_LDAP_Queries.md) | Deep-dive manual LDAP search techniques |
| 08 | [dsacls Enumeration](08_dsacls_Enumeration.md) | ACL enumeration using dsacls command |
