# DCOMExec

**Type:** Remote Execution
**Focus:** **DCOMExec** is a tool that leverages **Distributed Component Object Model (DCOM)** for executing commands remotely on Windows systems. **DCOM** is a Microsoft technology that allows applications to communicate with each other over a network, and **DCOMExec** uses this to execute commands remotely, similar to **WMIExec** but relying on **DCOM** instead.

---

## 1. Full Feature Overview

* **Remote Command Execution**: Execute commands on remote systems without needing additional agents or software.
* **No SMB Required**: Similar to **WMIExec**, **DCOMExec** does not rely on SMB for remote execution, making it useful for environments where SMB might be blocked or monitored.
* **Uses DCOM Protocol**: DCOMExec uses the **DCOM protocol** to interact with remote Windows machines and execute commands, providing a **stealthier** method for remote execution compared to other tools.
* **Authentication**: Supports **NTLM** and **Kerberos** authentication mechanisms.

---

## 2. Requirements & Setup

### Requirements

* **Target System**: The target must be a Windows machine with **DCOM** enabled.
* **Network Access**: The system executing **DCOMExec** must have network access to the target system over **DCOM’s default port (TCP 135)**.

### Installation

**DCOMExec** is part of the **Impacket** suite. To use it, you must first install Impacket.

1. **Install Impacket**:

   ```bash
   pip install impacket
   ```

2. **Verify Installation**:
   After installing Impacket, verify that **DCOMExec** is available by running:

   ```bash
   dcomexec.py -h
   ```

---

## 3. Core Usage

### 3.1 Basic Syntax

The basic syntax for executing commands on a remote machine using **DCOMExec** is:

```bash
dcomexec.py <domain>/<username>:<password>@<target> "<command>"
```

**Example:**

```bash
dcomexec.py WORKGROUP/Administrator:password@192.168.1.10 "ipconfig"
```

This command will execute **`ipconfig`** on the remote machine **192.168.1.10** using the **Administrator** credentials.

### 3.2 Execute PowerShell Commands

To execute PowerShell commands remotely, you can use the same syntax:

**Example:**

```bash
dcomexec.py WORKGROUP/Administrator:password@192.168.1.10 "powershell -Command Get-Process"
```

This will run the **`Get-Process`** PowerShell cmdlet on the remote machine.

### 3.3 Custom Commands

You can also run custom shell or PowerShell commands.

**Example:**

```bash
dcomexec.py WORKGROUP/Administrator:password@192.168.1.10 "cmd.exe /c echo Hello World > C:\Temp\test.txt"
```

This runs a **CMD** command that creates a text file at **C:\Temp\test.txt** with the content `Hello World`.

---

## 4. Tips, Tricks, Best Practices

* **Bypass SMB Restrictions**: **DCOMExec** is particularly useful when **SMB** ports are blocked or filtered in the environment.
* **Network Visibility**: **DCOMExec** traffic may be less visible on the network compared to **SMB-based tools** like **PsExec**, making it a stealthier option for remote execution.
* **Credential Caching**: Like other Impacket tools, you can use **Kerberos tickets** or **cached NTLM credentials** for authentication.
* **Persistence**: Use **DCOMExec** to create scheduled tasks or persist on remote systems by running scripts that will trigger at specific times.

---

## 5. Cheat Sheet

```bash
# Execute a command on a remote system using DCOMExec
dcomexec.py DOMAIN/username:password@remote_host "command"

# Execute PowerShell command remotely
dcomexec.py DOMAIN/username:password@remote_host "powershell -Command 'Get-Process'"

# Execute command with output redirection
dcomexec.py DOMAIN/username:password@remote_host "cmd.exe /c echo 'Hello' > C:\Temp\file.txt"
```

---
