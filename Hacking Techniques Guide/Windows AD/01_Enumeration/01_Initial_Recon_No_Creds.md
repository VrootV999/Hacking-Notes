# No-Creds Initial Reconnaissance

## Overview

Initial recon is performed without any domain credentials. The goal is to identify domain controllers, enumerate domain users, discover shares, and gather information that can be used for initial access (password spraying, AS-REP roasting, etc.). In modern environments, many of these techniques have limited effectiveness but can yield results in poorly configured domains.

## DNS Reconnaissance

### Basic DNS Lookups

```bash
# DNS resolution of domain controllers
nslookup domain.local
nslookup domain.local <dc-ip>

# SRV record lookup (LDAP, Kerberos, GC)
nslookup -type=SRV _ldap._tcp.dc._msdcs.domain.local
nslookup -type=SRV _kerberos._tcp.domain.local
nslookup -type=SRV _gc._tcp.domain.local

# Alternative with dig
dig SRV _ldap._tcp.dc._msdcs.domain.local @<dc-ip>
dig SRV _kerberos._tcp.domain.local @<dc-ip>
dig SRV _gc._tcp.domain.local @<dc-ip>

# Zone transfer attempt (rarely works externally)
dig axfr @<dns-server> domain.local
nslookup -type=any domain.local <dns-server>
```

### DNS Enumeration with dnsrecon

```bash
# SRV records
dnsrecon -d domain.local -t srv -n <dc-ip>

# Zone transfer attempt
dnsrecon -d domain.local -t axfr -n <dc-ip>

# Standard enumeration
dnsrecon -d domain.local -t std -n <dc-ip>
```

### DNS-Dumpster (web-based)

```bash
# Automated DNS recon via CLI tools
dnsenum --enum domain.local -n <dc-ip>
dnsmap domain.local
```

## Nmap Scanning

### Discovery Scans

```bash
# Quick ping sweep
nmap -sn <subnet>/24 -oA ping-sweep

# Find open ports on DCs
nmap -p 53,88,135,139,389,445,636,3268,3269,5985,9389 <ip-range> -oA dc-port-scan

# Full TCP scan
nmap -p- -T4 <target> -oA full-tcp

# NSE scripts for AD enumeration
nmap --script smb-os-discovery.nse -p 445 <dc-ip>
nmap --script smb-security-mode.nse -p 445 <dc-ip>
nmap --script smb-protocols.nse -p 445 <dc-ip>
nmap --script ldap-rootdse.nse -p 389 <dc-ip>

# All relevant enum scripts
nmap -sC -sV -p 53,88,135,139,389,445,464,593,636,3268,3269,3389,5985,5986,9389 <dc-ip>
```

### Detailed SMB Scripts

```bash
# Comprehensive SMB enumeration
nmap --script smb-enum-shares -p 445 <target>
nmap --script smb-enum-users -p 445 <target>
nmap --script smb-enum-groups -p 445 <target>
nmap --script smb-enum-domains -p 445 <target>
nmap --script smb-enum-services -p 445 <target>
nmap --script smb-enum-processes -p 445 <target>
nmap --script smb-enum-sessions -p 445 <target>

# SMB vulnerability checks
nmap --script smb-vuln-* -p 445 <target>
nmap --script smb2-capabilities -p 445 <target>
nmap --script smb-ls -p 445 <target>
```

## SMB Null Session Enumeration

### Testing for Null/Anonymous Access

```bash
# NetExec SMB null session check
nxc smb <dc-ip> -u '' -p '' --shares
nxc smb <dc-ip> -u 'a' -p ''

# With enum4linux-ng
enum4linux-ng -A <dc-ip> -u '' -p ''
enum4linux-ng -A <dc-ip> -u 'Guest' -p ''

# With smbclient
smbclient -L //<dc-ip> -N
smbclient -L //<dc-ip>/ -U '' -N

# With rpcclient
rpcclient -U '' -N <dc-ip>
rpcclient -U ''%'' <dc-ip>

# smbmap (null session)
smbmap -H <dc-ip> -u '' -p ''
smbmap -H <dc-ip> -u 'null' -p ''
```

### RPC Commands via Null Session

```bash
# Connect with rpcclient (if null session works)
rpcclient -U '' -N <dc-ip>

# Inside rpcclient: server info
srvinfo
netdomenjoin
netservergetinfo 2

# Inside rpcclient: user enumeration
enumdomusers
enumdomgroups
queryuser <rid>
enumalsgroups builtin

# Inside rpcclient: domain info
querydominfo
enumdomains
lsaquery
lookupdomain <domain>
```

## RID Cycling

### Automated RID Cycling

```bash
# NetExec RID brute-force
nxc smb <dc-ip> -u '' -p '' --rid-brute
nxc smb <dc-ip> -u 'user' -p 'pass' --rid-brute

# crackmapexec (older syntax)
cme smb <dc-ip> -u '' -p '' --rid-brute 10000

# ridcycle.py (Impacket)
ridcycle.py <domain>/''''@<dc-ip>
ridcycle.py <domain>/'user':'pass'@<dc-ip> 10000

# enum4linux-ng (includes RID cycling)
enum4linux-ng -A -r <dc-ip> -u '' -p ''
```

### Manual RID Cycling with rpcclient

```bash
# Enumerate users by RID range (500-10000)
rpcclient $> lookupsids S-1-5-21-<domain-sid>-500
rpcclient $> lookupsids S-1-5-21-<domain-sid>-501
rpcclient $> lookupsids S-1-5-21-<domain-sid>-502
# ... iterate through RIDs

# Alternative: get domain SID first
rpcclient $> lsaquery
rpcclient $> enumdomusers
```

## Anonymous LDAP Enumeration

### Testing Anonymous LDAP Access

```bash
# Basic ldapsearch (null bind)
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s base "(objectClass=*)" namingContexts

# If naming contexts returned, enumerate further:
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s sub "(objectClass=user)" samaccountname cn

# Enumerate all objects (if anonymous bind works)
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" "(objectClass=*)"

# Check anonymous access with ldapsearch
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s sub "(objectClass=domain)"

# Enumerate domain users
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s sub "(&(objectClass=user)(objectCategory=person))" sAMAccountName userPrincipalName memberOf

# Enumerate groups
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s sub "(objectClass=group)" sAMAccountName member

# Enumerate computers
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s sub "(objectClass=computer)" dNSHostName operatingSystem

# Enumerate domain policies
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s sub "(objectClass=domainPolicy)"
```

### Using NetExec for Anonymous LDAP

```bash
# Null LDAP query
nxc ldap <dc-ip> -u '' -p '' -M ad_enum

# Check LDAP anonymous access
nxc ldap <dc-ip> -u '' -p '' --users
nxc ldap <dc-ip> -u '' -p '' --groups

# Anonymous LDAP with machine account
nxc ldap <dc-ip> -u '$' -p ''
```

## enum4linux-ng

### Full Enumeration

```bash
# Comprehensive enumeration (like enum4linux but updated)
enum4linux-ng -A <dc-ip> -u '' -p ''

# Without credentials
enum4linux-ng -A -U -S -G -P -r -R -M <dc-ip>

# With credentials (if available)
enum4linux-ng -A -u 'domain\user' -p 'password' <dc-ip>

# Individual check types
enum4linux-ng -U <dc-ip>          # User enumeration
enum4linux-ng -G <dc-ip>          # Group enumeration  
enum4linux-ng -S <dc-ip>          # Share enumeration
enum4linux-ng -P <dc-ip>          # Password policy
enum4linux-ng -r <dc-ip>          # RID cycling
enum4linux-ng -M <dc-ip>          # Machine info
enum4linux-ng -i <dc-ip>          # LSA policy info

# Custom RID range
enum4linux-ng -R <dc-ip> -R 1000-2000
```

## NetExec (Unauthenticated)

```bash
# Null session check
nxc smb <dc-ip> -u '' -p ''

# Anonymous logon check
nxc smb <dc-ip> -u 'a' -p ''

# Maps to check via null session
nxc smb <dc-ip> -u '' -p '' --shares

# NetExec LDAP anonymous checks
nxc ldap <dc-ip> -u '' -p ''
nxc ldap <dc-ip> -u '' -p '' -M ad_enum

# Password policy via null session
nxc smb <dc-ip> -u '' -p '' --pass-pol

# OS discovery
nxc smb <dc-ip> -u '' -p '' -M enum_av
nxc smb <dcip> -u '' -p '' --os
```

## Responder / Network Sniffing (Pre-Brute)

```bash
# Start Responder to capture LLMNR/NBT-NS/mDNS
sudo responder -I eth0 -wPv

# Inveigh (PowerShell LLMNR/NBNS spoofer)
Import-Module .\Inveigh.psd1
Invoke-Inveigh -NBNS Y -LLMNR Y -mDNS Y -Tool LLMNR -ConsoleOutput Y

# mitm6 (IPv6 DNS takeover)
sudo mitm6 -d domain.local -i eth0
```

## Password Policy Retrieval (No Creds)

```bash
# If null SMB session works
enum4linux-ng -P <dc-ip>
nxc smb <dc-ip> -u '' -p '' --pass-pol
rpcclient -U '' -N <dc-ip> -c "getdompwinfo"

# Without SMB: try LDAP anonymous 
ldapsearch -x -H ldap://<dc-ip> -b "DC=domain,DC=local" -s sub "(objectClass=domain)" minPwdLength lockoutThreshold
```

## Domain Information via LDAP RootDSE

```bash
# Connect to LDAP anonymously and read RootDSE
ldapsearch -x -H ldap://<dc-ip> -b "" -s base "(objectClass=*)"
nmap --script ldap-rootdse -p 389 <dc-ip>

# Key values to extract:
#   namingContexts        → domain DN
#   defaultNamingContext   → default domain DN
#   dnsHostName           → DC hostname
#   domainFunctionality   → domain functional level
#   forestFunctionality   → forest functional level  
#   supportedCapabilities → active directory features (LAPS, etc.)
#   subschemaSubentry     → schema path
```

## Domain Controller Discovery

```bash
# DNS-based DC discovery
nslookup -type=SRV _ldap._tcp.dc._msdcs.domain.local
nslookup -type=SRV _kerberos._tcp.domain.local

# nltest (from Windows domain-joined system)
nltest /dclist:domain.local
nltest /dsgetdc:domain.local

# NET command
net group "Domain Controllers" /domain

# Without domain-joined: use DNS
dig +short SRV _ldap._tcp.dc._msdcs.domain.local @<dns-ip>
dig +short SRV _kerberos._tcp.domain.local @<dns-ip>

# Get AD IPs through nmap
nmap --script broadcast-dns-service-discovery
```

## Additional Unauthenticated Checks

```bash
# Check for SMB signing requirements
nxc smb <dc-ip> -u '' -p '' -M smb_signing
nmap --script smb2-capabilities -p 445 <dc-ip>

# Check for WebDAV anonymous access
nxc webdav <dc-ip> -u '' -p ''

# Check for WinRM
nxc winrm <dc-ip> -u '' -p ''

# Test MSSQL (port 1433) - null session
nxc mssql <dc-ip> -u 'sa' -p ''

# NBT-NS enumeration
nmblookup -A <dc-ip>
nbtscan -r <subnet>/24
```

## Unauthenticated Attack Scripts / Tools

```bash
# PyLDAPSearch for anonymous LDAP
python3 -c "
import ldap3
server = ldap3.Server('dc-ip', get_info=ldap3.ALL)
conn = ldap3.Connection(server, authentication=ldap3.ANONYMOUS)
conn.bind()
print(server.info)
"

# SmbGhost scanner
python3 MS17-010-scanner.py <dc-ip>

# ZeroLogon scanner
python3 zerologon.py <dc-ip> domain.local
nxc smb <dc-ip> -u '' -p '' -M zerologon

# NoPac scanner
nxc smb <dc-ip> -u '' -p '' -M nopac

# PrintNightmare scanner
python3 CVE-2022-x.py <dc-ip>

# MS14-068 scanner (PAC spoofing)
python3 ms14-068.py -u <user> -p <pass> -s <user-sid> -d domain.local
```

## Resource Discovery (Without Domain Joining)

```bash
# List time sources (DC via NTP)
ntpdate -q <dc-ip>

# Check if kerberos is accessible
nmap -sS -p 88 --script krb5-enum-users <dc-ip>

# RPC portmap
rpcclient -U '' -N <dc-ip> -c "srvinfo"
```

## Stealth / OPSEC Considerations

- **Use LDAP instead of SMB**: LDAP anonymous queries are less likely to trigger alerts than SMB null sessions
- **Rotate source IPs**: When possible, rotate IPs or use proxies to avoid triggering account lockouts
- **Limit user enumeration**: RID cycling with large ranges triggers Windows event 4625
- **Time queries**: Spread out requests over hours to avoid threshold-based detection
- **Avoid nmap -sC on production**: The default script scan can be noisy; use targeted scripts
- **DNS queries are logged**: DNS query logs may be monitored; use alternate methods when possible
- **Guest account**: Check if Guest is enabled; can be used similar to null session on legacy systems
- **Windows Filtering Platform (WFP)**: Port scans are logged via event 5152, 5154

## Detection Notes

| Activity | Event ID | What to Look For |
|----------|----------|------------------|
| DNS SRV query | 3000+ | DNS Server logs showing _ldap._tcp SRV queries |
| Anonymous LDAP bind | 4662 | Object access audit on Directory Service Access |
| SMB null session | 5140 | Anonymous logon type 3 over SMB |
| RID cycling | 4625 | Many logon failures from same IP with different usernames |
| Port scan | 5152, 5154 | WFP packet drop; connection attempts across many ports |
| Failed logins (enum) | 4771 | Pre-authentication failures indicating user enumeration |
| NBT-NS queries | 8001 | Browser protocol broadcasts |

## Quick Reference Cheat Sheet

```bash
# 1. DNS Discovery
nslookup -type=SRV _ldap._tcp.dc._msdcs.<domain>

# 2. Check Null SMB
nxc smb <dc> -u '' -p '' --shares

# 3. Check Guest Access  
nxc smb <dc> -u 'Guest' -p '' --shares

# 4. RID Cycling (if null works)
nxc smb <dc> -u '' -p '' --rid-brute

# 5. Get Domain SID
rpcclient -U '' -N <dc> -c "lsaquery"

# 6. Enum4linux-ng comprehensive
enum4linux-ng -A <dc> -u '' -p ''

# 7. Anonymous LDAP naming contexts
ldapsearch -x -H ldap://<dc> -b "" -s base "(objectClass=*)" namingContexts

# 8. Password Policy
nxc smb <dc> -u '' -p '' --pass-pol

# 9. Domain Info
nxc smb <dc> -u '' -p '' --os

# 10. LDAP anonymous user enumeration
ldapsearch -x -H ldap://<dc> -b "DC=domain,DC=local" "(objectClass=user)" sAMAccountName -D '' -w ''
```
