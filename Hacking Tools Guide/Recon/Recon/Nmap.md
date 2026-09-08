
### Exclude
--exclude (ips)                          excludes the ip's u say
--excludefile  (ips)                       exclude targets with file

### scan types

-sU                                                  UDP scan
-sV                                                  Version detection
-sS                                                 Stealth scan (SYN scan)
-sT                                                  Connect scan
-sA                                                 TCP ACK scan
-sX                                                 TCP xmas scan 
-sN                                                 TCP NULL scan
-sF                                                  TCP  FIN scan
-6                                                    ipv6 scan

### Raw Packets

--send-eth                                      raw ethernet packets
--send-ip                                        raw IP packets

### Additional scan types

-O                                                    OS detection
-A                                                    Aggressive scan (includes -O and -sV)

### Forensics

-D                                                    Decoy scan
--spoof-mac                                    MAC address spoofing

### Firewall obstruction

-f                                                    augment packets
-sI                                                  zombie scan
--badsum                                        send badsum
--source-port (p)                 use a non configured port on victims firewall
--data-length  (size)                    append random data


### Additional TCP scans

-Pn                                                  don't ping
-sP                                                  ping only TCP scan
-PS                                                 TCP syn request
-PA                                                 TCP ack request 

-PU                                                 UDP ping
-PE                                                  ICMP echo ping
-PP                                                  ICMP timestamp ping
-PO                                                 IP protocol ping
-PM                                                CMP Address Mask Ping
### Information on scan

-traceroute                                     trace the route of the packet being sent
-R                                                  reverse DNS resolution

### Ports

--top-ports (N)                             Scan top N ports
-p (p)                                      Specify port(s) to scan
-p-                                         All ports

### Level

-T                                          level of scan 
-v                                                    verbose output

### Output

-ox                                                  output file

### Script

--script-updatedb                           update script DB
--script vuln                                    find vulnerability in the scan
--script (scripts)                           runs specific script that you asked
--script-args                                    runs specific arguments in the script

### Example:

nmap -sS -sV  -sU -sT -Pn -O -A -D RND:10 -ox (file) --spoof-mac 00:11:22:33:44:55 192.168.1.0/24 

### Decoy IP and MAC

#### IP
-D RND:(number)
-D ip1,ip2,ip3,ip3,ip4,ip5,ip6,ME

#### MAC-address
--spoof-mac 0
--spoof-mac (mac-addr)


### With forensic knowledge
nmap -sV -D RND:10 --spoof-mac 0 --data-length 2 --source-port 10 [IP]/[netmask]

nmap -sI D RND:10 --spoof-mac 0 --data-length 2 --source-port 10 [ip]/[netmask]



