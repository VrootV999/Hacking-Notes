# Initial Access — Windows Active Directory

Gaining a foothold in a Windows AD environment. These techniques target authentication protocols, misconfigurations, and vulnerable services to capture or relay credentials.

## Technique Matrix

| # | Technique | Target | Key Tools | Requires Creds | Hashcat Mode |
|---|-----------|--------|-----------|----------------|--------------|
| 01 | AS-REP Roasting | Kerberos (no pre-auth accounts) | GetNPUsers.py, Rubeus | ❌ | 18200 |
| 02 | Kerberoasting | Kerberos (service accounts) | GetUserSPNs.py, Rubeus | ✅ (any user) | 13100 |
| 03 | Password Spraying | Any auth endpoint | NetExec, Kerbrute | ❌ | — |
| 04 | LLMNR/NBT-NS Poisoning | Link-local name resolution | Responder, Inveigh | ❌ | — |
| 05 | mitm6 / DHCPv6 | IPv6 + WPAD | mitm6 + ntlmrelayx.py | ❌ | — |
| 06 | NTLM Relay | SMB / LDAP / HTTP | ntlmrelayx.py | ❌ | — |
| 07 | ZeroLogon / noPac | Netlogon / Kerberos | zerologon.py, noPac.py | ❌ | — |
| 08 | PrintNightmare | Print Spooler | nxc / impacket | ✅ | — |
| 09 | GPP Passwords | SYSVOL / Groups.xml | nxc / pyGPP | ❌ | — |
| 10 | SMB Attacks | SMB protocol | smbmap, impacket-smbclient, nxc | varies | — |
| 11 | LDAP Attacks | LDAP directory service | ldapsearch, nxc ldap, windapsearch | varies | — |
| 12 | Execution Methods | PowerShell / .NET / LOLBIN | PowerSharpPack, various bypasses | varies | — |

## Technique Files

| # | File | Description |
|---|------|-------------|
| 01 | [AS-REP Roasting](01_ASREPRoast.md) | Harvest credentials from accounts with pre-auth disabled |
| 02 | [Kerberoasting](02_Kerberoasting.md) | Request and crack service account tickets |
| 03 | [Password Spraying](03_Password_Spraying.md) | Low-and-slow password guessing across accounts |
| 04 | [LLMNR/NBT-NS Poisoning](04_LLMNR_NBTNS_Poisoning.md) | Responder-based link-local name poison |
| 05 | [mitm6 / DHCPv6](05_mitm6_DHCPv6.md) | IPv6 + WPAD authentication relay |
| 06 | [NTLM Relay](06_NTLM_Relay.md) | Relay captured NTLM authentication to targets |
| 07 | [ZeroLogon / noPac](07_ZeroLogon_NoPac.md) | Netlogon and Kerberos elevation vulnerabilities |
| 08 | [PrintNightmare](08_PrintNightmare.md) | Print Spooler RCE and LPE |
| 09 | [GPP Passwords](09_GPP_Stored_Passwords.md) | Extract cached Group Policy preferences passwords |
| 10 | [SMB Attacks](10_SMB_Attacks.md) | SMB protocol-specific attacks and abuse |
| 11 | [LDAP Attacks](11_LDAP_Specific_Attacks.md) | LDAP-specific attacks and directory service abuse |
| 12 | [Execution Methods](12_Execution_Methods.md) | Execution methods, AMSI bypass, and LOLBINS |

## Attack Flow Overview

```
Recon ─► AS-REP / Kerberoast / Spray ─► Valid Creds ─► Lateral Movement
                  │
            Poison / Relay ─► Credential Capture ─► Lateral Movement
                  │
         ZeroLogon / noPac ─► Domain Admin ─► DCSync
```

## Tooling Reference

- **Impacket** — `GetNPUsers.py`, `GetUserSPNs.py`, `ntlmrelayx.py`, `secretsdump.py`, `ticketer.py`
- **Rubeus** — Windows .NET tool for all Kerberos operations
- **NetExec (nxc)** — Switched replacement for CrackMapExec
- **Responder** — LLMNR/NBT-NS/mDNS poisoner
- **hashcat** — GPU-accelerated password cracking
- **Kerbrute** — Kerberos brute/spray (Go)

## OPSEC Principles

1. **Stay out of logs** — Avoid authentication where you don't need it
2. **Minimal touch** — One clean request > multiple noisy scans
3. **Encrypt C2** — Always route through SOCKS/Chisel
4. **Clean up** — Remove tools, delete created accounts
5. **Target selection** — Old workstations > servers > DCs
