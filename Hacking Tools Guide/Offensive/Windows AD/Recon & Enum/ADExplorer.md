# adExplorer

**Type:** Active Directory Enumeration & Analysis
**Focus:** **adExplorer** is a **GUI-based** tool designed to simplify the process of **enumerating**, **exploring**, and **analyzing** **Active Directory** (AD) environments. It allows for an **interactive view** of AD objects and attributes, making it a valuable tool for **post-exploitation** and **network assessment**.

---

## 1. Full Feature Overview

* **adExplorer** provides a **graphical interface** for exploring the contents of an **Active Directory environment**
* It allows for detailed exploration of **users**, **groups**, **organizational units** (OUs), **permissions**, **shares**, and more, all in real-time
* Unlike command-line tools, adExplorer provides a **visual representation** of AD objects, making it easier to understand relationships and configurations
* It helps in gathering intelligence on **privileged accounts**, **group memberships**, and **delegated permissions**, which are essential for **privilege escalation** and **lateral movement**

---

## 2. Requirements & Setup

### Requirements

* **Windows OS**: Since adExplorer is primarily developed for Windows, it runs best on **Windows 7/10/11** and above
* **Domain or LDAP access**: Requires access to an **Active Directory environment** or an **LDAP** server

### Installation

1. **Download adExplorer** from the official **Microsoft Sysinternals** website:

   * [adExplorer Download](https://docs.microsoft.com/en-us/sysinternals/downloads/adexplorer)

2. Extract the downloaded zip file to a directory.

3. Run **adExplorer** by double-clicking the executable.

---

## 3. Core Usage

### 3.1 Connect to Active Directory Server

* Upon launching **adExplorer**, you will be prompted to **connect to an AD server** using **LDAP** or **SSL**. Enter the **server IP**, **port**, and **credentials** to authenticate to the AD environment.

### 3.2 Explore AD Structure

* After connecting, you can explore the entire **Active Directory structure**, including:

  * **Domains**
  * **Organizational Units (OUs)**
  * **Users and Groups**
  * **Group Policies**
  * **Domain Controllers**
* You can click on various objects to view **detailed attributes**, such as **account policies**, **membership information**, and **permissions**.

### 3.3 Search for Specific Objects

* Use the search functionality to quickly locate specific AD objects such as:

  * **Specific users**
  * **Groups**
  * **Shared resources**
  * **Group Policy Objects (GPOs)**
* adExplorer allows you to filter search results using various attributes and operators to pinpoint key targets for **privilege escalation** or **exploitation**.

### 3.4 Export Data

* adExplorer allows you to **export data** about the AD environment for further analysis or documentation.
* You can export data in **CSV**, **XML**, or **JSON** formats for:

  * User information
  * Group memberships
  * Organizational Units (OUs)
  * Permissions and delegation

### 3.5 Analyze Permissions and Group Memberships

* **adExplorer** displays group memberships and access control entries (ACEs) for both users and groups. This makes it easier to:

  * Identify users with **privileged access**
  * Analyze **delegated permissions**
  * Detect **misconfigurations** that can lead to privilege escalation

---

## 4. Tips, Tricks, Best Practices

* **Focus on Administrative Groups**: Look for groups like **Domain Admins**, **Enterprise Admins**, **Schema Admins**, and **Enterprise Administrators** to identify privileged accounts that could be used for **escalating privileges**
* **Check for Delegated Permissions**: Use adExplorer to check for **delegated permissions** within the AD environment, which can be leveraged for **lateral movement** or to gain elevated access
* **Look for Hidden Admin Accounts**: AD might contain hidden admin accounts or service accounts with elevated permissions. Use **adExplorer’s search** functionality to locate them based on naming conventions or attributes like **logon scripts**
* **Use Exported Data for Attack Path Mapping**: After exporting AD data, use it in conjunction with tools like **BloodHound** to identify possible attack paths, **lateral movement** techniques, or areas for escalation
* **Regular Audits**: Regularly audit AD environments for **misconfigurations** in groups and permissions to minimize the risk of attackers exploiting them

---

## 5. Cheat Sheet

```bash
# Connect to an Active Directory server
adExplorer.exe

# Search for users or groups
1. Launch adExplorer
2. Use the search bar to query for a specific object
3. Apply filters for attributes like name, group membership, etc.

# Export data
1. Right-click on any object (user, group, etc.)
2. Select "Export" and choose the desired format (CSV, JSON, XML)
```

---
