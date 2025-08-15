# GraphQL Voyager

**Type:** GraphQL schema visualization and exploration tool
**Focus:** Full mapping of GraphQL API structure

---

## 1. Full Feature Overview

* Interactive graph of types, queries, mutations
* Visualization of interfaces, unions, enums, scalars
* Self-hosting for offline use
* Multiple schema support
* Offline JSON schema visualization
* Safe read-only exploration (no query execution)
* Integration with inql / graphqlmap pipelines

---

## 2. Installation & Setup

### Requirements

* Node.js 12+
* npm

### Quick Run via npx

```bash
npx graphql-voyager
```

### Clone & Host Locally

```bash
git clone https://github.com/APIs-guru/graphql-voyager.git
cd graphql-voyager
npm install
npm start
```

---

## 3. CLI & Usage

### Live Endpoint

```bash
npx graphql-voyager -e https://target.com/graphql
```

### Schema JSON File

```bash
npx graphql-voyager -s schema.json
```

### Multiple Schema Files

```bash
npx graphql-voyager -s schema1.json schema2.json
```

### Self-host Locally

* Start server: `npm start`
* Open browser: `http://localhost:3000`

---

## 4. Operational Tips

* Interactive exploration allows deep understanding of type relationships
* Combine with inql or graphqlmap outputs for full recon
* Useful for crafting targeted queries or discovering sensitive endpoints
* Safe for offline usage, prevents sending data to third-party servers
* Helps visualize complex API dependencies before pentesting

---

## 5. Cheat Sheet

```text
# Live GraphQL endpoint
npx graphql-voyager -e https://target.com/graphql

# Schema from JSON file
npx graphql-voyager -s schema.json

# Multiple schemas
npx graphql-voyager -s schema1.json schema2.json

# Self-host locally
git clone https://github.com/APIs-guru/graphql-voyager.git
cd graphql-voyager
npm install
npm start

# Combine with inql
inql -u https://target.com/graphql -o schema.json
npx graphql-voyager -s schema.json
```

---
