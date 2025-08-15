# smbclient

**Type:** File Sharing
**Focus:** **smbclient** is a command-line tool used for interacting with **SMB/CIFS** file shares. It allows users to access shared directories and files on remote machines, similar to how **ftp** works, but for **SMB**. It’s typically used in post-exploitation scenarios to enumerate or interact with SMB shares on Windows and Linux systems.

---

## 1. Full Feature Overview

* **SMB/CIFS File Sharing**: Access and interact with shared file systems over the network using the **SMB** protocol.
* **Remote File Manipulation**: Upload, download, and manipulate files on a remote server.
* **User Authentication**: Supports multiple forms of authentication, including **NTLM** and **Kerberos**.
* **Directory Enumeration**: Can list shares, files, and directories on a remote system.
* **Stealthy Access**: Works without needing a GUI, often evading detection better than traditional file explorers.

---

## 2. Requirements & Setup

### Requirements

* **Target System**: The target machine must have **SMB** enabled and file shares exposed.
* **Network Access**: **SMB** typically runs on **TCP ports 139** and **445**, so these ports must be open.
* **Credentials**: You’ll need valid credentials (username and password) to authenticate against the remote **SMB** share.

### Installation

1. **Linux (Debian/Ubuntu-based)**:

   ```bash
   sudo apt install smbclient
   ```

2. **Linux (RedHat/Fedora-based)**:

   ```bash
   sudo yum install samba-client
   ```

3. **Windows**: **smbclient** comes as part of the **Samba suite**, but if you're using Windows, you can use **PowerShell** or **Net Use** commands to access shares.

---

## 3. Core Usage

### 3.1 Basic Syntax

The basic syntax to connect to an SMB share using **smbclient** is:

```bash
smbclient //<target_ip>/<share_name> -U <username>
```

**Example:**

```bash
smbclient //192.168.1.10/shared -U user
```

This will prompt you for the password and give you access to the **`shared`** folder on the remote machine **192.168.1.10**.

### 3.2 File Operations

Once connected to a share, you can use commands to interact with files. Common commands include:

* **ls**: List files and directories in the current directory.

  ```bash
  smb: \> ls
  ```

* **get**: Download a file from the remote system.

  ```bash
  smb: \> get example.txt
  ```

* **put**: Upload a file to the remote system.

  ```bash
  smb: \> put myfile.txt
  ```

* **mget**: Download multiple files at once.

  ```bash
  smb: \> mget *.txt
  ```

* **mput**: Upload multiple files at once.

  ```bash
  smb: \> mput *.txt
  ```

### 3.3 Share Enumeration

You can list all available shares on a remote system with the **-L** option:

```bash
smbclient -L <target_ip> -U <username>
```

This will list all shared resources available on the target machine.

**Example:**

```bash
smbclient -L 192.168.1.10 -U guest
```

### 3.4 Remote Shell

You can execute commands on the remote system via the **smbclient** interactive shell. After connecting to the share, you’ll be in an SMB shell.

```bash
smb: \> dir
```

This will list files in the current directory on the remote share.

---

## 4. Tips, Tricks, Best Practices

* **SMB Version Detection**: You can detect the **SMB version** by trying to connect with different protocols (v1, v2, v3). Some systems may have **SMBv1** disabled, which could impact the effectiveness of **smbclient**.

  ```bash
  smbclient //192.168.1.10/shared -U user -m SMB2
  ```

* **Anonymous Access**: Some shares may be publicly accessible without authentication. You can try connecting anonymously:

  ```bash
  smbclient //192.168.1.10/shared -U guest
  ```

* **Password Cracking**: You can use **smbclient** as part of **brute-force attacks** on SMB shares with tools like **Hydra** or **Medusa** for credential cracking.

* **Using with Metasploit**: **smbclient** can be used in conjunction with **Metasploit**'s **smb** auxiliary modules for file sharing enumeration, access, and exploitation.

---

## 5. Cheat Sheet

```bash
# List available shares on a remote host
smbclient -L <target_ip> -U <username>

# Connect to a share with authentication
smbclient //<target_ip>/<share_name> -U <username>

# List files in the current share directory
smb: \> ls

# Download a file from the share
smb: \> get <filename>

# Upload a file to the share
smb: \> put <filename>

# Download multiple files
smb: \> mget *.txt

# Upload multiple files
smb: \> mput *.txt

# Execute commands remotely using the shell
smb: \> dir
```

---
