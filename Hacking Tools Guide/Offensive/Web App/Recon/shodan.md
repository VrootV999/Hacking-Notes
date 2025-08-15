# Shodan

**Type:** Internet-Wide Search Engine / Reconnaissance Tool
**Focus:** Discover exposed devices, services, and vulnerabilities

---

## 1. Full Feature Overview

* Search for connected devices by IP, hostname, port, service, or location
* Identify open ports, banners, and running services
* Detect vulnerabilities (CVEs) associated with discovered devices
* Supports filters: country, city, org, OS, hostname, port, product
* API access for automation and integration
* Export results in JSON, CSV, or XML
* Historical data queries
* Integration with tools like SpiderFoot, Metasploit, and Python scripts
* Shodan CLI for direct terminal usage

---

## 2. Installation & Setup

### Requirements

* Python 3.6+
* Pip
* Shodan API key (create free account at [https://account.shodan.io/](https://account.shodan.io/))

### Installation

```bash
# Install Shodan CLI
pip install shodan

# Initialize API key
shodan init YOUR_API_KEY
```

---

## 3. Core Usage

### 3.1 Basic Search

```bash
# Search for webcams
shodan search "webcamxp"

# Search by port
shodan search "port:22 country:US"
```

### 3.2 Retrieve Host Information

```bash
shodan host 8.8.8.8
```

### 3.3 Use Filters

* `country:<country_code>` → e.g., `country:US`
* `port:<port_number>` → e.g., `port:80`
* `org:"Organization Name"` → e.g., `org:"Google"`
* `os:"Linux"` → filter by operating system

```bash
shodan search "nginx country:US port:80"
```

### 3.4 Export Results

```bash
shodan download result_file.json "nginx country:US port:80"
```

---

## 4. API Usage

### Python Example

```python
import shodan

API_KEY = "YOUR_API_KEY"
api = shodan.Shodan(API_KEY)

# Search example
results = api.search("nginx port:80")
print(f"Total results: {results['total']}")
for result in results['matches']:
    print(result['ip_str'], result['port'], result['org'])
```

### Advanced API

* Count matching results: `api.count("nginx")`
* Get host info by IP: `api.host("8.8.8.8")`
* List exploits and CVEs associated with host: `api.exploits.search("nginx")`

---

## 5. Tips, Tricks, Best Practices

* Combine filters for precise results (e.g., country + port + org)
* Use Shodan CLI for quick recon in terminal
* Always check API rate limits
* Integrate with automation scripts or SpiderFoot for large-scale reconnaissance
* Validate results with other sources to avoid false positives

---

## 6. Cheat Sheet

```text
# Basic search
shodan search "webcamxp"

# Filter by country and port
shodan search "nginx country:US port:80"

# Retrieve host info
shodan host 8.8.8.8

# Download results
shodan download results.json "nginx country:US port:80"

# Initialize API key
shodan init YOUR_API_KEY

# Python API example
import shodan
api = shodan.Shodan("YOUR_API_KEY")
results = api.search("nginx port:80")
for r in results['matches']: print(r['ip_str'], r['port'], r['org'])
```

---
