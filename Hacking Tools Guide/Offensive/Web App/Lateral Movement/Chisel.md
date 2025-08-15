# chisel

**Type:** TCP/UDP Tunnel / Port Forwarding Tool
**Focus:** Bypassing firewalls, pivoting, and reverse tunnels

---

## 1. Full Feature Overview

* Fast TCP/UDP tunnel over HTTP, HTTPS, or WebSockets
* Works as client-server with minimal setup
* Supports port forwarding and remote connections
* Can be used for internal network pivoting
* Cross-platform: Linux, Windows, macOS
* Encrypted communication using TLS or SSH-like methods
* Supports dynamic port mapping and multiplexed connections

---

## 2. Installation & Setup

### Download Precompiled Binaries

* GitHub releases: [https://github.com/jpillora/chisel/releases](https://github.com/jpillora/chisel/releases)

```bash
# Example for Linux
wget https://github.com/jpillora/chisel/releases/download/1.8.1/chisel_1.8.1_linux_amd64.gz
gunzip chisel_1.8.1_linux_amd64.gz
chmod +x chisel_1.8.1_linux_amd64
```

### Build from Source

```bash
git clone https://github.com/jpillora/chisel.git
cd chisel
go build
```

---

## 3. Core Usage

### 3.1 Start Chisel Server

```bash
# Listen on port 8000 and allow client forwarding
./chisel server -p 8000 --reverse
```

### 3.2 Connect as Client

```bash
# Connect to server and forward remote port 3389 to local 3389
./chisel client SERVER_IP:8000 R:3389:localhost:3389
```

### 3.3 Dynamic Port Forwarding

```bash
# Forward all local ports dynamically
./chisel client SERVER_IP:8000 R:1080:socks
```

---

## 4. Tips, Tricks, Best Practices

* Always use `--reverse` for pivoting into internal networks
* Combine with Netcat or SMB tools for lateral movement
* Use TLS mode (`--tls`) for encrypted traffic to bypass detection
* Monitor connections with verbose mode: `-v`
* Useful in C2 setups for stealthy communication

---

## 5. Cheat Sheet

```text
# Start server
./chisel server -p 8000 --reverse

# Client connect with reverse port forwarding
./chisel client SERVER_IP:8000 R:3389:localhost:3389

# Dynamic SOCKS proxy
./chisel client SERVER_IP:8000 R:1080:socks

# Encrypted connection
./chisel client SERVER_IP:8000 --tls R:3389:localhost:3389

# Verbose output
./chisel client SERVER_IP:8000 -v R:3389:localhost:3389
```

---
