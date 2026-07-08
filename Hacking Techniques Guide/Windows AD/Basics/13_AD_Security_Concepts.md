# Active Directory Security Concepts

## What it is

This file covers the fundamental security constructs in Active Directory — SIDs, ACLs, security descriptors, privileged account protection mechanisms, and modern security features. These concepts underpin every authorization decision in Windows.

## Security Principals

A security principal is any entity that can be authenticated by Windows and granted access to resources.

### Types

| Principal type | Description | Examples |
|----------------|-------------|----------|
| **User** | Human user or service account | `CORP\jsmith`, `CORP\sqlsvc` |
| **Group** | Collection of users/computers | `CORP\Domain Admins`, `CORP\Sales` |
| **Computer** | Domain-joined machine | `CORP\WS001$` |
| **Service** | gMSA (Group Managed Service Account) | `CORP\gmsa_sql$` |
| **Well-known** | Built-in principals | `Everyone`, `Authenticated Users`, `SYSTEM` |

### Well-known security principals

| SID | Name | Description |
|-----|------|-------------|
| `S-1-1-0` | Everyone | All users and anonymous |
| `S-1-5-7` | Anonymous Logon | Unauthenticated users |
| `S-1-5-11` | Authenticated Users | All authenticated users and computers |
| `S-1-5-18` | SYSTEM | Local system account |
| `S-1-5-19` | NT Authority\LocalService | Local service account |
| `S-1-5-20` | NT Authority\NetworkService | Network service account |
| `S-1-5-32-544` | BUILTIN\Administrators | Local administrators |
| `S-1-5-32-545` | BUILTIN\Users | Local users |
| `S-1-5-32-546` | BUILTIN\Guests | Guest users |
| `S-1-5-32-547` | BUILTIN\Power Users | Power users (legacy) |
| `S-1-5-32-548` | BUILTIN\Account Operators | Account operators |
| `S-1-5-32-549` | BUILTIN\Server Operators | Server operators |
| `S-1-5-32-550` | BUILTIN\Print Operators | Print operators |
| `S-1-5-32-551` | BUILTIN\Backup Operators | Backup operators |
| `S-1-5-32-552` | BUILTIN\Replicator | Replicator |
| `S-1-5-domain-500` | Administrator | Built-in domain admin |
| `S-1-5-domain-501` | Guest | Built-in guest account |
| `S-1-5-domain-502` | krbtgt | Key Distribution Center account |
| `S-1-5-domain-512` | Domain Admins | Domain administrator group |
| `S-1-5-domain-513` | Domain Users | All domain users |
| `S-1-5-domain-514` | Domain Guests | Domain guest accounts |
| `S-1-5-domain-515` | Domain Computers | All domain computers |
| `S-1-5-domain-516` | Domain Controllers | Domain controllers group |
| `S-1-5-domain-517` | Cert Publishers | Certificate publishers |
| `S-1-5-domain-518` | Schema Admins | Schema administrators |
| `S-1-5-domain-519` | Enterprise Admins | Enterprise administrators |
| `S-1-5-domain-520` | Group Policy Creator Owners | Group Policy creators |

## SIDs (Security Identifiers)

A SID is a variable-length structure used to uniquely identify a security principal or security group.

### SID structure

```
S-R-I-S-S...  (text format)

Example: S-1-5-21-3623811015-3361044348-30300820-500

S  - SID marker
1  - Revision level
5  - Identifier Authority (NT Authority = 5)
21 - Subauthority count (3 means domain-level SID)
3623811015 - Subauthority 1 (domain component)
3361044348 - Subauthority 2 (domain component)
30300820   - Subauthority 3 (domain component)
500        - RID (Relative ID — Administrator)
```

### SID components

- **Identifier Authority** — identifies the issuing authority (SECURITY_NT_AUTHORITY = 5)
- **Subauthorities** — identify the domain and the specific account
- **Relative ID (RID)** — the last subauthority, unique within the domain

### Well-known SIDs vs domain SIDs

- **Well-known SIDs** — defined by Microsoft, same on all systems (e.g., `S-1-1-0` = Everyone)
- **Domain SIDs** — domain-specific, prefixed with the domain's SID (e.g., `S-1-5-21-<domain>-500`)

## RIDs (Relative IDs)

RIDs are the last subauthority in a SID, identifying the specific account within a domain.

### Well-known RIDs

| RID | Account |
|-----|---------|
| 500 | Administrator |
| 501 | Guest |
| 502 | krbtgt |
| 512 | Domain Admins group |
| 513 | Domain Users group |
| 514 | Domain Guests group |
| 515 | Domain Computers group |
| 516 | Domain Controllers group |
| 517 | Cert Publishers |
| 518 | Schema Admins |
| 519 | Enterprise Admins |

### RID cycle

Each DC in a domain gets a pool of RIDs from the RID Master (FSMO role). When a new security principal is created, it gets the next available RID from the pool.

**Attack angle:** RID Hijacking — modifying the RID of a user to match another user (e.g., changing a low-privileged user's RID to 500). This is detected by SID filtering in trust relationships.

## ACEs vs ACLs

### ACL (Access Control List)

A list of Access Control Entries (ACEs) attached to a securable object (file, registry key, AD object, etc.).

There are two types:

#### DACL (Discretionary Access Control List)

Controls access — who can do what to the object.

```
DACL Structure:
  Header:
    - AclRevision (2 = Windows 2000+, 4 = Windows 2003+)
    - Sbz1 (padding)
    - AclSize (total size)
    - AceCount (number of ACEs)
    - Sbz2 (padding)

  ACE 1: Allow John Smith - Read, Write (0x0002009F)
  ACE 2: Allow Domain Admins - Full Control (0x000F01FF)
  ACE 3: Deny Everyone - Read (0x0002009F)
  ...
```

#### SACL (System Access Control List)

Controls auditing — which operations should be logged.

```
SACL Structure:
  (same format as DACL but used for auditing)

  ACE 1: Audit Success - Domain Admins - Write (0x00000002)
  ACE 2: Audit Failure - Everyone - Read (0x00000001)
```

### ACE (Access Control Entry)

Each ACE contains:

| Field | Description |
|-------|-------------|
| **Type** | Access Denied (0x00), Access Allowed (0x01), System Audit (0x02) |
| **Flags** | Object-specific flags (container inheritance, etc.) |
| **Size** | Size of the ACE |
| **Access Mask** | Bitmask of granted/denied permissions |
| **SID** | Security Identifier of the trustee |

### ACE types

| ACE Type | Value | Applies to |
|----------|-------|------------|
| ACCESS_ALLOWED_ACE_TYPE | 0x00 | DACL — allow access |
| ACCESS_DENIED_ACE_TYPE | 0x01 | DACL — deny access |
| SYSTEM_AUDIT_ACE_TYPE | 0x02 | SACL — audit success/failure |
| ACCESS_ALLOWED_OBJECT_ACE_TYPE | 0x05 | DACL — object-specific allow (AD) |
| ACCESS_DENIED_OBJECT_ACE_TYPE | 0x06 | DACL — object-specific deny (AD) |
| SYSTEM_AUDIT_OBJECT_ACE_TYPE | 0x07 | SACL — object-specific audit (AD) |

### ACE order in DACL

Windows processes ACEs in a specific order:

1. **Explicit Deny ACEs** — first
2. **Explicit Allow ACEs** — second
3. **Inherited Deny ACEs** — third
4. **Inherited Allow ACEs** — fourth

**Important:** Deny ACEs always come before Allow ACEs. If a user matches both a Deny and Allow ACE, the Deny wins.

### Common AD permissions (access mask)

| Permission | Value | Description |
|------------|-------|-------------|
| Generic Read | 0x80000000 | Read access |
| Generic Write | 0x40000000 | Write access |
| Generic Execute | 0x20000000 | Execute access |
| Generic All | 0x10000000 | Full control |
| Full Control | 0x000F01FF | All standard rights |
| Read | 0x0002009F | List contents, read all properties |
| Write | 0x000200BC | Write properties |
| Create Child | 0x00000001 | Create child objects |
| Delete Child | 0x00000002 | Delete child objects |
| Delete | 0x00010000 | Delete the object |
| Write Owner | 0x00080000 | Take ownership |
| Write DAC | 0x00040000 | Modify permissions |
| Read Control | 0x00020000 | Read security descriptor |
| List Contents | 0x00000004 | List immediate children |
| List Object | 0x00000080 | List the object |

### Common AD extended rights

| Right | GUID | Description |
|-------|------|-------------|
| User-Force-Change-Password | `00299570-246d-11d0-a768-00aa006e0529` | Force password change |
| User-Change-Password | `ab721a53-1e2f-11d0-9819-00aa0040529b` | Change own password |
| Send-As | `ab721a54-1e2f-11d0-9819-00aa0040529b` | Send as mailbox |
| Receive-As | `ab721a55-1e2f-11d0-9819-00aa0040529b` | Receive as mailbox |
| DS-Replication-Get-Changes | `1131f6aa-9c07-11d1-f79f-00c04fc2dcd2` | Replicate directory changes |
| DS-Replication-Get-Changes-All | `1131f6ad-9c07-11d1-f79f-00c04fc2dcd2` | Replicate all changes (**DCSync**) |
| DS-Replication-Get-Changes-In-Filtered-Set | `89e95b76-444d-4c62-991a-0facbeda640c` | Replicate filtered changes |
| DS-Install-Replica | `9923a32a-3607-11d2-b9be-0000f87a36b2` | Add DC to domain |

### AD permission inheritance

Inherited ACEs are propagated from parent containers to child objects.

**Inheritance flags:**

| Flag | Value | Meaning |
|------|-------|---------|
| CONTAINER_INHERIT_ACE | 0x02 | ACE propagates to child containers |
| OBJECT_INHERIT_ACE | 0x01 | ACE propagates to child objects |
| INHERIT_ONLY_ACE | 0x08 | ACE only effective on children, not this object |
| NO_PROPAGATE_INHERIT_ACE | 0x04 | ACE propagates one level only |
| INHERITED_ACE | 0x10 | ACE was inherited, not explicit |

## Security Descriptors

A security descriptor contains all the security information for a securable object.

### Security descriptor structure

```
+------------------------------------------+
| Security Descriptor (SECURITY_DESCRIPTOR) |
|                                           |
|  Revision (1 byte)                        |
|  Sbz1 (1 byte)                            |
|  Control flags (2 bytes)                  |
|    - SE_OWNER_DEFAULTED                   |
|    - SE_GROUP_DEFAULTED                   |
|    - SE_DACL_PRESENT                      |
|    - SE_DACL_DEFAULTED                    |
|    - SE_SACL_PRESENT                      |
|    - SE_SELF_RELATIVE                     |
|    - SE_SACL_AUTO_INHERIT_REQ             |
|    - SE_DACL_AUTO_INHERIT_REQ             |
|  Owner SID (pointer or inline)            |
|  Group SID (pointer or inline)            |
|  DACL (pointer to ACL)                    |
|  SACL (pointer to ACL)                    |
+------------------------------------------+
```

### Self-relative vs absolute format

- **Self-relative** — security descriptor stored in contiguous memory with SIDs and ACLs inline; used for on-disk/on-wire storage
- **Absolute** — uses pointers; used for in-memory manipulation

## SDDL (Security Descriptor Definition Language)

SDDL is a string representation of security descriptors used in many Windows components.

### SDDL format

```
O:<owner>SID>G:<groupSID>D:<dacl_flags>(<ace>...)(<ace>...)
S:<sacl_flags>(<ace>...)(<ace>...)
```

### SDDL example

```
D:(A;;FA;;;BA)(A;;FA;;;SY)(A;;0x1200a9;;;BU)
```

Breakdown:

```
O:BA                       - Owner: Built-in Administrators
G:BU                       - Primary Group: Built-in Users
D:(ACE1)(ACE2)(ACE3)       - DACL with 3 ACEs

A;;FA;;;BA                 - Allow, 0x1F01FF (Full Control), to BA (Built-in Administrators)
A;;FA;;;SY                 - Allow, Full Control, to SY (SYSTEM)
A;;0x1200a9;;;BU           - Allow, Read + Execute to BU (Built-in Users)
```

### Common SDDL SID aliases

| Alias | SID | Description |
|-------|-----|-------------|
| AN | S-1-5-7 | Anonymous |
| AU | S-1-5-11 | Authenticated Users |
| BA | S-1-5-32-544 | Built-in Administrators |
| BG | S-1-5-32-546 | Built-in Guests |
| BU | S-1-5-32-545 | Built-in Users |
| DA | S-1-5-domain-512 | Domain Admins |
| DC | S-1-5-domain-515 | Domain Computers |
| DD | S-1-5-domain-514 | Domain Guests |
| DU | S-1-5-domain-513 | Domain Users |
| EA | S-1-5-domain-519 | Enterprise Admins |
| PA | S-1-5-domain-518 | Schema Admins |
| PO | S-1-5-32-550 | Print Operators |
| SO | S-1-5-32-549 | Server Operators |
| SY | S-1-5-18 | SYSTEM |

### SDDL ACE flags

```
A: Access Allowed
D: Access Denied
AU: System Audit
```

### SDDL permissions (common)

| Code | Meaning |
|------|---------|
| FA | Generic All (Full Control) |
| FR | Generic Read |
| FW | Generic Write |
| FX | Generic Execute |
| GA | Generic All |
| GR | Generic Read |
| GW | Generic Write |
| GX | Generic Execute |
| CC | Create Child |
| DC | Delete Child |
| LC | List Contents |
| RP | Read Property |
| WP | Write Property |
| CA | Control Access |
| LO | List Object |

## Delegation of Control

Delegation allows granting specific administrative rights to non-administrators without making them Domain Admins.

### Delegation wizard

Active Directory Users and Computers has a "Delegation of Control Wizard" that sets specific ACEs on OUs.

### Common delegations

| Task | Permissions required |
|------|---------------------|
| Reset user passwords | `User-Force-Change-Password` extended right on user objects |
| Create/delete users | `Create Child`, `Delete Child` on OU; object-specific for user class |
| Modify group membership | `Write Property` on `member` attribute |
| Join computer to domain | Pre-created computer accounts in AD |
| Manage DNS records | Write access to DNS objects |
| Manage GPOs | RW access to GPO objects and SYSVOL files |
| Manage printers | Write access to printer objects |

### Danger: Over-permissive delegation

Attackers look for:
- `GenericAll` / `GenericWrite` on user objects (can change passwords)
- `WriteProperty` on `member` attribute of privilege groups
- `WriteOwner` or `WriteDACL` on any object
- `ForceChangePassword` on admin accounts
- `DS-Replication-Get-Changes-All` on the domain

## AdminCount / AdminSDHolder / SDProp

### AdminCount

The `adminCount` attribute is set to `1` on any user or group that is a member of a **protected group**.

**Protected groups:**
- Administrators (BUILTIN)
- Domain Admins
- Enterprise Admins
- Schema Admins
- Account Operators
- Backup Operators
- Server Operators
- Print Operators
- Domain Controllers
- Read-Only Domain Controllers
- Group Policy Creator Owners
- Cryptographic Operators
- (and more, depending on domain functional level)

When `adminCount = 1`, the object is protected by **AdminSDHolder**.

### AdminSDHolder (AdminSDHolder container)

The AdminSDHolder container is stored in AD:

```
CN=AdminSDHolder,CN=System,DC=corp,DC=example,DC=com
```

It contains a **security descriptor** (template) that defines the desired permissions for all protected objects.

### SDProp (Security Descriptor Propagation)

SDProp is a process on the PDC Emulator that runs every **60 minutes** (by default). It:

1. Scans AD for all users/groups with `adminCount = 1`
2. Compares their ACLs to the AdminSDHolder ACL
3. **Resets** any ACLs that differ from the AdminSDHolder template

This means:
- If you add a non-admin user to Domain Admins, SDProp resets the user's ACL after 60 minutes
- Automated tools often rely on `adminCount` to identify privileged accounts
- Protected group members cannot have their ACLs modified (SDProp reverts changes)

```powershell
# Find all protected accounts
Get-ADUser -Filter {adminCount -eq 1} -Properties adminCount | Select Name, SamAccountName

# Find all protected groups
Get-ADGroup -Filter {adminCount -eq 1} -Properties adminCount | Select Name, SamAccountName

# View AdminSDHolder ACL
Get-Acl -Path "AD:\CN=AdminSDHolder,CN=System,DC=corp,DC=com" | Format-List
```

### Attack angle: AdminSDHolder modification

If an attacker has `Write` access to the AdminSDHolder container, they can **modify its security descriptor**. On the next SDProp run (within 60 minutes), all protected objects will inherit the new ACL.

**Attack:**
1. Grant `GenericAll` on AdminSDHolder to `CORP\jsmith`
2. SDProp propagates the change to all protected accounts
3. `jsmith` now has `GenericAll` on every Domain Admin account

### Offensive use of AdminCount

```powershell
# Find high-value targets (adminCount=1)
Get-ADUser -Filter {adminCount -eq 1} -Properties adminCount, memberOf | Select Name, memberOf
```

## Protected Users group

The Protected Users group (Windows 2012 R2+) provides **stronger protection** for high-value accounts.

### Protection limitations applied

| Limitation | Description |
|------------|-------------|
| No NTLM authentication | Kerberos only |
| No DES/RC4 encryption | AES only |
| No credential delegation | Cannot be delegated |
| No S4U2Self/S4U2Proxy | Cannot be used for service tickets |
| No NTLM pass-through | No NTLM fallback |
| No WDigest | Digest authentication blocked |
| No credential caching | No MS Cache (DCC2) for offline logon |
| Longer Kerberos lifetimes | Uses a shorter TGT lifetime (15 min for services, matching user) |

### Protection mechanisms

```
┌─────────────────────────────────────────────┐
│ Protected User (jsmith)                      │
│                                              │
│  Benefits:                                   │
│  ✓ AES-only Kerberos                          │
│  ✓ No NTLM                                   │
│  ✓ No delegation                              │
│  ✓ No credential caching                      │
│  ✓ No WDigest                                │
│                                              │
│  Cannot use:                                 │
│  ✗ NTLM authentication                       │
│  ✗ RC4/DES encryption                        │
│  ✗ Credential delegation                     │
│  ✗ Offline logon (cached creds)              │
└─────────────────────────────────────────────┘
```

### Using Protected Users

```powershell
# Add user to Protected Users group
Add-ADGroupMember -Identity "Protected Users" -Members "jsmith"

# Verify
Get-ADGroupMember -Identity "Protected Users"
```

**Note:** Test thoroughly before adding — many authentication scenarios may break because Protected Users cannot use NTLM, which is needed for many legacy applications.

## Authentication Policies and Authentication Silos

Windows Server 2012 R2+ introduces Authentication Policies and Silos for fine-grained access control.

### Authentication Policies

Restrict authentication behavior for specific accounts:

- **TGTLifetime** — maximum TGT lifetime for the policy
- **CompatibilityMode** — whether to enforce or audit
- **What can authenticate to the account:**
  - `None`, `User`, `Service`, `Computer`, `Any`

### Authentication Silos

Group accounts into a silo and enforce:
- Which accounts can authenticate
- Which services the silo accounts can access
- Kerberos ticket lifetime within the silo

### Example: service account isolation

```powershell
# Create an authentication policy for service accounts
New-ADAuthenticationPolicy -Name "ServiceAcctPolicy" `
    -UserTGTLifetimeMins 60 `
    -Description "Limit TGT lifetime for service accounts"

# Create a silo
New-ADAuthenticationPolicySilo -Name "SvcSilo" `
    -Description "Service account isolation" `
    -UserAuthenticationPolicy "ServiceAcctPolicy"
```

## Credential Guard

### What it is

Windows Defender Credential Guard (Windows 10/2016+) uses **virtualization-based security (VBS)** to isolate secrets from the running operating system.

### How it works

```
┌──────────────────────────────────────────────┐
│ Normal Operating System                       │
│                                               │
│  Processes (LSASS, browser, etc.)             │
│  │                                            │
│  │ Cannot directly access                     │
│  │ protected secrets                          │
│  │                                            │
├──────────────────────────────────────────────┤
│ Virtualization-Based Security (VBS)           │
│  ┌────────────────────────────────────────┐  │
│  │ Isolated User Mode (IUM) / VBS         │  │
│  │                                         │  │
│  │ LSA Isolated (Lsalso.exe)               │  │
│  │   - Kerberos keys                       │  │
│  │   - NTLM hashes (not stored)            │  │
│  │   - DPAPI keys (via isolated process)   │  │
│  │                                         │  │
│  │ Communication: Channel via Hyper-V      │  │
│  │ hypervisor                              │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

### What Credential Guard protects

| Credential type | Protected? | Notes |
|----------------|------------|-------|
| Kerberos TGT | Yes | Stored in LSA Isolated |
| NTLM hash | No | Not stored when Credential Guard is enabled |
| DPAPI master keys | Yes | Via isolated DPAPI |
| Service account creds | Yes | Through LSA Isolated |
| Plaintext passwords | No | Not stored by LSASS |
| WDigest creds | No | Should be disabled anyway |

### Limitations

- Only available on Windows 10/2016+ with UEFI, Secure Boot, VT-x/AMD-V, SLAT
- Does not protect against:
  - Attacks from SYSTEM (most tools run as SYSTEM)
  - Attacks before logon
  - Network-based attacks (relay, Kerberoasting)
- Breaks some features:
  - NTLM pass-through authentication
  - Kerberos unconstrained delegation
  - Credential Manager

## LSA Protection

LSA Protection (RunAsPPL) prevents non-Microsoft processes from accessing LSASS.

### How it works

When LSA Protection is enabled:

1. LSASS runs as a **Protected Process Light (PPL)**
2. Only Microsoft-signed processes can open LSASS
3. Tools like mimikatz cannot access LSASS via `OpenProcess`
4. Debugging LSASS is blocked without kernel debugging

### Enable LSA Protection

```powershell
# Registry path
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\Lsa" `
    -Name "RunAsPPL" -Value 1

# Or via Group Policy:
# Computer Configuration > Administrative Templates > System >
#   Local Security Authority > Configure LSASS to run as protected process
```

### Bypasses

- Kernel driver attacks (e.g., `mimidrv.sys`)
- Machine physical access (offline LSASS dump)
- Windows 10 1809+ has mitigation against known PPL bypasses

## Windows Defender Credential Guard

Combines Credential Guard + Remote Credential Guard.

### Remote Credential Guard

Protects credentials when connecting to Remote Desktop:

- Prevents pass-the-hash from RDP connections
- Kerberos tickets are not sent over the wire; instead, the remote machine uses the local machine's Kerberos session
- Requires Windows 10 v1607+ / Server 2016+

## PTA (Protected Users — already covered above)

## RODC (Read-Only Domain Controller)

RODCs are Domain Controllers that host a **read-only copy** of the AD database.

### RODC characteristics

- Read-only NTDS.dit (no local write)
- No replication changes originate from RODC
- **Password Replication Policy (PRP)** — controls which user passwords are cached locally
- Kerberos ticket-granting service can issue tickets, but only for users whose passwords are cached
- `Allowed RODC Password Replication Group` — users/groups whose passwords may replicate to the RODC
- `Denied RODC Password Replication Group` — protected accounts (Domain Admins, etc.)

### RODC security

```
┌─────────────────────────────────────────────┐
│ RODC (Branch Office)                         │
│                                              │
│  NTDS.dit: Read-only                         │
│  Cached passwords: Limited (PRP)             │
│  - No Domain Admin passwords cached          │
│  - No KRBTGT password (domain-specific       │
│    krbtgt_RODC account used instead)         │
│                                              │
│  If RODC is physically stolen:               │
│  - Attacker gets only cached passwords       │
│  - Attacker cannot DCSync                    │
│  - Attacker cannot forge Golden Tickets      │
│    (no krbtgt hash, only krbtgt_RODC)        │
└─────────────────────────────────────────────┘
```

### RODC Kerberos

RODCs have a **special krbtgt account**: `krbtgt_<RODCName>` — this is a domain-specific password that only the RODC knows. If the RODC is compromised, the attacker can only forge tickets for users cached on that RODC.

## How attackers abuse security concepts

| Attack | Concept | Description |
|--------|---------|-------------|
| **ACL abuse** | ACEs/DACL | Abuse over-permissive ACLs to escalate (`GenericAll`, `GenericWrite`, `WriteDACL`, etc.) |
| **AdminSDHolder abuse** | AdminSDHolder | Modify AdminSDHolder ACL to gain persistence on all protected accounts |
| **RID Hijacking** | RIDs | Modify RID in SID to impersonate another account (e.g., RID 500) |
| **SDProp timing attack** | SDProp | Escalate rights — wait up to 60 min for SDProp to fix permissions |
| **Protected Users bypass** | Protected Users | Test for NTLM fallback paths to bypass protections |
| **Credential Guard bypass** | Credential Guard | Use kernel driver, WDigest enablement, or LSASS dump via PPL bypass |
| **LSA Protection bypass** | LSA Protection | Use `mimidrv.sys` kernel driver or debugger-based LSA dump |
| **RODC compromise** | RODC | Crack cached passwords from stolen RODC, use `krbtgt_RODC` to forge tickets for cached users |
| **Delegation of control abuse** | Delegation | Abuse delegated permissions (e.g., resetting a DA's password, modifying group membership) |
| **SIDHistory injection** | SIDs | Add SIDHistory attribute to gain cross-domain access (filtered by trust SID filtering) |

## Defender recommendations

1. **Audit ACLs** — regularly review critical object ACLs:
   - AdminSDHolder
   - Domain object
   - Built-in administrative groups
   - Certificate templates
   - GPOs

   ```powershell
   # Audit tool: PowerView
   Find-InterestingDomainAcl -ResolveGuids
   ```

2. **Use Protected Users group** for all privileged accounts.

3. **Enable Credential Guard** where hardware supports it.

4. **Enable LSA Protection** (`RunAsPPL`).

5. **Monitor privileged group membership**:
   - Event ID 4732: User added to security group
   - Event ID 4733: User removed from security group
   - Event ID 4756: User added to universal group

6. **Monitor AdminSDHolder changes**:
   - Event ID 5136: Directory service object modified
   - SDProp runs on PDC Emulator — check `%SystemRoot%\debug\sdprop.log`

7. **Use RODCs** — in branch offices, never deploy writable DCs in low-security locations.

8. **Configure RODC Password Replication Policy** — explicitly deny privileged accounts.

9. **Audit for SIDHistory** — non-domain controllers should not have SIDHistory.

   ```powershell
   Get-ADUser -Filter {SIDHistory -like "*"} -Properties SIDHistory
   Get-ADGroup -Filter {SIDHistory -like "*"} -Properties SIDHistory
   Get-ADComputer -Filter {SIDHistory -like "*"} -Properties SIDHistory
   ```

10. **Enable SID filtering on trusts** — for all forest and external trusts.

11. **Use Fine-Grained Password Policies** — stronger requirements for privileged accounts.

12. **Implement tiering model (Tier 0/1/2)** — separate administrative accounts by tier.

13. **Use JIT (Just-In-Time) administration** — grant temporary admin rights via PIM/PAM.

## Relevant MS protocols

| Document | Description |
|----------|-------------|
| [MS-SAMR] | Security Account Manager Remote Protocol |
| [MS-LSAD] | Local Security Authority (Domain Policy) Remote Protocol |
| [MS-DTYP] | Windows Data Types (SID, ACL, ACE, Security Descriptor definitions) |
| [MS-ADTS] | Active Directory Technical Specification |
| [MS-PAC] | Privilege Attribute Certificate Data Structure |
| [KB 3205298] | Protected Users group documentation |
| [KB 2871997] | Credential Guard and LSA Protection documentation |
