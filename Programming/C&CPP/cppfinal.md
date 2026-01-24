# 1. Core Language Fundamentals & Types
5286

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
| `long int`               | Long integer (32-bit or 64-bit)              | 4 or 8       | -2,147,483,648 to 2,147,483,647 (32-bit) or -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807 (64-bit) |
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

>[!NOTE] NOTE
> 0 to (2^n) -1 unsigned 
> -2^n-1 to (2^n-1) -1 signed

--- 

### 1.1.3 Low-Level/Exploit-Relevant Types


#### 1.1.3.1 `std::uint8_t` (Fixed-width Unsigned 8-bit Integer)

#### 1.1.3.2 `std::uintptr_t` (Fixed-width Unsigned Integer for Pointers)


--- 

## 1.2 Type and Literal Basics

### 1.2.1 Literals
#### 1.2.1.1 Integer Literals
- An integer literal is a primary expression of the form
##### 1.2.1.1.1 Hex Literals
- It is the character sequence 0x or the character sequence 0X followed by one or more hexadecimal digits (0, 1, 2, 3,
4, 5, 6, 7, 8, 9, a, A, b, B, c, C, d, D, e, E, f, F)
    `int hex= 0x2A;`
---
##### 1.2.1.1.2 Octal Literals
- It is the digit zero (0) followed by zero or more octal digits (0, 1, 2, 3, 4, 5, 6, 7)
    `int oct= 052;`
---
##### 1.2.1.1.3 Decimal Literals
- It is a non-zero decimal digit (1, 2, 3, 4, 5, 6, 7, 8, 9), followed by zero or more decimal digits (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    `int dec= 42;`
---
##### 1.2.1.1.4 Boolean Literal(binary-literal)(since C++14)
- It is the character sequence 0b or the character sequence 0B followed by one or more binary digits (0, 1)
    `int bin= 0b101010;`

--- 

#### 1.2.1.2 Floating-point Literal
The Floating-point literals in C++ are the values that represent numbers with the fractional or decimal part. These can be either single-precision or double-precision values.

Like integer literals, the floating-point literals can also be defined as double or float by using suffix d and f respectively. By default, all the fractional numbers are considered to be of type double by C++ compiler if not specified.

##### 1.2.1.2.1 Float Literals (Suffix: f or F)
- Floating point literals are specified by adding f or F as a suffix to fractional values.
    `float f= 3.14f`
---
##### 1.2.1.2.2 Double Literals (Suffix: d or D)
- The double precision floating point literals are the default literals for fractional values but can also be manually specified.
    `double d = 3.14;`
---
##### 1.2.1.2.3 Scientific Notation
- The scientific notations help us to represent very large or small value in compact form.
    `long double ld = 1.22e11`
    `long double ld = 1.22e-11`
---
##### 1.2.1.2.4 Long Double Literals (Suffix: l or L)
- The long double floating point literals can be specified using l or L as a suffix to fractional values.
`long double ld = 3.14l;`

---
#### 1.2.1.3 Integer-Suffixes

- u or U: Indicates an unsigned integer. `123U`
- l or L: Indicates a long integer. `123L`
- ul or UL, lu or LU: Indicates an unsigned long integer. `123UL`
- ll or LL: Indicates a long long integer (on systems where long long is a distinct data type). `123LL`
- ull or ULL: Indicates an unsigned long long integer. `123ULL`

--- 

#### 1.2.1.4 Character Literals
The character literals in C++ are values that represent individual characters or escape sequences. They are enclosed in single quotes, and you can use them to represent the single character. As C++ using ASCII character set, there are 128 possible character literals.
    `char c = 'A';`

---

#### 1.2.1.5 String Literals
The string literals in C++ are the sequences of the characters enclosed in double quotes, and you can use them to represent text or character sequences.

    `const char* stringLiteral = "Hello, World!";`

--- 

#### 1.2.1.6 Boolean Literals
The boolean literals represent the truth values and have only two possible values: true and false. These values are used in the Boolean expressions and logic operations.
    `bool isTrue = true;`
    `bool isFalse = false;`

--- 

### 1.2.2 Booleans
#### 1.2.2.1 bool
A Literal used for stating two states of possible value 0/1 T/F
#### 1.2.2.2 true
- A keyword denoting one of the two possible values of type bool.
`bool test = true;`
#### 1.2.2.3 false (Representation: 1, 0)
- A keyword denoting one of the two possible values of type bool.
`bool test = false;`

--- 

### 1.2.3 Type Aliases
#### 1.2.3.1 typedef
- A typedef declaration has the same syntax as a variable or function declaration, but it contains the word typedef.
- The presence of typedef causes the declaration to declare a type instead of a variable or function.
- Once a type alias has been defined, it can be used interchangeably with the original name of the type
- typedef never creates a distinct type. It only gives another way of referring to an existing type.
```cpp 
int T;         // T has type int
typedef int T; // T is an alias for int
int A[100];         // A has type "array of 100 ints"
typedef int A[100]; // A is an alias for the type "array of 100 ints"

typedef int A[100];
// S is a struct containing an array of 100 ints
struct S {
    A data;
};

struct S {
    int f(int);
};
typedef int I;
// ok: defines int S::f(int)
I S::f(I x) { return x; }
```
##### Complex uses of typedef

1. typedef and Function Pointers:
- A function pointer type can be complicated to write, but typedef helps simplify it.

Without typedef: `void (*f)(int);  // f is a pointer to a function that takes an int and returns void`
With typedef: `typedef void (*f)(int);  // f is an alias for "pointer to function of int returning void"`
- Here, f is a shorthand for the pointer-to-function type, so the code is easier to understand and use later.

2. typedef and Pointers to Member Functions:
- Pointers to member functions are tricky because their syntax is more complex than regular function pointers.

Without typedef:`void (Foo::*pmf)(int);  // pmf is a pointer to a member function of Foo that takes int and returns void`
With typedef: `typedef void (Foo::*pmf)(int);  // pmf is an alias for "pointer to member function of Foo"`
- The typedef makes the code clearer and easier to manage.

3. Complex Declarations Simplified with typedef:
- Some function declarations can be quite complex to understand at first glance.

`void (Foo::*Foo::f(const char*))(int);`
Explanation: This declares a member function f of Foo that takes a const char* and returns a pointer to a function that takes an int and returns void.

`int (&g())[100];`
Explanation: This declares a function g() that returns a reference to an array of 100 int values.

```cpp
typedef void (Foo::pmf)(int);  // pmf is a pointer to member function type
pmf Foo::f(const char*);       // f is a member function of Foo
typedef int (&ra
```

--- 

#### 1.2.3.2 using
The syntax of using is very simple: the name to be defined goes on the left hand side, and the definition goes on
the right hand side. No need to scan to see where the name is.
```cpp 
using I = int;
using A = int[100];             // array of 100 ints
using FP = void(*)(int);        // pointer to function of int returning void
using MP = void (Foo::*)(int);  // pointer to member function of Foo of int returning void
```
- Creating a type alias with using has exactly the same effect as creating a type alias with typedef. It is simply an alternative syntax for accomplishing the same thing.
- Unlike typedef, using can be templated. A "template typedef" created with using is called an alias template.

--- 

### 1.2.4 Enums
#### 1.2.4.1 Enum Basics
An `enum` (short for "enumeration") is a user-defined data type that consists of a set of named integer constants. Enums are primarily used to assign symbolic names to a set of values, improving code readability and maintainability.

An enum is declared using the `enum` keyword, followed by the name of the enum and a list of constant values.

Example:
```cpp
enum Color {
    RED,    // Default value: 0
    GREEN,  // Default value: 1
    BLUE    // Default value: 2
};
````

In the above example, `RED` gets assigned the value `0`, `GREEN` gets assigned `1`, and `BLUE` gets assigned `2` by default. The value of each element can be explicitly set if needed.

--- 
#### 1.2.4.2 Enum with `std::underlying_type` and `std::to_underlying`

By default, the underlying type of an enum is usually `int`, but it can vary depending on the compiler. C++11 introduced the `std::underlying_type` which allows you to find the underlying type of an enum.

You can use `std::to_underlying()` to safely cast an enum value to its underlying type, which is especially useful when working with enums in functions that require integral values.

##### 1.2.4.2.1 `std::underlying_type`

`std::underlying_type` is a template that provides the underlying type of the enum. It’s typically used to work with enums in a more type-safe manner.

Example:

```cpp
#include <iostream>
#include <type_traits>

enum Color {
    RED = 1,
    GREEN = 5,
    BLUE = 10
};

int main() {
    std::cout << "Underlying type of Color: " 
              << typeid(std::underlying_type<Color>::type).name() << std::endl;
    return 0;
}
```

Output:
```Underlying type of Color: int```

---
##### 1.2.4.2.2 `std::to_underlying()`
The `std::to_underlying()` function provides a safe way to convert enum values to their underlying integral type. This is important because directly casting enums to integers may lead to issues if not done properly.

Example:

```cpp
#include <iostream>
#include <type_traits>

enum Color {
    RED = 1,
    GREEN = 5,
    BLUE = 10
};

int main() {
    Color color = GREEN;
    int colorValue = std::to_underlying(color);  // Safe conversion to underlying type
    std::cout << "Color value: " << colorValue << std::endl;
    return 0;
}
```

Output:

```Color value: 5```

---
#### 1.2.4.3 Enum Bitfields (Flags)
Enums can be used as bit flags to represent multiple options in a single variable. This is useful for things like permissions or settings where each bit represents a different option.

To define bit flags, the enum values are typically powers of two.

Example:

```cpp
enum class Permissions {
    READ = 1 << 0,   // 0001
    WRITE = 1 << 1,  // 0010
    EXECUTE = 1 << 2 // 0100
};

Permissions p = Permissions::READ | Permissions::EXECUTE; // Combine flags using bitwise OR
```

---
#### 1.2.4.4 Comparison between Regular Enum and Enum Class

* Regular enums expose their values directly, making it easy to accidentally use the wrong value.
* `enum class` restricts access to values and forces explicit casting to the underlying type, which increases safety.

Regular Enum:

```cpp
enum Color {
    RED = 1,
    GREEN = 2
};
```

Accessed directly:

```cpp
Color color = RED;
```

Enum Class:

```cpp
enum class Color {
    RED = 1,
    GREEN = 2
};
```

Accessed using the enum name:

```cpp
Color color = Color::RED;
```

---
## 1.3 Operators & Misc

### 1.3.1 String Manipulation
#### 1.3.1.1 std::string
`std::string` is a sequence of characters that can be manipulated using various methods provided by the C++ Standard Library. It's part of the `<string>` header and is widely used for working with text data.

Example:
```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "Hello, World!";
    std::cout << str << std::endl;
    return 0;
}
````

Here, the string `"Hello, World!"` is stored in a `std::string` variable `str`.

---
#### 1.3.1.2 Concatenation
String concatenation is the process of joining two or more strings together. In C++, this is done using the `+` operator or the `.append()` method.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str1 = "Hello, ";
    std::string str2 = "World!";
    std::string result = str1 + str2;  // Concatenation using '+'
    std::cout << result << std::endl;
    return 0;
}
```

Output:

```
Hello, World!
```

You can also use `.append()` to add a string to another:

```cpp
str1.append(str2);  // Same as str1 + str2
```

---
#### 1.3.1.3 .length()
The `.length()` method returns the number of characters in the string (excluding the null-terminator).

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "Hello, World!";
    std::cout << "Length: " << str.length() << std::endl;  // Outputs: 13
    return 0;
}
```

Output:

```
Length: 13
```

---
#### 1.3.1.4 .size()
The `.size()` method is essentially the same as `.length()`. It returns the number of characters in the string, and both can be used interchangeably.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    std::cout << "Size: " << str.size() << std::endl;  // Outputs: 15
    return 0;
}
```

Output:

```
Size: 15
```

---
#### 1.3.1.5 .at(index)
The `.at(index)` method returns the character at the specified index, and it performs bounds checking, which means it throws an `out_of_range` exception if the index is invalid.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    std::cout << "Character at index 4: " << str.at(4) << std::endl;  // Outputs: 'P'
    return 0;
}
```

Output:

```
Character at index 4: P
```

If you try accessing an invalid index:

```cpp
std::cout << str.at(20);  // Throws std::out_of_range exception
```

---
#### 1.3.1.6 [index]
Using the square bracket `[]` operator is another way to access a character in a string. Unlike `.at()`, it doesn't perform bounds checking, which can lead to undefined behavior if the index is out of range.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    std::cout << "Character at index 4: " << str[4] << std::endl;  // Outputs: 'P'
    return 0;
}
```

Output:

```
Character at index 4: P
```

Be cautious when using `[]` as accessing an invalid index could lead to crashes or undefined behavior.

---
#### 1.3.1.7 getline
`std::getline()` is used to read an entire line of input, including spaces, until a newline character is encountered. It reads input from an input stream (e.g., `std::cin`).

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string line;
    std::cout << "Enter a line of text: ";
    std::getline(std::cin, line);  // Reads the entire line
    std::cout << "You entered: " << line << std::endl;
    return 0;
}
```

Output:

```
Enter a line of text: This is a line with spaces.
You entered: This is a line with spaces.
```

---
#### 1.3.1.8 std::toupper
`std::toupper` is a function from the `<cctype>` header that converts a single character to its uppercase form.

Example:

```cpp
#include <iostream>
#include <cctype>

int main() {
    char c = 'a';
    std::cout << "Uppercase: " << std::toupper(c) << std::endl;  // Outputs: 'A'
    return 0;
}
```

Output:

```
Uppercase: A
```

It only works on a single character, so you may need to iterate over a string if you want to convert the whole string.

---
#### 1.3.1.9 std::tolower
`std::tolower` works similarly to `std::toupper` but converts a single character to its lowercase form.

Example:

```cpp
#include <iostream>
#include <cctype>

int main() {
    char c = 'A';
    std::cout << "Lowercase: " << std::tolower(c) << std::endl;  // Outputs: 'a'
    return 0;
}
```

Output:

```
Lowercase: a
```

For a whole string, loop through each character:

```cpp
std::string str = "HELLO";
for (char &c : str) {
    c = std::tolower(c);
}
```

---
#### 1.3.1.10 std::towupper
`std::towupper` is similar to `std::toupper`, but it works with wide characters (`wchar_t`). It’s useful when working with wide character strings (`std::wstring`).

Example:

```cpp
#include <iostream>
#include <cwctype>

int main() {
    wchar_t wc = L'a';
    std::wcout << L"Uppercase: " << std::towupper(wc) << std::endl;  // Outputs: 'A'
    return 0;
}
```

Output:

```
Uppercase: A
```

---
#### 1.3.1.11 std::towlower
`std::towlower` works similarly to `std::tolower` but for wide characters.

Example:

```cpp
#include <iostream>
#include <cwctype>

int main() {
    wchar_t wc = L'A';
    std::wcout << L"Lowercase: " << std::towlower(wc) << std::endl;  // Outputs: 'a'
    return 0;
}
```

Output:

```
Lowercase: a
```

---
#### 1.3.1.12 std::stoi
`std::stoi` is a function that converts a string to an integer. It's part of the `<string>` header and is useful for converting numeric strings to integer types.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "12345";
    int number = std::stoi(str);  // Converts string to integer
    std::cout << "Integer value: " << number << std::endl;  // Outputs: 12345
    return 0;
}
```

Output:

```
Integer value: 12345
```

`std::stoi` throws an exception if the conversion fails (e.g., if the string contains non-numeric characters).

---
#### 1.3.1.13 std::stof
`std::stof` is a function from the `<string>` header that converts a string to a `float`. It is useful when you need to extract floating-point values from a string.

Example:
```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "3.14";
    float num = std::stof(str);  // Converts string to float
    std::cout << "Float value: " << num << std::endl;  // Outputs: 3.14
    return 0;
}
````

Output:

```
Float value: 3.14
```

`std::stof` throws an exception (`std::invalid_argument` or `std::out_of_range`) if the string is not a valid float.

---
#### 1.3.1.14 std::to_string

`std::to_string` is a function that converts numeric values of various types (e.g., `int`, `float`, `double`, `long`) to their string representation. It's part of the `<string>` header.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    int num = 42;
    std::string str = std::to_string(num);  // Converts integer to string
    std::cout << "String value: " << str << std::endl;  // Outputs: "42"
    return 0;
}
```

Output:

```
String value: 42
```

You can also use `std::to_string` for other numeric types:

```cpp
double pi = 3.14159;
std::string pi_str = std::to_string(pi);  // "3.141590"
```

---
### 1.3.1.14 std::string::find

The `.find()` method is used to search for a substring within a string. It returns the index of the first occurrence of the substring, or `std::string::npos` if the substring is not found.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    size_t pos = str.find("Programming");  // Finds the substring "Programming"
    
    if (pos != std::string::npos) {
        std::cout << "Found at position: " << pos << std::endl;  // Outputs: 3
    } else {
        std::cout << "Substring not found!" << std::endl;
    }
    
    return 0;
}
```

Output:

```
Found at position: 3
```

You can also find characters:

```cpp
size_t pos = str.find('P');  // Finds first 'P' character
```

---
#### 1.3.1.15 std::string::find (with start position)

You can specify a starting position in `.find()`, so it searches from that point onwards.

Example:

```cpp
size_t pos = str.find("P", 4);  // Start searching from index 4
```

---
#### 1.3.1.16 std::string::replace

The `.replace()` method allows you to replace a portion of the string with another string. It accepts the starting position, the length of the portion to replace, and the new string to insert.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    str.replace(0, 3, "Java");  // Replace "C++" with "Java"
    std::cout << str << std::endl;  // Outputs: "Java Programming"
    return 0;
}
```

Output:

```
Java Programming
```

You can replace a single character as well:

```cpp
str.replace(0, 1, "X");  // Replace 'J' with 'X'
```
---
#### 1.3.1.17 std::string::replace (with iterators)

You can also replace part of the string using iterators.

Example:

```cpp
std::string str = "Hello, World!";
str.replace(str.begin() + 7, str.end(), "Everyone");  // Replace from position 7 to the end
std::cout << str << std::endl;  // Outputs: "Hello, Everyone"
```

---
#### 1.3.1.18 std::string::substr

The `.substr()` method is used to extract a substring from the string. You provide the starting index and the length of the substring to extract.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    std::string sub = str.substr(4, 11);  // Extract substring starting from index 4, length 11
    std::cout << sub << std::endl;  // Outputs: "Programming"
    return 0;
}
```

Output:

```
Programming
```

If the length is not specified, the substring goes to the end of the string:

```cpp
std::string sub = str.substr(4);  // Extract substring starting from index 4 to end
```

---
#### 1.3.1.19 std::string::insert

The `.insert()` method is used to insert a string or character at a specific position within the original string.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C Programming";
    str.insert(2, "++ ");  // Insert "++ " at index 2
    std::cout << str << std::endl;  // Outputs: "C++ Programming"
    return 0;
}
```

Output:

```
C++ Programming
```

You can also insert a character at a specific position:

```cpp
str.insert(7, 3, '!');  // Insert '!!!' at position 7
```

---
#### 1.3.1.20 std::string::erase

The `.erase()` method removes characters from a string. You can specify the position and the number of characters to remove.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    str.erase(4, 2);  // Erase 2 characters starting at position 4
    std::cout << str << std::endl;  // Outputs: "C Programming"
    return 0;
}
```

Output:

```
C Programming
```

You can also erase from a specific position to the end:

```cpp
str.erase(4);  // Erase from position 4 to the end
```

---
#### 1.3.1.21 std::string::compare

The `.compare()` method compares two strings lexicographically. It returns:

* `0` if the strings are equal,
* a negative value if the calling string is less than the compared string,
* a positive value if the calling string is greater than the compared string.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str1 = "Apple";
    std::string str2 = "Banana";
    
    if (str1.compare(str2) < 0) {
        std::cout << str1 << " is less than " << str2 << std::endl;
    } else if (str1.compare(str2) > 0) {
        std::cout << str1 << " is greater than " << str2 << std::endl;
    } else {
        std::cout << str1 << " is equal to " << str2 << std::endl;
    }
    return 0;
}
```

Output:

```
Apple is less than Banana
```

---
#### 1.3.1.22 std::string::c_str

The `.c_str()` method returns a pointer to a null-terminated C-style string (i.e., a `const char*`) that represents the content of the `std::string`. This is useful when working with APIs that require C-style strings.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    const char* cstr = str.c_str();  // Get C-style string
    std::cout << cstr << std::endl;  // Outputs: "C++ Programming"
    return 0;
}
```

Output:

```
C++ Programming
```

---
#### 1.3.1.23 std::string::clear

The `.clear()` method removes all characters from the string, effectively making it an empty string.

Example:

```cpp
#include <iostream>
#include <string>

int main() {
    std::string str = "C++ Programming";
    str.clear();  // Clears the string
    std::cout << "String after clear: '" << str << "'" << std::endl;  // Outputs: ""
    return 0;
}
```

Output:

```
String after clear: ''
```

--- 
### 1.3.2 Operators
#### 1.3.2.1 Arithmetic Operators
Arithmetic operators are used to perform basic mathematical operations such as addition, subtraction, multiplication, and division on numeric values.

- **`+`**: Addition
- **`-`**: Subtraction
- **`*`**: Multiplication
- **`/`**: Division
- **`%`**: Modulus (remainder after division)

#### Example:
```cpp
#include <iostream>

int main() {
    int a = 10, b = 3;
    
    std::cout << "Addition: " << (a + b) << std::endl;  // 13
    std::cout << "Subtraction: " << (a - b) << std::endl;  // 7
    std::cout << "Multiplication: " << (a * b) << std::endl;  // 30
    std::cout << "Division: " << (a / b) << std::endl;  // 3 (integer division)
    std::cout << "Modulus: " << (a % b) << std::endl;  // 1

    return 0;
}
````

Output:

```
Addition: 13
Subtraction: 7
Multiplication: 30
Division: 3
Modulus: 1
```

**Note:** For division, if both operands are integers, the result is also an integer. To perform floating-point division, at least one operand should be a `float` or `double`.

---
#### 1.3.2.2 Comparison Operators
Comparison operators are used to compare two values or expressions. These operators return a boolean value (`true` or `false`).

* **`==`**: Equal to
* **`!=`**: Not equal to
* **`>`**: Greater than
* **`<`**: Less than
* **`>=`**: Greater than or equal to
* **`<=`**: Less than or equal to

#### Example:

```cpp
#include <iostream>

int main() {
    int a = 10, b = 5;

    std::cout << "a == b: " << (a == b) << std::endl;  // false (0)
    std::cout << "a != b: " << (a != b) << std::endl;  // true (1)
    std::cout << "a > b: " << (a > b) << std::endl;    // true (1)
    std::cout << "a < b: " << (a < b) << std::endl;    // false (0)
    std::cout << "a >= b: " << (a >= b) << std::endl;  // true (1)
    std::cout << "a <= b: " << (a <= b) << std::endl;  // false (0)

    return 0;
}
```

Output:

```
a == b: 0
a != b: 1
a > b: 1
a < b: 0
a >= b: 1
a <= b: 0
```

**Note:** Comparison operators are frequently used in conditional statements such as `if`, `while`, and `for` to control program flow based on values.

---
#### 1.3.2.3 Logical Operators (&&, ||, !)
Logical operators are used to combine or negate conditional expressions. These operators are essential in controlling flow based on boolean logic.

* **`&&` (AND)**: Returns `true` if both conditions are true.
* **`||` (OR)**: Returns `true` if at least one condition is true.
* **`!` (NOT)**: Negates the boolean value; returns `true` if the condition is false, and vice versa.

#### Example:

```cpp
#include <iostream>

int main() {
    bool a = true, b = false;

    // AND (&&)
    std::cout << "(a && b): " << (a && b) << std::endl;  // false (0)

    // OR (||)
    std::cout << "(a || b): " << (a || b) << std::endl;  // true (1)

    // NOT (!)
    std::cout << "(!a): " << (!a) << std::endl;  // false (0)
    std::cout << "(!b): " << (!b) << std::endl;  // true (1)

    return 0;
}
```

Output:

```
(a && b): 0
(a || b): 1
(!a): 0
(!b): 1
```

**Logical AND (&&)**: Both operands must be true for the result to be true.

```cpp
if (a && b) {
    // This block will not execute because b is false
}
```

**Logical OR (||)**: At least one operand must be true for the result to be true.

```cpp
if (a || b) {
    // This block will execute because a is true
}
```

**Logical NOT (!)**

```cpp
if (!a) {
    // This block will not execute because a is true
}
```

Logical operators are commonly used in `if` statements, loops, and other conditional structures to control program flow based on multiple conditions.

--- 
### 1.3.3 Misc
#### 1.3.3.1 sizeof
`sizeof` is an operator in C++ that returns the size (in bytes) of a variable or data type. It's commonly used to determine the memory footprint of types and variables.

- Examples
```cpp
#include <iostream>

int main() {
    int x = 42;
    double y = 3.14;
    
    std::cout << "Size of int: " << sizeof(int) << " bytes" << std::endl;   // Typically 4 bytes
    std::cout << "Size of x: " << sizeof(x) << " bytes" << std::endl;       // Depends on system, typically 4 bytes
    std::cout << "Size of double: " << sizeof(double) << " bytes" << std::endl;  // Typically 8 bytes
    std::cout << "Size of y: " << sizeof(y) << " bytes" << std::endl;       // Depends on system, typically 8 bytes
    
    return 0;
}
````

Output:

```
Size of int: 4 bytes
Size of x: 4 bytes
Size of double: 8 bytes
Size of y: 8 bytes
```

* `sizeof` can be applied to variables, data types, and even arrays or structures.
* For dynamic memory allocation (like pointers), it gives the size of the pointer, not the allocated memory.

**Note:** `sizeof` returns a value of type `size_t`, which is an unsigned integer type capable of storing the size of any object.

---
#### 1.3.3.2 strlen
`strlen` is a function from the `<cstring>` header that returns the length of a C-style string (null-terminated character array). It does **not** count the null-terminator (`'\0'`).

- Example
```cpp
#include <iostream>
#include <cstring>

int main() {
    const char* str = "Hello, World!";
    
    std::cout << "Length of string: " << strlen(str) << std::endl;  // 13 (doesn't count null-terminator)
    
    return 0;
}
```

Output:

```
Length of string: 13
```

* `strlen` is useful for working with C-style strings (`const char*`) but does not work directly with `std::string`.

---

#### 1.3.3.3 typeid (RTTI)
`typeid` is used to obtain type information about an object or type during runtime. This is part of C++'s **Run-Time Type Information (RTTI)** feature, which allows you to query the type of polymorphic objects.

* `typeid` returns a reference to a `std::type_info` object.
* It can be used with pointers and references, and when applied to polymorphic types, it will return the actual type of the object.

- Example
```cpp
#include <iostream>
#include <typeinfo>

class Base {
public:
    virtual void show() { std::cout << "Base class\n"; }
};

class Derived : public Base {
public:
    void show() override { std::cout << "Derived class\n"; }
};

int main() {
    Base* ptr = new Derived();
    
    std::cout << "Type of ptr: " << typeid(*ptr).name() << std::endl;  // Actual type of object is Derived
    
    delete ptr;
    return 0;
}
```

Output:

```
Type of ptr: Derived
```

**Note:**

* `typeid` can be especially useful when working with polymorphic types (i.e., classes with virtual functions).
* `typeid` works at runtime for polymorphic objects, but it gives compile-time information for non-polymorphic types.

---
#### 1.3.3.4 auto
`auto` is a keyword in C++ that allows the compiler to automatically deduce the type of a variable based on its initializer. This is particularly useful for reducing redundancy in type declarations and for working with complex types.

- Example
```cpp
#include <iostream>
#include <vector>

int main() {
    auto x = 10;          // auto deduces type as int
    auto y = 3.14;        // auto deduces type as double
    auto str = "Hello";   // auto deduces type as const char*
    
    std::cout << "x: " << x << ", y: " << y << ", str: " << str << std::endl;
    
    std::vector<int> v = {1, 2, 3};
    for (auto it = v.begin(); it != v.end(); ++it) {
        std::cout << *it << " ";
    }

    return 0;
}
```

Output:

```
x: 10, y: 3.14, str: Hello
1 2 3 
```

* `auto` is commonly used with iterators or when the type is obvious from context (e.g., for variables with complicated types like containers).
* It improves code maintainability and readability by reducing the need to explicitly write out types.

**Note:** `auto` must be initialized with a value to let the compiler deduce its type.

---
#### 1.3.3.5 Overflow
Overflow occurs when an arithmetic operation results in a value that exceeds the maximum or minimum limit of a data type. In C++, this can happen when performing arithmetic on integers or floating-point numbers.

##### 1.3.3.5.1 Integer Overflow

When an integer exceeds its type’s maximum value, it wraps around and produces undefined results. The same happens for negative overflow.

Example (signed integer overflow):

```cpp
#include <iostream>
#include <climits>  // For INT_MAX

int main() {
    int max = INT_MAX;  // Maximum value for int (usually 2147483647 on most systems)
    
    std::cout << "Max int: " << max << std::endl;
    
    int overflow = max + 1;  // This will cause overflow
    std::cout << "Overflowed value: " << overflow << std::endl;  // Undefined behavior

    return 0;
}
```

Output (varies based on compiler and system):

```
Max int: 2147483647
Overflowed value: -2147483648
```

---
##### 1.3.3.5.2 Floating-Point Overflow

Overflow also applies to floating-point types, where the value exceeds the maximum representable value (`INFINITY` in `<cmath>`). It may cause the program to produce infinity (`inf`).

Example (float overflow):

```cpp
#include <iostream>
#include <cmath>

int main() {
    float largeValue = 1e38f;  // A very large float
    std::cout << "Large Value: " << largeValue << std::endl;

    float overflow = largeValue * 10.0f;  // This will overflow
    std::cout << "Overflowed value: " << overflow << std::endl;  // Outputs: inf

    return 0;
}
```

Output:

```
Large Value: 1e+38
Overflowed value: inf
```

---
##### 1.3.3.5.3 Preventing Overflow

* **Unsigned Types**: For unsigned types, overflow wraps around starting from 0.
* **Checks**: You can prevent overflow by checking conditions before performing operations (e.g., check for addition/subtraction that exceeds limits).
* **Libraries**: Some compilers provide extensions or libraries (like `std::overflow_error`) to handle overflow in a more controlled way.
--- 

## 1.4 Object Model & Evaluation Semantics

### 1.4.1 Storage Duration & Lifetime
Storage duration refers to the period during which the memory occupied by an object is reserved, and the object itself exists. The lifetime of an object refers to the period when the object is fully constructed and usable. C++ provides various categories for storage duration and object lifetime to manage resources effectively.

#### 1.4.1.1 Automatic Storage Duration
Automatic storage duration refers to variables that are created when the program enters a block (like a function or a loop) and are destroyed when the block is exited. These variables are stored on the stack and are typically local variables.

- **Local variables** have automatic storage duration by default.
- These objects are automatically created and destroyed, so there is no need for manual memory management (e.g., `delete` or `free`).

#### Example:
```cpp
#include <iostream>

void function() {
    int x = 5;  // Automatic storage duration
    std::cout << "x: " << x << std::endl;
}  // 'x' is destroyed when function exits

int main() {
    function();
    return 0;
}
````

In this example, the local variable `x` is automatically created when the function `function()` is called, and destroyed when the function exits.

**Note**: The lifetime of the object is tied to the scope in which it was declared, and it is automatically destroyed when the scope ends.

---
#### 1.4.1.2 Static Storage Duration
Static storage duration means that the variable or object exists for the entire duration of the program’s execution. Static variables are initialized only once and retain their values between function calls.

* **Global variables**, **static variables**, and **constants** have static storage duration.
* The memory for static objects is allocated before `main()` begins and deallocated after the program terminates.

#### Example:

```cpp
#include <iostream>

void function() {
    static int count = 0;  // Static variable retains value between function calls
    count++;
    std::cout << "Count: " << count << std::endl;
}

int main() {
    function();  // Count: 1
    function();  // Count: 2
    function();  // Count: 3
    return 0;
}
```

Output:

```
Count: 1
Count: 2
Count: 3
```

In this case, `count` is a static variable, meaning it persists across multiple calls to `function()`, and it retains its state between calls.

**Note**: Static variables are initialized only once, and they exist throughout the entire program runtime. They can be used inside functions (declared as `static`) or outside functions (as global variables).

---
#### 1.4.1.3 Dynamic Storage Duration
Dynamic storage duration applies to memory that is allocated at runtime using operators like `new` or `malloc` and must be manually deallocated using `delete` or `free`.

* Objects with dynamic storage duration are created during the execution of the program and exist until they are explicitly destroyed.
* Dynamic memory is allocated from the heap and can be resized or freed during the program’s execution.

- Example:

```cpp
#include <iostream>

int main() {
    int* ptr = new int(5);  // Dynamically allocated memory
    std::cout << "Value: " << *ptr << std::endl;
    
    delete ptr;  // Memory deallocation
    return 0;
}
```

Output:

```
Value: 5
```

In this example, `ptr` points to dynamically allocated memory that holds the value `5`. The memory must be manually deallocated using `delete`.

**Note**: Failing to deallocate memory causes **memory leaks**. It is crucial to always `delete` or `free` dynamically allocated memory when it's no longer needed.

---
#### 1.4.1.4 Thread-Local Storage Duration
Thread-local storage duration is a feature that allows variables to be specific to each thread in a multi-threaded program. These variables are created when a thread begins and destroyed when the thread terminates.

* Variables with thread-local storage duration are initialized at thread start and are destroyed when the thread finishes.
* You can declare thread-local variables using the `thread_local` keyword.

#### Example:

```cpp
#include <iostream>
#include <thread>

thread_local int count = 0;  // Thread-local variable

void increment() {
    count++;
    std::cout << "Thread-local count: " << count << std::endl;
}

int main() {
    std::thread t1(increment);
    std::thread t2(increment);
    
    t1.join();
    t2.join();
    
    return 0;
}
```

Output:

```
Thread-local count: 1
Thread-local count: 1
```

Here, `count` is a thread-local variable, meaning each thread has its own instance of `count`. The value of `count` is independent across threads, and each thread can modify its own version of `count` without interfering with other threads.

**Note**: `thread_local` ensures that each thread has its own instance of a variable, which is important for thread safety.

---
#### 1.4.1.5 Object Lifetime vs Storage Duration
While storage duration defines the period during which an object occupies memory, **object lifetime** defines the period during which the object is constructed and usable.

* **Storage duration** refers to when the memory for an object is allocated and deallocated.
* **Object lifetime** refers to the time during which the object is constructed and destructed.

#### Example (Object Lifetime vs Storage Duration):

```cpp
#include <iostream>

class MyClass {
public:
    MyClass() { std::cout << "Object created!" << std::endl; }
    ~MyClass() { std::cout << "Object destroyed!" << std::endl; }
};

int main() {
    MyClass obj;  // Object is created here, and its lifetime is tied to scope
    return 0;
}
```

Output:

```
Object created!
Object destroyed!
```

* In this example, `obj` has **automatic storage duration** (since it’s a local variable), and its **lifetime** begins when it’s created and ends when the scope (function) ends. The memory is automatically released when the scope is exited, and the destructor is called at that point.

**Key Difference**:

* **Storage Duration**: How long an object exists in memory.
* **Object Lifetime**: The duration for which an object is constructed and usable in its given context.

**Note**: For dynamically allocated memory (`new`/`malloc`), the **storage duration** lasts as long as the memory remains allocated, and the **lifetime** of the object continues until the memory is deallocated using `delete` or `free`.

---
### 1.4.2 Evaluation Order & Sequencing
In C++, **evaluation order** refers to the order in which expressions are evaluated, and **sequencing** refers to the rules that define how and when operations are executed relative to each other. These concepts are important for avoiding bugs and undefined behavior in your programs.

#### 1.4.2.1 Order of Evaluation (Pre-C++17 vs C++17+)
In C++ prior to C++17, the order in which function arguments, operands of operators, and expressions were evaluated was largely unspecified, leading to potential undefined behavior or unexpected results.

- **Pre-C++17**: The C++ standard did not specify the order of evaluation for function arguments or operands. This means that, for example, the order in which arguments to a function were evaluated could vary between compilers or compiler settings.

```cpp
#include <iostream>

int foo(int a, int b) {
  std::cout << "foo(" << a << ", " << b << ")" << std::endl;
  return a + b;
}

int main() {
  int x = 2, y = 3;
  foo(x++, ++y);  // Undefined order of evaluation
  return 0;
}
```

In this case, it's unclear whether `x++` or `++y` will be evaluated first, which could result in different outputs or behaviors depending on the compiler.

* **C++17 and Beyond**: Starting from C++17, the order of evaluation has been defined for certain expressions. Specifically:

  * **Function arguments** are evaluated in the order they appear in the parameter list (left-to-right).
  * **Operator operands** are evaluated in left-to-right order for most operators (e.g., `+`, `-`, `*`), but there are still exceptions for some operators like the comma operator (`,`), where the left-hand side is evaluated first.

  This change ensures that you can rely on consistent evaluation order across compilers and platforms.

- Example (C++17)

```cpp
#include <iostream>

int add(int a, int b) {
    std::cout << "add(" << a << ", " << b << ")" << std::endl;
    return a + b;
}

int main() {
    int x = 2, y = 3;
    add(x++, ++y);  // Evaluated left-to-right in C++17 and beyond
    return 0;
}
```

Output:
```add(2, 4)```

In this example, `x++` is evaluated first (evaluating `x` to `2`), and then `++y` is evaluated (evaluating `y` to `4`).

---
#### 1.4.2.2 Sequence Points
A **sequence point** is a point in the program where all previous evaluations (such as function calls, assignments, and operators) must be completed before any further evaluations occur. Sequence points prevent undefined behavior by ensuring that evaluations happen in a well-defined order.

Common sequence points include:

* The **end of a full expression** (e.g., after the right-hand side of an assignment).
* **Function calls** (after arguments are evaluated but before the function body starts executing).
* The **semicolon** at the end of a statement.

- Example of a Sequence Points

```cpp
#include <iostream>

int main() {
    int a = 5, b = 10;
    a = b + 2;  // '=' is a sequence point (b + 2 is evaluated before assignment)
    std::cout << "a: " << a << ", b: " << b << std::endl;  // Output: a: 12, b: 10
    return 0;
}
```

In the statement `a = b + 2`, the expression `b + 2` is evaluated first (before the assignment), and the assignment happens after that, marking the sequence point. This ensures the evaluation order is clear.

**Important Sequence Points**:

* **Semicolons** (`;`) separate statements, ensuring that previous expressions are fully evaluated.
* **Commas** in a `for` loop, function arguments, or initializer lists ensure that all expressions before the comma are evaluated before the next expression.

---
#### 1.4.2.3 Short-Circuit Guarantees
Short-circuiting is a behavior of logical operators (`&&`, `||`) where the second operand is not evaluated if the result can be determined from the first operand.

* **`&&` (Logical AND)**: If the first operand is false, the second operand is not evaluated because the overall result will be false.
* **`||` (Logical OR)**: If the first operand is true, the second operand is not evaluated because the overall result will be true.

Short-circuiting ensures that only the necessary conditions are evaluated, which can be useful for performance and preventing undefined behavior (e.g., avoiding a null pointer dereference).

- Example
```cpp
#include <iostream>

bool isNull(int* ptr) {
    return ptr == nullptr;
}

int main() {
    int* ptr = nullptr;
    if (!isNull(ptr) && *ptr > 0) {  // The second condition is not evaluated because the first is false
        std::cout << "*ptr is greater than 0" << std::endl;
    } else {
        std::cout << "Second condition was not evaluated" << std::endl;
    }
    return 0;
}
```

Output:

```
Second condition was not evaluated
```

* In the above example, since `isNull(ptr)` returns `true` (because `ptr` is `nullptr`), the second part of the condition (`*ptr > 0`) is not evaluated, thus avoiding a potential **segmentation fault**.

Short-circuiting can also be used in conditionals to avoid expensive or unsafe operations.

---
#### 1.4.2.4 Undefined Behavior from Unsequenced Access
Accessing the same variable multiple times in an expression without a clear sequence of operations can lead to **undefined behavior**. In C++, if a variable is modified or accessed multiple times within a single statement, and there is no sequence point between the accesses, the behavior is undefined.

* **Unsequenced access** occurs when:

  * An object is modified more than once within an expression (e.g., `x = x++`).
  * An object is both modified and accessed without an intervening sequence point (e.g., `x = x + 1;` where `x` is modified and then accessed).

##### Example (Undefined Behavior):

```cpp
#include <iostream>

int main() {
    int x = 5;
    x = x++ + 1;  // Undefined behavior, due to unsequenced modification and access of 'x'
    std::cout << "x: " << x << std::endl;
    return 0;
}
```

In this example, `x++` and `x =` are **unsequenced** operations on `x`, meaning the compiler may evaluate them in any order. This leads to **undefined behavior** because the sequence of operations on `x` is not guaranteed by the C++ standard.

**Common Pitfall**: Using `x = x++` or similar expressions, where the same object is modified twice without a sequence point, is a classic cause of undefined behavior.

##### Proper Sequencing Example:

```cpp
#include <iostream>

int main() {
    int x = 5;
    int temp = x++;  // x is first incremented, then assigned to temp
    x = temp + 1;    // Now x is safely reassigned
    std::cout << "x: " << x << std::endl;  // x: 6
    return 0;
}
```

Here, `x++` is properly sequenced, and its value is safely used in the next statement.

**Note**: Always be cautious when modifying variables multiple times in the same statement. To avoid undefined behavior, make sure there are sequence points or use clear, well-structured operations.

---
### 1.4.3 Endianness & Byte Order
Endianness refers to the order in which bytes are stored in memory when representing data types (especially multi-byte types such as integers or floats). It is crucial to understand byte order when working with low-level programming, networking, or cross-platform applications.


#### 1.4.3.1 Little-endian vs Big-endian
The terms **little-endian** and **big-endian** describe two common ways to arrange the bytes of a multi-byte data type in memory.

- **Little-endian**: The least significant byte (LSB) is stored first (at the lowest memory address). This is the format used by **Intel x86** and **x86-64** architectures.

- **Big-endian**: The most significant byte (MSB) is stored first (at the lowest memory address). This is the format used by architectures like **Motorola 68k** and **SPARC**.

##### Example of Little-endian (4-byte integer):
Consider a 32-bit integer `0x12345678`. In little-endian, it would be stored in memory as:
```

Memory Address: 0x100  0x101  0x102  0x103
Value (Little-endian): 78  56  34  12

```

##### Example of Big-endian (4-byte integer):
In big-endian, the same integer `0x12345678` would be stored as:
```

Memory Address: 0x100  0x101  0x102  0x103
Value (Big-endian): 12  34  56  78

````

The difference in byte ordering can lead to issues when transferring data between systems with different endianness, especially in network protocols or cross-platform applications.

---
#### 1.4.3.2 Network Byte Order
In network communication, data is transmitted using **network byte order**, which is always **big-endian**. This standard ensures that all machines, regardless of their native endianness, can correctly interpret the data.

When sending data over a network, the **host byte order** (which can be either little-endian or big-endian) must be converted to **network byte order** (big-endian), and vice versa, when receiving data.

- **Host byte order**: The byte order used by the host machine (little-endian or big-endian).
- **Network byte order**: Always big-endian.

C++ provides functions for converting between host and network byte order:
- `htons()` (Host-to-Network Short): Converts a 16-bit value.
- `htonl()` (Host-to-Network Long): Converts a 32-bit value.
- `ntohs()` (Network-to-Host Short): Converts from network to host byte order.
- `ntohl()` (Network-to-Host Long): Converts from network to host byte order.

- Examples
```cpp
#include <iostream>
#include <arpa/inet.h>  // For htonl and ntohl

int main() {
    uint32_t host_order = 0x12345678;
    uint32_t network_order = htonl(host_order);  // Convert to network byte order

    std::cout << "Host order: 0x" << std::hex << host_order << std::endl;
    std::cout << "Network order: 0x" << std::hex << network_order << std::endl;

    uint32_t converted_back = ntohl(network_order);  // Convert back to host byte order
    std::cout << "Converted back to host order: 0x" << std::hex << converted_back << std::endl;

    return 0;
}
````

Output:

```
Host order: 0x12345678
Network order: 0x78563412
Converted back to host order: 0x12345678
```

In the above example, `htonl()` converts the value from host byte order to network byte order, and `ntohl()` converts it back to host byte order.

**Note**: When working with networking APIs or writing cross-platform code, always be sure to handle byte order conversion to ensure compatibility.

---
#### 1.4.3.3 std::endian (C++20)
In C++20, the `<bit>` header introduced the `std::endian` enum, which provides a way to check the endianness of the system at compile-time or runtime. It has three values:

* `std::endian::little`: Indicates a little-endian system.
* `std::endian::big`: Indicates a big-endian system.
* `std::endian::native`: Represents the native byte order of the system.

The `std::endian` enum is used to determine the byte order of the system in a portable way, making it easier to write code that handles endianness correctly.

- Example
```cpp
#include <iostream>
#include <bit>

int main() {
    if (std::endian::native == std::endian::little) {
        std::cout << "This system is little-endian." << std::endl;
    } else {
        std::cout << "This system is big-endian." << std::endl;
    }
    
    return 0;
}
```

Output (on little-endian systems):

```
This system is little-endian.
```

In this example, the program checks the system's endianness using `std::endian::native` and prints the appropriate message.

**Note**: The `std::endian` enum is a compile-time feature that can be used to write more portable code, particularly when working with system-level programming, file formats, or network protocols.

---
#### 1.4.3.4 Manual Byte Swapping
In cases where you need to convert data between different byte orders (e.g., when working with a custom file format or communication protocol), you may need to manually swap the bytes. This is commonly done for multi-byte data types like integers or floating-point numbers.

To swap bytes, you can write a function that manually exchanges the positions of the bytes.

- Example (Manual Byte Swapping for 32-bit Integer):
```cpp
#include <iostream>
#include <cstdint>

uint32_t swap_bytes(uint32_t value) {
    return ((value >> 24) & 0x000000FF) |
           ((value >> 8)  & 0x0000FF00) |
           ((value << 8)  & 0x00FF0000) |
           ((value << 24) & 0xFF000000);
}

int main() {
    uint32_t original = 0x12345678;
    uint32_t swapped = swap_bytes(original);
    
    std::cout << "Original: 0x" << std::hex << original << std::endl;
    std::cout << "Swapped: 0x" << std::hex << swapped << std::endl;

    return 0;
}
```

Output:

```
Original: 0x12345678
Swapped: 0x78563412
```

In this example, `swap_bytes()` swaps the byte order of a 32-bit integer. The function works by shifting the bytes into their new positions.

For multi-byte values, you can use similar functions to swap their byte order. **Note**: This is especially important when working with raw binary data or network protocols, where the byte order is not guaranteed.

**Note**: The C++ standard library also provides `std::byte` (in `<cstddef>`) to represent a byte, which can make byte manipulation more type-safe when working with binary data.

---
# 2. Memory, Pointers, References & Casting

## 2.1 Pointers and References

### 2.1.1 Memory & Pointers

Memory and pointers are fundamental concepts in C++ programming, allowing direct access and manipulation of memory. Understanding how to work with memory addresses, pointer operations, and dynamic memory management is key to becoming proficient in C++.

#### 2.1.1.1 Memory Addressing (&)
The **address-of operator** `&` is used to get the memory address of a variable or object. It is commonly used to obtain a pointer to the variable.

- Examples
```cpp
#include <iostream>

int main() {
    int x = 10;
    int* p = &x;  // p holds the address of x

    std::cout << "Address of x: " << &x << std::endl;  // Prints memory address of x
    std::cout << "p points to address: " << p << std::endl;  // Same address as above
    std::cout << "Value of x through pointer: " << *p << std::endl;  // Dereferencing p to get value

    return 0;
}
````

Output:

```
Address of x: 0x7ffeefbff56c
p points to address: 0x7ffeefbff56c
Value of x through pointer: 10
```

In this example, `&x` gives the memory address of variable `x`, and the pointer `p` holds that address. Using `*p`, you can access the value stored at that address.

---
#### 2.1.1.2 Pointers (*)
A **pointer** is a variable that stores the memory address of another variable. The asterisk `*` is used to declare a pointer and dereference it to access the value it points to.

- Examples
```cpp
#include <iostream>

int main() {
    int x = 5;
    int* p = &x;  // Pointer p points to x

    std::cout << "Pointer p stores address: " << p << std::endl;  // Address of x
    std::cout << "Value pointed to by p: " << *p << std::endl;  // Value of x through pointer p

    return 0;
}
```

Output:

```
Pointer p stores address: 0x7ffee3b9c5a0
Value pointed to by p: 5
```

In this example, the pointer `p` is assigned the address of `x`. The `*p` operator dereferences the pointer to access the value stored at that address.

---
#### 2.1.1.3 Dereference (*p)
Dereferencing a pointer means accessing the value stored at the memory address the pointer is pointing to. The asterisk `*` is used to dereference the pointer.

- Examples
```cpp
#include <iostream>

int main() {
    int x = 42;
    int* p = &x;  // p points to x

    std::cout << "Value of x: " << x << std::endl;  // Direct access
    std::cout << "Value of x through pointer: " << *p << std::endl;  // Dereference p

    return 0;
}
```

Output:

```
Value of x: 42
Value of x through pointer: 42
```

Here, the pointer `p` is dereferenced using `*p` to access the value stored at the address `p` points to (which is the value of `x`).

**Important**: Dereferencing a pointer that points to an invalid or uninitialized address leads to undefined behavior (e.g., accessing a null pointer or an uninitialized pointer).

---
#### 2.1.1.4 nullptr
`nullptr` is a special keyword introduced in C++11 that represents a null pointer. It is type-safe and ensures that pointers do not point to arbitrary memory addresses.

* Before C++11, `NULL` was used to represent a null pointer, but `nullptr` is a better, type-safe replacement.
* `nullptr` is automatically convertible to any pointer type but is not implicitly convertible to integral types.

- Examples
```cpp
#include <iostream>

int main() {
    int* p = nullptr;  // p is a null pointer

    if (p == nullptr) {
        std::cout << "Pointer is null!" << std::endl;
    }

    return 0;
}
```

Output:

```
Pointer is null!
```

In this example, `p` is initialized to `nullptr`, and the program checks if it points to `nullptr` before using it. This prevents dereferencing invalid pointers.

**Note**: Using `nullptr` is preferred over `NULL` because it avoids ambiguity when working with pointers and ensures type safety.

---
#### 2.1.1.5 new
The `new` keyword is used to allocate memory dynamically on the heap. It creates an object or array and returns a pointer to the allocated memory.

- Example
```cpp
#include <iostream>

int main() {
    int* p = new int(10);  // Allocates memory and initializes it with 10

    std::cout << "Value at allocated memory: " << *p << std::endl;  // Dereference to get value

    delete p;  // Free the allocated memory
    return 0;
}
```

Output:

```
Value at allocated memory: 10
```

Here, `new int(10)` allocates memory for a single integer and initializes it to `10`. The pointer `p` holds the address of the allocated memory. After using the allocated memory, it's important to deallocate it using `delete`.

**Note**: Always use `delete` to free dynamically allocated memory to avoid memory leaks.

---
#### 2.1.1.6 delete
The `delete` keyword is used to deallocate memory that was previously allocated using `new`. It ensures that dynamically allocated memory is properly freed and avoids memory leaks.

- Examples
```cpp
#include <iostream>

int main() {
    int* p = new int(42);  // Dynamically allocate memory
    std::cout << "Value: " << *p << std::endl;  // Access value

    delete p;  // Free dynamically allocated memory

    return 0;
}
```

Output:

```
Value: 42
```

In this example, `delete` is used to deallocate the memory that `p` points to after it is no longer needed.

**Note**: Using `delete` on a pointer that was not allocated with `new` or has already been deleted results in undefined behavior.

---
#### 2.1.1.7 delete[]
When allocating an array dynamically with `new[]`, you must deallocate it with `delete[]` to correctly free the memory.

- Examples
```cpp
#include <iostream>

int main() {
    int* arr = new int[3]{1, 2, 3};  // Dynamically allocate an array

    std::cout << "Array elements: ";
    for (int i = 0; i < 3; i++) {
        std::cout << arr[i] << " ";  // Access array elements
    }
    std::cout << std::endl;

    delete[] arr;  // Deallocate the array
    return 0;
}
```

Output:

```
Array elements: 1 2 3
```

In this example, `new[]` is used to allocate an array of integers, and `delete[]` is used to deallocate it. It's crucial to use `delete[]` when dealing with arrays to avoid memory leaks or undefined behavior.

**Note**: Always match `new[]` with `delete[]` and `new` with `delete` to ensure proper memory management.

---
### 2.1.2 Raw Pointers (T*) and Pointer Arithmetic

### 2.1.3 References
References in C++ are a way to create an alias for an existing variable, allowing you to refer to it indirectly without copying its value. References are used extensively in C++ to optimize performance and provide flexibility in function calls and object manipulation.

#### 2.1.3.1 int& ref
A reference is declared using the `&` symbol, and it must always be initialized when it is created. A reference to a variable allows you to modify the variable directly through the reference.

- **Syntax**: `int& ref = var;` creates a reference `ref` to the variable `var`.
- A reference does not create a new object; it just creates an alias for an existing object.

- Examples
```cpp
#include <iostream>

int main() {
    int x = 10;
    int& ref = x;  // ref is a reference to x

    std::cout << "x: " << x << std::endl;  // x: 10
    ref = 20;  // Changing the value through the reference

    std::cout << "x after modification through ref: " << x << std::endl;  // x: 20
    std::cout << "ref: " << ref << std::endl;  // ref: 20

    return 0;
}
````

Output:

```
x: 10
x after modification through ref: 20
ref: 20
```

In this example, `ref` is a reference to `x`. Modifying `ref` directly changes the value of `x` because they are essentially the same variable.

**Note**: References must always be initialized and cannot be reassigned to refer to a different object after their initial assignment.

---
#### 2.1.3.2 Call Site Reference
In C++, references are commonly used in function calls to pass variables by reference, which allows functions to modify the original arguments passed to them. This avoids copying data and can improve performance, especially with large objects or arrays.

* **Pass-by-reference**: A function that takes a reference to a variable allows it to modify the original variable passed to it.
* **Syntax**: `void func(int& ref)` takes `ref` as a reference, meaning changes to `ref` inside `func` will affect the original variable.

- Examples
```cpp
#include <iostream>

void increment(int& ref) {
    ref++;  // Increment the original variable
}

int main() {
    int num = 5;
    std::cout << "Before increment: " << num << std::endl;  // 5

    increment(num);  // num is passed by reference

    std::cout << "After increment: " << num << std::endl;  // 6
    return 0;
}
```

Output:

```
Before increment: 5
After increment: 6
```

In this example, the function `increment()` takes an `int&` parameter, meaning the argument `num` is passed by reference. The modification of `ref` inside the function also modifies `num`, since they refer to the same object.

**Note**: Passing by reference is especially useful for large objects like `std::vector` or custom classes, where passing by value would be inefficient.

---
#### 2.1.3.3 Rvalue References (T&&)
Introduced in C++11, **rvalue references** are used to bind to temporary objects (rvalues). They allow you to implement **move semantics**, which enables efficient transfer of resources from temporary objects without unnecessary copies.

* **Syntax**: `T&&` declares an rvalue reference, where `T` is the type.
* Rvalue references enable **move constructors** and **move assignment operators** to avoid copying large objects unnecessarily.

- Example (Rvalue Reference and Move Semantics):
```cpp
#include <iostream>
#include <vector>

class MyClass {
public:
    std::vector<int> data;
    
    // Move constructor
    MyClass(MyClass&& other) noexcept {
        data = std::move(other.data);  // Move data instead of copying
        std::cout << "Move constructor called" << std::endl;
    }

    // Copy constructor
    MyClass(const MyClass& other) {
        data = other.data;  // Copy data
        std::cout << "Copy constructor called" << std::endl;
    }

    void addData(int value) {
        data.push_back(value);
    }
};

int main() {
    MyClass obj1;
    obj1.addData(10);
    
    MyClass obj2 = std::move(obj1);  // Move obj1 into obj2 using move constructor

    std::cout << "obj2 data size: " << obj2.data.size() << std::endl;  // obj2 owns the data
    return 0;
}
```

Output:

```
Move constructor called
obj2 data size: 1
```

In this example, `obj1` is moved into `obj2` using the move constructor. The move operation transfers the ownership of the resources (in this case, the `std::vector<int>`) from `obj1` to `obj2` without copying the data.

* **`std::move`** is used to cast `obj1` to an rvalue reference, indicating that `obj1` can be moved from.

**Move Semantics**:

* **Move constructor**: Transfers resources from a temporary object to a new object without copying.
* **Move assignment operator**: Transfers resources from a temporary object to an already existing object.

- Example (Move Assignment):
```cpp
#include <iostream>
#include <vector>

class MyClass {
public:
    std::vector<int> data;

    // Move assignment operator
    MyClass& operator=(MyClass&& other) noexcept {
        if (this != &other) {  // Avoid self-assignment
            data = std::move(other.data);  // Move data
            std::cout << "Move assignment called" << std::endl;
        }
        return *this;
    }

    void addData(int value) {
        data.push_back(value);
    }
};

int main() {
    MyClass obj1;
    obj1.addData(10);

    MyClass obj2;
    obj2 = std::move(obj1);  // Move assignment

    std::cout << "obj2 data size: " << obj2.data.size() << std::endl;  // obj2 owns the data
    return 0;
}
```

Output:

```
Move assignment called
obj2 data size: 1
```

In this case, `std::move` is used to invoke the move assignment operator, transferring the data from `obj1` to `obj2`.

**Rvalue References and Move Semantics**:

* They provide a way to efficiently transfer resources from temporary objects without copying.
* They are used with `std::move()` to indicate that the object can be moved instead of copied.

**Note**: You cannot bind an rvalue reference to an lvalue, and rvalue references can be very powerful for optimizing performance, especially when dealing with containers like `std::vector` or custom classes with expensive copy operations.

--- 
### 2.1.4 Memory Layout and Alignment
Memory alignment is an important concept when working with low-level programming or optimizing data storage. Misalignment can result in performance penalties or undefined behavior on certain architectures. C++ provides tools to control and inspect memory alignment.

#### 2.1.4.1 alignas
The `alignas` keyword is used to specify the alignment requirement of a variable or structure. It ensures that the object is allocated at an address that is a multiple of the specified alignment.

- **Syntax**: `alignas(type) variable;` or `alignas(n) type variable;`
- You can use `alignas` to ensure that variables, types, or structures are aligned to specific memory boundaries for performance or hardware requirements.

- Examples
```cpp
#include <iostream>
#include <align>

struct alignas(16) MyStruct {
    int a;
    double b;
};

int main() {
    MyStruct s;
    std::cout << "Alignment of MyStruct: " << alignof(MyStruct) << std::endl;
    std::cout << "Address of s: " << &s << std::endl;
    
    return 0;
}
````

Output:

```
Alignment of MyStruct: 16
Address of s: 0x7ffd3b76f5d0
```

In this example, `alignas(16)` ensures that the object `MyStruct` is aligned to a 16-byte boundary. The `alignof(MyStruct)` query confirms the alignment, and the address of `s` is printed. The alignment helps optimize memory access on certain architectures where accessing data aligned to specific boundaries is faster.

**Note**: The `alignas` keyword is especially useful in performance-critical applications like graphics programming, low-level systems programming, and certain embedded systems where alignment plays a significant role in execution speed.

---
#### 2.1.4.2 alignof
The `alignof` operator is used to determine the alignment (in bytes) of a given type or object. It returns the alignment requirement for the type, which is useful for determining how much padding is required for proper alignment in structures or arrays.

* **Syntax**: `alignof(type)` or `alignof(variable)`
* It helps you understand the memory layout of data structures and manage memory alignment efficiently.

- Examples
```cpp
#include <iostream>

struct MyStruct {
    char a;     // 1 byte
    int b;      // 4 bytes (aligned to 4-byte boundary)
};

int main() {
    std::cout << "Alignment of char: " << alignof(char) << std::endl;  // 1
    std::cout << "Alignment of int: " << alignof(int) << std::endl;    // 4
    std::cout << "Alignment of MyStruct: " << alignof(MyStruct) << std::endl;  // 4

    return 0;
}
```

Output:

```
Alignment of char: 1
Alignment of int: 4
Alignment of MyStruct: 4
```

In this example:

* `alignof(char)` returns `1` because `char` has the least alignment requirement.
* `alignof(int)` returns `4` because `int` typically requires 4-byte alignment.
* `alignof(MyStruct)` returns `4`, as the largest alignment requirement in the structure (`int b`) dictates the overall alignment.

**Important Notes**:

* The alignment of a structure or class is typically determined by the member with the largest alignment requirement.
* Misaligned access to data can lead to slower performance, or on some architectures, it can cause a crash. Using `alignof` and `alignas` helps ensure proper alignment for better performance and correctness.

- Example of Alignment in Structures

When a structure contains members of different data types, C++ automatically adds padding to ensure the proper alignment of each member, especially when dealing with large data types like `double` or `long long`.

- Example:
```cpp
#include <iostream>

struct MisalignedStruct {
    char a;       // 1 byte
    double b;     // 8 bytes (aligned to 8-byte boundary)
};

struct AlignedStruct {
    char a;       // 1 byte
    alignas(8) double b;  // 8 bytes, explicitly aligned to 8-byte boundary
};

int main() {
    std::cout << "Size of MisalignedStruct: " << sizeof(MisalignedStruct) << std::endl;
    std::cout << "Size of AlignedStruct: " << sizeof(AlignedStruct) << std::endl;

    return 0;
}
```

Output:

```
Size of MisalignedStruct: 16
Size of AlignedStruct: 16
```

In the case of `MisalignedStruct`, the compiler adds padding between `a` and `b` to align `b` to an 8-byte boundary. By using `alignas(8)` on `b` in `AlignedStruct`, we ensure that `b` is aligned to 8 bytes without requiring additional padding, thus maintaining efficient memory access.

---

### Key Takeaways:

* **`alignas`** allows you to specify the alignment requirement of a variable or structure, ensuring that memory is allocated at the correct boundary.
* **`alignof`** provides the alignment requirement for any type, useful for optimizing data layout and avoiding misalignment.
* Proper alignment is critical in performance-sensitive systems, and **using `alignas` and `alignof`** helps ensure that data is stored in memory efficiently and can be accessed quickly.

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

Describes how a program’s memory is organized at runtime, focusing on where data lives, how it’s accessed, and ABI-level rules that govern correctness and performance. Covers stack behavior, calling conventions, and low-level details critical for debugging, optimization, and systems programming.

---
### 2.3.1 Stack Memory Internals

Region of memory used for function calls, local variables, and control flow. Operates in a strict LIFO (Last In, First Out) manner. Managed automatically by the compiler and CPU instructions.

Key properties:

* Grows downward on most architectures (x86, x86-64)
* Very fast allocation/deallocation
* Limited size compared to heap
* Thread-local (each thread has its own stack)
* Lifetime tied to scope
---

#### 2.3.1.1 Stack Frames

A stack frame (activation record) is the block of stack memory allocated for a single function call.

Typically contains:

* Function parameters (if not passed in registers)
* Return address
* Saved base/frame pointer
* Local variables
* Temporaries and spilled registers

Created on function entry and destroyed on function exit.

```c
void foo(int a) {
    int x = 10;
    int y = a + x;
}
```

Conceptual layout (high → low address):

* Function arguments
* Return address
* Saved base pointer
* Local variables (x, y)

Important points:

* Size determined at compile time (unless VLAs are used)
* Nested calls create nested frames
* Recursive calls create multiple independent frames
---

#### 2.3.1.2 Saved Return Address

The return address is the instruction pointer where execution resumes after the function finishes.

Mechanism:

* On x86/x86-64, `call` instruction pushes the return address onto the stack
* `ret` pops it back into the instruction pointer (RIP/EIP)

```asm
call foo   ; pushes return address
...
ret        ; jumps back to caller
```

Characteristics:

* Stored automatically by CPU
* Critical for control flow integrity
* Corruption leads to crashes or exploits (stack smashing, ROP)
* Protected by mechanisms like stack canaries and shadow stacks

---
#### 2.3.1.3 Base Pointer (RBP/EBP)

Base pointer (frame pointer) provides a stable reference point within a stack frame.

Registers:

* EBP (32-bit x86)
* RBP (64-bit x86-64)

Typical function prologue/epilogue:

```asm
push rbp
mov rbp, rsp
sub rsp, 32
...
leave
ret
```

Usage:

* Access locals and parameters at fixed offsets
* Simplifies debugging and stack unwinding
* Makes stack frames predictable

Offsets example:

* `[rbp - 4]` → local variable
* `[rbp + 8]` → return address

Optimizations:

* Compiler may omit frame pointer (`-fomit-frame-pointer`)
* Increases available registers
* Makes debugging harder

---
#### 2.3.1.4 Stack Alignment

Stack alignment ensures data is placed at addresses optimal for the CPU.

Rules (common ABIs):

* x86-64 System V ABI: stack must be 16-byte aligned before `call`
* Required for SIMD instructions (SSE, AVX)

Why it matters:

* Misalignment causes performance penalties
* Some instructions fault on misaligned access

Example:

```c
void foo() {
    double d;   // requires 8-byte alignment
}
```

Compiler responsibilities:

* Insert padding in stack frame
* Adjust stack pointer accordingly

Notes:

* Alignment is relative to the stack pointer at call boundaries
* Caller is usually responsible for alignment

---
#### 2.3.1.5 Red Zone (SysV ABI)

A special optimization feature in the x86-64 System V ABI.

Definition:

* 128-byte area below the current stack pointer (RSP)
* Guaranteed not to be clobbered by interrupts or signal handlers

Usage:

* Leaf functions can use it without adjusting RSP
* Avoids stack pointer modification

```c
int foo() {
    int x = 5;  // may live in red zone
    return x;
}
```

Properties:

* Only valid in SysV ABI (Linux, macOS)
* Not available on Windows x64 ABI
* Disabled in kernel code and with certain compiler flags

Compiler control:

* Enabled by default in user-space
* Disabled with `-mno-red-zone`

Purpose:

* Reduce instruction count
* Improve performance for small functions

---
### 2.3.2 Heap Memory Internals

Dynamic memory region used for allocations whose size and lifetime are determined at runtime. Managed explicitly via allocators (`malloc/free`, `new/delete`) or runtime systems. Shared across threads and persists beyond function scope until explicitly released.

Key properties:

* Grows upward on most systems
* Much larger than stack
* Slower than stack due to bookkeeping
* Prone to fragmentation
* Managed by a heap allocator (glibc ptmalloc, jemalloc, tcmalloc, etc.)

---
#### 2.3.2.1 Heap Metadata

Extra information stored by the allocator to manage heap blocks. Usually placed adjacent to user data.

Common metadata fields:

* Block size
* Allocation status (in-use / free)
* Previous block status
* Pointers for free list linking

Typical layout (simplified):

* [ metadata ][ user data ][ padding ]

```c
int *p = (int*)malloc(sizeof(int));
*p = 42;
```

Internals (conceptual):

* Allocator reserves more than requested
* Metadata stored before `p`
* Returned pointer skips metadata

Characteristics:

* Not visible to user code
* Size and format allocator-dependent
* Corruption leads to undefined behavior
* Used for coalescing adjacent free blocks

Security relevance:

* Heap overflow can overwrite metadata
* Exploited in classic heap attacks
* Hardened by checks, cookies, safe-linking

---
#### 2.3.2.2 Free Lists and Bins

Mechanisms used to track free memory blocks for reuse.

Free lists:

* Linked lists of free blocks
* Blocks grouped by size or class
* Enable fast allocation without OS calls

Bins:

* Containers holding free blocks of certain sizes
* Exact-size bins or size ranges
* Small bins vs large bins

Conceptual example:

* Bin 16B → blocks of size 16
* Bin 32B → blocks of size 32
* Unsorted bin → recently freed blocks

```c
void *a = malloc(32);
free(a);
void *b = malloc(32);  // reused from free list
```

Strategies:

* First-fit
* Best-fit
* Segregated storage

Trade-offs:

* Faster allocation
* Increased metadata
* Fragmentation risk

---
#### 2.3.2.3 Fragmentation

Inefficient use of heap memory due to allocation patterns.

Types:

* External fragmentation: free memory exists but not contiguous
* Internal fragmentation: allocated block larger than requested

Example:

```c
malloc(24);  // allocator gives 32 bytes
```

Causes:

* Variable-sized allocations
* Frequent alloc/free cycles
* Poor bin size granularity

Effects:

* Increased memory usage
* Allocation failures despite free memory
* Performance degradation

Mitigation:

* Size class rounding
* Coalescing adjacent free blocks
* Pool allocators
* Custom allocators for fixed-size objects

---
#### 2.3.2.4 Heap Grooming Concepts

Technique of intentionally shaping heap layout through controlled allocations and frees.

Purpose:

* Predict placement of heap objects
* Control adjacency of blocks
* Exploit or prevent exploitation

Typical steps:

* Allocate specific sizes
* Free selected blocks
* Reallocate to occupy freed slots

```c
void *a = malloc(64);
void *b = malloc(64);
free(a);
void *c = malloc(64);  // likely reuses a's slot
```

Use cases:

* Exploit development (heap exploitation)
* Fuzzing
* Debugging allocator behavior
* Testing memory safety

Key ideas:

* Deterministic allocator behavior
* Bin manipulation
* Reuse patterns

Notes:

* Highly allocator-specific
* Modern allocators add randomization and hardening
* Less predictable in multi-threaded programs

---
### 2.3.3 Object Representation

Defines how objects are laid out in memory at the byte level. Covers rules that govern size, alignment, ordering, and hidden bytes inserted by the compiler. Critical for ABI compatibility, performance, serialization, and security.

---
#### 2.3.3.1 Padding and Alignment

Alignment is the requirement that objects be placed at memory addresses that are multiples of a specific value. Padding is unused space inserted to satisfy alignment constraints.

Reasons:

* CPU alignment requirements
* Faster memory access
* SIMD and atomic correctness

Basic rules:

* Each object has an alignment requirement
* Struct alignment equals the max alignment of its members
* Compiler inserts padding between members and at the end

```c
struct A {
    char c;
    int i;
};
```

Typical layout (32/64-bit):

* `c` at offset 0
* 3 bytes padding
* `i` at offset 4
* `sizeof(struct A) == 8`

Reordering effect:

```c
struct B {
    int i;
    char c;
};
```

Layout:

* `i` at offset 0
* `c` at offset 4
* 3 bytes tail padding

Key points:

* Padding is not initialized
* Layout is compiler- and ABI-dependent
* `#pragma pack` / `__attribute__((packed))` reduce padding but may hurt performance

---
#### 2.3.3.2 Struct Layout Guarantees

Language-level guarantees that define what is and is not predictable about object layout.

C guarantees:

* Members appear in declared order
* No reordering of members
* Address of first member equals address of struct
* Padding may exist between members

C++ adds:

* Standard-layout types have C-compatible layout
* Empty base optimization allowed
* Multiple inheritance affects layout

```c++
struct S {
    int a;
    double b;
};
```

Guaranteed:

* `a` precedes `b`
* `offsetof(S, b)` is valid

Not guaranteed:

* Exact offsets
* Total size
* Padding amount

Special cases:

* Bit-fields: implementation-defined layout
* `alignas` can increase alignment
* `std::byte` has no padding assumptions

ABI considerations:

* Structs passed by value follow ABI rules
* Padding may be included in copies

---
#### 2.3.3.3 Information Disclosure via Padding

Padding bytes may contain uninitialized or stale data, leading to information leaks.

How it happens:

* Struct copied or sent without clearing padding
* Padding retains old stack or heap contents

```c
struct Packet {
    char type;
    int value;
};

struct Packet p;
p.type = 1;
p.value = 100;
// padding between type and value is uninitialized
```

Leak vectors:

* Network transmission
* File I/O
* IPC
* Logging raw memory

Security impact:

* Leaks stack addresses
* Reveals sensitive data
* Breaks ASLR assumptions

Mitigation:

* Zero-initialize structs

```c
struct Packet p = {0};
```

* Use `memset`
* Avoid copying raw structs across trust boundaries
* Serialize fields explicitly
* Use `-ftrivial-auto-var-init=zero` (where supported)

Notes:

* Packed structs reduce padding but may introduce misaligned accesses
* Sanitizers can detect uninitialized reads

---
### 2.3.2 Heap Memory Internals

Dynamic memory region used for allocations whose size and lifetime are determined at runtime. Managed explicitly via allocators (`malloc/free`, `new/delete`) or runtime systems. Shared across threads and persists beyond function scope until explicitly released.

Key properties:

* Grows upward on most systems
* Much larger than stack
* Slower than stack due to bookkeeping
* Prone to fragmentation
* Managed by a heap allocator (glibc ptmalloc, jemalloc, tcmalloc, etc.)

---
#### 2.3.2.1 Heap Metadata

Extra information stored by the allocator to manage heap blocks. Usually placed adjacent to user data.

Common metadata fields:

* Block size
* Allocation status (in-use / free)
* Previous block status
* Pointers for free list linking

Typical layout (simplified):

* [ metadata ][ user data ][ padding ]

```c
int *p = (int*)malloc(sizeof(int));
*p = 42;
```

Internals (conceptual):

* Allocator reserves more than requested
* Metadata stored before `p`
* Returned pointer skips metadata

Characteristics:

* Not visible to user code
* Size and format allocator-dependent
* Corruption leads to undefined behavior
* Used for coalescing adjacent free blocks

Security relevance:

* Heap overflow can overwrite metadata
* Exploited in classic heap attacks
* Hardened by checks, cookies, safe-linking

---
#### 2.3.2.2 Free Lists and Bins

Mechanisms used to track free memory blocks for reuse.

Free lists:

* Linked lists of free blocks
* Blocks grouped by size or class
* Enable fast allocation without OS calls

Bins:

* Containers holding free blocks of certain sizes
* Exact-size bins or size ranges
* Small bins vs large bins

Conceptual example:

* Bin 16B → blocks of size 16
* Bin 32B → blocks of size 32
* Unsorted bin → recently freed blocks

```c
void *a = malloc(32);
free(a);
void *b = malloc(32);  // reused from free list
```

Strategies:

* First-fit
* Best-fit
* Segregated storage

Trade-offs:

* Faster allocation
* Increased metadata
* Fragmentation risk

---
#### 2.3.2.3 Fragmentation

Inefficient use of heap memory due to allocation patterns.

Types:

* External fragmentation: free memory exists but not contiguous
* Internal fragmentation: allocated block larger than requested

Example:

```c
malloc(24);  // allocator gives 32 bytes
```

Causes:

* Variable-sized allocations
* Frequent alloc/free cycles
* Poor bin size granularity

Effects:

* Increased memory usage
* Allocation failures despite free memory
* Performance degradation

Mitigation:

* Size class rounding
* Coalescing adjacent free blocks
* Pool allocators
* Custom allocators for fixed-size objects

---
#### 2.3.2.4 Heap Grooming Concepts

Technique of intentionally shaping heap layout through controlled allocations and frees.

Purpose:

* Predict placement of heap objects
* Control adjacency of blocks
* Exploit or prevent exploitation

Typical steps:

* Allocate specific sizes
* Free selected blocks
* Reallocate to occupy freed slots

```c
void *a = malloc(64);
void *b = malloc(64);
free(a);
void *c = malloc(64);  // likely reuses a's slot
```

Use cases:

* Exploit development (heap exploitation)
* Fuzzing
* Debugging allocator behavior
* Testing memory safety

Key ideas:

* Deterministic allocator behavior
* Bin manipulation
* Reuse patterns

Notes:

* Highly allocator-specific
* Modern allocators add randomization and hardening
* Less predictable in multi-threaded programs

---
### 2.3.4 Unions and Type Punning

Techniques that reinterpret the same memory as different types. Used for low-level programming, serialization, bit manipulation, and performance-critical code. Highly sensitive to language rules, compiler optimizations, and undefined behavior.

---
#### 2.3.4.1 Union-based Type Punning

Using a union to store a value of one type and read it as another.

```c
union U {
    int i;
    float f;
};

union U u;
u.i = 0x3f800000;
float x = u.f;
```

Concept:

* All union members share the same memory
* Writing one member and reading another reinterprets bits

C rules:

* Allowed to read from any member
* Result is implementation-defined
* Commonly used in systems code

C++ rules:

* Reading inactive member is undefined behavior
* Exception: reading common initial sequence or `unsigned char`

Use cases:

* Bit-level inspection
* Low-level hardware interfaces
* Legacy code

Risks:

* Compiler optimizations may break assumptions
* Non-portable behavior
* Endianness dependence

---
#### 2.3.4.2 Strict Aliasing Rules

Compiler rules that assume pointers of different types do not refer to the same memory.

Purpose:

* Enable aggressive optimizations
* Reduce memory reloads

Violation example:

```c
int x = 10;
float *f = (float*)&x;
float y = *f;  // strict aliasing violation
```

Allowed aliasing:

* Same type
* `char*`, `unsigned char*`, `std::byte*`
* Certain compatible types
* Through unions (C, limited)

Effects of violation:

* Undefined behavior
* Incorrect code under optimization
* Bugs appearing only in release builds

Compiler flags:

* `-fstrict-aliasing` (enabled by default)
* `-fno-strict-aliasing` disables optimizations

Key point:

* “Works on my machine” is not correctness

---
#### 2.3.4.3 memcpy vs reinterpret_cast

Reinterpreting memory safely by copying bytes.

Unsafe approach:

```cpp
float f = *reinterpret_cast<float*>(&i);
```

Problems:

* Violates strict aliasing
* Undefined behavior
* Optimizer may remove or reorder loads

Safe approach:

```cpp
int i = 0x3f800000;
float f;
std::memcpy(&f, &i, sizeof(f));
```

Why `memcpy` works:

* Operates on raw bytes
* Compiler understands intent
* Optimized to register moves

Properties:

* Well-defined behavior
* Portable
* Slightly more verbose

Guideline:

* Prefer `memcpy` for bit reinterpretation pre-C++20

---
#### 2.3.4.4 std::bit_cast as Safer Alternative

C++20 utility for explicit, safe bit reinterpretation.

```cpp
#include <bit>

int i = 0x3f800000;
float f = std::bit_cast<float>(i);
```

Requirements:

* Source and destination types same size
* Both trivially copyable

Advantages:

* Compile-time checked
* No undefined behavior
* Clear semantic intent
* Zero runtime cost

Invalid usage:

```cpp
std::bit_cast<double>(i);  // size mismatch
```

Use cases:

* Floating-point bit hacks
* Hashing
* Serialization
* SIMD-friendly code

Comparison:

* `reinterpret_cast`: unsafe
* `memcpy`: safe, verbose
* `std::bit_cast`: safe, expressive

---

# 3. Control Flow & Functions

## 3.1 Control Flow and Loops

Directs execution order based on conditions evaluated at runtime or compile time. Fundamental for decision-making, branching, and eliminating unnecessary code paths.

### 3.1.1 Control Flow

Execution paths chosen based on boolean expressions, values, or compile-time constants. Implemented using conditional statements and expressions.

---
#### 3.1.1.1 if / else if / else

Executes blocks conditionally based on boolean expressions evaluated top-down.

```c
if (x > 0) {
    y = 1;
} else if (x == 0) {
    y = 0;
} else {
    y = -1;
}
```

Rules:

* Conditions evaluated in order
* First true branch executes
* Remaining branches skipped
* `else` is optional

Notes:

* Condition must be scalar convertible to `bool`
* Short-circuiting applies in conditions
* Nesting allowed but reduces readability

Scope:

* Variables declared inside blocks are block-scoped

---
#### 3.1.1.2 switch (switch with strings via workarounds)

Selects execution path based on integral or enum values.

```c
switch (n) {
    case 1:
        foo();
        break;
    case 2:
        bar();
        break;
    default:
        baz();
}
```

Rules:

* Expression must be integral or enum
* `case` labels are compile-time constants
* `break` prevents fallthrough
* `default` is optional

Fallthrough:

```c
case 1:
case 2:
    foo();
    break;
```

String workaround (C):

```c
if (strcmp(s, "add") == 0) { ... }
else if (strcmp(s, "sub") == 0) { ... }
```

String workaround (C++):

```cpp
if (s == "add") { ... }
```

Hashed switch pattern:

```cpp
switch (hash(s)) {
    case HASH_ADD: ...
}
```

C++17 enhancement:

```cpp
switch (int x = f(); x) { ... }
```

---
#### 3.1.1.3 Ternary Operator

Expression-level conditional operator.

```c
int max = (a > b) ? a : b;
```

Properties:

* Returns a value
* Both branches must be type-compatible
* Right-associative

Nested usage:

```c
int r = (x > 0) ? 1 : (x < 0 ? -1 : 0);
```

Advantages:

* Concise
* Useful in initializations

Disadvantages:

* Hurts readability when nested
* Not a replacement for complex logic

---
#### 3.1.1.4 if constexpr

Compile-time conditional (C++17+). Branch discarded at compile time if condition is false.

```cpp
template<typename T>
void print(T x) {
    if constexpr (std::is_integral_v<T>) {
        std::cout << x;
    } else {
        std::cout << "not int";
    }
}
```

Rules:

* Condition must be compile-time constant
* Non-selected branch is not instantiated
* Avoids SFINAE complexity

Differences from `if`:

* `if`: runtime decision
* `if constexpr`: compile-time decision

Use cases:

* Templates
* Type-dependent logic
* Removing dead code paths

Limitations:

* Only available in C++
* Cannot depend on runtime values

---
### 3.1.2 Loops

Used to repeatedly execute a block of code while a condition holds. Control iteration, termination, and flow of repeated operations.

#### 3.1.2.1 for

Count-controlled loop with explicit initialization, condition, and iteration expression.

```c
for (int i = 0; i < 10; i++) {
    sum += i;
}
```

Execution order:

* Initialization (once)
* Condition check
* Body
* Iteration expression
* Repeat

Properties:

* All three expressions optional
* Variables can be scoped to loop
* Common for fixed iteration counts

Infinite loop:

```c
for (;;) {
    work();
}
```

Multiple expressions:

```c
for (i = 0, j = n; i < j; i++, j--) { }
```

---
#### 3.1.2.2 while

Condition-controlled loop evaluated before each iteration.

```c
while (x > 0) {
    x--;
}
```

Characteristics:

* Zero or more iterations
* Condition checked at entry
* Suitable when iteration count is unknown

Common pattern:

```c
while ((c = getchar()) != EOF) { }
```

Risk:

* Incorrect condition leads to infinite loop

---
#### 3.1.2.3 do-while

Post-tested loop where condition is evaluated after the body executes.

```c
do {
    read_input();
} while (valid());
```

Properties:

* Executes at least once
* Condition ends with semicolon
* Useful for menu-driven logic

Difference from `while`:

* Body guaranteed to run once

---
#### 3.1.2.4 Range-Based for

C++ loop for iterating over containers and ranges.

```cpp
for (int x : vec) {
    sum += x;
}
```

Reference form:

```cpp
for (int& x : vec) {
    x *= 2;
}
```

Const reference:

```cpp
for (const int& x : vec) { }
```

Requirements:

* `begin()` and `end()` defined
* Works with arrays, STL containers, initializer lists

Advantages:

* Safer and clearer
* No index errors
* Encourages idiomatic C++

Limitations:

* No direct index access
* Cannot easily skip elements without logic

--- 
### 3.1.3 Loop Control

Statements that alter normal loop execution by exiting early or skipping iterations. Improve control over flow without modifying loop conditions directly.

---
#### 3.1.3.1 break

Immediately terminates the nearest enclosing loop or `switch` statement.

```c
for (int i = 0; i < 10; i++) {
    if (i == 5)
        break;
}
```

Behavior:

* Control jumps to statement after loop
* Only exits one level
* Valid in `for`, `while`, `do-while`, `switch`

Nested loops:

```c
for (;;) {
    while (cond) {
        break;  // exits while only
    }
}
```

Notes:

* No labeled break in C/C++
* Overuse may reduce clarity
* Often used for early termination or search success

---
#### 3.1.3.2 continue

Skips remaining loop body and proceeds to next iteration.

```c
for (int i = 0; i < 10; i++) {
    if (i % 2 == 0)
        continue;
    process(i);
}
```

Behavior by loop type:

* `for`: jumps to iteration expression
* `while` / `do-while`: jumps to condition check

Example in `while`:

```c
while (x--) {
    if (x == 3)
        continue;
    work();
}
```

Key points:

* Does not exit the loop
* Useful for filtering iterations
* Can obscure logic if overused

---

## 3.2 Functions and Parameters

### 3.2.1 Functions

Reusable blocks of code that encapsulate logic, enable abstraction, and support modular design. Central to both C and C++ program structure.

---
#### 3.2.1.1 Definition

Specifies the function’s implementation and body.

```c
int add(int a, int b) {
    return a + b;
}
```

Components:

* Return type
* Function name
* Parameter list
* Function body

Rules:

* Exactly one definition per function
* Must match declared prototype
* Return statement required for non-`void`

C++ notes:

* Functions can be overloaded
* Default arguments allowed

---
#### 3.2.1.2 Prototype

Declares a function’s interface without its body.

```c
int add(int a, int b);
```

Purpose:

* Enables type checking
* Allows use before definition
* Required across translation units

Rules:

* Must match definition exactly
* Parameter names optional
* Types mandatory

```c
int add(int, int);
```

C++ extras:

* Function declarations can appear multiple times
* `extern` implied by default

---
#### 3.2.1.3 void

Used to indicate absence of a value or parameters.

Void return type:

```c
void log_error(void) {
    puts("error");
}
```

Void parameters:

```c
void foo(void);
```

Meaning:

* Returns nothing
* No usable return value

C vs C++:

* In C: `void` means no parameters
* In C++: empty parameter list already means no parameters

Restrictions:

* Cannot declare variable of type `void`
* Can use `void*` as generic pointer

---
#### 3.2.1.4 Free Functions

Functions not associated with a class or object.

```cpp
int square(int x) {
    return x * x;
}
```

Characteristics:

* Exist at namespace or global scope
* Common in C and C-style C++
* Can be namespaced in C++

```cpp
namespace math {
    int square(int x);
}
```

Usage:

* Utility functions
* Stateless operations
* Entry point (`main`)

Linkage:

* Global by default
* Can be restricted with `static` (C) or anonymous namespaces (C++)

---
### 3.2.2 Parameters

#### 3.2.2.1 Pass by Value

In Pass by Value, the function creates a completely independent copy of the actual parameter's data in a new memory location on the function's stack frame.

```cpp
void modify(int n) {
    n = n + 10; // Only the local copy 'n' is changed
}

int main() {
    int x = 5;
    modify(x);
    // x is still 5
    return 0;
}

```

Characteristics:

* **Memory Isolation:** The actual argument and the formal parameter reside at different memory addresses.
* **Overhead:** For large objects (complex structs or large classes), this involves a "Deep Copy," which triggers copy constructors and consumes significant CPU cycles and stack space.
* **Directionality:** Data flow is strictly one-way: from the caller to the function.
* **C-Standard:** This is the default and only behavior in C (pointers themselves are passed by value).

---
#### 3.2.2.2 Pass by Reference (&)

Pass by Reference provides the function with an alias to the original variable. No new memory is allocated for the data itself; the function operates directly on the caller's memory address.

```cpp
void modify(int &n) {
    n = n + 10; // Modifies the original variable in main
}

int main() {
    int x = 5;
    modify(x);
    // x is now 15
    return 0;
}

```

Characteristics:

* **No Copying:** Extremely efficient for large data structures as it avoids the constructor/destructor overhead of a copy.
* **Two-way Communication:** Allows a function to "return" multiple values by modifying the input arguments.
* **Const References:** A critical C++ pattern `void func(const Type &arg)` allows for the performance of a reference while guaranteeing the function cannot modify the data.
* **Syntax Requirement:** Unlike pointers, you don't need to dereference (using `*`) inside the function; you treat the parameter like a normal variable.
* **Non-Nullable:** A reference must be initialized and cannot be null, making it safer than passing by pointer/address.

---

#### 3.2.2.3 Default Parameters (Optional args)

Default parameters allow a function to be called with fewer arguments than specified. The compiler automatically substitutes the missing arguments with the predefined values provided in the function declaration.

```cpp
// Declaration (usually in header file)
void configure(int port, string host = "localhost", int timeout = 30);

// Definition
void configure(int port, string host, int timeout) {
    // Implementation logic
}

int main() {
    configure(8080);                    // Uses "localhost" and 30
    configure(8080, "127.0.0.1");       // Uses 30
    configure(8080, "192.168.1.1", 60); // Overrides all defaults
}

```

Characteristics:

* **The Right-to-Left Rule:** Once a parameter is given a default value, all subsequent parameters to its right must also have default values. `void func(int a = 1, int b)` is a compilation error.
* **Single Definition:** Default values should be specified in the function declaration (prototype) only. Redefining them in the function body definition is illegal.
* **Ambiguity Risk:** Can lead to "Ambiguous Call" errors during Function Overloading. For example, `void f(int)` and `void f(int, int = 0)` will conflict if called as `f(5)`.
* **Static Binding:** The values are bound at compile-time. If the default value is a global variable, the value used is whatever that variable holds at the moment of the function call.

---
### 3.2.3 Function Overloading
#### 3.2.3.1 Function Overloading (Different parameter types)

Function overloading allows multiple functions in the same scope to share the same name, provided their "signatures" (parameter lists) are distinct. This is a form of compile-time (static) polymorphism, where the compiler determines which function to call based on the arguments provided.

```cpp
void print(int i) {
    printf("Printing int: %d\n", i);
}

void print(double f) {
    printf("Printing float: %f\n", f);
}

void print(string s) {
    cout << "Printing string: " << s << endl;
}

void print(int i, string s) {
    cout << i << " : " << s << endl;
}

```

Characteristics:

* **Signature Elements:** The compiler distinguishes functions based on the number of parameters, the types of parameters, and the sequence/order of those types.
* **Return Type Exclusion:** The return type is **not** part of the function signature for overloading purposes. Declaring `int func(int)` and `void func(int)` in the same scope is a compilation error.
* **Const/Volatile Qualifiers:** Overloading can occur based on `const` or `volatile` qualifiers for reference or pointer parameters (e.g., `void process(int&)` vs `void process(const int&)`).
* **Name Mangling:** Since the linker requires unique names, the C++ compiler performs "Name Mangling" (or Name Decoration), encoding the parameter types into the function name internally (e.g., `_Z5printi` for `int` and `_Z5printNSt7__cxx11...` for `string`).
* **C Compatibility:** C does not support name mangling, which is why overloading is not possible in standard C.

---
#### 3.2.3.2 Function Hiding & Overload Resolution

**Function Hiding (Name Hiding):**
In C++, when a derived class defines a function with the same name as a function in the base class, it hides **all** versions of that function from the base class, regardless of whether the signatures match. This is because the compiler stops searching for the name once it finds a match in the innermost scope (the derived class).

```cpp
class Base {
public:
    void log(int x) {}
    void log(double x) {}
};

class Derived : public Base {
public:
    void log(string s) {} // Hides BOTH log(int) and log(double)
};

int main() {
    Derived d;
    // d.log(10);      // Error: Base::log(int) is hidden by Derived::log(string)
    d.Base::log(10);   // Success: Explicitly call the Base version
}

```

*Note: To prevent hiding and allow overloading across classes, use the `using Base::log;` declaration in the derived class.*

**Overload Resolution:**
This is the complex process the compiler uses to select the "best viable function" for a specific call.

The Resolution Steps:

1. **Candidate Functions:** The compiler identifies all functions with the called name that are visible in the current scope.
2. **Viable Functions:** It narrows the list to functions that can be called with the provided arguments (matching number of parameters or using default arguments, and having compatible types).
3. **Best Match Selection:** The compiler ranks the viable functions based on conversion quality:
* **Exact Match:** No conversion required, or only trivial conversions (like array-to-pointer).
* **Promotion:** Integral promotions (e.g., `bool`/`char` to `int`) or `float` to `double`.
* **Standard Conversion:** For example, `int` to `double`, or derived-class pointer to base-class pointer.
* **User-Defined Conversion:** Conversions via constructors or conversion operators.
* **Ellipsis:** Matching against `...` (variadic functions) is the lowest rank.


4. **Ambiguity:** If two functions have the same rank (e.g., `func(int, double)` and `func(double, int)` called with `func(1, 1)`), the compiler generates an error.

---

### 3.2.4 Function Pointers
#### 3.2.4.1 int (*funcPtr)(int, int)

A function pointer is a variable that stores the memory address of a function's executable code. Unlike data pointers that point to variables on the stack or heap, function pointers point to the "Text" (Code) segment of memory.

```cpp
int add(int a, int b) { return a + b; }
int subtract(int a, int b) { return a - b; }

// Syntax: return_type (*ptrName)(parameter_types)
int (*operation)(int, int); 

int main() {
    operation = add;        // Pointing to add function
    int sum = operation(5, 3); // Invoking: 8

    operation = &subtract;  // Explicit address-of (optional)
    int diff = (*operation)(10, 4); // Dereference syntax (optional)
}

```

Characteristics:

* **Declaration Syntax:** The parentheses around `*ptrName` are critical. `int *f(int, int)` is interpreted as a function returning an `int*`, whereas `int (*f)(int, int)` is a pointer to a function.
* **Type Strictness:** The pointer's signature must perfectly match the target function's return type and parameter types (including `const` qualifiers).
* **Decoupling:** They allow for "Late Binding," where the specific function to be executed is decided at runtime rather than compile-time.
* **Jump Tables:** Arrays of function pointers can replace long `switch-case` blocks, providing  access to operations (common in state machines or opcode dispatchers).
* **Modern Alternatives:** While raw pointers are used in C, C++ developers often use `std::function` or `templates` for better type safety and flexibility.

---
#### 3.2.4.2 Callbacks

A callback is a functional programming pattern where a piece of executable code (a function) is passed as an argument to another function. This "caller" function then executes the passed function at a specific point in its logic.

```cpp
// A function that takes a callback as a parameter
void filter(int* arr, int size, bool (*isMatch)(int)) {
    for (int i = 0; i < size; i++) {
        if (isMatch(arr[i])) {
            printf("%d fits the criteria.\n", arr[i]);
        }
    }
}

// Possible callback functions
bool isEven(int n) { return n % 2 == 0; }
bool isPositive(int n) { return n > 0; }

int main() {
    int nums[] = {-2, 1, 4, 7};
    filter(nums, 4, isEven);     // Passing isEven as callback
    filter(nums, 4, isPositive); // Passing isPositive as callback
}

```

Characteristics:

* **Inversion of Control (IoC):** The low-level function (e.g., `filter`) defines the execution flow, but the high-level logic (e.g., `isEven`) is supplied by the user.
* **Asynchronous Execution:** Frequently used in event-driven programming (GUIs, Networking) where a function is triggered only after an event (like a mouse click or data packet arrival) occurs.
* **C Standard Library Usage:** The `qsort` function in `stdlib.h` is a classic example, requiring a comparison callback: `void qsort(void *base, size_t nmemb, size_t size, int (*compar)(const void *, const void *));`.
* **Generic Programming:** Callbacks allow a single function to behave differently based on the logic passed to it, promoting code reuse and modularity.

---
### 3.2.5 Recursion

```cpp
long long factorial(int n) {
    // Base Case: prevents infinite recursion
    if (n <= 1) {
        return 1;
    }
    // Recursive Step: function calls itself with a decremented value
    return n * factorial(n - 1);
}

```

* **Efficiency:** While logically elegant, this specific implementation is  in terms of both time and space complexity due to the stack overhead.

---
### 3.2.6 Scope
#### 3.2.6.1 Local Variables

Local variables are declared inside a function block `{}` or a specific control structure (like a `for` loop). They are created on the **Stack** when the execution enters the block and are destroyed immediately upon exit.

```cpp
void myFunction() {
    int x = 10; // Local variable
    if (x > 0) {
        int y = 20; // Block-scope local variable
    }
    // y is no longer accessible here
}
// x is no longer accessible here

```

Characteristics:

* **Scope:** Limited strictly to the block `{}` in which they are defined.
* **Lifetime:** Automatic storage duration; they exist only while the block is active.
* **Memory:** Stored on the function’s stack frame.
* **Initialization:** They are **not** automatically initialized by the compiler. Using an uninitialized local variable results in "garbage values" and undefined behavior.
* **Shadowing:** A local variable can have the same name as a global variable. In such cases, the local variable "shadows" or hides the global one within that specific scope.

---
#### 3.2.6.2 Global Variables

Global variables are defined outside of all functions, usually at the top of the program. They are accessible from any part of the code (any function) within the same file, and potentially from other files.

```cpp
int globalCount = 100; // Global variable

void increment() {
    globalCount++; // Accessing global variable
}

int main() {
    increment();
    printf("%d", globalCount); // Output: 101
}

```

Characteristics:

* **Scope:** File scope (or program scope if used with `extern`). They are visible to every function defined after their declaration.
* **Lifetime:** Static storage duration; they are created when the program starts and destroyed only when the program terminates.
* **Memory:** Stored in the **Data Segment** (initialized) or **BSS Segment** (uninitialized) of the program's memory, not the stack.
* **Initialization:** Automatically initialized to zero (or `NULL` for pointers) by the compiler if no value is provided.
* **Risks:** Excessive use of global variables is discouraged because they make debugging difficult (any function can change the state), lead to "spaghetti code," and create issues in multi-threaded environments (race conditions).
* **Accessing Shadowed Globals:** In C++, if a local variable has the same name as a global, you can access the global using the scope resolution operator `::` (e.g., `::globalCount`).

--- 
### 3.2.7 main
#### 3.2.7.1 int main()

The `main` function serves as the designated entry point for every C and C++ program. When the Operating System (OS) executes a program, it transfers control to this function.

```cpp
int main() { 
    // code
}

// Alternative for Command Line Arguments
int main(int argc, char* argv[]) {
    // code
}

```

Characteristics:

* **Return Type:** Must return an `int`. This integer is the "Exit Status" or "Return Code" sent back to the operating system.
* **Signature:** While `int main()` is the most common, the standard also defines `int main(int argc, char* argv[])` to handle command-line inputs.
* **Special Case:** Unlike other functions, if the compiler reaches the end of `main` without finding a `return` statement, it implicitly inserts `return 0;` (in C99 and later, and all C++ versions).
* **No Manual Calls:** You should never call `main()` from within your own code; it is reserved for the runtime environment.

---

#### 3.2.7.2 {...}

The curly braces define the **Function Body** and establish the outermost **Block Scope** of the program logic.

```cpp
int main() 
{ // Start of Block Scope
    int x = 5; 
    {
        int y = 10; // Nested Block Scope
    } // y is destroyed here
    return 0;
} // x is destroyed here

```

Characteristics:

* **Compound Statement:** Everything between `{` and `}` is treated as a single unit by the compiler.
* **Automatic Storage:** Any variables declared inside these braces are "Automatic" (local). They are pushed onto the stack when the brace opens and popped off when the brace closes.
* **Control Flow:** The closing brace `}` signifies the end of the main thread of execution for that specific function.

---

#### 3.2.7.3 return 0 / 1

The `return` statement terminates the `main` function and passes an integer value (Exit Status) back to the parent process (usually the Shell or OS).

```cpp
int main() {
    if (file_not_found) {
        return 1; // Unsuccessful termination
    }
    return 0; // Successful termination
}

```

Characteristics:

* **`return 0`:** Interpreted as `EXIT_SUCCESS`. It signals to the OS that the program completed its task exactly as intended without errors.
* **`return 1` (or non-zero):** Interpreted as `EXIT_FAILURE`. Different non-zero numbers (1, 2, -1, etc.) can be used to signal different types of errors to scripts or automation tools.
* **Standard Macros:** In `<stdlib.h>` (C) or `<cstdlib>` (C++), you can use the macros `EXIT_SUCCESS` and `EXIT_FAILURE` for better portability.
* **Impact on Scripting:** In Linux/Unix, you can check this value immediately after execution using `echo $?`; in Windows, using `echo %errorlevel%`.

--- 
## 3.3 I/O and Math

### 3.3.1 Input and Output
#### 3.3.1.1 #include <iostream>

This is a preprocessor directive that includes the **Input/Output Stream** library, which is part of the C++ Standard Library.

```cpp
#include <iostream>

```

Characteristics:

* **Header File:** It defines the objects `std::cin`, `std::cout`, `std::cerr`, and `std::clog`.
* **Declarations:** It contains the definitions for the stream classes (`istream`, `ostream`) required for basic console I/O.
* **Namespace:** All objects within this header are defined inside the `std` namespace.
* **C vs C++:** In C, you would use `<stdio.h>` for functions like `printf` and `scanf`. `iostream` is the type-safe C++ equivalent.

---
#### 3.3.1.2 cout

`cout` (Character Output) is an object of the `ostream` class used to display data to the standard output device (usually the console screen).

```cpp
std::cout << "Value: " << 42 << std::endl;

```

Characteristics:

* **Insertion Operator (`<<`):** Used to "insert" data into the stream.
* **Buffering:** `cout` is buffered, meaning it collects data in memory before printing it to the screen for efficiency.
* **Type Safety:** Unlike `printf`, `cout` automatically detects the data type (int, float, string) and formats it correctly without format specifiers (like `%d`).
* **Chaining:** Multiple insertion operators can be linked in a single statement (cascading).

---
#### 3.3.1.3 cin

`cin` (Character Input) is an object of the `istream` class used to read data from the standard input device (usually the keyboard).

```cpp
int age;
std::cout << "Enter age: ";
std::cin >> age;

```

Characteristics:

* **Extraction Operator (`>>`):** Used to "extract" data from the stream and store it in a variable.
* **Whitespace Sensitive:** By default, `cin` stops reading when it encounters whitespace (space, tab, or newline). To read an entire line including spaces, `std::getline()` is used instead.
* **Type Mismatch:** If the user enters a character when an `int` is expected, `cin` enters a "fail state" and stops further input until cleared.
* **Waiting:** It pauses program execution until the user provides input and presses Enter.

---
#### 3.3.1.4 endl or '\n'

Both are used to insert a newline character, but they differ significantly in how they handle the output buffer.

```cpp
std::cout << "Line 1" << std::endl; // Newline + Flush
std::cout << "Line 2\n";           // Newline only

```

Characteristics:

* **`'\n'` (Newline Character):** * Simply adds a newline.
* Faster and more efficient because it does not force the buffer to empty.
* Preferred for high-performance loops or frequent printing.


* **`std::endl` (End Line):** * Adds a newline **and** flushes the output buffer (`std::cout.flush()`).
* Ensures that the output appears immediately on the screen.
* Can cause performance hits if used excessively due to repeated hardware I/O requests.

--- 
### 3.3.2 Common Math Functions
#### 3.3.2.1 sqrt

Computes the square root of a non-negative number. Part of the `<cmath>` (C++) or `<math.h>` (C) library.

```cpp
#include <cmath>
double result = sqrt(25.0); // result = 5.0

```

Characteristics:

* **Return Type:** Returns a `double`, `float`, or `long double`.
* **Domain Error:** If the input is negative, it returns `NaN` (Not a Number) and may set `errno` to `EDOM`.
* **Complexity:** Implemented using hardware instructions or iterative methods like Newton-Raphson.

---
#### 3.3.2.2 pow

Calculates the value of a base raised to the power of an exponent ().

```cpp
double result = pow(2.0, 3.0); // 2^3 = 8.0

```

Characteristics:

* **Syntax:** `pow(base, exponent)`.
* **Precision:** Uses floating-point arithmetic. For integer-only powers, a custom loop is often faster and more precise.
* **Special Cases:** `pow(0, 0)` is usually 1, but can be implementation-defined. Negative bases with fractional exponents result in `NaN`.

---
#### 3.3.2.3 floor

Returns the largest integer value less than or equal to the argument (rounds down toward negative infinity).

```cpp
double val = floor(3.8);  // 3.0
double neg = floor(-3.2); // -4.0

```

Characteristics:

* Useful for array indexing calculations or converting floating-point coordinates to grid integers.

---
#### 3.3.2.4 ceil

Short for "ceiling." Returns the smallest integer value greater than or equal to the argument (rounds up toward positive infinity).

```cpp
double val = ceil(3.1);  // 4.0
double neg = ceil(-3.8); // -3.0

```

Characteristics:

* Often used in pagination logic (e.g., calculating total pages needed for  items).

---
#### 3.3.2.5 min()

Returns the smaller of two values. In C++, this is part of the `<algorithm>` header (not `cmath`).

```cpp
#include <algorithm>
int result = std::min(10, 20); // 10

```

Characteristics:

* **Type Strictness:** In C++, both arguments must be of the exactly same type (or you must specify the template type like `std::min<double>(10, 12.5)`).
* **C-Style:** In C, this is often implemented as a macro: `#define min(a,b) ((a)<(b)?(a):(b))`.

---
#### 3.3.2.6 max()

Returns the larger of two values. Found in the `<algorithm>` header.

```cpp
int result = std::max(10, 20); // 20

```

Characteristics:

* Follows the same type-matching rules as `min()`.
* Highly efficient; usually compiled down to a single conditional move instruction (`cmov`).

---
#### 3.3.2.7 round()

Rounds the argument to the nearest integer value.

```cpp
double a = round(3.5);  // 4.0
double b = round(3.4);  // 3.0
double c = round(-3.5); // -4.0

```

Characteristics:

* **Midpoint Policy:** Rounds halfway cases away from zero (e.g., 0.5 becomes 1, -0.5 becomes -1).
* **Availability:** Introduced in C++11 and C99. Older standards required manual implementation: `floor(x + 0.5)`.

---
#### 3.3.2.8 log()

Calculates the **natural logarithm** (base-) of a number.$

```cpp
double val = log(2.718); // Approx 1.0

```

Characteristics:

* **Base-10:** For common logs, use `log10(x)`.
* **Base-2:** For binary logs, use `log2(x)` (C++11/C99).
* **Domain:** The argument must be greater than 0. If , it returns `-HUGE_VAL` (); if , it returns `NaN`.

---

### 3.3.3 CMath
The `<cmath>` header provides a collection of functions and macros for performing common mathematical operations on floating-point numbers.

---
#### 3.3.3.1 Mathematical Constants and Special Values

This section covers the fundamental macros and types used to represent extreme values, non-numeric results, and classification states in floating-point arithmetic.

##### 3.3.3.1.1 Floating-Point Constants

These macros represent infinity and "Not-a-Number," often resulting from undefined operations (like division by zero or square roots of negative numbers).

* **`HUGE_VAL` / `HUGE_VALF` / `HUGE_VALL**`: Represents a value too large to be represented by the type (`double`, `float`, and `long double` respectively). Usually resolves to infinity.
* **`INFINITY`**: A constant representing positive infinity.
* **`NAN`**: Represents "Not-a-Number."

```cpp
#define HUGE_VAL  /* implementation-defined */
#define HUGE_VALF /* implementation-defined */
#define HUGE_VALL /* implementation-defined */
#define INFINITY  /* positive infinity */
#define NAN       /* quiet NaN */

```

---
##### 3.3.3.1.2 Floating-Point Classifications

Macros returned by the `fpclassify()` function to identify the nature of a floating-point value.

* **`FP_INFINITE`**: Value is positive or negative infinity.
* **`FP_NAN`**: Value is Not-a-Number.
* **`FP_NORMAL`**: A standard non-zero floating-point number.
* **`FP_SUBNORMAL`**: A value very close to zero with reduced precision.
* **`FP_ZERO`**: Value is exactly zero (positive or negative).

```cpp
#define FP_INFINITE  /* constant */
#define FP_NAN       /* constant */
#define FP_NORMAL    /* constant */
#define FP_SUBNORMAL /* constant */
#define FP_ZERO      /* constant */

```

---
##### 3.3.3.1.3 Error Handling

C++ handles math errors via two mechanisms: `errno` (legacy C-style) and floating-point exceptions.

* **`math_errhandling`**: An integer bitmask that tells you if the current implementation uses `MATH_ERRNO` or `MATH_ERREXCEPT`.
* **`MATH_ERRNO`**: If set, the global `errno` variable is updated on error.
* **`MATH_ERREXCEPT`**: If set, floating-point exceptions (like `FE_DIVBYZERO`) are raised on error.

```cpp
#define MATH_ERRNO     /* constant */
#define MATH_ERREXCEPT /* constant */
#define math_errhandling /* bitmask of MATH_ERRNO | MATH_ERREXCEPT */

```

---
#### 3.3.3.2 Trigonometric Functions

Trigonometric functions in C++ compute the relationships between angles and sides of triangles. All angles are measured in **radians**.

##### 3.3.3.2.1 Basic Trigonometric Functions

These functions compute the standard circular ratios.

* **`sin()` / `cos()` / `tan()**`: Computes the sine, cosine, and tangent of an angle  (in radians).
* **`sinf()` / `cosf()` / `tanf()**`: `float` versions for better performance or lower memory footprint.
* **`sinl()` / `cosl()` / `tanl()**`: `long double` versions for higher precision.

```cpp
namespace std {
  /* floating-point-type */ cos(/* floating-point-type */ x);
  float cosf(float x);
  long double cosl(long double x);

  /* floating-point-type */ sin(/* floating-point-type */ x);
  float sinf(float x);
  long double sinl(long double x);

  /* floating-point-type */ tan(/* floating-point-type */ x);
  float tanf(float x);
  long double tanl(long double x);
}

```

---

##### 3.3.3.2.2 Inverse Trigonometric Functions

These functions return the angle (in radians) whose trigonometric ratio is .

* **`asin()`**: Arcsine; returns values in .
* **`acos()`**: Arccosine; returns values in .
* **`atan()`**: Arctangent; returns values in .

```cpp
namespace std {
  /* floating-point-type */ acos(/* floating-point-type */ x);
  float acosf(float x);
  long double acosl(long double x);

  /* floating-point-type */ asin(/* floating-point-type */ x);
  float asinf(float x);
  long double asinl(long double x);

  /* floating-point-type */ atan(/* floating-point-type */ x);
  float atanf(float x);
  long double atanl(long double x);
}

```

---
##### 3.3.3.2.3 Long Double Version
  * `acosl()`, `asinl()`, `atanl()`
  * `cosl()`, `sinl()`, `tanl()`

---

##### 3.3.3.2.4 Two-Argument Arctangent

The `atan2` function is critical for coordinate geometry.

* **`atan2(y, x)`**: Computes the arctangent of  but uses the signs of both arguments to determine the correct quadrant of the resulting angle. It is more robust than `atan(y/x)` because it handles  (vertical lines) without division-by-zero errors.

```cpp
namespace std {
  /* floating-point-type */ atan2(/* floating-point-type */ y, 
                                 /* floating-point-type */ x);
  float atan2f(float y, float x);
  long double atan2l(long double y, long double x);
}

```

---
#### 3.3.3.3 Hyperbolic Functions

Hyperbolic functions are analogs of the ordinary trigonometric functions but are based on hyperbolas rather than circles. They are frequently used in physics (e.g., the shape of a hanging cable) and complex analysis.

##### 3.3.3.3.1 Basic Hyperbolic Functions

These functions calculate the hyperbolic sine, cosine, and tangent.

* **`sinh()`**: Computes the hyperbolic sine ().
    $\sinh(x) = \frac{e^x - e^{-x}}{2}$
* **`cosh()`**: Computes the hyperbolic cosine ().
    $\sinh(x) = \frac{e^x - e^{-x}}{2}$
* **`tanh()`**: Computes the hyperbolic tangent ().

```cpp
namespace std {
  /* floating-point-type */ cosh(/* floating-point-type */ x);
  float coshf(float x);
  long double coshl(long double x);

  /* floating-point-type */ sinh(/* floating-point-type */ x);
  float sinhf(float x);
  long double sinhl(long double x);

  /* floating-point-type */ tanh(/* floating-point-type */ x);
  float tanhf(float x);
  long double tanhl(long double x);
}

```

---

##### 3.3.3.3.2 Inverse Hyperbolic Functions

These functions return the value whose hyperbolic function is .

* **`asinh()`**: Inverse hyperbolic sine.
* **`acosh()`**: Inverse hyperbolic cosine (defined for ).
* **`atanh()`**: Inverse hyperbolic tangent (defined for ).

```cpp
namespace std {
  /* floating-point-type */ acosh(/* floating-point-type */ x);
  float acoshf(float x);
  long double acoshl(long double x);

  /* floating-point-type */ asinh(/* floating-point-type */ x);
  float asinhf(float x);
  long double asinhl(long double x);

  /* floating-point-type */ atanh(/* floating-point-type */ x);
  float atanhf(float x);
  long double atanhl(long double x);
}

```

---
#### 3.3.3.4 Exponential and Logarithmic Functions

These functions handle powers of , powers of 2, and various forms of logarithms. They are highly optimized for precision, especially near zero.

##### 3.3.3.4.1 Exponential Functions

Functions that calculate .

* **`exp()`**: Computes the base- exponential ().
* **`exp2()`**: Computes 2 raised to the power  ().
* **`expm1()`**: Computes . This is significantly more accurate than `exp(x) - 1` when  is very close to zero.
        $\text{expm1}(x) = e^x - 1$

```cpp
namespace std {
  /* floating-point-type */ exp(/* floating-point-type */ x);
  float expf(float x);
  long double expl(long double x);

  /* floating-point-type */ exp2(/* floating-point-type */ x);
  float exp2f(float x);
  long double exp2l(long double x);

  /* floating-point-type */ expm1(/* floating-point-type */ x);
  float expm1f(float x);
  long double expm1l(long double x);
}

```

---

##### 3.3.3.4.2 Logarithmic Functions

Functions that calculate the exponent required to produce a certain number.

* **`log()`**: The natural logarithm (, base ).
    $\log_e(x) = \ln(x)$
* **`log10()`**: Common logarithm (base 10).
    $\log_{10}(x) = \frac{\ln(x)}{\ln(10)}$
* **`log2()`**: Binary logarithm (base 2).
* **`log1p()`**: Computes . This is much more accurate than `log(1 + x)` for very small values of .

```cpp
namespace std {
  /* floating-point-type */ log(/* floating-point-type */ x);
  float logf(float x);
  long double logl(long double x);

  /* floating-point-type */ log10(/* floating-point-type */ x);
  float log10f(float x);
  long double log10l(long double x);

  /* floating-point-type */ log2(/* floating-point-type */ x);
  float log2f(float x);
  long double log2l(long double x);

  /* floating-point-type */ log1p(/* floating-point-type */ x);
  float log1pf(float x);
  long double log1pl(long double x);
}

```

---

##### 3.3.3.4.3 Logarithmic Utility Functions

These functions are used to extract the exponent part of a floating-point number’s internal representation.

* **`logb()`**: Returns the signed exponent of  as a floating-point value.
* **`ilogb()`**: Returns the signed exponent of  as an integer.

```cpp
namespace std {
  constexpr /* floating-point-type */ logb(/* floating-point-type */ x);
  constexpr float logbf(float x);
  constexpr long double logbl(long double x);

  constexpr int ilogb(/* floating-point-type */ x);
  constexpr int ilogbf(float x);
  constexpr int ilogbl(long double x);
}

```

---
#### 3.3.3.5 Floating-Point Manipulation

These functions allow you to decompose floating-point numbers into their constituent parts (mantissa and exponent) or perform specialized division and remainder operations.

##### 3.3.3.5.1 Fractional and Exponent Manipulation

Used to break a number into its normalized fraction and power of 2, or to reassemble them.

* **`frexp()`**: Decomposes a number  into a normalized fraction (mantissa) in the range  and an integer exponent , such that .
* **`ldexp()`**: The inverse of `frexp`; computes .
* **`scalbn()` / `scalbln()**`: Efficiently computes  (usually ). `scalbln` accepts a `long int` for larger exponents.

```cpp
namespace std {
  constexpr /* floating-point-type */ frexp(/* floating-point-type */ value, int* exp);
  constexpr float frexpf(float value, int* exp);
  constexpr long double frexpl(long double value, int* exp);

  constexpr /* floating-point-type */ ldexp(/* floating-point-type */ x, int exp);
  constexpr float ldexpf(float x, int exp);
  constexpr long double ldexpl(long double x, int exp);

  constexpr /* floating-point-type */ scalbn(/* floating-point-type */ x, int n);
  constexpr /* floating-point-type */ scalbln(/* floating-point-type */ x, long int n);
}

```

---

##### 3.3.3.5.2 Modular and Remainder Functions

Functions for dividing floating-point numbers and extracting the remainder or fractional part.

* **`modf()`**: Splits a value into its integer and fractional parts. Both parts carry the same sign as the original value.
* **`fmod()`**: Computes the floating-point remainder of  (specifically  where  is the truncated quotient).
* **`remainder()`**: Similar to `fmod`, but uses the rounded quotient (IEE 754 standard).
* **`remquo()`**: Computes the same remainder as `remainder()`, but also stores the last few bits of the quotient in a pointer.

```cpp
namespace std {
  constexpr /* floating-point-type */ modf(/* floating-point-type */ value, /* floating-point-type */* iptr);
  
  constexpr /* floating-point-type */ fmod(/* floating-point-type */ x, /* floating-point-type */ y);
  
  constexpr /* floating-point-type */ remainder(/* floating-point-type */ x, /* floating-point-type */ y);
  
  constexpr /* floating-point-type */ remquo(/* floating-point-type */ x, /* floating-point-type */ y, int* quo);
}

```

---
#### 3.3.3.6 Power Functions

These functions provide tools for exponentiation, calculating various roots, and determining geometric distances. They are designed to handle different floating-point precisions (`float`, `double`, and `long double`).

##### 3.3.3.6.1 Power and Root Functions

Used to compute the result of raising a base to an exponent or finding the principal  root of a value.

* **`pow()`**: Computes the base  raised to the power  ().
    $\text{pow}(x, y) = x^y$
* **`sqrt()`**: Computes the square root of  (). If , a domain error occurs.
* **`cbrt()`**: Computes the cubic root of  (). Unlike `sqrt`, it can handle negative inputs.

```cpp
namespace std {
  /* floating-point-type */ pow(/* floating-point-type */ x, /* floating-point-type */ y);
  float powf(float x, float y);
  long double powl(long double x, long double y);

  /* floating-point-type */ sqrt(/* floating-point-type */ x);
  float sqrtf(float x);
  long double sqrtl(long double x);

  /* floating-point-type */ cbrt(/* floating-point-type */ x);
  float cbrtf(float x);
  long double cbrtl(long double x);
}

```

---

##### 3.3.3.6.2 Hypotenuse Functions

Calculates the length of the hypotenuse of a right-angled triangle. These functions are preferred over manual calculation because they use an algorithm that avoids internal overflow or underflow during the squaring process.

* **`hypot(x, y)`**: Computes the 2D hypotenuse: .
    $\text{hypot}(x, y) = \sqrt(x^2 + y^2)$
* **`hypot(x, y, z)`**: Computes the 3D distance from the origin:  (Available since C++17).

```cpp
namespace std {
  /* floating-point-type */ hypot(/* floating-point-type */ x, /* floating-point-type */ y);
  float hypotf(float x, float y);
  long double hypotl(long double x, long double y);

  // three-dimensional hypotenuse
  float hypot(/* floating-point-type */ x, /* floating-point-type */ y, /* floating-point-type */ z);
}

```

---

##### 3.3.3.6.3 Linear Interpolation

Introduced in C++20, this function performs a "mix" between two values based on a weight.

* **`lerp()`**: Computes the linear interpolation between  and  for the parameter . The result is calculated as . If , it returns ; if , it returns .

```cpp
namespace std {
  // linear interpolation
  constexpr /* floating-point-type */ lerp(/* floating-point-type */ a, 
                                           /* floating-point-type */ b, 
                                           /* floating-point-type */ t) noexcept;
}

```

---
#### 3.3.3.7 Absolute Value Functions

These functions are used to obtain the magnitude of a numerical value, effectively stripping away the negative sign if one exists.

##### 3.3.3.7.1 Integer Absolute Functions

In the `<cmath>` header (and `<cstdlib>`), `abs()` is overloaded to handle various integer widths. These return the positive version of the provided integer.

* **`abs()`**: Returns the absolute value of an integer. If the input is positive or zero, it is returned as is; if negative, the sign is flipped.
* **`absf()`**: A specific variant (often found in extended headers or used in C) to represent the float version of absolute value. In standard C++, this is typically handled by std::abs(float) or fabsf().

* **`absl()`**: A specific variant representing the long double version of absolute value. In standard C++, this is typically handled by std::abs(long double) or fabsl().

```cpp
namespace std {
  constexpr int abs(int j);                     // absolute value for int
  constexpr long int abs(long int j);           // absolute value for long
  constexpr long long int abs(long long int j); // absolute value for long long
}

```

> [!NOTE]
> In modern C++, it is generally recommended to use std::abs() for all types, as 
> it is overloaded for int, float, double, and long double. However, the
> explicit suffixes (f for float, l for long double) are useful in systems programming or when interfacing with C code.

---
##### 3.3.3.7.2 Floating-Point Absolute Functions

For decimal numbers, `fabs` (Floating-point ABSolute) is the standard choice. While C++ overloads `std::abs()` for floating-point types, `fabs` is often used to be explicit about the type being handled, especially in C-compatibility contexts.

* **`fabs()`**: Computes the absolute value of a floating-point number .
* **`fabsf()` / `fabsl()**`: Explicit versions for `float` and `long double` respectively, used to avoid implicit conversions.

```cpp
namespace std {
  constexpr /* floating-point-type */ fabs(/* floating-point-type */ x);
  constexpr float fabsf(float x);
  constexpr long double fabsl(long double x);
  constexpr long double fabsf(long double x);
  
  // Note: std::abs is also overloaded for floating-point types
  // but is technically "deleted" for certain generic cases to prevent ambiguity
  constexpr /* floating-point-type */ abs(/* floating-point-type */ j); 
}

```

---
#### 3.3.3.8 Rounding Functions

Rounding functions convert floating-point values into integer values based on specific directional rules. These are essential for mapping continuous data to discrete steps.

##### 3.3.3.8.1 Basic Rounding

These functions provide predictable, fixed-direction rounding regardless of the fractional magnitude.

* **`ceil()`**: The "Ceiling" function. Rounds **upward** toward positive infinity. Result is the smallest integer .
* **`floor()`**: The "Floor" function. Rounds **downward** toward negative infinity. Result is the largest integer .
* **`trunc()`**: The "Truncate" function. Rounds toward **zero**. It simply discards the fractional part (acts like `floor` for positive numbers and `ceil` for negative numbers).

```cpp
namespace std {
  constexpr /* floating-point-type */ ceil(/* floating-point-type */ x);
  constexpr float ceilf(float x);
  constexpr long double ceill(long double x);

  constexpr /* floating-point-type */ floor(/* floating-point-type */ x);
  constexpr float floorf(float x);
  constexpr long double floorl(long double x);

  constexpr /* floating-point-type */ trunc(/* floating-point-type */ x);
  constexpr float truncf(float x);
  constexpr long double truncl(long double x);
}

```

---
##### 3.3.3.8.2 Rounding to Nearest Integer

These functions determine the result based on which integer is numerically closer to the input.

* **`round()`**: Rounds to the nearest integer. If the value is exactly halfway (0.5), it rounds **away from zero** (e.g., , ).
* **`lround()` / `llround()**`: Identical to `round()`, but returns the result as a `long` or `long long` respectively.
* **`nearbyint()`**: Rounds to the nearest integer using the current floating-point rounding environment (usually "round to nearest, ties to even"). It does **not** raise the `FE_INEXACT` exception.
* **`rint()`**: Similar to `nearbyint()`, but **does** raise a floating-point exception if the result differs from the argument.
* **`lrint()` / `llrint()**`: Rounds using the current rounding mode and returns a `long` or `long long`.

```cpp
namespace std {
  /* nearest integer, returns floating-point type */
  /* floating-point-type */ nearbyint(/* floating-point-type */ x);
  float nearbyintf(float x);
  long double nearbyintl(long double x);

  /* nearest integer, returns floating-point type, may throw exception */
  /* floating-point-type */ rint(/* floating-point-type */ x);
  float rintf(float x);
  long double rintl(long double x);

  /* nearest integer, returns long/long long */
  long int lrint(/* floating-point-type */ x);
  long int lrintf(float x);
  long int lrintl(long double x);

  long long int llrint(/* floating-point-type */ x);
  long long int llrintf(float x);
  long long int llrintl(long double x);

  /* nearest integer, halfway cases away from zero */
  constexpr /* floating-point-type */ round(/* floating-point-type */ x);
  constexpr float roundf(float x);
  constexpr long double roundl(long double x);

  /* nearest integer (away from zero), returns long/long long */
  constexpr long int lround(/* floating-point-type */ x);
  constexpr long int lroundf(float x);
  constexpr long int lroundl(long double x);

  constexpr long long int llround(/* floating-point-type */ x);
  constexpr long long int llroundf(float x);
  constexpr long long int llroundl(long double x);
}

```

---
##### 3.3.3.8.3 Comparison Table

| Function | 2.3 | 2.5 | 2.7 | -2.3 | -2.5 | -2.7 |
| --- | --- | --- | --- | --- | --- | --- |
| `floor` | 2.0 | 2.0 | 2.0  | -3.0 | -3.0 | -3.0 |
| `ceil` | 3.0 |3.0  | 3.0 | -2.0 | -2.0 | -2.0  |
| `trunc` | 2.0  |2.0  | 2.0 | -2.0 | -2.0 | -2.0  |
| `round` | 2.0 | 3.0 | 3.0 | -2.0  | -3.0  | -3.0  |

---
#### 3.3.3.9 Sign and Magnitude Functions

These functions are used to manipulate the signs of floating-point numbers and to inspect or compare the properties of floating-point values (like whether they are infinite or "Not a Number").

##### 3.3.3.9.1 Sign Functions

Functions used to extract or transfer the sign of a value.

* **`copysign()`**: Composes a value with the magnitude of  and the sign of . This is particularly useful for handling signed zeros (e.g., ensuring a result has the correct sign based on a direction vector).
* **`nan()`**: Returns a quiet NaN (Not-a-Number) value. The `tagp` string can be used to distinguish between different types of NaNs.

```cpp
namespace std {
  constexpr /* floating-point-type */ copysign(/* floating-point-type */ x, /* floating-point-type */ y);
  constexpr float copysignf(float x, float y);
  constexpr long double copysignl(long double x, long double y);

  double nan(const char* tagp);
  float nanf(const char* tagp);
  long double nanl(const char* tagp);
}

```

---
##### 3.3.3.9.2 Floating-Point Classification

These functions allow you to check the state and validity of a floating-point number.

* **`fpclassify()`**: Returns the category of the value: `FP_INFINITE`, `FP_NAN`, `FP_NORMAL`, `FP_SUBNORMAL`, or `FP_ZERO`.
* **`isfinite()`**: Returns `true` if the value is not infinite and not NaN.
* **`isinf()`**: Returns `true` if the value is positive or negative infinity.
* **`isnan()`**: Returns `true` if the value is Not-a-Number (NaN).
* **`isnormal()`**: Returns `true` if the value is a "normal" number (not zero, subnormal, infinite, or NaN).
* **`signbit()`**: Returns `true` if the sign of  is negative (works even for negative zeros and negative infinities).

```cpp
namespace std {
  constexpr int fpclassify(/* floating-point-type */ x);
  
  constexpr bool isfinite(/* floating-point-type */ x);
  constexpr bool isinf(/* floating-point-type */ x);
  constexpr bool isnan(/* floating-point-type */ x);
  constexpr bool isnormal(/* floating-point-type */ x);
  constexpr bool signbit(/* floating-point-type */ x);
}

```

---

##### 3.3.3.9.3 Floating-Point Comparison

Standard operators (like `<` or `>`) can sometimes cause issues with NaN values. These specialized functions provide safe comparison logic.

* **`isgreater()` / `isless()**`: Compares  and . Returns `false` if either argument is NaN, without raising an exception.
* **`isgreaterequal()` / `islessequal()**`: Comparisons for "greater or equal" and "less or equal".
* **`islessgreater()`**: Returns `true` if  or  (i.e., they are not equal and neither is NaN).
* **`isunordered()`**: Returns `true` if one or both of the arguments are NaN.

```cpp
namespace std {
  constexpr bool isgreater(/* floating-point-type */ x, /* floating-point-type */ y);
  constexpr bool isgreaterequal(/* floating-point-type */ x, /* floating-point-type */ y);
  constexpr bool isless(/* floating-point-type */ x, /* floating-point-type */ y);
  constexpr bool islessequal(/* floating-point-type */ x, /* floating-point-type */ y);
  constexpr bool islessgreater(/* floating-point-type */ x, /* floating-point-type */ y);
  constexpr bool isunordered(/* floating-point-type */ x, /* floating-point-type */ y);
}

```

---
#### 3.3.3.10 Mathematical Special Functions

Introduced largely in C++17, these functions address complex mathematical needs in physics, statistics, and engineering. They handle advanced calculus, probability distributions, and wave mechanics.

---

##### 3.3.3.10.1 Gamma and Error Functions

These are fundamental in statistics (Normal distributions) and advanced calculus.

* **`erf()`**: The Gauss error function, used to calculate the probability of a variable falling within a range.
    $\text{erf}(x) = \frac{2}{\sqrt(\pi\)} \int_0^x e^{-t^2} \, dt$
* **`erfc()`**: The complementary error function (). (1−erf(x))
* **`tgamma()`**: The "True Gamma" function, which extends the factorial function to real and complex numbers.
    $\Gamma(z) = \int_0\infty t^{z-1} e^{-t} \, dt$
* **`lgamma()`**: Calculates the natural logarithm of the absolute value of the Gamma function (). ln∣Γ(x)∣
* **`beta()`**: The Euler integral of the first kind, related to Gamma functions.

```cpp
namespace std {
  /* floating-point-type */ erf(/* floating-point-type */ x);
  /* floating-point-type */ erfc(/* floating-point-type */ x);
  
  /* floating-point-type */ tgamma(/* floating-point-type */ x);
  /* floating-point-type */ lgamma(/* floating-point-type */ x);

  /* floating-point-type */ beta(/* floating-point-type */ x, /* floating-point-type */ y);
}

```

---

##### 3.3.3.10.2 Bessel and Neumann Functions

Used to solve differential equations involving cylindrical or spherical symmetry (e.g., heat conduction, wave propagation).

* **`cyl_bessel_j()` / `sph_bessel()**`: Cylindrical/Spherical Bessel functions of the first kind.
    $J_n(x) = \frac{1}{\pi} \int_0\pi \cos(n \theta - x \sin \theta) \, d\theta$
* **`cyl_bessel_i()` / `cyl_bessel_k()**`: Modified cylindrical Bessel functions.
* **`cyl_neumann()` / `sph_neumann()**`: Bessel functions of the second kind.

```cpp
namespace std {
  /* Cylindrical Bessel first kind */
  /* floating-point-type */ cyl_bessel_j(/* floating-point-type */ nu, /* floating-point-type */ x);

  /* Spherical Bessel first kind */
  /* floating-point-type */ sph_bessel(unsigned n, /* floating-point-type */ x);

  /* Cylindrical Neumann */
  /* floating-point-type */ cyl_neumann(/* floating-point-type */ nu, /* floating-point-type */ x);
}

```

---

##### 3.3.3.10.3 Elliptic Integrals

Commonly used in calculating the arc length of ellipses and in electromagnetism.

* **`comp_ellint_1 / 2 / 3()`**: Complete elliptic integrals of the first, second, and third kind.
* **`ellint_1 / 2 / 3()`**: Incomplete elliptic integrals.

```cpp
namespace std {
  /* Complete elliptic integral of the first kind */
  /* floating-point-type */ comp_ellint_1(/* floating-point-type */ k);

  /* Incomplete elliptic integral of the second kind */
  /* floating-point-type */ ellint_2(/* floating-point-type */ k, /* floating-point-type */ phi);
}

```

---

##### 3.3.3.10.4 Polynomial and Zeta Functions

Orthogonal polynomials used in numerical analysis and the Riemann zeta function used in number theory.

* **`hermite()`**: Hermite polynomials (used in quantum mechanics).
* **`laguerre()` / `assoc_laguerre()**`: Laguerre and associated Laguerre polynomials.
* **`legendre()` / `assoc_legendre()**`: Legendre and associated Legendre functions.
* **`riemann_zeta()`**: The Riemann zeta function . ζ(x)
    $\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s}$
* **`expint()`**: The exponential integral function.

```cpp
namespace std {
  /* Hermite polynomials */
  /* floating-point-type */ hermite(unsigned n, /* floating-point-type */ x);

  /* Legendre polynomials */
  /* floating-point-type */ legendre(unsigned l, /* floating-point-type */ x);

  /* Riemann zeta function */
  /* floating-point-type */ riemann_zeta(/* floating-point-type */ x);

  /* Exponential integral */
  /* floating-point-type */ expint(/* floating-point-type */ x);
}

```

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

| OS      | Extension |
| ------- | --------- |
| Linux   | `.a`      |
| macOS   | `.a`      |
| Windows | `.lib`    |

##### Create Static Libraries
G++
- Step 1: Compile to Object File
`g++ -c src/mylib.cpp -Iinclude`
- Step 2: Create Static Library
`ar rcs libmylib.a mylib.o`

MSVC
```bat
cl /c src\mylib.cpp /I include
lib mylib.obj /OUT:mylib.lib
```

---
##### Use Static Libraries
G++ `g++ main.cpp -L. -lmylib -Iinclude`
msvc `cl main.cpp mylib.lib /I include`

---
#### 4.1.3.9 Dynamic Libraries

- Step 1: Compile with position-independent code
- Step 2: Create Shared Library

##### Linux
`g++ -fPIC -c src/mylib.cpp -Iinclude`
`g++ -shared -o libmylib.so mylib.o`
Usage
`g++ main.cpp -L. -lmylib -Iinclude export LD_LIBRARY_PATH=. ./a.out`

##### MacOS
`g++ -fPIC -c src/mylib.cpp -Iinclude`
`g++ -dynamiclib -o libmylib.dylib mylib.o`
Usage
`export DYLD_LIBRARY_PATH=. ./a.out`

##### Windows(msvc)
`cl /LD src\mylib.cpp /I include /Fe:mylib.dll`
`cl main.cpp mylib.lib /I include`
Usage
should be in PATH or at the place of executable
>[!NOTE]
> The format to be followed for windows dynamic libraries are quite different

```cpp 
#ifdef MYLIB_EXPORTS
#define MYLIB_API __declspec(dllexport)
#else
#define MYLIB_API __declspec(dllimport)
#endif
/* in the file your gonna use your file*/ 
#define MYLIB_EXPORTS
#include "mylib.h"
```

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
### 4.1.8 Project Structure
#### 4.1.8.1 Using Make 
```txt
my_project/
├─ Makefile
├─ src/
├─ include/
```

---
#### 4.1.8.2 Using Cmake
```txt
my_project/
├─ CMakeLists.txt   ← REQUIRED (root)
├─ src/
├─ include/
├─ lib/          # or external/
    ├─ static/    # .a (Linux/macOS), .lib (Windows)
    ├─ shared/    # .so (Linux), .dll (Windows), .dylib (macOS)
    └─ headers/   # optional, public headers if library needs them
├─ tests/
└─ README.md

#cmake after result
my_project/
├─ CMakeLists.txt
├─ src/
├─ lib/          # or external/
    ├─ static/    # .a (Linux/macOS), .lib (Windows)
    ├─ shared/    # .so (Linux), .dll (Windows), .dylib (macOS)
    └─ headers/   # optional, public headers if library needs them
├─ build/           
    └─ Makefile      ← generated
    └─ CMakeCache.txt 
    └─ cmake_install.cmake
    └─ CMakeFiles
```
- you can run cmake in build so to test

#### Basic Etiquettes
-  Put binaries in src/
-  Commit build/ to git
-  Mix Makefile + CMake
-  Put headers next to .c files randomly
-  Hardcode platform paths
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

### 10.1.3 Compiler
The cpp and c compiler has 4 main functions, and here is a summary of what it does.

- Preprocessing: Clean up and copy-paste (#include stuff).

- Compilation: Turn C++ into Assembly (Logic check).

- Assembly: Turn Assembly into Binary (1s and 0s).

- Linking: Glue all the binary pieces together into one executable.

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
