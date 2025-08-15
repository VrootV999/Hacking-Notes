# LSASecrets

**Type**: Post-Exploitation, Credential Dumping
**Focus**: **LSASecrets** is a tool that dumps the **Local Security Authority (LSA) secrets** on a Windows machine. It can be used to extract **password hashes**, **clear-text passwords**, **Kerberos keys**, and other sensitive information stored in the LSA secrets database.

---

## 1. Overview

* **Purpose**: LSASecrets can be used to dump sensitive information like **credentials** and **password hashes** that are stored within the **Windows LSA secrets store**. These secrets may include **service account credentials**, **stored passwords**, and **Kerberos keys**.
* **Key Features**:

  * Dump credentials stored in the LSA database.
  * Extract sensitive information used for post-exploitation.
  * **Kerberos** ticket information and **domain passwords**.

---

## 2. Usage

LSASecrets is usually used with tools like **Mimikatz** or **PowerShell** scripts for credential dumping.

**Mimikatz Example**:

```bash
mimikatz.exe "sekurlsa::lsa" "lsa::dump"
```

---

## 3. Best Practices

* **Utilize with privilege escalation**: You need **SYSTEM** privileges to access and dump LSA secrets.
* **Ensure data protection**: The information in LSA secrets can grant full access to domain systems if Kerberos keys or **clear-text passwords** are dumped.

---

