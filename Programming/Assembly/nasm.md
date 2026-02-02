nasm(netwide assembler)
# key concepts
- uses intel syntax (destination, source)
- no use of register prefix
- size specifiers

```asm
;mov 32 bit
mov eax, 5
;16 bit mov
mov ax, 5
```

- comments `;this is a comment`
- sections

```asm
;global mark symbols visible outside the file
global _start
;section to switch between sections
section .data
```

- directives to define data

``
db define byte
dw define word
dd define double
dq define quad word
``

- define constants in nasm using 

`PI equ 3.14`

- macros in nasm

```asm 
%macro print_string 1
    mov rax, 1          ; syscall number for sys_write
    mov rdi, 1          ; file descriptor (stdout)
    mov rsi, %1         ; address of the string (first argument)
    mov rdx, 13         ; length of the string
    syscall
%endmacro
section .data
message db 'Hello, World!', 0x0A

section .text
global _start

_start:
    print_string message  ; Use the macro to print the string

    ; Exit program
    mov rax, 60          ; syscall number for sys_exit
    xor rdi, rdi         ; exit code 0
    syscall
```

