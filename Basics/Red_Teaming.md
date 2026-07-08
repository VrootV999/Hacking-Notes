# Vulnerability Assesment and Penetration Test limitations
Vulnerability Assessments

This is the simplest form of security assessment, and its main objective is to identify as many vulnerabilities in as many systems in the network as possible. To this end, concessions may be made to meet this goal effectively. For example, the attacker's machine may be allowlisted on the available security solutions to avoid interfering with the vulnerability discovery process. This makes sense since the objective is to look at every host on the network and evaluate its security posture individually while providing the most information to the company about where to focus its remediation efforts.

To summarize, a Vulnerability Assessment focuses on scanning hosts for vulnerabilities as individual entities so that security deficiencies can be identified and effective security measures can be deployed to protect the network in a prioritized manner. Most of the work can be done with automated tools and performed by operators without requiring much technical knowledge.

As an example, if you were to run a vulnerability assessment over a network, you would normally try to scan as many of the hosts as possible, but wouldn't actually try exploiting any vulnerabilities at all:

---
# Penetration Test
On top of scanning every single host for vulnerabilities, we often need to understand how they impact our network as a whole. Penetration tests add to vulnerability assessments by allowing the pentester to explore the impact of an attacker on the overall network by doing additional steps that include:

1. Attempt to exploit the vulnerabilities found on each system. This is important as sometimes a vulnerability might exist in a system, but compensatory controls in place effectively prevent its exploitation. It also allows us to test if we can use the detected vulnerabilities to compromise a given host.
2. Conduct post-exploitation tasks on any compromised host, allowing us to find if we can extract any helpful information from them or if we might use them to pivot to other hosts that were not previously accessible from where we stand.

- Penetration tests might start by scanning for vulnerabilities just as a regular but provide further information on how an attacker can chain vulnerabilities to achieve specific goals. While its focus remains on identifying vulnerabilities and establishing measures to protect the network, it also considers the network as a whole ecosystem and how an attacker could profit from interactions between its components.

- If we were to perform a penetration test using the same example network as before, on top of scanning all of the hosts on the network for vulnerabilities we would try confirm if they can be exploited in order to show the impact an attacker could have on the network: 

- By analyzing how an attacker could move around our network, we also gain a basic insight on possible security measure bypasses and our ability to detect a real threat actor to a certain extent, limited because the scope of a penetration test is usually extensive and Penetration testers don't care much about being loud or generating lots of alerts on security devices since time constraints on such projects often requires us to check the network in a short time.

---
# Advanced Persistent Threats and why Regular Pentesting is not Enough
- While the conventional security engagements we have mentioned cover the finding of most technical vulnerabilities, there are limitations on such processes and the extent to which they can effectively prepare a company against a real attacker. Such limitations include:
- As a consequence, some aspects of penetration tests might significantly differ from a real attack, like:

1. Penetration tests are LOUD: Usually, pentesters won't put much effort into trying to go undetected. Unlike real attackers, they don't mind being easy to detect, as they have been contracted to find as many vulnerabilities as they can in as many hosts as possible.
2. Non-technical attack vectors might be overlooked: Attacks based on Social Engineering or physical intrusions are usually not included in what is tested.
3. Relaxation of security mechanisms: While doing a regular penetration test, some security mechanisms might be temporarily disabled or relaxed for the pentesting team in favor of efficiency. Although this might sound counterintuitive, it is essential to remember that pentesters have limited time to check the network. Therefore, it is usually desired not to waste their time searching for exotic ways to bypass IDS/IPS, WAF, intrusion deception or other security measures, but rather focus on reviewing critical technological infrastructure for vulnerabilities.

- On the other hand, real attackers won't follow an ethical code and are mostly unrestricted in their actions. Nowadays, the most prominent threat actors are known as Advanced Persistent Threats (APT), which are highly skilled groups of attackers, usually sponsored by nations or organised criminal groups. They primarily target critical infrastructure, financial organisations, and government institutions. They are called persistent because the operations of these groups can remain undetected on compromised networks for long periods.

- If a company is affected by an APT, would it be prepared to respond effectively? Could they detect the methods used to gain and maintain access on their networks if the attacker has been there for several months? What if the initial access was obtained because John at accounting opened a suspicious email attachment? What if a zero-day exploit was involved? Do previous penetration tests prepare us for this?

---
# Red Team Engagement
- To keep up with the emerging threats, red team engagements were designed to shift the focus from regular penetration tests into a process that allows us to clearly see our defensive team's capabilities at detecting and responding to a real threat actor. They don't replace traditional penetration tests, but complement them by focusing on detection and response rather than prevention.

- Red teaming is a term borrowed from the military. In military exercises, a group would take the role of a red team to simulate attack techniques to test the reaction capabilities of a defending team, generally known as blue team, against known adversary strategies. Translated into the world of cybersecurity, red team engagements consist of emulating a real threat actor's Tactics, Techniques and Procedures (TTPs) so that we can measure how well our blue team responds to them and ultimately improve any security controls in place.

- Every red team engagement will start by defining clear goals, often referenced as crown jewels or flags, ranging from compromising a given critical host to stealing some sensitive information from the target. Usually, the blue team won't be informed of such exercises to avoid introducing any biases in their analysis. The red team will do everything they can to achieve the goals while remaining undetected and evading any existing security mechanisms like firewalls, antivirus, edr, ips/ids and others. Notice how on a red team engagement, not all of the hosts on a network will be checked for vulnerabilities. A real attacker would only need to find a single path to its goal and is not interested in performing noisy scans that the blue team could detect.

- Taking the same network as before, on a red team engagement where the goal is to compromise the intranet server, we would plan for a way to reach our objective while interacting as little as possible with other hosts. Meanwhile, the blue team's capacity to detect and respond accordingly to the attack can be evaluated: 

- It is important to note that the final objective of such exercises should never be for the red team to "beat" the blue team, but rather simulate enough TTPs for the to learn to react to a real ongoing threat adequately. If needed, they could tweak or add security controls that help to improve their detection capabilities.

- Red team engagements also improve on regular penetration tests by considering several attack surfaces:
    - Technical Infrastructure: Like in a regular penetration test, a red team will try to uncover technical vulnerabilities, with a much higher emphasis on stealth and evasion.
    - Social Engineering: Targeting people through phishing campaigns, phone calls or social media to trick them into revealing information that should be private.
    - Physical Intrusion: Using techniques like lockpicking, RFID cloning, exploiting weaknesses in electronic access control devices to access restricted areas of facilities.

- Depending on the resources available, the red team exercise can be run in several ways:
    - Full Engagement: Simulate an attacker's full workflow, from initial compromise until final goals have been achieved.
    - Assumed Breach: Start by assuming the attacker has already gained control over some assets, and try to achieve the goals from there. As an example, the red team could receive access to some user's credentials or even a workstation in the internal network.
    - Table-top Exercise:  An over the table simulation where scenarios are discussed between the red and blue teams to evaluate how they would theoretically respond to certain threats. Ideal for situations where doing live simulations might be complicated.

---
# Teams and Functions of an Engagement
There are several factors and people involved within a red team engagement. Everyone will have their mindset and methodology to approach the engagement personnel; however, each engagement can be broken into three teams or cells. Below is a brief table illustrating each of the teams and a brief explanation of their responsibilities.
| Team | Definition |
| ---- | ---- |
| Red Cell |	A red cell is the component that makes up the offensive portion of a red team engagement that simulates a given target's strategic and tactical responses. |
| Blue Cell |	The blue cell is the opposite side of red. It includes all the components defending a target network. The blue cell is typically comprised of blue team members, defenders, internal staff, and an organisation's management. | 
| White Cell | Serves as referee between red cell activities and blue cell responses during an engagement. Controls the engagement environment/network. Monitors adherence to the ROE. Coordinates activities required to achieve engagement goals. Correlates red cell activities with defensive actions. Ensures the engagement is conducted without bias to either side. | 


- These teams or cells can be broken down further into an engagement hierarchy.
- Since this is a red team-oriented room, we will focus on the responsibilities of the red cell. Below is a table outlining the roles and responsibilities of members of the red team.

| Role | Purpose | 
| ---- | ---- |
| Red Team Lead 	| Plans and organises engagements at a high level—delegates, assistant lead, and operators engagement assignments. | 
| Red Team Assistant Lead  | 	Assists the team lead in overseeing engagement operations and operators. Can also assist in writing engagement plans and documentation if needed. | 
| Red Team Operator | Executes assignments delegated by team leads. Interpret and analyse engagement plans from team leads. | 

- As with most red team functions, each team and company will have its own structure and roles for each team member. The above table only acts as an example of the typical responsibilities of each role.

---
# Engagement structure
- A core function of the red team is adversary emulation. While not mandatory, it is commonly used to assess what a real adversary would do in an environment using their tools and methodologies. The red team can use various cyber kill chains to summarize and assess the steps and procedures of an engagement.

- The blue team commonly uses cyber kill chains to map behaviors and break down an adversaries movement. The red team can adapt this idea to map adversary TTPs (Tactics, Techniques, and Procedures) to components of an engagement.

- Many regulation and standardization bodies have released their cyber kill chain. Each kill chain follows roughly the same structure, with some going more in-depth or defining objectives differently. Below is a small list of standard cyber kill chains.

    - Lockheed Martin Cyber Kill Chain 
    - Unified Kill Chain 
    - Varonis Cyber Kill Chain 
    - Active Directory Attack Cycle 
    - ATT&CK Framework 

- In this room, we will commonly reference the "Lockheed Martin Cyber Kill Chain." It is a more standardized kill chain than others and is very commonly used among red and blue teams.

- The Lockheed Martin kill chain focuses on a perimeter or external breach. Unlike other kill chains, it does not provide an in-depth breakdown of internal movement. You can think of this kill chain as a summary of all behaviors and operations present.

Components of the kill chain are broken down in the table below.
| Technique | Purpose | Examples | 
| ---- | ---- | ---- |
| Reconnaissance | Obtain information on the target | Harvesting emails, | 
| Weaponization | Combine the objective with an exploit. Commonly results in a deliverable payload. | Exploit with backdoor, malicious office document| 
| Delivery | How will the weaponized function be delivered to the target | Email, web, USB | 
| Exploitation | Exploit the target's system to execute code | MS17-010, Zero-Logon, etc. | 
| Installation | Install malware or other tooling | Mimikatz, Rubeus, etc. | 
| Command & Control | Control the compromised asset from a remote central controller | Empire, Cobalt Strike, etc. |
| Actions on Objectives | Any end objectives: ransomware, data exfiltration, etc. | Conti, LockBit2.0, etc.| 


---
# Engagement Details
## Red Team Engagement Planning: Objectives, Scope, and Approaches
1. The Core Foundation: Client Objectives

Client objectives are the ultimate keystone of a red team engagement. Because engagements are inherently complex and highly bureaucratic, clearly defined goals prevent the campaign from becoming unstructured, unplanned, and ineffective.

- Mutual Understanding: Objectives must be collaboratively discussed and agreed upon by both the client and the red team to align expectations on deliverables.

- Documentation & Design: These objectives form the direct basis for all subsequent engagement documentation, rules of engagement (RoE), and tactical planning.

- Tone Setting: Objectives establish the overall tone, boundaries, and underlying philosophy of the entire campaign.

> [!DANGER]  DANGER
> The Risk of No Objectives: Without concrete goals, a red team campaign devolves into a chaotic, 


## 2. Categorizing the Engagement Approach

Depending on the client's objectives and cyber maturity, the red team must decide how focused the assessment will be. Engagements generally fall into two categories:

- A. Focused Adversary Emulation
    - Definition: A highly targeted campaign designed to mimic the specific Tactics, Techniques, and Procedures (TTPs) of a real-world threat actor.

    - Targeting: The red team emulates a specific Advanced Persistent Threat (APT) group or threat actor known to target the client's specific industry.

    - Example: A financial institution emulating APT38 (a North Korean state-sponsored threat group specializing in financial cyberheists).

- B. General Internal / Network Penetration Test

    - Definition: A broader, less targeted assessment of the network infrastructure.

    - Targeting: It utilizes a wider, more standard array of TTPs rather than restricting itself to a single threat actor's playbook.

    - Purpose: Aims to uncover as many systemic vulnerabilities and configuration weaknesses as possible across the environment.

| Feature | General Penetration Test | Focused Adversary Emulation | 
| ---- | ---- | ---- |
| Focus | Broad network/infrastructure vulnerabilities | Specific threat actor behaviors & TTPs | 
| TTPs Used | "Standard wide-ranging security exploits" | "Threat intelligence-driven actor-specific" | 
| Primary Goal | Identify as many flaws as possible | Test detection and response capabilities | 


## 3. Defining the Scope (The Boundaries)
While objectives outline what the client wants to achieve, the scope defines the operational boundaries of where and how the red team can maneuver.

- Client Ownership: Unlike objectives (which are mutually discussed), the scope should only be definitively set by the client, as they possess the ultimate understanding of their own network risks and operational liabilities.
- Red Team Feedback: The red team may raise a grievance or concern if a scope restriction severely hinders the viability of the engagement, but the client retains final sign-off.
- Inclusions vs. Exclusions: A well-defined scope explicitly outlines what is in-scope (authorized targets) and what is out-of-scope (strictly forbidden targets/actions).

Common Verbiage & Examples in a Scope Document:
- `10.0.0.8/20` is in scope.
- `10.0.3.8/18` is out of scope.
- Production servers are completely off-limits.
- No exfiltration of sensitive data or personally identifiable information (PII) is permitted.
- System downtime or service disruption is not permitted under any circumstances.

## 4. Expanding the Framework: Crucial Additions for Red Team Success

To elevate these notes into a production-ready framework, the following industry-standard elements must be integrated into the planning phase:

- Rules of Engagement (RoE): A formal, legally binding document derived from the scope. It outlines execution timelines, communication channels (such as daily status updates), and specific technical constraints (e.g., specific hours testing can occur).

- The "Get Out of Jail Free" Card: A formal authorization letter signed by high-level executives (e.g., CISO or CIO). It grants the red team explicit permission to conduct simulated attacks and must be carried by operators at all times during physical or sensitive digital testing.

- Deconfliction Protocols: A pre-arranged process to handle situations where the client's internal Blue Team (SOC) detects the Red Team. The client's trusted agents must be able to verify whether an alert is a result of the simulated engagement or an actual malicious breach.

## 5. Red Team Analysis & Strategic Execution

When a red team receives a bare reading of the client's objectives and scope, they must analyze it with a dynamic, adversary-focused mindset.

- Read Between the Lines: Understand the deeper security implications behind the client's restrictions (e.g., if production is off-limits, look for staging environments that mirror production).
- Immediate Drafts: The red team should be capable of drafting comprehensive, actionable engagement plans based solely on the initial constraints and goals provided.
- From Objectives to Action: The client's objectives only set the baseline definition. The final, granular execution steps—including delivery vectors, persistence mechanisms, and lateral movement paths—will be expanded upon in the formal Engagement Plan.

---
# Rules of Engagement (RoE)
Rules of Engagement (RoE) are a legally binding outline of the client objectives and scope with further details of engagement expectations between both parties. This is the first "official" document in the engagement planning process and requires proper authorization between the client and the red team. This document often acts as the general contract between the two parties; an external contract or other NDAs (Non-Disclosure Agreement) can also be used.

The format and wording of the RoE are critical since it is a legally binding contract and sets clear expectations.

Each structure will be determined by the client and red team and can vary in content length and overall sections. Below is a brief table of standard sections you may see contained in the RoE.
| Section Name | Section Details | 
| ---- | ---- |
| Executive Summary	| Overarching summary of all contents and authorization within RoE document | 
| Purpose | Defines why the RoE document is used | 
| References | Any references used throughout the RoE document (HIPPA, ISO, etc.) | 
| Scope | Statement of the agreement to restrictions and guidelines | 
| Definitions | Definitions of technical terms used throughout the RoE document |
| Rules of Engagement and Support Agreement	| Defines obligations of both parties and general technical expectations of engagement conduct | 
| Provisions | Define exceptions and additional information from the Rules of Engagement | 
| Requirements, Restrictions, and Authority | Define specific expectations of the red team cell |
| Ground Rules| Define limitations of the red team cell's interactions |
| Resolution of Issues/Points of Contact | Contains all essential personnel involved in an engagement | 
| Authorization | Statement of authorization for the engagement | 
| Approval | Signatures from both parties approving all subsections of the preceding document | 
| Appendix | Any further information from preceding subsections | 


When analyzing the document, it is important to remember that it is only a summary, and its purpose is to be a legal document. Future and more in-depth planning are required to expand upon the RoE and client objectives.

---
# Campaign Planning
Prior to this task, we have primarily focused on engagement planning and documentation from the business perspective. Campaign planning uses the information acquired and planned from the client objectives and and applies it to various plans and documents to identify how and what the red team will do.

Each internal red team will have its methodology and documentation for campaign planning. We will be showing one in-depth set of plans that allows for precise communication and detailed documentation. The campaign summary we will be using consists of four different plans varying in-depth and coverage adapted from military operations documents. Each plan can be found in the table below with a brief explanation.

| Type of Plan | Explanation of Plan | Plan Contents | 
| ---- | ---- | ---- | 
| Engagement Plan | An overarching description of technical requirements of the red team. |  CONOPS, Resource and Personnel Requirements, Timelines | 
| Operations Plan | An expansion of the Engagement Plan. Goes further into specifics of each detail.  | Operators, Known Information, Responsibilities, etc. | 
| Mission Plan | The exact commands to run and execution time of the engagement. | Commands to run, Time Objectives, Responsible Operator, etc. | 
| Remediation Plan | Defines how the engagement will proceed after the campaign is finished. |  Report, Remediation consultation, etc. | 


---
# Engagement Documents

Engagement Plan:
| Component	| Purpose | 
| ---- | --- | 
| CONOPS (Concept of Operations) | Non-technically written overview of how the red team meets client objectives and target the client. | 
| Resource plan | Includes timelines and information required for the red team to be successful—any resource requirements: personnel, hardware, cloud requirements. | 

Operations Plan:
| Component | Purpose | 
| ---- | ---- | 
| Personnel | Information on employee requirements. | 
| Stopping conditions | How and why should the red team stop during the engagement. | 
| RoE (optional) | - | 
| Technical requirements | What knowledge will the red team need to be successful. | 

Mission Plan:
| Component | Purpose | 
| ---- | ---- | 
| Command playbooks (optional) | Exact commands and tools to run, including when, why, and how. Commonly seen in larger teams with many operators at varying skill levels.| 
| Execution times | Times to begin stages of engagement. Can optionally include exact times to execute tools and commands. | 
| Responsibilities/roles | Who does what, when. | 


Remediation Plan (optional):
| Component	| Purpose | 
| ---- | ---- | 
| Report |  Summary of engagement details and report of findings. | 
| Remediation/consultation  | How will the client remediate findings? It can be included in the report or discussed in a meeting between the client and the red team.|

--- 
## Resource Plan
The resource plan is the second document of the engagement plan, detailing a brief overview of dates, knowledge required (optional), resource requirements. The plan extends the CONOPS and includes specific details, such as dates, knowledge required, etc.

Unlike the CONOPS, the resource plan should not be written as a summary; instead, written as bulleted lists of subsections. As with most red team documents, there is no standard set of resource plan templates or documents; below is an outline of example subsections of the resource plan.

- Header
    - Personnel writing
    - Dates
    - Customer
- Engagement Dates
    - Reconnaissance Dates
    - Initial Compromise Dates
    - Post-Exploitation and Persistence Dates
    - Misc. Dates
- Knowledge Required (optional)
    - Reconnaissance
    - Initial Compromise
    - Post-Exploitation
- Resource Requirements
    - Personnel
    - Hardware
    - Cloud
    - Misc.

The key to writing and understanding a resource plan is to provide enough information to gather what is required but not become overbearing. The document should be straight to the point and define what is needed.

---
## Operations Plan
The operations plan is a flexible document(s) that provides specific details of the engagement and actions occurring. The plan expands upon the current CONOPS and should include a majority of specific engagement information; the RoE can also be placed here depending on the depth and structure of the RoE.

The operations plan should follow a similar writing scheme to the resource plan, using bulleted lists and small sub-sections. As with the other red team documents, there is no standard set of operation plan templates or documents; below is an outline of example subsections within the operations plan.

- Header
    - Personnel writing
    - Dates
    - Customer
- Halting/stopping conditions (can be placed in RoE depending on depth)
- Required/assigned personnel
- Specific TTPs and attacks planned
- Communications plan
- Rules of Engagement (optional)

The most notable addition to this document is the communications plan. The communications plan should summarize how the red cell will communicate with other cells and the client overall. Each team will have its preferred method to communicate with clients. Below is a list of possible options a team will choose to communicate.

- vectr.io (opens in new tab)
- Email
- Slack

---
## Mission Plan
The mission plan is a cell-specific document that details the exact actions to be completed by operators. The document uses information from previous plans and assigns actions to them.

How the document is written and detailed will depend on the team; as this is an internally used document, the structure and detail have less impact. As with all the documents outlined in this room, presentation can vary; this plan can be as simple as emailing all operators. Below is a list of the minimum detail that cells should include within the plan.

- Objectives
- Operators
- Exploits/Attacks
- Targets (users/machines/objectives)
- Execution plan variations

The two plans can be thought of similarly; the operations plan should be considered from a business and client perspective, and the mission plan should be thought of from an operator and red cell perspective.

---
# Concept of Operations (CONOPS)

The Concept of Operation (CONOPS) is a part of the engagement plan that details a high-level overview of the proceedings of an engagement; we can compare this to an executive summary of a penetration test report. The document will serve as a business/client reference and a reference for the red cell to build off of and extend to further campaign plans.

The CONOPS document should be written from a semi-technical summary perspective, assuming the target audience/reader has zero to minimal technical knowledge. Although the CONOPS should be written at a high level, you should not omit details such as common tooling, target group, etc. As with most red team documents, there is not a set standard of a CONOPS document; below is an outline of critical components that should be included in a CONOPS

- Client Name
- Service Provider
- Timeframe
- General Objectives/Phases
- Other Training Objectives (Exfiltration)
- High-Level Tools/Techniques planned to be used
- Threat group to emulate (if any)

The key to writing and understanding a CONOPS is to provide just enough information to get a general understanding of all on-goings. The CONOPS should be easy to read and show clear definitions and points that readers can easily digest.

---
# Threat Intelligence
Threat Intelligence (TI) or Cyber Threat Intelligence (CTI) is the information, or TTPs (Tactics, Techniques, and Procedures), attributed to an adversary, commonly used by defenders to aid in detection measures. The red cell can leverage CTI from an offensive perspective to assist in adversary emulation.

CTI can be consumed (to taken action upon data) by collecting IOCs (Indicators of Compromise) and TTPs commonly distributed and maintained by ISACs (Information and Sharing Analysis Centers). Intelligence platforms and frameworks also aid in the consumption of CTI, primarily focusing on an overarching timeline of all activities.

> [!Note]
> The term ISAC is used loosely in the threat intelligence landscape and often refers to a threat intelligence platform.

Traditionally, defenders use threat intelligence to provide context 
to the ever-changing threat landscape and quantify findings.
IOCs are quantified by traces left by adversaries such as domains, 
IPs, files, strings, etc. 
The Blue Team can utilize various IOCs to build detections and analyze behavior. 
From a red team perspective, you can think of threat intelligence as 
the red team's analysis of the Blue Team's ability to properly leverage for detections.

---
## Applying Threat Intel to the Red Team
As previously mentioned, the red team will leverage CTI to aid in adversary emulation and support evidence of an adversary's behaviors.

To aid in consuming CTI and collecting TTPs, red teams will often use threat intelligence platforms and frameworks such as  MITRE ATT&CK, TIBER-EU, and OST Map.

These cyber frameworks will collect known TTPs and categorize them based on varying characteristics such as,

- Threat Group
- Kill Chain Phase
- Tactic
- Objective/Goal

Once a targeted adversary is selected, the goal is to identify all TTPs categorized with that chosen adversary and map them to a known cyber kill chain. This concept is covered further in the next task.

Leveraging TTPs is used as a planning technique rather than something a team will focus on during engagement execution. Depending on the size of the team, a CTI team or threat intelligence operator may be employed to gather TTPs for the red team. During the execution of an engagement, the red team will use threat intelligence to craft tooling, modify traffic and behavior, and emulate the targeted adversary. This concept is covered further in task 5.

Overall the red team consumes threat intelligence to analyze and emulate the behaviors of adversaries through collected TTPs and IOCs.

---
## TIBER-EU Framework
TIBER-EU (Threat Intelligence-based Ethical Red Teaming) is a common framework developed by the European Central Bank that centers around the use of threat intelligence.

From the ECB TIBER-EU white paper (opens in new tab), "The Framework for Threat Intelligence-based Ethical Red Teaming (TIBER-EU) enables European and national authorities to work with financial infrastructures and institutions (hereafter referred to collectively as 'entities') to put in place a programme to test and improve their resilience against sophisticated cyber attacks."

The main difference between this framework and others is the "Testing" phase that requires threat intelligence to feed the red team's testing.

This framework encompasses a best practice rather than anything actionable from a red team perspective.

There are several public white papers and documents if you are interested in reading about this framework further,

[ecb.europa](https://www.ecb.europa.eu/pub/pdf/other/ecb.tiber_eu_framework.en.pdf)
[crest](https://www.crest-approved.org/membership/tiber-eu/)

---
## TTP mapping
TTP Mapping is employed by the red cell to map adversaries' collected TTPs to a standard cyber kill chain. Mapping TTPs to a kill chain aids the red team in planning an engagement to emulate an adversary.

To begin the process of mapping TTPs, an adversary must be selected as the target. An adversary can be chosen based on,

- Target Industry
- Employed Attack Vectors
- Country of Origin
- Other Factors

MITRE ATT&CK will do most of the work needed, but we can also supplement threat intelligence information with other platforms and frameworks. Another example of a TTP framework is OST Map.

[ost-map](https://github.com/intezer/ost-map)

OST Map provides a visual map to link multiple threat actors and their TTPs.

Other open-source and enterprise threat intelligence platforms can aid red teamers in adversary emulation and mapping, such as,
- Mandiant Advantage
- Ontic
- CrowdStrike Falcon

---
## Other Red Team application of CTI
CTI can also be used during engagement execution, emulating the adversary's behavioral characteristics, such as
- C2 Traffic
    - User Agents
    - Ports, Protocols
    - Listener Profiles
- Malware and Tooling
    - IOCs
    - Behaviors

The first behavioral use of CTI we will showcase is C2(Command & Control) traffic manipulation. A red team can use CTI to identify adversaries' traffic and modify their C2 traffic to emulate it.

An example of a red team modifying C2 traffic based on gathered CTI is malleable profiles (opens in new tab). A malleable profile allows a red team operator to control multiple aspects of a C2's listener traffic.

Information to be implemented in the profile can be gathered from ISACs and collected IOCs or packet captures, including,
- Host Headers
- POST URIs
- Server Responses and Headers

The gathered traffic can aid a red team to make their traffic look similar to the targeted adversary to get closer to the goal of adversary emulation.

The second behavioral use of CTI is analyzing behavior and actions of an adversaries' malware and tools to develop your offensive tooling that emulates similar behaviors or has similar vital indicators.

An example of this could be an adversary using a custom dropper. The red team can emulate the dropper by,
- Identifying traffic
- Observing syscalls and API calls
- Identifying overall dropper behavior and objective
- Tampering with file signatures and IOCs

Intelligence and tools gathered from behavioral threat intelligence can aid a red team in preparing the specific tools they will use to action planned TTPs.

---
## Creating a Threat Intel Driven Campaign 
A threat-intel-driven campaign will take all knowledge and topics previously covered and combine them to create a well-planned and researched campaign.

The task flow in this room logically follows the same path you would take as a red team to begin planning a campaign,

1. Identify framework and general kill chain
2. Determine targeted adversary
3. Identify adversary's TTPs and IOCs
4. Map gathered threat intelligence to a kill chain or framework
5. Draft and maintain needed engagement documentation
6. Determine and use needed engagement resources (tools, C2, modification, domains, etc.)

### Comparing CyberKill Chain with MITRE Framework

| Cyber Kill Chain | MIRE ATT&CK | 
| ---- | ---- |
| Recon | Reconnaissance | 
| Weaponization | Execution | 
| Delivery | Initial Access | 
| Exploitation | Initial Access | 
| Installation | Persistence/Defense Evasion |
| Command & Control | Command and Control | 
| Actions on Objectives | Exfiltration / Impact |

---
# Operational Security(OPSEC)
“Systematic and proven process by which potential adversaries can be denied information about capabilities and intentions by identifying, controlling, and protecting generally unclassified evidence of the planning and execution of sensitive activities. The process involves five steps: identification of critical information, analysis of threats, analysis of vulnerabilities, assessment of risks, and application of appropriate countermeasures.”

Let’s dive into the definition from a Red team perspective. As a Red team member, your potential adversaries are the Blue team and third parties. The Blue Team is considered an adversary as we are attacking the systems they are hired to monitor and defend. Red vs Blue Team. exercises are common to help an organization understand what threats exist in a given environment and better prepare their Blue team if a real malicious attack occurs. As Red teamers, even though we are abiding by the law and authorized to attack systems within a defined scope, it does not change the fact that we are acting against The Blue team's objectives and trying to circumvent their security controls. The Blue team wants to protect their systems, while we want to penetrate them.

Denying any potential adversary the ability to gather information about our capabilities and intentions is critical to maintaining OPSEC.OPSEC is a process to identify, control and protect any information related to the planning and execution of our activities. Frameworks such as Lockheed Martin's Cyber Kill Chain and MITRE ATT&CK help defenders identify the objectives an adversary is trying to accomplish. MITRE ATT&CK is arguably at the forefront of reporting and classifying adversary tactics, techniques, and procedures (TTPs) and offers a publicly accessible knowledge base as publicly available threat intelligence and incident reporting as its primary data source.

The OPSEC process has five steps:
## 1. Identify Critical Information
What a red teamer considers critical information worth protecting depends on the operation and the assets or tooling used. In this setting, critical information includes, but is not limited to, the red team’s intentions, capabilities, activities, and limitations. Critical information includes any information that, once obtained by the Blue team, would hinder or degrade the red team’s mission.

To identify critical information, the red team needs to use an adversarial approach and ask themselves what information an adversary, the Blue team, in this case, would want to know about the mission. If obtained, the adversary will be in a solid position to thwart the red team’s attacks. Therefore, critical information is not necessarily sensitive information; however, it is any information that might jeopardise your plans if leaked to an adversary. The following are some examples:

- Client information that your team has learned. It's unacceptable to share client specific information such as employee names, roles, and infrastructure that your team has discovered. Sharing this type of information should kept on need-to-know basis as it could compromise the integrity of the operation. The Principle of Least Privilege (PoLP) dictates that any entity (user or process) must be able to access only the information necessary to carry out its task. PoLP should be applied in every step taken by the Red Team.
- Red team information, such as identities, activities, plans, capabilities and limitations. The adversary can use such information to be better prepared to face your attacks.
- Tactics, Techniques, and Procedures (TTP) that your team uses in order to emulate an attack.
- OS, cloud hosting provider, or C2 framework utilised by your team. Let’s say that your team uses Pentoo (opens in new tab) for penetration testing, and the defender knows this. Consequently, they can keep an eye for logs exposing the OS as Pentoo. Depending on the target, there is a possibility that other attackers are also using Pentoo to launch their attacks; however, there is no reason to expose your OS if you don’t have to.
- Public IP addresses that your red team will use. If the Blue team gains access to this kind of information, they could quickly mitigate the attack by blocking all inbound and outbound traffic to your IP addresses, leaving you to figure out what has happened.
- Domain names that your team has registered. Domain names play a significant role in attacks such as Phishing. Likewise, if the Blue team figures out the domain names you will be using to launch your attacks, they could simply block or sinkhole your malicious domains to neutralize your attack.
- Hosted websites, such as Phishing websites, for adversary emulation.

---
## 2. Analyse threats
After we identify critical information, we need to analyse threats. Threat analysis refers to identifying potential adversaries and their intentions and capabilities. Adapted from the US Department of Defense (DoD) Operations Security () Program Manual (opens in new tab), threat analysis aims to answer the following questions:

1. Who is the adversary?
2. What are the adversary’s goals?
3. What tactics, techniques, and procedures does the adversary use?
4. What critical information has the adversary obtained, if any?

The task of the red team is to emulate an actual attack so that the Blue team discovers its shortcomings, if any, and becomes better prepared to face incoming threats. The Blue team’s main objective is to ensure the security of the organization’s network and systems. The intentions of the Blue team are clear; they want to keep the red team out of their network. Consequently, considering the task of the red team, the Blue team is considered our adversary as each team has conflicting objectives. We should note that the Blue team’s capabilities might not always be known at the beginning.

Malicious third-party players might have different intentions and capabilities and might pause a threat as a result. This party can be someone with humble capabilities scanning the systems randomly looking for low-hanging fruit, such as an unpatched exploitable server, or it can be a capable adversary targeting your company or your client systems. Consequently, the intentions and the capabilities of this third party can make them an adversary as well.

| Adversary | Intentions | Capabilities | 
| ---- | ---- | ---- |
| Blue team | Keep intruders out | Not always known |
| Malicious third-party | Varies | Varies| 

We consider any adversary with the intent and capability to take actions that would prevent us from completing our operation as a threat:
$$ {threat} = {adversary} + {intent} + {capabilities} $$
In other words, an adversary without the intent or capability does not pose a threat for our purposes.

---
## 3. Analyse vulnerabilities
After identifying critical information and analysing threats, we can start with the third step: analysing vulnerabilities. This is not to be confused with vulnerabilities related to cybersecurity. An OPSEC vulnerability exists when an adversary can obtain critical information, analyse the findings, and act in a way that would affect your plans.

To better understand an OPSEC vulnerability as related to red teaming, we'll consider the following scenario. You use Nmap to discover live hosts on a target subnet and find open ports on live hosts. Moreover, you send various phishing emails leading the victim to a phishing webpage you're hosting. Furthermore, you're using the Metasploit framework to attempt to exploit certain software vulnerabilities. These are three separate activities; however, if you use the same IP address(es) to carry out these different activities, this would lead to an OPSEC vulnerability. Once any hostile/malicious activity is detected, the Blue team is expected to take action, such as blocking the source IP address(es) temporarily or permanently. Consequently, it would take one source IP address to be blocked for all the other activities use this IP address to fail. In other words, this would block access to the destination IP address used for the phising server, and the source IP address using Nmap by and Metasploit Framework.

Another example of an OPSEC vulnerability would be an unsecured database that's used to store data received from phishing victims. If the database is not properly secured, it may lead to a malicious third party compromising the operation and could result in data being exfiltrated and used in an attack against your client's network. As a result, instead of helping your client secure their network, you would end up helping expose login names and passwords.

Lax OPSEC could also result in less sophisticated vulnerabilities. For instance, consider a case where one of your red team members posts on social media revealing your client's name. If the Blue team monitors such information, it will trigger them to learn more about your team and your approaches to better prepare against expected penetration attempts.

---
## 4. Assess risks
We finished analysing the vulnerabilities, and now we can proceed to the fourth step: conducting a risk assessment. NIST defines a risk assessment as "The process of identifying risks to organizational operations (including mission, functions, image, reputation), organizational assets, individuals, other organizations, and the Nation, resulting from the operation of an information system." In OPSEC, risk assessment requires learning the possibility of an event taking place along with the expected cost of that event. Consequently, this involves assessing the adversary’s ability to exploit the vulnerabilities.

Once the level of risk is determined, countermeasures can be considered to mitigate that risk. We need to consider the following three factors:

1. The efficiency of the countermeasure in reducing the risk
2. The cost of the countermeasure compared to the impact of the vulnerability being exploited.
3. The possibility that the countermeasure can reveal information to the adversary

Let’s revisit the two examples from the previous task. In the first example, we considered the vulnerability of scanning the network with Nmap, using the Metasploit framework, and hosting the Phishing pages using the same public IP address. We analysed that this is a vulnerability as it makes it easier for the adversary to block our three activities by simply detecting one activity. Now let’s assess this risk. To evaluate the risk related to this vulnerability, we need to learn the possibility of one or more of these activities being detected. We cannot answer this without obtaining some information about the adversary’s capabilities. Let’s consider the case where the client has a Security Information and Event Management (SIEM) in place. A SIEM is a system that allows real-time monitoring and analysis of events related to security from different sources across the network. We can expect that a SIEM would make it reasonably uncomplicated to detect suspicious activity and connect the three events. As a result, we would assess the related risk as high. On the other hand, if we know that the adversary has minimal resources for detecting security events, we can assess the risk related to this vulnerability as low.

Let’s consider the second example of an unsecured database used to store data received from a Phishing page. Based on data collected from several research groups using honeypots, we can expect various malicious bots to actively target random IP addresses on the Internet. Therefore, it is only a matter of time before a system with weak security is discovered and exploited.


---
## 5. Apply appropriate countermeasures
The final step is applying countermeasures. The US Department of Defense (DoD) Operations Security (DoD) Operations security(OPSEC) Program Manual states, “Countermeasures are designed to prevent an adversary from detecting critical information, provide an alternative interpretation of critical information or indicators (deception), or deny the adversary’s collection system.”

Let’s revisit the two examples we presented in the Vulnerability Analysis task. In the first example, we considered the vulnerability of running Nmap, using the Metasploit framework, and hosting the Phishing pages using the same public IP address. The countermeasure for this one seems obvious; use a different IP address for each activity. This way, you can ensure that if one activity was detected the public IP address is blocked, the other activities can continue unaffected.

In the second example, we considered the vulnerability of an unsecured database used to store data received from a Phishing page. From a risk assessment perspective, we considered it as high risk due to malicious third parties potentially looking for random easy targets. The countermeasure, in this case, would be to ensure that the database is adequately secured so that the data cannot be accessed except by authorized personnel.


---
If the adversary discovers that you are scanning their network with nmap(the Blue team in our case), they should easily be able to discover the IP address used. For instance, if you use this same IP address to host a phishing site, it won’t be very difficult for the Blue team to connect the two events and attribute them to the same actor.

OPSEC is not a solution or a set of rules; OPSEC is a five-step process to deny adversaries from gaining access to any critical information.

---
