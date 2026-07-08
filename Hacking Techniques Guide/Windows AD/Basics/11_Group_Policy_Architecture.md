# Group Policy Architecture

## What it is

Group Policy is Microsoft's infrastructure for centralized configuration management in Active Directory. It allows administrators to define security, desktop, and application settings for users and computers across the organization.

Group Policy is a **primary attack surface** because:
- It distributes configuration to all domain-joined machines
- Misconfigurations grant wide access
- SYSVOL (the storage for GPOs) is readable by all authenticated users
- Group Policy Preferences historically stored passwords

## GPO structure

A Group Policy Object (GPO) has two components:

### GPC (Group Policy Container)

Stored in AD (LDAP) under:
```
CN=Policies,CN=System,DC=corp,DC=example,DC=com
```

Contains:
- Version number
- Status (enabled/disabled)
- WMI filter link
- Security descriptor (who can read/apply the GPO)
- GPT path (path to the corresponding SYSVOL folder)
- Extensions list (which client-side extensions process this GPO)

### GPT (Group Policy Template)

Stored in SYSVOL at:
```
\\corp.example.com\SYSVOL\corp.example.com\Policies\{GPO-GUID}\
```

```
{GUID}\
+-- GPT.INI                (version info, display name)
+-- Machine\               (computer configuration)
|   +-- registry.pol       (registry settings for HKLM)
|   +-- Scripts\           (startup/shutdown scripts)
|   |   +-- Startup\
|   |   +-- Shutdown\
|   +-- Microsoft\Windows NT\SecEdit\
|   |   +-- GptTmpol.inf   (security template)
|   +-- Preferences\       (Group Policy Preferences)
|       +-- Registry.xml
|       +-- Shortcuts.xml
|       +-- ScheduledTasks.xml
|       +-- ...
+-- User\                  (user configuration)
|   +-- registry.pol       (registry settings for HKCU)
|   +-- Scripts\           (logon/logoff scripts)
|   |   +-- Logon\
|   |   +-- Logoff\
|   +-- Preferences\       (user preferences)
|       +-- ...
+-- Adm\                   (ADM/ADMX template files - legacy)
```

## GPC vs GPT summary

| Aspect | GPC | GPT |
|--------|-----|-----|
| Storage | Active Directory (LDAP) | SYSVOL (file system) |
| Path | `CN=Policies,CN=System,DC=domain` | `\\domain\SYSVOL\domain\Policies\{GUID}\` |
| Contents | Version, status, security filter | Registry.pol, scripts, preferences |
| Replication | AD replication | DFS-R or FRS |
| Access | LDAP (authenticated users) | SMB (authenticated users) |

## SYSVOL

SYSVOL is a shared directory on every DC that stores:
- Group Policy templates (GPT)
- Logon/logoff/startup/shutdown scripts
- Domain-wide files (folder redirection targets)

**Path:**
```
\\<domain>\SYSVOL\<domain>\         (shared as SYSVOL)
\\<domain>\SYSVOL\<domain>\SCRIPTS\ (shared as NETLOGON)
```

**Permission:** `Authenticated Users` have **Read** access by default. This is needed for GPO application but also means **any authenticated user can read all GPO files**.

### Attack angle: SYSVOL enumeration

```bash
# Read GPOs from SYSVOL
smbclient //dc01.corp.com/SYSVOL -U jsmith
> cd corp.com/Policies
> ls -R

# Download all GPO XML preferences (may contain cPassword)
import glob
gpp_path = "\\\\corp.com\\SYSVOL\\corp.com\\Policies\\"
for xml in glob.glob(gpp_path + "**/Preferences/**/*.xml", recursive=True):
    with open(xml) as f:
        content = f.read()
        if "cPassword" in content:
            print(f"Found cPassword in: {xml}")
```

## ADMX/ADML files

ADMX files define the registry-based policy settings available in Group Policy editors.

### ADMX (Administrative Template XML-based)

- Windows Vista+ format
- Stored in `%SystemRoot%\PolicyDefinitions\`
- Central store: `\\<domain>\SYSVOL\<domain>\Policies\PolicyDefinitions\`
- Language-neutral (.admx) + language-specific (.adml)

### ADM (Administrative Template Legacy)

- Windows 2000/XP format
- Stored inside the GPT itself (`.Adm` folder)
- INI-based format
- Deprecated but still supported

### Central Store

The Central Store is the recommended location for ADMX files. Create it at:
```
\\<domain>\SYSVOL\<domain>\Policies\PolicyDefinitions\
```

All DCs replicate this automatically via DFS-R.

## GPO processing order (LSDOU)

Group Policy is applied in a specific order — **Local, Site, Domain, OU**.

```
1. Local Group Policy (LGPO)
   - Applied first; lowest precedence
   - Stored in %SystemRoot%\System32\GroupPolicy

2. Site-level GPOs
   - Linked to the AD Site object
   - Applied after local policy

3. Domain-level GPOs
   - Linked to the domain object
   - Applied after site policies

4. OU-level GPOs
   - Applied in OU hierarchy order (parent → child)
   - Child OUs are processed last (highest precedence)
   - Multiple GPOs at the same level: link order (lowest number = highest precedence)
```

**Precedence (last writer wins):**
```
LGPO → Site → Domain → Parent OU → Child OU
(lowest)                              (highest)
```

**Multiple GPOs per level:** GPO link order determines priority. GPO with link order 1 wins over link order 2.

## GPO inheritance and blocking

By default, child containers inherit GPOs from parent containers.

### Inheritance blocking

An OU can be configured to **Block Inheritance**:
```
Domain: Default Domain Policy
  +-- OU: Servers (inherits domain policy)
       +-- OU: SQL Servers (Block Inheritance) -- ignores domain and parent OU policies
            (only GPOs linked directly to this OU apply)
```

### Enforcement (No Override)

A GPO can be set to **Enforced** (formerly "No Override"):
```
Enforced GPO at Domain level always applies, even if:
  - Child OU has "Block Inheritance"
  - Another GPO has conflicting settings
```

Precedence with enforcement:
```
Enforced GPOs (from highest to lowest level)
    |
Normal GPOs (LSDOU order, last writer wins)
```

## Security filtering

GPOs can be scoped to apply only to specific security groups.

### Default security filter

By default, only **Authenticated Users** have the `Apply Group Policy` permission (ACE). This means all authenticated users and computers get the GPO.

### Custom filtering

Change the security filter:
1. Remove `Authenticated Users`
2. Add specific security group (e.g., `Sales Users`)
3. Grant `Read` and `Apply Group Policy` permissions to that group

Only members of the specified group will receive the GPO settings.

## WMI filtering

WMI filters allow dynamically scoping GPOs based on system properties.

### Common WMI filters

```sql
-- Apply GPO only to Windows 10 workstations
SELECT * FROM Win32_OperatingSystem WHERE Version LIKE "10.%" AND ProductType = "1"

-- Apply GPO only to Windows Server 2019+
SELECT * FROM Win32_OperatingSystem WHERE Version LIKE "10.0.17%" AND ProductType = "2"

-- Apply GPO only to computers with more than 8GB RAM
SELECT * FROM Win32_ComputerSystem WHERE TotalPhysicalMemory > 8589934592

-- Apply GPO only to domain controllers
SELECT * FROM Win32_OperatingSystem WHERE ProductType = "2"
```

### Processing

1. During policy application, the client evaluates WMI filters
2. If the filter returns TRUE, the GPO applies
3. If the filter returns FALSE, the GPO is skipped
4. WMI filter evaluation is **slow** — excessive filters delay logon

## Loopback processing

Loopback processing changes how user policies are applied when a user logs onto a specific computer.

### Normal mode (default)

- User policy is applied based on the user's OU location
- Computer policy is applied based on the computer's OU location

### Loopback Merge mode

- User policy is applied from both the user's OU **and** the computer's OU
- Computer OU's user policies merge (last writer wins for conflicts)

### Loopback Replace mode

- User policy from the computer's OU **replaces** user policy from the user's OU
- Used for kiosk computers, terminal servers, and shared workstations

**Example:** A user in `OU=Sales` logs into a kiosk in `OU=Kiosks`. With Loopback Replace, the kiosk's user policies replace the Sales user policies, ensuring a locked-down experience.

## Administrative templates

Administrative Templates provide a UI for setting registry-based policy.

### ADMX policy structure

```
<policy name="DisableTaskMgr"
        class="User"
        displayName="$(string.DisableTaskMgr)"
        explainText="$(string.DisableTaskMgr_Explain)"
        key="Software\Microsoft\Windows\CurrentVersion\Policies\System"
        valueName="DisableTaskMgr">
    <enabledValue>
        <decimal value="1" />
    </enabledValue>
    <disabledValue>
        <decimal value="0" />
    </disabledValue>
</policy>
```

### ADMX policy categories

- **Computer Configuration → Administrative Templates**
  - Windows Components
  - System
  - Network
  - Printers
  - Start Menu and Taskbar
  - Desktop
  - Control Panel
  - Shared Folders

- **User Configuration → Administrative Templates**
  - (Same categories as Computer Configuration, but applied to HKCU)

## registry.pol

The `registry.pol` file contains the actual registry settings that will be applied to the target registry hive.

### File format

```
[RegistryPath1]
"ValueName1"=REG_TYPE:ValueData1
"ValueName2"=REG_TYPE:ValueData2

[RegistryPath2]
"ValueName"=REG_TYPE:ValueData
```

### Binary format (actual on-disk)

The `registry.pol` file uses a binary format with specific headers:

```
+-------------------------------+
| File Header (12 bytes)        |
|   - Magic: PReg\x00\x01       |
|   - Version: 1 or 3           |
+-------------------------------+
| Entry 1:                      |
|   - Key Size (2 bytes)        |
|   - Value Size (2 bytes)      |
|   - Type (4 bytes)            |
|   - Key Name (UTF-16)         |
|   - Value Name (UTF-16)       |
|   - Data (binary)             |
+-------------------------------+
| Entry 2: ...                  |
+-------------------------------+
```

For machine policies, the target is `HKLM\Software\Policies` (and subkeys).
For user policies, the target is `HKCU\Software\Policies` (and subkeys).

## GPO refresh interval

| Setting | Default | Range |
|---------|---------|-------|
| Computer GPO refresh | 90 minutes | 0-64800 minutes |
| User GPO refresh | 90 minutes | 0-64800 minutes |
| Random delay | 0-30 minutes | 0-1440 minutes |
| Security policy refresh | 16 hours (every 90 min+30 min at boot) | - |

### Manual refresh

```cmd
gpupdate /target:computer /force    # Refresh computer policies
gpupdate /target:user /force        # Refresh user policies
gpupdate /force                     # Refresh all policies

# Check applied GPOs
gpresult /r                         # Summary report
gpresult /h gporeport.html          # HTML report
gpresult /z                         # Detailed verbose output
```

## GPO versioning

Each GPO has version numbers stored in both the GPC (AD) and GPT (SYSVOL):

- **User version** — increments when user configuration changes
- **Computer version** — increments when computer configuration changes

During refresh, the client compares its cached version with the version in the GPC (AD). If the version hasn't changed, the GPO is not re-applied (performance optimization).

### Version mismatch

If the GPC and GPT versions don't match (due to replication latency), the GPO may not apply correctly. This is a common troubleshooting scenario:

```powershell
# Check GPO version info
Get-GPO -Name "Default Domain Policy" | Select-Object UserVersion, ComputerVersion

# Force replication
Repadmin /replicate
```

## Group Policy vs local policy

| Aspect | Group Policy (AD) | Local Policy (LGPO) |
|--------|-------------------|---------------------|
| Scope | All domain-joined computers/users | Single computer |
| Storage | AD + SYSVOL | `%SystemRoot%\System32\GroupPolicy` |
| Management | GPMC, PowerShell, AD | secpol.msc, gpedit.msc |
| Precedence | Applied after local (overrides) | Applied first (overridden by GPO) |
| Processing | Background refresh (90 min) | Applied at boot only |
| Security Filtering | Yes (groups, WMI) | No |
| Loopback | Yes (merge/replace) | No |
| Targeting | Sites, domains, OUs | Single machine only |

## How attackers abuse Group Policy

| Attack | Description |
|--------|-------------|
| **cPassword extraction** | GPP (Group Policy Preferences) stored passwords in XML files encrypted with a known AES key (since 2012: CVE-2014-2085). Any authenticated user can read them. |
| **SYSVOL enumeration** | Read all GPO files from SYSVOL to find scripts, configuration data, and sensitive information |
| **SharpGPOAbuse** | Add user to local admin group via GPO modification; create scheduled tasks; add startup scripts |
| **PyGPOAbuse** | Python version of SharpGPOAbuse to modify GPOs when the attacker has GPO write rights |
| **Permission delegation abuse** | Users with `Write` or `Modify` on a GPO can modify it to deploy malicious settings |
| **Group Policy Preferences (GPP) passwords** | Extract cached passwords from `Groups.xml`, `Services.xml`, `ScheduledTasks.xml`, etc. |
| **Malicious logon scripts** | Modify GPO logon scripts to deploy backdoors to all domain-joined computers |
| **Registry.pol manipulation** | Inject malicious registry settings via GPO (e.g., disable security features) |
| **Restricted Groups abuse** | Use `Restricted Groups` to add unauthorized users to `Domain Admins` or `Local Administrators` |
| **WMI filter tampering** | Modify WMI filters to extend or reduce GPO scope |
| **Security filtering bypass** | If a GPO has weak permissions on `Authenticated Users`, modify it through a different group |

### GPP cPassword vulnerability

Group Policy Preferences (GPP) allowed administrators to deploy passwords for local accounts, services, and scheduled tasks. The passwords were encrypted with a **static, known AES key**:

```python
# Decrypt GPP cPassword
from Crypto.Cipher import AES
import base64

key = (
    b"\x4e\x99\x06\xe8\xfc\xb6\x6c\xc9"
    b"\xfa\xf4\x93\x10\x62\x0f\xfe\xe8"
    b"\xf4\x96\xe8\x06\xcc\x05\x79\x90"
    b"\x20\x9b\x09\xa4\x33\xb6\x6c\x1b"
)

def decrypt_cpassword(encrypted_password):
    decoded = base64.b64decode(encrypted_password)
    cipher = AES.new(key, AES.MODE_CBC, b"\x00" * 16)
    decrypted = cipher.decrypt(decoded)
    return decrypted.rstrip(b"\x00").decode("utf-16-le")

# Usage
print(decrypt_cpassword("s5j8h3k5j8h3kj5h38kjh5kj38h5k3j5h3k5j38h5"))
```

**Tools:**
```bash
gpp-decrypt "s5j8h3k5j8h3kj5h38kjh5kj38h5k3j5h3k5j38h5"
```

## Defender recommendations

1. **Audit GPO modifications** — enable auditing on GPO objects:
   - Event ID 5136: Directory Service change (GPO modified)
   - Event ID 5137: Directory Service object created
   - Event ID 5141: Directory Service object deleted

2. **Restrict GPO modification** — only authorized administrators should have `Write` or `Modify` permissions on GPOs. Use AGPM (Advanced Group Policy Management) for change control.

3. **Remove all GPP passwords** — scan SYSVOL for XML files with `cPassword` and remove them. GPP passwords are no longer created by default (patched in MS14-025).

4. **Scan SYSVOL for sensitive data**:
   ```powershell
   Get-ChildItem -Recurse -Path "\\corp.com\SYSVOL\corp.com\Policies" |
       Select-String -Pattern "cPassword|password|secret" -SimpleMatch
   ```

5. **Review GPO permissions regularly** — use `Get-GPPermission` to audit who can edit GPOs.

6. **Use security filtering** — remove `Authenticated Users` from GPOs that should not apply to all users/computers.

7. **Limit who can link GPOs** — restrict `Link GPOs` permission to specific administrators.

8. **Enable GPO auditing via Advanced Audit Policy**:
   - `Audit Directory Service Changes` — Success
   - Monitor for GPO modification events

9. **Use slow-link detection** — prevent GPO application over slow links if the network path is untrusted.

10. **Validate GPO consistency** — periodically run `Get-GPOReport` and verify all GPOs match expected baselines.

11. **Monitor for SharpGPOAbuse** — detect when users are added to privileged groups via GPO (monitor local group membership changes).

## Relevant MS protocols and tools

| Document | Description |
|----------|-------------|
| [MS-GPOL] | Group Policy Protocol Specification |
| [MS-GPREF] | Group Policy Preference Protocol |
| [MS-GPREG] | Group Policy Registry Extension Protocol |
| [MS-GPSI] | Group Policy Security Extension Protocol |
| [MS-GPSCRIPT] | Group Policy Scripts Extension Protocol |
| [MS-GPC] | Group Policy Core Protocol |
| SharpGPOAbuse | .NET tool for GPO abuse |
| PyGPOAbuse | Python tool for GPO abuse |
| PowerView | PowerShell tool with GPO enumeration functions |
| Group Policy Management Console (GPMC) | Microsoft management tool |
