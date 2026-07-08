# MSRPC Protocol

## What it is

Microsoft Remote Procedure Call (MSRPC) is Microsoft's implementation of the DCE/RPC (Distributed Computing Environment / Remote Procedure Call) standard. It is the primary inter-process communication mechanism in Windows, allowing processes on different machines to call functions as if they were local.

In AD, MSRPC is used by nearly every critical service:

- **LSARPC** — Local Security Authority (domain policy, SID translation)
- **Netlogon** — Domain authentication and secure channel
- **SAMR** — Security Account Manager (user/group management)
- **DRSUAPI** — Directory Replication Service (DC replication)
- **EPM** — Endpoint Mapper (locates RPC services)

## DCE/RPC and Microsoft extensions

### DCE/RPC basics

DCE/RPC defines:
- **Interface** — a set of related procedures, identified by a UUID (GUID)
- **Procedure** — a single function within an interface
- **Binding** — establishing a connection to a specific RPC service
- **Endpoints** — specific transport addresses where services listen
- **RPC transport** — how RPC messages are carried over the network (named pipes, TCP, etc.)

### Interface UUIDs

Each RPC interface is identified by a unique UUID (GUID):

| Interface UUID | Name | Purpose |
|---------------|------|---------|
| `12345778-1234-ABCD-EF00-0123456789AB` | LSARPC | LSA policy |
| `12345779-1234-ABCD-EF00-0123456789AB` | LSARPC (DS) | LSA directory services |
| `12345775-1234-ABCD-EF00-0123456789AB` | Netlogon | Netlogon secure channel |
| `12345776-1234-ABCD-EF00-0123456789AB` | SAMR | SAM management |
| `E3514235-4B06-11D1-AB04-00C04FC2DCD2` | DRSUAPI | Directory replication |
| `1FF70682-0A51-30E8-076D-740BE8CEE98B` | LSA Lookup | SID/name lookup (LSAP) |
| `6BFFD098-0213-11D2-A03F-00C04FC9B232` | LSA Lookup (DS) | Name/SID lookup (DS) |
| `F6BEFFF7-9ADA-48AC-8191-69D3CAE375F6` | BKDUP | Backup key (DPAPI) |
| `50ABC2A4-574D-40B3-9D66-EE4FD5FBA076` | DRSUAPI (DC cracking) | DC name cracking |

### RPC transport options

MSRPC can be transported over:

| Transport | Description | Default endpoint |
|-----------|-------------|-----------------|
| **SMB named pipes** | RPC over `\PIPE\<name>` via SMB | Port 445 |
| **TCP** | RPC over TCP directly | Port 135 (EPM) + dynamic ports |
| **HTTP** | RPC over HTTP (RPC over HTTP Proxy) | Port 80/443 |
| **LRPC** | Local RPC (same machine) | LPC port |
| **LLLRPC** | Local LPC (faster) | LPC port |

## RPC endpoint mapper (EPM)

The Endpoint Mapper (EPM) runs on **TCP/UDP port 135** on every Windows machine. It maps RPC interface UUIDs to the actual endpoints (TCP ports, named pipes) where the service is listening.

### EPM resolution flow

```
Client                                             Server
  │                                                  │
  │  1. Connect to EPM (port 135)                    │
  │  ─────────────────────────────────────────────→  │
  │                                                  │
  │  2. ept_map: "Where is interface                │
  │     {12345778-...}?"                             │
  │  ─────────────────────────────────────────────→  │
  │                                                  │
  │  3. EPM responds:                                │
  │     "Interface is at \\PIPE\lsarpc"              │
  │     (or TCP port 49664, etc.)                    │
  │  ←───────────────────────────────────────────── │
  │                                                  │
  │  4. Client connects to endpoint                  │
  │  ─────────────────────────────────────────────→  │
  │                                                  │
  │  5. RPC bind + operations                        │
  │  ─────────────────────────────────────────────→  │
  │                                                  │
```

### EPM protocols

- **Remote:** RPC over TCP/UDP port 135
- **Local:** LRPC via `\PIPE\epmapper` or LPC port

## LSARPC (Local Security Authority)

### Purpose

LSARPC manages:
- Domain policy (password policy, Kerberos policy)
- SID translation (SID ↔ name)
- Trust relationships
- Audit policy
- Privilege assignment

### Interface UUID: `12345778-1234-ABCD-EF00-0123456789AB`

### Common operations

| Operation | Description | Attack relevance |
|-----------|-------------|------------------|
| `LsarOpenPolicy` | Open a handle to the LSA policy object | Required before other operations |
| `LsarQueryInformationPolicy` | Query domain policy settings | Enumerate password policy, lockout policy |
| `LsarQueryDomainInformationPolicy` | Domain-specific policy info | Enumerate domain SID |
| `LsarEnumerateTrustedDomains` | List trusted domains | Enumerate trust relationships |
| `LsarLookupSids` | SID → Name translation | Identify user/group accounts |
| `LsarLookupNames` | Name → SID translation | Resolve account names to SIDs |
| `LsarQuerySecurityObject` | Query security descriptor on LSA objects | Check permissions |
| `LsarAddPrivilegesToAccount` | Add privileges to an account | Privilege escalation (requires high privileges) |
| `LsarSetInformationPolicy` | Set policy values | Modify domain policy (requires high privileges) |

### Transport

- **Named pipe:** `\PIPE\lsarpc`
- **TCP endpoint:** Dynamic (obtained from EPM)

## Netlogon

### Purpose

Netlogon (NRPC) handles:
- Domain computer secure channel (machine account authentication)
- Pass-through authentication (NTLM)
- DC locator
- Trust relationship verification
- Kerberos KDC-Proxy

### Interface UUID: `12345775-1234-ABCD-EF00-0123456789AB`

### Common operations

| Operation | Description | Attack relevance |
|-----------|-------------|------------------|
| `NetrServerReqChallenge` | Request a session challenge | First step of Netlogon session setup |
| `NetrServerAuthenticate3` | Authenticate the secure channel | Core authentication |
| `NetrLogonGetSessionInfo` | Get logon session info | Recon (low-priv) |
| `NetrLogonSamLogonWithFlags` | Perform pass-through auth (NTLM) | NTLM authentication path |
| `NetrLogonGetDomainInfo` | Query domain info | Domain information gathering |
| `NetrEnumerateTrustedDomains` | List trusted domains | Trust enumeration |
| `NetrGetDcName` | Get DC name for a domain | Recon |

### Zerologon (CVE-2020-1472)

**The most critical Netlogon vulnerability.** An attacker could:

1. Establish a Netlogon secure channel to a DC
2. Set the AES key to all zeros via `NetrServerAuthenticate3` with a zero-computed session key
3. Change the DC's computer account password in AD to an empty string
4. Use the empty password to DCSync as the DC

**Fixed:** August 2020 security update. Required changes:
- DCs reject AES-zero session keys
- DCs enforce `RequireStrongerSessionKey` for all Netlogon connections
- Account-level `FullSecureChannelProtection` flag can be set

### Transport

- **Named pipe:** `\PIPE\netlogon`
- **TCP endpoint:** Dynamic (obtained from EPM)

## SAMR (Security Account Manager)

### Purpose

SAMR provides access to the Security Account Manager database:
- Enumerate users, groups, domains
- Query user/group information
- Manage account attributes

### Interface UUID: `12345776-1234-ABCD-EF00-0123456789AB`

### Common operations

| Operation | Description | Attack relevance |
|-----------|-------------|------------------|
| `SamrConnect` | Connect to the SAM | Required to start |
| `SamrEnumerateDomains` | List domains in SAM | Recon (domain info) |
| `SamrOpenDomain` | Open a domain handle | Required for domain operations |
| `SamrEnumerateUsersInDomain` | **List all users** | **Primary user enumeration** |
| `SamrEnumerateGroupsInDomain` | List all groups | Group enumeration |
| `SamrQueryInformationUser` | Query user attributes | User info (account status, etc.) |
| `SamrLookupNamesInDomain` | Resolve names to RIDs | Recon |
| `SamrLookupIdsInDomain` | Resolve RIDs to names | Recon |
| `SamrGetAliasMembership` | Get group membership for an alias | Membership enumeration |
| `SamrQueryInformationDomain` | Domain info | Password policy, lockout info |
| `SamrSetInformationUser` | Modify user attributes | Account manipulation (requires priv) |

### SAMR enumeration in practice

SAMR enumeration is the **most common AD reconnaissance technique**. Any authenticated user can enumerate:

- All usernames (sAMAccountName, RID, user flags)
- All group names
- Domain RID ranges
- Domain password policy

```powershell
# Via PowerShell (ADSI or .NET)
$samr = [ADSI]"WinNT://$env:USERDOMAIN"
$samr.Children | Where-Object {$_.SchemaClassName -eq 'User'} | ForEach-Object {
    $_.Name
}
```

```bash
# Using rpcclient (Linux)
rpcclient -U "CORP\\jsmith" 10.10.10.10
  > enumdomusers
  > enumalsgroups builtin
  > querydispinfo
  > lookupnames Administrator
```

### Why SAMR is dangerous

- **No special privileges required** — any domain user can enumerate everything
- **No LDAP query required** — works even if LDAP is blocked/disabled
- **No audit logging by default** — SAMR operations are not logged in security audit log (only in SAM event log)
- **Cannot be blocked easily** — disabling SAMR breaks many management tools

### Transport

- **Named pipe:** `\PIPE\samr`
- **TCP endpoint:** Dynamic (obtained from EPM)

## DRSUAPI (Directory Replication Service)

### Purpose

DRSUAPI handles Active Directory replication between domain controllers.

### Interface UUID: `E3514235-4B06-11D1-AB04-00C04FC2DCD2`

### Common operations

| Operation | Description | Attack relevance |
|-----------|-------------|------------------|
| `DRSBind` | Bind to the DRS service | Required for DRS operations |
| `DRSGetNCChanges` | **Request replication changes** | **DCSync — extract password hashes** |
| `DRSCrackNames` | Name/SID lookup | Recon (SID/name resolution) |
| `DRSDomainControllerInfo` | DC info | Recon |
| `DRSReplicaAdd` | Add a replication partner | DCShadow (register rogue DC) |
| `DRSReplicaDel` | Remove a replication partner | Disrupt replication |
| `DRSReplicaModify` | Modify replication settings | Replication manipulation |
| `DRSGetReplicationInfo` | Get replication status | Recon |

### DCSync — The most dangerous DRSUAPI attack

DCSync uses `DRSGetNCChanges` to replicate directory data (including password hashes) from a DC.

**What an attacker needs:**
- Any of these privileges:
  - `Replicating Directory Changes` (`DS-Replication-Get-Changes`)
  - `Replicating Directory Changes All` (`DS-Replication-Get-Changes-All`)
  - `Replicating Directory Changes In Filtered Set` (`DS-Replication-Get-Changes`)

Domain Admins, Enterprise Admins, and Domain Controllers have these rights by default. Attackers with any of these privileges can extract:

- All user NTLM hashes
- All Kerberos keys (AES128, AES256, RC4)
- All supplemental credentials
- The KRBTGT hash
- Trust passwords

```bash
# Using impacket
impacket-secretsdump -just-dc CORP/jsith:password@DC01.corp.com

# Or for specific user
impacket-secretsdump -just-dc-user krbtgt CORP/jsith:password@DC01.corp.com
```

### Transport

- **Named pipe:** `\PIPE\drsuapi`
- **TCP endpoint:** Dynamic (obtained from EPM)

## RPC binding explained

RPC binding is the process of establishing a connection to a specific RPC interface on a remote machine.

### Binding string format

```
[object_uuid,transfer_syntax]@[transport]:[endpoint],[authtype]
```

For example:
```
ncalrpc:[samr]                              # Local RPC
ncacn_ip_tcp:10.10.10.10[49664]             # TCP
ncacn_np:10.10.10.10[\PIPE\samr]            # Named pipe
ncacn_http:10.10.10.10[6001]                # HTTP (RPC over HTTP)
```

### Authentication

RPC supports several authentication levels:

| Level | Value | Description |
|-------|-------|-------------|
| RPC_C_AUTHN_LEVEL_NONE | 1 | No authentication |
| RPC_C_AUTHN_LEVEL_CONNECT | 2 | Authenticate at connect |
| RPC_C_AUTHN_LEVEL_CALL | 3 | Authenticate each call |
| RPC_C_AUTHN_LEVEL_PKT | 4 | Authenticate each packet |
| RPC_C_AUTHN_LEVEL_PKT_INTEGRITY | 5 | Packet integrity (signing) |
| RPC_C_AUTHN_LEVEL_PKT_PRIVACY | 6 | Packet privacy (encryption) |

## Commonly abused RPC operations summary

| Operation | Interface | Required rights | Abuse |
|-----------|-----------|-----------------|-------|
| `SamrEnumerateUsersInDomain` | SAMR | Authenticated user | User enumeration |
| `SamrQueryInformationUser` | SAMR | Authenticated user | User details |
| `SamrEnumerateDomains` | SAMR | Authenticated user | Domain info |
| `LsarQueryInformationPolicy` | LSARPC | Authenticated user | Password policy |
| `LsarEnumerateTrustedDomains` | LSARPC | Authenticated user | Trust enumeration |
| `LsarLookupNames` | LSARPC | Authenticated user | SID resolution |
| `NetrServerReqChallenge` | Netlogon | Authenticated user | Session setup (pre-auth) |
| `NetrServerAuthenticate3` | Netlogon | Machine account | Secure channel |
| `NetrLogonSamLogonWithFlags` | Netlogon | Machine account | NTLM pass-through |
| `DRSBind` | DRSUAPI | Authenticated user | Replication bind |
| `DRSGetNCChanges` | DRSUAPI | Replication rights | **DCSync** |
| `DRSCrackNames` | DRSUAPI | Authenticated user | Name/SID resolution |
| `DRSReplicaAdd` | DRSUAPI | Domain Admin | **DCShadow** |

## How attackers abuse MSRPC

| Attack | Target | Description |
|--------|--------|-------------|
| **SAMR enumeration** | SAMR | Anonymous or low-privileged enumeration of all domain users, groups, and RIDs |
| **DCSync** | DRSUAPI | Replicate password hashes from DC (DA, EA, or replication rights required) |
| **DCShadow** | DRSUAPI | Register a rogue DC and push malicious objects (DA required) |
| **Zerologon (CVE-2020-1472)** | Netlogon | Exploit cryptographic weakness in Netlogon session to take over DC |
| **PrivExchange** | EWS → Netlogon | Exchange server push subscription → trigger NTLM auth relay to DC |
| **Shadow Credentials** | DRSUAPI | Add key credential to user/computer to enable PKINIT-based impersonation |
| **LSARPC trust enumeration** | LSARPC | Enumerate domain trusts to plan lateral movement |
| **RPC endpoint scanning** | EPM | Discover RPC services and available interfaces |
| **RPC over SMB relay** | Named pipes | Relay authenticated RPC connections to different targets |
| **RPC brute-force** | SAMR | Brute-force user existence (enumeration) |

## Defender recommendations

1. **Restrict SAMR access** — Block anonymous SAMR access:
   - `Network access: Restrict anonymous access to Named Pipes and Shares` = **Enabled**
   - `Network access: Do not allow anonymous enumeration of SAM accounts` = **Enabled**
   - These do **not** stop authenticated users from using SAMR

2. **Monitor RPC events:**
   - Event ID 5145: Named pipe access (check for `\PIPE\samr`, `\PIPE\lsarpc`, `\PIPE\drsuapi`)
   - Event ID 4662: AD object access (check for `DRSGetNCChanges` — `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2`)
   - Event ID 4672: Special privileges assigned
   - Event ID 4688: Process creation (rpcping, rpcdump.exe, etc.)

3. **Enable SAMR audit logging** — Windows 10/2016+ includes SAMR auditing:
   ```powershell
   auditpol /set /subcategory:"SAM" /success:enable /failure:enable
   ```

4. **Use Windows Defender Firewall** — block RPC ports (135 TCP/UDP + dynamic ports) from untrusted networks.

5. **Patch promptly** — Netlogon vulnerabilities (Zerologon, etc.) are critical and routinely exploited.

6. **Limit who has replication rights** — audit `DS-Replication-Get-Changes-All` and `DS-Replication-Get-Changes` regularly.

7. **Disable SAMR if possible** — not easily done without breaking functionality, but monitoring is essential.

8. **RPC hardening:**
   - `HKLM\Software\Microsoft\Rpc\RestrictRemoteClients` = 1 (Windows 2008+)
   - `HKLM\Software\Policies\Microsoft\Windows NT\Rpc\EnableAuthEpResolution` = 1

9. **Use Just Enough Administration (JEA)** — restrict who can manage DCs and domain objects.

## Relevant MS protocols

| Document | Description |
|----------|-------------|
| [MS-RPCE] | Remote Procedure Call Protocol Extensions |
| [MS-SAMR] | Security Account Manager (SAM) Remote Protocol |
| [MS-LSAD] | Local Security Authority (Domain Policy) Remote Protocol |
| [MS-NRPC] | Netlogon Remote Protocol |
| [MS-DRSR] | Directory Replication Service (DRS) Remote Protocol |
| [MS-ERREF] | Windows Error Reporting Protocol (contains NTSTATUS codes) |
| [C706] | DCE/RPC Specification (Open Group) |
