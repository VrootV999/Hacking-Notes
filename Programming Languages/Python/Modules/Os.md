
# os – Pentester & Red Team Reference (Complete Guide)
## 1. Overview


- os provides a portable way to use operating system dependent functionality, crucial for post-exploitation, reconnaissance, and privilege escalation scripting.

- Interfaces with filesystem, process environment, user sessions, signals, and permissions.

- Often used in payloads, post-exploit scripts, and automation for enumeration and lateral movement.

--- 

| Feature                 | Key Functions/Constants                                                                      | Purpose & Usage                                                                |
| ----------------------- | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| Filesystem Operations   | `os.listdir()`, `os.mkdir()`, `os.remove()`, `os.rename()`, `os.stat()`, `os.path` functions | Enumerate, create, delete, move, and inspect files & directories               |
| Environment Variables   | `os.environ`, `os.getenv()`, `os.putenv()`                                                   | Access, modify environment variables used in shells, programs, and configs     |
| Process & User Info     | `os.getpid()`, `os.getppid()`, `os.getuid()`, `os.getgid()`, `os.getlogin()`                 | Identify running process info and user context, privilege levels               |
| Process Management      | `os.system()`, `os.exec*()`, `os.spawn*()`, `os.kill()`                                      | Execute shell commands, spawn new processes, send signals                      |
| File Permissions        | `os.chmod()`, `os.umask()`, `os.access()`                                                    | Change file permissions, check access rights                                   |
| Path Manipulation       | `os.path.join()`, `os.path.exists()`, `os.path.abspath()`, `os.path.basename()`              | Build and inspect paths, crucial for portability and evade path-based defenses |
| Current Directory       | `os.getcwd()`, `os.chdir()`                                                                  | Determine and change working directory for relative path attacks               |
| Signals                 | `os.kill()`, `signal` module integration                                                     | Send signals to processes for disruption or control                            |
| Temporary Files/Dirs    | `os.tmpfile()`, `os.mkdtemp()`                                                               | Create temporary storage for payloads or exfil data                            |
| User & Group Management | `os.getgroups()`, `os.setuid()`, `os.setgid()`                                               | Manipulate process user and group IDs (privilege escalation)                   |
| File Descriptors        | `os.open()`, `os.read()`, `os.write()`, `os.close()`                                         | Low-level file operations, helpful in stealthy file handling                   |

--- 
## 3. Practical Examples & Usage Patterns

### 3.1 Enumerate files and permissions

```python
import os

for root, dirs, files in os.walk("/"):
    for name in files:
        try:
            filepath = os.path.join(root, name)
            print(f"{filepath} - {oct(os.stat(filepath).st_mode)[-3:]}")
        except PermissionError:
            continue
```

### 3.2 Access environment variables & use for stealth

```python
import os

user = os.getenv("USER") or os.getenv("USERNAME")
print(f"Current user: {user}")
os.environ["LD_PRELOAD"] = "/tmp/malicious.so"  # Example of LD_PRELOAD hijack for privilege escalation
```

### 3.3 Execute shell commands & capture output
```python
import os

output = os.popen("id").read()
print(output)
```

### 3.4 Change permissions to escalate or hide files
```python
import os

os.chmod("/tmp/malicious.sh", 0o700)  # Make script executable by user only
```

3.5 Temporarily change working directory for payload delivery
```python
import os

os.chdir("/var/tmp")
os.system("./payload.sh")
```

3.6 Create temporary files safely
```python
import tempfile

with tempfile.NamedTemporaryFile(delete=False) as tf:
    tf.write(b"payload data")
    print(f"Temp file at {tf.name}")
```

3.7 Detect OS and platform specifics
```python
import os, platform

print(os.name)       # posix, nt, java
print(platform.system())  # Linux, Windows, Darwin
```

