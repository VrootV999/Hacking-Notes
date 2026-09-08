# C++ Core Concepts Notes

**Purpose:** Quick re-learning and revisiting all core concepts of C++
**Style:** Short, precise, complete with syntax, explanation, and commented examples

---

## 0. Initialisation of Variables
These are few ways to Initialise variables
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

## 1. Namespace

Use: Avoid name conflicts in large projects.

```cpp
#include <iostream>
using namespace std; // Avoid in headers

int main() {
    cout << "Hello"; // std::cout if no 'using'
}

namespace math {
    int add(int a, int b) { return a + b; }
}

int result = math::add(3, 4); // Access using scope resolution
using namespace math;
result = add(3, 4);

// C++17+ Nested
namespace outer::inner {
    void greet() {}
}
```

---

## 2. Type Aliases (typedef / using)

Use: Rename data types for clarity.

```cpp
typedef unsigned int uint;
uint a = 10; // same as unsigned int

// Modern C++11+
using uint = unsigned int;
```

---

## 3. Using

```cpp
using namespace std;         // Avoid in headers
using std::cout test;        // Only for cout
using myint = unsigned int;  // Alias for type
```

---

## 4. Type Conversion

```cpp
int x = 5;
double y = (double)x; // explicit
int z = y; // implicit
```

---

## Casting
```cpp 
// Static cast: safest general-purpose cast for common conversions.
double d = 123.45;
int i = static_cast<int>(d);
// Dynamic cast: safe downcasting with runtime type checking.
Base* base = new Derived();
Derived* derived = dynamic_cast<Derived*>(base);
// Reinterpret cast: raw memory reinterpretation (dangerous).
void* ptr = &i;
uintptr_t address = reinterpret_cast<uintptr_t>(ptr);
// Const cast: adds or removes const qualifier.
const char* str = "hello";
char* writeable = const_cast<char*>(str);
// Bit cast (C++20): safe bit-pattern reinterpretation.
float f = 3.14f;
uint32_t bits = std::bit_cast<uint32_t>(f);
```

---

## 5. Control Flow

### if / else if / else

```cpp
int x = 10;
if (x < 5) cout << "Small";
else if (x == 10) cout << "Equal";
else cout << "Big";
```

### switch

```cpp
switch(x) {
  case 1: cout << "One"; break;
  case 2: cout << "Two"; break;
  default: cout << "Other";
}
```

### switch with strings → ❌ Not supported directly

```cpp
string cmd = "start";
if (cmd == "start") cout << "Start";
else if (cmd == "stop") cout << "Stop";
```

---

## 6. Ternary Operator

```cpp
int max = (a > b) ? a : b;
```

---

## Global Variable 

```cpp 
// Makes a constant accessible
// from other files (external linkage).
// Useful for shared constants
// needed across multiple •epp files.
extern const int BUFFER_SIZE = 1024;

// File-private compile-time constant
// that doesn't generate address references.
// Good for optimization when the constant
// is only needed in one file.
static constexpr double TAX_RATE = 0.08;

// Function that can be evaluated at
// compile-time and has a single definition
// across files. Reduces code duplication
// while enabling compile-time computation.
inline constexpr double kelvinToCelsius(double kelvin){
  return kelvin - 273.15;
}

// Modern way to define compile-time class
// constants without separate definition.
// Combines zero runtime overhead with
// single-instance storage.
class Config {
  inline static constexpr int MAX_CONNECTIONS = 100;
}
```

### 1. inline
|   Name             |Defenition|
| ------------------ | ----------------- |
| inline function    | Optimization & ODR Compliance. It suggests to the compiler that the function body should be inserted directly at each call site (inlining) instead of making a standard function call. This relaxes the One Definition Rule (ODR), allowing the function definition to appear in multiple files (e.g., in a header) without causing linking errors. The compiler may ignore the suggestion for large functions.|
| inline variable    | ODR Compliance & Single Instance Guarantee. It tells the compiler and linker that the variable should have exactly one instance across all translation units. This is particularly useful for defining constants or global state directly in header files, guaranteeing a single shared memory location.|

```cpp 
namespace lib {
inline namespace v1 {
void func() { /* v1 implementation */ }
namespace v2 1
void func() { /* v2 implementation */ }
int main() {
lib:: v1:: func();
lib:: v2:: func();
lib:: func();
// Calls v1.
// Calls v2.
// Calls v1 because it's inlined.
}
```

### 2. constexpr 
## 🧠 The `constexpr` Keyword and `inline` Implication in C++


| Feature | Applies To | Linkage Implication & Rule | Solution for Headers |
| :--- | :--- | :--- | :--- |
| **`constexpr` Function** | Function Definitions | **Implicitly `inline`**. This means the function can be defined in headers and included in multiple translation units without causing multiple definition errors at link time. The compiler may insert the code at call sites for optimization. | **No action required.** The `inline` behavior is automatic, you do not need to explicitly add the `inline` keyword. |
| **`constexpr` Variable** | Variable Definitions | **NOT implicitly `inline`**. If you define a `constexpr` variable in a header and include it in multiple translation units, the linker will find multiple definitions and cause an error. | You **must explicitly mark it as `inline constexpr`** (since C++17) to guarantee that only one instance of the variable exists across all translation units. |

```cpp 
//❎ wrong
constexpr std::string t = "this wont work";
// ✅ correct 
constexpr std::string_view what = "this works";
```
---

## 7. Loops

```cpp
// for
for (int i = 0; i < 5; i++) cout << i;

// while
int i = 0;
while (i < 5) cout << i++;

// do-while
int j = 0;
do { cout << j++; } while (j < 5);

// range-based for
int arr[] = {1, 2, 3};
for (int x : arr) cout << x;
```

---

## 8. Break / Continue

```cpp
for (int i = 0; i < 10; i++) {
  if (i == 5) break;
  if (i % 2 == 0) continue;
  cout << i;
}
```

---

## 9. Libraries

```cpp
#include <iostream>
#include <cmath>
#include <string>
#include <vector>
#include <algorithm>
#include <typeinfo>
```

---

## static 

```cpp 
// A static variable in a function
// persists between function calls.
void func() {
  static int counter = 0;
  counter++;
}
// Static class members exist
// independently of any instance.
class MyClass {
  static int counter;
  static void method ();
};
// Static variables and functions can only
// be accessed from the cpp file which
// they are defined in.
static int value;
static void helper();
```
---

## 10. Common Functions

```cpp
sizeof(arr);   // bytes
strlen(str);   // string length (C-style)
sqrt(25); pow(2, 3); floor(2.9); ceil(2.1);
sort(arr, arr+n); reverse(arr, arr+n);
```

---

## 11. Arrays

```cpp
int arr[3] = {1, 2, 3};
cout << arr[0];
```

---

## 12. Memory Addressing & Pointers

```cpp
int a = 5;
cout << &a;          // address
int* p = &a;         // pointer to int
cout << *p;          // dereference
int* p2 = nullptr;   // safe null ptr
```

---

## 13. References

```cpp
int a = 10;
int& ref = a; // alias
ref = 20;     // modifies a
```

---

## interface 

```cpp 
class MyInterface {
public:
    virtual void func1() = 0;
    virtual void func2() = 0;
    virtual void func3() = 0;
    virtual ~MyInterface() {}
} ;
```

--- 

## 14. Recursion

```cpp
int fact(int n) {
  if (n <= 1) return 1;
  return n * fact(n - 1);
}
```

---

## 15. Struct

```cpp
struct Point {
  int x, y;
};
Point p = {1, 2};
```

---

## 16. Enum

```cpp
enum Color { RED, GREEN, BLUE };
Color c = GREEN;
```

---

## 17. Class Basics

```cpp
class Box {
public:
  int w;
  Box() { w = 0; }       // default constructor
  Box(int x) { w = x; }  // overloaded
};

// Getter/Setter
class Box2 {
  int w;
public:
  int get() { return w; }
  void set(int x) { w = x; }
};
```

---

## 18. Inheritance & Polymorphism

```cpp
class A { public: void speak() {} };
class B : public A { public: void walk() {} };

class Base {
public:
  virtual void show() { cout << "Base"; }
};
class Derived : public Base {
  void show() override { cout << "Derived"; }
};
```

---

## 19. Function Overloading / Default Args

```cpp
int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }

void greet(string name = "User") {
  cout << "Hello " << name;
}
```

---

## 20. Inline & Function Pointers

```cpp
inline int square(int x) { return x * x; }

int add(int a, int b) { return a + b; }
int (*funcPtr)(int, int) = add;
```

---

## 21. Dynamic Memory

```cpp
int* arr = new int[10];
delete[] arr;
```

---

## 22. Exception Handling

```cpp
try {
  throw runtime_error("Oops");
} catch (exception& e) {
  cout << e.what();
}
```

---

## 23. Templates (Intro)

```cpp
template <typename T>
T add(T a, T b) {
  return a + b;
}
```

---

## 24. Lambda Expressions (C++11+)

```cpp
auto square = [](int x) { return x * x; };
```

---

## 25. STL Containers (Quick Glance)

```cpp
#include <vector>
vector<int> v = {1, 2, 3};
v.push_back(4);

#include <map>
map<string, int> m;
m["age"] = 25;
```

---

## 26. Data Types Summary

### Fundamental

* `int`, `float`, `double`, `char`, `bool`
* `long`, `long long`, `unsigned`

### Modifiers

* `const`, `static`, `volatile`, `mutable`

### Fixed-Width (C++11+)

```cpp
#include <cstdint>
int8_t a; uint32_t b;
```

---

## 27. Misc

```cpp
// Type Info
#include <typeinfo>
int a = 5;
cout << typeid(a).name();

// auto
auto x = 42; // inferred type

// Literals
42, 0x2A, 052, 42u, 3.14f

// Overflow
unsigned char val = 255;
val += 1; // wraps to 0
```

---

## 28. Summary for OSCP / Exploit Dev

| Use Case               | Type                 |
| ---------------------- | -------------------- |
| Byte-level payload     | `uint8_t`, `char`    |
| Port numbers / offsets | `unsigned short`     |
| Shellcode length       | `const size_t`       |
| Integer overflow bugs  | `int`, `unsigned`    |
| Memory address ops     | `void*`, `uintptr_t` |

---

## 29. Random Function

```cpp
#include <iostream>
#include <random>    //random (best)
int main(){
    std::cout << RAND_MAX << "\n";    //shows maximum number limit for rand
    std::cout >> rand() << "\n";  //random but provides the same so not good

    srand(time(nullptr));
    std::cout << rand() << "\n";   //random but based on time seed so vulnerable af 

    //using random library 
    std::random_device rd;  // a random device is created
    std::uniform_int_distribution<int> dist(x,y); // creates random value b/w x and y
    std::uniform_real_distribution<double> dist(x,y) //float distribution
    std::cout << dist(rd) << "\n"; // print it out

    std:: random_device dev;
    std: :mt19937 rng(dev));
    std:: uniform_int_distribution<
       std::mt19937::result_type > dist(x, y);
    int num = dist(rng);
}

```
--- 

## Stanard Library
### to_underlying
### move
### shared_pointer
### unique_pointer
### refernece_wrapper 
### void
### monostate 
### pair
### deque
### variant 
### visit
### toupper tolower 
### towupper towlower
### stoi stol stoll stof stod stold 
### map 
### set 
### value_cast (rvalue prvalue glvalue lvalue rvalue)
### unordered_set 
### unordered_map 
### addressof
### to_address
### list 
### vector 
### remove 
### empty
### lock_guard
### scoped_lock
### thread 
### function 
### filesystem
### jthread 
### copyable_function
### expected
### optional
### promise
### spam



## deducing this 
## RAII 
## CRTP
## header (ODR and DRY)
## friend
## compiler support portability
## libraries static and dynamic 
## meta build system 
## build system
## dependency
## macros 
## string manipulation
## free functions
## lambda
## Initialization
## Sequential Generation
## Filtering
## Slicing
## Reduction
## Flattening
## Method Chaining
## Set Operations
## abstraction
## ranges
## hashmap
## async
## UI for cpp or c#
## templates
## template metaprogramming  and SFINAE
## compile time programming
## constexpr consteval constinit
## cpp concepts features
## serialisation
## networking
## cryptography
## enums
## garbage value initialisation
## classes Inheritance Polymorphism destructors this overide specifiers 
## safe cpp code writing
## clean cpp code writing
## constructor
## call site reference 
## operator overloading
## file managementa
## other file accessing ABI
## new, delete
## ownership and move semantics
## rvalue glvalues prvalues
## move semantics (algorithm and std)
## cherno, cppcon, jason turner, low level learning
