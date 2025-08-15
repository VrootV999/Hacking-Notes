# SharpHound

**Type:** Active Directory Enumeration, Privilege Escalation
**Focus:** **SharpHound** is a **privilege escalation** and **Active Directory enumeration** tool that's part of the **BloodHound** project. It is used to collect data from **Active Directory** environments and map out potential **attack paths** for **lateral movement** and **privilege escalation**. The primary function of SharpHound is to gather information about **group memberships**, **permissions**, and **Access Control Lists (ACLs)** that could be leveraged by attackers to escalate privileges within the domain.

---

## 1. Full Feature Overview

* **Group Enumeration**: SharpHound identifies **group memberships**, including users that belong to high-privilege groups like **Domain Admins**, **Enterprise Admins**, and **Backup Operators**.
* **ACL Enumeration**: SharpHound enumerates **Access Control Lists (ACLs)**, identifying potential misconfigurations or permissions that attackers can exploit to escalate privileges or move laterally within a network.
* **Domain Trusts**: It also identifies **domain trusts** (if any) and potential privilege escalation paths across different domains in the Active Directory environment.
* **Attack Path Visualization**: It helps BloodHound visualize paths from **low-privileged users** to high-value targets like **Domain Admins**, providing insight into how attackers might compromise critical accounts.
* **Efficient Data Collection**: SharpHound uses efficient scanning techniques, ensuring fast and comprehensive data collection even in large, complex **Active Directory environments**.

---

## 2. Requirements & Setup

### Requirements

* **Windows**: SharpHound is primarily designed for Windows environments, as it interfaces directly with Windows-based **Active Directory**.
* **.NET Framework**: SharpHound requires **.NET Framework 4.5+** to run on a Windows machine.
* **Administrative Privileges**: While SharpHound can be run with **low-privileged credentials**, higher privileges (such as **Domain Admin**) will yield more comprehensive results.
* **PowerShell/Command Prompt**: SharpHound can be run from either **PowerShell** or **Command Prompt**.

### Installation

1. **Clone the BloodHound repository**:

   ```bash
   git clone https://github.com/BloodHoundAD/BloodHound.git
   ```

2. **Navigate to the SharpHound directory**:

   ```bash
   cd BloodHound
   cd SharpHound
   ```

3. **Compile SharpHound (if necessary)**: SharpHound is written in **C#**, so you'll need to compile it with the provided **Visual Studio** project files. If you are on a **Windows** machine, you can build the **SharpHound** tool using **Visual Studio**.
   Alternatively, the **compiled SharpHound.exe** can be found in the **BloodHound** repository's releases section.

---

## 3. Core Usage

### 3.1 Running SharpHound for Basic Enumeration

You can run SharpHound to perform a simple enumeration of the Active Directory environment.

```bash
SharpHound.exe -c All -ip <target_ip> -domain <domain_name> - ou <target_ou>
```

Where:

* **`-c All`**: Collects all categories, including **group memberships**, **ACLs**, **permissions**, and **domain trusts**.
* **`-ip`**: The **IP address** of the target **Domain Controller**.
* **`-domain`**: The **domain** of the target **Active Directory** environment.
* **`-ou`**: The **organizational unit** to target (optional).

This will collect data about the **Active Directory** groups and permissions across the domain.

### 3.2 Running SharpHound with Specific Collection Flags

You can customize your collection by targeting specific types of information. Below are some of the flags you can use:

* **Group Enumeration**: To collect only **group membership** information.

  ```bash
  SharpHound.exe -c Group -ip <target_ip> -domain <domain_name>
  ```
* **ACL Enumeration**: To collect **Access Control Lists (ACLs)** only.

  ```bash
  SharpHound.exe -c ACL -ip <target_ip> -domain <domain_name>
  ```
* **Domain Trusts**: To collect information on **domain trusts** between domains.

  ```bash
  SharpHound.exe -c Trusts -ip <target_ip> -domain <domain_name>
  ```
* **Admin Enumeration**: To identify **admin group memberships**.

  ```bash
  SharpHound.exe -c Admins -ip <target_ip> -domain <domain_name>
  ```

### 3.3 Save Results to a File

SharpHound allows you to save its output to a **JSON file** for later analysis or import into **BloodHound**'s graphical interface.

```bash
SharpHound.exe -c All -ip <target_ip> -domain <domain_name> -ou <target_ou> -json <output_file.json>
```

Where:

* **`-json`**: Specifies the output file where the data will be saved.

This file can be imported into **BloodHound** for visualization of **attack paths** and **privilege escalation** opportunities.

### 3.4 Running SharpHound in Background (Stealth Mode)

To avoid detection by defenders, you may want to run SharpHound in a way that doesn't trigger alerts.

```bash
SharpHound.exe -c All -ip <target_ip> -domain <domain_name> -quiet -delay 1000
```

Where:

* **`-quiet`**: Suppresses most of SharpHound's output to make the tool run quietly.
* **`-delay 1000`**: Adds a delay between enumeration queries to avoid triggering **IDS/IPS** alerts.

---

## 4. Tips, Tricks, Best Practices

* **Use BloodHound for Visualization**: Once you have collected the data with SharpHound, import the data into **BloodHound** to visualize **attack paths** and identify potential privilege escalation opportunities.
* **Target Specific OUs**: When running SharpHound, focus on targeting specific **Organizational Units (OUs)** if you are conducting a targeted assessment.
* **Leverage Elevated Privileges**: If possible, run SharpHound with **domain admin** or elevated credentials for more comprehensive data collection. Higher-level access will help reveal **privileged accounts**, **sensitive groups**, and **domain trusts**.
* **Adjust for Stealth**: Use the **`-quiet`** and **`-delay`** flags when running SharpHound in sensitive environments to avoid detection by defenders.
* **Perform Regular Scans**: Schedule regular scans with SharpHound to monitor for new **privilege escalation paths** or any **misconfigurations** that may appear over time.

---

## 5. Cheat Sheet

```bash
# Basic collection with all categories
SharpHound.exe -c All -ip <target_ip> -domain <domain_name>

# Collect specific group enumeration data
SharpHound.exe -c Group -ip <target_ip> -domain <domain_name>

# Collect ACL information only
SharpHound.exe -c ACL -ip <target_ip> -domain <domain_name>

# Collect domain trust information
SharpHound.exe -c Trusts -ip <target_ip> -domain <domain_name>

# Save the output in JSON format for later import into BloodHound
SharpHound.exe -c All -ip <target_ip> -domain <domain_name> -json <output_file.json>

# Run in quiet mode with delays for stealth
SharpHound.exe -c All -ip <target_ip> -domain <domain_name> -quiet -delay 1000
```

---

