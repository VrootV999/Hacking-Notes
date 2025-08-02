# What we’ll be covering in this page

1. • Networking in detail
2. • TCP/IP and OSI models
3. • Network topologies and architectures
4. • Networking devices, its protocols and everything about it

  

  

  

# Types of Devices in a Network

## Network Devices

- **Network adapter**: NIC for device communication
- **Hub**: Network repeater
- **Switch**: Uses MAC addresses for data routing
- **Router**: Uses MAC and IP for traffic routing
- **Modem**: Translates signals between ends
- **Firewall**: Network security guard
- **Bridge**: Connects separate networks

  

# Terminal (End-Devices)

A terminal is an electronic or electromechanical device used to input and output data from a computer or a computer system.
- **Client**: Requests services
- **Server**: Provides services
### Types of Terminals:

- **Dumb Terminal:** Simple input/output device with no processing capabilities.
- **Intelligent Terminal:** Has some processing power and memory for local data manipulation.
- **Specialized Terminal:** Designed for specific tasks like point-of-sale systems.
- **Smart Terminal:** Advanced terminals with significant local processing power.

### Terminal Functions:

- Data input and output
- User interface for computer systems
- Remote access to centralized computing resources

Protocols used: Telnet, SSH, RDP

# Network Adapter

Also known as a Network Interface Card (NIC), a network adapter enables a device to connect to a network.

### Types:

- Ethernet adapters
- Wireless adapters (Wi-Fi)
- Fiber optic adapters

### Connection Interfaces:

- PCI
- PCIe
- USB
- Integrated (on-board)

Used in: computers, servers, IoT devices

Protocols used: Ethernet, Wi-Fi (802.11), TCP/IP

# Hub

A hub is a basic networking device that connects multiple devices in a local area network (LAN).

### Types:

- **Active Hub:** Amplifies incoming signals before broadcasting.
- **Passive Hub:** Simply splits the signal without amplification.

Hubs are not commonly used today because they broadcast data to all connected devices, creating unnecessary network traffic.

How it works: Receives data on one port and transmits it to all other ports.

Protocols used: Ethernet

# Bridges

A bridge is a network device that connects and filters traffic between two network segments.

### Types:

- Transparent Bridge
- Source Routing Bridge
- Source Routing Transparent Bridge
- Translational Bridge
- Remote Bridge
- Wireless Bridge

Protocols used: Spanning Tree Protocol (STP), Ethernet

# Switch

A switch is an intelligent networking device that connects multiple devices in a LAN and uses MAC addresses to forward data to the correct destination.

### Types:

- **Managed Switch:** Offers advanced configuration options and monitoring capabilities.
- **Unmanaged Switch:** Simple plug-and-play device with no configuration options.

### Features:

- VLAN support
- Quality of Service (QoS)
- Port mirroring
- Link aggregation

Protocols used: Ethernet, Spanning Tree Protocol (STP), VLAN Trunking Protocol (VTP)

# Router

A router is a networking device that forwards data packets between computer networks, using IP addresses to determine the best path for data transmission.

### Features:

- Network Address Translation (NAT)
- Firewall capabilities
- DHCP server
- VPN support

### Types:

- Wired routers
- Wireless routers
- Core routers
- Edge routers
- Virtual routers

Protocols used: IP, OSPF, BGP, RIP, EIGRP

  

# Network Topologies

Network topology refers to the arrangement of nodes and connections in a network. Here are some common types:

## Star Topology

- **Connection:** All nodes connect to a central hub or switch
- **Security****: Relatively secure as traffic passes through the central point
- **Pros****:Easy to install and manage, fault isolation
- **Cons**: Dependent on central hub; if it fails, the entire network fails

## Bus Topology

- **Connection**: All devices connect to a single cable (the bus)
- **Security**:Less secure as all data travels on the same line
- **Pros**:Easy to install, requires less cable
- **Cons**:Limited bandwidth, vulnerable to heavy traffic

## Ring Topology

- **Connection**: Devices connect in a closed loop
- **Security**: Moderately secure, data passes through each node
- **Pros**: Equal access for all devices, performs well under heavy load
- **Cons**:*Failure of one device can affect the entire network

## Mesh Topology

- **Connection**:Each device connects to every other device
- **Security**:Highly secure due to multiple paths
- **Pros**: Highly reliable, no single point of failure
- **Cons**: Complex to set up, requires more resources

## Tree Topology

- **Connection**: Hierarchical structure with a root node and child nodes
- **Security**: Security can be implemented at different levels
- **Pros**: Scalable, easy to manage
- **Cons**: Dependent on root node, can be costly

## Hybrid Topology

- **Connection**:Combination of two or more topologies
- **Security**: Varies based on the combined topologies
- **Pros**: Flexible, can be optimized for specific needs
- **Cons**: Can be complex to manage and troubleshoot

  

# Network Area Types

## PAN (Personal Area Network)

Smallest network for personal devices.

- **Examples:** Bluetooth, infrared
- **Range:** Up to 10m

## LAN (Local Area Network)

Connects devices in limited area.

- **Examples:** Office, home Wi-Fi
- **Range:** Up to 1km

## CAN (Campus Area Network)

Connects multiple LANs in limited area.

- **Examples:** Universities, corporate campuses
- **Range:** Up to 5km

## MAN (Metropolitan Area Network)

Covers larger areas than LANs.

- **Examples:** City-wide networks
- **Range:** Up to 50km

## WAN (Wide Area Network)

Connects networks over large distances.

- **Examples:** Internet, global corporate networks
- **Range:** Global

## GAN (Global Area Network)

Uses satellites for worldwide coverage.

- **Examples:** Satellite phones, GPS
- **Range:** Worldwide

These classifications show network scale from personal to global systems.

  

# Network Models

Network models provide a framework for understanding how data is transmitted across networks. Here's a table comparing two primary models: OSI and TCP/IP.

# TCP/IP Model

|                                                            |                                                        |                                                                 |
| ---------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------- |
| Layer         | Data Unit | Specialized Device |
| 4. Application | Segment                                                | (-)                                                             |
| 3. Transport     | Packets                                                | Router                                                          |
| 2. Network      | Frames                                                 | Switch                                                          |
| 1. Physical    | Bit                                                    | Hub,NIC                                                         |

# OSI Model

|                                                            |                                                        |                                                                 |
| ---------------------------------------------------------- | ------------------------------------------------------ | --------------------------------------------------------------- |
| Layer         | Data Unit | Specialized Device |
| 7. Application | Data                                                   | Gateway                                                         |
| 6. Presentation  | Data                                                   | -                                                               |
| 5. Session      | Data                                                   | -                                                               |
| 4. Transport   | Segment                                                | -                                                               |
| 3. Network    | Packet                                                 | Router                                                          |
| 2. Data Link   | Frame                                                  | Switch, Bridge                                                  |
| 1. Physical    | Bit                                                    | Hub, Repeater, Network Interface Card (NIC), Cables             |

  

# Data Transfer in the OSI Model

## Encapsulation and Decapsulation

The OSI model uses encapsulation and decapsulation to transfer data between devices:

### Encapsulation (Sender's Side):

- Data starts at the Application layer (Note: TCP-Segments UDP - Datagram)
- Each layer adds its own header (and sometimes trailer) to the data
- The data unit is passed down through each layer
- At the Physical layer, data is converted to bits for transmission

### Header in layer 4

The header in Layer 4 (Transport Layer) contains information for managing data transmission:

- **Source Port**: Identifies the sending application or process
- **Destination Port**: Specifies the receiving application or process
- **Sequence Number**: Helps in ordering and reassembling data segments
- **Acknowledgement Number**: Indicates the next expected sequence number
- **Flags**: Control bits for connection management (e.g., SYN, ACK, FIN)
- **Checksum**: Used for error detection in the segment

These components ensure reliable, ordered, and error-checked delivery of data between applications on different hosts.

  

### Header in layer 1

The Ethernet frame consists of the following headers:

- Preamble: Synchronizes the receiver's clock (7 bytes)
- Start Frame Delimiter (SFD): Marks the start of the frame (1 byte)
- Destination MAC Address: Identifies the recipient device (6 bytes)
- Source MAC Address: Identifies the sending device (6 bytes)
- EtherType: Indicates the protocol of the payload (2 bytes)
- Payload: Contains the actual data being transmitted (46-1500 bytes) 0x0600 (IPv4,IPv6,ARP)== 0x05Pc (IEEE 802__)
- Frame Check Sequence (FCS): Detects transmission errors (4 bytes)

### Decapsulation (Receiver's Side):

- Bits are received at the Physical layer
- Each layer removes its header (and trailer) from the data unit
- The process continues up through the layers
- The original data reaches the Application layer

## Three-Way Handshake

The three-way handshake is used to establish a reliable connection in TCP:

### Procedure:

1. SYN: Client sends a SYN (synchronize) packet to the server
2. SYN-ACK: Server responds with a SYN-ACK (synchronize-acknowledge) packet
3. ACK: Client sends an ACK (acknowledge) packet to the server

After these steps, a reliable connection is established for data transfer.

## Address Resolution Protocol (ARP)

ARP is used to map IP addresses to MAC addresses in a local network:

### ARP Request:

- Device broadcasts an ARP request to all devices on the local network
- The request contains the target IP address

### ARP Reply:

- The device with the matching IP address sends an ARP reply
- The reply contains the device's MAC address

### ARP Cache:

- Devices maintain an ARP cache to store recent IP-to-MAC mappings
- This reduces the need for frequent ARP requests
- Entries in the ARP cache typically expire after a set time

Understanding these processes is crucial for comprehending how data moves through networks efficiently and securely.

  

> [!important]  
> Note that Source: youno change in ip or mac address when it goes through otehr devices except arp requestRouter: Routing table ARP table NAT tableSwitch: CAM table ARP tableDNS server: DNS cache  

  

# PROTOCOLS

  
  

### **Ethernet**

- **IEEE 802.3**: Standard for Ethernet wired networking.
- **Ethernet Frame Format**: Defines how data is organized and transmitted on Ethernet networks.
- **ARP (Address Resolution Protocol)**: Resolves IP addresses to MAC addresses.
- **STP (Spanning Tree Protocol)**: Prevents loops in a network with redundant paths.
- **LLDP (Link Layer Discovery Protocol)**: Device discovery protocol for identifying neighboring devices.

  

### **VLAN (Virtual LAN)**

- **IEEE 802.1Q**: Standard for VLAN tagging.
- **VTP (VLAN Trunking Protocol)**: Manages the addition, deletion, and renaming of VLANs across a network.
- **PTP (Precision Time Protocol)**: Synchronizes clocks in a VLAN network.
- **GVRP (GARP VLAN Registration Protocol)**: Registers VLANs dynamically across devices.
- **MVRP (Multiple VLAN Registration Protocol)**: Automates VLAN configuration across multiple devices.
- **IEEE 802.1ad (QinQ)**: Allows multiple VLANs to be encapsulated in a single VLAN.
- **PvLAN (Private VLAN)**: Provides isolation between devices within the same VLAN.
- **PPP (Point-to-Point Protocol)**: Encapsulation protocol for point-to-point connections.
- **HDLC (High-Level Data Link Control)**: Protocol for data encapsulation on point-to-point links.

  

### **DHCP (Dynamic Host Configuration Protocol)**

- **RFC 2131**: Defines the DHCP standard for dynamic IP assignment.
- **DHCPv4**: Protocol for assigning IPv4 addresses dynamically.
- **DHCPv6**: Protocol for assigning IPv6 addresses dynamically.
- **User Datagram Protocol (UDP)**: DHCP messages are encapsulated in UDP packets in port 68,67
- **BOOTP (Bootstrap Protocol)**: Predecessor to DHCP, used for bootstrapping network devices.
- **PXE (Preboot Execution Environment)**: Allows devices to boot from a network server.
- I**P (Internet Protocol)**: Core protocol for addressing and routing data.
- **CDP (Cisco Discovery Protocol)**: Cisco devices to discover and share information about other
- **DTP (Dynamic Trunking Protocol**): used to negotiate trunking on a link between cisco switches
- **HSRP (Hot Standby Router Protocol)**: for redundancy by adding routers into a virtual router.
- **MPLS (Multiprotocol Label Switching)**: RIP but for Cisco switches find short rout to enhance.

### **Router**

- **IP (Internet Protocol)**: Core protocol for addressing and routing data.
- **BGP (Border Gateway Protocol)**: Routes data between different autonomous systems on the internet.
- **OSPF (Open Shortest Path First)**: Finds the shortest path in large networks.
- **EIGRP (Enhanced Interior Gateway Routing Protocol)**: Cisco’s distance-vector routing protocol.
- **ICMP (Internet Control Message Protocol)**: Sends error and diagnostic messages.
- **RIP (Routing Information Protocol)**: Distance-vector routing protocol.
- **IS-IS (Intermediate System to Intermediate System)**: Link-state routing protocol for large networks.

  

### **Switch**

- **IEEE 802.1D (STP)**: Prevents loops in network topologies.
- **IEEE 802.1Q**: Used for VLAN tagging.
- **LLDP (Link Layer Discovery Protocol)**: Discovers directly connected devices.
- **RSTP (Rapid Spanning Tree Protocol)**: Faster version of STP to prevent network loops.

---

### **Hub**

- **IEEE 802.3**: Protocol used by legacy hubs for Ethernet communication.
- **CSMA/CD**: Manages collisions on shared Ethernet networks.

  

### **Wi-Fi (Wireless Fidelity)**

- **IEEE 802.11a**: 5 GHz Wi-Fi standard.
- **IEEE 802.11b**: 2.4 GHz Wi-Fi standard.
- **IEEE 802.11g**: 2.4 GHz, higher-speed Wi-Fi.
- **IEEE 802.11h**: Dynamic frequency selection (DFS) and power control for 5 GHz.
- **IEEE 802.11n**: 2.4 and 5 GHz Wi-Fi with MIMO (multiple-input, multiple-output).
- **IEEE 802.11ac**: 5 GHz, faster throughput and wider channels.
- **IEEE 802.11ax (Wi-Fi 6)**: Improved performance in dense environments.
- **IEEE 802.11l**: Secure link-layer mobility support.
- **IEEE 802.11r**: Fast BSS (Basic Service Set) transition, improving handoff times.
- **IEEE 802.11k**: Optimizes the selection of access points.
- **IEEE 802.11v**: Network management for wireless clients.
- **IEEE 802.11w**: Management frame protection, enhancing Wi-Fi security.
- **WPA2/WPA3 (Wi-Fi Protected Access)**: Security protocols for encrypting wireless traffic.

  

### **LAN (Local Area Network)**

- **IEEE 802.3 (Ethernet)**: For wired LAN communication.
- **IEEE 802.11 (Wi-Fi)**: For wireless LAN communication.
- **ARP (Address Resolution Protocol)**: Resolves IP addresses to MAC addresses.

  

### **WLAN (Wireless LAN)**

- **IEEE 802.11**: Wireless LAN communication standard.
- RADIUS: remote authentication; dial in user service
- **WPA2/WPA3**: For encrypting and securing wireless traffic.
- **EAP (Extensible Authentication Protocol)**: Authentication framework in wireless networks.

i) **EAP-TLS (Transport Layer Security)**:Utilizes client and server digital certificates for strong auth

ii) **EAP-TTLS (Tunneled Transport Layer Security)**: createtunnelwithacertificatetoalowlegacyauth

iii) **EAP-PEAP (Protected Extensible Authentication Protocol)**: Encapsulate EAP w/ tls certificate

iv) **EAP-FAST (Flexible Authentication via Secure Tunneling): secure tunnel by pac**

v) **EAP-GTC (Generic Token Card): uses a challenge or OTP for cred based auth**

vi) **EAP-PSK (Pre-Shared Key): uses pre shared key for auth without need of RADIUS**

vii) **EAP-SIM (Subscriber Identity Module)**: auth using SIM-Card

viii) **EAP-AKA (Authentication and Key Agreement)**: uses UMTS but with key generation and auth

# **Cloud Service**

- **SaaS (Software as a Service)**: Delivers software over the internet without local installation.
- **PaaS (Platform as a Service)**: Provides cloud-based platforms for developers to build applications.
- **IaaS (Infrastructure as a Service)**: Provides virtualized computing resources over the internet.
- **HTTP/HTTPS**: Secure communication for cloud-based web services.
- **REST**: Architectural style for interacting with web services.
- **SOAP**: Messaging protocol used in web services.

  

> [!important]  
> NOTE:  IEEE 802.11 consist only a,b,g,n,ac,ax

# **KUBERNETES**

- Kubernetes provides a way to automate the deployment, scaling, and operations of application containers across clusters of hosts. It supports various containerization technologies like Docker and containerd
- **Cluster**: A set of nodes (physical or virtual machines) that run containerized applications.
- **Node**: A single machine (either physical or virtual) in a Kubernetes cluster, running containerized applications.
- **Pod**: The smallest unit in Kubernetes, a pod is a group of one or more containers that share storage and network resources.
- **container**: A self-contained environment that runs a specific application or service.

### How is Kubernetes Used?

Kubernetes is used to manage containerized applications in production environments. It can be deployed on a variety of cloud providers (AWS, GCP, Azure) or on-premises data centers. Here’s how it's typically used:

1. **Container Orchestration**: Automates the management of containers, ensuring that the right number of containers (pods) are running.
2. **Scaling**: Automatically scales applications based on demand, scaling up and down the number of pods.
3. **Service Discovery & Load Balancing**: Exposes applications as services and provides load balancing across them.
4. **Self-Healing**: Automatically restarts containers that fail or become unresponsive.
5. **Rolling Updates**: Allows for zero-downtime updates of applications.
6. **Declarative Configuration**: Configuration is typically specified using YAML or JSON files, allowing the application to be defined and deployed with consistency.
7. **Resource Management**: Provides resource quotas and limits, ensuring that workloads don’t consume more resources than allocated.

### Vulnerabilities to be exploited in Kubernetes 

- **Misconfiguration**: like
					- open API server
					- Insecure RBAC
					- insecure Authentication Server
					- Lack of Network policies
			**CVE-2020-8554 (Kubernetes API Server Vulnerability)**
			**CVE-2018-1002105 (Kubernetes Privilege Escalation)**
			**CVE-2020-8555 (Docker Container Privilege Escalation)**
			**CVE-2019-11247 (Kubernetes Insecure Kubelet)**
- secrets file in Kubernetes contains the API key or the json key and could be used for privilege escalation

### **How People Use Kubernetes**:

1. **Deploying Applications**:
    
    - Developers package their applications into containers and then create **Kubernetes manifests** (YAML files) that describe how the containers should be deployed. These manifests define pods, deployments, services, and other resources in the cluster.
2. **Scaling and Managing**:
    
    - Kubernetes automatically manages scaling (adding or removing pods), load balancing, and self-healing of applications.
3. **Hosting Kubernetes on Cloud**:
    
    - Kubernetes clusters can be deployed on cloud platforms like AWS, Google Cloud, or Azure. These cloud providers offer managed Kubernetes services (e.g., **EKS** for AWS, **GKE** for Google Cloud, **AKS** for Azure) that handle the complexity of setting up and maintaining Kubernetes clusters.
    - Alternatively, Kubernetes can also be hosted on private data centers using platforms like **Minikube** (for local testing) or **Rancher**.
4. **Public Access**:
    
    - If you want to make your Kubernetes-hosted application public, you can expose it through a **LoadBalancer service** or an **Ingress controller**, which routes traffic to the appropriate pods running your application.

# **Docker**

- Docker is an open-source platform for automating the deployment, scaling, and management of applications inside containers.
#### **Key Concepts of Docker**:

1. **Container**:
    
    - A container is a lightweight, stand-alone, and executable package that includes everything needed to run a piece of software (code, runtime, libraries, etc.). Containers are isolated from each other and from the host system, but they share the same OS kernel.
2. **Image**:
    
    - A Docker image is a snapshot or blueprint of a container. It contains everything needed to run an application, including code, dependencies, and environment configurations. Images are used to create containers.
3. **Dockerfile**:
    
    - A Dockerfile is a text document that contains instructions to build a Docker image. It defines how the image will be created, which software to install, and how to configure it.
4. **Docker Engine**:
    
    - The Docker Engine is the runtime that builds and runs containers. It includes a daemon process (the Docker service) that manages containers and images.
5. **Docker Hub**:
    
    - Docker Hub is a cloud-based registry for storing and sharing Docker images. It’s like an app store for Docker images where developers can upload and share pre-built images or download publicly available ones.

#### **How Docker Works**:

1. **Building the Image**:
    
    - A developer creates a **Dockerfile** which defines how the application should be built (e.g., which base OS to use, what software to install, etc.).
    - The Docker Engine reads the Dockerfile and creates a **Docker image**.
2. **Running a Container**:
    
    - Once the image is built, the developer uses the Docker Engine to **run a container** based on the image. This container is a running instance of the image and can interact with other containers or the host system.
3. **Uploading and Sharing**:
    
    - After building a Docker image, developers can upload it to **Docker Hub** or a private registry, where it can be shared with others. Other developers can then pull the image from the registry and run it locally.

### **Vulnerabilities in Docker**:
- Misconfigured RBAC: 
- Insecure API  server:
- Exposing Services:

# **Containerd** 

- it’s responsible for the lifecycle of containers, such as image transfer and storage, container execution and supervision, and managing container-related tasks. It doesn't provide all the features of Docker (like building images or advanced networking), but instead focuses on running containers at scale.
- **Container Runtime**:
    
    - **containerd** is a container runtime, meaning it is responsible for pulling container images from registries, running containers, and managing their lifecycle. It is the underlying engine that interfaces with the OS-level features to create, start, stop, and delete containers.
- **Image**:
    
    - Like Docker, containerd uses container images to define the environment and application inside the container. Images are pulled from a container registry and run as containers.
- **Tasks**:
    
    - In containerd, **tasks** refer to containers that are actively running. The containerd engine manages the lifecycle of these tasks, such as creating, starting, stopping, and killing containers.
- **Namespaces**:
    
    - containerd supports **namespaces**, which allow you to isolate container runtimes on the same host, providing a way to have separate container environments for different users or systems.
- **Plugins**:
    
    - containerd is highly modular and supports plugins for features like networking, storage, and container runtime support. Kubernetes and other orchestrators use plugins to integrate containerd into their systems.
- **Containerd Daemon**:
    
    - containerd runs as a background service (daemon), which interacts with the operating system and manages container resources like CPU, memory, and network access. The daemon listens for container management requests, whether from a local CLI, an orchestration platform, or a container orchestrator like Kubernetes.

# Nutshell of K8 , Docker , Containerd

### Containerd
- **Pulling images** from a registry (e.g., Docker Hub).
- **Creating containers** from those images.
- **Running containers** and managing their resource usage (like CPU, memory, etc.).
- **Stopping, starting, and deleting containers**.
- **Managing container logs**.

### Docker
- **Building container images** (`docker build`).
- **Container networking** (making containers communicate with each other).
- **Volume management** (storing persistent data across container restarts).
- **Container orchestration at a basic level** (e.g., Docker Compose).

### K8
- **Scheduling**: Deciding which node should run which container based on the available resources (CPU, memory, disk, etc.).
- **Scaling**: Automatically adding or removing container instances (pods) depending on traffic or load.
- **Failover/Health**: Ensuring containers are running and automatically restarting containers or re-scheduling them if they fail.

