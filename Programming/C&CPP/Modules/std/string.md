# **8. `string.h` (String Handling Library)**

The **`string.h`** library provides a set of functions for manipulating **C strings** (null-terminated character arrays). String manipulation is a critical skill for **pen testers** and **red teamers**, as improper handling of strings can lead to **buffer overflows**, **format string vulnerabilities**, and other serious security issues. Furthermore, attackers can use `string.h` functions for **password cracking**, **input validation bypass**, and **data exfiltration**.

---

### **Key Functions and Concepts in `string.h`**

1. **`strlen()`**

   * **Purpose**: Returns the length of a string (not including the null-terminating character).
   * **Common Use**: Checking the size of user inputs to avoid buffer overflows or **format string vulnerabilities**.
   * **Example**:

     ```c
     char *str = "Hello, world!";
     size_t len = strlen(str);
     ```

2. **`strcmp()`**

   * **Purpose**: Compares two strings lexicographically.
   * **Common Use**: Checking user inputs or comparing sensitive data like passwords. This function is vulnerable to **timing attacks** if not used correctly.
   * **Example**:

     ```c
     if (strcmp(user_input, "password123") == 0) {
         // Password is correct
     }
     ```

3. **`strncmp()`**

   * **Purpose**: Compares the first `n` characters of two strings.
   * **Common Use**: Useful for comparing part of a string or validating fixed-length input.
   * **Example**:

     ```c
     if (strncmp(user_input, "admin", 5) == 0) {
         // User is an admin
     }
     ```

4. **`strcpy()`**

   * **Purpose**: Copies a null-terminated string from the source to the destination.
   * **Common Use**: Vulnerable to **buffer overflow** attacks if the destination buffer is not large enough.
   * **Example**:

     ```c
     char dest[20];
     strcpy(dest, "This is a long string");
     ```

5. **`strncpy()`**

   * **Purpose**: Copies the first `n` characters from the source to the destination.
   * **Common Use**: Safer version of `strcpy()`, but still requires careful buffer size management.
   * **Example**:

     ```c
     char dest[10];
     strncpy(dest, "Short", sizeof(dest)-1);
     dest[sizeof(dest)-1] = '\0';  // Null-terminate
     ```

6. **`strcat()`**

   * **Purpose**: Concatenates (appends) one string to the end of another.
   * **Common Use**: Often vulnerable to **buffer overflow** if the destination buffer isn’t large enough.
   * **Example**:

     ```c
     char dest[20] = "Hello, ";
     strcat(dest, "world!");
     ```

7. **`strncat()`**

   * **Purpose**: Appends the first `n` characters of one string to another.
   * **Common Use**: Safer version of `strcat()`, but still needs careful management of buffer sizes.
   * **Example**:

     ```c
     char dest[20] = "Hello, ";
     strncat(dest, "world!", sizeof(dest)-strlen(dest)-1);
     ```

8. **`memcpy()`**

   * **Purpose**: Copies a block of memory from one location to another.
   * **Common Use**: Used for copying **raw data** from one buffer to another. This is often useful in **exploits** that involve manipulating memory.
   * **Example**:

     ```c
     char source[] = "Some data";
     char dest[20];
     memcpy(dest, source, strlen(source) + 1);
     ```

9. **`memmove()`**

   * **Purpose**: Moves a block of memory, ensuring that it handles overlapping memory regions correctly.
   * **Common Use**: Similar to `memcpy()`, but **safer** when the source and destination buffers overlap.
   * **Example**:

     ```c
     char buffer[20] = "Hello, world!";
     memmove(buffer + 7, buffer, strlen(buffer) + 1);
     ```

10. **`memset()`**

    * **Purpose**: Fills a block of memory with a specified value.
    * **Common Use**: Useful for **initializing buffers** or **zeroing memory**. It can also be used to **overwrite sensitive data** in memory.
    * **Example**:

      ```c
      char buffer[20];
      memset(buffer, 0, sizeof(buffer));  // Zero out the buffer
      ```

11. **`strchr()`**

    * **Purpose**: Finds the first occurrence of a character in a string.
    * **Common Use**: Searching for delimiters or specific characters within strings (e.g., to find a password delimiter).
    * **Example**:

      ```c
      char *str = "Hello, world!";
      char *ptr = strchr(str, ',');  // Finds the first comma
      ```

12. **`strrchr()`**

    * **Purpose**: Finds the last occurrence of a character in a string.
    * **Common Use**: Searching for a character from the **end of the string**, often useful for **file path manipulation** or **URL parsing**.
    * **Example**:

      ```c
      char *str = "/home/user/file.txt";
      char *ptr = strrchr(str, '/');  // Finds the last '/'
      ```

13. **`strstr()`**

    * **Purpose**: Finds the first occurrence of a substring in a string.
    * **Common Use**: Searching for specific substrings within data, often used for **data parsing** and **information gathering**.
    * **Example**:

      ```c
      char *str = "admin:password123";
      char *ptr = strstr(str, "admin");  // Finds the substring "admin"
      ```

14. **`strtok()`**

    * **Purpose**: Splits a string into tokens based on delimiters.
    * **Common Use**: Useful for parsing structured data (e.g., CSV files, URLs, etc.) or for **command parsing**.
    * **Example**:

      ```c
      char str[] = "apple,banana,cherry";
      char *token = strtok(str, ",");
      while (token != NULL) {
          printf("%s\n", token);
          token = strtok(NULL, ",");
      }
      ```

---

### **Advanced Use Cases for `string.h` in Penetration Testing & Red Teaming**

#### **1. Buffer Overflow Vulnerabilities**

**Objective**: Exploit `strcpy()` and other unsafe functions to overwrite memory.

##### **Technique**:

* Functions like `strcpy()`, `strcat()`, and `sprintf()` are dangerous when used with unvalidated user inputs, making them a common vector for **buffer overflow attacks**.

```c
char buffer[100];
strcpy(buffer, user_input);  // If user_input is larger than 100 bytes, it will overflow.
```

* **Real-World Use Case**: An attacker might provide input longer than the allocated buffer, causing **stack corruption** and allowing **code injection**.

---

#### **2. Format String Vulnerabilities**

**Objective**: Use **format string bugs** to manipulate memory or **read sensitive data**.

##### **Technique**:

* Misusing `printf()` or `sprintf()` with user-controlled format specifiers can lead to **information leakage** or **arbitrary code execution**.

```c
printf(user_input);  // Vulnerable to format string exploit
```

* **Real-World Use Case**: An attacker could use `%x` or `%n` to **leak memory** or overwrite important variables.

---

#### **3. Exploiting Null-Termination and String Handling**

**Objective**: Craft inputs that manipulate string handling and cause vulnerabilities.

##### **Technique**:

* An attacker may exploit **null terminator manipulation** to bypass input validation or control the execution flow of a program. In particular, **null byte injection** is useful for **bypassing filters** or **truncating strings** in certain operations.

```c
strcpy(dest, "Hello\x00World");
```

* **Real-World Use Case**: The null byte `\x00` can be injected into inputs to manipulate how strings are processed, allowing attackers to **bypass input validation** or **control program behavior**.

---

#### **4. Tokenization and Command Injection**

**Objective**: Use `strtok()` to break up a command and inject **malicious payloads**.

##### **Technique**:

* An attacker can use **string tokenization** to inject commands or break down inputs into malicious tokens for execution.

```c
char command[256];
strtok(user_input, " ");  // Split input and inject a shell command
```

* **Real-World Use Case**: By splitting user input into tokens, an attacker might exploit **improper handling of user input** to inject malicious commands.

---

