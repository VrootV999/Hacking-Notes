# PsExec

**Type:** Remote Execution
**Focus:** **PsExec** is one of the most well-known tools for executing commands on remote Windows machines. It is part of **Sysinternals Suite**, and it relies on **SMB** to facilitate command execution over the network. PsExec allows attackers to remotely execute commands, transfer files, and launch processes on remote systems.

---

## 1. Full Feature Overview

* **Remote Command Execution**: Run commands and scripts remotely on Windows systems.
* **File Transfer**: Copy files to and from the target system during or after execution.
* **Windows Services**: Launch processes as Windows services, allowing persistence or escalation of privileges.
* **No Installation Required**: PsExec doesn't require the installation of additional software on the target system.
* **SMB Protocol**: PsExec uses **SMB** (Server Message Block) to communicate with the target machine.
* **Authentication**: Supports **NTLM** and **Kerberos** authentication for remote execution.

---

## 2. Requirements & Setup

### Requirements

* **Target System**: A Windows machine with **SMB** ports open.
* **Network Access**: PsExec requires the ability to access the target machine over **TCP port 445** (SMB port).
* **Credentials**: You will need valid credentials for the target machine (username/password or SYSTEM privileges).

### Installation

1. **Download PsExec**:
   You can download the **PsExec** tool from the official Sysinternals page.

   * [Download PsExec](https://docs.microsoft.com/en-us/sysinternals/downloads/psexec)

2. **Verify PsExec**:
   After extracting, open a terminal and verify the installation by running:

   ```bash
   psexec -h
   ```

   This should display help information about PsExec's syntax and options.

---

## 3. Core Usage

### 3.1 Basic Syntax

To execute a command remotely using **PsExec**, the syntax is as follows:

```bash
psexec.exe \\<target> -u <username> -p <password> <command>
```

**Example:**

```bash
psexec.exe \\192.168.1.10 -u Administrator -p password ipconfig
```

This will execute **`ipconfig`** on the remote machine at **192.168.1.10** using the **Administrator** credentials.

### 3.2 Execute PowerShell Commands

You can also run **PowerShell** commands remotely using PsExec:

**Example:**

```bash
psexec.exe \\192.168.1.10 -u Administrator -p password powershell -Command "Get-Process"
```

This runs the **`Get-Process`** PowerShell cmdlet on the target machine.

### 3.3 Running Scripts and Commands in Background

PsExec allows you to run commands or scripts in the background on the target system.

**Example:**

```bash
psexec.exe \\192.168.1.10 -u Administrator -p password cmd /c "start notepad.exe"
```

This command will execute **notepad.exe** in the background on the remote system.

### 3.4 File Transfer

**PsExec** allows file transfers by using the `-c` flag, which automatically copies the executable to the target system before executing it.

**Example:**

```bash
psexec.exe \\192.168.1.10 -u Administrator -p password -c my_script.bat
```

This command will copy the **my\_script.bat** file to the target system's temporary directory and then execute it.

---

## 4. Tips, Tricks, Best Practices

* **Run as SYSTEM**: To run commands with **SYSTEM** privileges, use the `-s` flag to execute as a system service. This is often useful for gaining higher privileges.

  ```bash
  psexec.exe \\192.168.1.10 -s cmd
  ```

* **Evasion Techniques**: If **Windows Defender** or antivirus software is flagging PsExec, consider using **encoded payloads** or running the command over **SSH** or through **ProxyChains**.

* **Network Visibility**: PsExec’s reliance on **SMB** means it's detectable by network intrusion detection systems (IDS), but it’s widely used for lateral movement because of its simplicity.

* **Persistence**: You can use **PsExec** to install backdoors or persistence mechanisms, such as adding scheduled tasks or launching reverse shells that connect back to your listener.

* **Target Multiple Machines**: PsExec can be used to target multiple systems by specifying a range of IPs or hostnames.

  ```bash
  psexec.exe \\192.168.1.1,192.168.1.2,192.168.1.3 -u Administrator -p password ipconfig
  ```

---

## 5. Cheat Sheet

```bash
# Basic remote command execution
psexec.exe \\<target> -u <username> -p <password> <command>

# Execute PowerShell command remotely
psexec.exe \\<target> -u <username> -p <password> powershell -Command "<PowerShell Command>"

# Execute command as SYSTEM
psexec.exe \\<target> -u <username> -p <password> -s <command>

# Run a script on a remote system
psexec.exe \\<target> -u <username> -p <password> -c <script.bat>

# Run command on multiple systems
psexec.exe \\<target1>,<target2> -u <username> -p <password> <command>
```

---
