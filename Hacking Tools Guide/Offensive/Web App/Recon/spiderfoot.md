# SpiderFoot

**Type:** Open-Source Intelligence (OSINT) Automation Tool
**Focus:** Reconnaissance, footprinting, attack surface mapping

---

## 1. Full Feature Overview

* Automated scanning for domains, IPs, emails, names, phone numbers, and usernames
* Integrates with multiple data sources: WHOIS, Shodan, VirusTotal, HaveIBeenPwned, DNS servers
* Discovery of subdomains, DNS records, netblocks, ports, and services
* Detection of leaked credentials and data breaches
* Active and passive reconnaissance
* API integration for extended data collection
* Export results in CSV, JSON, PDF, or SQLite
* Scheduling and automation via command line or web interface
* Customizable modules for extensibility

---

## 2. Installation & Setup

### Requirements

* Python 3.8+
* Pip

### Installation

```bash
# Clone repository
git clone https://github.com/smicallef/spiderfoot.git
cd spiderfoot

# Install dependencies
pip install -r requirements.txt
```

### Launch

* **Web Interface**

```bash
python sf.py -l 127.0.0.1:5001
# Access via http://127.0.0.1:5001
```

* **CLI Mode**

```bash
python sf.py -s target.com -m all -o OUTPUT.html
```

---

## 3. Core Usage

### 3.1 Scanning a Domain

```bash
# Passive scan
python sf.py -s target.com -m passive_dns,whois,geoip -o output.json

# Full scan
python sf.py -s target.com -m all -o full_report.html
```

### 3.2 Scanning IP or Subnet

```bash
python sf.py -s 192.168.1.0/24 -m all -o ip_scan.json
```

### 3.3 Email Recon

```bash
python sf.py -s email@example.com -m breaches,social,whois -o email_report.json
```

---

## 4. Advanced Usage

* **Module Selection:** Only run specific modules to reduce noise or API usage

```bash
python sf.py -s target.com -m subdomain_dns,whois -o report.json
```

* **API Integration:** Configure API keys for Shodan, VirusTotal, etc., in `sfcli.cfg`
* **Scheduling:** Use cron or Windows Task Scheduler to automate scans
* **Database Output:** Store results in SQLite for incremental scans

```bash
python sf.py -s target.com -m all -o db.sqlite3
```

---

## 5. Tips, Tricks, Best Practices

* Always respect API rate limits to avoid blocking
* Combine SpiderFoot with other OSINT tools for layered reconnaissance
* Use CLI mode for automation and web interface for exploration
* Validate findings with multiple sources
* Run in isolated environment to avoid leaking queries to public networks

---

## 6. Cheat Sheet

```text
# Web UI
python sf.py -l 127.0.0.1:5001

# Full domain scan
python sf.py -s target.com -m all -o full_report.html

# Passive modules only
python sf.py -s target.com -m passive_dns,whois,geoip -o output.json

# Scan IP range
python sf.py -s 192.168.1.0/24 -m all -o ip_scan.json

# Email reconnaissance
python sf.py -s email@example.com -m breaches,social,whois -o email_report.json

# Store results in database
python sf.py -s target.com -m all -o db.sqlite3
```

---
