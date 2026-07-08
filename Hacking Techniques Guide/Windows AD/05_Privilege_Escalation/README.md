# Windows AD Privilege Escalation

## Overview

Privilege escalation in Active Directory environments spans two broad categories: **local** (gaining SYSTEM/Administrator on a single host) and **domain** (gaining Domain Admin or equivalent across the AD forest). These notes cover both paths, from basic Windows local privesc to advanced Kerberos delegation attacks.

## Privesc Methodology

```
1. Local Privesc (current host)     → WinPEAS, SeatBelt, PowerUp
2. ACL Abuse (AD objects)           → ForceChangePassword, GenericAll, WriteDACL
3. AdminSDHolder / SDProp           → Backdoor privileged groups
4. Kerberos Delegation              → Unconstrained, Constrained, RBCD
5. Group Membership Abuse           → DnsAdmins, Backup Operators, etc.
6. LAPS / LAPS Escalation           → Read LAPS passwords, ESC1-ESC13
```

## Attack Mapping by Goal

| Goal | Technique | Tooling |
|------|-----------|---------|
| Local SYSTEM | Token Impersonation | RogueWinRM, JuicyPotato, PrintSpoofer |
| Local SYSTEM | Unquoted Service Paths | PowerUp, manual |
| Local SYSTEM | Modifiable Service | PowerUp, sc config |
| Local SYSTEM | DLL Hijacking | Process Monitor, procmon |
| Local Admin | AlwaysInstallElevated | PowerUp |
| Local Admin | Modifiable Service Binary | PowerUp, icacls |
| Domain Admin | ForceChangePassword | PowerView, net user |
| Domain Admin | GenericAll on Group | PowerView, Add-DomainGroupMember |
| Domain Admin | WriteDACL on Domain | PowerView, DSync |
| Domain Admin | DCSync Rights | secretsdump.py, mimikatz |
| Domain Admin | Unconstrained Delegation | Printer Bug + Rubeus |
| Domain Admin | Constrained Delegation | Rubeus s4u, getST.py |
| Domain Admin | RBCD | rbcd.py, PowerView |
| Domain Admin | DnsAdmins DLL Load | dnscmd |
| Domain Admin | Backup Operators | secretsdump.py, diskshadow |
| Domain Admin | AdminSDHolder Backdoor | PowerView, Set-DomainObject |
| Domain Admin | Token Privilege Abuse | RogueWinRM, JuicyPotato, PrintSpoofer, various |
| Domain Admin | Trust Account Abuse | Rubeus, Impacket, PowerView |

## Tool Quick Reference

| Tool | Purpose |
|------|---------|
| WinPEAS.exe | Windows local privesc enumeration |
| SeatBelt.exe | Windows security audit enumeration |
| PowerUp.ps1 | PowerShell local privesc checks |
| SharpUp.exe | C# local privesc checks |
| Rubeus.exe | Kerberos interaction, delegation attacks |
| mimikatz.exe | Credential extraction, DCSync |
| impacket (secretsdump.py) | DCSync, remote credential dumping |
| impacket (getST.py) | Service ticket requests |
| impacket (rbcd.py) | RBCD manipulation |
| impacket (printerbug.py) | MS-RPRN abuse for unconstrained delegation |
| BloodHound | Graph-based attack path analysis |
| PowerView | AD enumeration and abuse |
| NetExec | Cross-protocol exploitation |
| Certify.exe / certipy | ADCS abuse |

## Detection Table

| Activity | Event ID | Source |
|----------|----------|--------|
| Local privilege escalation via service | 4697, 7045 | Security/System |
| Token impersonation | 4672 | Security (special logon) |
| ACL modification | 5136 | Directory Service Changes |
| Password reset | 4724 | Security |
| Group member added | 4728, 4729, 4732, 4733 | Security |
| DCSync | 4662 (DS-Replication-Get-Changes) | Security (Audit DS Access) |
| TGT request | 4768 | Security |
| TGS request | 4769 | Security |
| Service ticket delegation | 4769 (forwardable) | Security |
| S4U2Self/S4U2Proxy | 4769 | Security |
| RBAC delegation change | 5136 (msDS-AllowedToActOnBehalfOfOtherIdentity) | Directory Service Changes |
| LAPS read | 4662 | Security |
| AdminSDHolder modification | 5136 | Directory Service Changes |
| DLL loaded via printer | 7034, 7031 | System |
| Backup Operator backup | 5248 | Security |
| DNS plugin modified | 770 | DNS Server |

## Prerequisites

- Local Admin on at least one domain-joined host for most domain escalation paths
- Valid domain credentials for LDAP-based enumeration and attacks
- Network connectivity to Domain Controllers (port 389/636, 88, 445)
- Appropriate tools on disk or ability to load in-memory (C2, PowerShell)

## OPSEC Overview

- **WinPEAS/SeatBelt** generate process creation events (4688) and may trigger EDR on-disk scans
- **PowerView** cmdlets may be logged by PowerShell ScriptBlock Logging (4104) and Module Logging
- **Impacket tools** run from Linux, leaving no Windows event logs on the attacker's host, but network traffic is observable (Kerberos, SMB)
- **Rubeus** generates Kerberos traffic visible to domain controllers (4768, 4769)
- **BloodHound** data collection via SharpHound generates LDAP queries (4662) and session enumeration (4624 network logons)
- **Editing ACLs** generates 5136 events — immediate detection if monitored
- **Token impersonation** via named pipes (Potato family) generates specific network connection events

## Technique Files

| # | File | Description |
|---|------|-------------|
| 01 | [Local Privesc](01_Local_PrivEsc_Windows.md) | Windows local privilege escalation fundamentals |
| 02 | [Domain ACL Abuse](02_Domain_PrivEsc_ACL.md) | Escalate via AD object ACL misconfigurations |
| 03 | [AdminSDHolder](03_AdminSDHolder.md) | Abuse AdminSDHolder and SDProp propagation |
| 04 | [Delegation Attacks](04_Delegation_Attacks.md) | Overview of Kerberos delegation attacks |
| 05 | [Unconstrained Delegation](05_Unconstrained_Delegation.md) | Unconstrained delegation abuse with Printer Bug |
| 06 | [Constrained Delegation](06_Constrained_Delegation.md) | Constrained delegation and protocol transition |
| 07 | [RBCD](07_RBCD.md) | Resource-Based Constrained Delegation |
| 08 | [Abusing Group Memberships](08_Abusing_Group_Memberships.md) | Privileged group member abuse (DnsAdmins, Backup Operators, etc.) |
| 09 | [LAPS Privesc](09_LAPS_PrivEsc.md) | LAPS password read and escalation |
| 10 | [Token Privileges](10_Privileged_Accounts_Token_Privileges.md) | Token privileges deep-dive on privileged accounts |
| 11 | [Trust Accounts Cross-Domain](11_Trust_Accounts_Cross_Domain.md) | Trust Account$ cross-domain abuse |
