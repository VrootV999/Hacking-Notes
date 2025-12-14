# 1. Core Language Fundamentals & Types

## 1.1 Initialisation & Data Types

### 1.1.1 Initialisation of Variables

```cpp 
int x; // Default initialization: uninitialized (garbage value)
int x{}; // Value initialization: 0
int x = {}; // Value initialization (with equals): 0
int x = int(); // Value initialization (creates temporary, then copy): 0
int x = 10; // Copy initialization: 10
int x = (10); // Copy initialization (creates temporary, then copy): 10
int x = (1, 0); // Copy initialization (comma operator evaluates to rightmost): 0
int x(10); // Direct initialization: 10
int x{10}; // Direct list (uniform) initialization: 10
int x = {10}; // Copy list initialization: 10
auto x = 10; // Type deduction: int, value 10
auto x(10); // Type deduction: int, value 10 (since C++17, earlier was std::initializer_list<int>)
auto x = (10); // Type deduction: int, value 10
auto x{10}; // Type deduction: std::initializer_list<int> with one element 10
auto x = {1, 0}; // Type deduction: std::initializer_list<int> with elements {1, 0}
Point p{1, 2}; // Aggregate initialization
Point p = {.x = 1, .y = 2}; // Designated initialization (C++20/23)
auto [a, b] = std::pair(1, 2); // Structured binding initialization
std::vector<int> v{1, 2, 3}; // std::initializer_list initialization
auto* p = new MyClass{1, 2}; // Dynamic allocation with brace init
constexpr int x = 42; // Constant expression initialization
auto f = [x = 42]() { return x; }; // Lambda init-capture
foo({1, 2}); // Braced initializer as function arg
```


--- 

### 1.1.2 Data Types Summary
#### 1.1.2.1 int

| Type                 | Description                                  | Size (bytes) | Range (for signed)                                                                                           |
| -------------------- | -------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------ |
| `char`               | Single character (8-bit)                     | 1            | -128 to 127 (signed)                                                                                         |
| `unsigned char`      | Unsigned character (8-bit)                   | 1            | 0 to 255                                                                                                     |
| `short`              | Short integer (16-bit)                       | 2            | -32,768 to 32,767                                                                                            |
| `unsigned short`     | Unsigned short (16-bit)                      | 2            | 0 to 65,535                                                                                                  |
| `int`                | Integer (typically 32-bit on 32-bit systems) | 4            | -2,147,483,648 to 2,147,483,647                                                                              |
| `unsigned int`       | Unsigned integer (typically 32-bit)          | 4            | 0 to 4,294,967,295                                                                                           |
| `long`               | Long integer (32-bit or 64-bit)              | 4 or 8       | -2,147,483,648 to 2,147,483,647 (32-bit) or -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 (64-bit) |
| `unsigned long`      | Unsigned long (32-bit or 64-bit)             | 4 or 8       | 0 to 4,294,967,295 (32-bit) or 0 to 18,446,744,073,709,551,615 (64-bit)                                      |
| `long long`          | Long long integer (64-bit)                   | 8            | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807                                                      |
| `unsigned long long` | Unsigned long long (64-bit)                  | 8            | 0 to 18,446,744,073,709,551,615                                                                              |
| `int8_t`             | Fixed-width integer (signed 8-bit)           | 1            | -128 to 127                                                                                                  |
| `uint8_t`            | Fixed-width unsigned integer (8-bit)         | 1            | 0 to 255                                                                                                     |
| `int16_t`            | Fixed-width integer (signed 16-bit)          | 2            | -32,768 to 32,767                                                                                            |
| `uint16_t`           | Fixed-width unsigned integer (16-bit)        | 2            | 0 to 65,535                                                                                                  |
| `int32_t`            | Fixed-width integer (signed 32-bit)          | 4            | -2,147,483,648 to 2,147,483,647                                                                              |
| `uint32_t`           | Fixed-width unsigned integer (32-bit)        | 4            | 0 to 4,294,967,295                                                                                           |
| `int64_t`            | Fixed-width integer (signed 64-bit)          | 8            | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807                                                      |
| `uint64_t`           | Fixed-width unsigned integer (64-bit)        | 8            | 0 to 18,446,744,073,709,551,615                                                                              |
---

#### 1.1.2.2 float

| Type          | Description                                             | Size (bytes) | Range                                |
| ------------- | ------------------------------------------------------- | ------------ | ------------------------------------ |
| `float`       | Single precision floating-point (32-bit)                | 4            | 1.5 × 10^−45 to 3.4 × 10^38          |
| `double`      | Double precision floating-point (64-bit)                | 8            | 5.0 × 10^−324 to 1.7 × 10^308        |
| `long double` | Extended precision floating-point (depends on platform) | 8, 12, or 16 | Varies (typically 80-bit or 128-bit) |
| `float32_t`   | Fixed-width single precision float (32-bit)             | 4            | Same as `float`                      |
| `float64_t`   | Fixed-width double precision float (64-bit)             | 8            | Same as `double`                     |
---

#### 1.1.2.3 Pointer Types

| Type      | Description                         | Size (bytes)                   |
| --------- | ----------------------------------- | ------------------------------ |
| `void*`   | Void pointer (generic pointer type) | 8 (on 64-bit) or 4 (on 32-bit) |
| `char*`   | Pointer to a `char`                 | 8 (on 64-bit) or 4 (on 32-bit) |
| `int*`    | Pointer to an `int`                 | 8 (on 64-bit) or 4 (on 32-bit) |
| `float*`  | Pointer to a `float`                | 8 (on 64-bit) or 4 (on 32-bit) |
| `double*` | Pointer to a `double`               | 8 (on 64-bit) or 4 (on 32-bit) |
| `long*`   | Pointer to a `long`                 | 8 (on 64-bit) or 4 (on 32-bit) |
---

#### 1.1.2.4 char

| Type            | Description                  | Size (bytes) |
| --------------- | ---------------------------- | ------------ |
| `char`          | A single character           | 1            |
| `signed char`   | Signed single character      | 1            |
| `unsigned char` | Unsigned single character    | 1            |
| `wchar_t`       | Wide character (for Unicode) | 2 or 4       |
| `char16_t`      | UTF-16 character (C++11)     | 2            |
| `char32_t`      | UTF-32 character (C++11)     | 4            |
| `std:string` `std::basic_string<char>`    | UTF8 and ASCII| 1-4          |
| `std:wstring` `std::basic_string<wchar_t`   | UTF-16(win) UTF-32(linux)    |2(win)4(linux)|
---

#### 1.1.2.5 size

| Type        | Description                                               | Size (bytes)                   |
| ----------- | --------------------------------------------------------- | ------------------------------ |
| `size_t`    | Typically used for memory sizes and array indices         | 8 (on 64-bit) or 4 (on 32-bit) |
| `ssize_t`   | Signed version of `size_t` (used in certain OS libraries) | 8 (on 64-bit) or 4 (on 32-bit) |
| `ptrdiff_t` | Difference between two pointers                           | 8 (on 64-bit) or 4 (on 32-bit) |
---

#### 1.1.2.6 Other Types

| Type        | Description                                | Size (bytes)                   |
| ----------- | ------------------------------------------ | ------------------------------ |
| `bool`      | Boolean (true/false, typically 1 byte)     | 1                              |
| `nullptr_t` | Represents the `nullptr` constant in C++11 | 8 (on 64-bit) or 4 (on 32-bit) |

---

#### 1.1.2.7 Summary Of Common Types
* **Integer types**:

  * `char`, `unsigned char` = **1 byte**
  * `short`, `unsigned short` = **2 bytes**
  * `int`, `unsigned int`, `long`, `unsigned long` = **4 bytes** (typically, but `long` can be 8 bytes on some platforms like 64-bit Linux)
  * `long long`, `unsigned long long`, `int64_t`, `uint64_t` = **8 bytes**

* **Floating-point types**:

  * `float` = **4 bytes**
  * `double` = **8 bytes**
  * `long double` = typically **8**, **12**, or **16 bytes** depending on the platform

* **Character types**:

  * `char`, `unsigned char`, `signed char` = **1 byte**
  * `wchar_t`, `char16_t`, `char32_t` = typically **2**, **4**, or **4 bytes** (depends on platform)

* **Pointers**:

  * **8 bytes** (on a 64-bit system, can be 4 bytes on a 32-bit system)

* **Size and memory types**:

  * `size_t`, `ptrdiff_t` = **8 bytes** (on 64-bit)
  * `ssize_t` = **8 bytes** (on 64-bit)

* **string**:
  * `string`: `std::string` `std::basic_string<char>` = **1 to 4 bytes** UTF-8 with ASCII, sizeof() returns byte size not length
  * `wstring`: `std::wstring` `std::basic_string<wchar_t>` = **2(utf-16 on windows) to 4(utf32 on linux) bytes** 

--- 

### 1.1.3 Low-Level/Exploit-Relevant Types


#### 1.1.3.1 `std::uint8_t` (Fixed-width Unsigned 8-bit Integer)
#### 1.1.3.2 `std::uintptr_t` (Fixed-width Unsigned Integer for Pointers)


--- 

## 1.2 Type and Literal Basics

### 1.2.1 Literals
#### 1.2.1.1 Integer Literals
#### 1.2.1.2 Hex Literals
#### 1.2.1.3 Octal Literals
#### 1.2.1.4 Unsigned Literals
#### 1.2.1.5 Float Literals

--- 

### 1.2.2 Booleans
#### 1.2.2.1 bool
#### 1.2.2.2 true
#### 1.2.2.3 false (Representation: 1, 0)

--- 

### 1.2.3 Type Aliases
#### 1.2.3.1 typedef
#### 1.2.3.2 using

--- 

### 1.2.4 Enums
#### 1.2.4.1 enum Color
#### 1.2.4.2 std::to_underlying

--- 

## 1.3 Operators & Misc

### 1.3.1 String Manipulation
#### 1.3.1.1 std::string
#### 1.3.1.2 Concatenation
#### 1.3.1.3 .length()
#### 1.3.1.4 .size()
#### 1.3.1.5 .at(index)
#### 1.3.1.6 [index]
#### 1.3.1.7 getline
#### 1.3.1.8 std::toupper
#### 1.3.1.9 std::tolower
#### 1.3.1.10 std::towupper
#### 1.3.1.11 std::towlower
#### 1.3.1.12 std::stoi
#### 1.3.1.13 etc.

--- 

### 1.3.2 Operators
#### 1.3.2.1 Arithmetic Operators
#### 1.3.2.2 Comparison Operators
#### 1.3.2.3 Logical Operators (&&, ||, !)

--- 

### 1.3.3 Misc
#### 1.3.3.1 sizeof
#### 1.3.3.2 strlen
#### 1.3.3.3 typeid (RTTI)
#### 1.3.3.4 auto
#### 1.3.3.5 Overflow

--- 

## 1.4 Object Model & Evaluation Semantics

### 1.4.1 Storage Duration & Lifetime

#### 1.4.1.1 Automatic Storage Duration

#### 1.4.1.2 Static Storage Duration

#### 1.4.1.3 Dynamic Storage Duration

#### 1.4.1.4 Thread-Local Storage Duration

#### 1.4.1.5 Object Lifetime vs Storage Duration

---

### 1.4.2 Evaluation Order & Sequencing

#### 1.4.2.1 Order of Evaluation (Pre-C++17 vs C++17+)

#### 1.4.2.2 Sequence Points

#### 1.4.2.3 Short-Circuit Guarantees

#### 1.4.2.4 Undefined Behavior from Unsequenced Access

---

### 1.4.3 Endianness & Byte Order

#### 1.4.3.1 Little-endian vs Big-endian

#### 1.4.3.2 Network Byte Order

#### 1.4.3.3 std::endian (C++20)

#### 1.4.3.4 Manual Byte Swapping

---


# 2. Memory, Pointers, References & Casting

## 2.1 Pointers and References

### 2.1.1 Memory & Pointers
#### 2.1.1.1 Memory Addressing (&)
#### 2.1.1.2 Pointers (*)
#### 2.1.1.3 Dereference (*p)
#### 2.1.1.4 nullptr
#### 2.1.1.5 new
#### 2.1.1.6 delete
#### 2.1.1.7 delete[]

--- 

### 2.1.2 Raw Pointers (T*) and Pointer Arithmetic

### 2.1.3 References
#### 2.1.3.1 int& ref
#### 2.1.3.2 Call Site Reference
#### 2.1.3.3 Rvalue References (T&&)

--- 

### 2.1.4 Memory Layout and Alignment
#### 2.1.4.1 alignas
#### 2.1.4.2 alignof

--- 

## 2.2 Casting

### 2.2.1 Type Conversion
#### 2.2.1.1 Implicit Conversion
Performed automatically by the compiler when:
- Converting from **smaller → larger** type (int → long → float → double)
- Converting between compatible types  
- When mixing types in expressions (the “usual arithmetic conversions”)

Rules (simplified)
1. **Integer promotions**: `char`, `short` → `int`
2. If mixed types: result converts to the **largest** type in the expression.

```c
int a = 5;
double b = 2.5;
double c = a + b; // 'a' promoted to double automatically
```
---
#### 2.2.1.2 Explicit Conversion
Performed when you tell the compiler to manually convert.

Why Use Explicit Casts
1. When converting narrowing types (double → int)
2. To avoid warnings
3. To make intent clear
4. When dealing with pointers in low-level code (carefully)
---

### 2.2.2 Casting
#### Cpp-Style Casting
- static_cast – safe, compile-time checks
- reinterpret_cast – low-level, dangerous
- const_cast – removes const
- dynamic_cast – for polymorphism
---
#### C-Style Casting
```c
double d = 9.7;
int x = (int)d;   // truncates → 9
```
---
#### 2.2.2.1 static_cast
**Purpose:** Compile-time, safe, well-defined conversions.
**Use Cases**
- Numeric conversions
- Converting up/down within inheritance (downcasting must be correct)
- Removing ambiguity (e.g., void* → T*)
- Explicit constructor/conversion calls
---
```cpp
double d = 3.14;
int x = static_cast<int>(d);       // narrowing

Base* b = new Derived();
Derived* dptr = static_cast<Derived*>(b); // assumes b is actually Derived*
```
---

#### 2.2.2.2 dynamic_cast
Purpose: Safe downcasting with RTTI. Works only with polymorphic classes (has virtual functions).
Behavior
- Returns nullptr (for pointers) if cast is invalid
- Throws std::bad_cast (for references)
```cpp
struct Base { virtual ~Base(){} };
struct Derived : Base {};

Base* b = new Base();
Derived* d = dynamic_cast<Derived*>(b); // d == nullptr
```
---
#### 2.2.2.3 reinterpret_cast
Purpose: Low-level, bitwise reinterpretation.
Dangerous. No guarantee the result is meaningful.
Use cases
- Casting between unrelated pointer types
- Integer ↔ pointer conversions
- Very low-level systems code
```cpp
int x = 0x12345678;
char* p = reinterpret_cast<char*>(&x); // raw byte access
```
---
#### 2.2.2.4 const_cast
Purpose: Add/remove const or volatile.
Cannot remove constness of objects originally defined const.
```cpp 
void print(int* p) { *p = 10; }

const int a = 5;
print(const_cast<int*>(&a)); // UB: a is truly const
```
---
#### 2.2.2.5 std::bit_cast (C++20)
Purpose: Copy raw bits from one type to another of equal size.
No UB, unlike many reinterpret cast scenarios.
Requirements
- sizeof(T1) == sizeof(T2)
- Both must be trivially copyable.
```cpp 
#include <bit>
#include <cstdint>

float f = 1.0f;
uint32_t bits = std::bit_cast<uint32_t>(f); // read float's bit pattern
```
---
### 2.2.3 Type Casting (Exploit Context)

--- 

## 2.3 Memory Layout Internals

### 2.3.1 Stack Memory Internals

#### 2.3.1.1 Stack Frames

#### 2.3.1.2 Saved Return Address

#### 2.3.1.3 Base Pointer (RBP/EBP)

#### 2.3.1.4 Stack Alignment

#### 2.3.1.5 Red Zone (SysV ABI)

---

### 2.3.2 Heap Memory Internals

#### 2.3.2.1 Heap Metadata

#### 2.3.2.2 Free Lists and Bins

#### 2.3.2.3 Fragmentation

#### 2.3.2.4 Heap Grooming Concepts

---

### 2.3.3 Object Representation

#### 2.3.3.1 Padding and Alignment

#### 2.3.3.2 Struct Layout Guarantees

#### 2.3.3.3 Information Disclosure via Padding

---

### 2.3.4 Unions and Type Punning

#### 2.3.4.1 Union-based Type Punning

#### 2.3.4.2 Strict Aliasing Rules

#### 2.3.4.3 memcpy vs reinterpret_cast

#### 2.3.4.4 std::bit_cast as Safer Alternative

---

# 3. Control Flow & Functions

## 3.1 Control Flow and Loops

### 3.1.1 Control Flow
#### 3.1.1.1 if / else if / else
#### 3.1.1.2 switch (switch with strings via workarounds)
#### 3.1.1.3 Ternary Operator
#### 3.1.1.4 if constexpr

--- 

### 3.1.2 Loops
#### 3.1.2.1 for
#### 3.1.2.2 while
#### 3.1.2.3 do-while
#### 3.1.2.4 Range-Based for

--- 

### 3.1.3 Loop Control
#### 3.1.3.1 break
#### 3.1.3.2 continue

--- 

## 3.2 Functions and Parameters

### 3.2.1 Functions
#### 3.2.1.1 Definition
#### 3.2.1.2 Prototype
#### 3.2.1.3 void
#### 3.2.1.4 Free Functions

--- 

### 3.2.2 Parameters
#### 3.2.2.1 Pass by Value
#### 3.2.2.2 Pass by Reference (&)
#### 3.2.2.3 Default Parameters (Optional args)

--- 

### 3.2.3 Function Overloading
#### 3.2.3.1 Function Overloading (Different parameter types)
#### 3.2.3.2 Function Hiding & Overload Resolution

--- 

### 3.2.4 Function Pointers
#### 3.2.4.1 int (*funcPtr)(int, int)
#### 3.2.4.2 Callbacks

--- 

### 3.2.5 Recursion
#### 3.2.5.1 Factorial example

--- 

### 3.2.6 Scope
#### 3.2.6.1 Local Variables
#### 3.2.6.2 Global Variables

--- 

### 3.2.7 main
#### 3.2.7.1 int main()
#### 3.2.7.2 {...}
#### 3.2.7.3 return 0 / 1

--- 

## 3.3 I/O and Math

### 3.3.1 Input and Output
#### 3.3.1.1 #include <iostream>
#### 3.3.1.2 cout
#### 3.3.1.3 cin
#### 3.3.1.4 endl or '\n'

--- 

### 3.3.2 Common Math Functions
#### 3.3.2.1 sqrt
#### 3.3.2.2 pow
#### 3.3.2.3 floor
#### 3.3.2.4 ceil
#### 3.3.2.5 min()
#### 3.3.2.6 max()
#### 3.3.2.7 round()
#### 3.3.2.8 log()

--- 

### 3.3.3 Math (Header)
#### 3.3.3.1 #include <cmath>

--- 

## 3.4 ABI & Calling Conventions

### 3.4.1 Function Call Mechanics

#### 3.4.1.1 Function Prologue and Epilogue

#### 3.4.1.2 Parameter Passing (Registers vs Stack)

#### 3.4.1.3 Return Value Conventions

#### 3.4.1.4 Stack Cleanup Responsibility

---

### 3.4.2 ABI Stability

#### 3.4.2.1 Itanium ABI (Linux)

#### 3.4.2.2 MSVC ABI (Windows)

#### 3.4.2.3 ABI Breakage and Compatibility

---

# 4. Organization, Modifiers & Compile-Time

## 4.1 Organization and Linkage

### 4.1.1 Namespace
#### 4.1.1.1 using namespace
#### 4.1.1.2 :: Scope Resolution
#### 4.1.1.3 Nested (C++17+)

--- 

### 4.1.2 Using
#### 4.1.2.1 using namespace
#### 4.1.2.2 using std::cout
#### 4.1.2.3 Type Alias

--- 

### 4.1.3 Libraries
#### 4.1.3.1 #include
#### 4.1.3.2 <iostream>
#### 4.1.3.3 <cmath>
#### 4.1.3.4 <string>
#### 4.1.3.5 <vector>
#### 4.1.3.6 <algorithm>
#### 4.1.3.7 <typeinfo>
#### 4.1.3.8 Static Libraries
#### 4.1.3.9 Dynamic Libraries

--- 

### 4.1.4 Header
#### 4.1.4.1 One Definition Rule (ODR)
#### 4.1.4.2 Don't Repeat Yourself (DRY)

--- 

### 4.1.5 Modules (C++20)
#### 4.1.5.1 export module
#### 4.1.5.2 import
#### 4.1.5.3 module partition (Crucial for build times and ODR)

--- 

### 4.1.6 Compilation Model & Linking
#### 4.1.6.1 Preprocessor
#### 4.1.6.2 Translation Units
#### 4.1.6.3 static vs. extern
#### 4.1.6.4 Name Mangling
#### 4.1.6.5 Manual ABI Control (extern "C")

--- 

### 4.1.7 Macros

--- 

## 4.2 Modifiers and Attributes

### 4.2.1 Modifiers
#### 4.2.1.1 const
#### 4.2.1.2 static
#### 4.2.1.3 volatile
#### 4.2.1.4 mutable

--- 

### 4.2.2 Attributes
#### 4.2.2.1 [[nodiscard]]
#### 4.2.2.2 [[maybe_unused]]
#### 4.2.2.3 [[fallthrough]]
#### 4.2.2.4 [[likely]] (C++20)
#### 4.2.2.5 [[unlikely]] (C++20)

--- 

### 4.2.3 Const Correctness
#### 4.2.3.1 const on Variables
#### 4.2.3.2 const on Parameters
#### 4.2.3.3 const on Member Functions
#### 4.2.3.4 const T* p vs. T* const p

--- 

### 4.2.4 volatile
#### 4.2.4.1 Hardware Access
#### 4.2.4.2 Multi-threading

--- 

### 4.2.5 Global Variable
#### 4.2.5.1 extern const
#### 4.2.5.2 static constexpr
#### 4.2.5.3 inline constexpr

--- 

### 4.2.6 static
#### 4.2.6.1 Function variable persistence
#### 4.2.6.2 Class members
#### 4.2.6.3 File-scope linkage

--- 

### 4.2.7 inline
#### 4.2.7.1 Function (Optimization & ODR)
#### 4.2.7.2 Variable (ODR & Single Instance Guarantee)
#### 4.2.7.3 Nested Namespace

--- 

## 4.3 Compile-Time Features

### 4.3.1 constexpr
#### 4.3.1.1 constexpr Function (Implicitly inline)
#### 4.3.1.2 constexpr Variable

--- 

### 4.3.2 consteval
#### 4.3.2.1 consteval
#### 4.3.2.2 constinit

--- 

### 4.3.3 Compile-Time Programming
#### 4.3.3.1 Template Metaprogramming
#### 4.3.3.2 SFINAE
#### 4.3.3.3 Type Traits
#### 4.3.3.4 if constexpr

--- 

### 4.3.4 Compile-Time Utilities
#### 4.3.4.1 std::is_same_v
#### 4.3.4.2 std::enable_if_t
#### 4.3.4.3 Fold Expressions (C++17)
#### 4.3.4.4 Non-Type Template Parameters (C++20)

--- 

## 4.4 Binary & Object Files

### 4.4.1 Object Files

#### 4.4.1.1 .o / .obj Files

#### 4.4.1.2 Relocations

#### 4.4.1.3 Symbol Tables

---

### 4.4.2 Symbols and Visibility

#### 4.4.2.1 Static Symbols

#### 4.4.2.2 External Symbols

#### 4.4.2.3 Weak Symbols

#### 4.4.2.4 Symbol Resolution Order

---


# 5. Object-Oriented Programming (OOP)

## 5.1 Class Basics and Lifetime

### 5.1.1 Struct & Class Basics
#### 5.1.1.1 struct Point
#### 5.1.1.2 class Box
#### 5.1.1.3 public
#### 5.1.1.4 private
#### 5.1.1.5 protected

--- 

### 5.1.2 Constructor
#### 5.1.2.1 Default Constructor
#### 5.1.2.2 Overloaded Constructor
#### 5.1.2.3 Parameterized Constructor
#### 5.1.2.4 Explicit Constructor

--- 

### 5.1.3 Destructors

--- 

### 5.1.4 this
#### 5.1.4.1 this
#### 5.1.4.2 deducing this

--- 

### 5.1.5 Encapsulation
#### 5.1.5.1 Getter/Setter
#### 5.1.5.2 Encapsulation

--- 

### 5.1.6 friend

--- 

### 5.1.7 Object Lifetime
#### 5.1.7.1 Rule of Zero/Three/Five (Copy/Move/Destructor)

--- 

## 5.2 Inheritance and Polymorphism

### 5.2.1 Inheritance
#### 5.2.1.1 Single Inheritance
#### 5.2.1.2 Multilevel Inheritance
#### 5.2.1.3 Multiple Inheritance (class B : public A)
#### 5.2.1.4 Virtual Inheritance & Diamond Problem

--- 

### 5.2.2 Polymorphism
#### 5.2.2.1 virtual
#### 5.2.2.2 override

--- 

### 5.2.3 Interface
#### 5.2.3.1 Pure virtual functions (= 0)
#### 5.2.3.2 Virtual Destructor

--- 

## 5.3 Advanced Class Features

### 5.3.1 Internals
#### 5.3.1.1 VTables Structure and Usage
#### 5.3.1.2 VTable Overwrite Techniques (RE/Exploit Context)

--- 

### 5.3.2 Operator Overloading

--- 

### 5.3.3 Design Patterns
#### 5.3.3.1 Singleton
#### 5.3.3.2 Factory
#### 5.3.3.3 Observer
#### 5.3.3.4 Strategy
#### 5.3.3.5 RAII (key)

--- 

# 6. Advanced C++ & Idioms

## 6.1 Templates

### 6.1.1 Templates
#### 6.1.1.1 template <typename T>
#### 6.1.1.2 Function Templates
#### 6.1.1.3 Class Templates
#### 6.1.1.4 Template Specialization

--- 

### 6.1.2 Modern Templates
#### 6.1.2.1 Concepts (C++20)
#### 6.1.2.2 requires Clause

--- 

## 6.2 Exceptions and Lambdas

### 6.2.1 Exception Handling
#### 6.2.1.1 try
#### 6.2.1.2 catch
#### 6.2.1.3 throw
#### 6.2.1.4 std::exception
#### 6.2.1.5 noexcept
#### 6.2.1.6 Stack Unwinding

--- 

### 6.2.2 Lambda Expressions & Closures
#### 6.2.2.1 [](){}
#### 6.2.2.2 Init-Capture
#### 6.2.2.3 Syntax and Capture Lists ([], [=], [&])
#### 6.2.2.4 Anonymous Functions

--- 

## 6.3 Idioms and Semantics

### 6.3.1 RAII (Resource Acquisition Is Initialization)
#### 6.3.1.1 Resource Lifetime Management
#### 6.3.1.2 Scope-based Cleanup
#### 6.3.1.3 Destructor Guarantees

--- 

### 6.3.2 CRTP (Curiously Recurring Template Pattern)

--- 

### 6.3.3 Move Semantics
#### 6.3.3.1 Rvalue Glvalues Prvalues (value_cast)
#### 6.3.3.2 std::move
#### 6.3.3.3 Move Constructor
#### 6.3.3.4 Move Assignment Operator
#### 6.3.3.5 Algorithms and std library

--- 

### 6.3.4 Coroutines (C++20)
#### 6.3.4.1 co_await
#### 6.3.4.2 co_yield

--- 

## 6.4 Type Erasure

### 6.4.1 Type Erasure
#### 6.4.1.1 std::function (Type Erasure in Action)
#### 6.4.1.2 std::any / std::variant (Alternative Approaches)
#### 6.4.1.3 type erasure and performance tradeoffs

--- 

## 6.5 C++ ↔ Assembly Mapping

### 6.5.1 Compilation Output Analysis

#### 6.5.1.1 How Functions Compile to Assembly

#### 6.5.1.2 Stack Variables in Assembly

#### 6.5.1.3 Register Allocation Effects

---

### 6.5.2 Object-Oriented Constructs in Assembly

#### 6.5.2.1 Constructors and Destructors in Assembly

#### 6.5.2.2 Virtual Dispatch Mechanism

#### 6.5.2.3 Exception Tables (.eh_frame)

---

## 6.6 Standard Library Internals

### 6.6.1 Container Internals

#### 6.6.1.1 std::vector Growth Strategy

#### 6.6.1.2 Small String Optimization (SSO)

#### 6.6.1.3 Iterator Invalidation Rules

#### 6.6.1.4 Allocator Usage Patterns

---

# 7. Memory Management & Ownership

## 7.1 Dynamic Memory

### 7.1.1 Garbage Value Initialisation

--- 

### 7.1.2 Dynamic Memory
#### 7.1.2.1 new
#### 7.1.2.2 delete[]
#### 7.1.2.3 C-style (malloc/free)
#### 7.1.2.4 C++ Operators (new/delete)
#### 7.1.2.5 Placement New

--- 

## 7.2 Smart Pointers

### 7.2.1 Smart Pointers (Ownership)
#### 7.2.1.1 std::shared_pointer
#### 7.2.1.2 std::unique_pointer
#### 7.2.1.3 std::weak_ptr
#### 7.2.1.4 std::make_shared
#### 7.2.1.5 std::make_unique

--- 

## 7.3 Custom Allocation

### 7.3.1 Custom Allocators
#### 7.3.1.1 allocate method
#### 7.3.1.2 deallocate method
#### 7.3.1.3 STL Container Customization
#### 7.3.1.4 Hardened/Embedded Memory Pools

--- 

## 7.4 Memory Safety Tooling

### 7.4.1 Sanitizers

#### 7.4.1.1 AddressSanitizer (ASan)

#### 7.4.1.2 UndefinedBehaviorSanitizer (UBSan)

#### 7.4.1.3 MemorySanitizer (MSan)

#### 7.4.1.4 ThreadSanitizer (TSan)

---

# 8. Standard Template Library (STL) & Utilities

## 8.1 Containers

### 8.1.1 Containers
#### 8.1.1.1 std::vector
#### 8.1.1.2 std::map
#### 8.1.1.3 std::deque
#### 8.1.1.4 std::list
#### 8.1.1.5 std::set
#### 8.1.1.6 std::unordered_set
#### 8.1.1.7 std::unordered_map

--- 

### 8.1.2 Container Utilities
#### 8.1.2.1 push_back
#### 8.1.2.2 remove
#### 8.1.2.3 empty

--- 

### 8.1.3 Arrays
#### 8.1.3.1 Fixed size Arrays
#### 8.1.3.2 Multi-dimensional Arrays
#### 8.1.3.3 Range-based for for Arrays

--- 

## 8.2 Iterators and Views

### 8.2.1 Iterators & Ranges
#### 8.2.1.1 Iterator Categories
#### 8.2.1.2 begin()
#### 8.2.1.3 end()
#### 8.2.1.4 Range-based for loops
#### 8.2.1.5 Ranges (C++20)
#### 8.2.1.6 Custom Iterators

--- 

### 8.2.2 String/Buffer Views (C++17/20)
#### 8.2.2.1 std::string_view (Non-owning view of a string)
#### 8.2.2.2 std::span (Non-owning view of contiguous sequences)

--- 

## 8.3 Utilities and Error Handling

### 8.3.1 Error Handling/Flow (Value-based)
#### 8.3.1.1 std::expected
#### 8.3.1.2 std::optional

--- 

### 8.3.2 Error Handling/Flow (Heterogeneous)
#### 8.3.2.1 std::pair
#### 8.3.2.2 std::tuple
#### 8.3.2.3 std::variant
#### 8.3.2.4 std::visit
#### 8.3.2.5 std::monostate

--- 

### 8.3.3 Type Utilities
#### 8.3.3.1 std::to_underlying
#### 8.3.3.2 std::move
#### 8.3.3.3 std::reference_wrapper
#### 8.3.3.4 std::void
#### 8.3.3.5 std::any

--- 

### 8.3.4 Address Utilities
#### 8.3.4.1 std::addressof
#### 8.3.4.2 std::to_address

--- 

### 8.3.5 Timers
#### 8.3.5.1 std::chrono
#### 8.3.5.2 high_resolution_clock
#### 8.3.5.3 duration
#### 8.3.5.4 time_point

--- 

### 8.3.6 Random Function
#### 8.3.6.1 <random>
#### 8.3.6.2 std::random_device
#### 8.3.6.3 std::uniform_int_distribution
#### 8.3.6.4 std::mt19937

--- 

## 8.4 Algorithms and I/O

### 8.4.1 Algorithms (Deep Dive)
#### 8.4.1.1 sort
#### 8.4.1.2 reverse
#### 8.4.1.3 std::for_each
#### 8.4.1.4 std::transform
#### 8.4.1.5 std::accumulate
#### 8.4.1.6 equivalents in std::ranges (C++20)

--- 

### 8.4.2 Input/Output
#### 8.4.2.1 IO Streams (std::iostream, std::fstream)
#### 8.4.2.2 File Handling (ofstream, .close())

--- 

# 9. Concurrency & Multi-threading

## 9.1 Threading/Concurrency

### 9.1.1 std::thread

--- 

### 9.1.2 std::jthread

--- 

### 9.1.3 std::promise

--- 

### 9.1.4 std::async

--- 

## 9.2 Synchronization

### 9.2.1 std::mutex

--- 

### 9.2.2 std::lock_guard

--- 

### 9.2.3 std::scoped_lock

--- 

### 9.2.4 std::condition_variable

--- 

## 9.3 volatile

### 9.3.1 volatile (Multi-threading context)

--- 

## 9.4 Memory Model

### 9.4.1 C++ Memory Model

#### 9.4.1.1 Data Races

#### 9.4.1.2 Happens-Before Relationship

#### 9.4.1.3 Atomic Operations

#### 9.4.1.4 Memory Ordering (Relaxed, Acquire, Release, Seq-Cst)

---


# 10. Security, Low-Level & Exploit Development (OSCP/Advanced RE Context)

## 10.1 Low-Level & Architecture

### 10.1.1 Low-Level Types
#### 10.1.1.1 Byte-level payload (uint8_t, char)
#### 10.1.1.2 Port numbers / offsets (unsigned short)
#### 10.1.1.3 Shellcode length (const size_t)
#### 10.1.1.4 Memory address ops (void*, uintptr_t)

--- 

### 10.1.2 OS/Architecture Fundamentals
#### 10.1.2.1 Call Conventions: cdecl, stdcall, fastcall, vectorcall.
#### 10.1.2.2 Compiler Optimization Effects: -O1, -O2, -O3.
#### 10.1.2.3 PE/ELF File Format Internals: Sections (.text, .data, .bss), Imports/Exports.
#### 10.1.2.4 Process Memory Layout: Stack vs. Heap, ASLR effects
#### 10.1.2.5 Bit Manipulation: Bitwise Operators, Bit Shifting.

--- 

## 10.2 Defensive & Offensive Concepts

### 10.2.1 Undefined Behavior & Pitfalls (Defensive Study)
#### 10.2.1.1 Use-After-Free (UAF)
#### 10.2.1.2 Buffer Overflow (BOF)
#### 10.2.1.3 Signed Integer Overflow
#### 10.2.1.4 Dangling Pointers/References

--- 

### 10.2.2 Advanced Exploit Techniques (Conceptual/Defensive)
#### 10.2.2.1 VTable Overwrite
#### 10.2.2.2 ROP & Shellcode Integration
#### 10.2.2.3 Direct Syscalls
#### 10.2.2.4 Compile-Time String/Data Obfuscation
#### 10.2.2.5 Heap Exploitation Primitives
#### 10.2.2.6 Control-Flow Integrity (CFI)
#### 10.2.2.7 Anti-Debugging/Anti-VM

--- 

## 10.3 Memory Corruption Taxonomy

### 10.3.1 Stack-Based Vulnerabilities

#### 10.3.1.1 Stack Buffer Overflow

#### 10.3.1.2 Stack Pivoting

#### 10.3.1.3 Return Address Overwrite

---

### 10.3.2 Heap-Based Vulnerabilities

#### 10.3.2.1 Heap Buffer Overflow

#### 10.3.2.2 Use-After-Free

#### 10.3.2.3 Double Free

#### 10.3.2.4 Type Confusion

---

### 10.3.3 Integer Issues

#### 10.3.3.1 Integer Truncation

#### 10.3.3.2 Signedness Bugs

#### 10.3.3.3 Size Calculation Errors

---

## 10.4 Compiler & Binary Hardening

### 10.4.1 Mitigations

#### 10.4.1.1 Stack Canaries

#### 10.4.1.2 NX / DEP

#### 10.4.1.3 ASLR

#### 10.4.1.4 PIE

#### 10.4.1.5 RELRO (Partial / Full)

#### 10.4.1.6 Control Flow Guard (CFG)

---

### 10.4.2 Bypass Concepts (Defensive Study)

#### 10.4.2.1 Info Leaks

#### 10.4.2.2 ROP under Mitigations

#### 10.4.2.3 Heap Grooming for Bypass

---

## 10.5 Fuzzing & Dynamic Analysis

### 10.5.1 Fuzzing

#### 10.5.1.1 libFuzzer

#### 10.5.1.2 AFL++

#### 10.5.1.3 Coverage-Guided Fuzzing

#### 10.5.1.4 Fuzzing STL-heavy Code

---

## 10.6 Exception Handling Internals

### 10.6.1 Exception Runtime

#### 10.6.1.1 Stack Unwinding Tables

#### 10.6.1.2 Personality Functions

#### 10.6.1.3 Zero-Cost Exceptions

#### 10.6.1.4 SEH (Windows)

---


# 11. External Development, Debugging & Resources

## 11.1 Build and External Systems

### 11.1.1 Build System Mastery
#### 11.1.1.1 CMake (Modern Standard)
#### 11.1.1.2 FetchContent
#### 11.1.1.3 cross-compilation

--- 

### 11.1.2 Networking and IPC
#### 11.1.2.1 Boost.Asio
#### 11.1.2.2 Sockets
#### 11.1.2.3 Named Pipes
#### 11.1.2.4 Shared Memory

--- 

### 11.1.3 External Libraries
#### 11.1.3.1 Networking
#### 11.1.3.2 UI (C++ or C#)
#### 11.1.3.3 Abstraction

--- 

### 11.1.4 Compiler Support Portability

--- 

### 11.1.5 Serialization
#### 11.1.5.1 Serialization
#### 11.1.5.2 Cryptography

--- 

## 11.2 Tooling and Quality

### 11.2.1 Tooling (Deep Dive)
#### 11.2.1.1 Disassemblers/Decompilers: IDA Pro/Ghidra proficiency.
#### 11.2.1.2 System Call Tracing: strace (Linux), ProcMon/ApiMonitor (Windows).
#### 11.2.1.3 Debugging Tools: GDB, Valgrind, AddressSanitizer (-fsanitize=address).

--- 

### 11.2.2 Code Quality
#### 11.2.2.1 Clean C++ Code Writing
#### 11.2.2.2 Safe C++ Code Writing

--- 

## 11.3 Resources

### 11.3.1 Resources
#### 11.3.1.1 Cherno
#### 11.3.1.2 CppCon
#### 11.3.1.3 Jason Turner
#### 11.3.1.4 Low Level Learning

--- 
# 12. Undefined Behavior & Language Edge Cases

## 12.1 Undefined Behavior Fundamentals

### 12.1.1 Undefined vs Implementation-Defined vs Unspecified Behavior

### 12.1.2 Compiler Exploitation of Undefined Behavior (Optimizations)

---

## 12.2 Common Sources of Undefined Behavior

### 12.2.1 Strict Aliasing Violations

### 12.2.2 Object Lifetime Violations

### 12.2.3 Type Punning Undefined Behavior

### 12.2.4 Out-of-Bounds Pointer Arithmetic

### 12.2.5 One-Past-the-End Pointer Rules

### 12.2.6 Signed Integer Overflow

### 12.2.7 Uninitialized Reads

---

# 13. Name Mangling, Symbols & Reverse Engineering

## 13.1 Name Mangling

### 13.1.1 Itanium C++ ABI Name Mangling (Linux / macOS)

### 13.1.2 MSVC Name Mangling (Windows)

### 13.1.3 Template Name Mangling and Symbol Explosion

---

## 13.2 Demangling & Symbol Recovery

### 13.2.1 Demangling with c++filt

### 13.2.2 Demangling in IDA Pro

### 13.2.3 Demangling in Ghidra

---

## 13.3 RTTI-Related Symbols

### 13.3.1 type_info Symbols (_ZTI*)

### 13.3.2 VTable Symbols (_ZTV*)

### 13.3.3 Cross-Module RTTI Symbol Resolution

---

# 14. RTTI Internals & Type Identification

## 14.1 RTTI Runtime Structures

### 14.1.1 type_info Object Layout

### 14.1.2 RTTI Memory Placement

---

## 14.2 dynamic_cast Internals

### 14.2.1 dynamic_cast Implementation

### 14.2.2 dynamic_cast Across Inheritance Hierarchies

### 14.2.3 Cross-DSO dynamic_cast Behavior

---

## 14.3 RTTI Configuration & Abuse

### 14.3.1 RTTI Stripping (-fno-rtti)

### 14.3.2 Type Confusion via RTTI Misuse

---

# 15. C++ in ELF / PE Binaries

## 15.1 Initialization & Termination

### 15.1.1 .ctors / .dtors Sections

### 15.1.2 .init_array / .fini_array

### 15.1.3 Global Object Construction Order

---

## 15.2 Static Initialization Pitfalls

### 15.2.1 Static Initialization Order Fiasco

### 15.2.2 Cross-Translation Unit Initialization

---

## 15.3 Thread-Local Storage

### 15.3.1 TLS Sections (.tdata, .tbss)

### 15.3.2 Thread-Local Object Initialization

---

## 15.4 Virtual Tables in Binaries

### 15.4.1 VTable Placement in ELF

### 15.4.2 VTable Placement in PE

### 15.4.3 VTable Discovery During Reverse Engineering

---
# 16. Common Mistakes, Bugs, Tips & Optimization Techniques

## 16.1 Beginner Mistakes & Gotchas

### 16.1.1 Initialization Errors

#### 16.1.1.1 Uninitialized Variables

#### 16.1.1.2 Assuming Zero Initialization

#### 16.1.1.3 Most Vexing Parse

#### 16.1.1.4 Narrowing Conversions with {}

#### 16.1.1.5 Incorrect auto Type Deduction

---

### 16.1.2 Pointer & Reference Mistakes

#### 16.1.2.1 Dangling Pointers

#### 16.1.2.2 Returning References to Local Variables

#### 16.1.2.3 Misusing nullptr vs NULL

#### 16.1.2.4 Invalid Pointer Arithmetic

#### 16.1.2.5 Forgetting delete / delete[]

---

### 16.1.3 Object Lifetime & Ownership Errors

#### 16.1.3.1 Double Free

#### 16.1.3.2 Use-After-Free

#### 16.1.3.3 Copying Owning Raw Pointers

#### 16.1.3.4 Missing Virtual Destructors

#### 16.1.3.5 Incorrect Rule of Three/Five Implementation

---

### 16.1.4 STL Misuse (Beginner Level)

#### 16.1.4.1 Out-of-Bounds Access (operator[])

#### 16.1.4.2 Iterator Invalidation

#### 16.1.4.3 Assuming Contiguous Storage Where It’s Not

#### 16.1.4.4 Modifying Containers During Iteration

#### 16.1.4.5 Confusing size() with capacity()

---

## 16.2 Common Bugs to Avoid (All Levels)

### 16.2.1 Undefined Behavior Traps

#### 16.2.1.1 Signed Integer Overflow

#### 16.2.1.2 Strict Aliasing Violations

#### 16.2.1.3 Accessing Objects Outside Lifetime

#### 16.2.1.4 One-Past-the-End Pointer Dereference

#### 16.2.1.5 Unsequenced Modifications

---

### 16.2.2 Concurrency Bugs

#### 16.2.2.1 Data Races

#### 16.2.2.2 Deadlocks

#### 16.2.2.3 Double Locking

#### 16.2.2.4 Forgetting Memory Ordering

#### 16.2.2.5 False Sharing

---

### 16.2.3 ABI & Binary-Level Bugs

#### 16.2.3.1 Mismatched new/delete Across Modules

#### 16.2.3.2 ODR Violations Across Shared Libraries

#### 16.2.3.3 RTTI and Exception Boundary Issues

#### 16.2.3.4 Struct Layout Assumptions

#### 16.2.3.5 Calling Convention Mismatches

---

## 16.3 Tips & Tricks (Modern C++)

### 16.3.1 Language & Syntax Tips

#### 16.3.1.1 Prefer {} Initialization

#### 16.3.1.2 Use auto Without Losing Type Clarity

#### 16.3.1.3 Use constexpr Whenever Possible

#### 16.3.1.4 Prefer enum class Over enum

#### 16.3.1.5 Use [[nodiscard]] for Error-Prone APIs

---

### 16.3.2 STL & Utility Tips

#### 16.3.2.1 Prefer emplace_back Over push_back

#### 16.3.2.2 Use std::span and std::string_view Carefully

#### 16.3.2.3 Prefer Algorithms Over Raw Loops

#### 16.3.2.4 Use std::optional / std::expected for Flow Control

#### 16.3.2.5 Reserve Capacity to Avoid Reallocations

---

### 16.3.3 Safety & Maintainability Tips

#### 16.3.3.1 RAII Everywhere

#### 16.3.3.2 Avoid Raw new/delete in Application Code

#### 16.3.3.3 Prefer Value Semantics

#### 16.3.3.4 Minimize Global State

#### 16.3.3.5 Make Invariants Explicit

---

## 16.4 Performance Optimization Techniques

### 16.4.1 General Optimization Principles

#### 16.4.1.1 Measure First (Profilers Over Guessing)

#### 16.4.1.2 Avoid Premature Optimization

#### 16.4.1.3 Understand Algorithmic Complexity

#### 16.4.1.4 Cache Locality Awareness

#### 16.4.1.5 Data-Oriented Design Basics

---

### 16.4.2 Low-Level & Compiler-Aware Optimizations

#### 16.4.2.1 Inlining and Its Tradeoffs

#### 16.4.2.2 Move Semantics vs Copying

#### 16.4.2.3 Branch Prediction Hints ([[likely]] / [[unlikely]])

#### 16.4.2.4 Avoiding Unnecessary Virtual Dispatch

#### 16.4.2.5 constexpr and Compile-Time Evaluation

---

### 16.4.3 Memory & Allocation Optimizations

#### 16.4.3.1 Avoid Heap Allocations in Hot Paths

#### 16.4.3.2 Small Object Optimization Patterns

#### 16.4.3.3 Custom Allocators for Performance

#### 16.4.3.4 Object Pools

#### 16.4.3.5 False Sharing Avoidance (alignas, padding)

---

### 16.4.4 Performance Pitfalls (What Slows You Down)

#### 16.4.4.1 Accidental Copies

#### 16.4.4.2 Excessive Temporary Objects

#### 16.4.4.3 Cache Line Thrashing

#### 16.4.4.4 Overuse of std::shared_ptr

#### 16.4.4.5 Abusing Exceptions for Control Flow

---
