# Wayback Machine for API Recon

**Type**: Information Gathering, Reconnaissance
**Focus**: **The Wayback Machine** (from **archive.org**) is a tool that allows users to view archived versions of websites. For security professionals, it can be an invaluable resource for discovering **old versions** of websites, **API endpoints**, and **documentation** that may have been inadvertently exposed or are no longer publicly available but may still be exploitable.

---

## 1. Overview

* **Purpose**: The Wayback Machine helps penetration testers find previously public **API endpoints** and **sensitive information** that might have been removed from the live version of a website or API.
* **Key Features**:

  * Archive snapshots of websites, APIs, and related assets.
  * Useful for discovering old **API documentation** and **keys**.
  * You can search by specific dates and access historical versions of a site.

---

## 2. Usage and Examples

### 2.1 Searching for Archived API Endpoints

If you're looking for old versions of an API documentation that may reveal sensitive endpoints:

1. Visit the **Wayback Machine**: [archive.org/web](https://archive.org/web/)
2. Enter the target website's URL.
3. Browse through the available archived snapshots by selecting a specific date.
4. Look for any exposed **API documentation** or endpoints that could give insight into the internal workings of the API.

For example, you might search for:

```
https://example.com/api/docs
```

If exposed in the past, it could contain valuable information like authentication methods, routes, and parameters.

---

## 3. Advanced Techniques

### 3.1 API Key Discovery

Sometimes, old versions of **API documentation** might still be visible, revealing the keys or tokens that were exposed earlier. You can automate or script checks to look for:

```bash
archive.org "API_KEY" "API_SECRET"
```

### 3.2 Using the Wayback Machine for API Version Changes

Older API versions may no longer be accessible publicly but can still be found via the Wayback Machine. Look for **changes in API versions** that may expose vulnerabilities or require security updates.

---


