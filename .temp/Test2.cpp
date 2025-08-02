#include <iostream>
#include <cstdint>      // for fixed-width types
#include <typeinfo>     // for type introspection
#include <cstring>      // for memory ops

using namespace std;

int main() {
    // Fundamental types and their typical sizes and ranges
    bool flag = true;                       // 1 byte: true (1) or false (0)
    char letter = 'A';                      // 1 byte: signed -128 to 127
    unsigned char uLetter = 255;            // 1 byte: unsigned 0 to 255

    short s = -32768;                       // 2 bytes: -32k to 32k
    unsigned short us = 65535;              // 2 bytes: 0 to 65k

    int i = 2147483647;                     // 4 bytes: -2B to +2B
    unsigned int ui = 4294967295;           // 4 bytes: 0 to 4.2B

    long l = 2147483647;                    // 4 or 8 bytes (platform-specific)
    long long ll = 9223372036854775807LL;   // 8 bytes: huge range

    float f = 3.14159f;                     // 4 bytes: ~7 digits precision
    double d = 9.81;                        // 8 bytes: ~15 digits precision
    long double ld = 1.6180339887L;         // 10-16 bytes: extended precision

    // Const modifier (read-only after initialization)
    const int BUFFER_SIZE = 512;
    // BUFFER_SIZE = 1024; // ❌ will throw error if uncommented

    // Overflow test
    unsigned char val = 255;
    val += 1; // wraps to 0 (unsigned overflow)
    cout << "Unsigned char overflow: " << (int)val << endl;

    // Type info at runtime
    cout << "Type of ll: " << typeid(ll).name() << endl;

    // Fixed-width types (from <cstdint>) — ideal for exploits
    int8_t  i8 = -128;              // exact 1 byte
    uint8_t u8 = 255;
    int16_t i16 = -32000;
    uint16_t u16 = 65000;
    int32_t i32 = -2147483648;
    uint32_t u32 = 4294967295;
    int64_t i64 = -9223372036854775807LL;
    uint64_t u64 = 18446744073709551615ULL;

    // Sizeof operator (in bytes)
    cout << "sizeof(int) = " << sizeof(int) << endl;
    cout << "sizeof(uint64_t) = " << sizeof(uint64_t) << endl;

    // Auto keyword (type inference)
    auto port = 8080;              // inferred as int
    auto ip = "127.0.0.1";         // inferred as const char*

    // Void pointer (generic address)
    void* ptr = malloc(64);
    cout << "Void pointer address: " << ptr << endl;
    free(ptr);

    return 0;
}

// Void return type (used in non-returning functions)
void scanNetwork() {
    cout << "Scanning..." << endl;
}

