# SMB Protocol

## What it is

Server Message Block (SMB) is a network file-sharing protocol that allows applications on a computer to read and write to files and request services from server programs on a computer network. In Active Directory environments, SMB is the primary transport for:

- File sharing (SYSVOL, NETLOGON, home directories)
- Named pipes (for MSRPC — lsarpc, samr, netlogon, drsuapi)
- Printer sharing
- Remote administration (via named pipes)
- Authentication transport (NTLMSSP, Kerberos ticket exchange)

## SMB protocol versions (dialects)

| Dialect | Windows version | Key features |
|---------|----------------|--------------|
| **SMB 1.0 (CIFS)** | Windows NT 4.0 – Windows 2003 | Original; verbose; slow; no encryption; no signing by default; many vulnerabilities (EternalBlue, WannaCry) |
| **SMB 2.0** | Windows Vista / 2008 | Major rewrite; fewer commands (19 vs ~100); compound operations; larger reads/writes |
| **SMB 2.1** | Windows 7 / 2008 R2 | Opportunistic locking leases; improved performance |
| **SMB 3.0** | Windows 8 / 2012 | **SMB Transparent Failover**; **SMB Multichannel**; **SMB Encryption**; VSS for SMB; Directory Leasing; Improved performance |
| **SMB 3.0.2** | Windows 8.1 / 2012 R2 | Minor updates |
| **SMB 3.1.1** | Windows 10 / 2016+ | **Pre-authentication integrity** (AES-CMAC); **SMB Encryption with AES-128-GCM**; Dialect negotiation update; Cluster improvements |

## SMB over NetBIOS vs Direct SMB

### SMB over NetBIOS (legacy)

- Transport: NBF (NetBIOS Frame) or NBT (NetBIOS over TCP)
- Port: **139/TCP**
- Requires NetBIOS session service
- Used in older Windows systems; still supported for backward compatibility

### Direct SMB (modern)

- Transport: TCP directly
- Port: **445/TCP**
- No NetBIOS dependency
- Preferred in modern environments

```
NetBIOS Session (port 139)          Direct SMB (port 445)
┌────────────────────┐             ┌────────────────────┐
│ NetBIOS header     │             │ SMB header          │
│ (4 bytes: type +   │             │ (direct on TCP)     │
│  length)            │             │                     │
│  ┌──────────────┐  │             │ SMB payload         │
│  │ SMB header    │  │             │                     │
│  │ SMB payload   │  │             │                     │
│  └──────────────┘  │             └────────────────────┘
└────────────────────┘
```

## SMB ports

| Port | Protocol | Purpose |
|------|----------|---------|
| 445/TCP | SMB (direct) | Direct SMB transport — primary |
| 139/TCP | NetBIOS Session | SMB over NetBIOS — legacy |
| 137/UDP | NetBIOS Name Service | NetBIOS name resolution |
| 138/UDP | NetBIOS Datagram | NetBIOS datagram service |

## SMB authentication

SMB supports two authentication mechanisms:

### NTLMSSP (NTLM)

- Negotiated during `SESSION_SETUP` command
- Standard NTLM challenge-response (see `04_NTLM_Protocol.md`)
- Vulnerable to relay if SMB signing is not enforced

### Kerberos

- Preferred mechanism in AD environments
- Requires valid SPN on the target server
- Uses AP-REQ message (service ticket) during session setup
- Much more secure than NTLM

**Negotiation order:** Kerberos is attempted first; falls back to NTLM if Kerberos fails.

## SMB signing

SMB signing ensures the integrity of SMB traffic (and optionally encrypts it).

| Setting | Meaning |
|---------|---------|
| `Microsoft network server: Digitally sign communications (always)` | Server requires signing by all clients |
| `Microsoft network client: Digitally sign communications (always)` | Client always signs |
| `Microsoft network server: Digitally sign communications (if client agrees)` | Server supports signing but doesn't require it |
| `Microsoft network client: Digitally sign communications (if server agrees)` | Client supports signing but doesn't require it |

**Default signing status:**

| Windows Version | Client (outbound) | Server (inbound) |
|----------------|-------------------|------------------|
| Windows 2000 | Enabled when possible | Disabled |
| Windows XP/2003 | Enabled when possible | Disabled |
| Windows Vista/2008+ | Enabled when possible | Enabled when possible |
| Windows 10/2016+ | Enabled when possible | **Required** (if SMB2 or higher) |

**How SMB signing works:**

1. During `SESSION_SETUP`, the client and server negotiate signing
2. A signing key is derived from the session key
3. Each SMB message carries a signature (HMAC-SHA256 for SMB3, HMAC-MD5 for SMB2)
4. The receiver validates the signature before processing the message

**Attack relevance:** SMB relay attacks fail when signing is enforced. If signing is not enforced, an attacker can relay authentication to a server that doesn't require signing.

## SMB encryption (SMB 3.x)

SMB encryption provides **confidentiality** (not just integrity).

- **SMB 3.0:** AES-128-CCM
- **SMB 3.1.1:** AES-128-GCM (preferred) or AES-128-CCM

**Pre-authentication integrity** (SMB 3.1.1+):
- Uses AES-CMAC to protect the negotiation phase
- Prevents man-in-the-middle downgrade attacks
- Makes the NTLM relay more difficult by binding the session setup to the negotiation

## Named pipes

Named pipes provide inter-process communication (IPC) over SMB. In AD, they are the transport for MSRPC.

| Named pipe | RPC service | Purpose |
|------------|-------------|---------|
| `\PIPE\lsarpc` | LSARPC | Local Security Authority — policy queries, SID translation |
| `\PIPE\netlogon` | Netlogon | Domain authentication, pass-through authentication |
| `\PIPE\samr` | SAMR | Security Account Manager — user/group enumeration and management |
| `\PIPE\drsuapi` | DRS | Directory Replication Service — DC replication |
| `\PIPE\winreg` | Remote Registry | Remote registry access |
| `\PIPE\wkssvc` | Workstation service | Computer management |
| `\PIPE\browser` | Browser service | Computer browsing (legacy) |
| `\PIPE\srvsvc` | Server service | Share management |
| `\PIPE\protected_storage` | Protected Storage | DPAPI (legacy) |

Access to named pipes is controlled by the Security Descriptor on the pipe. By default, domain users can access `samr`, `lsarpc`, `netlogon`, and `srvsvc`, which enables LDAP-less enumeration.

## SMB shares important for AD

| Share | Path | Purpose |
|-------|------|---------|
| **ADMIN$** | `C:\Windows` | Remote administration — administrative share |
| **C$**, **D$**, etc. | Root of drive | Administrative drive shares |
| **IPC$** | N/A | Named pipe transport — not a filesystem share |
| **SYSVOL** | `%SystemRoot%\SYSVOL\sysvol\domain` | Domain Group Policy templates (GPT), logon scripts; **authenticated users can read by default** |
| **NETLOGON** | `%SystemRoot%\SYSVOL\sysvol\domain\SCRIPTS` | Logon scripts; domain-joined computers run scripts from here |
| **PRINT$** | `%SystemRoot%\system32\spool\drivers` | Printer driver repository |

### SYSVOL contents

```
\\corp.com\SYSVOL\corp.com\
├── Policies
│   ├── {GUID-1}
│   │   ├── GPT.INI
│   │   ├── Machine
│   │   │   ├── registry.pol
│   │   │   ├── Scripts
│   │   │   └── Microsoft\Windows\...
│   │   └── User
│   │       ├── registry.pol
│   │       └── Scripts
│   └── {GUID-2}...
├── Scripts (NETLOGON)
│   ├── logon.bat
│   └── startup.vbs
└── Domain_name
    └── ...
```

## SMB client/server flow

### Connection establishment

```
Client                                            Server
  │                                                  │
  │  1. TCP Connect (port 445)                       │
  │  ─────────────────────────────────────────────→  │
  │                                                  │
  │  2. NEGOTIATE PROTOCOL                           │
  │  ─────────────────────────────────────────────→  │
  │  • Supported dialect list                        │
  │  • Client capabilities                           │
  │                                                  │
  │  3. NEGOTIATE RESPONSE                           │
  │  ←───────────────────────────────────────────── │
  │  • Selected dialect (e.g., "3.1.1")              │
  │  • Server capabilities                           │
  │  • Security blob (Kerberos or NTLM)              │
  │                                                  │
  │  4. SESSION_SETUP                                │
  │  ─────────────────────────────────────────────→  │
  │  • Security blob (Auth token)                    │
  │  • Capabilities                                  │
  │                                                  │
  │  5. SESSION_SETUP RESPONSE                       │
  │  ←───────────────────────────────────────────── │
  │  • Session ID                                    │
  │  • Final auth result                             │
  │                                                  │
  │  6. TREE_CONNECT                                 │
  │  ─────────────────────────────────────────────→  │
  │  • Share path: \\server\share                    │
  │  • Desired access                                │
  │                                                  │
  │  7. TREE_CONNECT RESPONSE                        │
  │  ←───────────────────────────────────────────── │
  │  • Tree ID (TID)                                 │
  │  • Share capabilities                            │
  │                                                  │
  │  8. CREATE (file/directory open)                 │
  │  ─────────────────────────────────────────────→  │
  │  • File name                                     │
  │  • Desired access, sharing mode                  │
  │  • Create disposition                            │
  │                                                  │
  │  9. CREATE RESPONSE                              │
  │  ←───────────────────────────────────────────── │
  │  • File ID                                       │
  │  • Creation info                                 │
  │                                                  │
  │  10. READ/WRITE/IOCTL (data operations)          │
  │  ─────────────────────────────────────────────→  │
  │  • File ID + offset + length                     │
  │                                                  │
  │  11. CLOSE                                       │
  │  ─────────────────────────────────────────────→  │
  │                                                  │
```

## SMB vs CIFS

| Aspect | SMB | CIFS |
|--------|-----|------|
| Full name | Server Message Block | Common Internet File System |
| Protocol version | 1.0 through 3.1.1 | SMB 1.0 |
| Released | 1980s (IBM), 1990s (Microsoft) | 1996 (Microsoft) |
| RFC | Various MS protocols | RFC 1001, 1002 (NetBIOS); RFC 3017 (CIFS) |
| Performance | High (SMB2/3 optimized) | Low (chatty protocol) |
| Security | Signing, encryption, pre-auth integrity | Weak or no security |
| Modern use | Primary file-sharing protocol in Windows | **Should be disabled** |

## SMB protocol commands

### Negotiate commands

| Command | Code | Description |
|---------|------|-------------|
| NEGOTIATE_PROTOCOL | 0x00 | Protocol dialect negotiation |
| SESSION_SETUP | 0x01 | User authentication and session creation |
| LOGOFF | 0x02 | End a session |
| TREE_CONNECT | 0x03 | Connect to a share |
| TREE_DISCONNECT | 0x04 | Disconnect from a share |

### File operations

| Command | Code | Description |
|---------|------|-------------|
| CREATE | 0x05 | Create or open a file |
| CLOSE | 0x06 | Close a file |
| FLUSH | 0x07 | Flush file buffers |
| READ | 0x08 | Read from a file |
| WRITE | 0x09 | Write to a file |
| LOCK | 0x0A | Lock a byte range |
| IOCTL | 0x0B | Device I/O control |
| QUERY_DIRECTORY | 0x0C | List directory contents |
| CHANGE_NOTIFY | 0x0D | Monitor directory changes |
| QUERY_INFO | 0x0E | Query file/share attributes |
| SET_INFO | 0x0F | Set file/share attributes |

### SMB2/3 commands (simplified)

| Command | Code | Description |
|---------|------|-------------|
| SMB2 NEGOTIATE | 0x0000 | Protocol negotiation |
| SMB2 SESSION_SETUP | 0x0001 | Authentication |
| SMB2 LOGOFF | 0x0002 | End session |
| SMB2 TREE_CONNECT | 0x0003 | Connect to share |
| SMB2 TREE_DISCONNECT | 0x0004 | Disconnect from share |
| SMB2 CREATE | 0x0005 | Create/open file |
| SMB2 CLOSE | 0x0006 | Close file |
| SMB2 FLUSH | 0x0007 | Flush |
| SMB2 READ | 0x0008 | Read data |
| SMB2 WRITE | 0x0009 | Write data |
| SMB2 LOCK | 0x000A | Byte-range lock |
| SMB2 IOCTL | 0x000B | Device control (used for FSCTL) |
| SMB2 QUERY_DIRECTORY | 0x000C | Directory listing |
| SMB2 CHANGE_NOTIFY | 0x000D | Change monitoring |
| SMB2 QUERY_INFO | 0x000E | Get attributes |
| SMB2 SET_INFO | 0x000F | Set attributes |
| SMB2 OPLOCK_BREAK | 0x0012 | Oplock notification |
| SMB2 ECHO | 0x0013 | Keep-alive |

## How attackers abuse SMB

| Attack | Description |
|--------|-------------|
| **SMB relay** | Intercept SMB authentication and relay to another SMB server or DC. Prevented by SMB signing |
| **Pass-the-Hash** | Use NTLM hash to authenticate via SMB (SMB session setup with NTLMSSP) |
| **Anonymous NULL session** | Connect to IPC$ without credentials to enumerate users, shares, and RPC interfaces |
| **EternalBlue (MS17-010)** | Exploit SMBv1 buffer overflow vulnerability for remote code execution (RCE) |
| **SMBGhost (CVE-2020-0796)** | SMBv3.1.1 compression vulnerability leading to RCE |
| **SMB scanner** | Enumerate open SMB shares, check for signing, check for supported dialects |
| **SYSVOL enumeration** | Read GPO files from SYSVOL for cached passwords, scripts, configuration data |
| **lsass dump via SMB** | Trigger `lsass.exe` dump remotely via SMB (DCSync alternative) |
| **Named pipe abuse** | Access samr, lsarpc, netlogon named pipes for RPC enumeration |
| **SMB admin share (ADMIN$)** | Access `\\target\ADMIN$` for remote file operations and malware deployment |
| **SMB brute-force** | Attempt password guessing over SMB (despite lockout policies) |
| **SMB share browsing** | Enumerate accessible SMB shares for data exfiltration |
| **Shadow Copy access** | Access Volume Shadow Copies via SMB to read locked files (e.g., NTDS.dit) |

## Defender recommendations

1. **Disable SMBv1** — SMBv1 is the source of most critical SMB vulnerabilities.

   ```powershell
   # Disable SMBv1 on Windows 8/2012+
   Set-SmbServerConfiguration -EnableSMB1Protocol $false
   ```

2. **Enable SMB signing** — set both server and client to "always" via Group Policy.

3. **Enable SMB encryption** (Windows 2012+) for sensitive traffic.

   ```powershell
   Set-SmbServerConfiguration -EncryptData $true
   ```

4. **Block SMB at the firewall** — block inbound/outbound ports 139 and 445 at network boundaries.

5. **Restrict anonymous access** — prevent NULL sessions:

   - Set `Network access: Do not allow anonymous enumeration of SAM accounts` = Enabled
   - Set `Network access: Do not allow anonymous enumeration of SAM accounts and shares` = Enabled
   - Set `Network access: Restrict anonymous access to Named Pipes and Shares` = Enabled

6. **Audit SMB shares** — regularly scan for unintentionally open shares.

7. **Enable SMB auditing**:

   ```powershell
   Set-SmbServerConfiguration -AuditSmb1Access $true
   Set-SmbServerConfiguration -AuditServerDoesNotEncrypt $true
   ```

8. **Monitor SMB events**:
   - Event ID 5140: SMB share accessed
   - Event ID 5142: SMB share created
   - Event ID 5143: SMB share modified
   - Event ID 5145: SMB named pipe accessed

9. **Require Kerberos for SMB** — if possible, disable NTLM entirely to remove relay vectors.

10. **Use LAPS** — prevent local admin credential reuse over SMB.

11. **Limit SYSVOL permissions** — sensitive data should not be placed in Group Policy preferences (cPassword vulnerability).

12. **Keep systems patched** — especially for SMB-related CVEs.

## Relevant RFCs and MS protocols

| Document | Description |
|----------|-------------|
| [MS-SMB] | Server Message Block (SMB) Protocol |
| [MS-SMB2] | Server Message Block (SMB) Protocol Versions 2 and 3 |
| [MS-FSRM] | File Server Resource Manager Protocol |
| [MS-DFSC] | Distributed File System (DFS) Referral Protocol |
| [MS-DFSNM] | Distributed File System (DFS) Namespace Management Protocol |
| [MS-SRVS] | Server Service Remote Protocol |
| [MS-WKST] | Workstation Service Remote Protocol |
| RFC 1001 | Protocol Standard for NetBIOS Service on TCP/UDP |
| RFC 1002 | NetBIOS Working Group Detailed Specifications |
