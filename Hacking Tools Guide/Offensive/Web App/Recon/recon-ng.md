# Recon-ng

**Type:** Web Reconnaissance Framework / OSINT Tool
**Focus:** Automated reconnaissance, data collection, and reporting

---

## 1. Full Feature Overview

* Modular framework similar to Metasploit but for reconnaissance
* Supports domain, IP, email, and social media recon
* Pre-built modules for WHOIS, DNS, SSL, social media, and breach lookups
* API key integration for multiple services: Shodan, VirusTotal, Twitter, Google, etc.
* Database-backed to store results for complex campaigns
* Supports reporting in HTML, CSV, JSON, and TXT
* CLI interface with scripting and automation
* Supports custom module creation

---

## 2. Installation & Setup

### Requirements

* Python 3.x
* Git

### Installation

```bash
# Clone repository
git clone https://github.com/lanmaster53/recon-ng.git
cd recon-ng

# Install dependencies
pip install -r REQUIREMENTS
```

### Launch

```bash
python recon-ng
```

---

## 3. Core Usage

### 3.1 Workspaces

* Isolate different campaigns

```bash
workspace create target_campaign
workspace select target_campaign
```

### 3.2 Add Domains/Targets

```bash
add domains example.com
show domains
```

### 3.3 Modules

* List available modules

```bash
show modules
```

* Load module

```bash
use recon/domains-hosts/google_site
```

* Configure module

```bash
options set SOURCE example.com
run
```

---

## 4. API Key Integration

* Configure API keys for services:

```bash
keys add shodan YOUR_SHODAN_API_KEY
keys add virus_total YOUR_VT_API_KEY
```

* Required for modules that query external services

---

## 5. Reporting & Exporting

```bash
# Export results in CSV
export csv /path/to/output.csv

# Export results in HTML
export html /path/to/output.html
```

---

## 6. Tips, Tricks, Best Practices

* Use workspaces for separate targets to avoid data mix-up
* Chain modules to automate large campaigns
* Regularly update modules with `marketplace update`
* Combine with SpiderFoot and Shodan for deeper recon
* Store API keys securely and avoid sharing

---

## 7. Cheat Sheet

```text
# Start Recon-ng
python recon-ng

# Create/select workspace
workspace create target_campaign
workspace select target_campaign

# Add target domain
add domains example.com
show domains

# Load module
use recon/domains-hosts/google_site
options set SOURCE example.com
run

# List modules
show modules

# Add API key
keys add shodan YOUR_SHODAN_API_KEY

# Export results
export csv /path/to/output.csv
export html /path/to/output.html
```

---

