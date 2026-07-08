# Kerberos Attacks

## Overview

Kerberos is the default authentication protocol in Active Directory. Understanding Kerberos internals is essential for offensive AD operations because many high-impact attacks target Kerberos messages, tickets, or delegation mechanisms.

## Kerberos Protocol Flow

```
1. AS-REQ  → Client → KDC (Authentication Service)
   - Client sends timestamp encrypted with user's NT hash (pre-authentication)
   - Username + Domain + Encrypted timestamp

2. AS-REP  → KDC → Client
   - TGT (Ticket-Granting Ticket) encrypted with krbtgt hash
   - Session key encrypted with user's NT hash
   - PAC (Privilege Attribute Certificate) inside TGT

3. TGS-REQ → Client → KDC (Ticket-Granting Service)
   - TGT + Authenticator + SPN (Service Principal Name)

4. TGS-REP → KDC → Client
   - Service Ticket (ST) encrypted with target service account's hash
   - Session key encrypted with TGT session key

5. AP-REQ  → Client → Application Server
   - Service Ticket + Authenticator
   - Server verifies using its own password hash
```

## Ticket Structure

```
Kerberos Ticket (TGT/ST):
  ┌─────────────────────────────────┐
  │ Privilege Attribute Certificate │  (PAC - contains group SIDs, user info)
  │   - User SID                    │
  │   - Group SIDs                  │
  │   - Logon time                  │
  │   - Extra SIDs                  │
  ├─────────────────────────────────┤
  │ Encrypted with target key       │  (krbtgt for TGT, service account for ST)
  │ (Client cannot read/modify)     │
  └─────────────────────────────────┘
```

## Authentication Service (AS) Exchange

- **AS-REQ**: Client sends pre-authentication data (timestamp encrypted with user's NT hash) to KDC
- **AS-REP**: KDC responds with TGT (encrypted with krbtgt hash) and session key (encrypted with user's key)
- **Without pre-auth**: If `DONT_REQ_PREAUTH` is set, client can request TGT without proving knowledge of password → **AS-REP Roasting**

## Ticket-Granting Service (TGS) Exchange

- **TGS-REQ**: Client presents TGT + authenticator + desired SPN
- **TGS-REP**: KDC responds with service ticket encrypted with the target service account's key
- **Offline brute force**: The service ticket can be extracted and cracked offline → **Kerberoasting**

## Attack Surface Summary

| Attack | Target | Key Required | Pre-auth | DC Contact |
|--------|--------|--------------|----------|------------|
| AS-REP Roasting | User hash (pre-auth disabled) | None | Bypassed | Yes (AS-REQ) |
| Kerberoasting | Service account hash | User creds | Normal | Yes (TGS-REQ) |
| Golden Ticket | krbtgt hash | Domain Admin | N/A | No (forged offline) |
| Silver Ticket | Service account hash | Service creds | N/A | No (forged offline) |
| Diamond Ticket | krbtgt AES key | Domain Admin | N/A | Decrypt + re-encrypt |
| Skeleton Key | DC memory | Domain Admin | N/A | Yes (on DC) |
| Delegation Abuse | Various | Varies | N/A | Varies |

## Key Kerberos Event IDs

| Event ID | Description |
|----------|-------------|
| 4768 | Kerberos TGT requested (AS-REQ/AS-REP) |
| 4769 | Kerberos service ticket requested (TGS-REQ/TGS-REP) |
| 4770 | Kerberos service ticket renewed |
| 4771 | Kerberos pre-authentication failed |
| 4772 | Kerberos authentication ticket request failed |
| 4648 | Logon with explicit credentials |
| 4672 | Admin logon (special privileges assigned) |

## Common Encryption Types

| etype | Type | Notes |
|-------|------|-------|
| 23 | RC4-HMAC | Most common, weakest, crackable with `-m 13100`/`-m 18200` |
| 17 | AES128-CTS-HMAC-SHA1 | Stronger, crackable with `-m 19600` |
| 18 | AES256-CTS-HMAC-SHA1 | Strongest, crackable with `-m 19600` |

## Tools Used

- **Impacket** (Python/Kali): `GetNPUsers.py`, `GetUserSPNs.py`, `ticketer.py`, `getST.py`, `goldenPac.py`
- **Rubeus** (C#/.NET): `asreproast`, `kerberoast`, `golden`, `diamond`, `s4u`, `asktgt`
- **Mimikatz** (C): `kerberos::golden`, `kerberos::tgt`, `misc::skeleton`, `sekurlsa::tickets`
- **Hashcat**: `-m 18200` (AS-REP), `-m 13100` (Kerberoast RC4), `-m 19600` (Kerberoast AES)

## Technique Files

| # | File | Description |
|---|------|-------------|
| 01 | [AS-REP Roasting](01_ASREPRoast_Deep.md) | Exploit DONT_REQ_PREAUTH for credential harvesting |
| 02 | [Kerberoasting](02_Kerberoasting_Deep.md) | Service ticket request and offline cracking |
| 03 | [Golden Ticket](03_Golden_Ticket.md) | Forge TGT using krbtgt hash |
| 04 | [Silver Ticket](04_Silver_Ticket.md) | Forge service ticket using service account hash |
| 05 | [Diamond Ticket](05_Diamond_Ticket.md) | Modify existing TGT with custom PAC |
| 06 | [Skeleton Key](06_Skeleton_Key.md) | Patch DC LSASS to accept any password |
| 07 | [Delegation Abuse](07_Kerberos_Delegation.md) | Unconstrained, constrained, and RBCD attacks |
| 08 | [Enterprise Admin Cross-Forest](08_Enterprise_Admin_Cross_Forest.md) | From Domain Admin to Enterprise Admin |
| 09 | [Kerberos RC4 TGS](09_Kerberos_RC4_TGS.md) | Forcing RC4 TGS when AES is enabled |
