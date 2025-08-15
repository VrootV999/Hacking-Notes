


# SafetyKatz

**Type**: Post-Exploitation, Credential Dumping
**Focus**: **SafetyKatz** is a variant of **Mimikatz**. It is used for dumping credentials and Kerberos tickets from memory. SafetyKatz works similarly to Mimikatz but is often used in scenarios where **Mimikatz** is already detected.

---

## 1. Overview

* **Purpose**: SafetyKatz allows for **credential dumping**, **Kerberos ticket extraction**, and **credential reuse**. It can be used for **post-exploitation** activities to extract and manipulate credentials stored in **Windows memory**.
* **Key Features**:

  * Dumps **passwords** and **Kerberos tickets** from memory.
  * Can extract **clear-text passwords** and **hashed passwords**.
  * Supports **Pass-the-Ticket** and **Golden Ticket** attacks.

---

## 2. Usage

SafetyKatz has similar functionality to Mimikatz and can be used to extract credentials or **Kerberos tickets**.

Example of credential dumping with SafetyKatz:

```bash
SafetyKatz.exe sekurlsa::logonPasswords
```

This command dumps all passwords and authentication tokens from the local system memory.

---

## 3. Best Practices

* **Use SafetyKatz as a fallback** if **Mimikatz** is detected.
* Be aware that extracting sensitive credentials can be noisy and trigger endpoint protection systems.
