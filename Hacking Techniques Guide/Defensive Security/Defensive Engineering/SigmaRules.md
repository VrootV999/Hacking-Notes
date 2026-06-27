# Sigma Rules — Defensive Engineering Master Guide

## Table of Contents
1. [What is Sigma?](#what-is-sigma)
2. [Sigma vs. YARA](#sigma-vs-yara)
3. [Core Rule Anatomy](#core-rule-anatomy)
4. [Rule Sections in Depth](#rule-sections-in-depth)
   - [title, id, status, description](#title-id-status-description)
   - [references, author, date](#references-author-date)
   - [logsource](#logsource)
   - [detection](#detection)
   - [falsepositives, level, tags](#falsepositives-level-tags)
5. [Sigma Taxonomy](#sigma-taxonomy)
   - [category, product, service](#category-product-service)
   - [Full Logsource Reference](#full-logsource-reference-table)
6. [Detection Modifiers](#detection-modifiers)
   - [contains, startswith, endswith](#contains-startswith-endswith)
   - [all, base64, base64offset, utf16le](#all-base64-base64offset-utf16le)
   - [re, cidr, lt, gt, le, ge](#re-cidr-lt-gt-le-ge)
   - [Modifier Combinations](#modifier-combinations)
7. [Detection Expression Types](#detection-expression-types)
   - [string matching](#1-string-matching)
   - [list matching](#2-list-matching)
   - [keyword matching](#3-keyword-matching)
   - [numeric matching](#4-numeric-matching)
   - [IP CIDR matching](#5-ip-cidr-matching)
   - [regular expression](#6-regular-expression)
   - [wildcard matching](#7-wildcard-matching)
   - [map/field presence](#8-mapfield-presence)
8. [Condition Logic](#condition-logic)
   - [selection, filter](#selection-and-filter)
   - [1 of, all of](#1-of-all-of)
   - [negation](#negation)
   - [aggregation count](#aggregation-count)
   - [temporal proximity](#temporal-proximity)
   - [value aggregation](#value-aggregation)
   - [near](#near)
9. [Sigma Specification v1 vs v2](#sigma-specification-v1-vs-v2)
   - [Sigma v2 Features](#sigma-v2-features)
10. [Sigma Correlation Rules](#sigma-correlation-rules)
    - [event_count](#event_count)
    - [value_count](#value_count)
    - [temporal](#temporal)
    - [ordered_temporal](#ordered_temporal)
11. [Sigma Test Format](#sigma-test-format)
12. [Log Source Deep Dives](#log-source-deep-dives)
    - [Windows Event Log (Security)](#windows-security-event-log)
    - [Windows Event Log (Sysmon)](#windows-sysmon)
    - [Windows PowerShell](#windows-powershell)
    - [Windows Security Audit Categories](#windows-security-audit-categories)
    - [Linux Auditd](#linux-auditd)
    - [Linux Syslog](#linux-syslog)
    - [macOS Unified Log](#macos-unified-log)
    - [Network (Zeek, Suricata)](#network-zeek-suricata)
    - [Cloud (AWS CloudTrail, Azure, GCP)](#cloud-aws-cloudtrail-azure-gcp)
13. [Sigma Pipelines](#sigma-pipelines)
    - [Field Mapping](#field-mapping)
    - [Field Name Transformations](#field-name-transformations)
    - [Log Source Transformations](#log-source-transformations)
    - [Built-in Pipelines](#built-in-pipelines)
14. [pySigma — The Modern Converter](#pysigma--the-modern-converter)
    - [Installation](#installation)
    - [Basic Usage](#basic-usage)
    - [Plugin Architecture](#plugin-architecture)
    - [Backend Development](#backend-development)
    - [Processing Pipelines](#processing-pipelines-in-pysigma)
15. [Backend Reference](#backend-reference)
    - [Elasticsearch / Elastic Security](#elasticsearch--elastic-security)
    - [Splunk](#splunk)
    - [QRadar / AQL](#qradar--aql)
    - [Microsoft Sentinel / Azure](#microsoft-sentinel--azure)
    - [Chronicle / BigQuery](#chronicle--bigquery)
    - [Loki (Grafana)](#loki-grafana)
    - [Logpoint](#logpoint)
    - [ArcSight](#arcsight)
    - [NetWitness](#netwitness)
    - [SoumniBot](#soumnibot)
    - [Elasticsearch Query DSL](#elasticsearch-query-dsl)
    - [OpenSearch](#opensearch)
    - [CrowdStrike](#crowdstrike)
    - [Splunk Data Model](#splunk-data-model)
    - [Splunk DataSource](#splunk-datasource)
    - [PowerShell](#powershell)
16. [Rule Development Lifecycle](#rule-development-lifecycle)
    - [Identify Gap](#1-identify-detection-gap)
    - [Research TTP](#2-research-ttp)
    - [Draft Rule](#3-draft-rule)
    - [Validate with Tests](#4-validate-with-tests)
    - [Convert & Test in SIEM](#5-convert--test-in-siem)
    - [Tune & Deploy](#6-tune--deploy)
    - [Monitor & Maintain](#7-monitor--maintain)
17. [Real-World Rule Examples](#real-world-rule-examples)
    - [PowerShell Encoded Command](#1-powershell-encoded-command-execution)
    - [Mimikatz Detection](#2-mimikatz-detection-via-event-id-7)
    - [Cobalt Strike Named Pipe](#3-cobalt-strike-named-pipe)
    - [Ransomware — Mass File Extensions](#4-ransomware---mass-file-extension-renaming)
    - [Pass-the-Hash](#5-pass-the-hash-detection)
    - [DCSync Attack](#6-dcsync-attack)
    - [WMI Persistence](#7-wmi-persistence)
    - [Suspicious Service Installation](#8-suspicious-service-installation)
    - [DNS Tunneling](#9-dns-tunneling)
    - [New User Account Created](#10-new-user-account-created)
    - [Logon from Unusual Country](#11-logon-from-unusual-country)
    - [Disabled Security Logging](#12-attempt-to-disable-security-logging)
    - [Process Injection (Sysmon EID 8)](#13-process-injection-sysmon-eid-8)
    - [Outbound RDP Connection](#14-outbound-rdp-connection)
    - [Azure Key Vault Access from Unusual IP](#15-azure-key-vault-access-from-unusual-ip)
    - [AWS IAM Privilege Escalation](#16-aws-iam-privilege-escalation)
    - [Linux SSH Brute Force](#17-linux-ssh-brute-force)
    - [Kubernetes Container to Cluster Admin](#18-kubernetes-container-to-cluster-admin)
    - [Web Shell Detection via Logs](#19-web-shell-detection-via-logs)
    - [Disabled Antivirus](#20-attempt-to-disable-antivirus)
18. [MITRE ATT&CK Mapping](#mitre-attck-mapping)
    - [Common TTPs by Sigma Rule Type](#common-ttps-by-sigma-rule-type)
19. [Sigma Rule Management at Scale](#sigma-rule-management-at-scale)
    - [Repository Structure](#repository-structure)
    - [Naming Conventions](#naming-conventions)
    - [Versioning](#versioning)
    - [Quality Gates](#quality-gates)
20. [Performance Optimization](#performance-optimization)
    - [Field Selection](#field-selection)
    - [Modifier Choice](#modifier-choice)
    - [Condition Structure](#condition-structure)
    - [Logsource Precision](#logsource-precision)
    - [Aggregation Performance](#aggregation-performance)
21. [Common Pitfalls & Anti-Patterns](#common-pitfalls--anti-patterns)
22. [Testing & Validation](#testing--validation)
    - [Test Format Specification](#test-format-specification)
    - [Automated Testing](#automated-testing)
23. [Sigma OSS Repositories & Feeds](#sigma-oss-repositories--feeds)
24. [Integration Ecosystem](#integration-ecosystem)
25. [Sigma CLI Reference](#sigma-cli-reference)
    - [sigmac — Legacy Tool](#sigmac--legacy-tool)
    - [Sigma CLI (Modern)](#sigma-cli-modern)
26. [Appendix A: Quick Reference](#appendix-a-quick-reference)
27. [Appendix B: Logsource Quick Reference](#appendix-b-logsource-quick-reference)
28. [References & Further Reading](#references--further-reading)

---

## What is Sigma?

Sigma is a **generic and open signature format** for log events. Created by Florian Roth (Neo23x0) and Thomas Patzke, it allows detection engineers to write detection rules **once** and convert them to any SIEM or log management platform.

Sigma is to **log events** what YARA is to **files**.

**Core Philosophy:** *"Write once, detect everywhere."*

```yaml
# One Sigma rule → any SIEM
```
```yaml
# → Elasticsearch query
# → Splunk SPL search
# → QRadar AQL
# → Microsoft Sentinel KQL
# → ArcSight ESM filter
# → LogPoint search
# → AWS Athena / BigQuery SQL
# → PowerShell script
```

**Why Sigma in Defensive Engineering?**
- **Vendor-agnostic detection** — decouple detection logic from SIEM platform
- **Community-driven** — 2000+ rules in the official repository, shared across organizations
- **MITRE ATT&CK aligned** — every rule maps to TTPs
- **Granular logsource taxonomy** — precisely target specific log types (Windows Security, Sysmon, PowerShell, auditd, etc.)
- **Correlation rules** — detect multi-step attacks (Sigma v2)
- **Testable** — rules include test cases with expected matches/non-matches
- **Pipeline transforms** — adapt to field naming differences across log shippers (Winlogbeat, Sysmon-ng, etc.)

---

## Sigma vs. YARA

| Dimension | Sigma | YARA |
|---|---|---|
| **Target** | Log events (text/structured) | Files, processes, memory (binary) |
| **Format** | YAML | YARA DSL (custom syntax) |
| **Output** | SIEM queries (SPL, KQL, Lucene, etc.) | Pattern matching engine |
| **Analogy** | Snort rules for logs | AV signatures for binaries |
| **Use case** | Detection in SIEM, EDR, data lakes | Malware identification, IR triage |
| **Correlation** | Multi-event correlation (v2) | Single-file scan only |
| **Community** | ~3000+ rules (official repo) | ~5000+ rules (YARA-Rules, others) |
| **Fields** | Structured event fields | Byte offsets, module attributes |
| **Conversion** | `sigmac` / `pySigma` backends | N/A (native engine) |
| **Tests** | Inline test cases in YAML | External testing frameworks |
| **Version** | v1 (stable), v2 (emerging) | 4.x (stable) |

**Complementary relationship:**
- Sigma → detects *behavior* (what happened) in logs
- YARA → detects *artifacts* (what file/memory) on disk
- Use both: YARA on endpoints, Sigma in SIEM

---

## Core Rule Anatomy

```yaml
title: PowerShell Encoded Command Execution
id: f0f9e3b9-3e9f-4a9f-9f9f-9f9f9f9f9f9f
status: stable
description: Detects execution of encoded PowerShell commands
references:
    - https://attack.mitre.org/techniques/T1059/001/
    - https://docs.microsoft.com/en-us/powershell/
author: Sigma Rule Contributor
date: 2020/01/15
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1059.001
    - attack.defense_evasion
    - attack.t1027
    - windows
logsource:
    category: process_creation
    product: windows
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|base64offset:
            - ' -e '
            - ' -en '
            - ' -enc '
            - ' -enco'
    condition: selection
falsepositives:
    - Administrative scripts using encoded commands
level: high
```

---

## Rule Sections in Depth

### title, id, status, description

```yaml
title: Write Once, Detect Everywhere        # Human-readable, unique name
id: b2a5b3c4-d5e6-4789-8f01-234567890abc   # UUID v4 — globally unique identifier
status: stable                                # stable | test | experimental | deprecated | unsupported
description: |
    A multi-line description
    explaining what this rule detects,
    the technique, and context.
```

**Status values:**
| Status | Meaning | Use |
|---|---|---|
| `stable` | Production-ready, well-tested | Deployed and monitored |
| `test` | Needs validation, recently written | Testing pipeline, not in production |
| `experimental` | Exploratory, high FP rate likely | Research/hunting only |
| `deprecated` | Superseded or obsolete | Keep for reference, not for deployment |
| `unsupported` | Cannot be converted for technical reasons | Documented but unusable |

### references, author, date

```yaml
references:
    - https://attack.mitre.org/techniques/T1059/001/
    - https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1059.001/T1059.001.md
    - https://docs.microsoft.com/en-us/powershell/
    - https://twitter.com/i/web/status/1234567890
    - Internal case IR-2024-001
author:
    - Name Surname (org)
    - @twitter_handle
    - Organization Name
date: 2020/01/15              # YYYY/MM/DD
modified: 2024/06/27           # YYYY/MM/DD
```

### logsource

The `logsource` section selects which log types this rule applies to. It's a **pre-filter** — if the log source doesn't match, the rule is skipped entirely.

```yaml
logsource:
    category: process_creation     # Broad category
    product: windows               # OS/product level
    service: sysmon                # Specific service (optional)
    definition: 'Requirements: Sysmon EID 1 must be enabled'
```

**logsource fields (hierarchical from broad to specific):**

```
category       → process_creation, file_event, registry_event, network_connection, dns, ...
  product      → windows, linux, macos, aws, azure, gcp, office, network, ...
    service    → sysmon, security, powershell, auditd, iis, apache, zeek, suricata, ...
```

**Special categories:**
- `category: process_creation` — Process creation events (Sysmon EID 1, Security EID 4688)
- `category: file_event` — File operations (Sysmon EID 11, auditd)
- `category: registry_event` — Registry access (Sysmon EID 12/13/14)
- `category: network_connection` — Network events (Sysmon EID 3, Network logs)
- `category: image_load` — Module load events (Sysmon EID 7)
- `category: process_access` — Process access (Sysmon EID 10)
- `category: dns` — DNS queries (Sysmon EID 22, Zeek DNS, Windows DNS)
- `category: firewall` — Firewall allow/block events
- `category: web` — Web server logs (IIS, Apache, Nginx)
- `category: audit` — General audit events
- `category: authentication` — Logon/logoff events
- `category: application` — Application-specific logs
- `category: certificate` — Certificate services events

### detection

The heart of the rule. Defines **what** to match.

```yaml
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|base64offset: '-enc '
    filter:
        CommandLine|contains:
            - 'Write-Host'
            - 'Get-Help'
    condition: selection and not filter
```

**Structure:**
- Named **maps** (arbitrary names like `selection`, `filter`, `keywords`) containing field-value pairs
- The **condition** combines these maps with boolean logic
- Items within a map are implicitly **AND**-ed
- Multiple values per field are implicitly **OR**-ed
- Underscore-prefixed maps (`_filter`) are treated as **exclusion filters** automatically

### falsepositives, level, tags

```yaml
falsepositives:
    - Administrative activity
    - 'Some legitimate tool: ProcessHacker'
    - Penetration testing engagement
    - Unknown (limited data)
level: high                          # critical | high | medium | low | informational
tags:
    - attack.execution               # MITRE ATT&CK tactic (lowercase)
    - attack.t1059.001               # MITRE ATT&CK technique ID
    - attack.defense_evasion         # Multiple tactics per rule
    - attack.t1027
    - detection.threat_hunting       # Custom tags
    - use_case.active_directory      # Custom use-case tags
    - os.windows                     # OS tag
```

**Level meaning (guidelines):**
| Level | Criteria |
|---|---|
| `critical` | Immediate threat to infrastructure (ransomware, C2, credential theft) |
| `high` | Clear malicious behavior with low FP rate |
| `medium` | Suspicious behavior, may need tuning or correlation |
| `low` | Informational, hunting, possible reconnaissance |
| `informational` | Notable but not suspicious events |

---

## Sigma Taxonomy

### category, product, service

The full logsource hierarchy:

```
category: process_creation
  ├── product: windows
  │     ├── service: sysmon        (Sysmon EID 1)
  │     ├── service: security      (Windows Security EID 4688)
  │     └── service: powershell    (PowerShell EID 400/800)
  ├── product: linux
  │     └── service: auditd        (auditd execve)
  └── product: macos
        └── service: esf           (Endpoint Security Framework)

category: file_event
  ├── product: windows
  │     ├── service: sysmon        (Sysmon EID 11)
  │     └── service: security      (Windows Security EID 4663)
  └── product: linux
        └── service: auditd

category: registry_event
  └── product: windows
        ├── service: sysmon        (Sysmon EID 12, 13, 14)
        └── service: security      (Windows Security EID 4657)

category: network_connection
  ├── product: windows
  │     ├── service: sysmon        (Sysmon EID 3)
  │     ├── service: firewall      (Windows Firewall EID 5157)
  │     └── service: security      (Security EID 5156)
  ├── product: linux
  │     └── service: auditd
  └── product: network
        ├── service: zeek
        ├── service: suricata
        └── service: iptables

category: image_load
  └── product: windows
        └── service: sysmon        (Sysmon EID 7)

category: process_access
  └── product: windows
        └── service: sysmon        (Sysmon EID 10)

category: dns
  ├── product: windows
  │     └── service: sysmon        (Sysmon EID 22)
  ├── product: linux
  │     └── service: auditd
  └── product: network
        └── service: zeek

category: web
  ├── product: windows
  │     └── service: iis
  └── product: linux
        ├── service: apache
        └── service: nginx

category: audit
  ├── product: windows
  └── product: linux

category: authentication
  ├── product: windows
  │     ├── service: security      (EID 4624, 4625, 4648, 4768, 4769)
  │     └── service: sysmon        (Sysmon EID 8 — CreateRemoteThread)
  └── product: linux
        └── service: auditd

category: process_termination
  ├── product: windows
  │     ├── service: sysmon        (Sysmon EID 5)
  │     └── service: security
  └── product: linux
        └── service: auditd

category: driver_load
  └── product: windows
        ├── service: sysmon        (Sysmon EID 6)
        └── service: security      (EID 4673)

category: pipe_event
  └── product: windows
        └── service: sysmon        (Sysmon EID 17, 18)

category: registry_set
  └── product: windows
        └── service: sysmon        (Sysmon EID 13, 14)

category: registry_delete
  └── product: windows
        └── service: sysmon        (Sysmon EID 12, 13, 14)

category: registry_add
  └── product: windows
        └── service: sysmon        (Sysmon EID 12, 13, 14)

category: raw_access_thread
  └── product: windows
        └── service: sysmon        (Sysmon EID 9)

category: wmi_event
  └── product: windows
        ├── service: sysmon        (Sysmon EID 19, 20, 21)
        └── service: security
```

### Full Logsource Reference Table

| category | product | service | Description |
|---|---|---|---|
| `process_creation` | `windows` | `sysmon` | Sysmon EID 1 — Process creation |
| `process_creation` | `windows` | `security` | Windows Security EID 4688 |
| `process_creation` | `windows` | `powershell` | PowerShell EID 400/800 |
| `process_creation` | `linux` | `auditd` | auditd execve syscall |
| `process_creation` | `macos` | `esf` | macOS ESF process events |
| `process_creation` | `windows` | `microsoft365defender` | M365D process events |
| `process_creation` | `windows` | `crowdstrike` | CrowdStrike ProcessRollup2 |
| `file_event` | `windows` | `sysmon` | Sysmon EID 11 — FileCreate |
| `file_event` | `windows` | `security` | Security EID 4663 |
| `file_event` | `linux` | `auditd` | auditd file events |
| `file_event` | `macos` | `esf` | macOS ESF file events |
| `registry_event` | `windows` | `sysmon` | Sysmon EID 12/13/14 |
| `registry_event` | `windows` | `security` | Security EID 4657 |
| `registry_set` | `windows` | `sysmon` | Sysmon EID 13 |
| `registry_delete` | `windows` | `sysmon` | Sysmon EID 12 |
| `registry_add` | `windows` | `sysmon` | Sysmon EID 12/13/14 |
| `network_connection` | `windows` | `sysmon` | Sysmon EID 3 |
| `network_connection` | `windows` | `security` | Security EID 5156 |
| `network_connection` | `windows` | `firewall` | Windows FW EID 5157 |
| `network_connection` | `linux` | `auditd` | auditd network |
| `network_connection` | `network` | `zeek` | Zeek conn.log |
| `network_connection` | `network` | `suricata` | Suricata flow |
| `dns` | `windows` | `sysmon` | Sysmon EID 22 — DNSEvent |
| `dns` | `network` | `zeek` | Zeek dns.log |
| `dns` | `network` | `suricata` | Suricata DNS |
| `dns` | `linux` | `auditd` | auditd DNS |
| `image_load` | `windows` | `sysmon` | Sysmon EID 7 — Image loaded |
| `image_load` | `windows` | `sysmon` | Sysmon EID 23 — Image loaded (deleted) |
| `process_access` | `windows` | `sysmon` | Sysmon EID 10 — Process access |
| `process_termination` | `windows` | `sysmon` | Sysmon EID 5 — Process terminated |
| `process_termination` | `linux` | `auditd` | auditd exit |
| `driver_load` | `windows` | `sysmon` | Sysmon EID 6 — Driver loaded |
| `driver_load` | `windows` | `security` | Security EID 4673 |
| `pipe_event` | `windows` | `sysmon` | Sysmon EID 17/18 — Pipe created/connected |
| `raw_access_thread` | `windows` | `sysmon` | Sysmon EID 9 — RawAccessRead |
| `wmi_event` | `windows` | `sysmon` | Sysmon EID 19/20/21 — WMI |
| `wmi_event` | `windows` | `security` | Windows WMI-Activity |
| `web` | `windows` | `iis` | IIS web server logs |
| `web` | `linux` | `apache` | Apache access.log |
| `web` | `linux` | `nginx` | Nginx access.log |
| `web` | `linux` | `tomcat` | Tomcat access log |
| `authentication` | `windows` | `security` | Security EID 4624/4625/4768/4769/4776 |
| `authentication` | `linux` | `auditd` | pam authentication |
| `authentication` | `linux` | `sshd` | SSH auth log |
| `authentication` | `network` | `zeek` | Zeek conn.log |
| `audit` | `windows` | `security` | Various Windows Security EIDs |
| `audit` | `linux` | `auditd` | General auditd events |
| `application` | `windows` | `application` | Windows Application Event Log |
| `application` | `linux` | `syslog` | Linux syslog |
| `application` | `macos` | `unifiedlog` | macOS unified log |
| `certificate` | `windows` | `security` | Security EID 4886/4887/4888 |
| `process_hollowing` | `windows` | `sysmon` | Sysmon EID 8 — CreateRemoteThread |
| `scheduled_task` | `windows` | `security` | Security EID 4698/4699 |
| `scheduled_task` | `windows` | `taskscheduler` | Task Scheduler operational |
| `service_installation` | `windows` | `security` | Security EID 4697 |
| `service_installation` | `windows` | `system` | System EID 7045 |
| `dcom` | `windows` | `security` | Security EID 5154/5158 |
| `rdp` | `windows` | `terminal` | Terminal Services |
| `vpn` | `linux` | `openvpn` | OpenVPN logs |
| `email` | `network` | `exchange` | Exchange transport |
| `email` | `office` | `365` | Office 365 audit |
| `cloud` | `aws` | `cloudtrail` | AWS CloudTrail |
| `cloud` | `azure` | `activity` | Azure Activity Log |
| `cloud` | `azure` | `signin` | Azure AD Sign-in |
| `cloud` | `gcp` | `audit` | GCP Cloud Audit Logs |
| `kubernetes` | `cloud` | `k8s` | Kubernetes audit |
| `container` | `cloud` | `docker` | Docker daemon logs |

---

## Detection Modifiers

Modifiers are postfixed to field names with `|` to transform matching behavior.

### contains, startswith, endswith

```yaml
selection:
    FieldName|contains: 'substring'       # Case-insensitive substring match
    FieldName|startswith: 'prefix'        # Field starts with value
    FieldName|endswith: '\powershell.exe' # Field ends with value
```

- **Default** (no modifier) = exact match
- `|contains` = case-insensitive substring
- `|startswith` = case-insensitive prefix
- `|endswith` = case-insensitive suffix

### all, base64, base64offset, utf16le

```yaml
selection:
    # All values must match (AND instead of OR)
    CommandLine|all:
        - 'value1'
        - 'value2'

    # Base64 encoded content (decode + match)
    CommandLine|base64: 'powershell'

    # Base64 offset variants (standard, URL-safe, padding variants)
    CommandLine|base64offset:
        - '-enc '
        - '-enco'

    # UTF-16LE (Windows wide string encoding) — decode then match
    CommandLine|utf16le: 'malicious'

    # Wide string encoding variants
    Field|wide: 'value'
```

**base64offset** is the most powerful — it automatically handles all three base64 alignment variants (offset 0, 1, 2):

```
Input:     "-enc "
Base64:    LQBlAG4AYwAgAA==    (offset 0 — standard)
           LQBlAG4AYwAgAA==    (offset 1)
           LQBlAG4AYwAgAA==    (offset 2 — URL-safe, etc.)
```

### re, cidr, lt, gt, le, ge

```yaml
selection:
    # Regular expression match
    CommandLine|re: '(?i).*Invoke-Expression.*'

    # CIDR match (IP fields)
    SourceIp|cidr: '10.0.0.0/8'
    DestinationIp|cidr:
        - '192.168.0.0/16'
        - '172.16.0.0/12'

    # Numeric comparisons
    EventID:
        - 4624
        - 4625
    EventID|lt: 1000        # Less than 1000
    EventID|gt: 500         # Greater than 500
    EventID|le: 1000        # Less than or equal
    EventID|ge: 500         # Greater than or equal

    # In-range (via two conditions)
    EventID:
        - 500..1000         # Between 500 and 1000 inclusive (Sigma v2)
```

### Modifier Combinations

```yaml
selection:
    # Multiple modifiers on one field (pipe-separated)
    CommandLine|contains|base64offset:
        - '-enc '
        - '-enco'
        - '-encodedCommand'

    # Case-insensitive regex
    CommandLine|re|i: 'Malware.*v\d+'

    # Contains + wide
    Field|contains|wide: 'value'

    # All + contains
    Field|all|contains:
        - 'sub1'
        - 'sub2'
```

**Full modifier reference:**

| Modifier | Scope | Description |
|---|---|---|
| (none) | all | Exact match (case-insensitive) |
| `contains` | string | Substring match |
| `startswith` | string | Prefix match |
| `endswith` | string | Suffix match |
| `all` | list | All values must match (AND logic) |
| `base64` | string | Decode base64 then apply match |
| `base64offset` | string | Decode all base64 offset variants |
| `utf16le` | string | Decode UTF-16LE then apply match |
| `wide` | string | Match as wide string (UTF-16LE) |
| `re` | string | Regular expression match |
| `cidr` | IP | CIDR range match |
| `lt` | numeric | Less than |
| `gt` | numeric | Greater than |
| `le` | numeric | Less than or equal |
| `ge` | numeric | Greater than or equal |
| `i` | regex | Case-insensitive regex (postfix modifier) |

---

## Detection Expression Types

### 1. String Matching

```yaml
selection:
    Image: 'C:\Windows\System32\cmd.exe'      # Exact match
    Image|endswith: '\cmd.exe'                 # Suffix
    Image|contains: 'cmd'                      # Substring
    Image|startswith: 'C:\Windows'             # Prefix
```

### 2. List Matching

```yaml
selection:
    EventID:
        - 4688          # Process creation
        - 4689          # Process termination
        - 4690          # Handle duplication
    # Matches if EventID is ANY of these values (OR)
```

### 3. Keyword Matching

```yaml
# Keywords search across multiple fields
detection:
    keywords:
        - 'malware'
        - 'C2'
        - 'backdoor'
    condition: keywords
```

Keywords match against **all indexed fields** (full-text search in the SIEM).

### 4. Numeric Matching

```yaml
selection:
    EventID: 4624
    LogonType|gt: 2
    LogonType|lt: 11
    TargetUserName|startswith: 'Admin'
```

### 5. IP CIDR Matching

```yaml
selection:
    SourceIp|cidr:
        - '10.0.0.0/8'
        - '172.16.0.0/12'
        - '192.168.0.0/16'
    DestinationIp|cidr: '203.0.113.0/24'
```

### 6. Regular Expression

```yaml
selection:
    CommandLine|re: '(?i)(Invoke-(Expression|Command|Shellcode)|IEX\s+\()'
    DnsQueryName|re: '^[a-z0-9]{20,}\.(com|net|org|xyz|top)$'
    UrlPath|re: '/[a-z]{3,10}/[a-f0-9]{32}\.php'
```

### 7. Wildcard Matching

```yaml
selection:
    # Sigma v2 — explicit wildcard
    Image|wildcard: 'C:\Users\*\AppData\Local\Temp\*'
    CommandLine|contains|wildcard: '*.ps1'

    # In v1, wildcards are implicit in string values:
    CommandLine: '*-enc *'      # v1 treats * as wildcard automatically
```

### 8. Map/Field Presence

```yaml
selection:
    # Field exists (any value)
    TargetUserName: '*'           # Wildcard matches any non-empty value

    # Field does not exist (negation with `not`)
condition: selection and not TargetUserName
```

---

## Condition Logic

### Selection and Filter

```yaml
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains: '-enc '
    filter:
        CommandLine|contains: 'Write-Host'
    condition: selection and not filter
```

### 1 of, All of

```yaml
detection:
    selection1:
        EventID: 4688
        Image|endswith: '\psexec.exe'
    selection2:
        EventID: 4688
        Image|endswith: '\PAExec.exe'
    selection3:
        EventID: 4688
        Image|endswith: '\paexec.exe'
    condition: 1 of selection*
    # Equivalent: selection1 or selection2 or selection3
```

```yaml
detection:
    selection1:
        Image|endswith: '\powershell.exe'
    selection2:
        CommandLine|contains: '-enc '
    selection3:
        CommandLine|contains: '-nop'
    condition: all of selection*
    # Equivalent: selection1 and selection2 and selection3
```

### Negation

```yaml
detection:
    selection:
        EventID: 4688
        Image|endswith: '\powershell.exe'
    filter:
        CommandLine|contains:
            - 'Get-Help'
            - 'Write-Host'
            - 'Get-Process'
    filter_admin:
        UserName|endswith: '-admin'
    condition: selection and not filter and not filter_admin
```

**Map names starting with `_` (underscore) are automatically treated as exclusions:**

```yaml
detection:
    selection:
        EventID: 4688
    _filter:
        Image|endswith: '\svchost.exe'
    condition: selection and not _filter
```

### Aggregation Count

```yaml
# Sigma v2 — correlation rules
detection:
    selection:
        EventID: 4625          # Failed logon
    timeframe: 5m
    condition: selection | count() > 10
    # More than 10 failed logons in 5 minutes (brute force)
```

```yaml
detection:
    selection:
        EventID: 4663
        ObjectName|startswith: 'C:\Users'
        AccessMask: '0x2'       # Write
    timeframe: 15m
    condition: selection | count(SourceUserName) > 100
    # More than 100 write events from one user in 15m
```

### Temporal Proximity

```yaml
# Sigma v2 correlation
type: temporal
name: Mimikatz_Detected_After_Powershell
detection:
    # Sequence: PowerShell download → Mimikatz execution within 30 seconds
    - selection_powershell:
        EventID: 4688
        Image|endswith: '\powershell.exe'
    - selection_mimikatz:
        EventID: 4688
        Image|endswith: '\mimikatz.exe'
    timeframe: 30s
    ordered: true
condition: selection_powershell followed by selection_mimikatz
```

### Value Aggregation

```yaml
# Count distinct values
type: value_count
name: Failed_Logins_Multiple_Users
detection:
    selection:
        EventID: 4625
    timeframe: 5m
    condition: selection | count_distinct(TargetUserName) > 5
    # More than 5 unique target accounts in 5 minutes
```

### Near

```yaml
# Events near each other in time
type: near
name: Process_Creation_Near_File_Download
detection:
    - selection_process:
        EventID: 4688
    - selection_download:
        EventID: 11            # Sysmon FileCreate
        TargetFilename|endswith: '.exe'
    timeframe: 10s
    condition: selection_process near selection_download
```

---

## Sigma Specification v1 vs v2

| Feature | v1 | v2 |
|---|---|---|
| **Stable/released** | Stable (de facto) | Emerging (pySigma 0.14+) |
| **Condition syntax** | Map-based boolean | Map-based + correlation DSL |
| **Correlation rules** | ❌ Not supported | ✅ `event_count`, `value_count`, `temporal`, `ordered_temporal`, `near` |
| **Aggregation** | ❌ | ✅ `count()`, `count_distinct()`, `sum()`, `avg()` |
| **Timeframe** | ❌ | ✅ `timeframe: 5m` |
| **Wildcard explicit** | Implicit in strings | Explicit `wildcard` modifier |
| **Range syntax** | Manual `lt`/`gt` | `500..1000` syntax |
| **Keyword search** | ✅ keywords field | ✅ keywords field |
| **Tests embedded** | YAML format | Same, extended |
| **Backends** | sigmac (Python 2+3) | pySigma (Python 3.8+) |
| **Plugin system** | Limited | Rich plugin architecture |
| **Pipelines** | Basic | Full processing pipelines |
| **FieldRE** | ❌ | ✅ Field rename via regex |
| **URL field test** | ❌ | ✅ Fetch URL for test data |
| **Combined rule sets** | ❌ | ✅ `combine` in rules |


### Sigma v2 Features

**Range syntax:**
```yaml
detection:
    selection:
        EventID: 500..1000     # Between 500 and 1000 inclusive
        LogonType:
            - 2..10
            - 11               # 2-10 OR 11
```

**Explicit wildcard:**
```yaml
detection:
    selection:
        Image|wildcard: 'C:\Users\*\AppData\Local\Temp\*'
        CommandLine|wildcard: '*.ps1'
```

**Aggregation in conditions:**
```yaml
detection:
    selection:
        EventID: 4625
    timeframe: 5m
    condition: selection | count() > 10

# Count by field:
condition: selection | count(SourceIp) > 5
```

---

## Sigma Correlation Rules

Correlation rules (Sigma v2 via pySigma) enable multi-event detection.

### event_count

Count events matching a selection within a timeframe.

```yaml
title: Multiple Failed Logons for Single User
id: b2a5b3c4-d5e6-4789-8f01-234567890abc
status: experimental
description: Detects brute force attempts against a single user account
logsource:
    category: authentication
    product: windows
detection:
    selection:
        EventID: 4625        # Failed logon
        TargetUserName: '*'   # Non-empty target user
    timeframe: 5m
    condition: selection | count() > 10
level: high
```

### value_count

Count distinct values of a field across events within a timeframe.

```yaml
title: Failed Logons from Many Different Users
id: c3b5c4d5-e6f7-4890-9f12-34567890abcd
status: experimental
description: Detects password spraying across many accounts
logsource:
    category: authentication
    product: windows
detection:
    selection:
        EventID: 4625
    timeframe: 5m
    condition: selection | count_distinct(TargetUserName) > 5
level: high

---
# Statistical outlier detection
title: Unusual Number of Failed Logons — Statistical Baseline
id: d4c5d6e7-f8a9-4901-af23-4567890abcde
description: Detects when failed logon count exceeds statistical baseline
logsource:
    category: authentication
    product: windows
detection:
    selection:
        EventID: 4625
    timeframe: 1h
    condition: selection | count() > (selection | baseline(p50) + 3 * selection | baseline(stdev))
level: medium
```

### temporal

Sequence of events — A happened then B happened within a timeframe.

```yaml
title: Suspicious Process Access by Unknown Tool
type: temporal
name: Suspicious_Process_Access
logsource:
    product: windows
    service: sysmon
detection:
    # Process access (EID 10) followed by process termination (EID 5)
    - selection_access:
        EventID: 10
        GrantedAccess: '0x1FFFFF'  # All access
    - selection_terminate:
        EventID: 5
    timeframe: 5s
    ordered: true
condition: selection_access followed by selection_terminate
level: high
```

### ordered_temporal

Same as temporal, but events must occur in exact order.

```yaml
title: Credential Dumping — Procdump on LSASS
type: ordered_temporal
name: Procdump_LSASS
logsource:
    product: windows
    service: sysmon
detection:
    - selection_process:
        EventID: 1
        Image|endswith: '\procdump.exe'
        CommandLine|contains: 'lsass'
    - selection_handle:
        EventID: 10          # Process access
        TargetImage|endswith: 'lsass.exe'
        GrantedAccess: '0x1FFFFF'
    timeframe: 30s
    condition: selection_process followed by selection_handle
level: critical
```

---

## Sigma Test Format

Rules can include inline tests:

```yaml
title: Testable Rule
id: ...
status: stable
logsource:
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 1
        Image|endswith: '\powershell.exe'
        CommandLine|contains|base64offset: '-enc '
    condition: selection
falsepositives: []
level: high

# Test cases (YAML list at the end)
tests:
    - name: Encoded PowerShell command should match
      commandline: powershell.exe -enc SQBFAFgAIAAoAE4AZQB3AC0ATwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AbQBhAGwAaQBjAGkAbwB1AHMALgBjAG8AbQAvAHAAYQB5AGwAbwBhAGQAJwApAA==
      Image: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
      EventID: 1
      match: true

    - name: Normal PowerShell help should not match
      commandline: powershell.exe Get-Help -Name Get-Process
      Image: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
      EventID: 1
      match: false

    - name: PowerShell version check should not match
      commandline: powershell.exe -Command "Write-Host 'test'"
      Image: C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
      EventID: 1
      match: false
```

**Test fields:**

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Test case name |
| `match` | Yes | `true` = should match, `false` = should not match |
| `commandline` | No | Value for CommandLine field |
| `Image` | No | Value for Image field |
| `EventID` | No | Value for EventID field |
| *(any field)* | No | Value for the specified field |
| `url` | No | URL to fetch test data from (Sigma v2) |

---

## Log Source Deep Dives

### Windows Security Event Log

Windows Security log events that Sigma rules commonly target:

| Event ID | Description | Sigma Category |
|---|---|---|
| 4624 | Successful logon | authentication |
| 4625 | Failed logon | authentication |
| 4634 | Logoff | authentication |
| 4648 | Explicit credential logon (RunAs) | authentication |
| 4672 | Admin logon (special privileges assigned) | authentication |
| 4688 | Process created | process_creation |
| 4689 | Process exited | process_termination |
| 4697 | Service installed | service_installation |
| 4698 | Scheduled task created | scheduled_task |
| 4699 | Scheduled task deleted | scheduled_task |
| 4700 | Scheduled task enabled | scheduled_task |
| 4701 | Scheduled task disabled | scheduled_task |
| 4702 | Scheduled task updated | scheduled_task |
| 4719 | Audit policy changed | audit |
| 4720 | User account created | audit |
| 4722 | User account enabled | audit |
| 4723 | Password change attempt | authentication |
| 4724 | Password reset attempt | authentication |
| 4726 | User account deleted | audit |
| 4732 | Member added to security group | audit |
| 4738 | User account changed | audit |
| 4740 | Account locked out | authentication |
| 4768 | Kerberos TGT requested | authentication |
| 4769 | Kerberos service ticket requested | authentication |
| 4770 | Kerberos service ticket renewed | authentication |
| 4771 | Kerberos pre-auth failed | authentication |
| 4776 | NTLM logon (domain controller) | authentication |
| 4793 | Password policy check | authentication |
| 4798 | User's local group membership enumerated | audit |
| 4799 | Security-enabled local group membership enumerated | audit |
| 4800 | Workstation locked | authentication |
| 4801 | Workstation unlocked | authentication |
| 4886 | Certificate Services received request | certificate |
| 4887 | Certificate Services approved/denied | certificate |
| 4888 | Certificate Services denied | certificate |
| 4898 | Certificate Services loaded template | certificate |
| 4902 | Per-user audit policy table created | audit |
| 4944 | Windows Firewall policy has changed | firewall |
| 4946 | Rule added to Windows Firewall | firewall |
| 5152 | Windows Filtering Platform blocked packet | firewall |
| 5154 | WFP permitted connection | network_connection |
| 5156 | WFP allowed connection | network_connection |
| 5157 | WFP blocked connection | network_connection |
| 5158 | WFP bind to local port | network_connection |
| 5447 | WPS filter change | audit |

### Windows Sysmon

Sysmon (System Monitor) provides the richest Windows event data for Sigma rules:

| Event ID | Name | Sigma Category |
|---|---|---|
| 1 | Process creation | process_creation |
| 2 | Process change (file deleted) | file_event |
| 3 | Network connection detected | network_connection |
| 4 | Sysmon service state changed | sysmon_status |
| 5 | Process terminated | process_termination |
| 6 | Driver loaded | driver_load |
| 7 | Image loaded | image_load |
| 8 | CreateRemoteThread detected | process_access |
| 9 | RawAccessRead detected | raw_access_thread |
| 10 | Process access | process_access |
| 11 | FileCreate | file_event |
| 12 | RegistryEvent (Object delete) | registry_delete |
| 13 | RegistryEvent (Value set) | registry_set |
| 14 | RegistryEvent (Key and value rename) | registry_event |
| 15 | FileCreateStreamHash | file_event |
| 16 | Sysmon config change | sysmon_status |
| 17 | PipeEvent (Pipe created) | pipe_event |
| 18 | PipeEvent (Pipe connected) | pipe_event |
| 19 | WmiEvent (WmiEventFilter) | wmi_event |
| 20 | WmiEvent (WmiEventConsumer) | wmi_event |
| 21 | WmiEvent (WmiEventConsumerToFilter) | wmi_event |
| 22 | DNSEvent (DNS query) | dns |
| 23 | FileDelete (detected) | file_event |
| 24 | ClipboardChange | clipboard_event |
| 25 | ProcessTampering | process_tampering |
| 255 | Error | error |

### Windows PowerShell

| EID | Provider | Description |
|---|---|---|
| 400 | PowerShell | Engine state changed (started) |
| 403 | PowerShell | Engine state changed (stopped) |
| 600 | PowerShell | Provider started |
| 800 | PowerShell | Pipeline execution details |
| 4103 | PowerShell (Module Logging) | Module logging — command invocation |
| 4104 | PowerShell (Script Block Logging) | Script block logging — script content |
| 4105 | PowerShell (Script Block Logging) | Script block started |
| 4106 | PowerShell (Script Block Logging) | Script block stopped |
| 53504 | PowerShell (Transcription) | PowerShell transcription started |
| 7937 | PowerShell (Security) | Event 7937 — suspicious actions |

### Windows Security Audit Categories

For fine-tuning `logsource` with Windows Security logs:

```yaml
logsource:
    product: windows
    service: security
    definition: 'Requirements: Audit Process Creation audit policy must be enabled'
```

Key audit subcategories relevant to Sigma:

| Subcategory | Event IDs |
|---|---|
| Audit Process Creation | 4688, 4689 |
| Audit Logon | 4624, 4625, 4634, 4647, 4648 |
| Audit Account Logon | 4768, 4769, 4770, 4771, 4776 |
| Audit Object Access | 4656, 4658, 4660, 4663, 4659 |
| Audit Registry | 4657 |
| Audit File Share | 5140, 5142, 5143, 5145 |
| Audit Policy Change | 4719, 4902, 4904, 4905, 4907 |
| Audit Privilege Use | 4672, 4673, 4674 |
| Audit User Account Management | 4720, 4722, 4723, 4724, 4726, 4738, 4740 |
| Audit Detailed Tracking | 4688, 4692, 4694 |
| Audit Handle Manipulation | 4658 |
| Audit Directory Service Access | 4662, 5136, 5137, 5139 |
| Audit Kerberos Service Ticket Operations | 4769 |

### Linux Auditd

```yaml
logsource:
    product: linux
    service: auditd
```

Key auditd event types:

| Type | Field | Description |
|---|---|---|
| SYSCALL | syscall | Syscall number |
| SYSCALL | exe | Executable path |
| SYSCALL | uid/gid | User/group IDs |
| EXECVE | argc/argv | Execve arguments |
| PATH | name | File path accessed |
| CONFIG_CHANGE | key | Audit rule key |
| USER_LOGIN | acct | Login account |
| USER_CMD | command | User command |
| CRED_ACQ | op | Credential acquisition |
| ANOM_ABEND | sig | Abnormal process termination |

**Example Sigma rule for auditd:**

```yaml
title: Linux Sudo Usage
logsource:
    product: linux
    service: auditd
detection:
    selection:
        type: 'SYSCALL'
        syscall: 'execve'
        exe: '/usr/bin/sudo'
    condition: selection
```

### Linux Syslog

```yaml
logsource:
    product: linux
    service: syslog
```

Key services: `sshd`, `cron`, `sudo`, `kernel`, `auth.log`, `daemon`, `kern`

**SSH auth example:**

```yaml
title: SSH Brute Force Attack
logsource:
    product: linux
    service: syslog
detection:
    selection:
        program: 'sshd'
        message|contains: 'Failed password for'
    timeframe: 5m
    condition: selection | count() > 20
level: high
```

### macOS Unified Log

```yaml
logsource:
    product: macos
    service: unifiedlog
```

macOS event sources: `process`, `kernel`, `logd`, `securityd`, `opendirectoryd`, `configd`

### Network (Zeek, Suricata)

```yaml
# Zeek
logsource:
    product: network
    service: zeek
    definition: 'Requirements: Zeek with conn.log, dns.log, http.log'

# Suricata
logsource:
    product: network
    service: suricata
```

**Zeek log types:** `conn.log`, `dns.log`, `http.log`, `ssl.log`, `ftp.log`, `smtp.log`, `ssh.log`, `dhcp.log`, `files.log`, `notice.log`

**Suricata event types:** `alert`, `flow`, `dns`, `http`, `tls`, `ssh`, `smtp`

### Cloud (AWS CloudTrail, Azure, GCP)

```yaml
# AWS CloudTrail
logsource:
    service: cloudtrail
    product: aws
    definition: 'Requirements: CloudTrail must be enabled on all accounts'

# Azure Active Directory / Microsoft 365
logsource:
    service: m365
    product: azure

# Azure Activity Log
logsource:
    service: activity
    product: azure

# GCP Cloud Audit
logsource:
    service: audit
    product: gcp
```

**AWS CloudTrail example:**

```yaml
title: AWS Console Login from Unusual Location
logsource:
    service: cloudtrail
    product: aws
detection:
    selection:
        eventName: 'ConsoleLogin'
        userIdentity.type: 'Root'
        sourceIPAddress|cidr:
            - '10.0.0.0/8'
            - '172.16.0.0/12'
            - '192.168.0.0/16'
    condition: selection
level: critical
```

**Azure example:**

```yaml
title: Azure Key Vault Access from Suspicious IP
logsource:
    service: activity
    product: azure
detection:
    selection:
        operationName: 'VaultGet' or 'VaultListSecrets'
        callerIpAddress|cidr:
            - '10.0.0.0/8'
            - '172.16.0.0/12'
            - '192.168.0.0/16'
    condition: selection
level: high
```

---

## Sigma Pipelines

Pipelines transform Sigma rules to match field naming and data format differences across log shippers and backends.

### Field Mapping

A pipeline maps Sigma field names to actual backend field names:

```yaml
# Pipeline: winlogbeat (Elastic)
name: winlogbeat
priority: 50
transformations:
  - field_name_map:
      Image: process.executable
      CommandLine: process.command_line
      ParentImage: process.parent.executable
      ParentCommandLine: process.parent.command_line
      TargetFilename: file.path
      SourceIp: source.ip
      DestinationIp: destination.ip
      DestinationPort: destination.port
      SourcePort: source.port
      UserName: user.name
      TargetUserName: user.name
```

```yaml
# Pipeline: sysmon-to-splunk
name: sysmon_to_splunk
priority: 50
transformations:
  - field_name_map:
      Image: Image
      CommandLine: CommandLine
      EventID: EventCode
      TargetFilename: TargetFilename
      SourceIp: SourceIp
      DestinationIp: DestinationIp
      DestinationPort: DestinationPort
```

### Field Name Transformations

```yaml
transformations:
  # Regex-based field rename
  - field_name_regex:
      from: '^winlog\.'
      to: ''

  # Lowercase all field names
  - field_name_lowercase: ~

  # Prefix fields
  - field_name_prefix:
      prefix: 'EventData.'

  # Add suffix
  - field_name_suffix:
      suffix: '_raw'

  # Remove null fields
  - remove_null_fields: ~

  # Set default field
  - set_field:
      field: event.kind
      value: event
```

### Log Source Transformations

```yaml
transformations:
  # Map logsource to backend event code
  - logsource_to_field:
      field: EventID
      mapping:
        windows/sysmon/process_creation: 1
        windows/sysmon/file_event: 11
        windows/sysmon/network_connection: 3
        windows/security/authentication:
          - 4624
          - 4625
        windows/security/process_creation: 4688

  # Filter by event source
  - filter_logsource:
      provider: 'Microsoft-Windows-Sysmon'
```

### Built-in Pipelines

Common pipelines shipped with pySigma backends:

| Backend | Pipeline | Description |
|---|---|---|
| Elasticsearch | `winlogbeat` | Winlogbeat ECS field mapping |
| Elasticsearch | `logs-*` | Generic ECS logs |
| Elasticsearch | `endgame` | Elastic Endgame ECS |
| Splunk | `cim` | Splunk CIM data model |
| Splunk | `datasource` | Splunk DataSource model |
| QRadar | `qradar` | QRadar field mapping |
| Azure Sentinel | `asim` | Azure Sentinel ASIM |
| LogPoint | `logpoint` | LogPoint SIEM |
| AWS Athena | `aws_athena` | Athena/CloudTrail tables |

---

## pySigma — The Modern Converter

### Installation

```bash
# Core pySigma library
pip install pysigma

# Backends (one or more)
pip install pysigma-backend-elasticsearch       # Elasticsearch / Elastic Security
pip install pysigma-backend-splunk              # Splunk SPL
pip install pysigma-backend-qradar              # IBM QRadar AQL
pip install pysigma-backend-azure-sentinel      # Microsoft Sentinel KQL
pip install pysigma-backend-secops              # Various (Loki, BigQuery, etc.)
pip install pysigma-backend-loki                # Grafana Loki LogQL
pip install pysigma-backend-logpoint            # LogPoint
pip install pysigma-backend-netwitness          # NetWitness
pip install pysigma-backend-splunkdatasource     # Splunk DataSource
pip install pysigma-backend-crowdstrike         # CrowdStrike

# All-in-one
pip install pysigma pysigma-backend-elasticsearch pysigma-backend-splunk pysigma-backend-qradar pysigma-backend-azure-sentinel
```

### Basic Usage

```bash
# Convert a single rule to Elasticsearch query
sigma convert -t es-qs -p winlogbeat rule.yml

# Convert a single rule to Splunk SPL
sigma convert -t splunk -p splunk_cim rule.yml

# Convert a single rule to QRadar AQL
sigma convert -t qradar -p qradar rule.yml

# Convert a directory of rules
sigma convert -t es-qs -p winlogbeat -r rules/ -o output/

# List available targets and pipelines
sigma list targets
sigma list pipelines

# Validate rule
sigma check rule.yml

# Show rule information
sigma info rule.yml
```

**Python API:**

```python
from sigma.collection import SigmaCollection
from sigma.backends.elasticsearch import ElasticsearchBackend
from sigma.pipelines.windows import sigma_pipeline_winlogbeat

# Load rules
rules = SigmaCollection.load_yaml("rule.yml")

# Or from directory
rules = SigmaCollection.load_directory("rules/")

# Choose backend + pipeline
backend = ElasticsearchBackend(
    processing_pipeline=sigma_pipeline_winlogbeat()
)

# Convert
queries = backend.convert(rules)

for query in queries:
    print(query)  # Elasticsearch query DSL string
```

### Plugin Architecture

```bash
# List installed plugins
sigma plugin list

# Install a backend plugin
sigma plugin install pysigma-backend-splunk

# Create a custom plugin
sigma plugin create my-backend
```

**Discovering available pipelines:**

```python
from sigma.plugin import SigmaPluginRegistry

# List all installed pipelines
for plugin in SigmaPluginRegistry.plugins:
    print(plugin.name, plugin.version)
```

### Backend Development

```python
from sigma.backends.base import SingleQuerySigmaBackend
from sigma.conversion.state import ConversionState

class CustomBackend(SingleQuerySigmaBackend):
    identifier = "custom"
    output_format = "json"

    def __init__(self, processing_pipeline=None):
        super().__init__(processing_pipeline)

    def convert_condition(self, cond, state: ConversionState):
        # Implement custom conversion logic
        pass

    def finalize_query(self, query, state):
        return json.dumps({"query": query})
```

### Processing Pipelines in pySigma

```python
from sigma.pipeline import SigmaPipeline
from sigma.processing.transformations import (
    FieldNameMappingTransformation,
    LowercaseFieldNamesTransformation,
    FieldMappingTransformation,
)

pipeline = SigmaPipeline(
    transformations=[
        FieldNameMappingTransformation({
            "Image": "process.executable",
            "CommandLine": "process.command_line",
        }),
        LowercaseFieldNamesTransformation(),
    ]
)
```

---

## Backend Reference

### Elasticsearch / Elastic Security

```bash
sigma convert -t es-qs -p winlogbeat rule.yml
sigma convert -t es-qs -p logs-endpoint rule.yml   # Elastic Agent
sigma convert -t es-qs -p logs-windows rule.yml     # Generic Windows
sigma convert -t es-qs -p ecs-windows rule.yml      # ECS Windows
sigma convert -t es-dsl -p winlogbeat rule.yml      # Raw DSL
sigma convert -t es-rule -p winlogbeat rule.yml     # Elastic Security rule API
```

**Output types:**
- `es-qs` — Query string (Lucene syntax)
- `es-dsl` — Raw Elasticsearch Query DSL (JSON)
- `es-rule` — Elastic Security rule format (importable via API)

**Example output (Lucene):**
```
process.executable:\\powershell.exe AND process.command_line:*.exe*
```

**Example output (DSL):**
```json
{
  "query": {
    "bool": {
      "must": [
        {"wildcard": {"process.executable": "*\\powershell.exe"}},
        {"wildcard": {"process.command_line": "*.exe*"}}
      ]
    }
  }
}
```

### Splunk

```bash
sigma convert -t splunk -p splunk_cim rule.yml
sigma convert -t splunk -p splunk_datamodel rule.yml
sigma convert -t splunk -p splunk_datasource rule.yml
```

**Example output:**
```
source="WinEventLog:Microsoft-Windows-Sysmon/Operational" Image=*\\powershell.exe CommandLine=*-enc*
```

With CIM data model:
```
| datamodel Process search | search process_name=powershell.exe AND process_exec=*\\powershell.exe
```

### QRadar / AQL

```bash
sigma convert -t qradar rule.yml
```

**Example output (AQL):**
```
SELECT * FROM events WHERE IMAGE = '*\\powershell.exe' AND COMMANDLINE LIKE '%-enc%'
```

### Microsoft Sentinel / Azure

```bash
sigma convert -t azure-sentinel rule.yml
sigma convert -t azure-sentinel -p asim rule.yml   # ASIM pipeline
```

**Example output (KQL):**
```
SecurityEvent
| where EventID == 4688
| extend Process = tostring(Process)
| where Process endswith "\\powershell.exe"
| where CommandLine contains "-enc"
```

### Chronicle / BigQuery

```bash
sigma convert -t bigquery rule.yml
```

**Example output (SQL):**
```sql
SELECT * FROM `project.dataset.events`
WHERE SPLIT(Image, '\\')[OFFSET(ARRAY_LENGTH(SPLIT(Image, '\\'))-1)] = 'powershell.exe'
AND CommandLine LIKE '%-enc%'
```

### Loki (Grafana)

```bash
sigma convert -t loki rule.yml
```

**Example output (LogQL):**
```
{job="windows"} |= "powershell" |= "-enc"
```

### LogPoint

```bash
sigma convert -t logpoint rule.yml
```

**Example output:**
```
norm_id=WinServerMS PowerShell Image=*\\powershell.exe CommandLine=*-enc*
```

### ArcSight

```yaml
# ArcSight ESM filters use CEF format integration
# Typically via custom parser
```

### NetWitness

```bash
sigma convert -t netwitness rule.yml
```

### SoumniBot

SoumniBot is a unified detection interface that uses Sigma as its rule language:

```bash
soumniBot run rule.yml
```

### Elasticsearch Query DSL

```bash
sigma convert -t es-dsl rule.yml
```

### OpenSearch

Same as Elasticsearch backend (API compatible):

```bash
sigma convert -t es-qs -p winlogbeat rule.yml
```

### CrowdStrike

```bash
sigma convert -t crowdstrike rule.yml
```

### Splunk Data Model

```bash
sigma convert -t splunk -p splunk_datamodel rule.yml
```

### Splunk DataSource

```bash
sigma convert -t splunk -p splunk_datasource rule.yml
```

### PowerShell

```bash
# Target: PowerShell Detection Script
sigma convert -t powershell rule.yml
```

**Example output:**
```powershell
Get-WinEvent -LogName Microsoft-Windows-Sysmon/Operational | Where-Object {
    $_.Id -eq 1 -and
    $_.Properties[5].Value -like '*\powershell.exe'
}
```

---

## Rule Development Lifecycle

### 1. Identify Detection Gap

- Review threat intelligence, incident reports, red team findings
- Track new techniques from CISA, MITRE ATT&CK, threat feeds
- Use Atomic Red Team (ART) to validate coverage
- Map existing rules vs. techniques in your `coverage_matrix.csv`

### 2. Research TTP

- Understand the technique: MITRE ATT&CK page, blog posts, code repos
- Reproduce in lab environment
- Collect log samples from the attack
- Identify the **canonical log events** produced
- Determine the precise `logsource` (product, category, service)

### 3. Draft Rule

```yaml
title: Suspect Technique
id: <generate UUID v4>
status: test
description: |
    Detects technique X based on Y log event.
references:
    - https://attack.mitre.org/techniques/TXXXX/
author: You
date: YYYY/MM/DD
tags:
    - attack.tXXXX
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        # Distinguishing fields
        Image|endswith: '\something.exe'
        CommandLine|contains: 'suspicious_flag'
    filter:
        # Known false positive edges
        UserName|endswith: '\\admin'
    condition: selection and not filter
falsepositives:
    - Unknown at this time
level: high
```

### 4. Validate with Tests

Write test cases directly in the YAML:

```yaml
tests:
    - name: Malicious command should match
      Image: C:\Windows\something.exe
      CommandLine: 'something.exe /suspicious_flag'
      EventID: 1
      match: true
    - name: Normal admin usage should not match
      Image: C:\Windows\something.exe
      CommandLine: 'something.exe /legit'
      EventID: 1
      match: false
```

Run tests:
```bash
sigma check -t es-qs rule.yml
```

### 5. Convert & Test in SIEM

```bash
# Convert to your backend
sigma convert -t splunk -p splunk_cim rule.yml

# Run against SIEM test environment
# Verify:
# 1. Known malicious events trigger
# 2. Known benign events do NOT trigger
# 3. Latency is acceptable
```

### 6. Tune & Deploy

- Adjust `filter` for false positives
- Add `falsepositives` entries
- Set `status: stable`
- Deploy to staging → monitor 7 days → promote to production
- Set alerting threshold, notification channel

### 7. Monitor & Maintain

- Track FP rate weekly
- Update MITRE ATT&CK mappings as new versions release
- Review quarterly: still relevant? Too noisy? Superseded?
- When technique becomes obsolete, set `status: deprecated`

---

## Real-World Rule Examples

### 1. PowerShell Encoded Command Execution

```yaml
title: PowerShell Encoded Command Execution
id: f0f9e3b9-3e9f-4a9f-9f9f-9f9f9f9f9f9f
status: stable
description: Detects execution of encoded PowerShell commands often used for obfuscation
references:
    - https://attack.mitre.org/techniques/T1059/001/
    - https://docs.microsoft.com/en-us/powershell/
author: Sigma Community
date: 2020/01/15
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1059.001
    - attack.defense_evasion
    - attack.t1027
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        Image|endswith:
            - '\powershell.exe'
            - '\pwsh.exe'
        CommandLine|contains|base64offset:
            - '-enc '
            - '-enco'
            - '-encodedCommand'
            - ' -e '
            - '-en '
    condition: selection
falsepositives:
    - Administrative scripts using encoded commands
    - Software installation scripts
level: high
```

### 2. Mimikatz Detection via Event ID 7

```yaml
title: Mimikatz Detection — LSASS Access via Sysmon EID 7
id: a5c7e2d1-3f8b-4a1c-9e5d-6b2f8c3a1d0e
status: stable
description: Detects Mimikatz loading into memory via Sysmon image load events
references:
    - https://github.com/gentilkiwi/mimikatz
    - https://attack.mitre.org/techniques/T1003/001/
author: Defensive Engineering Team
date: 2021/06/15
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1003.001
    - attack.t1003.002
logsource:
    category: image_load
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 7
        ImageLoaded|endswith:
            - '\mimikatz.exe'
            - '\mimilib.dll'
            - '\mimispool.dll'
            - '\kuhl_m_sekurlsa.dll'
            - '\kuhl_m_kerberos.dll'
            - '\kuhl_m_privilege.dll'
            - '\kuhl_m_lsadump.dll'
    condition: selection
falsepositives:
    - Legitimate penetration testing engagement
level: critical
```

### 3. Cobalt Strike Named Pipe

```yaml
title: Cobalt Strike Named Pipe — Metasploit Pipes
id: b6d8f3e2-4a9c-5b1d-8f6e-7c3a9d2b1e4f
status: stable
description: Detects Cobalt Strike Beacon using known named pipe patterns
references:
    - https://www.cobaltstrike.com/
    - https://attack.mitre.org/techniques/T1055/
author: Defensive Engineering Team
date: 2022/03/10
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1055
    - attack.t1574.002
logsource:
    category: pipe_event
    product: windows
    service: sysmon
detection:
    selection:
        EventID:
            - 17    # Pipe created
            - 18    # Pipe connected
        PipeName|contains:
            - '\msf_'
            - '\msf'
            - '\status_'
            - '\postex_'
    condition: selection
falsepositives:
    - None observed; named pipe names are unique to Cobalt Strike
level: critical
```

### 4. Ransomware — Mass File Extension Renaming

```yaml
title: Suspicious Mass File Extension Renaming — Possible Ransomware
id: c7e9a4f3-5b1d-6c2e-9a7f-8d4b0e3c2f5a
status: stable
description: Detects rapid file renaming with suspicious extensions, indicative of ransomware
references:
    - https://attack.mitre.org/techniques/T1486/
author: Defensive Engineering Team
date: 2023/05/20
modified: 2024/06/27
tags:
    - attack.impact
    - attack.t1486
logsource:
    category: file_event
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 11
        TargetFilename|contains:
            - '.encrypted'
            - '.locked'
            - '.crypted'
            - '.crypto'
            - '.lockbit'
            - '.encrypt'
    timeframe: 1m
    condition: selection | count() > 50
falsepositives:
    - Backup software renaming files during restore operations
level: critical
```

### 5. Pass-the-Hash Detection

```yaml
title: Pass-the-Hash — NTLM Logon with Explicit Credentials
id: d8f0b5a4-6c2e-7d3f-8a1b-9e4c1f5d3a6b
status: stable
description: Detects NTLM logon with explicit credentials, potentially pass-the-hash
references:
    - https://attack.mitre.org/techniques/T1550/002/
    - https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624
author: Defensive Engineering Team
date: 2022/08/01
modified: 2024/06/27
tags:
    - attack.lateral_movement
    - attack.t1550.002
logsource:
    category: authentication
    product: windows
    service: security
detection:
    selection:
        EventID: 4624
        LogonType: 9                # NewCredentials (RunAs)
        LogonProcessName: 'NtLmSsp'
        AuthenticationPackageName: 'NTLM'
    condition: selection
falsepositives:
    - Legitimate RunAs usage with NTLM (rare in modern environments)
level: high
```

### 6. DCSync Attack

```yaml
title: DCSync Attack — Directory Replication Service Request
id: e9a1c6b5-7d3f-8e4a-9b1c-0f5d2a6e4b7c
status: stable
description: Detects DCSync attacks where an account requests domain replication via DS-Replication-Get-Changes
references:
    - https://attack.mitre.org/techniques/T1003/006/
author: Defensive Engineering Team
date: 2021/10/05
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1003.006
logsource:
    category: audit
    product: windows
    service: security
detection:
    selection:
        EventID: 4662
        ObjectType: 'DS-Replication-Get-Changes'
        AccessMask: '0x100'          # Replication access
    filter:
        UserName|endswith: '\\DC$'   # DC machine accounts are expected
    condition: selection and not filter
falsepositives:
    - Domain controller machine accounts
level: critical
```

### 7. WMI Persistence

```yaml
title: WMI Persistence — ActiveScriptEventConsumer
id: f0b2d7c6-8e4f-9a5b-1c2d-3e6f8a0b7d8e
status: stable
description: Detects WMI event subscription persistence using ActiveScriptEventConsumer
references:
    - https://attack.mitre.org/techniques/T1546/003/
    - https://learn.microsoft.com/en-us/windows/win32/wmisdk/wmi-events
author: Defensive Engineering Team
date: 2022/11/15
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1546.003
    - attack.execution
    - attack.t1047
logsource:
    category: wmi_event
    product: windows
    service: sysmon
detection:
    selection:
        EventID:
            - 19  # WmiEventFilter
            - 20  # WmiEventConsumer
            - 21  # WmiEventConsumerToFilter
        # ActiveScriptEventConsumer = persistent script execution
        Consumer: 'ActiveScriptEventConsumer'
    condition: selection
falsepositives:
    - Enterprise management software (SCCM, LANDesk)
level: high
```

### 8. Suspicious Service Installation

```yaml
title: Suspicious Service Installation
id: a1c3e5b7-9d2f-4e6a-8b0c-2d4f6e8a0c1e
status: stable
description: Detects suspicious service installations from temp directories or unusual names
references:
    - https://attack.mitre.org/techniques/T1543/003/
author: Defensive Engineering Team
date: 2020/09/10
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1543.003
    - attack.privilege_escalation
logsource:
    category: service_installation
    product: windows
    service: security
detection:
    selection:
        EventID: 4697
    selection_image:
        ServiceFileName|contains:
            - '\TEMP\'
            - '\Temp\'
            - '\temp\'
            - '\Windows\Temp\'
            - '\Users\'
            - '%APPDATA%'
            - '%TEMP%'
    selection_name:
        ServiceName|contains:
            - 'svchost'         # Masquerading
            - 'windows'
            - 'update'
            - 'security'
            - 'defender'
    selection_start:
        ServiceStartType: 2     # Auto-Start
    condition: selection and selection_image and (selection_name or selection_start)
falsepositives:
    - Legitimate software installation from temp directories
level: high
```

### 9. DNS Tunneling

```yaml
title: DNS Tunneling — High Entropy Subdomain Queries
id: b2d4f6a8-0c1e-3f5a-7b9d-1e3f5a7b9c0d
status: experimental
description: Detects DNS queries with high-entropy subdomains, potentially DNS tunneling
references:
    - https://attack.mitre.org/techniques/T1572/
author: Defensive Engineering Team
date: 2023/12/01
modified: 2024/06/27
tags:
    - attack.command_and_control
    - attack.t1572
logsource:
    category: dns
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 22
        QueryName|re: '^[a-f0-9]{32,}\.(com|net|org|info|top|xyz|club)$'
    timeframe: 5m
    condition: selection | count() > 10
falsepositives:
    - CDNs using hash-based hostnames
    - Legitimate dynamic DNS services
level: medium
```

### 10. New User Account Created

```yaml
title: New User Account Created
id: c3e5f7a9-1b2d-4f6a-8c0e-2f4a6b8c0d1e
status: stable
description: Detects creation of new local or domain user accounts
references:
    - https://attack.mitre.org/techniques/T1136/
author: Defensive Engineering Team
date: 2022/02/14
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1136.001
    - attack.t1136.002
logsource:
    category: audit
    product: windows
    service: security
detection:
    selection:
        EventID: 4720
    filter_domain:
        UserName|endswith: '$'       # Computer accounts
    filter_service:
        UserName|contains: 'HealthMailbox'  # Exchange mailboxes
    condition: selection and not filter_domain and not filter_service
falsepositives:
    - IT creating accounts for new employees
    - Provisioning automation
level: high
```

### 11. Logon from Unusual Country

```yaml
title: Logon from Unusual Geographical Location
id: d4f6a8b0-2c3e-5f7a-9b1d-3e5f7a9b1c2d
status: experimental
description: Detects user logon from a country not previously seen for that user
references:
    - https://attack.mitre.org/techniques/T1078/
author: Defensive Engineering Team
date: 2023/03/22
modified: 2024/06/27
tags:
    - attack.initial_access
    - attack.t1078
    - detection.baseline
logsource:
    category: authentication
    product: azure
    service: signin
detection:
    selection:
        Status: 'Success'
        RiskLevel: 'medium' or 'high'
    condition: selection
falsepositives:
    - Employee travel to new countries
    - VPN usage routing through different countries
level: medium
```

### 12. Attempt to Disable Security Logging

```yaml
title: Attempt to Disable Security Logging
id: e5f7a9b1-3d4e-6f8a-0c2d-4e6f8a0c2d3e
status: stable
description: Detects attempts to disable or tamper with Windows security logging
references:
    - https://attack.mitre.org/techniques/T1562/
author: Defensive Engineering Team
date: 2022/05/30
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1562.001
    - attack.t1562.002
    - attack.t1562.006
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection_wevtutil:
        Image|endswith: '\wevtutil.exe'
        CommandLine|contains:
            - 'cl '
            - 'clear-log'
            - 'set-log'
    selection_auditpol:
        Image|endswith: '\auditpol.exe'
        CommandLine|contains:
            - '/clear'
            - '/remove'
            - '/disable'
    selection_powershell:
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - 'Stop-Service'
            - 'Disable-Service'
            - 'Clear-EventLog'
            - 'Remove-EventLog'
            - 'Set-Service'
        CommandLine|contains:
            - 'EventLog'
            - 'WinRM'
            - 'audit'
    selection_sc:
        Image|endswith: '\sc.exe'
        CommandLine|contains:
            - 'EventLog'
            - 'WinRM'
        CommandLine|contains:
            - 'stop'
            - 'config'
    condition: 1 of selection_*
falsepositives:
    - Administrators clearing logs for maintenance
    - Log rotation scripts
level: high
```

### 13. Process Injection (Sysmon EID 8)

```yaml
title: Process Injection — CreateRemoteThread Detected
id: f6a8b0c2-4e5f-7a9b-1d3e-5f7a9b1d3e4f
status: stable
description: Detects CreateRemoteThread API call, indicative of process injection
references:
    - https://attack.mitre.org/techniques/T1055/
author: Defensive Engineering Team
date: 2021/02/10
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1055.001
    - attack.t1055.012
logsource:
    category: process_access
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 8
        SourceImage|endswith:
            - '\powershell.exe'
            - '\cmd.exe'
            - '\wscript.exe'
            - '\cscript.exe'
            - '\mshta.exe'
            - '\regsvr32.exe'
            - '\rundll32.exe'
            - '\winword.exe'
            - '\excel.exe'
            - '\outlook.exe'
            - '\wmplayer.exe'
            - '\java.exe'
            - '\svchost.exe'
    filter:
        TargetImage|startswith: 'C:\Windows\System32\'
    condition: selection and not filter
falsepositives:
    - Antivirus software
    - Debugging tools (x64dbg, Windbg)
    - Legitimate process monitoring tools
level: high
```

### 14. Outbound RDP Connection

```yaml
title: Outbound RDP Connection from Non-Admin Workstation
id: a7b9c1d3-5f6a-8b0c-2e4f-6a8b0c2e4f5a
status: experimental
description: Detects outbound RDP connections from workstations, which is uncommon in most environments
references:
    - https://attack.mitre.org/techniques/T1021/001/
author: Defensive Engineering Team
date: 2023/08/15
modified: 2024/06/27
tags:
    - attack.lateral_movement
    - attack.t1021.001
logsource:
    category: network_connection
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 3
        DestinationPort: 3389
        Protocol: 'tcp'
        Initiated: 'true'
    # Filter out known admin/jump boxes
    filter_admin:
        Image|endswith: '\mstsc.exe'
    condition: selection and not filter_admin
falsepositives:
    - RDP from terminal servers
    - RDP from IT admin workstations
level: medium
```

### 15. Azure Key Vault Access from Unusual IP

```yaml
title: Azure Key Vault Access from Unusual IP Range
id: b8c0d2e4-6a7b-9c1d-3f5a-7b9c1d3f5a6b
status: experimental
description: Detects access to Azure Key Vault from IP ranges outside expected corporate ranges
references:
    - https://attack.mitre.org/techniques/T1525/
author: Defensive Engineering Team
date: 2024/01/10
modified: 2024/06/27
tags:
    - attack.collection
    - attack.t1525
logsource:
    service: activity
    product: azure
detection:
    selection:
        operationName:
            - 'VaultGet'
            - 'VaultListSecrets'
            - 'SecretGet'
            - 'KeyGet'
    filter_corp:
        callerIpAddress|cidr:
            - '10.0.0.0/8'
            - '172.16.0.0/12'
            - '192.168.0.0/16'
            - '100.64.0.0/10'
    condition: selection and not filter_corp
falsepositives:
    - External developers or services accessing key vault
level: high
```

### 16. AWS IAM Privilege Escalation

```yaml
title: AWS IAM Privilege Escalation — CreatePolicy with Full Access
id: c9d1e3f5-7a8b-0c2d-4e6f-8a0c2d4e6f7a
status: experimental
description: Detects creation of IAM policies granting full administrative access
references:
    - https://attack.mitre.org/techniques/T1098/
    - https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreatePolicy.html
author: Defensive Engineering Team
date: 2023/10/05
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1098
    - attack.privilege_escalation
logsource:
    service: cloudtrail
    product: aws
detection:
    selection:
        eventName: 'CreatePolicy' or 'PutUserPolicy' or 'PutGroupPolicy'
        requestParameters.policyDocument: '*Effect":"Allow*'
        requestParameters.policyDocument: '*Action":"*"*'       # Wildcard action
        requestParameters.policyDocument: '*Resource":"*"*'     # Wildcard resource
    condition: selection
falsepositives:
    - Authorized cloud administrators setting up new accounts
level: high
```

### 17. Linux SSH Brute Force

```yaml
title: SSH Brute Force — Multiple Failed Authentications
id: d0e2f4a6-8b9c-1d3e-5f7a-9b1d3e5f7a8b
status: stable
description: Detects multiple failed SSH authentication attempts within a short timeframe
references:
    - https://attack.mitre.org/techniques/T1110/
author: Defensive Engineering Team
date: 2022/04/10
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1110
logsource:
    category: authentication
    product: linux
    service: syslog
detection:
    selection:
        program: 'sshd'
        message|contains: 'Failed password for'
    timeframe: 10m
    condition: selection | count() > 20
falsepositives:
    - Misconfigured services retrying authentication
    - Network latency causing retries
level: high
```

### 18. Kubernetes Container to Cluster Admin

```yaml
title: Kubernetes — Container Access to Cluster-Admin Role
id: e1f3a5b7-9c0d-2e4f-6a8b-0c2e4f6a8b0c
status: experimental
description: Detects when a container attempts to escalate to cluster-admin role
references:
    - https://attack.mitre.org/techniques/T1610/
author: Defensive Engineering Team
date: 2024/03/01
modified: 2024/06/27
tags:
    - attack.privilege_escalation
    - attack.t1610
logsource:
    service: k8s
    product: cloud
detection:
    selection:
        verb: 'create' or 'update' or 'bind'
        objectRef.resource: 'clusterrolebindings'
        objectRef.name|contains:
            - 'cluster-admin'
            - 'clusteradmin'
    filter:
        user.username|contains:
            - 'system:'
            - 'kube-admin'
    condition: selection and not filter
falsepositives:
    - Authorized cluster administrators
level: high
```

### 19. Web Shell Detection via Logs

```yaml
title: Web Shell Detection — Suspicious HTTP POST with Process Creation
id: f2a4b6c8-0d1e-3f5a-7b9c-1d3f5a7b9c0d
status: experimental
description: Detects web shell usage by correlating web requests with subsequent process creation
references:
    - https://attack.mitre.org/techniques/T1505/003/
author: Defensive Engineering Team
date: 2023/06/20
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1505.003
logsource:
    category: web
    product: linux
    service: apache
detection:
    selection:
        c-uri|contains:
            - '/cmd.php'
            - '/shell.aspx'
            - '/exec.jsp'
            - '/eval.php'
            - '/uploads/'
        cs-method: 'POST'
        sc-status: 200
    condition: selection
falsepositives:
    - Legitimate file upload functionality
level: high
```

### 20. Attempt to Disable Antivirus

```yaml
title: Attempt to Disable Antivirus or Security Software
id: a3b5c7d9-1e2f-4a6b-8c0d-2e4f6a8b0c1d
status: stable
description: Detects attempts to disable or tamper with antivirus/security software
references:
    - https://attack.mitre.org/techniques/T1562/001/
author: Defensive Engineering Team
date: 2022/07/01
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1562.001
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection_defender:
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - 'Disable-MpPreference'
            - 'Set-MpPreference'
            - 'Remove-MpPreference'
            - 'Add-MpPreference'
            - 'Stop-MpService'
            - 'Set-MpPreference -DisableRealtimeMonitoring $true'
            - 'Set-MpPreference -DisableIOAVProtection $true'
    selection_av_termination:
        Image|endswith: '\sc.exe'
        CommandLine|contains:
            - 'stop WinDefend'
            - 'stop SecurityHealthService'
            - 'stop wscsvc'
    selection_registry:
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - 'DisableAntiSpyware'
            - 'DisableRealtimeMonitoring'
            - 'DisableBehaviorMonitoring'
            - 'DisableBlockAtFirstSeen'
    condition: 1 of selection_*
falsepositives:
    - IT administrators disabling AV for legitimate software installation
level: high
```

---

## MITRE ATT&CK Mapping

### Common TTPs by Sigma Rule Type

| ATT&CK ID | Name | Common Sigma Category | Example |
|---|---|---|---|
| T1059.001 | PowerShell | process_creation | `-enc`, `IEX`, `DownloadString` |
| T1059.003 | Windows Command Shell | process_creation | `cmd.exe /c`, `/k` |
| T1059.005 | Visual Basic | process_creation | `wscript.exe`, `cscript.exe` |
| T1059.007 | JavaScript | process_creation | `mshta.exe`, `JScript` |
| T1003.001 | LSASS Memory | process_access (EID 10) | `lsass.exe` access |
| T1003.006 | DCSync | audit (EID 4662) | Replication Get Changes |
| T1055.001 | Process Injection | process_access (EID 8) | CreateRemoteThread |
| T1055.012 | Process Hollowing | process_creation | Unmap + SetThreadContext |
| T1078 | Valid Accounts | authentication | 4624, 4625 |
| T1098 | Account Manipulation | audit | 4720, 4723, 4724, 4732 |
| T1110 | Brute Force | authentication | 4625, SSH failures |
| T1136 | Create Account | audit | 4720 |
| T1486 | Data Encrypted for Impact | file_event | Mass file renames |
| T1505.003 | Web Shell | web | Suspicious POST |
| T1543.003 | Windows Service | service_installation | EID 4697, 7045 |
| T1546.003 | WMI Event Subscription | wmi_event | EID 19, 20, 21 |
| T1547.001 | Registry Run Keys | registry_set | CurrentVersion\Run |
| T1550.002 | Pass the Hash | authentication | NTLM + LogonType 9 |
| T1552.001 | Credentials in Files | file_event | Sensitive file access |
| T1562.001 | Disable AV | process_creation | MpPreference, sc stop |
| T1562.002 | Disable Event Logging | process_creation | wevtutil cl, auditpol |
| T1569.002 | Service Execution | process_creation | sc, psexec |
| T1572 | Protocol Tunneling | dns | DNS tunneling patterns |
| T1021.001 | RDP | network_connection | Port 3389 |
| T1021.002 | SMB/Admin Shares | network_connection | Port 445 |
| T1047 | WMI | wmi_event | wmic, WMI execution |
| T1190 | Exploit Public-Facing App | web | Known exploit patterns |

---

## Sigma Rule Management at Scale

### Repository Structure

```
sigma-rules/
├── rules/
│   ├── windows/
│   │   ├── builtin/                  # Windows built-in events (Event Log)
│   │   │   ├── security/             # Windows Security Event Log
│   │   │   │   ├── account_management/
│   │   │   │   ├── audit_policy/
│   │   │   │   ├── authentication/
│   │   │   │   ├── process_creation/
│   │   │   │   ├── service/
│   │   │   │   └── ...
│   │   │   ├── system/               # Windows System Event Log
│   │   │   ├── application/          # Windows Application Event Log
│   │   │   └── powershell/           # PowerShell Operational
│   │   ├── sysmon/                   # Sysmon-specific
│   │   │   ├── process_creation/
│   │   │   ├── network_connection/
│   │   │   ├── file_event/
│   │   │   ├── registry_event/
│   │   │   ├── image_load/
│   │   │   ├── process_access/
│   │   │   ├── dns_query/
│   │   │   ├── pipe_event/
│   │   │   └── wmi_event/
│   │   ├── malware/                  # Known malware family rules
│   │   │   ├── cobalt_strike/
│   │   │   ├── mimikatz/
│   │   │   ├── ransomwares/
│   │   │   └── backdoors/
│   │   └── office/                   # Office application events
│   ├── linux/
│   │   ├── auditd/
│   │   ├── syslog/
│   │   └── sshd/
│   ├── macos/
│   │   └── unifiedlog/
│   ├── network/
│   │   ├── zeek/
│   │   ├── suricata/
│   │   └── iptables/
│   ├── cloud/
│   │   ├── aws/
│   │   │   └── cloudtrail/
│   │   ├── azure/
│   │   │   ├── activity/
│   │   │   └── signin/
│   │   └── gcp/
│   │       └── audit/
│   ├── web/
│   │   ├── apache/
│   │   ├── nginx/
│   │   ├── iis/
│   │   └── tomcat/
│   └── application/
│       ├── exchange/
│       ├── sqlserver/
│       ├── docker/
│       └── kubernetes/
├── correlations/                     # Sigma v2 correlation rules
├── pipelines/                        # Custom pipelines
├── tests/
│   ├── test_rules.py
│   └── fixtures/                     # Test data
├── scripts/
│   ├── validate_all.py
│   ├── coverage_matrix.py
│   └── convert_all.py
├── .github/
│   └── workflows/
│       └── sigma-ci.yml
├── Coverage.md                       # MITRE ATT&CK coverage matrix
├── CHANGELOG.md
└── README.md
```

### Naming Conventions

```
{technique_keyword}_{description}_{scope}.yml

Examples:
- sysmon_powershell_encoded_command.yml
- win_security_dcsync.yml
- win_suspicious_mimikatz_image_load.yml
- lin_ssh_bruteforce.yml
- cloud_aws_iam_policy_abuse.yml
- web_webshell_access.yml
```

**Name prefix convention (official Sigma repo):**

| Prefix | Meaning |
|---|---|
| `win_` | Windows (any provider) |
| `sysmon_` | Sysmon-specific |
| `lnx_` | Linux |
| `mac_` | macOS |
| `web_` | Web server |
| `net_` | Network |
| `cloud_` | Cloud provider |
| `app_` | Application-specific |
| `corr_` | Correlation rule (v2) |

### Versioning

```yaml
# In rule
modified: 2024/06/27

# git-based versioning
git tag v2024.06.27 -m "June 2024 rule set"
```

### Quality Gates

```bash
# 1. Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('rule.yml'))"

# 2. Check with Sigma
sigma check rule.yml

# 3. Run tests
sigma check -t es-qs rule.yml

# 4. Validate UUID format
python -c "import uuid; uuid.UUID('f0f9e3b9-...')"

# 5. Check MITRE mapping
# Verify tag format (attack.tXXXX) against https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json

# 6. Lint (custom)
python scripts/lint_rule.py rule.yml
```

---

## Performance Optimization

### Field Selection

```yaml
# BAD — loose, scans many fields
detection:
    keywords:
        - 'malware'

# GOOD — specific field, faster
detection:
    selection:
        Image|endswith: '\malware.exe'
```

- Use specific field names over keyword search
- Prefer `endswith`/`startswith` over `contains` (smaller search space)
- Avoid `contains` on long string fields (CommandLine, Message)
- Use `EventID` as a pre-filter in `logsource`

### Modifier Choice

```yaml
# FAST — exact match
Image: 'C:\Windows\System32\cmd.exe'

# SLOWER — substring
CommandLine|contains: 'cmd'

# FASTEST when possible
EventID: 4688
```

**Modifier performance (fastest → slowest):**
1. `(none)` exact match
2. `startswith` prefix
3. `endswith` suffix
4. `contains` substring
5. `re` regex
6. `base64offset` (generates 3 variations)
7. `base64` (full decode + match)

### Condition Structure

```yaml
# BAD — conditions that can't short-circuit efficiently
condition: selection1 and selection2 and selection3

# GOOD — put most selective map first
detection:
    selection_fast:
        EventID: 4625
    selection_slow:
        TargetUserName|startswith: 'admin'
    condition: selection_fast and selection_slow
```

### Logsource Precision

```yaml
# COARSE (checks all Windows logs — slowest)
logsource:
    category: process_creation
    product: windows

# PRECISE (checks only Sysmon EID 1 — fastest)
logsource:
    category: process_creation
    product: windows
    service: sysmon
```

### Aggregation Performance

```yaml
# Aggregation rules (v2) are resource-intensive:
# - Larger timeframe = more memory
# - count_distinct > count()
# - window size matters

# BAD — very wide window, high memory
timeframe: 24h
condition: selection | count_distinct(TargetUserName) > 5

# GOOD — narrow window, fast
timeframe: 5m
condition: selection | count() > 10
```

---

## Common Pitfalls & Anti-Patterns

| Pitfall | Example | Problem | Fix |
|---|---|---|---|
| No filter section | `condition: selection` | High FP rate | Add `filter` to exclude known benign |
| Too broad keywords | `keywords: 'powershell'` | Matches every PowerShell use | Narrow to specific flags: `-enc` |
| Wrong logsource | `product: windows` for Linux rules | Rule never matches | Match `product` and `service` correctly |
| Missing logsource | No `logsource` | Rule applies to ALL logs (slow) | Always specify `category`, `product`, `service` |
| Idle UUID | Same UUID reused | Collisions | Each rule needs unique UUID v4 |
| Overly aggressive | `level: critical` for low-confidence rules | Alert fatigue | Match level to confidence |
| `contains` on Image | `Image|contains: 'powershell'` | Slow, matches paths containing "powershell" | Use `endswith` |
| No test cases | No `tests` section | Hard to validate | Always include test cases |
| `all of selection*` misuse | `all of selection*` with 15 maps | Never matches | Use `1 of selection*` for OR |
| Forgetting `definition` | No `definition` field | Unclear prerequisites | Document required log sources |
| Outdated tags | Old MITRE version | Mismatched TTPs | Keep tags current with MITRE releases |
| Empty falsepositives | `falsepositives: []` | No documentation | At minimum put "Unknown at this time" |
| Wildcard overload | `Image|contains: '*'` | Meaningless match | Remove wildcard-only values |
| Date format | `date: 2024/27/06` | Invalid date | Use YYYY/MM/DD |
| Correlating across log sources | One `logsource` for all selections | Events come from different sources | Use separate rules or v2 correlation |

---

## Testing & Validation

### Test Format Specification

```yaml
tests:
    # Standard field test
    - name: Description of test
      EventID: 4688
      Image: C:\Windows\System32\cmd.exe
      CommandLine: 'cmd.exe /c whoami'
      match: true

    # Field path with dots
    - name: Nested field test
      process.executable: 'C:\Windows\System32\cmd.exe'
      match: true

    # URL-based (fetch test data)
    - name: Remote test data
      url: https://raw.githubusercontent.com/.../test_evtx.evtx
      match: true
```

### Automated Testing

```bash
# Validate all rules in directory
for f in rules/**/*.yml; do
    sigma check "$f" || echo "FAIL: $f"
done

# Run tests for a single rule
sigma check -t es-qs -p winlogbeat rule.yml

# Run all tests for all rules
sigma check -t es-qs -p winlogbeat rules/

# With verbose output
sigma check -t splunk -p splunk_cim -v rule.yml
```

```python
# Automated validation script
from sigma.collection import SigmaCollection
from sigma.check import SigmaChecker
from sigma.backends.elasticsearch import ElasticsearchBackend
from sigma.pipelines.windows import sigma_pipeline_winlogbeat
import sys

rules = SigmaCollection.load_directory("rules/")
backend = ElasticsearchBackend(
    processing_pipeline=sigma_pipeline_winlogbeat()
)
checker = SigmaChecker(rules, backend)

results = checker.check_rules()
failed = [r for r in results if not r.passed]

if failed:
    for f in failed:
        print(f"FAIL: {f.rule.title} - {f.errors}")
    sys.exit(1)
else:
    print(f"All {len(results)} rules passed!")
```

---

## Sigma OSS Repositories & Feeds

| Resource | URL | Description |
|---|---|---|
| **Official Sigma Repository** | https://github.com/SigmaHQ/sigma | Main rule repository (1500+ rules) |
| **Sigma Spec** | https://github.com/SigmaHQ/sigma-specification | Sigma specification v1 and v2 |
| **pySigma** | https://github.com/SigmaHQ/pySigma | Python library for Sigma (modern) |
| **Sigma CLI** | https://github.com/SigmaHQ/sigma-cli | CLI for pySigma |
| **sigmac** | https://github.com/SigmaHQ/sigma/tree/master/tools | Legacy converter (Python 2+3) |
| **Uncoder.io** | https://uncoder.io | Web-based Sigma converter (SOC Prime) |
| **Sigma Rules Converted** | https://github.com/security-onion-solutions/securityonion-sigma | Pre-converted for Security Onion |
| **Azure Sentinel Sigma** | https://github.com/Azure/Azure-Sentinel/tree/master/Detections/Sigma | Azure Sentinel conversions |
| **Elastic Rules** | https://github.com/elastic/detection-rules | Elastic's rule set (Sigma-compatible) |
| **Splunk Security Content** | https://research.splunk.com/ | Splunk detection content (Sigma-related) |
| **CISA Sigma** | https://github.com/cisagov/cybersecurity-performance-analytics/tree/main/sigma | CISA's Sigma rules |
| **Sigconverter.io** | https://sigconverter.io | Online Sigma converter |
| **SOC Prime Detection Marketplace** | https://tdm.socprime.com | Commercial Sigma rule marketplace |

---

## Integration Ecosystem

| Platform | Integration Method | Notes |
|---|---|---|
| **Elastic Security** | pySigma Elasticsearch backend | Direct rule import via API |
| **Splunk ES** | pySigma Splunk backend + CIM | Rule → SPL search |
| **Microsoft Sentinel** | pySigma Azure Sentinel backend | KQL output, Logic App |
| **IBM QRadar** | pySigma QRadar backend | AQL output |
| **ArcSight ESM** | Manual CEF mapping | Custom parser needed |
| **LogRhythm** | Manual conversion | Limited Sigma support |
| **LogPoint** | pySigma LogPoint backend | Native Integration |
| **Chronicle (SecOps)** | pySigma BigQuery backend | SQL for BigQuery |
| **Grafana Loki** | pySigma Loki backend | LogQL rules |
| **Devo** | Manual conversion | Limited native support |
| **CrowdStrike Falcon** | pySigma CrowdStrike backend | Event Search API |
| **Palo Alto XSOAR** | Sigma rule → XSOAR playbook | Custom integration |
| **TheHive / Cortex** | Sigma analyzer | Rule import |
| **MISP** | Sigma export | Share rules as MISP events |
| **Wazuh** | Sigma → Wazuh rules | Custom conversion |
| **Security Onion** | Native Sigma support | Automatically converts |
| **SOC Prime** | Uncoder.io platform | Multi-platform conversion |

---

## Sigma CLI Reference

### sigmac — Legacy Tool

```bash
# Convert single rule
sigmac -t splunk -c splunk-windows.yml rule.yml

# Convert directory
sigmac -t es-qs -c winlogbeat.yml -r rules/ -o output/

# List targets
sigmac -l

# List configurations
sigmac -C

# Validate rule
sigmac -T rule.yml
```

### Sigma CLI (Modern)

```bash
# Conversion
sigma convert -t es-qs -p winlogbeat rule.yml
sigma convert -t splunk -p splunk_cim -r rules/ -o queries/

# Validation
sigma check rule.yml
sigma check -t es-qs -p winlogbeat rule.yml

# Info
sigma info rule.yml

# List available
sigma list targets
sigma list pipelines

# Plugin management
sigma plugin list
sigma plugin install pysigma-backend-splunk

# Configuration
sigma config --show
sigma config set default-backend splunk
sigma config set default-pipeline splunk_cim
```

---

## Appendix A: Quick Reference

### Rule Template (minimal)

```yaml
title: Rule Title
id: <uuid>
status: test
description: Brief description
author: Your Name
date: 2024/06/27
tags:
    - attack.tXXXX
logsource:
    category: <category>
    product: <product>
detection:
    selection:
        Field: 'value'
    condition: selection
falsepositives:
    - Unknown
level: medium
```

### UUID Generation

```bash
# Linux
uuidgen

# macOS
uuidgen

# Python
python -c "import uuid; print(uuid.uuid4())"

# PowerShell
[guid]::NewGuid().ToString()
```

### Common Field Names

| Sigma Field | Sysmon Field | Winlogbeat ECS | Splunk CIM |
|---|---|---|---|
| `EventID` | `EventID` | `event.code` | `EventCode` |
| `Image` | `Image` | `process.executable` | `Image` |
| `CommandLine` | `CommandLine` | `process.command_line` | `CommandLine` |
| `ParentImage` | `ParentImage` | `process.parent.executable` | `ParentImage` |
| `ParentCommandLine` | `ParentCommandLine` | `process.parent.command_line` | `ParentCommandLine` |
| `TargetFilename` | `TargetFilename` | `file.path` | `TargetFilename` |
| `SourceIp` | `SourceIp` | `source.ip` | `SourceIp` |
| `DestinationIp` | `DestinationIp` | `destination.ip` | `DestinationIp` |
| `DestinationPort` | `DestinationPort` | `destination.port` | `DestinationPort` |
| `ImageLoaded` | `ImageLoaded` | `dll.path` | `ImageLoaded` |
| `User` | `User` | `user.name` | `User` |
| `TargetObject` | `TargetObject` | `registry.path` | `TargetObject` |
| `PipeName` | `PipeName` | `pipe.name` | `PipeName` |
| `QueryName` | `QueryName` | `dns.question.name` | `QueryName` |

---

## Appendix B: Logsource Quick Reference

| category | product | service | Common Event IDs |
|---|---|---|---|
| `process_creation` | `windows` | `sysmon` | 1 |
| `process_creation` | `windows` | `security` | 4688 |
| `process_creation` | `windows` | `powershell` | 400, 800 |
| `process_creation` | `linux` | `auditd` | SYSCALL execve |
| `file_event` | `windows` | `sysmon` | 11 |
| `file_event` | `windows` | `security` | 4663 |
| `file_event` | `linux` | `auditd` | PATH, SYSCALL |
| `registry_set` | `windows` | `sysmon` | 13 |
| `registry_delete` | `windows` | `sysmon` | 12 |
| `registry_event` | `windows` | `security` | 4657 |
| `network_connection` | `windows` | `sysmon` | 3 |
| `network_connection` | `windows` | `security` | 5156, 5157 |
| `network_connection` | `network` | `zeek` | conn.log |
| `dns` | `windows` | `sysmon` | 22 |
| `dns` | `network` | `zeek` | dns.log |
| `image_load` | `windows` | `sysmon` | 7 |
| `image_load` | `windows` | `sysmon` | 23 (deleted) |
| `process_access` | `windows` | `sysmon` | 10 |
| `process_access` | `windows` | `sysmon` | 8 (CreateRemoteThread) |
| `wmi_event` | `windows` | `sysmon` | 19, 20, 21 |
| `pipe_event` | `windows` | `sysmon` | 17, 18 |
| `raw_access_thread` | `windows` | `sysmon` | 9 |
| `authentication` | `windows` | `security` | 4624, 4625, 4768, 4769, 4776 |
| `authentication` | `linux` | `syslog` | sshd |
| `service_installation` | `windows` | `security` | 4697 |
| `service_installation` | `windows` | `system` | 7045 |
| `scheduled_task` | `windows` | `security` | 4698, 4699, 4702 |
| `audit` | `windows` | `security` | 4719, 4720–4765, 4902 |
| `web` | `linux` | `apache` | access.log |
| `web` | `linux` | `nginx` | access.log |
| `web` | `windows` | `iis` | w3c log |
| `cloud` | `aws` | `cloudtrail` | CloudTrail events |
| `cloud` | `azure` | `activity` | Azure Activity |
| `cloud` | `azure` | `signin` | Azure AD Sign-in |
| `cloud` | `gcp` | `audit` | Cloud Audit Log |
| `kubernetes` | `cloud` | `k8s` | Kubernetes audit |

---

## Appendix C: Coverage Matrix Template

Track your Sigma rule coverage against MITRE ATT&CK:

```csv
Tactic,Technique,ID,Sigma Rule Title,Status,Log Source,Level,Last Updated
Execution,PowerShell,T1059.001,Powershell Encoded Command,Production,Windows Sysmon EID 1,High,2024-06-27
Execution,Command and Scripting Interpreter,T1059.003,Suspicious Cmd Patterns,Production,Windows Security 4688,Medium,2024-05-15
Credential Access,LSASS Memory,T1003.001,Mimikatz Image Load,Production,Windows Sysmon EID 7,Critical,2024-06-01
...
```

---

## Additional Real-World Rule Examples (21–40)

### 21. Cobalt Strike — Named Pipe Metasploit Pattern

```yaml
title: Cobalt Strike — Named Pipe Metasploit Patterns
id: d1f3a5b7-9c2e-4f6a-8b0d-1e3f5a7b9c0d
status: stable
description: Detects Cobalt Strike Beacon using known Metasploit-style named pipe patterns
references:
    - https://www.cobaltstrike.com/
    - https://attack.mitre.org/techniques/T1574/002/
author: Defensive Engineering Team
date: 2022/03/15
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1574.002
    - attack.t1055
logsource:
    category: pipe_event
    product: windows
    service: sysmon
detection:
    selection_named_pipe:
        EventID:
            - 17    # Pipe Created
            - 18    # Pipe Connected
        PipeName|contains:
            - '\msf_'
            - '\meterpreter_'
            - '\postex_'
            - '\stderr_'
            - '\stdin_'
            - '\stdout_'
            - '\wkssvc_'            # Known Cobalt Strike named pipe
    selection_network:
        EventID: 3
        DestinationPort:
            - 80
            - 443
            - 4444
            - 5555
            - 8080
            - 8443
    condition: selection_named_pipe or selection_network
falsepositives:
    - Metasploit penetration testing
level: critical
```

### 22. Cobalt Strike — Process Injection with Callback

```yaml
title: Cobalt Strike — Process Injection Followed by Network Callback
id: f2a4b6c8-0d1e-3f5a-7b9c-1d3f5a7b9c0d
status: stable
description: Detects Cobalt Strike injection pattern — process creation in Office app then network callback
references:
    - https://www.cobaltstrike.com/
    - https://attack.mitre.org/techniques/T1055/
author: Defensive Engineering Team
date: 2022/06/01
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1055.001
    - attack.defense_evasion
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection_parent:
        ParentImage|endswith:
            - '\winword.exe'
            - '\excel.exe'
            - '\outlook.exe'
            - '\powerpnt.exe'
            - '\wmplayer.exe'
            - '\firefox.exe'
            - '\chrome.exe'
            - '\iexplore.exe'
        Image|endswith:
            - '\powershell.exe'
            - '\cmd.exe'
            - '\regsvr32.exe'
            - '\rundll32.exe'
            - '\mshta.exe'
            - '\cscript.exe'
            - '\wscript.exe'
    condition: selection_parent
falsepositives:
    - Office add-ins that spawn legitimate processes
    - Web browsers spawning helper processes
level: high
```

### 23. Emotet — Office Macro with WMI and Network Connection

```yaml
title: Emotet — Office Macro Process with WMI and Network Connections
id: e3b5c7d9-1f2a-4b6c-8d0e-2f4a6b8c0d1e
status: stable
description: Detects Emotet dropper pattern — Office product spawning WMI and making network connections
references:
    - https://malpedia.caad.fkie.fraunhofer.de/details/win.emotet
    - https://attack.mitre.org/techniques/T1204/002/
author: Defensive Engineering Team
date: 2023/01/20
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1204.002
    - attack.t1059.001
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection_office:
        ParentImage|endswith:
            - '\winword.exe'
            - '\excel.exe'
            - '\outlook.exe'
    selection_child:
        Image|endswith:
            - '\wscript.exe'
            - '\cscript.exe'
            - '\powershell.exe'
            - '\regsvr32.exe'
    selection_callback:
        Image|endswith:
            - '\powershell.exe'
            - '\wscript.exe'
            - '\cscript.exe'
        CommandLine|contains:
            - '.downloadstring'
            - '.downloadfile'
            - 'http://'
            - 'https://'
            - 'webclient'
            - 'winhttp'
            - 'xmlhttp'
    condition: selection_office and selection_child and selection_callback
falsepositives:
    - Legitimate Office macros with network downloads
level: high
```

### 24. Emotet — RunDLL32 with DLL from Temp

```yaml
title: Emotet/Loader — Rundll32 Execution from Temp Directory
id: f4c6d8e0-2a3b-4c7d-9e1f-3a5b7c9d1e2f
status: stable
description: Detects Rundll32 executing a DLL from temp directories, common in Emotet and other loaders
references:
    - https://malpedia.caad.fkie.fraunhofer.de/details/win.emotet
    - https://attack.mitre.org/techniques/T1218/011/
author: Defensive Engineering Team
date: 2023/02/10
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1218.011
    - attack.execution
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        Image|endswith: '\rundll32.exe'
        CommandLine|contains:
            - '\AppData\Local\Temp\'
            - '\AppData\Roaming\'
            - '\Windows\Temp\'
            - '\TEMP\'
            - '%TEMP%'
    filter:
        CommandLine|contains:
            - 'appwiz.cpl'
            - 'shell32.dll'
            - 'printui.dll'
            - 'ieframe.dll'
            - 'dfshim.dll'
    condition: selection and not filter
falsepositives:
    - Legitimate software installers using temp directories
level: high
```

### 25. IcedID / Bumblebee — Process Hollowing via Unmap

```yaml
title: Process Hollowing — NtUnmapViewOfSection with Process Creation
id: a5b7c9d1-3e4f-5a8b-9c0d-2e4f6a8b0c1d
status: experimental
description: Detects process hollowing technique using ZwUnmapViewOfSection followed by process creation
references:
    - https://attack.mitre.org/techniques/T1055/012/
    - https://redcanary.com/blog/process-hollowing/
author: Defensive Engineering Team
date: 2023/04/15
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1055.012
logsource:
    category: image_load
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 7
        ImageLoaded|contains:
            - 'ntdll.dll'
    filter:
        Image|startswith:
            - 'C:\Windows\System32\'
            - 'C:\Windows\SysWOW64\'
            - 'C:\Program Files\'
            - 'C:\Program Files (x86)\'
    condition: selection and not filter
falsepositives:
    - Security tools that monitor process creation
level: medium
```

### 26. TrickBot — SystemInfo Gathering

```yaml
title: TrickBot — System Information Discovery via systeminfo
id: b6c8d0e2-4f5a-6b9c-0d1e-3f5a7b9c0d1e
status: stable
description: Detects TrickBot executing systeminfo and other discovery commands
references:
    - https://malpedia.caad.fkie.fraunhofer.de/details/win.trickbot
    - https://attack.mitre.org/techniques/T1082/
author: Defensive Engineering Team
date: 2023/03/01
modified: 2024/06/27
tags:
    - attack.discovery
    - attack.t1082
    - attack.t1083
    - attack.t1069
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        Image|endswith:
            - '\systeminfo.exe'
            - '\whoami.exe'
            - '\netstat.exe'
            - '\ipconfig.exe'
            - '\tasklist.exe'
            - '\qwinsta.exe'
            - '\qprocess.exe'
        CommandLine|contains:
            - '/ALL'
            - '-ano'
            - '/SVC'
    condition: selection
falsepositives:
    - IT troubleshooting
    - Scripts collecting system state
level: medium
```

### 27. QakBot — Process Injection via WMI

```yaml
title: QakBot — WMI Process Creation with Callback
id: c7d9e1f3-5a6b-7c0d-1e2f-4a6b8c0d1e2f
status: experimental
description: Detects QakBot using WMI for process execution with subsequent network connections
references:
    - https://malpedia.caad.fkie.fraunhofer.de/details/win.qakbot
    - https://attack.mitre.org/techniques/T1047/
author: Defensive Engineering Team
date: 2023/05/20
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1047
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        Image|endswith: '\wmiprvse.exe'
        CommandLine|contains:
            - 'powershell'
            - 'cmd.exe'
            - 'rundll32'
            - 'regsvr32'
    condition: selection
falsepositives:
    - Legitimate WMI-based management software (SCCM, PDQ)
level: high
```

### 28. Ryuk / Conti — Service Stop and Shadow Copy Deletion

```yaml
title: Ransomware — Service Termination and Volume Shadow Copy Deletion
id: d8e0f2a4-6b7c-8d1e-2f3a-5b7c9d1e2f3a
status: stable
description: Detects ransomware killing services and deleting shadow copies (Ryuk, Conti, LockBit)
references:
    - https://attack.mitre.org/techniques/T1486/
    - https://attack.mitre.org/techniques/T1490/
author: Defensive Engineering Team
date: 2023/06/10
modified: 2024/06/27
tags:
    - attack.impact
    - attack.t1486
    - attack.t1490
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection_shadow:
        Image|endswith:
            - '\vssadmin.exe'
            - '\wmic.exe'
            - '\wbadmin.exe'
            - '\bcdedit.exe'
            - '\diskshadow.exe'
        CommandLine|contains:
            - 'delete shadows'
            - 'shadowcopy'
            - 'resize shadowstorage'
            - 'delete catalog'
            - 'bootsect'
            - '/set {default} recoveryenabled'
    selection_service:
        Image|endswith:
            - '\net.exe'
            - '\sc.exe'
            - '\wmic.exe'
            - '\powershell.exe'
        CommandLine|contains:
            - 'stop'
            - '/y'
        CommandLine|contains:
            - 'SQL'
            - 'sqlserver'
            - 'backup'
            - 'memtas'
            - 'mepocs'
            - 'vss'
            - 'veeam'
            - 'backup'
            - 'Sophos'
            - 'McAfee'
            - 'Defender'
            - 'Sentinel'
    condition: 1 of selection_*
falsepositives:
    - Legitimate backup and recovery operations
    - System maintenance activities
level: critical
```

### 29. LockBit — Rapid File Encryption Pattern

```yaml
title: LockBit — Extensive File Modifications in Temp Directory
id: e9f1a3b5-7c8d-9e2f-3a4b-6c8d0e2f3a4b
status: stable
description: Detects LockBit ransomware encrypting files by monitoring mass file modifications
references:
    - https://attack.mitre.org/techniques/T1486/
    - https://blogs.blackberry.com/en/2022/10/lockbit-3-0-analyst-notes
author: Defensive Engineering Team
date: 2023/07/01
modified: 2024/06/27
tags:
    - attack.impact
    - attack.t1486
logsource:
    category: file_event
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 11
        TargetFilename|contains:
            - '.lockbit'
            - '.lockbit3'
            - '.abcd'
            - '.ekpt'            # LockBit encrypted extension
            - '.shifr'
    timeframe: 5m
    condition: selection | count() > 20
falsepositives:
    - Legitimate file renaming tools
level: critical
```

### 30. PrintNightmare (CVE-2021-34527)

```yaml
title: PrintNightmare — Spoolsv Child Process or DLL Load
id: f0a2b4c6-8d9e-0f1a-2b3c-5d7e9f1a2b3c
status: stable
description: Detects exploitation of PrintNightmare vulnerability via spoolsv.exe spawning processes or loading suspicious DLLs
references:
    - https://attack.mitre.org/techniques/T1068/
    - https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527
author: Defensive Engineering Team
date: 2021/07/10
modified: 2024/06/27
tags:
    - attack.privilege_escalation
    - attack.t1068
    - cve.2021-34527
    - cve.2021-1675
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        ParentImage|endswith: '\spoolsv.exe'
        Image|endswith:
            - '\powershell.exe'
            - '\cmd.exe'
            - '\rundll32.exe'
            - '\regsvr32.exe'
            - '\wscript.exe'
            - '\cscript.exe'
            - '\mshta.exe'
            - '\powershell_ise.exe'
    filter_rpc:
        CommandLine|contains:
            - 'rpc'
            - 'Rpc'
    condition: selection and not filter_rpc
falsepositives:
    - Print management software that interacts with spoolsv
level: critical
```

### 31. Log4Shell (CVE-2021-44228)

```yaml
title: Log4Shell — JNDI Injection Attempt in Web Logs
id: a1b3c5d7-9e0f-1a2b-3c4d-6e8f0a1b2c3d
status: stable
description: Detects Log4Shell (CVE-2021-44228) exploitation attempts via JNDI LDAP/RMI patterns in logs
references:
    - https://attack.mitre.org/techniques/T1190/
    - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-44228
author: Defensive Engineering Team
date: 2021/12/15
modified: 2024/06/27
tags:
    - attack.initial_access
    - attack.t1190
    - cve.2021-44228
logsource:
    category: web
    product: linux
    service: apache
detection:
    selection:
        cs-uri-query|contains:
            - 'jndi:ldap://'
            - 'jndi:rmi://'
            - 'jndi:ldaps://'
            - 'jndi:dns://'
            - 'jndi:iiop://'
            - '${jndi:'
            - '${env:'
            - '${sys:'
    condition: selection
falsepositives:
    - Security scanners testing for vulnerability
level: critical
```

### 32. Log4Shell — Outbound LDAP Query

```yaml
title: Log4Shell — Outbound LDAP Connection from Java Process
id: b2c4d6e8-0a1b-2c3d-4e5f-7a9b0c1d2e3f
status: stable
description: Detects Java process initiating outbound LDAP connections, indicative of Log4Shell exploitation
references:
    - https://attack.mitre.org/techniques/T1190/
    - https://www.lunasec.io/docs/blog/log4j-zero-day/
author: Defensive Engineering Team
date: 2021/12/20
modified: 2024/06/27
tags:
    - attack.lateral_movement
    - attack.t1190
    - cve.2021-44228
logsource:
    category: network_connection
    product: linux
    service: auditd
detection:
    selection:
        Image|endswith: '\java.exe'
        DestinationPort: 389
        Protocol: 'tcp'
    condition: selection
falsepositives:
    - Legitimate LDAP authentication from Java applications
level: critical
```

### 33. Zerologon (CVE-2020-1472)

```yaml
title: Zerologon — Netlogon Elevation of Privilege Attempts
id: c3d5e7f9-1b2c-3d4e-5f6a-8b9c0d1e2f3a
status: stable
description: Detects Zerologon exploitation attempts using multiple Netlogon requests with zero-computer-key authentication
references:
    - https://attack.mitre.org/techniques/T1068/
    - https://msrc.microsoft.com/update-guide/vulnerability/CVE-2020-1472
author: Defensive Engineering Team
date: 2020/09/20
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1068
    - cve.2020-1472
logsource:
    category: authentication
    product: windows
    service: security
detection:
    selection:
        EventID: 5805          # Netlogon authentication failure
        LogonProcessName: 'Netlogon'
    timeframe: 5m
    condition: selection | count() > 100
falsepositives:
    - Network issues causing authentication failures
level: critical
```

### 34. ProxyShell (CVE-2021-34473, CVE-2021-34523, CVE-2021-31207)

```yaml
title: ProxyShell — Exchange PowerShell Virtual Directory Access
id: d4e6f8a0-2c3d-4e5f-6a7b-9c0d1e2f3a4b
status: stable
description: Detects ProxyShell attack chain via Exchange PowerShell virtual directory access
references:
    - https://attack.mitre.org/techniques/T1190/
    - https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34473
author: Defensive Engineering Team
date: 2021/08/15
modified: 2024/06/27
tags:
    - attack.initial_access
    - attack.t1190
    - cve.2021-34473
    - cve.2021-34523
    - cve.2021-31207
logsource:
    category: web
    product: windows
    service: iis
detection:
    selection:
        cs-uri-query|contains:
            - '/autodiscover/autodiscover.json'
            - '/ecp/'
            - '/powershell/'
        cs-method: 'POST'
    condition: selection
falsepositives:
    - Exchange health checks
    - Legitimate PowerShell remoting to Exchange
level: critical
```

### 35. AWS — Root Account Login

```yaml
title: AWS — Root Account Login without MFA
id: e5f7a9b1-3d4e-5f6a-7b8c-0d1e2f3a4b5c
status: stable
description: Detects root user login to AWS console without MFA authentication
references:
    - https://attack.mitre.org/techniques/T1078/
    - https://docs.aws.amazon.com/IAM/latest/UserGuide/root-user.html
author: Defensive Engineering Team
date: 2023/08/01
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1078
logsource:
    service: cloudtrail
    product: aws
detection:
    selection:
        eventName: 'ConsoleLogin'
        userIdentity.type: 'Root'
        additionalEventData.MFAUsed: 'No'
    filter_mfa:
        additionalEventData.MFAUsed: 'Yes'
    filter_ip:
        sourceIPAddress|cidr: '10.0.0.0/8'
    condition: selection and not filter_mfa and not filter_ip
falsepositives:
    - Emergency break-glass procedures
    - AWS support across accounts
level: critical
```

### 36. AWS — S3 Bucket Public Access Modification

```yaml
title: AWS — S3 Bucket Policy Changed to Public Access
id: f6a8b0c2-4e5f-6a7b-8c9d-1e2f3a4b5c6d
status: stable
description: Detects changes to S3 bucket policies that allow public read/write access
references:
    - https://attack.mitre.org/techniques/T1530/
    - https://docs.aws.amazon.com/AmazonS3/latest/dev/access-control-block-public-access.html
author: Defensive Engineering Team
date: 2023/09/01
modified: 2024/06/27
tags:
    - attack.collection
    - attack.t1530
logsource:
    service: cloudtrail
    product: aws
detection:
    selection:
        eventName:
            - 'PutBucketAcl'
            - 'PutBucketPolicy'
            - 'DeleteBucketPolicy'
            - 'PutBucketPublicAccessBlock'
        requestParameters.bucketName|startswith:
            - 'logs'
            - 'backup'
            - 'prod'
            - 'secret'
            - 'confidential'
    selection_public:
        requestParameters.AccessControlPolicy.AccessControlList.Grant.URI|contains:
            - 'http://acs.amazonaws.com/groups/global/AllUsers'
            - 'http://acs.amazonaws.com/groups/global/AuthenticatedUsers'
    condition: selection and selection_public
falsepositives:
    - Authorized security team creating public data sets
    - Authorized static website hosting
level: high
```

### 37. Azure — Privileged Role Activation

```yaml
title: Azure AD — Privileged Role Activation (PIM)
id: a7b9c1d3-5f6a-7b8c-9d0e-2f3a4b5c6d7e
status: stable
description: Detects activation of Azure AD Privileged Identity Management (PIM) roles
references:
    - https://attack.mitre.org/techniques/T1078/
    - https://docs.microsoft.com/en-us/azure/active-directory/privileged-identity-management/
author: Defensive Engineering Team
date: 2023/10/01
modified: 2024/06/27
tags:
    - attack.privilege_escalation
    - attack.t1078
logsource:
    service: audit
    product: azure
detection:
    selection:
        operationName: 'Activate role'
        properties.role|contains:
            - 'Global Administrator'
            - 'Exchange Administrator'
            - 'SharePoint Administrator'
            - 'Application Administrator'
            - 'Security Administrator'
            - 'Privileged Role Administrator'
            - 'Conditional Access Administrator'
            - 'User Administrator'
    condition: selection
falsepositives:
    - Authorized PIM activations by IT staff
level: high
```

### 38. GCP — IAM Policy Change

```yaml
title: GCP — IAM Policy Modification for Sensitive Roles
id: b8c0d2e4-6a7b-8c9d-0e1f-3a4b5c6d7e8f
status: experimental
description: Detects modifications to IAM policies granting sensitive roles to new principals
references:
    - https://attack.mitre.org/techniques/T1098/
    - https://cloud.google.com/iam/docs/understanding-roles
author: Defensive Engineering Team
date: 2023/11/01
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1098
logsource:
    service: audit
    product: gcp
detection:
    selection:
        methodName: 'SetIamPolicy'
        serviceName:
            - 'iam.googleapis.com'
            - 'cloudresourcemanager.googleapis.com'
    selection_role:
        binding.role|contains:
            - 'roles/owner'
            - 'roles/editor'
            - 'roles/admin'
            - 'roles/iam.securityAdmin'
            - 'roles/iam.roleAdmin'
    condition: selection and selection_role
falsepositives:
    - Infrastructure-as-Code automation (Terraform, Pulumi)
level: high
```

### 39. Kubernetes — Privileged Pod Creation

```yaml
title: Kubernetes — Privileged Container Created
id: c9d1e3f5-7a8b-9c0d-1e2f-4a5b6c7d8e9f
status: stable
description: Detects creation of a container with privileged security context
references:
    - https://attack.mitre.org/techniques/T1610/
    - https://kubernetes.io/docs/concepts/security/pod-security-standards/
author: Defensive Engineering Team
date: 2023/12/01
modified: 2024/06/27
tags:
    - attack.privilege_escalation
    - attack.t1610
logsource:
    service: k8s
    product: cloud
detection:
    selection:
        verb: 'create' or 'update'
        objectRef.resource:
            - 'pods'
            - 'deployments'
            - 'statefulsets'
            - 'daemonsets'
            - 'jobs'
            - 'cronjobs'
    selection_privileged:
        requestObject.spec.containers.securityContext.privileged: 'true'
    selection_hostpid:
        requestObject.spec.hostPID: 'true'
    selection_hostnet:
        requestObject.spec.hostNetwork: 'true'
    condition: selection and (selection_privileged or selection_hostpid or selection_hostnet)
falsepositives:
    - Authorized monitoring agents (requires host access)
    - Authorized system daemons
level: high
```

### 40. Kubernetes — Secrets Enumeration

```yaml
title: Kubernetes — Secrets Enumerated or Exported
id: d0e2f4a6-8b9c-0d1e-2f3a-5b6c7d8e9f0a
status: stable
description: Detects enumeration of Kubernetes secrets, potentially credential access
references:
    - https://attack.mitre.org/techniques/T1552/007/
    - https://kubernetes.io/docs/concepts/configuration/secret/
author: Defensive Engineering Team
date: 2024/01/01
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1552.007
logsource:
    service: k8s
    product: cloud
detection:
    selection:
        verb: 'list' or 'get' or 'watch'
        objectRef.resource: 'secrets'
    filter:
        user.username|startswith:
            - 'system:'
            - 'kube'
    condition: selection and not filter
falsepositives:
    - Authorized Kubernetes operators
    - CI/CD pipelines accessing secrets
level: high
```

---

## More Real-World Rules (41–60)

### 41. Linux — Crontab Persistence

```yaml
title: Linux — Cron Job Created or Modified
id: e1f3a5b7-9c0d-1e2f-3a4b-6c7d8e9f0a1b
status: stable
description: Detects creation or modification of cron jobs, a common persistence mechanism
references:
    - https://attack.mitre.org/techniques/T1053/003/
author: Defensive Engineering Team
date: 2023/03/15
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1053.003
    - attack.privilege_escalation
logsource:
    category: file_event
    product: linux
    service: auditd
detection:
    selection:
        type: 'SYSCALL'
        syscall: 'open' or 'openat'
        name|contains:
            - '/var/spool/cron/'
            - '/etc/cron.d/'
            - '/etc/crontab'
            - '/etc/cron.hourly/'
            - '/etc/cron.daily/'
            - '/etc/cron.weekly/'
            - '/etc/cron.monthly/'
        name|endswith:
            - '.sh'
            - '.py'
            - '.pl'
    condition: selection
falsepositives:
    - Authorized system administrators
    - Package manager installing cron jobs
level: high
```

### 42. Linux — SSH Key Exfiltration

```yaml
title: Linux — SSH Authorized Keys Modified
id: f2a4b6c8-0d1e-2f3a-4b5c-7d8e9f0a1b2c
status: stable
description: Detects modification of SSH authorized_keys files, potentially persistence via SSH keys
references:
    - https://attack.mitre.org/techniques/T1098/004/
author: Defensive Engineering Team
date: 2023/04/01
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1098.004
logsource:
    category: file_event
    product: linux
    service: auditd
detection:
    selection:
        type: 'SYSCALL' or 'PATH'
        name|contains:
            - '.ssh/authorized_keys'
            - '.ssh/authorized_keys2'
            - '/root/.ssh'
    filter:
        uid: 0               # Root is expected to manage keys
    condition: selection and not filter
falsepositives:
    - Users legitimately adding their own SSH keys
level: high
```

### 43. macOS — Gatekeeper Bypass

```yaml
title: macOS — Gatekeeper Bypass via xattr
id: a3b5c7d9-1e2f-3a4b-5c6d-8e9f0a1b2c3d
status: stable
description: Detects attempts to bypass macOS Gatekeeper using xattr to remove quarantine attributes
references:
    - https://attack.mitre.org/techniques/T1553/
    - https://objective-see.com/blog/blog_0x72.html
author: Defensive Engineering Team
date: 2023/05/01
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1553
logsource:
    category: process_creation
    product: macos
    service: esf
detection:
    selection:
        Image|endswith: '/xattr'
        CommandLine|contains:
            - 'com.apple.quarantine'
            - '-dr'
            - '-d'
    condition: selection
falsepositives:
    - Developers removing quarantine flags from legitimate downloaded SDKs
level: high
```

### 44. macOS — Launch Daemon Persistence

```yaml
title: macOS — Launch Daemon or Agent Created
id: b4c6d8e0-2f3a-4b5c-6d7e-9f0a1b2c3d4e
status: stable
description: Detects creation of LaunchDaemons or LaunchAgents for persistence
references:
    - https://attack.mitre.org/techniques/T1543/001/
author: Defensive Engineering Team
date: 2023/06/01
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1543.001
    - attack.privilege_escalation
logsource:
    category: file_event
    product: macos
    service: esf
detection:
    selection:
        name|contains:
            - '/Library/LaunchDaemons/'
            - '/Library/LaunchAgents/'
            - '~/Library/LaunchAgents/'
        name|endswith: '.plist'
    condition: selection
falsepositives:
    - Software installation adding legitimate plists
level: high
```

### 45. Phishing — Suspicious Email Attachment

```yaml
title: Phishing — Suspicious Attachment Types Detected in Email
id: c5d7e9f1-3a4b-5c6d-7e8f-0a1b2c3d4e5f
status: stable
description: Detects emails with suspicious attachment types commonly used in phishing campaigns
references:
    - https://attack.mitre.org/techniques/T1566/001/
author: Defensive Engineering Team
date: 2023/07/01
modified: 2024/06/27
tags:
    - attack.initial_access
    - attack.t1566.001
logsource:
    category: email
    product: office
    service: 365
detection:
    selection:
        AttachmentName|endswith:
            - '.exe'
            - '.vbs'
            - '.vbe'
            - '.ps1'
            - '.psm1'
            - '.js'
            - '.jse'
            - '.wsf'
            - '.wsh'
            - '.hta'
            - '.docm'
            - '.xlsm'
            - '.pptm'
            - '.jar'
            - '.msi'
            - '.scr'
            - '.cpl'
    selection_ext:
        AttachmentName|re: '\.(doc|xls|ppt|pdf)\.(exe|vbs|js|ps1)$'  # Double extension
    condition: selection or selection_ext
falsepositives:
    - Business workflows that rely on executable attachments
    - Signed software installers from trusted vendors
level: high
```

### 46. Exchange — Suspicious Mail Forwarding Rule

```yaml
title: Exchange — Suspicious Mail Forwarding Rule Created
id: d6e8f0a2-4b5c-6d7e-8f9a-1b2c3d4e5f6a
status: stable
description: Detects creation of mailbox forwarding rules to external domains, potentially data exfiltration
references:
    - https://attack.mitre.org/techniques/T1114/003/
author: Defensive Engineering Team
date: 2023/08/01
modified: 2024/06/27
tags:
    - attack.collection
    - attack.t1114.003
logsource:
    category: email
    product: office
    service: 365
detection:
    selection:
        Operation:
            - 'New-InboxRule'
            - 'Set-Mailbox'
            - 'Set-MailboxFolder'
        Parameters|contains:
            - 'ForwardTo'
            - 'ForwardingAddress'
            - 'ForwardingSmtpAddress'
            - 'RedirectTo'
    selection_external:
        Parameters|contains:
            - '@gmail.com'
            - '@yahoo.com'
            - '@outlook.com'
            - '@hotmail.com'
            - '@protonmail.com'
            - '@aol.com'
            - '@mail.ru'
            - '@yandex.com'
            - '@tutanota.com'
    condition: selection and selection_external
falsepositives:
    - Authorized business forwarding to external partners
level: high
```

### 47. SQL Server — Suspicious Query Pattern

```yaml
title: SQL Server — Suspicious Query Pattern (Possible SQL Injection)
id: e7f9a1b3-5c6d-7e8f-9a0b-2c3d4e5f6a7b
status: experimental
description: Detects suspicious SQL queries that might indicate SQL injection or data exfiltration
references:
    - https://attack.mitre.org/techniques/T1190/
author: Defensive Engineering Team
date: 2023/09/01
modified: 2024/06/27
tags:
    - attack.initial_access
    - attack.t1190
logsource:
    category: application
    product: windows
    service: mssql
detection:
    selection:
        message|contains:
            - 'xp_cmdshell'
            - 'xp_regwrite'
            - 'xp_regread'
            - 'xp_dirtree'
            - 'xp_subdirs'
            - 'sp_configure'
            - 'OPENROWSET'
            - 'OPENDATASOURCE'
            - 'BULK INSERT'
            - 'EXEC xp_'
            - 'WAITFOR DELAY'
            - 'BENCHMARK('
    condition: selection
falsepositives:
    - Authorized DBA activity
    - Database maintenance scripts
level: high
```

### 48. SQL Server — Suspicious User Added to sysadmin Role

```yaml
title: SQL Server — User Added to sysadmin Fixed Server Role
id: f8a0b2c4-6d7e-8f9a-0b1c-3d4e5f6a7b8c
status: stable
description: Detects when a user is added to the sysadmin fixed server role in SQL Server
references:
    - https://attack.mitre.org/techniques/T1098/
author: Defensive Engineering Team
date: 2023/10/01
modified: 2024/06/27
tags:
    - attack.persistence
    - attack.t1098
    - attack.privilege_escalation
logsource:
    category: application
    product: windows
    service: mssql
detection:
    selection:
        message|contains:
            - 'ALTER SERVER ROLE'
            - 'sysadmin'
            - 'ADD MEMBER'
    condition: selection
falsepositives:
    - Authorized DBA adding new administrators
level: critical
```

### 49. Docker — Container Access to Host Filesystem

```yaml
title: Docker — Container Mounted Host Filesystem
id: a9b1c3d5-7e8f-9a0b-1c2d-4e5f6a7b8c9d
status: experimental
description: Detects Docker containers created with host filesystem mounts, potentially container escape
references:
    - https://attack.mitre.org/techniques/T1611/
author: Defensive Engineering Team
date: 2023/11/01
modified: 2024/06/27
tags:
    - attack.privilege_escalation
    - attack.t1611
logsource:
    category: process_creation
    product: linux
    service: auditd
detection:
    selection:
        Image|endswith: '/docker'
        CommandLine|contains:
            - '-v /'
            - '--volume /'
            - '-v /etc'
            - '-v /root'
            - '-v /var/run/docker.sock'
            - '/:/host'
            - '--privileged'
    condition: selection
falsepositives:
    - Authorized monitoring containers
    - Infrastructure containers needing host access
level: high
```

### 50. Docker — Container Escape via Debug Mode

```yaml
title: Docker — Container Started with Elevated Capabilities
id: b0c2d4e6-8f9a-0b1c-2d3e-5f6a7b8c9d0e
status: experimental
description: Detects Docker containers started with elevated Linux capabilities
references:
    - https://attack.mitre.org/techniques/T1611/
author: Defensive Engineering Team
date: 2023/12/01
modified: 2024/06/27
tags:
    - attack.privilege_escalation
    - attack.t1611
logsource:
    category: process_creation
    product: linux
    service: auditd
detection:
    selection:
        Image|endswith: '/docker'
        CommandLine|contains:
            - '--cap-add=SYS_ADMIN'
            - '--cap-add=SYS_PTRACE'
            - '--cap-add=SYS_MODULE'
            - '--cap-add=DAC_READ_SEARCH'
            - '--cap-add=NET_ADMIN'
            - '--cap-add=SYS_RAWIO'
            - '--security-opt seccomp=unconfined'
            - '--security-opt apparmor=unconfined'
    condition: selection
falsepositives:
    - Authorized debugging containers
level: high
```

### 51. OT/ICS — Unusual Modbus Command

```yaml
title: OT/ICS — Suspicious Modbus Function Code Usage
id: c1d3e5f7-9a0b-1c2d-3e4f-6a7b8c9d0e1f
status: experimental
description: Detects unusual Modbus function codes in OT/ICS network traffic
references:
    - https://attack.mitre.org/techniques/T0843/
    - https://modbus.org/
author: Defensive Engineering Team
date: 2024/01/15
modified: 2024/06/27
tags:
    - attack.impact
    - attack.t0843
    - attack.t0883
    - ot.ics
logsource:
    category: network_connection
    product: network
    service: zeek
detection:
    selection:
        service: 'modbus'
    selection_codes:
        modbus.function_code:
            - 5   # Write Single Coil
            - 6   # Write Single Register
            - 15  # Write Multiple Coils
            - 16  # Write Multiple Registers
            - 8   # Diagnostics
            - 20  # File Record Access
            - 21  # Write Mask Register
    condition: selection and selection_codes
falsepositives:
    - SCADA engineering workstations
    - Authorized PLC programming
level: high
```

### 52. OT/ICS — Unauthorized PLC Programming

```yaml
title: OT/ICS — Unauthorized PLC Programming Access
id: d2e4f6a8-0b1c-2d3e-4f5a-7b8c9d0e1f2a
status: experimental
description: Detects unauthorized programming attempts on PLC devices in OT environments
references:
    - https://attack.mitre.org/techniques/T0812/
    - https://attack.mitre.org/techniques/T0840/
author: Defensive Engineering Team
date: 2024/02/01
modified: 2024/06/27
tags:
    - attack.control
    - attack.t0812
    - attack.t0840
    - ot.ics
logsource:
    category: authentication
    product: network
    service: zeek
detection:
    selection:
        service: 's7comm' or 'modbus' or 'cip'
    selection_unauth:
        user|contains:
            - 'anonymous'
            - 'default'
            - 'guest'
            - 'admin'
        logon_type: 'default' or 'anonymous'
    selection_bad:
        result: 'failure' or 'denied' or 'rejected'
    timeframe: 10m
    condition: selection and (selection_unauth or selection_bad | count() > 5)
falsepositives:
    - Network scanning tools
    - Configuration management systems
level: high
```

### 53. OT/ICS — Remote Access to Control System

```yaml
title: OT/ICS — Remote Access Software Detected in Control Environment
id: e3f5a7b9-1c2d-3e4f-5a6b-8c9d0e1f2a3b
status: stable
description: Detects remote access tools running in OT/ICS environments
references:
    - https://attack.mitre.org/techniques/T0823/
author: Defensive Engineering Team
date: 2024/03/01
modified: 2024/06/27
tags:
    - attack.lateral_movement
    - attack.t0823
    - ot.ics
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        Image|endswith:
            - '\teamviewer.exe'
            - '\AnyDesk.exe'
            - '\splashtop.exe'
            - '\logmein.exe'
            - '\vncserver.exe'
            - '\vncviewer.exe'
            - '\radmin.exe'
            - '\ammyy.exe'
            - '\screenconnect.exe'
            - '\gotoassist.exe'
            - '\mstsc.exe'
            - '\chrome.exe'
    condition: selection
falsepositives:
    - Authorized remote support sessions
    - Approved vendor access
level: high
```

### 54. IoT — Firmware Update from Untrusted Source

```yaml
title: IoT — Unverified Firmware Update Attempt
id: f4a6b8c0-2d3e-4f5a-6b7c-9d0e1f2a3b4c
status: experimental
description: Detects attempts to flash IoT device firmware from untrusted sources
references:
    - https://attack.mitre.org/techniques/T1542/001/
author: Defensive Engineering Team
date: 2024/04/01
modified: 2024/06/27
tags:
    - attack.persist"
    - attack.t1542.001
    - iot.embedded
logsource:
    category: network_connection
    product: linux
    service: syslog
detection:
    selection:
        program|contains:
            - 'fwupd'
            - 'fwupdate'
            - 'flashrom'
            - 'dfu-util'
            - 'avrdude'
            - 'esptool'
            - 'openocd'
        message|contains:
            - 'firmware'
            - 'flash'
            - 'bootloader'
    condition: selection
falsepositives:
    - Authorized firmware update deployments
level: medium
```

### 55. DNS — DGA Detection via Algorithmic Domain

```yaml
title: DNS — Algorithmic Domain Generation (DGA) Detection
id: a5b7c9d1-3e4f-5a6b-7c8d-0e1f2a3b4c5d
status: experimental
description: Detects DNS queries to domains characteristic of domain generation algorithms
references:
    - https://attack.mitre.org/techniques/T1568/002/
author: Defensive Engineering Team
date: 2024/01/20
modified: 2024/06/27
tags:
    - attack.command_and_control
    - attack.t1568.002
logsource:
    category: dns
    product: network
    service: zeek
detection:
    selection_dga_regex:
        query|re: '^[a-z]{20,}\.(com|net|org|info|top|xyz|club|work|space)$'
    selection_dga_hex:
        query|re: '^[0-9a-f]{16,}\.(com|net|org|top|xyz)$'
    selection_dga_nxdomain:
        query|re: '^[bcdfghjklmnpqrstvwxyz]{15,}\.(com|net|org)$'
    selection_dga_long:
        query|re: '^[a-z0-9]{25,}\.(com|net|org|top|xyz|site)$'
    timeframe: 10m
    condition: (1 of selection_*) | count() > 5
falsepositives:
    - CDN resolvers using hash-based hostnames
    - Legitimate dynamic DNS services
level: medium
```

### 56. DNS — Data Exfiltration via TXT Records

```yaml
title: DNS — Potential Data Exfiltration via Unexpected TXT Records
id: b6c8d0e2-4f5a-6b7c-8d9e-1f2a3b4c5d6e
status: experimental
description: Detects large or unusual numbers of TXT record queries, indicative of DNS tunneling
references:
    - https://attack.mitre.org/techniques/T1048/
author: Defensive Engineering Team
date: 2024/02/15
modified: 2024/06/27
tags:
    - attack.exfiltration
    - attack.t1048
logsource:
    category: dns
    product: network
    service: zeek
detection:
    selection:
        query_type: 'TXT'
    selection_long:
        query|re: '^[a-z0-9._-]{50,}'
    timeframe: 5m
    condition: (selection and selection_long) | count() > 20
falsepositives:
    - DKIM/DMARC verification
    - SPF record lookups
level: high
```

### 57. Insider Threat — Mass File Access Outside Business Hours

```yaml
title: Insider Threat — Mass File Access Outside Business Hours
id: c7d9e1f3-5a6b-7c8d-9e0f-2a3b4c5d6e7f
status: experimental
description: Detects unusual mass file access outside normal business hours, potential data exfiltration
references:
    - https://attack.mitre.org/techniques/T1020/
author: Defensive Engineering Team
date: 2024/03/15
modified: 2024/06/27
tags:
    - attack.exfiltration
    - attack.t1020
logsource:
    category: file_event
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 11
        TargetFilename|contains:
            - '\Documents\'
            - '\Desktop\'
            - '\Downloads\'
            - '\.ssh\'
            - '\.aws\'
            - '\config\'
        TargetFilename|endswith:
            - '.docx'
            - '.xlsx'
            - '.pptx'
            - '.pdf'
            - '.txt'
            - '.csv'
            - '.zip'
            - '.rar'
            - '.7z'
    timeframe: 1h
    condition: selection | count() > 100
falsepositives:
    - Late-working employees
    - Backup software
level: medium
```

### 58. Insider Threat — USB Mass Storage Device Connected

```yaml
title: Insider Threat — USB Mass Storage Device Connected
id: d8e0f2a4-6b7c-8d9e-0f1a-3b4c5d6e7f8a
status: stable
description: Detects connection of USB mass storage devices, potential data exfiltration vector
references:
    - https://attack.mitre.org/techniques/T1091/
author: Defensive Engineering Team
date: 2024/04/01
modified: 2024/06/27
tags:
    - attack.initial_access
    - attack.t1091
logsource:
    category: application
    product: windows
    service: system
detection:
    selection:
        EventID: 20001 or 20003    # USB storage connection events
        Message|contains:
            - 'USB'
            - 'mass storage'
            - 'disk drive'
    condition: selection
falsepositives:
    - Authorized USB use
level: low
```

### 59. Supply Chain — Compromised Package Download

```yaml
title: Supply Chain — Malicious Package Download from Package Managers
id: e9f1a3b5-7c8d-9e0f-1a2b-4c5d6e7f8a9b
status: experimental
description: Detects download of known compromised packages from npm, PyPI, or other registries
references:
    - https://attack.mitre.org/techniques/T1195/001/
author: Defensive Engineering Team
date: 2024/05/01
modified: 2024/06/27
tags:
    - attack.initial_access
    - attack.t1195.001
logsource:
    category: network_connection
    product: linux
    service: syslog
detection:
    selection_npm:
        program|contains: 'npm'
        message|contains:
            - 'install'
            - 'download'
        Message|contains:
            - 'package'
    selection_pip:
        program|contains: 'pip'
        message|contains:
            - 'install'
            - 'download'
    selection_nuget:
        program|contains: 'nuget'
        message|contains:
            - 'install'
    selection_vuln_pkg:
        message|contains:
            - 'eslint-scope'
            - 'event-stream'
            - 'flatmap-stream'
            - 'colourama'
            - 'urllib'
    condition: (1 of selection_*) and selection_vuln_pkg
falsepositives:
    - Developers downloading packages for testing
level: high
```

### 60. Supply Chain — CI/CD Pipeline Secret Exposure

```yaml
title: Supply Chain — CI/CD Pipeline Secret Exported or Logged
id: f0a2b4c6-8d9e-0f1a-2b3c-5d6e7f8a9b0c
status: stable
description: Detects potential secret exposure in CI/CD pipeline logs or output artifacts
references:
    - https://attack.mitre.org/techniques/T1552/
author: Defensive Engineering Team
date: 2024/06/01
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1552
logsource:
    category: web
    product: cloud
    service: github
detection:
    selection:
        action:
            - 'github.audit'
            - 'actions.workflow'
    selection_secret:
        message|contains:
            - 'AWS_SECRET'
            - 'AWS_ACCESS'
            - 'TF_VAR_'
            - 'AZURE_CLIENT'
            - 'GITHUB_TOKEN'
            - 'NPM_TOKEN'
            - 'DOCKER_PASSWORD'
            - 'API_KEY'
            - 'SECRET_KEY'
            - 'PRIVATE_KEY'
            - '-----BEGIN'
    selection_exposed:
        message|contains:
            - 'echo'
            - 'print'
            - 'write-output'
            - 'console.log'
    condition: selection and selection_secret and selection_exposed
falsepositives:
    - Legitimate logging of masked secrets (verify)
level: high
```

---

## More Rules (61–70)

### 61. Detection of Detection — Anti-Sigma Techniques

```yaml
title: Detection of Detection — Log Tampering or Deletion
id: a1b3c5d7-9e0f-1a2b-3c4d-6e7f8a9b0c1d
status: stable
description: Detects attempts to identify, disable, or tamper with logging systems (anti-Sigma/forensics)
references:
    - https://attack.mitre.org/techniques/T1562/
    - https://attack.mitre.org/techniques/T1614
author: Defensive Engineering Team
date: 2024/06/01
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1562.001
    - attack.t1562.006
    - attack.t1614
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection_wevtutil:
        Image|endswith: '\wevtutil.exe'
        CommandLine|contains:
            - 'cl '
            - 'clear-log'
            - 'set-log'
            - 'Windows PowerShell'
            - 'Microsoft-Windows-Sysmon'
            - 'Security'
    selection_eventlog:
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - 'Clear-EventLog'
            - 'Remove-EventLog'
            - 'Limit-EventLog'
            - 'Clear-WinEvent'
    selection_auditpol:
        Image|endswith: '\auditpol.exe'
        CommandLine|contains:
            - '/remove'
            - '/clear'
            - 'set /subcategory'
    selection_fsutil:
        Image|endswith: '\fsutil.exe'
        CommandLine|contains:
            - 'usn'
            - 'deletejournal'
    selection_sysmon:
        Image|endswith: '\sysmon.exe'
        CommandLine|contains:
            - '-c '
            - '/c '
            - '-u '      # Uninstall Sysmon
    condition: 1 of selection_*
falsepositives:
    - Authorized log management
    - Incident response teams clearing logs
level: critical
```

### 62. Process Creation from Suspicious Named Pipe

```yaml
title: Process Creation from Suspicious Named Pipe — Possible Impersonation
id: b2c4d6e8-0a1b-2c3d-4e5f-7a8b9c0d1e2f
status: experimental
description: Detects process creation where the parent process is a suspicious named pipe
references:
    - https://attack.mitre.org/techniques/T1055/
author: Defensive Engineering Team
date: 2024/06/10
modified: 2024/06/27
tags:
    - attack.privilege_escalation
    - attack.t1055
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 1
        ParentImage|endswith:
            - '\svchost.exe'
            - '\services.exe'
            - '\lsass.exe'
            - '\winlogon.exe'
            - '\csrss.exe'
        Image|endswith:
            - '\powershell.exe'
            - '\cmd.exe'
            - '\cscript.exe'
            - '\wscript.exe'
            - '\rundll32.exe'
            - '\regsvr32.exe'
            - '\mshta.exe'
    filter:
        ParentCommandLine|contains:
            - '-k'
            - '-p'
            - 'sess'
    condition: selection and not filter
falsepositives:
    - Legitimate svchost child processes
level: high
```

### 63. Non-Interactive PowerShell Process

```yaml
title: Non-Interactive PowerShell Process — Hidden Window
id: c3d5e7f9-1a2b-3c4d-5e6f-8a9b0c1d2e3f
status: stable
description: Detects PowerShell execution with window style hidden, common in malicious scripts
references:
    - https://attack.mitre.org/techniques/T1059/001/
author: Defensive Engineering Team
date: 2024/05/15
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1059.001
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 1
        Image|endswith: '\powershell.exe'
        CommandLine|contains:
            - '-WindowsStyle Hidden'
            - '-WindowStyle Hidden'
            - '-Window Hidden'
            - '-W Hidden'
            - '-nop -w 1'
            - '-noprofile -windowstyle hidden'
            - '-ep bypass -w hidden'
    filter_admin:
        CommandLine|contains:
            - 'Get-WinEvent'
            - 'Get-Process'
            - 'Get-Service'
            - 'Register-ScheduledJob'
    condition: selection and not filter_admin
falsepositives:
    - IT admin scripts running silently
    - Software installers using hidden windows
level: high
```

### 64. .NET Assembly Reflectively Loaded

```yaml
title: .NET Assembly Reflective Loading — System.Reflection.Assembly.Load
id: d4e6f8a0-2b3c-4d5e-6f7a-9b0c1d2e3f4a
status: experimental
description: Detects .NET assembly reflective loading via System.Reflection.Assembly.Load from byte arrays
references:
    - https://attack.mitre.org/techniques/T1620/
author: Defensive Engineering Team
date: 2024/04/20
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1620
logsource:
    category: image_load
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 7
        ImageLoaded|endswith: '\clr.dll' or '\mscoree.dll' or '\coreclr.dll'
    filter:
        Image|startswith:
            - 'C:\Program Files'
            - 'C:\Windows\System32\WindowsPowerShell'
            - 'C:\Windows\Microsoft.NET'
    condition: selection and not filter
falsepositives:
    - .NET applications loading CLR
level: medium
```

### 65. Anomalous PowerShell Module Load Order

```yaml
title: Anomalous PowerShell Module Load — Non-Standard Path
id: e5f7a9b1-3c4d-5e6f-7a8b-0c1d2e3f4a5b
status: stable
description: Detects PowerShell loading modules from non-standard locations
references:
    - https://attack.mitre.org/techniques/T1059/001/
author: Defensive Engineering Team
date: 2024/03/10
modified: 2024/06/27
tags:
    - attack.execution
    - attack.t1059.001
logsource:
    category: image_load
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 7
        Image|endswith: '\powershell.exe'
        ImageLoaded|contains:
            - '\AppData\'
            - '\Temp\'
            - '\Downloads\'
            - '\Users\'
    condition: selection
falsepositives:
    - PowerShell modules installed in user context
level: medium
```

### 66. MSHTA Suspicious Callback

```yaml
title: MSHTA Suspicious Network Callback
id: f6a8b0c2-4d5e-6f7a-8b9c-1d2e3f4a5b6c
status: stable
description: Detects mshta.exe making outbound network connections, potential C2 callback
references:
    - https://attack.mitre.org/techniques/T1218/005/
author: Defensive Engineering Team
date: 2024/02/01
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1218.005
logsource:
    category: network_connection
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 3
        Image|endswith: '\mshta.exe'
        Initiated: 'true'
        Protocol: 'tcp'
    condition: selection
falsepositives:
    - Legitimate MSHTA usage with network access
level: critical
```

### 67. Process Access to SAM Registry Hive

```yaml
title: Credential Access — SAM Registry Hive Access
id: a7b9c1d3-5e6f-7a8b-9c0d-2e3f4a5b6c7d
status: stable
description: Detects process access to SAM registry hive for credential extraction
references:
    - https://attack.mitre.org/techniques/T1003/002/
author: Defensive Engineering Team
date: 2024/01/01
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1003.002
logsource:
    category: registry_event
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 13
        TargetObject|contains:
            - '\SAM\SAM\Domains\Account\Users'
            - '\SAM\SAM\Domains\Account\F'
            - 'HKEY_LOCAL_MACHINE\SAM'
    condition: selection
falsepositives:
    - Security software accessing SAM
    - Legitimate password tools
level: critical
```

### 68. LSASS Process Access from Suspicious Process

```yaml
title: Credential Access — LSASS Process Access from Non-Standard Process
id: b8c0d2e4-6f7a-8b9c-0d1e-3f4a5b6c7d8e
status: stable
description: Detects suspicious processes accessing LSASS for credential dumping
references:
    - https://attack.mitre.org/techniques/T1003/001/
author: Defensive Engineering Team
date: 2024/01/05
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1003.001
logsource:
    category: process_access
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 10
        TargetImage|endswith: '\lsass.exe'
        GrantedAccess: '0x1FFFFF' or '0x1010' or '0x1F3FFF' or '0x1F1FFF'
    filter:
        SourceImage|startswith:
            - 'C:\Windows\System32\'
            - 'C:\Windows\SysWOW64\'
    filter_svchost:
        SourceImage|endswith: '\svchost.exe'
    filter_wininit:
        SourceImage|endswith: '\wininit.exe'
    condition: selection and not filter and not filter_svchost and not filter_wininit
falsepositives:
    - Antivirus/EDR scanning LSASS
    - Microsoft Defender
level: critical
```

### 69. Unloading of Sysmon Driver

```yaml
title: Defense Evasion — Sysmon Driver Unloaded
id: c9d1e3f5-7a8b-9c0d-1e2f-4a5b6c7d8e9f
status: stable
description: Detects attempts to unload the Sysmon driver, a defense evasion technique
references:
    - https://attack.mitre.org/techniques/T1562/001/
author: Defensive Engineering Team
date: 2024/02/10
modified: 2024/06/27
tags:
    - attack.defense_evasion
    - attack.t1562.001
logsource:
    category: driver_load
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 4              # Sysmon service state changed
        Message|contains:
            - 'unloaded'
            - 'stopped'
            - 'terminated'
    filter_update:
        Message|contains:
            - 'update'
            - 'upgrade'
    condition: selection and not filter_update
falsepositives:
    - Authorized Sysmon updates or upgrades
level: critical
```

### 70. Mimikatz — Compatible Command Line Arguments

```yaml
title: Mimikatz — Compatible Command Line Arguments
id: d0e2f4a6-8b9c-0d1e-2f3a-5b6c7d8e9f0a
status: stable
description: Detects command line arguments characteristic of Mimikatz usage
references:
    - https://attack.mitre.org/techniques/T1003/001/
    - https://github.com/gentilkiwi/mimikatz
author: Defensive Engineering Team
date: 2024/03/01
modified: 2024/06/27
tags:
    - attack.credential_access
    - attack.t1003.001
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 1
        CommandLine|contains:
            - 'sekurlsa::logonPasswords'
            - 'sekurlsa::minidump'
            - 'sekurlsa::wdigest'
            - 'kerberos::golden'
            - 'kerberos::tgt'
            - 'lsadump::sam'
            - 'lsadump::dcsync'
            - 'crypto::certificates'
            - 'privilege::debug'
            - 'token::elevate'
            - 'vault::cred'
            - 'dpapi::'
    condition: selection
falsepositives:
    - Authorized penetration testing
level: critical
```

---

## Sigma Conversion Examples — Input to Backend

### Example 1: Basic Process Creation Rule

**Sigma Rule:**
```yaml
title: PowerShell Encoded Command
logsource:
    category: process_creation
    product: windows
    service: sysmon
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|base64offset: '-enc '
    condition: selection
```

**Elasticsearch (Lucene) — `es-qs`:**
```
process.executable:*\\powershell.exe AND process.command_line:(-enc OR -enc* OR LQBlAG4AYwAgAA)
```

**Elasticsearch (DSL) — `es-dsl`:**
```json
{
  "query": {
    "bool": {
      "must": [
        {"wildcard": {"process.executable": "*\\powershell.exe"}},
        {"query_string": {"query": "process.command_line:(-enc OR -enco OR -encodedCommand)"}}
      ]
    }
  }
}
```

**Splunk SPL — `splunk`:**
```
source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=1 Image=*\\powershell.exe (CommandLine="-enc *" OR CommandLine="-enco *" OR CommandLine="-encodedCommand *")
```

**Microsoft Sentinel KQL — `azure-sentinel`:**
```kusto
Sysmon
| where EventID == 1
| where Image endswith "\\powershell.exe"
| where CommandLine contains "-enc" or CommandLine contains "-enco" or CommandLine contains "-encodedCommand"
```

**QRadar AQL — `qradar`:**
```sql
SELECT * FROM events
WHERE LOGSOURCENAME(logsourceid) LIKE '%Sysmon%'
AND IMAGE = '*\\powershell.exe'
AND (COMMANDLINE LIKE '%-enc%' OR COMMANDLINE LIKE '%-enco%' OR COMMANDLINE LIKE '%-encodedCommand%')
```

**Grafana Loki LogQL — `loki`:**
```logql
{job="windows"} |= "Sysmon" |= "powershell.exe" |= "-enc"
```

### Example 2: Network Connection Detection

**Sigma Rule:**
```yaml
title: Suspicious Outbound RDP
logsource:
    category: network_connection
    product: windows
    service: sysmon
detection:
    selection:
        EventID: 3
        DestinationPort: 3389
        Initiated: 'true'
        Protocol: 'tcp'
    filter:
        Image|endswith: '\mstsc.exe'
    condition: selection and not filter
```

**Elasticsearch (Lucene):**
```
event.code:3 AND destination.port:3389 AND network.protocol:tcp AND NOT process.executable:*\\mstsc.exe
```

**Splunk SPL:**
```
index=windows source="WinEventLog:Microsoft-Windows-Sysmon/Operational" EventCode=3 DestinationPort=3389 Protocol=tcp NOT Image=*\\mstsc.exe
```

**Azure Sentinel KQL:**
```kusto
Sysmon
| where EventID == 3
| where DestinationPort == 3389
| where Protocol == "tcp"
| where Initiated == "true"
| where Image !endswith "\\mstsc.exe"
```

### Example 3: Multiple Selection Maps

**Sigma Rule:**
```yaml
title: Suspicious Service Installation
logsource:
    product: windows
    service: security
detection:
    selection:
        EventID: 4697
    selection_temp:
        ServiceFileName|contains: '\Temp\'
    selection_name:
        ServiceName|contains:
            - 'svchost'
            - 'windows'
    condition: selection and selection_temp and selection_name
```

**Elasticsearch (Lucene):**
```
event.code:4697 AND file.path:*\\Temp\\* AND (winlog.event_data.ServiceName:*svchost* OR winlog.event_data.ServiceName:*windows*)
```

**Splunk SPL:**
```
source="WinEventLog:Security" EventCode=4697 ServiceFileName=*\\Temp\\* (ServiceName=*svchost* OR ServiceName=*windows*)
```

### Example 4: Aggregation / Correlation Rule

**Sigma Rule (v2):**
```yaml
title: Brute Force — Multiple Failed Logons
logsource:
    category: authentication
    product: windows
    service: security
detection:
    selection:
        EventID: 4625
    timeframe: 5m
    condition: selection | count() > 10
```

**Elasticsearch (DSL):**
```json
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"event.code": "4625"}},
        {"range": {"@timestamp": {"gte": "now-5m"}}}
      ]
    }
  },
  "aggs": {
    "failed_count": {
      "value_count": {"field": "event.code"}
    }
  }
}
```

**Splunk SPL:**
```spl
index=windows source="WinEventLog:Security" EventCode=4625
| timechart span=5m count
| where count > 10
```

---

## Sigma Pipeline Development Deep Dive

### Custom Pipeline Example: Map Sigma Fields to Custom ECS-Like Schema

```python
from sigma.pipeline import SigmaPipeline
from sigma.processing.transformations import (
    FieldNameMappingTransformation,
    FieldNamePrefixTransformation,
    LowercaseFieldNamesTransformation,
    SetFieldTransformation,
    ReplaceFieldValueTransformation,
    DropFieldTransformation,
    RuleFailureTransformation,
)
from sigma.processing.conditions import (
    LogsourceCondition,
    RuleDetectionItemCondition,
)

# Every event has an event.dataset field
# Map Windows Sysmon events to a custom schema

custom_pipeline = SigmaPipeline(
    name="custom_win_schema",
    priority=50,
    transformations=[
        # Map all known Sigma fields to custom schema
        FieldNameMappingTransformation({
            "Image": "process.executable",
            "CommandLine": "process.args",
            "ParentImage": "process.parent.executable",
            "ParentCommandLine": "process.parent.args",
            "TargetFilename": "file.path",
            "TargetObject": "registry.path",
            "SourceIp": "network.source.ip",
            "DestinationIp": "network.destination.ip",
            "SourcePort": "network.source.port",
            "DestinationPort": "network.destination.port",
            "ImageLoaded": "dll.path",
            "User": "user.name",
            "ParentUser": "user.parent.name",
            "PipeName": "pipe.name",
            "QueryName": "dns.question.name",
            "QueryResults": "dns.answers",
            "EventID": "event.code",
            "LogonType": "logon.type",
            "SourceImage": "process.source.executable",
            "TargetImage": "process.target.executable",
            "GrantedAccess": "process.access_rights",
            "CallTrace": "process.call_trace",
            "Company": "pe.company",
            "Description": "pe.description",
            "Product": "pe.product",
            "FileVersion": "pe.file_version",
            "OriginalFileName": "pe.original_filename",
            "IntegrityLevel": "process.integrity_level",
            "Hashes": "file.hash.sha256",
        }),

        # Lowercase all field names
        LowercaseFieldNamesTransformation(),

        # Add fixed fields
        SetFieldTransformation("event.kind", "event"),
        SetFieldTransformation("event.dataset", "windows.sysmon"),

        # Replace empty Hashes field
        ReplaceFieldValueTransformation("file.hash.sha256", "", None),

        # Drop noisy fields
        DropFieldTransformation("process.args"),  # example: drop if sensitive

        # Logsource conditions: only apply to Sysmon
        LogsourceCondition(
            product="windows",
            service="sysmon",
        ),
    ],
)
```

### Field Renaming via Regex

```python
from sigma.processing.transformations import FieldNameRegexRenameTransformation

pipeline = SigmaPipeline(transformations=[
    # Convert dot-notation to nested object notation
    FieldNameRegexRenameTransformation(
        regex=r'\.',
        replacement='.',  # ElasticSearch compatible nested
    ),

    # Remove trailing underscores
    FieldNameRegexRenameTransformation(
        regex=r'_$',
        replacement='',
    ),

    # Convert CamelCase to snake_case
    FieldNameRegexRenameTransformation(
        regex=r'([a-z])([A-Z])',
        replacement=r'\1_\2',
    ),
    FieldNameRegexRenameTransformation(
        regex=r'([A-Z]+)([A-Z][a-z])',
        replacement=r'\1_\2',
    ),
])
```

### Log Source to Field Mapping Pipeline

```python
from sigma.processing.transformations import LogsourceToFieldTransformation

pipeline = SigmaPipeline(transformations=[
    LogsourceToFieldTransformation(
        field="winlog.provider_name",
        mapping={
            ("windows", "sysmon", "process_creation"): "Microsoft-Windows-Sysmon",
            ("windows", "sysmon", "network_connection"): "Microsoft-Windows-Sysmon",
            ("windows", "security", "process_creation"): "Microsoft-Windows-Security-Auditing",
            ("windows", "security", "authentication"): "Microsoft-Windows-Security-Auditing",
            ("linux", "syslog", None): "syslog",
            ("network", "zeek", None): "zeek",
        }
    )
])
```

---

## Sigma False Positive Tuning — Detailed Guide

### Step-by-Step FP Reduction

```yaml
# Version 1 — Initial detection (high FP)
title: PowerShell Execution (Initial)
detection:
    selection:
        Image|endswith: '\powershell.exe'
    condition: selection
# FP: ~1000/day in typical environment

# Version 2 — Add specific flag (medium FP)
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains: '-enc '
    condition: selection
# FP: ~50/day (administrative scripts)

# Version 3 — Add exclusions (low FP)
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|base64offset: '-enc '
    filter_admins:
        UserName|endswith:
            - '-admin'
            - '_svc'
            - '_script'
    filter_known:
        CommandLine|contains:
            - 'Write-Host'
            - 'Get-Help'
            - 'Send-MailMessage'
    filter_paths:
        CommandLine|startswith:
            - 'C:\Program Files\'
            - 'C:\Windows\System32\'
    condition: selection and not filter_admins and not filter_known and not filter_paths
# FP: ~2-5/day (manageable)

# Version 4 — Use external allowlist via field
detection:
    selection:
        Image|endswith: '\powershell.exe'
        CommandLine|contains|base64offset: '-enc '
    filter:
        UserName|contains:
            - 'admin'
            - 'svc'
            - 'backup'
            - 'automation'
    filter_knownIP:
        SourceIp|cidr:
            - '10.10.10.0/24'  # IT admin subnet
            - '192.168.10.0/24' # Automation subnet
    condition: selection and not filter and not filter_knownIP
# FP: ~0-1/week (production-ready)
```

### FP Feedback Loop Process

```
Alert Fires
    │
    ▼
[1] Triaged by Analyst
    │
    ├─ True Positive → Incident Response
    │
    └─ False Positive → Document reasons
        │
        ▼
[2] Identify distinguishing characteristic
    ├─ Image path differs
    ├─ User is system/service account
    ├─ Command line has known-good flag
    └─ Time-based (maintenance window)
        │
        ▼
[3] Add exclusion rule (filter or keyword)
    │
    ▼
[4] Update rule in Git → PR → Review
    │
    ▼
[5] Deploy to staging → Monitor 7 days
    │
    ▼
[6] If FP rate < threshold → Promote to production
    │
    └─ If > threshold → Iterate again
```

---

## Migration Guide: sigmac → pySigma

| sigmac (Legacy) | sigma CLI / pySigma (Modern) |
|---|---|
| `sigmac -t splunk rule.yml` | `sigma convert -t splunk rule.yml` |
| `sigmac -t es-qs -c winlogbeat.yml rule.yml` | `sigma convert -t es-qs -p winlogbeat rule.yml` |
| Config files (`.yml`) | Pipeline plugins (Python packages) |
| Limited target list | Plugin-based (extensible) |
| Python 2 only | Python 3.8+ |
| No correlation rules | Correlation rules (v2) |
| `-c` flag for config | `-p` flag for pipeline |
| Manual field maps | Full processing pipeline |
| No test framework | `sigma check` with test execution |
| No plugin system | Rich plugin system (`sigma plugin install`) |

**Migration steps:**
```bash
# 1. Install pySigma and backends
pip install sigma-cli pysigma-backend-elasticsearch pysigma-backend-splunk

# 2. Find equivalent pipeline
# sigmac: -c winlogbeat.yml
# sigma:  -p winlogbeat

# 3. Test conversion side-by-side
sigmac -t es-qs -c winlogbeat.yml rule.yml > old_query.txt
sigma convert -t es-qs -p winlogbeat rule.yml > new_query.txt
diff old_query.txt new_query.txt

# 4. Update scripts / automation
# Replace: sigmac -t splunk -c splunk_cim.yml rule.yml
# With:    sigma convert -t splunk -p splunk_cim rule.yml

# 5. Migrate custom configs to pipelines
# Convert inline config files to proper Python pipeline classes
```

---

## Sigma Alert Response Playbooks

### Playbook Template: High-Severity Alert Response

```yaml
# Example playbook for Sigma alert
alert_title: Mimikatz Detection — LSASS Access
rule_id: a5c7e2d1-3f8b-4a1c-9e5d-6b2f8c3a1d0e
tier: T1 (SOC Analyst)
severity: Critical

steps:
  - step: 1
    action: Verify alert
    details: |
      1. Confirm the alert is from a production system
      2. Check SourceImage and TargetImage fields
      3. Verify GrantedAccess value (0x1FFFFF = suspicious)
    time_sla: 5 minutes

  - step: 2
    action: Initial containment
    details: |
      1. Isolate the affected host from network (EDR isolation)
      2. Collect full memory dump from affected process
      3. Capture process tree and network connections
    time_sla: 15 minutes

  - step: 3
    action: Deep investigation
    details: |
      1. Check for other LSASS access events on same host (past 7 days)
      2. Search for credential dumping tools (Mimikatz, procdump)
      3. Review authentication logs for anomalous logins
      4. Check for lateral movement from this host (Event ID 4624, 4648)
    tools:
      - EDR query: process_access SourceImage != trusted
      - SIEM search: authentication SourceIp = compromised_host

  - step: 4
    action: Response
    details: |
      1. If confirmed:
         a. Escalate to Tier 2
         b. Initiate incident response process
         c. Reset affected user passwords
         d. Revoke Kerberos TGTs for affected accounts
      2. If false positive:
         a. Document in rule falsepositives
         b. Add filter if recurring pattern
    time_sla: 30 minutes

  - step: 5
    action: Recovery
    details: |
      1. Reimage affected host
      2. Monitor for signs of persistence
      3. Update detection rules based on TTPs observed
```

---

## Sigma Performance Benchmarking

### Measuring Rule Performance in Splunk

```bash
# Splunk — benchmark individual rule
| search index=windows EventCode=1 Image=*\\powershell.exe CommandLine=*enc*
| stats count

# Time the search
| search index=windows EventCode=1 Image=*\\powershell.exe CommandLine=*enc*
| stats count
| eval search_time=now() - _time_earliest

# Use tstats for faster searches (data model acceleration)
| tstats count from datamodel=Endpoint.Processes
  where Processes.process = *powershell.exe
  by Processes.process, Processes.dest, _time
```

### Measuring Rule Performance in Elasticsearch

```bash
# Elasticsearch — benchmark with _count API
curl -X GET "localhost:9200/windows-*/_count" -H 'Content-Type: application/json' -d'
{
  "query": {
    "bool": {
      "must": [
        {"wildcard": {"process.executable": "*\\powershell.exe"}},
        {"query_string": {"query": "process.command_line:*enc*"}}
      ]
    }
  }
}'

# Benchmark with Search Profiler (Kibana)
# Dev Tools → Search profiler → Paste query
```

### Rule Performance Categories

| Category | Latency (per million events) | Recommendation |
|---|---|---|
| Single EID filter (`EventCode=1`) | ~50ms | Use freely |
| Simple field match (`Image=*\\x.exe`) | ~100ms | Use freely |
| `contains` on short field | ~200ms | Acceptable |
| `contains` on long field (CommandLine) | ~500ms | Minimize |
| `base64offset` modifier | ~800ms | Use for high-severity rules |
| `re` / regex modifier | ~1-5s | Use sparingly, anchor patterns |
| Aggregation (count, distinct) | ~2-10s | Use narrow timeframes |
| Multiple OR conditions | ~100-500ms | Combine via EID filter |
| CIDR matching | ~200ms | Acceptable |

---

## Appendix D: Sigma Rule Quick Reference Card

### One-Liner Rules for Log Sources

```yaml
# Windows Security — Process creation
logsource: {category: process_creation, product: windows, service: security}
detection: {selection: {EventID: 4688, Image|endswith: '\evil.exe'}, condition: selection}

# Sysmon — Network connection
logsource: {category: network_connection, product: windows, service: sysmon}
detection: {selection: {EventID: 3, DestinationIp|cidr: '203.0.113.0/24'}, condition: selection}

# AWS CloudTrail — Console login
logsource: {service: cloudtrail, product: aws}
detection: {selection: {eventName: 'ConsoleLogin', userIdentity.type: 'Root'}, condition: selection}

# Linux — SSH failed auth
logsource: {category: authentication, product: linux, service: syslog}
detection: {selection: {program: 'sshd', message|contains: 'Failed password'}, condition: selection}

# Web — Apache suspicious query
logsource: {category: web, product: linux, service: apache}
detection: {selection: {c-uri|contains: '../../../etc/passwd'}, condition: selection}
```

### Common Sigma Field Quick Reference

| What you want | Sigma Field | Windows Event | Sysmon EID |
|---|---|---|---|
| Process name | `Image` | 4688 `NewProcessName` | 1 `Image` |
| Command line | `CommandLine` | 4688 `CommandLine` | 1 `CommandLine` |
| Parent process | `ParentImage` | 4688 `ParentProcessName` | 1 `ParentImage` |
| Source IP | `SourceIp` | 5156 `SourceAddress` | 3 `SourceIp` |
| Destination IP | `DestinationIp` | 5156 `DestAddress` | 3 `DestinationIp` |
| DNS query | `QueryName` | — | 22 `QueryName` |
| File created | `TargetFilename` | 4663 `ObjectName` | 11 `TargetFilename` |
| Registry key | `TargetObject` | 4657 `ObjectName` | 13 `TargetObject` |
| DLL loaded | `ImageLoaded` | — | 7 `ImageLoaded` |
| User account | `User` / `TargetUserName` | 4624 `TargetUserName` | 1 `User` |
| Named pipe | `PipeName` | — | 17/18 `PipeName` |
| Source port | `SourcePort` | 5156 `SourcePort` | 3 `SourcePort` |
| Destination port | `DestinationPort` | 5156 `DestPort` | 3 `DestinationPort` |
| Process ID | `ProcessId` | 4688 `NewProcessId` | 1 `ProcessId` |

---

## Appendix E: Sigma Rule IDE / Editor Support

| Editor | Support | How to use |
|---|---|---|
| VS Code | YAML + Schema | Install `SigmaHQ.sigma` extension from marketplace |
| JetBrains | YAML + Custom | YAML plugin + schema validation |
| Vim/Neovim | Syntax + LSP | `yaml-language-server` with Sigma schema |
| Sublime Text | YAML syntax | YAML highlighting, no Sigma-specific |

**VS Code Extension features:**
- Syntax highlighting for Sigma YAML
- Validation against Sigma specification
- Auto-completion for fields, categories, services
- Snippets for common rule patterns
- Preview converted query in various backends

---

## Appendix F: Sigma Threat Hunting Queries

```yaml
# Hunting: Processes running from user-writable paths
title: HUNT — Suspicious Process Path
status: experimental
logsource: {category: process_creation, product: windows, service: sysmon}
detection:
    selection:
        Image|contains:
            - '\AppData\Local\Temp\'
            - '\AppData\Roaming\'
            - '\Users\*\Downloads\'
            - '\Users\*\Desktop\'
            - '\Windows\Temp\'
            - 'C:\Temp\'
    condition: selection

# Hunting: Processes with no parent (orphan)
title: HUNT — Orphan Process
status: experimental
logsource: {category: process_creation, product: windows, service: sysmon}
detection:
    selection:
        EventID: 1
        ParentProcessId: 4     # PID 4 = System (no real parent)
    condition: selection

# Hunting: Rare scheduled task names
title: HUNT — Suspicious Scheduled Task Names
status: experimental
logsource: {category: scheduled_task, product: windows, service: security}
detection:
    selection:
        EventID: 4698
        TaskName|contains:
            - 'Updater'
            - 'Update'
            - 'Windows'
            - 'System'
            - 'Security'
            - 'Microsoft'
    condition: selection
```

---

## Appendix G: Sigma Rule Statistics & Metrics

Track these metrics for your Sigma rule set:

```yaml
# Per-rule metrics
- rule_id: <uuid>
  title: <rule_title>
  age_days: 365
  total_alerts: 1250
  true_positives: 45          (3.6%)
  false_positives: 1205       (96.4%)
  fp_rate: 0.964
  last_tuned: 2024-06-01
  status: active
  action: needs_tuning        # needs_tuning | good | retired
```

**Aggregate metrics:**
- Total rules deployed: 250
- Rules with FP rate > 90%: 12 (flag for tuning)
- Rules with zero alerts (90d): 45 (consider retirement)
- Average alert-to-FP ratio: 1:20
- MITRE ATT&CK coverage: 85 techniques (of 200+ relevant)

---

*"Write once, detect everywhere. Logs are the story — Sigma is the language."*

*Last updated: 2026-06-27. Maintained by Defensive Engineering Team.*

- **Official Sigma HQ:** https://github.com/SigmaHQ
- **Sigma Specification:** https://github.com/SigmaHQ/sigma-specification
- **pySigma Documentation:** https://pysigma.readthedocs.io/
- **Sigma CLI:** https://github.com/SigmaHQ/sigma-cli
- **MITRE ATT&CK:** https://attack.mitre.org/
- **Atomic Red Team:** https://github.com/redcanaryco/atomic-red-team
- **Uncoder.io (SOC Prime):** https://uncoder.io
- **Sigconverter.io:** https://sigconverter.io
- **Elastic Detection Rules:** https://github.com/elastic/detection-rules
- **Splunk Security Content:** https://research.splunk.com/
- **Azure Sentinel Sigma:** https://github.com/Azure/Azure-Sentinel/tree/master/Detections/Sigma
- **CISA Sigma:** https://github.com/cisagov/cybersecurity-performance-analytics/tree/main/sigma
- **Wazuh Sigma:** https://documentation.wazuh.com/current/user-manual/ruleset/sigma.html
- **Security Onion Sigma:** https://docs.securityonion.net/en/2.4/sigma.html
- **Sigma vs. YARA:** https://www.nextron-systems.com/2024/01/15/sigma-vs-yara/
- **Windows Security Event Log reference:** https://docs.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624
- **Sysmon reference:** https://docs.microsoft.com/en-us/sysinternals/downloads/sysmon
- **Sigma rule writing workshop:** https://github.com/SigmaHQ/sigma/wiki

---
