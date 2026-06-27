### Course Resources
- **Free E-Books:** github.com/utilsec/Getting_Started_with_ICS (IT Pros and OT Professionals versions)
- **Newsletter:** Guarding the Gears - Industrial Cyber Security Weekly (mikeholcomb.com)
- **Course Materials:** Review questions for each module, course slides

### ICS/OT Cyber Security Certifications
1. **ISA/IEC 62443 Series (Most Popular Route):**
   - Cybersecurity Fundamentals Specialist (entry-level)
   - Cybersecurity Risk Assessment Specialist
   - Cybersecurity Design Specialist (secure network design)
   - Cybersecurity Maintenance Specialist (operations & maintenance)
   - ISA/IEC 62443 Cybersecurity Expert (all four exams)
   - Cost: ~$1,600 per course/exam; ISA membership ($160/yr) gives ~20% discount
2. **SANS Courses:** GICSP, GRID, GCIP
3. **CompTIA SecOT+:** Newer vendor-neutral OT certification

### Mandatory Annual Reading
- **Dragos Year in Review** - ICS/OT threat activity report
- **Verizon Data Breach Investigations Report (DBIR)** - Comprehensive breach data

### ICS/OT Podcasts
- CS2AI Podcast Show, Control Loop, Industrial Security Podcast, Unsolicited Response, DarkNet Diaries

### ICS/OT Conferences
- S4 Conference, SANS ICS Summit, ICS Village (DEF CON), BSidesICS/OT

---
## Terminology and Meaning
- OT(Operational Technology) refers to hardware and software that control physical devices in industrial systems.
- OT is risky and requires you to get to the field and protect the environment physically and Technologically. OT is connected to IT nowadays for logistics and shipping managements to connect with the business. It is physically safe, there can be potential harm. There are few potential attack vectors when we connect our
- OT network to IT and The IT connected to the Internet. A better security Idea would be not allowing IT to talk with OT and only OT can send data to IT.
- ICS(industrial Control System) are large scale deployments as a subnets of OT in industrial environment.
- SCADA(Supervisory Control and Data Acquisition) often refer to control systems that communicate over multiple locations over wide area links.
- ICS is like how LAN works and SCADA is like how WAN works.
- Asset Owners: They refer to the parties that own the facility and responsible for the cyber security of the environment.
- Asset Operator: They refer to the people who are responsible for running the facility.(can be 3rd party too)
- Asset Owners can be operators but it is optional.
- Critical Infrastructure are defined by each countries government.
- In us There are 16 of Critical Infrastructure.
    - Chemical
    - Comercial Facility
    - Communication
    - Critical Manufacturing
    - Dams
    - Defense Industrial Base
    - Emergency Services
    - Energy
    - Financial Services
    - Food and Agriculture
    - Government Facilities
    - Healthcare and Public Health
    - Information Technology
    - Nuclear Reactor
    - Water and Wastewater system
    - Transporation System

---
## Attack Vector
- From the IT network(only when sending data to OT is available).
- Physically brought in by "transitory cyber assets"(connect directly to the OT)
- Control system exposed directly to the Internet
- remote access capabilities
- Malicious Insiders

---
## Critical Infrastructure Sectors

- Critical infrastructure is defined by each country's government; the definition and list varies by nation.
- In the U.S., there are **16 recognized critical infrastructure sectors** (with "Space" being considered as a 17th).
- These sectors are highly **interdependent** — failure in one cascades to others:
  - Chemical sector provides pesticides for Agriculture
  - Agriculture requires Water for irrigation and Energy to power pumps
  - Transportation moves fuel for Energy and goods for all sectors
  - Communications underpins IT, Emergency Services, and Financial Services
  - Healthcare depends on Energy, Water, and Transportation
- Societal impact: extended failure of these systems leads to breakdown of civilization.
- OT/ICS security is critical because most of these sectors rely on industrial control systems to operate.

### The 16 U.S. Critical Infrastructure Sectors
1. **Chemical** - Manufacturing, storage, and transport of chemicals
2. **Commercial Facilities** - Public venues, offices, entertainment
3. **Communications** - Telecommunications, internet, broadcasting
4. **Critical Manufacturing** - Metal, machinery, electrical equipment manufacturing
5. **Dams** - Dam infrastructure and water retention systems
6. **Defense Industrial Base** - Military equipment and defense supply chain
7. **Emergency Services** - Police, fire, EMS response systems
8. **Energy** - Electric grid, oil, natural gas, nuclear power
9. **Financial Services** - Banking, securities, insurance
10. **Food and Agriculture** - Farming, food processing, distribution
11. **Government Facilities** - Federal, state, local government buildings
12. **Healthcare and Public Health** - Hospitals, clinics, public health systems
13. **Information Technology** - Hardware, software, data centers
14. **Nuclear Reactors, Materials, and Waste** - Nuclear power plants and materials
15. **Transportation Systems** - Aviation, rail, roads, pipelines, maritime
16. **Water and Wastewater Systems** - Drinking water, wastewater treatment

### Key OT/CS Takeaways
- **Energy** and **Water** are the most commonly targeted in OT/CS attacks.
- **Transportation** (pipelines, rail signals) and **Critical Manufacturing** are increasingly targeted.
- Asset owners/operators in these sectors are responsible for cybersecurity under regulations like NERC CIP (Energy), TSA directives (Transportation), and CFATS (Chemical).
- The interconnectedness means defending one sector alone is insufficient — a holistic approach is required.

https://youtube.com/playlist?list=PLOSJSv0hbPZAlINIh1HcB0L8AZcSPc80g&si=Z6ZZb4jaZQXXmx9U

---
### **II. Differences Between IT and OT Networks**
*   **Primary Priority (Safety):** In OT, **safety is the primary consideration**. IT focuses on protecting sensitive information, while OT focuses on the physical safety of onsite personnel and the general public.,
*   **Physical Environment:** IT assets are typically in safe office settings. OT assets are located in plants (refineries, power plants, mines) that can be physically dangerous.,
*   **Data Usage:**
    *   **IT:** Manages large amounts of stored data like spreadsheets and documents.
    *   **OT:** Processes **very small amounts of real-time data** from sensors to make immediate physical decisions.
*   **Security Triads:**
    *   **IT (CIA):** Focuses on **Confidentiality**, Integrity, and Availability.
    *   **OT:** Prioritizes **Physical Safety, Environmental Safety, and Availability**, followed by the Integrity of process data., Confidentiality is often a lower priority unless a proprietary formula is involved.
*   **Business Connectivity and Risk:** IT and OT networks are often connected because the business side (IT) needs data from the production side (OT) to coordinate **shipping, logistics, and supply chain** needs. 
*   **The Internet Connection Point:** The primary risk to OT is not usually a direct connection to the internet, but rather its connection to the IT network, which *is* connected to the internet. If a path exists for IT to reach into OT, an attacker will eventually find and exploit it.
*   **Data Processing Nuance:** Unlike IT systems that manage large files, OT assets have **very little storage space** and process **very small amounts of real-time data** solely to determine immediate physical actions.

---
### **III. The Five Main Ways Attackers Enter OT Networks**
1.  **Through the IT Network:** The most common path because IT is connected to the internet and often has a communication path into the OT network for business logistics.,
2.  **Transitory Cyber Assets:** Laptops, USB drives, and smartphones brought into the plant physically., If these are infected and plugged into the OT network, the malware spreads.
3.  **Internet-Exposed Assets:** OT systems (like PLCs or HMIs) that are mistakenly connected directly to the internet, allowing anyone in the world to attempt to exploit them.
4.  **Remote Access:** Exploiting poorly configured remote access used by vendors or employees to perform maintenance from home.,,
5.  **Malicious Insiders:** Employees or contractors with legitimate credentials and physical access who intend to cause harm.
*   **Transitory Cyber Assets (NERC CIP Term):** This category includes more than just USBs; it specifically encompasses **smartphones and vendor laptops** that store process data and are physically brought into the environment.
*   **The Remote Access Dilemma:** While remote access is a major attack vector, it is often utilized for **safety reasons**. It is physically safer for a technician to upgrade firmware from home than to stand in the middle of a potentially hazardous plant.
*   **Malicious Insiders:** These are not just disgruntled employees but can include **partners or vendors** who have been granted legitimate credentials and physical access but intend to cause harm.
*   **IP Address Escalation:** A simple thermostat becomes a major security risk only when it is assigned an **IP address (TCP/IP)**. This allows it to talk to other local systems and exposes it to the internet, where attackers can manipulate it to run up electric bills or, in industrial cases, cause safety issues.
*   **Logic over Storage:** OT assets like thermostats have an **operating system and code** designed to do a limited number of jobs; they are not designed for general computing tasks like spreadsheets.

---
### **IV. Basic Example of OT: The Thermostat**
*   **Components:** A thermostat is a computer with memory, a processor, and code.,
*   **The Set Point:** It has a programmed variable (e.g., 70 degrees).
*   **The Control Loop:** The device takes **sensor data** (the current temperature) and compares it to the set point. If it's too warm, it sends an electrical signal to a **physical asset** (the air conditioner) to turn it on., Once the temperature is back to the set point, it sends a signal to turn it off.
*   **Network Risk:** The risk increases exponentially when these devices are given an IP address (TCP/IP), potentially exposing them to the local network or the internet.,
*   **LAN vs. WAN:** A helpful way to distinguish these is that **ICS is to a LAN (Local Area Network)** as **SCADA is to a WAN (Wide Area Network)**. SCADA is specifically for systems that require remote communication over distances via 5G or satellite.
*   **IoT Dependency:** Consumer IoT (e.g., Amazon Alexa) differs from OT because it has **limited local computing power** and **requires a cloud server** to function. If the internet goes down, IoT devices generally stop working, whereas true OT performs its logic locally.
*   **Asset Owners vs. Operators:** The **Asset Owner** is the company that owns the facility (e.g., Dominion Energy), while the **Operator** is the entity running it. Sometimes they are the same company, but other times a third party is hired to manage operations.

---
### **V. Defining OT, ICS, and SCADA**
*   **OT (Operational Technology):** The general term for computers used to control physical systems.
*   **ICS (Industrial Control Systems):** "Industrial strength" OT used in critical infrastructure.
*   **SCADA vs. ICS:**
    *   **ICS:** Refers to local systems (LAN) at a single physical location, like a power plant.,
    *   **SCADA:** Refers to systems spread over a wide geographical area (WAN) using 5G or satellite to communicate with remote substations.,
*   **IoT vs. OT:** Consumer IoT (e.g., Alexa) requires the cloud to function and lacks local computing power., True OT performs its logic and processing locally.
*   **Owners and Operators:** The **Asset Owner** is the company that owns the facility; the **Operator** is the entity responsible for running it.,

---
### **VI. Critical Infrastructure and Interconnectedness**
*   **The 16 Sectors:** In the U.S., there are 16 recognized critical sectors, with "Space" currently being considered as a 17th.
*   **Interdependence:** Sectors are highly interconnected; for example, the **Chemical sector** provides pesticides for **Agriculture**, which in turn requires **Water** for irrigation and **Energy** to pump it.
*   **Societal Impact:** The source notes that if these systems fail for extended periods, society enters "Walking Dead territory," where civilization begins to break down.

---
### **VII. Advanced Concepts in OT Incidents**
*   **Loss of Visibility (Stuxnet):** One of the most sophisticated tactics used in Stuxnet was recording **normal telemetry data** and playing it back to operators. This made everything look perfect in the control room while the equipment was physically being destroyed.
*   **Living off the Land (2022 Blackout):** Recent attacks have shown that nation-states don't always need custom malware. In a 2022 Ukrainian incident, attackers used **built-in operating system commands** and legitimate software (MicroSCADA) to log in and flip breakers.
*   **Targeting SIS (TRISIS):** The source emphasizes that the only reason to target **Safety Instrumented Systems (SIS)** is to disable life-safety protections, indicating an intent to cause an explosion or kill people.

---
### **VIII. History of OT Incidents**
*   **SQL Slammer (2003):** Infected a **nuclear power plant** (Davis-Bessie) because a contractor installed a T1 line that bypassed the supposed "air gap.",
*   **Stuxnet (2010):** A joint U.S./Israeli attack on Iranian centrifuges. It introduced **"loss of visibility,"** playing back normal data to operators while physically destroying equipment in the background.,
*   **Ukraine Blackouts (2015/2016):** Russian attackers took control of Windows machines to flip breakers and shut off power during winter.,
*   **TRISIS/Triton (2017):** Malware targeting **Safety Instrumented Systems (SIS)** in a petrochemical plant. This was the first known attack designed specifically to disable life-safety fail-safes.,
*   **Colonial Pipeline (2021):** A watershed moment where a ransomware group (not a nation-state) took the largest U.S. gasoline pipeline offline, proving that **IT/OT convergence** makes OT a target for all hackers.,
*   **Pipe Dream (2022):** A nation-state-developed automated framework (similar to Metasploit) for targeting and controlling OT networks.,

---
### **IX. Securing the Environment**
*   **Secure Network Architecture:** The **#1 way to protect OT**. It involves allowing OT to "push" data to IT but strictly **prohibiting IT from reaching into the OT network**.,
*   **Physical Security:** Often overlooked; if an attacker can touch an asset, they can own it via password resets or physical hacking tools.,
*   **Standards:** **ISA/IEC 62443** is the international standard for building an OT security program; **NIST 800-82** is a U.S. government alternative.,
*   **The Sliding Scale of Cybersecurity:** Organizations should prioritize **Architecture and Passive Defense** (monitoring) because they provide the highest **Return on Investment (ROI)** for risk reduction.,, Offensive capabilities like penetration testing are expensive and should be done last.,
*   **The One-Way Push Rule:** For secure network architecture, organizations should allow OT to **"push"** data out to IT, but never allow the IT network to **reach back into** or initiate communication with the OT network.
*   **The Sliding Scale of Cybersecurity:** Security should be built in this order to maximize **Return on Investment (ROI)**:
    1.  **Architecture:** (Highest risk reduction, lowest cost).
    2.  **Passive Defense:** (Monitoring and detection).
    3.  **Active Defense:** (Incident response analysts).
    4.  **Offensive Capabilities:** (Penetration testing - should be done last as it is expensive and offers the least relative risk reduction).

---
### **I. Real-World Example: Combined Cycle Natural Gas Power Plant**
The video uses a power plant as a primary example to illustrate ICS concepts.
*   **The Process:** Natural gas is brought in and heated to turn a turbine, which spins a generator to create electricity.
*   **Combined Cycle Efficiency:** Modern plants use a second "loop" where the exhaust heat from the first turbine heats water to create steam, which turns a second turbine and generator, significantly increasing electrical output.
*   **Safety Priority:** These environments are highly energized and physically dangerous, emphasizing why **safety** is the top priority in OT.

---
### **II. Engineering Terms: ISBL, OSBL, Greenfield, and Brownfield**
*   **ISBL (Inside Battery Limits):** All systems and components that make up the actual plant itself (e.g., turbines, generators, steam pipes).
*   **OSBL (Outside Battery Limits):** Resources on the site used to support the plant but not part of the physical plant itself, such as the parking lot, security gate, control room, or water storage tanks.
*   **Greenfield Projects:** Brand new facilities. This is the ideal time to design and "build in" cybersecurity from the ground up.
*   **Brownfield Projects:** Existing facilities (often 10–50 years old). These are difficult to secure because old systems are fragile; a small change (like adding a firewall) could bring down the entire site.

---
### **III. The Industrial Life Cycle**
1.  **FEED (Front-End Engineering Design):** Engineers create the schematics and blueprints for the facility.
2.  **EPC (Engineering, Procurement, and Construction):** The company (like Fluor) sources materials (steel, concrete, control systems) and builds the site.
3.  **Commissioning/Testing:** Units are tested individually to ensure they operate safely before being turned over to the **Asset Owner**.
4.  **O&M (Operations and Maintenance):** The day-to-day running and preventative maintenance of the plant.
5.  **Decommissioning:** Turning off and removing the site at the end of its useful life (often 30–50 years).

---
### **IV. Types of Control Systems**
*   **Field Devices:** Sensors (detect temperature, humidity) and actuators (valves, pumps, motors). These are often overlooked in cybersecurity because they require physical access to manipulate.
*   **PLC (Programmable Logic Controller):** The most common control system. It is a computer with a processor and memory that runs code (logic) to process inputs and outputs.
*   **DCS (Distributed Control System):** A centralized hierarchy used to manage multiple individual PLCs and complex processes across a plant.
*   **SCADA (Supervisory Control and Data Acquisition):** Used for wide geographical areas (WAN) like power transmission, often communicating via cellular or satellite links.
*   **HMI (Human Machine Interface):** A graphical dashboard for operators to see process data and push buttons to control the PLC.
*   **SIS (Safety Instrumented System):** The "fail-safe" backup system designed specifically to protect human life. It should be **air-gapped** or islanded from other networks.
*   **Engineering Workstation (EWS):** A laptop or PC used to program PLCs and update firmware. These are high-value targets for attackers because they contain the process logic.
*   **Data Historian:** A database (often MS SQL) that stores historical process data for business logistics and billing. It is frequently the **#1 attack target** because it often sits in a DMZ between the IT and OT networks.

---
### **V. Industrial Networking and Protocols**
*   **TCP/IP:** The common language of the internet. Most industrial protocols have been adapted to run over TCP/IP, which introduces the risk of unintentional internet exposure.
*   **The OSI Model:** A 7-layer framework (Physical to Application) that allows different hardware and software to communicate.
*   **Modbus:** The most common industrial protocol. It uses a client-server relationship and typically runs over **TCP Port 502**.
    *   **Coils:** Store single-bit (0 or 1) values for "on/off" actions.
    *   **Registers:** Store larger values, such as temperature or set points.
*   **Other Protocols:**
    *   **S7:** Siemens proprietary protocol.
    *   **OPC/OPC UA:** OPC is older and complex; OPC UA is the modern, secure, open-source replacement.
    *   **DNP3/IEDs:** Used specifically in power transmission.

---
### **VI. Tools and Programming**
*   **Ladder Logic:** The most common programming language for PLCs.
*   **PLC Key Switches:**
    *   **Run Mode:** Read-only mode. Secure because it prevents remote changes to the code or firmware.
    *   **Program Mode:** Read/write mode. Used for updates but vulnerable if left on accidentally.
*   **Wireshark:** A free tool used to capture and analyze network packets (zeros and ones). It uses **"dissectors"** to translate raw data into readable industrial protocols like Modbus.
*   **Promiscuous Mode:** A setting that allows a network card to see all traffic on a wire, even if not addressed to that specific computer.

---
### **I. The "One Thing" to Protect OT: The Firewall**
*   **The Single Most Effective Defense:** If an organization can only do one thing to protect an OT network, it is to install a **firewall** between the IT and OT networks.
*   **Risk Mitigation:** A properly configured firewall prevents threats like ransomware from spreading from the compromised IT environment into the physical plant. 
*   **Operational Resilience:** While a ransomware attack may "burn down" the IT office, a firewall ensures the plant continues generating power or manufacturing goods safely.
*   **Default Deny:** Firewalls should be configured to **block all traffic** by default, only opening specific "holes" required for business operations.

### **II. The IT Cyber Kill Chain (Lockheed Martin)**
This model explains the common process attackers use to breach an IT network before moving toward OT.
1.  **Reconnaissance:** Attackers gather Open Source Intelligence (OSINT) from Google, LinkedIn, and social media to find employee names and email structures.
2.  **Weaponization:** Coupling a phishing email with a malicious link or attachment. (Note: Phases 1 and 2 are typically **undetectable** by the victim organization).
3.  **Delivery:** Sending the malicious email to targets.
4.  **Exploitation:** The victim triggers the malware by clicking the link or opening the attachment.
5.  **Installation:** The malware installs itself on the victim's machine.
6.  **Command and Control (C2):** The infected system reaches out to an attacker-controlled server on the internet, giving the attacker remote access to the computer.
7.  **Actions on Objectives:** The attacker pursues their mission, such as data theft, espionage, or deploying ransomware.

### **III. The Expanded Purdue Model**
This framework segments the environment into functional layers to secure communication.
*   **Levels 4 & 5 (Enterprise IT):** The "back office" where employees use email and the internet. This is the most dangerous zone due to its direct internet exposure.
*   **Level 3.5 (The DMZ):** A critical "Enforcement Boundary" between IT and OT. It should ideally use **two layers of firewalls from different vendors** to prevent a single "zero-day" exploit from bypassing both.
*   **Level 3 (Site Operations):** Contains systems like Active Directory, patch management, and site-wide historians. These are almost exclusively **Windows-based**.
*   **Level 2 (Supervisory Control):** Includes HMIs, SCADA servers, and engineering workstations. These are also primarily Windows-based, making them easy targets if an attacker breaches the IT-OT boundary.
*   **Level 1 (Local Control):** The "true" control layer containing **PLCs, RTUs, and IEDs**. These run custom operating systems or Linux; Windows usage drops off significantly here.
*   **Level 0 (The Process):** Physical sensors and actuators (valves, pumps, motors).
*   **The "One Up, One Down" Rule:** As a general rule, assets should only communicate with the layer immediately above or below them.

### **IV. Firewalls, Protocols, and ACLs**
*   **The 5-Tuple:** Packet filtering firewalls use a list of five items to allow or deny traffic: Source IP, Source Port, Destination IP, Destination Port, and Protocol (TCP/IP, UDP, or ICMP).
*   **Traffic Directionality:** Connections should always be **initiated by OT** to "pull" data (like patches) or "push" data (like logs) to the DMZ. The IT network should **never** be allowed to originate a connection into OT.
*   **Common Ports to Monitor:** 
    *   **IT:** 80/443 (Web), 3389 (Remote Desktop), 21 (FTP), 22 (SSH).
    *   **OT:** 502 (Modbus), 102 (S7).
*   **Stateful Inspection:** Modern firewalls track active connections to ensure "return traffic" is legitimate and not a spoofing attempt.
*   **Deep Packet Inspection (DPI):** Advanced firewalls (like mGuard) that can look inside the packet to allow only specific OT commands (e.g., allowing an HMI to "read" but not "write" to a PLC).
*   **Switches:** While switches can use Access Control Lists (ACLs), they are **not firewalls** and should not replace them for segmenting IT from OT.

### **V. Data Diodes and Unidirectional Gateways**
*   **Data Diodes:** Specialized appliances that use physics (light/fiber) to ensure data can **physically** only travel in one direction. There is zero possibility of return traffic, making them the most secure option, though they are more expensive.
*   **Unidirectional Gateways:** A combination of hardware and software that emulates one-way traffic. They are common alternatives to diodes but are theoretically "hackable" because they rely on software.

### **VI. The ICS Cyber Kill Chain**
Developed by Michael Assante and Rob Lee, this model describes the specific steps an attacker takes once they have transitioned from the IT network into the OT network. It highlights that because Level 2 and 3 assets are often Windows-based, attackers can use the same techniques in OT that they used to breach IT.

### **VII. Industrial Internet of Things (IIoT)**
*   **Concept:** Using thousands of sensors on assets (like locomotives or wind turbines) for **predictive analytics** to prevent accidents and schedule maintenance.
*   **Security Strategy:** Since IIoT requires connecting OT assets to the cloud, it must be done via **outbound-only connections**. Using data diodes or firewalls ensures data reaches the cloud for analysis without allowing attackers to come back into the OT environment.

### **VIII. Secure Remote Access**
*   **The "Necessary Evil":** Required for vendors to perform maintenance or firmware upgrades remotely.
*   **Safety Benefit:** It is physically safer for a technician to work from home than to stand in a dangerous plant during an upgrade.
*   **Security Requirements:** Must use **VPNs, Jump Boxes, Multi-Factor Authentication (MFA)**, and "on-demand" access rather than persistent connections.

### **IX. Lessons from the TRISIS/Triton Incident**
*   **Isolation of SIS:** The Safety Instrumented System (SIS) must be **islanded or air-gapped** from the rest of the network. In the TRISIS attack, the SIS was exposed, allowing attackers to target the life-safety controllers.
*   **Key Switch Management:** Physical key switches on controllers should be kept in **"Run" mode** to prevent remote unauthorized programming changes, although this is not a bulletproof defense against sophisticated bypasses.
---
### **I. Introduction to Asset Registers**
*   **Definition:** In the OT world, an "Asset Inventory" is commonly referred to as an **Asset Register**. It is a comprehensive list of all hardware, software, and firmware within the environment.
*   **Accuracy:** While it is difficult to maintain a 100% accurate register, the goal is to get as close to perfect as possible.
*   **The "Treasure Map":** If an attacker obtains your asset register, they essentially have a blueprint or treasure map of your environment, including software versions and known vulnerabilities they can exploit.

### **II. Importance of the Asset Register**
*   **Foundation for Security:** You cannot effectively perform **Vulnerability Management** or **Incident Detection and Response** without knowing exactly what assets are in your environment.
*   **Operational Context:** During an incident, the register allows you to identify the asset (e.g., an Allen-Bradley PLC), its criticality, and the correct personnel to contact.
*   **Consequences of Failure:** The lack of an asset register can lead to devastating breaches where businesses go under and people lose their jobs because they cannot recover from an infection (e.g., the story of a manufacturing plant that shut down after an infected USB was used).

### **III. What to Track in an Asset Register**
A robust register should include the following information for all physical and virtual assets:
*   **General Identity:** Asset ID, Asset Name (naming conventions), and Asset Type (PLC, HMI, Sensor, etc.).
*   **Physical Information:** Physical location (building, substation, or field) and the Manufacturer/Vendor.
*   **Hardware Details:** Model number, Serial number, and Hardware version.
*   **Software & Firmware:** Firmware versions, software applications, and specific software versions—crucial for mapping to vulnerabilities.
*   **Network Properties:** IP Addresses (if running TCP/IP) and MAC Addresses (physical 48-bit addresses).
*   **Operational Context:** Mission-critical status (e.g., if this asset goes down, does the whole plant stop?), responsible party (who to contact), and current status (production vs. maintenance).
*   **Cyber Architecture:** Zone and Conduit assignments based on **ISA/IEC 62443**.

### **IV. The Four Main Ways to Build an Asset Register**
1.  **Walking the Environment:** Physically tracing cables from switches to end devices.
    *   **Pros:** Highly accurate for physical confirmation.
    *   **Cons:** Extremely time-consuming, expensive, and can put employees in "Harm's Way" in dangerous plant environments.
2.  **Reviewing Existing Data:** Examining project files and documentation.
    *   **Sources:** Network diagrams, system design specifications, PLC programming files, and **Procurement/Purchase records** (invoices).
    *   **Network Clues:** Checking ARP tables on managed switches and firewalls to find IP/MAC address pairings.
3.  **Passive Listening (Sniffing):** Capturing network traffic without generating new packets.
    *   **Tools:** Using **Wireshark** to "listen" to the wire.
    *   **Benefits:** Safe for OT because it doesn't risk crashing sensitive or old equipment.
    *   **Limitations:** You only see devices that happen to be talking during the capture window.
4.  **Active Scanning:** Generating packets to probe the network.
    *   **Tool:** **Nmap** (Network Mapper).
    *   **Risks:** High risk of crashing older OT equipment that isn't designed to handle unexpected network packets.
    *   **Requirement:** Never perform active scanning without explicit authorization.

### **V. Active Scanning with Nmap**
*   **Nmap Objectives:** Identify live hosts, open ports (the "doors and windows" of a system), services/applications, and software versions.
*   **TCP vs. UDP:** TCP is connection-oriented (3-way handshake); UDP is connectionless and faster but harder to scan accurately.
*   **Scanning Techniques:**
    *   **Ping Sweep (`-sn`):** Quickly finds live IP addresses on a subnet.
    *   **Port Scanning (`-p-`):** Checks all 65,535 possible TCP ports.
    *   **Service Scan (`-sV`):** Probes open ports to determine the vendor and version of the software.
    *   **Nmap Scripting Engine (NSE):** Using specialized scripts like `modbus-discover.nse` to pull metadata (firmware, slave IDs) directly from PLCs.

### **VI. Passive Listening & OT Protocols**
*   **Visibility:** Many OT assets do not use TCP/IP but talk in industrial protocols like **PROFINET** or advertise themselves via **LLDP** (Link Layer Discovery Protocol).
*   **Encryption:** Most OT traffic is unencrypted, which is an advantage for security professionals as it makes it easier to identify malicious commands without needing to break encryption.
*   **Vendor Software Discovery:** Tools like Siemens' **TIA Portal** or Automation Direct's **Click PLC** software use broadcast traffic to find devices, revealing their firmware, IP, and hardware state (Run vs. Program mode).

### **VII. Securing the Asset Register**
*   **Storage Location:** Avoid storing the register in the cloud where it is more susceptible to compromise; keep it locally on-premise.
*   **System Hardening:** The server or workstation holding the register must be hardened following **CIS guidelines**.
*   **Access Controls:** Use strict permissions and physical security (locked data centers) to prevent unauthorized access.
*   **Emergency Access:** If the register (e.g., an Excel file) is encrypted, ensure the team has the password available for emergency response.
*   **Lifecycle Management:** The register must be updated regularly (at least quarterly) through authorized **Change Management** procedures.

### **I. Overview: Threat, Vulnerability, and Risk Management**
*   **The Core Objective:** Cybersecurity in both IT and OT is fundamentally about **reducing risk** to the environment. The goal is to stop bad things from happening or, if they do occur, to limit the damage as much as possible.
*   **The Difference in Prioritization:** While IT and OT share similarities, the methodology for finding and prioritizing vulnerabilities differs significantly because OT environments are much more sensitive to active disruptions.
*   **Key Themes:**
    *   What threat and vulnerability management are.
    *   How to prioritize vulnerabilities based on risk.
    *   The difference between **Passive** and **Active** identification.
    *   How patching works in OT.
    *   Establishing a **Threat Intelligence** program (on a budget).

---

### **II. Understanding Risk: The Business Perspective**
*   **The Risk Formula:** Risk is composed of the **Threat** (attacker), **Vulnerability** (weakness), **Probability** (chance of occurrence), and **Impact** (negative consequences).
    *   **Threat Actors:** Nation-states, ransomware groups, activists, and "script kitties".
    *   **Probability:** This must be as realistic as possible using real-world data.
    *   **Impact:** Can be measured as "worst-case scenario" vs. "realistic scenario".
*   **Business Drivers:** Risk is ultimately viewed through the lens of **money**.
    *   **Cost of Downtime:** A critical risk question is: *"How much does it cost the business if the plant goes down for 24 hours?"* This can range from $10,000 to hundreds of millions of dollars depending on the company's size.
    *   **Budget and Resources:** The business (executives), not the security professional, determines the **risk tolerance** (how much risk they are willing to take).
*   **Qualitative vs. Quantitative Risk:**
    *   **Quantitative:** Hard facts and metrics (e.g., "A breach costs $15 million").
    *   **Qualitative:** "Gut instinct" or subjective assessments, which can be prone to error.

---

### **III. The Importance of the Asset Register**
*   **The Foundation:** You cannot protect what you don't know you have. An accurate asset register is the starting point for both vulnerability management and incident response.
*   **Vulnerability Mapping:** By knowing the **vendor, model, and firmware version** (e.g., a Siemens S7-1200 running firmware 3.84), you can manually look up known vulnerabilities without scanning the device.

---

### **IV. The IT Vulnerability Management Process**
This traditional IT process serves as the baseline before moving to OT:
1.  **Scan:** Use tools like **Nessus** to generate packets that probe hosts for open ports and services.
2.  **Prioritize:** Assign risk levels (Low, Medium, High, Critical) based on the **CVSs score (0-10)**.
    *   **Critical (Level 9-10):** Easy to exploit remotely, granting full administrative control. These often require remediation within 24–48 hours.
    *   **Informational:** Notes about hostnames or versions that are useful for context (and for attackers).
3.  **Remediate:** Work with asset owners to apply patches or fix configurations.
4.  **Rescan:** Verify that the fix was successful.

---

### **V. OT Vulnerability Management: Nuances and Strategy**
*   **The Danger of Active Scanning:** Older OT assets may crash, reboot, or even **"brick"** (become permanently unusable) when they receive unexpected network packets from a scanner.
*   **Active vs. Passive Identification:**
    *   **Active:** Probing the network (unrestricted in IT; highly restricted in OT).
    *   **Passive:** Using a tool like **Wireshark** in "promiscuous mode" to listen to traffic and identify assets by the data they naturally advertise.
*   **Scanning the Purdue Model:**
    *   **Levels 3, 3.5, and 4 (IT/DMZ):** Generally safe to scan and patch Windows-based systems (historians, workstations) if they don't impact life safety.
    *   **Levels 0-2 (The Process):** Avoid active scanning of HMIs, PLCs, and sensors unless there is no threat to safety or uptime.
*   **FAT and SAT (The "Free Reign" Phase):** The best time for active scanning and penetration testing is during **Factory Acceptance Testing (FAT)** or **Site Acceptance Testing (SAT)**, as the equipment is not yet in production.
*   **Compensating Controls:** If a vulnerability cannot be patched (e.g., the plant cannot shut down for 9 months), you can apply "compensating controls" like **network segmentation** or enhanced monitoring to lower the risk to an acceptable level.

---

### **VI. Threat Intelligence (TI)**
*   **Definition:** Monitoring news and real-world events to determine if they apply to your specific environment and taking action if they do.
*   **Starting a Program for Free:** You do not need a $200,000 budget. You can start by monitoring:
    *   **News Sources:** Bleeping Computer (highly recommended), SANS Internet Storm Center, Wired, and CISA advisories.
    *   **Vendor Reports:** Publicly available research from Dragos or Mandiant.
*   **Advanced TI Concepts:**
    *   **Indicators of Compromise (IOCs):** Evidence like IP addresses, domain names, or file hashes that indicate an attacker is present.
    *   **The Diamond Model:** A framework for analyzing incidents by looking at the **Adversary, Infrastructure, Capability, and Victim**.
    *   **Attribution:** Naming the attacker (e.g., "Sandworm"). While "cool" for research, a defender’s primary goal is simply getting the attacker out of the environment.

---

### **VII. Information Sharing and ISACs**
*   **The Problem with Silos:** Organizations that don't share information allow attackers to reuse the same tactics on other victims.
*   **ISACs (Information Sharing and Analysis Centers):** Groups organized by industry (Energy, Water, Rail, etc.) where members share attack data anonymously.
    *   **Energy ISAC (E-ISAC):** One of the largest and most prominent in the OT world.
    *   **Informational vs. Formal:** Informal sharing often happens under **Chatham House Rules** (information can be shared, but sources/names must remain confidential).

### **I. Introduction to OSINT for ICS/OT**
*   **Definition:** Open Source Intelligence (OSINT) is the use of information and tools freely available on the internet—meaning they are not behind a paywall or a login—to gather intelligence. 
*   **Primary Goal:** The objective is for organizations to find their own control systems that are exposed to the internet before attackers do, allowing them to fix the issues.
*   **Intelligence Types:** While OSINT is the focus, other forms include Human Intelligence (HUMINT) from spies and Signals Intelligence (SIGINT) gathered from electronic signals.
*   **Context:** OSINT applies to both IT and OT environments, as the tools and tactics are often interchangeable.

---

### **II. Entry Points and the Importance of Reconnaissance**
*   **Refresher on Entry Points:** Attackers primarily enter OT networks through:
    1.  The IT network (most common via phishing).
    2.  Transitory cyber assets (USB drives, vendor laptops, smartphones).
    3.  **Direct internet exposure (the focus of this section).**
    4.  Remote access capabilities.
    5.  Malicious insiders.
*   **The Reconnaissance Loop:** Attackers perform reconnaissance to increase their mission success. To combat this, defenders must perform the same reconnaissance on themselves to find and fix vulnerabilities.
*   **Case Study (Cyber Avengers):** In late 2023, an Iranian-associated activist group called the Cyber Avengers targeted Unitronics Vision PLCs exposed to the internet in water treatment plants. They used a default password ("1111") to take control and display a hacking signature on the integrated HMI.

---

### **III. Google Dorking (Specialized Searches)**
*   **The Tool:** While AI tools (Gen AI, ChatGPT) are becoming popular for OSINT, Google remains the "tried and true" search engine for indexed, public information.
*   **Google Dorks:** These are specialized search strings using specific operators to find sensitive files.
    *   `filetype:`: Used to find specific files like PDFs or Excel sheets (e.g., `filetype:pdf "network diagram"`).
    *   `site:`: Limits results to a specific domain (e.g., `site:microsoft.com`).
    *   `cache:`: View the version of a page Google saved before it was potentially taken down.
    *   `intitle:` and `inurl:`: Search for keywords in the page title or the URL address bar.
*   **Google Hacking Database (GHDB):** A formal database of these searches maintained by the Offensive Security team.
*   **Legal/Ethical Note:** Clicking a link found via Google is legal OSINT; attempting to brute force or break into that page is where it becomes illegal.

---

### **IV. NSA Elite Wolf Project**
*   **Origin:** Published by the NSA in response to "Volt Typhoon" (Chinese nation-state activity) targeting critical infrastructure.
*   **Mechanism:** It consists of **Snort rules** (intrusion detection signatures) for vendors like Allen-Bradley, SEL, and Siemens.
*   **Reverse Engineering:** Defenders can take strings from these Snort rules (such as specific URL paths like `/RootForm/AdvancedDiags`) and turn them into Google dorks to find exposed PLC web interfaces.
*   **Findings:** These searches can reveal a PLC's web interface, which may expose:
    *   The model and serial number.
    *   Internal IP addresses of the PLC and engineering workstations.
    *   Current TCP connections, showing every public IP address (potential attackers) currently talking to that PLC.

---

### **V. WHOIS Information and IP Tracking**
*   **WHOIS:** A database of registration information for domain names and IP addresses.
*   **Tracking Assets:** If an exposed PLC is found via an IP address, WHOIS can help identify where in the world it is (Geo-IP) and what organization is associated with it.
*   **Anonymization:** Many individuals and companies use privacy services to hide their home addresses in these records.
*   **Tool (DNSlytics):** Used to see a map of IP locations and WHOIS data.
*   **Utility:** This helps distinguish if an IP is a generic ISP (like Verizon), which is hard to track, or a specific company/security entity (like Palo Alto Networks performing internet scanning).

---

### **VI. DNS (Domain Name System) and DNS Dumpster**
*   **Function:** DNS maps human-readable domain names to the IP addresses computers use to connect.
*   **Reverse DNS:** Resolves an IP address back to its associated domain name.
*   **Naming Conventions:** Naming schemes often help attackers identify targets (e.g., "PLC01" or "EWS" for Engineering Workstation).
*   **DNS Dumpster:** A free web tool that provides up to 100 DNS records for a target.
    *   It identifies MX (mail) records, TXT records (often revealing third-party app associations like Google or Facebook), and host (A) records.
    *   It provides an **Autonomous System Number (ASN)** to identify which organization (e.g., Akamai, Microsoft, or the target company) is hosting the asset.
    *   It generates a flowchart/map showing how different systems and subdomains are connected.

---

### **VII. Digital Certificates and Censys**
*   **Context:** Certificates identify websites and allow for encryption (HTTPS). They are ubiquitous in IT but less common in OT.
*   **The OT Encryption Debate:** Encryption protects confidentiality, but in OT, it can slow down real-time responses and prevent security tools (like Snort) from inspecting traffic for malicious activity.
*   **Censys:** A search engine that indexes 3.3 billion services and is particularly strong at finding digital certificates.
    *   Unlike Shodan, Censys scans **all 65,535 TCP ports**.
    *   Defenders can search for certificate strings (e.g., "s7-1200 controller family") to find Siemens PLCs that have encrypted web interfaces.
    *   Certificates often expose the **internal IP address** of the host when they are created.

---

### **VIII. Dangers of Social Media**
*   **Platforms:** Technicians often post on LinkedIn or the "PLC" subreddit.
*   **Information Leakage:** Pictures of "pretty" new jobs or requests for help with old equipment can reveal:
    *   The specific model and hardware version of assets.
    *   Whether a PLC is in "Run" or "Stop" mode.
    *   Passwords written on sticky notes.
*   **Proprietary Data:** A case was cited where a client employee posted a photo of their workstation on LinkedIn; a billion-dollar proprietary chemical formula was visible on the monitor in the background.
*   **Badges:** Posting "first day" badge photos allows attackers to create visually accurate fake badges to use for social engineering or tailgating.

---

### **IX. Shodan (The Search Engine for Things)**
*   **History:** Created in 2009 by John Matherly to find devices connected to the internet, with a heavy focus on ICS/OT.
*   **How it Works:** Shodan scans the internet and "grabs banners" (metadata) from open ports.
*   **Explore Feature:** Allows users to browse by protocol, such as Modbus (Port 502), S7 (Port 102), BACnet, and Ethernet/IP (Port 44818).
*   **Honeypots:** Fake systems designed to be attacked so defenders can learn attacker tactics.
    *   **High Fidelity:** Because nothing should ever talk to a Honeypot, any alert is 99.9% likely to be an actual attack.
    *   Shodan tags known honeypots to prevent researchers from being fooled.
*   **Shodan Images:** Captures screenshots of Remote Desktop (RDP) sessions and webcams.
    *   **RDP Risks:** Screenshots often show the administrator username and notifications that the system is missing security updates.
    *   **Webcams:** Often left on the OT network (e.g., at construction sites or security gates), providing an easy initial foothold for attackers.
    *   **HMIs:** Some HMIs are exposed in "read-only" mode, but they still reveal the underlying process, chemical levels, or equipment status to attackers.

### **I. Philosophy: "Defense is Doable"**
*   **The Approach:** Industrial cybersecurity defense should be practical and approachable, not overly complicated.
*   **Why OT is Easier to Defend than IT:**
    *   **Predictable Traffic:** Communication patterns are highly limited. For example, an HMI only talks to a PLC at specific intervals.
    *   **Fewer Hosts:** Even the world's largest OT environments typically have fewer hosts than a standard corporate IT network.
    *   **Visibility:** Because there is less overall noise and traffic, it is much easier to identify anomalies through Network Security Monitoring (NSM).

---

### **II. Detecting the Five Main Entry Points**
Incident detection serves as a **detective control** (rather than preventative) to identify when an attacker uses one of the five primary pathways:
1.  **IT to OT Pivot:** Monitoring the DMZ and OT network for activity originating from the IT side.
2.  **Transitory Cyber Assets:** Detecting compromised smartphones, USBs, or laptops when they connect to the network.
3.  **Internet Exposure:** Using vulnerability management to find assets accidentally exposed to the web. (Note: Exposed PLCs can be hit by over 200 unique IP addresses in 24 hours).
4.  **Remote Access:** Identifying unauthorized use of remote tools or stolen credentials, especially when MFA is absent.
5.  **Malicious Insiders:** Often the hardest to detect, requiring a high-level monitoring program.

---

### **III. The SANS 6-Phase Incident Response Process**
The video utilizes the SANS Institute’s six-phase model as the standard framework:
1.  **Preparation:** Building the program, training the team, and establishing policies.
2.  **Identification (Detection):** Detecting suspicious activity. **Key Insight:** 99.9% of the time, detection tools find **operational issues** (misconfigurations) rather than hackers, which still provides major value for site uptime.
3.  **Containment:** Limiting the attacker's spread and preventing further damage.
4.  **Eradication:** Completely removing the attacker and their artifacts from the network.
5.  **Recovery:** Returning the business to normal operations. This is the **primary concern for executives**.
6.  **Lessons Learned:** A post-incident review to improve the program and prevent recurrence.

---

### **IV. Phase 1: Preparation (The Foundation)**
*   **Incident Response Program:** Organizations should have a short policy mandating a program, which then contains detailed guidelines and procedures.
*   **The Dynamic Team (CSIRT):**
    *   The team is **dynamic**, bringing in members as needed (e.g., malware analysts, PLC technicians, or legal counsel) rather than involving everyone for minor events.
    *   **Key Stakeholders:** Control system engineers, plant managers, HR, and external retainers (e.g., Dragos or Mandiant).
*   **Out-of-Band Communication:** Defenders must assume attackers can monitor internal email, Teams, or VOIP. Teams should use secure apps like **Signal** on personal phones for coordination.
*   **Tabletop Exercises:** Realistic simulations (like "Dungeons and Dragons" for security) used to test the response plan.
    *   **Injects:** Adding new clues or challenges, such as a "fake reporter" calling to see if employees leak information.

---

### **V. Phase 2: Identification & Detection Tools**
*   **SIEM (Security Information and Event Management):** A central location to store and analyze event data from firewalls, EDR, and PLCs.
    *   **Context is King:** An event (e.g., a car driving away) isn't "bad" without context (e.g., was it the owner or a thief?).
    *   **Unified Monitoring:** Ideally, IT and OT data roll up into a single view for the entire environment.
*   **Network Security Monitoring (NSM):**
    *   **Traffic Types:** Unicast (1-to-1), Broadcast (1-to-all), and Multicast (1-to-some).
    *   **Visibility Tools:**
        *   **Managed Switches:** Require **Span Ports/Port Mirroring** to send copies of all traffic to a monitoring sensor.
        *   **Netflow:** Tracks IP addresses and ports to find patterns over time; more affordable than full packet capture.
*   **The Encryption Dilemma:** Encrypting traffic within an OT network makes monitoring nearly impossible without expensive tools to "break" the encryption. In OT, it is often safer to leave internal traffic unencrypted for easier detection.
*   **EDR (Endpoint Detection and Response):** Tools like CrowdStrike or Windows Defender that monitor processes and file changes at the operating system level.

---

### **VI. Indicators of Compromise (IOCs) & MITRE ATT&CK**
*   **IOCs:** Evidence of an attack, such as IP addresses, domain names, or **file hashes** (digital fingerprints).
    *   **Stale Data:** IP and domain IOCs often lose value after 30 days as they are cleaned up by owners.
*   **Pyramid of Pain:** File hashes are easy for attackers to change (by altering one bit), but **Tactics, Techniques, and Procedures (TTPs)** are the hardest to change.
*   **MITRE ATT&CK for ICS:** A matrix used to categorize what attackers do once they gain access. It serves as a "Bible" for both defense and penetration testing.

---

### **VII. Honeypots & Threat Hunting**
*   **Honeypots:** Fake systems (e.g., a virtual PLC) designed to look like real targets.
    *   **High Fidelity Alert:** Because no one should ever be talking to a Honeypot, any activity is 99.9% likely to be malicious.
*   **Threat Hunting:** Proactively searching the network under the assumption that an attacker is **already inside**.

---

### **VIII. Phases 3–6: Responding to an Incident**
*   **Containment:** Determining if a system can be disconnected. In OT, you **must consult engineers** first to ensure disconnecting a system won't cause a plant shutdown or a safety hazard.
*   **Eradication:** Identifying the entry point, resetting all passwords, and rebuilding compromised systems **while the network is offline**.
*   **Recovery:** Bringing the plant back online safely. Monitoring should remain in an "elevated state" for several months afterward.
*   **Lessons Learned:** Meeting after a breather to identify gaps and create an **Action Plan**. Success is measured by holding people accountable to these improvements so the same attack cannot happen again.

### **I. Standards vs. Regulations**
It is critical to distinguish between best practices and legal mandates:
*   **Industry Standards:** These are **suggestions and best practices** created by industry groups (engineers, technicians, and security professionals). There is no law requiring adherence to a standard, but they are essential for improving security posture.
*   **Regulations:** These are **legal mandates** from government entities (federal, state, or municipal). Failure to comply can result in heavy fines, site shutdowns, or even prison time. 
*   **Legal Disclaimer:** Only **lawyers** can provide definitive answers on whether an organization meets a specific legal regulatory requirement.

---

### **II. NIST 800-82 (The US Government Standard)**
NIST 800-82 is a free, comprehensive standard funded by the US government.
*   **Version 3:** The latest version (released in late 2023) is over 300 pages and serves as a detailed checklist for security controls.
*   **Utility:** It provides a solid "OT Overview" in the first 30 pages, making it an excellent high-level introduction to the field.
*   **Building a Program:**
    *   **The Business Case:** Security must be sold to leadership by highlighting **safety, environmental protection, and operational uptime**. 
    *   **The ROI of Security:** Security tools often find operational/performance issues that help a plant run more efficiently, which is a major selling point to executives.
    *   **The Charter:** A cybersecurity program requires a formal policy (Charter) authorized by the highest level of executive leadership (CEO) to ensure it receives proper budget and resources.
*   **Risk Management:** Focuses on identifying threats, assessing probability/impact, and tracking them in a **Risk Register**.
*   **Special Considerations:**
    *   **Supply Chain:** Highlights risks like the **SolarWinds attack**, where attackers compromised software updates to gain access to thousands of organizations.
    *   **Safety Systems (SIS):** Emphasizes protecting the fail-safe backups that shut down a plant during an emergency.

---

### **III. ISA/IEC 62443 (The "Gold Standard")**
This is an internationally recognized suite of standards developed jointly by the International Society of Automation (ISA) and the International Electrotechnical Commission (IEC).
*   **Structure:** It is not a single document but a family of **14 standards** broken into four categories: General, Policies & Procedures, System, and Component.
*   **Shared Responsibility:** Security is not just the job of one team; it requires a partnership between IT, OT, engineering, and maintenance personnel.
*   **Security Levels (SL):** Defines how much protection is needed based on the threat:
    *   **SL 1:** Protection against casual or coincidental violation (unintentional mistakes).
    *   **SL 2:** Protection against intentional violation using **simple means** (common ransomware).
    *   **SL 3:** Protection against intentional violation using sophisticated means.
    *   **SL 4:** Protection against **advanced nation-state actors**.
*   **Zones and Conduits:** The process of breaking a network into "Zones" based on functionality and defining the "Conduits" (communication paths) between them.
*   **Risk Assessments:**
    *   **High-Level:** Performed at the start of a project using architectural diagrams.
    *   **Detailed:** Intensive 4–5 day workshops involving 20–30 stakeholders to identify "worst-case" and "realistic" scenarios for every asset in a zone.

---

### **IV. Key Regulations and Other Standards**
*   **ISO 27001/27002:** Though IT-focused, it is valuable in OT for its emphasis on **Continual Improvement**—constantly evolving security as attackers evolve.
*   **NERC CIP:** A mandatory regulation in North America for any facility generating or transmitting **bulk power**. It carries heavy fines for non-compliance.
*   **CFATS (Chemical Facility Anti-Terrorism Standards):** A US regulation for facilities holding "Chemicals of Interest" (COI) that could be used for sabotage or theft.
*   **TSA Security Directives:** Emerging regulations for **Pipeline and Rail** operators following the 2021 Colonial Pipeline breach.
    *   **Requirements:** Organizations must have a designated cybersecurity coordinator, incident response plans, and conduct regular vulnerability assessments.
*   **Water Sector:** While often vague, general requirements exist for ensuring the safety and availability of clean water, which implicitly includes cyber security to prevent unauthorized process changes.

### **V. Strategic Implementation**
*   **The Threshold of Tolerance:** Every business must decide its "risk threshold"—how much risk it is willing to accept versus how much it will spend to reach a specific Security Level.
*   **Continuous Monitoring:** Following a standard like NIST 800-82 or ISA/IEC 62443 can often make an organization 95% compliant with future regulations before they even become law.
*   **Operational Benefits:** Security programs often act as a **market differentiator**, allowing companies to prove they are more secure than their competitors.

---
#### **I. Standards vs. Regulations**
*   **Standards:** These are **best practices and suggestions** developed by industry experts (e.g., ISA/IEC 62443, NIST 800-82). No law requires adherence to a standard, but they are essential for improving security posture.
*   **Regulations:** These are **legal mandates** from government entities (federal, state, or municipal). Failure to comply can result in heavy fines, shutdowns, or prison time.
*   **Legal Note:** Only **lawyers** can definitively confirm if an organization meets legal regulatory requirements.

#### **II. NIST 800-82 (The US Government Standard)**
*   **Overview:** A free, comprehensive standard funded by the US government. 
*   **Version 3:** Includes an "OT Overview" (first 30 pages) that serves as an excellent high-level introduction to the field. 
*   **Building a Program:**
    *   **The Business Case:** Security must be sold to leadership by emphasizing **safety, environmental protection, and operational uptime**.
    *   **ROI:** Security tools often identify operational/performance issues that help a plant run more efficiently—a major selling point for executives.
    *   **The Charter:** A program requires a formal policy (Charter) authorized by high-level leadership (CEO) to ensure it receives proper budget and resources.
*   **Supply Chain & Safety:** Version 3 highlights risks like the **SolarWinds attack** (compromised software updates) and the need to protect **Safety Instrumented Systems (SIS)**.

#### **III. ISA/IEC 62443 (The "Gold Standard")**
*   **Structure:** An internationally recognized family of **14 standards** categorized into General, Policies & Procedures, System, and Component sections.
*   **Shared Responsibility:** Requires partnership between IT, OT, engineering, and maintenance.
*   **Security Levels (SL):** Ranges from **SL 1** (protection against casual mistakes) to **SL 4** (protection against advanced nation-state actors).
*   **Foundational Requirements (FR):** Seven key areas, including Identification and Authentication, Use Control, System Integrity, and Data Confidentiality.
*   **Risk Assessments:**
    *   **High-Level:** Performed at project start using architectural diagrams.
    *   **Detailed:** Intensive workshops (4–5 days) involving 20–30 stakeholders to identify specific risks for every asset in a zone.

#### **IV. Specific Regulations**
*   **NERC CIP:** Mandatory regulation for any facility in North America that generates or transmits **bulk power**.
*   **CFATS:** US regulation for facilities holding **Chemicals of Interest (COI)** that could be targets for sabotage or theft.
*   **TSA Security Directives:** Legal requirements for **Pipeline and Rail** operators following the Colonial Pipeline breach.
*   **Water Sector:** Though often vague, general requirements mandate the safety and availability of clean water, which implicitly includes cyber protection.

---

### **Part 10: Introduction to ICS/OT Penetration Testing**

This final content section covers how to safely and ethically test the defenses of a control system environment.

#### **I. Authorization and Legal Considerations**
*   **Permission:** Explicit authorization from the **asset owner** is mandatory. Testing without it is illegal, making you "just another attacker".
*   **Scope:** Testers must stay strictly within the agreed-upon scope. Crossing into the OT network when only the DMZ was authorized can lead to legal issues or termination of the contract.
*   **Safe Testing:** Testing is often performed in a **lab environment** or against a backup site to avoid impacting the availability of a production plant.

#### **II. Suggested Resources and Books**
*   ***Hacking Exposed: Industrial Control Systems***: Considered a foundational text for understanding ICS exploitation.
*   ***Pentesting Industrial Control Systems* (Paul Smith)**: Focuses on building virtualized control networks and uses the Click PLC as a learning target.

#### **III. The Pentest vs. Maturity Debate**
*   **Fundamentals First:** Most organizations do not need a pentest immediately. They should first implement fundamentals: **secure network architecture, asset registers, monitoring, and vulnerability management**.
*   **ROI of Security:** Architecture reduces more risk for less money than an expensive pentest. A pentest is typically the **final step** in a cybersecurity maturity roadmap.

#### **IV. Historical Incidents as Case Studies**
*   **Ukraine 2015 Blackout:** Attackers used phishing for initial access, reconfigured UPS backups (to ensure the plant stayed dark during the fix), and used "KillDisk" to wipe engineering workstations after flipping breakers.
*   **Ukraine 2022 Blackout:** A more advanced attack using **"Living off the Land" (LOTL)** techniques. Attackers used built-in OS commands and legitimate software (MicroSCADA) to turn off power rather than custom malware, making detection difficult.

#### **V. Pentest Methodology (Miter ATT&CK for ICS)**
The video adapts the Miter framework into a flow that includes:
*   **Reconnaissance & OSINT:** Finding exposed assets using **Shodan, Census, and SNMP walking**.
*   **Initial Access:** Pivoting from the IT network (the #1 way), using infected USBs, or exploiting internet-exposed PLCs.
*   **Discovery:** Mapping the network to find data historians, HMIs, and PLCs.
*   **Collection:** Gathering specific data like PLC **Operating Modes**.
    *   *Note:* A PLC in **Run Mode** is more secure than in Program Mode, but it may still allow logic changes.
*   **Impact:** The ultimate goal is **loss of visibility** (blinding operators) and **loss of control** (manipulating the physical process).

#### **VI. Modern Tools: LOTL and Chat GPT**
*   **Living off the Land:** Using built-in tools like **Powershell** ensures that the attacker doesn't need to download suspicious files like Nmap that could trigger alerts.
*   **Chat GPT:** Can be used to quickly generate custom offensive and defensive scripts, such as Python scrapers for exposed PLC pages or Powershell port scanners.

---
