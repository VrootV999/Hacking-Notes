# Postman

**Type:** API development and testing tool
**Focus:** API exploration, testing, automation, and reconnaissance

---

## 1. Full Feature Overview

* API request crafting (GET, POST, PUT, DELETE, PATCH, OPTIONS)
* Support for REST, GraphQL, SOAP, and WebSocket APIs
* Environment and variable management
* Collections for organizing requests
* Automated testing with scripts (pre-request and test scripts)
* Authorization support: Basic, Bearer, OAuth 1/2, API keys, Digest
* Response validation, status code assertions, and JSON schema validation
* Export and import collections for sharing
* Monitor APIs for uptime and response correctness
* CLI tool: `newman` for running collections in pipelines
* Integration with RapidAPI for discovering endpoints

---

## 2. Installation & Setup

### Requirements

* Windows, macOS, Linux
* Node.js (for Newman CLI)

### Postman Desktop

* Download from [https://www.postman.com/downloads/](https://www.postman.com/downloads/)
* Install and open the GUI

### Newman CLI Installation

```bash
npm install -g newman
```

### Verify Installation

```bash
newman -v
```

---

## 3. Core Usage

### 3.1 Sending a Request

* REST GET example:

```http
GET https://api.example.com/users
Authorization: Bearer <token>
```

* REST POST example:

```http
POST https://api.example.com/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

* GraphQL query example:

```json
POST https://api.example.com/graphql
Content-Type: application/json

{
  "query": "{ users { id, email } }"
}
```

---

### 3.2 Using Environments & Variables

```json
// Environment JSON
{
  "id": "env1",
  "name": "TestingEnv",
  "values": [
    {"key": "base_url", "value": "https://api.example.com"}
  ]
}
```

```http
GET {{base_url}}/users
```

---

## 4. Advanced Usage

### 4.1 Authorization Methods

* Bearer token: `Authorization: Bearer <token>`
* API Key: `x-api-key: <key>`
* OAuth 2.0: Automated token fetching

### 4.2 Pre-request Scripts

* Used to dynamically generate headers or tokens

```javascript
pm.environment.set("authToken", "Bearer " + generateToken());
```

### 4.3 Test Scripts

* Validate responses

```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains user email", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.users[0]).to.have.property("email");
});
```

### 4.4 Running Collections via CLI (Newman)

```bash
newman run collection.json -e environment.json --reporters cli,json,html
```

---

## 5. Recon & Offensive Security Tips

* Use Postman to explore undocumented endpoints
* Combine with RapidAPI and Wayback Machine to discover APIs
* Export API collections and automate fuzzing using Newman + wfuzz/dalfox
* Use environment variables for rapid pivoting between targets
* Chain requests to test chained vulnerabilities (auth bypass, chained GraphQL queries)
* Postman’s console provides request/response debugging for subtle security issues

---

## 6. Cheat Sheet

```text
# Install Newman CLI
npm install -g newman

# Send GET request
GET https://api.example.com/users
Authorization: Bearer <token>

# Send POST request with JSON
POST https://api.example.com/login
Content-Type: application/json
Body: { "username": "admin", "password": "password123" }

# Use environment variables
GET {{base_url}}/users

# Pre-request scripts
pm.environment.set("authToken", "Bearer " + generateToken());

# Test scripts
pm.test("Status code is 200", function () { pm.response.to.have.status(200); });

# Run collection via CLI
newman run collection.json -e environment.json --reporters cli,json,html

# Combine with recon workflow
# 1. Discover endpoints via RapidAPI or Wayback Machine
# 2. Import into Postman
# 3. Test, automate, and validate responses
```

---
