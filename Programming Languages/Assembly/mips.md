# Registers
32bit registers 
| registers | usage | 
| ---- | ---- |
| Generic  |  |
| $zero | 0 |
| $t0-t9 |  Temporary Registers caller saved |
| Reserved | |
| $at | assembler temporary |
| $k0-$k1 | kernel registers |
| Functions | |
| $v0-$v1 |  Return Values |
| $a0-$a3 | Arguments registers |
| $s0-$s7 | Saved registers Callee saved |
| Memory |  |
| $sp | stack pointer |
| $fp | frame pointer |
| $gp | global pointer |

---
# syscall
same yk ofc, make calls to kernel to do I/O operations frequently

$v0     Operation number
$a0-a3  Operation parameters
$v0     Results

Syscall flow in MIPS
- Load the Service Code: Put the operation ID into $v0.
- Load Arguments: Place input values into the argument registers (starting at $a0).
- Execute: Call the syscall instruction.
- Retrieve Results: If the call returns a value (like reading an integer), it is typically placed in $v0.

Syscall table
visit `https://gpages.juszkiewicz.com.pl/syscalls-table/syscalls.html` for all the syscall available for all architectures

---
# All instructions

## Arithmetic

| Instruction         | Parameters                                         | Functionality + Example                               |
| ------------------- | -------------------------------------------------- | ----------------------------------------------------- |
| `add rd, rs, rt`    | `rd=dest`, `rs/src1`, `rt/src2`                    | Add with overflow trap → `add $t0, $t1, $t2`          |
| `addi rt, rs, imm`  | `rt=dest`, `rs=src`, `imm=16-bit signed immediate` | Add immediate → `addi $t0, $t1, 10`                   |
| `addu rd, rs, rt`   | `rd=dest`, `rs/src1`, `rt/src2`                    | Unsigned add → `addu $t0, $t1, $t2`                   |
| `addiu rt, rs, imm` | `rt=dest`, `rs=src`, `imm=signed immediate`        | Add immediate unsigned → `addiu $sp, $sp, -0x20`      |
| `sub rd, rs, rt`    | `rd=dest`, `rs/src1`, `rt/src2`                    | Signed subtract → `sub $t0, $t1, $t2`                 |
| `subu rd, rs, rt`   | `rd=dest`, `rs/src1`, `rt/src2`                    | Unsigned subtract → `subu $t0, $t1, $t2`              |
| `mult rs, rt`       | `rs=src1`, `rt=src2`                               | Signed multiply → result in `HI/LO` → `mult $t0, $t1` |
| `multu rs, rt`      | `rs=src1`, `rt=src2`                               | Unsigned multiply → `multu $t0, $t1`                  |
| `div rs, rt`        | `rs=numerator`, `rt=denominator`                   | Signed divide → `div $t0, $t1`                        |
| `divu rs, rt`       | `rs=numerator`, `rt=denominator`                   | Unsigned divide → `divu $t0, $t1`                     |
| `mfhi rd`           | `rd=dest`                                          | Move from `HI` → `mfhi $t0`                           |
| `mflo rd`           | `rd=dest`                                          | Move from `LO` → `mflo $t0`                           |
| `mthi rs`           | `rs=source`                                        | Move to `HI` → `mthi $t0`                             |
| `mtlo rs`           | `rs=source`                                        | Move to `LO` → `mtlo $t0`                             |


## Logical and Bitwise Instructions
| Instruction        | Parameters                                         | Functionality + Example                  |
| ------------------ | -------------------------------------------------- | ---------------------------------------- |
| `and rd, rs, rt`   | `rd=dest`, `rs/src1`, `rt/src2`                    | Bitwise AND → `and $t0, $t1, $t2`        |
| `andi rt, rs, imm` | `rt=dest`, `rs=src`, `imm=zero-extended immediate` | AND immediate → `andi $t0, $t1, 0xFF`    |
| `or rd, rs, rt`    | `rd=dest`, `rs/src1`, `rt/src2`                    | Bitwise OR → `or $t0, $t1, $t2`          |
| `ori rt, rs, imm`  | `rt=dest`, `rs=src`, `imm=immediate`               | OR immediate → `ori $t0, $t1, 0x1000`    |
| `xor rd, rs, rt`   | `rd=dest`, `rs/src1`, `rt/src2`                    | Bitwise XOR → `xor $t0, $t1, $t2`        |
| `xori rt, rs, imm` | `rt=dest`, `rs=src`, `imm=immediate`               | XOR immediate → `xori $t0, $t1, 1`       |
| `nor rd, rs, rt`   | `rd=dest`, `rs/src1`, `rt/src2`                    | Bitwise NOR → `nor $t0, $t1, $zero`      |
| `lui rt, imm`      | `rt=dest`, `imm=upper 16 bits`                     | Load upper immediate → `lui $t0, 0x1234` |


## Shift Instructions

| Instruction         | Parameters                                | Functionality + Example                                |
| ------------------- | ----------------------------------------- | ------------------------------------------------------ |
| `sll rd, rt, shamt` | `rd=dest`, `rt=src`, `shamt=shift amount` | Shift left logical → `sll $t0, $t1, 2`                 |
| `srl rd, rt, shamt` | `rd=dest`, `rt=src`, `shamt=shift amount` | Shift right logical → `srl $t0, $t1, 1`                |
| `sra rd, rt, shamt` | `rd=dest`, `rt=src`, `shamt=shift amount` |  Shift right arithmetic  → `sra $t0, $t1, 1`             |
| `sllv rd, rt, rs`   | `rd=dest`, `rt=value`, `rs=shift count`   | Variable left shift → `sllv $t0, $t1, $t2`             |
| `srlv rd, rt, rs`   | `rd=dest`, `rt=value`, `rs=shift count`   | Variable logical right shift → `srlv $t0, $t1, $t2`    |
| `srav rd, rt, rs`   | `rd=dest`, `rt=value`, `rs=shift count`   | Variable arithmetic right shift → `srav $t0, $t1, $t2` |


## Comparison Instructions

| Instruction         | Parameters                               | Functionality + Example                           |
| ------------------- | ---------------------------------------- | ------------------------------------------------- |
| `slt rd, rs, rt`    | `rd=dest`, `rs=lhs`, `rt=rhs`            | (set on less than)Set if `rs < rt` signed → `slt $t0, $t1, $t2`     |
| `sltu rd, rs, rt`   | `rd=dest`, `rs=lhs`, `rt=rhs`            | Unsigned compare → `sltu $t0, $t1, $t2`           |
| `slti rt, rs, imm`  | `rt=dest`, `rs=lhs`, `imm=rhs immediate` | Compare immediate signed → `slti $t0, $t1, 10`    |
| `sltiu rt, rs, imm` | `rt=dest`, `rs=lhs`, `imm=rhs immediate` | Compare immediate unsigned → `sltiu $t0, $t1, 10` |


## Branch & Jump Instructions
| Instruction         | Parameters                                | Functionality + Example                    |
| ------------------- | ----------------------------------------- | ------------------------------------------ |
| `beq rs, rt, label` | `rs=lhs`, `rt=rhs`, `label=branch target` | Branch if equal → `beq $t0, $t1, done`     |
| `bne rs, rt, label` | `rs=lhs`, `rt=rhs`, `label=branch target` | Branch if not equal → `bne $t0, $t1, fail` |
| `blez rs, label`    | `rs=value`, `label=branch target`         | Branch if `rs <= 0` → `blez $t0, end`      |
| `bgtz rs, label`    | `rs=value`, `label=branch target`         | Branch if `rs > 0` → `bgtz $t0, loop`      |
| `bltz rs, label`    | `rs=value`, `label=branch target`         | Branch if `rs < 0` → `bltz $t0, neg`       |
| `j target`          | `target=absolute jump address/label`      | Unconditional jump → `j main`              |
| `jal target`        | `target=function label/address`           | Jump and link → `jal printf`               |
| `jr rs`             | `rs=jump target register`                 | Jump register → `jr $ra`                   |
| `jalr rd, rs`       | `rd=link register`, `rs=target register`  | Indirect call → `jalr $ra, $t9`            |


## Load and Store Instructions

| Instruction            | Parameters                                             | Functionality + Example                    |
| ---------------------- | ------------------------------------------------------ | ------------------------------------------ |
| `lw rt, offset(base)`  | `rt=dest`, `base=base addr reg`, `offset=displacement` | Load word → `lw $t0, 0($sp)`               |
| `lh rt, offset(base)`  | `rt=dest`, `base=addr reg`, `offset=displacement`      | Load signed halfword → `lh $t0, 2($sp)`    |
| `lhu rt, offset(base)` | `rt=dest`, `base=addr reg`, `offset=displacement`      | Load unsigned halfword → `lhu $t0, 2($sp)` |
| `lb rt, offset(base)`  | `rt=dest`, `base=addr reg`, `offset=displacement`      | Load signed byte → `lb $t0, 0($a0)`        |
| `lbu rt, offset(base)` | `rt=dest`, `base=addr reg`, `offset=displacement`      | Load unsigned byte → `lbu $t0, 0($a0)`     |
| `sw rt, offset(base)`  | `rt=source`, `base=addr reg`, `offset=displacement`    | Store word → `sw $ra, 0x1c($sp)`           |
| `sh rt, offset(base)`  | `rt=source`, `base=addr reg`, `offset=displacement`    | Store halfword → `sh $t0, 2($sp)`          |
| `sb rt, offset(base)`  | `rt=source`, `base=addr reg`, `offset=displacement`    | Store byte → `sb $t0, 0($a0)`              |


## Misc Instructions

| Instruction  | Parameters                 | Functionality + Example             |
| ------------ | -------------------------- | ----------------------------------- |
| `syscall`    | none                       | Trigger syscall handler → `syscall` |
| `nop`        | none                       | No operation → `nop`                |
| `break code` | `code=optional debug code` | Breakpoint trap → `break 1`         |


## Common pseudoInstructions (Syntatic Sugar)

| Instruction      | Parameters                        | Functionality + Example                  |
| ---------------- | --------------------------------- | ---------------------------------------- |
| `li rt, imm`     | `rt=dest`, `imm=value`            | Load immediate → `li $t0, 0x1337`        |
| `la rt, label`   | `rt=dest`, `label=symbol address` | Load address → `la $a0, msg`             |
| `move rd, rs`    | `rd=dest`, `rs=source`            | Register copy → `move $t0, $t1`          |
| `b label`        | `label=branch target`             | Unconditional branch → `b loop`          |
| `mul rd, rs, rt` | `rd=dest`, `rs/src1`, `rt/src2`   | Multiply pseudo-op → `mul $t0, $t1, $t2` |

---

