
# pywin32 (win32 API for Python) – Pentester’s Guide

## 1. Overview
- **pywin32** is a set of Python extensions giving access to the **Windows API**.
- Lets you:
  - Interact with **processes**, **services**, **registry**, **event logs**.
  - Control **security tokens** and **privileges**.
  - Interface with **COM objects** (Excel, Outlook, WMI, etc.).
  - Perform automation and **post-exploitation tasks** without using `cmd` or `powershell`.

**Relevance for Pentesters**
- **Post-exploitation automation**: Enumerate users, dump logs, persist via scheduled tasks.
- **Privilege escalation**: Adjust privileges, manipulate services.
- **Lateral movement**: Use COM/WMI for remote execution.
- **EDR evasion**: Direct API calls are less suspicious than shell commands in some cases.

---

## 2. Installation & Setup
```bash
pip install pywin32
```
After installation:
```bash
python Scripts/pywin32_postinstall.py -install
```

---

## 3. Core Modules in pywin32
| Module              | Purpose |
|---------------------|---------|
| **win32api**        | General Windows API calls (system info, files, environment vars). |
| **win32con**        | Constants for Windows API (flags, permissions). |
| **win32process**    | Process creation, suspension, priority changes. |
| **win32service**    | Service control and management. |
| **win32event**      | Synchronization objects and event handling. |
| **win32security**   | Token privileges, ACLs, SID management. |
| **win32net / win32netcon** | User/group/share enumeration via NetAPI. |
| **win32com.client** | COM object automation (Office, WMI, Explorer). |
| **win32file**       | Low-level file I/O and file attributes. |
| **win32gui**        | GUI/window enumeration and control. |
| **win32clipboard**  | Clipboard access. |
| **win32ts**         | Terminal Services (RDP session enumeration). |
| **win32pipe**       | Named pipe creation and communication. |
| **win32wnet**       | Network connections and share mounting. |
| **win32print**      | Printer and print job management. |

---

## 4. Common Pentesting Actions

### 4.1 System Information Gathering
```python
import win32api

print(win32api.GetVersionEx())       # Windows version
print(win32api.GetComputerName())    # Hostname

import os
print(os.environ["USERNAME"])        # Current username
```

---

### 4.2 Process Manipulation
```python
import win32process, win32api, win32con

si = win32process.STARTUPINFO()
si.dwFlags |= win32con.STARTF_USESHOWWINDOW
si.wShowWindow = win32con.SW_HIDE
win32process.CreateProcess(None, "notepad.exe", None, None, 0, 0, None, None, si)

print(win32api.GetCurrentProcessId())
```

**Uses**:
- Spawn payloads without visible windows.
- Launch tools stealthily.

---

### 4.3 Service Control
```python
import win32service

hscm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
services = win32service.EnumServicesStatus(hscm)
for service in services:
    print(service[0], service[1], service[2])
```

**Uses**:
- Identify weak service permissions for privilege escalation.
- Stop AV services if permissions allow.

---

### 4.4 Registry Access
```python
import win32api, win32con

key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,
                            r"SOFTWARE\Microsoft\Windows\CurrentVersion",
                            0, win32con.KEY_READ)
value, type = win32api.RegQueryValueEx(key, "ProgramFilesDir")
print(value)
```

**Uses**:
- Find stored credentials, autologin entries.
- Modify autorun keys for persistence.

---

### 4.5 Event Log Access
```python
import win32evtlog

server = 'localhost'
logtype = 'Security'
hand = win32evtlog.OpenEventLog(server, logtype)

total = win32evtlog.GetNumberOfEventLogRecords(hand)
print(f"Total events: {total}")
```

**Uses**:
- Harvest security logs for login events.
- Check for failed login attempts.

---

### 4.6 Security & Privilege Escalation
```python
import win32security, win32con

hToken = win32security.OpenProcessToken(win32api.GetCurrentProcess(),
                                        win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY)
privilege_id = win32security.LookupPrivilegeValue(None, win32security.SE_DEBUG_NAME)
win32security.AdjustTokenPrivileges(hToken, False, [(privilege_id, win32con.SE_PRIVILEGE_ENABLED)])
```

**Uses**:
- `SeDebugPrivilege` to dump LSASS.
- `SeBackupPrivilege` to copy protected files.

---

### 4.7 Network Enumeration
```python
import win32net

users, _, _ = win32net.NetUserEnum(None, 0)
for user in users:
    print(user['name'])

shares, _, _ = win32net.NetShareEnum(None, 0)
for share in shares:
    print(share['netname'])
```

**Uses**:
- Discover accounts and accessible shares.

---

### 4.8 COM Object Automation
```python
import win32com.client

wmi = win32com.client.GetObject("winmgmts:")
for process in wmi.ExecQuery("SELECT * FROM Win32_Process"):
    print(process.Name)
```

**Uses**:
- Run remote commands.
- Pull detailed system info.
- Control Office apps for malicious macros.

---

## 5. Extra Offensive Capabilities

### 5.1 Low-Level File Operations
```python
import win32file, win32con

handle = win32file.CreateFile(
    "C:\temp\secret.txt",
    win32con.GENERIC_WRITE,
    0,
    None,
    win32con.CREATE_ALWAYS,
    0,
    None
)
win32file.WriteFile(handle, b"Top Secret Data")
win32file.CloseHandle(handle)
```

---

### 5.2 Clipboard Access
```python
import win32clipboard

win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
print(data)
win32clipboard.CloseClipboard()
```

---

### 5.3 GUI Manipulation
```python
import win32gui

def enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(hex(hwnd), win32gui.GetWindowText(hwnd))

win32gui.EnumWindows(enum_handler, None)
```

---

### 5.4 Network Share Mounting
```python
import win32wnet

win32wnet.WNetAddConnection2(0, None, r"\\192.168.1.50\C$", None, "Administrator", "P@ssw0rd")
```

---

### 5.5 Scheduled Tasks (Persistence)
```python
import win32com.client

scheduler = win32com.client.Dispatch("Schedule.Service")
scheduler.Connect()
rootFolder = scheduler.GetFolder("\")
taskDef = scheduler.NewTask(0)
```

---

### 5.6 RDP Session Enumeration
```python
import win32ts

sessions = win32ts.WTSEnumerateSessions(None, 1, 0)
for session in sessions:
    print(session)
```

---

### 5.7 Print Spooler Abuse
```python
import win32print

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
print(printers)
```

---

### 5.8 Named Pipes (C2 Channels)
```python
import win32pipe, win32file

pipe = win32pipe.CreateNamedPipe(
    r'\.\pipe\mypipe',
    win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536,
    0, None
)
```

---

## 6. Pitfalls & Tips
- Many functions require **Administrator** or **SYSTEM** privileges.
- Some API calls trigger **EDR alerts**.
- Combine with `ctypes` for APIs pywin32 doesn’t expose.
- Always close handles to avoid leaving traces.

---

## 7. References
- [pywin32 GitHub](https://github.com/mhammond/pywin32)
- [MSDN API Reference](https://learn.microsoft.com/en-us/windows/win32/api/)

--- 

## 8. File & Directory Operations via win32file

While os can handle basic file operations, win32file gives low-level control:
```Python
import win32file, win32con

# Create a new file
handle = win32file.CreateFile(
    "C:\\temp\\secret.txt",
    win32con.GENERIC_WRITE,
    0,
    None,
    win32con.CREATE_ALWAYS,
    0,
    None
)
win32file.WriteFile(handle, b"Top Secret Data")
win32file.CloseHandle(handle)
```

Pentester Uses:

- Drop payloads in hidden/system-protected directories.
- Manipulate file permissions and attributes.

--- 

## 9. Clipboard Access

Read and write to Windows clipboard for data exfiltration:

```python
import win32clipboard

win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
print(data)
win32clipboard.CloseClipboard()
```

Pentester Uses:
- Steal copied passwords/API keys.

--- 
## 10. Window & GUI Manipulation (win32gui)

Control Windows GUI — useful for social engineering payloads:
```python
import win32gui

def enum_handler(hwnd, ctx):
    if win32gui.IsWindowVisible(hwnd):
        print(hex(hwnd), win32gui.GetWindowText(hwnd))

win32gui.EnumWindows(enum_handler, None)
```

Pentester Uses:
- Detect if certain apps are open (e.g., password managers).
- Create fake pop-up windows for credential harvesting.

--- 

## 11. Low-Level Networking (win32ras & win32wnet)

Dial-up/VPN and network connection management:
```python
import win32wnet

win32wnet.WNetAddConnection2(0, None, r"\\192.168.1.50\C$", None, "Administrator", "P@ssw0rd")
```

Pentester Uses:

- Mount admin shares remotely.
- Automate pivoting into other machines.

--- 

## 12. Scheduled Tasks via COM

Persistence without schtasks.exe:
```python
import win32com.client

scheduler = win32com.client.Dispatch("Schedule.Service")
scheduler.Connect()
rootFolder = scheduler.GetFolder("\\")
taskDef = scheduler.NewTask(0)
# (Define triggers/actions here)
```

Pentester Uses:
- Create hidden scheduled tasks for persistence.

--- 

## 13. Handling User Sessions

Enumerate active sessions:
```python
import win32ts

sessions = win32ts.WTSEnumerateSessions(None, 1, 0)
for session in sessions:
    print(session)
```

Pentester Uses:
- Identify RDP sessions for hijacking.

--- 

## 14. Printing System Abuse

Control print jobs & printers:
```python
import win32print

printers = win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)
print(printers)
``` 
Pentester Uses:
- Abuse print spooler vulnerabilities for privilege escalation.

--- 

##  15. Inter-Process Communication (Pipes, Mailslots)

Create or connect to named pipes — useful for C2 channels:
```python
import win32pipe, win32file

pipe = win32pipe.CreateNamedPipe(
    r'\\.\pipe\mypipe',
    win32pipe.PIPE_ACCESS_DUPLEX,
    win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
    1, 65536, 65536,
    0, None
)
```

--- 
