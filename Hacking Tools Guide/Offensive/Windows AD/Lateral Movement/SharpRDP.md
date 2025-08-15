# SharpRDP

**Type:** RDP Enumeration/Exploitation
**Focus:** **SharpRDP** is a tool that helps exploit and enumerate **Remote Desktop Protocol (RDP)** services on remote machines. It is designed to check for common misconfigurations, test **RDP access**, and help attackers interact with RDP services for post-exploitation purposes.

---

## 1. Full Feature Overview

* **RDP Brute Force**: Attempts to brute-force RDP credentials using common password lists.
* **RDP Session Enumeration**: Checks for active **RDP sessions** and active user sessions on the target machine.
* **RDP Connection Testing**: Attempts to establish an **RDP connection** to verify if the target is vulnerable or misconfigured.
* **Supports Credential Testing**: Allows testing of usernames and passwords against the RDP service.
* **Advanced Interaction**: Can be used to create persistent connections and interact with the RDP session in a post-exploitation scenario.

---

## 2. Requirements & Setup

### Requirements

* **Target System**: The target must have **RDP** (Remote Desktop Protocol) enabled, typically running on port **3389**.
* **Network Access**: You need network access to port **3389** on the target machine.
* **Credentials**: If you are brute-forcing or testing credentials, you will need to supply a list of **usernames** and **passwords**.
* **Windows Environment**: SharpRDP is built on **C#** and runs on **Windows**.

### Installation

1. **Clone the SharpRDP Repository**:

   First, clone the repository from **GitHub**:

   ```bash
   git clone https://github.com/EmpireProject/SharpRDP.git
   cd SharpRDP
   ```

2. **Build the Project**:

   SharpRDP requires **Visual Studio** to compile the code. Open the project in **Visual Studio** and build it.

   * Open the project file `SharpRDP.sln` in **Visual Studio**.
   * Build the solution to compile the executable.

3. **Download Precompiled Binaries**:

   You can also find precompiled binaries in the release section on **GitHub**. If you prefer not to compile from source, simply download the **SharpRDP.exe** binary.

   GitHub: [SharpRDP Releases](https://github.com/EmpireProject/SharpRDP/releases)

---

## 3. Core Usage

### 3.1 Brute-forcing RDP Credentials

To brute-force RDP credentials, use the **SharpRDP** tool to specify a list of potential usernames and passwords. The syntax for brute-forcing is:

```bash
SharpRDP.exe -ip <target_ip> -u <username_list> -p <password_list> -t <target_port>
```

**Example:**

```bash
SharpRDP.exe -ip 192.168.1.10 -u userlist.txt -p passlist.txt -t 3389
```

This command will attempt to brute-force RDP credentials on **192.168.1.10** using usernames from **userlist.txt** and passwords from **passlist.txt**.

### 3.2 Testing RDP Connection

If you simply want to check if RDP is open on a target, use the `-check` flag to test the connection:

```bash
SharpRDP.exe -ip 192.168.1.10 -check
```

This will check if RDP is enabled and accepting connections on port **3389**.

### 3.3 Enumerating RDP Sessions

To check for active RDP sessions on a target machine, use the `-enum` flag. This will enumerate all active **RDP sessions**:

```bash
SharpRDP.exe -ip 192.168.1.10 -enum
```

This will provide you with details about the active sessions, such as the username and the session ID.

### 3.4 Running SharpRDP in Interactive Mode

To use **SharpRDP** in an interactive way and attempt to exploit an RDP service with known credentials, you can use the `-interactive` flag:

```bash
SharpRDP.exe -ip 192.168.1.10 -u administrator -p password -interactive
```

This will attempt to connect to the RDP service on **192.168.1.10** using **administrator** as the username and **password** as the password. Once connected, you will interact with the RDP session.

---

## 4. Tips, Tricks, Best Practices

* **Use Strong Wordlists**: For brute-forcing, use large, diverse password lists and combine them with known usernames like "Administrator" or "User1."

  **Example**: Use **rockyou.txt** or **SecLists** for password lists.

* **Check for RDP Misconfigurations**: Before attempting brute-force, check if RDP is exposed without encryption or weakly configured (e.g., using `-check`).

* **Password Cracking**: If you have a **hash** of the RDP login credentials, use tools like **John the Ripper** or **Hashcat** to perform offline cracking before attempting brute-forcing.

* **RDP Bypass**: Some RDP configurations may have bypasses, such as **RDP login bypass** via **NLA (Network Level Authentication)** or **man-in-the-middle attacks**.

* **Use ProxyChains for Stealth**: If you want to hide your attack or bypass IP-based restrictions, use **ProxyChains** or VPNs to route traffic through anonymous networks.

---

## 5. Cheat Sheet

```bash
# Brute-force RDP credentials with username and password lists
SharpRDP.exe -ip <target_ip> -u <username_list> -p <password_list> -t 3389

# Test if RDP is open on the target
SharpRDP.exe -ip <target_ip> -check

# Enumerate active RDP sessions on the target
SharpRDP.exe -ip <target_ip> -enum

# Connect interactively to an RDP session
SharpRDP.exe -ip <target_ip> -u <username> -p <password> -interactive
```

---
