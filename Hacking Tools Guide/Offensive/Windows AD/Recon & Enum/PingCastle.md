# PingCastle

**Type:** Active Directory Security & Risk Assessment
**Focus:** **PingCastle** is a **security assessment tool** designed for **Active Directory** environments. It helps security professionals perform a **security risk analysis** of their **AD infrastructure**, identifying **misconfigurations**, potential **attack paths**, and **vulnerabilities** within an **Active Directory** domain.

---

## 1. Full Feature Overview

* **PingCastle** evaluates the **security posture** of Active Directory (AD) environments, helping identify **weaknesses** and **misconfigurations** that could be exploited by attackers.
* The tool generates a **security score** and provides recommendations to improve **AD security**.
* **PingCastle** includes multiple modules for different types of assessments, including **security audits**, **attack path analysis**, and **privilege escalation** tests.
* It helps identify areas like **overly permissive group memberships**, **weak account policies**, **high-risk delegation**, and **other exploitable vulnerabilities**.

---

## 2. Requirements & Setup

### Requirements

* **Active Directory Environment**: You need access to a **Windows AD domain** for testing and assessment.
* **Windows OS**: PingCastle runs on **Windows** but can be used to analyze remote **AD environments** from any machine.

### Installation

1. **Download PingCastle** from the official GitHub repository or the PingCastle website:

   * [PingCastle GitHub](https://github.com/EntynetProject/PingCastle)

2. **Extract the ZIP file** to any directory.

3. To run PingCastle, simply execute the **PingCastle executable**:

   ```bash
   PingCastle.exe
   ```

---

## 3. Core Usage

### 3.1 Running an Assessment

```bash
# Run the PingCastle assessment against an AD environment
PingCastle.exe /scan /domain <domain_name> /user <username> /password <password>
```

* **`/scan`**: Initiates the scan to evaluate the security of the AD domain.
* **`/domain`**: Specifies the domain to be scanned.
* **`/user`**: Provides a **username** with sufficient access rights to the domain for the scan.
* **`/password`**: Specifies the **password** of the user. You can also use **Kerberos authentication** for better security.

This command will perform a **security assessment** of the domain and output a report that includes a security score and recommendations.

### 3.2 Generating a Security Report

```bash
# Generate a security report after the scan
PingCastle.exe /report <path_to_report>
```

* This generates a **comprehensive security report** summarizing the findings of the scan. It will include detailed information on:

  * **Security score** of the domain (high = safe, low = vulnerable)
  * **Misconfigurations** (e.g., **weak passwords**, **over-permissive group memberships**)
  * **Attack paths** and **privileged accounts**
  * **Recommendations** to improve AD security

### 3.3 Attack Path Analysis

```bash
# Perform attack path analysis to find lateral movement vectors
PingCastle.exe /attackpath /domain <domain_name> /user <username> /password <password>
```

* This feature identifies **attack paths** through the AD environment, helping pentesters and defenders understand potential lateral movement routes for an attacker within the domain.
* It highlights critical findings like **misconfigured trusts**, **elevated user accounts**, and **over-permissive access** that can be leveraged for **escalation**.

### 3.4 Running the Health Check

```bash
# Run a quick health check on the AD domain to identify critical issues
PingCastle.exe /health /domain <domain_name> /user <username> /password <password>
```

* This command runs a **quick security check**, providing insights into the most critical security weaknesses that could be exploited immediately. It’s useful for **quick assessments** and **pre-engagement preparations**.

---

## 4. Tips, Tricks, Best Practices

* **Focus on Low Security Score**: If your **PingCastle security score** is low, it indicates that there are **critical vulnerabilities** or misconfigurations in your AD environment. Pay attention to the **audit recommendations** and fix the issues before they’re exploited.
* **Privilege Escalation**: Use **PingCastle’s attack path analysis** to identify **privileged accounts** and potential escalation routes. It helps you map out how to move from **low-level accounts** to **Domain Admins**.
* **Combine with BloodHound**: After running PingCastle, you can export the findings and use them in combination with **BloodHound** to visualize attack paths and exploit potential vulnerabilities further.
* **Use Scheduled Scans**: Regularly run **PingCastle scans** on your Active Directory environment to proactively spot and fix any emerging risks.
* **Understand Group Delegation**: Pay attention to **delegated permissions** and ensure that only trusted accounts have **administrative access**. Misconfigured delegation is a frequent attack vector for **lateral movement**.

---

## 5. Cheat Sheet

```bash
# Scan an AD environment
PingCastle.exe /scan /domain <domain_name> /user <username> /password <password>

# Generate a security report
PingCastle.exe /report <path_to_report>

# Perform attack path analysis
PingCastle.exe /attackpath /domain <domain_name> /user <username> /password <password>

# Run a quick AD health check
PingCastle.exe /health /domain <domain_name> /user <username> /password <password>
```

---
