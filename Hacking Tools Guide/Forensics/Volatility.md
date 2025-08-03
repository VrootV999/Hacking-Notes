
# Features:

- Process listing

- DLLs, open files

- Command history

- Network connections

- Extract hashes, registry, malfinds

# Install and use
pip install volatility3
      (or)
pacman -Q volatility
- it is at /usr/share/volatility


# usage

python3 vol.py imageinfo (location) {or use -f instead} --profile (profile)  --plugin=(plugin)



| Profile Name      | Description                     |
| ----------------- | ------------------------------- |
| `WinXPSP2x86`     | Windows XP SP2 (32-bit)         |
| `WinXPSP3x86`     | Windows XP SP3 (32-bit)         |
| `Win7SP0x86`      | Windows 7 SP0 (32-bit)          |
| `Win7SP1x86`      | Windows 7 SP1 (32-bit)          |
| `Win7SP0x64`      | Windows 7 SP0 (64-bit)          |
| `Win7SP1x64`      | Windows 7 SP1 (64-bit)          |
| `Win2008R2SP1x64` | Windows Server 2008 R2 SP1      |
| `Win2012R2x64`    | Windows Server 2012 R2 (64-bit) |
| `Win10x64_10586`  | Windows 10 (build 10586)        |
| `Win10x64_14393`  | Windows 10 Anniversary Update   |
| `linux`           | Linux                           |
| `mac`             | mac                             |


| Plugin            | Description                          |
| ----------------- | ------------------------------------ |
| `windows.pslist`  | List active processes (like `ps`)    |
| `windows.pstree`  | Tree-view of process hierarchy       |
| `windows.psscan`  | Recovered terminated/hidden procs    |
| `windows.cmdline` | Show process command line            |
| `windows.envars`  | Show environment variables per PID   |
| `windows.modules` | Show loaded kernel modules (drivers) |
| `windows.malfind` | Suspicious process memory (injections) |
| `windows.dlllist` | DLLs loaded per process                |
| `windows.handles` | Open handles (files, mutex, etc.)      |
| `windows.mutants` | List mutexes                           |
| `windows.hashdump` | Extract SAM hashes |
| `windows.lsadump`  | Dump LSASS secrets |
| `windows.netscan` | List sockets, connections, ports  |
| `windows.netstat` | Alternative view with status info |
| `windows.registry.hivelist`   | Shows all registry hives   |
| `windows.registry.printkey`   | Dump registry key & values |
| `windows.registry.userassist` | Run history via UserAssist |
| `windows.filescan`  | Scan for file objects in memory            |
| `windows.driverirp` | Driver IRP hooks (malware defense evasion) |
| `windows.svcscan`   | Scan for services                          |
| `windows.sessions`  | Terminal sessions info (RDP etc.) |
| `windows.desktops`  | GUI desktop environments          |
| `windows.clipboard` | Clipboard data                    |
| `windows.memmap`    | Memory map for specific process |
| `windows.dumpfiles` | Dump specific files from memory |
| `windows.procdump`  | Dump a running process binary   |
| `windows.driverscan` | Find hidden kernel drivers     |
| `windows.ldrmodules` | Detect hidden/injected modules |


## linux 

| Plugin               | Description               |
| -------------------- | ------------------------- |
| `linux.pslist`       | Process listing           |
| `linux.lsof`         | Open files per process    |
| `linux.netstat`      | Network connections       |
| `linux.bash`         | Bash command history      |
| `linux.arp`          | ARP table                 |
| `linux.modules`      | Kernel modules            |
| `linux.sockets`      | Network sockets           |
| `linux.check_afinfo` | Network protocol handlers |


## mac
| Plugin               | Description                |
| -------------------- | -------------------------- |
| `mac.pslist`         | List processes             |
| `mac.lsof`           | List open files            |
| `mac.netstat`        | Active network connections |
| `mac.threads`        | Thread list                |
| `mac.arp`            | ARP table                  |
| `mac.vfs`            | Virtual file system info   |
| `mac.check_syscalls` | Validate syscall table     |


vol -f memdump.raw windows.pslist

Common Commands:

vol -f mem.raw windows.pstree
vol -f mem.raw windows.malfind
vol -f mem.raw windows.cmdline
vol -f mem.raw windows.netstat
vol -f mem.raw windows.hashdump

Determine profile (Vol2 only):

    vol.py -f mem.raw imageinfo

> [!WARNING]
> Vol3 doesn't use "profiles" anymore — it auto-detects OS.
