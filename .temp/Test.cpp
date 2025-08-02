// Topic 1: namespace
// Namespaces avoid naming conflicts
#include <iostream>

namespace tools {
    void greet() {
        std::cout << "Hello from tools!" << std::endl;
    }
}

using std::endl;
using namespace std;
int main() {
    tools::greet(); // Access using namespace
    return 0;
}

// Topic 2: typedef
// Used to create aliases for existing types
typedef unsigned int uint;
uint id = 5;

// Topic 3: type aliases
// Modern replacement for typedef
using ushort = unsigned short;
ushort port = 80;

// Topic 4: type conversion
// Implicit and explicit conversion
int a = 10;
double b = (double)a; // explicit

// Topic 5: switch
int x = 2;
switch (x) {
    case 1: std::cout << "One"; break;
    case 2: std::cout << "Two"; break;
    default: std::cout << "Other";
}

// Topic 6: if, else, else if
if (x == 1) {
    std::cout << "One";
} else if (x == 2) {
    std::cout << "Two";
} else {
    std::cout << "Other";
}

// Topic 7: switch for strings (not native)
// Use if-else or map<string, func> instead

// Topic 8: ternary operator
int y = (x == 2) ? 100 : 0;

// Topic 9: loops
for (int i = 0; i < 3; i++) std::cout << i;
while (x--) std::cout << x;
do { x++; } while (x < 3);

// Topic 10: libraries
#include <iostream> // cout, cin
#include <vector>   // vectors
#include <string>   // strings

// Topic 11: break, continue
for (int i = 0; i < 5; i++) {
    if (i == 2) continue;
    if (i == 4) break;
    std::cout << i;
}

// Topic 12: return
int square(int n) {
    return n * n;
}

// Topic 13: array
int arr[3] = {1, 2, 3};
std::cout << arr[0];

// Topic 14: common functions
sizeof(arr); // size in bytes

// Topic 15: cmath
#include <cmath>
sqrt(9); pow(2, 3); sin(0);

// Topic 16: foreach (range-based for loop)
for (int val : arr) {
    std::cout << val;
}

// Topic 17: array functions - manual in C++
#include <algorithm>
std::sort(arr, arr + 3);

// Topic 18: memory address
int z = 5;
std::cout << &z; // prints address

// Topic 19: pointers
int *ptr = &z; // points to z
std::cout << *ptr; // dereference

// Topic 20: nullptr
ptr = nullptr; // safe null pointer

// Topic 21: recursion
int fact(int n) {
    if (n <= 1) return 1;
    return n * fact(n - 1);
}

// Topic 22: struct
struct Host {
    std::string ip;
    int port;
};
Host h = {"127.0.0.1", 80};

// Topic 23: enum
enum State { OFF, ON };
State power = ON;

// Topic 24: constructor & overloading
class Shell {
public:
    Shell() {}              // default
    Shell(std::string n) { name = n; }
    std::string name;
};

// Topic 25: getter & setter
class Port {
    int p;
public:
    void set(int val) { p = val; }
    int get() { return p; }
};

// Topic 26: inheritance
class Exploit {
public:
    void run() { std::cout << "Running..."; }
};
class BufferOverflow : public Exploit {};

// Topic 27: polymorphism
class Base {
public:
    virtual void speak() { std::cout << "Base"; }
};
class Derived : public Base {
public:
    void speak() override { std::cout << "Derived"; }
};

Base* obj = new Derived();
obj->speak(); // prints "Derived"

// END - condensed C++ essentials for OSCP
// Fast, useful, and powerful C++ patterns for exploit dev

