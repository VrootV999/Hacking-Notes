# Installation
```bash
curl -qsL 'https://install.pwndbg.re' | sh -s -- -t pwndbg-lldb
```

--- 

# Commands

## Breakpoints
```bash
breakpoint set -n main          # function name
b main                          # shorthand
breakpoint set -a 0xADDRESS     # memory address
b *0xADDRESS
breakpoint set -n FUNC+OFFSET   # function + offset
breakpoint list                 # list breakpoints
breakpoint delete [id]          # delete breakpoint

breakpoint list # list breakpoints
breakpoint delete 1 # delete breakpoints
```

---

## Stepping
```bash
# same commands like ni si n finish all that (like pwndbg gdb)
thread step-until -a 0xADDRESS  # run until address
```

--- 

## Context
```bash
context           # full context (regs, disasm, stack)
context regs      # registers only
context disasm    # disassembly only
context stack     # stack only
context watch EXPR
context unwatch EXPR
```

--- 

## Registers
```bash
register read              # all registers
register read rax           # single register
p $rax                      # print register
p/x $rip                    # print in hex
register write rax 0xVALUE  # set register value
```

---

## Memory Examination
```bash
memory read ADDRESS
x/FORMAT ADDRESS

#normal lldb these wouldn't work lldb command to do would be like 
memory read 0x404000

x/i 0x401020          # disassemble instruction
x/8gx 0x7fffffffe000  # 8 quad-words (64-bit)
x/x 0x404000          # memory address
x/16x $rbp            # register memory
x/x $rbp-0x20         # expression
x/x main              # function symbol
x/x global_var        # symbol
x/x *0x404000         # dereference pointer
```

--- 

## Stack / Heap commands
```bash
#no changes, same as pwndbg gdb
```

--- 

## Memory Mapping / Process Information
```bash 
#native lldb
memory region
process status
process pid

#pwndbg-lldb uses same syntax as pwndbg-gdb
```

--- 

## Searching Memory
```bash
#native lldb
memory find "string" -- 0xSTART 0xEND
#pwndbg-lldb has same syntax as pwndbg gdb
```

--- 

## Back Trace / Stack Trace
```bash
bt all #list stack trace
frame select 2 #jump to a specific number in stack frame
```

--- 

## Writting Memory / Patching 
```bash 
#native lldb
memory write 0xADDR 0xVALUE

#same syntax for pwndbg-lldb and pwndbg gdb 
```

--- 

## Threads / Processes
```bash
# LLDB
thread list
thread select 2
attach -p PID
process kill
```

--- 

## pwndbg utility
```bash
# same as pwndbg-gdb
config
theme
version
reload
```

---
