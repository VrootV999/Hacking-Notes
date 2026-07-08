# AD Recon Checklist (Pre-Compromise)

## DNS Discovery

- [ ] Enumerate DNS servers: `nslookup -type=NS <domain>` or `dnsrecon -d <domain> -t std`
- [ ] Zone transfer attempt: `dig axfr @<dns-server> <domain>` — Look for successful zone transfer (misconfiguration)
- [ ] Enumerate SRV records: `nmap --script dns-srv-enum --script-args dns-srv-enum.domain=<domain>`
- [ ] DNS brute-force subdomains: `dnsrecon -d <domain> -t brt -D <wordlist>` — Identify additional AD-integrated subdomains
- [ ] Resolve domain controllers: `nslookup -type=SRV _ldap._tcp.dc._msdcs.<domain>`
- [ ] Enumerate all DNS records: `adidnsdump -u <domain>\\<user> -p <pass> <dc-ip>` — Dump all AD-integrated DNS records (post-creds)

## Network Scanning

- [ ] Discover live hosts: `nmap -sn <subnet>/<mask> -oA live-hosts`
- [ ] Port scan top ports: `nmap -T4 -p- <target> --min-rate=1000 -oA full-portscan`
- [ ] Identify domain controllers: `nmap -p 389,636,3268,3269,88,464,135,445 <subnet>` — DCs typically have these open
- [ ] Identify SQL servers: `nmap -p 1433,1434 <subnet>` — Potential targets
- [ ] Identify web servers: `nmap -p 80,443,8080,8443 <subnet>` — Potential attack surface
- [ ] Identify RDP hosts: `nmap -p 3389 <subnet>`
- [ ] Identify WinRM hosts: `nmap -p 5985,5986 <subnet>`
- [ ] Scan for SMB signing disabled: `nmap --script smb2-security-mode -p 445 <subnet>` — Targets for NTLM relay
- [ ] Check for MS17-010 (EternalBlue): `nmap --script smb-vuln-ms17-010 -p 445 <targets>`
- [ ] Identify hosts with SMBv1 enabled: `nmap --script smb-protocols -p 445 <targets>`

## SMB Null Sessions (Pre-Creds)

- [ ] Test null SMB session: `smbclient -N -L //<target-ip>` — Look for shares accessible without creds
- [ ] Null session enum via rpcclient: `rpcclient -U "" -N <target-ip>` then `srvinfo`, `enumdomusers`, `enumdomgroups`
- [ ] Enumerate shares via SMBMap: `smbmap -u "" -p "" -H <target-ip>`
- [ ] Null SMB user enumeration: `enum4linux -U <target-ip>`
- [ ] Enumerate OS info via null session: `enum4linux -O <target-ip>`
- [ ] Enumerate password policy via null session: `enum4linux -P <target-ip>` — Useful for password spray targeting

## Anonymous LDAP (Pre-Creds)

- [ ] Test anonymous LDAP bind: `ldapsearch -x -H ldap://<dc-ip> -b "dc=<domain>,dc=<tld>"` — LDAP allows anonymous binds if misconfigured
- [ ] Enumerate domain naming context: `ldapsearch -x -H ldap://<dc-ip> -s base namingcontexts`
- [ ] Enumerate users via anonymous LDAP: `ldapsearch -x -H ldap://<dc-ip> -b "dc=<domain>,dc=<tld>" "(objectClass=user)" sAMAccountName`
- [ ] Enumerate groups via anonymous LDAP: `ldapsearch -x -H ldap://<dc-ip> -b "dc=<domain>,dc=<tld>" "(objectClass=group)" name`
- [ ] Enumerate computers via anonymous LDAP: `ldapsearch -x -H ldap://<dc-ip> -b "dc=<domain>,dc=<tld>" "(objectClass=computer)" dNSHostName`

## User Enumeration (Pre-Creds)

- [ ] Enumerate users via Kerberos (Kerbrute): `kerbrute userenum -d <domain> <userlist> --dc <dc-ip>` — Non-intrusive user enumeration, no logs on DC
- [ ] RID cycling: `crackmapexec smb <target-ip> -u '' -p '' --rid-brute` — Brute-force RIDs to discover user accounts
- [ ] Check for common usernames via AS-REP: `kerbrute userenum -d <domain> --dc <dc-ip> users.txt` — AS-REP requests reveal valid users
- [ ] Validate usernames via NTP: `ntp-wait -v <dc-ip>` — NTP doesn't help directly, but time sync is needed for Kerberos

## Password Policy Enumeration

- [ ] Enumerate via null session: `enum4linux -P <target-ip>`
- [ ] Enumerate via LDAP (if anonymous bind allowed): `ldapsearch -x -H ldap://<dc-ip> -b "dc=<domain>,dc=<tld>" "(objectClass=domain)" lockoutThreshold lockoutDuration lockOutObservationWindow minPwdLength pwdHistoryLength`
- [ ] Enumerate via CrackMapExec: `crackmapexec smb <target-ip> -u <user> -p <pass> --pass-pol` (post-creds)
- [ ] Check fine-grained password policies: `ldapsearch -x -H ldap://<dc-ip> -b "cn=Fine-Grained Password Policies,cn=System,dc=<domain>,dc=<tld>"` — Look for PSOs that may have weaker requirements

## OSINT / External Recon

- [ ] Harvest emails via LinkedIn/Google dorking: `site:linkedin.com/in "companyname"`
- [ ] Discover subdomains: `amass enum -d <domain>` or `subfinder -d <domain>`
- [ ] Find leaked creds via DeHashed/HaveIBeenPwned: Search company domain for breaches
- [ ] Enumerate GitHub for leaks: `gitdumper <url>` or search for config files with passwords
- [ ] Discover certificate transparency logs: `crt.sh -d <domain>` — Identify subdomains
- [ ] Enumerate SPF/DMARC records: `dig txt _dmarc.<domain>` — Understand email infrastructure
- [ ] Shodan search: `shodan search org:"<company>"` — Identify exposed services

## Pre-Creds AD Environment Mapping

- [ ] Identify domain via SMB: `nmap --script smb-os-discovery -p 445 <target-ip>` — OS and domain info
- [ ] Identify domain via Kerberos: `nmap -p 88 --script krb5-enum-users --script-args krb5-enum-users-realm='<domain>' <dc-ip>`
- [ ] Check for web enrollment portals: `nmap -p 443 --script http-title <dc-ip>` / `certsvc` — Identify AD CS endpoints
- [ ] Check for Exchange: `nmap -p 443 --script http-title <exchange-ip>` — Exchange often means privileged accounts
- [ ] Check for ADFS: `nmap -p 443 <adfs-ip>` — Federation endpoints, potential token attacks

## OPSEC Notes

- `Nmap scanning` will trigger IDS/IPS if not throttled; use `-T2` or `--scan-delay` for stealth
- `Kerbrute` user enumeration is stealthier than SMB/LDAP as pre-auth failures log differently
- `Null sessions` are rare on modern AD but worth checking on legacy or misconfigured domains
- Use `proxychains` or `socks` proxies for scanning in engagement scenarios
- Always use a VPN/proxy external to the target; never scan from your real IP
- Log your recon steps for attribution during debrief
