# What is Cybersecurity 
Protecting Networks, systems, and data from digital threats.

# CIA Triad

# What is the CIA Triad?
It is the Goal for Cybersecurity
The CIA Triad is a fundamental model for information security, representing the three primary goals:

- `Confidentiality`: Protecting sensitive information from unauthorized access. (FA,2FA,MFA,Encryption, ACL)
- `Integrity`: Ensuring data remains accurate and unaltered. (Hashing,Digital Signature, Certificate,checksum)
- `Availability`: Ensuring authorized users have reliable access to information when needed. (Redundancy,fault tolerance, patching,backup,load balancers)  

---
# Defense in Depth Stratergy
- `Physical Security`: Guards, CCTV, biometric access  for physcial assets.
- `Network Security`: Firewalls and IDS, IPS, etc... 
    - `Integrity`: Protecting data from unauthorized changes.
    - `Confidentiality`: Ensuring only authorized access to sensitive data.
    - `Availability`: Guaranteeing reliable access to network resources.
    - `Understanding Firewall`
        - Packet-Filtering: Inspect individualpackets based on criteria like IP addresses and ports.
        - Stateful Inspection: Tracks connection states for better threat detection.
        - Next-Generation firewall(NGFW): Integrate IPS, DPI, XDR and application monitoring.
    - `Network Segmentation`:
        - Splitting Networks into sectors for more protection is called as segmentation.
        - It can be done with the help of a firewall or various networking devices and implementing a firewall between the connection between the access point for that part of network so that it doesn't get accessed easily by anyone.

            - `DMZ`: Houses public services, separated from the internal network.
            - `Internal Networks`: Protects sensitive data with restricted external access.

    - `IDS and IPS`:
        - `IDS`: Monitors traffic, Generates alerts for potential threats.
        - `IPS`: Actively blocks or mitigates detected threats.
    - `Various detection methods`:
        - `Signatures based`: a common signature is used to identify attacks(hashes for known malware kinds).
        - `Anomaly-based`: based on how it works and its behavior(behavioral analysis)
        - `Stateful Protocol Analysis`: Examin the traffic against porotocol behavior, identify violation of RFC specifications or is abused to tunnel malicious data.
        - `Reputation-based detection`: Cross-references communicating IP addresses, domains, and URLs against global threat intelligence feed to block connections to known C2 servers and malicious infrastructures.
- `Endpoint Security`: Antivirus software and host-based firewalls for individual devices.
    - Endpoint security portects individual devices connected to a network. its done to ensure data confidentiality, integrity and availability for endpoint devices.
    - `Various Detection method`:
        - `signature-based scanning`: checking files to known signatures, low-overhead detection.
        - `heuristic analysis`: Detect new malware by analyzing suspicious behaviors(with static rules).
        - `behavioral monitoring`: monitor Detect malware by programs behavior(with dynamic analysis)
        - `machine learning & predictive AI`: leverage analysis and triage with AI and ML.
        - `Sandbox detonation & emulation`: execute the suspicious files in an isolated virtual environment to observe their true functional capabilities.
    - `EDR`: Continuously monitors endpoint activity for threats and provide real-time responses, often automated to isolate threats and analyzes how threats entered and actions taken.
    - `Firewall and Intrusion Detection`: Control network traffic based on rules and monitor for malicious activity like file changes(HIDS).
    - `Mobile Device Security`:  Enforce policies like encryption and remote wipe(MDM solutions). Whitelist and blacklist apps and protect against social engineering attacks.
    - `IoT Security`: update the firmware and isolate IoT devices from critical systems, ensure only authorized devices connect.
    - `Challenges`: Evolving Threats, Performance impact, user behavior.
---
# Combining CIA Triad and Defence-in-Depth
- `Multiple-Layers`:  Implement various security measures to protect against diverse threats.
- `Comprehensive Protection`: Address confidentiality, integrity, and availability at each security layer.

---
# Threat vs Risk vs Vulnerabilities

- `Vulnerability`: Vulnerable means susceptible to attack or damage. In information security, a vulnerability is a weakness.
- `Threat`: A threat is a potential danger associated with this weakness or vulnerability.
- `Risk`: The risk is concerned with the likelihood of a threat actor exploiting a vulnerability and the consequent impact on the business.

---

# Types of Attacks by Hackers

## Overview of Attack Types

- `OSINT`: Open-Source Intelligence; gathering publicly available information.
- `DDoS`: Distributed Denial of Service; overwhelming a service with traffic to make it unavailable.
- `Phishing`: Deceptive attempts to steal credentials or personal information by impersonating trustworthy entities.
- `Reconnaissance`: Collecting information about a target to exploit vulnerabilities.
- `Man-in-the-Middle (MITM)`: Intercepting communication between two parties to steal or alter information.
- `Password Cracking`: Using various techniques to discover passwords.
- `Privilege Escalation`: Exploiting a system vulnerability to gain higher privileges.
- `Exfiltration`: Unauthorized transfer of data from a system.

---
# Cybersecurity Roles and Responsibility
- `Cybersecurity Analysts`: Monitor Network activity and respond to threats.
    - `Monitor Network activity`: Use SIEM systems to identify suspicious behavior or anomalies
    - `Incident Detection and Response`: Detect Potential security incidents and take action to mitigate them.
    - `Analyze logs and reports`: Review logs from security tools to identify potential threats.
    - `Implement Security Measures`: Recommend and implement security enhancements based on observed threats.
- `Penetration Testers`: Simulate Cyberattacks to find vulnerabilities.
    - `Vulnerability Assesments`: Identify potential security gaps in applications,networks and systems.
    - `Simulate attacks`: to test the effectiveness of security measures.
    - `Report findings`: Provide detailed reports on vulnerabilities and recommend improvements.
    - `Compliance Testing`: Ensure the organization's security posture meets regulatory requirements.
- `Security Architects`: Design secure network and infrastructures.
    - `Develop Security Policies`:  Establish guidelines for securing information systems.
    - `Network Design`: Create secure network architectures, including firewalls, IPS, and VPNs.
    - `Risk Assessment`: Evaluate risks associated with new technologies or network changes.
    - `Continuous improvement`: Regularly update security measures to address emergin threats.
- `Incident Responder`: Manages and responds to security breaches.
    - `investigate Incidents`: Analyze the cause, scope, and impact of security breaches.
    - `Mitigate Threats`:  Take Immediate actions to limit the damage of an incident
    - `Recovery and Remediation`: Assist in restoring systems and implementing preventive measures.
    - `Documentation and Reporting`: Document incidents and lessons learned to improve future response efforts.
- `Chief Information Security Officer(CISO)`: Oversees the entire Cybersecurity strategy of an organisation.
    - `Strategic Planning`: Develop the Organization's Cybersecurity policies and procedures.
    - `Budget Management`: Allocate resources for cybersecurity initiatives.
    - `Compliance Oversight`: Ensure Adherence to data protection regulations and standards.
    - `Executive Communication`: Report to the executive board on cybesecurity risks and strategies.
- `Security Engineer`: Builds and maintains security systems and tools.
    - `System Design`: Create secure configurations for networks and applications.
    - `Tool Development`: customize security tools to meet the organization's specific needs.
    - `Performance Monitoring`: Ensure that security systems perform optimally.
- `Forensic Analysts`: Takes all the evidence left in after an incident(digital fingerprints) and analyze to find the attacker or their tactics.
    - `Digital Evidence Collection`: Acquire and preserve digital evidence from compromised systems.
    - `Analysis of Attack Methods`: Determine the TTP used by attackers.
    - `Legal Documentation`: Document findings to support legal actions or regulatory requirements.
---
# Ethical and Legal Aspects
- `Ethical Hacking`: Testing Security with permission to identify vulnerabilities. (black,grey,white)
- `Data Privacy Laws`: Regulations like GDPR set guidelines for handling personal data.
- `Compliance`: companies must adhere to regulations to avoid penalities.

## Ethical Principles
- `Confidentiality`: Respect privacy and prevent unauthorized disclosure of information.
- `Integrity`: Ensure data accuracy and reliability, avoiding misinformation or tampering.
- `Availability`: Maintain system accessibility and avoid unjustified service disruptions.
- `Accountability`: Take responsibility for actions and rectify issues when mistakes occur.

## Legal Framework: GDPR
- `Consent`: Obtain Permission before collecting personal data.
- `Access Rights`:  Allow individuals to access and delete their data.
- `minimization`: collect only necessary data.
- `Penalties`: Substantial fines for violations

## Legal Framework: HIPAA & CFAA
- `HIPAA`: Pretects health information in the US. Requires safeguards, limited access, and prompt breach reporting.
- `CFAA`: Addresses computer-related offenses like unauthorized access and harmful software transmission. used to prosecute cybercriminals.

## Ethical Dilemmas
- `Zero-Day Vulnerabilities`: Should professionals disclose vulnerabilities that could be used maliciously?
    - `Private Reporting`: Report vulnerabilities to affected organization privately.
    - `Remediation Time`: Allow time for fixes before public disclosure.
    - `Bug Bounty Programs`: incentivize ethical hacking.
- `Government Surveillance`: Should experts participate in activities that may infringe on privacy rights?
- `Whistle blowing`: exposing wrong doings of government is a conflict between ethicality and legal obligation.

---
# SIEM(Security Information and Event Management)
- A central location to store and analyze event data from firewalls, EDR, and PLCs.
- Collects data from various sources like network devices and servers.
- Generates alerts for threats and reports for Compliance
- Identifies patterns and relationships to detect security incidents.

---
# Log Management
- Gather Logs from diverse sources like firewalls and servers.
- Ensure log storage for compliance and analysis.
- Sources should be easily traceable when it comes to logs.
---
# DAD
The security of a system is attacked through one of several means. It can be via the disclosure of secret data, alteration of data, or destruction of data.

- Disclosure is the opposite of confidentiality. In other words, disclosure of confidential data would be an attack on confidentiality.
- Alteration is the opposite of Integrity. For example, the Integrity of a cheque is indispensable.
- Destruction/Denial is the opposite of Availability.

The opposite of the CIA Triad would be the DAD Triad: Disclosure, Alteration, and Destruction.

Consider the previous example of patient records and related systems:

- Disclosure: As in most modern countries, healthcare providers must maintain medical records’ confidentiality. As a result, if an attacker succeeds in stealing some of these medical records and dumping them online to be viewed publicly, the health care provider will incur a loss due to this data disclosure attack.
- Alteration: Consider the gravity of the situation if the attacker manages to modify patient medical records. This alteration attack might lead to the wrong treatment being administered, and consequently, this alteration attack could be life-threatening.
- Destruction/Denial: Consider the case where a medical facility has gone completely paperless. If an attacker manages to make the database systems unavailable, the facility will not be able to function properly. They can go back to paper temporarily; however, the patient records won’t be available. This denial attack would stall the whole facility.

Protecting against disclosure, alteration, and destruction/denial is of utter significance. This protection is equivalent to working to maintain confidentiality, Integrity and availability.

Protecting confidentiality and Integrity to an extreme can restrict availability, and increasing availability to an extreme can result in losing confidentiality and Integrity. Good security principles implementation requires a balance between the three.


---
# Parkerian Hexad

In 1998, Donn Parker proposed the Parkerian Hexad, a set of six security elements. They are:

- Availability
- Utility
- Integrity
- Authenticity
- Confidentiality
- Possession

We have already covered four of the above six elements. Let's discuss the remaining two elements:

- Utility: Utility focuses on the usefulness of the information. For instance, a user might have lost the decryption key to access a laptop with encrypted storage. Although the user still has the laptop with its disk(s) intact, they cannot access them. In other words, although still available, the information is in a form that is not useful, i.e., of no utility.
- Possession: This security element requires that we protect the information from unauthorized taking, copying, or controlling. For instance, an adversary might take a backup drive, meaning we lose possession of the information as long as they have the drive. Alternatively, the adversary might succeed in encrypting our data using ransomware; this also leads to the loss of possession of the data.

---

# DDoS (Distributed Denial of Service)

## What is DDoS?

A DDoS attack overwhelms a network, server, or service with a flood of traffic, making it unusable for legitimate users.

## Types of DDoS Attacks

- Volumetric Attacks: Saturating bandwidth with fake traffic.
- Application Layer Attacks: Targeting specific applications to exhaust server resources.
- Protocol Attacks: Exploiting vulnerabilities in network protocols like SYN flooding.

> [!important]  
> can be automated using BOTNET  

## Dos

It is to make services or network folded with traffic but Dos is done with single terminal

  

Network Dos: overwellming network bandwidth

Application Dos: overwellming applicational resources like cpu, gpu etc..

operational technology Dos: targeting industrial devices like SCADA. OT’s, PLc’s  
(supervisory control and data requisition)  
(programable logic controllers)  

---

# Phishing

## What is Phishing?

Phishing is a cyber attack that uses disguised emails or messages to trick individuals into providing sensitive information.

## Types of Phishing

- Spam: Mass unsolicited emails.
- Spim: Spam sent over instant messaging.
- Credential Harvesting: Stealing usernames and passwords.
- Smishing: Phishing via SMS.
- Vishing: Phishing over voice calls.
- Whaling: Targeting high-profile individuals.
- Other Types: Deceptive tactics like clone phishing and spear phishing.

  

## Email Phising

  

1. mass mailing: public mailing
2. spearphishing: selective phishing
3. whaling: big fish phishing
4. pharming: poisoning the DNS cache of a device to redirect or do whatever attack the attacker likes

---

# Pretexting

## What is Pretexting?

Pretexting involves creating a fabricated scenario to manipulate someone into divulging sensitive information.

## Steps in Pretexting

1. Creating a Fake Story: Crafting a believable scenario to gain trust.
2. Gathering Information: Using social engineering to obtain personal or confidential details.
3. Exploiting Trust: Utilizing the obtained information for malicious purposes.

---

# Information Gathering/Reconnaissance

## What is Information Gathering?

- Active Recon: Direct interaction with the target to gather information (e.g., port scanning).
- Passive Recon: Collecting information without directly interacting with the target (e.g., social media research).

  

### Active Recon

- Port scanning
- vulnerability scanning
- enumeration
- social engineering to manipulate.

  

### Passive recon

- OSINT
- shoulder spoffing

---

# Website Attacks

## Types of Website Attacks

- SQL Injection: Injecting malicious SQL queries to manipulate databases.
- Cross-Site Scripting (XSS): Injecting scripts into websites that run in users' browsers.
- Cross-Site Request Forgery (CSRF): Forcing users to perform actions they didn't intend by exploiting their authenticated session.
- Directory Traversal: Accessing restricted directories on a web server.
- File Inclusion: Including malicious files via improper input handling.

---

### Typo Squatting

- What is Typo Squatting?: Registering misspelled versions of popular websites to trick users into visiting malicious websites.

---

### Prepending

- What is Prepending?: Adding malicious or deceptive content at the beginning of legitimate communication or code to mislead users.

---

### Watering Hole Attack

- What is a Watering Hole Attack?: Infecting commonly visited websites by the target group with malware to compromise visitors.

---

# Non-Repudiation

- What is Non-Repudiation?: Ensuring that a person or entity cannot deny the authenticity of their actions, such as sending a message or making a transaction.(a.ka trust by heart)
- can be trusted with Hash.

---

# Zero Trust

- What is Zero Trust?: A security model where no entity (internal or external) is trusted by default, and every action requires verification before granting access.

---
# Trust but Verify

- Trust but Verify: This principle teaches that we should always verify even when we trust an entity and its behaviour. An entity might be a user or a system. Verifying usually requires setting up proper logging mechanisms; verifying indicates going through the logs to ensure everything is normal. In reality, it is not feasible to verify everything; just think of the work it takes to review all the actions taken by a single entity, such as Internet pages browsed by a single user. This requires automated security mechanisms, such as , intrusion detection, and intrusion prevention systems

---
# How to Enhance Security in an Organization

## Adaptive Identity

Implement mechanisms to continuously authenticate users based on risk factors.  
examine the individual and apply security contol on based o their process and what the users is by position, place or the person.  

ex: if a chinese user trys to log-in to the DB can trace the connection to find who he is, or automate a stronger authentication if needed.

## Threat Scope Reduction

Minimize the attack surface by restricting unnecessary access and exposure.

ex: gain access to the network only by the people in that place or access through vpn and use MFA so Initial access is hard.

## Policy-Driven Access Control

Use dynamic policies to control access based on roles, behavior, and other risk factors.

## Security Zones

- What are Security Zones?: Dividing a network into segments to manage access and reduce the risk of compromise between trusted and untrusted zones.
- Make one or more network segments and create different policies and requlate the internal and external traffic with the policies.
- Seperation is created with Groups and VPN

# PEP, PDP, and Policy Engine Workflow

1. Policy Engine: Evaluates access policies.(comapares the sent or recieved data with the policy)
2. Policy Administrator: Enforces decisions from the policy engine.
3. Policy Enforcement Point (PEP): Intermediary that controls the flow of data between trusted and untrusted zones based on policies. (GATEKEEPER)
4. Policy Decision point (PDP): enforces policy by taking decisions to allow or not allow the data.
5. PEP: finds info of the data
6. PDP: Decides its fate. Consists policy administrator and policy engine.

  

|        |         |                      |        |     |
| ------ | ------- | -------------------- | ------ | --- |
|        |         | Policy Engine        |        |     |
|        |         | Policy Administrator |        |     |
|        |         | \| \|                |        |     |
| System | ——————> | PEP                  | —————> | DB  |
|        |         |                      |        |     |

---

  

# AAA Framework

Identification : say you are you.

Authorization : what you are allowed to do (authrization model, policies)

Authentication : prove that you are what you are. (hashing)

Accounting : logs of yours showing what have you done, every single actions of yours

  

In general AAA servers are presented in every network in front of the access given to the user and this does everything that it should and also it can be either centralized or decentralized.

  

client————>Internet————> VPN/Firewall———→Internal File System  
|  
|——> AAA server  

## Authorization Model

  

Says what is accessible and what is used by putting it in the middle getting the access to the internal network or the database.

it is either an authorization model or tons of policies that you have to either make or follow a certain policy premade and add it to you network or during the login access. Creating policies can be difficult, time consuming and also can be vulnerable.

Seperate users frin wgat they access

easy to set with simple abstraction

done by putting the required users in a group for staffs and students so teacher’s would be added in the teachers group and the students in the students group.

  

types of authorization model

Role-Based Access Control (RBAC) : assign user roles

Attribute-Based Access Control (ABAC) : characteristics like job, location, etc

Relationship-Based Access Control (ReBAC) : using relationship b/w user and the object

Discretionary Access Control (DAC) : give full acces to the object that hey own.

Zero Trust Network Access (ZTNA) : only what they need no more or no less.

  

---

# Response plan

  

plan to respond to attacks.  
consists preparation, identification,containment, eradication,recovery & learning.  

---

# Log analysis

analysing the logs in the firewall, application, network manager etc..

---

  

  

# Proxy Protocol

  

## HTTP

- hypertext transfer protocol
- send info in plain text
- readable so not secure

  

## HTTPS

- hypertext transfer protocol secure
- uses SSL
- hard to crack by anyone (hackers, goverment, ISP) anyone
- anonymous

  

## SOCKS

- Socket Secure
- flexible and work with various traffics
- use TCP and UDP
- used in livestreaming and gaming
- not as safe as HTTPS
- consist of v4 and v5

  

---

  

# VPN

  

it is known as Virtual Private Network which is used to hide your ip and make yourself anonymous by tunneling and also encrypt the data that is being send and even isp can’t go through it.

  

- Tunneling: VPN creates a "tunnel" between your device and a VPN server. This tunnel encrypts all your internet traffic, protecting it from eavesdropping or interception.
- Encryption: VPN uses encryption algorithms to scramble the data, so even if it’s intercepted, it can’t be read without the encryption key.
- IP Masking: VPNs mask your real IP address with the IP address of the VPN server, making it harder to trace your location or online activity.

  

### Key VPN Protocols:

Each protocol dictates how data is encrypted and transmitted. Some common VPN protocols include:

- OpenVPN:
    - Encryption: Uses SSL/TLS for key exchange, highly secure.
    - Usage: Open-source, commonly used due to its strong security and flexibility.
    - Strengths: High security, supports various encryption ciphers (AES, Blowfish).
    - Weaknesses: Requires third-party software, may have slower speeds depending on configuration.
- IKEv2/IPsec (Internet Key Exchange Version 2):
    - Encryption: Often paired with IPsec for encryption.
    - Usage: Works well with mobile devices, resilient to network changes (e.g., switching from Wi-Fi to mobile data).
    - Strengths: Stability, fast reconnects.
    - Weaknesses: Susceptible to blocking by firewalls.
- PPTP (Point-to-Point Tunneling Protocol):
    - Encryption: Uses basic encryption (128-bit keys), less secure.
    - Usage: One of the oldest protocols, known for speed but outdated in terms of security.
    - Strengths: Speed, easy setup.
    - Weaknesses: Weak encryption, vulnerable to attacks.
- L2TP/IPsec (Layer 2 Tunneling Protocol):
    - Encryption: Combines L2TP (for tunneling) with IPsec for encryption.
    - Usage: More secure than PPTP, but slower.
    - Strengths: Strong encryption.
    - Weaknesses: Slower speeds due to double encapsulation.
- WireGuard:
    - Encryption: Modern, lightweight protocol using state-of-the-art cryptography.
    - Usage: Open-source, high performance, minimal overhead.
    - Strengths: Extremely fast, secure, easy to audit.
    - Weaknesses: Still relatively new, not widely adopted yet.

  

### Tips while Working using VPN for Hackers:

- IP Hopping: Hackers may rotate between multiple VPN servers to make tracking more difficult. Each switch results in a new IP, further obfuscating their activities.
- Logless VPNs: Ethical hackers prefer VPN services that don’t keep logs of user activity, ensuring no records can be accessed by authorities or leaked.
- Encryption for Sensitive Data: VPNs ensure that sensitive information (such as credentials, exploits, or vulnerability reports) being transmitted over the network remains encrypted and secure from potential interception by malicious actors.

  

### Threats & Limitations of VPNs:

- VPN Leakage: Sometimes, VPNs may leak data such as DNS requests or even IP addresses, which could expose hackers during a penetration test or investigation.
- Trust in VPN Provider: If the VPN provider logs activity or shares data with authorities, the user may lose their anonymity.
- Vulnerable Protocols: Older VPN protocols (like PPTP) are easier to crack, making them unsuitable for sensitive operations.

  

### VPN Internals – Under the Hood & Vulnerabilities for Hackers

#### How VPN Works – Internal Architecture:

A VPN works by creating a secure, encrypted connection between the user’s device and a remote server. Here’s how it looks under the hood:

1. Client-Side:
    - VPN Software: Installed on the client device (PC, smartphone, etc.). This software manages VPN protocols, encryption, and the secure tunnel setup.
    - Encryption Process: Data packets generated by the device (e.g., browsing, sending emails) are encrypted using a pre-defined encryption method (AES, RSA, etc.).
    - Packet Encapsulation: The encrypted data is encapsulated into another packet (outer packet) and routed through the VPN tunnel to the VPN server.
2. Tunnel Establishment:
    - Handshake: The VPN client and VPN server exchange keys (using SSL/TLS, DH, or other protocols) to authenticate each other and establish a secure tunnel.
    - Encryption Keys: Once authenticated, both parties agree on encryption keys to secure the traffic.
    - Data Transmission: The encrypted data is then sent through the secure tunnel over the internet. The data is hidden within the encrypted tunnel (tunneling protocols: OpenVPN, WireGuard, etc.).
3. Server-Side:
    - Decryption: The VPN server receives the encrypted packets, decrypts them using the shared key, and forwards the packets to the destination (e.g., website, network service).
    - Response Handling: Any response from the destination server (like a web page) goes back through the VPN server, gets re-encrypted, and is sent back to the client through the tunnel.
4. Key VPN Components:
    - Authentication: Secure user authentication through protocols like SSL/TLS, PSK, or certificates.
    - Encryption Algorithms: Common algorithms like AES-256, RSA, and ChaCha20 ensure data confidentiality.
    - Transport Protocol: Either TCP (reliable, slower) or UDP (faster, less reliable) is used for communication.

  

#### How Hackers Can Attack VPN Connections:

Although VPNs provide strong security, there are still potential vulnerabilities that hackers can exploit.

##### 1. VPN Exploits:

Hackers may attempt to exploit vulnerabilities in the VPN infrastructure:

- Exploiting Weak Protocols:
    - PPTP: Hackers can break weak encryption algorithms like MS-CHAPv2 used in PPTP (Point-to-Point Tunneling Protocol). This is an outdated protocol, and tools like _ASLEAP_ can be used to crack the authentication.
    - IPsec Vulnerabilities: While IPsec is secure, certain configurations, such as using weak Diffie-Hellman groups for key exchange, can be cracked by attackers.
- Man-in-the-Middle (MITM) Attacks:
    - Intercepting VPN Traffic: If the attacker has access to the same network as the victim (like on public Wi-Fi), they can attempt a MITM attack by creating fake DNS or intercepting the initial handshake between the client and VPN server.
    - Downgrade Attacks: Hackers may force the client to use weaker VPN protocols (like PPTP instead of OpenVPN) and crack the session using weaker encryption methods.
- DNS Leaks:
    - DNS Traffic Exposure: Some VPNs may suffer from DNS leaks where DNS queries are routed outside the encrypted tunnel, allowing attackers to intercept and monitor DNS requests.
    - DNS Poisoning: If DNS traffic is leaked, hackers can perform DNS poisoning attacks, redirecting users to malicious websites.
- Exploiting VPN Clients:
    - Outdated Software: Many VPN clients have vulnerabilities if not regularly updated. Attackers could exploit buffer overflows or remote code execution flaws to compromise the VPN client.
    - Malware in VPN Clients: Compromised VPN clients (especially free or pirated versions) can contain backdoors or malware, allowing attackers to spy on the user’s data even while they believe they’re protected.

##### 2. Breaking Encryption:

- Brute Force Attack on Keys: VPNs using weak encryption keys (short key lengths) are susceptible to brute force attacks. With sufficient computational power, hackers can guess the encryption key and decrypt traffic.
- Quantum Threat: While currently theoretical, quantum computers may be able to break widely used encryption methods (like RSA) in the future.

##### 3. Compromising the VPN Server:

- VPN Server Vulnerabilities: If a hacker gains control over a VPN server (via a vulnerability, misconfiguration, or credential theft), they can:
    - Decrypt Traffic: Since the server has access to the encryption keys, the hacker can decrypt and monitor user traffic.
    - Insert Malicious Content: Hackers can modify the responses from legitimate websites, injecting malware into the victim’s data stream.

##### 4. Social Engineering & Phishing:

- Fake VPN Software: Hackers might trick users into downloading fake VPN apps that mimic legitimate services but secretly log traffic or send data to malicious servers.
- Phishing for VPN Credentials: If hackers obtain login credentials through phishing or credential stuffing, they can compromise the VPN account and monitor the victim’s traffic.

  

### Can Hackers Bypass a VPN?

While VPNs provide strong encryption and security, they are not invulnerable. Hackers can potentially bypass or compromise a VPN by:

1. Exploiting Weak Protocols: Using tools to crack weak encryption algorithms.
2. Attacking the VPN Server: If hackers compromise the VPN server, they can monitor or modify user traffic.
3. Targeting VPN Leaks: Exploiting DNS, WebRTC, or IPv6 leaks to bypass VPN coverage.
4. Compromising the End Device: Malware or direct access to the victim’s device renders VPN protection moot.

However, with robust VPN protocols (like OpenVPN, WireGuard) and strong encryption (AES-256), it is difficult for hackers to directly break into a secure VPN connection itself without resorting to other indirect methods like social engineering, device compromise, or server attacks.

  

---

  

# Onion Routing

  

## What is Onion Routing?

Onion routing is a technique for anonymous communication over a computer network. It was originally designed by the U.S. Navy to protect sensitive government communications. Today, the most famous implementation of onion routing is Tor (The Onion Router), used for secure, anonymous internet browsing.

- Onion Routing: Data is encrypted in multiple layers, like layers of an onion, and is routed through several intermediate nodes (called relays). Each relay only knows the immediate predecessor and successor but not the entire route or destination.
- Tor (The Onion Router): An open-source software that enables anonymous communication by implementing onion routing to hide a user’s location and usage patterns.

  

## How Onion Routing Works – Under the Hood:

1. User Request: When a user initiates a request to access a website via Tor:
    - The Tor client selects a random path of at least three relays (entry node, middle node, exit node) from the Tor network.
2. Layered Encryption:
    - The request is encrypted multiple times before it is sent. Each layer of encryption corresponds to one of the relays along the path.
    - The outermost layer can only be decrypted by the first relay (entry node), the second layer by the middle relay, and the final layer by the exit node.
3. Routing the Data:
    - Entry Node: The client’s request first goes to the entry node. This node can see the IP address of the user but does not know the final destination or contents of the data.
    - Middle Node: The request is forwarded to a middle relay, which further decrypts the data, without knowing the origin or final destination.
    - Exit Node: The last relay (exit node) decrypts the innermost layer, revealing the destination website or server. However, the exit node cannot see the user’s IP address or the original data.
4. Returning Data:
    - The response from the destination (e.g., a web server) goes back through the same relays in reverse, each one encrypting it in layers. By the time it reaches the user, only the user’s Tor client can fully decrypt the response.

- Key Terms:
    - Entry Node: First relay in the circuit, knows the user’s IP.
    - Middle Node: Intermediate relay that forwards traffic without knowing the user or the destination.
    - Exit Node: Final relay that decrypts and forwards traffic to the destination (e.g., a website).

  

## Protocols Used in Onion Routing (Tor):

- TLS (Transport Layer Security): Tor uses TLS for its encrypted tunnels between relays, ensuring secure communication.
- RSA: Public-key cryptography (RSA) is used to establish secure connections and for the encryption of session keys between relays.
- AES (Advanced Encryption Standard): AES is used to encrypt communication between relays for faster and secure data transfer.
- Diffie-Hellman: This is used for secure key exchange during the setup of circuits between the client and relays

  

## Vulnerabilities of Tor:

While Tor provides significant anonymity, it is not without its flaws. Some vulnerabilities that hackers or authorities may exploit include:

### 1. End-to-End Timing Attacks:

- Attackers may attempt to correlate the timing of traffic entering and leaving the Tor network. By analyzing the timing patterns, they could deanonymize users.
- Mitigation: Randomized delays and circuit changes within Tor, but the risk persists.

### 2. Exit Node Monitoring:

- Exit Nodes are a critical point of vulnerability since they can see unencrypted traffic sent to the final destination. Malicious exit nodes can sniff sensitive data (HTTP traffic, email, etc.).
- Hackers' Exploit: Attackers can run malicious exit nodes to intercept traffic, monitor users, or inject malicious content.
- Mitigation: Use HTTPS or encrypted protocols end-to-end, even within the Tor network.

### 3. Traffic Correlation:

- Advanced attackers (like governments) can monitor traffic at both the entry and exit nodes and attempt to correlate patterns to deanonymize users.
- Hackers’ Exploit: By monitoring entry points to Tor and exit points to the internet, they can try to link the incoming and outgoing traffic.
- Mitigation: Constantly switching relays and ensuring large-scale usage of the Tor network to make such attacks difficult.

### 4. Sybil Attacks (Relay Manipulation):

A Sybil attack occurs when a hacker runs a large number of Tor relays simultaneously to try and control enough of the network to deanonymize users.

- How it Works:
    - Hackers set up multiple malicious nodes in the Tor network. If they manage to control enough nodes, they can potentially see both the user’s IP (from the entry node) and the destination traffic (at the exit node).
    - By increasing their share of nodes in the network, the attacker increases the probability that users will choose their relays for their Tor circuits.
- Risk:
    - The attacker could deanonymize users by correlating the traffic from their controlled nodes.
    - If both the entry and exit nodes in a circuit are under the attacker's control, they can directly link the user’s IP to their activities.
- Example: In 2020, it was discovered that over 23% of Tor exit relays were controlled by malicious actors trying to conduct Sybil attacks and monitor user traffic.
- Defense: The Tor network tries to prevent Sybil attacks by detecting unusual relay behavior and banning malicious nodes. The randomness in node selection and regular rotation of circuits also helps mitigate the risk.

### 5. Tor Browser Exploits:

- Vulnerabilities in the Tor Browser (such as JavaScript exploits) can reveal a user’s real IP address.
- Hackers' Exploit: By exploiting browser vulnerabilities (e.g., malicious JavaScript), hackers can run malicious code that circumvents the protection provided by Tor.
- Mitigation: Tor Browser often disables JavaScript, but exploits may still occur. Keeping the browser and extensions updated is crucial.

### 6. Guard Node Attacks:

- The entry node (guard node) is the only node that knows the user’s real IP address. A malicious or compromised guard node could deanonymize users.
- Hackers' Exploit: If a hacker controls or compromises the guard node, they can trace users by associating their IP address with the encrypted traffic.
- Mitigation: Tor automatically rotates guard nodes periodically to reduce risk.

### 7. Eavesdropping on Public Wi-Fi:

- Using Tor over public Wi-Fi poses additional risks if attackers control the Wi-Fi access point.
- Hackers' Exploit: Hackers can conduct man-in-the-middle (MITM) attacks on public networks, injecting malicious content or monitoring unencrypted traffic.
- Mitigation: Always use HTTPS or other end-to-end encryption protocols.

### 8. Malware:

- Malware installed on a user's machine can bypass Tor and reveal the user’s identity by directly leaking information or using network connections outside of Tor.
- Hackers' Exploit: By distributing malware, hackers can monitor a user’s activity even if they use Tor.
- Mitigation: Use secure, updated operating systems (like Tails OS), avoid downloading files while using Tor, and scan for malware regularly.

  

### 9.  State-Level Attacks:

- Government agencies with vast surveillance capabilities may attempt to correlate traffic entering and leaving the Tor network.
- Example: The NSA has been known to monitor large portions of the internet and correlate Tor traffic with user activity.
- Possibility: Highly sophisticated and requires significant resources, but possible.

### 10. Compromised Relays:

- Hackers (or authorities) can run malicious relays (entry, middle, or exit nodes) and try to deanonymize users by analyzing traffic patterns.
- Example: In 2014, researchers found that malicious relays were being used to deanonymize Tor users in an attack targeting the Tor network.

### 11. JavaScript and Browser Exploits:

- Vulnerabilities in the browser can reveal a user’s real IP address, even when they are using Tor.
- Example: The FBI used a Firefox vulnerability in 2013 to deanonymize users of Tor hidden services in a child pornography investigation.

### 12. De-anonymization via Exit Nodes:

- Malicious exit nodes can sniff unencrypted traffic, capture credentials, and monitor sensitive communications.
- Example: Hackers have set up rogue exit nodes to collect unencrypted traffic or inject malicious content.

  

## How Hackers Might Attack Tor or Exploit It:
 
- Running Malicious Nodes: Hackers can set up multiple relays (entry or exit nodes) to try to monitor traffic and deanonymize users by analyzing patterns.
- Browser Exploits: Hackers may exploit vulnerabilities in the Tor browser or encourage users to enable JavaScript, allowing them to run malicious code and reveal user IP addresses.
- Traffic Analysis: If hackers control both the entry and exit points, they can use traffic analysis to trace users.
- Phishing & Social Engineering: Hackers may use phishing techniques to trick users into revealing sensitive information, bypassing the security offered by Tor.

## can TOR be hacked??

- Tor Network Attacks: Hard but possible with extensive resources (traffic correlation, compromised relays, etc.).
- Client-Side Exploits: Common attack method (JavaScript exploits, browser vulnerabilities, malware on user devices).

  

---

  

# Firewall

  
## What is Firewall  

firewall is a network security system that monitors and controls incoming and outgoing network traffic based on pre-defined security rules. Its main purpose is to act as a barrier between trusted internal networks and untrusted external networks (e.g., the internet), preventing unauthorized access and ensuring network security.  
  
  

## Types of Firewalls

1. Packet-Filtering Firewall:
    - How it Works: It inspects each packet passing through the network and allows or blocks them based on the source IP address, destination IP address, protocol, and port number.
    - Use Case: Provides basic filtering and is often used in routers.
2. Stateful Inspection Firewall:
    - How it Works: Tracks the state of active connections and makes decisions based on the context of traffic rather than individual packets. It allows traffic only if it is part of an established connection.
    - Use Case: Commonly used for managing TCP connections and ensuring legitimate session-based traffic.
3. Proxy Firewall (Application-Level Gateway):
    - How it Works: Acts as an intermediary between users and the internet, filtering requests at the application layer. It inspects traffic at the protocol level (e.g., HTTP, FTP) and can prevent direct connections between internal and external networks.
    - Use Case: Offers more advanced filtering, often used to control web traffic or email traffic.
4. Next-Generation Firewall (NGFW):
    - How it Works: Integrates traditional firewall features with additional functionalities like deep packet inspection (DPI), intrusion detection and prevention (IDS/IPS), and application awareness.
    - Use Case: Used in enterprise environments for advanced threat protection.
5. Unified Threat Management (UTM) Firewall:
    - How it Works: Combines various security functions (firewall, antivirus, VPN, content filtering, etc.) into one device, providing comprehensive network protection.
    - Use Case: Ideal for small to medium-sized businesses that need all-in-one security solutions.
6. Cloud Firewalls:
    - How it Works: Firewalls hosted in the cloud to protect cloud-based infrastructure, applications, and services. They offer scalable security for cloud environments.
    - Use Case: Used in modern cloud computing environments.

  

## Security Features of Firewalls

- Packet Filtering: Firewalls analyze the packets' headers (IP, port, protocol) and enforce rules to allow or deny them.
- Deep Packet Inspection (DPI): Analyzes packet contents, not just headers, to detect malicious data or rule violations.
- Stateful Inspection: Firewalls monitor active connections and ensure packets belong to a legitimate session.
- Intrusion Detection and Prevention (IDPS): Detects and blocks suspicious or malicious activities (e.g., port scans, brute-force attacks).
- Application Awareness: Firewalls can understand and filter traffic based on specific applications (e.g., allowing Skype but blocking BitTorrent).
- VPN Integration: Firewalls often support Virtual Private Network (VPN) functionality to allow secure remote access.

  

## Protocols in use

  

1. TCP: transmission control protocol
2. UDP: User Datagram Protocol
3. IP : Internet Protocol
4. ICMP: Internet Control Message Protocol
5. HTTP Hypertext Transfer Protocol
6. HTTPS: Hypertext Transfer Protocol secure
7. FTP: File Transfer Protocol
8. SMTP: Simple Mail Transfer Protocol
9. SNMP (Simple Network Management Protocol)
10. Telnet
11. SSH (Secure Shell)
12. RDP (Remote Desktop Protocol)
13. L2TP (Layer 2 Tunneling Protocol)
14. PPTP (Point-to-Point Tunneling Protocol)
15. IPSec (Internet Protocol Security)
16. SSL (Secure Sockets Layer) / TLS (Transport Layer Security)

  

## How Hackers Exploit Firewalls

Although firewalls provide essential security, hackers can exploit weaknesses or misconfigurations. Here are some ways a hacker might exploit a firewall:

1. Bypassing Through Open Ports:
    - How it Works: Hackers scan for open ports that are not adequately protected. If a service (e.g., HTTP, FTP) is running on an open port and the firewall allows traffic through it, attackers can exploit vulnerabilities in that service.
    - Example: If port 80 (HTTP) is open, an attacker may try to exploit a vulnerability in the web server.
2. Firewall Misconfigurations:
    - How it Works: Incorrect firewall configurations can expose the network to attacks. For example, if unnecessary ports are left open or inbound rules are too permissive, hackers can use these to gain entry.
    - Example: Allowing all inbound traffic from specific IP ranges might let malicious traffic through if the IP range is spoofed.
3. Firewalking:
    - How it Works: Firewalking is a technique used to map the rules of a firewall. By sending packets with incremental TTL (Time to Live) values, hackers can discover open ports and rules enforced by the firewall.
    - Exploitation: Once the hacker identifies which ports and protocols are allowed, they can focus their attacks on those services.
4. Port Scanning:
    - How it Works: Hackers use tools like Nmap to perform port scanning to identify open ports and services running behind the firewall. Once they identify open ports, they can exploit vulnerabilities in those services.
    - Defense: Firewalls can use port-knocking techniques to obscure open ports, only allowing traffic after a specific sequence of actions.
5. Application Layer Exploits:
    - How it Works: Even with a firewall in place, if an application (e.g., web server, database) is vulnerable, attackers can exploit weaknesses at the application layer, bypassing the firewall's protection.
    - Example: A SQL Injection vulnerability in a web application could allow an attacker to bypass the firewall completely.
6. Denial-of-Service (DoS) Attacks:
    - How it Works: Hackers can flood a firewall with massive amounts of traffic, overwhelming its processing capabilities and causing legitimate traffic to be blocked or degraded.
    - Tools: Low Orbit Ion Cannon (LOIC) or High Orbit Ion Cannon (HOIC) are common tools for launching DoS attacks.
7. IP Spoofing:
    - How it Works: Hackers can spoof the source IP address to bypass IP-based firewall rules. Firewalls that rely solely on IP addresses for filtering are vulnerable to IP spoofing.
    - Example: Attackers can impersonate a trusted IP to get through the firewall.
8. Exploiting Stateful Firewalls:
    - How it Works: Some firewalls rely on keeping track of the state of a connection. If an attacker is aware of the traffic patterns, they can send crafted packets that mimic valid sessions to bypass the firewall.
    - Example: Using TCP Split Handshake tricks the firewall into thinking the attacker's packets are part of an established connection.

  

## How Firewalls Work Under the Hood

1. Packet Inspection:
    - Firewalls inspect every packet of data passing through the network. Based on the header information (IP addresses, port numbers, protocol), the firewall decides whether to allow or deny the packet.
2. Rule Evaluation:
    - Firewalls have a set of rules (also called Access Control Lists, ACLs). The firewall matches each incoming and outgoing packet against these rules to decide whether to block or allow it.
    - Example rule: `ALLOW TCP traffic from IP 192.168.1.10 to port 80`
3. Stateful Packet Filtering:
    - Stateful firewalls track the state of active connections, allowing only packets that are part of an established session. This ensures that only legitimate traffic can pass through.
4. Logging:
    - Firewalls log traffic, especially denied packets. This logging is useful for auditing, intrusion detection, and forensic analysis.
5. Packet Dropping:
    - If a packet violates any rule (e.g., a suspicious IP, port, or protocol), the firewall drops it without forwarding it to the destination.

  

## How to Crack or Bypass a Firewall

1. Tunneling:
    - Hackers can bypass firewalls using tunneling protocols like SSH tunneling, VPNs, or DNS tunneling. These methods encapsulate malicious traffic inside legitimate traffic, bypassing the firewall's filtering.
2. Exploiting Open Ports:
    - Open ports (e.g., 80/443 for HTTP/HTTPS) often bypass firewall filtering. Attackers can craft exploits targeting services on these ports, as they are allowed through by default.
3. Social Engineering:
    - Hackers may convince a network administrator or user to change firewall settings (e.g., by sending phishing emails), leading to vulnerabilities in the configuration.
4. Bypassing with IPv6:
    - Some firewalls are misconfigured for IPv6 traffic. Hackers can leverage this by sending IPv6 traffic to bypass IPv4-based firewall rules.

  

## IDS (Intrusion Detection System)

### What is IDS?

An Intrusion Detection System (IDS) is a security tool designed to monitor network or system activity for malicious activity or policy violations. It works by analyzing traffic, logs, and system events to detect unauthorized actions.

- Types of IDS:
    1. Network-Based IDS (NIDS):
        
        - Monitors network traffic for signs of attacks.
        - Analyzes incoming and outgoing network packets.
        - Examples: Snort, Suricata.
    2. Host-Based IDS (HIDS):
        
        - Installed on individual host devices (like servers or workstations).
        - Monitors system activity such as file integrity, logs, and user behavior.
        - Examples: OSSEC, Tripwire.
    3. Signature-Based IDS:
        
        - Relies on predefined patterns (signatures) of known attacks.
        - It compares incoming traffic to these signatures to detect attacks.
        - Pros: Effective at detecting known threats.
        - Cons: Cannot detect new or unknown threats.
    4. Anomaly-Based IDS:
        
        - Monitors baseline traffic and behavior to detect deviations.
        - It raises alarms when there is unusual activity or a pattern that doesn’t match typical behavior.
        - Pros: Can detect new, unknown attacks (zero-day).
        - Cons: Higher false positives if the baseline isn't accurate.
    5. Hybrid IDS:
        
        - Combines both signature-based and anomaly-based detection.
        - Attempts to balance the strengths of both methods.
        - Example: Snort with additional anomaly detection plugins.

### Security Features of IDS:

1. Alert Generation:
    
    - IDS generates alerts when it detects suspicious activity or known attack signatures.
2. Logging:
    
    - IDS logs detected events for analysis, helping in forensic investigations.
3. Traffic Analysis:
    
    - IDS inspects network traffic to identify malicious behavior based on known attack patterns (signatures) or unusual activity (anomalies).
4. Real-Time Monitoring:
    
    - Most IDS solutions operate in real-time, providing immediate feedback to the security team.

### How Hackers Exploit IDS:

1. Evasion Techniques:
    
    - Packet Fragmentation: Hackers can break malicious payloads into smaller fragments to evade signature-based detection. IDS may not reassemble fragments properly, allowing the attack to slip through.
    - Polymorphic Malware: Attackers change the appearance of malware (its signature) to evade detection.
    - Obfuscation: Malicious payloads are encoded or disguised to evade detection by IDS signatures.
2. Flooding the IDS with Noise:
    
    - Attackers may flood the IDS with so much data that it becomes overwhelmed, causing it to miss legitimate attacks (Denial of Service for IDS).
3. Tunneling:
    
    - Hackers may tunnel malicious traffic over encrypted or uncommon ports to bypass IDS detection.
4. Zero-Day Exploits:
    
    - IDS systems rely heavily on signatures, and new attacks may not have signatures in the IDS database, allowing zero-day exploits to bypass detection.

### How IDS Works Under the Hood:

1. Traffic Inspection:
    
    - IDS monitors traffic using packet capture tools like Wireshark or tcpdump.
    - It inspects headers and payloads of network packets for known attack patterns or deviations.
2. Signature Matching (for Signature-based IDS):
    
    - The IDS compares incoming traffic to a database of attack signatures and flags matching patterns as potential intrusions.
3. Anomaly Detection (for Anomaly-based IDS):
    
    - The IDS creates a baseline of normal traffic and alerts if the traffic deviates significantly from this baseline.
4. Behavioral Analysis:
    
    - HIDS monitors system processes, file integrity, login events, and resource usage for suspicious patterns.

---

## IPS (Intrusion Prevention System)

### What is IPS?

An Intrusion Prevention System (IPS) is similar to an IDS but goes a step further by not only detecting malicious activity but also actively blocking or preventing it. IPS is often deployed inline in the network, allowing it to actively intercept and block threats in real-time.

- Types of IPS:
    1. Network-Based IPS (NIPS):
        
        - Monitors and analyzes network traffic for signs of attacks and takes action to block malicious packets.
        - Example: Cisco FirePower, Suricata (with IPS features).
    2. Host-Based IPS (HIPS):
        
        - Installed on individual machines (like HIDS but with prevention features).
        - Monitors for local system attacks and prevents or quarantines harmful processes.
        - Example: OSSEC with prevention modules.
    3. Signature-Based IPS:
        
        - Like IDS, but it also takes action to block any traffic matching a known attack signature.
        - Blocking can be done by dropping packets, resetting connections, or blocking IPs.
    4. Anomaly-Based IPS:
        
        - Identifies unusual patterns or deviations from established behavior and takes preventive actions.
        - Can stop new or unknown attacks (zero-day) that deviate from normal network behavior.
    5. Hybrid IPS:
        
        - Combines both signature-based and anomaly-based methods to provide more robust protection.

### Security Features of IPS:

1. Real-Time Prevention:
    
    - IPS not only detects but actively blocks or mitigates attacks.
2. Traffic Blocking:
    
    - Can drop malicious packets, reset connections, or block traffic from a suspicious IP address.
3. Alerting and Logging:
    
    - Similar to IDS, IPS generates alerts, but it can also provide additional context, such as reasons for blocking traffic.
4. Protocol Anomaly Detection:
    
    - IPS can monitor protocols like HTTP, DNS, or FTP for anomalies, ensuring that valid traffic is not mistaken for malicious.

### How Hackers Exploit IPS:

1. Evasion:
    
    - Encrypted Traffic: Attackers might use SSL/TLS encryption to disguise malicious payloads from IPS (as IPS may not decrypt the traffic).
    - Fragmentation and Tunneling: Attackers might fragment packets or use uncommon ports to avoid detection.
2. DoS on IPS:
    
    - Similar to IDS, attackers may overwhelm IPS systems with traffic, forcing the IPS to fail or miss attacks.
3. Exploiting IPS's False Positives:
    
    - Attackers may generate legitimate-looking traffic to overwhelm the IPS with false positives, causing it to block legitimate traffic and allow the attack to go through.
4. Zero-Day and Custom Payloads:
    
    - IPS systems depend on signatures, and a novel attack with no signature can often bypass IPS defenses.

### How IPS Works Under the Hood:

1. Inline Traffic Analysis:
    
    - IPS systems are often deployed inline, meaning they sit directly in the traffic path. They analyze packets as they pass through and can block harmful traffic immediately.
2. Signature Matching and Blocking:
    
    - Similar to IDS, the IPS matches packets to a signature database. If a match is found, the IPS blocks the malicious packet.
3. Anomaly Detection and Mitigation:
    
    - When traffic deviates significantly from normal patterns, the IPS triggers preventive measures such as dropping packets or resetting connections.
4. Behavioral Analysis:
    
    - IPS systems analyze traffic patterns and behavior to detect new or unknown attacks based on unusual activities or behavior outside established norms.

---

## How to Crack or Bypass IDS/IPS (For Ethical Hacking and Testing)

As an ethical hacker, understanding how attackers bypass IDS/IPS is crucial for testing and improving security measures. Here are some techniques:

1. Encryption (SSL/TLS):
    
    - Encrypting traffic helps attackers bypass network-based IDS/IPS, as the system can’t inspect the payload inside the encrypted traffic.
2. Tunneling Attacks:
    
    - Attackers use common protocols (HTTP, DNS) to tunnel malicious traffic, hoping to evade detection by the IDS/IPS.
3. Fragmentation:
    
    - By fragmenting malicious packets, attackers can evade signature-based IDS/IPS that don’t reassemble the fragments.
4. Polymorphism:
    
    - Attackers modify the signature of their attack to make it unrecognizable by signature-based IDS/IPS systems.
5. DoS/DDoS Attacks on IDS/IPS:
    
    - Flooding the system with unnecessary traffic, causing it to miss the actual attack or crash.

---
# Security Models
## Bell-LaPadula Model 

The Bell-LaPadula Model aims to achieve confidentiality by specifying three rules:

- Simple Security Property : This property is referred to as “no read up”; it states that a subject at a lower security level cannot read an object at a higher security level. This rule prevents access to sensitive information above the authorized level.
- Star Security Property : This property is referred to as “no write down”; it states that a subject at a higher security level cannot write to an object at a lower security level. This rule prevents the disclosure of sensitive information to a subject of lower security level.
- Discretionary-Security Property : This property uses an access matrix to allow read and write operations. An example access matrix is shown in the table below and used in conjunction with the first two properties.

| Subjects | Object A | Object B |
| ---- | ---- | ---- |
| Subject 1 | Write | No Access | 
| Subject 2 | Read/Write | Read | 

The first two properties can be summarized as “write up, read down.” You can share confidential information with people of higher security clearance (write up), and you can receive confidential information from people with lower security clearance (read down).

There are certain limitations to the Bell-LaPadula model. For example, it was not designed to handle file-sharing.

---
## The Biba Integrity Model
The Biba Model aims to achieve Integrity by specifying two main rules:

    Simple Integrity Property : This property is referred to as “no read down”; a higher Integrity subject should not read from a lower Integrity object.
    Star Integrity Property : This property is referred to as “no write up”; a lower Integrity subject should not write to a higher Integrity object.

These two properties can be summarized as “read up, write down.” This rule is in contrast with the Bell-LaPadula Model, and this should not be surprising as one is concerned with confidentiality while the other is with Integrity.

Biba Model suffers from various limitations. One example is that it does not handle internal threats (insider threat)

---
## The Clark-Wilson Model

The Clark-Wilson Model also aims to achieve Integrity by using the following concepts:

    Constrained Data Item (CDI) : This refers to the data type whose Integrity we want to preserve.
    Unconstrained Data Item (UDI) : This refers to all data types beyond CDI, such as user and system input.
    Transformation Procedures (TPs) : These procedures are programmed operations, such as read and write, and should maintain Integrity the of CDIs.
    Integrity Verification Procedures (IVPs) : These procedures check and ensure the validity of CDIs.


## Brewer and Nash model
## Goguen-Meseguer model
## Sutherland model
## Graham-Denning model
## Harrison-Ruzzo-Ullman model

---
# Defense-in Depth 
Defence-in-Depth refers to creating a security system of multiple levels; hence it is also called Multi-Level Security.

Consider the following analogy: you have a locked drawer where you keep your important documents and pricey stuff. The drawer is locked; however, do you want this drawer lock to be the only thing standing between a thief and your expensive items? If we think of multi-level security, we would prefer that the drawer be locked, the relevant room be locked, the main door of the apartment be locked, the building gate be locked, and you might even want to throw in a few security cameras along the way. Although these multiple levels of security cannot stop every thief, they would block most of them and slow down the others.

---
# ISO/IEC

he International Organization for Standardization (ISO) and the International Electrotechnical Commission (IEC) have created the ISO/IEC 19249. In this task, we will brush briefly upon ISO/IEC 19249:2017 Information technology - Security techniques - Catalogue of architectural and design principles for secure products, systems and applications. The purpose is to have a better idea of what international organizations would teach regarding security principles.

## ISO/IEC 19249 lists five architectural principles:

- Domain Separation: Every set of related components is grouped as a single entity; components can be applications, data, or other resources. Each entity will have its own domain and be assigned a common set of security attributes. For example, consider the x86 processor privilege levels: the operating system kernel can run in ring 0 (the most privileged level). In contrast, user-mode applications can run in ring 3 (the least privileged level). Domain separation is included in the Goguen-Meseguer Model.
- Layering: When a system is structured into many abstract levels or layers, it becomes possible to impose security policies at different levels; moreover, it would be feasible to validate the operation. Let’s consider the OSI (Open Systems Interconnection) model with its seven layers in networking. Each layer in the OSI model provides specific services to the layer above it. This layering makes it possible to impose security policies and easily validate that the system is working as intended. Another example from the programming world is disk operations; a programmer usually uses the disk read and write functions provided by the chosen high-level programming language. The programming language hides the low-level system calls and presents them as more user-friendly methods. Layering relates to Defence in Depth.
- Encapsulation: In object-oriented programming (OOP), we hide low-level implementations and prevent direct manipulation of the data in an object by providing specific methods for that purpose. For example, if you have a clock object, you would provide a method increment() instead of giving the user direct access to the seconds variable. The aim is to prevent invalid values for your variables. Similarly, in larger systems, you would use (or even design) a proper Application Programming Interface (API) that your application would use to access the database.
- Redundancy: This principle ensures availability and Integrity. There are many examples related to redundancy. Consider the case of a hardware server with two built-in power supplies: if one power supply fails, the system continues to function. Consider a RAID 5 configuration with three drives: if one drive fails, data remains available using the remaining two drives. Moreover, if data is improperly changed on one of the disks, it would be detected via the parity, ensuring the data’s Integrity.
- Virtualization: With the advent of cloud services, virtualization has become more common and popular. The concept of virtualization is sharing a single set of hardware among multiple operating systems. Virtualization provides sandboxing capabilities that improve security boundaries, secure detonation, and observance of malicious programs.

## ISO/IEC 19249 teaches five design principles:

- Least Privilege: You can also phrase it informally as “need-to basis” or “need-to-know basis” as you answer the question, “who can access what?” The principle of least privilege teaches that you should provide the least amount of permissions for someone to carry out their task and nothing more. For example, if a user needs to be able to view a document, you should give them read rights without write rights.
- Attack Surface Minimisation: Every system has vulnerabilities that an attacker might use to compromise a system. Some vulnerabilities are known, while others are yet to be discovered. These vulnerabilities represent risks that we should aim to minimize. For example, in one of the steps to harden a Linux system, we would disable any service we don’t need.
- Centralized Parameter Validation: Many threats are due to the system receiving input, especially from users. Invalid inputs can be used to exploit vulnerabilities in the system, such as denial of service and remote code execution. Therefore, parameter validation is a necessary step to ensure the correct system state. Considering the number of parameters a system handles, the validation of the parameters should be centralized within one library or system.
- Centralized General Security Services: As a security principle, we should aim to centralize all security services. For example, we would create a centralized server for authentication. Of course, you might take proper measures to ensure availability and prevent creating a single point of failure.
- Preparing for Error and Exception Handling: Whenever we build a system, we should take into account that errors and exceptions do and will occur. For instance, in a shopping application, a customer might try to place an order for an out-of-stock item. A database might get overloaded and stop responding to a web application. This principle teaches that the systems should be designed to fail safe; for example, if a firewall crashes, it should block all traffic instead of allowing all traffic. Moreover, we should be careful that error messages don’t leak information that we consider confidential, such as dumping memory content that contains information related to other customers.

---
# Cloud Security
- Involves policies, controls and technologies to protect cloud data. IaaS provides virtual resources, PaaS offers app development platforms, SaaS delivers software online.
- `SRM(Shared Responsibility Model)`: Secures infrastructure like servers and networks. secures data applications and configurations.
- `Key Challenges`: Data Security(encryption,ACL,DLP),Access Management(MFA,IAM,Privilege access),Compliance(GDPR,HIPAA,CFAA)
- `Cloud security tools`: 
    - CASBs (Cloud access security broker)
    - CWPPs (Cloud workload protection platform)
    - CSPM (Cloud Security Posture Management)
    - CNAPP (Cloud-Native Application Protection Platform)
    - CIEM (Cloud Infrastructure Entitlement Management)
    - DSPM (Data Security Posture Management)
    - KSPM (Kubernetes Security Posture Management)
    - IaC & Secrets Scanning (Infrastructure as Code
    - CDR (Cloud Detection and Response)
    - AI-SPM (AI Security Posture Management)
    - SASE (Secure Access Service Edge)
    - SSE (Security Service Edge)
    - Enterprise Browsers
    - SSPM (SaaS Security Posture Management)
    - ASPM (Application Security Posture Management)
    - SCA (Software Composition Analysis)-  
    - SAST (Static Application Security Testing)
    - DAST (Dynamic Application Security Testing)
    - IAST (Interactive Application Security Testing)
    - Secret Scanning,
    - API Security Posture Management (ASPM / APISec)
- CASBs (Cloud Access Security Broker): Enforces security policies, compliance, and data governance between enterprise users and cloud service providers.
- CWPPs (Cloud Workload Protection Platform): Secures application workloads—such as virtual machines, containers, and serverless functions—across multi-cloud environments.
- CSPM (Cloud Security Posture Management): Automates compliance monitoring, risk assessment, and misconfiguration detection across cloud infrastructure.
- CNAPP (Cloud-Native Application Protection Platform): Unifies CSPM, CWPP, and developer security into a single platform to protect applications from build to runtime.
- CIEM (Cloud Infrastructure Entitlement Management): Manages and audits identity permissions and access privileges to enforce the principle of least privilege in the cloud.
- DSPM (Data Security Posture Management): Discovers, classifies, and monitors sensitive data stores across cloud environments to prevent unauthorized data exposure.
- KSPM (Kubernetes Security Posture Management): Audits and secures Kubernetes clusters, container orchestration configurations, and cluster-level role-based access controls.
- IaC & Secrets Scanning (Infrastructure as Code): Scans developer infrastructure templates and code repositories prior to deployment to detect misconfigurations and embedded secrets.
- CDR (Cloud Detection and Response): Monitors runtime telemetry and behavioral patterns in cloud environments to detect and respond to active threats.
- AI-SPM (AI Security Posture Management): Discovers, inventories, and secures generative AI models, LLMs, and associated data pipelines in cloud ecosystems.
- SASE (Secure Access Service Edge): Merges wide-area networking with comprehensive cloud security services into a unified, cloud-delivered architecture.
- SSE (Security Service Edge): Combines core cloud security functions—such as SWG, CASB, and ZTNA—into a single cloud-native service edge.
- Enterprise Browsers: Specialized corporate browsers designed to isolate business activity, enforce data loss prevention, and control access to SaaS platforms.
- SSPM (SaaS Security Posture Management): Monitors, audits, and secures SaaS application configurations, user permissions, and third-party integrations.
- ASPM (Application Security Posture Management): Aggregates and correlates security findings from various application testing tools to prioritize risk across the software portfolio.
- SCA (Software Composition Analysis): Scans open-source dependencies and third-party libraries within codebases to identify known vulnerabilities and license compliance risks.
- SAST (Static Application Security Testing): Analyzes source code or binaries without executing them to find security vulnerabilities early in the development lifecycle.
- DAST (Dynamic Application Security Testing): Evaluates running applications from the outside by simulating external cyberattacks to discover runtime vulnerabilities.
- IAST (Interactive Application Security Testing): Combines elements of SAST and DAST by monitoring application behavior from within via agents during execution or testing.
- Secret Scanning: Automated toolsets that search source code, repositories, and build artifacts for leaked credentials, API keys, and passwords.
- API Security Posture Management (APISec): Discovers, inventories, and secures APIs across cloud and application ecosystems by monitoring traffic, endpoints, and compliance.

---
# Attack Vector
- Refers to the mode of attack.
- In detail it is the way of access for certain level of privilege to use it as a point of leverage to get what you need or move laterally as an attacker.
- There are various modes of attack which can be either for initial access or various exploitations within the network for more privilege or lateral movement.
- Common ones are Phishing, Malware, Exploits, Brute Force, Insider Threat.
- `Software`: Buffer overflow, SQLI, XSS, CSRF, etc...
- `Configuration vulnerability`: Unsecured defaults, exposed services
- `Human Vulnerability`: Social Engineering, Weak passwords
---
# Threat Intelligence & Incident Detection
- refers to the information about potential or existing threats, informing an organization's cybersecurity strategy. It includes attack methods, IoCs, Vulnerabilities and cybercriminal tactics.
- Types include Strategic(high-level threat landscape),Tactical(TTPs), operational(real-time,ongoing-attacks).
- `Enhanced Detection`: Understanding threats allows updating detection rules in SIEM and IDS/IPS for accurate incident identification.
- `Proactive defense`: Anticipate attacks and take preventive measures before threats materialize.
- `Informed incident response`: Real-time intelligence aids informed devisions during incidents, helping contain and remediate threats.
- `Gathering Threat intelligence`: OSINT, Internal Sources, Commercial Feeds,Dark Web
- `Methods of Incident Detection`:  Signature Based, Anomaly based, Behavioral Analysis

## Network Intrusion Detection techniques
- `Signature-Based`: Compare traffic against known attack signatures.
- `Anomaly-Based`: Identifies deviations from normal network behavior.
- `Stateful Protocol Analysis`:  Compare traffic to protocol standards, examining network connection states. struggles with encrypted traffic.
- `Behavioral Analysis`: Requires dynamic analysis of the packets. uses techniques like metadata & flow analysis(with tools like NetFlow sFlow or IPFIX), and baseline profiling(protocols used, active hours, typical data columes, etc..)
- `NIDS`: Network Intrusion Detection system or NIDS, placed at strategic points inside the network to monitor traffic from all devices. analyze packets against signature db and anomaly patterns to spot threats like port scans, ddos or lateral movements.
- `Challenges`:  High volume of false positives, encryption, resource intensive analysis.
- `Machine Learning and LLM based Analysis`: Anomaly Detection,False Positives, automation
- `Best Practices`: Regular updates of system and signatures, tune detection thresholds, implement a multi-layered approach, conduct regular network audits.

---
## Endpoint Threat Monitoring
- `Defenition`: Employees or contractors misuse access to compromise data.Endpoint threat monitoring tracks activities on individual devices to detect malicious behavior, unauthorized access, or security incidents. It provides visibility into threats originating from or targeting endpoints.
- `Benifits`: Effective monitoring allows for early identification of compromises, rapid incident response and ensuring compliance with security policies.
- `EDR`: Endpoint Detection and response providese real-time monitoring, collecting data, analyzing behavior and enabling incident investigation and response. 
- `AV`: Antivirus or AntiMalware is used to remove known threats based on signatures and behavior analysis. They are most effective when combined with other techniques.
- `HIDS`: Host Intrusion Detection System or HIDS, plaved directly onto an individual endpoints or server. It monitors internal system characteristics, including operating system logs, running processes, system calls, and file integrity changes(FIB) to detect malicious activity isolated.
- `Challenges`: High volume of alerts if poor configuration, encrypted threats, remote/mobile devices.
- `Best Practices`: Deploy a multi-layered approach, automate threat detection and response, regularly update security tools, implement endpoint hardening techniques, monitor remote and mobile endpoint.

---
# Monitoring and Security Data sources
- Various Data sources for security includes Logs, alerts, and data collected from various sources.
- `Network Traffic Logs`: 
    - Capture Data Flowing Through the network.
    - Detect DDoS attacks by identifying unusual traffic patterns.
- `Firewall and IDS/IPS XDS Logs`: Track network connections, detect port scanners, threat information like malware payload, bruteforce attacks etc...
- `OS Logs`: Record system events like logins and errors.
- `Application Logs`: Track Software activities like database access, errors etc...
- `Endpoint Logs`: Get data from endpoints about network connections, file modification, user logins, etc...
- `Cloud Logs`: Information from cloud services, tracking user activity, etc...
- `Challenges`: Encrypted Traffic, Proxy
## `Visibility and Data Collection`: 
- It is necessary because: 
    - Real-Time threat detection
    - Early identification of vulnerabilities
- `Correlate Data`: Detect Sophisticated threats using multiple sources.
- `Identify Root Cause`: Trace events across systems.
- `Improve Response`: Provide data for investigation.
- `Role of Data Collection`
    - `System logs`: Records of user logins , application usage, system errors.
    - `Network Traffic`: Shows data flow and helps detect unusual patterns.
    `- Endpoint Data`: information from endpoints.
- `Data Correlation`: act of piecing information together to build a whole story.
- `Benifits of full visibility`: faster threat detection, proactive security, improved incident response.
- Also should be compliant with the laws.
- `Challenges`: High volume of Data, proxy servers, encrypted traffic.
    - `Encryption`: makes data sensitive data by making it unreadable without the key. but its a challenge when it comes to monitoring. We can do SSL decryption but its gonna cause overhead and will make it slow.
    - `Proxy`: Advanced Proxy Server Detection and monitoring, DNS Filtering, Threat intelligence.
---
# Threat Hunting
- Actively Seeking out Security Threats.
- It targets threats missed by automated systems.
- Focuses on stealthy long-term network intrutions.
- Hypothesis Creation,Investigation, detection, continuous  improvement.
- `Best Practices`:  Regular threats  hunts,  deep monitoring, Training in awareness,  use the right tool, leverage threat intel,  focus on high value target, document and share findings.
---
# Incident Response Process
- `Stage 1 Preparation`: 
    1. `Incident Response Plan(IRP)`: A detailed document outlining steps to follow during a security incident. Defining roles, responsibilities,  communication,  escalation procedure.
    2. `Team Training`:  training all incident response  team members  to follow IRP  and handle  various incident types through  exercises and simulations.
    3. `Security Tools`:  deploying and configuring monitoring tools like SIEM, firewalls and EDR  solutions to detect  suspicious activities.
- `Stage 2: Detection and Analysis`
    1. `Identification`: Identifying the incident and gathering information about the occurrence.
    2. `Data Collection`: Analyzing the scope and  severity of the  incident using automated  tools like IDS/IPS, log analysis and network  monitoring.
    3. `Analysis`: Determining the  nature of the attack, affected systems and potential damage.
- `Stage3 : Containment, Eradication and Recovery`
    1. `Containment`: Limiting damage by isolating affected systems,  blocking malicious IPs, or  disabling accounts.
    2. `Eradication`:  removing the incident's cause, like deleting malware  closing vulnerabilties, or  cleaning infected  systems.
    3. `Recovery`: Restoring  systems,  recovering data, and  ensuring full operational  capacity, with continuous  monitoring.
- `Step 4: Post-Incident Activity`
    1. `Post-Incident review`: Thorough analysis of the  incident, response  effectiveness, and  areas for  improvement.
    2. `Policy update`:  improving security policies,  procedures, and controls based on lessons learned.
    3. `Findings sharing`: sharing key  takeaways to raise awareness and preevent similar incidents.
---
## Evaluating Security Incidents (Log Analysis)

### What is Log Analysis?

Log analysis is the process of examining system, application, network, and security logs to identify suspicious activity, security incidents, and potential attacks.
- `Best Practices`: cetralized system, baselines, automation, correlation, proritize retention

### Common Log Sources

- System logs – OS events, startup/shutdown, errors.
- Application logs – Application activity and errors.
- Security logs – Authentication, authorization, access attempts.
- Firewall logs – Allowed/blocked network connections.
- IDS/IPS logs – Detected or prevented attacks.
- Authentication logs – Successful/failed login attempts.
- DNS logs – Domain lookup activity.
- Web server logs – HTTP requests and responses.

### Important Things to Look For

- Multiple failed login attempts.
- Login from unusual locations.
- Successful login after many failures.
- Privilege escalation.
- Unusual outbound traffic.
- Unexpected account creation.
- Malware detections.
- Access to sensitive files.
- Repeated firewall blocks.
- Activity outside normal business hours.

### Log Levels

Common severity levels include:

- Informational – Normal activity.
- Warning – Potential problem.
- Error – Something failed.
- Critical/Alert – Serious security/system problem.

---
#  Handling False Positives and True Incidents

### False Positive

A false positive occurs when a security tool identifies legitimate activity as malicious.

Example:
An antivirus flags a legitimate administrative tool as malware.
`Best Practices`: prioritize, document, communicate

### True Positive

A true positive occurs when a security tool correctly identifies malicious or suspicious activity.

Example:
An IDS detects an actual port scan.

### False Negative

A false negative occurs when malicious activity happens but the security tool fails to detect it.

Example:
Malware infects a computer but antivirus does not detect it.

### True Negative

A true negative occurs when legitimate activity is correctly identified as legitimate.

### Easy Table

| Result | Meaning |
| --- | --- |
| True Positive | Attack detected correctly |
| False Positive | Normal activity incorrectly flagged |
| True Negative | Normal activity correctly allowed |
| False Negative | Attack missed |

### Important

- Too many false positives → alert fatigue.
- Too many false negatives → attacks may go undetected.

### solution
- Fine tune tools
- Machine Learning
- Contextual Analysis

### To identify true incidents
- Context is key
- Data Correlation
- Verification

---

# Mitigation Strategies and Post-Incident Actions

### Mitigation

Mitigation means reducing the impact or likelihood of a security threat.

### Common Mitigation Techniques

- Patch vulnerable systems.
- Update antivirus signatures.
- Disable compromised accounts.
- Isolate infected systems.
- Block malicious IP addresses.
- Change compromised credentials.
- Apply firewall rules.
- Implement MFA.
- Segment the network.
- Restore systems from clean backups.

### Post-Incident Actions

After an incident:

1. Contain the incident.
2. Eradicate the threat.
3. Recover affected systems.
4. Document what happened.
5. Perform root cause analysis.
6. Update security controls.
7. Review policies and procedures.
8. Conduct lessons learned.

### Root Cause Analysis

Determines why the incident happened, rather than only fixing its symptoms.

---
# Threat Mitigation Tools

## Use of SIEM for Threat Detection

### SIEM

Security Information and Event Management (SIEM) collects, aggregates, correlates, and analyzes security events from multiple sources.

### Main Functions

- Log collection.
- Log aggregation.
- Event correlation.
- Threat detection.
- Alert generation.
- Security monitoring.
- Incident investigation.
- Reporting.

### Examples of SIEM Data

- Firewall logs.
- Authentication logs.
- Endpoint logs.
- IDS/IPS alerts.
- DNS logs.
- Cloud logs.

### Correlation

SIEM can connect multiple events to identify an attack.

Example:

Failed login → successful login → privilege escalation → unusual file access

Together, these may indicate a compromised account.

---

# Packet Analysis Tools (Wireshark Basics)

### Packet Analysis

Packet analysis examines network packets to understand network communication and identify suspicious traffic.

### Wireshark

Wireshark is a network protocol analyzer used to capture and inspect network traffic.

### Important Protocols

- Ethernet – Local network communication.
- ARP – Maps IP addresses to MAC addresses.
- IP – Network addressing/routing.
- TCP – Reliable connection-oriented communication.
- UDP – Faster connectionless communication.
- DNS – Domain-name resolution.
- HTTP/HTTPS – Web traffic.
- ICMP – Network diagnostic/error messages.

### Useful Wireshark Concepts

- Packet capture – Recording network traffic.
- Capture filter – Controls what traffic is captured.
- Display filter – Filters already captured packets.
- Source IP – Sender.
- Destination IP – Receiver.
- Source/Destination port – Identifies services/applications.

### Security Uses

- Detect suspicious traffic.
- Investigate malware communication.
- Identify port scans.
- Troubleshoot network issues.
- Analyze protocols.

---

# Host-Based Tools (HIDS, Antivirus)

### Host-Based Security

Security controls installed directly on endpoints such as:

- Computers.
- Servers.
- Laptops.
- Workstations.

### HIDS

Host-Based Intrusion Detection System (HIDS) monitors activity on an individual host for suspicious behavior.

It can monitor:

- File changes.
- System activity.
- Logs.
- Processes.
- Configuration changes.

### HIPS

Host-Based Intrusion Prevention System (HIPS) detects and can block/prevent suspicious activity.

### Antivirus / Anti-Malware

Detects, blocks, quarantines, and removes malicious software.

### Difference

| Tool | Main Purpose |
| --- | --- |
| HIDS | Detect suspicious host activity |
| HIPS | Detect + prevent suspicious host activity |
| Antivirus | Detect/block malware |

---

# Basic Techniques for Malware Analysis

### Malware

Malware is software designed to damage, disrupt, spy on, or gain unauthorized access to systems.

### Common Malware Types

- Virus – Attaches to legitimate files and requires execution.
- Worm – Self-propagates across systems/networks.
- Trojan – Malicious software disguised as legitimate software.
- Ransomware – Encrypts/locks data and demands payment.
- Spyware – Secretly collects information.
- Rootkit – Hides malicious activity and maintains privileged access.
- Keylogger – Records keystrokes.
- Bot/Botnet malware – Turns systems into remotely controlled devices.

### Static Analysis

Analyzing malware without executing it.

Examples:

- File hashes.
- Strings.
- File metadata.
- Code examination.
- Antivirus scanning.

### Dynamic Analysis

Analyzing malware while it is running, preferably in an isolated environment.

Look at:

- Network connections.
- Processes.
- Registry changes.
- Files created.
- System changes.

### Sandbox

An isolated environment used to safely execute and analyze suspicious files.

 ### Hash

A hash can help identify whether a file matches a known malicious file.

Common hashes:

- MD5
- SHA-1
- SHA-256

Security+ focus: Know the difference between static and dynamic analysis.

---

# Graded Quiz: Security Monitoring and Response

For this section, remember the major concepts:

- Log analysis.
- SIEM.
- IDS/IPS.
- HIDS/HIPS.
- False positive vs false negative.
- Incident response.
- Malware analysis.
- Packet analysis.
- Containment.
- Eradication.
- Recovery.
- Lessons learned.

A common exam scenario asks what should be done first. Think in terms of:

Identify → Contain → Eradicate → Recover → Lessons Learned

---

# Host-Based Security Fundamentals

## Antivirus and Anti-Malware Strategies

### Antivirus

Software designed to detect, prevent, and remove malicious software.

### Detection Methods

#### Signature-Based Detection

Compares files against known malware signatures.

Advantages:

- Fast.
- Effective against known malware.

Disadvantage:

- Less effective against new/unknown malware.

#### Heuristic-Based Detection

Looks for suspicious characteristics or code patterns.

Can detect previously unknown malware.

#### Behavioral-Based Detection

Monitors what software does rather than simply what it looks like.

Example:

> A program suddenly encrypts thousands of files.

This could indicate ransomware behavior.

#### Machine Learning / AI-Based Detection

Uses models to identify suspicious patterns and behavior.

### Other Important Concepts

- Quarantine – Isolates suspicious files.
- Real-time protection – Continuously monitors activity.
- Signature updates – Keep malware definitions current.
- Endpoint protection – Protects individual devices.

---

# Intrusion Detection/Prevention at the Host Level

### HIDS

Detects suspicious activity on a specific host.

### HIPS

Detects and prevents suspicious host activity.

### HIDS Can Monitor

- File integrity.
- System logs.
- Processes.
- Configuration.
- User activity.

### Detection vs Prevention

IDS = Detect and alert

IPS = Detect and block

### Host vs Network

| Type | Monitoring |
| --- | --- |
| HIDS/HIPS | Individual host |
| NIDS/NIPS | Network traffic |

---

 # Operating System Security Configurations

 OS security configuration involves setting the operating system to reduce security risks.

 ### Important Configurations

 #### Account Security

- Strong passwords.
- MFA.
- Account lockout.
- Disable unused accounts.
- Least privilege.

#### Patch Management

Keep the OS and software updated to fix vulnerabilities.

#### Firewall

Controls inbound and outbound network traffic.

#### File Permissions

Control who can read, write, modify, or execute files.

#### User Account Control

Prevents unauthorized applications/users from performing privileged actions.

#### Secure Boot

Helps ensure only trusted software loads during startup.

#### Disk Encryption

Protects data if the device is lost or stolen.

Examples:

- Full-disk encryption.
- File-level encryption.

#### Screen Lock

Automatically locks inactive systems.

### Principle of Least Privilege

Users and applications should receive only the permissions they need.

---

# Application Whitelisting and Blacklisting

### Application Whitelisting

Only approved applications are allowed to run.

Example:

> Only Microsoft Office and approved company applications can execute.

### Advantages

- Strong protection against unknown applications.
- Reduces unauthorized software.
- Helps prevent malware execution.

### Application Blacklisting

Known unwanted or malicious applications are blocked.

 ### Difference

| Whitelisting | Blacklisting |
| --- | --- |
| Allow known/approved | Block known/bad |
| Default deny | Default allow |
| Stronger control | Easier to manage |


---

# Read More About Host-Based Security Fundamentals

### Key Concept

Host-based security focuses on protecting individual endpoints rather than the network as a whole.

Important controls:

- Antivirus/EDR.
- HIDS/HIPS.
- Host firewall.
- File permissions.
- OS hardening.
- Patch management.
- Encryption.
- Application control.
- Endpoint logging.

### Endpoint Detection and Response (EDR)

EDR continuously monitors endpoints, detects suspicious behavior, provides investigation data, and can help respond to threats.

---

# Network Security Analysis

## Network Security Analysis (IDS/IPS, Firewalls)

### IDS

Intrusion Detection System detects suspicious network activity and generates alerts.

### IPS

Intrusion Prevention System detects and can block malicious traffic.

### Network IDS vs Network IPS

- NIDS → Network-based detection.
- NIPS → Network-based prevention.

### Firewall

A security device/software that controls traffic based on predefined rules.

### Firewall Types

#### Packet-Filtering Firewall

Filters traffic based on:

- IP address.
- Port.
- Protocol.

#### Stateful Firewall

Tracks active connections and makes decisions based on connection state.

#### Proxy Firewall

Acts as an intermediary between clients and servers.

#### Next-Generation Firewall (NGFW)

Provides advanced capabilities such as:

- Application awareness.
- Deep packet inspection.
- Intrusion prevention.
- User awareness.


Firewall = controls traffic

IDS = detects

IPS = detects + prevents

---
# Analyzing Network Traffic and Protocol Basics

### Network Traffic

Data moving between systems over a network.

 ### Important Protocols

| Protocol | Purpose |
| --- | --- |
| HTTP | Web traffic |
| HTTPS | Encrypted web traffic |
| DNS | Name resolution |
| DHCP | Automatic IP configuration |
| FTP | File transfer |
| SSH | Secure remote administration |
| SMTP | Sending email |
| IMAP | Receiving/managing email |
| TCP | Reliable communication |
| UDP | Connectionless communication |
| ICMP | Diagnostics/errors |
| ARP | IP-to-MAC resolution |

### TCP

- Connection-oriented.
- Reliable.
- Uses acknowledgments.
- Uses a three-way handshake.

SYN → SYN-ACK → ACK

### UDP

- Connectionless.
- Faster/lower overhead.
- No guaranteed delivery.

### Common Security Concern

Cleartext protocols can expose data.

Examples:

- HTTP.
- FTP.
- Telnet.

Prefer secure alternatives such as:

- HTTPS.
- SFTP.
- SSH.

---

# Tools for Network Security Assessments

### Vulnerability Scanner

Identifies known vulnerabilities and weaknesses.

Examples:

- Nessus.
- OpenVAS/Greenbone.

### Port Scanner

Identifies open ports and available services.

Common tool:

- Nmap.

### Packet Analyzer

Examines network packets.

Example:

- Wireshark.

### Protocol Analyzer

Helps understand network communication and protocols.

### Network Mapper

Discovers:

- Hosts.
- Ports.
- Services.
- Operating systems.

### Common Security Tools to Remember

| Tool Type | Purpose |
| --- | --- |
| Nmap | Port/network scanning |
| Wireshark | Packet analysis |
| Nessus | Vulnerability scanning |
| SIEM | Log/event analysis |
| IDS/IPS | Intrusion detection/prevention |

---

# Common Network-Based Attack Patterns

### DoS

Denial of Service attempts to make a service unavailable.

### DDoS

Distributed Denial of Service uses multiple systems to attack a target.

DoS: One/few sources
DDoS: Many distributed sources

### Port Scanning

Attacker scans ports to discover available services.

### Man-in-the-Middle (MITM)

Attacker sends fake ARP information to associate their MAC address with acceptable amount of data lossacker secretly intercepts communication between two parties.

### Replay Attack

Attacker captures valid communication and retransmits it later.

### ARP Spoofing

Attacker sends fake ARP information to associate their MAC address with another IP.

### DNS Poisoning

Manipulates DNS information to redirect users to malicious destinations.

### DNS Tunneling

Uses DNS traffic to secretly transfer data or communicate with malware.

### IP Spoofing

Attacker falsifies the source IP address.

### Brute Force

Repeatedly attempts passwords/credentials until successful.

### Password Spraying

Attempts a small number of common passwords against many accounts.

### Credential Stuffing

Uses stolen username/password combinations against other services.

### Easy Distinction

Brute force: Many passwords → one account

Password spraying: One/few common passwords → many accounts

Credential stuffing: Stolen credentials → many services

---

# Security Policies and Procedures

## Developing Effective Security Policies

### Security Policy

A formal document defining an organization's security requirements, rules, responsibilities, and acceptable behavior.

### Common Security Policies

#### Acceptable Use Policy (AUP)

Defines appropriate use of company systems/resources.

#### Password Policy

Defines:

- Password requirements.
- Length.
- Complexity.
- Reuse restrictions.
- Lockout requirements.

#### Account Management Policy

Defines account creation, modification, review, and termination.

#### Access Control Policy

Defines who can access what resources.

#### Data Classification Policy

Defines how data should be categorized and protected.

Example classifications:

- Public.
- Internal.
- Confidential.
- Restricted.

#### Incident Response Policy

Defines how security incidents should be handled.
Guidelines are provided by NIST
#### Disaster Recovery Policy

Defines how systems/data are restored after a disaster.

### Important Principle
Policies should be:

- Clear.
- Enforceable.
- Regularly reviewed.
- Communicated to employees.
- Aligned with laws/regulations and business requirements.

---

# Incident Response and Disaster Recovery Planning

## Incident Response

### Incident

A security event that threatens confidentiality, integrity, or availability.

 ### Incident Response Process

1. Preparation
- Create policies.
- Train staff.
- Prepare tools.
- Define roles.

2. Detection/Analysis

- Identify suspicious activity.
- Analyze logs and alerts.
- Determine scope.

3. Containment
Stop the incident from spreading.

Types:

- Short-term containment
- Long-term containment

4. Eradication
Remove the root cause/threat.

Examples:

- Remove malware.
- Patch vulnerability.
- Delete malicious accounts.

5. Recovery
Restore systems to normal operation.

6. Lessons Learned
Review the incident and improve security.

### Disaster Recovery

Disaster Recovery (DR) focuses on restoring IT systems and services after a disruptive event.

### Important DR Concepts

#### RTO

Recovery Time Objective

Maximum acceptable time to restore a service.

> "How quickly must we recover?"

#### RPO

Recovery Point Objective

Maximum acceptable amount of data loss measured in time.

> "How much data can we afford to lose?"

### Example

If:
- RTO = 4 hours
- RPO = 1 hour

The system should be restored within 4 hours, with no more than 1 hour of data loss.

---

# Continuous Monitoring Practices

### Continuous Monitoring

Regular/ongoing observation of systems, networks, users, and security controls to detect threats and changes.

### What to Monitor?

- Network traffic.
- Authentication.
- User activity.
- Endpoint activity.
- Vulnerabilities.
- Configuration changes.
- Security alerts.
- System logs.
- Cloud environments.

### Benefits

- Early threat detection.
- Faster incident response.
- Detect unauthorized changes.
- Identify vulnerabilities.
- Improve compliance.

### Important Technologies
- SIEM.
- IDS/IPS.
- EDR.
- Vulnerability scanners.
- Network monitoring.
- Log management.

### Baseline

A baseline represents normal system/network behavior.

If normal traffic is usually 100 MB/hour and suddenly becomes 10 GB/hour, that deviation may indicate suspicious activity.

### MTTR and MTTD
Mean time to respond and mean time to detect. 
This is a metric which indicates that the continuous monitoring program is effectively enhancing organizational security.

---

# Security Training and Awareness

### Security Awareness Training

Educates employees about cybersecurity risks and safe behavior.

### Common Training Topics

- Phishing.
- Social engineering.
- Password security.
- MFA.
- Malware.
- Data protection.
- Physical security.
- Incident reporting.
- Acceptable use.
- Removable media.
- Secure remote work.

### Phishing

Fraudulent communication designed to trick users into revealing information or performing an unsafe action.

### Types of Phishing
- Phishing – General phishing.
- Spear phishing – Targeted at a specific person/group.
- Whaling – Targets senior executives/high-value individuals.
- Smishing – SMS/text-message phishing.
- Vishing – Voice/phone phishing.
### Social Engineering

Manipulating people into revealing information or performing actions that compromise security.

### Common Social Engineering Techniques
- Pretexting.
- Phishing.
- Baiting.
- Tailgating.
- Impersonation.
- Quid pro quo.

### Security Awareness Best Practices
- Regular training.
- Phishing simulations.
- Clear reporting procedures.
- Teach employees to verify unusual requests.
- Encourage strong passwords and MFA.
- Train employees to recognize social engineering.

---

# ⭐ High-Priority Security+ Concepts to Memorize

If you're studying these topics specifically for CompTIA Security+, make sure you can quickly distinguish these:

| Concept | Remember |
| --- | --- |
| SIEM | Collects/correlates/analyzes security logs |
| IDS | Detects and alerts |
| IPS | Detects and blocks |
| HIDS | IDS on a host |
| HIPS | IPS on a host |
| Firewall | Controls network traffic |
| Wireshark | Packet analysis |
| Nmap | Network/port scanning |
| Vulnerability Scanner | Finds vulnerabilities |
| Static Malware Analysis | Analyze without executing |
| Dynamic Malware Analysis | Analyze while executing |
| False Positive | Legitimate activity flagged as malicious |
| False Negative | Malicious activity missed |
| RTO | Maximum acceptable recovery time |
| RPO | Maximum acceptable data loss |
| Least Privilege | Minimum required permissions |
| Whitelisting | Allow approved applications |
| Blacklisting | Block known unwanted applications |
| DoS | Deny service |
| DDoS | Distributed denial of service |
| MITM | Intercept communication |
| ARP Spoofing | Fake ARP mappings |
| DNS Poisoning | Manipulate DNS resolution |
| Brute Force | Many password attempts against an account |
| Password Spraying | Common password against many accounts |
| Credential Stuffing | Reuse stolen credentials |
| SIEM | Centralized security event visibility |
| EDR | Endpoint detection and response |
| AUP | Rules for acceptable technology use |
| Incident Response | Handle and recover from security incidents |
| Continuous Monitoring | Ongoing security observation |

## ⭐ Incident Response — Memorize This Order

Preparation → Detection/Analysis → Containment → Eradication → Recovery → Lessons Learned

## ⭐ Malware Analysis — Memorize This

Static = Don't run it

Dynamic = Run it in an isolated environment

## ⭐ Detection Tools — Memorize This

SIEM → Logs

Wireshark → Packets

Nmap → Ports/Hosts

IDS → Detect

IPS → Prevent

HIDS → Host detection

HIPS → Host prevention

EDR → Endpoint monitoring + response

These notes should give you a solid Security+ revision foundation for the topics you listed, without going unnecessarily deep into the individual video material.

---
