# Autorize

**Type:** Authorization / Access Control Testing Tool
**Focus:** Detecting broken access control vulnerabilities in web applications

---

## 1. Installation & Setup

### Requirements

* Python 3.6+ (`python3 --version`)
* Pip package manager
* Firefox or Chrome for BurpSuite/Proxy integration (optional)
* Git for cloning

### Installation Steps

1. **Clone Repository**

```bash
git clone https://github.com/1N3/Autorize.git
cd Autorize
```

2. **Install Dependencies**

```bash
pip3 install -r requirements.txt
```

3. **Verify Installation**

```bash
python3 autorize.py -h
```

* Displays help menu to confirm installation

---

## 2. Supported Workflows

* **Test access control bypass** by modifying HTTP requests
* **Check role-based access control (RBAC) issues**
* **Automate detection of endpoints vulnerable to privilege escalation**

---

## 3. Integration with BurpSuite / Proxy

* **Capture Requests** in BurpSuite
* **Export Requests** as `.txt` or use HTTP history
* **Feed into Autorize**:

```bash
python3 autorize.py -r requests.txt -u https://target.com -p "username=attacker&role=admin"
```

### Key Flags

| Flag           | Description                          |
| -------------- | ------------------------------------ |
| `-r <file>`    | Request file exported from BurpSuite |
| `-u <url>`     | Target endpoint for testing          |
| `-p <payload>` | Parameter modification for testing   |
| `-v`           | Verbose mode, shows request/response |
| `-t <threads>` | Number of concurrent tests           |

---

## 4. Command-Line Usage

### Basic Test

```bash
python3 autorize.py -r requests.txt -u https://target.com
```

### Test Specific Parameters

```bash
python3 autorize.py -r requests.txt -p "role=admin" -u https://target.com
```

### Run Concurrent Tests

```bash
python3 autorize.py -r requests.txt -t 10 -u https://target.com
```

---

## 5. Workflow (Professional)

1. **Intercept requests** using BurpSuite or proxy
2. **Export request(s)** into a `.txt` file
3. **Run Autorize** against endpoints:

```bash
python3 autorize.py -r requests.txt -u https://target.com
```

4. **Analyze Results**

   * HTTP 200 responses on restricted endpoints indicate potential access control issues
5. **Modify parameters** for deeper tests:

```bash
-p "user_id=1&role=admin"
```

6. **Automate Multi-threaded Testing** to speed up large application testing

---

## 6. Advanced Features

* **Parameter Fuzzing**

  * Autorize can iterate through multiple parameter values to test access control boundaries

```bash
python3 autorize.py -r requests.txt -p "role=admin,user,guest"
```

* **Session Cookie Testing**

  * Tests access control bypass using different session cookies

```bash
python3 autorize.py -r requests.txt -c "SESSIONID=abcd1234" -u https://target.com
```

* **Integration with CI/CD Pipelines**

  * Can be scripted into automated security scans by feeding request logs from staging or testing environments

---

## 7. Tips, Tricks & Best Practices

* Always **use a copy of production/staging requests**—do not test on live users
* Start with **passive enumeration** before parameter fuzzing
* Combine with **BurpSuite Repeater** to validate findings
* Multi-threading speeds up large applications but watch for **rate-limiting**
* Use verbose mode `-v` to capture unexpected behaviors

---

## 8. Quick Reference Cheat Sheet

```text
# Basic Usage
python3 autorize.py -r requests.txt -u https://target.com

# Test specific parameters
python3 autorize.py -r requests.txt -p "role=admin" -u https://target.com

# Multi-threaded testing
python3 autorize.py -r requests.txt -t 10 -u https://target.com

# Parameter fuzzing
python3 autorize.py -r requests.txt -p "role=admin,user,guest" -u https://target.com

# Session cookie testing
python3 autorize.py -r requests.txt -c "SESSIONID=abcd1234" -u https://target.com
```

---
