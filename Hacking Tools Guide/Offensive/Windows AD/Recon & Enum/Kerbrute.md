# KerBrute

**Type:** Brute-forcing, Authentication, Kerberos
**Focus:** **KerBrute** is a **Kerberos brute-forcing** tool, primarily used to **enumerate** valid **user accounts** in a **Windows Active Directory** environment via **Kerberos authentication**. It helps in **password spraying** attacks and assists with identifying weak or misconfigured accounts that can be leveraged for further **post-exploitation** activities.

---

## 1. Full Feature Overview

* **Kerberos Authentication**: Uses **Kerberos authentication** to **validate** the existence of **user accounts** within a domain without requiring **domain controller access**.
* **Username Enumeration**: Brute-forces a list of usernames and attempts to identify valid ones by checking Kerberos ticket responses.
* **Password Spraying**: KerBrute can be used for **password spraying** attacks by attempting to authenticate a large number of users with a single password, reducing the chance of lockouts.
* **Domain Controller Discovery**: Automatically detects and connects to the **target domain controller (DC)** to conduct brute-force or password-spray attacks.
* **Performance**: Optimized for **speed**, allowing attackers to brute-force large lists of usernames very quickly.
* **Account Lockout Detection**: Detects when an account becomes **locked** due to failed authentication attempts, helping refine subsequent attacks.

---

## 2. Requirements & Setup

### Requirements

* **Domain Information**: The target domain and domain controller (DC) information is needed. You can either specify it manually or let KerBrute auto-detect it.
* **Python**: **KerBrute** is written in **Python**, so Python 3 is required to run the tool.
* **Access to a Kerberos-enabled environment**: You need access to a **Kerberos**-enabled environment, typically **Windows** or **Active Directory**.

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/vanhauser-thc/KerBrute.git
   cd KerBrute
   ```

2. **Install Dependencies**:

   * Install Python requirements:

     ```bash
     pip3 install -r requirements.txt
     ```

3. **Run KerBrute**:

   * Run the tool using the following syntax:

     ```bash
     python3 kerbrute.py -d <domain> -U <user_list> -P <password_list>
     ```

---

## 3. Core Usage

### 3.1 Basic Command Syntax

```bash
kerbrute.py -d <domain> -U <user_list> -P <password_list> [options]
```

Where:

* **`-d <domain>`**: Specifies the **domain** (e.g., **example.com**).
* **`-U <user_list>`**: A file containing a list of usernames to test against the **Kerberos server**.
* **`-P <password_list>`**: A file containing a list of **passwords** for password spraying.

### 3.2 Username Enumeration

```bash
# Check if a list of usernames are valid for the given domain
python3 kerbrute.py userenum -d <domain> -U <user_list>
```

* **`userenum`**: Enumerates usernames and checks if they exist in the **Kerberos authentication system**.

### 3.3 Password Spraying Attack

```bash
# Perform a password spraying attack with a single password across all users
python3 kerbrute.py passspray -d <domain> -U <user_list> -P <password>
```

* **`passspray`**: Executes a **password spraying** attack, attempting a single password for all users in the specified list.

### 3.4 Brute Force Password Attempts

```bash
# Brute force each user in the user list with passwords from the password list
python3 kerbrute.py brute -d <domain> -U <user_list> -P <password_list>
```

* **`brute`**: Performs a **brute-force** attack, testing each combination of users and passwords from the respective lists.

### 3.5 Automatic Domain Controller Discovery

```bash
# Auto-discovery of domain controllers and target the correct one
python3 kerbrute.py passspray -d <domain> -U <user_list> -P <password> --dc-ip <domain_controller_ip>
```

* **`--dc-ip <domain_controller_ip>`**: Optionally specify a **domain controller IP** if automatic discovery fails.

### 3.6 Account Lockout Detection

```bash
# Enable lockout detection to avoid triggering too many lockouts
python3 kerbrute.py brute -d <domain> -U <user_list> -P <password_list> --lockout
```

* **`--lockout`**: Enables **lockout detection**, preventing the tool from triggering account lockouts after several failed attempts.

### 3.7 Output Formatting

```bash
# Save the output to a file
python3 kerbrute.py brute -d <domain> -U <user_list> -P <password_list> --output results.txt
```

* **`--output <filename>`**: Saves the results to a text file for further analysis or reporting.

---

## 4. Tips, Tricks, Best Practices

* **Use Large Wordlists**: When conducting **brute force** or **password spraying**, make sure to use well-curated and large wordlists, especially for common **passwords**.
* **Avoid Lockouts**: Use the **lockout detection** feature to prevent triggering account lockouts, which could result in being blocked from further attempts.
* **Use with Hydra**: Combine **KerBrute** with other tools like **Hydra** for additional password-guessing capabilities in **Kerberos** environments.
* **Domain Controller Discovery**: If the domain controller is not known, **KerBrute** can automatically detect and connect to it, but always specify it manually if needed to speed up the attack.
* **Monitor Account Status**: When using **username enumeration**, make sure to monitor **account status** after running tests. Look for accounts that are **active** but have weak or easy-to-guess passwords.
* **Use Common Passwords**: For **password spraying** attacks, **use common passwords** (e.g., `Password123`, `Welcome1`, etc.) for higher chances of success.

---

## 5. Cheat Sheet

```bash
# Basic username enumeration against the domain
python3 kerbrute.py userenum -d <domain> -U <user_list>

# Perform a password spraying attack with a single password
python3 kerbrute.py passspray -d <domain> -U <user_list> -P <password>

# Perform a brute force attack for all users with a password list
python3 kerbrute.py brute -d <domain> -U <user_list> -P <password_list>

# Enable account lockout detection to avoid triggering lockouts
python3 kerbrute.py brute -d <domain> -U <user_list> -P <password_list> --lockout

# Save output to a file
python3 kerbrute.py brute -d <domain> -U <user_list> -P <password_list> --output results.txt
```

---
