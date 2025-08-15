# Insomnia

**Type:** API client & testing tool
**Focus:** REST, GraphQL, gRPC API testing, automation, and debugging

---

## 1. Full Feature Overview

* REST, GraphQL, SOAP, and gRPC support
* Environment variables & templating
* Authentication: Bearer, Basic, OAuth2, API Key
* Request chaining and workflows
* Export requests to cURL, Postman, or code snippets
* Automated testing with test suites & scripts (JavaScript)
* Plugins for extended functionality
* Environment management for multiple APIs/projects
* Workspace sharing for teams
* Supports importing OpenAPI/Swagger specs

---

## 2. Installation & Setup

### Requirements

* Windows, macOS, Linux

### GUI Installation

* Download from [https://insomnia.rest/download](https://insomnia.rest/download)
* Install and launch

### CLI Installation

```bash
# macOS (Homebrew)
brew install --cask insomnia

# Linux (Snap)
sudo snap install insomnia
```

---

## 3. Core Usage

### 3.1 Creating Requests

* REST Example:

```http
GET https://api.example.com/users
Authorization: Bearer <token>
Content-Type: application/json
```

* GraphQL Example:

```json
POST https://api.example.com/graphql
{
  "query": "{ users { id, email } }"
}
```

### 3.2 Environments

* Create global, workspace, and environment variables
* Example: `${{ base_url }}/users`

### 3.3 Authentication

* Set per request or per environment
* OAuth2, Bearer Token, Basic Auth, API Key headers

---

## 4. Advanced Usage

### 4.1 Automated Testing

```javascript
// Example script in Insomnia test tab
const response = pm.response.json();
pm.test("Check user count", () => {
  pm.expect(response.users.length).to.be.above(0);
});
```

### 4.2 Workflows

* Request chaining using environment variables
* Conditional request execution based on previous response

### 4.3 Plugins

* Install via Preferences → Plugins
* Examples: JSON schema validation, auto-mocking

### 4.4 Import/Export

* OpenAPI/Swagger import
* Export workspace as JSON for sharing

---

## 5. Recon & Offensive Security Tips

* Use Insomnia for API endpoint enumeration
* Combine with automated fuzzing tools like **wfuzz**, **dalfox**, **arjun**
* Use environment variables for multi-target testing
* Script payloads for SQLi, XSS, SSRF tests
* Export requests for integration into CI/CD or other testing pipelines

---

## 6. Cheat Sheet

```text
# REST request
GET https://api.example.com/users
Authorization: Bearer <token>

# GraphQL request
POST https://api.example.com/graphql
Body: { "query": "{ users { id, email } }" }

# CLI install
brew install --cask insomnia      # macOS
sudo snap install insomnia        # Linux

# Environment variable
${{ base_url }}/users

# Automated test script
const response = pm.response.json();
pm.test("Check user count", () => { pm.expect(response.users.length).to.be.above(0); });

# Plugins
- JSON schema validation
- Auto-mocking

# Recon/offensive tips
- Endpoint enumeration
- Fuzzing with wfuzz/dalfox/arjun
- Multi-target testing via env variables
- SQLi/XSS/SSRF payload scripting
```

---
