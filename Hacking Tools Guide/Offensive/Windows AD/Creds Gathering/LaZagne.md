# LaZagne

**Type:** Credential Dumping & Recovery Tool
**Focus:** **LaZagne** is an open-source tool used for **password extraction** from various applications on Windows, Linux, and macOS systems. It is designed to dump stored credentials from applications like **browsers**, **email clients**, **messengers**, **FTP clients**, and more. It supports multiple platforms and can be useful in post-exploitation to gain access to stored passwords for further exploitation.

---

## 1. Full Feature Overview

* **Cross-Platform Support**: LaZagne works on **Windows**, **Linux**, and **macOS**.
* **Multi-Application Support**: It extracts passwords from numerous applications, including browsers (Chrome, Firefox, Edge), email clients (Thunderbird, Outlook), and password managers.
* **Multiple Storage Locations**: It can extract passwords from various types of storage, such as **Windows Credential Manager**, **keychain databases**, and **SQL databases**.
* **No Installation Required**: The tool can be used directly without installation, which makes it easy to use in a live attack scenario.
* **Open-Source**: Free to use, and the source code is available for modifications and customization.

---

## 2. Requirements & Setup

### Requirements

* **Python**: LaZagne is written in Python and requires **Python 2.7 or Python 3.x** for execution.
* **Platform Compatibility**: It works across multiple platforms, including Windows, Linux, and macOS.

### Installation

1. **Clone LaZagne from GitHub**:

   ```bash
   git clone https://github.com/AlessandroZ/LaZagne.git
   cd LaZagne
   ```

2. **Install Dependencies**:

   LaZagne has a few dependencies that you can install using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

3. **For Windows Users**:

   For Windows, you may need to install **Python 2.7** or **Python 3.x** to run the tool.

---

## 3. Core Usage

### 3.1 Basic Syntax

The basic syntax to run **LaZagne** is:

```bash
python3 laZagne.py <module_name>
```

* **module\_name**: This is the specific module for which you want to extract credentials. It could be `browsers`, `messengers`, `wifi`, etc.

### 3.2 Available Modules

1. **Browsers**: Dump credentials stored in browsers (Chrome, Firefox, Edge).

   ```bash
   python3 laZagne.py browsers
   ```

2. **Messengers**: Extract credentials from instant messaging apps (Skype, Telegram, etc.).

   ```bash
   python3 laZagne.py messengers
   ```

3. **WiFi Passwords**: Extract WiFi passwords stored in the system.

   ```bash
   python3 laZagne.py wifi
   ```

4. **FTP Clients**: Extract FTP client credentials (e.g., FileZilla).

   ```bash
   python3 laZagne.py ftp
   ```

5. **Email Clients**: Dump credentials from email clients like Thunderbird, Outlook, etc.

   ```bash
   python3 laZagne.py email
   ```

6. **Windows Credentials**: Extract **Windows** credentials stored in the **Windows Credential Manager**.

   ```bash
   python3 laZagne.py wincred
   ```

7. **Others**: There are other modules for extracting credentials from various applications, including password managers, RDP clients, and more.

---

### 3.3 Full Credential Dump

To dump all supported credentials in one go:

```bash
python3 laZagne.py all
```

This will extract passwords from **browsers**, **messengers**, **email clients**, **FTP clients**, and more.

---

## 4. Tips, Tricks, Best Practices

* **Run with Elevated Privileges**: Some applications store credentials that are only accessible by **administrative users**. Running LaZagne as **Administrator** or with **root** privileges may yield more results.
* **Network Traffic Monitoring**: If using LaZagne for post-exploitation, monitor network traffic to detect any **reverse shells** or unusual traffic patterns that might indicate the tool’s activities.
* **Use for Lateral Movement**: Once you have dumped credentials from one machine, you can reuse them for lateral movement, targeting other machines on the network.
* **Extract WiFi Credentials**: In many environments, WiFi passwords are stored in the system. Extracting these passwords can be useful for bypassing network restrictions or further infiltration.
* **Automation**: You can automate LaZagne to run as part of a larger post-exploitation script to dump credentials across many machines or servers.

---

## 5. Cheat Sheet

```bash
# Dump credentials from browsers
python3 laZagne.py browsers

# Extract passwords from messaging apps
python3 laZagne.py messengers

# Dump WiFi passwords from the target system
python3 laZagne.py wifi

# Extract FTP client credentials
python3 laZagne.py ftp

# Extract email client credentials (e.g., Outlook, Thunderbird)
python3 laZagne.py email

# Dump Windows credentials from Windows Credential Manager
python3 laZagne.py wincred

# Dump all supported credentials in one go
python3 laZagne.py all
```

---
