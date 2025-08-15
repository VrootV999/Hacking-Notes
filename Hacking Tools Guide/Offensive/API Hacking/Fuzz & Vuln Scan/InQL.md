# inql

**Type:** GraphQL security scanner and recon tool
**Focus:** Complete GraphQL enumeration, introspection, vulnerability detection

---

## 1. Full Feature Overview

* Schema discovery via introspection
* Query, mutation, and type enumeration
* Sensitive data exposure detection
* Over-fetching and parameter discovery
* Authentication support (Bearer, cookies, custom headers)
* Custom introspection queries
* Wordlist and payload testing
* JSON output for automation
* Silent mode for scripts
* Integration with fuzzers: dalfox, wfuzz, arjun
* Recon workflow: subfinder + httpx pipelines

---

## 2. Installation & Setup

### Requirements

* Python 3.6+
* pip or pip3

### Install via pip

```bash
pip install inql
```

### Verify

```bash
inql --version
```

### Optional Dependencies

* `requests` for HTTP requests
* `colorama` for CLI highlighting

---

## 3. CLI Usage (Exhaustive)

```bash
inql -u <endpoint> [OPTIONS]
```

### Common Options

| Option   | Description                   |
| -------- | ----------------------------- |
| -u       | Target GraphQL endpoint       |
| -q       | Specific query/mutation       |
| -i       | Custom introspection JSON     |
| -w       | Query wordlist                |
| -p       | Custom payload file           |
| -H       | Custom headers                |
| -C       | Cookies                       |
| --vulns  | Automatic vulnerability check |
| -o       | Output file (JSON/CSV)        |
| --silent | Silent mode                   |
| --json   | JSON output                   |
| -v       | Verbose output                |

---

## 4. Examples (All Cases)

### Basic introspection

```bash
inql -u https://target.com/graphql
```

### Save schema

```bash
inql -u https://target.com/graphql -o schema.json
```

### Authentication

```bash
# Bearer token
inql -u https://target.com/graphql -H "Authorization: Bearer <token>"

# Cookies
inql -u https://target.com/graphql -C "session=<cookie>"
```

### Custom introspection

```bash
inql -u https://target.com/graphql -i custom.json
```

### Vulnerability detection

```bash
inql -u https://target.com/graphql --vulns
```

### Wordlist testing

```bash
inql -u https://target.com/graphql -w queries.txt
```

### Custom payloads

```bash
inql -u https://target.com/graphql -p payloads.txt
```

### Automation / silent JSON

```bash
inql -u https://target.com/graphql --silent --json -o output.json
```

### Integration in pipeline

```bash
subfinder -d example.com -silent | httpx -silent -path /graphql | xargs -I {} inql -u {}
```

---

## 5. Operational & Security Notes

* Only test authorized APIs
* Introspection can leak sensitive fields
* JSON output is ideal for automated vulnerability scanning
* Silent mode avoids log clutter in pipelines
* Combine with **graphqlmap** for vulnerability scanning and **GraphQL Voyager** for visualization
* Adjust request rate to avoid WAF or API throttling
* Edge tip: feed inql output to dalfox for parameter fuzzing

---

