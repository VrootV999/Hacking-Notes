# Enum4linux

**Type:** Enumeration, SMB, Active Directory
**Focus:** **Enum4linux** is a **Linux-based** tool for gathering **information** from **Windows** machines via **SMB (Server Message Block)** protocol. It is primarily used for **Active Directory enumeration** in **penetration testing** and **red teaming**, offering a wide range of methods for **gathering information** about Windows networks, users, shares, and groups.

---

## 1. Full Feature Overview

* **User Enumeration**: Allows attackers to gather information about **user accounts**, including **active accounts**, **group memberships**, and **password policies**.
* **Group Enumeration**: Lists all available **user groups** on the domain and identifies which users are members of privileged groups such as **Domain Admins** and **Enterprise Admins**.
* **Share Enumeration**: Enumerates **shares** on the target machine, including hidden shares.
* **Password Policy**: Gathers the **password policy** of the domain, including lockout thresholds and password expiration settings.
* **OS Version**: Identifies the **operating system** and version of the target machine.
* **Machine Information**: Provides additional machine-specific details such as **hostname**, **IP address**, and **workgroup/domain**.
* **Net Session Information**: Retrieves information on current **network sessions**, including active SMB connections.

---

## 2. Requirements & Setup

### Requirements

* **Linux/Windows (via Cygwin)**: While **Enum4linux** is primarily designed for **Linux**, it can be used on **Windows** with **Cygwin**.
* **SMB Access**: You need access to the target machine's SMB service (either public or via credentials).
* **Python 3.x**: The tool is written in **Python**, so Python 3 is required to run it.

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/byt3bl33d3r/enum4linux.git
   cd enum4linux
   ```

2. **Run Enum4linux**:

   * **No installation** is necessary as the tool is a Python script. Simply run it with the following command:

     ```bash
     python3 enum4linux.py <target_ip>
     ```

---

## 3. Core Usage

### 3.1 Basic Command Syntax

```bash
python3 enum4linux.py -a <target_ip>
```

Where:

* **`-a`**: A shorthand for **all-encompassing** enumeration, which gathers **user information**, **shares**, **groups**, **password policies**, etc.
* **`<target_ip>`**: The IP address or **hostname** of the target machine.

### 3.2 User Enumeration

```bash
# Gather user enumeration information
python3 enum4linux.py -U <target_ip>
```

* **`-U`**: Lists all **user accounts** on the target system, including **disabled accounts**, **account status**, **user groups**, and **logon information**.

### 3.3 Group Enumeration

```bash
# Enumerate groups and their members
python3 enum4linux.py -G <target_ip>
```

* **`-G`**: Lists all **user groups** on the machine along with **group memberships**, identifying privileged groups like **Domain Admins**.

### 3.4 Share Enumeration

```bash
# List shared resources on the target machine
python3 enum4linux.py -S <target_ip>
```

* **`-S`**: Enumerates **file shares** on the target machine, including **hidden shares** (e.g., `IPC$`, `ADMIN$`, etc.).

### 3.5 Password Policy

```bash
# Retrieve the password policy of the target domain
python3 enum4linux.py -P <target_ip>
```

* **`-P`**: Enumerates the **password policy** (e.g., **password expiration**, **lockout settings**, and **minimum password length**).

### 3.6 OS and Machine Information

```bash
# Retrieve OS version and machine-specific information
python3 enum4linux.py -o <target_ip>
```

* **`-o`**: Retrieves the **OS version**, **hostname**, and **machine details** (such as **domain/workgroup name**).

### 3.7 Net Session Information

```bash
# Enumerate active SMB sessions on the target
python3 enum4linux.py -N <target_ip>
```

* **`-N`**: Retrieves **current SMB sessions**, showing active connections and the associated **usernames**.

---

## 4. Tips, Tricks, Best Practices

* **Combine with SMBclient**: After gathering **share information** with **Enum4linux**, use **SMBclient** to enumerate or interact with shared files for further enumeration or exploitation.
* **Use for Password Policy Checks**: Use **password policy** information to identify weak or misconfigured **password policies**, which could lead to further exploitation (e.g., weak passwords or long expiry times).
* **Find Misconfigured Shares**: Look for **misconfigured shares**, particularly those that are **wide open** (e.g., `Everyone` or `Domain Users` with **write access**). These can be used to further compromise the system.
* **Enumerate Group Memberships**: Focus on identifying **privileged groups** like **Domain Admins**. Target these accounts for **credential harvesting** or **lateral movement**.
* **Use Credentials for More Info**: If you have valid credentials, use them to gather more detailed information on the target system.

---

## 5. Cheat Sheet

```bash
# Basic enumeration of users, groups, shares, etc.
python3 enum4linux.py -a <target_ip>

# Enumerate user accounts
python3 enum4linux.py -U <target_ip>

# Enumerate group memberships
python3 enum4linux.py -G <target_ip>

# Enumerate shared resources (SMB shares)
python3 enum4linux.py -S <target_ip>

# Get the password policy of the target system
python3 enum4linux.py -P <target_ip>

# Retrieve OS version and machine details
python3 enum4linux.py -o <target_ip>

# Enumerate active SMB sessions
python3 enum4linux.py -N <target_ip>
```

---
