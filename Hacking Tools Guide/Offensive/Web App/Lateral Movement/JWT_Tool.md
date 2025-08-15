# JWT_tool

**Type:** JSON Web Token (JWT) Security / Penetration Testing Tool
**Focus:** Testing JWTs for vulnerabilities like weak signing, algorithm tampering, and token forging

---

## 1. Installation & Setup

### Requirements

* Python 3.6+ (`python3 --version`)
* Pip package manager
* Git for cloning repository

### Installation Steps

1. **Clone Repository**

```bash
git clone https://github.com/ticarpi/jwt_tool.git
cd jwt_tool
```

2. **Install Dependencies**

```bash
pip3 install -r requirements.txt
```

3. **Verify Installation**

```bash
python3 jwt_tool.py -h
```

* Displays help menu to confirm installation

---

## 2. Supported Workflows

* **Decode JWTs** to analyze payload and headers
* **Brute-force secret keys** for HMAC-signed JWTs
* **Test algorithm tampering** (e.g., `HS256` → `none`)
* **Forge tokens** to escalate privileges or bypass authentication
* **Inspect token expiration and claims**

---

## 3. Command-Line Usage

### Decode a JWT

```bash
python3 jwt_tool.py -t <JWT_TOKEN> -d
```

* `-t` specifies token
* `-d` decodes the token to show header and payload

### Bruteforce Secret (HMAC)

```bash
python3 jwt_tool.py -t <JWT_TOKEN> -b -w wordlist.txt
```

* `-b` enables brute force
* `-w` specifies path to wordlist
* Automatically detects HMAC algorithm (`HS256`, `HS384`, `HS512`)

### Test None Algorithm Vulnerability

```bash
python3 jwt_tool.py -t <JWT_TOKEN> --none
```

* Attempts to bypass signature verification by setting algorithm to `none`

### Forge JWT

```bash
python3 jwt_tool.py -f -p '{"role":"admin"}' -s mysecretkey
```

* `-f` enables forging
* `-p` specifies new payload as JSON
* `-s` specifies secret key

### Algorithm Change Attack

```bash
python3 jwt_tool.py -t <JWT_TOKEN> --alg "RS256" -k public.pem
```

* Changes algorithm (HS→RS or RS→HS) to test signature bypass

---

## 4. Workflow (Professional)

1. **Capture JWT**

   * Intercept using BurpSuite or Proxy
2. **Decode JWT**

   ```bash
   python3 jwt_tool.py -t <JWT_TOKEN> -d
   ```
3. **Analyze Claims**

   * Check `iss`, `exp`, `role`, `aud` fields for weaknesses
4. **Test Algorithm Vulnerabilities**

   ```bash
   python3 jwt_tool.py -t <JWT_TOKEN> --none
   ```
5. **Attempt Secret Key Bruteforce**

   ```bash
   python3 jwt_tool.py -t <JWT_TOKEN> -b -w wordlist.txt
   ```
6. **Forge Token**

   * Modify payload for privilege escalation or test access control bypass

---

## 5. Advanced Features

* **Support for Multiple Algorithms**

  * HS256, HS384, HS512, RS256, RS384, RS512
* **Dictionary Attack**

  * Wordlist-based secret key testing
* **Custom Payload Injection**

  * Craft payloads to bypass RBAC, escalate roles, or manipulate claims
* **Integration with BurpSuite / Proxies**

  * Intercept JWTs from Authorization headers or cookies

---

## 6. Tips, Tricks & Best Practices

* Always decode token first to understand payload and algorithm
* Use SecLists or custom wordlists for secret brute force
* Test `alg` manipulation carefully to avoid alerting WAFs
* Combine JWT\_tool findings with **Autorize** for full access control testing
* Verify token forgery on staging environments before testing production

---

## 7. Quick Reference Cheat Sheet

```text
# Decode JWT
python3 jwt_tool.py -t <JWT_TOKEN> -d

# Brute-force HMAC secret
python3 jwt_tool.py -t <JWT_TOKEN> -b -w wordlist.txt

# Test 'none' algorithm bypass
python3 jwt_tool.py -t <JWT_TOKEN> --none

# Forge JWT with new payload
python3 jwt_tool.py -f -p '{"role":"admin"}' -s mysecretkey

# Algorithm change attack (HS->RS)
python3 jwt_tool.py -t <JWT_TOKEN> --alg "RS256" -k public.pem
```

---
