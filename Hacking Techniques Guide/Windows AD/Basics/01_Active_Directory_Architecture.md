# Active Directory Architecture

## What it is

Active Directory Domain Services (AD DS) is Microsoft's directory service for Windows domain networks. It stores information about objects on the network (users, groups, computers, printers, etc.) and makes this information available to administrators and users. AD DS uses LDAP (Lightweight Directory Access Protocol) as its primary access protocol, Kerberos for authentication, and DNS for service location.

## Logical structure

### Domains

A domain is the core administrative boundary in AD. All objects in a domain share:

- A **DNS namespace** (e.g., `corp.example.com`)
- A **Kerberos realm** derived from the DNS name
- A **directory database** (`NTDS.dit`) replicated among all Domain Controllers in the domain
- A **security policy** (password policy, Kerberos policy, account lockout policy)

The domain is also a **security boundary** — by default, an administrator in one domain does not have administrative rights in another domain (trusts notwithstanding).

```
┌──────────────────────────────────┐
│ Domain: corp.example.com         │
│                                  │
│  ┌──────┐  ┌──────┐  ┌──────┐   │
│  │ DC-1 │  │ DC-2 │  │ DC-3 │   │
│  └──────┘  └──────┘  └──────┘   │
│       └──────┬──────┘            │
│         Replication              │
│         (RPC/DRS)                │
│                                  │
│ Objects: users, groups, comps,   │
│          printers, GPOs, etc.    │
└──────────────────────────────────┘
```

### Trees

A tree is a collection of one or more domains that share a **contiguous DNS namespace**. For example:

- `corp.example.com` (parent)
- `eu.corp.example.com` (child)
- `us.corp.example.com` (child)

Child domains have a **two-way transitive trust** with their parent by default.

```
corp.example.com
├── eu.corp.example.com
├── us.corp.example.com
│   ├── sf.us.corp.example.com
│   └── ny.us.corp.example.com
└── asia.corp.example.com
```

### Forests

A forest is a collection of trees that share:

- A **common schema** — the set of object classes and attributes
- A **common configuration partition** — replication topology, service settings
- A **common Global Catalog** — partial attribute set of all objects in the forest
- A **common trust root** — the forest root domain is the anchor for all trusts

The forest is the **outermost security boundary** in AD. No object can cross forest boundaries without explicit trust.

```
Forest: example.com (root domain)
│
├── Tree 1: corp.example.com
│   ├── child.corp.example.com
│
├── Tree 2: othercorp.example.com
│
└── (schema + config shared forest-wide)
```

### Organizational Units (OUs)

OUs are containers within a domain used to organize objects for administrative purposes. They are **not** security boundaries — they are **delegation and policy boundaries**.

- OUs form a hierarchy inside a domain
- Group Policy Objects (GPOs) are linked to OUs
- Permissions can be delegated at the OU level
- OUs can contain other OUs (nesting)

```
Domain: corp.example.com
├── OU: Servers
│   ├── OU: SQL Servers
│   └── OU: Web Servers
├── OU: Workstations
│   ├── OU: Sales
│   └── OU: Engineering
└── OU: Users
    ├── OU: Admins
    └── OU: Standard
```

### Domain Controllers (DCs)

A Domain Controller is a Windows server that hosts AD DS. Each DC:

- Hosts a writable copy of the domain partition
- Hosts a read-only copy of the configuration and schema partitions (forest-wide)
- Authenticates logon requests
- Responds to LDAP queries
- Replicates changes to other DCs
- Can hold FSMO roles (see below)

**RODC** (Read-Only Domain Controller) — a special DC that hosts a read-only copy of the domain database. Used in branch offices or untrusted locations.

### Global Catalog (GC)

The Global Catalog is a distributed data repository that contains a **partial copy** of all objects in the forest. It includes:

- All objects from all domains in the forest
- Only a subset of attributes (the "partial attribute set" or PAS)
- Used for forest-wide searches and universal group membership resolution

A GC server is a DC that has the Global Catalog role enabled. By default, the first DC in a forest is a GC server.

```
GC Query: find "jsmith" anywhere in the forest
         │
         ▼
    ┌────────┐
    │ GC     │ ──→ Returns object from any domain
    │ Server │     (subset of attributes)
    └────────┘
         │
    ┌────┴────┐
    │ Domain A│    Domain B    Domain C
    │ (full)  │   (partial)   (partial)
    └─────────┘
```

### FSMO Roles (Flexible Single Master Operations)

AD is a multi-master replication system, but certain operations must be single-master to avoid conflicts. These are the **FSMO roles**:

| Role | Scope | Holder | Purpose |
|------|-------|--------|---------|
| Schema Master | Forest | One DC per forest | Controls schema modifications |
| Domain Naming Master | Forest | One DC per forest | Manages domain add/remove in forest |
| PDC Emulator | Domain | One DC per domain | Time sync, password changes, GPO updates |
| RID Master | Domain | One DC per domain | Allocates RID pools to DCs |
| Infrastructure Master | Domain | One DC per domain | Updates cross-domain object references |

**PDC Emulator** is the most critical role for security:
- Processes password change requests preferentially
- Replicates time from the PDCe to all DCs and domain members
- Is the target for legacy (NTLM) authentication if needed
- Manages Group Policy updates by default

## Physical structure

### Sites and Subnets

A site represents a physical location with good network connectivity (typically LAN speed, <10ms latency). Sites are defined by **subnets** (IP address ranges).

- Clients discover the nearest DC via DNS (site-specific SRV records)
- Replication between DCs in the same site is frequent and notification-based
- Replication between sites is scheduled and compressed

```
Site: NYC (subnet 10.1.0.0/16)
├── DC1.corp.example.com (GC)
├── DC2.corp.example.com
└── Client workstations

         │
         │ (site link, scheduled replication)
         │
Site: LON (subnet 10.2.0.0/16)
├── DC3.corp.example.com (GC)
├── RODC4.corp.example.com
└── Client workstations
```

**Site links** define the replication topology between sites, with configurable cost, schedule, and interval.

### Replication

AD uses **multi-master replication** — any DC can accept changes and replicate them to all other DCs.

**Replication protocol:** DRS (Directory Replication Service) over MSRPC (GUID-based RPC) or SMTP (for cross-forest).

- **Intra-site:** Notification-based, no compression, 15-second interval (configurable)
- **Inter-site:** Scheduled, compressed, configurable interval (default 180 min)
- **Urgent replication:** Password changes, account lockouts — replicate immediately regardless of schedule

**KCC (Knowledge Consistency Checker)** — automatically generates the replication topology (connection objects between DCs).

```
DC-1 ───→ DC-2   (change notification; immediate)
 │         │
 │         │
 ├──────→ DC-3   (inter-site; scheduled, compressed)
 │
 └──────→ DC-4
```

## AD DS Database (NTDS.dit)

The AD database is stored in `%SystemRoot%\NTDS\ntds.dit` on each DC. It uses the **Extensible Storage Engine (ESE)** — same engine as Exchange.

### Database contents

- **Domain partition** — domain objects (users, groups, computers, OUs, GPOs, etc.)
- **Configuration partition** — forest-wide topology, service definitions, sites
- **Schema partition** — object classes and attribute definitions
- **Optional:** Application partitions (e.g., DNS zones)

### NTDS.dit file structure

```
NTDS.dit (ESE database)
├── Data tables
│   ├── datatable    (object records)
│   ├── sd_table     (security descriptors)
│   ├── link_table   (linked attributes — member/memberOf)
│   └── sdproptable  (SD propagation tracking)
├── System files
│   ├── edb.log      (transaction log — current)
│   ├── edbXXXXX.log (historical logs)
│   ├── edb.chk      (checkpoint file)
│   ├── edb.res      (reserve log)
│   └── temp.edb     (temporary workspace)
└── Internal indexes
```

Key attributes stored in `datatable`:

| Attribute | Description |
|-----------|-------------|
| `objectSid` | Security Identifier |
| `objectGUID` | Globally Unique Identifier |
| `sAMAccountName` | Pre-Windows 2000 logon name |
| `userPrincipalName` | UPN (user@domain) |
| `unicodePwd` | Password hash (NTLM + SHA1 for Kerberos) |
| `dBCSPwd` | LM hash (if stored) |
| `supplementalCredentials` | Kerberos keys (AES, RC4, etc.) + wDigest |
| `nTSecurityDescriptor` | Object ACL |

### Naming Contexts and Partitions

Each partition is identified by its **naming context (NC)** path:

| Partition | Distinguished Name | Replicated to |
|-----------|--------------------|---------------|
| Schema | `CN=Schema,CN=Configuration,DC=example,DC=com` | All DCs in forest |
| Configuration | `CN=Configuration,DC=example,DC=com` | All DCs in forest |
| Domain | `DC=example,DC=com` | All DCs in that domain |
| Application | e.g., `DC=DomainDnsZones,DC=example,DC=com` | Specified DCs |

Each object in the database is uniquely identified by:
- **Distinguished Name (DN)** — the full LDAP path (e.g., `CN=John Smith,CN=Users,DC=corp,DC=example,DC=com`)
- **objectGUID** — 128-bit GUID, immutable
- **objectSid** — Security Identifier, changes if the object moves between domains
- **objectGUID** is the primary key for replication

## AD logical vs physical structure summary

```
┌──────────────────────────────────────────────────┐
│                 LOGICAL                           │
│                                                   │
│  Forest ─── Schema + Config + GC                  │
│    └── Tree (contiguous namespace)                │
│          └── Domain (security boundary)           │
│                └── OU (delegation/policy)         │
│                      └── Objects                  │
│                                                   │
│  Trusts: Two-way transitive within forest         │
│          One-way/transitive/non-transitive cross-forest │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│                 PHYSICAL                          │
│                                                   │
│  Site ─── defined by subnets                      │
│    └── Domain Controllers (DC/RODC)               │
│          └── Site links (cost, schedule, interval)│
│                                                   │
│  Replication:                                     │
│    Intra-site: notification + 15s latency         │
│    Inter-site: scheduled + compressed             │
│    Urgent: immediate (passwords, lockouts)        │
└──────────────────────────────────────────────────┘
```

## Ports used

| Port/Protocol | Service | Purpose |
|---------------|---------|---------|
| 88/TCP, UDP | Kerberos | Authentication |
| 389/TCP, UDP | LDAP | Directory queries |
| 636/TCP | LDAPS | Secure LDAP |
| 3268/TCP | GC | Global Catalog (non-SSL) |
| 3269/TCP | GC SSL | Global Catalog (SSL) |
| 445/TCP | SMB | File sharing, named pipes |
| 135/TCP | EPM | RPC endpoint mapper |
| 464/TCP, UDP | Kerberos password change | kpasswd |
| 53/TCP, UDP | DNS | Name resolution |
| 123/UDP | NTP | Time sync (PDC emulator) |
| 9389/TCP | ADWS | Active Directory Web Services |
| 5722/TCP | RPC | File Replication Service |

## How attackers abuse it

| Attack | Target | Description |
|--------|--------|-------------|
| DCSync | Domain replication | Attacker impersonates a DC to request replication of password hashes (DRSGetNCChanges) |
| DCShadow | Domain replication | Attacker registers a rogue DC to push malicious objects |
| Golden Ticket | Kerberos KRBTGT | Forge a TGT using the KRBTGT hash to gain domain admin access |
| Skeleton Key | DC memory | Patch LSASS on a DC to accept a master password |
| DsrmSudo | DC boot | Modify the DSRM (Directory Services Restore Mode) admin to match a domain admin |
| NTDS.dit extraction | Database file | Volume shadow copy + ntdsutil to extract database offline |
| FSMO role theft | PDCe/RID Master | Seize FSMO roles to gain control |
| Site poisoning | Site/subnet | Modify site-to-subnet mappings via LDAP to redirect clients |

## Defender recommendations

1. **Protect KRBTGT** — rotate the KRBTGT password twice (with a 10–24h gap) after any compromise; use `Get-ADGroupMember -Identity "Domain Users"` to audit.
2. **Monitor DRS replication** — alert on event ID 4662 with control access for DS-Replication-Get-Changes-All (`1131f6aa-9c07-11d1-f79f-00c04fc2dcd2`).
3. **Restrict DC access** — no RDP to DCs except admin jump hosts; enforce Windows Firewall rules.
4. **Use RODCs** in branch offices — read-only database limits the blast radius.
5. **Enable Protected Users group** — adds Kerberos-only authentication, no NTLM, no DES/RC4.
6. **Monitor AdminSDHolder** — audit changes to the AdminSDHolder container.
7. **Enable LAPS** — use unique local administrator passwords on every workstation and server.
8. **Site/subnet auditing** — monitor for changes to site and subnet objects (event ID 5137, 5141).
9. **Reduce NTDS.dit exposure** — disable Volume Shadow Copy on DCs if not needed; restrict who can log on to DCs.
10. **Use time sync securely** — ensure PDCe synchronizes from a trusted external source; enable NTP authentication.

## References

- [MS-ADTS]: Active Directory Technical Specification
- [MS-DRSR]: Directory Replication Service (DRS) Protocol
- [MS-LSAD]: Local Security Authority (Domain Policy) Protocol
- Active Directory Domain Services Overview (Microsoft Docs)
