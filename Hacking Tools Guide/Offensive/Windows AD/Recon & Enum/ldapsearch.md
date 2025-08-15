# ldapsearch

**Type:** Enumeration, LDAP, Active Directory
**Focus:** **ldapsearch** is a command-line tool used to interact with **LDAP (Lightweight Directory Access Protocol)** directories, commonly used for **Active Directory (AD) enumeration**. It is part of the **OpenLDAP** package, providing an easy way to **search and query** directory services for information such as **user details**, **group memberships**, **shares**, and more.

---

## 1. Full Feature Overview

* **User Enumeration**: Allows querying of **user accounts**, including details like **usernames**, **group memberships**, **password policies**, and **last login times**.
* **Group Enumeration**: Retrieves information about **group memberships** within the **Active Directory**, helping identify users in privileged groups (e.g., **Domain Admins**, **Enterprise Admins**).
* **Domain Enumeration**: Can gather information about the domain and other **LDAP-based directories**.
* **AD Attributes**: Allows querying of specific **Active Directory attributes**, such as **object class**, **distinguished name (DN)**, and **objectGUID**.
* **Bind and Search**: Supports various **bind operations** (anonymous or authenticated) and the ability to perform **search queries** to gather the necessary information.
* **LDAP Injection**: Can be used to test for **LDAP injection** vulnerabilities in web applications that rely on LDAP services for authentication.

---

## 2. Requirements & Setup

### Requirements

* **Linux / macOS / Windows**: **ldapsearch** is available by default on many Linux systems and can also be installed on **macOS** and **Windows**.
* **LDAP Access**: The tool requires access to an **LDAP server** or **Active Directory** server for querying. If using **Windows AD**, ensure you have proper credentials or that the server allows anonymous binds.

### Installation

1. **Linux (Debian-based)**:

   ```bash
   sudo apt install ldap-utils
   ```

2. **macOS** (via Homebrew):

   ```bash
   brew install openldap
   ```

3. **Windows**:

   * Download **OpenLDAP** tools or use **Windows Subsystem for Linux (WSL)** to install the necessary tools.

---

## 3. Core Usage

### 3.1 Basic Command Syntax

```bash
ldapsearch -x -h <server_ip> -b <base_dn> -D <bind_dn> -w <password> <search_filter>
```

Where:

* **`-x`**: Use simple authentication instead of SASL (by default, LDAP supports SASL).
* **`-h <server_ip>`**: Specifies the target **LDAP server** (e.g., `ldap://target_ip`).
* **`-b <base_dn>`**: The **base distinguished name** (DN) to start the search from (e.g., `dc=example,dc=com`).
* **`-D <bind_dn>`**: The **DN** to bind to the LDAP server (e.g., `cn=admin,dc=example,dc=com`).
* **`-w <password>`**: The password for the **bind DN**.
* **`<search_filter>`**: The LDAP search filter to specify the data you want (e.g., `(objectClass=user)`).

### 3.2 Anonymous Bind (Without Credentials)

```bash
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(objectClass=user)"
```

* **`-x`**: Simple authentication with no credentials, which is useful if the server allows anonymous access.

### 3.3 Bind with Credentials (Authenticated Bind)

```bash
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" -D "cn=admin,dc=example,dc=com" -w "<password>" "(objectClass=person)"
```

* **`-D`**: Specifies the **bind DN** (the **admin** or **user** that you use to authenticate).
* **`-w`**: Password for the **bind DN**.

### 3.4 Searching for Users

```bash
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(objectClass=user)"
```

* This will return all **user accounts** within the **base DN** `dc=example,dc=com`.

### 3.5 Searching for Specific Attributes

```bash
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(sAMAccountName=jdoe)" dn mail
```

* This command searches for a specific **user** (`sAMAccountName=jdoe`) and retrieves the **DN** and **email** (`mail`) attributes.

### 3.6 Searching for Groups

```bash
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(objectClass=group)"
```

* This command enumerates all **groups** in the domain.

### 3.7 Retrieve Group Membership for a User

```bash
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(member=uid=jdoe,ou=users,dc=example,dc=com)"
```

* This searches for all **groups** that a particular user (`jdoe`) is a member of.

---

## 4. Tips, Tricks, Best Practices

* **Use Wildcards**: You can use **wildcard characters** (e.g., `*`) to search for more general information. For example:

  ```bash
  ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(sAMAccountName=*)"
  ```

  This will list all **user accounts**.

* **Test LDAP Injection**: You can test for **LDAP injection vulnerabilities** in applications using LDAP-based authentication by submitting **malicious input** in the search filters, like:

  ```bash
  (sAMAccountName=*)|(objectClass=*)
  ```

* **Check for Anonymous Access**: Some LDAP servers are configured to allow **anonymous binds**, which can provide valuable **directory information** without authentication.

* **Use for Post-Exploitation**: After compromising a system in an **Active Directory environment**, use **ldapsearch** to gather information about users, groups, shares, and other resources that may be useful for **lateral movement** or **privilege escalation**.

* **Combine with Other Tools**: Tools like **BloodHound** can take advantage of **LDAP** data gathered by **ldapsearch** to map out attack paths within the Active Directory.

* **Filter with Specific Attributes**: Use more specific **LDAP filters** to narrow down your results. For example, search for only users with a specific group membership or those who have been **recently modified**.

---

## 5. Cheat Sheet

```bash
# Perform a basic anonymous LDAP search for all users
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(objectClass=user)"

# Perform an authenticated bind (with credentials) to search for users
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" -D "cn=admin,dc=example,dc=com" -w "<password>" "(objectClass=user)"

# Search for a specific user by sAMAccountName
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(sAMAccountName=jdoe)"

# List all groups in the domain
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(objectClass=group)"

# Search for groups a specific user is a member of
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(member=uid=jdoe,ou=users,dc=example,dc=com)"

# Retrieve a specific user's email
ldapsearch -x -h <server_ip> -b "dc=example,dc=com" "(sAMAccountName=jdoe)" dn mail
```

---
