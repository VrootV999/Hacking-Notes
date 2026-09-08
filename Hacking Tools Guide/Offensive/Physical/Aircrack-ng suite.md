
## Airmon-ng

airmon-ng start (interface)
airmon-ng stop (interface)
airmon-ng check kill

## Airodump-ng

#### Syntax
--bssid            MAC-ADDR of the Router
-c                    Channel of the Router
-w                   output file
-d                   Bssid of the interface

#### EX
airodump-ng (interface) -d (bssid)
airodump-ng (interface) --bssid (bssid) -c (channel) -w (file)

## Aireplay-ng

--deauth         Deauth attack
-a                   BSSID
-c                   MAC-ADDR of the devices connected in the network

-0    Deauth attack
-1   Fake Auth attack
-3   Arp replay attack

#### EX
aireplay-ng -0  -a (bssid) (interface)
aireplay-ng -1  -a (bssid) (interface)
aireplay-ng -3  -a (bssid) (interface)

