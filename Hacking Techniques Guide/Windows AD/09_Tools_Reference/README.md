# Tools Reference Guide

## Overview

Comprehensive reference for the essential tools used in Active Directory security assessments. This section covers installation, syntax, modules, and practical examples for each tool.

## Quick Reference Table

| Tool | Category | Language | Auth Methods | Primary Use |
|------|----------|----------|--------------|-------------|
| Impacket | Multi-purpose | Python | NTLM, Kerberos, hashes | Protocol abuse, lateral movement, credential dumping |
| NetExec (nxc) | Multi-purpose | Python | NTLM, Kerberos, hashes | Automated pentesting, spraying, enumeration |
| BloodHound | Enumeration | C#/JS | LDAP creds | Attack path mapping, graph analysis |
| Mimikatz | Credential | C | Interactive | Credential extraction, ticket manipulation |
| Rubeus | Kerberos | C# | Interactive | Kerberos abuse, ticket requests/forgery |
| Responder | Poisoning | Python | N/A | LLMNR/NBTNS/mDNS poisoning |
| Inveigh | Poisoning | PowerShell | N/A | LLMNR/NBTNS/mDNS poisoning (Windows) |
| PowerView | Enumeration | PowerShell | AD creds | AD recon, ACL enumeration |
| Certipy | ADCS | Python | NTLM, Kerberos | ADCS abuse, certificate theft |
| Evil-WinRM | WinRM | Ruby | NTLM, hashes, key | WinRM shell with features |
| Kerbrute | Kerberos | Go | None | User enumeration, password spray |
| WinPEAS | Enumeration | .exe | Local | Windows privilege escalation checks |
| SeatBelt | Enumeration | C# | Local | Windows security config audit |

## Installation Methods

### Package Managers

```bash
# Pip (Python tools)
pip install impacket certipy-ad bloodhound-py netexec
pip install ldapdomaindump adidnsdump enum4linux-ng

# Go tools
go install github.com/ropnop/kerbrute@latest

# Ruby tools
gem install evil-winrm

# Kali/Parrot
sudo apt install impacket-scripts bloodhound neo4j responder kerbrute
```

### Manual Installation

```bash
# Impacket
git clone https://github.com/fortra/impacket.git
cd impacket && pip install .

# NetExec
git clone https://github.com/Pennyw0rth/NetExec.git
cd NetExec && pip install .

# Certipy
git clone https://github.com/ly4k/Certipy.git
cd Certipy && pip install .

# BloodHound.py
git clone https://github.com/dirkjanm/BloodHound.py.git
cd BloodHound.py && pip install .
```

### Windows Binaries

Most C# tools (Rubeus, SharpHound, SeatBelt, Certify) are pre-compiled binaries available via GitHub releases or can be compiled with `csc.exe` or Visual Studio.

## Tool Selection by Task

| Task | Recommended Tool |
|------|-----------------|
| Initial domain enum (no creds) | enum4linux-ng, ldapdomaindump, nxc |
| Domain enum (with creds) | BloodHound, PowerView, AD Module |
| Kerberoasting | Rubeus, Impacket GetUserSPNs.py |
| AS-REP roasting | Impacket GetNPUsers.py, Rubeus |
| Password spraying | Kerbrute, nxc, CrackMapExec |
| Credential dumping | Mimikatz, Impacket secretsdump.py |
| Lateral movement | Impacket (psexec/wmiexec/smbexec), Evil-WinRM |
| NTLM relay | Impacket ntlmrelayx.py |
| ADCS abuse | Certipy, Certify |
| LLMNR/NBTNS poison | Responder, Inveigh |
| Silver/Golden tickets | Mimikatz, Impacket ticketer.py |
| Delegation abuse | Impacket getST.py, Rubeus |
| SMB/ share enumeration | smbmap, smbclient, nxc |
| Kerberos user enum | Kerbrute |
| Local privesc checks | WinPEAS, SeatBelt |
| GPP password check | nxc, PowerView |
| Password audit | nxc, Kerbrute |
| Zone transfer / DNS | adidnsdump |
| Relay to ADCS | ntlmrelayx.py, KrbRelay |

## Cheat Sheet Legend

- `<domain>` - Fully qualified domain name (e.g., `contoso.local`)
- `<target>` - Target IP or hostname
- `<user>` - Username (with or without domain prefix)
- `<pass>` - Plaintext password
- `<NTLM>` - NTLM hash (32 hex characters)
- `<LM>` - LM hash (32 hex characters, often `aad3b435b51404eeaad3b435b51404ee`)
- `<SID>` - Security Identifier

## Common Authentication Patterns

```bash
# Plaintext password
tool.py domain/user:pass@target

# NTLM hash (pass-the-hash)
tool.py domain/user@target -hashes LM:NTLM

# Kerberos (using ccache file)
export KRB5CCNAME=/path/to/ticket.ccache
tool.py domain/user@target -k -no-pass

# NTLM hash without LM
tool.py domain/user@target -hashes :NTLM
```

## Technique Files

| # | File | Description |
|---|------|-------------|
| 01 | [Impacket](01_Impacket_Complete.md) | Comprehensive Impacket reference and examples |
| 02 | [NetExec / CrackMapExec](02_NetExec_CrackMapExec.md) | Multi-protocol exploitation framework |
| 03 | [BloodHound](03_BloodHound.md) | Attack path mapping and graph analysis |
| 04 | [Mimikatz](04_Mimikatz.md) | Credential extraction and ticket manipulation |
| 05 | [Rubeus](05_Rubeus.md) | Kerberos abuse toolkit |
| 06 | [Responder / Inveigh](06_Responder_Inveigh.md) | LLMNR/NBT-NS/mDNS poisoning tools |
| 07 | [PowerView / AD Module](07_PowerView_ADModule.md) | PowerShell-based AD enumeration |
| 08 | [Certipy](08_Certipy.md) | AD CS abuse and certificate manipulation |
| 09 | [Evil-WinRM](09_EvilWinRM.md) | WinRM shell with advanced features |
| 10 | [Kerbrute](10_Kerbrute.md) | Kerberos user enumeration and password spraying |
| 11 | [WinPEAS / SeatBelt](11_WinPEAS_SeatBelt.md) | Windows privilege escalation enumeration |
| 12 | [Misc Tools](12_Misc_Tools.md) | Additional tools (smbmap, ldapdomaindump, enum4linux-ng, etc.) |
| 13 | [Commercial AD Tools](13_Commercial_AD_Tools.md) | Commercial and enterprise AD assessment tools |
