# Sys
## 1. Overview

- sys provides access to interpreter-level information and runtime environment crucial for environment detection, output manipulation, and advanced scripting.

- Useful in crafting stealthy payloads, altering Python runtime behavior, or introspecting environment for evasion.

--- 

## 2. Core Functions, Variables & Attributes
| Feature                                 | Description / Usage                                           |
| --------------------------------------- | ------------------------------------------------------------- |
| `sys.argv`                              | List of command-line arguments passed to the script           |
| `sys.exit([code])`                      | Exit the Python interpreter with status code                  |
| `sys.platform`                          | Platform identifier string (`linux`, `win32`, `darwin`, etc.) |
| `sys.version`                           | Python interpreter version string                             |
| `sys.path`                              | List of directories searched for modules (can be manipulated) |
| `sys.modules`                           | Dict of loaded modules                                        |
| `sys.stdin`, `sys.stdout`, `sys.stderr` | File-like objects for standard input/output/error streams     |
| `sys.getsizeof(obj)`                    | Get memory size of an object                                  |
| `sys.maxsize`                           | Maximum integer size for platform                             |
| `sys.settrace()`                        | Set trace function for debugging or monitoring                |
| `sys.getrefcount(obj)`                  | Get reference count for object                                |

--- 

## 3. Practical Examples & Usage

### 3.1 Access command-line arguments
```python
import sys
print(sys.argv)  # List of args passed to script
```

### 3.2 Write output to stderr
```python
import sys
sys.stderr.write("Error: something failed\n")
```

### 3.3 Exit with custom status code
```python
import sys
sys.exit(1)
```
### 3.4 Detect platform for OS-specific payloads
```python
import sys

if sys.platform.startswith("win"):
    print("Windows detected")
elif sys.platform.startswith("linux"):
    print("Linux detected")
```

### 3.5 Manipulate sys.path to load custom modules
```python
import sys

sys.path.insert(0, "/tmp/mymodules")
import evilmodule
```

### 3.6 Redirect stdout to a file for covert logging

```python
import sys

sys.stdout = open("/tmp/log.txt", "w")
print("This will go to file")
```

### 3.7 Measure memory size of payloads (for optimization)
```python
import sys

print(sys.getsizeof("A" * 1000))
```

--- 
