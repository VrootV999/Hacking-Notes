
# Scapy

## 2. Overview
- Scapy is a powerful Python-based interactive packet manipulation tool and library.
- Used for packet crafting, sniffing, decoding, injection, and network discovery.
- Extremely useful for pentesters and red teamers for custom network scanning, protocol fuzzing, MITM attacks, and more.
- Supports a wide range of protocols (Ethernet, IP, TCP, UDP, ICMP, DNS, ARP, etc.).
- Runs on Linux, macOS, and Windows (some features Windows-limited).

--- 

## Core Concept

| Concept         | Description                                         |
| --------------- | --------------------------------------------------- |
| Packets         | Composed of layers (Ethernet/IP/TCP/UDP/etc.)       |
| Layers          | Protocol layers stacked (layer 2, 3, 4, etc.)       |
| Fields          | Attributes of each layer (e.g., IP.src, TCP.dport)  |
| Packet crafting | Creating custom packets by layering protocols       |
| Sniffing        | Capturing packets from network interface            |
| Sending         | Injecting crafted packets into the network          |
| Dissection      | Parsing raw packet data into layers and fields      |
| Fuzzing         | Sending malformed packets to test protocol handling |
| Sessions        | Keeping track of conversations (TCP/UDP flows)      |

## 4. Basic use
### 4.1 Craft & send a packet
```python
from scapy.all import *

pkt = IP(dst="192.168.1.1")/ICMP()
send(pkt)
```
4.2 Sniff packets (simple capture)

packets = sniff(count=10)
packets.summary()

4.3 Show packet details

pkt.show()

4.4 Layer access & modification

print(pkt[IP].src)
pkt[IP].ttl = 128

4.5 Sending packets & receiving replies

ans, unans = sr(IP(dst="8.8.8.8")/ICMP())
ans.summary()

5. Advanced Packet Crafting
5.1 Custom TCP SYN scan

for port in range(20, 25):
    pkt = IP(dst="192.168.1.1")/TCP(dport=port, flags='S')
    resp = sr1(pkt, timeout=1, verbose=0)
    if resp and resp.haslayer(TCP) and resp.getlayer(TCP).flags == 0x12:
        print(f"Port {port} is open")

5.2 ARP Spoofing (MITM) Example

def arp_spoof(target_ip, spoof_ip):
    pkt = ARP(op=2, pdst=target_ip, hwdst=getmacbyip(target_ip), psrc=spoof_ip)
    send(pkt, verbose=0)

5.3 DNS Query Packet

dns_req = IP(dst="8.8.8.8")/UDP(dport=53)/DNS(rd=1,qd=DNSQR(qname="example.com"))
resp = sr1(dns_req, timeout=2)
resp.show()

6. Sniffing & Network Monitoring
6.1 Filter packets live (capture HTTP only)

sniff(filter="tcp port 80", prn=lambda x: x.summary(), count=20)

6.2 Save captured packets to file

pkts = sniff(count=50)
wrpcap("capture.pcap", pkts)

6.3 Read packets from pcap file

pkts = rdpcap("capture.pcap")
pkts[0].show()

7. Sessions & Stateful Analysis

sessions = sniff(session=TCPSession)
for sess, pkt_list in sessions.sessions().items():
    print(f"Session: {sess}")
    for pkt in pkt_list:
        pkt.summary()

8. Fuzzing & Protocol Testing

from scapy.layers.dns import DNS, DNSQR

fuzzed_pkt = IP(dst="8.8.8.8")/UDP(dport=53)/fuzz(DNS(rd=1, qd=DNSQR(qname="example.com")))
send(fuzzed_pkt)

    Useful to find protocol parsing bugs, DoS weaknesses, or exploit vulnerabilities in network devices.
