# dalfox

**Type:** XSS scanning and payload injection tool
**Focus:** Detecting and exploiting Cross-Site Scripting vulnerabilities

---

## 1. Overview

* **dalfox** is a powerful tool for automated XSS testing
* Supports:

  * Parameter discovery
  * Reflected and stored XSS
  * DOM-based XSS
  * Blind XSS reporting via interactsh

---

## 2. Installation & Setup

### Requirements

* Go 1.19+

### Installation via Go

```bash
GO111MODULE=on go install github.com/hahwul/dalfox/v2@latest
```

### Verify Installation

```bash
dalfox version
```

---

## 3. Core Usage

### 3.1 Basic XSS Scan

```bash
dalfox url https://target.com/page?search=test
```

### 3.2 Scan with Wordlist

```bash
dalfox url https://target.com/page?search=FUZZ -w xss_payloads.txt
```

### 3.3 Blind XSS Detection

```bash
dalfox url https://target.com/page?search=test --blind
```

* Automatically sends payloads to **interactsh** for OOB detection

### 3.4 Multiple URLs from File

```bash
dalfox file urls.txt
```

### 3.5 Fuzz Query Parameters

```bash
dalfox url https://target.com/page?search=FUZZ -w xss_payloads.txt
```

---

## 4. Advanced Usage

### 4.1 DOM XSS Detection

```bash
dalfox url https://target.com/page --dom
```

* Analyzes JavaScript on the page for client-side XSS

### 4.2 Silent Mode for Automation

```bash
dalfox url https://target.com/page --silent -o results.txt
```

* Outputs results in machine-readable format

### 4.3 Integration with Subdomain/Recon Workflows

```bash
subfinder -d example.com -silent | httpx -silent | dalfox file - 
```

* Combines live host discovery with XSS scanning

### 4.4 Custom Interactsh Server

```bash
dalfox url https://target.com/page --blind --interactsh-url https://custom.interactsh.com
```

* Useful for internal infrastructure or avoiding rate limits

---

## 5. Security & Operational Tips

* Test only on authorized targets
* Use `--rate` and `--timeout` to avoid DoS
* Combine with **httpx** to scan only live hosts
* Save results in JSON/CSV for automated workflows

---

## 6. Cheat Sheet

```text
# Basic XSS scan
dalfox url https://target.com/page?search=test

# Scan with wordlist
dalfox url https://target.com/page?search=FUZZ -w xss_payloads.txt

# Blind XSS detection via interactsh
dalfox url https://target.com/page?search=test --blind

# Multiple URLs from file
dalfox file urls.txt

# DOM XSS detection
dalfox url https://target.com/page --dom

# Silent mode
dalfox url https://target.com/page --silent -o results.txt

# Workflow integration with subfinder & httpx
subfinder -d example.com -silent | httpx -silent | dalfox file -
```

