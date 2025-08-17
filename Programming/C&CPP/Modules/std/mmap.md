## **5. `mmap.h` (Memory Mapping)**

The **`mmap`** function provides a way to map files or devices into memory, enabling processes to directly read from or write to specific memory regions. It’s an extremely powerful tool, especially when dealing with **buffer overflows**, **heap spraying**, or **code injection**. Understanding how `mmap()` works is crucial for executing **arbitrary code**, **bypassing security mechanisms**, and performing **advanced memory-related exploits**.

---

### **Key Functions and Concepts in `mmap.h`**

1. **`mmap()`**

   * **Purpose**: Maps files or devices into memory, creating a memory-mapped region that can be used for file I/O or process-to-process communication.
   * **Common Use**: Memory-mapped files are useful for reading or writing data to files without using traditional file I/O operations. It’s also used to map devices directly into memory.
   * **Example**:

     ```c
     void *addr = mmap(NULL, length, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
     if (addr == MAP_FAILED) {
       perror("mmap failed");
       exit(1);
     }
     ```

2. **`munmap()`**

   * **Purpose**: Unmaps a memory region that was previously mapped with `mmap()`.
   * **Common Use**: Once the memory mapping is no longer needed, `munmap()` is used to release the allocated memory.
   * **Example**:

     ```c
     if (munmap(addr, length) == -1) {
       perror("munmap failed");
       exit(1);
     }
     ```

3. **Memory Protection Flags**

   * **PROT\_READ**: Pages can be read.
   * **PROT\_WRITE**: Pages can be written.
   * **PROT\_EXEC**: Pages can be executed.
   * **PROT\_NONE**: Pages cannot be accessed.
   * **MAP\_PRIVATE**: Changes are private to the process and not reflected in the underlying file.
   * **MAP\_ANONYMOUS**: Mapping is not backed by any file, often used for creating anonymous memory regions.
   * **MAP\_SHARED**: Changes are shared with other processes that map the same file.
   * **MAP\_FIXED**: This flag forces the system to place the mapping at the specified address.

   These flags are particularly important for setting up memory regions that can be used for **code injection** or **buffer overflows**, and controlling the **read**, **write**, and **execution** access to the memory.

---

### **Advanced Use Cases for `mmap.h` in Penetration Testing & Red Teaming**

#### **1. Exploiting Memory with `mmap()` for Code Injection**

**Objective**: Use `mmap()` to allocate memory that is both **readable** and **executable**, allowing you to inject and execute arbitrary code, bypassing security mechanisms like **non-executable stack** (NX) and **data execution prevention** (DEP).

##### **Technique**:

* In modern systems, security mechanisms like **NX** bit and **DEP** are designed to prevent code from executing in certain memory regions. However, by using `mmap()` with the `PROT_READ | PROT_WRITE | PROT_EXEC` flags, you can create a **read-write-execute memory region** and inject shellcode directly into that region.

```c
void *addr = mmap(NULL, shellcode_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
if (addr == MAP_FAILED) {
    perror("mmap failed");
    exit(1);
}
memcpy(addr, shellcode, shellcode_size);
((void(*)())addr)();  // Execute the shellcode
```

* **Real-World Use Case**: After exploiting a vulnerability like a **buffer overflow**, you can use `mmap()` to allocate executable memory and inject **shellcode** to get a **reverse shell** or execute arbitrary commands.

---

#### **2. Heap Spraying with `mmap()`**

**Objective**: Use `mmap()` to allocate multiple **memory regions** for **heap spraying** attacks, a technique used to overwrite important function pointers or return addresses with **shellcode**.

##### **Technique**:

* **Heap spraying** involves allocating large numbers of memory regions (often through `mmap()`), and filling these regions with **payloads** or **shellcode**. By spraying the heap with **malicious content**, you increase the chances of **memory corruption** that will allow you to redirect execution to your injected payload.
* You can create memory regions at **specific addresses** and fill them with **NOP sleds** or **shellcode**. If the target application has a memory corruption vulnerability, the goal is to **control the program's execution flow** by redirecting it to one of these regions.

```c
for (int i = 0; i < 100; i++) {
    void *addr = mmap(NULL, shellcode_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (addr == MAP_FAILED) {
        perror("mmap failed");
        exit(1);
    }
    memcpy(addr, shellcode, shellcode_size);
}
```

* **Real-World Use Case**: In a **heap overflow** scenario, an attacker could use `mmap()` to create **multiple shellcode regions** in memory, hoping to trigger one of them with a corrupt function pointer or buffer overflow.

---

#### **3. Bypassing ASLR (Address Space Layout Randomization) with `mmap()`**

**Objective**: Allocate memory at predictable addresses to bypass **ASLR**, a security feature designed to randomize the memory layout of processes.

##### **Technique**:

* **ASLR** randomizes the memory addresses of process segments (e.g., stack, heap, libraries) to prevent attackers from exploiting predictable addresses. However, using `mmap()` with the **`MAP_FIXED`** flag allows you to **force a specific memory address** for the mapping. This can help bypass ASLR if the attacker can predict the address.

```c
void *addr = mmap((void *)0xdeadbeef, shellcode_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS | MAP_FIXED, -1, 0);
if (addr == MAP_FAILED) {
    perror("mmap failed");
    exit(1);
}
memcpy(addr, shellcode, shellcode_size);
((void(*)())addr)();  // Execute the shellcode
```

* **Real-World Use Case**: In a scenario where **ASLR** is enabled, an attacker can use `mmap()` with `MAP_FIXED` to inject **shellcode** at a known memory address, bypassing ASLR and executing the payload.

---

#### **4. Memory Corruption Exploits with `mmap()` and ROP (Return-Oriented Programming)**

**Objective**: Leverage `mmap()` to set up **ROP chains** in memory for **arbitrary code execution**.

##### **Technique**:

* **ROP** allows attackers to execute arbitrary code by chaining together **existing code snippets** (gadgets) in the process's memory. By using `mmap()`, an attacker can **allocate executable memory** to store **ROP chains** or **gadget sequences**, and then manipulate the program's control flow to execute the chain.

```c
void *addr = mmap(NULL, rop_chain_size, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
if (addr == MAP_FAILED) {
    perror("mmap failed");
    exit(1);
}
memcpy(addr, rop_chain, rop_chain_size);
((void(*)())addr)();  // Execute the ROP chain
```

* **Real-World Use Case**: After identifying a **buffer overflow** vulnerability, an attacker can inject a **ROP chain** into memory using `mmap()` and gain **arbitrary code execution** without needing to directly inject shellcode.

---
