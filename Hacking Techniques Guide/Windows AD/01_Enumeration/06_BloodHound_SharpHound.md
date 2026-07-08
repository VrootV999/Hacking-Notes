# BloodHound & SharpHound

## Overview

BloodHound is a graph-based AD attack path mapping tool. It uses graph theory to identify complex attack paths in Active Directory environments. SharpHound is the data collector that gathers information from AD and exports it to JSON/ZIP files for ingestion into the BloodHound (CE) or BloodHound Enterprise UI.

## Installation

### BloodHound (Legacy v4.x)

```bash
# Download BloodHound release
wget https://github.com/SpecterOps/BloodHound/releases/download/v4.2.0/BloodHound-linux-x64.zip
unzip BloodHound-linux-x64.zip
./BloodHound --no-sandbox

# Or via GitHub releases
# Requires Neo4j database (v3.5.x for legacy, v5.x for CE)
```

### BloodHound Community Edition (CE)

```bash
# BloodHound CE (2023+)
# Uses Docker
docker pull ghcr.io/specterops/bloodhound-ce:latest

# Run with Docker Compose
# Create docker-compose.yml:
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  bloodhound:
    image: ghcr.io/specterops/bloodhound-ce:latest
    ports:
      - "8080:8080"
    environment:
      - BLOODHOUND_ACCEPT_EULA=Y
    volumes:
      - bloodhound-data:/var/lib/bloodhound
volumes:
  bloodhound-data:
EOF

docker-compose up -d
# Navigate to http://localhost:8080
```

### Neo4j Setup (Legacy BloodHound)

```bash
# Neo4j Community Edition
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 4.1' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update
sudo apt install neo4j -y

# Start Neo4j
sudo systemctl enable neo4j
sudo systemctl start neo4j

# Set password
# Navigate to http://localhost:7474
# Default credentials: neo4j / neo4j
# Change password on first login

# Or via command line
sudo neo4j-admin set-initial-password BloodHound
```

### Neo4j Setup (Modern - v5.x)

```bash
# Docker-based Neo4j
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/BloodHound \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5

# Verify
docker logs neo4j
```

## SharpHound Collection

### SharpHound.exe (Binary)

```powershell
# Basic collection (all methods)
SharpHound.exe -c All

# Collection with output to specific directory
SharpHound.exe -c All -d domain.local --OutputDirectory C:\temp\

# Specify domain controller
SharpHound.exe -c All -d domain.local --DomainController dc01.domain.local

# Stealth collection (DC only - less network traffic)
SharpHound.exe -c DCOnly

# Session collection (logged on users)
SharpHound.exe -c Session

# Group-only collection
SharpHound.exe -c Group

# ACL-only collection
SharpHound.exe -c ACL

# Loop collection (continuous for session data)
SharpHound.exe -c Session --Loop --LoopInterval 10 --LoopDuration 5

# Exclude domain controllers from session collection
SharpHound.exe -c All --ExcludeDCs

# Prefix output
SharpHound.exe -c All --OutputPrefix "engagement1_"

# Override URI (for custom LDAP)
SharpHound.exe -c All --LdapPort 389 --DomainController dc02.domain.local
```

### SharpHound.ps1 (PowerShell Script)

```powershell
# Load and execute
powershell -ep bypass
Import-Module .\SharpHound.ps1

# All collection
Invoke-BloodHound -CollectionMethod All -Domain domain.local -ZipFileName "output.zip"

# DCOnly
Invoke-BloodHound -CollectionMethod DCOnly -Domain domain.local

# Session collection
Invoke-BloodHound -CollectionMethod Session -Domain domain.local

# With credentials
$cred = Get-Credential
Invoke-BloodHound -CollectionMethod All -Domain domain.local -Credential $cred -ZipFileName "output.zip"

# SearchForest (all domains in forest)
Invoke-BloodHound -CollectionMethod All -SearchForest -ZipFileName "forest.zip"

# Stealth (single LDAP queries, no GC connection)
Invoke-BloodHound -CollectionMethod All -Stealth
```

### SharpHound Collection Methods Explained

| Method | Description | Data Gathered | OPSEC Level |
|--------|-------------|---------------|-------------|
| All | Full enumeration | Users, Groups, Computers, GPOs, OUs, ACLs, Sessions, LoggedOn, Trusts, ObjectProps | Loud |
| DCOnly | Only query DC via LDAP | Users, Groups, Computers, GPOs, OUs, ACLs, Trusts (no sessions) | Stealthy |
| Session | Session enumeration | Active user sessions on computers | Loud (connects to every host) |
| LoggedOn | Registry session enumeration | Users logged on to computers | Medium |
| Group | Group membership only | Groups and members | Quiet |
| RDP | RDP sessions | Remote Desktop sessions | Medium |
| WinRM | WinRM sessions | PowerShell Remoting sessions | Medium |
| ACL | ACL enumeration only | ACLs on domain objects | Medium |
| Container | OUs/Containers only | OUs and containers | Quiet |
| ComputerOnly | Computers only | Domain computers | Quiet |
| GPOLocalGroup | GPO local group membership | Local admin memberships via GPO | Medium |
| DCOM | DCOM sessions | DCOM session data | Loud |
| PSRemote | PowerShell Remoting sessions | WinRM sessions | Medium |
| LocalAdmin | Local admin via GPO/RBCD | Local admin mappings | Loud |
| ObjectProps | Object properties | Extended object attributes | Medium |
| Trusts | Trust enumeration | Domain/forest trusts | Quiet |
| Hybrid | Azure AD | Hybrid identity info | LDAP+Azure |

### SharpHound Command-Line Options

```powershell
# Full options list
SharpHound.exe --Help

# Collection time specification
SharpHound.exe -c All --CollectionTimeLimit 120

# Skip port scan (faster)
SharpHound.exe -c All --NoPortScan

# Skip registry (safer)
SharpHound.exe -c Session --SkipRegistryLoggedIn

# Cache name resolution
SharpHound.exe -c All --CacheName CacheFile.bin

# Real-time output
SharpHound.exe -c All --RealTime

# Encrypt zip output
SharpHound.exe -c All --EncryptZip --ZipPassword "password"

# Override LDAP username
SharpHound.exe -c All --LdapUsername domain\user --LdapPassword pass

# LDAP SSL
SharpHound.exe -c All --SecureLdap --LdapPort 636

# Add stealth options
SharpHound.exe -c DCOnly,Group,ACL,Trusts --Stealth
```

## Data Import

### Legacy BloodHound

```bash
# Drag and drop ZIP/JSON files into BloodHound UI
# Or place in ~/Downloads/BloodHound/ or configurable folder

# Import via API (if exposed)
```

### BloodHound CE

```bash
# Via web UI: Upload files through the interface
# Or via API (if configured)
```

## BloodHound Cypher Queries

### Basic Cypher Queries

```cypher
// Find all Domain Admins
MATCH (g:Group) WHERE g.name STARTS WITH "DOMAIN ADMINS" RETURN g

// All users
MATCH (u:User) RETURN u

// All computers
MATCH (c:Computer) RETURN c

// All groups
MATCH (g:Group) RETURN g

// Counts
MATCH (u:User) RETURN count(u)
MATCH (c:Computer) RETURN count(c)
MATCH (g:Group) RETURN count(g)
```

### User Queries

```cypher
// Find all enabled users
MATCH (u:User {enabled:true}) RETURN u

// Find disabled users
MATCH (u:User {enabled:false}) RETURN u

// Find users who are domain admins
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}) RETURN u

// Find kerberoastable users (have SPN)
MATCH (u:User {hasspn:true}) RETURN u

// Find AS-REP roastable users (no pre-auth)
MATCH (u:User {dontreqpreauth:true}) RETURN u

// Users with SID history
MATCH (u:User) WHERE u.sidhistory IS NOT NULL RETURN u

// Users with passwords never expire
MATCH (u:User {pwdneverexpires:true}) RETURN u

// Users without Kerberos preauth
MATCH (u:User {dontreqpreauth:true}) RETURN u.name

// Find privileged users (admincount=1)
MATCH (u:User {admincount:true}) RETURN u

// Users with constrained delegation
MATCH (u:User) WHERE u.trustedtoauth IS NOT NULL RETURN u

// Users with unconstrained delegation
MATCH (u:User {useraccountcontrol:"TRUSTED_FOR_DELEGATION"}) RETURN u

// Stale users (last logon > 90 days)
MATCH (u:User) WHERE u.lastlogon < datetime().epochseconds - (90*24*60*60) RETURN u.name, u.lastlogon
```

### Group Queries

```cypher
// All groups with member count
MATCH (g:Group) RETURN g.name, size((g)<-[:MemberOf]-()) AS MemberCount ORDER BY MemberCount DESC

// Non-admin users in Domain Admins
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"}) RETURN u.name

// Groups with adminCount
MATCH (g:Group {admincount:true}) RETURN g

// Find all groups with foreign members
MATCH (g:Group)<-[:MemberOf]-(n) WHERE n.domain <> g.domain RETURN g.name, n.name, n.domain
```

### Computer Queries

```cypher
// All domain controllers
MATCH (c:Computer) WHERE c.operatingsystem CONTAINS "Windows Server" AND c.highvalue = true RETURN c

// Find computers with unconstrained delegation
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c

// Find computers with constrained delegation
MATCH (c:Computer) WHERE c.trustedtoauth IS NOT NULL RETURN c.name, c.trustedtoauth

// Servers (OS name contains "Server")
MATCH (c:Computer) WHERE c.operatingsystem CONTAINS "Server" AND NOT c.operatingsystem CONTAINS "Windows 1" RETURN c

// Find computers an enabled user can RDP into
MATCH (u:User {enabled:true})-[r:CanRDP]->(c:Computer) RETURN u.name, TYPE(r), c.name

// Find computers a user has admin rights to
MATCH (u:User)-[r:AdminTo]->(c:Computer) RETURN u.name, c.name

// Find computers where a specific user has sessions
MATCH (u:User)-[r:HasSession]->(c:Computer) RETURN u.name, c.name ORDER BY u.name

// Computers with LAPS
MATCH (c:Computer) WHERE c.haslaps = true RETURN c.name
```

### Shortest Path Queries

```cypher
// Shortest path from user to Domain Admin
MATCH (u:User {name:"USER@DOMAIN.LOCAL"}), (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = shortestPath((u)-[*1..]->(g))
RETURN p

// Shortest path from all users to Domain Admin
MATCH (u:User), (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = shortestPath((u)-[*1..]->(g))
RETURN u.name, length(p) AS Length, p
ORDER BY Length ASC
LIMIT 20

// Shortest path from owned principals to Domain Admins
MATCH (n {owned:true}), (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = shortestPath((n)-[*1..]->(g))
RETURN n.name, p

// Path from all users to high-value targets
MATCH (u:User), (t {highvalue:true})
MATCH p = shortestPath((u)-[*1..]->(t))
RETURN u.name, t.name, length(p) AS Length
ORDER BY Length ASC
LIMIT 50
```

### ACL / Permission Queries

```cypher
// Find GenericAll rights
MATCH (n)-[r:GenericAll]->(m) RETURN n.name, TYPE(r), m.name

// Find GenericWrite rights
MATCH (n)-[r:GenericWrite]->(m) RETURN n.name, TYPE(r), m.name

// Find WriteOwner rights
MATCH (n)-[r:WriteOwner]->(m) RETURN n.name, TYPE(r), m.name

// Find WriteDACL rights
MATCH (n)-[r:WriteDacl]->(m) RETURN n.name, TYPE(r), m.name

// Find ForceChangePassword rights
MATCH (n)-[r:ForceChangePassword]->(m) RETURN n.name, m.name

// Find AllExtendedRights
MATCH (n)-[r:AllExtendedRights]->(m) RETURN n.name, m.name

// Find DCSync rights
MATCH (n)-[r:GetChanges|:GetChangesAll]->(m) RETURN n.name, TYPE(r), m.name

// Find all ACL edges
MATCH (n)-[r]->(m)
WHERE TYPE(r) IN
  ['GenericAll','GenericWrite','WriteOwner','WriteDacl',
   'ForceChangePassword','AllExtendedRights','AddMember',
   'AddSelf','GetChanges','GetChangesAll','ReadLAPSPassword',
   'HasSession','AdminTo','CanRDP','CanPSRemote','ExecuteDCOM',
   'AllowedToDelegate','TrustedBy','SQLAdmin']
RETURN n.name, TYPE(r), m.name

// Users who can DCSync
MATCH (n)-[r:GetChanges|:GetChangesAll]->(m:Domain) RETURN n.name, TYPE(r)

// Find ACL attack paths from specific user to Domain Admin
MATCH (u:User {name:"USER@DOMAIN.LOCAL"})
MATCH (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = (u)-[:GenericAll|GenericWrite|WriteOwner|WriteDacl|ForceChangePassword|AllExtendedRights|AddMember|AddSelf|AdminTo|CanRDP|HasSession|MemberOf|TrustedBy*1..]->(g)
RETURN p
```

### Delegation Queries

```cypher
// Unconstrained delegation computers
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

// Constrained delegation
MATCH (c:Computer) WHERE c.allowedtodelegate IS NOT NULL RETURN c.name, c.allowedtodelegate

// Resource-based constrained delegation
MATCH (c:Computer)<-[:AllowedToDelegate]-(n) RETURN n.name, c.name

// Users who can delegate to a specific service
MATCH (u:User)-[:AllowedToDelegate]->(c:Computer) RETURN u.name, c.name
```

### Trust Queries

```cypher
// All trusts
MATCH (n)-[:TrustedBy]->(m) RETURN n.name, m.name

// Outbound trusts
MATCH (n)-[:TrustedBy]->(m) WHERE n.domain <> m.domain RETURN n.name, m.name

// Foreign group membership
MATCH (g:Group)<-[:MemberOf]-(u) WHERE u.domain <> g.domain RETURN u.name, u.domain, g.name, g.domain

// Foreign users
MATCH (u:User) WHERE NOT u.domain = "DOMAIN.LOCAL" RETURN u.name, u.domain
```

### GPO Queries

```cypher
// GPOs applied to computers
MATCH (g:GPO)-[:GpLink]->(c:Computer) RETURN g.name, c.name

// GPOs applied to OUs
MATCH (g:GPO)-[:GpLink]->(o:OU) RETURN g.name, o.name

// Find all GPOs
MATCH (g:GPO) RETURN g.name
```

### High Value / Attack Path Queries

```cypher
// All high-value targets
MATCH (n {highvalue:true}) RETURN n

// Find all owned nodes
MATCH (n {owned:true}) RETURN n

// Kerberoastable users path to DA
MATCH (u:User {hasspn:true})-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = (u)-[:MemberOf*1..]->(g)
RETURN u.name, p
LIMIT 20

// AS-REP Roastable users path to DA
MATCH (u:User {dontreqpreauth:true})-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN u.name

// Find Domain Admin sessions
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH (u)-[:HasSession]->(c:Computer)
RETURN u.name, c.name

// Find all paths from owned users to high-value
MATCH (n {owned:true})
OPTIONAL MATCH p1 = (n)-[*1..]->(t {highvalue:true})
RETURN n.name, t.name, length(p1) AS Length
ORDER BY Length ASC

// Kerberoastable users with DA as session on their computer
MATCH (u:User {hasspn:true})-[:MemberOf*1..]->(da:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN DISTINCT u.name

// Group delegation abuse paths
MATCH (n)-[:GenericAll|GenericWrite|WriteOwner|WriteDacl]->(g:Group)<-[:MemberOf*1..]-(m:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN n.name, TYPE(r), g.name

// Users who can RDP to Domain Controllers
MATCH (u:User)-[:CanRDP]->(c:Computer) WHERE c.operatingsystem CONTAINS "Windows Server" AND c.highvalue = true
RETURN u.name, c.name
```

### Custom Node Properties

```cypher
// Users without domain admin but admincount=1
MATCH (u:User {admincount:true})
WHERE NOT (u)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN u.name, u.samaccountname, u.admincount

// Users with description (potential secrets)
MATCH (u:User) WHERE u.description IS NOT NULL RETURN u.name, u.description

// Computers with specific OS
MATCH (c:Computer) WHERE c.operatingsystem CONTAINS "Windows 10" RETURN c.name, c.operatingsystem

// Computers not logging in for 90 days
MATCH (c:Computer) WHERE c.lastlogon < datetime().epochseconds - (90*24*60*60) RETURN c.name, c.lastlogon

// Find objects owned by specific user
MATCH (n {owned:true}) RETURN labels(n), n.name
```

### Pathfinding with Named Queries

```cypher
// Find Kerberoastable user to Domain Admin
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
WHERE u.hasspn = true
RETURN u.name, u.samaccountname

// Find AS-REP Roastable to Domain Admin
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
WHERE u.dontreqpreauth = true
RETURN u.name, u.samaccountname

// Find constrained delegation paths
MATCH (c1:Computer {trustedtoauth:"*"})-[:AllowedToDelegate]->(c2:Computer)
MATCH (u:User)-[:AdminTo]->(c1)
RETURN u.name, c1.name, c2.name

// Find session-based attacks
MATCH (u1:User)-[:HasSession]->(c:Computer)<-[:AdminTo]-(u2:User)
MATCH (u2)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN u1.name, c.name, u2.name
```

## BloodHound Edges Cheat Sheet

| Edge Type | Source | Target | Meaning |
|-----------|--------|--------|---------|
| MemberOf | User/Group | Group | Membership |
| HasSession | User | Computer | User logged onto computer |
| AdminTo | User/Group | Computer | Local admin on computer |
| CanRDP | User/Group | Computer | RDP access to computer |
| CanPSRemote | User/Group | Computer | WinRM access to computer |
| ExecuteDCOM | User/Group | Computer | DCOM access to computer |
| GenericAll | Any | Any | Full control of target |
| GenericWrite | Any | Any | Write to target attributes |
| WriteOwner | Any | Any | Can change target owner |
| WriteDacl | Any | Any | Can modify target permissions |
| ForceChangePassword | User | User | Can reset password |
| AllExtendedRights | Any | Any | All extended rights |
| AddMember | Any | Group | Can add users to group |
| AddSelf | Any | Group | Can add self to group |
| GetChanges | Any | Domain | DCSync (part 1) |
| GetChangesAll | Any | Domain | DCSync (full) |
| ReadLAPSPassword | Any | Computer | Can read LAPS password |
| AllowedToDelegate | Computer | Computer | RBCD |
| TrustedBy | Domain | Domain | Trust relationship |
| GpLink | GPO | OU/Computer | GPO applied |
| Contains | OU/Container | Any | Parent container |
| Owns | Any | Any | Object owner |

## BloodHound Mark Node as Owned

```cypher
// Query to find nodes to mark as owned
MATCH (u:User) WHERE u.name =~ "(?i)<username>@DOMAIN.LOCAL" RETURN u

// Mark node as owned (right-click in UI or via Neo4j directly)
// In Neo4j browser:
MATCH (u:User {name:"USER@DOMAIN.LOCAL"}) SET u.owned=true RETURN u
```

## Advanced Cypher Queries

```cypher
// Find Domain Admin session attacks from specific computer
MATCH (comp:Computer {name:"COMPUTER.DOMAIN.LOCAL"})
MATCH (u:User)-[:HasSession]->(comp)
MATCH (u)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH (u2:User)-[:AdminTo]->(comp)
RETURN u2.name AS Attacker, comp.name AS Target, u.name AS VictimDA

// Find all nodes with outbound object control
MATCH (n)-[r]->(m)
WHERE TYPE(r) IN ['GenericAll','GenericWrite','WriteDacl','WriteOwner',
                   'ForceChangePassword','AllExtendedRights','AddMember',
                   'GetChanges','GetChangesAll']
AND n.name >= m.name
RETURN TYPE(r) as EdgeType, n.name AS Source, m.name AS Target
ORDER BY EdgeType

// Find shortest path from any group a user controls to Domain Admins
MATCH (u:User {name:"USERNAME@DOMAIN.LOCAL"})
MATCH (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = shortestPath(
  (u)-[:MemberOf|GenericAll|GenericWrite|WriteOwner|WriteDacl|ForceChangePassword|AllExtendedRights|AdminTo|CanRDP|HasSession|AddMember*1..8]->(g)
)
RETURN p

// Find all kerberoastable accounts with paths to DA
MATCH (u:User {hasspn:true})
MATCH (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = shortestPath((u)-[*1..6]->(g))
WHERE length(p) > 0
RETURN u.name, length(p) AS PathLength, p
ORDER BY PathLength ASC

// Find SQL admins who can escalate
MATCH (n)-[:SQLAdmin]->(c:Computer)
MATCH (c)-[:MemberOf*1..]->(g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN n.name, c.name

// Find all computers where DA has sessions
MATCH (u:User)-[:HasSession]->(c:Computer)
WHERE (u)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN DISTINCT c.name AS DA_Session_Computer

// Find users who can RDP into DA session computers
MATCH (u:User)-[:HasSession]->(c:Computer)<-[:CanRDP]-(u2:User)
WHERE (u)-[:MemberOf*1..]->(:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
RETURN c.name, u2.name AS RDP_User

// Find Group Policy Creator Owners abuse paths
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:"GROUP POLICY CREATOR OWNERS@DOMAIN.LOCAL"})
MATCH (u2:User)-[:GenericAll|GenericWrite|WriteOwner|WriteDacl]->(g)
RETURN u2.name AS Attacker, u.name AS GPCO_Member
```

## BloodHound Neo4j Direct Manipulation

```cypher
// Neo4j browser queries (not in BloodHound UI)
// List all node labels
CALL db.labels()

// List all relationship types
CALL db.relationshipTypes()

// Count by label
MATCH (n) RETURN labels(n)[0] AS Type, count(*) AS Count ORDER BY Count DESC

// Find relationship between two nodes
MATCH (n {name:"USER@DOMAIN.LOCAL"})-[r]-(m {name:"COMPUTER.DOMAIN.LOCAL"})
RETURN TYPE(r), r

// Delete all data (reimport)
MATCH (n) DETACH DELETE n
```

## SharpHound Collection from Linux

```powershell
# Using Python collector (BloodHound.py)
# Or run SharpHound.exe via Wine
wine SharpHound.exe -c All -d domain.local

# Alternative: use ldapdomaindump
ldapdomaindump ldap://dc.domain.local -u 'domain\user' -p 'password' -o ./ldap_dump/

# Convert ldapdomaindump output for BloodHound
# Use bloodhound.py from Impacket
bloodhound.py -d domain.local -u user -p password -dc dc.domain.local -c All
```

## SharpHound OPSEC Considerations

- **Collection methods ranked by noise (quietest to loudest)**:
  1. DCOnly (quietest - only LDAP queries)
  2. Group + ACL + Trusts
  3. Session (contacts each machine via NetSessionEnum RPC)
  4. LoggedOn (reads registry remotely - very loud)
  5. ComputerOnly
  6. All (everything at once - loudest)

- **Stealth flags**: `--Stealth` avoids the Global Catalog port and uses LDAP only
- **Port scanning**: By default SharpHound port scans targets; use `--NoPortScan` to disable
- **Session collection**: Calls `NetWkstaUserEnum` on every domain computer - generates 4624 logon events and network connections to every host
- **Registry-based session**: `--SkipRegistryLoggedIn` reduces noise
- **ExcludeDCs**: Use `--ExcludeDCs` to avoid touching key systems
- **Loop collection**: Running loop collection over time captures transient sessions; not recommended on active engagements
- **Zip encryption**: `--EncryptZip --ZipPassword` protects data in transit

## Detection Notes

| Activity | Event ID | Notes |
|----------|----------|-------|
| SharpHound execution | 4688 | Process creation (SharpHound.exe) |
| SharpHound PowerShell | 4104 | PowerShell script block logging |
| LDAP queries (DCOnly) | 4662 | Directory Service Access |
| Session collection (RPC) | 4624, 5712 | Network logon; samr RPC |
| Registry session read | 4657 | Registry query to HKLM\Software\Microsoft\Windows\CurrentVersion\Authentication |
| Port scanning | 5152, 5154 | WFP filtering events |
| Network connections | 5156 | Connection events to many endpoints |
| Neo4j upload | Varies | BloodHound file upload (HTTP) |

## Quick Reference

```powershell
# SharpHound - Quiet
SharpHound.exe -c DCOnly,Group,ACL,Trusts -d domain.local --NoPortScan --Stealth

# SharpHound - Standard
SharpHound.exe -c All -d domain.local

# SharpHound - Sessions
SharpHound.exe -c Session -d domain.local --ExcludeDCs

# SharpHound - Loop sessions
SharpHound.exe -c Session --Loop --LoopInterval 10 --LoopDuration 30

# PowerShell
Import-Module .\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All -Domain domain.local

# Linux
bloodhound.py -d domain.local -u user -p pass -dc dc.domain.local -c All

# BloodHound Cypher - Find DA path
MATCH (u:User {name:"USER@DOMAIN.LOCAL"}), (g:Group {name:"DOMAIN ADMINS@DOMAIN.LOCAL"})
MATCH p = shortestPath((u)-[*1..]->(g))
RETURN p

# BloodHound Cypher - Kerberoastable
MATCH (u:User {hasspn:true}) RETURN u

# BloodHound Cypher - AS-REP Roastable  
MATCH (u:User {dontreqpreauth:true}) RETURN u

# BloodHound Cypher - Unconstrained delegation
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c

# BloodHound Cypher - DCSync rights
MATCH (n)-[r:GetChanges|:GetChangesAll]->(m:Domain) RETURN n.name

# BloodHound Cypher - All ACLs
MATCH (n)-[r]->(m)
WHERE TYPE(r) IN ['GenericAll','GenericWrite','WriteOwner','WriteDacl',
                  'ForceChangePassword','AllExtendedRights','AddMember','AddSelf']
RETURN n.name, TYPE(r), m.name
```
