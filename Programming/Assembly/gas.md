GAS (GNU Assembler)
# 1. Key concepts
- uses AT&T syntax (1st source, 2nd destination)
- registers are prefixed with %
- immediate values are prefixed with $
- comments `#this is a comment`
- There are some common directives like `.data .text .global`
```asm
#global is used to declare global functions and variables
.global _start
#.section directive is used to switch between sections
.section .data
#set syntax to intel
.intel_syntax noprefix
#.byte .word .long .quad are used to define variable with specific size
.word 0x123
#asciz is used for writing null terminated strings
.asciz "Hello world"
```
- syscalls are invoked through registers
- GAS macros 
```asm 
    .macro print_string str
        mov rax, 1         # syscall number for sys_write
        mov rdi, 1         # file descriptor (stdout)
        mov rsi, str       # pointer to the string
        mov rdx, 13        # length of the string
        syscall
    .endm
    .global _start
    .text

_start:
    print_string message 
    # Use the macro to print the string

    # Exit program
    mov rax, 60         # syscall number for sys_exit
    xor rdi, rdi        # exit code 0
    syscall

section .data
message:
    .asciz "Hello, World!"  # The message to print

```
- symbolic debuggins(used with gdb)
`as -g program.s -o program.o`
- local labels (temporary jump targets)
```asm 
    jmp L0
L1:
    # some code
    jmp L0
L0:
    # code here
```
- directives used to define data in gas 
`` 
b (8 bit)  1 byte
w (16 bit) 2 bytes
l (32 bit) 4 bytes
q (64 bit) 8 bytes
``

- Compiling using gcc
```bash
#compiler
gcc -c file.s -o file.o
#link using gcc
gcc file.o -o file
#convert c file into a asm
gcc -S file.c -o file.s
#specify syntax and verbose comment
gcc -S -masm=intel -fverbose-asm -o file.s file.c
#assembly with source code info and debug annotation
gcc -S -g -Wa,-adhln -fverbose-asm -o file.s file.c
```

---
