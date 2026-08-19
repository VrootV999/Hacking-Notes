CPP Complete Guide + Notes

# 1. Core Language Fundamentals

## 1.1 Initialisation of Variables: Default, Value, Copy, Direct, Direct List (Uniform), Copy List, Type Deduction (auto), Aggregate, Designated (C++20/23), Structured Binding, std::initializer_list, Dynamic Allocation, constexpr, Lambda Init-Capture, Braced Initializer as function arg.

---
## 1.2 Data Types Summary: int, float, double, char, bool, long, long long, unsigned.
### 1. **Integer Types**
### 2. **Floating-Point Types**
### 3. **Character Types**
### 4. **Pointer Types**
### 5. **Size and Memory Management Types**
### 6. **Other Types**

### Summary of Common Sizes on 64-bit Systems

## 1.3 Type Conversion: Implicit, Explicit.
Type conversion = changing a value from one data type to another.  
Two kinds: **implicit (automatic)** and **explicit (manual / cast)**.

### Implicit Type Conversion
---
### Explicit Type Conversion(casting)

#### Cpp-Style Casting
---
## 1.4 Casting: static_cast, dynamic_cast, reinterpret_cast, const_cast, std::bit_cast (C++20).
# C++ Casting
C++ provides four named casts + `std::bit_cast` (C++20).  
They are safer and more explicit than C-style casts.

### `static_cast`
### `dynamic_cast`
### `reinterpret_cast`
### `const_cast`

### `std::bit_cast (C++20)`
## 1.5 Memory & Pointers: Memory Addressing (&), Pointers (*), Dereference (*p), nullptr, new, delete.
### Memory Addressing (`&`)
`&` gives the **memory address** of a variable.

```cpp
int x = 10;
int* p = &x; // p stores the address of x
References: int& ref, call site reference.
```
---
### Pointers(`*`)
`*` stores an address of another variable.
- Pointer types must match the pointed-to type.
```cpp
int x = 42;
int* p = &x;   // pointer to int
```
--- 
### Dereferencing(`*p`)
* used on a pointer gives access to the value at that address.
```cpp
int x = 10;
int* p = &x;

*p = 20;      // modifies x
```
--- 
### nullptr
Represents an invalid / empty pointer (C++11+).
Use it instead of 0 or NULL.
```cpp 
int* p = nullptr;
```
--- 
### Dynamic Memory: new and delete
Allocates memory on the heap.
Always delete what you new.
#### Single Object
```cpp
int* p = new int(5);
delete p;
```
---
#### Array 
```cpp
int* arr = new int[10];
delete[] arr;
```
Points to remeber
- new → delete
- new[] → delete[]
- Dangling: pointer to freed memory
- Wild: uninitialized pointer
- Avoid by initializing to nullptr and deleting safely.
---

## 1.6 Literals: Integer, Hex, Octal, Unsigned, Float.

### Integer Literals
Default type: `int` (or larger if needed).
```cpp
int a = 42;
long b = 42L;
long long c = 42LL;
```
Suffix
- L / l → long
- LL / ll → long long
- U / u → unsigned
- Combine: 42UL, 42LLU, etc.
---
### Hexadecimal Literals
Prefix 0x or 0X.
```cpp
int x = 0xFF;    // 255
int y = 0X1A3;   // 419
```
---
### Octal Literals
Prefix 0 (leading zero).
```cpp 
int o = 077;     // octal 77 = decimal 63
```
---
### Binary Literals (C++14+)
Prefix 0b or 0B.
```cpp
int b = 0b1010;  // 10
```
---
### Unsigned Literals
Add U or u.
```cpp
unsigned int u1 = 10U;
unsigned long u2 = 100UL;
```
- Useful to avoid signed overflow.
---
### Floating-Point Literals
Default type: double.
```cpp
double d = 3.14;
float  f = 3.14f;
long double ld = 3.14L;
//scientific notation
double e = 1.23e4;   // 12300
float  g = 5.6e-3f;  // 0.0056
```
---
### Digit Separators (C++14+)
Use ' to improve readability.
```cpp
int n = 1'000'000;
double pi = 3.141'592'653;
```
---
## 1.6 Misc: sizeof, strlen, typeid, auto, Overflow.

### `sizeof`
Returns the **size in bytes** of a type or object.  
Evaluated at **compile time** (except VLAs in C).

```cpp
int x = 10;
size_t s1 = sizeof(int);  // size of type
size_t s2 = sizeof x;     // size of variable
```
---
### strlen (C)
Returns the length of a C-string, excluding the null terminator.
Works only on null-terminated strings.
> [!Note]Note: Undefined behavior if string has no '\0'.
```cpp 
char str[] = "hello";
size_t len = strlen(str);   // 5
```
---
### typeid (C++)
Returns a std::type_info object describing the type.
With polymorphism + references/pointers, gives dynamic type:
Needs at least one virtual function for dynamic type resolution.
```cpp 
#include <typeinfo>

int x = 5;
std::cout << typeid(x).name();      // implementation-defined
//With polymorphism + references/pointers, gives dynamic type:
Base* b = new Derived();
std::cout << typeid(*b).name();     // Derived
```
---
### auto (C++11+)
Automatic type deduction.
Compiler infers the type from the initializer.
```cpp
auto x = 10;        // int
auto y = 3.14;      // double
auto p = &x;        // int*
```
- Use auto when type is long, repetitive, or unimportant.
--- 
### Overflow
Occurs when a value exceeds the range of its type.
#### Integer Overflow
- Signed overflow = undefined behavior (UB)
- Unsigned overflow = wraps modulo 2ⁿ
```cpp 
unsigned int u = UINT_MAX;
u++;   // wraps to 0 (defined)
int x = INT_MAX;
x++;   // signed overflow → UB
```

#### Floating-Point Overflow
Results in +inf, -inf, or nan.
```cpp 
double d = 1e308 * 1e308; // inf
```
--- 

## 1.7 Type Aliases: typedef, using.

### `typedef`
Creates an alias for an existing type.

```c
typedef existing_type new_name;
typedef unsigned long ulong;
typedef int* intptr;

ulong a = 100;
intptr p = &a; // pointer to int? → WRONG TYPE, example for syntax only
```
---
### `using`
Modern, cleaner way to create type aliases.
Also works better with templates.
```cpp
using ulong = unsigned long;
using func_ptr = void(*)(int);
//typedef cannot do this cleanly.
template <typename T>
using vec = std::vector<T>;

vec<int> v; // alias for std::vector<int
```
---
### Difference b/w `typedef` & `using`
| Feature              | `typedef` | `using` |
| -------------------- | --------- | ------- |
| Basic alias          | ✔️        | ✔️      |
| Template alias       | ❌         | ✔️      |
| Readability          | Worse     | Better  |
| Modern C++ preferred | No        | Yes     |
---
## 1.8 Enums: enum Color.
`enum` defines a set of named integer constants.  
Improves readability and type safety.

### Basic Enum
```cpp
enum Color {
    Red,
    Green,
    Blue
};
````
* First value = `0` by default
* Subsequent values increment by 1
```cpp
Color c = Green;   // c == 1
```
---
### Custom Values

```cpp
enum Color {
    Red = 10,
    Green = 20,
    Blue = 30
};
```
---
### Using Enums in Code

```cpp
void paint(Color c) {
    if (c == Red) { /* ... */ }
}
```
---

### Scoped Enum (`enum class`, C++11)

Stronger type safety + no automatic int conversion
Use when you want clean namespaces and fewer accidental comparisons.

```cpp
enum class Color {
    Red,
    Green,
    Blue
};

Color c = Color::Red;

// Comparison only works with same enum type
if (c == Color::Red) { }
```

---

### Underlying Type (C++11+)

Specify storage type:

```cpp
enum class Color : uint8_t {
    Red,
    Green,
    Blue
};
```

---
* `enum` = named integer constants
* Values auto-increment unless manually set
* `enum class` = scoped, safer, no implicit int conversion

--- 

## 1.9 References: int& ref, call site reference.

Alias for an existing variable. Changes via reference affect the original. Only in C++, not C.

### basic syntax

```cpp
int x = 10;
int& ref = x; // ref refers to x
ref = 20;     // x becomes 20
```

---
### as function parameter

```cpp
void increment(int& n) {
    n++;
}

int main() {
    int a = 5;
    increment(a); // a becomes 6
}
```

---
### rules

* Must be initialized when declared.
* Cannot be null.
* Useful for avoiding copies and allowing modifications.
* `const` references can bind to temporary values without modifying them:

```cpp
void print(const int& n) {
    std::cout << n;
}
```

---

# 2. Control Flow & Functions

## 2.1 Control Flow: if / else if / else, switch, Ternary Operator, switch with strings.


### `if / else if / else`
Used for conditional branching.

```cpp
int x = 10;

if (x > 10) {
    // ...
} else if (x == 10) {
    // ...
} else {
    // ...
}
```
---

### `switch`

Efficient multi-branch selection.
Works with **integral types**: `int`, `char`, enums, etc.

```cpp
int x = 2;

switch (x) {
    case 1: break;
    case 2: /* ... */ break;
    default: break;
}
```
* Cases must be **constant expressions**
* `break` prevents fall-through
* Fall-through allowed intentionally:
```cpp
switch (x) {
    case 1:
    case 2: // falls through
        // ...
        break;
}
```

---

### Ternary Operator `?:`

Short inline conditional.
`condition ? value_if_true : value_if_false`

```cpp
int age = 20;
string s = (age >= 18) ? "adult" : "minor";
```

Useful for small expressions, not full logic blocks.

---

### Switch With Strings (C++)

`switch` **cannot** directly use `std::string`.
You must convert to an integer, typically via hashing.

Example
```cpp
#include <string>
#include <functional>

std::string s = "apple";

switch (std::hash<std::string>{}(s)) {
    case std::hash<std::string>{}("apple"):
        // ...
        break;
    case std::hash<std::string>{}("banana"):
        // ...
        break;
}
```

- Alternative Use `if` / `else`:

```cpp
if (s == "apple") { }
else if (s == "banana") { }
```

---
* `if / else` = flexible logic
* `switch` = efficient multi-branch for integral types
* Ternary = compact conditional expression
* `switch` can't handle strings directly → use hashing or `if/else`
---
## 2.2 Loops: for, while, do-while, Range-Based for.

### `for` Loop
Best when you know iteration count.

```cpp
for (int i = 0; i < 5; i++) {
    // runs 5 times
}
````

---

### `while` Loop

Runs while a condition is true.

```cpp
int x = 0;
while (x < 5) {
    x++;
}
```

Often used when number of iterations is unknown.

---

### `do-while` Loop

Runs **at least once**, condition checked afterward.

```cpp
int x = 0;
do {
    x++;
} while (x < 5);
```

---

### Range-Based `for` (C++11+)

Iterates directly over containers/arrays.

```cpp
std::vector<int> v = {1, 2, 3};
for (int x : v) {
    // read-only
}
//reference
for (int& x : v) {
    x *= 2;   // modifies elements
}
//With `auto`
for (auto& item : v) { /* ... */ }
```

---
* `for` → counting
* `while` → condition-controlled
* `do-while` → guaranteed 1 iteration
* Range-based `for` → simple container iteration
--- 

## 2.3 Loop Control: break, continue.
### `break`
Immediately exits the nearest loop (or switch).
```cpp
for (int i = 0; i < 10; i++) {
    if (i == 5) break;   // stops loop at i == 5
}
```
Useful when a condition is met early.

---

### `continue`
Skips the rest of the current iteration and moves to the next.
```cpp
for (int i = 0; i < 5; i++) {
    if (i == 2) continue;  // skip printing 2
    std::cout << i << "\n";
}
```
---
* `break` → exit loop immediately
* `continue` → skip to next iteration
---
## 2.4 Common Functions: sqrt, pow, floor, ceil, sort, reverse.

### sqrt

Returns square root of a number.
Requires `<math.h>` in C and `<cmath>` in C++.

```c
#include <math.h>
double r = sqrt(16.0); // 4.0
```

```cpp
#include <cmath>
double r = std::sqrt(25); // 5
```
---
### pow

Raises a base to an exponent.

```c
double r = pow(2, 3); // 8
```

```cpp
double r = std::pow(3, 4); // 81
```
---
### floor

Rounds a floating-point number down to the nearest integer.

```c
double x = floor(3.9); // 3.0
```

```cpp
double x = std::floor(-2.1); // -3.0
```
---
### ceil

Rounds a floating-point number up to the nearest integer.

```c
double x = ceil(3.1); // 4.0
```

```cpp
double x = std::ceil(-2.1); // -2.0
```
---
### sort

C uses `qsort`, C++ uses `std::sort`.

```c
#include <stdlib.h>

int cmp(const void *a, const void *b) {
    return (*(int*)a - *(int*)b);
}

int arr[] = {4, 2, 1, 3};
qsort(arr, 4, sizeof(int), cmp);
```

```cpp
#include <algorithm>
#include <vector>
std::vector<int> v = {4, 2, 1, 3};
std::sort(v.begin(), v.end());
```
---
### reverse

C has no built-in; do manually. C++ uses `std::reverse`.

```c
int arr[] = {1,2,3,4};
int n = 4;
for(int i = 0, j = n-1; i < j; i++, j--) {
    int temp = arr[i];
    arr[i] = arr[j];
    arr[j] = temp;
}
```

```cpp
#include <algorithm>
std::vector<int> v = {1,2,3,4};
std::reverse(v.begin(), v.end());
```
---

## 2.5 Recursion: Factorial example.

A function calling itself until a base condition stops it. Useful for problems naturally defined in smaller subproblems.

```c
int fact(int n) {
    if (n <= 1) return 1;     // base case
    return n * fact(n - 1);   // recursive step
}

int main() {
    int r = fact(5); // 120
}
```
---
```cpp
int fact(int n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}

int main() {
    int r = fact(5); // 120
}
```

---

## 2.6 Function Overloading: Different parameter types.

Same function name, different parameter lists. Resolved at compile time. Not available in C, only C++.

examples with different parameter types
```cpp
void print(int x) {
    std::cout << "int: " << x << "\n";
}

void print(double x) {
    std::cout << "double: " << x << "\n";
}

void print(const char* s) {
    std::cout << "string: " << s << "\n";
}

int main() {
    print(10);
    print(3.14);
    print("hello");
}
```

---
### rules

* Parameter types or count must differ.
* Return type alone cannot overload.
* Best-match overload chosen automatically.

---


## 2.7 Default Args: Optional parameters.
Functions can have parameters with default values. If argument is missing, default is used. Only in C++, not C.

### example

```cpp
#include <iostream>

void greet(std::string name = "Guest") {
    std::cout << "Hello, " << name << "!\n";
}

int main() {
    greet();          // Hello, Guest!
    greet("Alice");   // Hello, Alice!
}
```

---
### rules

* Default values assigned in function declaration or prototype.
* Once a parameter has default, all parameters to its right must also have defaults.

---


## 2.8 Function Pointers: int (*funcPtr)(int, int).
Pointer storing address of a function. Can be used to call functions dynamically. Useful for callbacks.

example (C)
```c
#include <stdio.h>

int add(int a, int b) {
    return a + b;
}

int main() {
    int (*funcPtr)(int, int) = add; // pointer to add
    int result = funcPtr(3, 4);     // calls add(3,4)
    printf("%d\n", result);          // 7
}
```
---

example (C++)
```cpp
#include <iostream>

int multiply(int a, int b) {
    return a * b;
}

int main() {
    int (*funcPtr)(int, int) = multiply;
    std::cout << funcPtr(3, 4); // 12
}
```
---
### rules

* Declaration: `returnType (*pointerName)(parameterTypes)`
* Can point to any function with matching signature.
* Supports dynamic selection of functions at runtime.

---

## 2.9 Lambda Expressions: [](){}, Init-Capture.

Anonymous functions defined inline. Can capture variables from surrounding scope. Only in C++, not C.

### basic syntax

```cpp
auto f = []() { 
    std::cout << "Hello Lambda\n"; 
};
f();
```

---
### with parameters

```cpp
auto add = [](int a, int b) { return a + b; };
std::cout << add(3, 4); // 7
```

---
### capture variables

```cpp
int x = 5, y = 10;

// capture by value
auto f1 = [x, y]() { return x + y; };

// capture by reference
auto f2 = [&x, &y]() { x += y; };

// init-capture (C++14+)
auto f3 = [z = x + y]() { return z * 2; };
```

---
### rules

* `[]` empty: no capture.
* `[=]` capture all by value, `[&]` all by reference.
* `[x, &y]` mix of value and reference.
* Init-capture allows creating new variables in lambda scope.

---


## 2.10 Free Functions

Regular functions not bound to any class. Can be called directly. In C++ they exist alongside member functions.

example (C)
```c
#include <stdio.h>

void greet() {
    printf("Hello World\n");
}

int main() {
    greet();
}
```

---
example (C++)
```cpp
#include <iostream>

void greet() {
    std::cout << "Hello World\n";
}

int main() {
    greet();
}
```

---
### notes

* Not tied to any object or class.
* Can be used as callbacks, with function pointers or lambdas.
* Contrast with member functions which require an object to call.

---

# 3. Organization & Linkage

## 3.1 Namespace: using namespace, :: Scope Resolution, Nested (C++17+).

Groups functions, variables, and classes to avoid name conflicts. Accessed via scope resolution `::`.

### basic usage

```cpp
#include <iostream>

namespace Math {
    int add(int a, int b) { return a + b; }
}

int main() {
    std::cout << Math::add(2, 3); // 5
}
```

---
### using directive

```cpp
using namespace Math;

int main() {
    std::cout << add(2, 3); // no need for Math:: prefix
}
```

---
### nested namespaces (C++17+)

```cpp
namespace A::B {
    int value = 10;
}

int main() {
    std::cout << A::B::value; // 10
}
```

---
### rules

* Avoid `using namespace` in headers to prevent conflicts.
* `::` accesses global scope or specific namespace.
* Nested namespaces simplify long chains of namespaces.

---
## 3.2 Using: using namespace, using std::cout, Type Alias.

`using` brings names into current scope or creates type aliases. Shortens code and avoids repetitive typing.

---
### using namespace

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "Hello\n"; // no std:: needed
}
```

---
### using specific member

```cpp
using std::cout;
using std::endl;

int main() {
    cout << "Hello" << endl;
}
```

---
### type alias

```cpp
using IntVec = std::vector<int>;  // C++11+
IntVec v = {1, 2, 3};
```

```cpp
typedef unsigned long ulong; // older C++ style
ulong x = 100;
```

---
### rules

* `using namespace` imports all names; can cause conflicts, use carefully.
* `using` for specific members avoids importing everything.
* Type aliases make code cleaner and easier to maintain.

---


## 3.3 Libraries: #include, <iostream>, <cmath>, <string>, <vector>, <algorithm>, <typeinfo>, Static and Dynamic libraries.

## 3.4 Macros

Macros are **preprocessor directives** that perform text substitution **before compilation**.  
Defined using `#define`.

### Object-like Macros
Simple replacement of constants or expressions.

```c
#define PI 3.14159
#define MAX_SIZE 100

int arr[MAX_SIZE];
double area = PI * r * r;
````

---

### Function-like Macros

Macros with parameters.

```c
#define SQUARE(x) ((x)*(x))

int a = 5;
int b = SQUARE(a);  // 25
```

**Tip:** Wrap parameters in parentheses to avoid precedence issues.

---

### Conditional Compilation

Control which code gets compiled.

```c
#define DEBUG

#ifdef DEBUG
    printf("Debugging...\n");
#endif
```

Other directives:

* `#ifndef` → if not defined
* `#undef` → undefine a macro
* `#if / #elif / #else / #endif` → complex conditions

---

### Macro vs Constant

* **Macro:** preprocessor, no type checking, text replacement
* **`const` / `constexpr` (C++):** type-checked, safer, scoped

```cpp
const double pi = 3.14159;   // preferred in C++
```

---
* `#define` → create constants or inline macros
* Function-like macros → beware of operator precedence
* Use `const` / `constexpr` in modern C++ for safer alternatives
* Conditional compilation → `#ifdef`, `#ifndef`, `#if`

---

## 3.5 Header: One Definition Rule (ODR), Don't Repeat Yourself (DRY).

### One Definition Rule (ODR)
Each variable, function, class, or template **must have exactly one definition** in the entire program (across all translation units), though **declarations** can appear multiple times.
```cpp
int x;           // OK in one .cpp file
extern int x;    // OK in multiple files
```
--- 
### Don't Repeat Yourself (DRY)
Avoid duplicating code; write reusable functions, classes, or templates instead of copying the same logic.

```cpp
int sum(int a, int b) { return a + b; }

int main() {
    int x = sum(5, 3);
    int y = sum(10, 7);
}
```

---

## 3.6 Compiler Support Portability

Compiler support and portability ensure your code works across different compilers and platforms.  
Consider **language standards**, system-specific features, and library availability.

### Language Standard
- Use standard C/C++ features for maximum portability.  
- Avoid compiler-specific extensions unless necessary.

```cpp
// Portable C++ code
#include <iostream>

int main() {
    std::cout << "Hello, portable world!\n";
}
```
--- 
### System-Specific Features

* Avoid OS-specific APIs if targeting multiple platforms.
* Use conditional compilation if necessary.

```cpp
#ifdef _WIN32
    // Windows-specific code
#else
    // Unix/Linux-specific code
#endif
```

--- 
### Compiler Warnings & Flags

* Enable warnings to catch non-portable constructs.
* Use flags like `-Wall -Wextra` (GCC/Clang) or `/W4` (MSVC).

---
### Libraries & Dependencies

* Prefer standard libraries over third-party ones for portability.
* If using third-party libraries, ensure they support all target platforms.

---
### Quick Summary

* Stick to standard C/C++ features
* Use conditional compilation for system-specific code
* Enable compiler warnings
* Prefer portable libraries

---

## 3.7 Compiler Tutorial
Compilers convert source code into machine code. Popular C/C++ compilers: **GCC**, **G++**, **MSVC**, **ICC**, **Clang**.  
Knowing flags, optimizations, and portability issues is crucial for performance and debugging.

### GCC / G++
GNU Compiler Collection. `gcc` for C, `g++` for C++.

```bash
gcc file.c -o output        # Compile C
g++ file.cpp -o output      # Compile C++
```

**Important Flags:**

* `-Wall` → Enable most warnings
* `-Wextra` → Additional warnings
* `-O0`, `-O1`, `-O2`, `-O3`, `-Ofast` → Optimization levels
* `-g` → Include debugging symbols
* `-std=c++17` → Select language standard
* `-march=native` → Optimize for your CPU
* `-pthread` → Enable multithreading support

**Performance Tips:**

* Use `-O2` or `-O3` for release builds
* Profile code with `gprof` to find bottlenecks
* Inline small functions using `inline` keyword or compiler hints

---

### MSVC (Microsoft Visual C++)

Command-line: `cl`, or via Visual Studio IDE.

```bat
cl /EHsc file.cpp          # Compile C++ file with exception handling
```

**Important Flags:**

* `/W4` → Enable high-level warnings
* `/O2` → Optimize for speed
* `/Od` → Disable optimizations (debug mode)
* `/MD` → Use multi-threaded runtime library
* `/Zi` → Debug info generation

**Tips:**

* Use `/Ob2` to inline functions aggressively
* `/GL` + `/LTCG` for whole-program optimization

---

### ICC (Intel C++ Compiler)

Optimized for Intel CPUs. Command: `icc` / `icpc`.

```bash
icpc file.cpp -O3 -xHost -ipo -o output
```

**Key Flags:**

* `-O3` → Aggressive optimization
* `-xHost` → Optimize for current CPU
* `-ipo` → Interprocedural optimization
* `-qopenmp` → Enable OpenMP
* `-g` → Debug info

**Tips:**

* ICC often generates faster code on Intel processors than GCC/MSVC
* Profile-guided optimization (`-prof-gen` / `-prof-use`) improves speed

---

### Clang

Fast, modern compiler with excellent diagnostics.

```bash
clang++ file.cpp -o output
```

**Key Flags:**

* `-Wall`, `-Wextra` → Warnings
* `-O0`, `-O2`, `-O3` → Optimization
* `-std=c++17` → Language standard
* `-fsanitize=address,undefined` → Detect memory/undefined behavior

**Tips:**

* Use `-Weverything` for maximum warnings
* Works well with Clang-Tidy for static analysis

---

### Cross-Compiler Tips

* Always specify **language standard** (`-std=c++17`)
* Enable warnings in **all builds**
* Use **profiling tools**: `gprof`, `perf`, `VTune`
* Use `-march` / CPU-specific flags for performance
* Debugging: always keep a debug build (`-g`) separate from release

---
### Quick Summary

* GCC/G++ → Linux, highly portable, flexible flags
* MSVC → Windows, integration with Visual Studio
* ICC → Intel CPU optimized, aggressive optimizations
* Clang → Fast, great diagnostics, modern C++ support
* Flags: warnings, optimization, standard selection, debug info
* Performance: profiling, inlining, CPU-specific instructions, whole-program optimization

---

# 4. Modifiers & Compile-Time

## 4.1 Modifiers: const, static, volatile, mutable.

## 4.2 Global Variable: extern const, static constexpr, inline constexpr.

## 4.3 static: Function variable persistence, Class members, File-scope linkage.

## 4.4 inline: Function (Optimization & ODR), Variable (ODR & Single Instance Guarantee), Nested Namespace.

## 4.5 constexpr: Function (Implicitly inline), Variable (Must be explicitly inline constexpr in headers).

## 4.6 consteval

## 4.7 constinit

## 4.8 Compile Time Programming

## 4.9 Template Metaprogramming

## 4.10 SFINAE

# 5. Object-Oriented Programming (OOP)

## 5.1 Struct: struct Point.

## 5.2 Class Basics: class Box, public, private, protected.

## 5.3 Constructor: Default, Overloaded.

## 5.4 Getter/Setter

## 5.5 Destructors

## 5.6 this

## 5.7 Inheritance: class B : public A.

## 5.8 Polymorphism: virtual, override.

## 5.9 Interface: Pure virtual functions (= 0), Virtual Destructor.

## 5.10 Operator Overloading

## 5.11 friend

# 6. Advanced C++ & Idioms

## 6.1 Templates: template <typename T>.

## 6.2 Exception Handling: try, catch, throw, std::exception.

## 6.3 Dynamic Memory: new, delete[].

## 6.4 constexpr Functions (compile-time computation)

## 6.5 Initialization

## 6.6 RAII (Resource Acquisition Is Initialization)

## 6.7 CRTP (Curiously Recurring Template Pattern)

## 6.8 deducing this

## 6.9 cpp concepts features

## 6.10 Clean C++ Code Writing

## 6.11 Safe C++ Code Writing

# 7. Memory Management & Ownership

## 7.1 Garbage Value Initialisation

## 7.2 Ownership and Move Semantics

## 7.3 Rvalue Glvalues Prvalues: value_cast (rvalue prvalue glvalue lvalue rvalue).

## 7.4 Move Semantics: Algorithms and std library.

## 7.5 std::shared_pointer

## 7.6 std::unique_pointer

# 8. Standard Template Library (STL) & Utilities

## 8.1 Containers: std::vector, std::map, std::deque, std::list, std::set, std::unordered_set, std::unordered_map.

## 8.2 Container Utilities: push_back, remove, empty.

## 8.3 Ranges: Sequential Generation, Filtering, Slicing, Reduction, Flattening, Method Chaining, Set Operations.

## 8.4 Type Utilities: std::to_underlying, std::move, std::reference_wrapper, std::void, std::monostate, std::pair, std::variant, std::visit.

## 8.5 Address Utilities: std::addressof, std::to_address.

## 8.6 Error Handling/Flow: std::expected, std::optional.

## 8.7 Threading/Concurrency: std::lock_guard, std::scoped_lock, std::thread, std::jthread, std::promise, std::async.

## 8.8 Function Utilities: std::function, std::copyable_function.

## 8.9 Memory/Views: std::span.

## 8.10 String Manipulation: std::toupper, std::tolower, std::towupper, std::towlower, std::stoi, std::stol, std::stoll, std::stof, std::stod, std::stold.

## 8.11 Random Function: <random> (std::random_device, std::uniform_int_distribution, std::mt19937).

# 9. External & Development

## 9.1 Libraries: std, Networking, UI (C++ or C#).

## 9.2 Abstraction

## 9.3 Metabuild System

## 9.4 Build System

## 9.5 Dependency

## 9.6 File Management

## 9.7 Other File Accessing ABI

## 9.8 Serialization

## 9.9 Networking

## 9.10 Cryptography

# 10. Security & Exploit Development (OSCP Context)

## 10.1 Byte-level payload: uint8_t, char.

## 10.2 Port numbers / offsets: unsigned short.

## 10.3 Shellcode length: const size_t.

## 10.4 Integer overflow bugs: int, unsigned.

## 10.5 Memory address ops: void*, uintptr_t.

# 11. Resources

## 11.1 Cherno

## 11.2 CppCon

## 11.3 Jason Turner

## 11.4 Low Level Learning

---
