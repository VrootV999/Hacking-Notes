# ldapdomaindump

**Type:** Active Directory Enumeration
**Focus:** **ldapdomaindump** is a Python tool used for **enumerating Active Directory (AD)** environments by extracting critical information, such as **user accounts**, **group memberships**, **permissions**, and **organizational unit** (OU) data. It helps in gathering detailed **AD data** to facilitate further attacks in **post-exploitation** and **lateral movement** phases.

---

## 1. Full Feature Overview

* **ldapdomaindump** is designed for **enumerating Active Directory** and **LDAP** (Lightweight Directory Access Protocol) data from a compromised machine
* The tool focuses on gathering **group memberships**, **user information**, **permissions**, **domain trusts**, and other critical **AD objects**
* Information gathered can be used for **privilege escalation**, **lateral movement**, and **finding attack paths** in a Windows-based network environment
* **ldapdomaindump** can extract data from both **on-premise** and **cloud-based** Active Directory setups

---

## 2. Requirements & Setup

### Requirements

* **Python 2.7 or higher**
* **Active Directory environment** or access to an **LDAP server**
* **LDAP** access credentials for connecting to the AD environment (admin credentials preferred for full access)

### Installation

```bash
# Clone the ldapdomaindump repository
git clone https://github.com/dirkjanm/ldapdomaindump.git
cd ldapdomaindump
# Install required dependencies
pip install -r requirements.txt
```

---

## 3. Core Usage

### 3.1 Basic Enumeration

```bash
# Start ldapdomaindump to enumerate the AD environment
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host>
```

* **`-u`**: Username for authenticating against the LDAP server
* **`-p`**: Password for the specified username
* **`-d`**: Domain to enumerate (can be in the form `domain.com`)
* **`-h`**: IP or hostname of the **LDAP server** (e.g., `192.168.1.10`)

### 3.2 Dump Group Information

```bash
# Dump group membership data
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --groups
```

* This command will dump group membership data, helping attackers identify **privileged groups** like **Domain Admins** or **Enterprise Admins**

### 3.3 Dump User Information

```bash
# Dump user account information
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --users
```

* Retrieves a list of **user accounts** from the AD environment, useful for identifying **service accounts** and **administrative users**

### 3.4 Dump Organizational Units (OUs)

```bash
# Dump organizational units and their objects
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --organisational-units
```

* Extracts **organizational unit** (OU) structure and **attributes**, giving insight into the domain's structure

### 3.5 Dump Permissions and Trusts

```bash
# Dump permissions and trusts data
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --permissions --trusts
```

* Lists **permissions** and **trust relationships** within the AD environment, helping identify vulnerable configurations or **lateral movement paths**

### 3.6 Output Data

```bash
# Save output in a CSV or JSON format
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --output json
```

* Use this option to save the output data in a structured format like **JSON** for further analysis or reporting

---

## 4. Tips, Tricks, Best Practices

* **Use Admin Credentials**: To get the most out of ldapdomaindump, use **domain administrator credentials** to get full access to **all objects** in the AD environment
* **Focus on Privileged Groups**: Pay close attention to **Domain Admins**, **Enterprise Admins**, and **Schema Admins** groups, as they can provide elevated privileges
* **Dump Trust Relationships**: Trust relationships often represent **lateral movement paths** in multi-domain environments, so enumerate these to understand how domains are connected
* **Combine with BloodHound**: Combine the data from **ldapdomaindump** with **BloodHound** for advanced **AD attack path analysis**
* **Automation**: Consider automating **ldapdomaindump** as part of your post-exploitation toolkit to gather critical information faster when on an engagement

---

## 5. Cheat Sheet

```bash
# Basic enumeration of AD data (users, groups, trusts)
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host>

# Dump group memberships
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --groups

# Dump user account information
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --users

# Dump organizational unit information
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --organisational-units

# Dump permissions and trust relationships
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --permissions --trusts

# Save output as JSON
python ldapdomaindump.py -u <username> -p <password> -d <domain> -h <ldap_host> --output json
```

---
