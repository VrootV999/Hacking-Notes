# Windows Active Directory — Basics

This folder covers the fundamental technologies that underpin Microsoft Active Directory (AD). Understanding these building blocks is essential before exploring attacks, tooling, or defensive strategies.

## How the technologies fit together

```
┌───────────────────────────────────────────────────────────────┐
│                   Active Directory Architecture               │
│  Domains · Trees · Forests · OUs · DCs · GC · FSMO · NTDS.dit │
└──────────┬────────────────────────────────────┬───────────────┘
           │                                    │
           ▼                                    ▼
┌─────────────────────┐  ┌──────────────────────────────────────┐
│   Authentication     │  │         Directory Access             │
│                      │  │                                      │
│  Kerberos ──┬── NTLM │  │  LDAP ──┬── LDAPS ──┬── Global Cat. │
│  PKINIT     │  relay │  │  GC     │  paging    │  search       │
│  FAST/armor │        │  │  controls             │              │
└─────────────┼────────┘  └──────────┬───────────┘              │
              │                      │                          │
              ▼                      ▼                          │
┌──────────────────────────────────────────────────────────────┐ │
│                     Transport Layer                          │ │
│                                                              │ │
│  SMB ──┬── named pipes ──┬── MSRPC (lsarpc, samr, netlogon) │ │
│  ports │  139/445         │  135 (EPM) + dynamic             │ │
│  139/445                 │                                    │ │
└────────┼─────────────────┼───────────────────────────────────┘ │
         │                 │                                     │
         ▼                 ▼                                     │
┌──────────────────────────────────────────────────────────────┐│
│                 Name Resolution                               ││
│                                                               ││
│  DNS (SRV, _msdcs) ──┬── LLMNR ──┬── NBT-NS ──┬── mDNS      ││
│  AD-integrated zones   │          │  WINS       │             ││
└────────────────────────┼──────────┼────────────┘             │
                         │          │                          │
                         ▼          ▼                          │
┌──────────────────────────────────────────────────────────────┐│
│              Supporting Infrastructure                       ││
│                                                              ││
│  Group Policy · ADCS/PKI · DPAPI · Security Principals/SIDs  ││
│  AdminSDHolder · Protected Users · Credential Guard          ││
└──────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────┘
```

## File map

| #  | File | Topic |
|----|------|-------|
| 01 | `01_Active_Directory_Architecture.md` | AD logical & physical structure, FSMO, replication, NTDS.dit, naming contexts |
| 02 | `02_Kerberos_Protocol.md` | Kerberos in AD, AS/TGS/AP exchange, PAC, delegation, FAST, PKINIT |
| 03 | `03_LDAP_Protocol.md` | LDAP directory structure, operations, search filters, controls, LDAP injection |
| 04 | `04_NTLM_Protocol.md` | LM/NT hash, NTLMv1/v2, challenge-response, NTLMSSP, relay basics |
| 05 | `05_SMB_Protocol.md` | SMB dialects, signing, encryption, named pipes, shares, CIFS comparison |
| 06 | `06_DNS_in_AD.md` | SRV records, AD-integrated zones, dynamic updates, DNS attacks |
| 07 | `07_NetBIOS_and_Name_Resolution.md` | NBT-NS, LLMNR, mDNS, WINS, name resolution order, wpAD |
| 09 | `09_MSRPC_Protocol.md` | DCE/RPC, endpoint mapper, lsarpc, samr, netlogon, drsuapi |
| 10 | `10_DPAPI_Architecture.md` | Master keys, domain backup keys, credential blobs, vaults |
| 11 | `11_Group_Policy_Architecture.md` | GPC/GPT, SYSVOL, LSDOU, security/WMI filtering, ADMX |
| 12 | `12_PKI_ADCS_Architecture.md` | CA hierarchy, templates, enrollment, revocation, attack surface |
| 13 | `13_AD_Security_Concepts.md` | SIDs, ACLs, DACL/SACL, AdminSDHolder, Protected Users, Credential Guard |
| 14 | `14_Lab_Setup_Guide.md` | Lab setup guide for AD testing environments |

## Prerequisites

- Basic networking (TCP/IP, ports, DNS)
- Windows domain-joined environment (conceptual)
- Familiarity with authentication concepts (tickets, tokens, hashes)

## How to use these files

Read them in order (01 → 14) for a structured deep-dive, or jump to a specific protocol as a reference. Each file follows the same structure:

1. **What it is** — definition and purpose
2. **How it works** — detailed technical explanation, protocol flow, diagrams
3. **Relevant RFCs & standards** — official references
4. **Ports used** — network ports and transport
5. **How attackers abuse it** — common attack techniques
6. **Defender recommendations** — hardening and detection guidance
