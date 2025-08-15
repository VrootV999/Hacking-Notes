# Amass

**Type:** Recon / Subdomain Enumeration / OSINT
**Focus:** Attack surface mapping, domain enumeration, DNS brute-forcing, passive and active reconnaissance

---

## 1. Installation & Setup

### Requirements

* Go 1.18+ installed (`go version`)
* Git for cloning (optional if using precompiled binaries)
* Internet access for OSINT data sources
* Optional: API keys for enhanced enumeration (VirusTotal, Shodan, Censys, SecurityTrails, etc.)

### Installation Methods

#### Option 1: Using Go

```bash
go install github.com/owasp-amass/amass/v3/...@latest
```

* Adds `amass` to `$GOPATH/bin`
* Verify: `amass -version`

#### Option 2: Using Precompiled Binary (Linux/macOS)

```bash
wget https://github.com/OWASP/Amass/releases/download/v3.22.0/amass_linux_amd64.zip
unzip amass_linux_amd64.zip
sudo mv amass_linux_amd64/amass /usr/local/bin/
amass -version
```

#### Option 3: Using Homebrew (macOS)

```bash
brew install amass
```

---

## 2. Configuration

* **Configuration File Location:** `~/.config/amass/config.ini`
* **Purpose:** Store API keys, default wordlists, resolver configurations, and logging preferences

### Example Configuration for API Keys

```ini
[Default]
; API Keys
Shodan = YOUR_SHODAN_KEY
VirusTotal = YOUR_VIRUSTOTAL_KEY
SecurityTrails = YOUR_SECURITYTRAILS_KEY
CensysID = YOUR_CENSYS_ID
CensysSecret = YOUR_CENSYS_SECRET
```

### Recommended Config Adjustments

* **Resolvers:** Use custom DNS resolvers for stealth
* **Timeouts:** Increase for large-scale enumeration
* **Logging:** Enable verbose logging for later analysis

---

## 3. Core Usage

### Passive Subdomain Enumeration

```bash
amass enum -passive -d target.com
```

* Uses OSINT sources only (no DNS brute-force)
* Outputs discovered subdomains

### Active Enumeration

```bash
amass enum -active -d target.com
```

* Uses DNS resolution and brute-force
* Requires wordlists (`-w /path/to/wordlist.txt`)

### Combined Passive + Active

```bash
amass enum -d target.com -o output.txt
```

* Combines OSINT + brute-force
* Saves results to `output.txt`

---

## 4. Key Commands & Options

| Command / Flag   | Description                                   |
| ---------------- | --------------------------------------------- |
| `-d <domain>`    | Target domain                                 |
| `-dir <path>`    | Output directory                              |
| `-o <file>`      | Output file                                   |
| `-oA <basename>` | Save in multiple formats (txt, json, graph)   |
| `-passive`       | Passive OSINT-only enumeration                |
| `-active`        | Active enumeration (DNS queries, brute-force) |
| `-src`           | Show source of discovered subdomains          |
| `-ip`            | Resolve subdomains to IP addresses            |
| `-brute`         | Enable brute-force subdomain enumeration      |
| `-w <wordlist>`  | Custom wordlist for brute-force               |
| `-r <resolver>`  | Custom DNS resolver                           |
| `-config <file>` | Custom config file                            |
| `-asn <asn>`     | Discover IP space related to an ASN           |
| `-cidr <range>`  | Target specific IP ranges                     |
| `-v`             | Verbose logging                               |
| `-json`          | Output in JSON format                         |

---

## 5. Advanced Enumeration

### Brute-Force with Wordlists

```bash
amass enum -d target.com -brute -w /usr/share/wordlists/subdomains.txt -o brute.txt
```

### Subdomain Takeover Detection

* Combine `amass` with external tools like `subjack` or `tko-subs`
* Export `-oA` results to JSON, feed into takeover tools

### IP Space Discovery

```bash
amass intel -org "Target Organization" -whois -ip
```

* Maps ASN, netblocks, and related IP ranges

### Graphical Mapping

```bash
amass viz -d target.com -o graph.gexf
```

* Generates GraphML/GEXF for Gephi or network visualization tools

---

## 6. API Key Integration

* Enhances discovery speed and depth

* Sources include:

  * **VirusTotal**
  * **Shodan**
  * **Censys**
  * **SecurityTrails**
  * **PassiveDNS**

* Example usage:

```bash
amass enum -d target.com -passive -config ~/.config/amass/config.ini
```

---

## 7. Recon Workflow (Professional)

1. **Passive Enumeration**

```bash
amass enum -passive -d target.com -o passive.txt
```

2. **Active Brute-Force Enumeration**

```bash
amass enum -brute -w /usr/share/wordlists/subdomains.txt -d target.com -o active.txt
```

3. **Merge Results**

```bash
cat passive.txt active.txt | sort -u > all_subdomains.txt
```

4. **IP Resolution**

```bash
amass dns -d target.com -ip -o ip_map.txt
```

5. **Visual Mapping (Optional)**

```bash
amass viz -d target.com -o graph.gexf
```

---

## 8. Tips, Tricks & Best Practices

* Always start passive to reduce noise
* Use multiple wordlists for brute-force enumeration
* Combine OSINT sources with API keys for maximum coverage
* Use `-v` for verbose mode to debug missed subdomains
* Export results in multiple formats for automation (`-oA target`)
* Feed results into other offensive tools (e.g., `httpx`, `wfuzz`)

---

## 9. Quick Reference Cheat Sheet

```text
# Passive OSINT
amass enum -passive -d target.com -o passive.txt

# Active Brute-Force
amass enum -d target.com -brute -w /usr/share/wordlists/subdomains.txt -o brute.txt

# Combined Passive + Active
amass enum -d target.com -o all.txt

# Resolve IPs
amass dns -d target.com -ip -o ip_map.txt

# Graphical Mapping
amass viz -d target.com -o graph.gexf

# Using API Keys
amass enum -passive -d target.com -config ~/.config/amass/config.ini
```

---
