# CrackMapExec

**Type:** Post-Exploitation, Network Enumeration, Lateral Movement
**Focus:** **CrackMapExec** (CME) is a **post-exploitation** tool and **network enumeration** tool that facilitates **lateral movement** and **credential validation** across a network of **Windows machines**. It automates common exploitation tasks in **Active Directory** environments, making it useful for **penetration testers**, **red teams**, and **attackers** to interact with and **exploit Windows networks**.

---

## 1. Full Feature Overview

* **Credential Validation**: CrackMapExec allows you to test **credentials** across multiple hosts, helping verify valid accounts.
* **Remote Command Execution**: Execute commands and scripts on remote systems without needing an active shell.
* **Network Enumeration**: List all available **shares**, **users**, and **services** running on machines.
* **Kerberos Support**: CME can perform **Kerberos-based attacks**, including **kerberos ticket extraction** and **pass-the-ticket**.
* **SMB & WinRM**: Supports multiple protocols for communication and command execution, including **SMB**, **WinRM**, **RDP**, and **SSH**.
* **Lateral Movement**: Facilitates moving laterally across a network using **valid credentials**, **SMB** shares, and other **exploitation techniques**.
* **Active Directory Enumeration**: Allows for detailed **AD enumeration**, including group memberships, **domain enumeration**, and **service account discovery**.

---

## 2. Requirements & Setup

### Requirements

* **Windows or Linux OS**: CrackMapExec runs on both **Linux** (via Python) and **Windows** (as an executable).
* **Python 3.x**: CME is a **Python-based** tool, so ensure **Python 3** is installed.
* **SMB/WinRM Access**: Requires access to **SMB shares** or **WinRM** services on target systems, typically with **admin privileges**.
* **Valid Credentials**: CME requires **valid credentials** (username/password or hashes) for authenticated operations.

### Installation

1. **Clone the CME repository**:

   ```bash
   git clone https://github.com/byt3bl33d3r/CrackMapExec.git
   cd CrackMapExec
   ```

2. **Install dependencies**:

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run CrackMapExec**:

   ```bash
   python3 crackmapexec.py
   ```

Alternatively, you can use **pre-compiled binaries** available for Windows from the official GitHub release page.

---

## 3. Core Usage

### 3.1 Basic Command Syntax

```bash
# General Command Format
crackmapexec [protocol] [target] [options]
```

Where:

* **\[protocol]**: The protocol to use (e.g., **smb**, **winrm**, **rdp**).
* **\[target]**: The target system(s), which can be an **IP address**, **IP range**, or **CIDR block**.
* **\[options]**: Specific commands or actions you want to perform.

### 3.2 SMB Enumeration

```bash
# Enumerate SMB shares across a range of IPs
crackmapexec smb 192.168.1.0/24 -u <username> -p <password> --shares
```

* **`--shares`**: Lists the available SMB shares on each machine.
* **`-u`**: Username to authenticate with.
* **`-p`**: Password or NTLM hash.

### 3.3 SMB Command Execution

```bash
# Execute a command remotely via SMB
crackmapexec smb 192.168.1.0/24 -u <username> -p <password> --exec-method smbexec "ipconfig"
```

* **`--exec-method smbexec`**: Specifies the method of command execution. `smbexec` allows you to run commands over SMB without needing a full remote shell.

### 3.4 SMB Credential Validation

```bash
# Validate credentials across a network range using SMB
crackmapexec smb 192.168.1.0/24 -u <username> -p <password> --test-password
```

* **`--test-password`**: Validates the given credentials against the target systems to see if the password is correct.

### 3.5 Lateral Movement (Remote Command Execution)

```bash
# Use SMB to run a command remotely on a target system
crackmapexec smb 192.168.1.10 -u <username> -p <password> --exec-method smbexec "net user hacker /add"
```

* This command adds a new **user** named `hacker` on the target machine.

### 3.6 WinRM Enumeration and Command Execution

```bash
# Execute a command using WinRM on a remote host
crackmapexec winrm 192.168.1.10 -u <username> -p <password> --exec "hostname"
```

* **WinRM** is used for **remote management** and can be more efficient in environments where SMB may be blocked.

### 3.7 Kerberos Ticket Extraction & Pass-the-Ticket

```bash
# Extract a TGT (Ticket Granting Ticket) with valid Kerberos credentials
crackmapexec smb 192.168.1.10 -u <username> -p <password> --kerberos
```

* This command will allow you to **extract Kerberos tickets** for further attacks like **Pass-the-Ticket** or **Golden Ticket** attacks.

---

## 4. Tips, Tricks, Best Practices

* **Credential Management**: Always use **strong credentials** and consider using **NTLM hashes** (if available) for authentication to avoid brute-forcing passwords.
* **WinRM Over SMB**: If **SMB** ports (445) are closed, try **WinRM** (ports 5985/5986) for remote execution.
* **Automate Scanning**: Use **CrackMapExec** as part of an **automated penetration test** to quickly identify **open shares**, **admin access**, and **other vulnerabilities** across a range of systems.
* **Escalate Privileges**: Use CME to identify **local administrators**, **high-privilege users**, or **group memberships** that might help you escalate to **domain administrator**.
* **Network Pivoting**: Combine CME with tools like **Chisel** or **socat** for **network tunneling** and **pivoting** to move from one machine to another within a compromised network.
* **Timing and Rate-Limiting**: Be aware of the **rate-limiting** and **firewall protection** on target networks. Use `-t` to limit requests and avoid detection.
* **Integration with BloodHound**: Export the results of CrackMapExec’s **AD enumeration** and integrate them with **BloodHound** to visualize attack paths and potential escalation paths.

---

## 5. Cheat Sheet

```bash
# Enumerate SMB shares across a network range
crackmapexec smb 192.168.1.0/24 -u <username> -p <password> --shares

# Execute a command on remote systems using SMB
crackmapexec smb 192.168.1.0/24 -u <username> -p <password> --exec-method smbexec "net user hacker /add"

# Validate credentials across a network range
crackmapexec smb 192.168.1.0/24 -u <username> -p <password> --test-password

# Use WinRM to execute a remote command
crackmapexec winrm 192.168.1.10 -u <username> -p <password> --exec "hostname"

# Perform a Kerberos-based attack and extract tickets
crackmapexec smb 192.168.1.10 -u <username> -p <password> --kerberos
```

---
