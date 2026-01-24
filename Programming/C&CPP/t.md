## 3.4.1 Function Call Mechanics

Function call mechanics refer to how the execution flow, parameters, return values, and the stack are managed during function calls. These are crucial to understanding performance, optimizations, and debugging.

### 3.4.1.1 Function Prologue and Epilogue

The **function prologue** and **function epilogue** are sequences of assembly instructions executed at the beginning and the end of a function, respectively. They handle the setup and cleanup tasks for function execution.

---
#### 3.4.1.1.1 Function Prologue

The prologue is responsible for preparing the function's environment before the body of the function is executed.

* **Save registers** that need to be preserved (e.g., callee-saved registers).
* **Push the return address** and **frame pointer** onto the stack.
* **Allocate space for local variables** by adjusting the stack pointer.

Example:

```asm
function_prologue:
    push ebp               ; Save the base pointer (old frame pointer)
    mov ebp, esp           ; Set up the new frame pointer
    sub esp, 16            ; Allocate space for local variables
```

---
#### 3.4.1.1.2 Function Epilogue

The epilogue is responsible for cleaning up the function's environment before returning control to the calling function.

* **Restore registers** that were saved.
* **Deallocate local variables** by resetting the stack pointer.
* **Return the function's result**, if applicable, and return control to the caller.

Example:

```asm
function_epilogue:
    mov esp, ebp           ; Restore the stack pointer
    pop ebp                ; Restore the base pointer
    ret                    ; Return control to the caller
```

---
### 3.4.1.2 Parameter Passing (Registers vs Stack)

Function parameters can be passed to a function via **registers** or the **stack**. The method of passing parameters depends on the calling convention used by the compiler.

---
#### 3.4.1.2.1 Passing Parameters via Registers

* **Registers** are faster than the stack because they are directly accessible.
* Typically, **first few parameters** are passed in registers.
* Common calling conventions (e.g., **cdecl, stdcall**) define which registers are used.

Example (x86 Calling Convention):

```cpp
int add(int a, int b) {
    return a + b;
}

// On the calling side, the parameters `a` and `b` would typically be passed in registers like `eax` or `ecx`.
```

---
#### 3.4.1.2.2 Passing Parameters via Stack

* If there are **too many parameters** to fit in registers, the compiler will pass the remaining parameters on the stack.
* The **stack** is used to maintain function call consistency (i.e., calling conventions).

Example:

```asm
push 4        ; Pass the first parameter (4)
push 3        ; Pass the second parameter (3)
call add      ; Call the function
```

---
### 3.4.1.3 Return Value Conventions

Function return values are returned using a specific register or memory location, depending on the platform and calling convention.

#### 3.4.1.3.1 Return Value in Registers

* In **x86 systems**, the return value is commonly stored in the **EAX** register.
* In **x86-64**, the return value is typically stored in **RAX**.

Example:

```cpp
int add(int a, int b) {
    return a + b;  // The return value is stored in RAX/EAX register
}
```

---
#### 3.4.1.3.2 Return Value in Memory

If the return value is large (e.g., a large struct or class), it may be passed via memory rather than in a register.

* **Pointers to structures** are returned in registers, and the caller is responsible for allocating memory.
* **Pass-by-reference** (e.g., `T&`) is commonly used for larger objects.

---
### 3.4.1.4 Stack Cleanup Responsibility

The stack cleanup responsibility refers to who "cleans up" the function's stack frame once the function execution is complete.

---
#### 3.4.1.4.1 Caller Cleanup

In **cdecl** calling convention, the caller is responsible for cleaning the stack after a function call.

* The caller must adjust the stack pointer after the function returns.
* This is done by removing the parameters that were pushed to the stack.

Example:

```asm
call function
add esp, 8    ; Clean up the stack by adjusting the stack pointer (removing parameters)
```

---
#### 3.4.1.4.2 Callee Cleanup

In **stdcall** and **fastcall** calling conventions, the callee is responsible for cleaning up the stack before returning.

* This ensures that the callee removes the parameters from the stack at the end of the function.
* The return address is automatically adjusted during the function return.

Example (stdcall):

```asm
call function
; After function returns, the callee cleans up the stack.
```

---
#### 3.4.1.4.3 Points of Failure

1. **Mismatched Calling Conventions**:

   * If the caller and callee use different calling conventions, it can lead to stack corruption, which may result in crashes or undefined behavior.
   * **Tip**: Always ensure that the calling convention is consistent across the program. If using a compiler, you can specify this with keywords like `__cdecl` or `__stdcall`.

2. **Stack Overflow**:

   * This occurs if there are too many function calls (deep recursion) or large local variables allocated on the stack, causing the stack pointer to exceed the stack's boundary.
   * **Tip**: Avoid deep recursion or large arrays on the stack. Use heap memory for large data structures if necessary.

3. **Register Clobbering**:

   * If the function does not correctly save the registers it uses, it could accidentally overwrite important data in registers that the caller expects to be preserved.
   * **Tip**: Use the proper calling convention and save callee-saved registers when needed.

4. **Improper Stack Cleanup**:

   * If the caller and callee disagree on who should clean up the stack, it can cause stack corruption, leading to crashes.
   * **Tip**: Make sure you're following the conventions for stack cleanup as defined by the calling convention (e.g., **cdecl** vs **stdcall**).

---
### 3.4.1.5 Key Tips & Tricks


1. **Stack Alignment**: In modern 64-bit systems, the stack must be aligned to 16 bytes for optimal performance. Ensure that all function calls respect this alignment to avoid crashes.

2. **Inline Functions**: If you want to avoid the overhead of function calls, use **inline functions** for small, frequently called functions. These functions will be expanded in place, reducing call overhead.

```cpp
inline int add(int a, int b) {
    return a + b;
}
```


3. **Tail Recursion**: If the last action in a function is a recursive call, the compiler can optimize it into a **tail call**, which does not add to the call stack, avoiding stack overflow.

```cpp
int factorial(int n, int acc = 1) {
    if (n <= 1) return acc;
    return factorial(n - 1, n * acc);  // Tail recursion
}
```

4. **Optimizing Parameter Passing**: Pass small objects (like ints or pointers) by value. Large objects (like classes or structs) should be passed by reference or pointer to avoid unnecessary copies.
---
