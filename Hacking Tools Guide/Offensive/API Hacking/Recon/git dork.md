# Git Dorking

**Type**: Reconnaissance, Information Gathering
**Focus**: **Git Dorking** is a technique used to search for sensitive data and credentials exposed on **GitHub** repositories by using **Google Dorking** queries. Attackers or penetration testers use this method to discover misconfigured Git repositories that may contain **API keys**, **database credentials**, **source code**, and other sensitive files.

---

## 1. Overview

* **Purpose**: Git Dorking enables attackers to identify **exposed secrets**, such as API keys, private keys, and authentication tokens that are accidentally pushed to public Git repositories.
* **Key Features**:

  * Uses Google search to find exposed sensitive data in repositories.
  * **GitHub** is a primary target, but this method can be applied to other platforms like **GitLab**, **Bitbucket**, etc.
  * Allows finding **configuration files** such as `.env`, `config.php`, and `secrets.json`.

---

## 2. Usage and Examples

### 2.1 Common Git Dorks

#### 2.1.1 Finding exposed **AWS credentials** in Git repositories

```bash
site:github.com "AWS_SECRET_ACCESS_KEY" "AWS_ACCESS_KEY_ID"
```

#### 2.1.2 Finding **Google API keys** in repositories

```bash
site:github.com "AIza" "google"
```

#### 2.1.3 Searching for **SSH private keys** in GitHub repositories

```bash
site:github.com "-----BEGIN RSA PRIVATE KEY-----"
```

#### 2.1.4 Searching for **OAuth tokens** in public repositories

```bash
site:github.com "oauth_token" "client_secret"
```

#### 2.1.5 Finding **.env files** which often contain sensitive data

```bash
site:github.com "env" ".env"
```

---

## 3. Advanced Techniques

### 3.1 Automating Git Dorking with Tools

Several tools can automate Git Dorking by running predefined Google Dork queries to search for sensitive data.

* **GitDorker**: A tool that automates searching for exposed secrets in GitHub repositories using Git Dorking.

  * GitHub: [GitDorker](https://github.com/obheda12/GitDorker)

### 3.2 Using API Keys and Credentials

If sensitive information such as API keys is exposed, attackers can often use them to gain unauthorized access to APIs, databases, or other services, depending on the keys' privileges.

---


