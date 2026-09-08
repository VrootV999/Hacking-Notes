# **what we’ll be covering  in this page**

1. • Cybersecurity Detailed
2. • Basics of Cyber Security like types of attacks, non-repudation, CIA triad, etc..
3. • Common vulnerabilities and exploits
4. • all Device in network and its security in use.
5. • About firewalls, intrusion detection systems, and other security tools
6. • Updates on the latest cybersecurity threats and trends

  

# **CIA Triad**

# **What is the CIA Triad?**

The CIA Triad is a fundamental model for information security, representing the three primary goals:

- **Confidentiality**: Protecting sensitive information from unauthorized access. (FA,2FA,MFA)
- **Integrity**: Ensuring data remains accurate and unaltered. (Hashing,Digital Signature, Certificate)
- **Availability**: Ensuring authorized users have reliable access to information when needed.  
    (Redundancy,fault tolerance, patching)  
    

---
# Threat vs Rish vs Vulnerabilities

- Vulnerability: Vulnerable means susceptible to attack or damage. In information security, a vulnerability is a weakness.
- Threat: A threat is a potential danger associated with this weakness or vulnerability.
- Risk: The risk is concerned with the likelihood of a threat actor exploiting a vulnerability and the consequent impact on the business.

---

# **Types of Attacks by Hackers**

## **Overview of Attack Types**

- **OSINT**: Open-Source Intelligence; gathering publicly available information.
- **DDoS**: Distributed Denial of Service; overwhelming a service with traffic to make it unavailable.
- **Phishing**: Deceptive attempts to steal credentials or personal information by impersonating trustworthy entities.
- **Reconnaissance**: Collecting information about a target to exploit vulnerabilities.
- **Man-in-the-Middle (MITM)**: Intercepting communication between two parties to steal or alter information.
- **Password Cracking**: Using various techniques to discover passwords.
- **Privilege Escalation**: Exploiting a system vulnerability to gain higher privileges.
- **Exfiltration**: Unauthorized transfer of data from a system.

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

# **DDoS (Distributed Denial of Service)**

## **What is DDoS?**

A DDoS attack overwhelms a network, server, or service with a flood of traffic, making it unusable for legitimate users.

## **Types of DDoS Attacks**

- **Volumetric Attacks**: Saturating bandwidth with fake traffic.
- **Application Layer Attacks**: Targeting specific applications to exhaust server resources.
- **Protocol Attacks**: Exploiting vulnerabilities in network protocols like SYN flooding.

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

# **Phishing**

## **What is Phishing?**

Phishing is a cyber attack that uses disguised emails or messages to trick individuals into providing sensitive information.

## **Types of Phishing**

- **Spam**: Mass unsolicited emails.
- **Spim**: Spam sent over instant messaging.
- **Credential Harvesting**: Stealing usernames and passwords.
- **Smishing**: Phishing via SMS.
- **Vishing**: Phishing over voice calls.
- **Whaling**: Targeting high-profile individuals.
- **Other Types**: Deceptive tactics like clone phishing and spear phishing.

  

## Email Phising

  

1. mass mailing: public mailing
2. spearphishing: selective phishing
3. whaling: big fish phishing
4. pharming: poisoning the DNS cache of a device to redirect or do whatever attack the attacker likes

---

# **Pretexting**

## **What is Pretexting?**

Pretexting involves creating a fabricated scenario to manipulate someone into divulging sensitive information.

## **Steps in Pretexting**

1. **Creating a Fake Story**: Crafting a believable scenario to gain trust.
2. **Gathering Information**: Using social engineering to obtain personal or confidential details.
3. **Exploiting Trust**: Utilizing the obtained information for malicious purposes.

---

# **Information Gathering/Reconnaissance**

## **What is Information Gathering?**

- **Active Recon**: Direct interaction with the target to gather information (e.g., port scanning).
- **Passive Recon**: Collecting information without directly interacting with the target (e.g., social media research).

  

### **Active Recon**

- Port scanning
- vulnerability scanning
- enumeration
- social engineering to manipulate.

  

### **Passive recon**

- OSINT
- shoulder spoffing

---

# **Website Attacks**

## **Types of Website Attacks**

- **SQL Injection**: Injecting malicious SQL queries to manipulate databases.
- **Cross-Site Scripting (XSS)**: Injecting scripts into websites that run in users' browsers.
- **Cross-Site Request Forgery (CSRF)**: Forcing users to perform actions they didn't intend by exploiting their authenticated session.
- **Directory Traversal**: Accessing restricted directories on a web server.
- **File Inclusion**: Including malicious files via improper input handling.

---

### **Typo Squatting**

- **What is Typo Squatting?**: Registering misspelled versions of popular websites to trick users into visiting malicious websites.

---

### **Prepending**

- **What is Prepending?**: Adding malicious or deceptive content at the beginning of legitimate communication or code to mislead users.

---

### **Watering Hole Attack**

- **What is a Watering Hole Attack?**: Infecting commonly visited websites by the target group with malware to compromise visitors.

---

# **Non-Repudiation**

- **What is Non-Repudiation?**: Ensuring that a person or entity cannot deny the authenticity of their actions, such as sending a message or making a transaction.(a.ka trust by heart)
- can be trusted with Hash.

---

# **Zero Trust**

- **What is Zero Trust?**: A security model where no entity (internal or external) is trusted by default, and every action requires verification before granting access.

---
# Trust but Verify

- Trust but Verify: This principle teaches that we should always verify even when we trust an entity and its behaviour. An entity might be a user or a system. Verifying usually requires setting up proper logging mechanisms; verifying indicates going through the logs to ensure everything is normal. In reality, it is not feasible to verify everything; just think of the work it takes to review all the actions taken by a single entity, such as Internet pages browsed by a single user. This requires automated security mechanisms, such as , intrusion detection, and intrusion prevention systems

---
# **How to Enhance Security in an Organization**

## **Adaptive Identity**

Implement mechanisms to continuously authenticate users based on risk factors.  
examine the individual and apply security contol on based o their process and what the users is by position, place or the person.  

ex: if a chinese user trys to log-in to the DB can trace the connection to find who he is, or automate a stronger authentication if needed.

## **Threat Scope Reduction**

Minimize the attack surface by restricting unnecessary access and exposure.

ex: gain access to the network only by the people in that place or access through vpn and use MFA so Initial access is hard.

## **Policy-Driven Access Control**

Use dynamic policies to control access based on roles, behavior, and other risk factors.

## **Security Zones**

- **What are Security Zones?**: Dividing a network into segments to manage access and reduce the risk of compromise between trusted and untrusted zones.
- Make one or more network segments and create different policies and requlate the internal and external traffic with the policies.
- Seperation is created with Groups and VPN

# **PEP, PDP, and Policy Engine Workflow**

1. **Policy Engine**: Evaluates access policies.(comapares the sent or recieved data with the policy)
2. **Policy Administrator**: Enforces decisions from the policy engine.
3. **Policy Enforcement Point (PEP)**: Intermediary that controls the flow of data between trusted and untrusted zones based on policies. (GATEKEEPER)
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

**Role-Based Access Control (RBAC) : assign user roles**

**Attribute-Based Access Control (ABAC) : characteristics like job, location, etc**

**Relationship-Based Access Control (ReBAC) : using relationship b/w user and the object**

**Discretionary Access Control (DAC) : give full acces to the object that hey own.**

**Zero Trust Network Access (ZTNA) : only what they need no more or no less.**

  

---

# Response plan

  

plan to respond to attacks.  
consists preparation, identification,containment, eradication,recovery & learning.  

---

# Log analysis

analysing the logs in the firewall, application, network manager etc..

---

  

  

# **Proxy Protocol**

  

## **HTTP**

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

  

- **Tunneling**: VPN creates a "tunnel" between your device and a VPN server. This tunnel encrypts all your internet traffic, protecting it from eavesdropping or interception.
- **Encryption**: VPN uses encryption algorithms to scramble the data, so even if it’s intercepted, it can’t be read without the encryption key.
- **IP Masking**: VPNs mask your real IP address with the IP address of the VPN server, making it harder to trace your location or online activity.

  

### **Key VPN Protocols:**

Each protocol dictates how data is encrypted and transmitted. Some common VPN protocols include:

- **OpenVPN**:
    - **Encryption**: Uses SSL/TLS for key exchange, highly secure.
    - **Usage**: Open-source, commonly used due to its strong security and flexibility.
    - **Strengths**: High security, supports various encryption ciphers (AES, Blowfish).
    - **Weaknesses**: Requires third-party software, may have slower speeds depending on configuration.
- **IKEv2/IPsec (Internet Key Exchange Version 2)**:
    - **Encryption**: Often paired with IPsec for encryption.
    - **Usage**: Works well with mobile devices, resilient to network changes (e.g., switching from Wi-Fi to mobile data).
    - **Strengths**: Stability, fast reconnects.
    - **Weaknesses**: Susceptible to blocking by firewalls.
- **PPTP (Point-to-Point Tunneling Protocol)**:
    - **Encryption**: Uses basic encryption (128-bit keys), less secure.
    - **Usage**: One of the oldest protocols, known for speed but outdated in terms of security.
    - **Strengths**: Speed, easy setup.
    - **Weaknesses**: Weak encryption, vulnerable to attacks.
- **L2TP/IPsec (Layer 2 Tunneling Protocol)**:
    - **Encryption**: Combines L2TP (for tunneling) with IPsec for encryption.
    - **Usage**: More secure than PPTP, but slower.
    - **Strengths**: Strong encryption.
    - **Weaknesses**: Slower speeds due to double encapsulation.
- **WireGuard**:
    - **Encryption**: Modern, lightweight protocol using state-of-the-art cryptography.
    - **Usage**: Open-source, high performance, minimal overhead.
    - **Strengths**: Extremely fast, secure, easy to audit.
    - **Weaknesses**: Still relatively new, not widely adopted yet.

  

### **Tips while Working using VPN for Hackers**:

- **IP Hopping**: Hackers may rotate between multiple VPN servers to make tracking more difficult. Each switch results in a new IP, further obfuscating their activities.
- **Logless VPNs**: Ethical hackers prefer VPN services that don’t keep logs of user activity, ensuring no records can be accessed by authorities or leaked.
- **Encryption for Sensitive Data**: VPNs ensure that sensitive information (such as credentials, exploits, or vulnerability reports) being transmitted over the network remains encrypted and secure from potential interception by malicious actors.

  

### **Threats & Limitations of VPNs**:

- **VPN Leakage**: Sometimes, VPNs may leak data such as DNS requests or even IP addresses, which could expose hackers during a penetration test or investigation.
- **Trust in VPN Provider**: If the VPN provider logs activity or shares data with authorities, the user may lose their anonymity.
- **Vulnerable Protocols**: Older VPN protocols (like PPTP) are easier to crack, making them unsuitable for sensitive operations.

  

### VPN Internals – Under the Hood & Vulnerabilities for Hackers

#### **How VPN Works – Internal Architecture:**

A VPN works by creating a secure, encrypted connection between the user’s device and a remote server. Here’s how it looks under the hood:

1. **Client-Side**:
    - **VPN Software**: Installed on the client device (PC, smartphone, etc.). This software manages VPN protocols, encryption, and the secure tunnel setup.
    - **Encryption Process**: Data packets generated by the device (e.g., browsing, sending emails) are encrypted using a pre-defined encryption method (AES, RSA, etc.).
    - **Packet Encapsulation**: The encrypted data is encapsulated into another packet (outer packet) and routed through the VPN tunnel to the VPN server.
2. **Tunnel Establishment**:
    - **Handshake**: The VPN client and VPN server exchange keys (using SSL/TLS, DH, or other protocols) to authenticate each other and establish a secure tunnel.
    - **Encryption Keys**: Once authenticated, both parties agree on encryption keys to secure the traffic.
    - **Data Transmission**: The encrypted data is then sent through the secure tunnel over the internet. The data is hidden within the encrypted tunnel (tunneling protocols: OpenVPN, WireGuard, etc.).
3. **Server-Side**:
    - **Decryption**: The VPN server receives the encrypted packets, decrypts them using the shared key, and forwards the packets to the destination (e.g., website, network service).
    - **Response Handling**: Any response from the destination server (like a web page) goes back through the VPN server, gets re-encrypted, and is sent back to the client through the tunnel.
4. **Key VPN Components**:
    - **Authentication**: Secure user authentication through protocols like SSL/TLS, PSK, or certificates.
    - **Encryption Algorithms**: Common algorithms like AES-256, RSA, and ChaCha20 ensure data confidentiality.
    - **Transport Protocol**: Either TCP (reliable, slower) or UDP (faster, less reliable) is used for communication.

  

#### **How Hackers Can Attack VPN Connections:**

Although VPNs provide strong security, there are still potential vulnerabilities that hackers can exploit.

##### 1. **VPN Exploits:**

Hackers may attempt to exploit vulnerabilities in the VPN infrastructure:

- **Exploiting Weak Protocols**:
    - **PPTP**: Hackers can break weak encryption algorithms like MS-CHAPv2 used in PPTP (Point-to-Point Tunneling Protocol). This is an outdated protocol, and tools like _ASLEAP_ can be used to crack the authentication.
    - **IPsec Vulnerabilities**: While IPsec is secure, certain configurations, such as using weak Diffie-Hellman groups for key exchange, can be cracked by attackers.
- **Man-in-the-Middle (MITM) Attacks**:
    - **Intercepting VPN Traffic**: If the attacker has access to the same network as the victim (like on public Wi-Fi), they can attempt a MITM attack by creating fake DNS or intercepting the initial handshake between the client and VPN server.
    - **Downgrade Attacks**: Hackers may force the client to use weaker VPN protocols (like PPTP instead of OpenVPN) and crack the session using weaker encryption methods.
- **DNS Leaks**:
    - **DNS Traffic Exposure**: Some VPNs may suffer from DNS leaks where DNS queries are routed outside the encrypted tunnel, allowing attackers to intercept and monitor DNS requests.
    - **DNS Poisoning**: If DNS traffic is leaked, hackers can perform DNS poisoning attacks, redirecting users to malicious websites.
- **Exploiting VPN Clients**:
    - **Outdated Software**: Many VPN clients have vulnerabilities if not regularly updated. Attackers could exploit buffer overflows or remote code execution flaws to compromise the VPN client.
    - **Malware in VPN Clients**: Compromised VPN clients (especially free or pirated versions) can contain backdoors or malware, allowing attackers to spy on the user’s data even while they believe they’re protected.

##### 2. **Breaking Encryption**:

- **Brute Force Attack on Keys**: VPNs using weak encryption keys (short key lengths) are susceptible to brute force attacks. With sufficient computational power, hackers can guess the encryption key and decrypt traffic.
- **Quantum Threat**: While currently theoretical, quantum computers may be able to break widely used encryption methods (like RSA) in the future.

##### 3. **Compromising the VPN Server**:

- **VPN Server Vulnerabilities**: If a hacker gains control over a VPN server (via a vulnerability, misconfiguration, or credential theft), they can:
    - **Decrypt Traffic**: Since the server has access to the encryption keys, the hacker can decrypt and monitor user traffic.
    - **Insert Malicious Content**: Hackers can modify the responses from legitimate websites, injecting malware into the victim’s data stream.

##### 4. **Social Engineering & Phishing**:

- **Fake VPN Software**: Hackers might trick users into downloading fake VPN apps that mimic legitimate services but secretly log traffic or send data to malicious servers.
- **Phishing for VPN Credentials**: If hackers obtain login credentials through phishing or credential stuffing, they can compromise the VPN account and monitor the victim’s traffic.

  

### **Can Hackers Bypass a VPN?**

While VPNs provide strong encryption and security, they are not invulnerable. **Hackers can potentially bypass or compromise a VPN** by:

1. **Exploiting Weak Protocols**: Using tools to crack weak encryption algorithms.
2. **Attacking the VPN Server**: If hackers compromise the VPN server, they can monitor or modify user traffic.
3. **Targeting VPN Leaks**: Exploiting DNS, WebRTC, or IPv6 leaks to bypass VPN coverage.
4. **Compromising the End Device**: Malware or direct access to the victim’s device renders VPN protection moot.

However, with **robust VPN protocols** (like OpenVPN, WireGuard) and **strong encryption (AES-256)**, it is difficult for hackers to directly break into a secure VPN connection itself without resorting to other indirect methods like social engineering, device compromise, or server attacks.

  

---

  

# Onion Routing

  

## **What is Onion Routing?**

Onion routing is a technique for anonymous communication over a computer network. It was originally designed by the U.S. Navy to protect sensitive government communications. Today, the most famous implementation of onion routing is **Tor (The Onion Router)**, used for secure, anonymous internet browsing.

- **Onion Routing**: Data is encrypted in multiple layers, like layers of an onion, and is routed through several intermediate nodes (called relays). Each relay only knows the immediate predecessor and successor but not the entire route or destination.
- **Tor (The Onion Router)**: An open-source software that enables anonymous communication by implementing onion routing to hide a user’s location and usage patterns.

  

## **How Onion Routing Works – Under the Hood:**

1. **User Request**: When a user initiates a request to access a website via Tor:
    - The **Tor client** selects a random path of at least three relays (entry node, middle node, exit node) from the Tor network.
2. **Layered Encryption**:
    - The request is encrypted **multiple times** before it is sent. Each layer of encryption corresponds to one of the relays along the path.
    - The outermost layer can only be decrypted by the first relay (entry node), the second layer by the middle relay, and the final layer by the exit node.
3. **Routing the Data**:
    - **Entry Node**: The client’s request first goes to the entry node. This node can see the IP address of the user but does not know the final destination or contents of the data.
    - **Middle Node**: The request is forwarded to a middle relay, which further decrypts the data, without knowing the origin or final destination.
    - **Exit Node**: The last relay (exit node) decrypts the innermost layer, revealing the destination website or server. However, the exit node cannot see the user’s IP address or the original data.
4. **Returning Data**:
    - The response from the destination (e.g., a web server) goes back through the same relays in reverse, each one encrypting it in layers. By the time it reaches the user, only the user’s Tor client can fully decrypt the response.

- **Key Terms**:
    - **Entry Node**: First relay in the circuit, knows the user’s IP.
    - **Middle Node**: Intermediate relay that forwards traffic without knowing the user or the destination.
    - **Exit Node**: Final relay that decrypts and forwards traffic to the destination (e.g., a website).

  

## **Protocols Used in Onion Routing (Tor)**:

- **TLS (Transport Layer Security)**: Tor uses TLS for its encrypted tunnels between relays, ensuring secure communication.
- **RSA**: Public-key cryptography (RSA) is used to establish secure connections and for the encryption of session keys between relays.
- **AES (Advanced Encryption Standard)**: AES is used to encrypt communication between relays for faster and secure data transfer.
- **Diffie-Hellman**: This is used for secure key exchange during the setup of circuits between the client and relays

  

## **Vulnerabilities of Tor**:

While Tor provides significant anonymity, it is not without its flaws. Some vulnerabilities that hackers or authorities may exploit include:

### 1. **End-to-End Timing Attacks**:

- Attackers may attempt to correlate the timing of traffic entering and leaving the Tor network. By analyzing the timing patterns, they could deanonymize users.
- **Mitigation**: Randomized delays and circuit changes within Tor, but the risk persists.

### 2. **Exit Node Monitoring**:

- **Exit Nodes** are a critical point of vulnerability since they can see unencrypted traffic sent to the final destination. Malicious exit nodes can sniff sensitive data (HTTP traffic, email, etc.).
- **Hackers' Exploit**: Attackers can run malicious exit nodes to intercept traffic, monitor users, or inject malicious content.
- **Mitigation**: Use HTTPS or encrypted protocols end-to-end, even within the Tor network.

### 3. **Traffic Correlation**:

- Advanced attackers (like governments) can monitor traffic at both the entry and exit nodes and attempt to correlate patterns to deanonymize users.
- **Hackers’ Exploit**: By monitoring entry points to Tor and exit points to the internet, they can try to link the incoming and outgoing traffic.
- **Mitigation**: Constantly switching relays and ensuring large-scale usage of the Tor network to make such attacks difficult.

### 4. **Sybil Attacks (Relay Manipulation)**:

A **Sybil attack** occurs when a hacker runs a large number of Tor relays simultaneously to try and control enough of the network to deanonymize users.

- **How it Works**:
    - Hackers set up **multiple malicious nodes** in the Tor network. If they manage to control enough nodes, they can potentially see both the user’s IP (from the entry node) and the destination traffic (at the exit node).
    - By increasing their share of nodes in the network, the attacker increases the probability that users will choose their relays for their Tor circuits.
- **Risk**:
    - The attacker could deanonymize users by correlating the traffic from their controlled nodes.
    - If both the entry and exit nodes in a circuit are under the attacker's control, they can directly link the user’s IP to their activities.
- **Example**: In 2020, it was discovered that over **23% of Tor exit relays** were controlled by malicious actors trying to conduct Sybil attacks and monitor user traffic.
- **Defense**: The Tor network tries to prevent Sybil attacks by detecting unusual relay behavior and banning malicious nodes. The randomness in node selection and regular rotation of circuits also helps mitigate the risk.

### 5. **Tor Browser Exploits**:

- Vulnerabilities in the **Tor Browser** (such as JavaScript exploits) can reveal a user’s real IP address.
- **Hackers' Exploit**: By exploiting browser vulnerabilities (e.g., malicious JavaScript), hackers can run malicious code that circumvents the protection provided by Tor.
- **Mitigation**: Tor Browser often disables JavaScript, but exploits may still occur. Keeping the browser and extensions updated is crucial.

### 6. **Guard Node Attacks**:

- The **entry node (guard node)** is the only node that knows the user’s real IP address. A malicious or compromised guard node could deanonymize users.
- **Hackers' Exploit**: If a hacker controls or compromises the guard node, they can trace users by associating their IP address with the encrypted traffic.
- **Mitigation**: Tor automatically rotates guard nodes periodically to reduce risk.

### 7. **Eavesdropping on Public Wi-Fi**:

- Using Tor over public Wi-Fi poses additional risks if attackers control the Wi-Fi access point.
- **Hackers' Exploit**: Hackers can conduct **man-in-the-middle (MITM) attacks** on public networks, injecting malicious content or monitoring unencrypted traffic.
- **Mitigation**: Always use **HTTPS** or other end-to-end encryption protocols.

### 8. **Malware**:

- **Malware** installed on a user's machine can bypass Tor and reveal the user’s identity by directly leaking information or using network connections outside of Tor.
- **Hackers' Exploit**: By distributing malware, hackers can monitor a user’s activity even if they use Tor.
- **Mitigation**: Use secure, updated operating systems (like Tails OS), avoid downloading files while using Tor, and scan for malware regularly.

  

### 9.  **State-Level Attacks**:

- Government agencies with vast surveillance capabilities may attempt to correlate traffic entering and leaving the Tor network.
- **Example**: The NSA has been known to monitor large portions of the internet and correlate Tor traffic with user activity.
- **Possibility**: Highly sophisticated and requires significant resources, but possible.

### 10. **Compromised Relays**:

- Hackers (or authorities) can run malicious relays (entry, middle, or exit nodes) and try to deanonymize users by analyzing traffic patterns.
- **Example**: In 2014, researchers found that malicious relays were being used to deanonymize Tor users in an attack targeting the Tor network.

### 11. **JavaScript and Browser Exploits**:

- Vulnerabilities in the browser can reveal a user’s real IP address, even when they are using Tor.
- **Example**: The **FBI** used a **Firefox vulnerability** in 2013 to deanonymize users of **Tor hidden services** in a child pornography investigation.

### 12. **De-anonymization via Exit Nodes**:

- Malicious exit nodes can sniff unencrypted traffic, capture credentials, and monitor sensitive communications.
- **Example**: Hackers have set up rogue exit nodes to collect unencrypted traffic or inject malicious content.

  

## **How Hackers Might Attack Tor or Exploit It**:
 
- **Running Malicious Nodes**: Hackers can set up multiple relays (entry or exit nodes) to try to monitor traffic and deanonymize users by analyzing patterns.
- **Browser Exploits**: Hackers may exploit vulnerabilities in the Tor browser or encourage users to enable JavaScript, allowing them to run malicious code and reveal user IP addresses.
- **Traffic Analysis**: If hackers control both the entry and exit points, they can use traffic analysis to trace users.
- **Phishing & Social Engineering**: Hackers may use phishing techniques to trick users into revealing sensitive information, bypassing the security offered by Tor.

## can TOR be hacked??

- **Tor Network Attacks**: Hard but possible with extensive resources (traffic correlation, compromised relays, etc.).
- **Client-Side Exploits**: Common attack method (JavaScript exploits, browser vulnerabilities, malware on user devices).

  

---

  

# Firewall

  
## What is Firewall  

**firewall** is a network security system that monitors and controls incoming and outgoing network traffic based on pre-defined security rules. Its main purpose is to act as a barrier between trusted internal networks and untrusted external networks (e.g., the internet), preventing unauthorized access and ensuring network security.  
  
  

## Types of Firewalls

1. **Packet-Filtering Firewall**:
    - **How it Works**: It inspects each packet passing through the network and allows or blocks them based on the source IP address, destination IP address, protocol, and port number.
    - **Use Case**: Provides basic filtering and is often used in routers.
2. **Stateful Inspection Firewall**:
    - **How it Works**: Tracks the state of active connections and makes decisions based on the context of traffic rather than individual packets. It allows traffic only if it is part of an established connection.
    - **Use Case**: Commonly used for managing TCP connections and ensuring legitimate session-based traffic.
3. **Proxy Firewall** (Application-Level Gateway):
    - **How it Works**: Acts as an intermediary between users and the internet, filtering requests at the application layer. It inspects traffic at the protocol level (e.g., HTTP, FTP) and can prevent direct connections between internal and external networks.
    - **Use Case**: Offers more advanced filtering, often used to control web traffic or email traffic.
4. **Next-Generation Firewall (NGFW)**:
    - **How it Works**: Integrates traditional firewall features with additional functionalities like deep packet inspection (DPI), intrusion detection and prevention (IDS/IPS), and application awareness.
    - **Use Case**: Used in enterprise environments for advanced threat protection.
5. **Unified Threat Management (UTM) Firewall**:
    - **How it Works**: Combines various security functions (firewall, antivirus, VPN, content filtering, etc.) into one device, providing comprehensive network protection.
    - **Use Case**: Ideal for small to medium-sized businesses that need all-in-one security solutions.
6. **Cloud Firewalls**:
    - **How it Works**: Firewalls hosted in the cloud to protect cloud-based infrastructure, applications, and services. They offer scalable security for cloud environments.
    - **Use Case**: Used in modern cloud computing environments.

  

## Security Features of Firewalls

- **Packet Filtering**: Firewalls analyze the packets' headers (IP, port, protocol) and enforce rules to allow or deny them.
- **Deep Packet Inspection (DPI)**: Analyzes packet contents, not just headers, to detect malicious data or rule violations.
- **Stateful Inspection**: Firewalls monitor active connections and ensure packets belong to a legitimate session.
- **Intrusion Detection and Prevention (IDPS)**: Detects and blocks suspicious or malicious activities (e.g., port scans, brute-force attacks).
- **Application Awareness**: Firewalls can understand and filter traffic based on specific applications (e.g., allowing Skype but blocking BitTorrent).
- **VPN Integration**: Firewalls often support Virtual Private Network (VPN) functionality to allow secure remote access.

  

## Protocols in use

  

1. TCP: transmission control protocol
2. UDP: User Datagram Protocol
3. IP : Internet Protocol
4. **ICMP: Internet Control Message Protocol**
5. HTTP Hypertext Transfer Protocol
6. HTTPS: Hypertext Transfer Protocol secure
7. **FTP: File Transfer Protocol**
8. SMTP: Simple Mail Transfer Protocol
9. **SNMP (Simple Network Management Protocol)**
10. **Telnet**
11. **SSH (Secure Shell)**
12. **RDP (Remote Desktop Protocol)**
13. **L2TP (Layer 2 Tunneling Protocol)**
14. **PPTP (Point-to-Point Tunneling Protocol)**
15. **IPSec (Internet Protocol Security)**
16. **SSL (Secure Sockets Layer) / TLS (Transport Layer Security)**

  

## How Hackers Exploit Firewalls

Although firewalls provide essential security, hackers can exploit weaknesses or misconfigurations. Here are some ways a hacker might exploit a firewall:

1. **Bypassing Through Open Ports**:
    - **How it Works**: Hackers scan for open ports that are not adequately protected. If a service (e.g., HTTP, FTP) is running on an open port and the firewall allows traffic through it, attackers can exploit vulnerabilities in that service.
    - **Example**: If port 80 (HTTP) is open, an attacker may try to exploit a vulnerability in the web server.
2. **Firewall Misconfigurations**:
    - **How it Works**: Incorrect firewall configurations can expose the network to attacks. For example, if unnecessary ports are left open or inbound rules are too permissive, hackers can use these to gain entry.
    - **Example**: Allowing all inbound traffic from specific IP ranges might let malicious traffic through if the IP range is spoofed.
3. **Firewalking**:
    - **How it Works**: Firewalking is a technique used to map the rules of a firewall. By sending packets with incremental TTL (Time to Live) values, hackers can discover open ports and rules enforced by the firewall.
    - **Exploitation**: Once the hacker identifies which ports and protocols are allowed, they can focus their attacks on those services.
4. **Port Scanning**:
    - **How it Works**: Hackers use tools like **Nmap** to perform **port scanning** to identify open ports and services running behind the firewall. Once they identify open ports, they can exploit vulnerabilities in those services.
    - **Defense**: Firewalls can use port-knocking techniques to obscure open ports, only allowing traffic after a specific sequence of actions.
5. **Application Layer Exploits**:
    - **How it Works**: Even with a firewall in place, if an application (e.g., web server, database) is vulnerable, attackers can exploit weaknesses at the application layer, bypassing the firewall's protection.
    - **Example**: A SQL Injection vulnerability in a web application could allow an attacker to bypass the firewall completely.
6. **Denial-of-Service (DoS) Attacks**:
    - **How it Works**: Hackers can flood a firewall with massive amounts of traffic, overwhelming its processing capabilities and causing legitimate traffic to be blocked or degraded.
    - **Tools**: **Low Orbit Ion Cannon (LOIC)** or **High Orbit Ion Cannon (HOIC)** are common tools for launching DoS attacks.
7. **IP Spoofing**:
    - **How it Works**: Hackers can spoof the source IP address to bypass IP-based firewall rules. Firewalls that rely solely on IP addresses for filtering are vulnerable to IP spoofing.
    - **Example**: Attackers can impersonate a trusted IP to get through the firewall.
8. **Exploiting Stateful Firewalls**:
    - **How it Works**: Some firewalls rely on keeping track of the state of a connection. If an attacker is aware of the traffic patterns, they can send crafted packets that mimic valid sessions to bypass the firewall.
    - **Example**: Using **TCP Split Handshake** tricks the firewall into thinking the attacker's packets are part of an established connection.

  

## How Firewalls Work Under the Hood

1. **Packet Inspection**:
    - Firewalls inspect every packet of data passing through the network. Based on the header information (IP addresses, port numbers, protocol), the firewall decides whether to **allow** or **deny** the packet.
2. **Rule Evaluation**:
    - Firewalls have a set of rules (also called **Access Control Lists**, ACLs). The firewall matches each incoming and outgoing packet against these rules to decide whether to block or allow it.
    - Example rule: `ALLOW TCP traffic from IP 192.168.1.10 to port 80`
3. **Stateful Packet Filtering**:
    - Stateful firewalls track the state of active connections, allowing only packets that are part of an established session. This ensures that only legitimate traffic can pass through.
4. **Logging**:
    - Firewalls log traffic, especially denied packets. This logging is useful for auditing, intrusion detection, and forensic analysis.
5. **Packet Dropping**:
    - If a packet violates any rule (e.g., a suspicious IP, port, or protocol), the firewall drops it without forwarding it to the destination.

  

## How to Crack or Bypass a Firewall

1. **Tunneling**:
    - Hackers can bypass firewalls using **tunneling** protocols like **SSH tunneling**, **VPNs**, or **DNS tunneling**. These methods encapsulate malicious traffic inside legitimate traffic, bypassing the firewall's filtering.
2. **Exploiting Open Ports**:
    - Open ports (e.g., 80/443 for HTTP/HTTPS) often bypass firewall filtering. Attackers can craft exploits targeting services on these ports, as they are allowed through by default.
3. **Social Engineering**:
    - Hackers may convince a network administrator or user to change firewall settings (e.g., by sending phishing emails), leading to vulnerabilities in the configuration.
4. **Bypassing with IPv6**:
    - Some firewalls are misconfigured for IPv6 traffic. Hackers can leverage this by sending IPv6 traffic to bypass IPv4-based firewall rules.

  

## **IDS (Intrusion Detection System)**

### **What is IDS?**

An **Intrusion Detection System (IDS)** is a security tool designed to monitor network or system activity for malicious activity or policy violations. It works by analyzing traffic, logs, and system events to detect unauthorized actions.

- **Types of IDS:**
    1. **Network-Based IDS (NIDS):**
        
        - Monitors network traffic for signs of attacks.
        - Analyzes incoming and outgoing network packets.
        - Examples: Snort, Suricata.
    2. **Host-Based IDS (HIDS):**
        
        - Installed on individual host devices (like servers or workstations).
        - Monitors system activity such as file integrity, logs, and user behavior.
        - Examples: OSSEC, Tripwire.
    3. **Signature-Based IDS:**
        
        - Relies on predefined patterns (signatures) of known attacks.
        - It compares incoming traffic to these signatures to detect attacks.
        - Pros: Effective at detecting known threats.
        - Cons: Cannot detect new or unknown threats.
    4. **Anomaly-Based IDS:**
        
        - Monitors baseline traffic and behavior to detect deviations.
        - It raises alarms when there is unusual activity or a pattern that doesn’t match typical behavior.
        - Pros: Can detect new, unknown attacks (zero-day).
        - Cons: Higher false positives if the baseline isn't accurate.
    5. **Hybrid IDS:**
        
        - Combines both signature-based and anomaly-based detection.
        - Attempts to balance the strengths of both methods.
        - Example: Snort with additional anomaly detection plugins.

### **Security Features of IDS:**

1. **Alert Generation:**
    
    - IDS generates alerts when it detects suspicious activity or known attack signatures.
2. **Logging:**
    
    - IDS logs detected events for analysis, helping in forensic investigations.
3. **Traffic Analysis:**
    
    - IDS inspects network traffic to identify malicious behavior based on known attack patterns (signatures) or unusual activity (anomalies).
4. **Real-Time Monitoring:**
    
    - Most IDS solutions operate in real-time, providing immediate feedback to the security team.

### **How Hackers Exploit IDS:**

1. **Evasion Techniques:**
    
    - **Packet Fragmentation:** Hackers can break malicious payloads into smaller fragments to evade signature-based detection. IDS may not reassemble fragments properly, allowing the attack to slip through.
    - **Polymorphic Malware:** Attackers change the appearance of malware (its signature) to evade detection.
    - **Obfuscation:** Malicious payloads are encoded or disguised to evade detection by IDS signatures.
2. **Flooding the IDS with Noise:**
    
    - Attackers may flood the IDS with so much data that it becomes overwhelmed, causing it to miss legitimate attacks (Denial of Service for IDS).
3. **Tunneling:**
    
    - Hackers may tunnel malicious traffic over encrypted or uncommon ports to bypass IDS detection.
4. **Zero-Day Exploits:**
    
    - IDS systems rely heavily on signatures, and new attacks may not have signatures in the IDS database, allowing zero-day exploits to bypass detection.

### **How IDS Works Under the Hood:**

1. **Traffic Inspection:**
    
    - IDS monitors traffic using packet capture tools like **Wireshark** or **tcpdump**.
    - It inspects headers and payloads of network packets for known attack patterns or deviations.
2. **Signature Matching (for Signature-based IDS):**
    
    - The IDS compares incoming traffic to a database of attack signatures and flags matching patterns as potential intrusions.
3. **Anomaly Detection (for Anomaly-based IDS):**
    
    - The IDS creates a baseline of normal traffic and alerts if the traffic deviates significantly from this baseline.
4. **Behavioral Analysis:**
    
    - HIDS monitors system processes, file integrity, login events, and resource usage for suspicious patterns.

---

## **IPS (Intrusion Prevention System)**

### **What is IPS?**

An **Intrusion Prevention System (IPS)** is similar to an IDS but goes a step further by not only detecting malicious activity but also actively blocking or preventing it. IPS is often deployed inline in the network, allowing it to actively intercept and block threats in real-time.

- **Types of IPS:**
    1. **Network-Based IPS (NIPS):**
        
        - Monitors and analyzes network traffic for signs of attacks and takes action to block malicious packets.
        - Example: Cisco FirePower, Suricata (with IPS features).
    2. **Host-Based IPS (HIPS):**
        
        - Installed on individual machines (like HIDS but with prevention features).
        - Monitors for local system attacks and prevents or quarantines harmful processes.
        - Example: OSSEC with prevention modules.
    3. **Signature-Based IPS:**
        
        - Like IDS, but it also takes action to block any traffic matching a known attack signature.
        - Blocking can be done by dropping packets, resetting connections, or blocking IPs.
    4. **Anomaly-Based IPS:**
        
        - Identifies unusual patterns or deviations from established behavior and takes preventive actions.
        - Can stop new or unknown attacks (zero-day) that deviate from normal network behavior.
    5. **Hybrid IPS:**
        
        - Combines both signature-based and anomaly-based methods to provide more robust protection.

### **Security Features of IPS:**

1. **Real-Time Prevention:**
    
    - IPS not only detects but actively blocks or mitigates attacks.
2. **Traffic Blocking:**
    
    - Can drop malicious packets, reset connections, or block traffic from a suspicious IP address.
3. **Alerting and Logging:**
    
    - Similar to IDS, IPS generates alerts, but it can also provide additional context, such as reasons for blocking traffic.
4. **Protocol Anomaly Detection:**
    
    - IPS can monitor protocols like HTTP, DNS, or FTP for anomalies, ensuring that valid traffic is not mistaken for malicious.

### **How Hackers Exploit IPS:**

1. **Evasion:**
    
    - **Encrypted Traffic:** Attackers might use SSL/TLS encryption to disguise malicious payloads from IPS (as IPS may not decrypt the traffic).
    - **Fragmentation and Tunneling:** Attackers might fragment packets or use uncommon ports to avoid detection.
2. **DoS on IPS:**
    
    - Similar to IDS, attackers may overwhelm IPS systems with traffic, forcing the IPS to fail or miss attacks.
3. **Exploiting IPS's False Positives:**
    
    - Attackers may generate legitimate-looking traffic to overwhelm the IPS with false positives, causing it to block legitimate traffic and allow the attack to go through.
4. **Zero-Day and Custom Payloads:**
    
    - IPS systems depend on signatures, and a novel attack with no signature can often bypass IPS defenses.

### **How IPS Works Under the Hood:**

1. **Inline Traffic Analysis:**
    
    - IPS systems are often deployed inline, meaning they sit directly in the traffic path. They analyze packets as they pass through and can block harmful traffic immediately.
2. **Signature Matching and Blocking:**
    
    - Similar to IDS, the IPS matches packets to a signature database. If a match is found, the IPS blocks the malicious packet.
3. **Anomaly Detection and Mitigation:**
    
    - When traffic deviates significantly from normal patterns, the IPS triggers preventive measures such as dropping packets or resetting connections.
4. **Behavioral Analysis:**
    
    - IPS systems analyze traffic patterns and behavior to detect new or unknown attacks based on unusual activities or behavior outside established norms.

---

## **How to Crack or Bypass IDS/IPS (For Ethical Hacking and Testing)**

As an ethical hacker, understanding how attackers bypass IDS/IPS is crucial for testing and improving security measures. Here are some techniques:

1. **Encryption (SSL/TLS):**
    
    - Encrypting traffic helps attackers bypass network-based IDS/IPS, as the system can’t inspect the payload inside the encrypted traffic.
2. **Tunneling Attacks:**
    
    - Attackers use common protocols (HTTP, DNS) to tunnel malicious traffic, hoping to evade detection by the IDS/IPS.
3. **Fragmentation:**
    
    - By fragmenting malicious packets, attackers can evade signature-based IDS/IPS that don’t reassemble the fragments.
4. **Polymorphism:**
    
    - Attackers modify the signature of their attack to make it unrecognizable by signature-based IDS/IPS systems.
5. **DoS/DDoS Attacks on IDS/IPS:**
    
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
