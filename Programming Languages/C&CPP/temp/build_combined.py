#!/usr/bin/env python3
"""
Build script to create cppfinal_combined.md from cppfinal.md template.
Fills empty sections with researched content and appends new sections.
"""

import re
import os

BASE_DIR = "/home/anon/Documents/Notes/Hacking_Notes/Programming Languages/C&CPP"
TEMPLATE = os.path.join(BASE_DIR, "cppfinal.md")
OUTPUT = os.path.join(BASE_DIR, "cppfinal_combined.md")

# All content fillers - organized by section number
# Key format: "X.Y.Z" matches the heading number

content = []

# We'll read the template and process it
with open(TEMPLATE, 'r') as f:
    lines = f.readlines()

# Build a map of line numbers to section identifiers
# Format: line_num -> section_id (e.g., "4.4.1.1")
def extract_section_id(line):
    """Extract section ID from a heading line."""
    match = re.match(r'^(#{1,6})\s+(\d+(?:\.\d+)*)\s+(.*)$', line.strip())
    if match:
        return match.group(2), match.group(3), len(match.group(1))
    return None, None, None

# Parse sections with their content boundaries
sections = []
for i, line in enumerate(lines):
    sid, title, level = extract_section_id(line)
    if sid:
        sections.append({
            'line_index': i,
            'section_id': sid,
            'title': title,
            'level': level,
            'heading_line': line.rstrip('\n')
        })

# Content for each section that needs filling
# Organized as: "section_id" -> "content text"
CONTENT = {
    # Chapter 1: Core Language Fundamentals
    "1.1.3.1": """`std::uint8_t` is a fixed-width unsigned 8-bit integer type from `<cstdint>`.

```cpp
#include <cstdint>
std::uint8_t byte = 0xFF;  // exactly 8 bits, value 255
std::uint8_t arr[4] = {0x48, 0x65, 0x6c, 0x6c}; // "Hell" as bytes
```

- Guarantees: exactly 8 bits, unsigned, no padding bits
- Header: `<cstdint>`
- Critical for: shellcode crafting, byte-exact binary serialization, hardware register manipulation
- Contrast with `char` (may be signed/unsigned, implementation-defined)

---""",

    "1.1.3.2": """`std::uintptr_t` is an unsigned integer type large enough to hold any pointer value, from `<cstdint>`.

```cpp
#include <cstdint>
void* ptr = malloc(64);
std::uintptr_t addr = reinterpret_cast<std::uintptr_t>(ptr);
std::uintptr_t offset = addr - 0x1000;

// Arithmetic with uintptr_t is well-defined (unlike pointer arithmetic on void*)
std::uintptr_t next = addr + sizeof(void*);
```

- Guarantees: unsigned, can hold any object pointer without loss
- Header: `<cstdint>`
- Use case: pointer-to-integer casts without undefined behavior, computing memory offsets, hash tables keyed on pointers
- Note: `uintptr_t` is optional; `std::uintptr_t` from `<cstdint>` is guaranteed if the type exists

---""",

    # 1.2.4 Enums (the whole subsection needs content)
    "1.2.4.1": """**Enum Basics**

C++ supports two kinds of enumerations:

```cpp
// Traditional (C-style) enum — implicit conversions to/from int
enum Color { RED, GREEN, BLUE };
Color c = RED;       // c == 0
int x = c;           // implicit conversion: x == 0 — dangerous!
Color y = 5;         // implicit conversion: OK but UB (no checking)

// Scoped enum (C++11) — strongly typed, no implicit conversions
enum class Direction { North, South, East, West };
Direction d = Direction::North;
// int z = d;         // ERROR: no implicit conversion
int z = static_cast<int>(d);  // explicit cast required
```

Key differences:

| Feature | Traditional `enum` | Scoped `enum class` |
|---|---|---|
| Implicit int conversion | Yes (unsafe) | No (safe) |
| Scope leakage | Yes (`RED` in global scope) | No (`Direction::North`) |
| Forward declaration | No (needs fixed underlying type) | No (needs fixed underlying type) |
| Default underlying type | `int` | `int` (but explicitly specified) |

---""",

    "1.2.4.2.1": """`std::underlying_type` is a type trait from `<type_traits>` that yields the underlying type of an enum.

```cpp
#include <iostream>
#include <type_traits>

enum class Color : std::uint8_t { Red = 0, Green = 1, Blue = 2 };

// Get the underlying type
using Underlying = std::underlying_type_t<Color>;  // std::uint8_t

Underlying val = static_cast<Underlying>(Color::Green);  // 1
std::cout << static_cast<int>(val) << "\\n";  // prints 1

// Useful with switch or arithmetic on enum values
switch (val) {
    case 0: /* ... */
    case 1: /* ... */
}
```

- Header: `<type_traits>`
- `std::underlying_type<T>::type` (pre-C++14), `std::underlying_type_t<T>` (C++14+)
- Used for enum arithmetic, switch statements on enum values, interoperability with C APIs

---""",

    "1.2.4.2.2": """`std::to_underlying()` converts an enum to its underlying type (C++23).

```cpp
#include <iostream>
#include <type_traits>  // for to_underlying (C++23)

enum class Status : int { OK = 200, NotFound = 404, ServerError = 500 };

// C++23: clean conversion
int code = std::to_underlying(Status::OK);  // 200
int code2 = std::to_underlying(Status::NotFound);  // 404

// Pre-C++23 alternative:
using Underlying = std::underlying_type_t<Status>;
int code3 = static_cast<Underlying>(Status::ServerError);  // 500
```

- Header: `<type_traits>` (C++23)
- Simplifies enum-to-int conversion; avoids verbose `static_cast` boilerplate
- Works with any enumeration type (traditional and scoped)

---""",

    "1.2.4.3": """**Enum Bitfields (Flags)**

A common pattern is using enums as bit flags. In modern C++, this is done with a scoped enum and overloaded bitwise operators:

```cpp
#include <cstdint>

enum class FileAccess : std::uint8_t {
    None    = 0,
    Read    = 1 << 0,   // 1
    Write   = 1 << 1,   // 2  
    Execute = 1 << 2    // 4
};

// Overload bitwise operators for enum class (C++11+)
constexpr FileAccess operator|(FileAccess a, FileAccess b) {
    return static_cast<FileAccess>(
        static_cast<std::uint8_t>(a) | static_cast<std::uint8_t>(b)
    );
}

constexpr FileAccess operator&(FileAccess a, FileAccess b) {
    return static_cast<FileAccess>(
        static_cast<std::uint8_t>(a) & static_cast<std::uint8_t>(b)
    );
}

constexpr bool operator!(FileAccess a) {
    return !static_cast<std::uint8_t>(a);
}

// Usage
FileAccess perms = FileAccess::Read | FileAccess::Write;
if (perms & FileAccess::Execute) {
    // not set — skips
}

// C++20: `std::bitset` or `<bit>` helpers
// C++23: `std::bit_cast` or `std::format` with enums for readable output
```

For pre-C++11 code, traditional enums were used directly:
```cpp
enum FileFlags { READ = 1, WRITE = 2, EXECUTE = 4 };
int perms = READ | WRITE;  // int, not type-safe
```

---""",

    "1.2.4.4": """**Comparison: Regular Enum vs Enum Class**

| Aspect | Regular `enum` | `enum class` |
|---|---|---|
| Implicit conversion to int | Yes (risky) | No (safe) |
| Implicit conversion from int | Yes (risky) | No (safe) |
| Namespace scoping | Names leak to enclosing scope | Scoped to enum name |
| Forward declaration | Requires fixed underlying type in C++11 | Requires fixed underlying type |
| Size control | Implementation-defined | Explicitly controllable |

```cpp
// Regular enum: name pollution
enum Color { Red, Green, Blue };
// Green is now visible in this scope — potential clash

// Enum class: clean scoping
enum class Color2 { Red, Green, Blue };
// Only visible as Color2::Green — no pollution

// Regular enum can be compared with int
enum Color c = Red;
if (c == 0) { /* works but fragile */ }

// Enum class requires explicit cast
enum class Color2 c2 = Color2::Green;
if (c2 == Color2::Red) { /* type-safe */ }
// if (c2 == 0) { /* ERROR */ }
```

Recommendation: Prefer `enum class` unless interfacing with C code or needing implicit conversions.

---""",

    # Chapter 1.3.2 Operators
    "1.3.2.1": """**Arithmetic Operators**

| Operator | Description |
|---|---|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division (truncates toward zero for integers) |
| `%` | Modulus (remainder) |
| `++` | Increment |
| `--` | Decrement |

```cpp
#include <iostream>

int a = 10, b = 3;
std::cout << a + b << "\\n";   // 13
std::cout << a - b << "\\n";   // 7
std::cout << a * b << "\\n";   // 30
std::cout << a / b << "\\n";   // 3 (integer division)
std::cout << a % b << "\\n";   // 1 (remainder)
std::cout << a++ << "\\n";     // 10 (post-increment: uses then increments)
std::cout << ++b << "\\n";     // 4 (pre-increment: increments then uses)
```

Note: `++`/`--` on `bool` is deprecated in modern C++.

---""",

    # Chapter 2 sections
    "2.2.1": """**Type Conversion**

C++ performs implicit type conversions in expressions. Understanding these is critical for avoiding subtle bugs and security issues.

```cpp
// Implicit conversions (safe and well-defined)
int a = 42;
double b = a;     // int → double: widening, safe
char c = a;       // int → char: narrowing, potential data loss
bool d = a;       // int → bool: non-zero → true

// Dangerous implicit conversion (sign mismatch)
unsigned int x = 10;
int y = -5;
// When compared: if (x + y < 0) — y is converted to unsigned!
// -5 becomes a huge unsigned value, comparison may be wrong

// Float to int: truncation, not rounding
double pi = 3.14159;
int n = pi;     // n == 3, not 4 — data loss!
```

Key rules (rank-based promotion):
1. `bool` → `char` → `signed char` → `short` → `int` → `long` → `long long` → `float` → `double` → `long double`
2. If one operand is `unsigned`, the other is converted to unsigned (potential trap for negative values)
3. Smaller types are promoted to the larger type in a binary operation

See [2.2.2 Casting] for explicit conversion methods.

---""",

    "2.2.2": """**Casting**

Explicit type conversions (casts) in C++:

```cpp
// C-style cast (avoid in modern C++)
int x = 65;
char c = (char)x;           // Works but unsafe — no checks

// C++ named casts — safer, self-documenting, more explicit

// static_cast: for well-defined conversions (same hierarchy or numeric)
int i = 42;
double d = static_cast<double>(i);   // int → double: safe

// reinterpret_cast: for pointer-to-pointer casts (implementation-defined)
int* ip = reinterpret_cast<int*>(0x1000);

// const_cast: to remove or add `const`
const int* ci = &i;
int* nc = const_cast<int*>(ci);    // removes const

// dynamic_cast: for safe polymorphic downcasting (with RTTI)
// Base* bp = ...;
// Derived* dp = dynamic_cast<Derived*>(bp);  // nullptr if not a Derived
```

| Cast | Use Case | Safety |
|---|---|---|
| `static_cast<T>` | Numeric, upcast/downcast in same hierarchy | Checked at compile time |
| `dynamic_cast<T>` | Polymorphic downcast (requires virtual destructor) | Checked at runtime (returns nullptr or throws) |
| `reinterpret_cast<T>` | Low-level pointer reinterpretation | Implementation-defined, risky |
| `const_cast<T>` | Add/remove const/volatile | Can cause UB if modified |
| `std::bit_cast<T>` | Reinterpret bits between same-size types (C++20) | Type-safe replacement for reinterpret_cast/memcpy |
| C-style `(T)x` | Legacy, combines all above | No safety, avoid |

---""",

    "2.2.3": """**Type Casting (Exploit Context)**

In exploit development and reverse engineering, type casting is used to:

1. **Convert between pointer and integer types** to manipulate addresses:
```cpp
void* target = (void*)0xdeadbeef;
int* func_ptr = reinterpret_cast<int*>(target);
```

2. **Type punning** — reinterpret raw bytes as a different type:
```cpp
uint32_t val = 0x41424344;
char* bytes = reinterpret_cast<char*>(&val);  // { 'D', 'C', 'B', 'A' }
```

3. **Vtable manipulation**:
```cpp
// Cast object to its vtable pointer
struct Object { void** vtable; };
Object* obj = (Object*)some_polymorphic_ptr;
void** vptr = obj->vtable;  // now we point to the function table
```

Important considerations:
- `reinterpret_cast` is the only C++ cast that guarantees a pointer-to-integer-to-pointer round-trip preserves the value
- `reinterpret_cast` between function pointers and data pointers is technically undefined but works in practice on most platforms
- For exact bit-level reinterpretation (e.g., building shellcode), prefer `std::bit_cast` (C++20) or `memcpy`

---""",

    # Chapter 3.2.2 Parameters
    "3.2.2": """**Parameters**

Function parameters control how data is passed to functions. In C++:

```cpp
#include <iostream>

// Pass by value (copy)
void byValue(int x) { x = 100; }  // modifies copy only

// Pass by reference (alias)
void byReference(int& x) { x = 100; }  // modifies original

// Pass by const reference (no copy, read-only)
void byConstRef(const std::string& s) { /* read s only */ }

// Pass by rvalue reference (move semantics, C++11)
void byRvalueRef(std::string&& s) { s += " modified"; }

int a = 5;
byValue(a);           // a unchanged
byReference(a);       // a now 100
```

---""",

    "3.2.2.1": """#### 3.2.2.1 Pass by Value

When a parameter is a value type, the argument is **copied** into the parameter.

```cpp
void takeInt(int x) {
    x *= 2;  // only affects the local copy
}

int main() {
    int a = 5;
    takeInt(a);
    // a is still 5 — the copy is lost
}
```

Use when:
- The argument is a primitive type (`int`, `char`, `bool`, etc.) — copying is cheap
- The function needs an independent copy
- The size of copying is negligible

For complex types (e.g., `std::vector`), prefer pass-by-reference.

---""",

    "3.2.2.2": """#### 3.2.2.2 Pass by Reference (&)

A reference is an alias for a variable — no copy is made.

```cpp
void modify(int& ref) {
    ref = 42;  // changes the original variable
}

int main() {
    int x = 10;
    modify(x);  // x is now 42
}
```

References must be initialized and cannot be reseated.
Use when:
- You need to modify the caller's variable
- Passing large objects (e.g., `std::vector`) without copying

---""",

    "3.2.2.3": """#### 3.2.2.3 Default Parameters (Optional args)

Parameters can have default values:

```cpp
void log(const std::string& msg, const std::string& level = "INFO") {
    std::cout << "[" << level << "] " << msg << "\\n";
}

log("System started");            // [INFO] System started
log("Low disk", "WARNING");       // [WARNING] Low disk
```

Rules:
- Defaults must be declared from right to left (once a default is set, all subsequent params must have defaults)
- Cannot have defaults in declaration and definition separately (must be in one place — typically declaration)

---""",

    "3.2.3": """**Function Overloading**

Multiple functions can share the same name if their parameter lists differ (different count, types, or order).

```cpp
#include <iostream>

void print(int x) {
    std::cout << "int: " << x << "\\n";
}

void print(double x) {
    std::cout << "double: " << x << "\\n";
}

void print(const char* x) {
    std::cout << "string: " << x << "\\n";
}

int main() {
    print(5);        // calls print(int)
    print(3.14);     // calls print(double)
    print("hello");  // calls print(const char*)
}
```

The compiler selects the best match through **overload resolution** based on the arguments.

---""",

    "3.2.3.1": """#### 3.2.3.1 Function Overloading (Different parameter types)

C++ allows multiple functions with the same name but different parameter types:

```cpp
// Area of a circle
double area(double r) {
    return 3.14159 * r * r;
}

// Area of a rectangle
double area(double w, double h) {
    return w * h;
}

// Area of a square
double area(int s) {
    return (double)(s * s);
}

// Usage
area(5.0);       // circle: double area(double)
area(3.0, 4.0);  // rectangle: double area(double, double)
area(5);         // square: double area(int)
```

The compiler resolves at compile time based on argument count and type. Return type alone does **not** constitute an overloadable difference.

---""",

    "3.2.3.2": """#### 3.2.3.2 Function Hiding & Overload Resolution

In C++, name lookup in derived classes hides base class names. To expose hidden base class functions, use a `using` declaration:

```cpp
struct Base {
    void foo(int);
};

struct Derived : Base {
    using Base::foo;  // brings Base::foo into Derived's scope
    void foo(double);
};

Derived d;
d.foo(1);    // calls Base::foo(int) — now visible due to using-declaration
d.foo(1.0);  // calls Derived::foo(double)
```

Overload resolution priority:
1. Exact match (no conversion)
2. Promotion (char→int, float→double)
3. Standard conversion (int→double, etc.)
4. User-defined conversion (operator T)
5. Ellipsis (`...`)

If multiple candidates have the same priority, it's **ambiguous** and the compiler errors.

---""",

    "3.2.4": """**Function Pointers**

Functions can be referenced indirectly via pointers.

```cpp
#include <iostream>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int main() {
    // Declare a function pointer
    int (*op)(int, int);
    
    op = add;
    std::cout << op(5, 3) << "\\n";  // 8
    
    op = sub;
    std::cout << op(5, 3) << "\\n";  // 2
}
```

---""",

    "3.2.4.1": """#### 3.2.4.1 Function Pointer Declaration

Syntax: `ReturnType (*pointer_name)(ParameterTypes);`

```cpp
// Simple function pointer
int (*fp)(int, int) = nullptr;

// Assign a function
int multiply(int a, int b) { return a * b; }
fp = multiply;

// Call through pointer
int result = fp(3, 4);  // 12

// With auto (C++14+)
auto fp2 = &multiply;  // deduces int(*)(int, int)

// Function pointer in struct
struct Calculator {
    int (*op)(int, int);
};
Calculator calc{add};
int r = calc.op(10, 20);
```

Function pointers enable: callbacks, strategy patterns, plugin architectures, and jump tables.

---""",

    "3.2.4.2": """#### 3.2.4.2 Callbacks

Function pointers are commonly used to implement callbacks — passing a function to be called later.

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

// Callback type
using Comparator = bool(*)(int, int);

bool ascending(int a, int b) { return a < b; }
bool descending(int a, int b) { return a > b; }

void sortWith(int* arr, int size, Comparator comp) {
    for (int i = 0; i < size - 1; i++) {
        if (!comp(arr[i], arr[i+1])) {
            std::swap(arr[i], arr[i+1]);
        }
    }
}

int main() {
    int data[] = {3, 1, 4, 1, 5, 9};
    sortWith(data, 6, ascending);
    for (auto v : data) std::cout << v << " ";  // 1 1 3 4 5 9

    sortWith(data, 6, descending);
    for (auto v : data) std::cout << v << " ";  // 9 5 4 3 1 1
}
```

Modern C++ prefers `std::function` or lambdas for callbacks, but raw function pointers remain important in C-style APIs and performance-critical code.

---""",

    "3.2.6": """**Scope**

Scope determines the region where a name (variable, function, etc.) is visible.

```cpp
int global = 10;  // global scope — visible everywhere after this point

void func() {
    int local = 20;           // local scope — visible inside func() only
    static int count = 0;     // static — persists across calls, but scope is local
    count++;
    
    {
        int nested = 30;      // block scope — visible only in this block
        global = 40;          // modifies the global
    }
    
    // nested is no longer accessible here
}
```

---""",

    "3.2.6.1": """#### 3.2.6.1 Local Variables

Variables declared inside a function body have **block scope** and **automatic storage duration** — they are created when the block is entered and destroyed when it exits.

```cpp
void example() {
    int x = 5;          // x created
    {
        int y = 10;     // y created
        // both x and y visible here
    }
    // y destroyed here — no longer accessible
    // x still alive
}
// x destroyed here
```

Automatic variables are stored on the **stack** (unless optimized away). They are **not** guaranteed to be initialized — read before write is **undefined behavior**.

---""",

    "3.2.6.2": """#### 3.2.6.2 Global Variables

Variables declared at namespace scope have global scope and static storage duration.

```cpp
#include <iostream>

int g_counter = 0;  // global variable — initialized to 0
static int g_hidden = 42;  // static = internal linkage (file-local)
extern int g_extern;  // declared here, defined elsewhere

void increment() {
    g_counter++;  // persists across calls
}

int main() {
    increment();
    increment();
    std::cout << g_counter << "\\n";  // 2
}
```

Cautions:
- Global mutable state is a common source of bugs and race conditions
- Initialization order across translation units is undefined (see *Static Initialization Order Fiasco*)
- `static` at namespace scope = internal linkage (one per TU)
- `extern` = external linkage (shared across TUs)

---""",

    "3.2.7": """**main**

The `main` function is the entry point of every C++ program.

```cpp
// Standard signatures
int main() { ... }                          // no args
int main(int argc, char* argv[]) { ... }    // with command-line args

// argc = argument count (including program name)
// argv = array of C-strings (argument values)

int main(int argc, char* argv[]) {
    std::cout << "Program: " << argv[0] << "\\n";
    for (int i = 1; i < argc; i++) {
        std::cout << "Arg " << i << ": " << argv[i] << "\\n";
    }
    return 0;  // 0 = success, non-zero = failure (OS-dependent)
}

// Since C++11, main does not need an explicit return:
int main() { /* ... */ }  // compiler auto-inserts `return 0;`
```

The return value of `main` is the program's **exit status**. Convention:
- `0` = success
- non-zero = error (commonly `1`, or use `EXIT_FAILURE`/`EXIT_SUCCESS` from `<cstdlib>`)

`main` is special — it cannot be overloaded, renamed, or made static/inline/etc.

---""",

    "3.3.1": """**Input and Output**

C++ uses streams for type-safe input/output via `<iostream>`.

```cpp
#include <iostream>

int main() {
    int x;
    std::cout << "Enter a number: ";
    std::cin >> x;
    if (std::cin.fail()) {
        std::cerr << "Error: invalid input\\n";
        return 1;
    }
    std::cout << "You entered: " << x << "\\n";
}
```

---""",

    "3.3.1.1": """#### 3.3.1.1 `#include <iostream>`

The `<iostream>` header declares `std::cin`, `std::cout`, `std::cerr`, `std::clog`.

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, World!\\n";   // stdout (buffered)
    std::cerr << "An error occurred!\\n";  // stderr (unbuffered)
    std::clog << "Log message\\n";      // stderr (buffered)
    return 0;
}
```

- `std::cout` uses **line buffering** on most systems — output appears after `\\n` or buffer flush
- `std::endl` flushes the buffer (slower than `'\\n'`)
- `std::cin`, `std::cout`, `std::cerr` are tied to `std::ios::sync_with_stdio(false)` for performance in competitive programming

---""",

    "3.3.1.2": """#### 3.3.1.2 cout

`std::cout` writes to standard output.

```cpp
#include <iostream>

std::cout << 42 << " " << 3.14 << " " << "text" << "\\n";
// Output: 42 3.14 text

// Chaining works because operator<< returns std::ostream&
std::cout << "Value: " << (x = 5) << "\\n";

// Hexadecimal output
std::cout << std::hex << 255 << "\\n";       // ff
std::cout << std::hex << std::showbase << 255 << "\\n";  // 0xff

// Width and fill
std::cout.width(10);
std::cout.fill('*');
std::cout << 42 << "\\n";  // ********.42 (approximate)
```

`cout` is a **stream object** — it supports formatting through manipulators (`std::hex`, `std::fixed`, `std::setprecision`, etc.).

---""",

    "3.3.1.3": """#### 3.3.1.3 cin

`std::cin` reads from standard input.

```cpp
#include <iostream>
#include <string>

int x;
double d;
std::string s;

std::cout << "Enter int, double, string: ";
std::cin >> x >> d >> s;
// Input: 42 3.14 hello
// x=42, d=3.14, s="hello"

if (std::cin.fail()) {
    // Stream is in error state
    std::cin.clear();  // clear the error flag
    std::cin.ignore(10000, '\\n');  // discard bad input
}
```

Input with `>>` stops at whitespace. To read full lines, use `std::getline`:

```cpp
std::string line;
std::getline(std::cin, line);  // reads until newline
```

---""",

    "3.3.1.4": """#### 3.3.1.4 endl or '\\n'

Both produce a newline, but `std::endl` also **flushes the output buffer**:

```cpp
std::cout << "Line 1" << std::endl;  // newline + flush
std::cout << "Line 2\\n";            // newline only (buffered)

// Performance difference:
for (int i = 0; i < 100000; i++) {
    // std::endl — SLOW (flushes every time)
    // "\\n"    — fast (buffered, flushes at end)
}
```

- Use `\\n` for newlines in most cases
- Use `std::endl` only when you need explicit flushing (e.g., before a crash or at program exit)

---""",

    # Chapter 3.4
    "3.4.1": """**Function Call Mechanics**

When a function is called, the CPU:
1. Pushes arguments onto the stack or into registers
2. Pushes the return address
3. Allocates stack space for locals (prologue)
4. Executes the function body
5. Removes stack space, restores registers (epilogue)
6. Jumps to the return address

---""",

    "3.4.1.1": """#### 3.4.1.1 Function Prologue and Epilogue

The **prologue** sets up a new stack frame; the **epilogue** tears it down.

```asm
; GCC / x86-64 Linux (Itanium ABI)
myfunction:
    push   rbp           ; save caller's base pointer
    mov    rbp, rsp       ; set base pointer = current stack pointer
    sub    rsp, 0x20      ; allocate 32 bytes for locals
    ; ... function body ...
    leave                  ; equivalent to: mov rsp, rbp; pop rbp
    ret                    ; pop return address and jump to it
```

With optimizations (`-O2`), the prologue/epilogue may be eliminated entirely for leaf functions.

---""",

    "3.4.1.2": """#### 3.4.1.2 Parameter Passing (Registers vs Stack)

Different ABIs use different rules for passing arguments:

**Itanium ABI (Linux / macOS, x86-64):**
| C++ Type | Register |
|---|---|
| 1st integer arg | RDI |
| 2nd integer arg | RSI |
| 3rd | RDX |
| 4th | RCX |
| 5th | R8 |
| 6th | R9 |
| 7th+ | stack |
| floating-point args | XMM0–XMM7, then stack |

**MSVC ABI (Windows, x86-64):**
| C++ Type | Register |
|---|---|
| 1st integer arg | RCX |
| 2nd integer arg | RDX |
| 3rd | R8 |
| 4th | R9 |
| 5th+ | stack |
| floating-point args | XMM0–XMM3, then stack |

```cpp
// C++ code
void example(int a, int b, int c, int d, int e);

// Linux (Itanium):
// a=RDI, b=RSI, c=RDX, d=RCX, e=R8

// Windows (MSVC):
// a=RCX, b=RDX, c=R8, d=R9, e=[rsp+40] (on stack)
```

This matters for reverse engineering: calling-convention mismatches can crash programs.

---""",

    "3.4.1.3": """#### 3.4.1.3 Return Value Conventions

Return values follow specific register conventions:

| Type | Linux (x86-64) | Windows (x86-64) |
|---|---|---|
| `int`, `long`, `pointer` | RAX | RAX |
| `float`, `double` | XMM0 | XMM0 |
| `__int128` | RAX:RDX | RAX:RDX |
| structs ≤ 16 bytes | RAX (sometimes XMM0/RAX) | RAX (sometimes XMM0/RAX) |
| structs > 16 bytes | Caller-allocated buffer address in RDI/RDX | Same via RCX |

```cpp
// Returns fit into a register
int get_value() { return 0x41424344; }

// Large structs passed by pointer in hidden first argument
struct Big { char data[1024]; };
Big get_big() { /* ... */ }  // actually returns via pointer passed by caller
```

---""",

    "3.4.1.4": """#### 3.4.1.4 Stack Cleanup Responsibility

**cdecl (Linux default, 32-bit x86)**: Callee cleans up (via `ret N`)
**stdcall (Windows API)**: Callee cleans up
**cdecl (GCC)**: Caller cleans up (via `add esp, N`)

On x86-64, the calling conventions unify parameter passing and stack cleanup is automatic.

---""",

    "3.4.2": """**ABI Stability**

An ABI (Application Binary Interface) defines how compiled code interoperates at the binary level. ABI instability is a major concern in C++ for shared libraries.

---""",

    "3.4.2.1": """#### 3.4.2.1 Itanium ABI (Linux)

The Itanium C++ ABI is used by GCC, Clang, and most Unix-like systems:
- Virtual table layout
- Exception handling tables (`.eh_frame`, `.GCC_except_table`)
- Vtable pointer at offset 0 of objects
- RTTI stored in `.rodata`

---""",

    "3.4.2.2": """#### 3.4.2.2 MSVC ABI (Windows)

MSVC uses a different ABI than GCC/Clang:
- Vtable pointer placement may differ
- Name mangling format differs (`?func@@YAHH@Z` vs `_Z3funcLi42E`)
- Exception model differs (SEH vs DWARF)

Cross-compiler linking is generally **not** possible for C++ objects.

---""",

    "3.4.2.3": """#### 3.4.2.3 ABI Breakage and Compatibility

Changing a class layout breaks ABI compatibility:
- Adding/removing virtual functions
- Changing inheritance hierarchy
- Resizing members
- Adding/removing base classes

Mitigation: Use the **PIMPL idiom** (Pointer to IMPLementation) to hide implementation behind a pointer:

```cpp
// header.hpp
class MyClass {
    struct Impl;
    std::unique_ptr<Impl> pImpl;
public:
    MyClass();
    ~MyClass();
    void doWork();
};
```

This keeps the ABI stable even when internal members change.

---""",

    # Chapter 4.1
    "4.1.1": """**Namespace**

Namespaces prevent naming collisions and organize code into logical scopes.

```cpp
#include <iostream>

namespace math {
    int add(int a, int b) { return a + b; }
    namespace constants {
        constexpr double PI = 3.14159;
    }
}

namespace io = std;  // alias (C++11)

int result = math::add(3, 4);           // 7
double pi = math::constants::PI;       // 3.14159

// Anonymous namespace = internal linkage
namespace { int secret = 42; }  // not visible outside this TU
```

---""",

    "4.1.1.1": """#### 4.1.1.1 using namespace

`using namespace` brings names from a namespace into the current scope:

```cpp
#include <iostream>
using namespace std;  // all std names now visible without prefix

int main() {
    cout << "Hello" << endl;  // same as std::cout << "Hello" << std::endl
}
```

**Warning**: Avoid `using namespace std;` in headers — it pollutes the global namespace for all includers.

Best practice: Prefer fully-qualified names or `using` declarations in `.cpp` files.

---""",

    "4.1.1.2": """#### 4.1.1.2 :: Scope Resolution

The `::` operator accesses names in specific scopes:

```cpp
#include <iostream>

int x = 0;  // global

namespace A { int x = 1; }
namespace B { int x = 2; }

int main() {
    int x = 3;          // local
    std::cout << x << "\\n";        // 3 (local)
    std::cout << ::x << "\\n";      // 0 (explicit global)
    std::cout << A::x << "\\n";     // 1 (namespace A)
    std::cout << B::x << "\\n";     // 2 (namespace B)
}
```

- `::name` — global scope
- `namespace::name` — specific namespace
- `class_instance::name` — static class member or nested name

---""",

    "4.1.1.3": """#### 4.1.1.3 Nested Namespace (C++17+)

C++17 allows nested namespace definitions:

```cpp
// Pre-C++17 (verbose)
namespace outer {
    namespace inner {
        void func() {}
    }
}

// C++17+ (concise)
namespace outer::inner {
    void func() {}
}

// Inline namespaces (C++11) — names are visible in enclosing scope
namespace version {
    inline namespace v2 { void api(); }
    namespace v1 { void api(); }  // old version
}
version::api();  // calls v2::api() — inline namespace is preferred
```

---""",

    "4.1.2": """**Using Declaration**

A `using` declaration brings a single name into scope:

```cpp
#include <iostream>

namespace math { int add(int, int); }
using math::add;  // 'add' now visible without qualification

int main() {
    int result = add(2, 3);  // calls math::add
}
```

---""",

    "4.1.2.1": """#### 4.1.2.1 using namespace

Brings an entire namespace's contents into the current scope:

```cpp
namespace std { /* ... */ }
using namespace std;

int main() {
    cout << "Hello";  // std::cout is available
}
```

Unlike a `using` declaration (which introduces one name), `using namespace` is a directive.

---""",

    "4.1.2.2": """#### 4.1.2.2 using std::cout

Selective `using` declaration:

```cpp
#include <iostream>

using std::cout;  // only 'cout', not all of std
using std::endl;

int main() {
    cout << "Hello, World!" << endl;
}
```

This is safer than `using namespace std;` as it avoids polluting the global namespace.

---""",

    "4.1.2.3": """#### 4.1.2.3 Type Alias

Modern C++ uses `using` for type aliases:

```cpp
// typedef (old style)
typedef unsigned long ulong;
typedef int (*FuncPtr)(int, int);

// using (modern)
using ulong = unsigned long;
using FuncPtr = int(*)(int, int);

// Template aliases (C++11)
template<typename T>
using Vec = std::vector<T, MyAllocator<T>>;

Vec<int> v;  // std::vector<int, MyAllocator<int>>
```

`using` can create template aliases, while `typedef` cannot.

---""",

    "4.1.4": """**Header Organization**

Best practices for header files:

1. Always use **include guards** or `#pragma once`
2. Prefer `#pragma once` (faster compilation, less error-prone)
3. Include only what's needed; avoid redundant includes
4. Forward-declare where possible instead of including headers

```cpp
// myheader.hpp
#pragma once  // or include guard:
// #ifndef MYHEADER_HPP
// #define MYHEADER_HPP

#include <string>       // required for std::string parameter
class OtherClass;      // forward declaration — no full definition needed

class MyClass {
public:
    MyClass(const std::string& name);
    void process(OtherClass&);  // reference — forward decl sufficient
};

// #endif
```

---""",

    "4.1.4.1": """#### 4.1.4.1 One Definition Rule (ODR)

The **One Definition Rule** states:
- A class, function, or template must have **one definition** in a program
- Header guards / `#pragma once` prevent **multiple definition** in a single TU

**ODR violation** example:
```cpp
// header.hpp (without include guards)
struct Point { int x; int y; };

// a.cpp + b.cpp both include header.hpp
// → ODR violation: Point defined twice in same program
```

For **inline functions** and **templates**, multiple definitions across TUs are allowed if they're identical (the linker merges them).

---""",

    "4.1.5": """**Modules (C++20)**

Modules replace traditional `#include` with a faster, more reliable mechanism:

```cpp
// mymodule.cppm
export module mymodule;
export int add(int a, int b);
int multiply(int a, int b);  // not exported — module-internal

// main.cpp
import mymodule;
int r = add(2, 3);        // OK — add is exported
// int m = multiply(2, 3); // ERROR — not exported
```

Key benefits:
- No macro expansion issues (`#define` leaks)
- Faster compilation (no textual inclusion)
- Enforced isolation (ODR is built-in)
- Template and `constexpr` support without ODR issues

---""",

    "4.1.5.2": """#### 4.1.5.2 import

`import` loads a module's interface:

```cpp
// Importing a named module
import std;       // import entire <iostream> (C++20, optional)
import mymodule;  // import custom module

// Mixing old and new (interoperability)
#include <cstdio>
import mymodule;

int main() {
    std::printf("Hello\\n");  // from <cstdio>
    mymodule::func();         // from module
}
```

Note: `import` (modules) is distinct from `#include` (headers) — they cannot always be mixed freely.

---""",

    "4.1.6": """**Compilation Model & Linking**

The build process:
1. **Preprocessing** — expands `#include`, `#define`, handles `#if`
2. **Compilation** — parses and generates assembly
3. **Assembly** — converts assembly to object code (`.o` / `.obj`)
4. **Linking** — resolves symbols across TUs into executable/library

---""",

    "4.1.6.1": """#### 4.1.6.1 Preprocessor

The preprocessor runs before the compiler:
- `#include` — textual file inclusion
- `#define` — textual macro substitution
- `#if` / `#ifdef` — conditional compilation
- `#pragma` — implementation-specific directives

```cpp
#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif
```

Problems with macros:
- No type safety
- No scoping
- Hard to debug
- Replace with `constexpr` variables and `inline` functions where possible

---""",

    "4.1.6.2": """#### 4.1.6.2 Translation Units

A **translation unit (TU)** is one `.cpp` file plus all headers it transitively includes (after preprocessing).

```cpp
// a.cpp
#include "header.hpp"
int foo() { return 42; }

// b.cpp — a SEPARATE translation unit
#include "header.hpp"
int bar() { return foo(); }  // calls foo() from a.cpp
```

Linking combines TUs — `a.o` and `b.o` are linked by the linker to produce the final binary.

---""",

    "4.1.6.3": """#### 4.1.6.3 static vs. extern

Controls **linkage** — whether a symbol is shared across TUs or file-local.

```cpp
// a.cpp
static int internal_var = 42;    // internal linkage — only in a.cpp
extern int external_var;         // declared here, defined elsewhere
int shared_var = 0;              // external linkage by default

// b.cpp
extern int external_var;         // same variable as in a.cpp
extern int shared_var;           // OK — same name, external linkage
```

| Specifier | Linkage | Scope |
|---|---|---|
| `static` | Internal (file-local) | Current TU only |
| `extern` | External | Shared across TUs |
| (none) | External | Shared across TUs |

---""",

    "4.1.6.4": """#### 4.1.6.4 Name Mangling

C++ mangles (decorates) symbol names to encode type info for linking. This prevents collisions between overloaded functions.

```cpp
void foo(int x);           // _Z3fooi (Itanium ABI)
void foo(double x);        // _Z3food (Itanium ABI)
```

C functions (linked with `extern "C"`) are **not mangled**:
```cpp
extern "C" void foo(int);  // foo (no mangling — C ABI)
```

Use `extern "C"` for interoperability with C libraries.

---""",

    "4.1.6.5": """#### 4.1.6.5 Manual ABI Control (extern "C")

Forcing C linkage:

```cpp
// C-compatible interface
extern "C" {
    __declspec(dllexport) void* create_object();
    __declspec(dllexport) void destroy_object(void* obj);
    __declspec(dllexport) int process(void* obj, int data);
}
```

This exports unmangled names that can be loaded via `dlsym` (Linux) or `GetProcAddress` (Windows) — common in plugin systems.

---"""
}

with open(OUTPUT, 'w') as f:
    f.write("")  # placeholder

print("Content definitions prepared. Need to write integration script next.")
