# httpx

**Type:** Fast HTTP/S probing tool
**Focus:** Recon, endpoint discovery, vulnerability enumeration

---

## 1. Overview

* **httpx** is a fast and multi-purpose HTTP probing tool for offensive security
* Common uses:

  * Detecting live hosts from a list of domains or subdomains
  * Fingerprinting web servers and technologies
  * Checking response codes, titles, headers, and TLS information
  * Integration into automated bug bounty workflows

---

## 2. Installation & Setup

### Requirements

* Go 1.19+

### Installation via Go

```bash
GO111MODULE=on go install github.com/projectdiscovery/httpx/cmd/httpx@latest
```

### Verify Installation

```bash
httpx -version
```

* Should display installed version and help options

---

## 3. Core Usage

### 3.1 Simple Host Probe

```bash
cat targets.txt | httpx
```

* Checks which hosts are alive
* Outputs URL, status code, title, and content length

### 3.2 Include HTTP Methods

```bash
httpx -l targets.txt -methods GET,POST
```

### 3.3 Detect Technologies

```bash
httpx -l targets.txt -tech-detect
```

* Detects CMS, frameworks, and server software

### 3.4 Custom Headers

```bash
httpx -l targets.txt -H "User-Agent: Mozilla/5.0"
```

---

## 4. Advanced Usage

### 4.1 Probing Specific Ports

```bash
httpx -l targets.txt -ports 80,443,8080
```

### 4.2 SSL/TLS Information

```bash
httpx -l targets.txt -tls-probe
```

* Collects certificate info, expiry, issuer, and more

### 4.3 Extracting URLs for Further Testing

```bash
httpx -l targets.txt -silent -status-code -title -tech-detect -o urls.txt
```

* Outputs results to file for **Burp Suite, wfuzz, dalfox, SSRF testing**, etc.

### 4.4 Using as Part of Subdomain Recon

```bash
subfinder -d example.com -silent | httpx -silent -tech-detect -o live.txt
```

* Combines **subdomain discovery** and **live host detection** in one workflow

### 4.5 Integration with Other Tools

* **Burp Suite/Intruder:** feed live hosts to scan endpoints
* **Vulnerability scanners:** use output as input for wfuzz, Arjun, dalfox

---

## 5. Security & Operational Tips

* Always validate targets for **authorized testing**
* Use `-timeout` and `-threads` to avoid DoS or server overload
* Combine `httpx` with **automation scripts** for continuous monitoring of target domains
* Save results in structured formats (`-o` for CSV, JSON) for workflow chaining

---

## 6. Cheat Sheet

```text
# Simple live host detection
cat targets.txt | httpx

# Detect technologies
httpx -l targets.txt -tech-detect

# Scan specific ports
httpx -l targets.txt -ports 80,443,8080

# TLS/SSL info
httpx -l targets.txt -tls-probe

# Use custom headers
httpx -l targets.txt -H "User-Agent: Mozilla/5.0"

# Output results to file for further testing
httpx -l targets.txt -silent -status-code -title -tech-detect -o urls.txt

# Chain with subfinder for full recon
subfinder -d example.com -silent | httpx -silent -tech-detect -o live.txt
```

---
