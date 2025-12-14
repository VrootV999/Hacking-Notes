# C and CPP
### 1. **Integer Types**

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

### 2. **Floating-Point Types**

| Type          | Description                                             | Size (bytes) | Range                                |
| ------------- | ------------------------------------------------------- | ------------ | ------------------------------------ |
| `float`       | Single precision floating-point (32-bit)                | 4            | 1.5 × 10^−45 to 3.4 × 10^38          |
| `double`      | Double precision floating-point (64-bit)                | 8            | 5.0 × 10^−324 to 1.7 × 10^308        |
| `long double` | Extended precision floating-point (depends on platform) | 8, 12, or 16 | Varies (typically 80-bit or 128-bit) |
| `float32_t`   | Fixed-width single precision float (32-bit)             | 4            | Same as `float`                      |
| `float64_t`   | Fixed-width double precision float (64-bit)             | 8            | Same as `double`                     |

### 3. **Character Types**

| Type            | Description                  | Size (bytes) |
| --------------- | ---------------------------- | ------------ |
| `char`          | A single character           | 1            |
| `signed char`   | Signed single character      | 1            |
| `unsigned char` | Unsigned single character    | 1            |
| `wchar_t`       | Wide character (for Unicode) | 2 or 4       |
| `char16_t`      | UTF-16 character (C++11)     | 2            |
| `char32_t`      | UTF-32 character (C++11)     | 4            |

### 4. **Pointer Types**

| Type      | Description                         | Size (bytes)                   |
| --------- | ----------------------------------- | ------------------------------ |
| `void*`   | Void pointer (generic pointer type) | 8 (on 64-bit) or 4 (on 32-bit) |
| `char*`   | Pointer to a `char`                 | 8 (on 64-bit) or 4 (on 32-bit) |
| `int*`    | Pointer to an `int`                 | 8 (on 64-bit) or 4 (on 32-bit) |
| `float*`  | Pointer to a `float`                | 8 (on 64-bit) or 4 (on 32-bit) |
| `double*` | Pointer to a `double`               | 8 (on 64-bit) or 4 (on 32-bit) |
| `long*`   | Pointer to a `long`                 | 8 (on 64-bit) or 4 (on 32-bit) |

### 5. **Size and Memory Management Types**

| Type        | Description                                               | Size (bytes)                   |
| ----------- | --------------------------------------------------------- | ------------------------------ |
| `size_t`    | Typically used for memory sizes and array indices         | 8 (on 64-bit) or 4 (on 32-bit) |
| `ssize_t`   | Signed version of `size_t` (used in certain OS libraries) | 8 (on 64-bit) or 4 (on 32-bit) |
| `ptrdiff_t` | Difference between two pointers                           | 8 (on 64-bit) or 4 (on 32-bit) |

### 6. **Other Types**

| Type        | Description                                | Size (bytes)                   |
| ----------- | ------------------------------------------ | ------------------------------ |
| `bool`      | Boolean (true/false, typically 1 byte)     | 1                              |
| `nullptr_t` | Represents the `nullptr` constant in C++11 | 8 (on 64-bit) or 4 (on 32-bit) |

---

### Summary of Common Sizes on 64-bit Systems

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

