# Kerberos Protocol in Active Directory

## What it is

Kerberos is a network authentication protocol designed by MIT and adopted by Microsoft as the **primary authentication protocol** for Active Directory. It provides mutual authentication — both the client and the server verify each other's identity — without transmitting passwords over the network.

In AD, Kerberos version 5 (RFC 4120) is the default. NTLM is used only as a fallback when Kerberos is unavailable.

## Protocol flow — The Kerberos exchange

Kerberos involves three parties:

- **Client** — the user or service requesting authentication
- **KDC (Key Distribution Center)** — the Domain Controller running the `kdc` service; handles AS and TGS roles
- **Service** — the resource the client wants to access (server, file share, etc.)

The KDC has two components:

1. **Authentication Service (AS)** — issues Ticket Granting Tickets (TGTs)
2. **Ticket Granting Service (TGS)** — issues service tickets

### Step 1: AS-REQ / AS-REP (Authentication Service Exchange)

```
Client                                  KDC (DC)
  │                                        │
  │  AS-REQ                                │
  │  ──────────────────────────────────→   │
  │  • sAMAccountName (username)           │
  │  • Domain name (realm)                 │
  │  • Encrypted timestamp                 │
  │    (pre-authentication data)          │
  │                                        │
  │  AS-REP                                │
  │  ←──────────────────────────────────  │
  │  • TGT (encrypted with KRBTGT hash)   │
  │  • Logon session key (encrypted        │
  │    with client's long-term key)        │
  │                                        │
```

**Pre-authentication:** The client encrypts a timestamp with its long-term key (derived from the password hash). Without this, the KDC returns no ticket. This prevents offline brute-force attacks.

**Pre-authentication timestamp format:**

```
╔══════════════════════════════════════════════════╗
║ PA-ENC-TIMESTAMP (type 2)                       ║
║                                                  ║
║  KerberosTime ::= 2026-07-08T14:30:00Z           ║
║  Encrypted with client key (RC4-HMAC or AES)    ║
╚══════════════════════════════════════════════════╝
```

**TGT structure (encrypted with KRBTGT hash):**

```
╔══════════════════════════════════════════════════╗
║ Ticket (TGT)                                     ║
║  tkt-vno  : 5                                    ║
║  realm    : CORP.EXAMPLE.COM                     ║
║  sname    : krbtgt/CORP.EXAMPLE.COM              ║
║  enc-part : (encrypted with KRBTGT hash)         ║
║    ┌──────────────────────────────────────────┐  ║
║    │ Flags       : forwardable, renewable,...  │  ║
║    │ Authtime    : 2026-07-08T14:30:00Z        │  ║
║    │ Starttime   : 2026-07-08T14:30:00Z        │  ║
║    │ Endtime     : 2026-07-09T00:30:00Z        │  ║
║    │ Renew-till  : 2026-07-15T14:30:00Z        │  ║
║    │ Client      : jsmith@CORP.EXAMPLE.COM     │  ║
║    │ caddr       : 10.10.10.50                 │  ║
║    │ Authorization-data: PAC                   │  ║
║    │   ├── Logon Info (user SID, group SIDs)   │  ║
║    │   ├── Credential Info                     │  ║
║    │   ├── Server Checksum (KRBTGT key)        │  ║
║    │   └── PrivSvr Checksum (KRBTGT key)       │  ║
║    └──────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════╝
```

### Step 2: TGS-REQ / TGS-REP (Ticket Granting Service Exchange)

```
Client                                  KDC (DC)
  │                                        │
  │  TGS-REQ                               │
  │  ──────────────────────────────────→   │
  │  • TGT (from AS-REP)                   │
  │  • Authenticator (timestamp encrypted  │
  │    with logon session key)            │
  │  • Service principal name (SPN)        │
  │    e.g., HOST/fileserver.corp.com      │
  │                                        │
  │  TGS-REP                               │
  │  ←──────────────────────────────────  │
  │  • Service ticket (encrypted with      │
  │    target service's long-term key)     │
  │  • Session key for service (encrypted  │
  │    with logon session key)             │
  │                                        │
```

**Service ticket (ST) structure (encrypted with service account's NTLM hash):**

```
╔══════════════════════════════════════════════════╗
║ Ticket (Service Ticket)                          ║
║  tkt-vno  : 5                                    ║
║  realm    : CORP.EXAMPLE.COM                     ║
║  sname    : HOST/fileserver.corp.com             ║
║  enc-part : (encrypted with service key)         ║
║    ┌──────────────────────────────────────────┐  ║
║    │ Flags       : forwardable, proxiable,... │  ║
║    │ Client      : jsmith@CORP.EXAMPLE.COM    │  ║
║    │ Authorization-data: PAC                  │  ║
║    │   (same PAC as TGT, relayed)             │  ║
║    └──────────────────────────────────────────┘  ║
╚══════════════════════════════════════════════════╝
```

### Step 3: AP-REQ / AP-REP (Application Request Exchange)

```
Client                                  Service
  │                                        │
  │  AP-REQ                                │
  │  ──────────────────────────────────→   │
  │  • Service ticket (ST)                 │
  │  • Authenticator (timestamp encrypted  │
  │    with service session key)           │
  │                                        │
  │  AP-REP (optional — mutual auth)       │
  │  ←──────────────────────────────────  │
  │  • Timestamp (encrypted with service   │
  │    session key)                        │
  │                                        │
```

The service:
1. Decrypts the service ticket with its own key
2. Extracts the session key and PAC
3. Verifies the authenticator timestamp
4. Validates the PAC signatures (if configured)
5. Creates a security context for the client

## PAC — Privilege Attribute Certificate

The PAC is the authorization data structure embedded inside Kerberos tickets used by Microsoft. It contains the user's security group memberships and privileges.

### PAC structure (`[MS-PAC]`)

```
PAC (PNID + multiple buffers)
│
├── KERB_VALIDATION_INFO (Logon Info)
│   ├── LogonTime, LogoffTime, KickOffTime
│   ├── PasswordLastSet
│   ├── UserSID (user's SID)
│   ├── GroupSIDs (group membership)
│   ├── ExtraSIDs (extra SIDs, e.g., from claims)
│   ├── UserAccountControl flags
│   ├── DomainSID
│   ├── DomainGroupSIDs
│   ├── ResourceGroupSIDs (for cross-domain)
│   └── LogonDomainName, UserName
│
├── CLIENT_INFO (Client Name/Full Name)
│
├── UPN_DNS_INFO (UPN and DNS domain)
│
├── SERVER_CHECKSUM (signed with service key)
│   └── Must be validated by the server
│
└── PRIVSVR_CHECKSUM (signed with KRBTGT key)
    └── Must be validated by the KDC
```

### PAC signature validation

- **PAC_SERVER_CHECKSUM** — The KDC signs the PAC with the target service's key. The service validates this when the ticket is presented, ensuring the KDC issued the ticket.
- **PAC_PRIVSVR_CHECKSUM** — The KDC signs the PAC with the KRBTGT account's key. This is used by the KDC during TGS requests to verify the PAC wasn't tampered with.

**CVE-2020-17049 (Kerberos Bronze Bit)**: If the KDC doesn't validate the PAC_PRIVSVR_CHECKSUM properly, an attacker can modify the PAC to escalate privileges.

## Encryption types

| Type | Enctype ID | Key Size | Used in AD |
|------|-----------|----------|------------|
| DES-CBC-CRC | 1 | 56-bit | Legacy; disabled by default since Windows 7/2008 R2 |
| DES-CBC-MD5 | 3 | 56-bit | Legacy; disabled by default |
| RC4-HMAC | 23 | 128-bit (MD5) | Default for backward compatibility; **most dangerous** — allows pass-the-hash |
| AES128-CTS-HMAC-SHA1-96 | 17 | 128-bit | Modern; preferred |
| AES256-CTS-HMAC-SHA1-96 | 18 | 256-bit | Modern; preferred |

RC4-HMAC (type 23) is significant for attackers because the NTLM hash is the key. If you have the NTLM hash, you can forge Kerberos tickets using RC4 encryption (no need to crack the password).

### Kerberos encryption flow

```
Password → NTLM hash → KERB_KEY (for RC4)
Password → NTLM hash + SHA1 → AES key (for AES128/256)
```

## The KRBTGT account

The `krbtgt` account is a **disabled, built-in account** on every DC (it exists in the AD database). Its password hash is known by every DC in the domain.

- The KRBTGT password **never expires** and is **rarely rotated**
- The KRBTGT hash is used to encrypt/decrypt all TGTs
- If an attacker obtains the KRBTGT hash, they can forge arbitrary TGTs (Golden Ticket attack)

## Kerberos policy

Kerberos policy is set via Group Policy at the domain level:

| Setting | Default | Description |
|---------|---------|-------------|
| Maximum lifetime for service ticket | 600 min | How long a TGS ticket is valid |
| Maximum lifetime for user ticket | 10 hours | How long a TGT is valid |
| Maximum lifetime for user ticket renewal | 7 days | How long a TGT can be renewed |
| Maximum tolerance for computer clock synchronization | 5 minutes | Max allowed clock skew between client and KDC |

## Clock skew

Kerberos requires that the client and KDC clocks be synchronized within 5 minutes (configurable). The timestamp in pre-authentication and authenticators is compared against the KDC's current time.

**Attack angle:** If an attacker can change a client's clock, they can replay old tickets. The 5-minute tolerance window is a common target for time-based attacks.

## S4U2Self and S4U2Proxy (Delegation)

### S4U2Self (Service-for-User-to-Self)

Allows a service to obtain a Kerberos service ticket to itself on behalf of a user. **No Kerberos delegation required** — the service doesn't need to have the user's credentials.

Use case: A web app with `ImpersonateLoggedOnUser` that wants to impersonate authenticed users.

### S4U2Proxy (Service-for-User-to-Proxy)

Allows a service to request a service ticket for another service on behalf of a user. This is **Kerberos delegation** — the service acts as a proxy for the user.

**Unconstrained delegation** (legacy):
- Allows a service to forward the user's TGT to any other service
- Set via `userAccountControl: TRUSTED_FOR_DELEGATION`
- **High risk** — if the service is compromised, the attacker can access any service as any user

**Constrained delegation** (modern):
- Limits which services the delegate can access
- Set via `msDS-AllowedToDelegateTo` attribute
- Protocol transition (S4U2Self + S4U2Proxy) allows transitioning from non-Kerberos auth (e.g., NTLM, Forms) to Kerberos

**Resource-based constrained delegation (RBCD)** (Windows 2012+):
- The target service specifies which accounts can delegate to it
- Set via `msDS-AllowedToActOnBehalfOfOtherIdentity` attribute on the target
- **Common attack:** if you have `GenericWrite` on a computer object, you can set this attribute to impersonate any user (e.g., domain admin) to that computer

```
S4U2Proxy Flow:

Client → Service A → KDC → Service B
            │
            └── S4U2Self: "Get me a ticket to myself as user jsmith"
                (Service A gets a ticket for jsmith → Service A)

            └── S4U2Proxy: "Get me a ticket to Service B as user jsmith"
                (Service A presents jsmith's TGT → gets ticket to Service B)
```

## Kerberos armoring (FAST)

Flexible Authentication via Secure Tunneling (FAST) — RFC 6113. Creates a protected tunnel between the client and KDC using a **trusted channel or armor key**.

- Prevents **Kerberoasting** over the wire (TGS-REQ packets containing the TGT are encrypted)
- Prevents **AS-REP Roasting** (AS-REP encryption failures are not observable)
- Requires Windows 8/2012 or later on client and DC sides
- Enabled via Group Policy: "Kerberos client support for FAST" and "Kerberos KDC support for FAST"
- Uses a **domain-joined machine's machine account key** to build the armor tunnel

## PKINIT

Public Key Cryptography for Initial Authentication (RFC 4556). Allows Kerberos authentication using **smart cards** or **certificates** instead of passwords.

- The client presents a certificate during AS-REQ (instead of pre-authentication timestamp)
- The KDC validates the certificate chain against the enterprise CA
- The resulting TGT is issued as normal

**Attack angle:** PKINIT can be used with certificate theft (see ADCS attacks — `PKI_ADCS_Architecture.md`).

## Cross-realm trusts and referrals

Kerberos referral: When a client requests a ticket for a service in another domain, the KDC either:

1. Returns a **referral ticket** (TGT for the target domain's KDC) if a trust exists
2. Issues a service ticket directly if the trust is within the same forest

```
Client → KDC(CORP) → "Need ticket to FILE.OTHERDOMAIN.COM"
KDC(CORP) → "I don't have that; here's a referral TGT for OTHERDOMAIN"
Client → KDC(OTHERDOMAIN) → "Here's the referral TGT; now give me a ticket to FILE"
KDC(OTHERDOMAIN) → "Here's your service ticket"
```

Cross-forest Kerberos requires **forest trust** and proper **name suffix routing**.

## Kerberos messages — Wire format

All Kerberos messages use ASN.1 DER encoding with the Kerberos protocol definition from RFC 4120.

```
╔═══════════════════════════════════════════════════╗
║ AS-REQ (KDC-REQ)                                 ║
║  pvno: 5                                         ║
║  msg-type: 10 (AS-REQ)                           ║
║  padata: [PA-PAC-REQUEST, PA-ENC-TIMESTAMP]      ║
║  req-body:                                       ║
║    cname: jsmith                                 ║
║    realm: CORP.EXAMPLE.COM                       ║
║    sname: krbtgt/CORP.EXAMPLE.COM                ║
║    till: 2026-07-09T00:30:00Z                    ║
║    kdc-options: forwardable, renewable           ║
╚═══════════════════════════════════════════════════╝
```

## How attackers abuse Kerberos

| Attack | Description | Key requirement |
|--------|-------------|-----------------|
| **Kerberoasting** | Request a service ticket for a service account; crack the NTLM hash offline from the TGS-REP | Valid domain user (no special privileges) |
| **AS-REP Roasting** | Request AS-REP for users with "Do not require Kerberos pre-authentication" set; get crackable encrypted data | Valid domain user, target user has `DONT_REQ_PREAUTH` |
| **Golden Ticket** | Forge a TGT using the KRBTGT hash | DA access (or DCSync) to get KRBTGT hash |
| **Silver Ticket** | Forge a service ticket using a service account's NTLM hash | Service account hash |
| **Overpass-the-Hash** | Use NTLM hash to request Kerberos tickets (RC4) | NTLM hash of a domain user |
| **Pass-the-Ticket** | Replay a captured TGT or service ticket | Ticket from a compromised session |
| **Diamond Ticket** | Decrypt a legitimate TGT, modify the PAC, re-encrypt with KRBTGT | KRBTGT hash |
| **Sapphire Ticket** | Modify the PAC_SERVER_CHECKSUM of a legitimate TGT when KDC doesn't validate it | Valid TGT + service key |
| **Bronze Bit** | CVE-2020-17049 — modify PAC in S4U2Proxy delegation tickets | Service with constrained delegation |
| **Delegation abuse** | Abuse RBCD, constrained delegation, or unconstrained delegation to impersonate users | Write access to `msDS-AllowedToActOnBehalfOfOtherIdentity` or compromised service |
| **DCSync** | Use replication to get KRBTGT hash or any user hash | Replication rights (often DA) |
| **Kerberos relay** | Relay Kerberos AP-REQ messages | N/A (variant of NTLM relay) |

## Defender recommendations

1. **Disable RC4 encryption** — Set `msDS-SupportedEncryptionTypes` to exclude RC4 (type 23). Forces AES-only Kerberos, preventing overpass-the-hash with RC4. Test carefully for backward compatibility.

2. **Rotate KRBTGT password** — Do this at least annually, and immediately after any suspected compromise. Use the two-step rotation method (reset twice with 10–24 hours gap) to avoid ticket issues.

3. **Monitor Kerberos events**:
   - Event ID 4768: TGT requested
   - Event ID 4769: Service ticket requested
   - Event ID 4770: TGT renewed
   - Event ID 4771: Pre-authentication failed (Kerberos)

4. **Enable Kerberos armoring (FAST)** — prevents offline cracking of TGS-REP (Kerberoasting).

5. **Set service account SPNs carefully** — only accounts that need SPNs should have them. Audit for unusual SPNs.

6. **Use Group Managed Service Accounts (gMSAs)** — automatic password rotation, no SPN exposure.

7. **Enforce strong service account passwords** — at least 25 characters, random.

8. **Audit delegation** — find all accounts with `TRUSTED_FOR_DELEGATION`, `TRUSTED_TO_AUTH_FOR_DELEGATION`, or `msDS-AllowedToActOnBehalfOfOtherIdentity` set.

9. **Enable "Kerberos client support for FAST" and "Kerberos KDC support for FAST"** via Group Policy.

10. **Monitor for anomalous TGT lifetimes** — TGTs with unusual durations may indicate Golden Tickets.

11. **Restrict KRBTGT replication** — only authorized users should be allowed to DS-Replication-Get-Changes-All.

## Relevant RFCs and MS protocols

| Document | Description |
|----------|-------------|
| RFC 4120 | The Kerberos Network Authentication Service (V5) |
| RFC 4121 | Kerberos V5 GSS-API Mechanism |
| RFC 4556 | Public Key Cryptography for Initial Authentication (PKINIT) |
| RFC 6113 | A Generalized Framework for Kerberos Pre-Authentication (FAST) |
| RFC 6806 | Kerberos Principal Name Canonicalization |
| RFC 8070 | PKINIT Freshness Extension |
| [MS-KILE] | Kerberos Protocol Extensions (Microsoft) |
| [MS-PAC] | Privilege Attribute Certificate Data Structure |
| [MS-SFU] | Kerberos Protocol Extensions: Service for User and Constrained Delegation Protocol |

## Ports used

| Port | Protocol | Direction | Purpose |
|------|----------|-----------|---------|
| 88/TCP, UDP | Kerberos | Client ↔ KDC | AS and TGS exchanges |
| 464/TCP, UDP | kpasswd | Client ↔ KDC | Kerberos password change |
| 445/TCP | SMB | Client ↔ KDC | Pass-through ticket requests (Netlogon) |
