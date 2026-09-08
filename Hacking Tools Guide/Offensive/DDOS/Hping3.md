A low level Dos tool

## Basic
-c (count)                           Number of packets to send
-S                                          SYN packets
-p (port)                             Target port
-a (spoof)                           Spoof source address 
    --spoof                         same as a
-i (time in ms)                    time interval in milliseconds
    --fast                                    -i u10000 (10 packets for second) 
    --faster                                 -i u1000 (100 packets for second) 
    --flood                                  fast af
-q                                         quiet
-V                                         verbose mode
-D                                         Debug info
-t                                           ttl 
	 --ttl                              same as t


## MODE
default mode                                                        TCP
-0                       --rawip                                        RAW IP
-1                       --icmp                                        ICMP mode
-2                       --udp                                          UDP mode
-8                        --scan                                        SCAN mode
-9                       --listen                                        listen mode
## Example:
hping3 -S -p 80 -c 1000 192.168.1.10
