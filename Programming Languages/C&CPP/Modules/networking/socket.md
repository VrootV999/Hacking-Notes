# socket.h

## **Key Concepts**:

1. **Sockets**: A socket is an endpoint for communication between two machines over a network. It acts as an abstraction that allows applications to send/receive data to/from another application over the internet.

2. **Socket Types**:

   * **SOCK\_STREAM**: A **TCP** socket (connection-oriented).
   * **SOCK\_DGRAM**: A **UDP** socket (connectionless).
   * **SOCK\_RAW**: A raw socket, often used for **packet sniffing** or **manipulating low-level IP packets**.

3. **Address Families**:

   * **AF\_INET**: IPv4 addresses.
   * **AF\_INET6**: IPv6 addresses.
   * **AF\_UNIX**: Local communication using file system paths (used for inter-process communication).

---

## **Important Functions and How They Work**:

#### **1. `socket()`**

* **Purpose**: Creates a socket and returns a file descriptor that can be used with other socket-related functions.

  * **Syntax**:

    ```c
    int socket(int domain, int type, int protocol);
    ```

    **Parameters**:

    * `domain`: Specifies the address family (e.g., `AF_INET` for IPv4, `AF_UNIX` for local communication).
    * `type`: Specifies the socket type (e.g., `SOCK_STREAM` for TCP, `SOCK_DGRAM` for UDP).
    * `protocol`: Specifies the protocol (usually `0`, letting the system choose the default for the socket type).

  * **Example**: Create a TCP socket:

    ```c
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd == -1) {
        perror("socket creation failed");
    }
    ```

  * **Use Case**: The `socket()` function is the starting point for almost all network-related functionality in C. It creates a network interface (socket) that other functions will interact with for sending/receiving data.

---

## **2. `bind()`**

* **Purpose**: Binds a socket to a specific local address and port number. This is typically done by a **server** before it starts listening for incoming connections.

  * **Syntax**:

    ```c
    int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    ```

    **Parameters**:

    * `sockfd`: The socket file descriptor created using `socket()`.
    * `addr`: A pointer to a `struct sockaddr_in` (IPv4) or `struct sockaddr_in6` (IPv6) that specifies the local address and port to bind.
    * `addrlen`: The size of the address structure.

  * **Example**: Bind a socket to `127.0.0.1:8080`:

    ```c
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = htonl(INADDR_ANY);  // Use local IP
    server_addr.sin_port = htons(8080);  // Bind to port 8080

    if (bind(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("bind failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    ```

  * **Use Case**: Binding is typically used by a **server** to associate the socket with a local address and port. **Attackers** can use `bind()` to set up a **bind shell**, where the victim machine listens for an incoming connection from the attacker.

---

## **3. `listen()`**

* **Purpose**: Places the socket into **listening mode**, enabling it to accept incoming connections. This is typically used by **servers** that are awaiting incoming client connections.

  * **Syntax**:

    ```c
    int listen(int sockfd, int backlog);
    ```

    **Parameters**:

    * `sockfd`: The socket descriptor created by `socket()`.
    * `backlog`: The maximum length of the queue for pending connections. If the queue is full, incoming connections are refused until the queue has space.

  * **Example**: Listen on a socket for incoming connections:

    ```c
    if (listen(sockfd, 5) == -1) {
        perror("listen failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    ```

  * **Use Case**: After binding a socket, `listen()` is called to start accepting incoming client connections. This is often used in **server-side applications**. In penetration testing, you can use this to set up a **reverse shell** or **listener** waiting for a connection from an exploited target.

---

## **4. `accept()`**

* **Purpose**: Accepts an incoming connection request from a client and returns a new socket for communication with that client.

  * **Syntax**:

    ```c
    int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
    ```

    **Parameters**:

    * `sockfd`: The listening socket descriptor, returned by `socket()` and `bind()`.
    * `addr`: A pointer to a `struct sockaddr_in` structure that will be filled with the address information of the connecting client.
    * `addrlen`: A pointer to the size of the address structure.

  * **Example**: Accept a connection from a client:

    ```c
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    int new_sock = accept(sockfd, (struct sockaddr *)&client_addr, &client_len);
    if (new_sock == -1) {
        perror("accept failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    ```

  * **Use Case**: `accept()` is used by servers to **accept client connections**. For example, in a **reverse shell**, this can be used by the attacker to accept a connection back from the compromised victim machine. This will establish the communication channel.

---

## **5. `connect()`**

* **Purpose**: Establishes a connection to a remote server (client-side). This is typically used by **clients** to connect to a server.

  * **Syntax**:

    ```c
    int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
    ```

    **Parameters**:

    * `sockfd`: The socket descriptor.
    * `addr`: The address structure of the server you want to connect to (e.g., `struct sockaddr_in`).
    * `addrlen`: The length of the address structure.

  * **Example**: Connect to a remote server:

    ```c
    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(8080);  // Remote server port
    inet_pton(AF_INET, "192.168.1.1", &server_addr.sin_addr);  // IP of the remote server

    if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("connect failed");
        close(sockfd);
        exit(EXIT_FAILURE);
    }
    ```

  * **Use Case**: `connect()` is used in **client-side** applications to establish a connection with a remote server. Attackers use it to set up **reverse shells**, where the victim connects back to the attacker’s machine for remote access.

---

## **6. `send()` and `recv()`**

* **Purpose**: Used to send and receive data over a socket.

  * **Syntax**:

    * `send()`:

      ```c
      ssize_t send(int sockfd, const void *buf, size_t len, int flags);
      ```

    * `recv()`:

      ```c
      ssize_t recv(int sockfd, void *buf, size_t len, int flags);
      ```

    **Parameters**:

    * `sockfd`: The socket descriptor.
    * `buf`: The buffer to send or receive data.
    * `len`: The length of the data to send or receive.
    * `flags`: Usually set to `0`. For more advanced use, flags like `MSG_DONTWAIT` can be used.

  * **Example**: Send and receive data over a socket:

    ```c
    char buffer[1024];
    strcpy(buffer, "Hello, World!");
    send(sockfd, buffer, strlen(buffer), 0);

    int bytes_received = recv(sockfd, buffer, sizeof(buffer), 0);
    buffer[bytes_received] = '\0';
    printf("Received: %s\n", buffer);
    ```

  * **Use Case**: These functions are fundamental for communication over a socket. Attackers can use `send()` and `recv()` to send payloads, execute commands on a victim machine, or transfer data during **data exfiltration** or **reverse shell** exploitation.

---

## **7. `close()`**

* **Purpose**
    -  Closes a socket, releasing the associated resources.

* **Syntax**:

  ```c
  int close(int sockfd);
  ```

  **Parameters**:

  * `sockfd`: The socket descriptor to be closed.

* **Example**: Close the socket:

  ```c
  close(sockfd);
  ```

* **Use Case**: After completing communication, sockets must be closed to **release system resources**. This is used in the cleanup phase of network-related exploits or tools.

---

# **Advanced Uses in Penetration Testing and Red Teaming**

1. **Reverse Shell**:

   * **Exploit Setup**: Use a **reverse shell** where the victim runs a program that **connects back** to an attacker’s machine using `connect()`, and `accept()` is used on the attacker’s side.

2. **Port Scanning**:

   * Use **`socket()`**, **`connect()`**, and **`recv()`** to build your own **port scanner**, trying to establish connections to different ports on a target and detect open ports.

3. **Denial of Service**:

   * Use **`send()`** and **`recv()`** with **spoofed IP addresses** to send **UDP floods** or **TCP SYN floods** for **DoS attacks**.

4. **Packet Crafting**:

   * Use **`raw sockets (SOCK_RAW)`** to **craft custom IP packets**. This is useful for **network reconnaissance**, **spoofing**, and **infiltrating firewalls**.

---
