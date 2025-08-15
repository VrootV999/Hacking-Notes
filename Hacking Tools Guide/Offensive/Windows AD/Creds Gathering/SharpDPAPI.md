# SharpDPAPI

**Type**: Post-Exploitation, Credential Dumping
**Focus**: **SharpDPAPI** is a **.NET** tool used for dumping credentials and secrets that are stored in **Windows Data Protection API (DPAPI)**. DPAPI is a system used by Windows for protecting sensitive information such as passwords, encryption keys, and other secrets. **SharpDPAPI** can decrypt and extract these secrets from **Windows machines**, often in post-exploitation scenarios.

---

## 1. Overview

* **Purpose**: SharpDPAPI allows attackers or penetration testers to extract sensitive data from Windows systems that are encrypted by the DPAPI mechanism.
* **Key Features**:

  * Decrypts DPAPI-encrypted secrets stored in the **Windows Credential Manager**, **Internet Explorer**, **Edge**, and other application-specific storage.
  * **Works for both user and machine DPAPI secrets**.
  * Requires **Local Administrator** or **SYSTEM** privileges to run.
  * Can also be used for **pass-the-hash** attacks if sensitive data (such as a password) is recovered.

---

## 2. Requirements & Setup

### Requirements

* **.NET Framework**: SharpDPAPI is a **.NET**-based tool, so you need to ensure that the target machine or your attack machine has the **.NET Framework** installed.
* **Privileged Access**: Requires **Administrator** or **SYSTEM** privileges to access DPAPI-protected data.
* **Windows OS**: SharpDPAPI works on **Windows** systems and extracts secrets that are encrypted using **DPAPI**.

### Installation

1. **Download or Clone the Repository**:

   You can download **SharpDPAPI** from the official **GitHub repository**:

   [SharpDPAPI GitHub](https://github.com/micahvandeusen/SharpDPAPI)

   Alternatively, clone the repository:

   ```bash
   git clone https://github.com/micahvandeusen/SharpDPAPI.git
   cd SharpDPAPI
   ```

2. **Build the Tool**:

   * Open **SharpDPAPI.sln** in **Visual Studio**.
   * Build the solution in **Release** mode.
   * The compiled executable (`SharpDPAPI.exe`) will be found in the `bin\Release` folder.

3. **Run SharpDPAPI**:

   The compiled tool can be executed directly from the command line on the target machine.

---

## 3. Core Usage

### 3.1 Dump DPAPI Secrets from Credential Manager

To dump **DPAPI secrets** stored in the **Windows Credential Manager**:

```bash
SharpDPAPI.exe /user:<target_user> /credman
```

* This command extracts **Credentials** encrypted by DPAPI and decrypts them if possible.
* **/user** specifies the target user profile for which secrets will be decrypted.

### 3.2 Dump DPAPI Secrets from Internet Explorer and Edge

To extract **DPAPI-encrypted secrets** from **Internet Explorer** and **Edge** (such as saved passwords):

```bash
SharpDPAPI.exe /user:<target_user> /ie
```

This command targets the **Internet Explorer** and **Edge** DPAPI storage locations.

### 3.3 Decrypting DPAPI Secrets from the Local Machine

If you need to dump secrets from the **machine-wide DPAPI** (secrets that are protected by the machine’s credentials, such as certain **machine-level credentials**), use the following:

```bash
SharpDPAPI.exe /machine
```

* This command targets the **machine-level secrets**, including those used by the operating system and certain applications.

### 3.4 Extracting the DPAPI Master Key

To extract the **DPAPI master key** used for decryption, use:

```bash
SharpDPAPI.exe /keydump
```

* This is a crucial step when **decrypting** machine or user-level **DPAPI secrets**, especially when you need to perform **offline decryption** or need to extract the master key.

---

## 4. Advanced Features & Techniques

### 4.1 Using SharpDPAPI to Extract Web Credentials

SharpDPAPI can be particularly useful for **exfiltrating saved web credentials** in **Internet Explorer** or **Edge**. For example:

```bash
SharpDPAPI.exe /user:<target_user> /ie /decrypt
```

* This extracts and decrypts passwords stored in web browsers, which are often encrypted using DPAPI.

### 4.2 Targeting Specific DPAPI Stores

SharpDPAPI can target specific locations for decrypting DPAPI-encrypted data. Use the `/target` flag for this:

```bash
SharpDPAPI.exe /target:Software\Microsoft\Windows\CurrentVersion\Internet Settings /user:<target_user>
```

This command will extract and decrypt specific keys or secrets stored under a specific registry or file path.

### 4.3 Using SharpDPAPI for Offline Attacks

If you have access to a **full disk image** or **Windows backup** of a target machine, you can run **SharpDPAPI** on the offline copy of the data to decrypt secrets without executing it live on the target machine. This is useful when the target machine is shut down, or you lack immediate access to it.

1. Mount the image or copy over files from the `\Users\<user>\AppData\Local\Microsoft\Credentials` directory (which contains DPAPI-protected secrets).
2. Run **SharpDPAPI** on the copied files.

---

## 5. Tips, Tricks, & Best Practices

* **Elevation**: To successfully dump DPAPI-protected data, ensure that you run SharpDPAPI with **elevated privileges** (e.g., **Administrator** or **SYSTEM**).
* **Persistence**: If you're extracting **machine-level secrets**, these may persist across user logins and could provide credentials that give you broader access.
* **Web Browsers**: Most **modern web browsers** store credentials encrypted using **DPAPI** on Windows systems, and SharpDPAPI is very effective at extracting them.
* **Offline Attacks**: Use **SharpDPAPI** for offline decryption in **forensics** or **data recovery scenarios**.
* **User-Specific Secrets**: Always make sure to specify the correct user profile when targeting **user-level DPAPI secrets** to ensure you're decrypting the correct data.
* **Use in Post-Exploitation**: SharpDPAPI is especially useful in post-exploitation scenarios to **extract sensitive credentials** that could lead to further lateral movement in a network.

---

## 6. Cheat Sheet

```bash
# Dump DPAPI secrets from Credential Manager
SharpDPAPI.exe /user:Administrator /credman

# Dump DPAPI secrets from Internet Explorer and Edge
SharpDPAPI.exe /user:Administrator /ie

# Dump machine-level DPAPI secrets
SharpDPAPI.exe /machine

# Extract the DPAPI master key
SharpDPAPI.exe /keydump

# Extract web credentials from Internet Explorer
SharpDPAPI.exe /user:Administrator /ie /decrypt

# Target specific DPAPI store
SharpDPAPI.exe /target:Software\Microsoft\Windows\CurrentVersion\Internet Settings /user:Administrator
```

---

## 7. Common Issues and Troubleshooting

* **"Access Denied" Errors**: If you see "Access Denied," make sure you're running **SharpDPAPI** with **administrator** or **SYSTEM** privileges.
* **Missing Secrets**: If no secrets are found, verify the correct profile is targeted and ensure the target account has DPAPI-protected data.
* **Corrupted Data**: In some cases, DPAPI-encrypted data may be corrupted, and decryption may not be possible. Always ensure you're using up-to-date tools and libraries.

---
