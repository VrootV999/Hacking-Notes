## What we'll be covering in this page

  

1. • Basics of networking
2. • Understand sub-netting

  

  

## Basics of IP Address and MAC Address

### IP Address

An **IP address** (Internet Protocol address) is a numerical label assigned to each device connected to a computer network that uses the Internet Protocol for communication. There are two types of IP addresses: IPv4 and IPv6. Here we will focus on **IPv4**

  

### IPv4 Address

**IPv4** (Internet Protocol version 4) is the most common form of IP addressing.

- **Bits**: 32 bits
- **Octets**: 4 octets (8 bits each)
- **Decimal Representation**: Written as four decimal numbers separated by dots (e.g., `192.168.1.1`)
- **Range**: Each octet can have a value between 0 and 255
- **Total Addresses**: 2^32 addresses (~4.3 billion)

  

### Characteristics of IPv4:

1. **Structure**: 32-bit address split into four 8-bit octets.
2. **Decimal Representation**: Four numbers separated by dots (e.g., `192.168.0.1`).
3. **Network and Host Parts**:
    - **Network Part**: Identifies the network.
    - **Host Part**: Identifies the specific device (host) within the network. In IP address of 193.168.0.1 in subnet mask of 255.255.255.0  
        i) network part: 192.168.0  
        ii) host part: .1  
        
4. **Classes**: IP addresses are categorized into Classes A, B, C, D, and E for different purposes (e.g., Class A for large networks, Class C for small networks).

  

### IPv4 Address Classes

  

|                                                      |                                                                |                                                              |                                                          |
| ---------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------- |
| Classes  | IP starting range | IP ending range | Subnet mask |
| A         | 1.0.0.0                                                        | 126.255.255.255                                              | 255.0.0.0                                                |
| B         | 128.0.0.0                                                      | 191.255.0.0                                                  | 255.0.0.0                                                |
| C         | 192.168.0.0                                                    | 223.255.255.0                                                | 255.255.255.0                                            |
| D         | 224.0.0.0                                                      | 239.255.255.255                                              | -                                                        |
| E         | 240.0.0.0                                                      | 255.255.255.255                                              | -                                                        |
| LocalHost | 127.0.0.0                                                      | 127.255.255.255                                              | loopback addr                                            |

  

### IPv6 Address

**IPv6** is designed to solve IPv4 exhaustion.

- **Bits**: 128 bits
- **Hexadecimal**: 8 groups of 4 hex digits (e.g., `2001:0db8::7334`)
- **Total Addresses**: 2^128 (virtually limitless)

### Parts of IPv6 Address:

1. **Global Routing Prefix**: Network identifier.
2. **Subnet ID**: Specific subnet identifier.
3. **Interface ID**: Unique device identifier.

  

### MAC Address

- **Bits**: 48 bits
- **Bytes**: 6 bytes
- **Hexadecimal Representation**: 12 hex digits (e.g., `00:1A:2B:3C:4D:5E`)

### Parts of MAC Address:

1. **OUI (Organizationally Unique Identifier)**: First 3 bytes (manufacturer-specific).
2. **Device ID**: Last 3 bytes (unique to each device).

  

## Conversion: Decimal to Binary and Binary to Decimal

### Decimal to Binary

1. Divide by 2 and record the remainders.
2. Read the binary number from bottom to top.

**Example**:

Decimal `10` → Binary `1010`

### Binary to Decimal

1. Multiply each binary digit by 2 raised to its position.
2. Sum the results.

**Example**:

Binary `1010` → Decimal `10`

  

### The IPv4 Address Exhaustion Problem (1999)  
  

By the late 1990s, it became evident that IPv4’s 32-bit address space (about 4.3 billion addresses) would soon be exhausted due to the explosive growth of the internet. This posed the risk of running out of available IP addresses, threatening global internet expansion.  
  
SOLUTION:  

**NAT : Network Address Translation**  
**IPv6 : Internet Protocol version 6 **
  
  

> [!important]  
> NAT was the reason that we have Private and Public IP addresses  

  

### Private IP Range

|                                                   |                                                     |                                                         |
| ------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------- |
| Classes | IP range | Subnet Mask |
| A    | 10.0.0.0 - 10.255.255.255                           | 255.0.0.0                                               |
| B    | 172.0.0.0 - 172.31.255.255                          | 255.255.0.0                                             |
| C    | 192.168.0.0 - 192.168.255.255                       | 255.255.255.0                                           |

  

### Types of NAT:

1. **Static NAT**
    - Maps one private IP address to one public IP address.
    - Used when a device inside the network must be accessible from outside using the same IP.
2. **Dynamic NAT**
    - Maps a pool of public IP addresses to a group of private IP addresses.
    - IPs are assigned on a first-come, first-served basis.
3. **Overloading (PAT)**
    - Also called **Port Address Translation** (PAT).
    - Maps multiple private IP addresses to a single public IP address by using different port numbers.
    - Most common form of NAT, often used in home networks.
