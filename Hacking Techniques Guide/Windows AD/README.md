# Windows Active Directory — Red Teaming Notes

## Description

Comprehensive technical notes covering Active Directory security assessment methodologies. This repository documents the full attack lifecycle — from initial reconnaissance through enumeration, credential access, lateral movement, privilege escalation, Kerberos abuse, ADCS attacks, persistence, and cross-boundary trust attacks.

## Attack Lifecycle / Kill Chain

```
RECONNAISSANCE
      │
      ▼
ENUMERATION ───────────────────────────────────────────┐
  ├─ Unauthenticated (null sessions, DNS, LDAP)        │
  ├─ Authenticated (PowerView, AD Module, BloodHound)  │
  ├─ ACL Enumeration (DACL/ACE analysis)               │
  ├─ Trust Enumeration (domain/forest trusts)           │
  ├─ GPO Enumeration (misconfigurations)               │
  └─ BloodHound (graph-based attack path analysis)      │
      │                                                 │
      ▼                                                 │
INITIAL ACCESS                                          │
  ├─ AS-REP Roasting                                    │
  ├─ Kerberoasting                                      │
  ├─ Password Spraying                                  │
  ├─ LLMNR/NBT-NS Poisoning                             │
  ├─ NTLM Relay                                         │
  ├─ ZeroLogon / noPac                                  │
  ├─ PrintNightmare                                     │
  └─ GPP Password Extraction                            │
      │                                                 │
      ▼                                                 │
CREDENTIAL ACCESS                                       │
  ├─ Mimikatz (LSASS, SAM, LSA Secrets)                 │
  ├─ DCSync / SecretsDump                               │
  ├─ Windows Credential Manager / DPAPI                 │
  ├─ Browser Credentials                                │
  └─ LAPS Password Reading                              │
      │                                                 │
      ▼                                                 │
LATERAL MOVEMENT                                        │
  ├─ Pass-the-Hash                                      │
  ├─ Overpass-the-Hash                                  │
  ├─ Pass-the-Ticket                                    │
  ├─ PsExec / WMI Exec / SMB Exec                       │
  ├─ PowerShell Remoting                                │
  ├─ Scheduled Tasks                                    │
  └─ RDP                                                │
      │                                                 │
      ▼                                                 │
PRIVILEGE ESCALATION ─────────────────────────────┐     │
  ├─ Local Privesc (WinPEAS, JuicyPotato, etc.)   │     │
  ├─ Domain ACL Abuse (ForceChangePassword, etc.)  │     │
  ├─ AdminSDHolder                                 │     │
  ├─ Unconstrained Delegation                      │     │
  ├─ Constrained Delegation                        │     │
  ├─ RBCD                                          │     │
  ├─ Group Membership Abuse                        │     │
  └─ LAPS Escalation                               │     │
      │                                            │     │
      ▼                                            │     │
KERBEROS ATTACKS                                    │     │
  ├─ Golden Ticket                                  │     │
  ├─ Silver Ticket                                  │     │
  ├─ Diamond Ticket                                 │     │
  ├─ Skeleton Key                                   │     │
  └─ Delegation Abuse                               │     │
      │                                            │     │
      ▼                                            │     │
ADCS ATTACKS                                        │     │
  ├─ ESC1–ESC13                                     │     │
  ├─ Certipy Enumeration                            │     │
  └─ Certificate Theft / Forgery                    │     │
      │                                            │     │
      ▼                                            │     │
PERSISTENCE                                         │     │
  ├─ Golden/Silver Ticket                           │     │
  ├─ DSRM Backdoor                                  │     │
  ├─ Skeleton Key                                   │     │
  ├─ DCShadow                                       │     │
  ├─ SSP                                    ────────┘     │
  ├─ AdminSDHolder                                        │
  ├─ Certificate Persistence                              │
  └─ GPO Persistence                                      │
      │                                                    │
      ▼                                                    │
ATTACK SCENARIOS (Trust Abuse)                             │
  ├─ Child → Parent Domain (ExtraSids)                     │
  ├─ Forest Trust Abuse (TDO, Kerberos)                    │
  └─ Cross-Forest Attack (Kerberoast, ACL)                 │
                                                           │
      ◄────────────────────────────────────────────────────┘
                      EVERYTHING LEADS TO DCSYNC
```

## Table of Contents

### 01 — Enumeration

| # | Topic | File |
|---|-------|------|
| 01 | Initial Recon (No Creds) | [01_Enumeration/01_Initial_Recon_No_Creds.md](./01_Enumeration/01_Initial_Recon_No_Creds.md) |
| 02 | Domain Enumeration | [01_Enumeration/02_Domain_Enumeration.md](./01_Enumeration/02_Domain_Enumeration.md) |
| 03 | ACL Enumeration | [01_Enumeration/03_ACL_Enumeration.md](./01_Enumeration/03_ACL_Enumeration.md) |
| 04 | Trust Enumeration | [01_Enumeration/04_Trust_Enumeration.md](./01_Enumeration/04_Trust_Enumeration.md) |
| 05 | GPO Enumeration | [01_Enumeration/05_GPO_Enumeration.md](./01_Enumeration/05_GPO_Enumeration.md) |
| 06 | BloodHound / SharpHound | [01_Enumeration/06_BloodHound_SharpHound.md](./01_Enumeration/06_BloodHound_SharpHound.md) |
| 07 | LDAP Queries | [01_Enumeration/07_LDAP_Queries.md](./01_Enumeration/07_LDAP_Queries.md) |
| — | README | [01_Enumeration/README.md](./01_Enumeration/README.md) |

### 02 — Initial Access

| # | Topic | File |
|---|-------|------|
| 01 | AS-REP Roasting | [02_Initial_Access/01_ASREPRoast.md](./02_Initial_Access/01_ASREPRoast.md) |
| 02 | Kerberoasting | [02_Initial_Access/02_Kerberoasting.md](./02_Initial_Access/02_Kerberoasting.md) |
| 03 | Password Spraying | [02_Initial_Access/03_Password_Spraying.md](./02_Initial_Access/03_Password_Spraying.md) |
| 04 | LLMNR/NBT-NS Poisoning | [02_Initial_Access/04_LLMNR_NBTNS_Poisoning.md](./02_Initial_Access/04_LLMNR_NBTNS_Poisoning.md) |
| 05 | mitm6 / DHCPv6 | [02_Initial_Access/05_mitm6_DHCPv6.md](./02_Initial_Access/05_mitm6_DHCPv6.md) |
| 06 | NTLM Relay | [02_Initial_Access/06_NTLM_Relay.md](./02_Initial_Access/06_NTLM_Relay.md) |
| 07 | ZeroLogon / noPac | [02_Initial_Access/07_ZeroLogon_NoPac.md](./02_Initial_Access/07_ZeroLogon_NoPac.md) |
| 08 | PrintNightmare | [02_Initial_Access/08_PrintNightmare.md](./02_Initial_Access/08_PrintNightmare.md) |
| 09 | GPP Stored Passwords | [02_Initial_Access/09_GPP_Stored_Passwords.md](./02_Initial_Access/09_GPP_Stored_Passwords.md) |
| — | README | [02_Initial_Access/README.md](./02_Initial_Access/README.md) |

### 03 — Credential Access

| # | Topic | File |
|---|-------|------|
| 01 | Mimikatz | [03_Credential_Access/01_Mimikatz.md](./03_Credential_Access/01_Mimikatz.md) |
| 02 | DCSync | [03_Credential_Access/02_DCSync.md](./03_Credential_Access/02_DCSync.md) |
| 03 | SecretsDump | [03_Credential_Access/03_SecretsDump.md](./03_Credential_Access/03_SecretsDump.md) |
| 04 | LSASS Dumping | [03_Credential_Access/04_LSASS_Dumping.md](./03_Credential_Access/04_LSASS_Dumping.md) |
| 05 | SAM / LSA / DPAPI | [03_Credential_Access/05_SAM_LSA_DPAPI.md](./03_Credential_Access/05_SAM_LSA_DPAPI.md) |
| 06 | Group Policy Preferences | [03_Credential_Access/06_Group_Policy_Preferences.md](./03_Credential_Access/06_Group_Policy_Preferences.md) |
| 07 | LAPS | [03_Credential_Access/07_LAPS.md](./03_Credential_Access/07_LAPS.md) |
| 08 | Browser Credentials | [03_Credential_Access/08_Browser_Credentials.md](./03_Credential_Access/08_Browser_Credentials.md) |
| 09 | Windows Credential Manager | [03_Credential_Access/09_Windows_Credential_Manager.md](./03_Credential_Access/09_Windows_Credential_Manager.md) |
| — | README | [03_Credential_Access/README.md](./03_Credential_Access/README.md) |

### 04 — Lateral Movement

| # | Topic | File |
|---|-------|------|
| 01 | Pass-the-Hash | [04_Lateral_Movement/01_Pass_The_Hash.md](./04_Lateral_Movement/01_Pass_The_Hash.md) |
| 02 | Overpass-the-Hash | [04_Lateral_Movement/02_Overpass_The_Hash.md](./04_Lateral_Movement/02_Overpass_The_Hash.md) |
| 03 | Pass-the-Ticket | [04_Lateral_Movement/03_Pass_The_Ticket.md](./04_Lateral_Movement/03_Pass_The_Ticket.md) |
| 04 | PsExec | [04_Lateral_Movement/04_PsExec.md](./04_Lateral_Movement/04_PsExec.md) |
| 05 | WMI Exec | [04_Lateral_Movement/05_WMI_Exec.md](./04_Lateral_Movement/05_WMI_Exec.md) |
| 06 | SMB Exec | [04_Lateral_Movement/06_SMB_Exec.md](./04_Lateral_Movement/06_SMB_Exec.md) |
| 07 | PowerShell Remoting | [04_Lateral_Movement/07_PowerShell_Remoting.md](./04_Lateral_Movement/07_PowerShell_Remoting.md) |
| 08 | Scheduled Tasks | [04_Lateral_Movement/08_Scheduled_Tasks.md](./04_Lateral_Movement/08_Scheduled_Tasks.md) |
| 09 | RDP | [04_Lateral_Movement/09_RDP.md](./04_Lateral_Movement/09_RDP.md) |
| 10 | DPAPI Lateral | [04_Lateral_Movement/10_DPAPI_Lateral.md](./04_Lateral_Movement/10_DPAPI_Lateral.md) |
| — | README | [04_Lateral_Movement/README.md](./04_Lateral_Movement/README.md) |

### 05 — Privilege Escalation

| # | Topic | File |
|---|-------|------|
| 01 | Local Privesc (Windows) | [05_Privilege_Escalation/01_Local_PrivEsc_Windows.md](./05_Privilege_Escalation/01_Local_PrivEsc_Windows.md) |
| 02 | Domain Privesc (ACL) | [05_Privilege_Escalation/02_Domain_PrivEsc_ACL.md](./05_Privilege_Escalation/02_Domain_PrivEsc_ACL.md) |
| 03 | AdminSDHolder | [05_Privilege_Escalation/03_AdminSDHolder.md](./05_Privilege_Escalation/03_AdminSDHolder.md) |
| 04 | Delegation Attacks | [05_Privilege_Escalation/04_Delegation_Attacks.md](./05_Privilege_Escalation/04_Delegation_Attacks.md) |
| 05 | Unconstrained Delegation | [05_Privilege_Escalation/05_Unconstrained_Delegation.md](./05_Privilege_Escalation/05_Unconstrained_Delegation.md) |
| 06 | Constrained Delegation | [05_Privilege_Escalation/06_Constrained_Delegation.md](./05_Privilege_Escalation/06_Constrained_Delegation.md) |
| 07 | RBCD | [05_Privilege_Escalation/07_RBCD.md](./05_Privilege_Escalation/07_RBCD.md) |
| 08 | Abusing Group Memberships | [05_Privilege_Escalation/08_Abusing_Group_Memberships.md](./05_Privilege_Escalation/08_Abusing_Group_Memberships.md) |
| 09 | LAPS Privesc | [05_Privilege_Escalation/09_LAPS_PrivEsc.md](./05_Privilege_Escalation/09_LAPS_PrivEsc.md) |
| — | README | [05_Privilege_Escalation/README.md](./05_Privilege_Escalation/README.md) |

### 06 — Kerberos Attacks

| # | Topic | File |
|---|-------|------|
| 01 | AS-REP Roasting (Deep) | [06_Kerberos_Attacks/01_ASREPRoast_Deep.md](./06_Kerberos_Attacks/01_ASREPRoast_Deep.md) |
| 02 | Kerberoasting (Deep) | [06_Kerberos_Attacks/02_Kerberoasting_Deep.md](./06_Kerberos_Attacks/02_Kerberoasting_Deep.md) |
| 03 | Golden Ticket | [06_Kerberos_Attacks/03_Golden_Ticket.md](./06_Kerberos_Attacks/03_Golden_Ticket.md) |
| 04 | Silver Ticket | [06_Kerberos_Attacks/04_Silver_Ticket.md](./06_Kerberos_Attacks/04_Silver_Ticket.md) |
| 05 | Diamond Ticket | [06_Kerberos_Attacks/05_Diamond_Ticket.md](./06_Kerberos_Attacks/05_Diamond_Ticket.md) |
| 06 | Skeleton Key | [06_Kerberos_Attacks/06_Skeleton_Key.md](./06_Kerberos_Attacks/06_Skeleton_Key.md) |
| 07 | Kerberos Delegation | [06_Kerberos_Attacks/07_Kerberos_Delegation.md](./06_Kerberos_Attacks/07_Kerberos_Delegation.md) |
| — | README | [06_Kerberos_Attacks/README.md](./06_Kerberos_Attacks/README.md) |

### 07 — ADCS Attacks

| # | Topic | File |
|---|-------|------|
| 01 | Certipy Enumeration | [07_ADCS_Attacks/01_Certipy_Enumeration.md](./07_ADCS_Attacks/01_Certipy_Enumeration.md) |
| 02 | ESC1 / ESC2 / ESC3 | [07_ADCS_Attacks/02_ESC1_ESC2_ESC3.md](./07_ADCS_Attacks/02_ESC1_ESC2_ESC3.md) |
| 03 | ESC4 / ESC5 / ESC6 | [07_ADCS_Attacks/03_ESC4_ESC5_ESC6.md](./07_ADCS_Attacks/03_ESC4_ESC5_ESC6.md) |
| 04 | ESC7 / ESC8 | [07_ADCS_Attacks/04_ESC7_ESC8.md](./07_ADCS_Attacks/04_ESC7_ESC8.md) |
| 05 | ESC9 / ESC10 / ESC11 | [07_ADCS_Attacks/05_ESC9_ESC10_ESC11.md](./07_ADCS_Attacks/05_ESC9_ESC10_ESC11.md) |
| 06 | ESC12 / ESC13 | [07_ADCS_Attacks/06_ESC12_ESC13.md](./07_ADCS_Attacks/06_ESC12_ESC13.md) |
| 07 | Certify / ForgeCert | [07_ADCS_Attacks/07_Certify_ForgeCert.md](./07_ADCS_Attacks/07_Certify_ForgeCert.md) |
| — | README | [07_ADCS_Attacks/README.md](./07_ADCS_Attacks/README.md) |

### 08 — Persistence

| # | Topic | File |
|---|-------|------|
| 01 | Golden Ticket Persistence | [08_Persistence/01_Golden_Ticket_Persistence.md](./08_Persistence/01_Golden_Ticket_Persistence.md) |
| 02 | Silver Ticket Persistence | [08_Persistence/02_Silver_Ticket_Persistence.md](./08_Persistence/02_Silver_Ticket_Persistence.md) |
| 03 | DSRM Backdoor | [08_Persistence/03_DSRM_Backdoor.md](./08_Persistence/03_DSRM_Backdoor.md) |
| 04 | Skeleton Key | [08_Persistence/04_Skeleton_Key.md](./08_Persistence/04_Skeleton_Key.md) |
| 05 | DCShadow | [08_Persistence/05_DCShadow.md](./08_Persistence/05_DCShadow.md) |
| 06 | AdminSDHolder Persistence | [08_Persistence/06_AdminSDHolder_Persistence.md](./08_Persistence/06_AdminSDHolder_Persistence.md) |
| 07 | SSP Backdoor | [08_Persistence/07_SSP_Backdoor.md](./08_Persistence/07_SSP_Backdoor.md) |
| 08 | Certificate Persistence | [08_Persistence/08_Certificate_Persistence.md](./08_Persistence/08_Certificate_Persistence.md) |
| 09 | GPO Persistence | [08_Persistence/09_Group_Policy_Persistence.md](./08_Persistence/09_Group_Policy_Persistence.md) |
| — | README | [08_Persistence/README.md](./08_Persistence/README.md) |

### 09 — Tools Reference

| # | Topic | File |
|---|-------|------|
| 01 | Impacket (Complete) | [09_Tools_Reference/01_Impacket_Complete.md](./09_Tools_Reference/01_Impacket_Complete.md) |
| 02 | NetExec / CrackMapExec | [09_Tools_Reference/02_NetExec_CrackMapExec.md](./09_Tools_Reference/02_NetExec_CrackMapExec.md) |
| 03 | BloodHound | [09_Tools_Reference/03_BloodHound.md](./09_Tools_Reference/03_BloodHound.md) |
| 04 | Mimikatz | [09_Tools_Reference/04_Mimikatz.md](./09_Tools_Reference/04_Mimikatz.md) |
| 05 | Rubeus | [09_Tools_Reference/05_Rubeus.md](./09_Tools_Reference/05_Rubeus.md) |
| 06 | Responder / Inveigh | [09_Tools_Reference/06_Responder_Inveigh.md](./09_Tools_Reference/06_Responder_Inveigh.md) |
| 07 | PowerView / AD Module | [09_Tools_Reference/07_PowerView_ADModule.md](./09_Tools_Reference/07_PowerView_ADModule.md) |
| 08 | Certipy | [09_Tools_Reference/08_Certipy.md](./09_Tools_Reference/08_Certipy.md) |
| 09 | Evil-WinRM | [09_Tools_Reference/09_EvilWinRM.md](./09_Tools_Reference/09_EvilWinRM.md) |
| 10 | Kerbrute | [09_Tools_Reference/10_Kerbrute.md](./09_Tools_Reference/10_Kerbrute.md) |
| 11 | WinPEAS / SeatBelt | [09_Tools_Reference/11_WinPEAS_SeatBelt.md](./09_Tools_Reference/11_WinPEAS_SeatBelt.md) |
| 12 | Misc Tools | [09_Tools_Reference/12_Misc_Tools.md](./09_Tools_Reference/12_Misc_Tools.md) |
| — | README | [09_Tools_Reference/README.md](./09_Tools_Reference/README.md) |

### 10 — Checklists

| # | Topic | File |
|---|-------|------|
| — | Overall Checklist | [10_Checklists/Overall WAD Checklist.md](./Checklist/Overall%20WAD%20Checklist.md) |
| — | Recon Checklist | [10_Checklists/Recon WAD Checklist.md](./Checklist/Recon%20WAD%20Checklist.md) |
| — | Enumeration Checklist | [10_Checklists/Enum WAD Checklist.md](./Checklist/Enum%20WAD%20Checklist.md) |
| — | Credential Access Checklist | [10_Checklists/Creds WAD Checklist.md](./Checklist/Creds%20WAD%20Checklist.md) |
| — | Exploit Checklist | [10_Checklists/Exploit WAD Checklist.md](./Checklist/Exploit%20WAD%20Checklist.md) |
| — | Post-Exploit Checklist | [10_Checklists/PExploit WAD Checklist.md](./Checklist/PExploit%20WAD%20Checklist.md) |

### 11 — Attack Scenarios

| # | Topic | File |
|---|-------|------|
| 01 | Child to Parent Domain | [11_Attack_Scenarios/01_Child_to_Parent_Domain.md](./11_Attack_Scenarios/01_Child_to_Parent_Domain.md) |
| 02 | Forest Trust Abuse | [11_Attack_Scenarios/02_Forest_Trust_Abuse.md](./11_Attack_Scenarios/02_Forest_Trust_Abuse.md) |
| 03 | Cross-Forest Attack | [11_Attack_Scenarios/03_Cross_Forest_Attack.md](./11_Attack_Scenarios/03_Cross_Forest_Attack.md) |
| — | README | [11_Attack_Scenarios/README.md](./11_Attack_Scenarios/README.md) |

## Quick Reference — Common Tools

| Tool | Category | Language | Primary Use |
|------|----------|----------|-------------|
| **Impacket** | Multi-purpose | Python | Protocol abuse, lateral movement, credential dumping |
| **NetExec (nxc)** | Multi-purpose | Python | Automated pentesting, spraying, enumeration |
| **BloodHound** | Enumeration | C#/JS | Attack path mapping, graph analysis |
| **Mimikatz** | Credential | C | Credential extraction, ticket manipulation |
| **Rubeus** | Kerberos | C# | Kerberos abuse, ticket operations |
| **PowerView** | Enumeration | PowerShell | AD recon, ACL enumeration, trust mapping |
| **Responder** | Poisoning | Python | LLMNR/NBTNS/mDNS poisoning |
| **Certipy** | ADCS | Python | ADCS abuse, certificate theft |
| **Evil-WinRM** | WinRM | Ruby | WinRM shell with advanced features |
| **Kerbrute** | Kerberos | Go | User enumeration, password spray |
| **WinPEAS** | Enumeration | .exe | Windows privilege escalation checks |
| **SeatBelt** | Enumeration | C# | Windows security config audit |

## Lab Environments for Practice

| Lab | Description | URL |
|-----|-------------|-----|
| **GOAD (Game of Active Directory)** | Multi-domain AD lab with multiple forests, trusts, and misconfigurations | https://github.com/Orange-Cyberdefense/GOAD |
| **BadBlood** | PowerShell script that populates an AD with misconfigurations | https://github.com/davidprowe/BadBlood |
| **VulnAD** | AD lab with security flaws for training | https://github.com/claranet/vuln_ad |
| **DetectionLab** | Lab with AD + security tooling for detection engineering | https://github.com/clong/DetectionLab |
| **Modify-GOAD** | Enhanced version of GOAD with additional scenarios | https://github.com/AdrianVollmer/Modify-GOAD |
| **PPSecurity** | AD attack/defense lab environment | https://github.com/chryzsh/awesome-windows-cc |
| **Windows Domain Lab** | Manual AD lab setup guide | https://github.com/rapid7/metasploit-lab |

## Resources & Attribution

### Tools & Frameworks
- **Impacket** — [https://github.com/fortra/impacket](https://github.com/fortra/impacket)
- **BloodHound** — [https://github.com/BloodHoundAD/BloodHound](https://github.com/BloodHoundAD/BloodHound)
- **Mimikatz** — [https://github.com/gentilkiwi/mimikatz](https://github.com/gentilkiwi/mimikatz)
- **NetExec** — [https://github.com/Pennyw0rth/NetExec](https://github.com/Pennyw0rth/NetExec)
- **Rubeus** — [https://github.com/GhostPack/Rubeus](https://github.com/GhostPack/Rubeus)
- **Certipy** — [https://github.com/ly4k/Certipy](https://github.com/ly4k/Certipy)
- **PowerView** — [https://github.com/PowerShellMafia/PowerSploit](https://github.com/PowerShellMafia/PowerSploit)
- **Responder** — [https://github.com/lgandx/Responder](https://github.com/lgandx/Responder)
- **Evil-WinRM** — [https://github.com/Hackplayers/evil-winrm](https://github.com/Hackplayers/evil-winrm)
- **Kerbrute** — [https://github.com/ropnop/kerbrute](https://github.com/ropnop/kerbrute)
- **WinPEAS** — [https://github.com/carlospolop/privilege-escalation-awesome-scripts](https://github.com/carlospolop/privilege-escalation-awesome-scripts)

### Educational Resources
- **Active Directory Security** — [https://adsecurity.org](https://adsecurity.org) (Sean Metcalf)
- **Harmj0y's Blog** — [http://blog.harmj0y.net](http://blog.harmj0y.net)
- **SpecterOps Blog** — [https://posts.specterops.io](https://posts.specterops.io)
- **Kerberos Attacks Explained** — [https://www.tarlogic.com/en/blog/how-kerberos-works/](https://www.tarlogic.com/en/blog/how-kerberos-works/)
- **The Hacker Recipes** — [https://www.thehacker.recipes](https://www.thehacker.recipes)
- **ired.team** — [https://www.ired.team](https://www.ired.team)
- **PayloadsAllTheThings** — [https://github.com/swisskyrepo/PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)
- **Active Directory Kill Chain** — [https://github.com/infosecn1nja/AD-Attack-Defense](https://github.com/infosecn1nja/AD-Attack-Defense)

### Books
- **"Active Directory Security"** — Sean Metcalf (adsecurity.org)
- **"The Active Directory Bible"** — Various community resources
- **"Red Team Development and Operations"** — Joe Vest & James Tubberville

## Usage Notes

- These notes are intended for authorized security assessments and lab environments only
- Commands are documented for both PowerShell (Windows) and bash (Linux/Kali)
- All commands should be tested in a lab before use in production assessments
- Event IDs listed in detection tables apply to Windows Server 2016+ / Windows 10+
- Tool versions and syntax may change — check tool documentation for the latest
- Some techniques require specific privileges or domain functional levels
- Validate connectivity and permissions before escalating to noisy techniques

## Conventions Used

| Notation | Meaning |
|----------|---------|
| `<domain>` | Fully qualified domain name |
| `<user>` | Username |
| `<pass>` | Plaintext password |
| `<NTLM>` | NTLM hash (32 hex characters) |
| `<hash>` | Any credential hash |
| `<SID>` | Security Identifier |
| `<dc-ip>` | Domain Controller IP |
| `<target>` | Target hostname or IP |

## Color Coding

- `[+]` — Success / Found
- `[-]` — Failure / Not Found
- `[*]` — Information / In Progress
- `[!]` — Warning / High Value
