# SoapUI

**Type:** API testing and security analysis tool
**Focus:** Functional, performance, and security testing for SOAP, REST, and GraphQL APIs

---

## 1. Full Feature Overview

* SOAP, REST, and GraphQL request support
* Functional testing with assertions and validations
* Security testing: SQL injection, XML bombs, XSS, SSRF, fuzzing
* Load and performance testing
* Environment and property management (global, project, test case levels)
* Test suites, test cases, and test steps
* Scriptable using Groovy for pre- and post-request actions
* CI/CD integration support (Maven, Jenkins)
* Export/import projects for sharing
* Automated regression testing

---

## 2. Installation & Setup

### Requirements

* Java 8+
* Windows, macOS, Linux

### Steps

1. Download from [https://www.soapui.org/downloads/](https://www.soapui.org/downloads/)
2. Install Java if not already installed
3. Run installer and follow GUI setup
4. Start SoapUI

### Optional: Command-line

```bash
# Run functional tests headlessly
testrunner.sh /path/to/project.xml -s"TestSuite" -c"TestCase"
```

---

## 3. Core Usage

### 3.1 Creating Requests

* REST GET

```http
GET https://api.example.com/users
Authorization: Bearer <token>
```

* SOAP Request (XML example)

```xml
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:usr="http://example.com/user">
   <soapenv:Header/>
   <soapenv:Body>
      <usr:GetUser>
         <usr:id>123</usr:id>
      </usr:GetUser>
   </soapenv:Body>
</soapenv:Envelope>
```

* GraphQL Request

```json
POST https://api.example.com/graphql
Content-Type: application/json

{
  "query": "{ users { id, email } }"
}
```

---

### 3.2 Assertions & Validations

* Status code assertion
* XPath / JSONPath assertions
* Response contains or not contains
* Schema validation

### 3.3 Environments & Properties

* Project-level, TestSuite-level, and TestCase-level properties
* Variable injection: `${#Project#base_url}/users`

---

## 4. Advanced Usage

### 4.1 Security Scans

* SQL Injection
* XSS Injection
* Command Injection
* SSRF & XML External Entity (XXE) testing
* Custom scripts for payload generation using Groovy

### 4.2 Load & Performance Testing

* Define load tests per endpoint
* Set concurrent threads, ramp-up, and iterations
* Generate graphs and performance reports

### 4.3 CI/CD Integration

```bash
# Maven plugin
mvn soapui:test -DprojectFile=/path/to/project.xml -DtestSuite="SuiteName"
```

---

## 5. Recon & Offensive Security Tips

* Use SoapUI for deep API fuzzing and attack simulation
* Combine with Postman/Hoppscotch for recon-driven test automation
* Leverage property expansion for multi-target testing
* Script complex attack chains with Groovy
* Export results to analyze error patterns, which may reveal vulnerabilities

---

## 6. Cheat Sheet

```text
# SOAP request example
POST https://api.example.com/soap
Body: <soapenv:Envelope>...</soapenv:Envelope>

# REST request example
GET https://api.example.com/users
Authorization: Bearer <token>

# GraphQL request
POST https://api.example.com/graphql
Body: { "query": "{ users { id email } }" }

# CLI headless test
testrunner.sh /path/to/project.xml -s"TestSuite" -c"TestCase"

# Environment variable usage
${#Project#base_url}/users

# Security tests
- SQLi, XSS, SSRF, XXE
- Groovy scripting for custom payloads

# Load testing
- Concurrent threads, ramp-up, iterations
- Performance graph reports

# CI/CD integration
mvn soapui:test -DprojectFile=/path/to/project.xml -DtestSuite="SuiteName"
```

---
