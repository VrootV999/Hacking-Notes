# 1. Core Language Fundamentals & Types

## 1.1 Initialisation & Data Types

### 1.1.1 Initialisation of Variables

```c
int x;              // Default: uninitialized (garbage value on stack)
int x = 10;         // Copy initialization
int x(10);          // Direct initialization (C++ style, NOT valid C)
int x = {10};       // Copy list initialization (C99)
int x = 0;          // Explicit zero initialization
int x{};            // NOT valid in C (C++ only)
```

---

### 1.1.2 Data Types Summary

#### 1.1.2.1 Integer Types

| Type | Description | Size (bytes) | Range (signed) |
|------|-------------|--------------|----------------|
| `char` | Single character | 1 | -128 to 127 |
| `unsigned char` | Unsigned character | 1 | 0 to 255 |
| `short` | Short integer | 2 | -32,768 to 32,767 |
| `unsigned short` | Unsigned short | 2 | 0 to 65,535 |
| `int` | Integer | 4 | -2,147,483,648 to 2,147,483,647 |
| `unsigned int` | Unsigned integer | 4 | 0 to 4,294,967,295 |
| `long` | Long integer | 4 or 8 | Depends on platform |
| `unsigned long` | Unsigned long | 4 or 8 | Depends on platform |
| `long long` | Long long integer | 8 | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| `unsigned long long` | Unsigned long long | 8 | 0 to 18,446,744,073,709,551,615 |
| `int8_t` | Fixed-width signed 8-bit | 1 | -128 to 127 |
| `uint8_t` | Fixed-width unsigned 8-bit | 1 | 0 to 255 |
| `int16_t` | Fixed-width signed 16-bit | 2 | -32,768 to 32,767 |
| `uint16_t` | Fixed-width unsigned 16-bit | 2 | 0 to 65,535 |
| `int32_t` | Fixed-width signed 32-bit | 4 | -2,147,483,648 to 2,147,483,647 |
| `uint32_t` | Fixed-width unsigned 32-bit | 4 | 0 to 4,294,967,295 |
| `int64_t` | Fixed-width signed 64-bit | 8 | -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 |
| `uint64_t` | Fixed-width unsigned 64-bit | 8 | 0 to 18,446,744,073,709,551,615 |

---

#### 1.1.2.2 Floating-Point Types

| Type | Description | Size (bytes) | Range |
|------|-------------|--------------|-------|
| `float` | Single precision | 4 | 1.5e-45 to 3.4e+38 |
| `double` | Double precision | 8 | 5.0e-324 to 1.7e+308 |
| `long double` | Extended precision | 8, 12, or 16 | Platform dependent |

---

#### 1.1.2.3 Pointer Types

| Type | Description | Size |
|------|-------------|------|
| `void*` | Generic pointer | 8 (64-bit) or 4 (32-bit) |
| `char*` | Pointer to char | 8 or 4 |
| `int*` | Pointer to int | 8 or 4 |
| `float*` | Pointer to float | 8 or 4 |
| `double*` | Pointer to double | 8 or 4 |
| `long*` | Pointer to long | 8 or 4 |
| `void (*)()` | Function pointer | 8 or 4 |

---

#### 1.1.2.4 char Types

| Type | Description | Size |
|------|-------------|------|
| `char` | Single character (may be signed or unsigned, implementation-defined) | 1 |
| `signed char` | Explicitly signed char | 1 |
| `unsigned char` | Explicitly unsigned char | 1 |
| `wchar_t` | Wide character (C95) | 2 or 4 |
| `char16_t` | UTF-16 (C11) | 2 |
| `char32_t` | UTF-32 (C11) | 4 |

---

#### 1.1.2.5 size_t and sizeof

```c
#include <stddef.h>
#include <stdint.h>

size_t x = sizeof(int);       // 4 on most platforms
size_t y = sizeof(void*);     // 8 on 64-bit, 4 on 32-bit

// size_t is unsigned, platform-dependent
// Use %zu for printf
printf("sizeof(int) = %zu\n", sizeof(int));
```

| Type | Description | Size |
|------|-------------|------|
| `size_t` | Unsigned integer type for sizes | 8 (64-bit) or 4 (32-bit) |
| `ssize_t` | Signed version of size_t | 8 or 4 |
| `ptrdiff_t` | Signed integer type for pointer differences | 8 or 4 |
| `intptr_t` | Signed integer type that can hold a pointer | 8 or 4 |
| `uintptr_t` | Unsigned integer type that can hold a pointer | 8 or 4 |

---

#### 1.1.2.6 Other Types

| Type | Description | Header |
|------|-------------|--------|
| `enum` | Enumeration type | - |
| `struct` | Structure type | - |
| `union` | Union type | - |
| `_Bool` | Boolean type (C99) | `<stdbool.h>` |
| `_Complex` | Complex number (C99) | `<complex.h>` |
| `FILE` | File stream | `<stdio.h>` |
| `va_list` | Variadic argument list | `<stdarg.h>` |

---

#### 1.1.2.7 Summary of Common Types on 64-bit Systems

| Type | Size (bytes) | Alignment |
|------|--------------|-----------|
| `char` | 1 | 1 |
| `short` | 2 | 2 |
| `int` | 4 | 4 |
| `long` | 8 | 8 |
| `long long` | 8 | 8 |
| `float` | 4 | 4 |
| `double` | 8 | 8 |
| `long double` | 16 | 16 |
| `void*` | 8 | 8 |
| `size_t` | 8 | 8 |

---

### 1.1.3 Low-Level/Exploit-Relevant Types

#### 1.1.3.1 `uint8_t` (Fixed-width Unsigned 8-bit Integer)

```c
#include <stdint.h>
uint8_t byte = 0xFF;  // Maximum value: 255
// Used for byte-level operations, network protocols, file formats
```

#### 1.1.3.2 `uintptr_t` (Fixed-width Unsigned Integer for Pointers)

```c
#include <stdint.h>
int x = 42;
uintptr_t addr = (uintptr_t)&x;  // Store pointer as integer
printf("Address: 0x%lx\n", addr);
```

#### 1.1.3.3 `_Bool` (Boolean Type)

```c
#include <stdbool.h>
bool flag = true;   // Actually _Bool, 1 byte
bool zero = false;  // 0
// Note: bool is just _Bool aliased by stdbool.h
```

---

## 1.2 Type and Literal Basics

### 1.2.1 Literals

#### 1.2.1.1 Integer Literals

##### 1.2.1.1.1 Hex Literals

```c
int hex = 0xFF;      // 255
int hex2 = 0X1A2B;   // 6699
```

##### 1.2.1.1.2 Octal Literals

```c
int oct = 077;       // 63 (leading zero = octal)
int oct2 = 0644;     // 420 (file permissions)
```

##### 1.2.1.1.3 Decimal Literals

```c
int dec = 42;
int neg = -100;
```

##### 1.2.1.1.4 Binary Literals (C23 / GCC Extension)

```c
int bin = 0b101010;  // 42 (C23 standard, GCC extension before)
int bin2 = 0B11110000;  // 240
```

---

#### 1.2.1.2 Floating-Point Literals

##### 1.2.1.2.1 Float Literals (Suffix: f or F)

```c
float f = 3.14f;
float g = 5.6e-3f;   // 0.0056
```

##### 1.2.1.2.2 Double Literals (Default)

```c
double d = 3.14;     // Default type for decimal
double e = 1.23e4;   // 12300.0
```

##### 1.2.1.2.3 Scientific Notation

```c
double large = 1.5e20;    // 1.5 * 10^20
double small = 3.0e-10;   // 3.0 * 10^-10
```

##### 1.2.1.2.4 Long Double Literals (Suffix: l or L)

```c
long double ld = 3.141592653589793238L;
```

---

#### 1.2.1.3 Integer Suffixes

```c
unsigned int u1 = 10U;         // unsigned
long l1 = 100L;                // long
unsigned long ul1 = 100UL;     // unsigned long
long long ll1 = 100LL;         // long long
unsigned long long ull1 = 100ULL; // unsigned long long
```

| Suffix | Type |
|--------|------|
| `u` or `U` | `unsigned int` |
| `l` or `L` | `long` |
| `ul` or `UL` | `unsigned long` |
| `ll` or `LL` | `long long` |
| `ull` or `ULL` | `unsigned long long` |

---

#### 1.2.1.4 Character Literals

```c
char c = 'A';           // ASCII 65
char nl = '\n';         // Newline
char null = '\0';       // Null character (0)
char backslash = '\\';  // Backslash
char tab = '\t';        // Tab
char oct = '\101';      // Octal: 'A'
char hex = '\x41';      // Hex: 'A'
// Wide characters (C95)
wchar_t wc = L'A';
// Unicode (C11)
char16_t c16 = u'A';
char32_t c32 = U'A';
```

---

#### 1.2.1.5 String Literals

```c
char* str = "Hello, World!";           // String literal (read-only in practice)
const char* str2 = "Hello";            // const is better practice
char arr[] = "Hello";                  // Modifiable array (6 bytes including \0)
char arr2[] = {'H','i','\0'};          // Equivalent, manual null terminator

// Multiline strings (not standard, but GCC extension)
// char* s = "line1" "line2";  // String concatenation (standard)

// Raw strings: NOT available in C (C++ only)
// Escape sequences
printf("Line1\nLine2\tTab\\\\Backslash\"Quote\'Apostrophe\n");
```

---

#### 1.2.1.6 Boolean Literals (C99)

```c
#include <stdbool.h>
bool t = true;   // Actually 1
bool f = false;  // Actually 0
// true is defined as 1, false as 0
// _Bool only stores 0 or 1 (any nonzero becomes 1)
```

---

#### 1.2.1.7 Digit Separators (C23)

```c
int million = 1'000'000;        // C23
double pi = 3.141'592'653;      // C23
int flags = 0xFF'AA'BB'CC;      // C23
```

---

#### 1.2.1.8 Binary Literals (C23)

```c
int b = 0b1010;    // 10
int b2 = 0B1111;   // 15
```

---

### 1.2.2 Booleans

#### 1.2.2.1 _Bool / bool

```c
#include <stdbool.h>
bool x = 1;    // true
bool y = 0;    // false
bool z = 42;   // true (any nonzero becomes 1)
// sizeof(bool) == 1
```

---

### 1.2.3 Type Aliases

#### 1.2.3.1 typedef

```c
typedef unsigned int uint;
typedef struct Point { int x, y; } Point;
typedef int (*FuncPtr)(int, int);

uint x = 10;
Point p = {1, 2};
FuncPtr fn = NULL;
```

---

#### 1.2.3.2 typedef vs #define

```c
typedef int* IntPtr;
#define INT_PTR int*

IntPtr a, b;    // Both are int* (correct)
INT_PTR c, d;   // c is int*, d is int (wrong! macro expansion)

// typedef is type-safe, #define is text substitution
```

---

### 1.2.4 Enums

#### 1.2.4.1 Enum Basics

```c
enum Color { RED, GREEN, BLUE };  // RED=0, GREEN=1, BLUE=2
enum Color c = RED;
printf("%d\n", c);  // 0
```

#### 1.2.4.2 Enum with Custom Values

```c
enum HttpStatus {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
};
// Values auto-increment: if STATUS_WARN not specified, next would be 501
```

#### 1.2.4.3 Enum Underlying Type

```c
enum Small : unsigned char { A, B, C };  // C++ only
// In C, enum size is implementation-defined (usually int)
// Use typedef for fixed size:
typedef unsigned char small_enum_t;
```

#### 1.2.4.4 Enum as Bitflags

```c
enum Flags {
    READ    = 1 << 0,  // 1
    WRITE   = 1 << 1,  // 2
    EXEC    = 1 << 2,  // 4
    ALL     = READ | WRITE | EXEC  // 7
};

int perms = READ | WRITE;
if (perms & READ) { /* has read */ }
if (perms & WRITE) { /* has write */ }
```

---

## 1.3 Operators & Misc

### 1.3.1 String Manipulation

#### 1.3.1.1 strlen

```c
#include <string.h>
size_t len = strlen("Hello");  // 5 (does not count \0)
```

#### 1.3.1.2 strcpy / strncpy

```c
char dst[20];
strcpy(dst, "Hello");                // Unsafe: no bounds check
strncpy(dst, "Hello", sizeof(dst)-1); // Safer but still imperfect
dst[sizeof(dst)-1] = '\0';          // Ensure null termination
```

#### 1.3.1.3 strcat / strncat

```c
char str[50] = "Hello";
strcat(str, " World");              // Unsafe
strncat(str, " World", sizeof(str) - strlen(str) - 1);  // Safer
```

#### 1.3.1.4 strcmp / strncmp

```c
int cmp = strcmp("abc", "abd");    // < 0 (c < d)
int cmp2 = strcmp("abc", "abc");   // 0 (equal)
int cmp3 = strcmp("abd", "abc");   // > 0
int ncmp = strncmp("abcdef", "abc", 3);  // 0 (first 3 match)
```

#### 1.3.1.5 strchr / strrchr

```c
char* p = strchr("Hello", 'l');    // Points to first 'l'
char* p2 = strrchr("Hello", 'l');  // Points to last 'l'
// Returns NULL if not found
```

#### 1.3.1.6 strstr

```c
char* p = strstr("Hello World", "World");  // Points to "World"
// Returns NULL if not found
```

#### 1.3.1.7 strtok

```c
char str[] = "Hello,World,How,Are,You";
char* token = strtok(str, ",");
while (token != NULL) {
    printf("%s\n", token);
    token = strtok(NULL, ",");  // Subsequent calls use NULL
}
// Modifies the original string (replaces delimiters with \0)
// NOT reentrant - not safe for multithreading
```

#### 1.3.1.8 sprintf / snprintf

```c
char buf[100];
sprintf(buf, "Name: %s, Age: %d", "Alice", 30);     // Unsafe
snprintf(buf, sizeof(buf), "Name: %s, Age: %d", "Alice", 30);  // Safe
```

#### 1.3.1.9 memcpy / memmove / memset / memcmp

```c
#include <string.h>
char src[] = "Hello";
char dst[10];
memcpy(dst, src, 6);           // Copy bytes (no overlap safety)
memmove(dst, src, 6);          // Copy bytes (handles overlap)
memset(dst, 'A', 10);          // Set bytes
int cmp = memcmp(dst, src, 5); // Compare bytes
```

---

### 1.3.2 Operators

#### 1.3.2.1 Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `3 + 2 = 5` |
| `-` | Subtraction | `3 - 2 = 1` |
| `*` | Multiplication | `3 * 2 = 6` |
| `/` | Division | `7 / 2 = 3` (integer) |
| `%` | Modulo | `7 % 2 = 1` |

```c
int a = 10 / 3;    // 3 (integer division truncates)
double b = 10.0 / 3;  // 3.333333...
int c = 10 % 3;    // 1
// Division by zero: UNDEFINED BEHAVIOR
// Integer overflow: UNDEFINED BEHAVIOR (signed)
// Unsigned overflow: wraps around (defined)
```

---

#### 1.3.2.2 Comparison Operators

| Operator | Description |
|----------|-------------|
| `==` | Equal to |
| `!=` | Not equal to |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal |
| `>=` | Greater than or equal |

---

#### 1.3.2.3 Logical Operators

| Operator | Description | Short-circuit |
|----------|-------------|---------------|
| `&&` | Logical AND | Yes |
| `\|\|` | Logical OR | Yes |
| `!` | Logical NOT | No |

```c
// Short-circuit evaluation
if (ptr != NULL && *ptr == 'A') {
    // Second operand not evaluated if ptr is NULL
}
```

---

#### 1.3.2.4 Bitwise Operators

| Operator | Description |
|----------|-------------|
| `&` | Bitwise AND |
| `\|` | Bitwise OR |
| `^` | Bitwise XOR |
| `~` | Bitwise NOT |
| `<<` | Left shift |
| `>>` | Right shift |

```c
int flags = 0;
flags |= (1 << 3);        // Set bit 3
flags &= ~(1 << 3);       // Clear bit 3
int toggled = flags ^ (1 << 3);  // Toggle bit 3
int is_set = (flags >> 3) & 1;   // Test bit 3
// Right shift of negative values: implementation-defined
// Left shift of negative values: undefined behavior
```

---

#### 1.3.2.5 Assignment Operators

```c
int x = 10;
x += 5;    // x = x + 5
x -= 3;    // x = x - 3
x *= 2;    // x = x * 2
x /= 4;    // x = x / 4
x %= 3;    // x = x % 3
x &= 0xFF; // x = x & 0xFF
x |= 0x10; // x = x | 0x10
x ^= 0x01; // x = x ^ 0x01
x <<= 2;   // x = x << 2
x >>= 1;   // x = x >> 1
```

---

#### 1.3.2.6 Ternary Operator

```c
int max = (a > b) ? a : b;
// condition ? value_if_true : value_if_false
```

---

#### 1.3.2.7 Comma Operator

```c
int x = (1, 2, 3);  // x = 3 (evaluates left to right, returns rightmost)
for (int i = 0, j = 10; i < j; i++, j--) { }
```

---

### 1.3.3 Misc

#### 1.3.3.1 sizeof

```c
printf("sizeof(char) = %zu\n", sizeof(char));       // Always 1
printf("sizeof(int) = %zu\n", sizeof(int));          // Usually 4
printf("sizeof(void*) = %zu\n", sizeof(void*));      // 8 on 64-bit

// sizeof is NOT a function - it's an operator
// evaluated at compile time (mostly)

// Array size
int arr[10];
size_t n = sizeof(arr) / sizeof(arr[0]);  // 10

// C11: sizeof can be applied to VLA (variable-length array)
int n = 10;
int vla[n];
size_t sz = sizeof(vla);  // n * sizeof(int)
```

---

#### 1.3.3.2 strlen vs sizeof

```c
char str[] = "Hello";
printf("sizeof = %zu\n", sizeof(str));  // 6 (includes \0)
printf("strlen = %zu\n", strlen(str));  // 5 (does not include \0)

char* ptr = "Hello";
printf("sizeof = %zu\n", sizeof(ptr));  // 8 (pointer size, NOT string length)
printf("strlen = %zu\n", strlen(ptr));  // 5
```

---

#### 1.3.3.3 Overflow

##### 1.3.3.3.1 Integer Overflow (Signed = UB)

```c
int x = INT_MAX;  // 2,147,483,647
x += 1;           // UNDEFINED BEHAVIOR (signed overflow)

unsigned int y = UINT_MAX;
y += 1;           // Defined: wraps to 0
```

##### 1.3.3.3.2 Floating-Point Overflow

```c
double x = 1.7e308;
x *= 10;          // Becomes INFINITY (defined)
```

##### 1.3.3.3.3 Preventing Overflow

```c
#include <limits.h>
#include <stdbool.h>

bool add_overflow(int a, int b, int* result) {
    if (a > 0 && b > INT_MAX - a) return true;  // overflow
    if (a < 0 && b < INT_MIN - a) return true;  // underflow
    *result = a + b;
    return false;
}
// C23: has_support/__builtin_add_overflow
```

---

#### 1.3.3.4 Typeof (C11 / C23)

```c
// C11: _Generic
// C23: typeof and typeof_unqual
int x = 42;
typeof(x) y = 10;      // C23
typeof_unqual(x) z = 5; // C23: removes qualifiers
```

---

## 1.4 Object Model & Evaluation Semantics

### 1.4.1 Storage Duration & Lifetime

#### 1.4.1.1 Automatic Storage Duration

```c
void func() {
    int x = 10;          // Automatic: lives until scope ends
    {
        int y = 20;      // Automatic: lives until inner scope ends
    }  // y is destroyed here
}  // x is destroyed here
// Stack-allocated, fast, LIFO order
```

#### 1.4.1.2 Static Storage Duration

```c
static int count = 0;   // File-scope static: lives for entire program
void func() {
    static int calls = 0;  // Function-scope static: initialized once
    calls++;               // Persists across calls
}
// Zero-initialized before main() starts
```

#### 1.4.1.3 Dynamic Storage Duration

```c
int* p = malloc(sizeof(int));  // Heap-allocated
*p = 42;
free(p);  // Must free manually
// Lives until explicitly freed (or program ends)
```

#### 1.4.1.4 Thread-Local Storage (C11)

```c
#include <threads.h>
_Thread_local int tls_var = 0;  // Each thread has its own copy
// Or: __thread (GCC extension)
```

---

### 1.4.2 Evaluation Order & Sequencing

#### 1.4.2.1 Order of Evaluation

```c
int x = 0;
int y = x++ + x++;  // UNDEFINED BEHAVIOR
// The order of evaluation of operands is unspecified

// Safe:
int a = 1;
int b = 2;
int c = a + b;  // a and b are independent, no UB
```

#### 1.4.2.2 Sequence Points

```c
// Sequence points occur at:
// ; (end of full expression)
// && || ?: , (as operators)
// After first operand of && and ||
// Before function call, after arguments are evaluated
// At return

// These create sequence points:
x = 5;           // sequence point after
f(a++, b++);     // sequence point after function call
if (a) b = 1;    // sequence point after condition evaluation
```

#### 1.4.2.3 Short-Circuit Guarantees

```c
if (ptr != NULL && *ptr != 0) {
    // *ptr not evaluated if ptr is NULL
}

if (x != 0 && y / x > 1) {
    // Division by x not evaluated if x is 0
}
```

---

### 1.4.3 Endianness & Byte Order

#### 1.4.3.1 Little-endian vs Big-endian

```c
// Little-endian: Least significant byte first (x86, x64)
// Big-endian: Most significant byte first (network byte order, some ARMs)

#include <stdint.h>
uint32_t val = 0x12345678;
uint8_t* bytes = (uint8_t*)&val;
// Little-endian: bytes = [0x78, 0x56, 0x34, 0x12]
// Big-endian:    bytes = [0x12, 0x34, 0x56, 0x78]
```

#### 1.4.3.2 Network Byte Order

```c
#include <arpa/inet.h>

uint32_t host = 0x12345678;
uint32_t network = htonl(host);  // Host to network long
uint32_t back = ntohl(network);  // Network to host long
uint16_t port = htons(8080);     // Host to network short
uint16_t host_port = ntohs(port); // Network to host short
```

#### 1.4.3.3 Manual Byte Swapping

```c
#include <stdint.h>

uint32_t swap32(uint32_t x) {
    return ((x & 0xFF) << 24) |
           ((x & 0xFF00) << 8) |
           ((x >> 8) & 0xFF00) |
           ((x >> 24) & 0xFF);
}

uint16_t swap16(uint16_t x) {
    return (x >> 8) | (x << 8);
}

// GCC builtins:
uint32_t swapped = __builtin_bswap32(0x12345678);  // 0x78563412
uint16_t swapped16 = __builtin_bswap16(0x1234);     // 0x3412
uint64_t swapped64 = __builtin_bswap64(0x0102030405060708ULL);
```

---

# 2. Memory, Pointers & Casting

## 2.1 Pointers and References

### 2.1.1 Memory & Pointers

#### 2.1.1.1 Memory Addressing (&)

```c
int x = 42;
printf("Address of x: %p\n", (void*)&x);  // e.g., 0x7fff5a3b
printf("Value at address: %d\n", x);
```

#### 2.1.1.2 Pointers (*)

```c
int x = 42;
int* p = &x;       // p stores address of x
printf("%d\n", *p); // 42 (dereference)
```

#### 2.1.1.3 Dereference (*p)

```c
int x = 10;
int* p = &x;
*p = 20;            // Modify x through pointer
printf("%d\n", x); // 20
```

#### 2.1.1.4 NULL

```c
#include <stddef.h>
int* p = NULL;      // NULL pointer (points to nothing)
// p = 0;           // Also NULL
// Dereferencing NULL: UNDEFINED BEHAVIOR (usually segfault)
if (p != NULL) { *p; }
```

#### 2.1.1.5 void*

```c
void* generic = malloc(100);  // Can hold any pointer type
int* int_ptr = (int*)generic;  // Must cast to use
char* str_ptr = (char*)generic;
// Cannot dereference void* directly
// Cannot do pointer arithmetic on void*
```

---

### 2.1.2 Pointer Arithmetic

```c
int arr[5] = {10, 20, 30, 40, 50};
int* p = arr;       // Points to arr[0]

p + 1;              // Points to arr[1] (advances by sizeof(int) = 4 bytes)
p + 2;              // Points to arr[2] (advances by 8 bytes)

*(p + 2);           // 30 (same as arr[2])
p[2];               // 30 (array subscript is syntactic sugar for *(p+2))

// Pointer difference
ptrdiff_t diff = &arr[4] - &arr[0];  // 4
```

#### 2.1.2.1 Pointer Arithmetic Rules

```c
// Valid operations:
// ptr + integer
// ptr - integer
// ptr - ptr (same array only)
// ptr == ptr, ptr != ptr
// ptr < ptr, ptr > ptr (same array only)

// Invalid operations:
// ptr + ptr (INVALID)
// ptr * integer (INVALID)
// ptr / integer (INVALID)
// Comparing pointers from different arrays (UNDEFINED)
```

---

### 2.1.3 Arrays and Pointers

```c
int arr[5] = {1, 2, 3, 4, 5};
int* p = arr;      // Array decays to pointer to first element

// sizeof differences
sizeof(arr);  // 20 (5 * sizeof(int))
sizeof(p);    // 8 (pointer size on 64-bit)

// They are NOT the same type!
// arr is int[5], p is int*
```

#### 2.1.3.1 Array Decay

```c
void func(int arr[]) {      // Actually receives int*
    printf("sizeof = %zu\n", sizeof(arr));  // 8 (pointer!)
}

void func2(int arr[5]) {    // Same thing: receives int*
    printf("sizeof = %zu\n", sizeof(arr));  // 8 (pointer!)
}

void func3(int (*arr)[5]) { // Receives pointer to array of 5 ints
    printf("sizeof = %zu\n", sizeof(*arr));  // 20 (actual array)
}
```

---

### 2.1.4 Multi-Dimensional Arrays and Pointers

```c
int arr[3][4];             // 2D array: 3 rows, 4 columns
int (*p)[4] = arr;         // Pointer to array of 4 ints

// Accessing
arr[1][2] = 42;
*(*(arr + 1) + 2) = 42;   // Equivalent

// Array of pointers
int* rows[3];              // Array of 3 int pointers
rows[0] = malloc(4 * sizeof(int));
```

---

### 2.1.5 Function Pointers

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int (*op)(int, int) = add;  // Function pointer
printf("%d\n", op(3, 4));   // 7

op = sub;
printf("%d\n", op(3, 4));   // -1

// Typedef for cleaner syntax
typedef int (*BinaryOp)(int, int);
BinaryOp operations[] = {add, sub};
```

---

### 2.1.6 const and Pointers

```c
const int* p1;        // Pointer to const int: *p1 = 5 (INVALID)
int const* p2;        // Same as above
int* const p3 = &x;   // Const pointer: p3 = &y (INVALID)
const int* const p4 = &x;  // Both const
```

---

### 2.1.7 restrict Keyword (C99)

```c
// Promise that pointers don't alias (enables optimization)
void copy(int* restrict dst, const int* restrict src, size_t n) {
    for (size_t i = 0; i < n; i++)
        dst[i] = src[i];  // Compiler can optimize assuming no overlap
}
// If they DO overlap: UNDEFINED BEHAVIOR
```

---

## 2.2 Casting

### 2.2.1 Implicit Conversion

```c
int i = 42;
double d = i;       // int -> double (widening, safe)
char c = 65;        // int -> char (narrowing, potential data loss)
int x = 3.14;       // double -> int (truncation, warning)
```

### 2.2.2 Explicit Conversion (C-style Cast)

```c
double d = 3.14;
int i = (int)d;        // 3 (truncates)
void* p = malloc(100);
int* ip = (int*)p;     // Cast void* to int*
char c = (char)256;    // 0 (overflow)
```

### 2.2.3 Casting Safety Levels

| Cast | Safety | Use Case |
|------|--------|----------|
| Implicit | Safe | Widening conversions |
| (int)d | Warning | Truncation, narrowing |
| (void*)p | Warning | Pointer type changes |
| (int*)p | Dangerous | Reinterpreting memory |
| *(int*)&f | Very Dangerous | Type punning |

---

## 2.3 Memory Layout Internals

### 2.3.1 Stack Memory Internals

```c
void func(int a, int b) {
    int local = 42;
    // Stack grows downward on x86/x64
    // Higher addresses
    // +------------------+
    // | return address   |  <- RBP points here (after prologue)
    // +------------------+
    // | saved RBP        |
    // +------------------+
    // | local variable   |  <- RSP points here
    // +------------------+
    // Lower addresses
}
```

#### 2.3.1.1 Stack Frames

```c
// Function call sequence (x86-64 System V ABI):
// 1. Push arguments (or pass in registers: RDI, RSI, RDX, RCX, R8, R9)
// 2. CALL instruction (pushes return address, jumps to function)
// 3. Function prologue: push rbp; mov rbp, rsp; sub rsp, N
// 4. Function body
// 5. Function epilogue: mov rsp, rbp; pop rbp; ret
```

#### 2.3.1.2 Saved Return Address

```c
// Stack buffer overflow overwrites return address
// Control flow hijacked when function returns
// Classic buffer overflow exploitation target
```

#### 2.3.1.3 Base Pointer (RBP/EBP)

```c
// RBP = frame pointer (if not optimized out)
// Function parameters at [RBP+16], [RBP+24], etc.
// Local variables at [RBP-8], [RBP-16], etc.
// With -fomit-frame-pointer: RSP used directly
```

#### 2.3.1.4 Stack Alignment

```c
// x86-64: 16-byte alignment required before CALL
// Red zone: 128 bytes below RSP (SysV ABI) for leaf functions
// -mno-red-zone disables red zone
```

---

### 2.3.2 Heap Memory Internals

#### 2.3.2.1 Heap Metadata

```c
// malloc implementations store metadata before allocated block
// glibc (ptmalloc): size field + flags in previous chunk's size field
// Each chunk has: size | prev_size | user_data...
// Size is always a multiple of 16 (on 64-bit)
```

#### 2.3.2.2 Free Lists and Bins

```c
// glibc bins:
// Fast bins: small chunks (<= 0x80), singly-linked, LIFO
// Small bins: <= 0x410, doubly-linked, FIFO
// Large bins: > 0x410, doubly-linked, size-ordered
// Unsorted bin: recently freed chunks (temporary)
// Tcache: per-thread cache (glibc 2.26+), singly-linked, LIFO
```

#### 2.3.2.3 Fragmentation

```c
// External fragmentation: free chunks scattered, not contiguous
// Internal fragmentation: wasted space within allocated chunks
// Mitigation: memory pools, custom allocators
```

---

### 2.3.3 Object Representation

#### 2.3.3.1 Padding and Alignment

```c
struct Padded {
    char a;     // 1 byte + 3 bytes padding
    int b;      // 4 bytes
    char c;     // 1 byte + 3 bytes padding (to align struct to 4 bytes)
};              // Total: 12 bytes (not 6!)

struct Unpadded {
    int b;      // 4 bytes
    char a;     // 1 byte
    char c;     // 1 byte + 2 bytes padding
};              // Total: 8 bytes

// Use __attribute__((packed)) to remove padding:
struct __attribute__((packed)) Packed {
    char a;     // 1 byte
    int b;      // 4 bytes
    char c;     // 1 byte
};              // Total: 6 bytes (but slower access!)
```

---

### 2.3.4 Type Punning

#### 2.3.4.1 Union-based Type Punning

```c
union FloatInt {
    float f;
    uint32_t i;
};

union FloatInt fi;
fi.f = 3.14f;
printf("Bits: 0x%08X\n", fi.i);  // Read as integer (type punning)
// Legal in C (but not in C++)
```

#### 2.3.4.2 Strict Aliasing Rules

```c
// You cannot access an object through an incompatible type
int x = 42;
float* fp = (float*)&x;  // UNDEFINED BEHAVIOR (strict aliasing violation)
*fp = 3.14f;              // Compiler may optimize assuming x and *fp don't alias

// Exception: char* can alias anything
char* cp = (char*)&x;     // OK (but still UB to write if it changes the type)
```

#### 2.3.4.3 memcpy for Type Punning (Safe)

```c
int x = 42;
float f;
memcpy(&f, &x, sizeof(f));  // Safe type punning
printf("%f\n", f);
// Compiler handles this correctly, no strict aliasing violation
```

#### 2.3.4.4 Restrict and Aliasing

```c
// restrict promises no aliasing
// Violating restrict: UNDEFINED BEHAVIOR
void add(int* restrict a, int* restrict b, int* result) {
    *result = *a + *b;
}
// add(&x, &x, &y);  // UB: a and b alias
```

---

# 3. Control Flow & Functions

## 3.1 Control Flow and Loops

### 3.1.1 Control Flow

#### 3.1.1.1 if / else if / else

```c
if (x > 0) {
    // positive
} else if (x < 0) {
    // negative
} else {
    // zero
}
```

#### 3.1.1.2 switch

```c
switch (value) {
    case 1:
        printf("One\n");
        break;
    case 2:
        printf("Two\n");
        break;
    default:
        printf("Other\n");
        break;
}
// Without break: fall-through to next case
// Case must be constant expression
// Duplicate cases: compilation error
```

#### 3.1.1.3 Ternary Operator

```c
int max = (a > b) ? a : b;
```

#### 3.1.1.4 Nested if

```c
if (a > 0) {
    if (b > 0) {
        // both positive
    } else {
        // a positive, b non-positive
    }
}
// Dangling else: else binds to nearest unmatched if
```

---

### 3.1.2 Loops

#### 3.1.2.1 for

```c
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}
// for (init; condition; update) body
// All three parts are optional: for (;;) is infinite loop
```

#### 3.1.2.2 while

```c
int i = 0;
while (i < 10) {
    printf("%d\n", i);
    i++;
}
```

#### 3.1.2.3 do-while

```c
int i = 0;
do {
    printf("%d\n", i);
    i++;
} while (i < 10);  // Always executes at least once
```

#### 3.1.2.4 Nested Loops

```c
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        printf("(%d,%d) ", i, j);
    }
}
```

---

### 3.1.3 Loop Control

#### 3.1.3.1 break

```c
while (1) {
    int c = getchar();
    if (c == EOF) break;  // Exit loop
}
// Break only exits the innermost loop
```

#### 3.1.3.2 continue

```c
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0) continue;  // Skip even numbers
    printf("%d\n", i);         // Prints odd numbers only
}
```

#### 3.1.3.3 goto

```c
// Use sparingly - mainly for multi-level break/continue or cleanup
for (int i = 0; i < 10; i++) {
    for (int j = 0; j < 10; j++) {
        if (found) goto done;  // Break out of nested loops
    }
}
done:
    printf("Found!\n");

// Cleanup pattern (common in Linux kernel)
int* a = malloc(100);
if (!a) goto fail_a;
int* b = malloc(200);
if (!b) goto fail_b;
// ... use a and b ...
free(b);
fail_b:
    free(a);
fail_a:
    return -1;
```

---

## 3.2 Functions and Parameters

### 3.2.1 Function Basics

```c
// Declaration (prototype)
int add(int a, int b);

// Definition
int add(int a, int b) {
    return a + b;
}

// No return value
void print_hello(void) {
    printf("Hello\n");
}
// void means: takes no arguments (not "no parameters")
// func() in C means unspecified arguments (NOT no arguments)
// Always use (void) for no parameters
```

---

### 3.2.2 Parameters

#### 3.2.2.1 Pass by Value

```c
void modify(int x) {
    x = 100;  // Only modifies local copy
}
int main() {
    int a = 5;
    modify(a);   // a is still 5
}
```

#### 3.2.2.2 Pass by Pointer

```c
void modify(int* x) {
    *x = 100;  // Modifies original value
}
int main() {
    int a = 5;
    modify(&a);  // a is now 100
}
```

#### 3.2.2.3 Default Parameters

```c
// NOT available in C (C++ feature)
// Workaround: use macros or check for sentinel values
void func(int x, int y /* = 0 */) {
    // Use y
}
// Caller must always pass both arguments
```

---

### 3.2.3 Function Overloading

```c
// NOT available in C (C++ feature)
// Workaround: use _Generic (C11) or different function names
int add_int(int a, int b) { return a + b; }
double add_double(double a, double b) { return a + b; }

// C11 _Generic alternative:
#define ADD(a, b) _Generic((a), \
    int: add_int, \
    double: add_double \
)(a, b)
```

---

### 3.2.4 Recursion

```c
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// Tail recursion (compiler may optimize to loop)
int factorial_tail(int n, int acc) {
    if (n <= 1) return acc;
    return factorial_tail(n - 1, n * acc);
}
// gcc -O2 -ftail-call-optimization enables TCO
```

---

### 3.2.5 Scope

#### 3.2.5.1 Local Variables

```c
void func() {
    int x = 10;          // Local to func
    {
        int y = 20;      // Local to inner block
    }
    // y is not accessible here
}
```

#### 3.2.5.2 Global Variables

```c
int global = 42;           // Global variable
static int file_scope = 1; // File-scope static (internal linkage)

extern int external_var;    // Declaration (defined elsewhere)

void func() {
    extern int another_var; // Can also declare extern inside function
}
```

---

### 3.2.6 main

```c
int main(void) { return 0; }         // Standard
int main(int argc, char* argv[]) { }  // With arguments
// argv[0] = program name
// argv[1..argc-1] = arguments
// argc = argument count

// argc/argv example:
int main(int argc, char* argv[]) {
    for (int i = 0; i < argc; i++)
        printf("argv[%d] = %s\n", i, argv[i]);
}
```

---

## 3.3 I/O and Math

### 3.3.1 Input and Output

#### 3.3.1.1 #include <stdio.h>

```c
#include <stdio.h>  // printf, scanf, fprintf, fopen, etc.
```

#### 3.3.1.2 printf

```c
printf("Hello, %s! Age: %d\n", "Alice", 30);

// Format specifiers:
// %d / %i  - signed int
// %u       - unsigned int
// %f       - double (default precision: 6)
// %e       - scientific notation
// %g       - shortest of %f and %e
// %c       - char
// %s       - string
// %p       - void* (pointer)
// %x       - unsigned hex (lowercase)
// %X       - unsigned hex (uppercase)
// %o       - unsigned octal
// %zu      - size_t
// %ld      - long
// %lld     - long long
// %%       - literal '%'

// Width and precision
printf("%10d\n", 42);        // "        42" (right-aligned, width 10)
printf("%-10d\n", 42);       // "42        " (left-aligned)
printf("%.2f\n", 3.14159);   // "3.14" (2 decimal places)
printf("%08x\n", 255);       // "000000ff" (zero-padded)
printf("%+d\n", 42);         // "+42" (show sign)
```

#### 3.3.1.3 scanf

```c
int x;
scanf("%d", &x);  // Read integer

char str[100];
scanf("%99s", str);  // Read string (limit width to prevent overflow)

float f;
scanf("%f", &f);  // Read float

int a, b;
scanf("%d %d", &a, &b);  // Read two integers

// Return value: number of items successfully read
// Always check return value!
if (scanf("%d", &x) != 1) {
    fprintf(stderr, "Invalid input\n");
}
```

#### 3.3.1.4 fgets (safer than scanf for strings)

```c
char buf[100];
if (fgets(buf, sizeof(buf), stdin) != NULL) {
    // buf includes trailing newline if there's room
    buf[strcspn(buf, "\n")] = '\0';  // Remove newline
}
// fgets reads at most sizeof(buf)-1 characters + null terminator
```

---

### 3.3.2 Common Math Functions

#### 3.3.2.1 sqrt

```c
#include <math.h>
double result = sqrt(16.0);  // 4.0
```

#### 3.3.2.2 pow

```c
double result = pow(2.0, 10.0);  // 1024.0
```

#### 3.3.2.3 floor / ceil

```c
double f = floor(3.7);  // 3.0
double c = ceil(3.2);   // 4.0
```

#### 3.3.2.4 fabs (absolute value for floats)

```c
double a = fabs(-3.14);  // 3.14
int b = abs(-42);        // 42 (from stdlib.h, for ints only)
```

#### 3.3.2.5 round

```c
double r1 = round(2.5);   // 3.0
double r2 = round(2.4);   // 2.0
double r3 = trunc(2.7);   // 2.0 (toward zero)
double r4 = rint(2.5);    // 2.0 or 3.0 (rounds to nearest, ties to even)
```

#### 3.3.2.6 min / max (No Standard Macro)

```c
// C doesn't have standard min/max (conflicts with macros)
// Safe alternatives:
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))
// Or use inline functions (type-safe):
static inline int max_int(int a, int b) { return a > b ? a : b; }
```

---

### 3.3.3 cmath / math.h Deep Dive

#### 3.3.3.1 Mathematical Constants

```c
#include <math.h>
// M_PI       = 3.14159265358979323846
// M_E        = 2.71828182845904523536
// M_LN2      = 0.69314718055994530942
// M_LN10     = 2.30258509299404568402
// INFINITY   = infinity
// NAN        = quiet NaN
// HUGE_VAL   = large finite value
```

#### 3.3.3.2 Trigonometric Functions

```c
double sin_val = sin(M_PI / 2);   // 1.0
double cos_val = cos(0);           // 1.0
double tan_val = tan(M_PI / 4);   // 1.0
double asin_val = asin(1.0);       // M_PI/2
double acos_val = acos(1.0);       // 0.0
double atan_val = atan(1.0);       // M_PI/4
double atan2_val = atan2(1.0, 1.0); // M_PI/4
```

#### 3.3.3.3 Hyperbolic Functions

```c
double sinh_val = sinh(1.0);
double cosh_val = cosh(1.0);
double tanh_val = tanh(1.0);
```

#### 3.3.3.4 Exponential and Logarithmic Functions

```c
double exp_val = exp(1.0);     // e^1
double log_val = log(M_E);     // 1.0 (natural log)
double log2_val = log2(8.0);   // 3.0
double log10_val = log10(100); // 2.0
double exp2_val = exp2(3.0);   // 8.0
```

#### 3.3.3.5 Power Functions

```c
double pow_val = pow(2.0, 10.0);    // 1024.0
double sqrt_val = sqrt(16.0);        // 4.0
double cbrt_val = cbrt(27.0);        // 3.0
double hypot_val = hypot(3.0, 4.0);  // 5.0
```

#### 3.3.3.6 Rounding Functions

```c
double floor_val = floor(3.7);   // 3.0
double ceil_val = ceil(3.2);     // 4.0
double trunc_val = trunc(3.9);   // 3.0
double round_val = round(3.5);   // 4.0
// lround, llround return long/long long
```

#### 3.3.3.7 Floating-Point Classification

```c
#include <math.h>
isfinite(1.0);     // true
isinf(INFINITY);   // true
isnan(NAN);        // true
signbit(-1.0);     // true (negative)
fpclassify(x) == FP_NORMAL;  // etc.
```

---

### 3.3.4 File I/O

```c
#include <stdio.h>

// Opening files
FILE* f = fopen("file.txt", "r");   // read
FILE* f = fopen("file.txt", "w");   // write (truncate)
FILE* f = fopen("file.txt", "a");   // append
FILE* f = fopen("file.txt", "r+");  // read+write
FILE* f = fopen("file.txt", "rb");  // binary read

if (f == NULL) {
    perror("fopen");  // Print error message
    return -1;
}

// Reading
int c;
while ((c = fgetc(f)) != EOF) {
    putchar(c);
}

char buf[100];
fgets(buf, sizeof(buf), f);  // Read line

size_t n = fread(buf, 1, sizeof(buf), f);  // Read bytes

// Writing
fputs("Hello\n", f);
fprintf(f, "Number: %d\n", 42);
fwrite(data, size, count, f);

// Seeking
fseek(f, 0, SEEK_SET);   // Beginning
fseek(f, 0, SEEK_END);   // End
fseek(f, -10, SEEK_CUR); // 10 bytes back
long pos = ftell(f);

// Closing
fclose(f);
// Always check fclose return value
```

---

# 4. Organization, Modifiers & Preprocessor

## 4.1 Organization and Linkage

### 4.1.1 Header Files

#### 4.1.1.1 #include

```c
#include <stdio.h>    // System header: searches system paths
#include "myfile.h"   // Local header: searches current directory first
```

#### 4.1.1.2 Include Guards

```c
// Traditional (works everywhere):
#ifndef MYHEADER_H
#define MYHEADER_H
// ... declarations ...
#endif

// Pragma once (non-standard, widely supported):
#pragma once
// ... declarations ...
```

#### 4.1.1.3 Forward Declarations

```c
struct Point;  // Forward declaration: incomplete type
void draw(struct Point* p);  // Can use pointer to incomplete type

struct Point {
    int x, y;
};
```

---

### 4.1.2 One Definition Rule (ODR)

```c
// Every function, variable, struct, etc. must be defined exactly once
// across the entire program (per translation unit)

// Header file (myheader.h):
extern int global_var;  // Declaration only
void func(int x);       // Declaration only

// Source file (myheader.c):
int global_var = 42;    // Definition
void func(int x) { }   // Definition
```

---

### 4.1.3 Static and extern

#### 4.1.3.1 extern (External Linkage)

```c
// global_var is visible to other translation units
int global_var = 42;        // External linkage by default
extern int shared_var;       // Declaration (defined elsewhere)
```

#### 4.1.3.2 static (Internal Linkage)

```c
static int file_var = 10;   // Only visible in this .c file
static void helper(void) { } // Only callable in this .c file
// Reduces symbol visibility, helps encapsulation
```

#### 4.1.3.3 static (File Scope vs Block Scope)

```c
static int file_scope = 10;  // Internal linkage (file-scope static)

void func() {
    static int call_count = 0;  // Block-scope static: persists across calls
    call_count++;
}
```

---

### 4.1.4 Compilation Model and Translation Units

```c
// Preprocessing: expands #include, #define, #if, etc.
// Compilation: translates to assembly (.s)
// Assembly: translates to object code (.o)
// Linking: combines object files into executable

// gcc -E file.c          # Preprocess only
// gcc -S file.c          # Compile to assembly
// gcc -c file.c          # Compile to object file
// gcc file1.o file2.o    # Link object files
// gcc -o program file1.c file2.c  # All-in-one
```

---

### 4.1.5 Static and Dynamic Libraries

#### 4.1.5.1 Static Libraries (.a / .lib)

```c
// Create:
gcc -c file1.c file2.c
ar rcs libmylib.a file1.o file2.o

// Use:
gcc main.c -L. -lmylib -o program
```

#### 4.1.5.2 Dynamic Libraries (.so / .dll / .dylib)

```c
// Linux:
gcc -shared -fPIC -o libmylib.so file1.c file2.c
gcc main.c -L. -lmylib -o program
export LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH

// Windows:
cl /LD file1.c file2.c /Fe:mylib.dll
cl main.c mylib.lib
```

---

### 4.1.6 Project Structure

#### 4.1.6.1 Using Make

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -Iinclude
SRC = $(wildcard src/*.c)
OBJ = $(SRC:.c=.o)

program: $(OBJ)
	$(CC) $(OBJ) -o program

src/%.o: src/%.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f src/*.o program
```

#### 4.1.6.2 Using CMake

```cmake
cmake_minimum_required(VERSION 3.10)
project(myproject C)
add_executable(program src/main.c src/util.c)
target_include_directories(program PRIVATE include)
```

---

## 4.2 Modifiers and Attributes

### 4.2.1 Storage Class Specifiers

| Specifier | Description |
|-----------|-------------|
| `auto` | Automatic storage (default, rarely used) |
| `register` | Suggest register allocation (mostly ignored) |
| `static` | Static storage / internal linkage |
| `extern` | External linkage |
| `_Thread_local` | Thread-local storage (C11) |

---

### 4.2.2 Type Qualifiers

#### 4.2.2.1 const

```c
const int x = 42;
const int* p = &x;     // Pointer to const int
int* const q = &y;     // Const pointer to int
const int* const r = &z; // Both const
```

#### 4.2.2.2 volatile

```c
volatile int hw_reg;   // Every access must go to memory
// Used for: MMIO, signal handlers, setjmp/longjmp
```

#### 4.2.2.3 restrict (C99)

```c
void func(int* restrict a, int* restrict b) {
    // Compiler assumes a and b don't alias
}
// Violating restrict: UNDEFINED BEHAVIOR
```

#### 4.2.2.4 _Atomic (C11)

```c
#include <stdatomic.h>
atomic_int counter = 0;
atomic_fetch_add(&counter, 1);  // Thread-safe
```

#### 4.2.2.5 _Static_assert (C11)

```c
_Static_assert(sizeof(int) == 4, "int must be 4 bytes");
_Static_assert(sizeof(void*) == 8, "Must be 64-bit");

// C11 syntax (with no message):
_Static_assert(sizeof(int) == 4);

// C23 syntax:
static_assert(sizeof(int) == 4, "int must be 4 bytes");
```

#### 4.2.2.6 _Noreturn (C11)

```c
#include <stdnoreturn.h>

_Noreturn void die(const char* msg) {
    fprintf(stderr, "%s\n", msg);
    exit(1);
    // Compiler knows this function never returns
    // No return value needed, no fall-through warning
}

// GCC/Clang extension:
__attribute__((noreturn)) void abort(void);

// C23 syntax:
[[noreturn]] void my_exit(int code);
```

---

### 4.2.3 Attributes

```c
// GCC/Clang (pre-C23):
__attribute__((noreturn)) void die(void);
__attribute__((unused)) int helper(void);
__attribute__((packed)) struct S { char a; int b; };
__attribute__((format(printf, 1, 2))) void debug(const char* fmt, ...);
__attribute__((aligned(64))) char cache_line[64];

// C23 standard attributes:
[[noreturn]] void die(void);
[[maybe_unused]] int helper(void);
[[deprecated]] void old_func(void);
[[nodiscard]] int important_func(void);
```

---

## 4.3 Preprocessor

### 4.3.1 Object-like Macros

```c
#define PI 3.14159
#define MAX_SIZE 1024
#define NULL ((void*)0)  // Standard NULL definition
```

### 4.3.2 Function-like Macros

```c
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))
#define ABS(x) ((x) < 0 ? -(x) : (x))
// Always use extra parentheses to avoid operator precedence issues
// BAD: #define SQUARE(x) x * x  -> SQUARE(1+2) = 1+2*1+2 = 5 (wrong!)
```

### 4.3.3 Stringification and Concatenation

```c
#define STRINGIFY(x) #x
#define CONCAT(a, b) a##b

int xy = 42;
STRINGIFY(xy)          // "xy" (string literal)
CONCAT(x, y)           // xy (token concatenation)
```

### 4.3.4 Conditional Compilation

```c
#define DEBUG

#ifdef DEBUG
    printf("Debug mode\n");
#endif

#ifndef RELEASE
    printf("Not release\n");
#endif

#if VERSION > 2
    // ...
#elif VERSION == 2
    // ...
#else
    // ...
#endif

// __FILE__, __LINE__, __func__, __DATE__, __TIME__
printf("File: %s, Line: %d, Func: %s\n", __FILE__, __LINE__, __func__);
```

### 4.3.5 #pragma

```c
#pragma once              // Include once (non-standard)
#pragma pack(1)           // Set struct packing alignment
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wunused-variable"
// ... code ...
#pragma GCC diagnostic pop
```

### 4.3.6 Variadic Macros (C99)

```c
#define DEBUG_LOG(fmt, ...) fprintf(stderr, "[DEBUG] " fmt "\n", ##__VA_ARGS__)

DEBUG_LOG("Value: %d", x);
DEBUG_LOG("Simple message");  // ##__VA_ARGS__ handles empty case
```

---

# 5. Data Structures

## 5.1 Structs

### 5.1.1 Basic Struct

```c
struct Point {
    int x;
    int y;
};

struct Point p = {1, 2};
printf("%d, %d\n", p.x, p.y);  // 1, 2
```

### 5.1.2 Struct Initialization

```c
struct Point p1 = {1, 2};           // Designated (C89)
struct Point p2 = {.x = 1, .y = 2}; // Designated initializers (C99)
struct Point p3 = {1};              // p3 = {1, 0} (remaining members zero-initialized)
```

### 5.1.3 Struct Assignment and Copying

```c
struct Point a = {1, 2};
struct Point b = a;     // Copy (value semantics)
a.x = 10;              // b.x is still 1 (independent copy)
```

### 5.1.4 Struct Padding and Alignment

```c
struct Padded {
    char a;     // 1 byte + 3 padding
    int b;      // 4 bytes
    char c;     // 1 byte + 3 padding
};              // Total: 12 bytes

struct __attribute__((packed)) Packed {
    char a;     // 1 byte
    int b;      // 4 bytes
    char c;     // 1 byte
};              // Total: 6 bytes (slower access)

#pragma pack(push, 1)
struct PackedPragma {
    char a;
    int b;
    char c;
};              // Total: 6 bytes
#pragma pack(pop)
```

### 5.1.5 Structs as Function Parameters

```c
// Pass by value (copies entire struct):
void print_point(struct Point p) { }

// Pass by pointer (efficient):
void print_point(const struct Point* p) {
    printf("%d, %d\n", p->x, p->y);
}
// Use -> to access members through pointer
```

### 5.1.6 Self-Referential Structs (Linked Lists)

```c
struct Node {
    int data;
    struct Node* next;  // Pointer to incomplete type (self-reference is OK)
};

struct Node head = {1, NULL};
struct Node second = {2, &head};
head.next = &second;
```

### 5.1.7 Anonymous Structs (C11)

```c
struct Container {
    struct { int x, y; };  // Anonymous struct
    int z;
};

struct Container c = { .x = 1, .y = 2, .z = 3 };
printf("%d\n", c.x);  // Direct access, no nested name
```

---

## 5.2 Unions

### 5.2.1 Basic Union

```c
union Data {
    int i;
    float f;
    char str[20];
};

union Data d;
d.i = 42;
printf("%d\n", d.i);    // 42
d.f = 3.14f;
printf("%d\n", d.i);    // Garbage (overwritten by f)
// All members share the same memory
// sizeof(union) = sizeof(largest member)
```

### 5.2.2 Tagged Union (Type Discrimination)

```c
enum Type { INT, FLOAT, STRING };

struct Value {
    enum Type type;
    union {
        int i;
        float f;
        char str[20];
    } data;
};

void print_value(struct Value* v) {
    switch (v->type) {
        case INT:    printf("%d\n", v->data.i); break;
        case FLOAT:  printf("%f\n", v->data.f); break;
        case STRING: printf("%s\n", v->data.str); break;
    }
}
```

### 5.2.3 Anonymous Unions (C11)

```c
struct Value {
    enum Type type;
    union {             // Anonymous union (no name needed)
        int i;
        float f;
        char str[20];
    };                  // Note: no semicolon after closing brace? Actually yes
};

struct Value v = { .type = INT, .i = 42 };
printf("%d\n", v.i);   // Direct access: v.i, not v.data.i
```

### 5.2.4 Type Punning with Unions (C, not C++)

```c
union FloatBits {
    float f;
    uint32_t i;
};

union FloatBits fb;
fb.f = 3.14f;
printf("Bits: 0x%08X\n", fb.i);  // Read float bits as integer
// Legal in C (not in C++)
```

---

## 5.3 Enums

### 5.3.1 Basic Enum

```c
enum Direction { UP, DOWN, LEFT, RIGHT };  // 0, 1, 2, 3
enum Direction dir = UP;
```

### 5.3.2 Custom Values

```c
enum HttpStatus {
    OK = 200,
    NOT_FOUND = 404,
    SERVER_ERROR = 500
};
```

### 5.3.3 Enum as Bitflags

```c
enum Permission {
    READ  = 1 << 0,  // 1
    WRITE = 1 << 1,  // 2
    EXEC  = 1 << 2,  // 4
    ALL   = READ | WRITE | EXEC  // 7
};

int perms = READ | WRITE;
if (perms & READ) { /* granted */ }
```

---

## 5.4 Bit-Fields

```c
struct Flags {
    unsigned int bold   : 1;  // 1 bit
    unsigned int italic : 1;  // 1 bit
    unsigned int color  : 4;  // 4 bits (0-15)
    unsigned int size   : 8;  // 8 bits (0-255)
};  // Total: probably 2 bytes (implementation-defined)

struct Flags f = { .bold = 1, .color = 5 };
// Bit-fields are implementation-defined in terms of:
// - Ordering (MSB vs LSB first)
// - Whether unsigned or signed
// - Padding behavior
// Not suitable for binary protocols (use shifts/masks instead)
```

---

## 5.5 Arrays and Strings

### 5.5.1 Arrays

```c
int arr[5] = {1, 2, 3, 4, 5};
int arr2[3] = {0};              // All zeros
int arr3[] = {1, 2, 3};         // Size deduced: 3
int arr4[10] = {[3] = 42};     // Designated: arr4[3]=42, rest=0 (C99)

// Multidimensional
int matrix[3][4] = {
    {1, 2, 3, 4},
    {5, 6, 7, 8},
    {9, 10, 11, 12}
};
```

### 5.5.2 Strings (char arrays)

```c
char str1[] = "Hello";           // {'H','e','l','l','o','\0'} - 6 bytes
char str2[10] = "Hello";         // {'H','e','l','l','o','\0',0,0,0,0}
const char* str3 = "Hello";      // Pointer to string literal (read-only)
char str4[6] = {'H','i','!','\0'};  // Manual null terminator
```

### 5.5.3 String Operations

```c
#include <string.h>
strlen(str);        // Length (not including \0)
strcpy(dst, src);   // Copy (unsafe)
strncpy(dst, src, n);  // Copy at most n bytes
strcat(dst, src);   // Concatenate (unsafe)
strncat(dst, src, n);  // Concatenate at most n chars
strcmp(s1, s2);     // Compare
strncmp(s1, s2, n); // Compare first n chars
strchr(str, c);     // Find first occurrence
strrchr(str, c);    // Find last occurrence
strstr(haystack, needle);  // Find substring
```

### 5.5.4 Array Decay

```c
void func(int arr[]) {     // Actually receives int*
    printf("%zu\n", sizeof(arr));  // 8 (pointer, not array!)
}
void func2(int (*arr)[5]) { // Receives pointer to array of 5 ints
    printf("%zu\n", sizeof(*arr));  // 20 (actual array)
}
```

---

# 6. Advanced C & Idioms

## 6.1 Function Pointers & Callbacks

### 6.1.1 Basic Function Pointers

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int (*op)(int, int) = add;
printf("%d\n", op(3, 4));  // 7

op = sub;
printf("%d\n", op(3, 4));  // -1
```

### 6.1.2 Typedef for Function Pointers

```c
typedef int (*BinaryOp)(int, int);
typedef void (*Callback)(void);
typedef int (*Comparator)(const void*, const void*);

int int_compare(const void* a, const void* b) {
    return *(const int*)a - *(const int*)b;
}
qsort(arr, n, sizeof(int), int_compare);
```

### 6.1.3 Function Pointer Arrays

```c
int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }
int mul(int a, int b) { return a * b; }

int (*ops[])(int, int) = {add, sub, mul};
printf("%d\n", ops[0](3, 4));  // 7 (add)
printf("%d\n", ops[1](3, 4));  // -1 (sub)
printf("%d\n", ops[2](3, 4));  // 12 (mul)
```

### 6.1.4 Callbacks

```c
void for_each(int* arr, size_t n, void (*callback)(int)) {
    for (size_t i = 0; i < n; i++)
        callback(arr[i]);
}

void print(int x) { printf("%d ", x); }
void double_val(int x) { printf("%d ", x * 2); }

int arr[] = {1, 2, 3, 4, 5};
for_each(arr, 5, print);       // 1 2 3 4 5
for_each(arr, 5, double_val);  // 2 4 6 8 10
```

---

## 6.2 Variadic Functions

### 6.2.1 Basic Variadic Functions

```c
#include <stdarg.h>

int sum(int count, ...) {
    va_list args;
    va_start(args, count);  // count is the last named parameter
    int total = 0;
    for (int i = 0; i < count; i++)
        total += va_arg(args, int);  // Get next argument as int
    va_end(args);
    return total;
}

printf("%d\n", sum(3, 10, 20, 30));  // 60
```

### 6.2.2 printf Implementation

```c
#include <stdarg.h>

void my_printf(const char* fmt, ...) {
    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);  // Forward to vprintf
    va_end(args);
}
```

### 6.2.3 Variadic Macro Forwarding

```c
#define LOG(fmt, ...) my_printf(__FILE__ ":" __LINE__ ": " fmt, ##__VA_ARGS__)
```

---

## 6.3 Type Punning

### 6.3.1 Union-based Type Punning

```c
union {
    float f;
    uint32_t i;
} u;

u.f = 3.14f;
printf("Bits: 0x%08X\n", u.i);
```

### 6.3.2 memcpy for Type Punning

```c
int x = 42;
float f;
memcpy(&f, &x, sizeof(f));  // Safe in C
// No strict aliasing violation
```

### 6.3.3 Strict Aliasing Rules

```c
// You cannot access an object through an incompatible type
int x = 42;
float* fp = (float*)&x;  // UNDEFINED BEHAVIOR
// Exception: char* can alias anything
```

---

## 6.4 _Generic (C11)

### 6.4.1 Basic _Generic

```c
#define type_name(x) _Generic((x), \
    int: "int", \
    float: "float", \
    double: "double", \
    char*: "string", \
    default: "unknown" \
)

printf("%s\n", type_name(42));        // "int"
printf("%s\n", type_name(3.14));      // "double"
printf("%s\n", type_name("hello"));   // "string"
```

### 6.4.2 Type-Safe Math

```c
#define sqrt(x) _Generic((x), \
    float: sqrtf, \
    double: sqrt, \
    long double: sqrtl \
)(x)
```

---

## 6.5 Compound Literals (C99)

```c
// Create unnamed objects
int* p = (int[]){1, 2, 3, 4, 5};  // Array compound literal
struct Point pt = (struct Point){1, 2};  // Struct compound literal

// Useful for passing temporary arrays
func((int[]){1, 2, 3});  // Pass temporary array to function
```

---

## 6.6 Flexible Array Members (C99)

```c
struct String {
    size_t len;
    char data[];  // Flexible array member (must be last)
};

struct String* s = malloc(sizeof(struct String) + 100);
s->len = 100;
strcpy(s->data, "Hello");
printf("%s\n", s->data);
// No padding after len, data is contiguous
```

---

## 6.7 Setjmp / Longjmp

```c
#include <setjmp.h>

jmp_buf env;

void risky_func(void) {
    longjmp(env, 42);  // Jump back to setjmp with value 42
}

int main(void) {
    int val = setjmp(env);  // Returns 0 first time, 42 after longjmp
    if (val == 0) {
        risky_func();
    } else {
        printf("Caught: %d\n", val);  // 42
    }
}
// WARNING: longjmp with local variables that have been modified
// and not declared volatile: UNDEFINED BEHAVIOR
```

---

## 6.8 Signal Handling

```c
#include <signal.h>

void handler(int signum) {
    printf("Caught signal %d\n", signum);
}

int main(void) {
    signal(SIGINT, handler);   // Simple (limited safe functions)
    // OR
    struct sigaction sa = { .sa_handler = handler };
    sigaction(SIGINT, &sa, NULL);  // More control

    while (1) pause();  // Wait for signal
}
// Only async-signal-safe functions allowed in handler
// Safe: write(), _exit(), kill(), signal()
// NOT safe: malloc(), printf(), lock()
```

---

## 6.9 _Alignas and _Alignof (C11)

```c
#include <stdalign.h>

alignas(64) char cache_line[64];  // Aligned to 64-byte boundary
alignas(16) int aligned_int;

printf("%zu\n", _Alignof(int));     // 4
printf("%zu\n", _Alignof(char));    // 1
printf("%zu\n", _Alignof(void*));   // 8 on 64-bit
```

---

## 6.10 Bit Manipulation (C)

```c
// Bit testing
int bit = (flags >> 3) & 1;      // Test bit 3
int bit2 = flags & (1 << 3);     // Test bit 3 (nonzero if set)

// Bit setting
flags |= (1 << 3);               // Set bit 3

// Bit clearing
flags &= ~(1 << 3);              // Clear bit 3

// Bit toggling
flags ^= (1 << 3);               // Toggle bit 3

// Bit counting (GCC builtin)
int count = __builtin_popcount(0xFF);    // 8
int count64 = __builtin_popcountll(0xFFFFFFFFULL);  // 32

// Count leading/trailing zeros
int clz = __builtin_clz(8);      // 28 (for 32-bit)
int ctz = __builtin_ctz(8);      // 3

// Bit width
int bw = __builtin_ia32_bsrdi(0xFF);  // Or use: 32 - __builtin_clz(x)
```

---

## 6.11 Inline Assembly (GCC AT&T)

```c
// Basic inline assembly
asm("movl $1, %eax");  // Simple instruction

// With inputs and outputs
int a = 10, b = 20, result;
asm("addl %%ebx, %%eax"
    : "=a" (result)       // Output: result in EAX
    : "a" (a), "b" (b)   // Inputs: a in EAX, b in EBX
);

// GCC extended asm (safer, more portable)
asm volatile(
    "rdtsc"                    // Read time stamp counter
    : "=a" (lo), "=d" (hi)    // Outputs
    :                          // No inputs
    :                          // No clobbers
);

// Useful for: reading CR registers, executing privileged instructions,
//             preventing compiler optimization around critical code
```

---

## 6.12 Preprocessor Metaprogramming

```c
// Stringification
#define STRINGIFY(x) #x
#define TOSTRING(x) STRINGIFY(x)
printf("Value: %s\n", TOSTRING(42));  // "42"

// Token concatenation
#define CONCAT(a, b) a##b
int xy = 42;
printf("%d\n", CONCAT(x, y));  // 42

// Macro counting
#define COUNT_ARGS(...) COUNT_ARGS_IMPL(__VA_ARGS__, 10,9,8,7,6,5,4,3,2,1)
#define COUNT_ARGS_IMPL(_1,_2,_3,_4,_5,_6,_7,_8,_9,_10,N,...) N

// Deferred expansion
#define EMPTY()
#define DEFER(id) id EMPTY()
#define EXPAND(...) __VA_ARGS__
// Useful for nested macro expansion
```

---

# 7. Memory Management & Ownership

## 7.1 Dynamic Memory

### 7.1.1 malloc

```c
#include <stdlib.h>

int* p = malloc(10 * sizeof(int));  // Allocate 10 ints
if (p == NULL) {
    // Handle allocation failure
    perror("malloc");
    exit(1);
}
// Memory is UNINITIALIZED (contains garbage)
free(p);
```

### 7.1.2 calloc

```c
int* p = calloc(10, sizeof(int));  // Allocate 10 ints, zero-initialized
// Each element is initialized to 0
// Returns NULL if allocation fails
free(p);
```

### 7.1.3 realloc

```c
int* p = malloc(5 * sizeof(int));
int* q = realloc(p, 10 * sizeof(int));
if (q == NULL) {
    // Original p is still valid!
    free(p);
    return;
}
p = q;  // realloc may have moved the memory
// Old pointer is INVALID if realloc moved the block
```

### 7.1.4 free

```c
free(p);
p = NULL;  // Good practice: prevent double-free
// free(NULL) is safe (no-op)
// Double free: UNDEFINED BEHAVIOR
// Use after free: UNDEFINED BEHAVIOR
```

### 7.1.5 malloc Implementation

```c
// glibc malloc uses brk() and mmap()
// Small allocations: brk() (heap expansion)
// Large allocations: mmap() (separate mapping)
//
// Each allocation has metadata (size, flags)
// Free chunks go into bins (fast, small, large, tcache)
// malloc(16) may actually allocate 32 bytes (alignment + metadata)
```

### 7.1.6 Memory Leaks

```c
void leak(void) {
    int* p = malloc(100);  // Leaked when function returns
    // No free() call
}
// Use valgrind to detect: valgrind --leak-check=full ./program
```

---

## 7.2 Memory Pools

### 7.2.1 Fixed-Size Pool Allocator

```c
#define POOL_SIZE 1024
#define BLOCK_SIZE 64

typedef struct Block {
    struct Block* next;
} Block;

typedef struct {
    Block* free_list;
    char memory[POOL_SIZE];
} Pool;

void pool_init(Pool* pool) {
    pool->free_list = (Block*)pool->memory;
    Block* current = pool->free_list;
    for (int i = 0; i < POOL_SIZE / BLOCK_SIZE - 1; i++) {
        current->next = (Block*)((char*)current + BLOCK_SIZE);
        current = current->next;
    }
    current->next = NULL;
}

void* pool_alloc(Pool* pool) {
    if (pool->free_list == NULL) return NULL;
    Block* block = pool->free_list;
    pool->free_list = block->next;
    return block;
}

void pool_free(Pool* pool, void* ptr) {
    Block* block = (Block*)ptr;
    block->next = pool->free_list;
    pool->free_list = block;
}
```

---

## 7.3 Stack vs Heap

| Feature | Stack | Heap |
|---------|-------|------|
| Speed | Fast (just move RSP) | Slow (system call) |
| Size | Limited (typically 1-8 MB) | Limited by RAM |
| Lifetime | Scope-based | Manual (free) |
| Fragmentation | None | Can fragment |
| Reallocation | Not possible | realloc() |
| Data races | Thread-local | Shared across threads |

```c
// Stack allocation
int arr[100];  // Automatic, freed when function returns

// Heap allocation
int* arr = malloc(100 * sizeof(int));  // Must free manually

// Variable-length arrays (C99, optional in C11)
int n = 100;
int vla[n];  // Stack-allocated, size determined at runtime
// VLAs have restrictions: no static storage, no file scope
```

---

### 7.3.1 Variable-Length Arrays (VLAs)

```c
// C99 feature, optional in C11, optional in C23
int n;
scanf("%d", &n);
int arr[n];  // VLA: size determined at runtime

// VLA characteristics:
// - Allocated on stack (automatic storage)
// - Size must be positive and known at runtime
// - Cannot have static or thread-local storage duration
// - Cannot be initialized with initializer list
// - sizeof works (evaluated at runtime)
// - Cannot be passed to functions without decay

// VLA as function parameter (only first dimension can be VLA):
void func(size_t n, int arr[n]) {  // Actually receives int*
    // arr is a pointer, not a VLA
}

// VLA with alloca (non-standard, GCC extension):
int* vla = alloca(n * sizeof(int));  // Similar to VLA but returns pointer
// alloca memory freed automatically when function returns
```

---

## 7.4 Memory-Mapped I/O (mmap)

# 8. Standard Library & Utilities

## 8.1 String Functions (string.h)

### 8.1.1 strlen

```c
size_t len = strlen("Hello");  // 5
```

### 8.1.2 strcpy / strncpy / strlcpy

```c
char dst[20];
strcpy(dst, "Hello");                     // Unsafe
strncpy(dst, "Hello", sizeof(dst)-1);     // Better but imperfect
dst[sizeof(dst)-1] = '\0';               // Ensure null termination

// BSD extension (safer):
strlcpy(dst, "Hello", sizeof(dst));       // Always null-terminates
```

### 8.1.3 strcat / strncat / strlcat

```c
char str[50] = "Hello";
strcat(str, " World");                              // Unsafe
strncat(str, " World", sizeof(str) - strlen(str) - 1);  // Better
strlcat(str, " World", sizeof(str));                 // BSD (safer)
```

### 8.1.4 strcmp / strncmp

```c
int cmp = strcmp("abc", "abd");     // < 0
int cmp2 = strcmp("abc", "abc");    // 0
int cmp3 = strcmp("abd", "abc");    // > 0
```

### 8.1.5 strchr / strrchr

```c
char* first = strchr("Hello", 'l');   // Points to first 'l'
char* last = strrchr("Hello", 'l');   // Points to last 'l'
```

### 8.1.6 strstr / strtok

```c
char* sub = strstr("Hello World", "World");
// strtok is not reentrant (use strtok_r for threads)
char* token = strtok_r(str, ",", &saveptr);
```

### 8.1.7 memcpy / memmove / memset / memcmp

```c
memcpy(dst, src, n);      // Copy bytes (no overlap safety)
memmove(dst, src, n);     // Copy bytes (handles overlap)
memset(dst, 0, n);        // Set n bytes to value
int cmp = memcmp(a, b, n);  // Compare n bytes
```

---

## 8.2 Math Functions (math.h)

### 8.2.1 Basic Math

```c
#include <math.h>
sqrt(16.0);      // 4.0
pow(2.0, 10.0);  // 1024.0
fabs(-3.14);     // 3.14
ceil(3.2);       // 4.0
floor(3.7);      // 3.0
round(2.5);      // 3.0
fmod(7.0, 3.0);  // 1.0
```

### 8.2.2 Trigonometric

```c
sin(M_PI / 2);   // 1.0
cos(0);           // 1.0
tan(M_PI / 4);   // 1.0
asin(1.0);       // M_PI/2
atan2(1.0, 1.0); // M_PI/4
```

### 8.2.3 Exponential and Logarithmic

```c
exp(1.0);      // e^1 = 2.718...
log(M_E);      // 1.0
log2(8.0);     // 3.0
log10(100.0);  // 2.0
exp2(3.0);     // 8.0
```

### 8.2.4 Min/Max (No Standard Macro)

```c
// C doesn't have standard min/max
// Safe alternatives:
#define MIN(a, b) ((a) < (b) ? (a) : (b))
#define MAX(a, b) ((a) > (b) ? (a) : (b))
// Or use inline functions for type safety
```

---

## 8.3 I/O Functions (stdio.h)

### 8.3.1 printf Family

```c
printf("%d %f %s\n", 42, 3.14, "hello");
fprintf(stderr, "Error: %s\n", msg);
sprintf(buf, "%d", 42);          // Unsafe
snprintf(buf, sizeof(buf), "%d", 42);  // Safe
```

### 8.3.2 scanf Family

```c
scanf("%d", &x);
fscanf(file, "%d", &x);
sscanf(str, "%d", &x);
```

### 8.3.3 File Operations

```c
FILE* f = fopen("file.txt", "r");  // Open
if (f == NULL) { perror("fopen"); return; }
fgets(buf, sizeof(buf), f);        // Read line
fputs("line\n", f);               // Write
fclose(f);                        // Close
```

### 8.3.4 Binary I/O

```c
FILE* f = fopen("data.bin", "rb");
size_t n = fread(buf, 1, sizeof(buf), f);
fclose(f);

FILE* f = fopen("data.bin", "wb");
fwrite(data, 1, size, f);
fclose(f);
```

---

## 8.4 Conversion Functions (stdlib.h)

```c
int x = atoi("42");          // String to int (simple, no error checking)
long l = atol("1000000");    // String to long
long long ll = atoll("123"); // String to long long

double d = atof("3.14");     // String to double

// Better (with error checking):
char* end;
long val = strtol("42abc", &end, 10);  // val=42, end points to "abc"
double val2 = strtod("3.14x", &end);   // val2=3.14, end points to "x"

// Random numbers
srand(time(NULL));  // Seed
int r = rand() % 100;  // 0-99 (modulo bias!)
```

---

## 8.5 Memory Functions (stdlib.h)

```c
void* p = malloc(100);     // Allocate
void* p = calloc(10, 10);  // Allocate zeroed
void* q = realloc(p, 200); // Resize
free(p);                    // Free
```

---

## 8.6 Time Functions (time.h)

```c
#include <time.h>

time_t now = time(NULL);              // Current time
struct tm* tm = localtime(&now);      // Local time
printf("%04d-%02d-%02d\n", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday);

char buf[100];
strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", tm);

clock_t start = clock();
// ... do work ...
clock_t end = clock();
double elapsed = (double)(end - start) / CLOCKS_PER_SEC;
```

---

## 8.7 Random Number Generation

```c
#include <stdlib.h>
#include <time.h>

srand(time(NULL));
int r = rand();                    // 0 to RAND_MAX
int r100 = rand() % 100;          // 0-99 (has modulo bias)
// Better: use arc4random() on BSD/macOS, or /dev/urandom on Linux
```

---

# 9. Concurrency & Multi-threading (C11)

## 9.1 Threads

### 9.1.1 POSIX Threads (pthreads)

```c
#include <pthread.h>

void* thread_func(void* arg) {
    int* val = (int*)arg;
    printf("Thread: %d\n", *val);
    return NULL;
}

int main(void) {
    pthread_t thread;
    int value = 42;
    pthread_create(&thread, NULL, thread_func, &value);
    pthread_join(thread, NULL);  // Wait for thread to finish
}
// Compile: gcc -pthread program.c
```

### 9.1.2 C11 Threads (threads.h)

```c
#include <threads.h>

int thread_func(void* arg) {
    printf("Thread\n");
    return 0;
}

int main(void) {
    thrd_t thread;
    thrd_create(&thread, thread_func, NULL);
    thrd_join(&thread, NULL);
}
// Less commonly supported than pthreads
```

---

## 9.2 Synchronization

### 9.2.1 Mutex

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

void* thread_func(void* arg) {
    pthread_mutex_lock(&mutex);
    // Critical section
    shared_var++;
    pthread_mutex_unlock(&mutex);
    return NULL;
}

// Variants:
// pthread_mutex_trylock() - non-blocking
// pthread_mutex_timedlock() - with timeout
// Recursive mutex: PTHREAD_RECURSIVE_MUTEX_INITIALIZER_NP
```

### 9.2.2 Condition Variables

```c
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond = PTHREAD_COND_INITIALIZER;
int ready = 0;

void* producer(void* arg) {
    pthread_mutex_lock(&mutex);
    ready = 1;
    pthread_cond_signal(&cond);  // Wake one waiter
    pthread_mutex_unlock(&mutex);
    return NULL;
}

void* consumer(void* arg) {
    pthread_mutex_lock(&mutex);
    while (!ready)
        pthread_cond_wait(&cond, &mutex);  // Atomically unlock + wait
    // Process
    pthread_mutex_unlock(&mutex);
    return NULL;
}
```

### 9.2.3 Read-Write Locks

```c
pthread_rwlock_t rwlock = PTHREAD_RWLOCK_INITIALIZER;

// Multiple readers can hold simultaneously
pthread_rwlock_rdlock(&rwlock);
// read shared data
pthread_rwlock_unlock(&rwlock);

// Only one writer at a time
pthread_rwlock_wrlock(&rwlock);
// modify shared data
pthread_rwlock_unlock(&rwlock);
```

---

## 9.3 Atomics (C11)

```c
#include <stdatomic.h>

atomic_int counter = ATOMIC_VAR_INIT(0);

// Thread-safe operations
atomic_fetch_add(&counter, 1);       // Increment
atomic_fetch_sub(&counter, 1);       // Decrement
int val = atomic_load(&counter);     // Read
atomic_store(&counter, 42);          // Write

// Compare and swap (lock-free)
int expected = 0;
atomic_compare_exchange_strong(&counter, &expected, 1);

// Memory ordering
atomic_store_explicit(&counter, 1, memory_order_release);
atomic_load_explicit(&counter, memory_order_acquire);
// memory_order_relaxed / memory_order_seq_cst
```

---

## 9.4 Thread-Local Storage

```c
#include <threads.h>

_Thread_local int tls_var = 0;  // Each thread has its own copy

// GCC extension:
__thread int tls_var2 = 0;

// Useful for: errno, per-thread caches, thread-local context
```

---

## 9.5 Thread Safety Patterns

```c
// Producer-Consumer with condition variable
// Reader-Writer with rwlock
// Thread pool with task queue
// Double-checked locking (with atomics, not just volatile!)
// RCU (Read-Copy-Update) for read-heavy workloads
```

---

## 9.6 Deadlock Prevention

```c
// Always lock in same order
// Use trylock + backoff
// Use timeout variants
// Avoid holding locks across syscalls
// Lock hierarchies

// ABBA deadlock:
// Thread 1: lock(A); lock(B);
// Thread 2: lock(B); lock(A);  // DEADLOCK!
// Fix: both threads lock(A) then lock(B)
```

---

# 10. Security, Low-Level & Exploit Development

## 10.1 Low-Level Types

```c
// Payload / shellcode
uint8_t shellcode[] = "\x31\xc0\x50\x68\x2f\x2f\x73\x68";

// Port numbers / offsets
uint16_t port = htons(4444);
uint32_t offset = 0x41424344;

// Memory addresses
uintptr_t addr = (uintptr_t)&target;
void* ptr = (void*)0x7fff12345678;
```

---

## 10.2 Buffer Overflow

### 10.2.1 Stack Buffer Overflow

```c
void vulnerable(char* input) {
    char buf[64];
    strcpy(buf, input);  // No bounds check!
    // If input > 64 bytes, overwrites saved RBP, return address
}

// Exploit: overwrite return address with shellcode address
// Payload: padding + shellcode_address + NOP_sled + shellcode
```

### 10.2.2 Stack Canary Bypass

```c
// Compiler inserts random canary between locals and saved RBP
// Buffer overflow must also overwrite canary
// Leak canary via format string or other vuln
// Or: brute-force (forking servers reset canary)
```

### 10.2.3 Ret2libc

```c
// Instead of shellcode, return to libc functions
// Payload: padding + canary + saved_rbp + pop_rdi_ret + bin_sh_addr + system_addr
// system("/bin/sh") gets a shell
```

---

## 10.3 Format String Vulnerabilities

```c
// If user input reaches printf directly:
printf(user_input);  // VULNERABLE!

// Reading stack:
printf("%08x.%08x.%08x");  // Leak stack values

// Writing arbitrary memory:
printf("%n", &target);      // Writes number of bytes printed so far
// %n allows writing to arbitrary addresses

// Exploit: overwrite GOT entry
printf("AAAA%7$n");        // Write 4 to address at stack position 7
// Stack: [target_address][AAAA][...][%7$n]
```

### 10.3.1 Format Specifiers

```c
// %n - writes count of bytes printed
// %hhn - writes 1 byte (char)
// %hn - writes 2 bytes (short)
// %n - writes 4 bytes (int)
// %lln - writes 8 bytes (long long)

// Example: write 0x08048000
printf("%128c%7$hn", 0, &target);  // Write 128 to target
```

---

## 10.4 Heap Exploitation

### 10.4.1 Heap Overflow

```c
// Overwrite heap metadata or adjacent chunks
// Use tcache poisoning (glibc 2.26+)
// Use fastbin attack
// Use unsorted bin attack
```

### 10.4.2 Use-After-Free

```c
char* chunk = malloc(64);
free(chunk);
// chunk still points to freed memory
char* chunk2 = malloc(64);  // May get same memory back
// Writing to chunk2 overwrites chunk's freed data
// Classic UAF: overwrite function pointer in freed object
```

### 10.4.3 Double Free

```c
char* p = malloc(64);
free(p);
free(p);  // Double free: UNDEFINED BEHAVIOR
// Attacker controls free list, can allocate at arbitrary address
```

---

## 10.5 ROP and Shellcode

### 10.5.1 Return-Oriented Programming

```c
// Chain small instruction sequences (gadgets) ending in ret
// Bypass NX (non-executable stack)
// Each gadget performs a small operation
// Gadgets found in libc, program binary

// gadget1: pop rdi; ret  (load argument)
// gadget2: pop rsi; ret  (load second argument)
// gadget3: syscall; ret  (invoke syscall)
// Chain: gadget1 -> addr_of_bin_sh -> system
```

### 10.5.2 Shellcode Injection

```c
// Position-independent code (PIC)
// No absolute addresses
// Uses relative jumps and syscalls
// Common: execve("/bin/sh", NULL, NULL)

// Linux x86-64 shellcode:
char shellcode[] =
    "\x48\x31\xf2"              // xor rdx, rdx
    "\x48\x31\xf6"              // xor rsi, rsi
    "\x48\xbb\x2f\x62\x69\x6e" // mov rbx, "/bin"
    "\x2f\x2f\x73\x68"          // "/sh"
    "\x53"                      // push rbx
    "\x48\x89\xe7"              // mov rdi, rsp
    "\x48\x31\xc0"              // xor rax, rax
    "\xb0\x3b"                  // mov al, 0x3b (execve)
    "\x0f\x05";                 // syscall
```

---

## 10.6 Syscalls

### 10.6.1 Direct Syscall

```c
// Linux x86-64: syscall number in RAX, args in RDI,RSI,RDX,R10,R8,R9
// int execve(const char* filename, char* const argv[], char* const envp[]);
// RAX=59, RDI=filename, RSI=argv, RDX=envp

// Inline assembly syscall:
long syscall_write(int fd, const void* buf, size_t count) {
    long ret;
    asm volatile (
        "syscall"
        : "=a" (ret)
        : "a" (1), "D" (fd), "S" (buf), "d" (count)
        : "rcx", "r11", "memory"
    );
    return ret;
}
```

### 10.6.2 Syscall Table

| Syscall | Number (x86-64) | Description |
|---------|-----------------|-------------|
| read | 0 | Read from fd |
| write | 1 | Write to fd |
| open | 2 | Open file |
| close | 3 | Close fd |
| mmap | 9 | Map memory |
| mprotect | 10 | Change memory protection |
| munmap | 11 | Unmap memory |
| execve | 59 | Execute program |
| exit | 60 | Exit process |
| clone | 56 | Create thread/process |
| signal | varies | Signal handling |

---

## 10.7 Compiler & Binary Hardening

### 10.7.1 Mitigations

| Mitigation | Flag | Description |
|------------|------|-------------|
| Stack Canary | `-fstack-protector-strong` | Random canary on stack |
| NX/DEP | `-z noexecstack` | Non-executable stack |
| PIE | `-fPIE -pie` | Position-independent executable |
| RELRO | `-z relro -z now` | Read-only GOT |
| FORTIFY | `-D_FORTIFY_SOURCE=2` | Bounded string functions |
| ASLR | (OS-level) | Randomize memory layout |
| CFI | `-fsanitize=cfi` | Control-flow integrity |
| Shadow Stack | `-fcf-protection=shadow-stack` | CET (Intel) |

### 10.7.2 Bypass Concepts

```c
// ASLR bypass: information leak (format string, info leak vuln)
// NX bypass: ROP chains
// PIE bypass: leak base address, calculate offsets
// Canary bypass: leak canary, or use format string %n
// RELRO bypass: partial RELRO still allows GOT overwrite
```

---

# 11. Debugging, Tooling & Resources

## 11.1 Debugging Tools

### 11.1.1 GDB

```bash
gdb ./program
(gdb) break main        # Set breakpoint
(gdb) run               # Run program
(gdb) step              # Step into
(gdb) next              # Step over
(gdb) continue          # Continue execution
(gdb) print variable    # Print variable
(gdb) x/20x $rsp       # Examine 20 hex words at RSP
(gdb) info registers    # Show registers
(gdb) backtrace         # Show call stack
(gdb) disassemble main  # Disassemble function
(gdb) watch variable    # Watch for changes
```

### 11.1.2 Valgrind

```bash
valgrind --leak-check=full ./program     # Memory leak detection
valgrind --tool=memcheck ./program        # Memory error detection
valgrind --tool=callgrind ./program       # Call graph profiling
valgrind --tool=cachegrind ./program      # Cache profiling
valgrind --tool=helgrind ./program        # Thread error detection
```

### 11.1.3 AddressSanitizer

```bash
gcc -fsanitize=address -g program.c -o program
# Detects: buffer overflow, use-after-free, double-free,
#          stack overflow, memory leaks
```

### 11.1.4 Other Sanitizers

#### UndefinedBehaviorSanitizer (UBSan)

```bash
gcc -fsanitize=undefined program.c -o program
./program
# Detects: signed overflow, null dereference, alignment issues,
#          bool overflow, enum out of range, float cast overflow,
#          integer divide by zero, shift exponent too large, etc.
```

#### ThreadSanitizer (TSan)

```bash
gcc -fsanitize=thread program.c -o program
# Detects data races, deadlocks
# Overhead: 5-15x slower, 5-10x memory
```

#### MemorySanitizer (MSan)

```bash
gcc -fsanitize=memory program.c -o program
# Detects reads of uninitialized memory
# Requires all code compiled with MSan (including libraries)
```

---

## 11.2 Build Systems

### 11.2.1 Make

```makefile
CC = gcc
CFLAGS = -Wall -Wextra -g -O2
LDFLAGS = -lm -lpthread

program: main.o util.o
	$(CC) $(LDFLAGS) -o $@ $^

%.o: %.c
	$(CC) $(CFLAGS) -c -o $@ $<

clean:
	rm -f *.o program
```

### 11.2.2 CMake

```cmake
cmake_minimum_required(VERSION 3.10)
project(myproject C)
set(CMAKE_C_STANDARD 11)
add_executable(program main.c util.c)
target_link_libraries(program m pthread)
```

### 11.2.3 Compiler Flags

```bash
# GCC/Clang
-O0 -g                # No optimization, debug symbols
-O2                    # Standard optimization
-O3                    # Aggressive optimization
-Wall -Wextra          # All warnings
-Werror                # Warnings as errors
-fsanitize=address     # AddressSanitizer
-fstack-protector-strong  # Stack canary
-fPIE -pie             # Position-independent executable
-z relro -z now        # Full RELRO
-D_FORTIFY_SOURCE=2    # Fortified functions
```

---

## 11.3 Disassemblers/Decompilers

### 11.3.1 IDA Pro / IDA Free

```bash
# Industry standard disassembler
# Decompiler output: C-like pseudocode
# Xrefs, function graphs, scripting (IDAPython)
```

### 11.3.2 Ghidra

```bash
# Free, open-source (NSA)
# Decompiler built-in
# Ghidra scripts for automation
# Supports ELF, PE, Mach-O, etc.
```

### 11.3.3 radare2 / Cutter

```bash
# Open-source, CLI-based
r2 -A ./binary
aaa                    # Analyze all
pdf @main              # Disassemble main
VV @main              # Visual mode
```

---

## 11.4 Resources

- **Beej's Guide to C Programming**: https://beej.us/guide/bgc/
- **Beej's Guide to Network Programming**: https://beej.us/guide/bgnet/
- **Modern C (Jens Gustedt)**: https://gustedt.gitlabpages.inria.fr/modern-c/
- **Compilers: Principles, Techniques, and Tools** (Dragon Book)
- **Computer Systems: A Programmer's Perspective** (CS:APP)
- **The Art of Exploitation** (Jon Erickson)
- **Linux Kernel Development** (Robert Love)

---

# 12. Undefined Behavior & Language Edge Cases

## 12.1 Undefined Behavior Fundamentals

```c
// C has three categories:
// 1. Undefined Behavior (UB): anything can happen
// 2. Implementation-Defined: compiler/platform defines behavior
// 3. Unspecified: one of multiple valid behaviors chosen

// UB examples:
int x = INT_MAX + 1;        // Signed integer overflow
int* p = NULL; *p = 42;     // Null pointer dereference
int arr[5]; arr[10] = 1;    // Out-of-bounds access
int x = 1/0;                // Division by zero
```

### 12.1.1 Common Undefined Behaviors

| Behavior | Example | Consequence |
|----------|---------|-------------|
| Signed overflow | `INT_MAX + 1` | Anything |
| Null dereference | `*NULL` | Segfault (usually) |
| Division by zero | `1 / 0` | Signal (usually) |
| Use after free | `free(p); *p` | Anything |
| Double free | `free(p); free(p)` | Anything |
| Buffer overflow | `arr[10]` in `arr[5]` | Anything |
| Strict aliasing | `int* p = (float*)&x` | Anything |
| Uninitialized read | `int x; use(x)` | Anything |
| Return of local | `return &local_var` | Dangling pointer |

---

## 12.2 Common Sources of UB

### 12.2.1 Signed Integer Overflow

```c
int x = INT_MAX;
x++;  // UNDEFINED BEHAVIOR
// Fix: use unsigned, or check before arithmetic
```

### 12.2.2 Strict Aliasing Violations

```c
int x = 42;
float* fp = (float*)&x;  // UB: incompatible type access
// Fix: use memcpy, union, or restrict
```

### 12.2.3 Uninitialized Variables

```c
int x;
printf("%d", x);  // UNDEFINED BEHAVIOR
// Fix: always initialize variables
```

### 12.2.4 Buffer Overflows

```c
char buf[10];
strcpy(buf, "this string is too long");  // UB: overflow
// Fix: use strncpy, snprintf, bounds checking
```

### 12.2.5 Pointer Arithmetic Out of Bounds

```c
int arr[5];
int* p = arr + 10;  // UB: past end of array
// Fix: keep pointers within array bounds
```

### 12.2.6 Modifying String Literals

```c
char* str = "Hello";
str[0] = 'h';  // UNDEFINED BEHAVIOR
// Fix: use char str[] = "Hello";
```

---

## 12.3 Implementation-Defined Behavior

```c
// Size of types (int could be 2 bytes on some systems)
// Endianness (little-endian vs big-endian)
// Right shift of negative numbers
// Signed integer representation (two's complement, ones' complement, sign-magnitude)
// Maximum recursion depth
```

---

## 12.4 Volatile Misconceptions

```c
// volatile does NOT:
// - Make variables atomic
// - Prevent compiler reordering
// - Provide memory ordering guarantees
// volatile IS for:
// - Memory-mapped I/O
// - Signal handlers
// - setjmp/longjmp
// Use _Atomic (C11) for thread safety
```

---

# 13. C in ELF / PE Binaries

## 13.1 ELF Binary Format (Linux)

### 13.1.1 ELF Header

```bash
readelf -h program          # Show ELF header
# Contains: magic number, architecture, entry point,
#           program header offset, section header offset
```

### 13.1.2 ELF Sections

| Section | Description |
|---------|-------------|
| `.text` | Executable code |
| `.rodata` | Read-only data (strings, constants) |
| `.data` | Initialized global/static variables |
| `.bss` | Uninitialized global/static variables |
| `.plt` | Procedure Linkage Table (dynamic linking) |
| `.got` | Global Offset Table (absolute addresses) |
| `.got.plt` | GOT entries for PLT |
| `.init` / `.fini` | Constructor/destructor code |
| `.dynamic` | Dynamic linking info |
| `.symtab` | Symbol table |
| `.strtab` | String table |
| `.debug_*` | Debug info |
| `.ctors` / `.dtors` | Constructor/destructor function pointers |

### 13.1.3 Dynamic Linking

```bash
ldd program                 # Show shared library dependencies
objdump -T program          # Show dynamic symbols
# PLT: trampoline for lazy binding
# GOT: stores absolute addresses of shared library functions
# GOT[0]: address of .dynamic section
# GOT[1]: identifier for dynamic linker
# GOT[2]: resolver function
```

---

## 13.2 PE Binary Format (Windows)

### 13.2.1 PE Header

```bash
# PE Header contains:
# - DOS Header (MZ magic)
# - COFF Header (machine type, number of sections)
# - Optional Header (entry point, image base, subsystem)
# - Section Headers (.text, .data, .rdata, .rsrc, etc.)
```

### 13.2.2 PE Sections

| Section | Description |
|---------|-------------|
| `.text` | Executable code |
| `.data` | Initialized data |
| `.rdata` | Read-only data, imports, exports |
| `.bss` | Uninitialized data |
| `.rsrc` | Resources (icons, dialogs, etc.) |
| `.reloc` | Relocation table |
| `.idata` | Import table |
| `.edata` | Export table |

### 13.2.3 DLL Hijacking

```c
// Application searches for DLLs in:
// 1. Application directory
// 2. System directory
// 3. Windows directory
// 4. PATH directories
// Attacker places malicious DLL in earlier search order
```

---

## 13.3 Reverse Engineering C Binaries

### 13.3.1 Recognizing C Patterns

```c
// Function prologue: push rbp; mov rbp, rsp; sub rsp, N
// Function epilogue: mov rsp, rbp; pop rbp; ret
// String references: lea rdi, [rip+OFFSET] (LEA with RIP-relative addressing)
// Function calls: call [plt+OFFSET] or call rax
// Loops: cmp + jl/jg/je/jne + jmp back
```

### 13.3.2 Symbol Recovery

```bash
# Stripped binaries: debug symbols removed
# Unstripped: full symbol info
nm program               # List symbols
nm -C program            # Demangle C++ names
objdump -t program       # Symbol table
c++filt _Z3foov          # Demangle: foo()
```

---

## 13.4 Process Memory Layout

```
High address
+------------------+
|     Stack        |  ← grows downward
|         ↓        |
|                  |
|         ↑        |
|     Heap         |  ← grows upward (brk/sbrk/mmap)
+------------------+
|       BSS        |  uninitialized globals
+------------------+
|      Data        |  initialized globals
+------------------+
|      Text        |  executable code (read-only)
+------------------+
Low address
```

### 13.4.1 Memory Segments

```c
// Text segment: read-only, executable
// Data segment: read-write, initialized
// BSS segment: read-write, zero-initialized
// Heap: dynamic memory (malloc)
// Stack: local variables, function calls

// Check segment addresses:
extern char etext, edata, end;  // Linker symbols
printf("Text ends at: %p\n", (void*)&etext);
printf("Data ends at: %p\n", (void*)&edata);
printf("BSS ends at: %p\n", (void*)&end);
```

---

# 14. Common Mistakes, Tips & Optimization

## 14.1 Common C Mistakes

### 14.1.1 Buffer Overflows

```c
char buf[10];
gets(buf);                    // NEVER use gets (removed in C11)
scanf("%s", buf);             // Unsafe
strcpy(buf, user_input);      // Unsafe
// Fix: use fgets, snprintf, strncpy with bounds
```

### 14.1.2 Off-by-One Errors

```c
for (int i = 0; i <= n; i++) { }  // One too many if n is array size
// Fix: i < n
```

### 14.1.3 Dangling Pointers

```c
int* p;
{
    int x = 42;
    p = &x;
}
printf("%d", *p);  // UB: x is out of scope
```

### 14.1.4 Null Pointer Dereference

```c
char* s = malloc(100);
strcpy(s, "Hello");  // Crash if malloc returned NULL
// Always check malloc return value
```

### 14.1.5 Memory Leaks

```c
void func(void) {
    char* p = malloc(100);
    if (error) return;  // Leak! No free()
    free(p);
}
// Fix: use goto for cleanup or check all return paths
```

### 14.1.6 Double Free

```c
free(p);
free(p);  // UNDEFINED BEHAVIOR
// Fix: set pointer to NULL after free
```

### 14.1.7 Integer Overflow in Allocation

```c
// attacker-controlled size
size_t n = user_input;
void* p = malloc(n * sizeof(int));  // Overflow if n is huge
// Fix: check for overflow before multiplying
if (n > SIZE_MAX / sizeof(int)) return NULL;
```

### 14.1.8 Format String Bug

```c
printf(user_input);  // VULNERABLE
// Fix: printf("%s", user_input);
```

### 14.1.9 Signed/Unsigned Comparison

```c
size_t len = strlen(str);
for (int i = 0; i < len; i++) { }  // Warning: signed/unsigned comparison
// Fix: use size_t for loop counter
```

### 14.1.10 Undefined Order of Evaluation

```c
int i = 0;
int a = i++ + i++;  // UB: unsequenced modifications
// Fix: separate statements
```

---

## 14.2 Tips & Tricks

### 14.2.1 Safe Memory Patterns

```c
// RAII-like cleanup pattern
int* func(void) {
    int* a = malloc(100);
    if (!a) goto fail_a;
    int* b = malloc(200);
    if (!b) goto fail_b;
    return combine(a, b);
fail_b:
    free(a);
fail_a:
    return NULL;
}
```

### 14.2.2 Const Correctness

```c
// Use const wherever possible
void print(const char* str);        // Promise: won't modify str
void modify(const int* arr, size_t n); // Promise: won't modify elements
// Helps prevent bugs, enables compiler optimization
```

### 14.2.3 Debugging Macros

```c
#ifdef DEBUG
    #define DBG(fmt, ...) fprintf(stderr, "[%s:%d] " fmt "\n", \
                                  __FILE__, __LINE__, ##__VA_ARGS__)
    #define ASSERT(cond) do { \
        if (!(cond)) { \
            fprintf(stderr, "ASSERT FAILED: %s at %s:%d\n", \
                    #cond, __FILE__, __LINE__); \
            abort(); \
        } \
    } while(0)
#else
    #define DBG(fmt, ...) ((void)0)
    #define ASSERT(cond) ((void)0)
#endif
```

### 14.2.4 Array Size Macro

```c
#define ARRAY_SIZE(arr) (sizeof(arr) / sizeof((arr)[0]))
int arr[] = {1, 2, 3, 4, 5};
size_t n = ARRAY_SIZE(arr);  // 5
```

---

## 14.3 Performance Optimization

### 14.3.1 Compiler Optimization

```bash
-O0    # No optimization (debugging)
-O1    # Basic optimizations
-O2    # Standard optimizations (recommended)
-O3    # Aggressive optimizations (may increase code size)
-Os    # Optimize for size
-Ofast # Aggressive, may violate strict standards (-ffast-math)
```

### 14.3.2 Profile-Guided Optimization

```bash
gcc -fprofile-generate program.c -o program
./program  # Generate profile data
gcc -fprofile-use program.c -o program_optimized
```

### 14.3.3 Cache-Friendly Code

```c
// Prefer sequential access (cache lines)
// Structure of Arrays vs Array of Structures:
struct AoS { int x[1000]; int y[1000]; };  // Interleaved
struct SoA { struct { int x; int y; } data[1000]; };  // Bad
struct SoA2 { int x[1000]; int y[1000]; };  // Good: sequential
```

### 14.3.4 Branch Prediction Hints

```c
// GCC: __builtin_expect
#define LIKELY(x)   __builtin_expect(!!(x), 1)
#define UNLIKELY(x) __builtin_expect(!!(x), 0)

if (LIKELY(condition)) { }
// C23: [[likely]] [[unlikely]]
```

### 14.3.5 Inline Functions

```c
// Header-only inline functions (avoid multiple definition)
static inline int max(int a, int b) {
    return a > b ? a : b;
}
// static inline in header: each TU gets its own copy
// No linking issues, compiler can inline
```

---

## 14.4 C Standards History

| Standard | Year | Key Features |
|----------|------|--------------|
| K&R C | 1972 | Original C |
| ANSI C (C89) | 1989 | Standard I/O, function prototypes |
| C99 | 1999 | `//` comments, VLAs, `_Bool`, `_Complex`, `restrict` |
| C11 | 2011 | `<threads.h>`, `<stdatomic.h>`, `_Generic`, `_Alignas` |
| C17/C18 | 2018 | Bug fixes (no new features) |
| C23 | 2024 | `typeof`, digit separators, `nullptr`, `#embed`, attributes |

---

# A. Inline Assembly

## A.1 GCC Extended Assembly (AT&T Syntax)

```c
// Basic form:
asm("instructions");

// Extended form (with operands):
asm("instructions" : outputs : inputs : clobbers);

// Example:
int result;
asm("imull %2, %1, %0"
    : "=r" (result)          // Output: result in any register
    : "r" (a), "r" (b)       // Inputs: a, b in any register
    : "cc"                   // Clobbers: condition codes
);
```

## A.2 Operand Constraints

| Constraint | Meaning |
|------------|---------|
| `r` | Any general-purpose register |
| `a` | EAX/RAX |
| `b` | EBX/RBX |
| `c` | ECX/RCX |
| `d` | EDX/RDX |
| `S` | ESI/RSI |
| `D` | EDI/RDI |
| `m` | Memory operand |
| `i` | Immediate value |
| `0`, `1` | Match operand 0, 1 |

## A.3 Common Patterns

```c
// Read/write from memory
volatile uint32_t* reg = (uint32_t*)0x12340000;
uint32_t val;
asm volatile("movl (%1), %0" : "=r" (val) : "r" (reg));

// Inline syscall (Linux x86-64)
static inline long syscall1(long num, long arg1) {
    long ret;
    asm volatile(
        "syscall"
        : "=a" (ret)
        : "a" (num), "D" (arg1)
        : "rcx", "r11", "memory"
    );
    return ret;
}

// CPUID
unsigned int eax, ebx, ecx, edx;
asm volatile("cpuid"
    : "=a" (eax), "=b" (ebx), "=c" (ecx), "=d" (edx)
    : "a" (0)
);
```

---

# B. Bit Manipulation

## B.1 Bit Operations

```c
// Set bit n
flags |= (1 << n);

// Clear bit n
flags &= ~(1 << n);

// Toggle bit n
flags ^= (1 << n);

// Test bit n
int is_set = (flags >> n) & 1;

// Count set bits (popcount)
int count = __builtin_popcount(flags);
int count64 = __builtin_popcountll(flags64);

// Count leading zeros
int clz = __builtin_clz(flags);

// Count trailing zeros
int ctz = __builtin_ctz(flags);

// Bit width (number of bits needed)
int bw = flags ? 32 - __builtin_clz(flags) : 0;

// Rotate
int rotated_left = __builtin_rotl32(val, n);
int rotated_right = __builtin_rotr32(val, n);
```

## B.2 Bit Mask Patterns

```c
// Isolate lowest set bit
int lowest = x & (-x);

// Clear lowest set bit
x = x & (x - 1);

// Check if power of two
int is_pow2 = (x > 0) && ((x & (x - 1)) == 0);

// Round up to next power of two
x--;
x |= x >> 1;
x |= x >> 2;
x |= x >> 4;
x |= x >> 8;
x |= x >> 16;
x++;
```

---

# C. Common Syscalls Reference

## C.1 Linux x86-64 Syscall Table

| Syscall | RAX | Args |
|---------|-----|------|
| read | 0 | fd, buf, count |
| write | 1 | fd, buf, count |
| open | 2 | filename, flags, mode |
| close | 3 | fd |
| stat | 4 | filename, statbuf |
| fstat | 5 | fd, statbuf |
| mmap | 9 | addr, length, prot, flags, fd, offset |
| mprotect | 10 | addr, length, prot |
| munmap | 11 | addr, length |
| brk | 12 | end_data_segment |
| ioctl | 16 | fd, request, arg |
| access | 21 | filename, mode |
| pipe | 22 | pipefd[2] |
| dup2 | 33 | oldfd, newfd |
| fork | 57 | (none) |
| execve | 59 | filename, argv, envp |
| exit | 60 | status |
| wait4 | 61 | pid, status, options, rusage |
| kill | 62 | pid, sig |
| uname | 63 | buf |
| fcntl | 72 | fd, cmd, arg |
| getdents | 78 | fd, dirp, count |
| getcwd | 79 | buf, size |
| openat | 257 | dirfd, filename, flags, mode |

## C.2 Windows Syscall Numbers

```c
// Windows syscall numbers change between versions
// Use ntdll.dll for direct syscalls
// Common: NtCreateFile, NtWriteFile, NtReadFile, NtAllocateVirtualMemory
// Syscall number in RAX, args in RCX, RDX, R8, R9, stack
// Syscall instruction: syscall (not int 0x2e)
```

---

# D. Memory Corruption Taxonomy

## D.1 Stack-Based

| Vulnerability | Description |
|--------------|-------------|
| Stack buffer overflow | Overwrite beyond buffer boundary |
| Stack pivoting | Move RSP to attacker-controlled address |
| Return address overwrite | Overwrite saved return address |
| Format string write | Use %n to write to arbitrary address |

## D.2 Heap-Based

| Vulnerability | Description |
|--------------|-------------|
| Heap buffer overflow | Overwrite beyond heap allocation |
| Use-after-free | Access freed memory |
| Double free | Free same pointer twice |
| Type confusion | Treat memory as different type |

## D.3 Integer Issues

| Vulnerability | Description |
|--------------|-------------|
| Integer overflow | Arithmetic wraps to unexpected value |
| Signedness bug | Signed/unsigned comparison confusion |
| Size calculation error | Overflow in malloc size computation |

---

# E. Compiler Flags Reference

## E.1 GCC / Clang Security Flags

```bash
# Stack protection
-fstack-protector-strong    # Canary for functions with buffers
-fstack-protector-all       # Canary for all functions
-fstack-clash-protection    # Prevent stack clash attacks

# NX / DEP
-z noexecstack              # Non-executable stack
-z execstack                # Executable stack (insecure)

# RELRO
-z relro                    # Partial RELRO
-z relro -z now             # Full RELRO (GOT read-only)

# PIE
-fPIE -pie                  # Position-independent executable
-fPIC -shared               # Position-independent shared library

# Fortification
-D_FORTIFY_SOURCE=2         # Bounded string functions
-D_FORTIFY_SOURCE=3         # More aggressive (GCC 12+)

# Control Flow Integrity
-fsanitize=cfi              # CFI (Clang)
-fcf-protection=full        # Intel CET (shadow stack + IBT)

# Warnings
-Wall -Wextra -Werror       # All warnings as errors
-Wformat-security           # Format string warnings
-Wl,-z,noexecstack          # Linker: no exec stack
```

## E.2 Optimization Flags

```bash
-O0              # No optimization
-O1              # Basic optimizations
-O2              # Standard (recommended)
-O3              # Aggressive
-Os              # Size optimization
-Ofast           # Aggressive (may break standards)
-flto            # Link-time optimization
-funroll-loops   # Loop unrolling
-march=native    # Optimize for current CPU
```
