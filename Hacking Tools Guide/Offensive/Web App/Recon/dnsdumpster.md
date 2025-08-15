# dnsdumpster

**Type:** DNS Reconnaissance / OSINT Tool
**Focus:** Subdomain discovery, DNS mapping, footprinting

---

## 1. Full Feature Overview

* Free online DNS recon tool and API
* Identifies subdomains, MX, NS, TXT, and A records
* Generates domain maps with DNS relationships
* Visual network diagrams (hostnames and IPs)
* Can be used for reconnaissance and attack surface mapping

---

## 2. Installation & Setup

### Online Usage

* Accessible via: [https://dnsdumpster.com](https://dnsdumpster.com)
* No installation required

### Local/API Usage

* Python package available: `dnsdumpster`

```bash
pip install dnsdumpster
```

---

## 3. Core Usage

### 3.1 Using Python API

```python
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI

api = DNSDumpsterAPI()
res = api.search("example.com")

# Print discovered hosts
for host in res['hosts']:
    print(host['domain'], host['ip'], host['type'])
```

### 3.2 Output Details

* `domain`: Subdomain or hostname
* `ip`: Associated IP address
* `type`: DNS record type (A, MX, NS, TXT)
* `provider`: Hosting provider or service if detected

---

## 4. Tips, Tricks, Best Practices

* Always verify results with multiple sources (e.g., Amass, Subfinder)
* Combine with SpiderFoot or Recon-ng for automated recon
* Use visual maps for easy attack surface identification
* Avoid overloading the service; respect API usage policies

---

## 5. Cheat Sheet

```text
# Install Python package
pip install dnsdumpster

# Example usage
from dnsdumpster.DNSDumpsterAPI import DNSDumpsterAPI
api = DNSDumpsterAPI()
res = api.search("example.com")
for host in res['hosts']:
    print(host['domain'], host['ip'], host['type'])
```

---
