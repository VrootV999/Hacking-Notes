
# Basic Features of PC Hardware
- Word: a 2-byte data item  
- Doubleword: a 4-byte (32 bit) data item  
- Quadword: an 8-byte (64 bit) data item
-  Paragraph: a 16-byte (128 bit) area 
-  Kilobyte: 1024 bytes
-  Megabyte: 1,048,576 bytes

| Decimal number | Binary representation | Hexadecimal representation |
| -------------- | --------------------- | -------------------------- |
| 0              | 0                     | 0                          |
| 1              | 1                     | 1                          |
| 2              | 10                    | 2                          |
| 3              | 11                    | 3                          |
| 4              | 100                   | 4                          |
| 5              | 101                   | 5                          |
| 6              | 110                   | 6                          |
| 7              | 111                   | 7                          |
| 8              | 1000                  | 8                          |
| 9              | 1001                  | 9                          |
| 10             | 1010                  | A                          |
| 11             | 1011                  | B                          |
| 12             | 1100                  | C                          |
| 13             | 1101                  | D                          |
| 14             | 1110                  | E                          |
| 15             | 1111                  | F                          |


| i   | ii  | iii | iv  |
| --- | --- | --- | --- |
|     |     |     | 1   |
| 0   | 1   | 1   | 1   |
| +0  | +0  | +1  | +1  |
| =0  | =0  | =10 | =11 |


```assembly
section .text  
    global main 
main:

;declare constant and variable
; static

section .data

;declare variables
;they aren't static and can be ;modified in runtime

section .bss 

```

## Syntax of Assembly Language Statements

```assembly
[label] mnemonic [operands] [;comment]
```

## Syscalls

[[x86_32_syscalls]]
[[x86_syscalls]]
[[aarch64_syscalls]]

## Data size

| Type specifier | Bytes addressed |
| -------------- | --------------- |
| BYTE           | 1               |
| WORD           | 2               |
| DWORD          | 4               |
| QWORD          | 8               |
| TWORD          | 10              |

## Variable Storage Space

| Directive | Purpose            | Storage space |
| --------- | ------------------ | ------------- |
| DB        | Define Byte        | 1 byte        |
| DW        | Define word        | 2 byte        |
| DD        | Define double word | 4 byte        |
| DQ        | Define quad word   | 8 byte        |
| DT        | Define ten bytes   | 10 byte       |

## Allocating Storage Space for Uninitialized Data


| Directive | Purpose          |
| --------- | ---------------- |
| RESB      | Reserve a byte   |
| RESW      | Reserve 2 bytes  |
| RESD      | Reserve 4 bytes  |
| RESQ      | Reserve 8 bytes  |
| REST      | Reserve 10 bytes |

```assembly

choice  DB 'Y'  
;ASCII of y = 79H 

number1 DW 12345  
;12345D = 3039H 

number2 DD 12345679 
;123456789D = 75BCD15H

stars times 9 db '*'
; the stars has the value *********


```


#### equ directive
```
TOTAL_STUDENTS equ 50

;a constant called total_students
```

#### %assign

```assembly
%assign TOTAL 10

;a numeric constant called total
```

#### %define
```assembly
%define PTR [EBP+4]

;a numeric or string constant called ptr
```


### Assembly Instructions 
