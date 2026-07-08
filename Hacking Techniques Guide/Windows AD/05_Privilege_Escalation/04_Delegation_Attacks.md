# Kerberos Delegation Attacks

## Overview

Kerberos delegation allows a service to impersonate a user when accessing resources. There are three types of delegation in Active Directory, each with distinct security implications and attack paths.

## Delegation Types

| Type | Attribute | Description | Attack Difficulty |
|------|-----------|-------------|------------------|
| **Unconstrained Delegation** | `TRUSTED_FOR_DELEGATION` (TGT delegation) | Service can impersonate user to ANY service | Medium (needs SpoolSample) |
| **Constrained Delegation** | `msDS-AllowedToDelegateTo` | Service can impersonate user to SPECIFIC services | Medium (needs hash) |
| **Resource-Based Constrained Delegation (RBCD)** | `msDS-AllowedToActOnBehalfOfOtherIdentity` | Target resource controls who can delegate to it | Low (if you have rights) |

## Attack Flow Decision Tree

```
┌─────────────────────────────────┐
│ Have you found delegation?       │
└────────────────┬────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
Unconstrained           Constrained
    │                         │
    ├─ SpoolSample            ├─ Know plaintext/hash?
    │  (Printer Bug)          │  ├─ YES → S4U2Self/S4U2Proxy
    │  + Rubeus monitor       │  │       (Rubeus s4u / getST.py)
    │  → TGT capture          │  └─ NO  → Need to crack or find
    │                         │
    └────────────┬────────────┘
                 ▼
           Resource-Based
           Constrained Delegation
                 │
                 ├─ Have Write/GenericAll on target?
                 │  ├─ YES → Set msDS-AllowedToActOnBehalfOfOtherIdentity
                 │  │       → Impersonate
                 │  └─ NO  → Need other path
                 │
                 └─ Also usable from Computer takeover
```

## Enumeration Overview

### PowerView

```powershell
# Unconstrained delegation computers
Get-DomainComputer -Unconstrained

# Constrained delegation (users)
Get-DomainUser -TrustedToAuth

# Constrained delegation (computers)
Get-DomainComputer -TrustedToAuth

# All delegation info for an object
Get-DomainObject -Identity computer01 -Properties msDS-AllowedToDelegateTo

# RBCD (who can delegate to a computer)
Get-DomainComputer -Identity target_computer -Properties msDS-AllowedToActOnBehalfOfOtherIdentity

# Find computers with msDS-AllowedToActOnBehalfOfOtherIdentity set
Get-DomainComputer -LDAPFilter "(msDS-AllowedToActOnBehalfOfOtherIdentity=*)"
```

### BloodHound

```cypher
// Unconstrained delegation
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

// Constrained delegation computers
MATCH (c:Computer) WHERE c.allowedtodelegate IS NOT NULL RETURN c.name, c.allowedtodelegate

// Constrained delegation users
MATCH (u:User) WHERE u.trustedtoauth IS NOT NULL RETURN u.name, u.trustedtoauth

// Resource-based constrained delegation
MATCH (c:Computer)<-[:AllowedToDelegate]-(n) RETURN n.name, c.name

// Find all delegation paths to DA
MATCH (c:Computer {unconstraineddelegation:true})
MATCH (u:User)-[:HasSession]->(c)
MATCH (u)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN c.name, u.name
```

### NetExec

```bash
# Find unconstrained delegation
nxc ldap dc01 -u user -p pass --trusted-for-delegation

# Find constrained delegation
nxc ldap dc01 -u user -p pass --trusted-to-auth

# Find all delegation
nxc ldap dc01 -u user -p pass -M delegation
```

## Attack Techniques Comparison

| Attack | Requires | Leverages | Result |
|--------|----------|-----------|--------|
| Unconstrained (Printer Bug) | Admin on unconstrained server | SpoolSample → TGT capture | Any user's TGT |
| Constrained (S4U2Self/S4U2Proxy) | User/computer hash for delegated account | Protocol transition + constrained delegation | TGS to any service |
| RBCD | Write/GenericAll/GenericWrite on target | msDS-AllowedToActOnBehalfOfOtherIdentity | TGS as any user to target |

## OPSEC Overview

| Attack | Events Generated | Detection Difficulty |
|--------|-----------------|---------------------|
| SpoolSample (Printer Bug) | 4688, 5156, 7036 | Medium |
| Rubeus monitor | None locally | Low (network Kerberos) |
| Rubeus s4u | 4769 (TGS requests) | Medium (unusual TGS) |
| getST.py | 4769 (TGS requests) | Medium |
| RBCD attribute set | 5136 | Low if quiet |

## Quick Enumeration Reference

```powershell
# Find unconstrained computers
Get-DomainComputer -Unconstrained

# Find constrained users/computers
Get-DomainUser -TrustedToAuth
Get-DomainComputer -TrustedToAuth

# Find RBCD relationships
Get-DomainComputer target -Properties msDS-AllowedToActOnBehalfOfOtherIdentity

# BloodHound unconstrained delegation
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

# BloodHound constrained delegation services
MATCH (c:Computer) WHERE c.allowedtodelegate IS NOT NULL RETURN c.name, c.allowedtodelegate

# BloodHound RBCD
MATCH (c:Computer)<-[:AllowedToDelegate]-(n) RETURN n.name, c.name
```
