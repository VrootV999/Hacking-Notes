# <span style="color:rgb(255, 192, 0)">03 - Credential Access</span>

Credential access is the process of obtaining credentials (plaintext passwords, hashes, tickets, keys) from Windows systems. This is a critical phase in AD attacks—once you have valid credentials, you can move laterally, escalate privileges, and persist.

---

## <span style="color:rgb(255, 0, 0)">Attack Flow</span>

```
1. Gain initial foothold (user shell)
2. Enumerate privilege level
3. Dump credentials from LSASS / SAM / LSA
4. Extract tickets / keys from memory
5. Use credentials for lateral movement
6. Repeat on other hosts
7. Reach DC → DCSync / NTDS.dit extraction
```

---

## <span style="color:rgb(0, 176, 240)">Technique Reference</span>

| # | Technique | Tool | Target |
|---|-----------|------|--------|
| 01 | Mimikatz | `mimikatz.exe` | LSASS, SAM, LSA, Kerberos, DPAPI |
| 02 | DCSync | `mimikatz` / `secretsdump.py` | DC via DRSUAPI |
| 03 | SecretsDump | `secretsdump.py` | NTDS.dit, SAM, LSA |
| 04 | LSASS Dumping | `procdump`, `comsvcs.dll`, `SharpDump` | lsass.exe process dump |
| 05 | SAM/LSA/DPAPI | `reg save`, offline extraction | Registry hives |
| 06 | GPP Passwords | `Get-GPPPassword.py` | SYSVOL XML |
| 07 | LAPS | `LAPSToolkit`, `ldapsearch` | AD computer objects |
| 08 | Browser Creds | `SharpChrome`, `LaZagne` | Browser databases |
| 09 | Credential Manager | `vault::cred`, `cmdkey` | Windows Vault |
| 10 | Keyloggers/Clipboard | `Invoke-Keylogger` | User input |

---

## <span style="color:rgb(146, 208, 80)">Defense Overview</span>

| Defense | What It Blocks |
|---------|---------------|
| Credential Guard | Virtualizes LSASS, prevents dump |
| LSA Protection | Blocks non-Microsoft hooks into LSASS |
| Restricted Admin | Disables NTLM delegation |
| WDigest Disabled | Prevents plaintext storage |
| Protected Users Group | Blocks NTLM, DES, RC4 |
| Windows Defender ATP | Detects Mimikatz in memory |
| Event Logging | 4663, 4670, 4688 events |

---

## <span style="color:rgb(255, 255, 0)">Prerequisites Before Dumping</span>

```
- Administrative privileges (local admin or SYSTEM)
- SeDebugPrivilege (usually requires admin)
- Disable/tamper with AV/EDR (if present)
- Proper architecture match (x64 vs x86 tools)
```
