# ligolo-ng

**Type:** TCP/UDP Tunnel / Network Pivoting Tool
**Focus:** Internal network access, firewall bypass, port forwarding

---

## 1. Full Feature Overview

* Reverse TCP/UDP tunneling for internal network access
* Works as client-server like Chisel
* Cross-platform: Windows, Linux
* Supports encrypted communication
* Enables lateral movement and pivoting within target networks
* Handles multiple concurrent tunnels
* Minimal footprint for stealthy operations

---

## 2. Installation & Setup

### Requirements

* Go 1.18+
* Git

### Installation

```bash
# Clone repository
git clone https://github.com/IgorKamil/ligolo-ng.git
cd ligolo-ng

# Build server and client
go build ./cmd/ligolo-server
go build ./cmd/ligolo-client
```

* Alternatively, download precompiled binaries from GitHub releases

---

## 3. Core Usage

### 3.1 Start Ligolo Server

```bash
# Listen on port 443 with TLS
./ligolo-server -listen 0.0.0.0:443 -tls-cert cert.pem -tls-key key.pem
```

### 3.2 Connect Client

```bash
# Connect client to server with reverse tunnel
./ligolo-client -server SERVER_IP:443 -tls -reverse -lport 3389 -rhost 10.0.0.5 -rport 3389
```

### 3.3 Multi-Port Forwarding

```bash
./ligolo-client -server SERVER_IP:443 -tls -reverse -lport 3389,445 -rhost 10.0.0.5 -rport 3389,445
```

---

## 4. Tips, Tricks, Best Practices

* Use TLS mode for encrypted traffic to evade network detection
* Combine with Netcat, SMB tools, or RDP for internal pivoting
* Run server on public IP and client inside target network
* Use multi-port forwarding for simultaneous service access
* Monitor tunnels using verbose mode: `-v`

---

## 5. Cheat Sheet

```text
# Start server with TLS
./ligolo-server -listen 0.0.0.0:443 -tls-cert cert.pem -tls-key key.pem

# Connect client with reverse tunnel
./ligolo-client -server SERVER_IP:443 -tls -reverse -lport 3389 -rhost 10.0.0.5 -rport 3389

# Forward multiple ports
./ligolo-client -server SERVER_IP:443 -tls -reverse -lport 3389,445 -rhost 10.0.0.5 -rport 3389,445

# Enable verbose logging
-v
```

---
