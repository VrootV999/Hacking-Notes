### WMIExec

**Type:** Remote Execution
**Focus:** **WMIExec** leverages **Windows Management Instrumentation (WMI)** to execute commands remotely on Windows machines. It's particularly useful in **post-exploitation** scenarios where the attacker is already inside the network and seeks to gain access to other machines.

---

## 1. Full Feature Overview

* **Remote Command Execution**: Execute arbitrary commands on remote systems without needing to install additional agents or software.
* **No SMB Required**: Unlike tools like **PsExec**, **WMIExec** does not require **SMB** to be open and instead relies on **WMI**, making it harder to detect.
* **Windows Management Instrumentation**: WMI is a management framework for Windows, and **WMIExec** uses this to interact with remote systems.
* **Authentication**: Supports both **NTLM** and **Kerberos** authentication.

---

## 2. Requirements & Setup

### Requirements

* **Target System**: A Windows system with **WMI** enabled.
* **Network Access**: The system executing WMIExec should have network access to the target, typically over **TCP 135** for WMI communication.

### Installation

Since **WMIExec** is part of the **Impacket** suite, you need to install Impacket.

1. **Install Impacket**:

   ```bash
   pip install impacket
   ```

2. **Verify Installation**:

   ```bash
   wmiexec.py -h
   ```

---

## 3. Core Usage

### 3.1 Basic Syntax

To execute a command on a remote Windows system using **WMIExec**, use the following syntax:

```bash
wmiexec.py <domain>/<username>:<password>@<target> "<command>"
```

**Example:**

```bash
wmiexec.py WORKGROUP/Administrator:password@192.168.1.10 "ipconfig"
```

This will execute the **`ipconfig`** command on the remote system at **192.168.1.10** using the credentials of the **Administrator** account.

### 3.2 Run Powershell Commands

You can also run PowerShell scripts remotely.

**Example:**

```bash
wmiexec.py WORKGROUP/Administrator:password@192.168.1.10 "powershell -Command Get-Process"
```

This will execute the **`Get-Process`** PowerShell cmdlet on the remote machine.

### 3.3 Custom Commands

You can run custom commands or scripts on the remote system.

**Example:**

```bash
wmiexec.py WORKGROUP/Administrator:password@192.168.1.10 "cmd.exe /c echo Hello World > C:\Temp\test.txt"
```

This runs a **CMD** command on the remote system that writes `Hello World` into a text file at **C:\Temp\test.txt**.

---

## 4. Tips, Tricks, Best Practices

* **Persistence**: You can use **WMIExec** to create persistent **backdoors** by scheduling tasks on the target system that trigger commands at specific intervals.
* **Bypassing Antivirus**: WMIExec’s use of **WMI** for remote execution can bypass some antivirus solutions that focus on SMB-based tools like **PsExec**.
* **Firewall Evasion**: Since **WMIExec** does not require **SMB**, it's effective in environments with **SMB blocking** or **strict firewall rules**.
* **Credential Caching**: Use **Windows credentials** from **Kerberos** tickets or **cached NTLM credentials** for remote authentication.

---

## 5. Cheat Sheet

```bash
# Execute command on a remote system
wmiexec.py DOMAIN/username:password@remote_host "command"

# Execute PowerShell command remotely
wmiexec.py DOMAIN/username:password@remote_host "powershell -Command 'Get-Process'"

# Execute remote command with output redirection
wmiexec.py DOMAIN/username:password@remote_host "cmd.exe /c echo 'Hello' > C:\Temp\file.txt"

# Run as a different user
wmiexec.py DOMAIN/username:password@remote_host -u "target_user" "command"
```

---
