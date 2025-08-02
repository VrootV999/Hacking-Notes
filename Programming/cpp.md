# C++ Core Concepts Notes

**Purpose:** Quick re-learning and revisiting all core concepts of C++
**Style:** Short, precise, complete with syntax, explanation, and commented examples

---

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
