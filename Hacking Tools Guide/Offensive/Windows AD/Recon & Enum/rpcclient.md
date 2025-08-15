# rpcclient

**Type:** SMB Protocol, Windows Remote Management
**Focus:** **rpcclient** is a command-line tool for interacting with Windows **SMB (Server Message Block)** services. It is part of the **Impacket** library and can be used for **network enumeration**, **interacting with Windows services**, and **manipulating user accounts** or **shares** remotely. It supports a wide range of SMB operations, including **authentication**, **access control**, and **remote service interaction**.

---

## 1. Full Feature Overview

* **Authentication**: rpcclient can be used to authenticate with remote **Windows SMB services**, either using **username/password** or **NTLM hashes**.
* **Remote Enumeration**: Enumerates **user accounts**, **shares**, and **group memberships** within a Windows domain or workgroup.
* **Service Interaction**: Allows for controlling **remote services** on a Windows machine, including **starting** and **stopping** services.
* **SMB Security & Exploitation**: Can be used for **security auditing** by interacting with **shares**, **ACLs**, and **user rights** on the target system.
* **Password Cracking**: It allows querying Windows systems to identify **weak or null passwords**.
* **Named Pipe Interaction**: Interact with **named pipes**, allowing advanced exploitation of certain SMB services.

---

## 2. Requirements & Setup

### Requirements

* **SMB Access**: You need access to an **SMB** service running on a target Windows machine.
* **Valid Credentials**: You can authenticate using **username/password** or **NTLM hashes**.
* **Impacket Installation**: `rpcclient` is part of the **Impacket** suite, so you need to have it installed.

### Installation

1. **Install Impacket**:

   * First, clone the repository:

     ```bash
     git clone https://github.com/SecureAuthCorp/impacket.git
     cd impacket
     ```
   * Install Impacket with pip:

     ```bash
     pip3 install .
     ```

2. **Run rpcclient**:
   Once installed, `rpcclient` can be executed directly:

   ```bash
   python3 -m impacket.examples.rpcclient <target_ip>
   ```

---

## 3. Core Usage

### 3.1 Basic Command Syntax

```bash
rpcclient -U <username> -P <password> <target_ip>
```

Where:

* **`-U <username>`**: Specifies the **username** to authenticate with.
* **`-P <password>`**: Specifies the **password** for the user or the **NTLM hash**.
* **`<target_ip>`**: The IP address of the target system.

### 3.2 Listing Shares

```bash
rpcclient -U <username> -P <password> <target_ip> -c "netshareenum"
```

* **`netshareenum`**: Lists all **shared resources** (shares) on the target system.

### 3.3 Enumerating Users

```bash
rpcclient -U <username> -P <password> <target_ip> -c "enumdomusers"
```

* **`enumdomusers`**: Lists all the **domain users** in the target system's domain.

### 3.4 Enumerating Groups

```bash
rpcclient -U <username> -P <password> <target_ip> -c "enumdomgroups"
```

* **`enumdomgroups`**: Lists all the **groups** within the domain and their members.

### 3.5 Dumping User Information

```bash
rpcclient -U <username> -P <password> <target_ip> -c "queryuser <username>"
```

* **`queryuser <username>`**: Displays detailed information about the specified **user**, including account status, password last set, and more.

### 3.6 Creating a New User

```bash
rpcclient -U <username> -P <password> <target_ip> -c "createuser <new_username> <new_password>"
```

* **`createuser <new_username> <new_password>`**: Creates a new user account on the target machine.

### 3.7 Changing a User Password

```bash
rpcclient -U <username> -P <password> <target_ip> -c "setuserinfo <username> 23 <new_password>"
```

* **`setuserinfo <username> 23 <new_password>`**: Changes the password for the specified user. The `23` refers to the user info field for passwords.

### 3.8 Listing Services

```bash
rpcclient -U <username> -P <password> <target_ip> -c "srvinfo"
```

* **`srvinfo`**: Lists **service-related information** about the target system, including OS version and service pack.

### 3.9 Interacting with Named Pipes

```bash
rpcclient -U <username> -P <password> <target_ip> -c "pipe <pipe_name>"
```

* **`pipe <pipe_name>`**: Allows interaction with a named pipe on the target system, useful for **advanced exploitation**.

---

## 4. Tips, Tricks, Best Practices

* **Null Sessions**: If a system has weak SMB settings, you might be able to access information without providing any credentials. Use **anonymous access** if possible.
* **Enumerating Shares First**: Before attempting to execute commands or exploit a system, always start by listing the **available shares** to understand what is exposed on the target machine.
* **Use NTLM Hashes**: If you don’t have the cleartext password for an account, use the **NTLM hash** for authentication, which allows you to bypass the need for the password.
* **Monitor SMB Port (445)**: Make sure **SMB** (port 445) is open and available for interaction.
* **SMB Relay**: Use **rpcclient** in combination with **responder** or **Inveigh** to perform an **SMB relay** attack, capturing and relaying credentials.
* **Service Interaction**: Use `srvinfo` and `net share` commands to explore services and shared resources that might have weak access controls.

---

## 5. Cheat Sheet

```bash
# Basic rpcclient usage to connect to a target
rpcclient -U <username> -P <password> <target_ip>

# List shares available on a remote system
rpcclient -U <username> -P <password> <target_ip> -c "netshareenum"

# Enumerate domain users
rpcclient -U <username> -P <password> <target_ip> -c "enumdomusers"

# Enumerate domain groups
rpcclient -U <username> -P <password> <target_ip> -c "enumdomgroups"

# Query detailed information for a specific user
rpcclient -U <username> -P <password> <target_ip> -c "queryuser <username>"

# Create a new user account
rpcclient -U <username> -P <password> <target_ip> -c "createuser <new_username> <new_password>"

# Change the password of a user
rpcclient -U <username> -P <password> <target_ip> -c "setuserinfo <username> 23 <new_password>"

# List services running on the target system
rpcclient -U <username> -P <password> <target_ip> -c "srvinfo"

# Interact with a named pipe on the target system
rpcclient -U <username> -P <password> <target_ip> -c "pipe <pipe_name>"
```

--
