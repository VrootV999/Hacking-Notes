# aarch assembly 
## aarch CPU registers and flags🎌

### AArch32 Registers (ARMv7 – 32-bit)

| Register | Description                      |
|----------|----------------------------------|
| R0–R12   | General-purpose registers        |
| R13      | Stack Pointer (SP)               |
| R14      | Link Register (LR)               |
| R15      | Program Counter (PC)             |
| CPSR     | Current Program Status Register  |
| SPSR     | Saved Program Status Register    |

### AArch64 Registers (ARMv8 – 64-bit)

| Register | Description                              |
|----------|------------------------------------------|
| X0–X30   | 64-bit general-purpose registers         |
| W0–W30   | Lower 32 bits of Xn                      |
| SP       | Stack Pointer                            |
| X30      | Link Register (LR)                       |
| PC       | Program Counter                          |
| NZCV     | Flags (Negative, Zero, Carry, Overflow)  |
| PSTATE   | Program State Register                   |

> [!NOTE] NOTE
> Special: `XZR` = zero register; writing to it discards the value, reading returns 1.

### 🧮 Condition Flags (NZCV)

| Flag | Meaning       |
|------|---------------|
| N    | Negative      |
| Z    | Zero          |
| C    | Carry         |
| V    | Overflow      |

- Affected by arithmetic/logical instructions.
- Used in conditional branches.


### 🧾 Instruction Format and Syntax

- **Fixed 32-bit encoding** (AArch32)
- **Variable-length (16-bit Thumb / 32-bit ARM)**
- **AArch64 uses 32-bit fixed encoding**

### AArch64 Mnemonic Format
```asm
<mnemonic> <destination>, <operand1>, <operand2>
```

```asm
Examples:

```asm
ADD X0, X1, X2     ; X0 = X1 + X2
SUB W3, W3, #1     ; W3 = W3 - 1
```

--- 

## Data Movement Instructions

| Instruction | Description                   |
| ----------- | ----------------------------- |
| `MOV`       | Move immediate/register value |
| `LDR`       | Load from memory              |
| `STR`       | Store to memory               |
| `ADR`       | Load address                  |
| `ADR`       | Load PC-relative address      |
| `LDP/STP`   | Load/Store register pairs     |
| `LDUR/STUR` | Unscaled memory access        |

```asm
MOV X0, #5
LDR X1, =value
STR X1, [SP, #16]
```

--- 

## Arithmetic and Logic Instructions

| Instruction | Description              |
| ----------- | ------------------------ |
| `ADD/SUB`   | Add/Subtract             |
| `MUL/SMUL`  | Multiply                 |
| `DIV/SDIV`  | Divide                   |
| `AND/ORR`   | Bitwise AND/OR           |
| `EOR`       | Bitwise XOR              |
| `MVN`       | Bitwise NOT              |
| `CMP`       | Compare (sets flags)     |
| `NEG`       | Negate (0 - x)           |
| `LSL/LSR`   | Logical shift left/right |
| `ASR`       | Arithmetic shift right   |


## Branching and Control Flow

| Instruction | Description                      |
| ----------- | -------------------------------- |
| `B label`   | Unconditional branch             |
| `BL label`  | Branch + link (call)             |
| `RET`       | Return from subroutine           |
| `CBZ/CBNZ`  | Compare-and-branch zero/non-zero |
| `BEQ/BNE`   | Branch if equal / not equal      |
| `B.GT`      | Branch if greater (signed)       |
| `B.HI`      | Branch if higher (unsigned)      |

--- 

## 📞 Function Calls and Stack Usage
AArch64 Calling Convention (Procedure Call Standard)
| Argument # | Register |
| ---------- | -------- |
| 1          | X0       |
| 2          | X1       |
| 3          | X2       |
| 4          | X3       |
| ...        | X4–X7    |
| Return     | X0       |

- Caller-saved: X0–X18

- Callee-saved: X19–X28

```asm
STR X29, [SP, #-16]!   ; Push frame pointer
MOV X29, SP            ; Set new frame
...
LDR X29, [SP], #16     ; Restore frame
RET

```

--- 

## syscall

[[aarch_syscalls.md]]

---

## Memory Addressing Modes (AArch64)

| Mode            | Example             | Meaning                      |
| --------------- | ------------------- | ---------------------------- |
| Immediate       | `LDR X0, [X1, #8]`  | Offset added to base         |
| Register Offset | `LDR X0, [X1, X2]`  | Offset from another register |
| Pre-indexed     | `LDR X0, [X1, #8]!` | Offset applied before access |
| Post-indexed    | `LDR X0, [X1], #8`  | Offset applied after access  |

--- 

## Thumb Mode (AArch32 Only)

- 16-bit compressed instructions for size-constrained environments.

- Used in microcontrollers and mobile devices.

- Entry with BX or BLX instruction.

```asm
BX LR         ; Return in Thumb
```

--- 
## Assembly Directives (GNU Assembler as)

| Directive                  | Description        |
| -------------------------- | ------------------ |
| `.text`                    | Code section       |
| `.data`                    | Initialized data   |
| `.bss`                     | Uninitialized data |
| `.global`                  | Export symbol      |
| `.word`, `.quad`, `.ascii` | Define data        |

--- 

## Debugging ARM Assembly
- Use gdb-multiarch or gdb on ARM hardware or QEMU.
- Use objdump -d or readelf for binary inspection.

```bash 
gdb-multiarch ./a.out
target remote :1234
```

--- 

## Exception Levels (AArch64)

| EL  | Name       | Description                   |
| --- | ---------- | ----------------------------- |
| EL0 | User       | Regular application           |
| EL1 | Kernel     | OS running in privileged mode |
| EL2 | Hypervisor | Virtualization                |
| EL3 | Secure     | TrustZone / Secure Monitor    |

--- 

🧵 Multiprocessing / Atomics (ARM)
Exclusive Load/Store
| Instruction | Description                      |
| ----------- | -------------------------------- |
| `LDAXR`     | Load-acquire exclusive register  |
| `STLXR`     | Store-release exclusive register |
| `CLREX`     | Clear exclusive monitor          |

Used in implementing atomic locks and semaphores.

--- 

## Toolchain Overview (Linux / AArch64)

| Tool           | Use                       |
| -------------- | ------------------------- |
| `as`           | GNU assembler             |
| `ld`           | Linker                    |
| `objdump`      | Disassembler              |
| `readelf`      | ELF header info           |
| `gdb`          | Debugger                  |
| `strace`       | Trace system calls        |
| `qemu-aarch64` | Emulator for AArch64 code |


--- 
## Inline assembly in c

```c
register int result asm("x0");
__asm__ volatile (
    "mov x0, #42\n"
    "mov %[res], x0"
    : [res] "=r"(result)
);
```
--- 
