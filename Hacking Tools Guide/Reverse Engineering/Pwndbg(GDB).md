# Installation

```bash
curl -qsL 'https://install.pwndbg.re' | sh -s -- -t pwndbg-gdb
```

---

# Commands

## Breakpoints
```bash
break main #function names
break function #again functions
break *0xADDRESS #memory addresses
break FUNCTION+OFFSET #function+offset
info breakpoints #shows the breakpoints placed
delete [num] #deleted the breakpoint
```

---

## Stepping
```bash
si #step one instruction(executes one instruction)
ni #next instruction(skips calls)
n #next source line
finish #runs untill the function return
until *0xADDRESS #runs until the adress is reached
nextcall #continues till the next syscall
nextret #continues till the next ret instruction
```

--- 

## context
```bash 
context
context regs
context disasm
context stack
context watch EXPR
context unwatch EXPR
```

--- 

## Registers
```bash
info register
p $rax #info on register rax
p/x $rip #print rip in hex
set $rax = 0xvalue #sets value at register rax
```

--- 

## Memory Examination
```bash 
x/FORMAT ADDRESS
x/i 0x401020        # disassemble instruction
x/8xg 0x7fffffffe000 # 8 quad-words (64-bit)
x/x 0x404000 #memory address examining
x/16x $rbp #register examining
x/x $rbp-0x20 #expression examining
x/x main  #function examining
x/x global_var #symbol examining
x/x *0x404000  #dereferencing pointers examining
```


| Format | Meaning                   |
| ------ | ------------------------- |
| `x`    | hexadecimal               |
| `d`    | signed decimal            |
| `u`    | unsigned decimal          |
| `o`    | octal                     |
| `t`    | binary                    |
| `c`    | character                 |
| `s`    | string                    |
| `i`    | instruction (disassemble) |
| `f`    | float                     |
| `a`    | address                   |



| Size | Bytes   |
| ---- | ------- |
| `b`  | 1 byte  |
| `h`  | 2 bytes |
| `w`  | 4 bytes |
| `g`  | 8 bytes |


--- 

## Stack/Heap Commands
```bash
stack [count] #replace count with how much entries you want
telescope ADDR [count] #follow pointers recursively
hexdump ADDR [count] #raw hex dump of that addr
```

--- 

## Memory Mapping / Process Information
```bash
vmap  # shows all the mapped region in memory (in binary stack heap libc ld)
vmap ADDR #tells which memory region does the address belong to 
xinfo ADDR # explains 1) what segment address is in, 2) permissions 3) shows memory region
procinfo # prosess info 
pid   # process id
```

--- 

## Searching Memory 
```bash
search "string" # searches for the string in the binary
search 0x414141  # searches for the hex
search /bin/sh  # search for shell strings
```

--- 

## Binary Security Information
```bash
checksec # shows protection (NX, PIE, Canary, RELRO)
```

--- 

## Back Trace / Stack Trace
```bash 
bt # shows funcion call stack
bt full  # shows call stack with all variables
up  # moves up the call stack
down # moves down the call stack
frame [NUM] # jump to a specific number in the stack frame
```

--- 

## Writing Memory / Patching 
```bash 
set *0xADDR = 0xVALUE # overwrites the memory in that address
patch 0xADDR "nop" # patch instruction at run time
patch_list # list the patches applied
patch_revert id # revert a patch
```

--- 

## Threads / Processes
```bash
info threads # list all threads
thread [num]  # switch to a specific thread
attach PID # attach gdb to a process running
kill # kill the debugger process
```

--- 

## pwndbg utility
```bash
pwndbg  # list all pwndbg commands
config # show or change pwndbg settings
theme # change theme
reload # reload pwndbg
version # yk what it is
```

--- 
