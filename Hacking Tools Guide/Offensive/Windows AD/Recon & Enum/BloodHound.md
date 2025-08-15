# BloodHound

**Type:** Enumeration, Active Directory, Privilege Escalation
**Focus:** **BloodHound** is an **Active Directory (AD)** enumeration tool used for **mapping out attack paths** within a domain. It helps identify **privileged users** and **lateral movement paths** for attackers. BloodHound is crucial for **Red Team** operations and **post-exploitation** phases, allowing testers to identify and exploit **misconfigurations** within Active Directory to escalate privileges and gain access to sensitive resources.

---

## 1. Full Feature Overview

* **Domain Enumeration**: BloodHound performs in-depth enumeration of **Active Directory (AD)** environments, including **users**, **groups**, and **permissions**.
* **Privilege Escalation**: The tool maps out possible **attack paths** from low-privileged accounts to high-privileged ones, such as **Domain Admins** or **Enterprise Admins**.
* **Group Memberships**: BloodHound can identify users who are members of sensitive groups (e.g., **Domain Admins**, **Enterprise Admins**, **Backup Operators**).
* **ACL Enumeration**: It can enumerate **Access Control Lists (ACLs)** for domain objects, identifying misconfigurations or opportunities for privilege escalation.
* **Attack Path Visualization**: BloodHound provides a **graphical interface** that visualizes potential **attack paths** based on **permissions**, helping **red teamers** identify the shortest path to privilege escalation.

---

## 2. Requirements & Setup

### Requirements

* **Active Directory Environment**: BloodHound is designed for use in environments running **Active Directory (AD)**.
* **Administrator or Domain User Access**: The tool requires **low-level credentials** (e.g., domain user access) to perform basic enumeration, but it can leverage higher privileges for more advanced functions.
* **Linux (for BloodHound) and Windows**: BloodHound can run on both **Linux** and **Windows** systems.

### Installation

1. **Install BloodHound on Kali Linux (or similar)**

   ```bash
   sudo apt install bloodhound
   ```

2. **Install BloodHound on Windows (using Windows Subsystem for Linux or native install)**:

   ```bash
   # Install prerequisites
   sudo apt install nodejs npm
   sudo npm install -g bloodhound
   ```

3. **Running BloodHound**:

   * Once installed, you can start the BloodHound interface by running:

     ```bash
     bloodhound
     ```

4. **Neo4j Setup**:
   BloodHound uses **Neo4j** as its database to store **Active Directory** enumeration data. You need to install **Neo4j** and configure it for use with BloodHound.

   ```bash
   sudo apt install neo4j
   sudo service neo4j start
   ```

5. **Database Setup**:

   * BloodHound will connect to a **Neo4j** instance to store its data.
   * The default username for **Neo4j** is **neo4j**, and the password is **neo4j** (you should change this after the initial setup).

---

## 3. Core Usage

### 3.1 BloodHound Interface

Once **BloodHound** is installed and running, you can interact with the graphical interface or use the **BloodHound** API. Here’s a breakdown of the core functionality in the **interface**:

1. **Importing Data**: You will typically use **SharpHound** (part of the BloodHound toolkit) to collect data from the target Active Directory environment. This data is then imported into the **Neo4j** database for analysis.

2. **Graph View**: The interface visualizes **Active Directory** objects, such as **users**, **groups**, and **domains**. It shows potential **attack paths** for **privilege escalation**.

3. **Attack Path Analysis**: BloodHound identifies the shortest path from a **low-privileged user** to **Domain Admin** (or other high-value targets). This analysis helps identify which users, groups, and permissions could be exploited for **lateral movement**.

### 3.2 Running SharpHound (BloodHound Data Collector)

The **SharpHound** tool is used to collect enumeration data for **BloodHound**. SharpHound will collect information about **group memberships**, **permissions**, and **ACLs**.

```bash
SharpHound.exe -c All -ip <target_ip> -domain <target_domain>
```

Where:

* **`-c All`**: This collects data for all categories, including **groups**, **user memberships**, **ACLs**, and **permissions**.
* **`-ip`**: Specifies the target IP for the Active Directory environment.
* **`-domain`**: Specifies the target domain for enumeration.

You can also run **SharpHound** in specific modes (e.g., to collect only **group memberships** or **ACLs**) based on your needs.

### 3.3 BloodHound Data Import

Once SharpHound has completed the enumeration, you can import the data into **Neo4j**.

1. **Navigate to the Neo4j Web Interface**: Access **Neo4j** via the browser at `http://localhost:7474`.
2. **Login**: Default credentials are **username: neo4j**, **password: neo4j** (change this for production environments).
3. **Import Data**: In the BloodHound interface, import the **SharpHound** data, which is typically saved in a `.json` format.

### 3.4 Analyze Attack Paths

Once data is imported, BloodHound will display a **graph** that represents all users, groups, and permissions. It will show possible attack paths to escalate privileges.

1. **Search for Target Users**: You can search for high-value targets like **Domain Admins** or other privileged accounts.
2. **Analyze Graph**: The graph will show the **attack paths** between users and privileged accounts. Look for **low-hanging fruits** like users who have direct or indirect memberships in **privileged groups**.
3. **Privilege Escalation**: Identify paths where an attacker can escalate privileges using **misconfigurations** or **privileged group memberships**.

---

## 4. Tips, Tricks, Best Practices

* **Enumerate Privileged Groups**: Focus on finding **privileged users** and **groups** that are the **high-value targets** for lateral movement (e.g., **Domain Admins**, **Enterprise Admins**).
* **Investigate ACLs**: Misconfigured **Access Control Lists** can give unauthorized users access to critical resources. BloodHound will help identify such weaknesses.
* **Leverage Low Privileges**: BloodHound will identify **low-level users** that have paths to high-privileged accounts, helping attackers escalate privileges.
* **Use BloodHound in Red Team Engagements**: BloodHound is a great tool for simulating real-world attacks and mapping out potential attack paths that might be missed with traditional AD enumeration tools.
* **Automate Data Collection**: You can schedule regular scans with **SharpHound** to keep the **BloodHound** graph up-to-date for continual monitoring of the **Active Directory environment**.

---

## 5. Cheat Sheet

```bash
# Collect data using SharpHound
SharpHound.exe -c All -ip <target_ip> -domain <target_domain>

# Run BloodHound on a Kali Linux/Windows system
bloodhound

# Import SharpHound data into Neo4j
# Import through the BloodHound Web Interface: http://localhost:7474
```

---
