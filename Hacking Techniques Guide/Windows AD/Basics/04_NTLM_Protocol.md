# NTLM Authentication Protocol

## What it is

NTLM (NT LAN Manager) is a suite of authentication protocols from Microsoft. It was the primary authentication protocol in Windows NT before Kerberos. In modern Active Directory environments, NTLM is a **fallback protocol** used when Kerberos authentication fails or is unavailable.

NTLM encompasses:
- **LM authentication** — legacy, weak, disabled by default
- **NTLMv1** — deprecated, easily cracked
- **NTLMv2** — current version, still widely used but weaker than Kerberos

## Hash types

### LM hash

The LM (LAN Manager) hash is the oldest, dating back to OS/2. It is **extremely weak**.

**How it's computed:**

```
1. Convert password to UPPERCASE (14 chars max)
2. Pad/truncate to 14 bytes
3. Split into two 7-byte halves
4. Each 7-byte half is used as a key for DES ECB encryption
5. Each half encrypts the constant string "KGS!@#$%"
6. Concatenate the two 8-byte ciphertexts → 16-byte LM hash
```

**Weaknesses:**
- Password truncated to 14 characters
- Password forced to uppercase (reduces keyspace)
- DES keys have parity bits (effective 56 bits per half)
- Each 7-byte half can be cracked independently (max 2^56 per half)
- Empty password halves are instantly recognizable

### NT hash (NTLM hash)

The NT hash is the modern hash used in NTLMv1 and NTLMv2. It is the hash stored in AD's NTDS.dit.

**How it's computed:**

```
NT-HASH = MD4(UTF-16-LE(password))
```

- Input: Password encoded as UTF-16 little-endian (no length limit)
- Output: 128-bit hash (16 bytes)
- Algorithm: MD4 (a single round, no salt)

**Key point:** The NT hash is the **master secret** in modern Windows authentication. If an attacker obtains an NT hash, they can:
- Authenticate as that user via NTLM (pass-the-hash)
- Request Kerberos tickets using RC4 encryption (overpass-the-hash)
- Decrypt Kerberos service tickets encrypted with RC4

### Hash storage in AD

In NTDS.dit:

| Attribute | Content |
|-----------|---------|
| `unicodePwd` | NTLM hash (and potentially LM hash) |
| `dBCSPwd` | LM hash (if stored) |
| `ntPwdHistory` | Previous NTLM hashes (up to 24 by default) |
| `supplementalCredentials` | Kerberos keys (AES128, AES256, RC4) + Digest hashes |

The `supplementalCredentials` attribute is especially valuable to attackers — it contains:
- RC4-HMAC key (same as NTLM hash)
- AES128-HMAC-SHA1 key
- AES256-HMAC-SHA1 key
- Digest (MD5) hashes

## NTLM authentication flow

NTLM uses a **challenge-response** mechanism — the password is never sent over the network.

### Three-step handshake

```
Client                                      Server
  │                                            │
  │  1. NEGOTIATE                              │
  │  ──────────────────────────────────────→  │
  │  • Version info                            │
  │  • Supported flags (NTLMv2, signing, etc.) │
  │  • Domain name (optional)                  │
  │                                            │
  │  2. CHALLENGE                              │
  │  ←──────────────────────────────────────  │
  │  • Server nonce (8-byte challenge)         │
  │  • Target info (server domain, DNS info)   │
  │  • Negotiated flags                        │
  │  • Target name                             │
  │                                            │
  │  3. AUTHENTICATE                           │
  │  ──────────────────────────────────────→  │
  │  • Username                                │
  │  • Domain name                             │
  │  • LMv2/NTLMv2 response (the proof)        │
  │  • Client nonce/timestamp                  │
  │  • Session key (encrypted)                 │
  │  • Version info                            │
  │                                            │
```

### NTLMv1 response computation

```
NTLMv1-Hash = NTLM-Hash (same as NT hash)
Response = DES(NT-Hash[0..7], Server-Challenge) ||
           DES(NT-Hash[8..15], Server-Challenge) ||
           DES(LM-Hash[0..7], Server-Challenge)
```

**Three DES encryptions:**
1. First 7 bytes of NT hash as DES key, encrypt the 8-byte challenge
2. Second 7 bytes of NT hash as DES key, encrypt the 8-byte challenge
3. First 7 bytes of LM hash as DES key, encrypt the 8-byte challenge

NTLMv1 response is 24 bytes.

### NTLMv2 response computation (modern)

```
NTLMv2-Hash = HMAC-MD5(NT-Hash, UpperCase-Username + Domain)
NTLMv2-Response = HMAC-MD5(NTLMv2-Hash, Server-Challenge + Blob)

Where Blob contains:
  - Client timestamp (8 bytes, 64-bit filetime)
  - Client nonce (8 bytes random)
  - Target info (variable, from CHALLENGE message)
  - MIC (Message Integrity Code, optional)
```

The full NTLMv2 response is sent as:

```
╔═══════════════════════════════════════════════════╗
║ NTLMv2 AUTHENTICATE message                       ║
║                                                   ║
║  LMv2 Response (24 bytes):                        ║
║    ┌───────────────────────────────────────────┐  ║
║    │ Client nonce (8 bytes)                     │  ║
║    │ HMAC-MD5 output (16 bytes)                │  ║
║    └───────────────────────────────────────────┘  ║
║                                                   ║
║  NTLMv2 Response (variable):                      ║
║    ┌───────────────────────────────────────────┐  ║
║    │ HMAC-MD5 output (16 bytes)                 │  ║
║    │ Blob:                                      │  ║
║    │   - Timestamp (8 bytes)                   │  ║
║    │   - Client nonce (8 bytes)                │  ║
║    │   - Target info (variable)                │  ║
║    │   - MIC (16 bytes, optional)              │  ║
║    └───────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════╝
```

## NTLMSSP (NTLM Security Support Provider)

NTLMSSP is the Security Support Provider (SSP) implementation of NTLM. It packages NTLM messages for transport over other protocols like SMB, HTTP, or RPC.

NTLMSSP messages are embedded in application-layer protocols. For example:

- **SMB:** NTLMSSP is negotiated during SMB `SESSION_SETUP` commands
- **HTTP:** NTLMSSP is carried in `WWW-Authenticate: NTLM` headers
- **RPC:** NTLMSSP is used as an RPC authentication service

### NTLMSSP message structure

All NTLMSSP messages share a common header:

```
╔═══════════════════════════════════════════════════╗
║ NTLMSSP Header                                   ║
║   Signature: "NTLMSSP\0" (8 bytes)               ║
║   MessageType: uint32 (1=NEGOTIATE, 2=CHALLENGE, ║
║                            3=AUTHENTICATE)        ║
║   Payload: (message-specific fields)              ║
╚═══════════════════════════════════════════════════╝
```

## Net-NTLMv1 vs Net-NTLMv2

The terms **Net-NTLMv1** and **Net-NTLMv2** refer to the network packets (challenge-response pairs), as opposed to the stored hashes (NTLM hash).

| Term | What it means | Crackability |
|------|---------------|--------------|
| NTLM hash | The MD4 hash stored in AD | Crackable offline (no salt) |
| Net-NTLMv1 | NTLMv1 response to a challenge | Crackable with challenge/response pairs |
| Net-NTLMv2 | NTLMv2 response to a challenge | Crackable but slower due to HMAC |

**Net-NTLMv1** is critically weak — the challenge-response can be cracked to recover the NTLM hash, or used in a **pass-the-challenge** attack.

**Net-NTLMv2** is the default in modern Windows. The HMAC construction makes cracking more expensive, but online brute-force or relay attacks are still viable.

## LMCompatibilityLevel

This setting controls **which NTLM versions a Windows system will send or accept**:

| Level | Sent by client | Accepted by server |
|-------|---------------|-------------------|
| 0 | LM and NTLMv1 | LM, NTLMv1, NTLMv2 |
| 1 | NTLMv1 (session security) | LM, NTLMv1, NTLMv2 |
| 2 | NTLMv2 only | LM, NTLMv1, NTLMv2 |
| 3 | NTLMv2 only | NTLMv1, NTLMv2 (rejects LM) |
| 4 | NTLMv2 only | NTLMv2 only (rejects LM and NTLMv1) |
| 5 | NTLMv2 only | NTLMv2 only (same as 4, but DCs reject LM/NTLMv1 for domain accounts) |

**Recommendation:** Level 5 for all systems. Level 4 is acceptable. Levels 0-2 are dangerous.

## NTLM auditing

Enable NTLM auditing via Group Policy to identify NTLM usage:

- **Network Security: Restrict NTLM: Audit NTLM authentication in this domain** → Enable
- **Network Security: Restrict NTLM: Audit NTLM authentication in this domain** → Enable for domain accounts
- **Network Security: Restrict NTLM: Add remote server exceptions for NTLM authentication** → Configure exempted servers

View NTLM usage with:
```powershell
# Check NTLM sessions
Get-WmiObject -Class Win32_LogonSession | Where-Object {$_.AuthenticationPackage -eq "NTLM"}

# Event logs
Get-WinEvent -LogName "Microsoft-Windows-NTLM/Operational" | Select-Object -First 10
```

## When NTLM falls back

NTLM is used when Kerberos is unavailable or fails. Common scenarios:

1. **Client cannot contact KDC** — no DC reachable (offline network, VPN disconnected)
2. **Cross-platform** — non-Windows systems connecting to Windows shares (Samba, etc.)
3. **Service doesn't have an SPN** — Kerberos requires a valid SPN for the target service
4. **Client explicitly sends NTLM** — some applications hardcode NTLM
5. **Firewall blocks Kerberos** — port 88 blocked between client and DC
6. **Local logon** — NTLM is used for local account authentication (workstation/local SAM)
7. **IIS/OWA with NTLM** — many web applications use NTLM for Windows integrated auth

## Domain cached credentials (MSCache2 / DCC2)

When a domain-joined computer cannot contact a DC, it caches the user's domain credentials locally. These are stored as **MSCache2 (DCC2)** hashes.

**How it works:**
```
DCC2-Hash = MD4( MD4(NT-Hash) + Username )
```

- Stored in `HKEY_LOCAL_MACHINE\SECURITY\Cache`
- Default cache size: 10 entries (configurable via Group Policy)
- Uses the user's NTLM hash plus username as inputs
- **Salting:** the hash is salted with the username (unlike the plain NTLM hash)

**Attack:** The MS Cache files can be extracted from a local SAM/SECURITY hive dump (e.g., via `secretsdump.py`) and cracked offline. Each entry takes about as long to crack as an NTLM hash.

## NTLM relay basics

NTLM relay is one of the most dangerous NTLM-based attacks.

### How it works

```
Attacker                          Victim Client              Target Server
  │                                 │                          │
  │     1. Connect to attacker      │                          │
  │  ←────────────────────────────  │                          │
  │                                 │                          │
  │     2. Send NTLM NEGOTIATE      │                          │
  │  ────────────────────────────→  │                          │
  │                                 │                          │
  │     3. Receive CHALLENGE         │                          │
  │  ←────────────────────────────  │                          │
  │                                 │                          │
  │                     4. Connect to Target Server            │
  │  ────────────────────────────────────────────────────────→ │
  │                                                           │
  │                    5. Relay NTLM NEGOTIATE                 │
  │  ────────────────────────────────────────────────────────→ │
  │                                                           │
  │                    6. Receive CHALLENGE from target         │
  │  ←────────────────────────────────────────────────────────│
  │                                                           │
  │     7. Send victim the target's challenge (instead of     │
  │        the attacker's challenge)                          │
  │  ────────────────────────────→  │                          │
  │                                 │                          │
  │     8. Receive AUTHENTICATE     │                          │
  │     (response to the target's   │                          │
  │      challenge)                 │                          │
  │  ←────────────────────────────  │                          │
  │                                 │                          │
  │                    9. Relay AUTHENTICATE message            │
  │  ────────────────────────────────────────────────────────→ │
  │                                                           │
  │                    10. Access granted                      │
  │  ←──────────────────────────────────────────────────────── │
```

The attacker relays the challenge-response to a different server (like a DC or SQL server), gaining access as the victim.

### Relay targets

- **SMB (to DC)** — authenticate to a DC's SMB share, dumping credentials (DCSync, etc.)
- **LDAP (to DC)** — authenticate over LDAP, creating/modifying directory objects
- **HTTP/OWA/EWS** — authenticate to Exchange Web Services
- **MSSQL** — authenticate to SQL Server
- **IMAP/POP3** — authenticate to email services

### NTLM relay mitigations

- **SMB signing** — required. Relayed SMB connections fail if signing is enforced.
- **LDAP signing + channel binding** — prevents LDAP relay.
- **Extended Protection for Authentication (EPA)** — binds the TLS channel to the NTLM exchange.
- **Disable NTLM** — if possible, use Kerberos only.

## Ports used for NTLM

NTLM itself does not use fixed ports. It rides over application protocols:

| Protocol | Ports | Usage |
|----------|-------|-------|
| SMB | 445/TCP | SMB session setup with NTLMSSP |
| HTTP | 80/TCP, 443/TCP | NTLM in WWW-Authenticate headers |
| LDAP | 389/TCP, 636/TCP | LDAP bind with SASL NTLM |
| SMTP | 25/TCP, 587/TCP | NTLM for mail authentication |
| IMAP | 143/TCP, 993/TCP | NTLM for mail authentication |
| POP3 | 110/TCP, 995/TCP | NTLM for mail authentication |
| RPC | 135/TCP + dynamic | NTLMSSP in RPC authentication |

## How attackers abuse NTLM

| Attack | Description |
|--------|-------------|
| **Pass-the-Hash (PtH)** | Use an NTLM hash directly to authenticate via NTLM (no password needed). Works because NTLM uses the hash as the secret |
| **NTLM relay** | Relay an NTLM challenge-response to gain access to another server |
| **NTLM cracking** | Capture Net-NTLMv1/v2 hashes (e.g., via Responder) and crack them offline to recover the plaintext password |
| **NTLMv1 cracking** | NTLMv1 challenge-responses can be cracked in minutes (only 2^56 keyspace per 7-byte chunk) |
| **SMB relay (SMB->SMB)** | Steal SMB authentication and relay to another SMB server |
| **SMB->LDAP relay** | Steal SMB authentication and relay to LDAP on a DC to add a user/modify ACLs |
| **WebDAV/NTLM** | Trick user to authenticate to attacker's WebDAV server via an Office document |
| **InetMgr/LDAP relay** | Relay captured NTLM to IIS with LDAP binding |
| **MS-Exchange relay** | Relay NTLM to Exchange Web Services for email access |
| **NTLM hash theft** | Use a shortcut (.lnk) file or "file://" URL pointing to attacker's SMB share to steal hash |

## Defender recommendations

1. **Disable NTLM entirely** — if Kerberos works everywhere, set `LMCompatibilityLevel = 5` and `Restrict NTLM: NTLM authentication in this domain = Deny all`.

2. **If NTLM is required:** audit first (`Audit NTLM authentication in this domain = Enable`) before moving to `Deny for domain accounts` then `Deny all`.

3. **Enable SMB signing** — for all systems (set `Microsoft network server: Digitally sign communications (always)` via GPO).

4. **Enable LDAP signing + channel binding** — prevents LDAP relay attacks.

5. **Use Extended Protection for Authentication (EPA)** on IIS and other web applications.

6. **Block outbound SMB (445)** on firewalls — prevents credential theft via file:// URLs.

7. **Educate users** — do not click links starting with `file://` or `\\attacker`.

8. **Enable Windows Defender Firewall** — block inbound RPC dynamic ports where possible.

9. **Monitor NTLM events:**
   - Event ID 4624: Account logon (NTLM)
   - Event ID 4776: NTLM credential validation
   - NTLM Operational log (Microsoft-Windows-NTLM/Operational)

10. **Use Network Security: Restrict NTLM: Add remote server exceptions** — allow only known servers to use NTLM.

11. **Set password policies** — enforce strong passwords (15+ characters) to slow offline cracking.

## Relevant RFCs and MS protocols

| Document | Description |
|----------|-------------|
| [MS-NLMP] | NT LAN Manager (NTLM) Authentication Protocol Specification |
| [MS-NTHT] | NTLM Hash and Password Storage |
| [MS-APDS] | Authentication Protocol Domain Support |
| [MS-LSAP] | Local Security Authority (Domain Policy) Protocol |
| RFC 1321 | MD4 (used for NTLM hash) |
| RFC 2104 | HMAC: Keyed-Hashing for Message Authentication (used in NTLMv2) |
