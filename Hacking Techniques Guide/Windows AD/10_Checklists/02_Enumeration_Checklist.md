# Post-Compromise Enumeration Checklist

## Domain Information

- [ ] Get domain info: `Get-NetDomain` — Basic domain name, SID, DC info
- [ ] Get domain SID: `Get-DomainSID` — Needed for Golden/Silver tickets
- [ ] Get domain policy: `Get-DomainPolicy` — Password policy, lockout, kerberos policy
- [ ] Get DC details: `Get-NetDomainController` — List all DCs, their OS versions, site info
- [ ] Enumerate AD sites and subnets: `Get-NetSite | Get-NetSubnet` — Physical network topology via AD

## User Enumeration

- [ ] Enumerate all domain users: `Get-NetUser | select cn, samaccountname, objectsid, description`
- [ ] Find users with descriptions containing passwords: `Get-NetUser -Description "*pass*"` — Common admin mistake
- [ ] Find disabled users: `Get-NetUser -UACFilter ACCOUNTDISABLE` — May be re-enabled as backdoor
- [ ] Find privileged users: `Get-NetUser -AdminCount` — Users with adminCount=1 (protected)
- [ ] Find users in specific OUs: `Get-NetUser -ADSPath "OU=Admins,DC=<domain>,DC=<tld>"`
- [ ] Find last logon timestamps: `Get-NetUser -Properties lastlogontimestamp, samaccountname` — Identify stale accounts
- [ ] Find users who never logon: `Get-NetUser -UACFilter PASSWD_NOTREQD` — Weak accounts
- [ ] Find users with SPNs: `Get-NetUser -SPN` or `setspn -T <domain> -Q */*`
- [ ] List all user objects with all properties: `Get-NetUser | Get-ObjectAcl`

## Group Enumeration

- [ ] Enumerate all domain groups: `Get-NetGroup -FullData`
- [ ] Get Domain Admin members: `Get-NetGroupMember "Domain Admins" -Recurse`
- [ ] Get Enterprise Admin members: `Get-NetGroupMember "Enterprise Admins" -Recurse`
- [ ] Get Schema Admin members: `Get-NetGroupMember "Schema Admins" -Recurse`
- [ ] Get Administrators members: `Get-NetLocalGroup -ComputerName <target>` — Local admin groups across domain
- [ ] Get nested group memberships: `Get-NetGroupMember <group> -Recurse` — Follow nested group chains
- [ ] Find users with DCSync rights: `Get-ObjectAcl -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "Replicating" }`
- [ ] List foreign security principals: `Get-NetForeignGroupMember` — Cross-domain/forest trust groups
- [ ] Enumerate local groups on all servers: `Invoke-ShareFinder -CheckShareAccess`

## Computer Enumeration

- [ ] Enumerate all domain computers: `Get-NetComputer | select dnshostname, operatingsystem, whencreated`
- [ ] Find computers with OS version details: `Get-NetComputer -FullData` — Identify old/unpatched systems
- [ ] Find computers in specific site: `Get-NetSite -SiteName <site> | Get-NetSubnet`
- [ ] Find domain controllers: `Get-NetComputer -Ping | ? { $_.operatingsystem -match "Server" }`
- [ ] Find SQL servers: `Get-NetComputer | ? { $_.operatingsystem -match "SQL" }`
- [ ] Find computers with constrained delegation: `Get-NetComputer -TrustedToAuth`
- [ ] Find computers with unconstrained delegation: `Get-NetComputer -Unconstrained`

## Group Policy Enumeration

- [ ] List all GPOs: `Get-NetGPO` — Display all GPO names and IDs
- [ ] Get GPO details: `Get-NetGPO -GPOName "<name>"` — Full GPO settings
- [ ] Find GPOs applied to specific OU: `Get-NetGPO -ADSpath "LDAP://OU=<ou>,DC=<domain>,DC=<tld>"`
- [ ] Find GPOs that modify local admin groups: `Get-NetGPO -ComputerName <target>` — Restricted groups
- [ ] Find GPOs with logon scripts: `Get-NetGPO -GPOName "<name>" | select *script*` — Potential code execution
- [ ] Find GPOs with vulnerable settings: `Get-NetGPO -GPOName "<name>" | select *password*` — LAPS/GPP?
- [ ] Locate SYSVOL for GPP passwords: `ls \\<domain>\SYSVOL\<domain>\Policies\`

## OU Enumeration

- [ ] Enumerate all OUs: `Get-NetOU -FullData`
- [ ] Get GPOs linked to OUs: `Get-NetGPO -ADSpath "LDAP://OU=<ou>,DC=<domain>,DC=<tld>"| select displayname, gpcFileSysPath`
- [ ] Find delegations on OUs: `Get-ObjectAcl -ADSpath "OU=<ou>,DC=<domain>,DC=<tld>" -ResolveGUIDs`
- [ ] Enumerate objects in each OU: `Get-NetOU <ou> | % { Get-NetComputer -ADSpath $_.adspath }`

## ACL Enumeration

- [ ] Enumerate ACLs for Domain Admins group: `Get-ObjectAcl -ResolveGUIDs -SamAccountName "Domain Admins"` — Who can modify DA?
- [ ] Find interesting ACLs (GenericAll/GenericWrite): `Find-InterestingDomainAcl -ResolveGUIDs`
- [ ] Enumerate ACL for Domain Admins (PowerView): `Invoke-ACLScanner -ResolveGUIDs`
- [ ] Find ACLs that grant DCSync: `Get-ObjectAcl -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "ExtendedRight" -and $_.ObjectType -eq "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2" }`
- [ ] Check user rights: `Get-ObjectAcl -SamAccountName <user> -ResolveGUIDs`
- [ ] Recursive ACL checking: `Find-InterestingDomainAcl -ResolveGUIDs` — Slow but exhaustive

## Trust Enumeration

- [ ] Enumerate domain trusts: `Get-NetDomainTrust` — Identify trust relationships
- [ ] Enumerate forest trusts: `Get-NetForestTrust` — Cross-forest trust relationships
- [ ] Enumerate all domains in forest: `Get-NetForestDomain`
- [ ] Enumerate trusts from the current forest: `Get-NetForestTrust -Forest <forest>`
- [ ] Check SID filtering status: `Get-NetDomainTrust | select TrustProperties` — Check if SID filtering is enabled
- [ ] Enumerate trusted domain objects: `Get-NetDomainTrust -Domain <domain>` — Bidirectional trust info

## Delegation Enumeration

- [ ] Find unconstrained delegation systems: `Get-NetComputer -Unconstrained` — Compromise = any user's TGT
- [ ] Find constrained delegation users/computers: `Get-NetUser -TrustedToAuth` / `Get-NetComputer -TrustedToAuth`
- [ ] Find resource-based constrained delegation (RBCD) targets: `Get-NetComputer | Get-ObjectAcl -ResolveGUIDs | ? { $_.ActiveDirectoryRights -match "GenericWrite|GenericAll" -and $_.SecurityIdentifier -match "S-1-5-21" }`
- [ ] List delegation details: `Get-NetUser -TrustedToAuth | select samaccountname, msds-allowedtodelegateto`
- [ ] List computers with delegation enabled: `Get-NetComputer -TrustedToAuth | select dnshostname, msds-allowedtodelegateto`

## SPN Enumeration

- [ ] List all SPNs: `setspn -T <domain> -Q */*` or `Get-NetUser -SPN | select samaccountname, serviceprincipalname`
- [ ] List SPNs for specific service: `Get-NetUser -SPN | ? { $_.serviceprincipalname -match "MSSQL" }` — SQL servers
- [ ] List SPNs for HTTP services: `Get-NetUser -SPN | ? { $_.serviceprincipalname -match "HTTP" }`
- [ ] Find SPNs for non-standard services: `Get-NetUser -SPN | select serviceprincipalname | sort -Unique` — Identify attack surface
- [ ] Check Kerberos encryption types for SPNs: `Get-NetUser -SPN | select samaccountname, serviceprincipalname, msds-supportedencryptiontypes`

## AS-REP Roast Targets

- [ ] Find users without Kerberos pre-auth: `Get-NetUser -PreauthNotRequired` — AS-REP roastable
- [ ] Get AS-REP users via CrackMapExec: `crackmapexec ldap <dc-ip> -u <user> -p <pass> --asreproast output.txt`
- [ ] Detailed AS-REP user check: `Get-NetUser -PreauthNotRequired | select samaccountname, userprincipalname, serviceprincipalname`

## AD CS (Active Directory Certificate Services)

- [ ] Enumerate CA servers: `certutil -config -` or `Get-NetComputer | ? { $_.dnshostname -match "CA|PKI|CA-SRV|SERVICENAME" }` — Look for CA/CAServer/pki naming
- [ ] Find CA via LDAP: `ldapsearch -x -H ldap://<dc-ip> -b "CN=Enrollment Services,CN=Public Key Services,CN=Services,CN=Configuration,DC=<domain>,DC=<tld>"`
- [ ] Enumerate certificate templates: `certutil -TCAInfo` or `Get-CertificationAuthority -ComputerName <ca-server>`
- [ ] Find ESC1 vulnerable templates (client auth + manager approval off + enrollee supplies subject): `Find-PKIAttackData -CA <ca>`
- [ ] Find ESC2/ESC3 vulnerable templates: `Find-PKIAttackData -CA <ca>` — Any Purpose / Signature templates
- [ ] Check ESC8 (NTLM relay to CA): Test if CA supports HTTP enrollment: `nmap -p 80,443 <ca-ip>`
- [ ] Enumerate issued certificates: `certutil -view -out "RequestID, Requestername, SerialNumber, NotBefore, NotAfter"`

## Network / System Enumeration

- [ ] Enumerate local admin users on all machines: `Invoke-ShareFinder -CheckShareAccess`
- [ ] Find open SMB shares: `Invoke-ShareFinder -ExcludeStandard`
- [ ] Find Windows Defender status: `Get-MpComputerStatus` — Check real-time monitoring status
- [ ] Enumerate local users: `Get-LocalUser`
- [ ] Enumerate local groups: `Get-LocalGroup`
- [ ] List running services: `Get-Service | ? Status -eq "Running"`
- [ ] List scheduled tasks: `Get-ScheduledTask` — Potential persistence or creds in tasks
- [ ] Check installed software: `Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*`
- [ ] Enumerate firewall rules: `netsh advfirewall firewall show rule name=all`
- [ ] Check AppLocker/AppControl policy: `Get-AppLockerPolicy -Effective`
- [ ] Check for antivirus products: `Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct`

## Object Properties / Extended Enumeration

- [ ] Find user objects with `adminCount=1`: `Get-NetUser -AdminCount` — Protected users (likely privileged)
- [ ] Check for service accounts with high privileges: `Get-NetUser -SPN -AdminCount`
- [ ] Find users with SidHistory: `Get-NetUser -SidHistory` — SID history can lead to privilege escalation
- [ ] Check LAPS password deployment: `Get-LAPSComputers` via LAPS module or `Get-NetComputer | ? { $_.ms-mcs-admpwd -ne $null }`
- [ ] Find computers with LAPS configured: `Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwdExpirationTime`

## BloodHound Data Collection

- [ ] Run SharpHound: `SharpHound.exe -c All --zipfilename output`
- [ ] Collect all data (largest): `SharpHound.exe -c All,LoggedOn --zipfilename full-data`
- [ ] Collect only ACL data: `SharpHound.exe -c ACL`
- [ ] Collect session data only (stealthy): `SharpHound.exe -c Session`
- [ ] Run from PowerShell: `Invoke-BloodHound -CollectionMethod All`
- [ ] Run with LDAP only (no network): `SharpHound.exe -c All --LDAPOnly`
- [ ] In壓 bloodhound data ingression: Upload to BloodHound GUI and run pre-built analysis queries

## OPSEC Notes

- PowerView/SharpHound generate significant LDAP traffic; use throttling for stealth
- Use `-LDAPOnly` when you want to avoid noisy network enumeration
- SharpHound session collection generates network connections to every machine — very noisy
- ACL enumeration is expensive; run targeted queries first
- Run enumeration from a compromised workstation, not from your C2 server directly
- Always use `-Domain` flag if working across trusts to avoid detection
- Clean up BloodHound zip files after ingestion — they contain sensitive AD structure data
