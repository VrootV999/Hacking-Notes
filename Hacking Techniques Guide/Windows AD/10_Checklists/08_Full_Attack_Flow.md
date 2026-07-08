# Full AD Attack Flow: End-to-End

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          PRE-ENGAGEMENT                                     │
│  - Define scope, rules of engagement, targets                                │
│  - Receive IP ranges, domain names, any provided creds                       │
│  - Set up C2 infrastructure, redirectors, domains                            │
│  - Prepare tooling: C2 implant, PowerView, Mimikatz, Rubeus, Impacket, etc.  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: RECONNAISSANCE (PRE-COMPROMISE)                                    │
│ GOAL: Map the environment without credentials                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  EXTERNAL RECON                                                              │
│  ├── OSINT: LinkedIn, Shodan, crt.sh, GitHub, HaveIBeenPwned                 │
│  ├── [ ] DNS discovery: nslookup/dnsrecon for NS, MX, SRV records           │
│  ├── [ ] Subdomain enumeration: amass/subfinder/crt.sh                       │
│  ├── [ ] Identify exposed services: VPN, OWA, ADFS, RDS, Citrix             │
│  └── [ ] Password spray external services (if in scope and MFA not enforced)│
│                                                                              │
│  INTERNAL RECON                                                              │
│  ├── [ ] Network sweep (nmap -sn) to discover live hosts                    │
│  ├── [ ] Full port scan on discovered hosts                                 │
│  ├── [ ] Identify DCs (port 389, 636, 88, 464, 445 open)                    │
│  ├── [ ] Identify infrastructure: Exchange, SQL, CA, WSUS, SCCM             │
│  ├── [ ] Null session check (SMB/LDAP anonymous access)                     │
│  ├── [ ] SMB signing scan → identify relay candidates                       │
│  ├── [ ] Kerbrute user enumeration (stealthy)                               │
│  ├── [ ] AS-REP roast scan (pre-creds)                                      │
│  └── [ ] Record findings: DC IPs, subnet topology, users, services          │
│                                                                              │
│  DECISION POINT: Did we find exposed creds, null sessions, or vulns?        │
│  YES → Move to Initial Access                                                │
│  NO  → Need password spray or LLMNR/NBT-NS poison if on L2                  │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: INITIAL ACCESS / FOOTHOLD                                          │
│ GOAL: Obtain first set of credentials or code execution                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Choose technique based on recon findings:                                  │
│                                                                              │
│  [ ] AS-REP Roasting → hashcat -m 18200 → plaintext password                │
│  │     └── Gained: low-priv or privileged user creds                        │
│  │                                                                          │
│  [ ] Kerberoasting → hashcat -m 13100 → service account password            │
│  │     └── Gained: service account creds (often local admin)                │
│  │                                                                          │
│  [ ] Password Spray → valid user:password pair found                        │
│  │     └── Gained: user creds, maybe privileged                            │
│  │                                                                          │
│  [ ] LLMNR/NBT-NS Poisoning (Responder) → NTLMv2 hash captured              │
│  │     └── [ ] Crack hash → password gained                                 │
│  │     └── [ ] Relay hash (if SMB signing off) → access to target           │
│  │                                                                          │
│  [ ] mitm6 + NTLM relay → relayed auth to DC/LDAP → new machine account     │
│  │     └── Gained: machine account or user TGT                              │
│  │                                                                          │
│  [ ] ZeroLogon (CVE-2020-1472) → DC password nulled → DCSync all hashes     │
│  │     ⚠ Destructive: RESTORE password after dumping                        │
│  │                                                                          │
│  [ ] PrintNightmare → SYSTEM on target                                      │
│  │                                                                          │
│  [ ] GPP / SYSVOL → plaintext password from Groups.xml                     │
│  │                                                                          │
│  └── Regardless of technique, DOCUMENT: discovered users, hashes, passwords│
│                                                                              │
│  ONCE CREDENTIALS OBTAINED:                                                  │
│  [ ] Validate access with CrackMapExec                                      │
│  [ ] Drop initial C2 beacon                                                 │
│  [ ] Establish persistence (simple: scheduled task, service, WMI)           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: POST-COMPROMISE ENUMERATION                                        │
│ GOAL: Understand the AD environment thoroughly                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  CORE AD ENUMERATION:                                                        │
│  [ ] Domain info: SID, DCs, functional levels                               │
│  [ ] All domain users → look for descriptions with passwords                │
│  [ ] All domain groups → nested memberships                                │
│  [ ] All computers → OS versions, creation dates, location                  │
│  [ ] OUs → structure, GPO links                                             │
│  [ ] Trust relationships → domain trusts, forest trusts                    │
│                                                                              │
│  VULNERABILITY SCANNING:                                                     │
│  [ ] SPNs → Kerberoast targets                                              │
│  [ ] AS-REP → pre-auth disabled users                                       │
│  [ ] Delegation → unconstrained, constrained, RBCD                          │
│  [ ] ACLs → Find-InterestingDomainAcl or BloodHound                         │
│  [ ] AD CS → vulnerable certificate templates (ESC1-ESC8)                   │
│  [ ] GPO → readable/writable GPOs, GPP passwords                            │
│  [ ] LAPS → who can read, enablement                                        │
│  [ ] SIDHistory → cross-domain escalation paths                             │
│  [ ] AdminSDHolder → check current ACL                                      │
│                                                                              │
│  BLOODHOUND:                                                                 │
│  [ ] Run SharpHound -c All                                                  │
│  [ ] Process in BloodHound GUI                                              │
│  [ ] Run pre-built queries: Find all paths to DA                            │
│  [ ] Identify shortest path from current user to DA                         │
│                                                                              │
│  DECISION POINT: What privileges do we have?                                 │
│  ┌──────────────────────────────────────────────────────────────────┐       │
│  │  Domain Admin → Go to Credential Access / Persistence            │       │
│  │  Local Admin on any box → Gather creds, move laterally           │       │
│  │  Standard Domain User → Look for escalation paths                │       │
│  └──────────────────────────────────────────────────────────────────┘       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: CREDENTIAL ACCESS / DUMPING                                        │
│ GOAL: Extract high-value credentials (Domain Admin, krbtgt, service accts)  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  IF DOMAIN ADMIN:                                                            │
│  [ ] DCSync (Mimikatz or Impacket secretsdump)                              │
│  │     → All user NTLM hashes                                               │
│  │     → krbtgt hash (for persistence)                                      │
│  │     → Trust passwords                                                    │
│  │                                                                          │
│  IF LOCAL ADMIN:                                                             │
│  [ ] Mimikatz sekurlsa::logonpasswords → plaintext/hashes from logged-on     │
│  [ ] Procdump LSASS → offline extraction                                    │
│  [ ] SAM + SYSTEM hive → local account hashes                               │
│  [ ] LSA secrets → service account passwords                                │
│  [ ] DPAPI master keys → vault/browser credential decryption                │
│                                                                              │
│  IF STANDARD USER:                                                           │
│  [ ] Browser credential extraction (Chrome/Firefox/Edge)                    │
│  [ ] Windows Credential Manager / Vault                                     │
│  [ ] GPP passwords if not yet extracted                                     │
│  [ ] File shares → search for sensitive files, scripts, configs             │
│  [ ] Email inbox → search for shared passwords, onboarding docs             │
│                                                                              │
│  TRIAGE COLLECTED CREDS:                                                     │
│  [ ] Categorize by privilege level                                           │
│  [ ] Test hashes: CrackMapExec against domain targets                       │
│  [ ] Crack weak hashes offline                                              │
│  [ ] Prioritize: krbtgt > DA > EA > Service Accounts > Domain Users         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: LATERAL MOVEMENT                                                   │
│ GOAL: Pivot through the environment to reach high-value targets             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TECHNIQUES (choose based on target and stealth requirements):               │
│  [ ] Pass-the-Hash (NTLM) → CrackMapExec, Impacket, wmiexec, psexec         │
│  [ ] Overpass-the-Hash → Rubeus asktgt from NTLM → Kerberos auth            │
│  [ ] Pass-the-Ticket → Export tickets, inject, access                      │
│  [ ] PsExec → Classic but noisy (PSEXESVC service)                         │
│  [ ] WMI → Quieter than PsExec, uses DCOM                                 │
│  [ ] WinRM → HTTP/HTTPS, PowerShell remoting                               │
│  [ ] Scheduled Tasks → atexec, schtasks                                    │
│  [ ] RDP → restricted admin mode (PtH over RDP)                            │
│                                                                              │
│  STRATEGY:                                                                   │
│  [ ] Lateral movement = "Hunt for DA sessions"                              │
│  [ ] On each compromised host: run credential access (Phase 4)              │
│  [ ] Check CrackMapExec --loggedon-users on targets                         │
│  [ ] When DA session found on a box:                                        │
│  │   → Wait for user to be active or force auth                            │
│  │   → Dump LSASS to steal DA creds                                        │
│  │   → Or PtH/OPtH with any DA hash you find                               │
│  └── If DA creds obtained: Phase 4 (DCSync)                                 │
│                                                                              │
│  DECISION POINT: Do we have Domain Admin?                                    │
│  YES → Final escalation to Domain Admin group, Dump krbtgt, Persist         │
│  NO  → Continue lateral movement / privilege escalation                    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 6: PRIVILEGE ESCALATION                                               │
│ GOAL: Escalate from current privileges to Domain Admin                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ANALYSIS FROM BLOODHOUND:                                                   │
│  [ ] Follow shortest path to Domain Admin                                   │
│  [ ] Check for:                                                             │
│  │   ├── Unconstrained delegation → printer bug → TGT capture              │
│  │   ├── Constrained delegation → S4U2Proxy abuse                          │
│  │   ├── RBCD → GenericWrite on computer → local admin                     │
│  │   ├── ACL abuse → ForceChangePassword, AddMember, GenericAll            │
│  │   ├── AD CS → ESC1 (certificate template abuse) → instant DA           │
│  │   ├── GPO → modify to add user to DA group or local admin               │
│  │   ├── AdminSDHolder → modify, wait 60 min for SDProp                   │
│  │   └── LAPS → read LAPS password for DC = local admin on DC → DCSync    │
│                                                                              │
│  EXECUTION:                                                                  │
│  [ ] Execute chosen escalation path                                         │
│  [ ] Verify escalated privileges (whoami /groups, crackmapexec against DC)   │
│  [ ] After obtaining DA: DCSync krbtgt + all users                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 7: PERSISTENCE                                                         │
│ GOAL: Maintain long-term access                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PRIMARY (Stealth, Long-term):                                               │
│  [ ] Golden Ticket → Mimikatz kerberos::golden, store krbtgt hash           │
│  [ ] Silver Tickets → Create for CIFS, HOST, LDAP, HTTP, WSMAN on key boxes │
│  [ ] Certificate persistence → Export DA user cert or CA private key        │
│                                                                              │
│  SECONDARY (Preferred fallback):                                             │
│  [ ] AdminSDHolder → Add backdoor user with DCSync rights                   │
│  [ ] WMI Event Subscription → Event-triggered C2 beacon                    │
│  [ ] Service persistence → Create/modify service to launch beacon           │
│                                                                              │
│  TERTIARY (Options — use with caution):                                     │
│  [ ] DSRM → Set DSRM password = DA, enable normal logon                     │
│  [ ] Skeleton Key → LSASS patch on DC (⚠ reboot = lost)                    │
│  [ ] DCShadow → Push malicious attributes via fake DC replication           │
│  [ ] SSP → Register malicious SSP on DC (password logging)                  │
│  [ ] GPO → Add startup scripts or restricted groups                         │
│                                                                              │
│  DOCUMENTATION:                                                              │
│  [ ] Record all persistence methods used                                     │
│  [ ] Record krbtgt hash, golden ticket params, cert serial numbers           │
│  [ ] Record backdoor user names and passwords                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 8: COVER TRACKS / CLEANUP                                             │
│ GOAL: Remove evidence of compromise (or document for client)                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  IF CLEANUP REQUIRED (PER ENGAGEMENT SCOPE):                                │
│  [ ] Remove all C2 beacons / implants                                       │
│  [ ] Delete all created users                                               │
│  [ ] Remove user from all added groups                                      │
│  [ ] Revert ACL changes (AdminSDHolder, object permissions)                 │
│  [ ] Revert GPO modifications to original settings                          │
│  [ ] Delete scheduled tasks                                                 │
│  [ ] Remove added services                                                  │
│  [ ] Delete registry run keys                                               │
│  [ ] Remove WMI subscriptions                                                │
│  [ ] Reset DSRM password if changed                                         │
│  [ ] Restore any modified LSASS patches (skeleton key requires reboot)       │
│  [ ] Delete dumped files (LSASS dumps, NTDS.dit, hashes, logs)              │
│  [ ] Clear PowerShell history: rm $env:APPDATA\Microsoft\Windows\PowerShell\ │
│      PSReadLine\ConsoleHost_history.txt                                      │
│  [ ] Clear event logs if necessary: Wevtutil cl System / Security / App     │
│  [ ] Remove tools/binaries from all systems                                  │
│  [ ] Check for any additional tools dropped                                  │
│                                                                              │
│  EVIDENCE COLLECTION (FOR DEBRIEF):                                          │
│  [ ] Screenshots of key findings                                             │
│  [ ] Logs of commands executed                                               │
│  [ ] Timeline of actions                                                     │
│  [ ] Password/hash lists (anonymized for report)                             │
│  [ ] Network diagrams with attack paths                                      │
│  [ ] Recommendations for each finding                                        │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          DEBRIEF & REPORTING                                │
│  - Executive summary for non-technical stakeholders                          │
│  - Technical findings with AD attack paths                                   │
│  - Remediation recommendations per finding                                   │
│  - Timeline of attack flow                                                   │
│  - Password/hash exposure (minimized)                                        │
│  - Highlight critical risks: krbtgt hash loss, AD CS misconfigs, ACLs       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Decision Flow (Quick Reference)

### At each phase, ask:

1. **Recon**: "What's exposed? Where are targets?"
2. **Initial Access**: "Can I get a foothold without triggering alerts?"
3. **Enumeration**: "What escalation paths exist from my current position?"
4. **Credential Access**: "Do I have DA? If yes, DCSync. If no, dump LSASS."
5. **Lateral Movement**: "Where are DA sessions present?"
6. **Privilege Escalation**: "What's the shortest path to DA from current user?"
7. **Persistence**: "What happens if I lose access? Have I secured krbtgt?"
8. **Cleanup**: "What evidence remains?" / "What does the client need to fix?"

### Priority Escalation Paths

```
Most Common / Effective:
1. ACL Abuse (BloodHound will find this)  →  DA
2. AD CS ESC1 (Certificate template)      →  DA
3. Unconstrained Delegation + Printer Bug →  TGT Capture → DA
4. RBCD (GenericWrite on computer)        →  Local admin → creds → DA
5. GPO Modification                       →  DA

If all else fails:
6. AdminSDHolder                          →  DA (noisy, 60 min wait)
7. Exchange group abuse                   →  DA (if Exchange present)
8. LAPS password read on DC               →  Local admin → DCSync → DA
```

--- 

## Quick Command Reference by Phase

| Phase | Tool | Command |
|---|---|---|
| Recon | nmap | `nmap -sV -p 389,636,88,445,3389,5985,5986 <subnet>` |
| Recon | kerbrute | `kerbrute userenum -d <domain> --dc <dc-ip> users.txt` |
| Initial Access | GetNPUsers | `GetNPUsers.py <domain>/ -usersfile users.txt -format hashcat` |
| Initial Access | GetUserSPNs | `GetUserSPNs.py <domain>/<user>:<pass> -request` |
| Enumeration | PowerView | `Get-NetUser -SPN / -PreauthNotRequired / -AdminCount` |
| Enumeration | SharpHound | `SharpHound.exe -c All` |
| Cred Access | mimikatz | `sekurlsa::logonpasswords` |
| Cred Access | secretsdump | `secretsdump.py <domain>/<user>:<pass>@<dc-ip> -just-dc` |
| Lateral Move | crackmapexec | `crackmapexec smb <target> -u <user> -H <hash> -x whoami` |
| Lateral Move | wmiexec | `wmiexec.py -hashes <lm:nt> <domain>/<user>@<target>` |
| Priv Esc | Rubeus | `Rubeus s4u /user:<user> /rc4:<hash> /impersonateuser:admin /msdsspn:"cifs/<target>"` |
| Priv Esc | rbcd | `rbcd.py <domain>/<user>:<pass> -dc-ip <dc> -target <comp> -action write` |
| Persistence | mimikatz | `kerberos::golden /user:Administrator /domain:<domain> /sid:<sid> /krbtgt:<hash> /ptt` |
| Persistence | Rubeus | `Rubeus golden /rc4:<krbtgt> /user:admin /domain:<domain> /sid:<sid> /ptt` |
