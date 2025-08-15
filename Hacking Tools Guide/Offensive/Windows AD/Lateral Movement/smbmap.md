# smbmap

**Type:** SMB Enumeration
**Focus:** **smbmap** is a powerful tool for enumerating **SMB shares** and assessing their access controls. It allows attackers to enumerate available shares, test access levels (read, write, execute), and check for potential vulnerabilities in file and directory permissions across a network.

---

## 1. Full Feature Overview

* **SMB Share Enumeration**: Enumerate available SMB shares on a network and check access levels.
* **Permissions Checking**: Test for **read**, **write**, and **execute** access on SMB shares.
* **Recursive Directory Enumeration**: Crawl through directories on remote systems and get details about files and directories.
* **Supports Multiple Target IPs**: Scan multiple machines at once for SMB shares, saving time on large networks.
* **Report Generation**: Generates a summary report of access permissions, which is useful for exploitation planning.

---

## 2. Requirements & Setup

### Requirements

* **Target System**: The target system should have SMB shares exposed and accessible over TCP port **445** (SMB port).
* **Network Access**: You need network access to the target SMB server.
* **Credentials**: **smbmap** supports anonymous access and also user/password combinations.

### Installation

1. **Install smbmap on Kali Linux**:

   ```bash
   sudo apt install smbmap
   ```

2. **Install smbmap on macOS** (via Homebrew):

   ```bash
   brew install smbmap
   ```

3. **Install smbmap from GitHub**:

   ```bash
   git clone https://github.com/shawncshepherd/smbmap.git
   cd smbmap
   python3 setup.py install
   ```

---

## 3. Core Usage

### 3.1 Basic Syntax

The basic syntax to start an **SMB share enumeration** using **smbmap** is:

```bash
smbmap -H <target_ip> -u <username> -p <password>
```

This will enumerate SMB shares on the target machine and show access rights.

**Example:**

```bash
smbmap -H 192.168.1.10 -u guest -p guest
```

This will enumerate the SMB shares on **192.168.1.10** using **guest** credentials.

### 3.2 Listing Shares and Permissions

To list the shares and their access permissions, use the `-R` option:

```bash
smbmap -H <target_ip> -u <username> -p <password> -R
```

**Example:**

```bash
smbmap -H 192.168.1.10 -u Administrator -p password -R
```

This command will list all shares and recursively check the permissions on each of them.

### 3.3 Testing Write Access

To check if you have **write** access to a specific share, use the `-A` option:

```bash
smbmap -H <target_ip> -u <username> -p <password> -A
```

This will test the **write** permissions of each share.

**Example:**

```bash
smbmap -H 192.168.1.10 -u Administrator -p password -A
```

### 3.4 Recursive Directory Scanning

To scan and list all files and directories under a share, use the `-r` option:

```bash
smbmap -H <target_ip> -u <username> -p <password> -r <share_name>
```

This will recursively enumerate the files within the specified share.

**Example:**

```bash
smbmap -H 192.168.1.10 -u Administrator -p password -r shared
```

### 3.5 Multiple Targets

You can use **smbmap** to scan multiple target machines by providing a list of IP addresses:

```bash
smbmap -H <target1>,<target2>,<target3> -u <username> -p <password>
```

**Example:**

```bash
smbmap -H 192.168.1.10,192.168.1.11 -u Administrator -p password
```

This command will enumerate SMB shares on **192.168.1.10** and **192.168.1.11**.

---

## 4. Tips, Tricks, Best Practices

* **Credential Reuse**: If you have multiple targets with similar configurations, you can reuse the same **username** and **password** across several IP addresses to speed up enumeration.

* **Brute-forcing SMB**: You can pair **smbmap** with tools like **Hydra** to brute-force SMB credentials and identify weak passwords on shares.

* **Network Scanning**: Before running **smbmap** on a range of machines, use **nmap** or **masscan** to identify active SMB hosts in the network.

* **Null Sessions**: If SMB shares allow **null sessions** (unauthenticated access), you can attempt to enumerate shares without credentials.

* **Access Checks**: **smbmap** can be used to quickly check if you have **write** or **execute** access to shares, allowing attackers to plan further post-exploitation actions.

---

## 5. Cheat Sheet

```bash
# Basic SMB enumeration
smbmap -H <target_ip> -u <username> -p <password>

# List all available shares and permissions
smbmap -H <target_ip> -u <username> -p <password> -R

# Check for write access to SMB shares
smbmap -H <target_ip> -u <username> -p <password> -A

# Recursively enumerate files in a share
smbmap -H <target_ip> -u <username> -p <password> -r <share_name>

# Scan multiple targets for SMB shares
smbmap -H <target1>,<target2> -u <username> -p <password>
```

---
