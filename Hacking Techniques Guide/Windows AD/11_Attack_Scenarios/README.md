# Attack Scenarios Overview

## Overview

This section covers multi-step attack chains that leverage Active Directory trust relationships to move laterally across domains and forests. These scenarios build on individual techniques covered in earlier sections and combine them into end-to-end attack paths.

## Trust Relationship Fundamentals

Trust relationships define authentication boundaries between AD domains and forests. Understanding the trust model is essential before attempting cross-boundary attacks.

| Trust Type | Created Between | Transitive | SID Filtering Default |
|------------|-----------------|------------|----------------------|
| Parent-Child | Parent and child domains in same forest | Yes | Disabled (intra-forest) |
| Tree-Root | Tree root and domain in same forest | Yes | Disabled (intra-forest) |
| Forest | Two forests | Configurable | Enabled (inter-forest) |
| External | AD domain and non-AD realm | No | Enabled |
| Shortcut | Optimize trust path | Yes | Depends |

## Attack Scenario Matrix

| # | Scenario | Source | Target | Key Technique |
|---|----------|--------|--------|---------------|
| 01 | Child-to-Parent Domain | Child domain | Parent domain | ExtraSids golden ticket with Enterprise Admins SID |
| 02 | Forest Trust Abuse | Domain in forest | Other forest | TDO abuse, inter-realm Kerberos |
| 03 | Cross-Forest Attack | Domain in forest | Other forest | Kerberoasting, ACL abuse across trusts |
| 04 | DC Compromise via Print Server + Delegation | Domain in forest | Domain Controller | Printer Bug + Unconstrained Delegation |

## Attack Flow Diagram

```
Compromise Child Domain
       │
       ▼
Enumerate Trusts ──► Identify Parent-Child Relationship
       │
       ▼
Extract krbtgt Hash (Child DC)
       │
       ▼
Forge Golden Ticket with ExtraSids (Enterprise Admins SID)
       │
       ▼
Authenticate to Parent DC ──► DCSync Parent Domain
       │
       ▼
Compromise Entire Forest

───────────────────────────────────

Compromise Domain in Forest A
       │
       ▼
Enumerate Forest Trusts ──► Identify Forest B Trust
       │
       ▼
Check SID Filtering Status ──► SID Filtering Disabled? ──► ExtraSids Attack
       │                                               │
       │                                          (Enabled)
       ▼                                               │
Kerberoast Across Trust                               │
       │                                               │
       ▼                                               ▼
Access Resources in Forest B                Limited to Authenticated Users Only
```

## Table of Contents

| File | Title | Description |
|------|-------|-------------|
| [01_Child_to_Parent_Domain.md](./01_Child_to_Parent_Domain.md) | Child-to-Parent Domain Attack | Escalate from child to parent domain via SID history abuse |
| [02_Forest_Trust_Abuse.md](./02_Forest_Trust_Abuse.md) | Forest Trust Abuse | Abuse forest trust relationships for cross-forest access |
| [03_Cross_Forest_Attack.md](./03_Cross_Forest_Attack.md) | Cross-Forest Attack | Kerberoasting and ACL abuse across forest trusts |
| [04_DC_Print_Server_Kerberos_Delegation.md](./04_DC_Print_Server_Kerberos_Delegation.md) | DC Compromise via Print Server + Delegation | DC compromise via Printer Bug, unconstrained delegation, and Kerberos |

## Prerequisites

- Domain Admin (or equivalent) on the source domain
- Ability to extract krbtgt hash or trust keys
- Network connectivity between domains (ports 88, 389, 445, 135)
- Knowledge of the target domain/forest SID
- PowerView, Mimikatz, Rubeus, Impacket on the attack host

## OPSEC Considerations

- Golden ticket creation with extra SIDs generates no event on the child DC (ticket is forged offline)
- TGS requests using the forged ticket will generate 4769 events on the parent DC
- DCSync across trusts generates replication events (4662) on the target DC
- Cross-domain authentication attempts are logged in both domains
- SID history queries (sidHistory=*) are specific LDAP filters that can trigger detection rules
