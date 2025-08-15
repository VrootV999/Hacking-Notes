# Swagger UI

**Type:** API documentation and testing tool
**Focus:** Visualize and interact with OpenAPI/Swagger specifications

---

## 1. Full Feature Overview

* Render OpenAPI (v2/v3) specs into interactive documentation
* Send API requests directly from the UI
* Supports GET, POST, PUT, DELETE, PATCH, OPTIONS
* Explore request parameters, headers, query params, and request body
* Supports authentication: Basic, Bearer, API Key, OAuth2
* Customizable interface for branding or local deployment
* Mock server generation for testing APIs without backend
* Integrates with Swagger Editor for spec creation and validation
* Supports exporting requests to cURL, Postman, or client SDKs
* Can be used in security testing pipelines for recon and fuzzing

---

## 2. Installation & Setup

### Browser Version

* Access: [https://swagger.io/tools/swagger-ui/](https://swagger.io/tools/swagger-ui/)
* No installation needed

### Local Deployment

```bash
git clone https://github.com/swagger-api/swagger-ui.git
cd swagger-ui
npm install
npm run build
# Serve the dist folder using any web server
npx serve dist
```

* Open `http://localhost:8080` to view Swagger UI

### Docker Deployment

```bash
docker pull swaggerapi/swagger-ui
docker run -p 8080:8080 -e SWAGGER_JSON=/foo/swagger.yaml -v $(pwd)/swagger.yaml:/foo/swagger.yaml swaggerapi/swagger-ui
```

---

## 3. Core Usage

### 3.1 Load an OpenAPI Spec

* URL: `http://localhost:8080/?url=https://api.example.com/openapi.json`
* Drag-and-drop local YAML/JSON spec files

### 3.2 Send Requests

* Select endpoint
* Fill query params, path params, headers, and body
* Click **Try it out**
* Inspect response status, headers, and body

---

## 4. Advanced Usage

### 4.1 Authentication

* Configure security schemes in OpenAPI spec
* Provide Bearer tokens, API keys, or OAuth2 in UI

### 4.2 Customization

* Modify `index.html` or `swagger-initializer.js`
* Theme, layout, and branding adjustments
* Integrate into CI/CD pipelines for internal API documentation

### 4.3 Mock Servers

```bash
npm install -g swagger-cli
swagger-cli mock ./swagger.yaml
# Starts a mock API server for testing requests
```

---

## 5. Recon & Offensive Security Tips

* Use Swagger UI to enumerate endpoints for recon
* Export all requests to Postman or Hoppscotch for fuzzing
* Analyze parameter types for injection testing (SQLi, XSS, SSRF)
* Combine with automated scanners like **httpx**, **wfuzz**, or **dalfox**
* Useful in API bug bounty and penetration testing workflows

---

## 6. Cheat Sheet

```text
# Browser access
http://localhost:8080/?url=https://api.example.com/openapi.json

# Local build
git clone https://github.com/swagger-api/swagger-ui.git
cd swagger-ui
npm install
npm run build
npx serve dist

# Docker run
docker run -p 8080:8080 -e SWAGGER_JSON=/foo/swagger.yaml -v $(pwd)/swagger.yaml:/foo/swagger.yaml swaggerapi/swagger-ui

# Authentication
- Add security scheme in OpenAPI spec
- Input Bearer, API Key, OAuth2 token in UI

# Mock server
swagger-cli mock ./swagger.yaml

# Recon & offensive testing
- Export endpoints for Postman/Hoppscotch
- Test all parameters for SQLi, XSS, SSRF
- Integrate with scanners like httpx, wfuzz, dalfox
```

---
