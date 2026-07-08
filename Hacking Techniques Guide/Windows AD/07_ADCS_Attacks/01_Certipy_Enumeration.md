# Certipy AD CS Enumeration

## Overview

Enumeration is the critical first phase of any AD CS attack. [Certipy](https://github.com/ly4k/Certipy) by Oliver Lyak (ly4k) is the de-facto tool for enumerating and exploiting AD CS from Linux. It queries the CA server, analyzes certificate templates, checks ACLs, and identifies all ESC vulnerabilities automatically.

## Installation

```bash
# Install via pip
pip3 install certipy-ad

# Verify installation
certipy --help
```

## Primary Enumeration Commands

### Basic Find (All Templates, CA Info, PKI Objects)

```bash
# Full enumeration, output to files
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10

# Output to files with specified CA
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -ca 'CA-SERVER'
```

The output creates a directory with:
- `*.txt` — Human-readable report
- `*.json` — Machine-readable data
- `*.zip` — BloodHound-compatible data

### Find Only Vulnerable Templates

```bash
# Filter to only vulnerable templates
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -vulnerable
```

### Output to stdout (No Files)

```bash
# Print to terminal instead of files
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout
```

### Output to stdout + Vulnerable Only

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -stdout -vulnerable
```

### BloodHound Output

```bash
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -bloodhound
```

Then import the generated ZIP into BloodHound to visualize AD CS attack paths.

### Targeted Enumeration Options

```bash
# Enumerate specific CA
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -ca 'CA-SERVER.domain.local\CA-NAME'

# Hide output of non-vulnerable templates
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -vulnerable -hide-admins

# Show only enabled templates
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -enabled
```

### Using NTLM Hash Instead of Password

```bash
certipy find -u 'user@domain.local' -hashes 'LM:HASH' -dc-ip 192.168.1.10

# If LM hash is not available
certipy find -u 'user@domain.local' -hashes ':NTLMHASH' -dc-ip 192.168.1.10
```

### Using Kerberos Authentication

```bash
# With Kerberos ticket
certipy find -u 'user@domain.local' -k -dc-ip 192.168.1.10

# With specific KDC
certipy find -u 'user@domain.local' -k -dc-host 'dc.domain.local'
```

## What Certipy Finds

### Certificate Authority Information

- CA server name, hostname, IP
- CA certificate chain
- CA configuration (SAN flag, etc.)
- CA security descriptor/ACLs

### Certificate Template Analysis

For each template, Certipy analyzes:

- **Template Name** and display name
- **EKUs** (Extended Key Usages) — Client Authentication, Smart Card Logon, Any Purpose, etc.
- **Enrollment Rights** — Who can enroll (SIDs mapped to group names)
- **Enrollment Flags** — `CT_FLAG_ENROLLEE_SUPPLIES_SUBJECT` (allows SAN in request)
- **Manager Approval** — Whether CA manager approval is required
- **Authorized Signatures** — Number of required authorized signatures
- **Schema Version** — V1 vs V2 templates (V2 have more security features)
- **Security Descriptor** — Full ACL of the template
- **Validity Period** — How long certificates are valid

### Vulnerability Detection

Certipy checks each template against known ESC conditions and reports:

```
Template: VulnTemplate
  [+] Vulnerabilities
    ESC1 - SAN Misconfiguration
      - Enrollee supplies subject
      - Manager approval is disabled
      - Authorized signatures are not required
    ESC2 - Any Purpose EKU
      - Template has Any Purpose EKU
```

### PKI Object ACLs

- CA object ACLs (in AD)
- PKI enrollment containers
- NTAuthCertificates object permissions

## BloodHound AD CS Integration (v4+)

BloodHound v4+ has specific AD CS nodes and edges:

- **Enroll** edge — user/group can enroll in a template
- **Enforce** edge — template linked to CA
- **TrustedBy** edge — NTAuthCertificates trusted by domain
- **ADCSESC1** through **ADCSESC13** edges

```bash
# Generate BloodHound JSON with AD CS info
certipy find -u 'user@domain.local' -p 'Password123!' -dc-ip 192.168.1.10 -bloodhound

# Or use BloodHound's built-in collector
SharpHound.exe --collectionMethods All --includeDomainLocalGroup --enforceCertChain
```

## Understanding Output

### JSON Structure

The output JSON has:

```json
{
  "Certificate Authorities": [
    {
      "CA Name": "CA-SERVER.domain.local\\CA-NAME",
      "DNS Hostname": "ca.domain.local",
      "Enabled": true,
      "Client Authentication": true,
      "EDITF_ATTRIBUTESUBJECTALTNAME2": false,
      "...": "..."
    }
  ],
  "Certificate Templates": [
    {
      "Template Name": "VulnTemplate",
      "Display Name": "Vulnerable Template",
      "Schema Version": 2,
      "EKUs": ["1.3.6.1.5.5.7.3.2", "1.3.6.1.4.1.311.20.2.2"],
      "Enrollment Rights": ["DOMAIN\\Domain Users"],
      "Enrollee Supplies Subject": true,
      "Manager Approval": false,
      "Authorized Signatures": 0,
      "Vulnerabilities": ["ESC1"]
    }
  ]
}
```

## OPSEC Considerations

- `certipy find` generates LDAP queries that are logged as `Event ID 4662` (An operation was performed on an object)
- Multiple queries in rapid succession may trigger SOC alerts
- Use `-dc-ip` to target specific DC (avoid replication if possible)
- Consider running from a compromised Windows host with `Certify.exe` for reduced network noise
- The `-bloodhound` output needs to be exfiltrated carefully

## Detection

- **Event ID 4662**: An operation was performed on an object — look for LDAP queries against `CN=Certificate Templates`, `CN=Public Key Services`, `CN=Enrollment Services`
- **Event ID 5136**: A directory service object was modified — if attacker attempts to modify template ACLs
- Monitor for anomalous `certipy` user agent strings in LDAP traffic
- Logs are generated on the **Domain Controller** used for LDAP queries, not the CA server
