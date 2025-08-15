# Hoppscotch

**Type:** API testing and reconnaissance tool
**Focus:** Lightweight, browser-based API client for REST, GraphQL, WebSocket, and Server-Sent Events

---

## 1. Full Feature Overview

* Send HTTP requests (GET, POST, PUT, DELETE, PATCH, OPTIONS)
* GraphQL queries and mutations
* WebSocket and SSE connections
* Environment and variable management
* Authentication support: Basic, Bearer, API keys, OAuth 2.0
* Request history and collections
* Export and import requests/collections (JSON)
* Custom headers, cookies, and body types (JSON, form-data, URL-encoded)
* CLI tool available via `hoppscotch-cli`
* Integration with automated scripts for pipelines
* Browser-based, lightweight alternative to Postman

---

## 2. Installation & Setup

### Browser Version

* Visit: [https://hoppscotch.io](https://hoppscotch.io)
* No installation needed

### Self-host / Local Installation

```bash
git clone https://github.com/hoppscotch/hoppscotch.git
cd hoppscotch
npm install
npm run dev  # starts local server
```

* Access locally: `http://localhost:3000`

### CLI Version

```bash
npm install -g hoppscotch-cli
hoppscotch --help
```

---

## 3. Core Usage

### 3.1 REST API Request

```http
GET https://api.example.com/users
Authorization: Bearer <token>
```

```http
POST https://api.example.com/login
Content-Type: application/json

{
  "username": "admin",
  "password": "password123"
}
```

### 3.2 GraphQL

```json
POST https://api.example.com/graphql
Content-Type: application/json

{
  "query": "{ users { id, email } }"
}
```

### 3.3 WebSocket

```javascript
ws://example.com/socket
# Send messages and receive responses interactively
```

---

## 4. Advanced Usage

### 4.1 Environment & Variables

* Define environment variables: `{{base_url}}`
* Switch between multiple environments (dev, staging, prod)

### 4.2 Authentication

* Bearer, API key, Basic Auth, OAuth 2.0 token flows
* Supports dynamic token injection using variables

### 4.3 Collections

* Organize requests by projects or targets
* Export and import collections as JSON
* Run sequences of requests for chained testing

### 4.4 CLI Automation

```bash
hoppscotch send --method GET --url https://api.example.com/users --header "Authorization: Bearer <token>"
```

---

## 5. Recon & Offensive Security Tips

* Lightweight replacement for Postman in recon pipelines
* Combine with **Wayback Machine** or **RapidAPI** to discover hidden endpoints
* Use variable environments for rapid pivoting between targets
* Export collections and feed into automated fuzzing pipelines
* Browser-based real-time testing for XSS, SSRF, or API misconfigurations
* Can test GraphQL endpoints interactively without setup overhead

---

## 6. Cheat Sheet

```text
# Browser: live testing
https://hoppscotch.io

# Local installation
git clone https://github.com/hoppscotch/hoppscotch.git
cd hoppscotch
npm install
npm run dev
# Open: http://localhost:3000

# CLI usage
npm install -g hoppscotch-cli
hoppscotch send --method GET --url https://api.example.com/users --header "Authorization: Bearer <token>"

# Environment variable
GET {{base_url}}/users

# GraphQL query
POST {{base_url}}/graphql
Body: { "query": "{ users { id email } }" }

# Export/import collections for automation
```

---
