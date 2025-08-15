# PowerView

**Type:** Enumeration, PowerShell, Active Directory
**Focus:** **PowerView** is a **PowerShell** tool used for **Active Directory (AD)** enumeration and **domain enumeration**. It is widely used in **Red Team** engagements and **penetration testing** to gather information about AD environments, exploit misconfigurations, and find targets for **lateral movement**. It is part of the **PowerSploit** framework but can also be used standalone.

---

## 1. Full Feature Overview

* **Domain Enumeration**: PowerView allows attackers to gather information about **domains**, **domain controllers**, **OU (Organizational Unit)** structures, and more.
* **Group Membership Enumeration**: Helps identify **group memberships** and which users belong to sensitive groups, such as **Domain Admins**, **Enterprise Admins**, and other privileged groups.
* **User Enumeration**: Enumerates **user attributes**, including **group memberships**, **last logon**, and **logon scripts**.
* **Domain Trusts**: Enumerates domain **trusts**, which helps in **domain enumeration** and **pivoting**.
* **Active Directory Shares**: Lists **Active Directory shares**, useful for finding accessible resources.
* **AD ACL Enumeration**: Can be used to inspect **Active Directory Access Control Lists** (ACLs) to find misconfigurations or weaknesses in the environment.
* **Kerberos Ticket Extraction**: Extracts **Kerberos tickets** from a compromised system, useful for **Pass-the-Ticket** attacks.

---

## 2. Requirements & Setup

### Requirements

* **PowerShell**: **PowerView** is a **PowerShell** script, so you need access to **PowerShell** on a **Windows** system (works with both **Windows** and **PowerShell Core**).
* **Active Directory Environment**: PowerView works in **Active Directory (AD)** environments, so you need access to a network with **AD** or **domain**.
* **Administrator or Low-Level Credentials**: While some functions can work with **low-level access**, certain features require **domain admin** privileges or the use of **token impersonation** (e.g., **Pass-the-Hash**).

### Installation

1. **Clone PowerSploit Repository**:

   ```bash
   git clone https://github.com/PowerShellMafia/PowerSploit.git
   cd PowerSploit
   ```

2. **Load PowerView** in PowerShell:

   ```powershell
   Import-Module .\PowerView.ps1
   ```

---

## 3. Core Usage

### 3.1 Basic Command Syntax

```powershell
Import-Module .\PowerView.ps1
```

Where:

* **`Import-Module`**: Loads the **PowerView** module into PowerShell.
* After importing the module, you can run the various **PowerView** cmdlets directly in the PowerShell session.

### 3.2 Domain Enumeration

```powershell
# Get domain information
Get-NetDomain
```

* **`Get-NetDomain`**: Retrieves the **domain name**, **domain controllers**, and basic domain-related information.

### 3.3 Domain Controller Enumeration

```powershell
# Enumerate all domain controllers in the domain
Get-NetDomainController
```

* **`Get-NetDomainController`**: Lists **domain controllers** in the target domain.

### 3.4 Group Membership Enumeration

```powershell
# Enumerate all groups in the domain
Get-NetGroup

# Find all members of the Domain Admins group
Get-NetGroupMember -GroupName "Domain Admins"
```

* **`Get-NetGroup`**: Lists all groups in the domain.
* **`Get-NetGroupMember`**: Lists members of a specific group (e.g., **Domain Admins**, **Enterprise Admins**, etc.).

### 3.5 User Enumeration

```powershell
# List all users in the domain
Get-NetUser

# Get detailed information about a specific user
Get-NetUser -UserName "username"
```

* **`Get-NetUser`**: Retrieves a list of all users in the domain.
* **`Get-NetUser -UserName "username"`**: Retrieves detailed information about a specific user (e.g., **group memberships**, **last logon**, **password policies**).

### 3.6 Domain Trust Enumeration

```powershell
# Enumerate domain trusts
Get-NetDomainTrust
```

* **`Get-NetDomainTrust`**: Retrieves **domain trusts**, which are useful for lateral movement or pivoting to other domains.

### 3.7 Active Directory Shares

```powershell
# Enumerate Active Directory Shares
Get-NetShare
```

* **`Get-NetShare`**: Lists all **shares** in the Active Directory environment.

### 3.8 Kerberos Ticket Extraction (for TGT)

```powershell
# Dump Kerberos tickets
Get-Ticket
```

* **`Get-Ticket`**: Dumps **Kerberos tickets** from the compromised system, which can then be used for **Pass-the-Ticket** attacks.

### 3.9 Access Control List (ACL) Enumeration

```powershell
# Enumerate Active Directory ACLs
Get-NetADObjectAcl
```

* **`Get-NetADObjectAcl`**: Retrieves the **Access Control Lists (ACLs)** for Active Directory objects, useful for discovering misconfigurations.

---

## 4. Tips, Tricks, Best Practices

* **Use for Initial Recon**: Start using **PowerView** in **initial reconnaissance** to gather information about the domain, groups, and users. This gives you a sense of the **attack surface**.
* **Search for Privileged Accounts**: Focus on identifying **privileged groups** like **Domain Admins** and **Enterprise Admins**. These groups are high-value targets for **privilege escalation** and **lateral movement**.
* **Pivot via Trusts**: If there are domain trusts, use them for **pivoting** into other domains. You can leverage trusted domains for further enumeration or exploitation.
* **Inspect ACLs**: Use **ACL enumeration** to find misconfigured permissions that may allow you to **elevate privileges** or **access sensitive data**.
* **Enumerate Shares**: Look for **misconfigured shares** that could be exploited for further post-exploitation activities (e.g., **writeable shares** or **sensitive information**).
* **Use with Other Tools**: **PowerView** can be used in conjunction with tools like **BloodHound** to map out attack paths and **post-exploitation scenarios**.

---

## 5. Cheat Sheet

```powershell
# Import PowerView Module
Import-Module .\PowerView.ps1

# Enumerate domain information
Get-NetDomain

# Enumerate all domain controllers
Get-NetDomainController

# List all groups in the domain
Get-NetGroup

# Get members of the "Domain Admins" group
Get-NetGroupMember -GroupName "Domain Admins"

# List all users in the domain
Get-NetUser

# Get detailed information about a specific user
Get-NetUser -UserName "username"

# Enumerate domain trusts
Get-NetDomainTrust

# Enumerate Active Directory shares
Get-NetShare

# Dump Kerberos tickets from the current session
Get-Ticket

# Enumerate AD object ACLs for permission issues
Get-NetADObjectAcl
```

---
