# wfuzz

**Type:** Web fuzzing tool
**Focus:** Parameter fuzzing, brute-forcing, and vulnerability discovery

---

## 1. Overview

* **wfuzz** is a flexible web application fuzzing tool
* Common uses:

  * Parameter fuzzing (GET/POST)
  * Directory and file brute-forcing
  * Detecting hidden endpoints
  * Injection points (SQLi, XSS, SSRF, etc.)

---

## 2. Installation & Setup

### Requirements

* Python 3.7+

### Installation via pip

```bash
pip install wfuzz
```

### Verify Installation

```bash
wfuzz --version
```

---

## 3. Core Usage

### 3.1 Basic Fuzzing

```bash
wfuzz -c -z file,wordlist.txt -u http://target.com/FUZZ
```

* `-c`: colored output
* `-z file,wordlist.txt`: defines the payload source
* `FUZZ`: placeholder in the URL

### 3.2 POST Request Fuzzing

```bash
wfuzz -c -z file,params.txt -d "username=FUZZ&password=FUZZ" -u http://target.com/login
```

### 3.3 Multiple Payloads

```bash
wfuzz -c -z file,usernames.txt -z file,passwords.txt -d "username=FUZZ1&password=FUZZ2" -u http://target.com/login
```

### 3.4 Status Code Filtering

```bash
wfuzz -c -z file,wordlist.txt -u http://target.com/FUZZ -fc 404
```

* Filters out 404 responses

---

## 4. Advanced Usage

### 4.1 Recursive Fuzzing

* Chain multiple fuzzers for nested directories

```bash
wfuzz -c -z file,dirs.txt -u http://target.com/FUZZ/FUZZ2
```

### 4.2 Header Fuzzing

```bash
wfuzz -c -z file,useragents.txt -H "User-Agent: FUZZ" -u http://target.com
```

### 4.3 JSON Body Fuzzing

```bash
wfuzz -c -z file,payloads.txt -d '{"username":"FUZZ","password":"FUZZ"}' -H "Content-Type: application/json" -u http://target.com/api/login
```

### 4.4 Advanced Filters

* Filter by response length, words, regex:

```bash
wfuzz -c -z file,wordlist.txt -u http://target.com/FUZZ -fl 1234 -fw 12 -fr "regex"
```

* `-fl`: filter by length
* `-fw`: filter by word count
* `-fr`: filter by regex

---

## 5. Security & Operational Tips

* Always verify you have permission to test targets
* Use smaller wordlists first to avoid DoS
* Combine with **subfinder** or **httpx** to fuzz only live endpoints
* Save results using `-o` or redirect output to file

---

## 6. Cheat Sheet

```text
# Basic GET fuzzing
wfuzz -c -z file,wordlist.txt -u http://target.com/FUZZ

# POST request fuzzing
wfuzz -c -z file,params.txt -d "username=FUZZ&password=FUZZ" -u http://target.com/login

# Multiple payloads
wfuzz -c -z file,usernames.txt -z file,passwords.txt -d "username=FUZZ1&password=FUZZ2" -u http://target.com/login

# Filter out 404
wfuzz -c -z file,wordlist.txt -u http://target.com/FUZZ -fc 404

# Header fuzzing
wfuzz -c -z file,useragents.txt -H "User-Agent: FUZZ" -u http://target.com

# JSON body fuzzing
wfuzz -c -z file,payloads.txt -d '{"username":"FUZZ","password":"FUZZ"}' -H "Content-Type: application/json" -u http://target.com/api/login

# Advanced filtering
wfuzz -c -z file,wordlist.txt -u http://target.com/FUZZ -fl 1234 -fw 12 -fr "regex"
```

