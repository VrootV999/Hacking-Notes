# arjun

**Type:** HTTP parameter discovery and fuzzing tool
**Focus:** Automatic parameter enumeration for web applications

---

## 1. Overview

* **arjun** automatically discovers GET and POST parameters for a target URL
* Useful for finding hidden or undocumented endpoints
* Can be combined with fuzzing or XSS/SQLi scanners

---

## 2. Installation & Setup

### Requirements

* Python 3.6+

### Installation via Git

```bash
git clone https://github.com/s0md3v/Arjun.git
cd Arjun
pip install -r requirements.txt
```

### Verify Installation

```bash
python arjun.py --help
```

---

## 3. Core Usage

### 3.1 Scan Single URL

```bash
python arjun.py -u https://target.com/page
```

### 3.2 Scan with GET and POST Parameters

```bash
python arjun.py -u https://target.com/page -m GET,POST
```

### 3.3 Save Output to File

```bash
python arjun.py -u https://target.com/page -o results.txt
```

### 3.4 Silent Mode

```bash
python arjun.py -u https://target.com/page -s
```

* Reduces verbosity for automation

---

## 4. Advanced Usage

### 4.1 Scan Multiple URLs from File

```bash
python arjun.py -i urls.txt -o output.txt
```

### 4.2 Custom Wordlist

```bash
python arjun.py -u https://target.com/page -w wordlist.txt
```

### 4.3 Integration with Recon Workflow

```bash
subfinder -d example.com -silent | httpx -silent | xargs -I {} python arjun.py -u {} -o arjun_results.txt
```

---

## 5. Security & Operational Tips

* Use only on authorized targets
* Combine with vulnerability scanners like **dalfox** or **wfuzz**
* Use silent mode and output files for large-scale recon
* Wordlists can be customized to speed up or expand discovery

---

## 6. Cheat Sheet

```text
# Scan single URL
python arjun.py -u https://target.com/page

# Scan GET and POST parameters
python arjun.py -u https://target.com/page -m GET,POST

# Save output to file
python arjun.py -u https://target.com/page -o results.txt

# Silent mode
python arjun.py -u https://target.com/page -s

# Scan multiple URLs from file
python arjun.py -i urls.txt -o output.txt

# Use custom wordlist
python arjun.py -u https://target.com/page -w wordlist.txt

# Workflow integration with subfinder & httpx
subfinder -d example.com -silent | httpx -silent | xargs -I {} python arjun.py -u {} -o arjun_results.txt
```

