Cars use something known as SDR which is commonly used in our phones and routers like 
- 2.4 Ghz   for   WIFI
- 5 Ghz      for 5G
- Bluetooth
and much more and our cars use these to receive a certain frequency and the car will open.

all key manufacturers use a password in order to protect the car like it is a set of numbers and it is most likely the same password used in all the time to lock and unlock but sometimes better ones use a method where every time when it locks or unlock it updates the password by a certain number and the car and the key increment/decrement by that value.    (Rolling Code)

# Things you need
- Flipper Zero  (portable)
- Phone (must be rooted)
- Laptop (use a RTL/SDR, monitoring software, HackRF one , signal amplifier)
  
# Key Frequency
-  USA and Japan     315  Mhz
-  Europe                   433.9 Mhz
- remember that all the devices that transmit some frequency should be Registered with FCC so find the FCC id from the device and you basically find the frequency range it is operation.
# Stratergies

## Replay attack
- recieve and then send it
## Rolling code Hacking
- simple yet a bit complex to pull off
- jam the first click and capture it.
- capture the second click.  
- determine the algorithm and then do a replay attack
## Signal Jamming
- signals never receive and car never locks and we can use it to open it.
- can be useful if the person didn't care about the sound and you jammed it leaving it open.
- can be used in cars at the year of 2014 and 2020 like Honda or even old luxury cars.
-  basically a Dos and can be called Gaussian signal which is throwing random garbage         signal to block the signal
  
  
  
# Tutorial on this will be coming soon and also tools guide on it. the Producer of this notes is broke and can't buy the tools. 

  
# Connecting to the Controler area network  
you need to connect to the car's control area network to get the car to open.

# Steps involved in CAN hacking
## Connecting to the car's CAN.
- it can be done by connecting your laptop to the port used in the car which is a diagnostic port known as ODB-II port 
## sniff packets that are required for igniting the engine
- sniff the certain packet which is sent for igniting the engine
## Reverse Engineer by sending the packet
- send the packet which is appropriate for starting the car.


# Can-utils
## 1. setup 
- ip link ls    (check if the interface is up)
- ip link set up can0 type can bitrate 500000
- ip link ls   (check if the interface is up)
## 2. monitor and sniff
- cansniffer -c "interface"
- shift + 3 + space + enter
- look at what changes colours and that is the one to change arbitary code.

