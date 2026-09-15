# ARP Protocol Basics
- Address Resolution Protocol(ARP) is used for discovery of mac addresses in the network.
- To communicate with a device we need to know the mac-address of the device which is within the network and for that we'd send an ARP packet to discover the mac addresses.
- Request (who has xxx.xxx.xxx.xxx Tell xx:xx:xx:xx:xx:xx)
```wireshark
Address Resolution Protocol (request)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: request (1)
    Sender MAC address: NetlinkIct_83:21:b9 (8c:13:e2:xx:xx:xx)
    Sender IP address: 192.168.1.1
    Target MAC address: 00:00:00_00:00:00 (00:00:00:00:00:00)
    Target IP address: 192.168.1.3
```
- Reply (xxx.xxx.xxx.xxx is at yy:yy:yy:yy:yy:yy)
```wireshark
Address Resolution Protocol (reply)
    Hardware type: Ethernet (1)
    Protocol type: IPv4 (0x0800)
    Hardware size: 6
    Protocol size: 4
    Opcode: reply (2)
    Sender MAC address: Intel_f7:5f:d0 (dc:1b:a1:xx:xx:xx)
    Sender IP address: 192.168.1.3
    Target MAC address: NetlinkIct_83:21:b9 (8c:13:e2:yy:yy:yy)
    Target IP address: 192.168.1.1
```

- The device stores all the mac addresses of the devices in a table called as the `ARP table`
- To look at the stored `ARP table` you can do. `arp -a` in `mac/windows/linux` or also use `ip neigh` in linux.

---
# MiTM Explained
- MiTM is the act of Being in the middle of a connection and tapping into it to get everything being communicated.
- We can do MiTM in various ways which includes `ARP Spoofing`, `DNS Spoofing/Cache Poisoning`, `Evil Twin/Rogue Access Point`, `ICMP Redirect`, `DHCP Spoofing`
    - `ARP Spoofing`: Its the act of pretending to be the router and sending fake arp messages to link their own MAC address with another devices's IP address usually the router. which then fools the victim device thinking the attacker is the router now and then start sending packets to us and now the attacker forwards it to the router. so he can listen to all the packets.
    - `DNS Spoofing/Cache Poisoning`: The attacker manipulates Domain Name System records (either on a local network or via compromised DNS servers) to redirect a user's traffic from a legitimate website to a malicious, attacker-controlled replica.
    - `Evil Twin/Rogue Access Point`: An attacker sets up a fraudulent Wi-Fi hotspot mimicking a legitimate network (like a public cafe or corporate guest network). When victims connect, all their wireless traffic routes directly through the attacker's device.
    - `ICMP Redirect`: The attacker sends forged Internet Control Message Protocol (ICMP) redirect messages to a target host, tricking the device into updating its routing table and sending traffic through the attacker's machine instead of the real gateway.
    - `DHCP Spoofing`: An attacker deploys a rogue DHCP server on a local network to hand out malicious configuration settings to clients—such as assigning a fake IP address for the default gateway or a malicious DNS server.

---
