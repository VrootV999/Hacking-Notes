# ADRecon

**Type:** Active Directory Enumeration, Post-Exploitation
**Focus:** **ADRecon** is a powerful Active Directory enumeration tool used for **discovering** and **mapping** Active Directory environments. It provides detailed insights into **AD configurations**, **user/group memberships**, **domain trusts**, and other critical information for **lateral movement** and **privilege escalation**. It automates the process of gathering useful data from a domain for **penetration testers**, **red teamers**, and **attackers** to exploit weaknesses in the Active Directory environment.

---

## 1. Full Feature Overview

* **User Enumeration**: Identifies **user accounts**, including **administrator** and **service accounts**, which may be useful for **lateral movement** or **privilege escalation**.
* **Group Enumeration**: Lists all **AD groups**, including **privileged groups** such as **Domain Admins**, **Enterprise Admins**, and others.
* **Domain Trusts**: Discover **trusted domains** and relationships, which may allow further attacks into other domains or systems.
* **Service Account Discovery**: Identify **service accounts** and associated **SPNs** (Service Principal Names) that can be targeted for **Kerberos** exploitation.
* **Active Directory Details**: Enumerates **Domain Controllers**, **OS version**, **domain policies**, and **user/group memberships**.
* **Detailed Export**: It can export the collected data in **JSON** or **CSV** format for further analysis and reporting.

---

## 2. Requirements & Setup

### Requirements

* **Windows/Linux**: **ADRecon** can be used on both **Windows** and **Linux** systems.
* **Valid Domain Credentials**: The tool requires a valid set of credentials (username/password or NTLM hashes) for interaction with the target Active Directory environment.
* **Impacket**: **ADRecon** relies on **Impacket** (for **SMB** and **LDAP** interactions) for some of its functionality.

### Installation

1. **Clone the ADRecon Repository:**

   ```bash
   git clone https://github.com/samratashok/ADRecon.git
   cd ADRecon
   ```

2. **Install Dependencies**:

   * Install **Python3** and necessary dependencies:

     ```bash
     pip3 install -r requirements.txt
     ```

3. **Run ADRecon**:

   * Use the following command to start the tool:

     ```bash
     python3 ADRecon.py -d <domain_name> -u <username> -p <password>
     ```

---

## 3. Core Usage

### 3.1 Basic Command Syntax

```bash
ADRecon.py -d <domain_name> -u <username> -p <password> [options]
```

Where:

* **`-d <domain_name>`**: The name of the target domain to enumerate.
* **`-u <username>`**: The username for **domain authentication**.
* **`-p <password>`**: The password for **domain authentication** or an **NTLM hash**.

### 3.2 Domain Information Enumeration

```bash
# Enumerate detailed domain information including DCs, trusts, etc.
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --domain-info
```

* **`--domain-info`**: Provides basic information about the domain such as **Domain Controllers (DC)**, **Trusts**, **Domain SID**, and **Domain policies**.

### 3.3 Enumerating Domain Users

```bash
# Enumerate all domain users
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --users
```

* **`--users`**: Lists all **domain users** with additional details such as **last logon**, **account status**, and **group memberships**.

### 3.4 Enumerating Domain Groups

```bash
# Enumerate all domain groups
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --groups
```

* **`--groups`**: Lists all **domain groups** and associated members.

### 3.5 Service Account and SPN Enumeration

```bash
# Enumerate service accounts and SPNs
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --spn
```

* **`--spn`**: Identifies **service accounts** and associated **SPNs** that may be leveraged for **Kerberos** attacks like **Pass-the-Ticket** or **Kerberos Ticket Granting Ticket (TGT)** extraction.

### 3.6 Group Membership Enumeration

```bash
# Enumerate group memberships (e.g., Domain Admins, Enterprise Admins)
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --group-memberships
```

* **`--group-memberships`**: Displays **group memberships** for specific users and identifies if a user is a member of **privileged groups** like **Domain Admins** or **Enterprise Admins**.

### 3.7 Exporting Results

```bash
# Export results to CSV or JSON for further analysis
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --output <output_path> --format csv
```

* **`--output <output_path>`**: Specifies the file path to export results.
* **`--format csv`**: Options for exporting results in **CSV** format (you can also use **JSON**).

---

## 4. Tips, Tricks, Best Practices

* **Automate Active Directory Auditing**: Run **ADRecon** regularly to identify changes within the **Active Directory** structure. This can help you spot **new users**, **groups**, or **service accounts** added to the environment.
* **Escalate Privileges**: Look for **service accounts** with elevated privileges, especially those that have **SPNs** configured. These accounts can often be exploited for **Kerberos**-related attacks.
* **Cross-Domain Attacks**: If there are **domain trusts**, you can use **ADRecon** to map out cross-domain relationships and pivot to other domains or environments.
* **Use of Hashes**: If you don’t have access to cleartext passwords, use **NTLM hashes** to authenticate with **ADRecon**.
* **Search for Weak Accounts**: Focus on accounts with **weak passwords**, **expired accounts**, or those with **inactive user status**. These can be entry points for further exploitation.
* **Export for Reporting**: Use the **export feature** to generate detailed reports in **CSV** or **JSON** format that can be integrated with other tools or used for post-exploitation analysis.

---

## 5. Cheat Sheet

```bash
# Basic Domain Information
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --domain-info

# Enumerate all domain users
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --users

# Enumerate all domain groups
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --groups

# Enumerate service accounts and SPNs
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --spn

# Enumerate group memberships of users
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --group-memberships

# Export results to CSV format
python3 ADRecon.py -d <domain_name> -u <username> -p <password> --output /path/to/report.csv --format csv
```

---
