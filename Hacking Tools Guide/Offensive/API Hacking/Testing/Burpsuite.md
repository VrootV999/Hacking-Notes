# Burp Suite

**Type:** Web Application Security Testing / Proxy / Penetration Testing
**Focus:** Interception, scanning, fuzzing, vulnerability discovery, and automation

---

## 1. Installation & Setup

### Requirements

* Java 11+ (for Burp Suite Professional / Community)
* Internet access for Community download or license verification
* Optional: Browser with manual proxy configuration (Firefox, Chrome)

### Installation Methods

#### Option 1: Official Installer (Windows/macOS/Linux)

1. Download from [PortSwigger](https://portswigger.net/burp)
2. Run installer:
3. Launch Burp Suite

#### Option 2: Using Snap (Linux)

```bash
sudo snap install burpsuite
burpsuite
```

---

## 2. Configuration

### Proxy Setup

* **Default Proxy:** `127.0.0.1:8080`
* Configure browser to route traffic through Burp’s proxy
* Enable **intercept** to capture requests for testing

### Certificates

* Install Burp CA certificate to avoid SSL/TLS errors:

```text
1. Proxy → Options → Import / Export CA
2. Export as DER/PEM
3. Add to browser or OS trusted certificates
```

### Project Options

* **Scope:** Define target domains to reduce noise
* **Logging:** Enable to track request/response data
* **User Options:** Keyboard shortcuts, display preferences

---

## 3. Core Modules

| Module               | Purpose                                                   |
| -------------------- | --------------------------------------------------------- |
| **Proxy**            | Intercept, modify, and forward HTTP/HTTPS requests        |
| **Target**           | Define scope, map site structure, site map analysis       |
| **Scanner**          | Automatic vulnerability scanning (Professional only)      |
| **Intruder**         | Automated fuzzing of parameters and endpoints             |
| **Repeater**         | Manual testing by replaying and modifying requests        |
| **Sequencer**        | Analyze randomness of tokens and session IDs              |
| **Decoder**          | Encode/decode data (Base64, URL, HTML, etc.)              |
| **Comparer**         | Compare responses, requests, or files for differences     |
| **Extensions**       | Add custom functionality via BApp Store or custom scripts |
| **Engagement Tools** | Annotations, issue tracking, notes                        |

---

## 4. Common Usage

### 4.1 Intercepting Requests

1. Enable **Proxy → Intercept → On**
2. Send browser traffic through `127.0.0.1:8080`
3. Modify request headers, cookies, or parameters as needed
4. Forward to server after inspection

### 4.2 Repeater Testing

```text
# Steps:
1. Right-click intercepted request → Send to Repeater
2. Modify request parameters manually
3. Send and analyze response
```

### 4.3 Intruder Fuzzing

* **Positions:** Identify which parameters to fuzz
* **Payloads:** Choose wordlists (`SimpleList`, `SecLists`)
* **Attack Types:** Sniper, Battering Ram, Pitchfork, Cluster Bomb

```bash
# Example: Fuzz login endpoint
Target: POST /login
Positions: username, password
Payloads: usernames.txt, passwords.txt
Attack: Cluster Bomb
```

### 4.4 Scanner (Pro)

* Automated vulnerability detection:

  * SQLi, XSS, SSRF, CSRF, Open Redirect, File Inclusion
* Use **active scan** for full coverage or **passive scan** for safe observation

---

## 5. Extensions & Automation

### BApp Store Extensions

* **Autorize:** Access control testing
* **Logger++:** Enhanced request logging
* **Turbo Intruder:** High-performance fuzzing
* **Retire.js:** JavaScript vulnerability scanning

### Custom Extensions

* Languages: **Java**, **Python (Jython)**, **Ruby**
* Automate workflows, integrate APIs, custom reporting

### CLI Integration

* Burp Suite Professional supports **headless scanning** and automated reporting:

```bash
java -jar burpsuite_pro.jar --project-file=myproject.burp --user-config=myconfig.json
```

---

## 6. Advanced Techniques

### Session Handling

* Configure session tokens in **Project Options → Sessions**
* Automatic token handling for authenticated fuzzing

### Macros & CSRF Tokens

* Setup macros to handle login flows
* Capture dynamic CSRF tokens for automated Intruder attacks

### Collaborator Integration

* Use Burp Collaborator for detecting **blind SSRF, OOB vulnerabilities**

### Active Scanning Tips

* Limit scope to reduce false positives
* Use **Scan Configurations** to tune detection thresholds
* Combine with **Intruder** for targeted exploitation

---

## 7. Workflow (Professional)

1. **Proxy Configuration** → Intercept traffic
2. **Scope Definition** → Add target domains
3. **Passive Analysis** → Review site map
4. **Active Scanning** → Identify vulnerabilities
5. **Manual Testing** → Repeater + Intruder
6. **Automation & Extensions** → Autorize, Turbo Intruder, Logger++
7. **Reporting** → Export findings (HTML, XML, JSON)

---

## 8. Tips, Tricks & Best Practices

* Always define **scope** to avoid illegal testing outside targets
* Use **extensions** to enhance workflow efficiency
* Save **project files** for continuous testing
* Prefer **Intruder + Payload lists from SecLists** for comprehensive fuzzing
* Leverage **Collaborator** for OOB testing
* Combine Burp results with tools like `Amass`, `httpx`, or `wfuzz` for integrated recon

---

## 9. Quick Reference Cheat Sheet

```text
# Proxy Interception
Proxy → Intercept → On
Browser → 127.0.0.1:8080

# Send request to Repeater
Right-click → Send to Repeater

# Intruder Setup
Right-click → Send to Intruder
Set Positions → Load Payloads → Start Attack

# Scanner (Pro)
Target → Site Map → Scan → Active Scan

# Extensions
Extender → BApp Store → Install (Autorize, Logger++, Turbo Intruder)

# Headless Scan (CLI, Pro)
java -jar burpsuite_pro.jar --project-file=myproject.burp --user-config=myconfig.json
```

---
