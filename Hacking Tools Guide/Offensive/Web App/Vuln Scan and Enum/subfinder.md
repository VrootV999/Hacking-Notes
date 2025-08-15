# subfinder

**Type:** Subdomain discovery tool
**Focus:** Reconnaissance, subdomain enumeration

---

## 1. Overview

* **subfinder** discovers subdomains of target domains quickly and accurately
* Uses passive sources primarily, can integrate active methods
* Often chained with `httpx` for live host detection

---

## 2. Installation & Setup

### Requirements

* Go 1.19+

### Installation via Go

```bash
GO111MODULE=on go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

### Verify Installation

```bash
subfinder -version
```

---

## 3. Core Usage

### 3.1 Basic Subdomain Enumeration

```bash
subfinder -d example.com
```

### 3.2 Output to File

```bash
subfinder -d example.com -o subdomains.txt
```

### 3.3 Silent Mode

```bash
subfinder -d example.com -silent
```

* Removes verbose logs for cleaner output

### 3.4 Multiple Domains

```bash
subfinder -dL domains.txt -o all_subdomains.txt
```

---

## 4. Advanced Usage

### 4.1 Using API Keys for Better Coverage

* Subfinder can integrate with APIs (Censys, VirusTotal, etc.)

```bash
subfinder -d example.com -all
```

* Pulls from passive and API sources

### 4.2 Combine with httpx for Live Hosts

```bash
subfinder -d example.com -silent | httpx -silent -o live.txt
```

### 4.3 Integration in Bug Bounty Workflow

* Feed discovered subdomains into scanners like **wfuzz, dalfox, SSRFPwned**
* Automate chaining for continuous monitoring

---

## 5. Security & Operational Tips

* Use API keys to increase accuracy and avoid rate limits
* Always ensure you have authorization to test target domains
* Save results in JSON/CSV for automation and workflow integration

---

## 6. Cheat Sheet

```text
# Single domain
subfinder -d example.com

# Save to file
subfinder -d example.com -o subdomains.txt

# Silent mode
subfinder -d example.com -silent

# Multiple domains
subfinder -dL domains.txt -o all_subdomains.txt

# Use passive + API sources
subfinder -d example.com -all

# Combine with httpx for live hosts
subfinder -d example.com -silent | httpx -silent -o live.txt
```

