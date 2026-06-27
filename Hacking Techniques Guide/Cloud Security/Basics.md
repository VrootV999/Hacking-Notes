# Cloud Security Basics

## 1. Introduction to Cloud Computing

### 1.1 Definition of Cloud Computing (NIST SP 800-145)
Cloud computing is a model for enabling ubiquitous, convenient, on-demand network access to a shared pool of configurable computing resources (networks, servers, storage, applications, and services) that can be rapidly provisioned and released with minimal management effort or service provider interaction.

### 1.2 Essential Characteristics
- **On-demand self-service**: Users can provision computing capabilities automatically without requiring human interaction with the provider
- **Broad network access**: Capabilities are available over the network and accessed through standard mechanisms (mobile phones, tablets, laptops, workstations)
- **Resource pooling**: Provider's computing resources are pooled to serve multiple consumers using a multi-tenant model, with physical/virtual resources dynamically assigned/reassigned according to consumer demand
- **Rapid elasticity**: Capabilities can be elastically provisioned and released, in some cases automatically, to scale rapidly outward/inward commensurate with demand
- **Measured service**: Cloud systems automatically control/optimize resource use by leveraging metering capabilities at some level of abstraction appropriate to the service type

### 1.3 Cloud Service Models

#### Infrastructure as a Service (IaaS)
Provides virtualized computing resources over the internet. The provider manages physical infrastructure, while the customer manages the OS, middleware, runtime, data, and applications.

**Examples:**
- AWS EC2 (Elastic Compute Cloud)
- Azure Virtual Machines
- Google Compute Engine (GCE)

**Responsibility Breakdown:**
| Layer | Provider | Customer |
|-------|----------|----------|
| Physical Data Center | Provider | - |
| Networking Hardware | Provider | - |
| Storage Hardware | Provider | - |
| Virtualization/Hypervisor | Provider | - |
| Guest OS | - | Customer |
| Middleware/Runtime | - | Customer |
| Applications | - | Customer |
| Data | - | Customer |
| Access Management | - | Customer |

#### Platform as a Service (PaaS)
Provides a platform allowing customers to develop, run, and manage applications without the complexity of building/maintaining the underlying infrastructure.

**Examples:**
- AWS Elastic Beanstalk
- Azure App Service
- Google App Engine
- Heroku

**Responsibility Breakdown:**
| Layer | Provider | Customer |
|-------|----------|----------|
| Physical Data Center | Provider | - |
| Networking Hardware | Provider | - |
| Storage Hardware | Provider | - |
| Virtualization/Hypervisor | Provider | - |
| Guest OS | Provider | - |
| Middleware/Runtime | Provider | - |
| Applications | - | Customer |
| Data | - | Customer |
| Access Management | Shared | Shared |

#### Software as a Service (SaaS)
Provides ready-made software applications over the internet on a subscription basis. The provider manages everything from infrastructure to the application itself.

**Examples:**
- Microsoft 365 (Office 365)
- Google Workspace (G Suite)
- Salesforce
- Dropbox

**Responsibility Breakdown:**
| Layer | Provider | Customer |
|-------|----------|----------|
| Physical Data Center | Provider | - |
| Networking Hardware | Provider | - |
| Storage Hardware | Provider | - |
| Virtualization/Hypervisor | Provider | - |
| Guest OS | Provider | - |
| Middleware/Runtime | Provider | - |
| Applications | Provider | - |
| Data | - | Customer |
| Access Management | Shared | Shared |

#### Function as a Service (FaaS) / Serverless
Executes code in response to events without managing servers. The provider handles all infrastructure; the customer provides only code.

**Examples:**
- AWS Lambda
- Azure Functions
- Google Cloud Functions

### 1.4 Cloud Deployment Models

#### Public Cloud
Cloud infrastructure provisioned for open use by the general public. Owned/operated by a cloud provider.
- **Pros**: No capital expenditure, pay-as-you-go pricing, virtually unlimited scalability, no maintenance overhead
- **Cons**: Less control over security, multi-tenancy risks, potential data sovereignty issues, vendor lock-in
- **Examples**: AWS, Azure, GCP

#### Private Cloud
Cloud infrastructure provisioned for exclusive use by a single organization. Can be on-premises or hosted by a third-party.
- **Pros**: Full control over security/compliance, dedicated resources, higher customization, isolation from other tenants
- **Cons**: Higher costs, requires internal expertise, limited scalability compared to public cloud, capital expenditure required
- **Types**: On-premises private cloud, hosted private cloud, virtual private cloud

#### Hybrid Cloud
Combination of public and private clouds bound together by standardized/ proprietary technology enabling data/application portability.
- **Pros**: Flexibility to choose optimal environment per workload, ability to burst to public cloud during peak demand, keeps sensitive data on-premises, cost optimization
- **Cons**: Increased complexity, network latency between environments, requires robust integration, potential compliance challenges
- **Use Cases**: Cloud bursting, disaster recovery, data backup, dev/test in public cloud with production in private

#### Community Cloud
Cloud infrastructure provisioned for exclusive use by a specific community of consumers from organizations with shared concerns (security, compliance, jurisdiction).
- **Pros**: Shared costs across organizations, aligned compliance requirements, specialized for industry needs
- **Cons**: Limited provider options, governance complexity, may require consensus on decisions
- **Examples**: Government cloud (GovCloud), healthcare community cloud, financial services community cloud

#### Multi-Cloud
Using multiple cloud providers simultaneously to avoid vendor lock-in, optimize costs, or meet regulatory requirements.
- **Pros**: No single point of failure, best-of-breed services per workload, negotiating leverage
- **Cons**: Increased management complexity, security consistency challenges, data integration difficulties, higher operational costs

### 1.5 Cloud Computing Benefits
- **Cost Efficiency**: Eliminates capital expenditure on hardware; pay-as-you-go model converts CapEx to OpEx
- **Global Scale**: Ability to scale globally with data centers around the world
- **Speed and Agility**: Resources available in minutes vs. weeks/months for traditional IT
- **Reliability**: Data backup, disaster recovery, and business continuity built-in; providers offer 99.9%+ SLAs
- **Security**: Providers invest heavily in physical and logical security; many certifications (SOC, ISO, PCI-DSS)
- **Automatic Updates**: Providers handle patching and maintenance of infrastructure
- **Elasticity**: Resources automatically scale up/down based on demand, preventing over/under provisioning

---

## 2. The Shared Responsibility Model

### 2.1 Core Concept
The shared responsibility model is a security and compliance framework that divides accountability between the cloud service provider (CSP) and the customer. The division maps precisely to what each party controls. **The customer is ALWAYS responsible for:**
- Data
- Endpoints (devices accessing the cloud)
- Accounts and identities
- Access management
- Configuration of cloud services

### 2.2 Responsibility Breakdown by Service Model

```
On-Premises:  Customer: [Data][Apps][Runtime][OS][Virtualization][Servers][Storage][Networking]
IaaS:         Customer: [Data][Apps][Runtime][OS] | Provider: [Virtualization][Servers][Storage][Networking]
PaaS:         Customer: [Data][Apps] | Provider: [Runtime][OS][Virtualization][Servers][Storage][Networking]
SaaS:         Customer: [Data][Access] | Provider: [Apps][Runtime][OS][Virtualization][Servers][Storage][Networking]
```

### 2.3 Customer Responsibilities (ALWAYS)
| Area | Details |
|------|---------|
| Data | Data classification, encryption decisions, data governance, compliance with regulations |
| Endpoints | Client devices, mobile devices, laptops, desktops, IoT devices accessing cloud services |
| Accounts | Creating, managing, removing user accounts; identity lifecycle management |
| Access Management | RBAC, MFA, conditional access policies, least privilege enforcement |
| Configuration | Properly configuring cloud services, security groups, bucket policies, encryption settings |

### 2.4 Provider Responsibilities (ALWAYS)
| Area | Details |
|------|---------|
| Physical Security | Data centers, access controls, surveillance, guards |
| Hardware | Servers, storage devices, networking equipment |
| Virtualization | Hypervisor security, isolation between tenants |
| Global Infrastructure | Regions, availability zones, edge locations |
| Base Service Availability | Service uptime, DDoS protection on provider infrastructure |

### 2.5 Common Misconfigurations Leading to Breaches (Cloud Security Alliance Data)
1. **Publicly exposed storage buckets** (S3 buckets, Azure Blob, GCS buckets)
2. **Overly permissive IAM policies** (wildcard `*` actions/resources)
3. **Unrestricted inbound/outbound network rules** (0.0.0.0/0)
4. **Default credentials unchanged**
5. **No encryption enabled** (data at rest or in transit)
6. **Excessive permissions** (administrator access granted unnecessarily)
7. **Unused resources left running** (attack surface expansion)
8. **No logging/monitoring enabled**
9. **Misconfigured security groups** (open SSH/RDP to internet)
10. **Hardcoded secrets/keys in code** or exposed in public repositories

---

## 3. The CIA Triad in Cloud Security

### 3.1 Overview
The CIA triad is the foundational information security model: **Confidentiality**, **Integrity**, **Availability**.

| Pillar | Definition | Cloud-Specific Risks | Mitigations |
|--------|-----------|---------------------|-------------|
| **Confidentiality** | Ensuring data is accessible only to authorized entities | Publicly exposed storage, leaked secrets, compromised credentials, insufficient encryption | Encryption (AES-256/TLS), IAM least privilege, MFA, secrets management, private networking |
| **Integrity** | Ensuring data has not been tampered with or altered | Unauthorized edits, accidental deletes, rogue scripts, data corruption | Versioning, immutable backups, checksums/hashing, read-only roles, audit logging |
| **Availability** | Ensuring systems/data are accessible when needed | DDoS attacks, resource exhaustion, misconfigured autoscaling, provider outages, natural disasters | Multi-AZ/region deployment, autoscaling, load balancing, health checks, backup/DR plans, SLA monitoring |

### 3.2 Confidentiality Deep Dive

**Encryption Types:**
- **Encryption at Rest**: Protecting stored data (AES-256, SSE-S3, EBS encryption, RDS encryption)
- **Encryption in Transit**: Protecting data during transmission (TLS 1.2/1.3, HTTPS, VPN, IPsec)
- **Encryption in Use**: Protecting data during processing (confidential computing, Intel SGX, AMD SEV-SNP, homomorphic encryption)

**Data Classification Levels:**
1. **Public**: No sensitivity, can be freely shared
2. **Internal**: For internal use only, not sensitive
3. **Confidential**: Business-sensitive data with access restrictions
4. **Restricted**: Highly sensitive data (PII, PHI, financial records, trade secrets)
5. **Regulatory**: Data subject to legal/regulatory requirements (GDPR, HIPAA, PCI-DSS)

**Key Management:**
- **Customer-Managed Keys (CMK/CMEK)**: Customer creates and controls keys
- **Customer-Supplied Keys (CSEK)**: Customer provides their own keys
- **AWS KMS**: Managed key creation, rotation, and auditing; integrates with AWS services
- **Azure Key Vault**: Cloud HSM-backed key storage, secret management, certificate management
- **GCP Cloud KMS**: Centralized key management, global or regional keys, HSM support
- **Cloud HSM**: Dedicated hardware security module for FIPS 140-2 Level 3 compliance
- **BYOK (Bring Your Own Key)**: Customer generates key, provider imports it
- **HYOK (Hold Your Own Key)**: Customer retains exclusive key control outside provider

### 3.3 Integrity Deep Dive

**Integrity Controls:**
- **Checksums and Hashing**: SHA-256, SHA-3 for data verification
- **Digital Signatures**: Authenticate source and verify integrity
- **Versioning**: Object versioning in S3, Git-based infrastructure as code
- **Immutable Storage**: Write Once Read Many (WORM) storage, S3 Object Lock, Azure Immutable Blob
- **Database ACID Compliance**: Atomicity, Consistency, Isolation, Durability for transactional integrity
- **Blockchain / Ledger**: Amazon QLDB, Azure Confidential Ledger

**Audit Logging:**
- **AWS CloudTrail**: Records all API calls across AWS accounts; can be delivered to CloudWatch Logs or S3
- **Azure Activity Log**: Subscription-level and tenant-level audit logs
- **GCP Cloud Audit Logs**: Admin Activity, Data Access, System Events, Policy Denied audit logs
- **Database Audit Logs**: AWS RDS Enhanced Monitoring, Azure SQL Auditing, GCP Cloud SQL Audit

### 3.4 Availability Deep Dive

**Availability Concepts:**
- **Regions**: Geographic areas with multiple AZs (e.g., us-east-1, eu-west-2, ap-southeast-1)
- **Availability Zones (AZs)**: Isolated locations within a region with independent power/cooling/network
- **Edge Locations**: CDN endpoints for content caching and edge computing (AWS CloudFront, Azure CDN, GCP Cloud CDN)

**High Availability Architectures:**
- **Active-Passive**: One active instance, one standby; failover on failure
- **Active-Active**: All instances active; load balancer distributes traffic
- **Multi-AZ**: Resources deployed across multiple AZs for fault isolation
- **Multi-Region**: Resources deployed across regions for disaster recovery
- **Global Load Balancing**: Route53 (AWS), Traffic Manager (Azure), Cloud DNS (GCP)

**Disaster Recovery Strategies:**
| Strategy | RPO | RTO | Cost | Description |
|----------|-----|-----|------|-------------|
| Backup & Restore | Hours | Hours | Low | Periodically back up data; restore to new environment |
| Pilot Light | Minutes | Hours | Medium | Core services running; scale up on failover |
| Warm Standby | Seconds | Minutes | Medium-High | Reduced-size production environment; scales on failover |
| Multi-Site Active-Active | Near-zero | Near-zero | High | Fully redundant environment serving traffic |

**Recovery Metrics:**
- **RPO (Recovery Point Objective)**: Maximum acceptable data loss (measured in time)
- **RTO (Recovery Time Objective)**: Maximum acceptable downtime
- **MTPD (Maximum Tolerable Period of Disruption)**: Total time business can function without the system
- **WRT (Work Recovery Time)**: Time to validate/restore operations after recovery

---

## 4. Identity and Access Management (IAM)

### 4.1 Core Concepts
IAM is the framework for managing digital identities and controlling access to resources. **Identity is the new perimeter** in cloud security.

**IAM Components:**
- **Users**: Individual people or service accounts with credentials
- **Groups**: Collections of users with common permission needs
- **Roles**: Sets of permissions assumable by users/services/applications
- **Policies**: JSON documents defining permissions (allow/deny)
- **Permissions**: Statements specifying which actions are allowed/denied on which resources (optionally under conditions)

### 4.2 IAM Policy Structure (AWS Example)
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::example-bucket/*",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": "192.168.1.0/24"
        },
        "Bool": {
          "aws:MultiFactorAuthPresent": "true"
        }
      }
    }
  ]
}
```

**Policy Elements:**
- **Effect**: Allow or Deny (explicit deny always overrides allow)
- **Principal**: Who the policy applies to (user, role, service, account)
- **Action**: The operation being permitted/denied (e.g., `s3:GetObject`, `ec2:RunInstances`)
- **Resource**: The resource(s) the action applies to (ARN format)
- **Condition**: When the policy is in effect (IP range, time, MFA status, VPC endpoint, tags)

### 4.3 Principle of Least Privilege
Every user, service, and component should have only the minimum permissions necessary to perform its function.

**Implementation:**
1. Start with no permissions (default-deny)
2. Grant permissions incrementally based on specific job requirements
3. Regularly review and revoke unused permissions
4. Use managed policies where possible, custom policies for precise control
5. Implement Just-In-Time (JIT) access for elevated permissions
6. Use temporary credentials instead of long-lived access keys

### 4.4 Authentication Methods

**Single-Factor Authentication (SFA):**
- Password-based authentication only

**Multi-Factor Authentication (MFA):**
- **Something you know**: Password, PIN
- **Something you have**: Phone (SMS/authenticator app), hardware token (YubiKey, RSA SecurID), smart card
- **Something you are**: Biometrics (fingerprint, face, retina)
- **Somewhere you are**: Geolocation, IP range

**Passwordless Authentication:**
- FIDO2, WebAuthn
- Windows Hello, Apple Face ID/Touch ID
- Biometric authentication with device-bound keys

### 4.5 Federation and Single Sign-On (SSO)

**Federation Protocols:**
- **SAML 2.0 (Security Assertion Markup Language)**: XML-based, commonly used for enterprise SSO; exchanges authentication/authorization data between IdP and SP
- **OAuth 2.0**: Authorization framework; issues access tokens (JWT) for delegated access; widely used for API authorization
- **OpenID Connect (OIDC)**: Identity layer on top of OAuth 2.0; provides authentication with ID tokens (JWT); used by Google, Microsoft, AWS Cognito
- **SAML vs OIDC**: SAML is enterprise-focused (SSO for web apps); OIDC is modern (web, mobile, API, SPAs)

**Identity Providers (IdPs):**
- AWS IAM Identity Center (AWS SSO)
- Azure AD / Microsoft Entra ID
- Google Cloud Identity / Google Workspace
- Okta, Ping Identity, OneLogin, Keycloak (self-hosted)

**Identity Federation:**
- Allows users authenticated by an external IdP to access cloud resources
- AWS IAM roles with SAML/OIDC federation
- Azure AD External Identities / B2B collaboration
- Google Cloud Workforce Identity Federation

### 4.6 Service Accounts and Application Authentication
- **IAM Roles for Services**: EC2, Lambda, ECS, EKS assume roles to make API calls
- **Service Principals**: Azure AD identity for applications/services
- **Service Accounts**: GCP service accounts with key-based or workload identity federation authentication
- **Access Keys**: Long-lived AWS access keys (Access Key ID + Secret Access Key), used for programmatic access
- **Temporary Credentials**: AWS STS (Security Token Service), Azure Managed Identities, GCP Workload Identity
- **API Keys**: For service-to-service authentication; rotate regularly and avoid storing in code

### 4.7 Authorization Models

**RBAC (Role-Based Access Control):**
- Permissions assigned to roles; users assigned to roles; widely used across all cloud providers
- Roles map to job functions (e.g., Admin, ReadOnly, Developer, SecurityAudit)

**ABAC (Attribute-Based Access Control):**
- Permissions based on attributes (tags, user attributes, resource metadata)
- More granular and dynamic than RBAC
- Example: "Allow developers to manage resources tagged with their team name"

**PBAC (Policy-Based Access Control):**
- Centralized policy engine that evaluates access requests against policies
- AWS Organizations SCPs, Azure Policy, GCP Organization Policies

**Conditional Access:**
- Azure AD Conditional Access: Enforce MFA, device compliance, location-based policies
- AWS IAM Conditions: Source IP, MFA status, time, VPC endpoint, user agent

### 4.8 IAM Best Practices
1. **Enable MFA** on all accounts, especially privileged users and root accounts
2. **Use roles instead of long-lived keys** for applications and services
3. **Apply least privilege** - grant only required permissions
4. **Use policy conditions** to restrict access (IP, time, MFA, VPC)
5. **Regularly audit permissions** using IAM Access Analyzer, CloudTrail, and third-party tools
6. **Remove unused credentials** - delete unused users, keys, roles
7. **Implement Just-In-Time (JIT) access** for elevated permissions
8. **Use service control policies** (SCPs) in AWS Organizations to enforce guardrails
9. **Separate duties** - no single user should have both read and write access where separation is needed
10. **Use resource-based policies** for cross-account access instead of sharing credentials

**Cloud Provider IAM Differences:**

| Feature | AWS IAM | Azure AD / RBAC | GCP Cloud IAM |
|---------|---------|-----------------|---------------|
| Identity Source | AWS IAM users + external IdP | Azure AD | Cloud Identity / external IdP |
| Policy Type | JSON policy documents | RBAC roles (built-in + custom) | Predefined + custom roles |
| Organization | AWS Organizations + SCPs | Management Groups + Azure Policy | Organization + Organization Policies |
| Service Accounts | IAM Roles | Managed Identities | Service Accounts |
| Cross-Account | Role assumption (STS) | Azure Lighthouse | Cross-project IAM + Service Account impersonation |
| Condition Keys | aws:SourceIp, aws:MultiFactorAuthPresent, etc. | IP, location, device, risk | google:source_ip, etc. |

---

## 5. Network Security in the Cloud

### 5.1 Virtual Private Cloud (VPC)

A VPC is a logically isolated section of the cloud network where you can launch resources. It provides full control over the virtual networking environment.

**VPC Components:**
- **CIDR Block**: IP address range for the VPC (e.g., 10.0.0.0/16)
- **Subnets**: Segments of the VPC CIDR; can be public (with internet gateway) or private (without)
- **Route Tables**: Define where network traffic is directed
- **Internet Gateway (IGW)**: Allows communication between VPC and internet
- **NAT Gateway / NAT Instance**: Allows private subnet resources to initiate outbound internet traffic (but not receive inbound)
- **Virtual Private Gateway (VGW)**: Connects VPC to on-premises via VPN or Direct Connect
- **VPC Peering**: Connects two VPCs privately using IPv4/IPv6
- **Transit Gateway**: Hub-and-spoke connectivity model for hundreds/thousands of VPCs
- **VPC Endpoints**: Private connection to AWS services without traversing the internet (Gateway Endpoints for S3/DynamoDB, Interface Endpoints for other services)
- **Egress-Only Internet Gateway**: IPv6-only outbound internet access

**Subnet Types:**
- **Public Subnet**: Has route to Internet Gateway; resources can have public IPs
- **Private Subnet**: No direct route to internet; accessed through NAT Gateway or VPN
- **VPN-Only Subnet**: Accessible only through VPN connection from on-premises
- **Isolated Subnet**: Completely isolated with no external connectivity

### 5.2 Security Groups vs. Network ACLs

| Feature | Security Group | Network ACL |
|---------|--------------|-------------|
| **Scope** | Instance-level (stateful) | Subnet-level (stateless) |
| **State** | Stateful - return traffic automatically allowed | Stateless - return traffic must be explicitly allowed |
| **Rules** | Allow rules only (implicit deny all) | Allow and Deny rules (evaluated in order) |
| **Evaluation** | All rules evaluated together | Rules evaluated in number order |
| **Supports** | IPv4, IPv6 | IPv4, IPv6 |
| **Return Traffic** | Automatically allowed regardless of inbound rules | Must be explicitly allowed |
| **Use Case** | Instance-level micro-segmentation | Subnet-level broad filtering, additional layer of defense |

### 5.3 Network Segmentation Strategies
- **Multi-tier Architecture**: Web tier, application tier, database tier in separate subnets
- **Public vs Private**: Public-facing resources in public subnets; backed services in private subnets
- **Environment Isolation**: Dev, test, staging, production in separate VPCs or accounts
- **Micro-segmentation**: Per-service or per-instance security group with minimal allowed traffic
- **Tier Access Control**: Web tier can access app tier, app tier can access database tier; no direct web-to-database access

### 5.4 Cloud Firewall and WAF

**Web Application Firewall (WAF):**
- AWS WAF, Azure WAF, GCP Cloud Armor
- Protects web applications from common exploits (SQL injection, XSS, CSRF)
- Supports custom rules, rate limiting, IP blacklisting/whitelisting, geo-blocking
- Integrates with CloudFront, ALB, API Gateway, App Gateway

**Cloud Firewall Options:**
- **AWS Network Firewall**: Managed firewall for VPC-level filtering, intrusion prevention
- **Azure Firewall**: Managed, cloud-based network security service; fully stateful
- **GCP Cloud Firewall**: Distributed firewall service embedded in VPC (no device to manage)
- **Third-Party**: Palo Alto Panorama, Check Point, Fortinet, Cisco FTD in cloud marketplace

### 5.5 DDoS Protection
- **AWS Shield**: Standard (free, protects against L3/L4 attacks) and Advanced ($3k/month, includes DDoS Response Team, cost protection, L7 mitigation)
- **Azure DDoS Protection**: Basic (free, always-on) and Standard (tuned to Azure resources, mitigation reports)
- **GCP Cloud Armor**: Google's WAF + DDoS protection at the edge

**DDoS Mitigation Best Practices:**
1. Use CDN/edge services (CloudFront, Azure CDN, Cloud CDN) to absorb traffic
2. Configure rate limiting on WAF
3. Use auto-scaling to handle traffic spikes
4. Set CloudWatch/Alert thresholds for traffic anomalies
5. Implement AWS Shield Advanced for critical workloads
6. Use Amazon Route 53 DNS-based failover to route away from attack targets
7. Employ S3 Origin Failover with CloudFront for static content

### 5.6 Zero Trust Network Architecture

**Core Principles:**
1. **Never trust, always verify**: No implicit trust based on network location
2. **Assume breach**: Design as if the network is already compromised
3. **Verify explicitly**: Always authenticate and authorize based on all available data points
4. **Least privilege access**: Grant minimum access required
5. **Micro-segmentation**: Isolate resources at granular level
6. **Continuous monitoring**: Log and analyze all traffic for anomalies

**Zero Trust Components:**
- **ZTNA (Zero Trust Network Access)**: BeyondCorp (Google), AWS Verified Access, Azure AD App Proxy, Zscaler, Cloudflare Access
- **SASE (Secure Access Service Edge)**: Combines SD-WAN with security functions (CASB, SWG, ZTNA, FWaaS)
- **CASB (Cloud Access Security Broker)**: Mediates user access to cloud services; provides visibility, compliance, data security, threat protection

### 5.7 SDN (Software-Defined Networking) in Cloud
- **SDN**: Separates control plane from data plane; enables programmable, centralized network management
- **Benefits**: Automated provisioning, dynamic traffic routing, centralized policy management, network virtualization
- **Examples**: AWS VPC (Java-based SDN), Azure Virtual Network, GCP Andromeda (SDN stack), VMware NSX

### 5.8 Network Security Best Practices
1. **Default-deny inbound, restrict outbound**: Minimize attack surface
2. **Use security groups as instance-level firewall**: Layer defense with NACLs at subnet level
3. **Enable VPC Flow Logs**: Capture network traffic metadata for analysis
4. **Deploy WAF for web-facing applications**: Protect against OWASP Top 10 attacks
5. **Use private endpoints for AWS/Azure/GCP services**: Keep traffic off the internet
6. **Implement network segmentation via subnets and security groups**: Separate tiers of application
7. **Use VPN or Direct Connect for hybrid connectivity**: Encrypt data in transit between on-prem and cloud
8. **Enable DDoS protection**: Use provider-native DDoS protection services
9. **Use Transit Gateway for multi-VPC/multi-region connectivity**: Centralized hub for routing
10. **Regularly audit security group rules**: Remove unused rules, detect overly permissive rules

---

## 6. Data Security in the Cloud

### 6.1 Cloud Data Lifecycle

The cloud data lifecycle describes the stages data passes through from creation to destruction.

```
Create → Store → Use → Share → Archive → Destroy
```

| Phase | Description | Security Controls |
|-------|-------------|------------------|
| **Create** | Data is generated, ingested, or uploaded | Classification labeling, encryption at birth (client-side or server-side), access controls |
| **Store** | Data is persisted in storage | Encryption at rest, access policies, versioning, backup |
| **Use** | Data is processed, read, transformed | Audit logging, IAM, in-transit encryption, confidential computing |
| **Share** | Data is transferred between systems/users | Encryption in transit, access controls, data loss prevention (DLP), CASB |
| **Archive** | Data is moved to long-term storage | Encryption, retention policies, immutability, offsite backup |
| **Destroy** | Data is permanently deleted | Secure deletion (NIST 800-88), cryptographic erasure, decommissioning verification |

### 6.2 Data Classification
Data must be classified to determine appropriate security controls.

**Classification Frameworks:**

| Level | Example | Controls Required |
|-------|---------|------------------|
| **Public** | Marketing materials, press releases | Basic access control |
| **Internal** | Internal memos, policies, employee directories | Access restricted to employees |
| **Confidential** | Customer data, financial reports, source code | Encryption, strict access control, audit logging |
| **Restricted** | PII, PHI, trade secrets, board materials | Encryption, MFA, strict audit trail, retention limits, DLP |
| **Regulatory** | Data subject to GDPR, HIPAA, PCI-DSS, SOX | All above + specific compliance controls, breach notification, right to audit |

**Data Discovery Tools:**
- AWS Macie: Automated discovery/classification of sensitive data in S3 (uses machine learning)
- Azure Purview / Microsoft Purview: Unified data governance, classification across on-prem and cloud
- GCP Sensitive Data Protection (DLP API): Inspect, classify, and de-identify sensitive data
- Third-party: BigID, Varonis, Spirion, Titus

### 6.3 Data Security Technologies

#### Encryption at Rest
| Cloud Provider | Service | Key Management |
|---------------|---------|----------------|
| AWS | SSE-S3 (S3 Managed Keys), SSE-KMS (KMS Keys), SSE-C (Customer Provided Keys) | AWS KMS, CloudHSM |
| Azure | SSE (Storage Service Encryption), Azure Disk Encryption, TDE (Transparent Data Encryption) | Azure Key Vault, Managed HSM |
| GCP | Server-side encryption (default), CMEK (Customer Managed Encryption Keys), CSEK (Customer Supplied Encryption Keys) | Cloud KMS, Cloud HSM |

#### Encryption in Transit
- **TLS 1.2/1.3**: Standard for HTTPS, API calls, database connections
- **IPsec VPN**: Site-to-site VPN between on-prem and cloud VPC
- **AWS PrivateLink / Azure Private Link / GCP Private Service Connect**: Private connectivity without internet traversal
- **MACsec**: Encryption at Layer 2 for Direct Connect/Azure ExpressRoute/GCP Dedicated Interconnect
- **SSH**: Secure shell for instance administration
- **mTLS**: Mutual TLS for service-to-service authentication

#### Client-Side Encryption
Data encrypted before being sent to the cloud. The provider never has access to the encryption keys.
- **AWS Encryption SDK / S3 Encryption Client**
- **Azure Client-Side Encryption with Key Vault**
- **GCP Tink / Cloud KMS encrypt before upload**
- **Third-party**: VeraCrypt, Cryptomator, Boxcryptor

#### Data Masking and Tokenization
- **Tokenization**: Replaces sensitive data with non-sensitive placeholder (token). Original data stored in secure vault. Used for PCI-DSS compliance.
- **Data Masking**: Obscures specific data elements (e.g., show only last 4 digits of SSN). Dynamic masking applies at query time.
- **Format-Preserving Encryption (FPE)**: Encrypts data while preserving original format (e.g., credit card number length/format remains valid).

### 6.4 Data Loss Prevention (DLP)
- **AWS Macie**: ML-powered; alerts on S3 objects containing sensitive data being publicly shared, accessed from unusual locations, or modified
- **Azure Information Protection / Microsoft Purview DLP**: Labeling, classification, policies to prevent sharing of sensitive data; integrates with Microsoft 365
- **GCP DLP**: Scan for, classify, and redact/de-identify sensitive data in text, images, and structured data
- **CASB DLP**: Cloud Access Security Brokers (Netskope, Zscaler, McAfee MVISION) enforce DLP across SaaS applications

### 6.5 Data Rights Management (DRM) / Information Rights Management (IRM)
- **AWS Nitro Enclaves**: Isolated, hardened enclaves for processing sensitive data; no persistent storage, no admin access
- **Azure Confidential Computing**: Executes code in TEE (Trusted Execution Environment) using Intel SGX/AMD SEV-SNP
- **GCP Confidential VMs**: Confidential computing for Compute Engine VMs
- **Microsoft Azure Information Protection**: Persistent protection (encryption, access restrictions) on documents/emails regardless of location
- **Vera, Seclore, NextLabs**: Third-party IRM solutions for document-level access control

### 6.6 Data Retention and Destruction

**Retention Policies:**
- Define how long different data types must be retained (regulatory, legal, operational requirements)
- **S3 Lifecycle Policies**: Transition to colder storage classes (S3 Standard-IA, S3 Glacier, S3 Glacier Deep Archive) and expire/deletion after defined periods
- **Azure Blob Lifecycle Management**: Tier to Cool, Archive; delete after period
- **GCP Object Lifecycle Management**: Set conditions for deletion or storage class transition

**Data Destruction Methods:**
| Method | Description | Standard |
|--------|-------------|----------|
| **Overwriting** | Write patterns over storage media | DoD 5220.22-M, NIST 800-88 Purge |
| **Degaussing** | Demagnetize magnetic media | NIST 800-88 Clear |
| **Physical Destruction** | Shredding, crushing, incineration | NIST 800-88 Destroy |
| **Cryptographic Erasure** | Destroy encryption keys making data unrecoverable | Fastest method, appropriate for encrypted data |

**Cloud Provider Data Decommissioning:**
- AWS: NIST 800-88 compliant media sanitization; no customer data on decommissioned storage devices
- Azure: NIST SP 800-88 and ISO/IEC 27001 certified data destruction
- GCP: Encryption key destruction renders data unrecoverable; physical media destroyed per NIST 800-88

### 6.7 Backup and Disaster Recovery

**Backup Types:**
- **Full Backup**: Complete copy of all data; longest time, most storage
- **Incremental Backup**: Only changes since last backup; faster, less storage
- **Differential Backup**: Changes since last full backup; balanced approach

**Cloud Backup Services:**
- **AWS Backup**: Centralized backup across AWS services; automated policy-based backups
- **Azure Backup**: Cloud-native backup for VMs, SQL, SAP, files; long-term retention
- **GCP Backup and DR**: Centralized backup/disaster recovery service
- **S3 Versioning**: Protects against accidental deletion/overwrite; allows recovery to previous version
- **S3 Object Lock**: WORM storage; prevents object deletion/overwrite for compliance

**3-2-1 Backup Rule:**
- **3** copies of data
- **2** different storage media
- **1** copy offsite (different region)

**Immutable Backups:**
- Backups that cannot be modified, encrypted, or deleted by anyone (including admins and ransomware)
- **S3 Object Lock (Governance/Compliance mode)**
- **Azure Blob Immutable Storage (Time-based/Legal hold policies)**
- **GCP Bucket Retention Policy (Bucket Lock)**

---

## 7. Cloud Infrastructure and Platform Security

### 7.1 Physical Security (Provider Responsibility)
- **Multi-layered Security**: Perimeter fencing, security guards, CCTV, biometric access, mantraps, two-factor access
- **Data Center Design**: N+1 or 2N redundancy for power, cooling, network; disaster-resistant locations
- **Access Control**: Least privilege physical access, visitor logs, escort requirements, badge access with audit trail
- **Environmental Controls**: Fire suppression (clean agent like FM-200/Novec 1230), temperature/humidity monitoring, leak detection
- **Compliance Certifications**: SOC 1/2/3 Type II, ISO 27001, PCI-DSS Level 1, FedRAMP, HIPAA BAAs

### 7.2 Compute Security

**Virtual Machine Security:**
- **OS Hardening**: Remove unnecessary services, disable unused ports, apply CIS benchmarks
- **Patch Management**: Regular patching cadence (OS and applications); automated patching with minimal downtime
- **Instance Metadata**: Prevent IMDS (Instance Metadata Service) attacks; use IMDSv2 with hop limit; restrict access with network controls
- **Golden Images**: CIS-hardened AMIs (Amazon Machine Images); automated image builder (AWS Image Builder, Packer)
- **Instance Isolation**: Hypervisor isolation enforced by provider; no cross-instance access

**Container Security:**
- **Image Scanning**: Scan for vulnerabilities (Trivy, Clair, Snyk, Amazon ECR scanning, Azure Container Registry scanning, GCP Artifact Analysis)
- **Container Runtime Security**: Falco, Aqua, Twistlock, Sysdig; detect anomalous behavior at runtime
- **Image Signing**: Docker Content Trust, Notary, Sigstore/Cosign; verify image provenance
- **Kubernetes Security**: RBAC, NetworkPolicies, PodSecurityPolicies (now Pod Security Standards/OPA Gatekeeper), secrets management, namespace isolation
- **CIS Benchmarks**: Docker CIS Benchmark, Kubernetes CIS Benchmark

**Serverless Security:**
- **Event Injection**: Validate all inputs to Lambda/Cloud Functions
- **IAM for Functions**: Least-privilege execution role per function; no wildcard permissions
- **Secret Management**: Use AWS Secrets Manager / Azure Key Vault / GCP Secret Manager to inject secrets; never hardcode
- **Dependency Management**: Scan Lambda layers, function dependencies for known vulnerabilities
- **Function Monitoring**: CloudWatch Logs / Azure Monitor / Cloud Logging; trace function invocations
- **VPC Configuration**: Lambda in VPC for access to private resources; configure VPC security groups

### 7.3 Storage Security

**Object Storage (S3, Azure Blob, GCS):**
- **Block Public Access at Account/Bucket Level**: Prevent any public exposure
- **Bucket Policies**: Control access at bucket level with condition keys (SourceIP, MFA, VPC Source)
- **Encryption**: Enable encryption by default (SSE-S3, SSE-KMS, customer-provided)
- **Versioning**: Protect against accidental overwrites and deletions
- **Access Logging**: S3 server access logs, CloudTrail data events for S3
- **Object Lock**: WORM compliance; prevent deletion/modification
- **Transfer Acceleration**: For fast uploads over long distances; use with HTTPS

**Block Storage (EBS, Azure Disk, GCP Persistent Disk):**
- **Encryption at Rest**: Enable encryption by default; use KMS customer-managed keys for control
- **Snapshots**: Encrypted snapshots; share only with authorized accounts
- **Volume Isolation**: Separate volumes per instance; properly detach/terminate unused volumes
- **Performance Monitoring**: IOPS, throughput, latency; set CloudWatch alarms for anomalies

**Database Security:**
- **Encryption at Rest**: RDS/KMS, Azure SQL TDE/Always Encrypted, Cloud SQL CMEK
- **Encryption in Transit**: TLS connections enforced; SSL/TLS certificates
- **Network Isolation**: Database in private subnet; security group restricting to application tier only
- **Authentication**: IAM database authentication (AWS), Azure AD authentication, Cloud SQL IAM authentication
- **Audit Logging**: RDS Enhanced Monitoring, Azure SQL Auditing, Cloud SQL Audit Logs
- **Backup Encryption**: Ensure backups are encrypted
- **Automated Patching**: Enable automatic minor version upgrades
- **Parameter Groups**: Secure database configuration (SSL enforcement, log_connections, log_disconnections)

### 7.4 Virtualization Security

**Hypervisor Security:**
- **Type 1 Hypervisor**: Bare-metal hypervisors (Xen, KVM, Hyper-V, VMware ESXi) run directly on hardware; no host OS attack surface
- **Provider Responsibilities**: Hypervisor patching, vulnerability management, tenant isolation
- **Side-Channel Attacks**: Mitigations for Spectre/Meltdown/L1TF/MDS; CPU microcode updates; guest-host memory isolation
- **Instance Isolation**: No instance can read another instance's memory/disk; hypervisor prevents cross-VM attacks
- **Dedicated Instances/Hosts**: Physical isolation for compliance requirements; full control over instance placement

**Container vs VM Security Isolation:**
| Aspect | VMs | Containers |
|--------|-----|------------|
| **Isolation Level** | Full (hypervisor-enforced) | Process-level (namespace/cgroup) |
| **Kernel** | Separate kernel per VM | Shared host kernel |
| **Attack Surface** | Smaller (hardware-backed) | Larger (shared kernel, syscall surface) |
| **Boot Time** | Minutes | Seconds |
| **Security Boundary** | Strong (hardware isolation) | Weaker (kernel isolation depends on configuration) |
| **Compromise Impact** | Isolated to one VM | Potential host/container escape |

### 7.5 Infrastructure as Code (IaC) Security

**IaC Tools:**
- **Terraform**: Cloud-agnostic, HCL language
- **AWS CloudFormation**: AWS-native, JSON/YAML
- **Azure ARM Templates / Bicep**: Azure-native declarative templates
- **Google Deployment Manager**: GCP-native
- **Pulumi**: Multi-cloud, general-purpose programming languages (TypeScript, Python, Go, C#)
- **Ansible**: Configuration management; push-based

**IaC Security Best Practices:**
1. **All infrastructure defined as code** - no manual provisioning
2. **Version control all IaC templates** in Git
3. **Scan IaC templates** before deployment for security issues (Checkov, tfsec, cfn-nag, terrascan, Snyk)
4. **Use policy as code** (Open Policy Agent, Sentinel, Azure Policy as Code, GCP Organization Policies)
5. **Principle of least privilege** for IaC execution roles
6. **State file security**: Encrypt terraform state files; use remote backends (S3 with DynamoDB locking, Azure Storage with blob lease)
7. **Secret management**: Never hardcode secrets in IaC; use secret stores or environment variables
8. **Immutable infrastructure**: Replace instances rather than modifying in place
9. **Drift detection**: Regularly compare deployed infrastructure with IaC templates; detect and remediate drift

---

## 8. Application Security in the Cloud

### 8.1 Secure Software Development Lifecycle (SSDLC)

**SDLC Phases with Security Activities:**

| Phase | Security Activities |
|-------|-------------------|
| **Requirements** | Threat modeling (STRIDE, PASTA), security requirements (OWASP ASVS), compliance requirements, privacy impact assessment |
| **Design** | Architecture review, trust boundary definition, security design patterns, attack surface analysis |
| **Development** | Secure coding standards (OWASP Top 10, CERT, CWE), peer review, SAST scanning, pre-commit hooks |
| **Testing** | DAST scanning, penetration testing, fuzz testing, dependency scanning, container scanning |
| **Deployment** | IaC scanning, secret scanning, compliance validation, immutable deployment, canary deployments |
| **Operations** | Runtime protection (RASP), WAF, monitoring, incident response, vulnerability management |

### 8.2 DevSecOps

DevSecOps integrates security into the DevOps pipeline. **Security is everyone's responsibility.**

**CI/CD Pipeline Security Gates:**
1. **Code Commit**: SAST scan, secret detection (git-secrets, truffleHog, GitLeaks), linting
2. **Build**: Dependency scan (OWASP Dependency-Check, Snyk, Dependabot), container image scan, software bill of materials (SBOM) generation
3. **Deploy to Dev**: DAST scan, IaC validation, configuration compliance check
4. **Deploy to Staging**: Penetration testing, fuzzing, compliance validation, load testing
5. **Deploy to Production**: WAF rules update, monitoring alerts configured, rollback plan validated

**Key DevSecOps Tools:**
| Category | Tools |
|----------|-------|
| **SAST** | SonarQube, Checkmarx, Fortify, Snyk Code, Semgrep |
| **DAST** | OWASP ZAP, Burp Suite, Acunetix, Qualys |
| **SCA (Dependency Scan)** | Snyk, OWASP Dependency-Check, Dependabot, Renovate, Trivy |
| **Container Scan** | Trivy, Clair, Snyk Container, Amazon ECR Scan, Docker Scout |
| **IaC Scan** | Checkov, tfsec, cfn-nag, Terrascan, KICS |
| **Secret Detection** | GitLeaks, TruffleHog, Git-secrets, GitHub Secret Scanning |
| **SBOM** | CycloneDX, SPDX, Syft |

### 8.3 OWASP Top 10 Cloud-Specific Risks

| # | Risk | Cloud Manifestation |
|---|------|-------------------|
| 1 | **Broken Access Control** | Overly permissive IAM policies, publicly exposed storage, missing authentication on serverless functions |
| 2 | **Cryptographic Failures** | No encryption at rest/in transit, weak keys, self-signed certificates, improper key management |
| 3 | **Injection** | SQL/NoSQL injection into cloud databases, command injection in Lambda/Cloud Functions, LDAP injection |
| 4 | **Insecure Design** | Lack of threat modeling, trust boundaries not defined, missing rate limiting on APIs, no defense in depth |
| 5 | **Security Misconfiguration** | Default credentials unchanged, unnecessary ports open, debug endpoints enabled, verbose error messages, CORS misconfigured |
| 6 | **Vulnerable and Outdated Components** | Unpatched OS in EC2/VM, open-source library vulnerabilities, outdated container images, deprecated SDK versions |
| 7 | **Identification and Authentication Failures** | No MFA, weak password policy, session fixation, JWT not validated, credential stuffing, no account lockout |
| 8 | **Software and Data Integrity Failures** | Unsigned container images, unsigned code, third-party package tampering (supply chain), pipeline injection |
| 9 | **Security Logging and Monitoring Failures** | CloudTrail not enabled, no log aggregation, no alerts on suspicious activity, insufficient retention, logs not monitored |
| 10 | **Server-Side Request Forgery (SSRF)** | Attacker tricks server to make requests to internal metadata endpoints (IMDSv1), internal services, cloud provider APIs |

### 8.4 API Security

**Cloud API Security Threats:**
- **Excessive Data Exposure**: APIs returning more data than needed (full objects instead of fields)
- **Mass Assignment**: Unvalidated parameters allowing modification of unintended object properties
- **Authorization Failures**: Broken function-level authorization (BFLA), broken object-level authorization (BOLA)
- **Rate Limiting Bypass**: Lack of throttling leading to resource exhaustion or brute force
- **API Key Leakage**: Keys in client-side code, public repos, logs, mobile apps

**API Security Controls:**
- **API Gateway**: AWS API Gateway, Azure API Management, GCP Apigee; authentication, throttling, validation, transformation
- **Authentication**: API keys, OAuth 2.0, JWT, mTLS
- **Input Validation**: Schema validation, parameter whitelisting, request size limits
- **Rate Limiting**: Per-user/IP throttling; burst limits, sustained limits
- **Logging and Monitoring**: API Gateway logs, CloudWatch/Stackdriver/Azure Monitor, anomaly detection
- **API Security Testing**: 42Crunch, Apisec, Noname Security, Salt Security; scan for API vulnerabilities

### 8.5 Identity Federation for Applications

**Web Application Authentication Patterns:**
- **Auth-as-a-Service**: AWS Cognito, Azure AD B2C, Auth0, Firebase Authentication
- **Social Login**: Google, Facebook, Apple, GitHub OAuth
- **Enterprise Federation**: SAML 2.0 with corporate IdP (Okta, Azure AD, OneLogin)
- **Token Exchange**: OAuth 2.0 token exchange, on-behalf-of flow

**Cloud-Native Secrets Management for Applications:**
- **AWS Secrets Manager**: Automatic rotation, fine-grained access, cross-Region replication
- **Azure Key Vault**: Secrets, keys, certificates; RBAC and access policies; soft-delete and purge protection
- **GCP Secret Manager**: Centralized secrets; versioning, replication, IAM-based access
- **HashiCorp Vault**: Dynamic secrets, leasing, revocation, encryption as a service

---

## 9. Cloud Security Operations

### 9.1 Logging and Monitoring

**Cloud Audit Logs:**

| Provider | Service | Captures |
|----------|---------|----------|
| AWS | **CloudTrail** | All API calls (management events: control plane; data events: S3, Lambda, DynamoDB); multi-region trails; organization trails |
| Azure | **Activity Log** | Subscription-level events (administrative, service health, autoscale, recommendation, security); Resource Logs per service |
| GCP | **Cloud Audit Logs** | Admin Activity (always enabled), Data Access (configurable), System Events, Policy Denied |

**Network Logs:**
- **VPC Flow Logs (AWS)**: Captures IP traffic metadata (src IP, dst IP, ports, protocol, packets, bytes, action) for VPC ENIs
- **NSG Flow Logs (Azure)**: Similar to VPC Flow Logs; capture ingress/egress IP traffic for NSGs
- **VPC Flow Logs (GCP)**: VPC flow logging for subnet-level network traffic metadata

**Infrastructure Logs:**
- **CloudWatch Logs (AWS)**: Collect, monitor, store logs from EC2, Lambda, ECS, and custom sources
- **Azure Monitor Logs**: Log Analytics workspaces, KQL query language for analysis
- **GCP Cloud Logging**: Collect, index, analyze logs; Log Explorer, Log-based metrics

**Application Logs:**
- **X-Ray (AWS)**: Distributed tracing for microservices; trace requests through services
- **Application Insights (Azure)**: Application performance monitoring, diagnostics, usage analytics
- **Cloud Trace (GCP)**: Distributed tracing latency data from Cloud Run, GKE, Compute Engine
- **OpenTelemetry**: Open-source, vendor-agnostic instrumentation for logs, metrics, and traces

### 9.2 Security Information and Event Management (SIEM)

**Cloud SIEM Solutions:**
- **Amazon Security Hub**: Aggregates findings from GuardDuty, Inspector, Macie, IAM Access Analyzer, Firewall Manager; CIS benchmarks
- **Azure Sentinel**: Cloud-native SIEM; intelligent security analytics; built-in connectors to Microsoft and third-party services; KQL queries
- **GCP Security Command Center**: Central security management; threat detection, vulnerability scanning, asset inventory
- **Splunk / ELK Stack / Sumo Logic / Datadog / QRadar**: Third-party SIEMs with cloud integration

**SIEM Best Practices:**
1. **Collect logs from ALL cloud services** (CloudTrail, VPC Flow Logs, WAF, DNS, CloudFront)
2. **Centralize log storage** in a dedicated security account (immutable S3 bucket with Object Lock)
3. **Establish baseline behavior** for normal activity; alert on deviations
4. **Create correlation rules** that connect seemingly unrelated events (e.g., IAM user creates access key + reads sensitive S3 data + exports data)
5. **Set retention periods** aligned with compliance requirements (1 year minimum, 3-7 years for regulated data)
6. **Test alert rules regularly** to ensure they work and reduce false positives
7. **Automate response** (SOAR) for known patterns

### 9.3 Threat Detection

**Native Cloud Threat Detection:**

| Provider | Service | Capabilities |
|----------|---------|-------------|
| AWS | **GuardDuty** | ML-powered threat detection; analyzes CloudTrail, VPC Flow Logs, DNS logs; detects crypto mining, port scanning, unusual API patterns, credential compromise, EC2 instance compromise |
| AWS | **Inspector** | Automated vulnerability management; scans EC2, ECR images, Lambda for CVEs; network reachability analysis |
| Azure | **Defender for Cloud** | CSPM (Cloud Security Posture Management), vulnerability scanning, threat protection for compute, storage, databases, containers; adaptive application controls |
| GCP | **Security Command Center** | Threat detection, vulnerability scanning (Web Security Scanner), asset discovery, event threat detection |
| GCP | **Event Threat Detection** | Detects malicious activity from Cloud Audit Logs (malware, token theft, DDoS, cryptomining, data exfiltration) |

**Third-Party Threat Detection:**
- **CrowdStrike Falcon**: Cloud workload protection, endpoint detection
- **Trend Micro Cloud One**: Workload security, container security, file storage security
- **Palo Alto Prisma Cloud**: CSPM, CWPP, CIEM, IaC scanning, container security
- **Wiz**: Agentless cloud security platform; vulnerability management, compliance, IaC scanning
- **Sysdig**: Container and Kubernetes security; runtime threat detection, image scanning
- **Lacework**: AI-driven anomaly detection; builds baseline of normal cloud behavior

### 9.4 Incident Response in the Cloud

**Cloud Incident Response Phases (NIST SP 800-61 + cloud adaptations):**

#### Preparation
- Pre-provisioned forensic analysis environment (forensic workstations, analysis tools)
- **Ami/VM/disk images** of baseline systems for comparison
- Inventory of cloud assets, criticality, ownership, network topology
- **Incident playbooks**: Specific runbooks for cloud scenarios (compromised IAM key, exposed S3 bucket, cryptomining, ransomware, DDoS)
- **Automation**: Lambda functions to automate containment actions (detach IAM policies, isolate instances via security groups, disable access keys)
- **Privileged Access**: Break-glass accounts with emergency access (MFA enforced, limited scope, audited)
- **Tooling**: Cloud-native (GuardDuty, Security Hub, AWS Config) and third-party (CrowdStrike, Splunk, Wiz)

#### Detection and Analysis
- **Alert sources**: SIEM, GuardDuty, Defender for Cloud, SCC, third-party CSPM/CWPP
- **Initial Scope**: Determine affected resources, IAM roles, accounts, regions, data, time window
- **CloudTrail Analysis**: Identify API calls made before/during incident; source IP, user agent, IAM user/role, time, action
- **VPC Flow Logs**: Trace network connections from/to compromised resources; C2 communication patterns, data exfiltration
- **S3 Access Logs**: Determine what data was read, accessed, or downloaded
- **CloudWatch Logs**: Application logs, OS logs for EC2 compromise
- **Memory/Volatile Data**: Capture EC2 instance memory (LiME, AVML), snapshot EBS volumes for forensics
- **Snapshot forensic evidence** (EBS snapshots, RDS snapshots) in isolated account

#### Containment, Eradication, Recovery
- **Short-term containment** (minutes):
  - Disable/rotate compromised access keys: `aws iam delete-access-key`
  - Detach IAM policies: `aws iam detach-user-policy`
  - Isolate compromised instance: Update security group to deny all traffic
  - Block IP address in WAF/NACL/Security Group
  - Disable compromised user login profile: `aws iam update-user --no-login-profile`
  - Revoke all session tokens: `aws sts revoke-sessions`
- **Medium-term containment** (hours):
  - Replace compromised EC2 instances with clean, patched versions
  - Enable enhanced monitoring
  - Review and revoke unnecessary IAM permissions
  - Reset all credentials (passwords, access keys, service account keys)
  - Review and remove unused IAM roles, users, policies
  - Enable block public access at account level
- **Eradication**:
  - Identify root cause (vulnerability, misconfiguration, stolen credential)
  - Remove backdoors, malware, unauthorized users/roles/resources
  - Patch vulnerabilities, fix misconfigurations
  - Remove unauthorized IAM resources (users, roles, policies, access keys)
  - Terminate unauthorized resources
- **Recovery**:
  - Restore from clean, verified backups
  - Verify backup integrity before restore
  - Test restored systems in isolated environment
  - Gradual production traffic re-routing
  - Verify all security controls are in place

#### Post-Incident Activity
- **Root cause analysis**: What failed? People, process, or technology?
- **Lessons learned**: Update runbooks, improve tools, fix gaps
- **Legal/compliance reporting**: Breach notification (if required by GDPR, CCPA, etc.)
- **Implement preventive controls**: Additional monitoring, automated response, strengthened policies
- **Board/executive reporting**: Incident summary, impact, remediation actions

### 9.5 Cloud Forensics Challenges

| Challenge | Description |
|-----------|-------------|
| **Multi-Tenancy** | Evidence may be co-mingled with other tenants; isolation/separation challenges |
| **Data Volatility** | Auto-scaling instances terminate automatically; ephemeral storage lost; container state non-persistent |
| **Log Preservation** | Logs may be overwritten in high-volume environments; ensure adequate retention and immutable storage |
| **Jurisdiction** | Data across regions/countries; different privacy laws, data access procedures |
| **Chain of Custody** | Cloud evidence is digital; must prove integrity (hashing), timestamp, access logging |
| **Provider Cooperation** | Provider response times vary; legal hold processes may take days; cloud provider may terminate compromised resources without notice |
| **Encryption** | Data at rest encrypted; need cooperation for key access; may be unable to access encrypted evidence |
| **Lack of Physical Access** | Cannot perform traditional forensic imaging (disk, memory, network tap); rely on provider APIs for evidence |
| **Speed of Investigation** | Cloud environments change rapidly; evidence may be ephemeral; automated response required |

**Forensic Evidence Collection:**
- **EBS Snapshots**: Volume-level forensic image; preserve in isolated forensic account
- **RDS Snapshots**: Database forensics; preserve in isolated account
- **CloudTrail Logs**: API call history; preserve to immutable bucket
- **VPC Flow Logs**: Network traffic metadata
- **Instance Memory**: Use tools like AVML (Azure VM Memory Linux), LiME, or commercial tools to capture RAM before termination
- **Container Forensics**: Export container logs, capture container image, analyze container filesystem

### 9.6 Patch and Configuration Management

**Patch Management:**
- **AWS Systems Manager Patch Manager**: Automated OS patching across EC2 fleet; maintenance windows; patch baselines
- **Azure Update Manager**: Patch compliance, scheduling, assess/update for Azure VMs and Arc-enabled servers
- **GCP OS Patch Management**: Patch deployments, patch compliance for Compute Engine instances
- **WSUS/YUM/APT**: Traditional in-instance patch management

**Configuration Management:**
- **AWS Config**: Continuously monitors and records AWS resource configurations; evaluates against desired configuration rules; detects configuration drift
- **Azure Policy**: Enforce organizational standards; evaluate compliance of Azure resources; prevent non-compliant resources
- **GCP Organization Policies**: Centralized constraints on GCP resources (e.g., restrict VM service accounts, allowed locations, public access prevention)

---

## 10. Compliance and Governance

### 10.1 Compliance Frameworks and Standards

| Standard | Focus | Cloud Relevance |
|----------|-------|----------------|
| **ISO 27001** | Information Security Management System (ISMS) | Foundation for cloud security management; certification available for providers |
| **ISO 27017** | Cloud-specific security controls | Extension of ISO 27002 for cloud; defines customer/provider responsibilities |
| **ISO 27018** | PII protection in public clouds | Privacy-specific controls for personal data in cloud |
| **SOC 1 (SSAE 18)** | Internal controls over financial reporting | Relevant for financial data in cloud |
| **SOC 2** | Security, Availability, Processing Integrity, Confidentiality, Privacy | Most commonly requested by cloud customers; Type I (design) vs Type II (operating effectiveness over time) |
| **SOC 3** | Public-facing SOC 2 report | Summary version; no confidential information; can be publicly shared |
| **PCI DSS** | Payment card data security | 12 requirements for handling credit card data in cloud |
| **HIPAA/HITECH** | Healthcare data protection | Required for PHI in cloud; BAA with provider required |
| **FedRAMP** | US government cloud security | DoD impact levels; baseline controls from NIST 800-53 |
| **GDPR** | EU data protection | Data subject rights, breach notification, data processing agreements |
| **CCPA/CPRA** | California consumer privacy | US state-level data privacy; right to know, delete, opt-out |
| **NIST CSF** | Cybersecurity framework | Identify, Protect, Detect, Respond, Recover functions |
| **CIS Controls** | Prioritized security controls | 18 controls; used as security baseline |
| **NIST 800-53** | Security and privacy controls | FedRAMP baseline; detailed control catalog |
| **NIST 800-145** | Cloud computing definition/characteristics | Defines essential characteristics, service models, deployment models |
| **CSA STAR** | Cloud security assurance | Self-assessment (Level 1), third-party audit (Level 2), continuous monitoring (Level 3) |
| **C5 (Germany)** | Cloud computing compliance | German government's cloud certification |

### 10.2 Cloud Compliance Responsibility

**Shared Compliance Model:**
| Compliance Aspect | Provider Responsibility | Customer Responsibility |
|-------------------|------------------------|------------------------|
| **Infrastructure compliance** | SOC, ISO, FedRAMP, PCI-DSS for underlying infrastructure | N/A (inherited from provider) |
| **Data compliance** | N/A (no access to customer data) | Data classification, handling, protection according to regulations |
| **Application compliance** | Only for SaaS provider-managed apps | Application-level controls, secure coding, configuration |
| **Contractual compliance** | SLA adherence, security commitments | Contractual obligations to own customers |
| **Audit support** | Provide compliance documentation, evidence, access for audits | Cooperate with audits, provide own evidence, manage downstream risks |

**Inherited vs. Customer-Managed Controls:**
- **Inherited**: Controls fully managed by the provider (physical security, infrastructure hardening, hypervisor security)
- **Customer-Managed**: Controls managed by the customer (IAM, data encryption, OS patching, application security, network configuration)
- **Shared**: Controls where responsibility is divided (patch management, vulnerability management, security awareness)

### 10.3 Cloud Governance

**Cloud Governance Pillars (AWS CAF):**
1. **Cost Governance**: Budgets, cost allocation tags, resource optimization, anomaly detection
2. **Security Governance**: IAM policies, detective controls, incident response, encryption standards
3. **Operational Governance**: Monitoring, alerting, incident management, change management, SLOs/SLIs/SLAs
4. **Compliance Governance**: Automate compliance checks, audit evidence collection, regulatory mappings
5. **Data Governance**: Data classification, retention policies, data lifecycle management, privacy controls

**Cloud Governance Tools:**
- **AWS Control Tower**: Set up governed multi-account environment; pre-built guardrails (preventive and detective); account factory; centralized logging
- **Azure Landing Zones**: Enterprise-scale architecture; subscription policies; management group hierarchy; Azure Blueprints
- **GCP Resource Hierarchy**: Organization > Folders > Projects > Resources; Organization Policies at each level

**Service Control Policies (SCPs) / Organization Policies:**
- **AWS SCPs**: Centrally control maximum permissions across accounts; cannot grant permissions (only deny); effective in member accounts
  - Example SCP: Deny EC2 instances without encryption; Deny using non-approved regions; Deny deleting CloudTrail logs
- **Azure Policy**: Enforce/deny resource configurations; audit compliance; remediation tasks; inherit through management group hierarchy
  - Example Azure Policy: Require SQL Server encryption; Restrict VM SKUs; Deny public IP on NICs
- **GCP Organization Policies**: Boolean/list constraints at organization/folder/project level; deny public bucket access; restrict VM external IPs

### 10.4 Audit Processes

**Cloud Audit Types:**
- **Internal Audit**: Organization's own audit team evaluates compliance with internal policies and standards
- **External Audit**: Independent third-party assesses against frameworks (SOC 2, ISO 27001, PCI DSS)
- **Provider Audit**: Customer audits the cloud provider (limited scope; usually rely on provider's certifications)
- **Regulatory Audit**: Government/regulatory body audits compliance with regulations

**Audit Evidence in the Cloud:**
- **Automated Evidence Collection**: AWS Config, Azure Policy, GCP Organization Policies provide compliance snapshots
- **CloudTrail/Activity Log/Audit Logs**: Complete history of administrative actions
- **Access Reports**: IAM credential reports, access analyzer findings, Azure AD sign-in/log reports
- **Vulnerability Assessments**: Inspector, Defender for Cloud, SCC findings
- **Configuration Snapshots**: Periodic AWS Config snapshots; Azure Resource Graph queries

**Audit Challenges in Cloud:**
1. **Dynamic Environments**: Traditional point-in-time audits insufficient; need continuous compliance monitoring
2. **Shared Responsibility**: Auditors must understand what provider vs. customer controls
3. **Lack of Physical Access**: Cannot walk through data centers; rely on SOC reports, certifications
4. **Multi-Tenancy**: Evidence must demonstrate tenant isolation
5. **Data Residency**: Data may move across regions; need controls to enforce data location

### 10.5 Vendor Management and Third-Party Risk

**Vendor Risk Assessment:**
- Review provider certifications (SOC 2 Type II, ISO 27001, FedRAMP, PCI-DSS Attestation of Compliance)
- Evaluate provider security posture: Incident response, encryption, access control, logging, BCDR
- Review provider's shared responsibility matrix
- Assess provider's sub-processors (third-party dependencies)
- Review security incident history and breach notifications
- Evaluate SLA commitments (uptime guarantees, response times, credits for breach)

**Contract Management:**
| Contract Element | Description |
|-----------------|-------------|
| **SLA (Service Level Agreement)** | Uptime guarantees (99.9%, 99.99%), performance metrics, credits for breaches, measurement methodology |
| **MSA (Master Service Agreement)** | Overall terms; liability limits, indemnification, termination, governing law |
| **DPA (Data Processing Agreement)** | Data processing terms; required for GDPR compliance; defines data controller/processor roles |
| **BAA (Business Associate Agreement)** | Required for HIPAA; defines PHI handling responsibilities |
| **SOW (Statement of Work)** | Specific service deliverables, timelines, requirements |
| **Right to Audit** | Customer's right to audit provider (often limited; provider may charge for audit support) |

**Vendor Lock-In Mitigation:**
- Use portable, open standards (Terraform for IaC, OpenTofu/Terraform for multi-cloud, Docker for containers, Kubernetes for orchestration, OIDC for identity)
- Avoid provider-specific services where open alternatives exist (use standard PostgreSQL instead of Aurora, standard Kafka instead of MSK, standard SQL instead of proprietary NoSQL)
- Design for multi-cloud or hybrid deployment (even if initially using single cloud)
- Maintain data portability (export data periodically, validate export format)
- Evaluate exit costs and data egress fees upfront

---

## 11. Legal, Risk, and Compliance (CCSP Domain 6)

### 11.1 Data Sovereignty and Jurisdiction

**Data Sovereignty**: Data is subject to the laws of the country/region where it is physically stored.

**Key Considerations:**
- **Data Residency Requirements**: Some countries require certain data to remain within national borders (GDPR in EU, PIPEDA in Canada, LGPD in Brazil, Personal Information Protection Law in China)
- **Conflict of Laws**: Cloud data across multiple jurisdictions may be subject to conflicting legal requirements
- **Law Enforcement Access**: US CLOUD Act allows US law enforcement to request data from US-based providers regardless of data location; GDPR restricts data transfer outside EU
- **Schrems II Ruling**: Invalidated EU-US Privacy Shield; requires supplementary measures for data transfers (Standard Contractual Clauses + technical controls)

**Cross-Border Data Transfer Mechanisms:**
1. **Adequacy Decision**: EC determines country has adequate data protection
2. **Standard Contractual Clauses (SCCs)**: Pre-approved contractual terms between data exporter/importer
3. **Binding Corporate Rules (BCRs)**: Multinational companies' internal data protection policies
4. **Code of Conduct**: Approved codes demonstrating compliance
5. **Certification**: Approved certification mechanisms (e.g., ISO 27018)

### 11.2 Privacy Regulations

| Regulation | Region | Key Requirements |
|------------|--------|-----------------|
| **GDPR** | EU/EEA | Data subject rights, consent, breach notification (72 hours), DPO, DPIA, data portability, right to erasure, data protection by design/default, fines up to 4% of global annual revenue |
| **CCPA/CPRA** | California | Right to know, delete, opt-out of sale; non-discrimination; private right of action for breaches |
| **HIPAA** | USA | PHI protection, BAAs, minimum necessary rule, privacy rule, security rule, breach notification |
| **PIPEDA** | Canada | Consent, reasonable collection/use/disclosure, access, accuracy, safeguards |
| **LGPD** | Brazil | Similar to GDPR; consent, data subject rights, DPO, breach notification, fines |
| **PDPA** | Singapore | Consent, purpose limitation, access/correction, data breach notification, data portability |
| **POPIA** | South Africa | Consent, purpose specification, security measures, data subject rights, breach notification |

### 11.3 eDiscovery in the Cloud

**eDiscovery Challenges:**
- Data across multiple jurisdictions with varying legal frameworks
- Data held by third-party provider; different response times and processes for legal hold
- Dynamic/auto-scaled resources; data may not persist in original form
- Provider may not allow direct forensic access

**eDiscovery Preparations:**
- Understand provider's processes for legal holds, data preservation, and data production
- Document data flow: where data resides, how it moves, who has access, retention periods
- Implement data classification to identify relevant data quickly
- Ensure ability to place legal hold on data (S3 Object Lock, Azure legal hold, GCP retention policies)
- Maintain data maps for rapid eDiscovery response

**Standards:**
- **ISO 27050**: Guidelines for eDiscovery in electronic environments
- **CSA eDiscovery Guidance**: Cloud-specific eDiscovery recommendations

### 11.4 Enterprise Risk Management (ERM) for Cloud

**Risk Management Process:**
```
1. Risk Identification → 2. Risk Assessment → 3. Risk Treatment → 4. Risk Monitoring → 5. Risk Communication
```

**Cloud-Specific Risks:**

| Risk Category | Examples |
|--------------|----------|
| **Strategic** | Vendor lock-in, provider viability, technology obsolescence, lack of cloud expertise, business disruption from provider outage |
| **Operational** | Misconfiguration, inadequate change management, loss of operational visibility, insufficient incident response capability, API failures, container escapes |
| **Financial** | Unexpected cost overruns, data egress fees, licensing complexity, provider price increases |
| **Compliance** | Violation of data residency laws, insufficient audit evidence, inability to meet regulatory requirements, shared responsibility confusion |
| **Security** | Data breaches, account compromise, insider threat, insecure APIs, DDoS, ransomware, supply chain attack, cryptojacking, metadata exposure |
| **Legal** | Cross-border data transfer restrictions, law enforcement access, breach notification failures, contractual disputes, intellectual property infringement |

**Risk Treatment Options:**
1. **Avoid**: Don't use cloud for high-risk workloads; keep on-premises
2. **Mitigate**: Implement controls to reduce likelihood/impact (encryption, IAM, MFA, monitoring)
3. **Transfer**: Cyber insurance; use managed services to shift responsibility to provider; indemnification clauses
4. **Accept**: Acknowledge and accept residual risk (requires documented risk acceptance by management)
5. **Share**: Share risk with provider or partner (via contractual agreements)

**Risk Assessment Methodologies:**
- **Qualitative**: Risk matrix (Likelihood x Impact = Risk Level); expert judgment
- **Quantitative**: Annualized Loss Expectancy (ALE = SLE x ARO); Monte Carlo simulation; FAIR (Factor Analysis of Information Risk)
- **FAIR Model**: Decomposes risk into probable loss event frequency and loss magnitude

**Key Cloud Risk Management Frameworks:**
- **CSA CCM (Cloud Controls Matrix)**: 197+ controls mapped to CSA STAR, ISO 27001, NIST, PCI-DSS, HIPAA
- **CAIQ (Consensus Assessments Initiative Questionnaire)**: Self-assessment questionnaire for cloud provider evaluations
- **NIST SP 800-30**: Guide for conducting risk assessments
- **ISO 27005**: Information security risk management
- **COBIT 5 for IT Governance**: Enterprise IT governance framework

### 11.5 Business Continuity and Disaster Recovery (BC/DR)

**BC/DR Planning for Cloud:**
- Identify critical workloads and their RPO/RTO requirements
- Design redundant architecture across AZs and regions
- Implement automated failover using cloud-native services (Route53 health checks + failover routing, Azure Traffic Manager, GCP Cloud DNS)
- Test DR procedures regularly (quarterly tabletop, annual full-scale failover test)
- Document runbooks for failover and failback procedures
- Ensure provider SLA for critical services meets BC requirements

**Cloud BC/DR Strategies:**
| Strategy | RPO | RTO | Architecture |
|----------|-----|-----|-------------|
| **Backup & Restore** | Hours to 1 day | Hours to 1 day | Scheduled backups to S3/Glacier/Azure Archive/GCP Archive; restore on failover |
| **Pilot Light** | Minutes | Tens of minutes | Core DB, config running minimal footprint; scale up infrastructure on failover |
| **Warm Standby** | Seconds | Minutes | Reduced-size production environment; DNS switch on failover |
| **Active-Active Multi-Site** | Near-zero | Near-zero | Full production in two+ regions; traffic split via global load balancer |

### 11.6 Audit Reports and Certifications

**SOC Reports for Cloud:**
- **SOC 1**: Internal controls over financial reporting (Type I: design; Type II: operating effectiveness over time)
- **SOC 2**: Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy)
- **SOC 3**: General-use version of SOC 2 (no detail on controls)

**Cloud Provider Certifications:**
- **AWS**: SOC 1/2/3, ISO 27001/27017/27018, PCI DSS Level 1, FedRAMP, HIPAA BAA, GDPR DPA, IRAP, C5, K-ISMS
- **Azure**: SOC 1/2/3, ISO 27001/27017/27018, PCI DSS Level 1, FedRAMP, HIPAA BAA, GDPR DPA, G-Cloud, IRAP
- **GCP**: SOC 1/2/3, ISO 27001/27017/27018, PCI DSS, FedRAMP, HIPAA BAA, GDPR DPA

**How to Evaluate Provider Certifications:**
- Check certification scope (which services, regions, and data centers are covered)
- Verify currency (certification date and renewal cycle)
- Review SOC reports for control deficiencies (review management letter for exceptions)
- Understand audit period covered and whether it's Type I or Type II
- Review shared responsibility mapping between your controls and provider controls

---

## 12. Practical Cloud Security Implementation

### 12.1 AWS Security Quick Wins (First 5 Steps)

1. **Enable CloudTrail** in all regions, all accounts; create multi-region trail; send to central S3 bucket with Object Lock
2. **Enable MFA** on root account; create IAM users/roles with least privilege
3. **Block public access** to S3 at account level (`aws s3 control put-public-access-block`)
4. **Enable GuardDuty** in all regions; configure Security Hub to aggregate findings
5. **Configure VPC Flow Logs** for all VPCs; send to CloudWatch Logs and/or S3

```bash
# Enable S3 block public access at account level
aws s3control put-public-access-block \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true \
  --account-id 123456789012

# Create multi-region CloudTrail
aws cloudtrail create-trail \
  --name my-trail \
  --s3-bucket-name my-cloudtrail-bucket \
  --is-multi-region-trail \
  --enable-log-file-validation \
  --include-global-service-events

# Enable GuardDuty
aws guardduty create-detector --enable

# Create VPC Flow Log
aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids vpc-xxx \
  --traffic-type ALL \
  --log-destination-type cloud-watch-logs \
  --log-group-name vpc-flow-logs
```

### 12.2 Azure Security Quick Wins

1. **Enable Azure Defender for Cloud** (free tier for CSPM, upgrade for advanced threat protection)
2. **Enable MFA** for all admin users via Conditional Access policy
3. **Enable Azure AD Identity Protection** for risk-based policies
4. **Enable diagnostic settings** on all subscriptions (send Activity Log and resource logs to Log Analytics workspace)
5. **Enable Azure Policy** for default resource restrictions (deny public IPs, require encryption)

```powershell
# Create diagnostic setting for subscription
$subscriptionId = Get-AzSubscription
$workspace = Get-AzOperationalInsightsWorkspace | Select-Object -First 1
Set-AzDiagnosticSetting `
  -ResourceId "/subscriptions/$($subscriptionId.Id)" `
  -WorkspaceId $workspace.ResourceId `
  -Enabled $true `
  -Category "Administrative","Security","Policy","AuditLog"

# Assign built-in policy for SQL encryption
New-AzPolicyAssignment `
  -Name "sql-encryption-policy" `
  -PolicySetDefinitionId "/providers/Microsoft.Authorization/policySetDefinitions/..."
```

### 12.3 GCP Security Quick Wins

1. **Enable Cloud Audit Logs** (Admin Activity already enabled; enable Data Access for sensitive APIs)
2. **Set up Organization Policies** (restrict VM external IPs, trusted images, location restrictions)
3. **Enable Security Command Center** (Standard tier free; Premium for advanced features)
4. **Enable MFA** for all users via Cloud Identity / Google Workspace
5. **Enable VPC Flow Logs** and Firewall Rules Logging

```bash
# Set organization policy to restrict public bucket access
gcloud resource-manager org-policies set-policy \
  --organization=123456789 \
  /path/to/iam.disableServiceAccountKeyUpload.yaml

# Create log sink to BigQuery for analysis
gcloud logging sinks create cloud-security-logs \
  bigquery.googleapis.com/projects/my-project/datasets/audit_logs \
  --log-filter='logName:"cloudaudit.googleapis.com"'
```

### 12.4 Common Cloud Security Tools Matrix

| Function | AWS | Azure | GCP | Multi-Cloud/Third-Party |
|----------|-----|-------|-----|------------------------|
| **SIEM/Security Analytics** | Security Hub | Sentinel, Log Analytics | Security Command Center | Splunk, Sumo Logic, ELK, Datadog |
| **Threat Detection** | GuardDuty | Defender for Cloud | Event Threat Detection, SCC | CrowdStrike, SentinelOne, Wiz, Lacework |
| **Vulnerability Scanning** | Inspector | Defender for Cloud VA | SCC, Web Security Scanner | Qualys, Rapid7, Tenable, Snyk |
| **CSPM (Posture Management)** | Security Hub, Config | Defender for Cloud, Azure Policy | SCC, Org Policies | Wiz, Prisma Cloud, Lacework, Check Point |
| **IAM** | IAM, IAM Identity Center | Azure AD, RBAC | Cloud IAM, Workforce Identity | Okta, Azure AD, OneLogin, Keycloak |
| **Secrets Management** | Secrets Manager, Systems Manager PS | Key Vault | Secret Manager | HashiCorp Vault, CyberArk, Akeyless |
| **Key Management** | KMS, CloudHSM | Key Vault, Managed HSM | Cloud KMS, Cloud HSM | HashiCorp Vault, Fortanix, Thales |
| **Web Application Firewall** | WAF, Shield | WAF, Front Door WAF | Cloud Armor | Cloudflare, Akamai, Fastly |
| **Container Security** | ECR Scan, GuardDuty EKS | Defender for Containers | SCC Container Threat Detection | Aqua, Sysdig, Prisma Cloud, Twistlock |
| **Data Classification** | Macie | Purview | Sensitive Data Protection | BigID, Varonis, Spirion |
| **Infrastructure Compliance** | Config, Audit Manager | Azure Policy, Blueprints | Org Policies, Resource Manager | Prisma Cloud, Wiz, Checkov, Terraform Sentinel |
| **Service Mesh/Network Security** | Network Firewall, WAF | Firewall, WAF | Cloud Armor, Firewall | Palo Alto VM-Series, Fortinet, Check Point |

---

## 13. Cloud Security Certifications

### 13.1 Overview of Major Certifications

| Certification | Focus | Level | Provider |
|--------------|-------|-------|----------|
| **CCSP** | Cloud security architecture, governance, compliance, risk management | Advanced | ISC2 + CSA |
| **CCSK** | Cloud security fundamentals | Foundational | CSA |
| **AWS Certified Security - Specialty** | AWS-specific security | Advanced | AWS |
| **Azure Security Engineer Associate (AZ-500)** | Azure-specific security | Intermediate | Microsoft |
| **Google Cloud Certified - Professional Cloud Security Engineer** | GCP-specific security | Advanced | Google |
| **CompTIA Security+** | General cybersecurity fundamentals | Foundational | CompTIA |
| **CISSP** | Broad security management | Advanced | ISC2 |
| **CISM** | Security management and governance | Advanced | ISACA |
| **CISA** | Audit and control | Advanced | ISACA |
| **CRISC** | Risk and control | Advanced | ISACA |

### 13.2 CCSP Domains Detailed

| Domain | Weight | Key Topics |
|--------|--------|------------|
| **1. Cloud Concepts, Architecture & Design** | 17% | Cloud computing definitions (NIST), service models, deployment models, cloud architecture components, security concepts, design principles, DR/BC, risk assessment, shared responsibility model |
| **2. Cloud Data Security** | 20% | Data lifecycle (create/store/use/share/archive/destroy), data classification, data at-rest/in-transit encryption, key management, tokenization, data loss prevention, data rights management, data retention/destruction, data sovereignty |
| **3. Cloud Platform & Infrastructure Security** | 17% | Physical environment security, network security (VPC/SG/NACL), compute/storage security, virtualization security, container/serverless security, BC/DR, infrastructure risk analysis |
| **4. Cloud Application Security** | 17% | Secure SDLC, application security testing (SAST/DAST), DevSecOps, identity/federation, APIs, secure coding, supply chain security, vulnerability management |
| **5. Cloud Security Operations** | 16% | Incident response (preparation/detection/containment/eradication/recovery/lessons learned), forensics, logging/monitoring, SIEM/SOAR, configuration management, patch management, change management |
| **6. Legal, Risk & Compliance** | 13% | Legal frameworks (GDPR, CCPA, HIPAA, SOX), data privacy, audit processes/methodologies, enterprise risk management, vendor management, eDiscovery, compliance frameworks, contracts (SLA/MSA/DPA), breach notification |

### 13.3 CSA Cloud Controls Matrix (CCM) and STAR

**CSA CCM**: 197+ controls across 16 domains:
- Application & Interface Security
- Audit Assurance & Compliance
- Business Continuity Management & Operational Resilience
- Change Control & Configuration Management
- Data Security & Information Lifecycle Management
- Data Center Security
- Encryption & Key Management
- Governance & Risk Management
- Human Resources Security
- Identity & Access Management
- Infrastructure & Virtualization Security
- Interoperability & Portability
- Mobile Security
- Security Incident Management, eDiscovery & Cloud Forensics
- Supply Chain Management, Transparency & Accountability
- Threat & Vulnerability Management

**CSA STAR Levels:**
- **Level 1**: Self-assessment (submit CAIQ)
- **Level 2**: Third-party independent assessment (SOC 2 Type II or equivalent + CCM mapping)
- **Level 3**: Continuous monitoring (automated compliance monitoring)

---

## 14. Cloud Security Attack Vectors and Case Studies

### 14.1 Major Cloud Attack Vectors

| Vector | Description | Real-World Example |
|--------|-------------|-------------------|
| **Misconfigured S3 Buckets** | Publicly accessible storage exposing sensitive data | Accenture (137 GB, plaintext credentials), WWE (3M records), Verizon (14M records), US DoD (1.8B social media records), GoDaddy |
| **Compromised Credentials** | Stolen access keys, leaked passwords, phishing | Capital One (2019, WAF SSRF + compromised IAM role); attacker accessed 100M+ customer records via misconfigured WAF |
| **IAM Privilege Escalation** | Exploiting permissive policies to gain elevated access | Multiple AWS IAM privilege escalation techniques (PassRole, CreatePolicyVersion, SetDefaultPolicyVersion, CreateLoginProfile) |
| **SSRF to Instance Metadata** | Server-Side Request Forgery accessing IMDS | Capital One breach (SSRF via WAF to metadata endpoint). IMDSv1 allows unauthenticated access; always use IMDSv2 with hop limit |
| **Supply Chain Attacks** | Compromised third-party components | SolarWinds (2020), CodeCov (2021); malicious code injected into build pipeline; propagated to cloud environments via trusted updates |
| **Container Escapes** | Breaking out of container isolation | CVE-2019-5736 (runC), CVE-2022-0811 (CRI-O), Kubernetes container escape allowing host OS root access |
| **Cryptomining (Cryptojacking)** | Unauthorized use of compute for cryptocurrency mining | Multiple cases of compromised AWS/Azure/GCP accounts used to spin up GPU instances for mining |
| **Ransomware in Cloud** | Encrypting cloud data with ransomware | Ransomware attacks targeting cloud storage (especially without versioning/Object Lock); backups also encrypted if accessible |
| **DDoS** | Distributed Denial of Service targeting cloud resources | GitHub (2018, 1.35 Tbps via memcached amplification), AWS (2020, 2.3 Tbps) |
| **API Abuse** | Exploiting cloud APIs for unauthorized access | Multiple serverless/Lambda vulnerabilities, API Gateway misconfigurations |
| **Insider Threat** | Malicious or negligent actions by authorized users | Tesla (2018, former employee modified code and exfiltrated data from AWS); Ubiquiti (2021, insider threatened to leak data / BEC) |

### 14.2 Capital One Breach (2019) - Detailed Analysis

**Attack Timeline:**
1. **Reconnaissance**: Attacker (Paige Thompson, former AWS employee) scanned internet for identifiable endpoints using specific AWS metadata characteristics
2. **SSRF Exploitation**: Capital One's WAF (Web Application Firewall) had a misconfiguration allowing SSRF (Server-Side Request Forgery). A WAF rule failed to block requests that could reach the EC2 metadata service
3. **Metadata Access**: Attacker accessed the EC2 instance metadata endpoint (169.254.169.254) to retrieve temporary IAM credentials assigned to the WAF role
4. **Credential Use**: Used the stolen IAM credentials to call AWS APIs as the WAF role
5. **Data Exfiltration**: The WAF IAM role had `s3:ListBucket` and `s3:GetObject` permissions (overly permissive). Attacker listed S3 buckets, found data store with customer data, and exfiltrated 30GB+
6. **Impact**: 100M+ US and 6M Canadian customer records exposed (names, addresses, credit scores, SSNs/bank account numbers)

**Root Causes:**
- SSRF vulnerability in WAF (missing filter on metadata endpoint)
- WAF IAM role had S3 read permissions (not least privilege)
- IMDSv1 was enabled (allows unauthenticated metadata access vs IMDSv2 which requires token)
- No data segmentation between WAF role and sensitive data

**Remediations Applied:**
- Upgraded to IMDSv2 (requires PUT requests + token for metadata)
- Tightened IAM policies for all roles (no S3 access unless strictly required; resource-based policies)
- Added network controls (security groups to block metadata endpoint access from untrusted traffic)
- Implemented GuardDuty with S3 anomaly detection
- Deployed automated IAM Access Analyzer

### 14.3 Common Cloud Security Misconfigurations Checklist

- [ ] S3/Blob/GCS buckets publicly accessible (check via provider tools)
- [ ] IAM policies with Action: `*` or Resource: `*` (wildcard permissions)
- [ ] Security groups allowing 0.0.0.0/0 to SSH (22), RDP (3389), databases
- [ ] Root/admin account without MFA
- [ ] CloudTrail/Audit Logs not enabled or not covering all regions
- [ ] Default encryption not enabled on storage/services
- [ ] EC2/VM access keys stored in instance or user data
- [ ] Unused security groups, IAM users, access keys, roles not removed
- [ ] Unrestricted outbound traffic to internet (no egress filtering)
- [ ] Public AMIs/container images used without verification
- [ ] Passwords hardcoded in code, config files, or public repos
- [ ] VPC Flow Logs not enabled
- [ ] GuardDuty/Defender/SCC not enabled
- [ ] Automatic minor version upgrades disabled on databases
- [ ] RDS/Cloud SQL publicly accessible
- [ ] Load balancer not using HTTPS listener
- [ ] SSL/TLS certificate not properly configured or expired
- [ ] No resource tagging for governance/labeling
- [ ] Backup/DR plan not tested
- [ ] IaC state files (terraform.tfstate) storing secrets in plaintext

---

## 15. Advanced Cloud Security Concepts

### 15.1 Confidential Computing

Confidential computing protects data **in use** by executing code in a hardware-based Trusted Execution Environment (TEE).

**Technologies:**
- **Intel SGX (Software Guard Extensions)**: Enclaves in memory; CPU-level isolation; code/data encrypted in memory - decrypted only inside CPU
- **Intel TDX (Trust Domain Extensions)**: Full VM-level confidential computing
- **AMD SEV/SEV-SNP (Secure Encrypted Virtualization)**: Encrypts VM memory; SNP adds integrity protection (memory encryption, nested page table protection)
- **NVIDIA Confidential Computing**: GPU memory isolation for AI/ML workloads

**Cloud Offerings:**
- **AWS Nitro Enclaves**: Isolated, hardened compute environments; no persistent storage, no shell access; attestation via KMS
- **Azure Confidential Computing**: Confidential VMs (DCasv5, ECasv5) with AMD SEV-SNP; Intel SGX for application enclaves
- **GCP Confidential VMs**: N2D VMs with AMD SEV-ES; Shielded VMs

**Use Cases:**
- Multi-party analytics (collaborate without exposing raw data)
- Protecting PII/PHI during processing
- Financial services (fraud models across institutions)
- IP protection (AI/ML models as protected assets)

### 15.2 Zero Trust Architecture (ZTA)

**Core Principles (NIST SP 800-207):**
1. All data sources and computing services are resources
2. All communication is secured regardless of network location
3. Access to individual enterprise resources is granted on a per-session basis
4. Access to resources is determined by dynamic policy (user/device health/behavior)
5. Monitor and measure integrity and security posture of all owned/associated assets
6. All resource authentication and authorization is dynamic and strictly enforced before access allowed
7. Collect as much information as possible about the current state of assets, network infrastructure, and communications to improve security posture

**Zero Trust in Cloud:**
- **Micro-segmentation**: Per-resource security groups, service-to-service IAM roles, namespace isolation
- **Service Mesh**: Envoy/Istio/Linkerd; mutual TLS, fine-grained traffic policies, observability
- **GCP BeyondCorp**: Zero Trust access based on device/user/context (not network location)
- **AWS Verified Access**: ZTNA for corporate applications without VPN
- **Azure AD Conditional Access**: Evaluate user, device, location, risk for access decisions

### 15.3 Service Mesh Security

**What is a Service Mesh?** Dedicated infrastructure layer for handling service-to-service communication in microservices architectures.

**Security Features:**
- **mTLS**: Automatic mutual TLS between all services; transparent encryption and authentication
- **Authorization Policies**: Fine-grained RBAC/ABAC at service level
- **Traffic Policies**: Rate limiting, circuit breaking, retry budgets for security and resilience
- **Observability**: Distributed tracing, metrics, access logs for all service communications
- **Identity-based Security**: Each service gets identity (SPIFFE-compliant) verified via X.509 certs

**Service Mesh Implementations:**
- **Istio**: Most popular; sidecar-based (Envoy proxy); mTLS, authorization, tracing, telemetry; integrates with GKE, AKS, EKS
- **Linkerd**: Lightweight, Rust-based sidecar proxy; automatic mTLS; minimal configuration
- **Consul Connect**: HashiCorp's service mesh; native integration with Consul service discovery
- **AWS App Mesh**: Managed service mesh for AWS; supports ECS, EKS, EC2
- **Open Service Mesh**: Lightweight, SMI-compliant, OSS

### 15.4 Cloud Security Posture Management (CSPM)

CSPM tools continuously monitor cloud environments for misconfigurations, compliance violations, and security risks.

**Key Capabilities:**
- **Configuration Assessment**: Scan against CIS benchmarks, NIST CSF, PCI-DSS, SOC 2
- **Compliance Monitoring**: Map to frameworks; report compliance scores; evidence collection
- **Drift Detection**: Alert when resource configurations deviate from IaC-defined state
- **IaC Scanning**: Integrate with CI/CD to scan templates before deployment
- **Remediation**: One-click fix or automated remediation via policy engines
- **Agentless**: Use cloud provider APIs (no agents needed)

**CSPM Vendors:**
- **Wiz**: Agentless; graph-based analysis; vulnerability finder, IaC scanning; supports AWS/Azure/GCP/OCI
- **Prisma Cloud (Palo Alto)**: CSPM + CWPP + CIEM + IAC; broadest feature set
- **Lacework**: ML-based behavioral analysis; anomaly detection
- **CloudCheckr (Netskope)**: Cost + security management
- **AWS Security Hub**: Native CSPM; aggregates findings, CIS benchmarks, automated compliance
- **Azure Defender for Cloud (CSPM tier)**: Secure score, compliance dashboard, recommendations
- **GCP Security Command Center (Premium)**: Threat detection + vulnerability + posture management

### 15.5 Cloud Infrastructure Entitlement Management (CIEM)

CIEM manages and enforces least privilege across cloud identities and entitlements.

**Key Functions:**
- **Entitlement Discovery**: Find all IAM users, roles, policies, service accounts across multi-cloud
- **Permission Analysis**: Identify unused/excessive permissions and privilege escalation paths
- **Least Privilege Enforcement**: Generate least-privilege policies based on actual usage
- **Cross-Cloud IAM**: Unified visibility across AWS/Azure/GCP
- **Usage Analytics**: Analyze actual permission usage vs. granted permissions; identify orphaned roles/users

**CIEM Vendors:**
- **CloudKnox (acquired by Microsoft, now part of Defender for Cloud)**
- **Ermetic (now part of Wiz)**
- **Saviynt**
- **AWS IAM Access Analyzer**

### 15.6 Cloud Workload Protection Platform (CWPP)

CWPP provides unified workload protection across VM, container, serverless, and on-premises.

**Key Capabilities:**
- **Vulnerability Scanning**: OS packages, libraries, application dependencies
- **Runtime Protection**: Behavioral monitoring; block malicious processes, file writes, network connections
- **Host Firewall**: Kernel-level or agent-based firewall rules
- **Integrity Monitoring**: File integrity, configuration drift detection
- **Application Control**: Allow-list approved applications; block unrecognized binaries
- **Exploit Prevention**: Behavioral exploit detection/prevention

**CWPP Vendors:**
- **CrowdStrike Falcon Cloud Security**: Single agent; EDR + CWPP; real-time protection
- **Trend Micro Cloud One - Workload Security**: Deep security for cloud workloads
- **Aqua Security**: Container and serverless focused
- **Sysdig**: Container/Kubernetes-focused runtime security
- **Amazon Inspector**: EC2/ECR vulnerability scanning

### 15.7 Secure Access Service Edge (SASE)

SASE converges network connectivity (SD-WAN) with cloud-native security functions.

**Components:**
- **SD-WAN**: Software-defined WAN for optimized connectivity to cloud
- **SWG (Secure Web Gateway)**: Web filtering, URL filtering, malware protection
- **CASB (Cloud Access Security Broker)**: Visibility and control over sanctioned/unsanctioned SaaS
- **ZTNA (Zero Trust Network Access)**: Application-specific, context-aware access without VPN
- **FWaaS (Firewall as a Service)**: Cloud-based next-gen firewall

**SASE Vendors:**
- **Zscaler**: ZTNA, SWG, CASB; cloud-native, no appliances
- **Cloudflare One**: ZTNA, SWG, CASB, DLP
- **Netskope**: CASB, SWG, ZTNA; strong data loss prevention
- **Palo Alto Prisma Access**: SASE with SD-WAN
- **Cato Networks**: SD-WAN + security in single platform

---

## 16. Cloud Security Resources

### Standards and Frameworks
- **NIST SP 800-145**: Cloud computing definition
- **NIST SP 800-210**: General guidelines on cloud security
- **NIST SP 800-207**: Zero Trust Architecture
- **NIST CSF (Cybersecurity Framework)**: Identify, Protect, Detect, Respond, Recover
- **ISO 27001/27017/27018**: ISMS, Cloud Security, PII Protection
- **CSA CCM (Cloud Controls Matrix)**: https://cloudsecurityalliance.org/research/cloud-controls-matrix
- **CSA CAIQ**: https://cloudsecurityalliance.org/research/consensus-assessments-initiative
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **OWASP Cloud Security Top 10**: https://owasp.org/www-project-cloud-security/
- **CIS Benchmarks**: https://www.cisecurity.org/benchmark/cloud-security

### Provider Documentation
- **AWS Security Best Practices**: https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
- **AWS Security Hub**: https://aws.amazon.com/security-hub/
- **Azure Security Best Practices**: https://learn.microsoft.com/en-us/azure/security/
- **Azure Defender for Cloud**: https://learn.microsoft.com/en-us/azure/defender-for-cloud/
- **GCP Security Best Practices**: https://cloud.google.com/docs/security
- **GCP Security Command Center**: https://cloud.google.com/security-command-center

### Tools
- **AWS CLI**: `aws configure`, `aws securityhub`, `aws guardduty`, `aws inspector`
- **Azure CLI**: `az security`, `az monitor`, `az policy`
- **GCP gcloud**: `gcloud services enable`, `gcloud scc`, `gcloud logging`
- **Terraform**: Infrastructure as Code for all providers
- **Checkov**: IaC security scanning (terraform, cloudformation, arm, bicep, terraform)
- **tfsec**: Terraform static analysis
- **Trivy**: Container and vulnerability scanner
- **OWASP ZAP**: Web application security scanner
- **CloudSploit / Aqua CloudSploit**: Open-source CSPM
- **Prowler**: AWS-specific security assessment tool (https://github.com/prowler-cloud/prowler)
- **ScoutSuite**: Multi-cloud security auditing tool
- **Steampipe**: Query cloud infrastructure with SQL

### Training and Certifications
- **CSA CCSK (Certificate of Cloud Security Knowledge)**: https://cloudsecurityalliance.org/education/ccsk/
- **ISC2 CCSP**: https://www.isc2.org/Certifications/CCSP
- **AWS Security-Specialty**: https://aws.amazon.com/certification/certified-security-specialty/
- **Azure AZ-500**: https://learn.microsoft.com/en-us/certifications/exams/az-500
- **GCP Professional Cloud Security Engineer**: https://cloud.google.com/learn/certification/cloud-security-engineer

### Playlists (Reference Sources)
- **Cloud Security Fundamentals Overview**: https://www.youtube.com/playlist?list=PLsfnCRA9QVnSj4gbP5W1W1CXjPRhe1oE2
- **Cyber Security Training for Beginners (Edureka)**: https://www.youtube.com/playlist?list=PL9ooVrP1hQOGPQVeapGsJCktzIO4DtI4_
- **CCSP Full Course**: https://www.youtube.com/playlist?list=PL2QcdSWyXri2e6jjpmdT0JAh_xtkgOEbZ

### Books
- "CCSP Certified Cloud Security Professional Official Study Guide" - Mike Chapple, David Seidl
- "CSA Guide to Cloud Computing" - Raj Samani, Brian Honan, Jim Reavis
- "Cloud Security: A Comprehensive Guide to Secure Cloud Computing" - Ronald Krutz, Russell Vines
- "Zero Trust Networks" - Razi Rais, Christina Morillo, Evan Gilman, Doug Barth
- "Hacking Kubernetes" - Andrew Martin, Michael Ducy
- "The DevOps Handbook" - Gene Kim, Jez Humble, Patrick Debois, John Willis

---

> **Remember**: In cloud security, the provider secures the infrastructure, but the customer is ALWAYS responsible for their data, identities, configurations, and applications. Most cloud breaches result from customer misconfiguration, not provider vulnerabilities.

---

## 17. Cloud Security Architecture Patterns

### 17.1 Single VPC / Single Account Architecture
- **Use Case**: Small deployments, development/testing, single application
- **Pros**: Simple, easy to manage, low cost
- **Cons**: No isolation, blast radius = entire account, limited security boundaries
- **Security Controls**: Security groups, NACLs, IAM with least privilege, enable CloudTrail + GuardDuty

### 17.2 Multi-VPC / Multi-Account (Hub-and-Spoke) Architecture
- **Use Case**: Production workloads, multiple teams/departments, compliance requirements
- **Architecture**: Central hub VPC/account for shared services (firewalls, VPN, logging, DNS); spoke VPCs/accounts for workloads
- **Security Benefits**:
  - Isolation between workloads
  - Centralized egress/inspection via Transit VPC/Network Virtual Appliance
  - Blast radius limited to single VPC/account
  - Simplified audit and compliance (central logging)
- **AWS**: AWS Organizations + Transit Gateway + VPCs + Network Firewall
- **Azure**: Management Groups + Virtual WAN + Hub VNet + Azure Firewall
- **GCP**: Organization + Shared VPC + Cloud Firewall

### 17.3 Three-Tier Web Application Architecture

```
Internet → WAF/CloudFront → ALB (Public Subnet) → Web Tier (App Subnet) → App Tier (Private Subnet) → DB Tier (Isolated Subnet)
```

**Security Layers**:
| Tier | Subnet Type | Security Controls |
|------|-------------|-------------------|
| **CDN/WAF** | Edge | DDoS protection (Shield/Cloud Armor), WAF rules (OWASP), rate limiting, geo-restriction, bot control |
| **Load Balancer** | Public | SSL/TLS termination, security group allowing HTTPS (443) from internet only, access logs |
| **Web Tier** | Private/App | Security group allowing HTTP(S) from ALB only, autoscaling group, OS hardening, CIS benchmark |
| **Application Tier** | Private | Security group allowing app traffic from web tier only, no direct internet access, NAT for outbound updates |
| **Database Tier** | Isolated/Data | Security group allowing DB port from app tier only, encryption at rest, automated backups, no public access |

### 17.4 Microservices / Service Mesh Architecture

**Components**:
- **API Gateway**: Entry point; authentication, rate limiting, routing, aggregation
- **Service Mesh**: Istio, Linkerd, Consul; mTLS between services, traffic policies, observability
- **Sidecar Proxies**: Envoy per service pod; intercept all traffic, enforce mTLS/authorization
- **Identity**: SPIFFE/SPIRE for workload identity; X.509 certs for each service

**Security Controls**:
- mTLS enforced for ALL service-to-service communication
- Authorization policies per service (which services can call which endpoints)
- Ingress/Egress control via Gateway API
- Service-level rate limiting and circuit breaking
- Distributed tracing for forensic analysis

### 17.5 Data Lake / Analytics Architecture

**Components**: S3/Data Lake Storage, Glue/Data Catalog, Athena/Redshift Spectrum/EMR, QuickSight

**Security Considerations**:
- **Encryption**: SSE-KMS with bucket policies enforcing encryption; encryption in transit (HTTPS only)
- **Access Control**: Bucket policies with VPC endpoint conditions; IAM roles for each analytics service
- **Data Classification**: Macie/Purview/Sensitive Data Protection for automatic classification
- **Row/Column Level Security**: Lake Formation, Redshift/Custom SQL views
- **Audit**: CloudTrail data events for S3, service-specific logs (Athena, Glue, EMR)
- **Network**: VPC endpoints for all analytics services; no public internet access
- **Data Masking**: Dynamic masking for PII in query results

### 17.6 Hybrid Cloud Architecture

**Components**:
- **VPN Connection**: Site-to-Site VPN (IPsec) between on-prem and cloud VPC
- **Dedicated Connection**: AWS Direct Connect / Azure ExpressRoute / GCP Dedicated Interconnect (more reliable, lower latency, higher bandwidth than VPN)
- **Private Connectivity**: AWS Transit Gateway + Direct Connect Gateway; Azure Virtual WAN + ExpressRoute
- **DNS Resolution**: Route53 Resolver / Azure DNS Private Resolver / GCP Cloud DNS forwarding

**Security Considerations**:
- **Encryption**: IPsec VPN (AES-256, SHA-256, D-H Group 14+); MACsec on dedicated connections
- **Routing**: BGP with prefix filtering; route leak prevention; dedicated private ASNs
- **Firewall**: Central inspection via NVA or cloud firewall (Palo Alto, Fortinet, Check Point in hub VNet/VPC)
- **Identity**: Extend on-prem AD to cloud (AD Connector, Azure AD Connect, GCP Managed AD); federated access
- **Network Segmentation**: Separate VPCs/VNets for different environments; route tables prevent unintended cross-environment traffic
- **Monitoring**: Unified monitoring across on-prem and cloud; SIEM aggregation

### 17.7 Disaster Recovery Architecture

**Deployment Patterns**:

| Pattern | Description | RPO | RTO | Cost |
|---------|-------------|-----|-----|------|
| **Backup & Restore** | Automated backups to secondary region; restore on failover | 1-24 hours | 4-24 hours | Low |
| **Pilot Light** | Core DB replicated; infrastructure scripted; scale up on failover | Minutes | 30-60 min | Medium |
| **Warm Standby (N-1)** | Reduced-size production in secondary region; scale up on DR | Seconds | 5-30 min | Medium-High |
| **Multi-Region Active-Active** | Full production in 2+ regions; traffic split; instant failover | Near-zero | Seconds | High |
| **Multi-Cloud DR** | Workload replicated to second cloud provider; failover between providers | Minutes | Minutes-Hours | High |

**Key DR Automation**:
- **AWS**: CloudFormation + Lambda + Route53 (DNS failover) + RDS Cross-Region Replication + S3 Cross-Region Replication
- **Azure**: Azure Site Recovery + Traffic Manager + SQL Geo-Replication + Cosmos DB multi-region writes
- **GCP**: Deployment Manager + Cloud DNS (geo-routing) + Cloud SQL cross-region replication + Spanner multi-region

### 17.8 CDN / Edge Computing Architecture

**Components**: CloudFront / Azure CDN / Cloud CDN + Lambda@Edge / CloudFront Functions / Cloud Run for edge computing

**Security Benefits**:
- DDoS absorption at edge
- SSL/TLS termination at edge (reduce origin load)
- WAF rules at edge (block attacks before they reach origin)
- Origin shielding (reduce origin load, hide origin IP)
- Geo-restriction (block countries)
- Signed URLs/Cookies (control access to content)
- Field-level encryption (encrypt specific fields at edge)

---

## 18. Cloud Cryptography Deep Dive

### 18.1 Symmetric Encryption Algorithms

| Algorithm | Key Size | Block Size | Status | Use Case |
|-----------|----------|------------|--------|----------|
| **AES-256** | 256-bit | 128-bit | Recommended | Data at rest (S3, EBS, RDS, Azure Disk, GCP Persistent Disk) |
| **AES-128** | 128-bit | 128-bit | Secure | Legacy systems, performance-critical |
| **AES-192** | 192-bit | 128-bit | Secure | Regulatory requirements |
| **ChaCha20** | 256-bit | N/A (stream) | Recommended (TLS 1.3) | Mobile, TLS 1.3 cipher suites; faster than AES on mobile CPUs |
| **Triple DES (3DES)** | 168-bit | 64-bit | Deprecated | Legacy systems; do not use for new deployments |
| **Blowfish** | 32-448 bit | 64-bit | Weak | Legacy; use Twofish or AES instead |
| **Twofish** | 128-256 bit | 128-bit | Secure | Open-source alternatives |

### 18.2 Asymmetric Encryption Algorithms

| Algorithm | Key Size | Use |
|-----------|----------|-----|
| **RSA** | 2048/4096-bit | Key exchange, digital signatures, TLS certificates, SSH keys |
| **ECC (ECDSA/ECDH)** | 256/384/521-bit | Same security as RSA with smaller keys; used in TLS, SSH, blockchain, JWT |
| **Ed25519** | 256-bit | Modern signature algorithm; fast, secure; used in SSH |
| **Curve25519/X25519** | 256-bit | Key exchange in TLS 1.3, SSH |
| **DSA** | 1024-3072-bit | Legacy; replaced by ECDSA/EdDSA |
| **Diffie-Hellman** | 2048/4096-bit | Key exchange (TLS, IPsec); use ECDH instead |
| **Post-Quantum (Kyber, Dilithium, SPHINCS+)** | Varies | NIST selected for future quantum-resistant cryptography (2024); final standards expected 2024-2025 |

### 18.3 Hash Functions

| Algorithm | Output Size | Status | Use Case |
|-----------|-------------|--------|----------|
| **SHA-256** | 256-bit | Recommended | File integrity, digital signatures, certificate verification, blockchain |
| **SHA-384** | 384-bit | Recommended | FIPS-compliant applications |
| **SHA-512** | 512-bit | Recommended | High-security requirements |
| **SHA-3 (256/384/512)** | Varies | Recommended | Newer standard; alternative to SHA-2 |
| **BLAKE2b/BLAKE2s** | Varies | Recommended | Faster than SHA-2/3; used in cryptocurrency, file hashing |
| **MD5** | 128-bit | Broken | Do not use (collision attacks) |
| **SHA-1** | 160-bit | Deprecated | Do not use (SHAttered collision attack, 2017) |

### 18.4 TLS/SSL in Cloud

**TLS Versions**:
| Version | Status | Notes |
|---------|--------|-------|
| **TLS 1.3** | Recommended | Fastest, most secure; 1-RTT handshake (0-RTT resume); AEAD-only ciphers; removed RSA key exchange, RC4, 3DES, CBC |
| **TLS 1.2** | Acceptable | Still widely used; ensure strong cipher suites only (ECDHE + AES-GCM + SHA-2) |
| **TLS 1.1** | Deprecated | Remove support; vulnerable to CBC padding oracle attacks (Lucky13) |
| **TLS 1.0** | Deprecated | Remove support; BEAST attack, POODLE |
| **SSL 3.0** | Insecure | POODLE attack; must not use |
| **SSL 2.0** | Insecure | Do not use |

**Cloud TLS Termination Options**:
- **CloudFront/ALB/NLB (AWS)**: Free SSL/TLS; ACM certificates; automatic renewal; TLS 1.3 support
- **Application Gateway/Front Door (Azure)**: TLS termination; Azure Key Vault for certificate storage
- **Cloud Load Balancer / Cloud CDN (GCP)**: Managed certificates; automatic renewal; TLS 1.2+
- **Nginx/HAProxy on EC2/VM**: Self-managed; complete control over cipher suites and TLS versions

**Recommended TLS Configuration**:
```
Protocols: TLS 1.2, TLS 1.3
Cipher Suites (TLS 1.2): TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384, TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
Cipher Suites (TLS 1.3): TLS_AES_256_GCM_SHA384, TLS_AES_128_GCM_SHA256, TLS_CHACHA20_POLY1305_SHA256
Key Exchange: ECDHE (P-256, P-384, X25519)
Certificate: RSA 2048+ or ECDSA P-256+
HSTS: max-age=31536000; includeSubDomains; preload
Perfect Forward Secrecy: Required (DHE or ECDHE)
```

### 18.5 Key Management Service (KMS) Deep Dive

**AWS KMS**:
- **Keys**: Customer managed (CMK), AWS managed, AWS owned
- **Key Specs**: Symmetric (AES-256) and Asymmetric (RSA_2048/3072/4096, ECC_NIST_P256/384/521, ECC_SECG_P256k1)
- **Key Rotation**: Automatic annual rotation for CMKs (can be enabled)
- **Key Policies**: Resource-based policies defining who can use/administrate keys
- **Grants**: Temporarily delegate KMS permissions to principals
- **HSM**: FIPS 140-2 Level 2 (KMS), Level 3 (CloudHSM, KMS Custom Key Store)
- **Multi-Region Keys**: Replicate keys across regions for DR
- **Integration**: 50+ AWS services (S3, EBS, RDS, Lambda, SQS, SNS, DynamoDB)

**Azure Key Vault**:
- **Key Types**: RSA (2048/3072/4096), EC (P-256/P-256K/P-384/P-521), symmetric (oct, 128-bit+), HSM-protected
- **Soft Delete**: Retains deleted keys/vaults for configurable retention period (7-90 days); purge protection prevents permanent deletion
- **Key Rotation**: Manual or automated via Event Grid + Function
- **Managed HSM**: FIPS 140-2 Level 3; fully managed HSM with dedicated HSM pool
- **RBAC vs Access Policies**: Two authorization models; RBAC recommended for centralized management

**GCP Cloud KMS**:
- **Key Types**: Symmetric (AES-256), Asymmetric (RSA, EC), HSM keys (FIPS 140-2 Level 3)
- **Key Rotation**: Automatic rotation (configurable period); can also manually rotate
- **Key Rings**: Group keys by purpose/environment; region-specific or global
- **Import**: Import existing keys (BYOK)
- **IAM Integration**: Fine-grained permissions per key
- **Cloud External Key Manager (Cloud EKM)**: Use keys from external KMS (Thales, Fortanix) outside GCP

### 18.6 Hardware Security Module (HSM) Deep Dive

| Provider | Service | Cert Level | Key Control | Pricing |
|----------|---------|------------|-------------|---------|
| **AWS** | CloudHSM | FIPS 140-2 Level 3 | Customer exclusive control; single-tenant HSM instances | Per-hour per HSM; ~$1.50/hr |
| **AWS** | KMS Custom Key Store | FIPS 140-2 Level 3 | Keys in CloudHSM; managed through KMS API | CloudHSM fees + KMS fees |
| **Azure** | Dedicated HSM | FIPS 140-2 Level 3, eIDAS | Customer-managed HSM appliances (Thales Luna) | Per-appliance; contact sales |
| **Azure** | Azure Managed HSM | FIPS 140-2 Level 3 | Managed pool of HSMs; RBAC-controlled; multi-region | Per-hour per partition |
| **GCP** | Cloud HSM | FIPS 140-2 Level 3 | Keys in Cloud KSM backed by HSM; shared HSM pool | Per-key version per month |
| **GCP** | Cloud EKM | FIPS 140-2 | Keys managed in external partner HSM (Thales, Fortanix) | Partner pricing |

**HSM Use Cases**:
- **PCI-DSS Compliance**: Generate and protect cardholder data encryption keys
- **Code Signing**: Sign code/manifests with HSM-protected keys
- **Certificate Authority**: Operate private CA with HSM-rooted trust
- **Database TDE Master Key**: Protect database encryption keys
- **Blockchain/PKI**: HSM-backed key generation and signing

### 18.7 Digital Certificates in Cloud

**Certificate Options**:

| Provider | Service | Certificate Types | Auto-Renewal |
|----------|---------|------------------|--------------|
| **AWS** | ACM (Certificate Manager) | Public (SSL/TLS), Private (PCA) | Yes (60 days before expiry) |
| **Azure** | Key Vault Certificates | Self-signed, CA-issued (integrated with DigiCert/GlobalSign/Let's Encrypt) | Yes (via Key Vault + App Gateway/ Front Door) |
| **GCP** | Certificate Manager | Google-managed (LetsEncrypt), Self-managed | Yes (Google-managed auto-renew) |

**Certificate Automation**:
- **ACME (Automated Certificate Management Environment)**: Let's Encrypt, ZeroSSL; automated issuance/renewal via certbot, acme.sh, lego
- **ACM (AWS)**: Request public certificates; deploy to CloudFront, ALB, API Gateway; automatic renewal
- **Azure Key Vault + App Gateway**: Automatic certificate renewal and deployment
- **GCP Certificate Manager**: Google-managed certificates auto-provisioned for Cloud Load Balancer, Cloud CDN

---

## 19. Cloud Security Automation

### 19.1 Automated Security Response (SOAR)

**Definition**: Security Orchestration, Automation, and Response — connecting security tools and automating response workflows.

**Cloud-Native SOAR Capabilities**:
- **AWS**:
  - EventBridge → Lambda/SNS → Automated response
  - GuardDuty → EventBridge → Lambda (e.g., isolate instance, disable access key)
  - Security Hub → Custom Actions → Systems Manager Automation
  - Config → EventBridge → Auto-remediation Lambda
- **Azure**:
  - Microsoft Sentinel SOAR (Playbooks via Logic Apps)
  - Automate incident response with 200+ connectors
  - Azure Policy auto-remediation (DeployIfNotExists, Modify)
- **GCP**:
  - Chronicle SOAR (Security Automation)
  - Cloud Functions triggered by SCC findings
  - Cloud Asset Inventory → Forseti/IAM Recommender auto-remediation

**Common Automated Response Actions**:

| Trigger | Automated Action |
|---------|-----------------|
| GuardDuty: UnauthorizedAccess:IAM/User | Disable access keys, detach IAM policies, send alert to Slack/PagerDuty |
| GuardDuty: CryptoCurrency:EC2/BitcoinTool.B | Quarantine instance (remove from target group, update SG to deny all, snapshot EBS) |
| Security Hub: S3 bucket public | Apply S3 Block Public Access; notify data owner |
| Config: Security group too permissive | Revoke ingress rule (automatically or via approval workflow) |
| GuardDuty: Recon:EC2/PortProbe | Update NACL to block source IP; enable VPC Flow Logs |
| Sentinel: User from Anonymous IP accessing sensitive data | Trigger MFA re-authentication; block user session |

**SOAR Playbook Example (AWS — Quarantine Compromised EC2)**:

```json
{
  "Trigger": "GuardDuty finding CryptoCurrency:EC2/BitcoinTool.B",
  "Actions": [
    { "Action": "Add tag", "Tag": "Compromised: true" },
    { "Action": "Detach instance from ASG", "SetDesiredCapacity: 0" },
    { "Action": "Update SG", "Revoke all inbound rules", "Add quarantine rule" },
    { "Action": "Create EBS snapshot", "Snapshot all volumes" },
    { "Action": "Notification", "Send to security team with instance details" },
    { "Action": "Create CloudWatch event", "Monitor instance for outbound traffic" }
  ],
  "User Approval": "Required before termination"
}
```

### 19.2 Policy as Code

**Definition**: Managing and enforcing security policies through code, integrated with CI/CD and IaC pipelines.

**Tools**:

| Tool | Language | Target | Integration |
|------|----------|--------|-------------|
| **Open Policy Agent (OPA)** / Rego | Rego | Any (K8s, Terraform, Cloud APIs) | CI/CD, admission controllers, API gateways |
| **Hashicorp Sentinel** | Sentinel | HashiCorp products (Terraform, Vault, Consul, Nomad) | Terraform Cloud, Enterprise |
| **AWS CloudFormation Guard** | Guard DSL | CloudFormation, Terraform, K8s | CLI, CI/CD pipeline |
| **Azure Policy as Code** | JSON/PowerShell/Bicep | Azure resources | Azure DevOps, GitHub Actions |
| **GCP Org Policies** | YAML/CLI | GCP resources | Cloud Build, Deployment Manager |
| **Kyverno** | YAML | Kubernetes | Admission controller (Kubernetes-native) |
| **jsPolicy** | JavaScript | Kubernetes | Admission controller |

**OPA Policy Example**:

```rego
# Require S3 bucket encryption
package terraform.s3

deny[msg] {
  resource := input.resources[name]
  resource.type == "aws_s3_bucket"
  not resource.config.server_side_encryption_configuration
  msg := sprintf("Bucket %v must have encryption enabled", [name])
}

# Require security group to block SSH from 0.0.0.0/0
deny[msg] {
  sg := input.resources[name]
  sg.type == "aws_security_group"
  rule := sg.config.ingress[_]
  rule.from_port <= 22
  rule.to_port >= 22
  rule.cidr_blocks[_] == "0.0.0.0/0"
  msg := sprintf("Security group %v allows SSH from 0.0.0.0/0", [name])
}
```

**Azure Policy Example**:

```json
{
  "if": {
    "field": "type",
    "equals": "Microsoft.Compute/virtualMachines"
  },
  "then": {
    "effect": "deny",
    "details": {
      "field": "Microsoft.Compute/virtualMachines/storageProfile.osDisk.managedDisk.diskEncryptionSet.id",
      "exists": "false"
    }
  }
}
```

### 19.3 CI/CD Security Pipeline

**Security Gates in Pipeline**:

```
Developer Commit
    ↓
[1] Pre-Commit Hooks: secret detection, linter, format check
    ↓
[2] Build: SAST scan, dependency scan, license compliance, SBOM generation
    ↓
[3] Container Build: Image scan, base image vuln scan, sign image (Cosign)
    ↓
[4] Deploy to DEV: IaC scan (Checkov/tfsec), kube-bench scan, config compliance
    ↓
[5] Deploy to STAGING: DAST scan, penetration testing, Fuzzing, Leak testing
    ↓
[6] Deploy to PRODUCTION: WAF rules update, monitoring config, rollback plan verified
```

**CI/CD Security Checklist**:
- [ ] **Code Repository**: Branch protection (require PR, required reviews, status checks); signed commits (GPG); secret scanning enabled (GitHub Advanced Security/GitLab Ultimate)
- [ ] **Build**: Isolated build environments (ephemeral containers); no secrets in build logs; dependency pins (lock files); reproducible builds; signed artifacts
- [ ] **Artifact Storage**: Signed container images (Cosign/Docker Content Trust); vulnerability-scanned before storage; immutable tags; retention policies
- [ ] **Deployment**: Immutable deployments (blue/green, canary); approval gates; deployment windows; automated rollback; change management records
- [ ] **Secrets**: NEVER in code; injected at runtime via Secrets Manager/Key Vault; rotated automatically; access audited

### 19.4 Infrastructure as Code (IaC) Security Automation

**Gauntlt / Security Testing in CI**:
```yaml
# .gitlab-ci.yml example
security-stage:
  stage: security
  script:
    - checkov -d terraform/ --framework terraform --quiet
    - tfsec terraform/ --no-colour
    - trivy config terraform/
    - trivy image myregistry.com/app:latest --severity CRITICAL,HIGH
    - snyk test --severity-threshold=high
    - curl -sL https://github.com/aquasecurity/kube-bench/releases/latest | kube-bench run --targets master,node
```

**Terraform Sentinel Policy Example**:
```sentinel
import "tfplan/v2" as tfplan

# Ensure all S3 buckets have encryption enabled
all_s3_encrypted = rule {
    all tfplan.resource_changes as _, rc {
        rc.type is "aws_s3_bucket" implies
            rc.change.after.server_side_encryption_configuration is not null
    }
}

# Ensure no security group allows SSH from anywhere
no_public_ssh = rule {
    all tfplan.resource_changes as _, rc {
        rc.type is "aws_security_group" implies
            not is_public_ssh(rc.change.after)
    }
}

main = rule {
    all_s3_encrypted and no_public_ssh
}
```

### 19.5 Automated Compliance Validation

**Continuous Compliance Monitoring**:
- **AWS Config**: 300+ managed rules (encrypted volumes, public access checks, security group rules); custom Lambda rules for bespoke checks
- **Azure Policy**: Built-in policy definitions (500+); custom policies; initiative definitions grouping policies; compliance dashboard
- **GCP Org Policies**: Organization-wide constraints; project-level overrides; continuous compliance evaluation
- **Automated Remediation**: AWS Config auto-remediation (SSM Automation); Azure Policy DeployIfNotExists/Modify effects; GCP Forseti auto-remediation

**Compliance as Code Pipeline**:
```
IaC Template → Compliance Policy Scan → Audit Evidence Generation → Report
       ↓                ↓                         ↓
   CheckOV/tfsec   Sentinel/OPA/Azure Policy   CloudTrail/Config    Security Hub/Dashboard
```

---

## 20. Cloud Security for Specific Industries

### 20.1 Healthcare (HIPAA/HITECH)

**HIPAA Rules**:
- **Privacy Rule**: Protects PHI; patient rights (access, amendment, accounting of disclosures)
- **Security Rule**: Administrative, physical, technical safeguards for ePHI
- **Breach Notification Rule**: Notification within 60 days; >500 individuals → HHS + media
- **Enforcement Rule**: Penalties up to $1.5M per violation category per year

**Cloud HIPAA Requirements**:
- **BAA (Business Associate Agreement)** with cloud provider
- **Encryption**: AES-256 for ePHI at rest; TLS 1.2+ for ePHI in transit
- **Access Controls**: Role-based access, unique user IDs, automatic logoff, emergency access procedure
- **Audit Controls**: Record/Examine all PHI access (CloudTrail, Config, VPC Flow Logs)
- **Integrity Controls**: Mechanism to authenticate ePHI (hashing, digital signatures)
- **Transmission Security**: Encrypted channels only

**HIPAA-Compliant AWS Architecture**:
```
WAF/Shield → ELB (TLS) → EC2 Auto Scaling (Private, encrypted EBS) → RDS (encrypted, Multi-AZ)
                    ↓                                              ↓
              CloudWatch (audit logs)                     KMS (PHI encryption keys)
                    ↓                                              ↓
              CloudTrail (encrypted S3, Object Lock)        VPC (isolated, No Public Access)
```

### 20.2 Financial Services (PCI-DSS, SOX, FFIEC)

**PCI-DSS v4.0 Requirements** (12 requirements, 6 goals):

| Goal | Requirements |
|------|-------------|
| **Build/Maintain Secure Network** | 1. Firewall configuration; 2. No default vendor passwords |
| **Protect Cardholder Data** | 3. Protect stored data (encryption, truncation, hashing, tokenization); 4. Encrypt transmission (TLS/HTTPS) |
| **Maintain Vulnerability Program** | 5. Use/update anti-malware; 6. Develop/maintain secure systems (patching) |
| **Implement Strong Access Control** | 7. Need-to-know access; 8. Unique IDs (+ MFA); 9. Restrict physical access |
| **Regularly Monitor/Test** | 10. Track/monitor all access to cardholder data; 11. Regular testing (ASV scan quarterly, penetration testing annually) |
| **Maintain Security Policy** | 12. Maintain information security policy |

**PCI-DSS in Cloud**:
- **CDE (Cardholder Data Environment)**: Isolated VPC/VNet with restricted access
- **Cloud Provider**: Must be PCI-DSS Level 1 validated (AWS, Azure, GCP)
- **SAQ (Self-Assessment Questionnaire)**: Determine which SAQ applies (A, A-EP, B, B-IP, C-VT, C, P2PE, D)
- **ASV (Approved Scanning Vendor)**: Quarterly external vulnerability scans of public-facing IPs
- **Penetration Testing**: Annual penetration testing on CDE; cloud provider permission required (AWS allows self-service, Azure allows, GCP allows)
- **Tokenization**: Replace PAN with tokens (reduce PCI scope); vault tokenization or cloud-native (AWS Tokenization)

**SOX Compliance**:
- **ITGC (IT General Controls)**: Access management, change management, computer operations, program development
- **Cloud Considerations**: Provider SOC 1 Type II report; segregate duties; audit trails; data integrity

**FFIEC (Financial Institutions)**:
- **Cloud Risk Assessment**: Due diligence, vendor management, concentration risk
- **Data Protection**: Encryption standards, key management, data sovereignty
- **Resilience**: Business continuity planning, DR testing, vendor contingency
- **Exams**: FFIEC examination handbooks for outsourced cloud services

### 20.3 Government / Public Sector (FedRAMP, IL4/5)

**FedRAMP Levels**:
| Impact Level | Data Type | Authorization Requirements |
|-------------|-----------|--------------------------|
| **Low** | Low sensitivity | Self-assessment; annual review |
| **Moderate** | Moderate sensitivity | Third-party assessment (3PAO); continuous monitoring; annual review |
| **High** | High sensitivity (law enforcement, health, emergency services) | Full JAB authorization; continuous monitoring; annual review |

**DoD Impact Levels**:
| Level | Description | Requirements |
|-------|-------------|-------------|
| **IL2** | Controlled Unclassified Information (CUI) | FedRAMP Moderate equivalent + NIST 800-171 |
| **IL4** | Controlled Unclassified Information (CUI) requiring CUI Enhanced | IL2 + Security requirements + FedRAMP High baseline |
| **IL5** | Controlled Unclassified Information (CUI) requiring CUI Enhanced with specific controls | IL4 + additional NIST 800-53 controls |
| **IL6** | Classified Information (Secret) | GALE-S classified environments; separate from commercial cloud |

**Government Compliance in Cloud**:
- **AWS GovCloud (US) / C2S**: Dedicated regions; US persons only; FedRAMP High, ITAR, EAR
- **Azure Government**: Physically isolated; US persons only; FedRAMP High, DISA IL5, CJIS, ITAR
- **GCP Assured Workloads**: FedRAMP High, HIPAA, CJIS, ITAR; geographic control; key access control

### 20.4 Education (FERPA)

**FERPA Requirements**:
- **Privacy**: Personally identifiable information (PII) from education records protected
- **Parental/Student Rights**: Right to inspect, amend records; consent for disclosure
- **Cloud Considerations**:
  - Written agreement with cloud provider specifying FERPA compliance
  - Direct control over access; appropriate technical measures
  - Ensure provider does not use data for any unauthorized purpose
  - Data retention and destruction policies
  - Breach notification procedures

---

## 21. Cloud Security Testing

### 21.1 Cloud Penetration Testing

**Methodology Adaptation**:
- **Discovery**: Identify cloud assets (public endpoints, certificates, DNS records, exposed buckets, APIs)
- **Reconnaissance**: Enumerate IAM permissions, VPC configurations, security groups, storage
- **IAM Assessment**: Test for privilege escalation paths (PassRole, CreatePolicyVersion, Trust policy exploitation)
- **Storage Assessment**: Check for public buckets/containers; test bucket policy bypasses
- **Network Assessment**: Security group rules, NACLs, VPC peering, VPN configurations
- **Application Assessment**: Web/API vulnerabilities (SSRF, IDOR, SQLi, XSS, authentication bypass)
- **Target: Cloud Provider**: OS vulnerabilities, container escape, hypervisor vulnerabilities

**Cloud Provider Penetration Testing Policies**:
- **AWS**: No prior approval needed for 75+ AWS services; prohibited: DNS poisoning, DoS/DDoS, physical security attacks, social engineering; use Penetration Testing Request Form for additional services
- **Azure**: Must notify Microsoft for penetration tests; prohibited: DoS/DDoS, physical security, social engineering; can self-scan with Azure Security Center
- **GCP**: Must follow Acceptable Use Policy; prohibited: DoS, social engineering, unauthorized access attempts on GCP infrastructure

**AWS Pentesting Tools**:
- **ScoutSuite**: Multi-cloud security audit tool (AWS/Azure/GCP)
- **Prowler**: AWS CLI security assessment; 200+ checks (CIS, GDPR, HIPAA, PCI-DSS)
- **Pacu**: AWS exploitation framework; IAM privilege escalation, S3 bucket enumeration, CloudTrail bypass, Lambda persistence
- **CloudSploit**: Open-source CSPM; scans for misconfigurations
- **Bucket Stream**: S3 bucket discovery and analysis
- **CloudBrute**: Multi-cloud enumeration tool

**Azure Pentesting Tools**:
- **AzAdExplorer / ROADtools**: Azure AD enumeration and exploitation
- **Stormspotter**: Azure attack surface mapping
- **MicroBurst**: Azure exploitation framework; storage enumeration, IAM abuse, function app analysis
- **Azurite**: Azure security assessment
- **PowerZure**: Azure security assessment and exploitation

**GCP Pentesting Tools**:
- **GCPBucketBrute**: GCS bucket enumeration
- **GCP-IAM-Exploitation**: Privilege escalation techniques
- **CloudSploit / ScoutSuite**: GCS bucket scanning
- **gcp_firewall_enum**: Firewall rule enumeration

### 21.2 Cloud Vulnerability Scanning

**Types of Cloud Vulnerability Scanning**:

| Scan Type | What It Checks | Frequency | Tools |
|-----------|---------------|-----------|-------|
| **Agent-based OS Scan** | OS packages for known CVEs | Weekly/daily | Amazon Inspector, Qualys, Tenable, Rapid7, CrowdStrike |
| **Agentless Network Scan** | Open ports, services, protocol vulnerabilities | Monthly/quarterly | Qualys, Tenable, Rapid7, Nmap |
| **Container Image Scan** | OS packages + application library CVEs | Every build | Trivy, Clair, Snyk, Amazon ECR, Azure Defender, GCP Artifact Registry |
| **IaC Scan** | Template misconfigurations before deployment | Every commit | Checkov, tfsec, cfn-nag, Terrascan, KICS |
| **Web Application Scan** | OWASP Top 10 vulnerabilities | Quarterly/after major changes | OWASP ZAP, Burp Suite, Acunetix, AWS WAF Security Automations |
| **API Scan** | API vulnerabilities (BOLA, BFLA, mass assignment) | Monthly/after API changes | 42Crunch, Noname, Salt, Apisec |
| **Secrets Scan** | Hardcoded credentials in repos | Every commit | GitLeaks, TruffleHog, Git-secrets, GitHub Secret Scanning |
| **License Scan** | Open-source license compliance | Every build | FOSSA, Snyk, WhiteSource |

### 21.3 Red Teaming in Cloud

**Cloud Red Team Objectives**:
1. **Initial Access**: Phishing → AWS IAM credentials; Exploit web app → SSRF → IMDS credential theft
2. **Privilege Escalation**: Exploit IAM misconfigurations (PassRole on EC2/Lambda, create policy, modify trust policies)
3. **Lateral Movement**: Assume role across accounts; use SSM/Systems Manager for instance access
4. **Persistence**: Lambda backdoor (trigger on CloudTrail events); IAM backdoor user; KMS backdoor (grant); Route53 DNS poisoning
5. **Data Exfiltration**: S3 to cross-account bucket; RDS snapshot sharing; Parameter Store retrieval; VPC endpoint DNS tunneling; compressed encrypted data via DNS/HTTPS

**Cloud Red Team Techniques**:

| Technique | Description | Detection |
|-----------|-------------|-----------|
| **Golden SAML** | Forge SAML tokens using stolen IdP signing key; authenticate as any user | Monitor SAML assertion validation; detect unexpected token issuance; inventory IdP signing keys |
| **STS Token Theft** | Steal temporary STS tokens from EC2 metadata, container env, CI/CD pipeline | GuardDuty UnauthorizedAccess findings; anomalous token usage patterns |
| **CloudTrail Bypass** | Disable/delete CloudTrail trail; modify trail to exclude certain events | CloudTrail MultiRegionTrail creation alert; Config rule for minimum 1 trail; S3 log bucket protection |
| **Lambda Persistence** | Create Lambda function triggered by CloudTrail events (CreateUser, etc.); execute attacker code | Review all Lambda triggers; monitor for unused/new Lambda functions with IAM roles |
| **KMS Backdoor** | Create KMS grant allowing external account to use key; attach grant to key | CloudTrail CreateGrant events; review all KMS grants; restrict who can create grants |
| **Organizational Resource Hijacking** | Create AWS Organizations in compromised account; invite other accounts | GuardDroid; monitor Organization API calls; SCP to restrict Organization actions |
| **DNS Tunneling** | Encode exfiltrated data in DNS queries to attacker-controlled domain | VPC Flow Logs analysis for anomalous DNS traffic patterns; DNS query monitoring |
| **S3 Exfiltration via Presigned URLs** | Generate presigned URLs for sensitive objects; exfiltrate via shared links | S3 server access logs for presigned URL access patterns; CloudTrail PutObject with presigned URL indicators |

### 21.4 Cloud Security Validation Tools

**Comprehensive Security Assessment Tools**:

| Tool | Cloud | Description |
|------|-------|-------------|
| **Prowler** | AWS | 300+ security checks (CIS, GDPR, HIPAA, PCI-DSS, NIST, SOC2); CLI tool; HTML/CSV reports |
| **ScoutSuite** | AWS/Azure/GCP | Multi-cloud security audit; 500+ rules; HTML reports |
| **Pacu** | AWS | AWS exploitation framework; IAM escalation, backdoor, CloudTrail manipulation, persistence |
| **CloudSploit** | AWS/Azure/GCP/GitHub/OCI | Open-source CSPM; 100+ checks; integrates with CI/CD |
| **Forseti Security** | GCP | GCP-specific security tool; inventory, scanning, policy enforcement, remediation |
| **Maestro (Azure)** | Azure | Azure security assessment and testing |
| **Zeus** | AWS | AWS security automation and analysis |
| **Cartography** | Multi-cloud | Infrastructure graph visualization for security analysis; Neo4j database |

### 21.5 Security Chaos Engineering

**Definition**: Proactively testing system resilience by injecting controlled failures/misconfigurations in cloud environments.

**Tools and Approaches**:
- **AWS Fault Injection Simulator (FIS)**: Pre-built fault injection experiments (EC2 stop, RDS failover, ASG termination, EBS pause IO); controlled, monitored, with safety limits
- **Azure Chaos Studio**: Fault injection (VM shutdown, NSG rule changes, Cosmos DB failover, AKS node drain); experiments with safety conditions
- **GCP Chaos Monkey / Simian Army**: Part of Spinnaker; randomly terminates instances to test resilience
- **LitmusChaos (CNCF)**: Kubernetes-native chaos engineering; pod failure, node drain, network latency

**Security Chaos Experiments**:
- Randomly detach IAM policies to test least privilege enforcement
- Modify security group rules to test defense-in-depth
- Disable CloudTrail briefly to test monitoring coverage
- Simulate bucket policy misconfiguration to test automated remediation
- Rotate KMS keys to test key management procedures
- Inject network latency to test DDoS mitigation

---

## 22. Cloud Security Monitoring and Analytics

### 22.1 Cloud Security Metrics and KPIs

| Category | Metric | Formula | Target |
|----------|--------|---------|--------|
| **IAM Hygiene** | % users with MFA enabled | (Users with MFA / Total Users) x 100 | 100% |
| **IAM Hygiene** | Unused IAM roles/users | Count of roles/users not used in 90 days | 0 |
| **IAM Hygiene** | Overly permissive policies | Count of policies with `*` in Action or Resource | 0 |
| **IAM Hygiene** | Root account activity count | Number of root account API calls in 30 days | 0 |
| **Encryption** | % encryption at rest | (Encrypted resources / Total resources) x 100 | 100% |
| **Encryption** | % encryption in transit | (HTTPS/TLS-enabled endpoints / Total) x 100 | 100% |
| **Encryption** | KMS key rotation compliance | (Keys with rotation / Total keys) x 100 | 100% |
| **Network** | Publicly exposed resources | Count of resources with public IP/bucket access | 0 |
| **Network** | Open ports to 0.0.0.0/0 | Count of SGs allowing ingress from anywhere | 0 |
| **Network** | VPC Flow Logs coverage | (VPCs with flow logs / Total VPCs) x 100 | 100% |
| **Logging** | CloudTrail coverage | (Regions with trail / Total regions) x 100 | 100% |
| **Logging** | Audit log retention compliance | (Retention >= 365 days / Total log sources) x 100 | 100% |
| **Monitoring** | Critical alert MTTA/MTTR | Average time to acknowledge/resolve | <30 min / <4 hrs |
| **Monitoring** | % false positive rate | (False positives / Total alerts) x 100 | <10% |
| **Vulnerability** | Critical/High CVEs by severity | Count per severity | 0 critical |
| **Vulnerability** | Mean time to patch (MTTP) | Average time from CVE disclosure to patch | <7 days (critical) |
| **Vulnerability** | Patching compliance | (Patched instances / Total instances) x 100 | 100% |
| **Incident** | Time to detect | Average time from compromise to detection | <1 hour |
| **Incident** | Time to respond | Average detection to containment | <4 hours |
| **Incident** | % cloud-related incidents | (Cloud incidents / Total incidents) x 100 | Monitor |
| **Incident** | Recurring incidents | Count of security events with same root cause | 0 |
| **Compliance** | % control compliance | (Passed controls / Total controls) x 100 | >=95% |
| **Compliance** | Audit findings | Count of audit findings per period | Trend decreasing |

### 22.2 Log Analytics and Threat Hunting

**KQL (Azure) Example — Detect Mass IAM Changes**:
```kusto
// Detect mass IAM policy changes (indicates privilege escalation attempt)
AuditLogs
| where OperationName contains "Add member to role" or OperationName contains "Update policy"
| summarize ChangeCount = count() by bin(TimeGenerated, 1h), UserPrincipalName
| where ChangeCount > 10
```

**CloudWatch Logs Insight (AWS) — Detect Unusual API Calls**:
```
fields @timestamp, @message
| filter eventSource = "iam.amazonaws.com"  
| filter eventName in ["CreateUser", "CreateAccessKey", "AttachUserPolicy", "PutUserPolicy"]
| stats count() as apiCount by eventName, userIdentity.arn, sourceIPAddress
| filter apiCount > 1
| sort @timestamp desc
```

**BigQuery/GCP Logging — Detect Bucket Permission Changes**:
```sql
SELECT
  timestamp, proto_payload.audit_log.authentication_info.principal_email,
  proto_payload.audit_log.method_name,
  proto_payload.audit_log.resource_name,
  proto_payload.audit_log.request
FROM `my-project.audit_logs.cloudaudit_googleapis_com_data_access`
WHERE
  proto_payload.audit_log.method_name LIKE '%SetIamPolicy%'
  AND proto_payload.audit_log.service_name = 'storage.googleapis.com'
ORDER BY timestamp DESC
LIMIT 100
```

**Threat Hunting Queries (AWS)**:

| Hunt | Query |
|------|-------|
| **IAM CreateUser from unusual IP** | `eventName = CreateUser AND sourceIPAddress NOT IN (corporate IP list)` |
| **EC2 instances with public AMI** | `eventName = RunInstances AND imageId NOT IN (approved AMI list)` |
| **S3 bucket made public** | `eventName = PutBucketAcl OR PutBucketPolicy AND bucketName CONTAINS "sensitive"` |
| **CloudTrail deletion attempts** | `eventName = DeleteTrail OR StopLogging OR UpdateTrail` |
| **Unusual cross-account access** | `userIdentity.type = AssumedRole AND sourceIPAddress NOT in VPC range` |
| **Large data exports** | `eventName = CopyObject OR GetObject AND bytesTransferred > 100MB` |
| **Hour of day anomalies** | API calls between 12AM-5AM from known users |
| **Console login without MFA** | `eventName = ConsoleLogin AND additionalEventData.MFAUsed != Yes` |

### 22.3 Cloud Security Benchmarking

**Cloud Benchmarks**:
| Benchmark | Coverage | Provider Support |
|-----------|----------|-----------------|
| **CIS AWS Foundations Benchmark** | 150+ controls (IAM, logging, monitoring, networking) | AWS Security Hub, Prowler, AWS Config |
| **CIS Azure Foundations Benchmark** | 150+ controls (IAM, security center, storage, networking, logging) | Azure Defender for Cloud, Azure Policy, ScoutSuite |
| **CIS GCP Foundations Benchmark** | 100+ controls (IAM, logging, networking, storage) | SCC, Forseti, ScoutSuite |
| **CIS Kubernetes Benchmark** | 100+ controls (master/node/etcd/policies) | kube-bench, kube-hunter, Defender for Containers, EKS Best Practices |
| **CIS Docker Benchmark** | 100+ controls (host/daemon/images/containers) | docker-bench-security, Trivy |
| **PCI-DSS Report on Compliance** | 12 requirements across CDE | ASV quarterly scans, SAQ, ROC |
| **SOC 2 Type II** | Trust Services Criteria (Security, Availability, Processing Integrity, Confidentiality, Privacy) | External auditor annually |

**Automating Benchmark Validation**:

```bash
# AWS — Run Prowler for CIS benchmark
prowler -b -g cis_1.1 -r us-east-1 -M html,csv,json

# K8s — Run kube-bench
kube-bench run --targets master,node --version 1.28

# Docker — Run docker-bench-security
docker run --pid host -v /var/run/docker.sock:/var/run/docker.sock docker-bench-security

# Checkov (IaC)
checkov -d . --framework terraform,cloudformation,kubernetes --quiet --output junitxml
```

### 22.4 Cloud Security Dashboard Design

**AWS Security Dashboard Layout**:
```
┌───────────────────────────────────────────────────────────┐
│  🟢 Security Score: 85% │ Critical Alerts: 2 │ Open Findings: 47 │
├────────────────┬────────────────┬─────────────────────────┤
│  GuardDuty      │  Security Hub  │  Compliance (Config)     │
│  • High: 2      │  • Critical: 5 │  • Non-compliant: 12    │
│  • Medium: 7    │  • High: 12    │  • CIS passes: 142/150  │
│  • Low: 23      │  • Failed: 30  │  • NIST passes: 180/200 │
│  [Trend: ▼ 15%] │  [Top: S3 pub]│  [Auto-remediate: ON]   │
├────────────────┴────────────────┴─────────────────────────┤
│  IAM                     │  Network              │  Compute  │
│  • Root activity: 0      │  • Open ports: 3       │  • Vulns: 19  │
│  • MFA compliance: 98%   │  • Flow logs: 95%     │  • Patched: 92%│
│  • Unused keys: 5        │  • WAF blocked: 1.2k  │  • OS: Win/Linux│
├───────────────────────────────────────────────────────────┤
│  Recent Activity (CloudTrail)                              │
│  • 09:42 | JohnD | s3:PutBucketPolicy | bucket-prod-data  │
│  • 09:15 | AutoScale | ec2:TerminateInstances | i-0abc123  │
└───────────────────────────────────────────────────────────┘
```

**Key Dashboard Widgets**:
- **Security Score / Secure Score** (aggregate from Security Hub, Defender for Cloud, SCC)
- **Alert Triage Queue** (GuardDuty/Defender/SCC findings with severity, status, age)
- **Compliance Posture** (% compliant per framework; top non-compliant controls)
- **IAM Health** (MFA %, unused entities, root activity, recent policy changes)
- **Network Exposure** (open ports, public resources, WAF blocks, DDoS events)
- **Vulnerabilities** (critical/high CVEs by resource type; MTTP trend)
- **Incident Timeline** (recent incidents with detection/response times)
- **Change Activity** (recent CloudTrail events; config changes; IaC drift)

---

## 23. Cloud Security Economics

### 23.1 Cost of Cloud Breach

**Cost Components (IBM 2024 Cost of Data Breach Report)**:
| Component | Average Cost |
|-----------|-------------|
| **Detection and Escalation** | $1.58M |
| **Post-Breach Response** | $1.08M |
| **Notification** | $0.89M |
| **Lost Business** | $1.45M |
| **Total Average** | $4.88M per breach |

**Cloud-Specific Cost Factors**:
- **Data Egress Fees**: Exfiltrating large datasets incurs provider charges (AWS: $0.09/GB first 10TB; Azure: $0.087/GB; GCP: $0.12/GB)
- **Forensic Investigation**: Cloud forensics requires specialized expertise; need to preserve/log API-level activity
- **Regulatory Fines**: GDPR up to 4% annual global revenue; PCI-DSS $5K-$100K/month; HIPAA up to $1.5M/year
- **Legal Costs**: Class-action lawsuits, contractual penalties, shareholder lawsuits
- **Remediation Costs**: Instance rebuilding, credential rotation, security improvements, architecture changes

### 23.2 Cloud Security ROI

**Cost Avoidance Metrics**:
- **Prevented breaches** x Average cost per breach = Avoided loss
- **Reduced incident response time** x Hourly incident cost = Savings
- **Automated compliance** vs Manual audit hours = Labor savings
- **Reduced alert fatigue** via improved detection = Security team efficiency

**Security Investment Categories**:

| Investment | Typical Annual Cost | ROI Justification |
|------------|-------------------|-------------------|
| **IAM + MFA** | $0 (provider included) / per-user MFA token ~$20 | Prevents 80%+ of credential-based breaches |
| **CloudTrail/Logging** | S3 storage costs ~$50-$500/mo per account | Required for incident investigation; compliance mandate |
| **GuardDuty/Defender/SCC** | ~$1-5 per GB of CloudTrail logs; per-instance | Detects threats in minutes vs days; median reduction: 60% detection time |
| **CSPM (Wiz/Prisma)** | ~$10-50 per resource per year | Continuous misconfiguration detection; prevents 80%+ of common cloud attacks |
| **Vulnerability Scanning** | Per-asset pricing; ~$5-50/instance/year | Reduces exploitable vulnerabilities; compliance requirement |
| **SIEM (Splunk/Sentinel)** | Per-GB ingested; $10-100+ per GB/month | Centralized security visibility; correlation across logs; incident investigation |
| **Security Training** | Per-user; $50-500/user/year | Reduces phishing success rate; security awareness; compliance requirement |

### 23.3 Cost Optimization for Cloud Security

**Strategies to Reduce Security Costs**:
1. **Use native security tools first** (GuardDuty, Security Hub, Defender, SCC) — often free tier or included in existing subscription
2. **Consolidate tools** — Avoid overlapping CSPM + CWPP + CIEM (use integrated platforms like Wiz, Prisma, Lacework)
3. **Automate compliance** — Reduce manual audit prep hours by 70%+ with continuous compliance monitoring
4. **Reduce alert noise** — Tune detection rules; reduce false positives; focus on actionable alerts
5. **Right-size log retention** — Hot storage for 30 days; cool/cold storage for 1+ year; archive after compliance requirement met
6. **Tagging for cost allocation** — Track security spending per environment, team, project
7. **Use Savings Plans / Reserved Instances for security VMs** — Consistent workloads qualify for discounts
8. **Benchmark and optimize** — Regular security tooling reviews; remove unused licenses; consolidate vendors

---

## 24. Cloud Security Awareness and Training

### 24.1 Cloud Security Roles and Responsibilities

| Role | Cloud Security Responsibilities |
|------|-------------------------------|
| **CISO** | Overall cloud security strategy; risk acceptance; budget; executive reporting |
| **Cloud Security Architect** | Design security architecture; evaluate new services; define security patterns; threat modeling |
| **Cloud Security Engineer** | Implement security controls; configure tools (GuardDuty, WAF, IAM); automate security responses |
| **DevSecOps Engineer** | Integrate security into CI/CD; IaC scanning; pipeline security gates; container security |
| **Cloud Administrator** | Configure IAM; manage access; maintain compliance; respond to operational security alerts |
| **Compliance Officer** | Ensure regulatory compliance; audit evidence collection; risk assessment; vendor due diligence |
| **Application Developer** | Secure coding; dependency management; application-level access control; secrets management |
| **Data Steward** | Data classification; data lifecycle management; data access reviews; retention/destruction |
| **Incident Responder** | Cloud incident handling; forensics; containment; recovery; lessons learned |
| **Security Analyst** | Monitor alerts; triage findings; threat hunting; SIEM management |

### 24.2 Cloud Security Training Topics

**Developer Security Training**:
1. **IAM Best Practices**: Least privilege, role-based access, policies, conditions; common IAM pitfalls
2. **Secure Coding**: OWASP Top 10 for cloud; input validation; API security; secrets management
3. **Container Security**: Image scanning, minimal base images, non-root user, read-only filesystem, security context
4. **Infrastructure as Code Security**: IaC scanning, secret detection, policy as code, immutability
5. **CI/CD Pipeline Security**: Security gates, artifact signing, dependency scanning, build integrity
6. **Data Protection**: Encryption at rest/transit, key management, data classification, retention policies
7. **Incident Response**: Identify security events, containment procedures, reporting process

**Administrator Training Topics**:
1. **IAM Deep Dive**: Policy creation, validation, federation, SSO, ABAC; privilege escalation risks
2. **Network Segmentation**: VPC design, security groups, NACLs, VPC endpoints, Transit Gateway
3. **Logging and Monitoring**: CloudTrail, flow logs, SIEM integration, alert configuration
4. **Incident Response**: Isolation techniques, evidence collection, access key revocation, forensic procedures
5. **Compliance**: Audit preparation, evidence collection, inherited vs customer-managed controls
6. **Cost Management**: Resource cleanup, cost anomaly detection, tagging, budgeting
7. **Change Management**: Approval processes, automation, IaC validation, deployment strategies

### 24.3 Phishing and Social Engineering in Cloud

**Cloud-Specific Social Engineering**:
- **Credential Harvesting**: Fake login pages mimicking AWS Console, Azure Portal, GCP Console, Okta, Office 365
- **MFA Fatigue**: Repeated push notification spamming until user approves; attacker then uses stolen session token
- **Cloud Support Impersonation**: Attacker poses as cloud provider support; requests access keys, account details
- **S3 URI Phishing**: Links to legitimate S3-hosted phishing pages (bucket hosting)
- **Shared Link Abuse**: Attackers send Cloud/SharePoint/Drive links containing malware embedded in legitimate cloud storage
- **API Key Harvesting via Fake Tools**: Fake SDK tools, CLI wrappers that steal credentials

**Phishing Prevention**:
- **Security Keys (FIDO2)**: Resistant to phishing; U2F tokens for all privileged users
- **Conditional Access Policies**: Block sign-ins from untrusted locations, devices, risk levels
- **Passwordless Authentication**: Windows Hello, FIDO2, Microsoft Authenticator
- **Security Training**: Simulated phishing campaigns; current threat awareness
- **Browser Isolation**: Remote browser isolation for risky sites
- **DMARC/DKIM/SPF**: Email authentication to prevent domain spoofing

---

## 25. Container and Kubernetes Security

### 25.1 Container Security Lifecycle

```
Build → Ship → Run → Runtime
```

| Phase | Security Activities | Tools |
|-------|-------------------|-------|
| **Build** | Base image selection (minimal, signed, trusted); dependency scan; SAST for Dockerfile; secrets scanning | Trivy, Snyk, Docker Scout, Hadolint, GitLeaks |
| **Ship** | Image signing (Cosign/Docker Content Trust); vulnerability scan; SBOM generation; registry access control | Cosign, Notary, Harbor, Amazon ECR, Azure ACR, GCP Artifact Registry |
| **Run** | Pod security standards; seccomp/apparmor profiles; read-only root FS; run as non-root; security context | OPA/Gatekeeper, Kyverno, Pod Security Admission, kube-bench |
| **Runtime** | Behavioral monitoring; unusual process/network/file detection; container escape prevention | Falco, Sysdig, Aqua, Twistlock, CrowdStrike, SentinelOne |

### 25.2 Dockerfile Security Best Practices

```dockerfile
# BAD — Large base image, root user, secrets in layer, unchecked packages
FROM ubuntu:latest
RUN apt-get update && apt-get install -y curl
COPY credentials.json /app/
USER root
EXPOSE 80 22 443
CMD ["python", "app.py"]

# GOOD — Minimal, non-root, multi-stage, no secrets, pinned versions
FROM python:3.11-slim AS builder
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
RUN addgroup --system app && adduser --system --ingroup app app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --chown=app:app app/ /app/
USER app
WORKDIR /app
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health
ENTRYPOINT ["python"]
CMD ["app.py"]
```

**Dockerfile Security Rules**:
- **Pin base image tags** (`python:3.11-slim`, NOT `python:latest` or `python`)
- **Use distroless or slim images** — reduces attack surface by 80%+; no shell, no package manager
- **Multi-stage builds** — Build tools in builder stage; only runtime artifacts in final image
- **Run as non-root** — `USER appuser`; never run containers as root
- **Read-only root filesystem** — `--read-only` flag or security context
- **No secrets in image layers** — Use build args, Docker secrets, or mount at runtime
- **Health check** — Define `HEALTHCHECK` instruction
- **No unnecessary packages** — Minimal attack surface; remove curl, wget, netcat, compilers, debug tools
- **Drop Linux capabilities** — `--cap-drop=ALL --cap-add=NET_BIND_SERVICE`
- **Use seccomp/apparmor** — Restrict syscalls; Docker default seccomp profile

### 25.3 Kubernetes Security Architecture

**K8s Attack Surface**:
```
API Server → etcd → Kubelet → kube-proxy → Container Runtime → Pods
```

| Component | Risk | Mitigation |
|-----------|------|------------|
| **API Server** | Unauthenticated access; privilege escalation; data exposure | Enable RBAC; audit logging; webhook token auth; OIDC integration; restrict access via network policies; API server flags (--anonymous-auth=false, --enable-admission-plugins=...) |
| **etcd** | All cluster data accessible; encryption bypass | Encryption at rest; TLS for etcd peer/client; restrict access to API server only; etcd in private network; firewall rules |
| **Kubelet** | Unauthenticated access to pod operations | Kubelet authentication/authorization enabled; disable anonymous access; certificate-based authentication |
| **kube-proxy** | Network policy bypass | Minimal iptables/IPVS rules; restrict kube-proxy permissions |
| **Container Runtime** | Container escape; host compromise | Seccomp, AppArmor, SELinux; drop capabilities; run as non-root; read-only root filesystem |
| **CRI-O / containerd** | Runtime vulnerabilities | Keep updated; use minimal runtime; restrict runtime access |

**K8s Security Controls**:

| Control | Implementation | Description |
|---------|---------------|-------------|
| **RBAC** | Role/ClusterRole + RoleBinding/ClusterRoleBinding | Define who can access what API resources; least privilege; system:masters group is dangerous |
| **Pod Security Standards** | PodSecurity Admission (v1.23+) | Privileged, Baseline, Restricted profiles; labels per namespace |
| **Network Policies** | NetworkPolicy resources | Restrict pod-to-pod communication; default-deny ingress/egress; allow specific CIDR/port/protocol |
| **OPA/Gatekeeper** | Admission controller webhook | Enforce custom policies (rego); label requirements; registry restrictions; resource limits |
| **Kyverno** | Admission controller (Kubernetes-native) | Validate/mutate/generate resources; policy sets per namespace or cluster |
| **Service Mesh (Istio)** | Sidecar injection; mTLS; authorization policies | mTLS enforced for all pod communication; fine-grained access policies |
| **Secrets Management** | External secrets (Vault, AWS Secrets Manager, Azure Key Vault, GCP Secret Manager) | Avoid native K8s Secrets (base64 encoded); use external secrets operator or CSI driver |
| **Pod Security Context** | securityContext in pod/deployment spec | runAsNonRoot, runAsUser, readOnlyRootFilesystem, capabilities, seccompProfile |

**Kubernetes RBAC Example**:
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { namespace: production, name: pod-reader }
rules:
- apiGroups: [""]
  resources: ["pods", "pods/log"]
  verbs: ["get", "watch", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { namespace: production, name: read-pods }
subjects:
- kind: User
  name: "jane@example.com"
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
```

**Network Policy Example**:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: api-deny-all
spec:
  podSelector:
    matchLabels:
      app: api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          app: frontend
    ports:
    - protocol: TCP
      port: 8080
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: database
    ports:
    - protocol: TCP
      port: 5432
```

### 25.4 Cloud-Native Container Registries Security

| Registry | Features | Security Controls |
|----------|----------|-------------------|
| **Amazon ECR** | Private/public registries; replication across regions | Image scanning (Basic/Enhanced Inspector); IAM permissions; lifecycle policies; KMS encryption; repository policies for cross-account |
| **Azure ACR** | Private registries; geo-replication; tasks | Defender for Containers scanning; RBAC; firewall/VNet integration; content trust (Docker Content Trust); AcrEncryption (customer-managed keys) |
| **GCP Artifact Registry** | Private/public; multi-format (Docker, Maven, npm, pip, apt) | CMEK encryption; IAM permissions; vulnerability scanning; VPC Service Controls; retention policies |
| **Harbor** | Open-source; cloud-agnostic | Vulnerability scanning (Trivy/Clair); RBAC; image replication; immutable tags; content trust; robotic accounts; audit logging |

### 25.5 Kubernetes Incident Response

**K8s Forensic Evidence Collection**:
```bash
# Collect pod logs
kubectl logs <pod-name> -n <namespace> --all-containers --tail=1000 > pod-logs.txt

# Describe pod (events, state, labels, annotations)
kubectl describe pod <pod-name> -n <namespace> > pod-describe.txt

# Collect pod definition (spec, status, metadata)
kubectl get pod <pod-name> -n <namespace> -o yaml > pod-definition.yaml

# Capture container filesystem (requires ephemeral container or debug pod)
kubectl debug -it <pod-name> -n <namespace> --image=ubuntu --copy-to=<debug-pod> -- /bin/bash

# Check RBAC bindings for user
kubectl get rolebindings,clusterrolebindings --all-namespaces | grep <user-email>

# Check NetworkPolicy coverage
kubectl get networkpolicies --all-namespaces

# Check events
kubectl get events --all-namespaces --sort-by='.lastTimestamp'

# Capture API audit logs (if sent to SIEM)
```

---

## 26. Serverless Security

### 26.1 Serverless Attack Surface

| Component | Risk | Mitigation |
|-----------|------|------------|
| **Function Code** | Vulnerabilities in function logic; dependency vulnerabilities | SAST/DAST scanning; dependency scanning; minimal dependencies; code review |
| **Function IAM Role** | Overly permissive execution role; privilege escalation | Least-privilege IAM role per function; resource-based conditions; no wildcard permissions |
| **Event Sources** | Event injection; malicious payloads; denial of wallet | Input validation; schema validation; rate limiting; reserved concurrency |
| **Environment Variables** | Secrets in env vars (can be viewed in console/API) | Use Secrets Manager / Parameter Store; encrypt env vars with KMS; never hardcode secrets |
| **Third-Party Libraries/Layers** | Vulnerable or malicious packages | Dependency scanning (Snyk, Trivy); lock files; layer signing; minimal base layers |
| **API Gateway** | Injection attacks; auth bypass; rate limiting bypass | WAF integration; request validation; auth (Cognito, Lambda authorizer, IAM); throttling |
| **Logs** | Sensitive data in logs | Log sanitization; never log PII/credentials; CloudWatch log encryption |
| **Function URL** | Publicly accessible function without auth | Require IAM auth; use API Gateway instead; Cognito/Auth0 for public APIs |

### 26.2 AWS Lambda Security

**Lambda Execution Role Example (Least Privilege)**:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:us-east-1:123456789012:log-group:/aws/lambda/my-function:*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:123456789012:table/my-table"
    },
    {
      "Effect": "Allow",
      "Action": "kms:Decrypt",
      "Resource": "arn:aws:kms:us-east-1:123456789012:key/my-key",
      "Condition": {
        "ForAnyValue:StringEquals": {
          "kms:EncryptionContext:service": "secretsmanager"
        }
      }
    }
  ]
}
```

**Security Controls**:
- **Reserved concurrency**: Prevent denial of wallet (unexpected high invocations); limit per function
- **Lambda in VPC**: Access private resources; configure security groups; no internet access (use VPC endpoints for AWS services)
- **Lambda@Edge**: Minimize code size (reduced attack surface); validate all CloudFront headers; don't process sensitive data at edge
- **Function URL**: Use AWS_IAM auth type; or use Cognito/OAuth for public endpoints; enable CORS cautiously
- **Function Policy**: Restrict who can invoke the function; use source ARN conditions; invoke-only when needed
- **Dead Letter Queue (DLQ)**: Failed invocations sent to SQS/SNS; monitor DLQ for errors
- **Tracing**: Enable X-Ray tracing for visibility; but don't trace sensitive data

**Lambda Security Checklist**:
- [ ] Least-privilege execution role (one role per function, no shared roles)
- [ ] No wildcard permissions in execution role
- [ ] Environment variables encrypted with KMS (at-rest encryption)
- [ ] Secrets in Secrets Manager / Parameter Store, not env vars
- [ ] Input validation on ALL event sources (API Gateway, SQS, SNS, DynamoDB Streams)
- [ ] Reserved concurrency set to avoid cost explosion
- [ ] Lambda in VPC for private resources; VPC endpoints for AWS services
- [ ] Function URL disabled or authenticated (AWS_IAM/Cognito)
- [ ] Dependencies scanned (Snyk/Trivy) before deployment
- [ ] CloudWatch Logs encrypted with KMS
- [ ] X-Ray tracing enabled (without sensitive data capture)
- [ ] DLQ configured for failed invocations

### 26.3 Azure Functions Security

**Security Controls**:
- **Authentication**: EasyAuth (built-in auth with Azure AD, Google, Facebook, Twitter, Microsoft Account); enable EasyAuth for all HTTP functions
- **Authorization**: Function-level keys (host key, function key); require key for HTTP triggers; Azure AD authentication
- **Managed Identity**: Use system-assigned or user-assigned managed identity instead of connection strings
- **Network Isolation**: VNet integration for function access to private resources; service endpoints or Private Link
- **App Settings Encryption**: Encrypt app settings at rest; use Key Vault references (`@Microsoft.KeyVault(SecretUri=...)`)
- **Always On**: Keep function warm (avoid cold start delays); applicable for premium/app service plan
- **IP Restrictions**: Restrict inbound traffic by IP whitelist (Access Restrictions)

### 26.4 Google Cloud Functions Security

**Security Controls**:
- **Authentication**: Cloud IAM on function invocation (allUsers, allAuthenticatedUsers, specific users/service accounts)
- **Ingress Settings**: Allow all, allow internal only, or allow internal and Cloud Load Balancing
- **VPC Connector**: Connect to VPC for private resource access (Serverless VPC Access)
- **Secrets**: Cloud Secret Manager integration; mount secrets as volumes or environment variables
- **Environment Variables**: Encrypted at rest automatically; don't store secrets (use Secret Manager)
- **Service Account**: Per-function service account with least privilege; avoid default compute engine SA

---

## 27. Cloud Security for DevOps and Agile

### 27.1 Security in Agile/Scrum

**Security Activities Per Sprint Phase**:

| Sprint Phase | Security Activities | Duration | Owner |
|-------------|-------------------|----------|-------|
| **Backlog Grooming** | Identify security user stories; threat model high-risk features; prioritize security debt | 30-60 min | PO + Security Champion |
| **Sprint Planning** | Estimate security stories; allocate capacity for security work; identify security acceptance criteria | Part of planning | Team + Security |
| **Development** | Secure coding practices; commit-time SAST scan; dependency scan; pre-commit hooks | Throughout sprint | Developers |
| **Code Review** | Security-focused code review; check for OWASP Top 10; verify IAM least privilege | Per PR | Developers |
| **Testing** | DAST scan; dependency vulnerability validation; IaC scanning; security regression tests | During testing | QA + DevSecOps |
| **Sprint Review** | Demonstrate security features; review security metrics; update risk register | End of sprint | Team + Stakeholders |
| **Sprint Retro** | Review security incidents from sprint; identify security process improvements; update definition of done | End of sprint | Team |

**Security Definition of Done**:
- [ ] All SAST/DAST findings at severity >= HIGH resolved or accepted
- [ ] No secrets committed (verified by secret scanner)
- [ ] All IaC validated by security policies (Checkov/tfsec passed)
- [ ] Dependencies scanned with no CRITICAL vulnerabilities
- [ ] Code reviewed with security checklist applied
- [ ] Least privilege IAM policy verified
- [ ] Data classification and handling requirements met
- [ ] Logging and monitoring configured
- [ ] Authentication and authorization validated
- [ ] Encryption at rest/transit verified

### 27.2 DevSecOps Maturity Model

| Level | Name | Characteristics |
|-------|------|-----------------|
| **0** | **No Security** | No security tools; no security testing; manual deployments; no IAM policies; credentials in code |
| **1** | **Initial** | Occasional vulnerability scans; perimeter firewalls only; no security in CI/CD; shared admin passwords |
| **2** | **Defined** | Security requirements documented; SAST in CI; basic IAM; security awareness training; incident response process |
| **3** | **Integrated** | SAST + DAST + dependency scanning in pipeline; IaC security scanning; runtime monitoring; automated compliance checks; threat modeling for new features |
| **4** | **Automated** | Automated security gates in CI/CD; policy as code (OPA/Sentinel); auto-remediation of misconfigurations; continuous compliance monitoring; SBOM generation |
| **5** | **Continuous** | Security chaos engineering; automated threat modeling; AI-driven anomaly detection; real-time risk scoring; self-healing security controls; zero-touch deployments |

### 27.3 Shift-Left Security

**Shift-Left Practices**:
1. **Pre-commit hooks**: Scan for secrets, lint IaC, check for malicious patterns before commit
2. **Developer security training**: OWASP Top 10, cloud IAM, secure coding, container security
3. **Secure coding templates**: Pre-approved libraries, frameworks, IaC modules with security baked in
4. **IDE plugins**: Snyk, SonarLint, GitLeaks, Checkov plugins for VS Code, IntelliJ
5. **Local scanning**: Run SAST/SCA scans locally before pushing to CI
6. **Security acceptance criteria**: Written before development starts

**Shift-Left ROI**:
```
Cost to fix vulnerability:
  Design:     $1X
  Dev:        $6X
  Test:       $15X
  Staging:    $40X
  Production: $100-500X
```

---

## 28. Cloud Security Compliance Deep Dive

### 28.1 GDPR Specific Cloud Controls

**Data Processing Requirements**:
- **Data Processing Agreement (DPA)** with cloud provider; covers data processing scope, purpose, duration, data subject rights
- **Data Protection Impact Assessment (DPIA)** for high-risk processing
- **Data Protection Officer (DPO)** appointment if required
- **Records of Processing Activities (ROPA)** maintained

**Technical Controls for GDPR**:
- **Data Minimization**: Collect/process only necessary data; anonymize/pseudonymize where possible
- **Encryption**: AES-256 at rest; TLS 1.2+ in transit; encryption key separation
- **Access Controls**: Strict need-to-know; access reviews quarterly; MFA for all access
- **Breach Notification**: Detect within 72 hours; notify supervisory authority; document all breaches
- **Data Subject Rights**: Right to erasure (automated deletion workflows); data portability (export in machine-readable format); right to rectification
- **Data Retention**: Defined retention schedules; automated data purging after retention period
- **Cross-Border Transfer**: Adequacy decision, SCCs, or BCRs for data leaving EU/EEA

**GDPR Cloud Architecture Requirements**:
```
EU Region (Primary, Restricted)
  └── Encryption: AES-256 + EU-resident KMS keys
  └── Logging: Immutable, 90-day default + 3-year for access logs
  └── Access: EU-based admin team only (MFA enforced)
  └── Data Processing: GDPR DPA in place
  
Controlled Replication (if needed)
  └── SCCs executed with data importer
  └── Technical controls: pseudo-anonymization before transfer
  └── Data location mapping maintained
  
Incident Response
  └── 72-hour notification process
  └── Automated DPA notification workflow
  └── Data Subject Rights portal
```

### 28.2 SOC 2 Cloud Implementation

**SOC 2 Trust Services Criteria**:

| Category | Description | Cloud Controls |
|----------|-------------|----------------|
| **Security** | Protected against unauthorized access | IAM, encryption, firewalls, WAF, IDS/IPS, CISO oversight, security awareness training |
| **Availability** | Available for operation and use | Multi-AZ, autoscaling, DR plan, RPO/RTO defined, SLAs, capacity management, incident response |
| **Processing Integrity** | Processing complete, valid, accurate, timely | Input validation, error handling, reconciliation, transaction logging, monitoring |
| **Confidentiality** | Information designated as confidential protected | Encryption, access controls, data classification, DLP, NDA agreements, data marking |
| **Privacy** | PII collected/used/retained/disclosed properly | PII inventory, privacy notice, consent, DSR response, data retention, breach response, DPIA |

**SOC 2 Evidence Collection in Cloud**:
| Control Area | Evidence Source | Collection Method |
|-------------|----------------|-------------------|
| **Logical Access** | IAM users, roles, policies, MFA settings | IAM credential report; CloudTrail; Config rules; AWS IAM Access Analyzer |
| **Change Management** | IaC changes, pipeline logs, approval records | GitHub; CI/CD pipeline audit; CloudTrail; Change management tickets |
| **System Operations** | Monitoring, incident management, capacity | CloudWatch alarms; GuardDuty findings; Incident reports; PagerDuty/ServiceNow |
| **Risk Management** | Risk register, vendor assessments, penetration test | Risk management system; Pen test reports; Vendor due diligence records |
| **Data Protection** | Encryption, key management, classification | KMS key rotation logs; Macie findings; Data retention schedule; DLP policies |
| **Physical Security** | Data center physical controls (inherited) | SOC 2 Type II report from cloud provider; Sub-processor list |
| **Personnel Security** | Background checks, training, confidentiality | HR records; Training completion records; Signed confidentiality agreements |

### 28.3 ISO 27001 Cloud Implementation

**ISMS (Information Security Management System) Requirements**:

| Clause | Requirement | Cloud Implementation |
|--------|-------------|---------------------|
| **4. Context** | Understanding org, stakeholders, ISMS scope | Define cloud scope (SaaS/PaaS/IaaS, providers, regions, services) |
| **5. Leadership** | Management commitment, policy, roles | Cloud security policy; CISO/cloud security team defined |
| **6. Planning** | Risk assessment, risk treatment, objectives | Cloud risk register; risk treatment plan; security objectives with KPIs |
| **7. Support** | Resources, competence, awareness, communication | Cloud security training; communication plan; incident notification procedures |
| **8. Operation** | Risk treatment, change management, supplier management | Cloud controls implemented (IAM, encryption, monitoring); vendor due diligence; change process |
| **9. Performance** | Monitoring, measurement, audit, management review | Cloud monitoring (GuardDuty, Security Hub); penetration testing; internal audit; management review |
| **10. Improvement** | Nonconformity, corrective action, continual improvement | Incident response; root cause analysis; cloud security improvements; lessons learned |

**ISO 27001 Annex A Controls for Cloud**:

| Control | Cloud Implementation |
|---------|---------------------|
| **A.5 Information Security Policies** | Cloud security policy, review annually |
| **A.6 Organization of Information Security** | Cloud security roles; segregation of duties; mobile device policy |
| **A.7 Human Resource Security** | Background checks; confidentiality agreements; termination access removal |
| **A.8 Asset Management** | Cloud asset inventory; data classification; media handling; acceptable use |
| **A.9 Access Control** | IAM; RBAC; MFA; privileged access management; access reviews |
| **A.10 Cryptography** | Encryption policy; key management; certificate management |
| **A.11 Physical Security** | Inherited from provider (review SOC 2 reports) |
| **A.12 Operations Security** | Cloud monitoring; patch management; malware protection; backup; logging |
| **A.13 Communications Security** | Network segmentation; encryption in transit; secure VPN/Direct Connect |
| **A.14 System Acquisition, Development** | SSDLC; IaC security; DevSecOps; cloud security requirements in procurement |
| **A.15 Supplier Relationships** | Cloud provider assessment; SLA review; vendor risk management; sub-processor list |
| **A.16 Incident Management** | Cloud incident response plan; breach notification; forensics; lessons learned |
| **A.17 Business Continuity** | Cloud BC/DR plan; RPO/RTO; backup verification; DR testing |
| **A.18 Compliance** | Regulatory compliance; IPR; audit evidence; cloud-related legal requirements |

---

## 29. Cloud Security Emerging Trends

### 29.1 AI/ML Security in Cloud

**AI-Specific Cloud Security Risks**:
- **Model Poisoning**: Attacker injects malicious data during training to manipulate model behavior
- **Adversarial Attacks**: Subtle input perturbations cause misclassification
- **Model Inversion**: Reconstruct training data from model outputs (privacy risk)
- **Model Extraction**: Steal model architecture/weights via API queries
- **Supply Chain**: Compromised ML libraries, pre-trained models, datasets
- **Prompt Injection** (LLMs): Manipulate prompt to bypass guardrails; extract system prompts

**Cloud AI Security Controls**:
- **AWS SageMaker Security**: VPC-only endpoints; KMS encryption; IAM fine-grained; model monitoring; MLOps security pipeline
- **Azure AI Security**: Content Safety (offensive content filtering); Responsible AI; Azure AI Studio RBAC; private endpoints
- **GCP Vertex AI Security**: VPC Service Controls; CMEK; IAM conditions; Data loss prevention on training data; model evaluation
- **Generic**: Input sanitization; output verification; model encryption; adversarial training; dataset versioning and signing; differential privacy

### 29.2 Quantum Computing Impact on Cloud Security

**Quantum Threats to Cloud Cryptography**:

| Cryptographic System | Current Algorithm | Quantum Threat | Timeline |
|---------------------|-------------------|----------------|----------|
| **Public Key (PKI)** | RSA, ECDSA, ECDH | Shor's algorithm breaks all public-key crypto | 10-20 years (CRQC) |
| **Symmetric** | AES-256 | Grover's algorithm halves security (AES-256 -> 128-bit) | 15-25 years |
| **Hashing** | SHA-256 | Slight reduction via Grover (collision resistance) | 15-25 years |

**Post-Quantum Cryptography (NIST Standards)**:

| Algorithm | Type | Key Size | Usage |
|-----------|------|----------|-------|
| **CRYSTALS-Kyber** | KEM (Key Encapsulation) | 800-1568 bytes | Key exchange (replaces ECDH/RSA-KEM) |
| **CRYSTALS-Dilithium** | Digital Signature | 1312-2592 bytes | Signatures (replaces ECDSA/RSA) |
| **FALCON** | Digital Signature | 666-1280 bytes | Compact signatures |
| **SPHINCS+** | Digital Signature (stateless hash) | 32-64 bytes | Stateless signatures (replaces RSA/ECDSA) |

**Cloud Provider PQC Readiness**:
- **AWS**: PQC research (hybrid key exchange in TLS); KMS post-quantum readiness; PQ cipher suites in testing
- **Azure**: Microsoft PQC research; hybrid certificates in testing; PQC TLS in Windows
- **GCP**: PQC research; Chrome/BoringSSL PQC support (X25519Kyber768 hybrid); Cloud KMS PQC preparation
- **General**: Migrate to quantum-safe algorithms before CRQC (Cryptographically Relevant Quantum Computer) arrives; inventory all public-key crypto usage; prioritize PQC migration for long-lived data

### 29.3 Cloud Security for 5G and Edge Computing

**Security Implications**:
- **Distributed Attack Surface**: Edge nodes extend cloud perimeter; each edge device is a potential entry point
- **Resource Constraints**: Edge devices have limited compute/memory for security controls; lightweight security required
- **Latency Requirements**: Security processing must not introduce unacceptable latency
- **Physical Security**: Edge devices in uncontrolled environments; tamper-resistant hardware required
- **Data Sovereignty**: Edge processing may cross jurisdictional boundaries; data localization requirements
- **Vast Scale**: Millions of devices; centralized management and monitoring essential

**Cloud Edge Security Controls**:
- **AWS Outposts / Wavelength**: Physical security; IAM same as AWS; encrypted local storage; dedicated network
- **Azure Stack Edge**: Hardware-encrypted; Azure governance extends; Defender for Cloud support; secure boot
- **GCP Distributed Cloud Edge**: Hardware security module; verified boot; encrypted storage; Cloud Console management
- **General**: Zero Trust at edge; mTLS for device-to-cloud; hardware root of trust (TPM 2.0); attestation; remote attestation services

### 29.4 Cloud Security and ESG (Environmental, Social, Governance)

**Cloud Security's Role in ESG**:
- **Environmental**: Green data centers; sustainable security (minimize compute for security scanning); energy-efficient encryption (ChaCha20 vs AES on mobile)
- **Social**: Data privacy as human right; accessible security (diverse security teams; user-friendly MFA); ethical AI; responsible disclosure
- **Governance**: Cloud governance frameworks; supplier diversity; board-level cloud risk oversight; transparency in security reporting

**ESG-Security Metrics**:
- Carbon footprint of security operations (security scanning compute hours)
- Security incident diversity and inclusion impact
- Percentage of security team from underrepresented groups
- Privacy impact assessments completed
- Board-level cybersecurity expertise
- Vendor security assessment scores
- Bug bounty program payments and researcher demographics

---

## 30. Cloud Security Case Studies

### 30.1 CodeCov Breach (2021) — Supply Chain Attack

**Timeline**:
1. **Initial Compromise**: Attacker gained access to CodeCov's Docker Image creation process (weak credential on shell script)
2. **Backdoor Injection**: Modified CodeCov Bash Uploader script to exfiltrate environment variables (including AWS keys, GitHub tokens) from CI/CD pipelines of CodeCov customers
3. **Data Exfiltration**: Modified uploader sent environment variables to attacker-controlled server (port 443, blended with legitimate traffic)
4. **Lateral Movement**: Attacker used stolen credentials to access customer AWS/GitHub environments; modified source code, exfiltrated data, escalated privileges

**Impact**: 31,000+ customers potentially affected (including Confluent, HashiCorp, Twilio, Rapid7, GoDaddy, Atlassian, npm)

**Lessons Learned**:
- **Supply Chain Risk**: Third-party CI/CD tools are high-value targets; vet security posture of all pipeline dependencies
- **Credential Hygiene**: Rotate all credentials after any third-party breach notice; use OIDC federation instead of long-lived keys in CI/CD
- **Pipeline Integrity**: Pin tool versions (hashes); use official distributions only; verify checksums
- **Network Segmentation**: CI/CD runners should have restricted network access (no direct internet if possible; use VPC endpoints)
- **Monitoring**: Monitor for unusual pipeline activity (new branches, modified workflows, unusual API access)
- **Emergency Response**: Have playbook for third-party security incident notification

### 30.2 SolarWinds Orion Attack (2020) — Software Supply Chain

**Timeline**:
1. **Initial Access**: Attacker (likely nation-state) compromised SolarWinds build environment (internal network via AD compromise)
2. **Trojan Injection**: Injected malicious code (Sunburst backdoor) into legitimate Orion software updates; compiled into signed binaries
3. **Distribution**: 18,000+ customers downloaded trojanized updates (automatic update mechanism)
4. **C2 Communication**: Backdoor used HTTP beaconing to attacker-controlled domains; blended with legitimate Orion traffic
5. **Post-Compromise**: In high-value targets, attacker deployed additional tools (Teardrop, Raindrop) via Sunburst for lateral movement, privilege escalation, data exfiltration

**Cloud Impact**: High-value targets included US Federal agencies (Treasury, Commerce, Homeland Security), Microsoft, FireEye, and multiple Fortune 500 companies

**Lessons Learned**:
- **Build Pipeline Security**: Harden build infrastructure; artifact signing + verification at all stages; isolated build environments; integrity monitoring
- **Code Signing**: Sign all builds (authenticode); verify signatures before installation; hardware security module for signing keys
- **Supply Chain Transparency**: SBOM (Software Bill of Materials) for all software; know what's in your dependencies
- **Update Integrity**: Validate updates (hash, signature) before installation; staged/controlled rollouts
- **Detection**: Monitor for anomalous DNS/HTTP beacons; log all process creation events; monitor for unexpected code execution in managed systems
- **Cloud-Specific**: Monitor IAM changes after 3rd-party software install; restrict cross-account access for managed instances

### 30.3 Uber Breach (2022 / 2016)

**2022 Incident**:
1. **Initial Access**: Attacker socially engineered Uber contractor (MFA fatigue); repeatedly pushed MFA notifications until user accepted
2. **Credential Theft**: After user approved MFA, attacker had valid session; gained access to Uber's Okta SSO
3. **Lateral Movement**: Escalated privilege to Okta super admin; accessed AWS Console, GCP Console, Duo, OneLogin, Slack, GSuite, HackerOne bug bounty (to delete vulnerability reports)
4. **Cloud Access**: Exfiltrated data from AWS and GCP environments (including encrypted backups, code repository, internal Slack messages)

**Root Causes**:
- **MFA Fatigue**: Push-based MFA allows user fatigue; should use number matching or hardware security keys (FIDO2)
- **No Risk-Based Access**: MFA prompt should evaluate location/device/behavior risk
- **Overly Permissive Access**: Contractor had unnecessary access; no privileged access workstation requirement
- **Insufficient Monitoring**: Lateral movement within first 30 minutes; attacker accessed 20+ tools before detection

**Remediations**:
- FIDO2 hardware security keys for all privileged accounts
- MFA number matching (required user to enter number shown on screen)
- Reduced contractor access; privileged access workstations
- Enhanced detection for MFA fatigue attacks
- Okta session security (risk-based conditional access)

### 30.4 Capital One Breach (2019) — WAF Misconfiguration

**Timeline**:
1. **Initial Reconnaissance**: Attacker (former AWS employee) scanned AWS metadata endpoints for vulnerable web applications; identified Capital One's WAF instance
2. **SSRF Exploitation**: Capital One ran a custom WAF on EC2 (not AWS WAF); the WAF had a Server-Side Request Forgery vulnerability allowing the attacker to call the EC2 metadata service (IMDSv1)
3. **Credential Theft**: Attacker called `http://169.254.169.254/latest/meta-data/iam/security-credentials/` from the WAF server; retrieved temporary AWS credentials for a WAF IAM role
4. **Data Exfiltration**: Using stolen credentials, attacker listed S3 buckets belonging to Capital One; downloaded 700+ buckets containing 140,000 SSNs, 80,000 bank account numbers, customer data from 2005-2019

**Impact**: 106 million customers affected; $190M in fines/penalties/settlements; 100+ class-action lawsuits; OCC consent order

**Root Causes**:
- **IMDSv1 Usage**: Metadata service had no session authentication or hop limit; IMDSv2 would have prevented the credential theft
- **Overly Permissive IAM Role**: The WAF server's IAM role had S3 read permissions to ALL buckets; should have been scoped to specific resources
- **Missing Network Segmentation**: WAF server had network access to S3 endpoints; should have been isolated with only proxy outbound access
- **No WAF on the WAF**: The custom WAF ran on a public EC2 instance with no web application firewall in front

**Lessons Learned**:
- **Always use IMDSv2** with hop limit 1 (prevents SSRF-based credential theft)
- **Instance IAM roles must be least privilege**: Never grant broad S3 access to workload roles; use S3 bucket policies with explicit conditions
- **Network segmentation for middleboxes**: WAF servers, proxies, and gateways should be in isolated subnets with restricted outbound access
- **No custom authentication/authorization devices on public internet**: Use managed WAF services (AWS WAF, CloudFront, Cloudflare, Akamai) that don't expose metadata service
- **Sensitive data discovery**: Proactive scanning for PII/PCI in storage; Macie or equivalent should have flagged exposed data
- **CloudTrail monitoring**: Alert on unusual ListBuckets/GetObject patterns; attacker spent days exfiltrating data

### 30.5 AWS S3 Breach (2017) — Public Bucket Misconfiguration (Alteryx, US DoD, Accenture)

**Timeline**:
1. **Discovery by Researchers**: UpGuard researchers discovered publicly accessible AWS S3 buckets containing personally identifiable information (PII) from multiple organizations
2. **Alteryx (2017)**: 123 million US households data (addresses, income, age, vehicle ownership, interests) exposed in public bucket; data from Experian aggregate
3. **US DoD/NSA (2017)**: 1.8 billion internet intelligence records (geolocation, server data, DNS queries) left in public AWS S3 bucket by Booz Allen Hamilton contractor
4. **Accenture (2017)**: 4 buckets publicly accessible (137 GB); contained API tokens, decryption keys, credentials, customer PII; used for automated backups with no authentication

**Root Causes**:
- **Public Bucket Permissions**: Bucket ACLs or policies allowed `Everyone` or `Any Authenticated AWS User` LIST/GET access
- **No Block Public Access**: Account-level or bucket-level S3 Block Public Access not enabled
- **No Data Classification**: Organizations unaware of what data was stored in which buckets
- **No Monitoring**: CloudTrail data events not enabled; no alerts on GetObject/ListBucket from anonymous principals

**Lessons Learned**:
- **Enable S3 Block Public Access at account level** (default recommended)
- **Never use S3 ACLs**: Use bucket policies with explicit conditions; disable ACLs entirely
- **Data classification is critical**: Know what data you have and where; use Macie or similar
- **CloudTrail data events**: Enable for sensitive buckets; monitor anonymous access patterns
- **Automated discovery**: CSPM tools to scan for public/overly-permissive storage
- **Default-deny mindset**: Buckets should be private by default; only grant access with explicit justification

### 30.6 Additional Notable Cloud Breaches

**Twilio (2022) — Social Engineering**:
- Attacker texted Twilio employees as "IT Support", claiming password issues; directed to phishing site mimicking Twilio SSO
- Stolen credentials gave access to internal console; exfiltrated Authy MFA 2FA user database
- **Lesson**: SMS-based social engineering; phishing-resistant MFA (FIDO2) required; employee phishing training

**LastPass (2022) — Cloud Key Compromise**:
- Attacker compromised a developer's personal computer; extracted master password from keylogger
- Accessed LastPass cloud development environment; exfiltrated source code, proprietary tech, customer vault backups
- **Lesson**: Cloud admin access from non-corporate devices; PAM for all cloud development; separate production and development environments; encrypt backups with separate key hierarchy

**Heroku/GitHub (2022) — OAuth Token Theft**:
- Attacker compromised Heroku engineering environment; stole OAuth tokens used by Heroku to access GitHub repositories
- Downloaded private repositories from multiple organizations (npm, HashiCorp, others)
- **Lesson**: OAuth token rotation; monitor token usage patterns; integrate detection for unexpected repository access; use short-lived tokens

**EasyJet (2020) — SaaS Breach**:
- 9 million customers affected; attacker accessed travel booking data including credit card details
- **Lesson**: SaaS provider breach impact; contractual security requirements; data encryption at rest (customer-managed keys)

**Marriott/Starwood (2018) — Cloud Migration Risk**:
- Attacker compromised Starwood reservation database; maintained access for 4 years (pre-dating Marriott acquisition)
- 500 million guest records exfiltrated; GDPR £99M fine
- **Lesson**: Security due diligence during M&A; cloud migration exposes legacy vulnerabilities; need thorough security assessment of acquired systems

---

## 31. Cloud Security Interview Questions

### 31.1 Technical Questions

**Q1: Explain the shared responsibility model for cloud security. How does it differ between IaaS, PaaS, and SaaS?**

The shared responsibility model divides security responsibilities between the cloud provider and the customer. The provider is responsible for security OF the cloud (physical infrastructure, networking, hypervisor), while the customer is responsible for security IN the cloud (data, identities, configurations, applications). In IaaS, the customer is responsible for more layers (OS, middleware, runtime). In PaaS, the provider extends to manage the OS and runtime, while the customer manages application code, data, and access. In SaaS, the provider manages almost everything except user access, data governance, and configuration.

**Q2: What is the principle of least privilege and how is it implemented in cloud IAM?**

Least privilege means granting only the minimum permissions necessary to perform a function. Implemented via: granular IAM policies with specific actions/resources/conditions; avoiding `*` wildcards; using groups for role-based access; regular permission reviews; temporary elevation (JIT/PIM); IAM Access Analyzer for unused permissions; policy conditions (IP, MFA, time, VPC); service-specific roles per component.

**Q3: Describe the difference between a Security Group and a Network ACL.**

Security Groups are stateful, instance-level firewalls that support allow rules only (implicit deny). They evaluate all rules together and automatically allow return traffic. Network ACLs are stateless, subnet-level firewalls that support both allow and deny rules. They evaluate rules in number order, and return traffic must be explicitly allowed. Security Groups are for micro-segmentation (per-instance), while NACLs provide subnet-level defense depth.

**Q4: How would you detect and respond to a compromised IAM key in AWS?**

Detection: GuardDuty findings (UnauthorizedAccess:IAM/User); CloudTrail analysis for unusual source IPs, user agents, API calls from unfamiliar geographies, or abnormal API call patterns. Response: Immediately disable/delete the access key (`aws iam update-access-key --status Inactive`); detach the IAM user/role from permissive policies; revoke all active sessions (STS `RevokeSessions`); review CloudTrail for actions taken with compromised key; notify data owners of potential data exposure; rotate all credentials (keys, passwords); investigate root cause; implement additional controls (MFA, IMDSv2, condition keys limiting access).

**Q5: What is encryption in transit vs at rest vs in use? Give examples.**

At-rest encryption protects stored data: AES-256 for S3, EBS, RDS (SSE-KMS), Azure Disk Encryption (BitLocker/DM-Crypt), GCP CMEK. In-transit encryption protects data moving between systems: TLS 1.2+ for HTTPS, API calls, database connections; IPsec VPN; MACsec for Direct Connect. In-use encryption protects data during processing: Confidential Computing (Intel SGX, AMD SEV-SNP, AWS Nitro Enclaves, Azure Confidential VMs, GCP Confidential VMs) where data is decrypted only inside CPU-protected enclaves.

**Q6: Explain the difference between a bucket policy and an IAM policy in AWS.**

IAM policies are identity-based: attached to users, groups, or roles; define what that identity can do across AWS. Bucket policies are resource-based: attached directly to S3 buckets; define who can access the bucket and under what conditions; allow cross-account access without needing to create IAM roles. Both policies use similar JSON structure; the effective permission is the union of all applicable identity-based and resource-based policies minus any explicit denies.

**Q7: How does AWS KMS key rotation work? What types of keys support it?**

AWS KMS supports automatic annual rotation for Customer Managed Keys (CMKs). When rotation occurs, KMS retains the old key material (for decrypting existing data) and creates new key material (used for all new encrypt operations). AWS managed keys rotate automatically every 3 years (cannot configure). AWS owned keys cannot be configured or rotated. For regulatory requirements, customer managed keys can also be rotated manually. Imported key material does NOT support automatic rotation (must import new material manually).

**Q8: Describe how to securely set up a three-tier web application in AWS.**

VPC with public subnets (ALB), private subnets (web + app), isolated subnets (RDS). WAF + CloudFront at edge. ALB with HTTPS (ACM certificate). Security groups: ALB allows 443 from internet; web tier allows HTTP from ALB only; app tier allows 8080 from web tier only; RDS allows 5432 from app tier only. RDS encrypted with KMS, multi-AZ enabled. Autoscaling groups with health checks. CloudTrail, VPC Flow Logs, GuardDuty enabled. S3 access logs stored encrypted with Object Lock.

**Q9: What is IMDSv2 and why is it important?**

Instance Metadata Service (IMDS) provides metadata about EC2 instances including IAM credentials. IMDSv1 allowed unauthenticated access (GET request to 169.254.169.254). IMDSv2 requires session-oriented requests: first a PUT request to get a token (with TTL), then the token is used in subsequent GET requests. Additionally, hop limit (1 by default) prevents containers/pods from accessing instance metadata. IMDSv2 mitigates SSRF attacks that could steal instance credentials.

**Q10: How do you implement DDoS protection in the cloud?**

Defense in depth: CloudFront/Azure CDN/Cloud CDN (absorb at edge); WAF with rate limiting, geo-restriction, bot control; AWS Shield Advanced/Azure DDoS Protection/GCP Cloud Armor (layer 3/4/7 mitigation); autoscaling (absorb traffic spikes); Route53/Azure DNS/GCP Cloud DNS (distributed DNS with anycast); S3 origin failover; health checks with DNS failover; security groups allowing only expected traffic; dedicated DDoS response team (Shield Advanced).

### 31.2 Scenario-Based Questions

**Q: Your organization stores PII in an S3 bucket. GuardDuty alerts that the bucket is being accessed from an unexpected IP address. Walk through your response.**

1. **Confirmation**: Check CloudTrail (GetObject, ListBucket events) from the suspicious IP; confirm IAM role/user used; check if bucket policy allows anonymous access
2. **Containment**: Apply S3 Block Public Access if not already; update bucket policy conditions (source IP restriction); rotate any exposed access keys; isolate IAM role
3. **Impact Assessment**: Use S3 access logs to determine which objects were accessed; classify data sensitivity (Macie scan); determine regulatory notification requirements
4. **Root Cause**: Review how the IP gained access (leaked keys, overly permissive policy, public bucket)
5. **Remediation**: Block public access at account level; enforce least-privilege S3 policies; enable CloudTrail data events for S3; tighten IAM (source IP conditions, MFA, VPC endpoints); implement S3 Block Public Access
6. **Notification**: Notify data subjects if required (GDPR 72-hour); notify security team

**Q: Your company uses EC2 for web servers and RDS for databases. An engineer accidentally left port 3306 (MySQL) open to the world on the RDS security group. What's the risk and how do you fix it?**

Risk: Anyone on the internet can attempt to connect to the database; brute force attacks on MySQL credentials; potential data exfiltration or ransomware. Fix: Immediately revoke the 0.0.0.0/0 ingress rule for port 3306; change RDS master password; review MySQL logs for unauthorized access attempts; enable automated RDS security group compliance check (AWS Config rule RDS_SG_RESTRICTED); use AWS Config to auto-remediate overly permissive security groups; implement least-privilege security group rules (allow port 3306 from app tier SG only).

**Q: You discover a Lambda function has an IAM role with `s3:*` and `*` as the resource. What is the risk, and what improvements do you make?**

Risk: If Lambda is compromised (vulnerable code, event injection, dependency exploit), attacker has full S3 access across ALL buckets in the account; can read, write, delete, or exfiltrate any S3 data. Improvements: Replace `s3:*` with specific actions (e.g., `s3:GetObject`, `s3:PutObject` only as needed); replace `Resource: *` with specific bucket ARN and object ARN; add condition keys (VPC source, source IP); use a dedicated bucket per Lambda function; enable CloudTrail data events for S3; use S3 access points for granular permissions; implement resource-based bucket policy as additional layer.

---

## 32. Cloud Security Glossary

| Term | Definition |
|------|------------|
| **ABAC** | Attribute-Based Access Control; access decisions based on user, resource, and environment attributes |
| **ACM** | AWS Certificate Manager; provision, manage, deploy SSL/TLS certificates |
| **ACL** | Access Control List; rules defining allowed/denied traffic (stateless in cloud networking) |
| **ALB** | Application Load Balancer; layer 7 load balancer with content-based routing, WAF integration |
| **API Gateway** | Managed service to create, publish, maintain, monitor, and secure APIs at scale |
| **ASG** | Auto Scaling Group; automatically scale EC2 instances based on demand/health |
| **BAA** | Business Associate Agreement; HIPAA required contract for PHI handling |
| **BYOK** | Bring Your Own Key; customer generates and imports their own encryption key |
| **CAIQ** | Consensus Assessments Initiative Questionnaire; CSA questionnaire for cloud provider assessments |
| **CASB** | Cloud Access Security Broker; intermediary between users and cloud apps for security policy enforcement |
| **CCM** | Cloud Controls Matrix; CSA framework of 197+ cloud security controls |
| **CCPA** | California Consumer Privacy Act; US state privacy regulation |
| **CCSP** | Certified Cloud Security Professional; ISC2 + CSA cloud security certification |
| **CDE** | Cardholder Data Environment; PCI-DSS defined scope of systems handling card data |
| **CIEM** | Cloud Infrastructure Entitlement Management; manage and enforce least privilege for cloud identities |
| **CIS** | Center for Internet Security; publishes security benchmarks for cloud platforms |
| **CLI** | Command Line Interface; tool to manage cloud services via commands |
| **CMK** | Customer Master Key; primary key in AWS KMS (now called KMS Key / Customer Managed Key) |
| **CNAME** | Canonical Name record; DNS record type for domain aliasing |
| **CRL** | Certificate Revocation List; list of revoked certificates |
| **CSA** | Cloud Security Alliance; organization defining cloud security standards (CCM, STAR, CCSK) |
| **CSC** | Cloud Service Consumer; customer using cloud services |
| **CSP** | Cloud Service Provider; organization providing cloud services (AWS, Azure, GCP) |
| **CSPM** | Cloud Security Posture Management; continuous monitoring for cloud misconfigurations |
| **CVE** | Common Vulnerabilities and Exposures; standardized vulnerability identifiers |
| **CWPP** | Cloud Workload Protection Platform; unified security for VMs, containers, serverless |
| **DAST** | Dynamic Application Security Testing; testing running application for vulnerabilities |
| **DLP** | Data Loss Prevention; preventing unauthorized data exfiltration |
| **DPA** | Data Processing Agreement; GDPR-required contract between controller and processor |
| **DR** | Disaster Recovery; restoring IT systems after catastrophic failure |
| **EBS** | Elastic Block Store; AWS block storage for EC2 |
| **EC2** | Elastic Compute Cloud; AWS virtual server service |
| **ECR** | Elastic Container Registry; AWS container image registry |
| **EKS** | Elastic Kubernetes Service; AWS managed Kubernetes |
| **ELB** | Elastic Load Balancer; AWS load balancing service |
| **ERM** | Enterprise Risk Management; organization-wide risk framework |
| **FaaS** | Function as a Service; serverless compute model (AWS Lambda, Azure Functions, GCP Cloud Functions) |
| **FedRAMP** | Federal Risk and Authorization Management Program; US government cloud security program |
| **FIPS** | Federal Information Processing Standards; US government cryptographic standards |
| **GDPR** | General Data Protection Regulation; EU data protection regulation |
| **HITECH** | Health Information Technology for Economic and Clinical Health Act; HIPAA expansion |
| **HSM** | Hardware Security Module; dedicated hardware for cryptographic key protection |
| **HYOK** | Hold Your Own Key; customer retains exclusive control over encryption keys |
| **IaC** | Infrastructure as Code; managing cloud resources through code (Terraform, CloudFormation) |
| **IAM** | Identity and Access Management; managing identities and access to cloud resources |
| **IaaS** | Infrastructure as a Service; virtualized computing resources (AWS EC2, Azure VM, GCP GCE) |
| **IdP** | Identity Provider; system that authenticates users (Okta, Azure AD, Keycloak) |
| **IGW** | Internet Gateway; allows VPC resources internet access |
| **IMDS** | Instance Metadata Service; provides metadata about cloud instances including credentials |
| **IRM** | Information Rights Management; persistent data protection regardless of location |
| **ISMS** | Information Security Management System; ISO 27001 management framework |
| **ISO** | International Organization for Standardization; publishes security standards (27001, 27017, 27018) |
| **JIT** | Just-In-Time; temporary elevation of privileges |
| **JWT** | JSON Web Token; token format for authentication/authorization claims |
| **KMS** | Key Management Service; managed cryptographic key service |
| **KQL** | Kusto Query Language; Azure Sentinel/Monitor query language |
| **MFA** | Multi-Factor Authentication; authentication requiring 2+ factors (knowledge, possession, inherence) |
| **mTLS** | Mutual Transport Layer Security; both parties present certificates for authentication |
| **NACL** | Network Access Control List; stateless subnet-level firewall in cloud |
| **NAT** | Network Address Translation; allows private instances outbound internet access |
| **NIST** | National Institute of Standards and Technology; US standards body (CSF, SP 800 series) |
| **OIDC** | OpenID Connect; authentication layer on OAuth 2.0 (JWT-based) |
| **OPA** | Open Policy Agent; open-source policy engine (Rego language) |
| **PaaS** | Platform as a Service; managed application platform (AWS Elastic Beanstalk, Azure App Service, GCP App Engine) |
| **PCI DSS** | Payment Card Industry Data Security Standard; credit card data protection standard |
| **PHI** | Protected Health Information; HIPAA-defined personal health data |
| **PII** | Personally Identifiable Information; data that can identify an individual |
| **PQC** | Post-Quantum Cryptography; cryptographic algorithms resistant to quantum computers |
| **RBAC** | Role-Based Access Control; permissions assigned to roles, users assigned to roles |
| **RDS** | Relational Database Service; AWS managed relational database |
| **RPO** | Recovery Point Objective; maximum acceptable data loss (time) |
| **RSA** | Rivest-Shamir-Adleman; asymmetric encryption algorithm |
| **RTO** | Recovery Time Objective; maximum acceptable downtime |
| **SaaS** | Software as a Service; ready-made applications (Microsoft 365, Salesforce, Google Workspace) |
| **SAML** | Security Assertion Markup Language; XML-based SSO authentication protocol |
| **SAST** | Static Application Security Testing; analyzing source code for vulnerabilities |
| **SBOM** | Software Bill of Materials; inventory of software components and dependencies |
| **SCC** | Security Command Center; GCP security management platform |
| **SCP** | Service Control Policy; centrally manage permissions in AWS Organizations |
| **SDLC** | Software Development Lifecycle; phases of software development |
| **SDN** | Software-Defined Networking; programmable network management (control plane/data plane separation) |
| **SGs** | Security Groups; stateful instance-level firewalls in cloud |
| **SIEM** | Security Information and Event Management; security log aggregation and analysis |
| **SLA** | Service Level Agreement; contract defining service guarantees (uptime, response time, credits) |
| **SNI** | Server Name Indication; TLS extension for multiple certificates on one IP |
| **SOAR** | Security Orchestration, Automation, and Response; automated security incident response |
| **SOC** | Service Organization Control; audit report types (SOC 1/2/3) for service providers |
| **SPIFFE** | Secure Production Identity Framework for Everyone; workload identity standard |
| **SSH** | Secure Shell; encrypted remote administration protocol |
| **SSO** | Single Sign-On; authenticate once to access multiple applications |
| **SSRF** | Server-Side Request Forgery; server-side request manipulation to access internal resources |
| **STAR** | Security, Trust, Assurance, and Risk; CSA registry of provider assessments |
| **STS** | Security Token Service (AWS); issue temporary credentials |
| **TEE** | Trusted Execution Environment; hardware-isolated compute environment (Intel SGX, AMD SEV) |
| **TLS** | Transport Layer Security; encryption protocol for secure communication (1.2, 1.3) |
| **TPM** | Trusted Platform Module; hardware security chip for attestation and encryption |
| **VPC** | Virtual Private Cloud; logically isolated cloud network |
| **WAF** | Web Application Firewall; filters HTTP traffic against OWASP Top 10 attacks |
| **WORM** | Write Once Read Many; immutable storage preventing modification/deletion |
| **ZTA** | Zero Trust Architecture; security model with no implicit trust, continuous verification |
| **ZTNA** | Zero Trust Network Access; application-specific access without VPN |

---

> Final Reminder: Cloud security is a shared responsibility, continuous process, and requires defense-in-depth. The most common breaches result from misconfigurations, not provider vulnerabilities. Implement IAM least privilege, enable encryption everywhere, log everything, monitor continuously, automate responses, and test your incident response regularly. The cloud gives you incredible power — use it responsibly.

---

## 33. Cloud Security Policies and Procedures

### 33.1 Cloud Security Policy Framework
A cloud security policy framework establishes the rules, guidelines, and procedures for secure cloud adoption and operations.

**Policy Hierarchy**:
```
Cloud Security Policy (Executive Level)       ← High-level principles, scope, governance
Cloud Security Standards (Tactical)           ← Minimum security requirements, baselines
Cloud Security Procedures (Operational)       ← Step-by-step instructions for implementation
Cloud Security Guidelines (Advisory)          ← Best practices, recommendations
```

### 33.2 Essential Cloud Security Policies

**1. Cloud Acceptable Use Policy**
- Authorized and prohibited uses of cloud services
- User responsibilities and accountability
- Data classification and handling requirements
- Personal device and BYOD restrictions
- Reporting security incidents
- Consequences of policy violations

**2. Cloud Access Control Policy**
- Identity lifecycle management (joiner/mover/leaver)
- MFA requirements (all users, mandatory for privileged)
- Password policy (complexity, length, rotation, history)
- Role-based access control principles
- Privileged access management procedures
- Session timeout and lockout policies
- API key and service account management
- Third-party access requirements

**3. Cloud Data Classification and Handling Policy**
- Data classification levels (Public, Internal, Confidential, Restricted, Regulatory)
- Handling requirements per classification level
- Encryption requirements (at rest, in transit, in use)
- Data retention and destruction schedules
- Data loss prevention (DLP) controls
- Data sovereignty and residency requirements
- Data sharing and cross-border transfer rules

**4. Cloud Encryption and Key Management Policy**
- Approved encryption algorithms (AES-256, TLS 1.2+, ChaCha20)
- Minimum key sizes (RSA 2048+, ECDSA P-256+)
- Key lifecycle management (generation, distribution, rotation, revocation, destruction)
- Key management service usage (KMS, CloudHSM, Key Vault)
- BYOK/HYOK requirements
- Certificate management (renewal, revocation, monitoring)
- HSM usage requirements

**5. Cloud Network Security Policy**
- VPC design standards (CIDR ranges, subnet sizing, segmentation)
- Firewall rules (default-deny inbound, restrict outbound)
- Network segmentation requirements (tier isolation, environment separation)
- Remote access requirements (VPN, bastion hosts, Zero Trust)
- DDoS protection requirements
- DNS security (DNSSEC, DNS filtering)
- API gateway security requirements

**6. Cloud Logging and Monitoring Policy**
- Log sources and coverage requirements
- Log retention periods per data type
- SIEM integration requirements
- Alert severity definitions and thresholds
- Monitoring coverage (CloudTrail, VPC Flow Logs, WAF logs, DNS logs)
- Log protection (immutability, encryption, access control)
- Log review frequency and responsibilities
- Automated response triggers

**7. Cloud Incident Response Policy**
- Incident classification and severity definitions
- Response team structure and roles
- Escalation procedures and timelines
- Containment, eradication, recovery procedures
- Forensic evidence collection requirements
- Communication plan (internal, legal, customers, regulators)
- Post-incident review requirements
- Third-party breach notification procedures

**8. Cloud Vendor and Third-Party Risk Policy**
- Vendor due diligence requirements (certifications, security posture, financial stability)
- Contract requirements (SLA, DPA, BAA, right to audit)
- Vendor risk assessment frequency
- Sub-processor approval requirements
- Vendor termination and data return/destruction procedures
- Cloud provider compliance certification requirements

**9. Cloud Application Security Policy**
- Secure SDLC requirements
- Code review and security testing (SAST/DAST/SCA)
- Vulnerability management and patching SLAs
- API security requirements
- Container security (image scanning, signing, runtime protection)
- Serverless security requirements
- Third-party component management (SBOM, dependency scanning)
- Infrastructure as Code requirements (scanning before deployment)

**10. Cloud Business Continuity and DR Policy**
- RPO/RTO requirements per workload criticality
- Backup frequency and retention requirements
- Backup verification procedures
- Disaster recovery testing frequency
- Multi-region / multi-AZ architecture requirements
- Failover and failback procedures
- Alternative provider contingency plans

### 33.3 Cloud Security Procedures

**User Onboarding Procedure**:
1. HR initiates new user request with role/department/access level
2. Manager approves access requirements
3. Security team creates cloud identity (IAM user, Azure AD user, Google account)
4. Admin assigns to appropriate groups/roles per job function
5. User receives initial password (must change on first login)
6. MFA enrollment required before first access
7. User completes cloud security awareness training within 30 days
8. Access granted; user notified
9. Access logged and tracked in identity management system

**User Offboarding Procedure**:
1. HR/Manager initiates offboarding request with effective date/time
2. Immediate (within 1 hour): Disable cloud accounts; revoke all sessions; rotate shared credentials
3. Within 24 hours: Remove from all groups/roles; delete API keys; remove from all cloud provider accounts
4. Within 7 days: Transfer ownership of resources created by user; review access logs for recent activity
5. Within 30 days: Permanently delete account; archive audit trail
6. Certificate of deletion returned to HR for record-keeping

**Incident Response Procedure (Detailed)**:
```
PHASE 1 — Triage (0-15 minutes)
  1.1 Acknowledge alert from monitoring system
  1.2 Gather initial information (what, when, who, affected resources)
  1.3 Classify severity (Critical/High/Medium/Low)
  1.4 Notify incident response team
  1.5 Create incident ticket in tracking system

PHASE 2 — Investigation (15-60 minutes)
  2.1 Review CloudTrail for involved accounts/roles/resources
  2.2 Review VPC Flow Logs for network activity
  2.3 Review IAM access analyzer for exposed resources
  2.4 Review affected application/system logs
  2.5 Determine initial scope (resources, data, time window)
  2.6 Escalate to management/deputy if high severity

PHASE 3 — Containment (30-120 minutes)
  3.1 If compromised IAM key: Disable key, detach policies, revoke sessions
  3.2 If compromised instance: Isolate via security group, snapshot volumes
  3.3 If exposed data: Block public access, rotate credentials, review access logs
  3.4 If active attack: Block source IPs via WAF/NACL/Azure Firewall
  3.5 Preserve evidence (EBS snapshots, CloudTrail, S3 access logs)
  3.6 Communicate containment status to stakeholders

PHASE 4 — Eradication (1-8 hours)
  4.1 Patch vulnerability (OS, application, configuration)
  4.2 Remove attacker persistence (backdoor users, keys, Lambda functions)
  4.3 Rotate ALL credentials that may have been exposed
  4.4 Restore from clean backup if system compromised
  4.5 Verify no remaining backdoors or persistence mechanisms

PHASE 5 — Recovery (1-24 hours)
  5.1 Gradually restore services in isolated environment
  5.2 Verify security controls before production return
  5.3 Monitor restored systems for 48+ hours
  5.4 Enable enhanced logging and monitoring
  5.5 Document all changes made during recovery

PHASE 6 — Post-Incident (1-2 weeks)
  6.1 Conduct root cause analysis
  6.2 Identify process/technology/people gaps
  6.3 Update incident response playbooks
  6.4 Implement preventive controls
  6.5 Report to management/board/compliance
  6.6 Legal review for breach notification requirements
  6.7 Update risk register
```

---

## 34. Cloud Security Runbooks

### 34.1 Runbook: S3 Bucket Public Exposure
**Trigger**: GuardDuty finding `Policy:IAMUser/S3BucketPubliclyReadable`, Security Hub `S3.1`, or CSAW alert

**Severity**: HIGH

**Response Steps**:
| Step | Action | Command / Tool | Timeline |
|------|--------|---------------|----------|
| 1 | Verify exposure | Check bucket ACL and bucket policy | 5 min |
| 2 | Apply Block Public Access | `aws s3api put-public-access-block` | 5 min |
| 3 | Apply account-level Block Public Access | `aws s3control put-public-access-block` | 5 min |
| 4 | Determine exposure window | Check S3 access logs and CloudTrail data events | 15 min |
| 5 | List exposed objects | `aws s3api list-objects-v2 --bucket <name>` | 10 min |
| 6 | Classify data sensitivity | Run Macie scan; check classification tags | 30 min |
| 7 | Determine if data was accessed | Check S3 server access logs for anonymous requester | 15 min |
| 8 | Notify data owner | Email/call bucket owner and data steward | Immediate |
| 9 | Review bucket policy | `aws s3api get-bucket-policy --bucket <name>` | 30 min |
| 10 | Implement permanent fix | Remove public access; enforce MFA/VPC conditions on bucket | 30 min |

**Escalation Criteria**: If sensitive data (PII, PHI, financial) exposed → Notify CISO, Legal, Privacy Officer

**Automation**:
```python
def lambda_handler(event, context):
    for finding in event['detail']['findings']:
        bucket_name = finding['Resource']['S3BucketDetails'][0]['Name']
        s3.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True, 'IgnorePublicAcls': True,
                'BlockPublicPolicy': True, 'RestrictPublicBuckets': True
            }
        )
        sns.publish(TopicArn=topic_arn, Message=f"AUTO-REMEDIATED: {bucket_name} blocked")
```

### 34.2 Runbook: Compromised IAM Access Key
**Trigger**: GuardDuty `UnauthorizedAccess:IAMUser/UserWithKeyExposed` or `CredentialAccess:User/AnomalousBehavior`

**Severity**: CRITICAL

**Response Steps**:
| Step | Action | Command / Tool | Timeline |
|------|--------|---------------|----------|
| 1 | Verify compromise | Check CloudTrail for API calls from unexpected IP/user agent | 5 min |
| 2 | Disable access key | `aws iam update-access-key --status Inactive` | 2 min |
| 3 | Detach permissive policies | `aws iam detach-user-policy --user-name <user> --policy-arn <arn>` | 5 min |
| 4 | Revoke all sessions | `aws sts revoke-sessions-by-user --user-name <user>` | 5 min |
| 5 | Disable console access | `aws iam delete-login-profile --user-name <user>` | 2 min |
| 6 | Investigate API calls | `aws cloudtrail lookup-events --lookup-attributes AttributeKey=Username,AttributeValue=<user>` | 30 min |
| 7 | Check for data access | S3 GetObject, DynamoDB GetItem, RDS DescribeDBInstances by user | 30 min |
| 8 | Check for resource creation | `ec2:RunInstances`, `lambda:CreateFunction`, `iam:CreateUser` | 30 min |
| 9 | Rotate key permanently | Create new key, delete old key | 15 min |
| 10 | Block source IP | `aws wafv2 update-ip-set --addresses <source_ip>/32` | 15 min |

**Post-Incident**: Implement IAM condition keys; use STS instead of long-lived keys; activate CloudTrail Insights

### 34.3 Runbook: Cryptomining on EC2
**Trigger**: GuardDuty `CryptoCurrency:EC2/BitcoinTool.B!DNS` or high CPU/network metrics

**Severity**: HIGH

**Response Steps**:
| Step | Action | Timeline |
|------|--------|----------|
| 1 | Stop/quarantine instance via security group isolation | 2 min |
| 2 | Snapshot EBS volumes for forensics | 5 min |
| 3 | Tag instance as compromised | 2 min |
| 4 | Check IAM role attached; review permissions | 5 min |
| 5 | Detach instance from ASG | 10 min |
| 6 | Investigate VPC Flow Logs for mining pool connections | 30 min |
| 7 | Check CloudTrail for instance launch details | 30 min |
| 8 | Block mining pool IPs in WAF/Network Firewall | 15 min |
| 9 | Identify entry vector (stolen keys, vulnerable app, public SSH) | 60 min |
| 10 | Deploy clean instance from CIS-hardened AMI | 30 min |

**Preventive Controls**: No public subnets for compute; egress filtering; GuardDuty in all regions; VPC endpoints

### 34.4 Runbook: Ransomware Detection in Cloud Storage
**Trigger**: Mass delete/encrypt alerts, GuardDuty S3 findings, unusual RenameObject/PutObject patterns

**Severity**: CRITICAL

**Response Steps**:
1. Activate Object Lock on affected buckets (Compliance mode)
2. Deny `s3:DeleteObject` and `s3:DeleteObjectVersion` via bucket policy
3. Isolate affected accounts via SCP
4. Enable versioning if not already enabled
5. Identify attacker access pattern via CloudTrail
6. Remove attacker access (disable keys, detach policies, block IPs)
7. Restore from versioning: `aws s3api list-object-versions` then restore
8. Restore from cross-region backup or Glacier
9. Run Macie scan on restored data
10. Notify legal/compliance for breach notification assessment

**Preventive Controls**: Object Lock (Compliance mode); versioning on ALL buckets; cross-region replication; air-gapped backup account; immutable backups with MFA delete

### 34.5 Runbook: RDS Security Breach
**Trigger**: GuardDuty `UnauthorizedAccess:RDS/MaliciousSQLCall`, database audit log alerts

**Severity**: CRITICAL

**Response Steps**:
1. Isolate database (update SG to deny all except maintenance)
2. Disable public accessibility: `aws rds modify-db-instance --no-publicly-accessible`
3. Create forensic snapshot: `aws rds create-db-snapshot`
4. Rotate database password: `aws rds modify-db-instance --master-user-password <new>`
5. Enable deletion protection: `aws rds modify-db-instance --deletion-protection`
6. Analyze RDS audit logs for suspicious queries (DROP, GRANT, SELECT *)
7. Analyze CloudTrail for RDS API calls
8. Rotate all application DB credentials
9. Restore from pre-incident snapshot if data manipulated

**RDS Hardening Checklist**:
- [ ] RDS in private subnet; SG allows only app tier
- [ ] Encryption at rest enabled
- [ ] TLS connection enforced
- [ ] Automated backups (35-day retention)
- [ ] Multi-AZ enabled
- [ ] Deletion protection enabled
- [ ] Database audit logging enabled
- [ ] IAM database authentication
- [ ] Master password in Secrets Manager with auto-rotation
- [ ] Automated minor version upgrades
- [ ] Parameter groups: log_connections=ON, log_disconnections=ON

---

## 35. Cloud Security Checklist Compendium

### 35.1 Account and Subscription Security
- [ ] Root account MFA enabled (hardware MFA preferred)
- [ ] Root account access keys deleted
- [ ] Root account email monitored; alerts for root login
- [ ] CloudTrail enabled in ALL regions; multi-region trail
- [ ] CloudTrail log file validation enabled; KMS encrypted
- [ ] CloudTrail logs in immutable S3 bucket in security account
- [ ] AWS Organizations/Azure MGMT Groups/GCP Organization configured
- [ ] SCPs/Azure Policies/Org Policies enforced
- [ ] Budget alerts configured (50%+ spike)
- [ ] All unused accounts/projects identified and removed
- [ ] Tagging strategy enforced (owner, environment, cost center, data class)
- [ ] Compliance standards identified and mapped

### 35.2 IAM Security
- [ ] MFA enforced for ALL users
- [ ] No IAM users with long-lived access keys (use roles/SSO)
- [ ] Password policy: min 14 chars, complexity
- [ ] Least privilege (no `*` in Action or Resource)
- [ ] IAM roles for EC2/Lambda/workloads (no embedded keys)
- [ ] IAM Access Analyzer configured and reviewed
- [ ] Unused users/roles/keys removed (90-day threshold)
- [ ] IAM credential report monthly
- [ ] SCPs limit maximum permissions
- [ ] IAM conditions used (SourceIp, MFA, VPC, time, tags)
- [ ] Cross-account roles instead of IAM users
- [ ] Federation with corporate IdP (SAML/OIDC)
- [ ] JIT elevation implemented
- [ ] API key rotation automated

### 35.3 Data Protection
- [ ] Encryption at rest for ALL storage services (default)
- [ ] Encryption in transit (TLS 1.2+) for ALL endpoints
- [ ] S3 Block Public Access at account level
- [ ] S3 bucket policies restrict access (no anonymous/authenticated)
- [ ] S3 Object Lock/Immutable Blob/WORM for critical data
- [ ] S3 versioning for ALL buckets
- [ ] EBS volumes encrypted by default
- [ ] RDS encrypted (AES-256 KMS)
- [ ] KMS key rotation enabled
- [ ] Secrets in Secrets Manager/Key Vault/Secret Manager
- [ ] Data classification labels automated (Macie/Purview/DLP)
- [ ] DLP policies for PII/PHI detection
- [ ] Backup encrypted (at rest and in transit)
- [ ] Retention policies aligned with legal requirements
- [ ] Secure deletion methods documented

### 35.4 Network Security
- [ ] VPCs using non-overlapping RFC 1918 CIDR ranges
- [ ] Security groups default-deny inbound; restrict outbound
- [ ] No SG with 0.0.0.0/0 for SSH (22), RDP (3389), databases
- [ ] NACLs as stateless defense layer
- [ ] VPC Flow Logs for ALL VPCs
- [ ] Public subnets restricted; no direct internet to private
- [ ] VPC endpoints for all cloud services
- [ ] WAF configured for all web-facing applications
- [ ] DDoS protection enabled (Shield Standard minimum)
- [ ] Network segmentation: separate subnets per tier
- [ ] Environment isolation: separate VPCs per env
- [ ] VPN/Direct Connect encrypted (IPsec or MACsec)
- [ ] Egress filtering implemented

### 35.5 Compute Security
- [ ] EC2 instances in private subnets (no public IPs)
- [ ] IMDSv2 enabled and enforced (hop limit=1)
- [ ] EBS volumes encrypted by default
- [ ] CIS benchmarks applied to all OS images
- [ ] Automated patching configured
- [ ] Security groups restrict inbound
- [ ] IAM roles attached (no access keys on instances)
- [ ] Instance termination protection
- [ ] Auto Scaling groups with health checks
- [ ] CloudWatch detailed monitoring enabled
- [ ] Golden AMI pipeline (hardened images rebuilt)

### 35.6 Container Security
- [ ] Minimal base images (distroless, scratch, alpine-slim)
- [ ] Image scanning in CI/CD (fail build on critical/high)
- [ ] No root user in containers
- [ ] Read-only root filesystem
- [ ] Linux capabilities dropped (ALL, then add needed)
- [ ] Images signed (Cosign/Docker Content Trust)
- [ ] RBAC for Kubernetes (no cluster-admin bindings)
- [ ] Network Policies (default-deny all)
- [ ] Pod Security Standards (Baseline/Restricted)
- [ ] Secrets from secret store (not hardcoded)
- [ ] Resource limits set
- [ ] Runtime detection (Falco, Sysdig)
- [ ] K8s audit logs shipped to SIEM
- [ ] etcd encrypted at rest

### 35.7 Logging and Monitoring
- [ ] CloudTrail/Activity Log/Audit Logs in all regions
- [ ] VPC Flow Logs for all VPCs
- [ ] DNS query logging enabled
- [ ] S3 server access logging for sensitive buckets
- [ ] WAF access logs enabled
- [ ] Database audit logs enabled
- [ ] Load balancer access logs enabled
- [ ] Logs centralized in SIEM
- [ ] Logs in immutable storage with sufficient retention
- [ ] Log access restricted to authorized personnel
- [ ] Threat detection enabled (GuardDuty/Defender/SCC)
- [ ] CSPM enabled
- [ ] Alerts for critical events (root activity, SG changes)
- [ ] Automated response (SOAR) configured
- [ ] Compliance monitoring continuous

### 35.8 Incident Response
- [ ] IR plan documented and tested quarterly
- [ ] Cloud-specific playbooks for common scenarios
- [ ] Forensic analysis environment pre-provisioned
- [ ] Evidence collection procedures documented
- [ ] Communication plan (internal, legal, PR, regulators)
- [ ] Incident severity definitions and escalation procedures
- [ ] IR team trained on cloud-specific tools
- [ ] Automated containment actions tested
- [ ] Breach notification procedures (GDPR/HIPAA/CCPA)
- [ ] Post-incident review process
- [ ] Tabletop exercises quarterly
- [ ] Root cause analysis process documented

### 35.9 Compliance
- [ ] Cloud provider certifications reviewed
- [ ] Shared responsibility matrix documented
- [ ] BAA/DPA in place (if handling PHI/PII)
- [ ] Data residency requirements identified/enforced
- [ ] Access to compliance reports verified
- [ ] Regulatory mappings documented
- [ ] Continuous compliance monitoring configured
- [ ] Compliance evidence collected and preserved
- [ ] Audit schedule defined
- [ ] Remediation process for non-compliant resources

### 35.10 Vendor/Third-Party
- [ ] Cloud provider due diligence completed
- [ ] Vendor risk assessment (security, financial, operational)
- [ ] Contracts reviewed (SLA, DPA, MSA, right to audit)
- [ ] Sub-processor list reviewed and approved
- [ ] Provider incident notification procedures documented
- [ ] Exit strategy documented
- [ ] Provider certifications verified and current
- [ ] Security questionnaires (CAIQ, SIG) reviewed
- [ ] Regular vendor risk reviews (annual minimum)
- [ ] Vendor lock-in risks assessed/mitigated

---

## 36. Cloud Security for Specific Services

### 36.1 AWS S3 Deep Security Configuration

**S3 Security Layers**: Account Block Public Access → Bucket Policy → Bucket ACL → Object ACL → Encryption

**S3 Encryption Options**:
| Option | Key Management | Use Case |
|--------|----------------|----------|
| SSE-S3 | AWS manages keys | Default; basic compliance |
| SSE-KMS | KMS customer-managed keys | Audit key usage; key rotation control; cross-account |
| SSE-C | Customer-provided keys | Customer handles keys |
| DSSE-KMS | KMS (dual-layer) | Highest security; two encryption layers |

**S3 Security Evaluation Script**:
```bash
#!/bin/bash
BUCKET=$1
echo "=== Bucket: $BUCKET ==="

# Check Block Public Access
aws s3api get-public-access-block --bucket $BUCKET 2>/dev/null || echo "Not configured"

# Check encryption
aws s3api get-bucket-encryption --bucket $BUCKET 2>/dev/null || echo "No default encryption"

# Check versioning
aws s3api get-bucket-versioning --bucket $BUCKET 2>/dev/null || echo "Not configured"

# Check Object Lock
aws s3api get-object-lock-configuration --bucket $BUCKET 2>/dev/null || echo "Not configured"

# Check public ACL grants
PUBLIC=$(aws s3api get-bucket-acl --bucket $BUCKET \
  --query 'Grants[?Grantee.URI==`http://acs.amazonaws.com/groups/global/AllUsers`]' 2>/dev/null)
if [ -n "$PUBLIC" ]; then echo "⚠ PUBLIC ACL FOUND!"; else echo "No public ACL grants"; fi
```

### 36.2 AWS Lambda Deep Security Configuration

**Lambda Security Controls**:
- **Execution Role**: One role per function; no shared roles; no wildcards; least privilege
- **Reserved Concurrency**: Prevent denial of wallet (cost explosion from unexpected invocations)
- **VPC**: Lambda in VPC for private resources; VPC endpoints for AWS services
- **Secrets**: Secrets Manager/Parameter Store (never env vars)
- **Input Validation**: Validate ALL event sources (API GW, SQS, SNS, EventBridge, S3, DynamoDB Streams)
- **Function URL**: Use AWS_IAM auth or disable; enable CORS cautiously
- **DLQ**: Dead Letter Queue for failed invocations (SQS/SNS)
- **Logging**: CloudWatch Logs encrypted with KMS; X-Ray tracing (without sensitive data)
- **Dependencies**: Scan all layers and dependencies (Snyk/Trivy) before deployment

**Lambda Code Security Patterns**:
```python
# BAD — Insecure code
def lambda_handler(event, context):
    import subprocess
    user_input = event['body']['filename']
    result = subprocess.run(['cat', user_input], capture_output=True)  # Command injection!
    return {'statusCode': 200, 'body': result.stdout}

# GOOD — Secure code
import boto3, json, os, logging
from botocore.exceptions import ClientError

logger = logging.getLogger(); logger.setLevel(logging.INFO)

ALLOWED_ACTIONS = {'read', 'write'}

def validate_input(event):
    body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
    allowed_keys = {'filename', 'action'}
    extra = set(body.keys()) - allowed_keys
    if extra: raise ValueError(f"Unexpected keys: {extra}")
    if body.get('action') not in ALLOWED_ACTIONS:
        raise ValueError(f"Invalid action: {body.get('action')}")
    filename = body.get('filename', '')
    if not filename or '..' in filename or '/' in filename:
        raise ValueError("Invalid filename (path traversal)")
    return body

def lambda_handler(event, context):
    try:
        body = validate_input(event)
        bucket = os.environ['S3_BUCKET']
        response = s3.get_object(Bucket=bucket, Key=f"uploads/{body['filename']}")
        return {
            'statusCode': 200,
            'body': response['Body'].read().decode('utf-8')[:10240],
            'headers': {'Content-Type': 'text/plain'}
        }
    except ValueError as e:
        return {'statusCode': 400, 'body': str(e)}
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        return {'statusCode': 500, 'body': 'Internal error'}
```

### 36.3 Azure Functions Security
- **EasyAuth**: Built-in authentication (Azure AD, Google, Facebook, Twitter, Microsoft); enable for all HTTP functions
- **Authorization Levels**: Function key, host key, anonymous; always require key for HTTP triggers
- **Managed Identity**: Use system/user-assigned managed identity (not connection strings)
- **VNet Integration**: Access private resources; service endpoints/Private Link
- **Key Vault References**: `@Microsoft.KeyVault(SecretUri=...)` for secrets in app settings
- **IP Restrictions**: Restrict inbound traffic via Access Restrictions
- **Always On**: Premium/App Service Plan for production (avoid cold start latency)

### 36.4 Google Cloud Functions Security
- **Cloud IAM**: Function invocation permissions (allUsers, allAuthenticatedUsers, specific principals)
- **Ingress Settings**: Allow internal only; or internal and CLB
- **VPC Connector**: Serverless VPC Access for private resource connectivity
- **Secret Manager**: Mount secrets as volumes or environment variables
- **Service Account**: Per-function SA with least privilege (not default compute engine SA)
- **Environment Variables**: Encrypted at rest; never store secrets

---

## 37. Cloud Security for Specific Attack Types

### 37.1 SSRF in Cloud
**Cloud-Specific SSRF Targets**:
| Target | URL |
|--------|-----|
| AWS IMDSv1 | `http://169.254.169.254/latest/meta-data/iam/security-credentials/<role>` |
| Azure IMDS | `http://169.254.169.254/metadata/instance?api-version=2021-02-01` |
| GCP Metadata | `http://metadata.google.internal/computeMetadata/v1/` |

**SSRF Mitigations**:
```python
# Application-level SSRF protection
METADATA_IPS = {'169.254.169.254', '169.254.169.253', '169.254.169.250'}
METADATA_HOSTNAMES = {'metadata', 'metadata.google.internal', '169.254.169.254'}

def validate_url(url):
    from urllib.parse import urlparse
    parsed = urlparse(url)
    hostname = parsed.hostname
    if hostname.startswith('10.') or hostname.startswith('172.16') or \
       hostname.startswith('192.168') or hostname == 'localhost':
        raise ValueError("Private IP blocked")
    if hostname in METADATA_HOSTNAMES:
        raise ValueError("Metadata endpoint blocked")
    return True
```

**Infrastructure SSRF Protection**:
- IMDSv2 (required, hop limit=1)
- VPC endpoint policies (restrict S3/Secrets to VPC only)
- Security groups blocking metadata endpoint from non-EC2 services
- WAF rules blocking metadata endpoint URLs
- Lambda@Edge / CloudFront Functions to filter request headers

### 37.2 IAM Privilege Escalation

**Dangerous Permissions (Escalation Vectors)**:
| Technique | Description | Mitigation |
|-----------|-------------|------------|
| PassRole | Attach admin role to EC2/Lambda | Restrict with `iam:PassedToService` condition |
| CreatePolicyVersion | Create new version of policy with full access | Deny `iam:SetDefaultPolicyVersion` |
| UpdateAssumeRolePolicy | Allow external principal to assume role | Restrict `iam:UpdateAssumeRolePolicy` |
| CreateAccessKey | Create access key for another user | Monitor with CloudTrail alerts |
| Lambda Layer Injection | Modify layer code for all functions | Restrict `lambda:UpdateFunctionCode` |
| CloudFormation Stack | Create stack with admin role | Limit `iam:PassRole` for CFN |

**Detection Queries**:
```bash
# Detect PassRole abuse
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=PassRole \
  --query 'Events[?contains(CloudTrailEvent, `ec2.amazonaws.com`)]'

# Detect CreatePolicyVersion with admin permissions
aws cloudtrail lookup-events --lookup-attributes AttributeKey=EventName,AttributeValue=CreatePolicyVersion \
  --query 'Events[?contains(CloudTrailEvent, `\"Action\":\"*\"`)]'
```

### 37.3 API Security Attacks
| Attack | Description | Protection |
|--------|-------------|------------|
| BOLA/IDOR | Accessing other users' objects via predictable IDs | UUIDs; ownership validation; API Gateway authorizers |
| Mass Assignment | Modifying unintended properties | Explicit allow-list of fields; DTOs |
| Rate Limit Bypass | Exceeding rate limits | WAF rate limiting; API Gateway throttling; Lambda reserved concurrency |
| API Key Leakage | Exposed keys in code/logs/repos | Key rotation; least privilege; scanning (GitLeaks) |
| JWT Manipulation | Algorithm none, weak key | Validate algorithm; strong keys; short expiry |

---

## 38. Cloud Security Logging Architecture

### 38.1 Centralized Logging Architecture (AWS)
```
Security Tooling Account
  └── Central S3 Bucket (immutable, Object Lock, KMS encrypted)
  │   ├── /aws/cloudtrail/ (all accounts, all regions)
  │   ├── /aws/vpc-flow-logs/ (all VPCs)
  │   ├── /aws/config/ (resource config history)
  │   └── /aws/guardduty/ (findings)
  └── Security Hub + GuardDuty (delegated admin)
  └── SIEM (OpenSearch/Splunk/Datadog)
  └── SOAR (EventBridge → Lambda)
  
Accounts send logs via:
  └── CloudTrail Organization Trail
  └── GuardDuty delegated admin
  └── Config aggregator
```

**Log Retention Tiering**:
| Log Type | Hot (SIEM) | Warm (S3 Std) | Cold (Glacier) | Archive (D Archive) |
|----------|-----------|--------------|----------------|-------------------|
| CloudTrail | 30 days | 90 days | 1-3 years | 3-7+ years |
| VPC Flow Logs | 14 days | 30 days | 90 days | 1 year |
| DNS Logs | 30 days | 90 days | 1 year | 3 years |
| S3 Access Logs | 14 days | 90 days | 1 year | 3 years |
| WAF Logs | 30 days | 90 days | 1 year | 3 years |
| GuardDuty | 90 days | 1 year | 3 years | 5 years |

**Log Protection**: Encrypted (KMS); integrity validated (CloudTrail SHA-256); immutable (Object Lock); access audited (meta-audit)

---

## 39. Cloud Security for Data Pipelines

### 39.1 Data Pipeline Security Fundamentals
**Secure Pipeline Components**: Source → Ingestion (TLS, Auth, Rate Limit) → Processing (Encrypt, Validate, Isolate) → Storage (Encrypt, Data Class, Retention, Immutable) → Consumption (Access Control, MFA, DLP, Audit)

**Pipeline Security Threat Model**:
| Threat | Example | Mitigation |
|--------|---------|------------|
| Data injection | Malformed/poisoned data | Schema validation, input sanitization, type checking |
| Data leakage | Unauthorized consumer | Access control, DLP, encryption, audit logging |
| Tampering | Man-in-the-middle during transit | TLS 1.2+, message signing, integrity checksums |
| Replay attack | Replayed events | Idempotency keys, deduplication, sequence numbers |
| Resource exhaustion | DoS on ingestion | Rate limiting, provisioning, auto-scaling, quotas |
| Insider threat | Authorized user exfiltration | Data classification, UEBA, access logging, separation of duties |

**Encryption Strategy by Pipeline Stage**:
| Stage | At Rest | In Transit | Notes |
|-------|---------|------------|-------|
| Source | Provider-managed KMS | TLS 1.2+ (HTTPS/TLS) | Database TDE or CMEK |
| Ingestion | KMS (SQS/Kinesis/EventHub) | TLS 1.2+ | Server-side encryption |
| Processing | Ephemeral (tmpfs/encrypted) | TLS for inter-service | In-memory (RAMSES for sensitive) |
| Storage | KMS/CMEK (AES-256) | TLS 1.2+ | Bucket-level encryption policies |
| Consumption | - | TLS 1.2+ (API calls) | End-to-end encryption for sensitive |

### 39.2 AWS Batch and ETL Pipeline Security

**AWS Glue Security Deep Dive**:
- **Data Catalog**: KMS encryption for catalog metadata; IAM policies per database/table; Lake Formation column-level security
- **Jobs (Spark/Python)**: Security configuration for KMS; CloudWatch logs encrypted; job parameters for secrets via Secrets Manager
- **Connections**: JDBC connections via VPC; SSL-enabled database connections; network isolation for data sources
- **Crawlers**: IAM role with least privilege; only crawl specified paths; exclude sensitive patterns
- **Bookmarks**: KMS encrypted; track processed data (prevents reprocessing)
- **Schema Registry**: Schema validation (avro/json/protobuf); compatibility checks (backward/forward/full)

**AWS EMR Security Deep Dive**:
- **Encryption**: At rest (EBS/KMS), in transit (TLS for Spark/Hive/HBase inter-node, S3-distcp encrypted)
- **Authentication**: Kerberos (MIT, AD); LDAP-backed; IAM roles for EC2 (instance profile)
- **Authorization**: Apache Ranger (HDFS, Hive, HBase); EMRFS authorization (S3 bucket policies based on IAM role)
- **Network**: VPC with security groups; private subnets for master/core/task nodes; service access via VPC endpoints
- **Logging**: Cluster logs to S3 (server access logs enabled); CloudWatch integration
- **Data Isolation**: EMRFS consistent view; S3 encryption client-side; per-cluster ephemeral storage encrypted
- **Security Configurations**: Pre-built security configurations (e.g., security-configuration-kerberos-minimalist.json for Kerberos setup)

**AWS Data Pipeline Security**:
- **Pipeline Definition**: IAM roles for pipeline execution; S3 staging directories encrypted; CloudWatch logging
- **Data Nodes**: S3 data nodes encrypted (SSE-S3/SSE-KMS); RDS/Redshift nodes with security group isolation
- **Activities**: EC2/E MR activities in VPC; logging to S3; pre/post conditions validated
- **Scheduling**: Frequency-based or on-demand; error handling for retries/alerts
- **Preconditions**: Validate source availability (table exists, data ready) before processing
- **Lifecycle**: Auto-terminate clusters after inactivity; delete temporary data per retention policy

### 39.3 Streaming Data Security

**Kinesis Data Streams Security**:
- **Encryption at Rest**: Server-side encryption with KMS (SSE-KMS); customer master key per stream
- **Encryption in Transit**: TLS for PutRecord/GetRecord; VPC endpoints for private access
- **Authentication**: IAM policies for PutRecord/GetRecord/ListStreams; conditions on source VPC, source IP, MFA
- **Authorization**: IAM-based; no native resource-based policies; use VPC endpoints with conditions
- **Monitoring**: CloudTrail data events (PutRecord, GetRecords, SplitShard, MergeShards); CloudWatch metrics (IncomingBytes, OutgoingBytes, UserErrors)
- **Data Retention**: Default 24h; up to 8760h (365 days); early data deletion prevention
- **Enhanced Fan-Out**: Registered consumers with dedicated throughput; IAM per-consumer
- **Resharding**: Split/merge shards; triggers CloudTrail event; monitor for unauthorized resharding (DoS)
- **KCL (Kinesis Client Library)**: Worker authentication with IAM; checkpointing to DynamoDB (encrypted)

**Kinesis Data Firehose Security**:
- **Delivery Streams**: KMS encryption for destination (S3/Redshift/Elasticsearch/Splunk)
- **Data Transformation**: Lambda function assumes IAM role with least privilege; function logs in CloudWatch
- **Buffering**: Size/interval-based; compression (GZIP/Snappy/ZSTD) before encryption
- **Error Handling**: Failed records to S3 error bucket (DLQ pattern); Lambda retries
- **Destination Security**: S3 with bucket policy (KMS decrypt for Redshift); Elasticsearch with VPC and IAM; Splunk HEC token authentication
- **Source Validation**: CloudWatch metrics for failed transformations; processing time alerts
- **Schema Conversion**: Parquet/ORC conversion with Glue Data Catalog integration

**Kinesis Data Analytics Security**:
- **Application**: IAM execution role; KMS for state store; CloudWatch logging
- **Input/Output**: Kinesis stream or Firehose delivery stream consumption
- **State**: Application state stored durably; encrypted at rest; can be snapshotted
- **Subnet**: VPC with private subnets; security groups for Flink/Kinesis Processors

### 39.4 Kafka/MSK Security Deep Dive

**Amazon MSK (Managed Streaming for Apache Kafka)**:
- **Encryption at Rest**: KMS per-broker EBS encryption (AES-256); configurable per-cluster
- **Encryption in Transit**: TLS 1.2 for client-broker, broker-broker, controller-broker; mutual TLS authentication
- **Authentication Options**:
  - **IAM Access Control** (best practice): Use IAM policies to authorize Kafka actions; integrates with AWS IAM
  - **SASL/SCRAM** (username/password): Store credentials in AWS Secrets Manager; automatic rotation
  - **Mutual TLS** (mTLS): Certificate-based authentication; ACM PCA integration for CA
  - **Unauthenticated**: Not recommended (dev/test only)
- **Authorization**: IAM policies (with IAM auth) or Apache Kafka ACLs (with SCRAM/mTLS)
- **Network Security**:
  - VPC with private subnets; multi-AZ for HA
  - Security groups restrict broker access to producers/consumers
  - VPC endpoints for cross-VPC access (not supported natively; use VPC peering/Transit Gateway)
  - Public access disabled by default
- **Broker Configuration**:
  - `auto.create.topics.enable=false` (prevent rogue topic creation)
  - `delete.topic.enable=false` (prevent accidental deletion)
  - `unclean.leader.election.enable=false` (prevent data loss)
  - `min.insync.replicas=2` (maintain write availability)
  - `default.replication.factor=3` (fault tolerance)
  - `log.retention.bytes` and `log.retention.hours` (storage limits)
- **Monitoring**: CloudWatch metrics (BytesInPerSec, BytesOutPerSec, CPUUtilization, KafkaDataLogsDiskUsed); Prometheus JMX Exporter; Broker logs to CloudWatch
- **Backup**: No native backup; use MirrorMaker 2 for cross-region replication; Kafka Connect for S3 sink; Kinesis connector
- **Upgrades**: Rolling upgrades (zero downtime); configuration changes without restart
- **Client Security**:
  - Use latest Kafka client libraries (TLS 1.2+)
  - DNS resolution via Route 53 private hosted zones
  - Java security properties file for TLS truststore/keystore
  - Client-side encryption for sensitive data (application-level encryption)

**Confluent Cloud Security**:
- Private network (AWS PrivateLink, Azure Private Link, GCP Private Service Connect)
- Role-based access control (RBAC) at organization, environment, cluster, topic level
- Audit logs for all API operations
- Data governance (Schema Registry with encryption)
- Stream lineage for data provenance

**Self-Managed Kafka Security**:
- OS-level firewall (iptables/security groups restrict broker ports 9092, 2181, 8083, 8081)
- ZooKeeper TLS (port 2181 with SSL)
- SASL mechanisms: GSSAPI (Kerberos), PLAIN (not recommended), SCRAM-SHA-256/512, OAUTHBEARER
- Delegation tokens for long-running clients
- Client quotas (network, request rate, connection) to prevent DoS
- Rate limiting per client ID for producer and consumer

---

## 40. Cloud Security DR

### 40.1 Security Controls DR Strategy
| Service | DR Strategy | RTO/RPO Impact |
|---------|-------------|----------------|
| IAM | Global; survives region failure | No impact |
| CloudTrail | Multi-region trail; organization trail | <15 min log delivery |
| GuardDuty | Enable in all regions + delegated admin | Real-time detection |
| Security Hub | Cross-region aggregator (central account) | Near-real-time |
| KMS | Multi-region keys (MRK) with automatic replication | <5 min promotion |
| Secrets Manager | Cross-region replication (manual or automatic) | Varies (hours for manual) |
| WAF | Recreate rules in DR region via IaC (CloudFormation/Terraform) | Per deployment |
| VPC | Replicate via CloudFormation/Terraform (SG, NACL, subnets, routes) | Per deployment |
| Logging | S3 CRR for logs to DR region; cross-region CloudWatch subscription | <15 min replication |
| Config | Multi-region delivery channel; aggregator in DR region | Near-real-time |
| EC2 | AMI replication (cross-region); auto scaling in DR; instance scheduler | Varies (RTO 15min-4h) |
| RDS | Cross-region read replica; Aurora Global Database; manual snapshot copy | RTO 1min (Aurora) to 1h |
| Route53 | Health checks + failover routing; active-passive or active-active | 0s DNS propagation |
| ACM | Request/reimport certificates in DR region; managed renewal | Manual per region |
| Systems Manager | Automation documents replicated; Parameter Store tier replicated | Per deployment |
| S3 | Cross-region replication (CRR) with correct IAM; S3 Object Lambda for transforms | 15min SLA (most within min) |

### 40.2 DR Architecture Patterns

**Active-Passive (Pilot Light)**:
- Core services run at minimum size in DR region (single AZ, no app servers)
- Data continuously replicated (RDS cross-region replica, S3 CRR)
- On failover, scale up DR infrastructure (auto scaling, increase capacity)
- Route53 health check fails → failover to DR
- **RTO**: 15-60 minutes; **RPO**: 1-5 minutes (RDS replication lag)
- **Cost**: ~10-20% of production (minimum run+replication)

**Active-Passive (Warm Standby)**:
- DR region runs at reduced size (single instance instead of cluster)
- Data replicated (same as pilot light); DR environment tests periodically
- Route53 weighted/failover routing; automated scaling on failover
- **RTO**: 5-15 minutes; **RPO**: 1-5 minutes
- **Cost**: ~40-50% of production

**Active-Active (Multi-Region)**:
- Application deployed and serving traffic from multiple regions
- Route53 latency-based or geolocation routing
- Data synchronized bidirectionally (RDS cross-region read replicas, DynamoDB global tables, S3 CRR)
- User sessions distributed (ElastiCache global datastore, DynamoDB global tables)
- **RTO**: Near-zero; **RPO**: <1 second to 5 seconds
- **Cost**: 2x production (running full stack in two regions)
- **Security Complexity**: KMS MRK required; consistent IAM across regions; synchronized logging

### 40.3 DR Security Configuration Per Provider

**AWS DR Security Setup**:
```bash
# Enable CloudTrail in DR region
aws cloudtrail create-trail --name security-trail-dr \
  --s3-bucket-name my-security-logs-dr \
  --is-multi-region-trail --enable-log-file-validation \
  --kms-key-id alias/cloudtrail-key-dr

# Enable GuardDuty in DR region
aws guardduty create-detector --enable --finding-publishing-frequency FIFTEEN_MINUTES

# Enable Security Hub in DR region
aws securityhub enable-security-hub --enable-default-standards

# Replicate KMS key (manual for imported key material; automatic for MRK)
aws kms replicate-key --key-id mrk-1234567890 \
  --replica-region eu-west-1 --description "DR MRK"
```

**Azure DR Security Setup**:
```powershell
# Enable Defender for Cloud in paired region
Set-AzSecurityPricing -Name "VirtualMachines" -Tier "Standard" -Subdomain "DR"

# Configure Azure Site Recovery for VMs
New-AzRecoveryServicesVault -Name "DRVault" -ResourceGroupName "dr-rg" -Location "East US"

# Enable Log Analytics in DR region
New-AzOperationalInsightsWorkspace -ResourceGroupName "dr-rg" -Name "dr-log-analytics" -Location "East US"

# Replicate Key Vault (manual - Key Vault does not auto-replicate)
Export-AzKeyVaultSecret -VaultName "prod-vault" -OutputFile "secrets.json"
Import-AzKeyVaultSecret -VaultName "dr-vault" -InputFile "secrets.json"
```

**GCP DR Security Setup**:
```bash
# Enable Security Command Center in DR project
gcloud services enable securitycenter.googleapis.com --project=dr-project

# Create Cloud Armor policy in DR region
gcloud compute security-policies create dr-waf-policy --project=dr-project

# Enable VPC Flow Logs in DR VPC
gcloud compute networks subnets update dr-subnet --enable-flow-logs

# Replicate secrets to DR project (manual)
gcloud secrets versions access latest --secret="db-password" --project=prod-project \
  | gcloud secrets versions add db-password --data-file=- --project=dr-project
```

### 40.4 DR Testing and Validation

**DR Testing Frequency**:
| Test Type | Frequency | Scope |
|-----------|-----------|-------|
| Tabletop exercise | Quarterly | Walk through DR plan; review runbooks; discuss scenarios |
| Component failover | Monthly | Test individual component (RDS failover, Route53 failover) |
| Regional failover | Semi-annually | Full regional failover in non-production environment |
| Full DR drill | Annually | Production failover (during maintenance window) or full non-prod failover |

**DR Test Validation Checklist**:
- [ ] IAM policies replicated and functional in DR region
- [ ] KMS multi-region keys can be promoted in DR region
- [ ] Secrets Manager replicas accessible by DR workloads
- [ ] CloudTrail logging to security account from DR region
- [ ] GuardDuty active and sending findings to security account
- [ ] Security Hub standards evaluated in DR region
- [ ] WAF rules deployed and blocking expected traffic
- [ ] VPC flow logs sending to central logging
- [ ] SIEM receiving logs from DR environment
- [ ] Incident response team can access DR environment
- [ ] IR playbooks work with DR region IP ranges and resource names
- [ ] Compliance controls pass in DR region (same controls as production)
- [ ] Monitoring dashboards populated with DR data
- [ ] Alerting configured for DR environment security events
- [ ] Backup/restore tested in DR region
- [ ] Secrets rotation works in DR region

### 40.5 DR Security Incident Response

**DR Activation Criteria**:
- Production region unavailable for >15 minutes (application-level)
- Data plane API degradation in primary region
- Compliance violation due to region-specific regulation
- Security incident requiring environment isolation (compromise of primary region)

**DR Security Incident Playbook**:
1. **Declare DR Event**: Notify security team; activate DR runbook
2. **Verify DR Readiness**: Check KMS MRK availability, secrets replication, GuardDuty status
3. **Fail Over DNS**: Update Route53 failover record; monitor health checks
4. **Activate DR Workloads**: Scale up DR environments; validate application function
5. **Validate Security Posture**: Run compliance scan (Config rules, Security Hub, CSPM); verify all controls active
6. **Redirect Logging**: Ensure logs from DR region flowing to SIEM; verify security events visible
7. **Monitor for Attacks**: Increase monitoring during transition; watch for attack during failover window
8. **Declare Stabilized**: All systems operational; security posture validated; monitoring confirmed
9. **Plan Failback**: After primary region restored, plan controlled failback with security validation
10. **Post-Mortem**: Document security gaps discovered during failover; update DR plan

### 40.6 Multi-Region Data Sovereignty

**Data Residency Controls for DR**:
- **AWS**: S3 Object Lock (compliance mode) for data retention; Organizations SCP preventing data movement outside approved regions
- **Azure**: Policy for allowed locations; Azure Blueprints with region restrictions; Customer Lockbox for access control
- **GCP**: Organization Policy constraints (`constraints/gcp.resourceLocations`); VPC Service Controls per region; Data Sovereignty via Assured Workloads

**Compliance-Conscious DR Architecture**:
- Replicate only to in-region or approved geo (e.g., EU-to-EU only)
- Use CMEK (customer-managed encryption keys) with region-restricted key material
- Implement data classification: sensitive data does not leave original region; mask/redact before cross-region transfer
- Audit all cross-region data access (CloudTrail, data access logs)
- Consider active-passive within same region (different AZ) for data sovereignty requirements

---

## 41. Cloud Security Economics

### 41.1 Cost of Cloud Breach (IBM 2024)
| Component | Average Cost |
|-----------|-------------|
| Detection and Escalation | $1.58M |
| Post-Breach Response | $1.08M |
| Notification | $0.89M |
| Lost Business | $1.45M |
| **Total** | **$4.88M** |

### 41.2 Security Cost Optimization
1. **Use free tiers**: CloudTrail mgmt events (free), GuardDuty 30-day trial, Security Hub 30-day trial
2. **Tighten scope**: Only enable data events for sensitive S3 buckets (not all)
3. **Optimize log retention**: 90d hot → 1y warm → 3y cold → 7y archive
4. **Consolidate tools**: Replace multiple overlapping tools with integrated platforms
5. **Automate**: Reduce manual security analyst hours via automated response
6. **Tag for cost allocation**: Track security costs per environment; identify over-provisioning
7. **Savings Plans**: Reserved capacity for security appliances (NGFW instances)
8. **Eliminate duplicate detection**: One tool per category; disable redundant controls

---

## 42. Cloud Security for Serverless Data Processing

### 42.1 Event-Driven Security Architecture
**Secure Event Pipeline**:
```
Event Source → EventBridge (filter, validate) → SQS (encrypted, DLQ) → Lambda (least privilege, VPC) → Storage (encrypted)
```

**Security Controls**:
- EventBridge: Filter on source, detail-type, severity; only process allowed events
- SQS: KMS encryption, DLQ for failures, max receive count, visibility timeout
- Lambda: One function per event type; reserved concurrency; VPC; Secrets Manager
- Step Functions: State machine for workflow orchestration; audited transitions; error handling

### 42.2 Step Functions Security Workflow
```json
{
  "Comment": "Automated Incident Response",
  "StartAt": "ClassifySeverity",
  "States": {
    "ClassifySeverity": {
      "Type": "Choice",
      "Choices": [
        {"Variable": "$.finding.Severity", "StringEquals": "CRITICAL", "Next": "NotifySecurityTeam"},
        {"Variable": "$.finding.Severity", "StringEquals": "HIGH", "Next": "AutoInvestigate"}
      ],
      "Default": "LogAndComplete"
    },
    "NotifySecurityTeam": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn.$": "$.AlertTopic",
        "Message": {"Severity": "CRITICAL", "Finding.$": "$.finding"},
        "Subject": "CRITICAL: Security Incident"
      },
      "Next": "WaitForApproval"
    },
    "ExecuteContainment": {
      "Type": "Parallel",
      "Branches": [
        {"StartAt": "QuarantineInstance", ...},
        {"StartAt": "DisableKeys", ...}
      ],
      "Next": "LogCompletion"
    }
  }
}
```

---

## 43. Cloud Security Services by Provider

### 43.1 AWS Security Services
| Service | Category | Pricing |
|---------|----------|---------|
| IAM | Identity | Free |
| Organizations | Governance | Free |
| CloudTrail | Logging | Free (mgmt), paid (data events) |
| Config | Compliance | Per config item, rule evaluation |
| Security Hub | CSPM | Per control check, finding |
| GuardDuty | Threat Detection | Per GB log analyzed |
| Inspector | Vulnerability | Per host assessment |
| WAF | Network Security | Per ACL, per request |
| Shield | DDoS | Standard free; Advanced $3000/mo |
| Network Firewall | Network Security | Per endpoint, per GB |
| KMS | Encryption | Per key, per operation |
| CloudHSM | Encryption | Per HSM per hour |
| Secrets Manager | Secrets | Per secret, per API call |
| Macie | Data Security | Per GB classified |
| Detective | Investigation | Per GB analyzed |
| Audit Manager | Compliance | Per resource, per assessment |
| Artifact | Compliance | Free |
| Systems Manager | Operations | Per instance, per operation |
| Backup | Backup | Per backup, per storage |

### 43.2 Azure Security Services
| Service | Category | Pricing |
|---------|----------|---------|
| Azure AD / Entra ID | Identity | Free tier; P1/P2 per user/month |
| RBAC | Access Control | Free |
| Policy | Governance | Free |
| Defender for Cloud | CSPM/CWPP | Free CSPM; paid plans per workload |
| Sentinel | SIEM/SOAR | Per GB ingested |
| Monitor | Monitoring | Per GB ingested |
| Activity Log | Logging | Free (90-day) |
| Key Vault | Encryption | Per transaction; premium for HSM |
| WAF (App GW/Front Door) | Network Security | Per hour + per GB |
| DDoS Protection | DDoS | Standard: $2944/month |
| Firewall | Network Security | Per hour + per GB |
| Private Link | Network | Per endpoint per hour |
| Purview | Data Governance | Per asset |
| Backup | Backup | Per protected instance |
| Site Recovery | DR | Per protected instance |
| Information Protection | Data Security | Per user (E5) |

### 43.3 GCP Security Services
| Service | Category | Pricing |
|---------|----------|---------|
| Cloud IAM | Identity | Free |
| Cloud Identity | Identity | Free Basic; Premium per user/month |
| Organization Policy | Governance | Free |
| Security Command Center | CSPM/Threat | Standard free; Premium per asset |
| Cloud Audit Logs | Logging | Admin free; Data Access paid |
| Cloud Logging | Monitoring | First 50GB free; $0.50/GB |
| Cloud KMS | Encryption | Per key version, per operation |
| Cloud HSM | Encryption | Per key version (premium) |
| Cloud Armor | Network Security | Per policy; Managed Protection Plus |
| Cloud Firewall | Network Security | Free |
| VPC Service Controls | Network | Free per perimeter |
| Secret Manager | Secrets | Per secret version, per access |
| Sensitive Data Protection | Data Security | Per GB, per transformation |
| Chronicle | SIEM | Per GB ingested |
| Assured Workloads | Compliance | Per project |
| Access Transparency | Audit | Per project per month |

---

## 44. Cloud Security for DNS and CDN

### 44.1 DNS Security Fundamentals
**DNS Attack Types**: Spoofing/Poisoning, Tunneling, DDoS, Subdomain Takeover, Domain Hijacking, DNS Rebinding, NXDOMAIN attacks, Random subdomain attacks, DNS Amplification

**DNS Security Controls by Provider**:

**AWS Route53 Security**:
- **DNSSEC signing** (prevents spoofing, cache poisoning): Uses KSM (key signing key) and ZSK (zone signing key) managed via KMS; enables origin authentication of DNS data
- **DNS query logging** to S3 (immutable, encrypted, with retention policy): Logs source IP, query type, response code, EDNS client subnet; CloudWatch metric filter for anomalies
- **Resolver DNS Firewall**: Block malicious domains (cryptomining, malware, ransomware, C2); domain lists from AWS Managed (proofpoint/threat-to-know) or custom; rule groups associated with VPCs
- **Private hosted zones** for internal DNS: Split-view DNS (internal != external); conditional forwarding for hybrid networks
- **Route53 Resolver**: Inbound/outbound endpoints for hybrid DNS resolution; forwarding rules for on-premises DNS; query logging for all resolver traffic
- **Health checks**: HTTP/HTTPS/TCP health checks for failover routing; calculated health checks (composite of multiple checks); SNI support for HTTPS
- **Traffic Flow**: Policy-based routing (geoproximity, latency, weighted); failover routing with health check; multi-value answer routing
- **Domain Registration**: Transfer lock, privacy protection, auto-renew; IAM policies to prevent unauthorized domain transfers

**Azure DNS Security**:
- Azure DNS (domain hosting) with Azure RBAC; private DNS zones for internal resolution
- Azure DNS Private Resolver for hybrid connectivity
- Azure Firewall DNS proxy (intercept DNS queries for inspection)
- DNS analytics via Azure Monitor; query logging to Log Analytics
- Alias records (prevent dangling DNS by linking to Azure resources)
- Conditional forwarding rules for on-premises DNS

**GCP Cloud DNS Security**:
- DNSSEC for managed zones (automatic or manual signing)
- Cloud DNS logging to Cloud Logging (queries, response codes)
- Private zones and forwarding zones for internal resolution
- Server policy (alternative NS delegation; rate limiting)
- IAM roles per zone (dns.admin, dns.reader, dns.viewer)
- VPC peering for private DNS across projects

**Azure Front Door / GCP External HTTP(S) LB + Cloud CDN**:
- Azure Front Door WAF policy (OWASP, rate limiting, geo-filtering)
- GCP Cloud CDN with Cloud Armor (WAF, DDoS protection)
- GCP Cloud CDN signed URLs/ cookies for private content
- Both: HTTPS enforcement, security headers, logging to SIEM

**Subdomain Takeover Prevention**:
```bash
# AWS: Scan for dangling DNS records
aws route53 list-resource-record-sets --hosted-zone-id ZONE_ID \
  --query 'ResourceRecordSets[?Type==`CNAME` || Type==`A`]' \
  | grep -i "s3-website\\|cloudfront\\|elb\\|azure\\|trafficmanager\\|cdn"

# Azure: Scan for dangling DNS
az network dns record-set list --resource-group my-rg --zone-name example.com \
  --query "[?type=='CNAME' || type=='A']" \
  | grep -i "azurewebsites\\|trafficmanager\\|cloudapp\\|cdn"

# GCP: Scan for dangling DNS
gcloud dns record-sets list --zone=my-zone --format="json" \
  | jq '.[] | select(.type=="CNAME" or .type=="A")'
```

**DNS Firewall (Outbound Filtering)**:
```bash
# AWS Route53 Resolver DNS Firewall
aws route53resolver create-firewall-rule-group --name "block-malicious-domains"
aws route53resolver associate-firewall-rule-group \
  --firewall-rule-group-id rfg-1234567890 \
  --vpc-id vpc-12345678 --priority 100

# Azure DNS proxy via Firewall
az network firewall policy rule-collection-group create \
  --name "DNSFilter" --policy-name "fw-policy" \
  --priority 100 --rule-collections @dns-rules.json

# GCP: Use Cloud NAT filtering or third-party DNS filtering
```

### 44.2 DNS Security Architecture Patterns

**Split-Horizon (Split-View) DNS**:
```
Public Zone (example.com):
  www.example.com → CloudFront (public)
  api.example.com → ALB (public)
  blog.example.com → CloudFront (public)

Private Zone (example.com):
  internal.example.com → Internal ALB (private)
  db.example.com → RDS endpoint (private)
  secrets.example.com → Secrets Manager VPC endpoint
  s3.example.com → S3 VPC endpoint
```
- Internal resolvers use private zone; external resolvers use public zone
- Prevents internal service discovery from external attackers
- Requires distinct DNS names for internal vs external services

**DNS-Based Compliance Controls**:
- Log all DNS queries to SIEM for threat detection and compliance audit
- DNS analytics for anomaly detection: unexpected TLDs, high entropy domains (DGA), beaconing patterns
- DNSSEC for all public zones (prevents DNS spoofing for compliance like PCI DSS Requirement 6.6)

### 44.3 CDN Security (CloudFront)
**Security Configuration**:
- **HTTPS enforced**: Redirect HTTP to HTTPS; viewer protocol policy (HTTPS-only); origin protocol policy (HTTPS-only)
- **Security headers**: HSTS (1 year, includeSubdomains, preload), CSP (strict policy), X-Frame-Options (DENY), X-Content-Type-Options (nosniff), Referrer-Policy (no-referrer), Permissions-Policy, X-XSS-Protection (deprecated but included for legacy)
- **WAF association**: OWASP Top 10 rules, rate limiting (per IP, per session), IP reputation lists, SQLi/XSS body inspection, bot control (CAPTCHA, block, challenge)
- **Geo-restriction**: Whitelist/blacklist countries; use with WAF geo match for more granular control
- **Signed URLs/Cookies**: For private content distribution; Canned policy (simple, same key for all) vs Custom policy (per-user restrictions, shorter validity); RSA key pairs via CloudFront Key Groups (not trusted signers which are legacy)
- **Origin Access Control (OAC)**: Restrict origin access to CloudFront only (replaces OAI for S3); works with S3, ALB, custom origins; uses AWS signature v4
- **Field-level encryption**: Encrypt sensitive fields (SSN, CC numbers) at edge using RSA public key; only backend with private key can decrypt; asymmetric encryption for data privacy
- **Real-time logs**: To Kinesis Data Streams for real-time monitoring, security analytics, and SIEM integration
- **Origin Shield**: Parent cache node aggregates requests from edge locations; reduces origin load, improves cache hit ratio; enable for origin protection against DDoS/scale events
- **Custom error responses**: No information leakage (don't expose internal error details, file paths, or stack traces); custom error pages
- **DDoS protection**: Shield Advanced for high-value distributions (cost protection, enhanced mitigation, DDoS Response Team access)
- **Lambda@Edge / CloudFront Functions**: Validate JWTs at edge; inject security headers; rewrite URLs; implement rate limiting per user; redirect to authentication endpoints
- **Origin failover**: Primary origin group + secondary origin group; automatic failover on 5xx errors
- **Continuous Deployment**: Invalidation of cached content after security updates; staged rollouts with CloudFront continuous deployment policy

**CDN Security Configuration Examples**:
```bash
# AWS CloudFront with OAC for S3
aws cloudfront create-distribution \
  --origin-domain-name my-bucket.s3.us-east-1.amazonaws.com \
  --origin-access-control-config-id oac-1234567890 \
  --default-root-object index.html \
  --viewer-protocol-policy redirect-to-https

# Azure Front Door WAF
az network front-door waf-policy create \
  --name "myWAFPolicy" --resource-group "myRG" --sku Premium_AzureFrontDoor \
  --mode Prevention --enabled-state Enabled

# GCP Cloud Armor with CDN
gcloud compute security-policies create my-cdn-policy \
  --description "WAF for CDN" --type CLOUD_ARMOR
gcloud compute backend-buckets create my-cdn-bucket \
  --gcs-security-policy my-cdn-policy --enable-cdn
```

**CDN DDoS Mitigation Stack**:
| Layer | Mitigation | Service |
|-------|------------|---------|
| L3/L4 | Volumetric DDoS (SYN flood, UDP amplification) | AWS Shield Standard/Advanced, Azure DDoS Protection, GCP Cloud Armor |
| L7 | Application DDoS (HTTP flood, slow loris) | WAF rate limiting, bot control, QoS rules |
| Edge | Traffic absorption | CDN edge caching (cache static content to reduce origin load) |
| Origin | Overload protection | Origin Shield, autoscaling, throttling |
| DNS | DNS amplification, NXDOMAIN flood | Route53 Shield, DNS Firewall, rate limiting |

### 44.4 Azure Front Door / GCP Cloud CDN Security

**Azure Front Door Security**:
- WAF policy (OWASP, rate limiting, geo-filtering, IP reputation, bot protection)
- Private Link support (origin access without public internet)
- WebSocket support (with WAF inspection)
- URL redirect/rewrite rules (canonical URLs, HTTPS enforcement)
- Caching rules (cache static; bypass for authenticated content)
- Azure DDoS Protection Standard for edge VNet
- Azure CDN (Standard from Microsoft) with WAF at edge locations

**GCP Cloud CDN / Cloud Armor Security**:
- Cloud Armor WAF (pre-configured OWASP rules, rate limiting, geo-based access, IP allow/deny)
- Cloud Armor Managed Protection Plus (advanced DDoS protection)
- Signed URLs and signed cookies for private content
- Cloud CDN with backend bucket (Cloud Storage) and backend service (LB)
- Origin authentication (Cloud Storage IAM permissions, signed headers for Compute Engine)
- Cache invalidation for content removal
- IAP (Identity-Aware Proxy) for authenticated origin access
- Cloud CDN logging to Cloud Logging for audit
- DDoS: Google Cloud Armor Adaptive Protection (ML-based DDoS detection)

---

## 45. Cloud Security Compliance Automation

### 45.1 Automated Evidence Collection (AWS)
| Control | Evidence Source |
|---------|----------------|
| Access Reviews | IAM Credential Report (scheduled Lambda) |
| Change Management | CloudTrail → CloudWatch → S3 (immutable) |
| Encryption at Rest | Config rules (encrypted-volumes, s3-bucket-sse-enabled) |
| Incident Response | GuardDuty → EventBridge → Security Hub → Jira/ServiceNow |
| Patch Management | Systems Manager Patch Reports → S3 |
| Vulnerability | Inspector → Security Hub → auto-create tickets |
| MFA Compliance | IAM credential report → compare → non-compliant report |
| Backup Verification | AWS Backup reports → validation job status |

### 45.2 Compliance Reporting as Code
```python
def generate_compliance_report():
    config = boto3.client('config')
    security_hub = boto3.client('securityhub')
    
    report = {
        'report_date': datetime.now().isoformat(),
        'frameworks': {}
    }
    
    # CIS Benchmark Compliance
    cis_results = config.describe_compliance_by_config_rule()
    cis_rules = [r for r in cis_results['ComplianceByConfigRules'] 
                 if 'cis' in r['ConfigRuleName'].lower()]
    report['frameworks']['CIS'] = {
        'total': len(cis_rules),
        'compliant': len([r for r in cis_rules if r['Compliance']['ComplianceType'] == 'COMPLIANT']),
        'non_compliant': len([r for r in cis_rules if r['Compliance']['ComplianceType'] == 'NON_COMPLIANT']),
        'percentage': round(len([r for r in cis_rules if r['Compliance']['ComplianceType'] == 'COMPLIANT']) / len(cis_rules) * 100, 2)
    }
    
    # Security Hub Compliance
    hub_results = security_hub.get_findings(
        Filters={'ComplianceStatus': [{'Value': 'FAILED', 'Comparison': 'EQUALS'}]},
        MaxResults=100
    )
    report['frameworks']['SecurityHub'] = {
        'total_failed': len(hub_results['Findings']),
        'controls': {}
    }
    return report
```

---

## 46. Cloud Security for Third-Party Integrations

### 46.1 Third-Party Risk Management Framework

**Third-Party Classification**:
| Tier | Risk Level | Examples | Controls Required |
|------|------------|----------|-------------------|
| Tier 1 | Critical | SIEM/SOAR, IdP, CI/CD, source control, cloud billing | Full security review, contract SOW, SOC 2, penetration test reports |
| Tier 2 | High | Monitoring tools, logging services, incident management | SOC 2, security questionnaire, contract security clauses |
| Tier 3 | Medium | Analytics, CRM, marketing automation | Security questionnaire, vendor risk assessment |
| Tier 4 | Low | Public SaaS (general productivity) | Terms of service review |

**Third-Party Integration Security Controls**:
1. **Least Privilege IAM**: Cross-account role with specific actions, resources, and conditions
2. **SCP Restrictions**: Deny IAM modifications, org changes, billing access at organization level
3. **Network Restrictions**: Source IP conditions (aws:SourceIp), VPC endpoints only (aws:SourceVpce)
4. **Data Segmentation**: Separate buckets/tables with prefix restrictions; no wildcard access to all data
5. **Monitoring**: CloudTrail alerts for third-party API calls; GuardDuty for unusual patterns
6. **Rotation**: Rotate shared credentials on schedule or on incident; auto-rotation via Secrets Manager
7. **Revocation**: Immediate revocation capability (delete role, blocklist tokens, revoke OAuth grants)
8. **Time-Boxing**: IAM with `aws:CurrentTime` condition for temporary access windows
9. **Notification**: SNS alert when third-party assumes role; Slack/Teams integration for awareness
10. **Data Minimization**: Share minimum data required; use views/masks/redaction; filter columns/rows

**Third-Party IAM Policy** (AWS):
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {"AWS": "arn:aws:iam::PARTNER_ACCOUNT:root"},
      "Action": "sts:AssumeRole",
      "Condition": {
        "StringEquals": {
          "aws:SourceIdentity": "partner-service-v2",
          "aws:SourceAccount": "PARTNER_ACCOUNT"
        },
        "Bool": {"aws:MultiFactorAuthPresent": "true"},
        "NumericLessThan": {"aws:TokenIssueTime": "2025-12-31T23:59:59Z"}
      }
    }
  ]
}
```

**Azure Third-Party Integration**:
```json
{
  "Name": "Partner Access",
  "Type": "CustomRole",
  "AssignableScopes": ["/subscriptions/SUBSCRIPTION_ID"],
  "Permissions": [{
    "Actions": ["Microsoft.Compute/virtualMachines/read"],
    "NotActions": [],
    "DataActions": ["Microsoft.Storage/storageAccounts/blobServices/containers/blobs/read"],
    "NotDataActions": []
  }]
}
```
- Use Azure AD B2B for external collaboration (MFA enforcement via Conditional Access)
- Azure Lighthouse for delegated resource management (granular permissions, audit)
- Managed identities for service-to-service authentication

**GCP Third-Party Integration**:
```bash
# Create a service account for third-party
gcloud iam service-accounts create partner-sa --display-name "Partner Service Account"

# Grant minimal IAM roles
gcloud projects add-iam-policy-binding my-project \
  --member="serviceAccount:partner-sa@my-project.iam.gserviceaccount.com" \
  --role="roles/storage.objectViewer"

# Create and rotate keys
gcloud iam service-accounts keys create partner-key.json \
  --iam-account=partner-sa@my-project.iam.gserviceaccount.com
```
- Workforce Identity Federation for external identity providers
- Service account impersonation (with `iam.serviceAccounts.signBlob` for signing)
- Access Transparency logs for third-party data access

### 46.2 Third-Party API Security

**API Key Management**:
- **Never embed keys in source code or config files shipped with application**
- Use cloud-native secret stores (AWS Secrets Manager, Azure Key Vault, GCP Secret Manager)
- Auto-rotation schedules: 30-90 days depending on sensitivity
- API key hashing: store only SHA-256 hash in database
- Prefix-based identification: `sk_live_abc123` vs `sk_test_def456`
- Scoped permissions per API key (read-only, specific endpoints, IP whitelist)
- Usage limits per key (rate limiting, quota tracking)
- Immediate revocation capability (key deletion, blocklist)
- Audit all key issuance and usage (creation, rotation, revocation events)

**OAuth 2.0 Security for Third-Party Integrations**:
- **Authorization Code + PKCE**: For browser-based and mobile apps
- **Client Credentials**: For server-to-server integrations
- **JWT Bearer Token**: For on-behalf-of flows
- **Scopes**: Minimum necessary scopes; audit scope usage
- **Token Lifetime**: Access tokens 15-60 minutes; refresh tokens up to 90 days (with re-authentication)
- **jti (JWT ID)**: Unique ID per token for revocation tracking
- **Revocation**: OAuth 2.0 token revocation endpoint; maintain token blocklist
- **Audience Validation**: Verify `aud` claim matches expected audience
- **Issuer Validation**: Verify `iss` claim matches expected issuer URL

### 46.3 Third-Party Monitoring and Incident Response

**Continuous Monitoring**:
```bash
# AWS: CloudTrail event for cross-account role assumption
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=AssumeRole \
  --query 'Events[?contains(CloudTrailEvent, `PARTNER_ACCOUNT`)]'

# Azure: Activity log for external user actions
az monitor activity-log list --query "[?authorization.action=='Microsoft.Authorization/roleAssignments/write']"

# GCP: Audit logs for service account usage
gcloud logging read 'protoPayload.authenticationInfo.principalEmail:"partner-sa@"'
```

**Alerting Rules**:
- Third-party assumes role at unusual time (outside business hours)
- Third-party accesses unusual volume of data (Anomaly detection)
- Third-party uses new/different source IP
- Third-party role assumption from unexpected region
- Third-party performs forbidden action (denied by SCP)
- Third-party API call frequency exceeds baseline
- Rotated key is still in use (indicates un-rotated local copy)

**Incident Response for Compromised Third-Party**:
1. **Immediate**: Delete cross-account role; revoke OAuth tokens; blocklist API keys
2. **Containment**: Isolate affected resources; restrict network access; rotate all related credentials
3. **Investigation**: CloudTrail logs for all third-party actions; assess data accessed/exfiltrated
4. **Notification**: Inform affected customers (GDPR 72-hour, breach notification laws)
5. **Post-Mortem**: Root cause; third-party security improvements; strengthen controls

### 46.4 Secure Token Management
- Short-lived JWTs (1 hour max; 15 minutes for sensitive operations)
- Unique token IDs (jti) for revocation tracking
- Rotate secrets on schedule (Secrets Manager auto-rotation every 30-90 days)
- Revocation list in DynamoDB/Redis for immediate invalidations (check on every request)
- Audit all token issuance and usage (who created, for what scope, when used)
- Token binding (bind token to client TLS certificate or OAuth client ID)
- Token storage: Secure HTTP-only cookies (browser), encrypted storage (mobile), OS keychain
- Refresh token rotation: issue new refresh token on each use; invalidate old one

---

## 47. Multi-Cloud Security Architecture

### 47.1 Multi-Cloud Security Challenges and Mitigations
| Challenge | Impact | Mitigation |
|-----------|--------|------------|
| IAM Fragmentation | Inconsistent access control, audit gaps | Centralized IdP (Okta/Azure AD/Keycloak); federate to all clouds with SAML/OIDC |
| Network Complexity | Traffic visibility gaps, misconfigurations | Cloud-neutral SD-WAN; IPSec VPN interconnects; cloud-agnostic service mesh (Istio, Consul) |
| Inconsistent Logging | Can't correlate incidents across clouds | Centralized SIEM; common log schema (OCSF, CEF, JSON); log shipper per cloud (Fluentd, Logstash) |
| Tool Fragmentation | Multiple UIs, skills, licensing | Multi-cloud platforms (Wiz, Prisma Cloud, Lacework, Orca) |
| Compliance Variations | Audit complexity, overlapping controls | Common framework (CSA CCM, NIST CSF, ISO 27001); map each cloud control to framework |
| Key Management | Key silos, inconsistent rotation | Cloud-agnostic KMS (HashiCorp Vault, Thales CipherTrust, Fortanix) |
| Skill Requirements | Limited cross-cloud expertise | Cross-train; use Terraform/Crossplane for consistency; IaC patterns abstraction |
| Data Residency | Data movement between jurisdictions | Region-restricted cloud accounts; data classification; DLP at egress points |
| Incident Response | Multiple tools, inconsistent playbooks | Unified SOAR (Splunk SOAR, Torq, Tines); cloud-agnostic playbooks |
| Container Orchestration | Inconsistent security controls | Cross-cloud service mesh (Istio); unified container registry; consistent admission controllers |
| Cost Attribution | Security cost allocation across clouds | Tagging strategy; showback reports; cloud management platforms |

### 47.2 Multi-Cloud Identity Federation Architecture

**Centralized IdP Design**:
```
┌─────────────────────────────────────────────────────────────────┐
│                        Central IdP (Okta/Azure AD)              │
├─────────────────────────────────────────────────────────────────┤
│  Users ← → MFA (FIDO2/TOTP/SMS) ← → SSO (SAML/OIDC)           │
└──────────┬──────────────┬─────────────────┬─────────────────────┘
           │              │                 │
     ┌─────▼─────┐  ┌────▼─────┐     ┌─────▼─────┐
     │ AWS SSO   │  │Azure AD  │     │ GCP       │
     │ (IAM IdC) │  │(SAML)    │     │(OIDC)    │
     └───────────┘  └──────────┘     └───────────┘
```

**Federation Configuration Per Provider**:

**AWS IAM Identity Center (SSO)**:
- Create permission sets for each role/access level (Admin, ReadOnly, SecurityAudit)
- Assign users/groups from external IdP via SCIM provisioning
- AWS SSO access portal (https://myapps.awsapps.com/start)
- Session duration: 1-8 hours (configurable); re-authentication on expiration
- Audit: CloudTrail for SSO events; Access Advisor for unused permissions

**Azure AD**:
- Azure AD is the IdP; external IdP via federation
- Conditional Access policies per cloud resource (MFA required for AWS/GCP access)
- Azure AD Application Proxy for on-premises app access to cloud resources
- Privileged Identity Management (PIM) for JIT cloud access

**GCP**:
- Workforce Identity Federation (federate external IdPs)
- Cloud Identity as IdP for GCP-only
- IAM conditions on federated access (source IP, time, device)
- Access Transparency for provider employee data access

### 47.3 Multi-Cloud Networking Security

**Network Connectivity Patterns**:
| Pattern | Use Case | Provider Implementations |
|---------|----------|------------------------|
| Direct Peering | Low-latency, high-bandwidth | AWS Direct Connect, Azure ExpressRoute, GCP Dedicated Interconnect |
| VPN IPSec | Site-to-site encrypted tunnels | AWS VPN, Azure VPN Gateway, GCP Cloud VPN (HA) |
| SD-WAN | Dynamic routing, centralized policy | VMware SD-WAN, Cisco Meraki, Fortinet SD-WAN |
| Cloud Interconnect | AWS ↔ Azure cross-cloud | Equinix Fabric, Megaport, PacketFabric |
| Zero Trust Network | Identity-based access, no VPN | Zscaler, Cloudflare Zero Trust, Netskope |

**Multi-Cloud Network Security Controls**:
- **Encrypted tunnels**: IPSec VPN (IKEv2, AES-256, SHA-256) or MACsec for direct connect
- **Traffic inspection**: NVA firewall (Palo Alto, Fortinet, Check Point) at interconnect point
- **Egress filtering**: Cloud Firewall/NACL/WAF on all cloud edges
- **DNS security**: Centralized DNS filtering for all clouds (Cloudflare Gateway, Cisco Umbrella)
- **DDoS**: Cloudflare / Akamai / Azure DDoS / AWS Shield — preferably edge-based CDN
- **Private connectivity**: Avoid public internet for inter-cloud traffic; use cloud exchanges
- **Micro-segmentation**: Consistent segment labels across clouds (Terraform modules)

### 47.4 Multi-Cloud Data Security

**Data Encryption Across Clouds**:
| Data State | AWS | Azure | GCP | Cloud-Agnostic |
|------------|-----|-------|-----|----------------|
| At Rest | AWS KMS (CMK) | Azure Key Vault (CMK) | Cloud KMS (CSEK) | HashiCorp Vault, Thales |
| In Transit | TLS 1.2+ (ACM) | TLS 1.2+ (Key Vault cert) | TLS 1.2+ (Certificate Manager) | cert-manager, Let's Encrypt |
| In Use | Nitro Enclaves | Confidential Computing (SGX) | Confidential VMs (SEV-SNP) | Fortanix, Anjuna |
| Key Material | CloudHSM | Managed HSM | Cloud HSM | Thales Luna, Azure Dedicated HSM |

**Multi-Cloud Data Governance**:
- **Data Classification**: Unified classification across clouds (public, internal, confidential, restricted)
- **DLP**: Cloud-agnostic DLP (Forcepoint, Symantec, Netskope) or provider-native (Macie, Purview, Sensitive Data Protection)
- **Data Retention**: Consistent S3 lifecycle / Blob tiering / GCS nearline-to-coldline policies
- **Data Portability**: Standard formats (Parquet, Avro, ORC); no provider-specific lock-in
- **Access Control**: IAM + bucket policies + VPC perimeters consistently applied
- **Audit**: Unified data access logging across all clouds (S3 access logs, Blob diagnostics, Cloud Audit Logs)

### 47.5 Multi-Cloud Security Operations

**Unified Incident Response Across Clouds**:
```bash
# AWS: Isolate compromised instance
aws ec2 modify-instance-attribute --instance-id i-12345 --groups sg-quarantine

# Azure: Apply NSG to VM
az network nsg rule create --name "DenyAll" --nsg-name quarantine-nsg \
  --priority 100 --direction Inbound --access Deny --protocol "*" \
  --destination-port-ranges "*"

# GCP: Add VPC firewall rule to isolate
gcloud compute firewall-rules create isolate-vm --direction INGRESS \
  --priority 100 --source-ranges 0.0.0.0/0 --action DENY \
  --target-tags compromised
```

**Common Incident Response Workflow**:
1. Detection (any cloud's monitoring detects threat)
2. Central SOAR receives alert; enriches with context from all clouds
3. Automated containment across affected clouds (quarantine, block, isolate)
4. Investigation with unified log view (SIEM aggregation)
5. Forensic evidence collection (snapshot, memory dump, log archive from each cloud)
6. Remediation (IaC deployment to fix configuration, patch, rebuild)
7. Post-mortem with unified timeline across clouds

### 47.6 Multi-Cloud Compliance and Governance

**Governance Controls Across Clouds**:
| Control | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Tagging Enforcement | SCP `aws:RequestTag` | Azure Policy `tagName` | Org Policy `constraints/tags` |
| Region Restriction | SCP `aws:RequestedRegion` | Azure Policy `locations` | Org Policy `gcp.resourceLocations` |
| Resource Type Restriction | SCP `ec2:InstanceType` | Azure Policy `resourceTypes` | Org Policy `compute.vmExternalIpAccess` |
| Encryption Enforcement | Config rule `encrypted-volumes` | Policy `sqlEncryption` | Org Policy `constraints/alwaysEncrypted` |
| Public Access Block | SCP `s3:PutBucketPublicAccessBlock` | Policy `storageAccountPublicAccess` | Org Policy `constraints/iam.allowedPolicyMemberDomains` |
| Audit Logging | Organization trail | Diagnostic settings at subscription | Org-level audit logs |
| Backup Enforcement | AWS Backup policies | Azure Backup Center | Backup and DR service |

**Multi-Cloud Compliance Framework Mapping**:
- Map each cloud's security controls to common framework (NIST CSF, ISO 27001, SOC 2, PCI DSS)
- Use CSA CCM (Cloud Controls Matrix) as universal mapping layer
- Automated compliance scanning across all clouds (Wiz, Prisma, Lacework, or native tools)
- Centralized evidence collection and reporting for audits

### 47.7 Multi-Cloud Security Tool Stack
```
Identity (IdP):          Okta / Azure AD / Keycloak / Auth0
CSPM:                    Wiz / Prisma Cloud / Lacework / Orca / CrowdStrike
CWPP:                    CrowdStrike / SentinelOne / Trend Micro / Palo Alto
Threat Detection:        Wiz / Lacework / Orca / Aqua
SIEM:                    Splunk / Azure Sentinel / Datadog / ELK / Chronicle
SOAR:                    Splunk SOAR / Torq / Tines / Palo Alto XSOAR
Secrets:                 HashiCorp Vault / CyberArk / Akeyless / Doppler
KMS:                     Thales CipherTrust / Fortanix / HashiCorp Vault
Network:                 Cloudflare / Zscaler / Palo Alto / Netskope
DDoS:                    Cloudflare / Akamai / Fastly / AWS Shield / Azure DDoS
Container:               Aqua / Sysdig / Prisma Cloud / Twistlock
IaC:                     Terraform / Pulumi / Crossplane / OpenTofu
Service Mesh:            Istio / Consul / Linkerd / Kuma
API Gateway:             Kong / Apigee / Tyk / Azure API Management
Workload Identity:       SPIFFE/SPIRE / cert-manager / Istio
Agentless Scanning:      Wiz / Orca / CrowdStrike / Aqua
Compliance Automation:   CloudHealth / Turbonomic / Flexera
Cost + Security:        CloudHealth / Vantage / FinOps + security overlay
```

### 47.8 Cloud-Agnostic IaC Security Patterns

**Terraform Multi-Cloud Security Module**:
```hcl
# Consistent encryption across clouds
module "encryption" {
  source = "./modules/encryption"
  
  providers = {
    aws = aws
    azurerm = azurerm
    google = google
  }
  
  # Same key material across clouds (via Vault)
  kms_key_arn     = var.aws_kms_key_arn
  key_vault_id    = var.azure_key_vault_id
  cloud_kms_key   = var.gcp_kms_key
}

# Consistent logging across clouds
module "logging" {
  source = "./modules/logging"
  
  aws_cloudtrail_bucket  = var.aws_log_bucket
  azure_log_workspace    = var.azure_workspace_id
  gcp_log_bucket         = var.gcp_log_bucket
  
  retention_days = 2557  # 7 years compliance
  enable_dns_logs = true
  enable_vpc_flow_logs = true
}
```

---

## 48. Cloud Security for DevOps Pipelines

### 48.1 GitHub Actions Security
```yaml
name: Secure Deploy
on: [push]
permissions:
  contents: read
  id-token: write  # For OIDC

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Secret detection
      - name: TruffleHog
        uses: trufflesecurity/trufflehog@v3
        with:
          extra_args: --only-verified
      
      # IaC scanning
      - name: Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: terraform/
          framework: terraform
          soft_fail: false
      
      - name: tfsec
        uses: aquasecurity/tfsec-action@v1.0.3
      
      # Container scanning
      - name: Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'ghcr.io/${{ github.repository }}:${{ github.sha }}'
          severity: 'CRITICAL,HIGH'
          format: 'sarif'
      
      # OIDC to AWS (no static keys)
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubDeployRole
          aws-region: us-east-1
      
      - name: Deploy
        run: terraform apply -auto-approve
```

### 48.2 Pipeline Security Checklist
- [ ] OIDC federation (no long-lived cloud keys in CI/CD)
- [ ] Secret detection (TruffleHog, GitLeaks) on every commit
- [ ] SAST scan (SonarQube, Semgrep, Checkmarx)
- [ ] Dependency scan (Snyk, Dependabot, Renovate)
- [ ] Container scan (Trivy, Clair, Snyk) - fail on CRITICAL/HIGH
- [ ] IaC scan (Checkov, tfsec, cfn-nag) - fail on security issues
- [ ] SBOM generation (CycloneDX, SPDX)
- [ ] Image signing (Cosign)
- [ ] Artifact integrity verification (hashes, signatures)
- [ ] Immutable deployments (blue/green, canary)
- [ ] Approval gates for production
- [ ] Automated rollback verified
- [ ] Deployment audit trail (who deployed, what, when)

---

## 49. Cloud Security Interview Questions (Extended)

### 49.1 Technical
**Q1: Explain the shared responsibility model for IaaS, PaaS, and SaaS.** The provider secures the cloud infrastructure; the customer secures their data, identities, configurations, and applications. IaaS: customer manages OS and above. PaaS: customer manages app code and data. SaaS: customer manages user access and data governance.

**Q2: What is the principle of least privilege in IAM?** Grant only the minimum permissions needed. Implemented via granular policies, avoiding `*` wildcards, groups for RBAC, regular reviews, JIT elevation, IAM conditions (IP, MFA, VPC), and IAM Access Analyzer.

**Q3: Difference between Security Group and NACL?** SG: stateful, instance-level, allow rules only. NACL: stateless, subnet-level, allow AND deny rules. SGs automatically allow return traffic; NACLs require explicit return rules.

**Q4: How to detect and respond to a compromised IAM key?** Detection: GuardDuty findings, CloudTrail unusual IPs/user agents. Response: Disable key, detach policies, revoke sessions, investigate CloudTrail, rotate key, block IP.

**Q5: Encryption at rest vs in transit vs in use?** At rest: AES-256 (S3, EBS, RDS). In transit: TLS 1.2+ (HTTPS, API calls). In use: Confidential Computing (SGX, SEV-SNP, Nitro Enclaves).

**Q6: Bucket policy vs IAM policy?** IAM: identity-based, attached to users/groups/roles. Bucket policy: resource-based, attached to S3 buckets, allows cross-account access. Effective permission = union minus explicit denies.

**Q7: AWS KMS key rotation?** Customer managed keys: automatic annual rotation. AWS managed: 3 years. Imported key material: manual rotation only.

**Q8: How to secure a three-tier web app in AWS?** WAF + CloudFront → ALB (HTTPS) → Web tier (private, SG from ALB) → App tier (private, SG from web) → RDS (isolated, SG from app). Encrypt at rest/in transit. CloudTrail + GuardDuty + VPC Flow Logs.

**Q9: What is IMDSv2 and why important?** Instance Metadata Service. v1: unauthenticated GET. v2: requires PUT for session token (TTL-bound). Hop limit 1 prevents container access. Mitigates SSRF credential theft.

**Q10: How do you implement DDoS protection?** Defense in depth: CDN (edge absorption), WAF (rate limiting, geo-block, bot control), Shield Advanced (L3/4/7 mitigation), autoscaling (absorb traffic), Route53 health checks + failover.

### 49.2 Scenario-Based
**Q: GuardDuty alerts on S3 access from unexpected IP. Walk through response.** 
1. Check CloudTrail: which objects accessed, IAM role used, source IP
2. Containment: Block Public Access, update bucket policy, rotate key, isolate role
3. Impact: S3 access logs for accessed objects; Macie scan for data classification
4. Root cause: leaked key, permissive policy, public bucket
5. Remediation: Block public access at account level; least privilege S3 policies; IAM conditions; CloudTrail data events
6. Notification: GDPR 72-hour, data subjects, security team

---

## 50. Cloud Security Final Reference

### 50.1 Core Principles Summary
1. **Shared Responsibility**: Provider secures infrastructure; customer secures data, identities, configurations, applications
2. **Identity is the New Perimeter**: No physical network boundary; IAM is the primary control
3. **Least Privilege**: Grant minimum permissions; review regularly; automate JIT elevation
4. **Defense in Depth**: Multiple overlapping controls (SG + NACL + WAF + IAM + encryption + monitoring)
5. **Encrypt Everything**: At rest (AES-256), in transit (TLS 1.2+), in use (Confidential Computing)
6. **Log Everything, Monitor Continuously**: CloudTrail, VPC Flow Logs, SIEM, threat detection (GuardDuty/Defender/SCC)
7. **Automate Security**: Policy as Code, IaC scanning, auto-remediation, SOAR playbooks
8. **Assume Breach**: Design architecture assuming compromise; implement containment, isolation, and blast radius reduction
9. **Data Classification**: Classify data by sensitivity; apply controls per classification level
10. **Continuous Compliance**: Automate compliance validation; collect evidence continuously; monitor for drift

### 50.2 Most Common Cloud Breach Causes
1. **Misconfigured storage** (S3/Blob/GCS buckets left public)
2. **Compromised credentials** (stolen keys, phished passwords, no MFA)
3. **Overly permissive IAM** (wildcard permissions, no conditions)
4. **Unpatched systems** (OS, application, container vulnerabilities)
5. **SSRF to metadata endpoints** (IMDSv1, metadata.google.internal)
6. **No logging or monitoring** (can't detect breaches in progress)
7. **API misconfiguration** (unauthenticated APIs, missing rate limiting)
8. **Supply chain attacks** (compromised CI/CD, third-party libraries)
9. **Insider threats** (malicious or negligent employees/contractors)
10. **Insufficient network segmentation** (flat networks, public RDS)

### 50.3 Cloud Security Mantra
```
The cloud provider secures the infrastructure.
YOU secure your data, identities, and configurations.
Most breaches are from misconfiguration, not provider vulnerabilities.
Implement least privilege. Enable encryption. Log everything.
Monitor continuously. Automate responses. Test incident plans.
Security is not a product — it is a continuous process.
```

---

> Final Reminder: Cloud security is a shared responsibility, continuous process, and requires defense-in-depth. The most common breaches result from misconfigurations, not provider vulnerabilities. Implement IAM least privilege, enable encryption everywhere, log everything, monitor continuously, automate responses, and test your incident response regularly. The cloud gives you incredible power — use it responsibly.

---

## 51. Cloud Security Tools — Comprehensive Reference

### 51.1 Cloud Provider Native Tools (Free/Included)

**AWS Native Security Tools**:
| Tool | Coverage | Use Case | Cost |
|------|----------|----------|------|
| **AWS IAM** | All AWS services | Identity, access control, policies, roles | Free |
| **AWS Organizations** | Multi-account | SCPs, consolidated billing, account management | Free |
| **AWS CloudTrail** | API activity | Audit logging, compliance evidence, incident investigation | Management events: free; Data events: paid |
| **AWS Config** | Resource config | Compliance monitoring, configuration history, drift detection | ~$0.003 per config item recorded |
| **AWS Security Hub** | Multi-service | Centralized findings, compliance standards (CIS, PCI, AWS FSBP) | $0.001 per check; $0.01 per finding |
| **Amazon GuardDuty** | Multi-service | ML-based threat detection (CloudTrail, VPC Flow, DNS, EKS, RDS, S3, Lambda) | ~$0.10/GB CloudTrail; $0.05/GB VPC Flow |
| **Amazon Inspector** | EC2, ECR, Lambda | Automated vulnerability scanning | Per instance/function assessment |
| **AWS WAF** | Web apps | Web application firewall (OWASP rules, rate limiting, bot control) | $5/mo per ACL + $0.60/1M requests |
| **AWS Shield Standard** | All AWS | L3/L4 DDoS protection | Free |
| **AWS KMS** | Encryption | Key management, rotation, audit | $1/key/month + $0.03/10k operations |
| **AWS Secrets Manager** | Secrets | Secret lifecycle, rotation, audit | $0.40/secret/month |
| **AWS Macie** | S3 | ML-based sensitive data discovery and classification | $0.50/GB classified |
| **AWS Artifact** | Compliance | SOC, ISO, PCI reports access | Free |
| **AWS Systems Manager** | EC2, on-prem | Patch management, Session Manager, automation | Free (SSM agent); paid features |
| **AWS Trusted Advisor** | All | Security, cost, performance recommendations | Basic: free; Enterprise: full checks |
| **AWS Audit Manager** | Compliance | Evidence collection, compliance report generation | Per resource per assessment |
| **AWS CloudWatch** | All metrics | Monitoring, logging, alerting, dashboards | Per metric, per GB log ingested |
| **AWS Firewall Manager** | Multi-account | Central WAF/Shield/Network Firewall management | No additional cost |
| **AWS Network Firewall** | VPC | Managed firewall, intrusion prevention | Per endpoint per hour |
| **AWS Verified Access** | Corporate apps | Zero Trust network access (ZTNA) | Per endpoint per hour |
| **AWS Private Certificate Authority** | Certificates | Private CA for internal PKI | Per CA per month + per cert |
| **AWS Directory Service** | AD | Managed Microsoft AD, AD Connector, Simple AD | Per directory per hour |
| **Amazon Detective** | Investigation | Graph-based security investigation and root cause analysis | Per GB analyzed |
| **Amazon Cognito** | App auth | User pools, identity pools, federation | Per MAU |
| **AWS Identity Center (SSO)** | Multi-account | SSO across AWS accounts and business apps | Free |
| **AWS Backup** | Backup | Centralized backup; cross-region/account; vault lock | Per backup; per storage |
| **AWS CloudFormation** | IaC | Infrastructure as Code (templates) | Free |
| **AWS Service Catalog** | Governance | Approved IT service catalog; controlled provisioning | Free |

**Azure Native Security Tools**:
| Tool | Coverage | Use Case | Cost |
|------|----------|----------|------|
| **Azure AD (Entra ID)** | Identity | Identity, SSO, MFA, Conditional Access | Free tier; P1/P2 per user |
| **Azure RBAC** | All Azure | Role-based access control | Free |
| **Azure Policy** | Resources | Compliance policies, remediation, guardrails | Free |
| **Defender for Cloud** | Multi-service | CSPM, CWPP, vulnerability, threat detection | Free CSPM; paid defender plans |
| **Microsoft Sentinel** | SIEM | Cloud-native SIEM, SOAR, threat intelligence | Per GB ingested ($2.46/GB) |
| **Azure Monitor** | All resources | Metrics, logs, alerts, Application Insights | Per GB ingested |
| **Azure Activity Log** | Subscription | Subscription-level events, audit trail | Free (90-day) |
| **Azure Key Vault** | Secrets, keys, certs | Secrets management, key management, certificate lifecycle | Per transaction; premium: HSM |
| **Azure WAF** | App Gateway, Front Door | OWASP rules, rate limiting, bot mitigation, geo-filtering | Per hour + per GB |
| **Azure DDoS Protection** | Virtual networks | Basic: free; Standard: adaptive tuning, mitigation reports | Basic: free; Standard: $2944/mo |
| **Azure Firewall** | Virtual networks | Stateful firewall, FQDN filtering, threat intelligence | Per hour + per GB |
| **Azure Private Link** | Network | Private connectivity to Azure services | Per endpoint per hour |
| **Microsoft Purview** | Data governance | Data classification, catalog, lineage, DLP | Per asset, per capacity unit |
| **Azure Information Protection** | Data | Data classification, labeling, protection | Per user (E5) |
| **Azure Backup** | VMs, SQL, SAP, files | Backup; cross-region; soft delete; vault | Per protected instance |
| **Azure Site Recovery** | DR | VM replication; disaster recovery | Per protected instance |
| **Azure Update Management** | VMs | Patch assessment and deployment | Per node |
| **Azure Automation** | Runbooks | Process automation; configuration management | Per automation minute |
| **Azure Blueprints** | Governance | Repeatable environment templates | Free |
| **Azure AD Identity Protection** | Identity | Risk-based detection; conditional access | Azure AD P2 required |
| **Azure Policy Guest Config** | VMs | In-guest policy evaluation | Per machine per hour |
| **Azure Resource Graph** | Inventory | Resource exploration; query across subscriptions | Free |
| **Azure Cloud Shell** | CLI | Browser-based CLI (PowerShell, Bash) | Free |
| **Azure Logic Apps** | Integration | Serverless workflows; SOAR integration | Per execution |
| **Azure Bastion** | Network | Secure RDP/SSH without public IPs | Per hour |
| **Azure Front Door** | CDN/WAF | Global load balancing; WAF; DDoS; CDN | Per hour + per GB |

**GCP Native Security Tools**:
| Tool | Coverage | Use Case | Cost |
|------|----------|----------|------|
| **Cloud IAM** | All GCP | Roles, policies, conditions, service accounts | Free |
| **Cloud Identity** | Users/devices | Identity, SSO, MFA, device management | Free basic; premium per user |
| **Organization Policies** | Organization | Centralized constraints; deny/restrict resource configs | Free |
| **Security Command Center** | Multi-service | CSPM, threat detection, vulnerability scanning | Standard: free; Premium per asset |
| **Cloud Audit Logs** | All services | Admin Activity (free), Data Access (paid), System Events | Admin: free; Data Access: paid |
| **Cloud Logging** | All services | Log storage, analysis, routing, export | 50GB free; $0.50/GB after |
| **Cloud Monitoring** | All services | Metrics, dashboards, alerting (Prometheus-based) | 300 metrics free; per metric after |
| **Cloud KMS** | Encryption | Key management, rotation, HSM integration | Per key version; per operation |
| **Cloud HSM** | Encryption | FIPS 140-2 Level 3 HSM | Per key version (premium) |
| **Cloud External Key Manager** | Encryption | External KMS key usage | Per operation (partner) |
| **Cloud Armor** | Network | WAF, DDoS, rate limiting, bot management | Per policy + per request |
| **Cloud Firewall** | VPC | Distributed firewall; ingress/egress rules | Free |
| **VPC Service Controls** | Data | Data exfiltration prevention perimeters | Free (per perimeter) |
| **Secret Manager** | Secrets | Secret storage, versioning, IAM-based access | Per version; per access |
| **Sensitive Data Protection (DLP)** | Data | Sensitive data inspection, classification, de-identification | Per GB inspected |
| **Chrome Enterprise Premium** | ZTNA | BeyondCorp; context-aware access; DLP | Per user per month |
| **Chronicle** | SIEM | Cloud SIEM; security analytics; threat detection | Per GB ingested |
| **Assured Workloads** | Compliance | FedRAMP, HIPAA, data residency controls | Per project |
| **Cloud Asset Inventory** | Inventory | Resource tracking; IAM policy analysis; history | Free |
| **Web Security Scanner** | Web apps | OWASP Top 10 scanning (App Engine, GKE, GCE) | Free |
| **Access Transparency** | Audit | Provider access audit logs | Per project per month |
| **Event Threat Detection** | Threat | Threat detection from Cloud Audit Logs | Per 100K log lines |
| **VM Threat Detection** | Compute | Malware detection on Compute Engine | Per vCPU hour |
| **Container Threat Detection** | GKE | Kernel-level threat detection in containers | Per node hour |
| **Policy Intelligence** | IAM | IAM recommender; policy analysis; activity analyzer | Free |
| **Cloud Data Loss Prevention** | Data | Inspect, classify, redact sensitive data | Per unit processed |
| **Binary Authorization** | GKE | Enforce signed container images; deployment approval | Per cluster per month |

### 51.2 Cloud Security Tools — Multi-Cloud & Third-Party

**CSPM (Cloud Security Posture Management)**:
| Tool | Supported Clouds | Key Features | Pricing |
|------|-----------------|--------------|---------|
| **Wiz** | AWS, Azure, GCP, OCI, Kubernetes | Agentless; graph-based analysis; IaC scanning; vulnerability finder; 25+ connectors; toxic combination analysis | Enterprise (resource-based) |
| **Prisma Cloud (Palo Alto)** | AWS, Azure, GCP, OCI, Alibaba | CSPM + CWPP + CIEM + IaC + Web App & API Security; 750+ out-of-box policies; compliance reports | Per workload/per hour |
| **Lacework** | AWS, Azure, GCP | ML-based behavioral analysis; anomaly detection; container security; IaC scanning | Per resource per month |
| **Orca Security** | AWS, Azure, GCP, OCI, Alibaba | Agentless side-scanning; deep workload analysis; contextual risk assessment | Per resource per month |
| **CloudSploit (Aqua)** | AWS, Azure, GCP, GitHub, OCI | Open-source CSPM; 100+ checks; CI/CD integration; HTML reports | Free/Open source |
| **Checkov (Bridgecrew)** | IaC (Terraform, CFN, ARM, K8s) | IaC security scanning; 1000+ policies; CI/CD integration; auto-fix | Free/Open source + SaaS |
| **Prowler** | AWS | 300+ security checks; CIS/GDPR/HIPAA/PCI/NIST/SOC2; CLI | Free/Open source |
| **ScoutSuite** | AWS, Azure, GCP | Multi-cloud security audit; 500+ rules; HTML reports | Free/Open source |
| **Forseti Security** | GCP | GCP-specific; inventory, scanning, policy enforcement, remediation | Free/Open source |
| **Cloud Custodian** | AWS, Azure, GCP | Policy engine; real-time resource compliance; auto-remediation | Free/Open source |
| **Snyk** | IaC, containers, open source | IaC scanning, container vulnerability, dependency scanning | Free tier; paid per developer |
| **Tenable Cloud Security** | AWS, Azure, GCP | Agentless CSPM; container security; vulnerability management | Per resource per month |
| **Qualys Cloud Security** | AWS, Azure, GCP | CSPM + vulnerability scanning; agent-based and agentless | Per asset per month |

**CWPP (Cloud Workload Protection)**:
| Tool | Supported | Key Features | Pricing |
|------|-----------|--------------|---------|
| **CrowdStrike Falcon** | AWS, Azure, GCP | Single agent; EDR + CWPP; real-time threat prevention; IOA; vulnerability management | Per workload per year |
| **SentinelOne Cloud Workload** | AWS, Azure, GCP | AI-powered EDR; autonomous response; container security; vulnerability | Per workload per year |
| **Trend Micro Cloud One** | AWS, Azure, GCP | Workload security; container security; file storage; network; application | Per workload per hour |
| **Aqua Security** | AWS, Azure, GCP, K8s | Container/severless focused; image scanning; runtime protection; K8s admission | Per node/per workload |
| **Sysdig Secure** | AWS, Azure, GCP, K8s | Container/K8s runtime security; Falco-based; image scanning; compliance | Per node per month |
| **Qualys Cloud Agent** | AWS, Azure, GCP | VMDR (vulnerability + patch); FIM; PCI compliance | Per asset per year |
| **Rapid7 InsightVM** | AWS, Azure, GCP | Vulnerability management; real-time risk scoring; compliance | Per asset per year |
| **Tenable.io** | AWS, Azure, GCP | Vulnerability management; container security; web app scanning | Per asset per year |

**CIEM (Cloud Infrastructure Entitlement Management)**:
| Tool | Supported | Key Features | Pricing |
|------|-----------|--------------|---------|
| **Wiz (Ermetic acquisition)** | AWS, Azure, GCP | IAM entitlement analysis; privilege escalation path detection; least privilege recommendations | Bundled with Wiz |
| **Prisma Cloud CIEM** | AWS, Azure, GCP | IAM analytics; unused permissions; cross-cloud entitlement visibility | Bundled with Prisma |
| **Saviynt** | AWS, Azure, GCP | IGA + CIEM; access reviews; automated provisioning | Per user/per workload |
| **AWS IAM Access Analyzer** | AWS | IAM policy analysis; unused access; cross-account access | Free |
| **Azure AD Entitlement Management** | Azure | Access reviews; entitlement management; PIM | Azure AD P2 |
| **GCP IAM Recommender** | GCP | Unused permissions; policy recommendations | Free |

**SIEM / SOAR**:
| Tool | Deployment | Key Features | Pricing |
|------|-----------|--------------|---------|
| **Splunk Cloud** | SaaS | Log aggregation; advanced correlation; dashboards; ML/AI analytics; SOAR integration | Per GB ingested |
| **Microsoft Sentinel** | Azure | Cloud-native SIEM; KQL queries; 200+ connectors; built-in SOAR (Logic Apps); UEBA | Per GB ingested |
| **Google Chronicle** | GCP | Cloud-native SIEM; massive scale; log normalization; threat intel; detections as code | Per GB ingested |
| **Elastic Security (ELK)** | Self-hosted/SaaS | Open-source SIEM; Elasticsearch + Kibana + beats; detection rules; ML | Free tier; paid for cloud |
| **Sumo Logic** | SaaS | Cloud-native; real-time analytics; compliance reports; threat intel | Per GB ingested |
| **Datadog Security Monitoring** | SaaS | SIEM + CSPM + Cloud Workload Security; integrated with APM/infra | Per GB ingested + per host |
| **Rapid7 InsightIDR** | SaaS | SIEM + UEBA + EDR; attacker behavior analytics; 900+ integrations | Per endpoint per month |
| **IBM QRadar on Cloud** | SaaS | Correlation rules; offense management; 700+ DSM parsers | Per EPS (events per second) |
| **Palo Alto Cortex XSIAM** | SaaS | AI-driven SOAR; extended detection and response; automation | Per endpoint per month |
| **Splunk SOAR (Phantom)** | SaaS/On-prem | Playbook automation; case management; 300+ integrations | Per action per month |
| **AWS Security Hub + EventBridge** | AWS | Native cloud SOAR; Lambda auto-remediation; custom actions | Per finding/check |
| **TheHive / Cortex** | Self-hosted | Open-source SOAR; case management; MISP integration; responder | Free/Open source |

**Container & Kubernetes Security**:
| Tool | Supported | Key Features | Pricing |
|------|-----------|--------------|---------|
| **Aqua Security** | All K8s, registries | Image scanning; runtime protection; K8s admission; KSPM | Per node per month |
| **Sysdig Secure** | K8s, EKS, AKS, GKE | Runtime security (Falco); image scanning; compliance (kube-bench); KSPM | Per node per month |
| **Prisma Cloud Compute** | K8s, containers, serverless | Image scanning; runtime; host security; K8s audit; CI/CD integration | Per workload per hour |
| **Snyk Container** | Registries, CI/CD | Container vulnerability scanning; base image recommendations; fix | Per image per month |
| **Trivy** | All | Open-source; container, filesystem, git repo, K8s scanning; SBOM | Free/Open source |
| **Clair** | Registries | Open-source container vulnerability scanner | Free/Open source |
| **Falco** | K8s, containers | Runtime security; behavioral monitoring; syscall analysis | Free/Open source (CNCF) |
| **kube-bench** | K8s | CIS Kubernetes Benchmark checker | Free/Open source |
| **kube-hunter** | K8s | Kubernetes penetration testing | Free/Open source |
| **OPA/Gatekeeper** | K8s | Policy engine; admission control; Rego policies | Free/Open source (CNCF) |
| **Kyverno** | K8s | Kubernetes-native policy engine; validate, mutate, generate | Free/Open source (CNCF) |
| **Checkov (K8s)** | K8s manifests | IaC/K8s security scanning | Free/Open source |
| **Kube Scanner (Aqua)** | K8s | K8s configuration scanning | Free |
| **Popeye** | K8s | K8s cluster resource sanitizer; configuration best practices | Free/Open source |
| **kubescape** | K8s | K8s security scanner; NSA/CISA hardening guidance; CIS | Free/Open source (CNCF) |
| **Harbor** | Registry | Container registry with vulnerability scanning; signing; RBAC; replication | Free/Open source (CNCF) |
| **Notary / Notation** | Images | Container image signing and verification | Free/Open source |
| **Cosign** | Images | Container signing, verification, key management (Sigstore) | Free/Open source |
| **Sigstore** | Images | Software signing; transparency log; keyless signing | Free |

**Secrets Management**:
| Tool | Deployment | Key Features | Pricing |
|------|-----------|--------------|---------|
| **HashiCorp Vault** | Self-hosted/Cloud/HCP | Dynamic secrets; encryption as a service; leasing; revocation; K8s integration | Free OSS; Enterprise per node |
| **AWS Secrets Manager** | AWS | Auto-rotation; fine-grained IAM; cross-region replication | $0.40/secret/month |
| **Azure Key Vault** | Azure | Secrets + keys + certs; RBAC; soft-delete; HSM option | Per transaction; premium per partition |
| **GCP Secret Manager** | GCP | IAM-based access; versioning; replication; audit | Per version/month + per access |
| **CyberArk Conjur** | Self-hosted/SaaS | Secrets management for DevOps; K8s integration; split knowledge | Per workload per month |
| **Akeyless** | SaaS | Secrets management; K8s external secrets; dynamic secrets; BYOK | Per secrets + per workload |
| **Doppler** | SaaS | Environment management; secrets sync; CI/CD integration | Free tier; paid per project |
| **External Secrets Operator** | K8s | Syncs secrets from cloud providers to K8s | Free/Open source |
| **Sealed Secrets** | K8s | Encrypt K8s Secrets into SealedSecrets (GitOps safe) | Free/Open source |
| **SOPS (Mozilla)** | Files | Encrypted files for IaC; supports AWS/GCP/Azure KMS, PGP, Age | Free/Open source |
| **git-crypt** | Git | Transparent Git encryption for sensitive files | Free/Open source |
| **truffleHog** | Repos | Secret scanning in Git history | Free/Open source |
| **GitLeaks** | Repos/CI | Secret scanning; pre-commit hooks; CI integration | Free/Open source/Enterprise |

**Network Security**:
| Tool | Deploy | Key Features |
|------|--------|--------------|
| **Cloudflare** | Edge/SaaS | CDN; WAF; DDoS; ZTNA; API shield; bot management; SASE |
| **Zscaler** | Cloud | ZTNA; SWG; CASB; DLP; cloud firewall; sandbox |
| **Palo Alto Prisma Access** | Cloud | SASE; SD-WAN; NGFW; threat prevention; URL filtering |
| **Palo Alto VM-Series** | Instance/Azure/GCP | NGFW in cloud marketplace; threat prevention; URL filtering |
| **Fortinet FortiGate** | Instance/Azure/GCP | NGFW; IPS; VPN; SD-WAN; security fabric |
| **Check Point CloudGuard** | Instance/Azure/GCP | NGFW; IPS; anti-bot; threat emulation; API-based security |
| **Cisco FTDv** | Instance/Azure/GCP | NGFW; IPS; AMP; URL filtering |
| **AWS Network Firewall** | AWS | Managed; stateful inspection; IPS; domain filtering; Suricata rules |
| **Azure Firewall** | Azure | Stateful; FQDN filtering; threat intel; DNAT; forced tunneling |
| **GCP Cloud Firewall** | GCP | Distributed; hierarchical; rules logging; firewall insights |
| **Cilium** | K8s | eBPF-based; network policy; mTLS; observability; Hubble |
| **Calico** | K8s/VM | Network policy; eBPF; wireguard encryption; WAF |
| **Wireguard** | VPN | Simple, fast, modern VPN; cloud-to-cloud and remote access |
| **OpenVPN** | VPN | Open-source VPN; access server for cloud connectivity |

**Vulnerability & Compliance Scanning**:
| Tool | Target | Key Features |
|------|--------|--------------|
| **Trivy** | Containers, filesystems, repos, K8s, IaC, SBOM | Comprehensive vulnerability scanner; OSS; fast |
| **Snyk** | Code, dependencies, containers, IaC, K8s | Developer-first; CI/CD integration; fix PRs |
| **Black Duck (Synopsys)** | Code, dependencies | SCA; license compliance; policies |
| **SonarQube** | Code | SAST; code quality; 30+ languages; CI/CD |
| **Semgrep** | Code | SAST; custom rules; OSS; multi-language |
| **Checkmarx** | Code | SAST + SCA + API security; CxFlow CI/CD |
| **Fortify** | Code | SAST + DAST + SCA; Fortify on Demand (cloud) |
| **Veracode** | Code | SAST + DAST + SCA; pipeline scanning |
| **Burp Suite** | Web apps | DAST; web app pentesting; scanner + proxy |
| **OWASP ZAP** | Web apps | DAST; OSS; automated scanning; CI/CD integration |
| **Acunetix** | Web apps | DAST; OWASP Top 10; network scanner; CI/CD |
| **Nessus (Tenable)** | VMs, cloud | Vulnerability scanning; compliance; config audit |
| **Qualys** | VMs, cloud, web | VMDR; policy compliance; web app scanning; cloud agent |
| **Rapid7 Nexpose/InsightVM** | VMs, cloud | Live monitoring; real-time risk; asset discovery |
| **Nmap** | Network | Port scanning; service detection; NSE scripts |
| **masscan** | Network | High-speed port scanning; large ranges |
| **Nikto** | Web | Web server scanner; outdated software; CVE checks |
| **wpscan** | WordPress | WordPress vulnerability scanner |
| **sqlmap** | Database | Automated SQL injection detection and exploitation |
| **OpenVAS / Greenbone** | Network | OSS vulnerability scanner; 50k+ plugins |

**Cloud Penetration Testing / Red Team**:
| Tool | Target | Key Features |
|------|--------|--------------|
| **Pacu (Rhino Security)** | AWS | AWS exploitation framework; IAM escalation; S3; Lambda backdoor; CloudTrail bypass |
| **ScoutSuite** | AWS, Azure, GCP | Multi-cloud security audit; 500+ rules; HTML report |
| **Prowler** | AWS | 300+ security checks; CIS/GDPR/HIPAA/PCI/NIST; HTML/CSV |
| **CloudSploit** | AWS, Azure, GCP | Open-source CSPM; 100+ checks; CI/CD integration |
| **Stormspotter** | Azure | Azure attack surface mapping; graph visualization |
| **ROADtools / ROADrecon** | Azure AD | Azure AD enumeration; token analysis; device registration |
| **MicroBurst** | Azure | Azure exploitation; storage blob enumeration; automation |
| **PowerZure** | Azure | Azure security assessment; privilege escalation; persistence |
| **Azurite** | Azure | Azure security exploration; resource enumeration |
| **GCPBucketBrute** | GCP | GCS bucket enumeration and content extraction |
| **CloudBrute** | AWS, Azure, GCP | Multi-cloud enumeration; storage, databases, functions |
| **Bucket Stream** | AWS | S3 bucket discovery; extraction; analysis |
| **Zeus (Praetorian)** | AWS | AWS security automation; IAM analysis; CIS checks |
| **Cartography** | Multi-cloud | Infrastructure graph; Neo4j; relationship analysis |
| **Stratus Red Team** | AWS, Azure, GCP | Granular attack simulation; detonation tests; IAC |
| **Atomic Red Team** | Multi-platform | MITRE ATT&CK mapping; test execution; detection validation |

**Cloud Forensics & Incident Response**:
| Tool | Target | Key Features |
|------|--------|--------------|
| **AWS Config** | AWS | Resource config history; compliance rules; drift detection |
| **CloudTrail Lake** | AWS | Managed audit and compliance data lake; SQL queries |
| **Amazon Detective** | AWS | Graph-based investigation; root cause analysis |
| **GuardDuty** | AWS | Threat detection; finding enrichment; integration with EventBridge |
| **Azure Resource Graph** | Azure | Resource exploration; change history; KQL queries |
| **Azure Activity Log** | Azure | Subscription events; diagnostic settings; retention |
| **Google Cloud Asset Inventory** | GCP | Resource inventory; IAM analysis; history |
| **Velociraptor** | Endpoints | Digital forensics; live response; OS-level collection |
| **Autopsy** | Disks | Forensic analysis; timeline; file carving; keyword search |
| **Sleuth Kit** | Disks | CLI forensic toolkit; disk analysis; file system forensics |
| **LiME** | Memory | Linux memory acquisition; forensics |
| **AVML (Azure VM Memory Linux)** | Azure | Memory acquisition for Azure Linux VMs |
| **DumpIt** | Memory | Windows memory acquisition |
| **Volatility** | Memory | Memory forensics framework; profile analysis; plugin-based |
| **Plaso (log2timeline)** | Timeline | Super timeline generation; file system, registry, event logs |
| **Timesketch** | Timeline | Collaborative forensic timeline analysis; web UI |
| **KAPE** | Windows | Collect and process Windows forensic artifacts quickly |
| **CyLR** | Hosts | Live response collection; cross-platform; SFTP/S3 export |
| **GRR Rapid Response** | Endpoints | Live forensics; incident response at scale (Google) |
| **OSQuery** | Endpoints | SQL-based OS instrumentation; security monitoring |

**DDoS Protection**:
| Tool | Type | Key Features |
|------|------|--------------|
| **Cloudflare** | Edge/SaaS | CDN-based DDoS; L3/4/7 mitigation; rate limiting; bot management; 200+ Tbps capacity |
| **Akamai Prolexic** | Edge/SaaS | Scrubbing centers; L3/4/7; 100+ Tbps capacity; SOC support |
| **AWS Shield** | Cloud | Standard (free): L3/4; Advanced ($3k/mo): L7, DRT, cost protection |
| **Azure DDoS Protection** | Cloud | Basic (free): always-on; Standard: adaptive tuning, SLA guarantee |
| **GCP Cloud Armor** | Cloud | WAF + DDoS; L3/4/7; Google edge network; rate limiting |
| **Imperva DDoS** | Cloud | WAF + DDoS; scrubbing centers; CDN integration; SOC |
| **Verisign DDoS** | Cloud | DNS-based mitigation; network scrubbing; 10+ Tbps |
| **Neustar DDoS** | Cloud | L3/4/7; DNS, NTP, SSDP reflection protection; SOC |
| **Fastly** | Edge/SaaS | CDN + DDoS; edge compute; WAF; instant purging |
| **Deflate / DDoS Deflate** | Server | OSS; detect and block IPs exceeding connection limits |

**Infrastructure as Code (IaC) Security Tools**:
| Tool | IaC Formats | Key Features |
|------|-------------|--------------|
| **Checkov** | Terraform, CFN, ARM, Bicep, K8s, Docker, Serverless | 1000+ policies; CLI; SaaS; CI/CD integration; auto-fix |
| **tfsec** | Terraform | HCL-focused; custom checks; CI/CD; SARIF output |
| **cfn-nag** | CloudFormation | CFN template scanning; IAM policy checks; open source |
| **Terrascan** | Terraform, K8s, Docker, CFN, ARM | CIS compliance; 500+ policies; OPA integration |
| **KICS (Checkmarx)** | IaC (16+ formats) | 70+ IaC types; SAST + SCA; CI/CD; SARIF |
| **Bridgecrew** | IaC | Checkov SaaS; compliance dashboards; auto-remediation |
| **Snyk IaC** | Terraform, K8s, CFN, ARM, Helm | CLI + SaaS; fix suggestions; policy engine |
| **Capsule** | K8s | Multi-tenancy; namespace governance; resource quotas |
| **jsPolicy** | K8s | Policy as JavaScript; admission controller; validation/mutation |
| **OPA (Conftest)** | IaC, K8s | Policy engine (Rego); admission control; CI/CD |
| **Sentinel (HashiCorp)** | Terraform, Vault, Consul, Nomad | Policy as code; multi-cloud; enterprise HashiCorp |
| **AzSkim (Azure)** | Azure ARM/Bicep | Azure CIS 1.4 compliance scope; automated |
| **Solano (GCP)** | GCP | GCP deployment validator; security checks |

**Monitoring & Observability**:
| Tool | Target | Key Features |
|------|--------|--------------|
| **Datadog** | Multi-cloud | Infrastructure + APM + Logs + Security; 700+ integrations; SIEM |
| **New Relic** | Multi-cloud | APM + infra + logs; AI-powered; full-stack observability |
| **Dynatrace** | Multi-cloud | Automatic discovery; Davis AI; runtime vulnerability; K8s |
| **Honeycomb** | Multi-cloud | Observability for high-cardinality; eBPF; SRE-focused |
| **Grafana** | Multi-cloud | Dashboards; Prometheus; Loki; Tempo; alerting; OSS |
| **Prometheus** | Multi-cloud | Metrics; alerting; time-series; CNCF; K8s native |
| **Loki** | Multi-cloud | Log aggregation; Prometheus-like; Grafana-native |
| **Elastic Observability** | Multi-cloud | Logs + metrics + APM + traces; ELK stack |
| **SigNoz** | Multi-cloud | Open-source Datadog alternative; traces + metrics + logs |
| **Netdata** | All | Real-time monitoring; 1s granularity; 2k+ metrics; OSS |
| **Uptime Kuma** | Multi-cloud | Self-hosted uptime monitoring; notifications; status pages |
| **Healthchecks.io** | Multi-cloud | Cron job monitoring; heartbeat; notification channels |
| **Better Uptime** | Multi-cloud | Uptime monitoring; status pages; incident management |

**Compliance & Audit Automation**:
| Tool | Frameworks | Key Features |
|------|------------|--------------|
| **Drata** | SOC 2, ISO 27001, HIPAA, GDPR, PCI, CCPA | Continuous compliance monitoring; 120+ integrations; evidence collection; automated control testing |
| **Vanta** | SOC 2, ISO 27001, HIPAA, PCI, GDPR | Trust management; automated evidence; vendor risk; questionnaires |
| **Secureframe** | SOC 2, ISO 27001, HIPAA, PCI, GDPR | Automated compliance; evidence collection; vendor risk; policy generator |
| **Thoropass (Laika)** | SOC 2, ISO 27001, HIPAA, PCI | Continuous compliance; auditor network; automated evidence |
| **ComplianceAsCode** | NIST, CIS, PCI, STIG | Open-source security content; automated hardening; SCAP |
| **OpenSCAP** | NIST, FISMA, FedRAMP | SCAP scanner; configuration validation; vulnerability assessment |
| **InSpec (Chef)** | CIS, custom | Compliance as code; automated tests; profiles; remote execution |
| **AWS Config Rules** | AWS CIS, PCI, NIST | Managed + custom rules; auto-remediation; compliance dashboard |
| **Azure Policy** | Azure CIS, PCI, NIST, SOC | Built-in + custom policies; DeployIfNotExists; Modify |
| **GCP Org Policies + Forseti** | GCP CIS, PCI, NIST | Organization constraints; scanner; enforcer; inventory |

---

## 52. Cloud Security Tips and Tricks

### 52.1 AWS Security Tips

**IAM Tips**:
1. **Use IAM Roles, not Users**: Never create IAM users for applications. Use roles for EC2, Lambda, ECS, EKS. Use IAM Identity Center (SSO) for humans.
2. **Least Privilege via IAM Access Analyzer**: Run `aws accessanalyzer` to identify unused permissions. Generate least-privilege policies based on actual usage.
3. **SCP Guardrails First**: Set SCPs BEFORE creating member accounts. Block root account actions, restrict regions, deny insecure resource creation at the Organization level.
4. **Permissions Boundaries**: Use permissions boundaries combined with SCPs to limit maximum permissions even for admin roles.
5. **Condition Keys are Free Security**: Always add `aws:SourceIp`, `aws:MultiFactorAuthPresent`, `aws:ViaAWSService`, `aws:RequestedRegion` conditions to policies. They cost nothing but prevent massive breaches.
6. **Auto-Rotate IAM Keys**: Use Secrets Manager auto-rotation for RDS/Redshift passwords. For IAM access keys, use Lambda to rotate on schedule.
7. **AWS CloudTrail Insights**: Enable CloudTrail Insights to automatically detect unusual API call patterns without writing custom rules.
8. **IAM Database Auth**: Use IAM database authentication for RDS/Aurora instead of passwords. Tokens auto-expire after 15 minutes.
9. **Root Account**: Enable hardware MFA. Delete root access keys. Never use root for daily operations. Set up billing alerts on the root account.
10. **Role Sessions**: Use `aws:SourceIdentity` condition in trust policies to track the original user assuming a role (prevents role confusion).

**S3 Tips**:
1. **Account-Level Block Public Access**: Enable immediately on ALL accounts. Cannot be overridden by bucket policies. This is the single most important S3 security control.
2. **S3 Object Lock**: Enable Object Lock when creating the bucket (can't be added later). Use Compliance mode for maximum protection. Prevents ransomware and accidental deletion.
3. **S3 Access Points**: Create separate access points per application/user group. Each AP has independent network controls and policies. Audit access via each AP.
4. **S3 Encryption**: Use `aws kms:GenerateDataKey` for client-side encryption. SSE-KMS gives you key usage audit trail. Enable default encryption at bucket level.
5. **S3 Lifecycle**: Set lifecycle rules to automatically transition to colder tiers and delete. Reduces storage costs AND attack surface (old data exposed in breaches).
6. **S3 Replication**: Use Cross-Region Replication (CRR) for DR compliance. Same-Region Replication (SRR) for log aggregation. Enable RTC (Replication Time Control) for predictable replication.
7. **S3 Event Notifications**: Use S3 Events + EventBridge + Lambda for automated responses (e.g., trigger malware scan on upload, auto-classify new objects).
8. **S3 Inventory**: Generate daily CSV/Parquet reports of all objects for compliance auditing. Use as reference for access reviews.
9. **S3 Requester Pays**: For shared datasets, enable Requester Pays to shift transfer costs to consumers. Prevents denial of wallet from your own account.
10. **S3 Batch Operations**: Use S3 Batch Operations to encrypt existing objects, change storage class, or copy objects at scale.

**Network Tips**:
1. **VPC Endpoints for Everything**: Never traverse the internet for AWS API calls. Use Gateway Endpoints (S3, DynamoDB) and Interface Endpoints (everything else). Free for Gateway; $ for Interface (but worth it for security).
2. **Security Group Referencing**: Reference other security groups (not CIDR blocks) in rules. This creates dynamic, auto-updating rules as instances scale.
3. **Prefix Lists**: Use managed prefix lists for frequently used IP ranges. Update once and all referencing SGs/NACLs update automatically.
4. **VPC Flow Logs at Scale**: Enable at VPC level (not subnet/ENI). Use `TrafficType: ALL`. Send to S3 with partition (year/month/day) for cost-effective querying via Athena.
5. **AWS Network Firewall Suricata Rules**: Use custom Suricata rules for domain-based egress filtering. Block cryptomining pools, malware C2, known bad IPs.
6. **Transit Gateway Network Manager**: Centralized view of all VPCs and on-prem networks. Monitor for unauthorized connections and routing changes.
7. **NAT Gateway Costs**: Each NAT Gateway costs ~$32/month + $0.045/GB. For high-volume accounts, use VPC endpoints to reduce NAT Gateway traffic significantly.
8. **PrivateLink vs VPC Peering**: Use PrivateLink for accessing services across accounts (no overlapping CIDR issues). Use VPC Peering for high-bandwidth inter-VPC traffic.
9. **Route53 Resolver Endpoints**: Use inbound/outbound resolver endpoints for hybrid DNS. Conditional forwarding rules for private DNS resolution.
10. **Egress-Only Internet Gateway**: For IPv6 workloads, use egress-only IGW to allow outbound-only internet access (no inbound).

**Logging Tips**:
1. **Centralized Logging Account**: Create a dedicated Security Tooling account for all logs. No production workloads in this account. Cross-account CloudTrail + Config aggregation.
2. **Immutable Logs**: S3 Object Lock in Compliance mode for log bucket. MFA delete enabled. KMS encryption. Access restricted to security read-only team.
3. **CloudTrail Organization Trail**: Create one Organization trail that covers ALL current and future accounts. Cannot be stopped by member accounts.
4. **Log Retention Automation**: S3 Lifecycle policy to transition logs. Intelligent-Tiering for unpredictable access patterns. Glacier Deep Archive at ~$1/TB/month for long-term.
5. **Athena on VPC Flow Logs**: Convert VPC Flow Logs to Parquet format. Query with Athena for network forensics. Costs pennies per query vs full SIEM ingestion.
6. **CloudWatch Contributor Insights**: For high-volume logs, use Contributor Insights to identify top contributors (source IPs, users, error codes) without ingesting all logs.
7. **GuardDuty for EKS**: Enable GuardDuty EKS protection. Detects suspicious Kubernetes API calls and pod-level threats.
8. **GuardDuty for RDS**: Enable GuardDuty RDS protection. Detects unusual RDS login patterns and SQL queries.
9. **GuardDuty for Lambda**: Enable GuardDuty Lambda protection. Detects suspicious function calls and IAM role abuse.
10. **Security Hub Automated Response**: Use Security Hub custom actions + EventBridge + Lambda for SOAR. Auto-remediate common findings (public S3, overly permissive SGs).

### 52.2 Azure Security Tips

1. **Azure PIM**: Use Privileged Identity Management for JIT (Just-In-Time) admin access. Time-bound roles, approval workflows, and activation audit. Reduces standing admin access by 95%+.
2. **Conditional Access**: Block all access from non-compliant devices, anonymous IPs, and risky sign-ins. Require MFA for all admin portals. Use session controls for sensitive apps.
3. **Azure Policy at Management Group**: Assign policies at the highest level (Management Group). They propagate to all subscriptions. Deny public IPs, require encryption, enforce tagging.
4. **Defender for Cloud (Free Tier)**: Enable on ALL subscriptions. The free tier provides CSPM + Secure Score + recommendations. The paid tier adds workload protection.
5. **Azure Key Vault Firewall**: Restrict Key Vault access to specific VNets and IPs. Enable soft-delete and purge protection. Deny public access for production vaults.
6. **Managed Identities**: Use managed identities for ALL Azure resources. Never use service principals with client secrets. System-assigned for single-resource; user-assigned for multi-resource.
7. **Azure Bastion**: Use Azure Bastion for RDP/SSH access. No public IPs on VMs. Browser-based HTML5 client. JIT access through Bastion.
8. **NSG Flow Logs**: Enable NSG Flow Logs on ALL subnets. Send to Log Analytics workspace for analysis. Traffic Analytics for geo-maps and traffic patterns.
9. **Azure Sentinel**: Use Free Data Connectors for Azure Activity, Azure AD, Defender, Office 365. Ingest all into Log Analytics for centralized SIEM. Use KQL for threat hunting.
10. **Azure Blueprints**: Define compliance baseline (policies, RBAC, ARM templates) as Blueprints. Apply to new subscriptions automatically. Version and update centrally.
11. **Azure AD Identity Protection**: Detect leaked credentials, risky sign-ins, and risky users. Automate with Conditional Access (force password change, block access).
12. **Azure Private Link**: Use for ALL PaaS services (SQL, Storage, Key Vault, AKS, etc.). Keeps traffic entirely on Microsoft backbone. No internet exposure.
13. **Azure Backup Vault Lock**: Enable Immutable Vault Lock (WORM) on Backup Vault. Prevents ransomware from deleting backups. Can't be disabled by anyone including admins.
14. **Azure Security Center Secure Score**: Aim for 95%+ Secure Score. Prioritize "High impact" recommendations. Track score trend weekly in management reporting.
15. **Azure RBAC for Management**: Use built-in roles (Contributor, Reader, Owner) sparingly. Create custom roles with explicit permissions. Deny assignments for critical exclusions.

### 52.3 GCP Security Tips

1. **Organization Policies**: Set at Organization level (not project). Deny public bucket access (`constraints/storage.publicAccessPrevention`). Restrict VM external IPs. Require OS Login. Disable service account key creation.
2. **VPC Service Controls**: Create perimeters around sensitive data projects. Prevent data exfiltration even from compromised service accounts. Block access from outside the perimeter.
3. **Cloud IAM Conditions**: Use IAM conditions for time-bound access, resource-based conditions, and IP-based restrictions. `request.time` for temporary access, `resource.service` for service-specific.
4. **Workload Identity Federation**: Use workload identity federation for CI/CD (no static keys). GitHub Actions, GitLab, BitBucket; any OIDC provider. Never download service account keys.
5. **Binary Authorization**: Enforce signed container images in GKE. Require attestation from approved authorities (KMS, Cloud Build). Block unsigned images from deploying.
6. **Cloud NAT with Logging**: Enable NAT gateway logging for all outbound traffic. Detect cryptomining, C2 communication, and anomalous egress patterns.
7. **Cloud Audit Logs**: Enable Data Access audit logs for sensitive services (BigQuery, Cloud Storage, Cloud SQL). Admin Activity is free and always-on. Data Access costs but is essential for compliance.
8. **Cloud Asset Inventory**: Use asset inventory for change detection, IAM policy analysis, and resource search. Export to BigQuery for historical analysis. Monitor for unexpected resource creation.
9. **Secret Manager**: Use Secret Manager for ALL secrets. IAM-based access control. Versioned and immutable. Audit trail of who accessed which secret and when.
10. **Shielded VMs**: Always use Shielded VMs (secure boot, vTPM, integrity monitoring). Protect against rootkits and boot-level malware. Verify boot integrity via Cloud Monitoring.
11. **Confidential VMs**: Use Confidential VMs for sensitive data processing. AMD SEV-ES memory encryption. No provider access to in-use memory. Use for multi-party computation and PII processing.
12. **Cloud DNS Logging**: Enable DNS logging for all zones. Detect DNS tunneling, malformed domains, and exfiltration attempts. Send logs to BigQuery for analysis.
13. **Cloud Shell**: Use Cloud Shell for CLI operations. Provides temporary, audited, authenticated shell. No local credential storage. Automatic OAuth2 token refresh.
14. **Firestore / Spanner Security**: Use CMEK for encryption at rest. VPC Service Controls for data exfiltration prevention. IAM conditions for row/collection level security.
15. **GKE Sandbox**: Use GKE Sandbox (gVisor) for untrusted workloads. Adds kernel isolation layer between container and host. Mitigates container escape vulnerabilities.

### 52.4 Multi-Cloud / General Security Tips

1. **Terraform Security**: Always run `terraform plan` with `-out=tfplan` and scan with Checkov/tfsec before apply. Use Terraform Cloud/Enterprise for remote state with encryption.
2. **Pre-Commit Hooks**: Add `pre-commit` hooks to ALL repos: `detect-secrets`, `truffleHog`, `checkov`, `terraform fmt`. Catch issues before they reach CI/CD.
3. **Ephemeral Credentials**: Use OIDC for CI/CD (GitHub Actions, GitLab CI, CircleCI). Never store cloud provider access keys in CI/CD secrets. OIDC issues short-lived (1 hour) tokens.
4. **Cloud Cost Alerts as Security Alerts**: An unexpected 5x cost spike often indicates a security incident (cryptomining, data exfiltration). Set budget alerts with security team notification.
5. **Tagging Strategy**: Enforce mandatory tags: `Environment`, `Owner`, `DataClassification`, `CostCenter`, `Compliance`, `DeploymentMethod`. Use tags in IAM conditions for fine-grained access.
6. **Incident Response Pre-Work**: Pre-provision forensic environment (analysis VM, tools installed, snapshot permissions). Pre-create SNS topics, Slack channels, and IR runbooks. Document AWS Support plan and escalation contacts.
7. **Tabletop Exercises**: Run quarterly tabletop exercises for common scenarios: public S3 bucket, compromised admin, ransomware, DDoS, cryptomining. Time each phase and improve.
8. **Security Moat**: Build security training into onboarding. Require cloud security fundamentals certification within 30 days. Run internal phishing campaigns quarterly.
9. **Customer Master Key Hygiene**: Rotate KMS keys annually (at minimum). Use automatic rotation for AWS KMS. Use separate keys per environment (dev, test, prod). Limit key administrators to 2-3 people.
10. **Service Control Policies**: Write SCPs from day one. Deny root account actions. Deny leaving Organizations. Deny disabling CloudTrail or GuardDuty. Deny non-compliant resource creation.
11. **Open Source Scanning**: Scan ALL dependencies for known vulnerabilities and licenses. Use Dependabot (GitHub) or Renovate. Set PR-level alerts. Patch critical within 24 hours.
12. **Security Champions**: Assign security champions in each engineering team. They amplify security practices, review designs, and triage findings. Multiply security team effectiveness by 10x.
13. **SBOM Everywhere**: Generate Software Bill of Materials (SBOM) for ALL deployments. CycloneDX or SPDX format. Use it for vulnerability correlation and supply chain risk management.
14. **Kubernetes Security**: Enable audit logs. Use OPA/Gatekeeper or Kyverno for admission policies. Enable Pod Security Standards (Restricted profile). Implement Network Policies (default deny).
15. **Container Image Hygiene**: Use minimal base images (distroless, scratch, alpine). Scan images in CI/CD with fail on CRITICAL. Sign images with Cosign. Use immutable tags.

---

## 53. Cloud Security Cheat Sheet

### 53.1 AWS CLI Security Commands Cheat Sheet

```bash
# =================== IAM ===================

# List users, groups, roles, policies
aws iam list-users
aws iam list-groups
aws iam list-roles
aws iam list-policies --scope Local

# Generate credential report (MFA, key usage, password last used)
aws iam generate-credential-report
aws iam get-credential-report --output text --query Content | base64 -d

# Analyze unused credentials
aws iam get-credential-report --output text --query Content | base64 -d | \
  awk -F',' '$4 == "false" {print "No MFA:", $1}'  # Users without MFA
awk -F',' '$5 == "N/A" {print "No keys:", $1}'      # No access keys (good)
awk -F',' '$10 == "true" && $16 > 90 {print "Key not rotated 90d:", $1}'  # Old keys

# Check for wildcard permissions
aws iam list-policies --scope Local --query 'Policies[].Arn' --output text | \
  xargs -I {} aws iam get-policy-version --policy-arn {} --version-id v1 --query \
  'PolicyVersion.Document.Statement[?Action==`*` || Action[0]==`*`]'

# Find unused IAM roles (>90 days)
aws iam list-roles --query 'Roles[?RoleLastUsed==null].[RoleName,CreateDate]' --output table

# List access keys and their last used date
aws iam list-access-keys --user-name <user> --query 'AccessKeyMetadata[].AccessKeyId'
aws iam get-access-key-last-used --access-key-id <key>

# Revoke sessions for compromised user
aws sts revoke-sessions-by-user --user-name <user>

# Apply IAM policy with condition (MFA required)
aws iam put-user-policy --user-name <user> --policy-name require-mfa \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action":"ec2:*","Resource":"*",\
  "Condition":{"Bool":{"aws:MultiFactorAuthPresent":"true"}}}]}'

# =================== S3 ===================

# Block public access at account level (CRITICAL)
aws s3control put-public-access-block --account-id <id> \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,\
  BlockPublicPolicy=true,RestrictPublicBuckets=true

# Check all buckets for public access
aws s3api list-buckets --query 'Buckets[].Name' --output text | xargs -I{} sh -c \
  'echo "Checking {}"; aws s3api get-public-access-block --bucket {} 2>/dev/null || echo "FAIL: No block"'

# List all buckets and their encryption status
aws s3api list-buckets --query 'Buckets[].Name' --output text | xargs -I{} sh -c \
  'enc=$(aws s3api get-bucket-encryption --bucket {} 2>&1); \
   [ -z "$enc" ] && echo "NO ENCRYPTION: {}" || echo "OK: {}"'

# Enable versioning on bucket
aws s3api put-bucket-versioning --bucket <name> \
  --versioning-configuration Status=Enabled

# Add bucket policy restricting to VPC
aws s3api put-bucket-policy --bucket <name> --policy '{
  "Version":"2012-10-17",
  "Statement":[{
    "Effect":"Deny",
    "Principal":"*",
    "Action":"s3:*",
    "Resource":["arn:aws:s3:::<bucket>","arn:aws:s3:::<bucket>/*"],
    "Condition":{"StringNotEquals":{"aws:SourceVpc":"vpc-xxx"}}
  }]
}'

# Enable Object Lock
# Can only be set on bucket creation:
aws s3api create-bucket --bucket <name> --object-lock-enabled-for-bucket
aws s3api put-object-lock-configuration --bucket <name> \
  --object-lock-configuration '{"ObjectLockEnabled":"Enabled","Rule":{"DefaultRetention":\
  {"Mode":"COMPLIANCE","Days":365}}}'

# =================== ENCRYPTION / KMS ===================

# List KMS keys
aws kms list-keys
aws kms list-aliases

# Enable automatic key rotation
aws kms enable-key-rotation --key-id <key-id>

# Encrypt/decrypt with KMS
aws kms encrypt --key-id <key-id> --plaintext fileb://plain.txt --output text --query CiphertextBlob
aws kms decrypt --ciphertext-blob fileb://encrypted.txt --output text --query Plaintext

# Generate data key (for client-side encryption)
aws kms generate-data-key --key-id <key-id> --key-spec AES_256

# List grants on KMS key (who has permission to use your key?)
aws kms list-grants --key-id <key-id>

# Revoke external access to KMS key
aws kms revoke-grant --key-id <key-id> --grant-id <grant-id>

# =================== LOGGING ===================

# Create multi-region CloudTrail
aws cloudtrail create-trail --name org-trail --s3-bucket-name <bucket> \
  --is-multi-region-trail --is-organization-trail --enable-log-file-validation \
  --kms-key-id <key-id>

# Start logging
aws cloudtrail start-logging --name <trail-name>

# Enable CloudTrail data events for S3/Lambda
aws cloudtrail put-event-selectors --trail-name <name> --event-selectors '[
  {"ReadWriteType":"All","IncludeManagementEvents":true,
   "DataResources":[{"Type":"AWS::S3::Object","Values":["arn:aws:s3:::<bucket>/"]}]
  }]'

# Enable VPC Flow Logs
aws ec2 create-flow-logs --resource-type VPC --resource-ids <vpc-id> \
  --traffic-type ALL --log-destination-type cloud-watch-logs \
  --log-group-name vpc-flow-logs --deliver-logs-permission-arn <role-arn>

# Create Config recorder
aws configservice put-configuration-recorder --configuration-recorder \
  name=default,roleARN=<role-arn>
aws configservice start-configuration-recorder --configuration-recorder-name default

# =================== GUARDDUTY ===================

# Enable GuardDuty
aws guardduty create-detector --enable

# List GuardDuty findings
aws guardduty list-findings --detector-id <id>
aws guardduty get-findings --detector-id <id> --finding-ids <ids>

# Create GuardDuty filter (ignore known false positives)
aws guardduty create-filter --detector-id <id> --name exclude-known-ips \
  --finding-criteria '{"Criterion":{"sourceIpAddress":{"Eq":["203.0.113.0"]}}}' \
  --action ARCHIVE

# =================== SECURITY HUB ===================

# Enable Security Hub
aws securityhub enable-security-hub --enable-default-standards

# Get findings by severity
aws securityhub get-findings --filters '{"SeverityLabel":[{"Value":"CRITICAL","Comparison":"EQUALS"}]}'

# Batch update findings status
aws securityhub batch-update-findings --finding-identifiers <ids> --workflow Status=RESOLVED

# =================== INSPECTOR ===================

# Enable Inspector
aws inspector2 enable --resource-types EC2 ECR

# Get vulnerability summary
aws inspector2 list-findings --filter-criteria \
  '{"severity":[{"comparison":"GT","value":0}]}'

# =================== NETWORK ===================

# Check security groups for SSH from anywhere
aws ec2 describe-security-groups --filters Name=ip-permission.from-port,Values=22 \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName,VpcId]'

# Check for default VPCs (should be removed)
aws ec2 describe-vpcs --filters Name=isDefault,Values=true \
  --query 'Vpcs[].VpcId'

# =================== REGIONS ===================

# List all regions
aws ec2 describe-regions --query 'Regions[].RegionName'

# Enable CloudTrail in all regions (check current trails)
aws cloudtrail describe-trails --query 'trailList[?IsMultiRegionTrail==`true`]'

# =================== COMPLIANCE ===================

# AWS Artifact: Get compliance reports
aws artifact download-agreement --agreement-name "AWS Customer Agreement"
aws artifact get-report --report-id <report-id>

# Create compliance report with Audit Manager
aws auditmanager create-assessment --name "SOC2-$(date +%Y)" \
  --framework-id <framework-id> --aws-account <account-id>

# =================== CONTAINER / EKS ===================

# List EKS clusters
aws eks list-clusters

# Get EKS cluster security config
aws eks describe-cluster --name <cluster> --query cluster.resourcesVpcConfig

# Update kubeconfig
aws eks update-kubeconfig --name <cluster-name>

# =================== SECRETS MANAGER ===================

# Create secret
aws secretsmanager create-secret --name prod-db-pass --secret-string <password>

# Rotate secret immediately
aws secretsmanager rotate-secret --secret-id <secret-arn>

# List all secrets
aws secretsmanager list-secrets --query 'SecretList[?Name!=null].[Name,LastRotatedDate]'
```

### 53.2 Azure CLI Security Commands Cheat Sheet

```bash
# =================== IDENTITY / AZURE AD ===================

# List users, groups, roles
az ad user list --output table
az ad group list --output table
az ad sp list --output table

# List role assignments at subscription level
az role assignment list --subscription <sub-id> --output table

# Check MFA status for users (requires Azure AD Premium)
az ad user list --query "[].{UPN:userPrincipalName, MFA:strongAuthenticationMethods}" --output table

# Create custom RBAC role
az role definition create --role-definition '{
  "Name": "Storage Read Only",
  "Description": "Read only access to storage",
  "Actions": ["Microsoft.Storage/storageAccounts/read", "Microsoft.Storage/storageAccounts/listKeys/action"],
  "AssignableScopes": ["/subscriptions/<sub-id>"]}'

# Get Azure AD sign-in logs
az monitor activity-log list --resource-provider Microsoft.AzureActiveDirectory

# =================== DEFENDER FOR CLOUD ===================

# Enable Defender for Cloud on subscription
az security auto-provisioning-setting update --name default --auto-provision On

# Get Secure Score
az security secure-score list --query "[].{Name:displayName, Score:currentScore}"

# Get recommendations
az security recommendation list --query "[?severity=='High'].[name,displayName]"

# =================== KEY VAULT ===================

# Create Key Vault
az keyvault create --name <name> --resource-group <rg> --location <loc> \
  --enabled-for-deletion true --bypass AzureServices

# Set secret
az keyvault secret set --vault-name <name> --name "mysecret" --value "s3cr3t"

# Enable soft-delete and purge protection
az keyvault update --name <name> --enable-soft-delete true \
  --enable-purge-protection true

# Set firewall to deny public access
az keyvault update --name <name> --default-action Deny

# =================== NETWORK ===================

# List NSGs with rules
az network nsg list --query "[].{Name:name, Rules:securityRules[].{Name:name,Port:destinationPortRange,Source:sourceAddressPrefix}}"

# Enable NSG Flow Logs
az network watcher flow-log create --nsg <nsg-name> --resource-group <rg> \
  --storage-account <storage-account> --retention 90

# List public IPs
az network public-ip list --query "[].{Name:name, IP:ipAddress, VM:ipConfiguration.virtualMachine.id}" --output table

# =================== STORAGE ===================

# Check storage account for public access
az storage account show --name <name> --query "allowBlobPublicAccess"

# Deny public access
az storage account update --name <name> --allow-blob-public-access false

# Enable infrastructure encryption (double encryption)
az storage account update --name <name> --require-infrastructure-encryption

# =================== LOGGING ===================

# Enable diagnostic settings for subscription
az monitor diagnostic-settings create --name SecurityAudit --subscription <sub> \
  --workspace <log-analytics-workspace> --logs '[{"category":"Administrative","enabled":true}]'

# Query Activity Log
az monitor activity-log list --start-time 2024-01-01 --max-events 100

# =================== POLICY ===================

# Assign policy to subscription
az policy assignment create --name "deny-public-ip" --policy <policy-definition-id> \
  --scope /subscriptions/<sub-id>

# List non-compliant resources
az policy state list --filter "complianceState eq 'NonCompliant'"
```

### 53.3 GCP gcloud Security Commands Cheat Sheet

```bash
# =================== IAM ===================

# List all service accounts
gcloud iam service-accounts list

# List IAM policies at project level
gcloud projects get-iam-policy <project-id> --format json

# Check if service account key exists
gcloud iam service-accounts keys list --iam-account <sa>@<project>.iam.gserviceaccount.com

# Disable service account key creation at org level
gcloud resource-manager org-policies disable-enforce \
  constraints/iam.disableServiceAccountKeyCreation \
  --organization <org-id>

# Add IAM binding (condition example)
gcloud projects add-iam-policy-binding <project> \
  --member user:user@example.com --role roles/compute.viewer \
  --condition 'expression=request.time < timestamp("2025-01-01T00:00:00Z"),title=temporary-access'

# Create custom IAM role
gcloud iam roles create StorageAuditor --project <project> \
  --title "Storage Auditor" --permissions storage.buckets.get,storage.objects.get \
  --stage GA

# =================== STORAGE / GCS ===================

# Check public access prevention on bucket
gcloud storage buckets describe gs://<bucket> --format="value(iamConfiguration.publicAccessPrevention)"

# Enforce public access prevention
gcloud storage buckets update gs://<bucket> --public-access-prevention

# Check all buckets for public access
gcloud storage buckets list --format="value(name)" | xargs -I{} sh -c \
  'pub=$(gcloud storage buckets describe gs://{} --format="value(iamConfiguration.publicAccessPrevention)" 2>/dev/null); \
   echo "{}: $pub"'

# Enable uniform bucket-level access (disable ACLs)
gcloud storage buckets update gs://<bucket> --uniform-bucket-level-access

# Set retention policy (immutable)
gcloud storage buckets update gs://<bucket> --retention-period 365d

# Add CMEK to bucket
gcloud storage buckets update gs://<bucket> --default-encryption-key=projects/<p>/locations/global/keyRings/<kr>/cryptoKeys/<key>

# =================== KMS ===================

# List key rings and keys
gcloud kms keyrings list --location global
gcloud kms keys list --keyring <keyring> --location global

# Rotate key
gcloud kms keys rotate --key <key> --keyring <kr> --location global

# Encrypt with CMEK
gcloud kms encrypt --plaintext-file=secret.txt --ciphertext-file=secret.enc \
  --key <key> --keyring <kr> --location global

# =================== ORGANIZATION POLICIES ===================

# List organization policies
gcloud resource-manager org-policies list --organization <org-id>

# Set VM external IP restriction
gcloud resource-manager org-policies set-policy --organization <org-id> policy.yaml
# policy.yaml content:
# constraint: constraints/compute.vmExternalIpAccess
# listPolicy:
#   allValues: DENY

# List effective org policies
gcloud resource-manager org-policies describe \
  constraints/iam.disableServiceAccountKeyCreation --effective \
  --organization <org-id>

# =================== LOGGING ===================

# List log sinks
gcloud logging sinks list

# Export audit logs to BigQuery
gcloud logging sinks create audit-bq-sink \
  bigquery.googleapis.com/projects/<project>/datasets/audit_logs \
  --log-filter='logName:"cloudaudit.googleapis.com"'

# Query logs (Admin Activity)
gcloud logging read 'logName="projects/<project>/logs/cloudaudit.googleapis.com%2Factivity"'

# Enable Data Access audit logs
gcloud logging read 'logName="projects/<project>/logs/cloudaudit.googleapis.com%2Fdata_access"'

# Create log metric for admin activity
gcloud logging metrics create root-login --description "Root account login" \
  --log-filter='protoPayload.methodName="google.cloud.auth.LoginService.LoginSuccess" AND protoPayload.authenticationInfo.principalEmail="root"'

# =================== SECURITY COMMAND CENTER ===================

# List SCC findings
gcloud scc findings list --organization <org-id> --category OPEN_FIREWALL

# List SCC assets
gcloud scc assets list --organization <org-id>

# =================== COMPUTE / GCE ===================

# List VMs with public IPs
gcloud compute instances list --format="value(name,zone,networkInterfaces[].accessConfigs[0].natIP)"

# Enable Shielded VM (secure boot, vTPM, integrity monitoring)
gcloud compute instances create <name> --shielded-vm --shielded-vm-secure-boot

# List firewall rules open to 0.0.0.0/0
gcloud compute firewall-rules list --filter="allowed[].ports=22 AND disabled=false" \
  --format="table(name,network,sourceRanges.list())"

# =================== GKE ===================

# Get cluster security settings
gcloud container clusters describe <cluster> --zone <zone> \
  --format="value(authenticatorGroupsConfig,networkPolicyEnabled,privateClusterConfig.enablePrivateNodes)"

# Enable Workload Identity
gcloud container clusters update <cluster> --zone <zone> --workload-pool=<project>.svc.id.goog

# Enable Binary Authorization
gcloud container clusters update <cluster> --zone <zone> --binauthz-evaluation-mode=PROJECT_SINGLETON

# =================== SECRETS ===================

# Create secret
gcloud secrets create my-secret --replication-policy automatic

# Add secret version
echo "s3cr3t" | gcloud secrets versions add my-secret --data-file=-

# List secrets
gcloud secrets list

# Access secret version
gcloud secrets versions access latest --secret my-secret

# =================== VPC SERVICE CONTROLS ===================

# Create access policy (org level)
gcloud access-context-manager policies create --organization <org-id> --title "Security Policy"

# Create service perimeter
gcloud access-context-manager perimeters create <name> \
  --policy <policy-id> --title "Data Perimeter" \
  --resources "projects/<project-number>" \
  --restricted-services "storage.googleapis.com" \
  --vpc-allowed-services "private.googleapis.com"
```

### 53.4 General Cloud Security Quick Commands

```bash
# =================== IAM AUDIT ===================

# Find users with admin access (AWS)
aws iam list-users --query "Users[].UserName" --output text | \
  xargs -I {} sh -c 'echo "Checking {}: $(aws iam list-attached-user-policies --user-name {} --query AttachedPolicies[].PolicyName --output text)"'

# Find overly permissive roles (Azure)
az role definition list --query "[?permissions[?actions[?contains(@, '*')]]].{Name:roleName, Actions:permissions[0].actions}"

# Find service account keys older than 90 days (GCP)
for sa in $(gcloud iam service-accounts list --format="value(email)"); do
  gcloud iam service-accounts keys list --iam-account $sa \
    --format="value(name.basename(),validAfterTime)" | \
    while read key created; do
      age=$(( ($(date +%s) - $(date -d "$created" +%s)) / 86400 ))
      [ $age -gt 90 ] && echo "OLD KEY: $sa $key ($age days)"
    done
done

# =================== NETWORK SCAN ===================

# Find open SSH/RDP globally (AWS)
aws ec2 describe-security-groups --filters \
  Name=ip-permission.from-port,Values=22,3389 \
  --query 'SecurityGroups[?IpPermissions[?IpRanges[?CidrIp==`0.0.0.0/0`]]].[GroupId,GroupName,Description]'

# Find public endpoints (Azure)
az network public-ip list --query "[?ipAddress!=null].{Name:name, IP:ipAddress, FQDN:dnsSettings.fqdn}"

# Find VM with external IPs (GCP)
gcloud compute instances list --format="table(name,zone,EXTERNAL_IP:label=ExternalIP)"

# =================== COMPLIANCE SCAN (ONE-LINERS) ===================

# AWS — CIS benchmark quick check
aws configservice describe-compliance-by-config-rule --query \
  'ComplianceByConfigRules[?Compliance.ComplianceType==`NON_COMPLIANT`].[ConfigRuleName,Compliance.ComplianceType]'

# AWS — Find unencrypted resources
echo "=== Unencrypted RDS ===" && aws rds describe-db-instances --query \
  'DBInstances[?StorageEncrypted==`false`].[DBInstanceIdentifier]'
echo "=== Unencrypted EBS ===" && aws ec2 describe-volumes --query \
  'Volumes[?Encrypted==`false`].[VolumeId,Size]'
echo "=== Unencrypted S3 ===" && aws s3api list-buckets --query 'Buckets[].Name' --output text | \
  xargs -I{} sh -c 'aws s3api get-bucket-encryption --bucket {} >/dev/null 2>&1 || echo "NO ENCRYPTION: {}"'

# Azure — Check diagnostic settings
az monitor diagnostic-settings list --resource /subscriptions/<sub-id> --query \
  "[?logs==null || logs[?enabled==`false`]].name"

# GCP — Check for public buckets
gcloud storage buckets list --format="value(name)" | xargs -I{} sh -c \
  'pub=$(gcloud storage buckets describe gs://{} --format="value(iamConfiguration.publicAccessPrevention)" 2>/dev/null); \
   [ "$pub" != "enforced" ] && echo "NOT LOCKED: {} ($pub)"'

# =================== INCIDENT RESPONSE (QUICK) ===================

# AWS — Immediate IAM containment
aws iam update-access-key --user-name <user> --access-key-id <key> --status Inactive
aws iam detach-user-policy --user-name <user> --policy-arn <arn>
aws iam put-user-policy --user-name <user> --policy-name deny-all \
  --policy-document '{"Version":"2012-10-17","Statement":[{"Effect":"Deny","Action":"*","Resource":"*"}]}'
aws sts revoke-sessions-by-user --user-name <user>

# Azure — Immediate role revocation
az role assignment delete --assignee <user> --scope /subscriptions/<sub-id>

# GCP — Disable service account
gcloud iam service-accounts disable <sa>@<project>.iam.gserviceaccount.com
gcloud iam service-accounts keys list --iam-account <sa>@<project>.iam.gserviceaccount.com | \
  tail -n +2 | awk '{print "gcloud iam service-accounts keys delete "$1" --iam-account <sa>@<project>.iam.gserviceaccount.com"}' | sh

# =================== COST SPIRE DETECTION ===================

# AWS — Find EC2 instances by launch time (potential cryptomining)
aws ec2 describe-instances --query \
  'Reservations[].Instances[?State.Name==`running`].[InstanceId,LaunchTime,InstanceType,Placement.AvailabilityZone]' \
  --output table | sort -k2

# AWS — Find unusually high data transfer
aws ec2 describe-instances --query \
  'Reservations[].Instances[?State.Name==`running`].[InstanceId,NetworkInterfaces[0].Association.PublicIp]' \
  --output table

# AWS — Check S3 for large data transfers
aws cloudwatch get-metric-statistics --namespace AWS/S3 --metric-name BucketSizeBytes \
  --dimensions Name=BucketName,Value=<bucket> Name=StorageType,Value=StandardStorage \
  --start-time $(date -d '7 days ago' --utc +%Y-%m-%dT%H:%M:%SZ) --end-time $(date --utc +%Y-%m-%dT%H:%M:%SZ) \
  --period 86400 --statistics Average
```

### 53.5 Cloud Security URLs Quick Reference

**AWS Security**:
- IAM Best Practices: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
- Security Pillar (Well-Architected): https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/
- AWS Security Blog: https://aws.amazon.com/blogs/security/
- AWS Security Reference Architecture: https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/
- CIS AWS Foundations: https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-standards-cis.html
- AWS Abuse Reporting: https://aws.amazon.com/report-abuse/
- AWS Penetration Testing: https://aws.amazon.com/security/penetration-testing/
- AWS KMS Key Policies: https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html
- S3 Security Best Practices: https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
- GuardDuty Findings: https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html

**Azure Security**:
- Azure Security Best Practices: https://learn.microsoft.com/en-us/azure/security/
- Microsoft Defender for Cloud: https://learn.microsoft.com/en-us/azure/defender-for-cloud/
- Azure AD Security: https://learn.microsoft.com/en-us/azure/active-directory/fundamentals/security-operations-introduction
- Azure Policy Built-in Definitions: https://learn.microsoft.com/en-us/azure/governance/policy/samples/built-in-policies
- Azure Security Benchmark: https://learn.microsoft.com/en-us/security/benchmark/azure/
- CIS Azure Foundations: https://www.cisecurity.org/benchmark/azure/
- Azure Penetration Testing: https://learn.microsoft.com/en-us/azure/security/fundamentals/pen-testing
- Azure Architecture Center: https://learn.microsoft.com/en-us/azure/architecture/

**GCP Security**:
- GCP Security Best Practices: https://cloud.google.com/docs/security
- Security Command Center: https://cloud.google.com/security-command-center
- GCP Security Blog: https://cloud.google.com/blog/products/identity-security
- GCP Compliance: https://cloud.google.com/compliance
- GCP Security Blueprint: https://cloud.google.com/security/blueprint
- CIS GCP Foundations: https://www.cisecurity.org/benchmark/google_cloud_computing_platform/
- GCP Penetration Testing: https://cloud.google.com/security/compliance/penetration-testing
- GCP IAM Conditions: https://cloud.google.com/iam/docs/conditions-overview
- VPC Service Controls: https://cloud.google.com/vpc-service-controls

**Multi-Cloud / General**:
- Cloud Security Alliance (CSA): https://cloudsecurityalliance.org/
- CSA CCM: https://cloudsecurityalliance.org/research/cloud-controls-matrix
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- NIST CSF: https://www.nist.gov/cyberframework
- CIS Benchmarks: https://www.cisecurity.org/benchmark/cloud_security
- MITRE ATT&CK Cloud Matrix: https://attack.mitre.org/matrices/enterprise/cloud/
- ISC2 CCSP: https://www.isc2.org/Certifications/CCSP
- Prowler: https://github.com/prowler-cloud/prowler
- ScoutSuite: https://github.com/nccgroup/ScoutSuite
- Stratus Red Team: https://github.com/DataDog/stratus-red-team
- Cartography: https://github.com/lyft/cartography
- Cloud Custodian: https://cloudcustodian.io/
- S3 Object Lock: https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html
- IMDSv2: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html

### 53.6 Quick Reference Tables

**Port Security Table**:
| Port | Service | Cloud Rule | Risk if Exposed |
|------|---------|-----------|-----------------|
| 22 | SSH | Block from 0.0.0.0/0; use SSM/Bastion | Brute force, credential theft, server compromise |
| 3389 | RDP | Block from 0.0.0.0/0; use Azure Bastion | Brute force, ransomware (common entry vector) |
| 3306 | MySQL/MariaDB | Private subnet only; SG from app tier | Data exfiltration, ransomware, SQL injection |
| 5432 | PostgreSQL | Private subnet only; SG from app tier | Data exfiltration, ransomware |
| 1433 | SQL Server | Private subnet only; SG from app tier | Data exfiltration, ransomware |
| 6379 | Redis | Private subnet only; auth required | Data exfiltration, cache poisoning |
| 27017 | MongoDB | Private subnet only; auth required | Data exfiltration, complete DB takeover |
| 443 | HTTPS | Public (with WAF) | Web app attacks (mitigated by WAF) |
| 80 | HTTP | Redirect to HTTPS | Unencrypted traffic |
| 25 | SMTP | Block outbound (abuse risk) | Spam relay, reputation damage |
| 9200 | Elasticsearch | Private subnet only; auth required | Data exfiltration, complete cluster takeover |

**Encryption Key Sizes and Algorithms**:
| Algorithm | Type | Minimum Size | Recommended Size | Cloud Support |
|-----------|------|-------------|-----------------|---------------|
| AES | Symmetric | 128-bit | 256-bit | All providers default |
| RSA | Asymmetric | 2048-bit | 4096-bit | KMS, CloudHSM, Key Vault, Cloud KMS |
| ECDSA | Asymmetric | P-256 | P-384 | KMS, CloudHSM, Key Vault, Cloud KMS |
| Ed25519 | Asymmetric | 256-bit | 256-bit | SSH, code signing |
| ChaCha20 | Symmetric | 256-bit | 256-bit | TLS 1.3 |
| SHA-2 | Hash | 256-bit | 256/384/512-bit | All providers |
| SHA-3 | Hash | 256-bit | 256/384/512-bit | Cloud KMS |

**Log Retention Requirements (Common Frameworks)**:
| Regulation | Minimum Retention | Notes |
|------------|------------------|-------|
| GDPR | 3 years | Depends on data type; Art 5(1)(e) |
| HIPAA | 6 years | 45 CFR 164.530 |
| PCI DSS v4.0 | 12 months minimum; 3-7 years recommended | Requirement 10.7 |
| SOC 2 | Per audit cycle (typically 1-3 years) | Defined in audit scope |
| SOX | 7 years | SEC 17a-4 |
| FedRAMP | 7 years | NIST 800-53 AU-11 |
| NIST CSF | 3-5 years | Per organization policy |
| CCPA | Duration of business relationship + reasonable period | Civil Code 1798.130 |

**IAM Best Practices Comparison**:
| Practice | AWS Implementation | Azure Implementation | GCP Implementation |
|----------|-------------------|---------------------|-------------------|
| MFA Enforcement | IAM policy condition `aws:MultiFactorAuthPresent` | Conditional Access policy requiring MFA | Cloud Identity MFA enforcement |
| Least Privilege | IAM Access Analyzer; unused permission analysis | Azure AD Entitlement Management; PIM | IAM Recommender; policy analysis |
| Privileged Access Management | IAM Access Analyzer; no native PAM | Azure AD PIM (JIT activation) | No native PAM (custom or third-party) |
| Federation | IAM Identity Center; SAML/OIDC | Azure AD (primary IdP) | Cloud Identity; Workforce Identity Federation |
| Service/App Identity | IAM Roles (EC2, Lambda, ECS, EKS) | Managed Identities (system/user assigned) | Service Accounts (with key rotation) |
| Permission Boundaries | Permissions Boundaries + SCPs | Azure Blueprints + Management Groups | Organization Policies + Custom Roles |
| Temporary Credentials | STS tokens (max 12h for roles, 36h for IAM) | Managed Identity tokens (auto-renewed) | Service Account tokens (max 1h) |
| Access Reviews | IAM Access Analyzer external access | Azure AD Access Reviews | IAM Recommender; Policy Analyzer |
| Emergency Access | Break-glass IAM users with MFA | Break-glass Azure AD accounts | Break-glass service accounts |
| Cross-Account Access | Cross-account IAM roles (STS AssumeRole) | Azure Lighthouse (delegated resource management) | Cross-project IAM; service account impersonation |

**Dangerous Cloud Permissions (Monitor Closely)**:
| AWS | Azure | GCP |
|-----|-------|-----|
| `iam:CreateUser` | `Microsoft.Authorization/roleAssignments/write` | `iam.serviceAccounts.create` |
| `iam:CreateAccessKey` | `Microsoft.Authorization/roleDefinitions/write` | `iam.serviceAccountKeys.create` |
| `iam:CreatePolicyVersion` | `Microsoft.AAD/domainServices/configurations` | `iam.roles.create` |
| `iam:SetDefaultPolicyVersion` | `Microsoft.Management/managementGroups/write` | `iam.roles.update` |
| `iam:PassRole` | `Microsoft.Authorization/policyAssignments/write` | `iam.serviceAccounts.setIamPolicy` |
| `iam:UpdateAssumeRolePolicy` | `Microsoft.Security/policies/write` | `resourcemanager.projects.setIamPolicy` |
| `ec2:RunInstances` (large instances) | `Microsoft.Compute/virtualMachines/write` | `compute.instances.create` (GPU instances) |
| `ec2:ModifyInstanceAttribute` | `Microsoft.Network/networkSecurityGroups/write` | `compute.firewalls.create` |
| `s3:PutBucketPolicy` | `Microsoft.Storage/storageAccounts/write` | `storage.buckets.setIamPolicy` |
| `organizations:InviteAccountToOrganization` | `Microsoft.Subscription/aliases/write` | `resourcemanager.organizations.get` |

---

> **Ultimate Cloud Security Reminder**: 
> - Identity is the new perimeter — **IAM is your most important security control**
> - The provider secures infrastructure — **YOU secure data, identities, and configurations**
> - Most breaches come from **misconfiguration**, not provider vulnerabilities
> - **Encrypt everything**: at rest (AES-256), in transit (TLS 1.3), in use (Confidential Computing)
> - **Log everything**: CloudTrail/Activity Log/Audit Log, VPC Flow Logs, WAF logs, DNS logs, database audit logs
> - **Monitor continuously**: GuardDuty/Defender/SCC, SIEM, CSPM, threat intelligence
> - **Automate responses**: SOAR playbooks, auto-remediation, policy as code
> - **Test regularly**: penetration testing, tabletop exercises, red team, security chaos engineering
> - **Patch everything**: OS, application, container, IaC dependencies — patching is your cheapest security control
> - **Think in terms of blast radius**: least privilege, network segmentation, multi-account architecture, immutable infrastructure
> - **Assume breach**: Design for failure; implement containment, isolation, and recovery procedures before they're needed
> - **Security is not a product — it is a continuous process** that must evolve with your cloud environment


---

## 54. Zero Trust Architecture in the Cloud

### 54.1 Zero Trust Principles (NIST SP 800-207)

**Core Tenets**:
1. **Never Trust, Always Verify**: No implicit trust based on network location; every access request must be authenticated and authorized
2. **Assume Breach**: Design for compromised state; minimize blast radius; segment access
3. **Least Privilege Access**: Grant minimum permissions necessary; JIT elevation
4. **Continuous Verification**: Not just at login — verify throughout session (risk-based)
5. **Micro-Segmentation**: Break network into smallest logical units; enforce per-connection
6. **Device Trust**: Verify device health/compliance before granting access
7. **Data-Centric Security**: Protect data regardless of location; encrypt, classify, DLP

### 54.2 Zero Trust Control Plane Architecture

**Control Plane Components**:
```
Policy Engine (PE) ─→ Policy Administrator (PA) ─→ PEP (Gateway/Agent)
       │                       │                           │
       ▼                       ▼                           ▼
  Continuous diagnostics  Session management          Enforce allow/deny
  Threat intelligence    Token/credential issue       Log all decisions
  Compliance checks      Re-authentication triggers   Block/quarantine
```

**AWS Zero Trust Implementation**:
- **Identity**: IAM (policy + conditions), IAM Identity Center (SSO), Cognito (external users)
- **Device**: Systems Manager (patch/compliance), Device Farm (mobile), Workspaces (VDI)
- **Network**: VPC (micro-segmentation), Security Groups (per-instance), Network Firewall, VPC endpoints
- **Application**: WAF (L7 filtering), API Gateway (auth, throttling), App Mesh (service mesh mTLS)
- **Data**: KMS (encryption), Macie (classification), S3 Block Public Access, Lake Formation (column-level)
- **Monitoring**: GuardDuty (threat), CloudTrail (audit), Detective (investigation), Security Hub (aggregation)

**Azure Zero Trust Implementation**:
- **Identity**: Azure AD Conditional Access, PIM, Identity Protection
- **Device**: Intune (compliance), Microsoft Defender for Endpoint (health), Azure AD device registration
- **Network**: NSG/ASG (micro-segmentation), Azure Firewall, Private Link, Virtual WAN
- **Application**: App Gateway WAF, API Management, Azure AD Application Proxy
- **Data**: Information Protection (labels), Purview (governance), Key Vault, Defender for Cloud Apps
- **Monitoring**: Sentinel (SIEM), Defender for Cloud, Azure Monitor

**GCP Zero Trust Implementation**:
- **Identity**: Cloud IAM, Identity-Aware Proxy (IAP), BeyondCorp Enterprise
- **Device**: Endpoint Verification, Access Context Manager (device policy)
- **Network**: VPC firewall rules, VPC Service Controls, Cloud Armor
- **Application**: IAP (context-aware access), Apigee (API security)
- **Data**: CMEK/CSEK, Data Loss Prevention API, Sensitive Data Protection
- **Monitoring**: Security Command Center, Chronicle, Cloud Audit Logs

### 54.3 BeyondCorp (Google's Zero Trust Model)

**BeyondCorp Principles**:
- Access based on user identity + device state, not network IP
- No VPN required; all access through context-aware proxy
- Device inventory with hardware/software attestation
- Automated certificate management for device identity
- Continuous device compliance scanning

**BeyondCorp Enterprise Components**:
1. **Access Context Manager**: Define access levels (device OS, IP range, device policy)
2. **Identity-Aware Proxy (IAP)**: Tunnel HTTPS traffic; enforce identity + context; no firewall rules
3. **VPC Service Controls**: Prevent data exfiltration from managed services
4. **Endpoint Verification**: Chrome extension for device compliance (OS patch, disk encrypted, screen lock)
5. **Context-Aware Access**: Evaluate device + user + request context before granting access

### 54.4 Micro-Segmentation in Cloud

**Implementation Strategies**:
| Layer | AWS | Azure | GCP |
|-------|-----|-------|-----|
| Compute | Security Groups (per-ENI) | NSG (per-subnet), ASG (per-NIC) | VPC firewall rules (per-instance tags) |
| Container | EKS SGs per pod, network policies | AKS network policies | GKE network policies, Dataplane V2 |
| Service Mesh | App Mesh (mTLS, routing) | Service Fabric | Istio on GKE (mTLS, auth policies) |
| API | API Gateway resource policies | API Management product/API policies | Apigee or Cloud Endpoints |
| Data | RDS SGs, S3 bucket policies, Lake Formation | SQL firewall, Blob firewall | IAM per dataset, VPC SC perimeters |
| Identity | IAM conditions, permission boundaries | Azure AD Conditional Access, managed identities | IAM conditions, workload identity federation |

**Network Micro-Segmentation Example (AWS)**:
```
┌─────────────────────────────────────────────────────┐
│ VPC (10.0.0.0/16)                                   │
│                                                      │
│  Public Subnet (10.0.1.0/24)                        │
│  SG: ALB-SG (allow 443 from 0.0.0.0/0)             │
│  ┌─────┐                                            │
│  │ ALB │                                            │
│  └──┬──┘                                            │
│     │                                               │
│  Private App Subnet (10.0.2.0/24)                   │
│  SG: App-SG (allow 8080 from ALB-SG)                │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐                │
│  │ App 1   │ │ App 2   │ │ App 3   │                │
│  └────┬────┘ └────┬────┘ └────┬────┘                │
│       │           │           │                      │
│  Private DB Subnet (10.0.3.0/24)                    │
│  SG: DB-SG (allow 3306 from App-SG)                 │
│  ┌──────────┐ ┌──────────┐                          │
│  │ RDS(Prim)│ │ RDS(Stby)│                          │
│  └──────────┘ └──────────┘                          │
└─────────────────────────────────────────────────────┘
```

### 54.5 Zero Trust for Remote Access (ZTNA)

**ZTNA Models**:
| Model | Description | Examples |
|-------|-------------|----------|
| Endpoint-Initiated | Agent on endpoint connects to ZTNA gateway | Zscaler, Netskope, Cloudflare WARP |
| Service-Initiated | Connector in network pulls connections | Twingate, Tailscale, Cloudflare Tunnel |
| Browser-Based | Zero-trust browser isolates sessions | Cloudflare Browser Isolation, Menlo, Symantec |

**ZTNA vs VPN**:
| Feature | Traditional VPN | ZTNA |
|---------|----------------|------|
| Access Model | Network-level (entire subnet) | Application-level (per app) |
| Authentication | At connection | Continuous per-request |
| Lateral Movement | Full network access | Micro-segmented per app |
| Performance | Through VPN concentrator | Edge-based, split tunneling |
| Management | Complex (certificates, profiles) | Simple (agent, browser) |
| Visibility | Limited to VPN logs | Per-session, per-app logs |
| User Experience | Connect every session | Always-on, transparent |

**Implementation Example (Cloudflare Zero Trust)**:
```bash
# Cloudflare Tunnel (cloudflared)
cloudflared tunnel create my-tunnel
cloudflared tunnel route dns my-tunnel app.internal.example.com

# Access policy (OIDC with Google Workspace)
cloudflared access login
cloudflared access rule create --hostname app.internal.example.com \
  --policy-name "allow-engineering" \
  --action allow \
  --any-of-email-domain example.com

# Browser Isolation for sensitive apps
cloudflared access rule create --hostname admin.internal.example.com \
  --policy-name "admin-isolation" \
  --action allow \
  --require-email user@example.com \
  --isolation-required true
```

### 54.6 Zero Trust Maturity Model

| Stage | Identity | Device | Network | Application | Data |
|-------|----------|--------|---------|-------------|------|
| **Traditional** | Password-only | BYOD/no control | VPN, flat network | No auth | No classification |
| **Initial** | MFA for admin | MDM enrolled | Segmentation start | Basic auth | Classification started |
| **Advanced** | SSO + MFA all | Device compliance | Micro-segmentation | Context-aware | Encryption + DLP |
| **Optimal** | Continuous auth (risk) | Auto-remediation | Zero Trust network | Continuous verification | Data-centric controls |

---

## 55. Cloud Security Posture Management (CSPM)

### 55.1 CSPM Overview

**Definition**: CSPM tools continuously monitor cloud environments for misconfigurations, compliance violations, and security risks. They automate detection, alerting, and remediation of cloud security issues.

**Key Capabilities**:
- **Configuration Assessment**: Evaluate cloud resource configurations against security benchmarks (CIS, NIST, SOC 2, PCI DSS, HIPAA)
- **Compliance Monitoring**: Continuous compliance against regulatory frameworks; evidence collection for audits
- **Misconfiguration Detection**: Public storage, overly permissive IAM, unencrypted data, exposed ports
- **Drift Detection**: Alert when IaC-defined configuration differs from actual state
- **Remediation Automation**: Auto-remediate common issues (close open ports, enable encryption, block public access)
- **Identity Analysis**: Detect unused permissions, cross-account access, privilege escalation paths
- **Network Visualization**: Map network topology, identify open ports, detect exposed services
- **Container/Orchestration Assessment**: K8s RBAC, pod security, cluster configuration

**Top CSPM Tools**:
| Tool | Key Features | Pricing Model |
|------|-------------|---------------|
| AWS Security Hub | Native AWS; AWS Config + GuardDuty + Inspector + Macie aggregation | Per control check, finding |
| Azure Defender for Cloud | Native Azure; hybrid/multi-cloud support | Free CSPM; paid workload protection |
| GCP Security Command Center | Native GCP; Premium includes threat detection | Standard free; Premium per asset |
| Wiz | Agentless; graph-based; full-stack analysis; API-connector for all clouds | Per resource per month |
| Prisma Cloud | CSPM + CWPP + CWP + CIEM; multi-cloud | Per workload per month |
| Lacework | Polygraph data analysis; behavioral baselining | Per workload per month |
| Orca Security | Agentless; side-scanning; risk prioritization | Per resource per month |
| CrowdStrike Falcon Horizon | CSPM integrated with EDR; multi-cloud | Per workload per month |
| Check Point CloudGuard | CSPM + network security; multi-cloud | Per workload per month |
| Qualys CloudView | CSPM + vulnerability scanning; multi-cloud | Per asset per month |

### 55.2 CSPM Implementation Strategy

**Phase 1: Discovery and Assessment**
1. Discover all cloud accounts/projects across all providers
2. Inventory all resources (compute, storage, network, IAM, databases)
3. Run initial compliance scan against CIS benchmarks
4. Identify critical misconfigurations (public storage, open ports, no encryption)
5. Establish baseline security score

**Phase 2: Remediation and Enforcement**
1. Prioritize findings by risk (CVE severity, data sensitivity, exploitability)
2. Auto-remediate critical issues (block public access, enable encryption)
3. Implement preventive controls (SCP, org policies, IaC guardrails)
4. Create remediation runbooks for common findings
5. Assign ownership for unresolved issues

**Phase 3: Continuous Monitoring**
1. Configure continuous scanning schedules (every 15-60 minutes)
2. Set up alerting for new critical findings (Slack, PagerDuty, email)
3. Integrate with SIEM/SOAR for automated response
4. Track security score trends over time
5. Report to leadership on posture improvements

**Phase 4: Compliance Automation**
1. Map controls to compliance frameworks (CIS, NIST, SOC 2, PCI DSS, HIPAA)
2. Automate evidence collection for audits
3. Generate compliance reports on demand
4. Monitor for compliance drift and alert
5. Prepare for auditor evidence requests

### 55.3 Critical CSPM Rules (CIS Benchmarks)

**CIS AWS Foundations Benchmark (Key Controls)**:
| Control | Description | Auto-Remediation |
|---------|-------------|------------------|
| 1.1 | IAM password policy (≥14 chars, require symbols/numbers/uppercase/lowercase) | AWS Config rule |
| 1.2-1.5 | MFA for root user, IAM users | Lambda auto-enable |
| 1.8 | IAM role for support access | AWS Config |
| 1.16 | IAM policies attached only to groups/roles | Config rule |
| 1.20 | S3 Block Public Access at account level | SCP enforcement |
| 2.1 | CloudTrail enabled in all regions | Config rule |
| 2.4 | CloudTrail log file validation enabled | Config rule |
| 2.5 | S3 bucket access logging enabled | Config rule |
| 2.7 | CloudTrail logs encrypted with KMS | Config rule |
| 3.1-3.14 | Logging (Config, VPC Flow Logs, CloudWatch) | Config rules |
| 4.1-4.5 | EC2 (IMDSv2, EBS encryption, no public IP) | Config rules |
| 5.1-5.10 | Networking (SG restricted ports, VPC Flow Logs) | Config rules + auto-remediate |

**CIS Azure Foundations Benchmark (Key Controls)**:
| Control | Description | Auto-Remediation |
|---------|-------------|------------------|
| 1.1-1.24 | IAM (MFA, RBAC, PIM, guest access) | Conditional Access + PIM |
| 2.3 | Defender for Cloud standard tier | Azure Policy |
| 3.1-3.15 | Storage (HTTPS only, firewall, logging, encryption) | Azure Policy |
| 4.1-4.9 | SQL Server (auditing, TDE, firewall, AAD auth) | Azure Policy |
| 5.1-5.7 | Logging (Activity Log, Log Analytics, diagnostic settings) | Azure Policy |
| 6.1-6.6 | Networking (NSG flow logs, firewall, DDoS) | Azure Policy |
| 7.1-7.5 | Compute (disk encryption, vulnerability assessment) | Azure Policy |
| 8.1-8.5 | Key Vault (firewall, purge protection, RBAC) | Azure Policy |

### 55.4 CSPM Automation and Integration

**CSPM + IaC Integration (Shift Left)**:
```hcl
# Terraform: Pre-deployment compliance check
resource "null_resource" "checkov_scan" {
  provisioner "local-exec" {
    command = "checkov -d . --framework terraform --soft-fail false"
  }
}

# Terraform: Post-deployment compliance via AWS Config
resource "aws_config_config_rule" "s3_bucket_public_access" {
  name = "s3-bucket-public-read-prohibited"
  
  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_PUBLIC_READ_PROHIBITED"
  }
}
```

**CSPM + CI/CD Integration**:
```yaml
# GitHub Actions: CSPM scan as deployment gate
- name: CSPM Pre-Deployment Scan
  uses: bridgecrewio/checkov-action@v12
  with:
    directory: terraform/
    framework: terraform
    soft-fail: false
    
- name: CSPM Post-Deployment Scan
  run: |
    # Trigger CSPM scan after deployment
    curl -X POST https://api.wiz.io/v1/cloud-scans \
      -H "Authorization: Bearer $WIZ_TOKEN" \
      -d '{"connector_id": "aws-prod"}'
```

**CSPM + SIEM Integration**:
- Forward CSPM findings to SIEM (Splunk, Sentinel, ELK, Chronicle)
- Correlation with threat intelligence and EDR alerts
- Automated ticketing (ServiceNow, Jira) for unresolved findings
- SOAR playbook triggers on critical CSPM findings
- Executive dashboards showing security posture trends

---

## 56. Cloud Workload Protection Platform (CWPP)

### 56.1 CWPP Overview

**Definition**: CWPP provides unified workload protection across VMs, containers, and serverless functions. Includes vulnerability management, intrusion detection, file integrity monitoring, and runtime protection.

**CWPP Key Capabilities**:
- **Vulnerability Management**: OS + application vulnerability scanning; container image scanning; serverless function scanning
- **Runtime Protection**: Behavioral monitoring; file integrity monitoring; network threat detection; process whitelisting
- **Intrusion Detection**: Host-based IDS; network-based IDS; anomaly detection on workload behavior
- **Anti-Malware**: Signature + behavioral + ML-based malware detection; fileless attack detection
- **Application Control**: Allowlisting (only approved binaries run); execution control; script control
- **Configuration Assessment**: CIS benchmark compliance; hardening checks; drift detection
- **System Integrity**: Rootkit detection; kernel integrity monitoring; boot integrity (TPM/measured boot)
- **Logging/Forensics**: Security event logging; forensic snapshot; immutable audit trail

**CWPP vs CSPM**:
| Aspect | CSPM | CWPP |
|--------|------|------|
| Focus | Cloud configuration | Workload runtime security |
| Scope | Control plane (IAM, storage, network config) | Data plane (OS, app, container) |
| Detection | Misconfigurations, compliance drift | Malware, exploits, behavioral anomalies |
| Agent | Agentless (API-based) | Agent or agentless (side-scanning) |
| Examples | Wiz, Security Hub, Prisma CSPM | CrowdStrike, SentinelOne, Trend Micro |

### 56.2 CWPP Architecture

**Agent-Based CWPP**:
```
┌──────────────────────────────────────────────┐
│ CWPP Management Console                      │
│ (Analysis, Alerting, Policy, Reporting)       │
└──┬───────────────────────────────────────┬───┘
   │                                       │
   ▼                                       ▼
┌──────────────┐                ┌──────────────┐
│ CWPP Agent   │                │ CWPP Agent   │
│ (AWS EC2)    │                │ (Azure VM)   │
│ - Processes  │                │ - Processes  │
│ - File sys   │                │ - File sys   │
│ - Network    │                │ - Network    │
│ - Audit logs │                │ - Audit logs │
└──────────────┘                └──────────────┘
   │                                       │
   ▼                                       ▼
┌──────────────┐                ┌──────────────┐
│ Agent: K8s   │                │ Agent: Lambda │
│ (DaemonSet)  │                │ (Layer/EXT)  │
└──────────────┘                └──────────────┘
```

**Agentless CWPP**:
- Side-scanning: Snapshot volumes, scan offline (Orca, Wiz)
- Cloud API-based: Read workload config + snapshots via cloud APIs
- No agent deployment required; minimal performance impact
- Limited runtime visibility (no process-level monitoring)
- Good for scanning-only use cases; agent required for runtime defense

### 56.3 CWPP Vulnerability Management

**Scanning Strategy**:
| Workload Type | Scan Method | Frequency | Coverage |
|--------------|-------------|-----------|----------|
| EC2 Linux | OS agent (Inspector, CrowdStrike) | Continuous | OS packages, kernel, config |
| EC2 Windows | OS agent (Inspector, Defender) | Continuous | OS, registry, installed apps |
| Container Images | Registry scan (ECR, GCR, Docker Hub) | On push + scheduled | OS + language packages, secrets |
| Running Containers | DaemonSet agent (Sysdig, Aqua) | Continuous | Runtime packages, file integrity |
| Lambda Functions | Code scan on deploy | On each deployment | Dependencies, code analysis |
| On-Premises VMs | Agent (same as cloud) | Continuous | Full visibility |

**Vulnerability Prioritization**:
| Factor | Weight | Examples |
|--------|--------|----------|
| CVSS Score | High | CVSS 9.0+ vs 4.0 |
| Exploitability | Critical | Public PoC, active exploits, wormable |
| Data Sensitivity | High | PII, PHI, PCI data on same host |
| Network Exposure | High | Public-facing vs internal-only |
| Business Criticality | Medium | Production vs dev |
| Attack Path | Critical | Part of attack path to crown jewels |
| EPSS Score | High | Probability of exploitation in wild |

**CVE Remediation SLA**:
| Severity | Patch Time | Emergency Process |
|----------|-----------|-------------------|
| Critical (CVSS 9.0+) | 24-48 hours | Emergency change; auto-patch or isolate |
| High (CVSS 7.0-8.9) | 7 days | Standard change window |
| Medium (CVSS 4.0-6.9) | 30 days | Next maintenance window |
| Low (CVSS 0.1-3.9) | 90 days | Normal patching cycle |

### 56.4 CWPP Runtime Protection

**Runtime Detection Techniques**:
- **Process Monitoring**: Track all process creation; alert on unexpected binaries (e.g., `minerd` for crypto mining)
- **File Integrity Monitoring**: Monitor critical files (/etc/passwd, /etc/shadow, binaries) for changes
- **Network Monitoring**: Detect unexpected outbound connections (C2 beacons); unusual port binds
- **Container Drift Detection**: Alert if container processes differ from image definition
- **Privilege Escalation Detection**: Track setuid/setgid changes; kernel exploit attempts
- **Memory Protection**: Detect code injection; ROP attacks; memory-scraping malware
- **Log Analysis**: Parse auth.log, syslog for suspicious patterns (brute force, sudo abuse)

**Response Actions**:
| Severity | Automated Response | Manual Response |
|----------|-------------------|-----------------|
| Malware detected | Kill process; quarantine workload; snapshot memory | Investigate origin; threat hunt |
| C2 beaconing | Block outbound IP; isolate workload | DNS/network investigation |
| Privileged escalation | Revoke credentials; isolate workload | Forensic analysis; timeline reconstruction |
| Crypto mining | Kill miner process; block mining pools | Find initial access vector |
| Unauthorized access | MFA challenge; block IP; kill session | Account compromise investigation |
| Container drift | Kill container; redeploy from image | Find root cause (image/tooling compromise) |

---

## 57. Cloud Security for AI/ML Workloads

### 57.1 AI/ML Attack Surface

**ML Pipeline Threat Model**:
| Stage | Threat | Impact |
|-------|--------|--------|
| Data Collection | Data poisoning | Model learns incorrect patterns |
| Data Storage | Data breach (PII in training data) | Privacy violation, regulatory fines |
| Data Preprocessing | Feature manipulation | Biased or incorrect model |
| Model Training | Model poisoning, backdoor insertion | Malicious behavior triggered by specific input |
| Model Storage | Model theft, IP theft | Competitive disadvantage |
| Model Deployment | Model inversion, extraction | Recover training data, steal model |
| Inference API | Adversarial examples, evasion | Model misclassification |
| Model Monitoring | Drift detection bypass | Degraded model over time |

### 57.2 Cloud ML Platform Security

**SageMaker Security (AWS)**:
- **Notebook Instances**: IAM role with least privilege; VPC-only (no internet); KMS encryption for EBS; lifecycle configs for auto-shutdown
- **Training Jobs**: IAM role with data access only; VPC for network isolation; encrypted S3 input/output; spot instances for cost (with checkpointing)
- **Model Artifacts**: Encrypted in S3; model registry with approval workflow; versioning
- **Endpoints**: IAM auth; VPC (private); KMS encryption; autoscaling; CloudWatch logging; WAF in front for HTTPS APIs
- **Ground Truth**: Encrypted labeling data; private workforce for sensitive data; audit trail of labeling actions
- **Feature Store**: KMS encryption; IAM per feature group; online/offline store with access control
- **Data Wrangler**: Data flow IAM role; KMS encryption; output to encrypted S3

**Azure ML Security**:
- **Workspace**: RBAC (contributor/reader/admin); managed identity for services; private endpoint connectivity
- **Compute**: Compute cluster/instance in VNet; managed identity; no public IP; SSH disabled by default
- **Datastores**: Key Vault for credentials; datastore credentials (SAS, service principal, account key); datastore registered in workspace
- **Datasets**: Versioned; IAM access control; encryption in transit/at rest
- **Pipelines**: Service principal authentication; data encryption between steps; ACR for container images
- **Endpoints**: Managed identity auth; VNet injection; TLS termination; logging to Application Insights

**Vertex AI Security (GCP)**:
- **Notebooks**: VPC-SC perimeter; IAM conditions; encryption with CMEK; OS login
- **Training**: CMEK for all data; VPC-SC; service account per job; custom container with vulnerability scanning
- **Models**: IAM per model; CMEK; model registry with approval; explainability (protected attributes)
- **Endpoints**: IAM auth; VPC-SC; private endpoint; Cloud Armor for L7 defense; logging to Cloud Audit Logs
- **Feature Store**: CMEK; IAM per feature store; online serving with private IP
- **Pipeline (Vertex AI Pipelines)**: Service account; encrypted artifacts; VPC-SC

### 57.3 ML-Specific Security Controls

**Data Poisoning Prevention**:
- **Data provenance**: Track data origin, transformations, and access
- **Input validation**: Validate data integrity and format before training
- **Data sanitization**: Remove outliers and anomalies; validate against expected distribution
- **Differential privacy**: Add calibrated noise to training data (prevents memorization of individual records)
- **Federated learning**: Train on decentralized data (no raw data leaves local environment)
- **Access controls**: Minimize who can modify training data; audit all data changes
- **Checksums**: Verify data integrity (hash comparison) before each training run

**Model Security**:
- **Model encryption**: Encrypt model artifacts at rest and in transit
- **Model watermarking**: Embed invisible watermarks to prove ownership
- **Adversarial training**: Train model on adversarial examples to improve robustness
- **Defensive distillation**: Train smaller model on larger model's probability vectors
- **Gradient masking**: Obfuscate gradients to prevent model extraction
- **Input perturbation**: Add noise to inference inputs to prevent inversion attacks
- **Rate limiting**: Throttle API calls to prevent model extraction via repeated queries
- **Output sanitization**: Round/scramble confidence scores; limit information in error messages
- **Membership inference defense**: Limit detail in model outputs to prevent determining if specific data was in training set

**ML Infrastructure Security**:
- **GPU instance security**: Nitro Enclaves for GPU workloads; no SSH access to training instances
- **Container isolation**: Run training in isolated containers; no unnecessary binaries/libraries
- **Network egress**: Block outbound internet from training environments (data exfiltration prevention)
- **Data deletion**: Ephemeral training environments: all data deleted after training completes
- **Secure multi-tenancy**: Hardware isolation for sensitive workloads; AMD SEV-SNP or Intel TDX for confidential ML
- **Dependency scanning**: Scan ML libraries (TensorFlow, PyTorch, scikit-learn) for known CVEs
- **Supply chain**: Verify ML model registries and container images with Cosign/Sigstore

### 57.4 AI Security Compliance

**Evolving AI Regulations**:
- **EU AI Act**: Risk-based classification (unacceptable, high, limited, minimal); requirements for high-risk AI (data governance, transparency, human oversight, accuracy, robustness)
- **US Executive Order on AI**: Safety testing, red-teaming, watermarking, privacy impact assessments
- **NIST AI Risk Management Framework (AI RMF)**: Govern, Map, Measure, Manage framework for AI risks
- **ISO/IEC 42001**: AI management system standard; risk assessment, controls, monitoring
- **GDPR implications**: Right to explanation for automated decisions; data minimization in training; data subject access rights for ML training data
- **CCPA/CPRA**: Consumer right to opt out of automated decision-making; disclosure of AI logic

### 57.5 GenAI Security (LLM-Specific)

**OWASP Top 10 for LLM Applications**:
| Risk | Description | Cloud Countermeasure |
|------|-------------|---------------------|
| LLM01: Prompt Injection | Manipulate LLM via crafted prompts | Input sanitization + output validation; parameterized prompts |
| LLM02: Sensitive Data Disclosure | LLM reveals training or context data | Data filtering; PII redaction; differential privacy |
| LLM03: Insecure Plugin Design | Plugin vulnerabilities | Plugin sandboxing; strict IAM for plugins |
| LLM04: Model DoS | Overwhelm LLM with requests | API Gateway rate limiting; WAF; autoscaling limits |
| LLM05: Supply Chain | Compromised model or dependencies | Model registry verification; signed model artifacts; SBOM |
| LLM06: Training Data Poisoning | Malicious data in training | Data validation; provenance tracking; access control |
| LLM07: Model Theft | Extract or copy model | API rate limiting; output perturbation; encryption |
| LLM08: Excessive Agency | LLM takes unintended actions | Scoped function calls; human-in-the-loop approval |
| LLM09: Overreliance | Blind trust in LLM output | Output validation; disclaimers; confidence scores |
| LLM10: Insecure Output Handling | Output injection (XSS, SSRF) | Sanitize output before rendering; CSP headers |

**GenAI Security Architecture**:
```
Client → API Gateway (auth, rate limit, WAF) → LLM Proxy (input sanitization, PII detection, prompt guard) → Model (SageMaker/Vertex AI/Azure OpenAI) → LLM Proxy (output validation, content filter, PII redaction) → Response
```



---

## 58. Cloud SIEM and SOAR

### 58.1 Cloud SIEM Architecture

**SIEM Pipeline Components**:
```
┌──────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│ Log      │ →  │ Log      │ →  │ SIEM      │ →  │ Analysis │ →  │ Response │
│ Sources  │    │ Shipping │    │ Platform  │    │ Engine   │    │ (SOAR)   │
└──────────┘    └──────────┘    └───────────┘    └──────────┘    └──────────┘
   CloudTrail      Fluentd       Splunk           Correlation      Automation
   VPC Flow Logs   Logstash      Sentinel         ML Models        Ticketing
   GuardDuty       CloudWatch    Chronicle        UEBA              IR Playbooks
   WAF             Azure Mon     ELK              Threat Intel     Remediation
   DNS Logs        Agent         Datadog          Anomalies        Block/Isolate
   OS Logs         OTel          Sumo Logic       Compliance       Notify
```

**Log Sources for Cloud SIEM**:
| Log Type | AWS | Azure | GCP |
|----------|-----|-------|-----|
| Control Plane | CloudTrail (management events) | Activity Log | Cloud Audit Logs (admin activity) |
| Data Plane | CloudTrail (data events) | Resource Logs | Cloud Audit Logs (data access) |
| Network | VPC Flow Logs, DNS logs | NSG Flow Logs, Azure Firewall logs | VPC Flow Logs, firewall logs |
| Application | ALB/CLB/NLB logs, CloudFront | App Gateway, Front Door logs | HTTP(S) LB logs, Cloud CDN |
| Database | RDS logs, Aurora logs, DynamoDB | SQL audit logs, Cosmos DB | Cloud SQL logs, Firestore |
| Security | GuardDuty, Security Hub, Inspector | Defender for Cloud, Sentinel | SCC, Chronicle |
| Workload | OS logs (CloudWatch Agent) | VM logs (Azure Monitor Agent) | OS logs (Ops Agent) |
| Container | EKS audit logs, container logs | AKS audit logs, container insights | GKE audit logs, container logs |

### 58.2 Cloud SIEM Platforms

**Azure Sentinel** (Cloud-Native SIEM):
- **Data Ingestion**: 100+ connectors for Microsoft, AWS, GCP, and third-party sources
- **Analytics**: Scheduled queries (KQL), ML-based anomaly detection, UEBA, fusion (multi-stage attack detection)
- **Threat Intelligence**: Built-in TAXII connector; custom threat intel feeds
- **Investigation**: Graph-based investigation (entity linking); hunting queries; bookmarks
- **Automation**: Playbooks (Logic Apps); automated response to incidents
- **Integration**: Microsoft 365 Defender, Defender for Cloud, Azure AD Identity Protection
- **Pricing**: Pay-as-you-go per GB ingested; 50-500 GB/day typical for enterprise
- **Retention**: 90 days free; up to 7 years (Log Analytics + hot/cold tiers)

**Sentinel Security Content**:
```kusto
// Detect anomalous CloudTrail AssumeRole events
CloudTrail
| where EventName == "AssumeRole"
| where TimeGenerated > ago(1h)
| summarize RoleCount = dcount(RequestParameters.roleArn) by UserIdentityArn, SourceIpAddress
| where RoleCount > 10
| join kind=inner (
    CloudTrail
    | where EventName == "AssumeRole"
) on SourceIpAddress
| summarize RolesAssumed = make_set(RequestParameters.roleArn) by UserIdentityArn, SourceIpAddress
| project UserIdentityArn, SourceIpAddress, RolesAssumed, RoleCount

// Detect GuardDuty CRITICAL findings
SecurityFinding
| where ProductName == "GuardDuty"
| where Severity >= 8
| summarize Count = count() by Id, Title, Severity, AccountId, Region
| extend AlertLink = strcat("https://console.aws.amazon.com/guardduty/home?region=", Region, "#/findings?search=", Id)

// Track lateral movement via EC2 RunInstances after IAM compromise
let CompromisedPrincipals = (
    CloudTrail
    | where EventName == "CreateAccessKey" or EventName == "UpdateLoginProfile"
    | summarize by UserIdentityArn
);
CloudTrail
| where EventName == "RunInstances"
| where UserIdentityArn in (CompromisedPrincipals)
| project TimeGenerated, UserIdentityArn, InstanceId, InstanceType, Region
```

**Splunk in Cloud**:
- Splunk Cloud (SaaS) or Splunk on EC2 (self-managed)
- AWS Add-on: CloudTrail, Config, GuardDuty, S3, EC2, ELB, VPC Flow Logs
- Azure Add-on: Activity Log, NSG Flow Logs, Azure AD, WAF
- GCP Add-on: Audit Logs, VPC Flow Logs, LB logs, Cloud Monitoring
- Security Content: Splunk Enterprise Security (ES) with risk-based alerting, threat intel, notable events
- **Pricing**: Ingest-based (typically $150-500/GB/month for Splunk Cloud)

**ELK Stack (Elastic + Logstash + Kibana) in Cloud**:
- Elastic Cloud (SaaS) or self-managed on EC2/AKS/GKE
- Filebeat/Logstash for log shipping
- Elastic Security for SIEM: detection rules, cases, timelines, endpoint security
- Cloud integrations: AWS, Azure, GCP modules
- **Pricing**: Elastic Cloud per GB ingested (typically $0.10-0.20/GB); self-managed free (infra cost)

**Google Chronicle**:
- Cloud-native SIEM designed for petabyte-scale
- Ingestion: Cloud Audit Logs, VPC Flow Logs, DNS logs, third-party logs
- Analytics: UDM (Unified Data Model); YARA-L detection rules; context-aware alerts
- **Pricing**: Per GB ingested; competitive for high-volume environments

### 58.3 Cloud SOAR

**SOAR (Security Orchestration, Automation, and Response)**:
| Capability | Description | Examples |
|------------|-------------|----------|
| Playbooks | Automated response workflows | Isolate instance, block IP, revoke key |
| Orchestration | Connect security tools via APIs | SIEM → EDR → Firewall → Ticketing |
| Case Management | Incident tracking with evidence | Jira, ServiceNow, PagerDuty integration |
| Threat Intel | Enrich IOCs, automate blocking | VirusTotal, AlienVault, MISP feeds |
| Reporting | Post-incident reports, metrics | Executive summary, SLA tracking |

**Cloud SOAR Tools**:
| Tool | Cloud-Native | Key Features |
|------|-------------|--------------|
| Splunk SOAR (Phantom) | No (SaaS/on-prem) | 400+ apps; playbook builder; customizable dashboards |
| Microsoft Sentinel | Yes (Azure) | Logic Apps playbooks; 300+ connectors; KQL-based |
| Palo Alto XSOAR | No (SaaS/on-prem) | 1000+ integrations; marketplace; Cortex XSIAM |
| Torq | No (SaaS) | Low-code; enterprise-grade automation; API-first |
| Tines | No (SaaS) | Low-code; workflow builder; security automation |
| Swimlane | No (SaaS/on-prem) | Low-code; case management; compliance reporting |
| AWS (custom) | Yes (AWS) | Step Functions + Lambda + EventBridge; DIY SOAR |

### 58.4 SIEM/SOAR Implementation Guide

**SIEM Implementation Phases**:
1. **Planning**: Identify log sources; define use cases (detection rules); plan retention; estimate volume/cost
2. **Ingestion**: Deploy log shippers; configure log sources; validate log format/quality; monitor ingestion pipeline
3. **Detection**: Create correlation rules; integrate threat intelligence; tune false positives
4. **Response**: Define alert severity (critical/high/medium/low); configure SOAR playbooks for automated response
5. **Investigation**: Train analysts on investigation workflows; create investigation templates
6. **Reporting**: Create dashboards for SOC metrics; executive reporting; compliance reports
7. **Continuous Improvement**: Tune rules based on feedback; add new log sources; update use cases

**SOAR Playbook Examples**:

**Playbook: Compromised IAM Key**
```yaml
trigger: GuardDuty finding (UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration)
steps:
  - enrichment:
      - Get CloudTrail events for IAM user (last 7 days)
      - Get resource access history
      - IP reputation check (VirusTotal, GreyNoise)
  - containment:
      - Disable IAM access keys (parallel)
      - Detach IAM policies (parallel)
      - Revoke all IAM session tokens
      - Add user to quarantine IAM group
  - investigation:
      - Create incident ticket in ServiceNow (P1)
      - Notify security team via Slack/PagerDuty
      - Begin forensic timeline
  - remediation:
      - Rotate all credentials used by this user
      - Review SCP for excessive permissions
      - Implement IAM conditions (IP, MFA)
  - recovery:
      - After investigation, create new keys with least privilege
      - Add to monitoring watchlist
```

**Playbook: Public S3 Bucket Detected**
```yaml
trigger: CSPM finding (S3 bucket public access)
steps:
  - enrichment:
      - Verify bucket public status (Config rule check)
      - Identify bucket contents (classify if sensitive)
      - CloudTrail access logs for bucket (last 24h)
  - containment:
      - Block all public access (BlockPublicAcls, BlockPublicPolicy)
      - Remove bucket policy with public effect
      - Disable ACLs on bucket
  - investigation:
      - Determine owner/team responsible
      - Check if unauthorized access occurred (CloudTrail data events)
      - If sensitive data exposed, initiate data breach process
  - remediation:
      - Enable account-level S3 Block Public Access
      - Add Config rule and auto-remediation
      - Tag bucket with classification
```

**SIEM/SOAR Cost Estimation**:
| Volume (GB/day) | Sentinel (monthly) | Splunk Cloud (monthly) | Elastic (monthly) |
|-----------------|-------------------|----------------------|-------------------|
| 50 GB | ~$2,500 | ~$7,500 | ~$2,500 |
| 200 GB | ~$10,000 | ~$30,000 | ~$10,000 |
| 1 TB | ~$49,500 | ~$150,000 | ~$49,500 |
| 5 TB | ~$247,500 | ~$750,000 | ~$247,500 |

*Note: Pricing varies significantly based on commitments, reserved capacity, negotiated discounts, and included retention*

---

## 59. Cloud Penetration Testing Methodology

### 59.1 Cloud Pentesting Overview

**Cloud Pentesting vs Traditional Pentesting**:
| Aspect | Traditional | Cloud |
|--------|-------------|-------|
| Scope | On-premises network + applications | Cloud APIs, IAM, configurations, serverless, containers |
| Authorization | IP whitelist, onsite | Cloud provider authorization (AWS Pentesting Policy), written authorization |
| Boundaries | Physical network perimeter | Identity perimeter, API boundaries, organizational units |
| Testing Methods | Port scanning, exploit, pivot | API enumeration, privilege escalation paths, misconfiguration |
| Attack Vectors | Network protocols, services | Cloud APIs, metadata service, OAuth tokens, cloud storage |
| Persistence | Backdoors, cron jobs | IAM roles, Lambda backdoors, API keys, service accounts |

**Cloud Provider Pentesting Policies**:
- **AWS**: Customers may test EC2, RDS, CloudFront, API Gateway, Lambda without approval; DO NOT test infrastructure (hypervisor, DNS, S3, anything below virtualization layer); prohibited: DoS, DNS poisoning, social engineering of AWS employees
- **Azure**: Customers may pentest their own resources; must follow Microsoft Cloud Unified Penetration Testing Rules of Engagement; prohibited: DoS, pen testing of Azure infrastructure
- **GCP**: Customers may pentest their own projects; must follow GCP Penetration Testing Policy; prohibited: testing Google infrastructure, DoS, social engineering
- **Authorization**: Submit test scope to provider (not always required but recommended); maintain evidence of authorization

### 59.2 Cloud Pentesting Phases

**Phase 1: Reconnaissance and Enumeration**

**Account/Project Discovery**:
```bash
# DNS-based cloud account discovery
# AWS: Check for known account IDs via S3 bucket names
nslookup my-bucket.s3.amazonaws.com

# Azure: Subdomain enumeration
dig CNAME myapp.azurewebsites.net

# GCP: Project ID discovery via storage bucket URLs
curl https://storage.googleapis.com/my-gcp-project-bucket/
```

**Service Enumeration**:
```bash
# Enumerate all resources in AWS account
aws resourcegroupstaggingapi get-resources --region us-east-1 --output json

# List all S3 buckets
aws s3api list-buckets --query 'Buckets[*].Name'

# Enumerate Lambda functions
aws lambda list-functions --region us-east-1

# List EC2 security groups
aws ec2 describe-security-groups --query 'SecurityGroups[*].GroupName'

# Enumerate IAM users, roles, groups, policies
aws iam list-users
aws iam list-roles
aws iam list-policies --scope Local
```

**Phase 2: IAM Privilege Escalation Testing**

**Common IAM Privilege Escalation Paths**:
| Action | Escalation Vector |
|--------|------------------|
| `iam:CreatePolicyVersion` | Create admin policy version; set as default |
| `iam:SetDefaultPolicyVersion` | Switch to older permissive version |
| `iam:PassRole` + `ec2:RunInstances` | Launch EC2 with admin role |
| `iam:CreateUser` + `iam:CreateAccessKey` | Create new admin user with keys |
| `iam:UpdateAssumeRolePolicy` | Modify trust policy to allow self-assumption |
| `iam:CreateRole` + `iam:AttachRolePolicy` | Create admin role; assume it |
| `lambda:CreateFunction` + `lambda:InvokeFunction` | Create Lambda with admin role |
| `iam:AttachUserPolicy` | Attach admin policy to your user |
| `iam:UpdateLoginProfile` | Change user's password |
| `iam:CreateLoginProfile` | Create console password for user |

**Privilege Escalation Testing Tools**:
```bash
# ScoutSuite - AWS/Azure/GCP security auditing
pip install scoutsuite
scout aws --report-dir ./scout-report

# Pacu - AWS exploitation framework
git clone https://github.com/RhinoSecurityLabs/pacu
python pacu.py
run iam__privesc_scan
run iam__enum_permissions
run ec2__enum
run s3__bucket_bruteforce

# SkyArk - Azure privilege escalation
git clone https://github.com/cyberark/SkyArk
Import-Module .\SkyArk.ps1
Get-AWShadowPermissions

# GCP-IAM-Exploiter
git clone https://github.com/agilepivot/gcp-iam-exploiter
python gcp_iam_exploiter.py --project PROJECT_ID
```

**Phase 3: Cloud Storage Assessment**

**S3/Blob/GCS Bucket Testing**:
```bash
# Enumerate public S3 buckets
# (using tools like s3-inspector, bucket-stream, or manually)
curl https://s3.amazonaws.com/BUCKET_NAME
curl https://BUCKET_NAME.s3.amazonaws.com/

# Test bucket permissions
aws s3api get-bucket-acl --bucket BUCKET_NAME
aws s3api get-bucket-policy --bucket BUCKET_NAME
aws s3api get-public-access-block --bucket BUCKET_NAME

# List and download objects if public
aws s3 ls s3://BUCKET_NAME --no-sign-request
aws s3 cp s3://BUCKET_NAME/sensitive.txt . --no-sign-request

# Azure Blob enumeration
curl https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER?restype=container&comp=list

# GCS bucket enumeration
curl https://storage.googleapis.com/BUCKET_NAME
curl https://storage.googleapis.com/storage/v1/b/BUCKET_NAME/o
```

**Phase 4: Metadata Service Testing**

**IMDS/Instance Metadata Attacks**:
```bash
# IMDSv1 (vulnerable) — SSRF to metadata endpoint
curl http://169.254.169.254/latest/meta-data/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ROLE_NAME

# IMDSv2
TOKEN=$(curl -X PUT http://169.254.169.254/latest/api/token -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl http://169.254.169.254/latest/meta-data/ -H "X-aws-ec2-metadata-token: $TOKEN"

# Azure IMDS
curl -H "Metadata: true" http://169.254.169.254/metadata/instance?api-version=2021-02-01

# GCP metadata
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token
```

**Phase 5: Network and Firewall Testing**

**Security Group/NACL/Firewall Testing**:
```bash
# Identify open ports (nmap from EC2 instance within VPC)
nmap -sT -p 22,80,443,3306,5432,6379,27017 TARGET_IP

# Test VPC peering connectivity
# Test cross-VPC access (VPC peering, Transit Gateway, VPN)
# Test VPC endpoint access (S3, DynamoDB, KMS, etc.)

# Azure NSG testing
az network nsg rule list --resource-group myRG --nsg-name myNSG --query "[].{Name:name, Port:destinationPortRange, Access:access}"

# GCP VPC firewall testing
gcloud compute firewall-rules list --project PROJECT_ID
```

**Phase 6: Container and Kubernetes Testing**

**K8s Attack Paths**:
| Attack Vector | Description | Test Command |
|--------------|-------------|--------------|
| RBAC Enumeration | Check service account permissions | `kubectl auth can-i --list` |
| Pod Escape | Break out of container | Check capabilities, hostPID, hostNetwork |
| Secrets Access | Dump secrets via API | `kubectl get secrets -o yaml` |
| Dashboard Exposure | Unauthenticated dashboard | `curl http://DASHBOARD_IP:8001` |
| kubelet API | kubelet without auth | `curl -k https://NODE_IP:10250/pods` |
| etcd Access | Unencrypted etcd | `curl http://ETCD_IP:2379/version` |
| Image Pull Secrets | Extract registry credentials | `kubectl get secrets -n kube-system` |
| Admission Webhook Bypass | Test policy engine | Create privileged pod with annotations/labels |

**Container Security Testing Tools**:
```bash
# kube-hunter - Kubernetes vulnerability scanner
pip install kube-hunter
kube-hunter --remote TARGET_IP

# kube-bench - CIS benchmark checker
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml

# Peirates - Kubernetes attack tool
git clone https://github.com/inguardians/peirates
./peirates

# Grype/Trivy - Container vulnerability scanning
grype myimage:latest
trivy image --severity CRITICAL,HIGH myimage:latest
```

**Phase 7: Serverless Testing**

**Lambda/Function Testing**:
- **Event Injection**: Craft malicious events to trigger Lambda functions (S3 events, API Gateway, SQS, DynamoDB Streams)
- **Environment Variable Inspection**: Check for secrets in Lambda env vars (database passwords, API keys)
- **IAM Role Exploitation**: If function has excessive permissions, use stolen credentials
- **Dependency Vulnerabilities**: Scan Lambda layers and dependencies for CVEs
- **Code Injection**: If function uses eval() or unsafe deserialization, attempt code injection
- **Denial of Service**: Trigger excessive invocations (resource exhaustion, cost spikes)
- **Cold Start Manipulation**: Exploit VPC cold start delays

**Phase 8: Reporting and Remediation**

**Pentest Report Structure**:
1. **Executive Summary**: Business impact, risk level, key findings
2. **Scope and Methodology**: What was tested, timeframe, tools used
3. **Findings**: Categorized by risk (Critical/High/Medium/Low)
4. **Technical Details**: Each finding with description, evidence, impact, remediation
5. **Attack Paths**: Chained exploitation demonstrating real-world impact
6. **Remediation Recommendations**: Prioritized by risk and effort
7. **Appendices**: Tool output, screenshots, log excerpts

### 59.3 Cloud Pentesting Tools

**Cloud-Specific Security Tools**:
| Tool | Purpose | Clouds Supported |
|------|---------|-----------------|
| ScoutSuite | Multi-cloud security auditing | AWS, Azure, GCP |
| Pacu | AWS exploitation framework | AWS |
| Cloudsploit | Cloud security scanner | AWS, Azure, GCP |
| Prowler | AWS CIS benchmark tool | AWS |
| Cloudsplaining | IAM privilege analysis | AWS |
| AWS Nuke | Resource deletion (cleanup after test) | AWS |
| AzureHound | Azure AD reconnaissance | Azure |
| ROADtools | Azure AD/M365 assessment | Azure |
| Stormspotter | Azure attack surface visualization | Azure |
| GCPHound | GCP attack path enumeration | GCP |
| Forseti Security | GCP security tooling | GCP |
| Kube-Hunter | Kubernetes security assessment | K8s |
| Kube-Bench | CIS benchmark for K8s | K8s |
| Trivy | Vulnerability scanner (containers, IaC, cloud) | Multi |

---

## 60. Cloud Threat Hunting

### 60.1 Threat Hunting Methodology

**Hunting Loop (Pyramid Model)**:
```
Hypothesis → Collect Data → Apply Analysis → Investigate → Respond → Improve
    ↑                                                                    │
    └────────────────────────────────────────────────────────────────────┘
```

**Hunting Hypotheses Examples**:
- "An attacker may be using compromised IAM keys to access our S3 buckets"
- "A crypto miner may be running on our EC2 instances"
- "An attacker may have backdoored our CI/CD pipeline"
- "There may be unauthorized cross-account access via assumed roles"
- "A container escape may have occurred in our EKS cluster"
- "An attacker may be tunneling data via DNS to bypass egress controls"

### 60.2 Cloud Hunting Data Sources

**Primary Hunting Data**:
| Data Source | AWS | Azure | GCP | Retention |
|-------------|-----|-------|-----|-----------|
| API Activity | CloudTrail | Activity Log | Cloud Audit Logs | 90-2557 days |
| DNS Queries | Route53 Resolver logs | Azure DNS logs | Cloud DNS logging | 30-365 days |
| Network Flow | VPC Flow Logs | NSG Flow Logs | VPC Flow Logs | 30-365 days |
| Authentication | CloudTrail (IAM events) | Sign-in logs | Cloud Audit Logs | 90-365 days |
| Process Events | Systems Manager | VM Insights | OS Config | 30-365 days |
| Container Events | EKS audit logs | AKS audit logs | GKE audit logs | 30-365 days |
| Database Queries | RDS audit logs | SQL audit logs | Cloud SQL logs | 30-365 days |
| WAF/Proxy | WAF logs, CloudFront | WAF logs, Front Door | Cloud Armor logs | 30-365 days |
| Vulnerability | Inspector | Defender for Cloud | SCC findings | Keep until fixed |
| Threat Intel | GuardDuty, Security Hub | Defender for Cloud | SCC (premium) | Keep until resolved |

### 60.3 Hunting Techniques and Queries

**AWS Hunting Queries**:

**Hypothesis: Stolen IAM keys used from unexpected location**
```bash
# CloudTrail: Access from unusual regions
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=AssumeRole
# Filter results for regions the user never accesses
# Look for: aws-region in responseElements.credentials.accessKeyId

# CloudTrail: Access from unexpected IPs
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=ConsoleLogin \
  --query 'Events[?contains(CloudTrailEvent, `SourceIpAddress`) && !contains(CloudTrailEvent, `"13.37.0.0/16"`)]'
```

**Hypothesis: Data exfiltration via S3**
```bash
# CloudTrail: Unusual volume of GetObject calls
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=GetObject \
  --start-time $(date -d '24 hours ago' +%s)
# Look for: high count from single principal in short time window

# CloudTrail: GetObject to unusual regions
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=CopyObject \
  --query 'Events[?contains(CloudTrailEvent, `eu-west-1`) && contains(CloudTrailEvent, `us-east-1`)]'

# S3 Server Access Logs: GET requests from anonymous principals
grep "REST.GET.OBJECT" s3-access-logs/ | grep "Anonymous"
```

**Hypothesis: Crypto mining on EC2**
```bash
# GuardDuty: Crypto currency findings
aws guardduty list-findings --detector-id DETECTOR_ID
aws guardduty get-findings --detector-id DETECTOR_ID --finding-ids FINDING_IDS

# CloudTrail: RunInstances with GPU instance types
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=RunInstances \
  --query 'Events[?contains(CloudTrailEvent, `p3`)]'

# VPC Flow Logs: Outbound traffic to known mining pools
# Filter for destination IPs in mining pool blocklists
cat vpc-flow-logs/* | grep "51.15.0.0\\|pool.minexmr.com\\|xmrpool.eu"

# Cost Explorer: Spike in compute spend
# Look for daily cost anomaly in EC2/GPU instance categories
```

**Hypothesis: Cross-account privilege escalation**
```bash
# CloudTrail: AssumeRole events to unknown accounts
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=AssumeRole
# Filter for role ARNs not in known account list

# IAM Access Analyzer: External access findings
aws accessanalyzer list-findings --analyzer-arn ANALYZER_ARN

# SCP/Organization: New account added without approval
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=CreateAccount
```

**Azure Hunting Queries**:

```kusto
// Sign-in from unusual locations or anonymous IPs
SigninLogs
| where TimeGenerated > ago(7d)
| where Status.errorCode == 0
| where RiskLevelDuringSignIn in ("medium", "high")
| summarize SignInCount = count() by UserPrincipalName, IPAddress, Location, RiskLevelDuringSignIn

// Role assignment changes (privilege escalation)
AuditLogs
| where OperationName == "Add member to role"
| where TimeGenerated > ago(7d)
| where TargetResources[0].modifiedProperties[0].oldValue != TargetResources[0].modifiedProperties[0].newValue
| project TimeGenerated, InitiatedBy.user.userPrincipalName, TargetResources[0].displayName

// Storage access from unusual IPs
StorageBlobLogs
| where TimeGenerated > ago(24h)
| where StatusCode == 200
| extend CallerIPAddress = parse_json(Properties)["callerIpAddress"]
| where CallerIPAddress !in (KNOWN_IP_LIST)
```

**GCP Hunting Queries**:

```bash
# GCP: Service account key creation
gcloud logging read "protoPayload.methodName='google.iam.admin.v1.CreateServiceAccountKey'" \
  --project PROJECT_ID --freshness=7d

# GCP: Bucket IAM policy changes
gcloud logging read "protoPayload.methodName='storage.setIamPolicy'" \
  --project PROJECT_ID --freshness=7d

# GCP: Instance creation with public IP
gcloud logging read \
  'protoPayload.methodName:"compute.instances.insert" AND protoPayload.request.networkInterfaces.accessConfigs' \
  --project PROJECT_ID --freshness=7d

# GCP: VPC Flow Logs analysis (BigQuery)
SELECT
  jsonPayload.connection.dest_ip,
  jsonPayload.connection.dest_port,
  COUNT(*) as connection_count
FROM `my_project.my_dataset.vpc_flow_logs`
WHERE TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR) < timestamp
  AND jsonPayload.reporter = 'DEST'
  AND jsonPayload.connection.dest_ip NOT IN (
    '10.0.0.0/8', '172.16.0.0/12', '192.168.0.0/16'
  )
GROUP BY dest_ip, dest_port
ORDER BY connection_count DESC
LIMIT 100
```

### 60.4 Automated Threat Hunting

**Hunting Automation with Python/Boto3**:
```python
import boto3
import datetime
from collections import Counter

def hunt_stale_credentials():
    """Find IAM users with keys older than 90 days"""
    iam = boto3.client('iam')
    users = iam.list_users()['Users']
    
    old_keys = []
    for user in users:
        keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        for key in keys:
            age = (datetime.datetime.now() - key['CreateDate'].replace(tzinfo=None)).days
            if age > 90:
                old_keys.append((user['UserName'], key['AccessKeyId'], age))
    
    return old_keys

def hunt_cross_account_roles():
    """Identify roles that allow external access"""
    iam = boto3.client('iam')
    roles = iam.list_roles()['Roles']
    
    external_roles = []
    for role in roles:
        trust_policy = role.get('AssumeRolePolicyDocument', {})
        if trust_policy:
            for statement in trust_policy.get('Statement', []):
                principal = statement.get('Principal', {})
                aws_principal = principal.get('AWS', '')
                if isinstance(aws_principal, str) and aws_principal != 'arn:aws:iam::ACCOUNT_ID:root':
                    external_roles.append(role['RoleName'])
    
    return external_roles
```

**Hunting with Jupyter Notebooks**:
- Use AWS + Moto (mock) for development
- Query Athena for historical CloudTrail analysis
- Use pandas for statistical anomaly detection
- Visualize with plotly/seaborn
- Store hunting playbooks as version-controlled notebooks

### 60.5 Threat Hunting Maturity

| Level | Description | Capabilities |
|-------|-------------|--------------|
| **Level 0: Initial** | Relies on automated alerts only | GuardDuty/Defender default alerts; no proactive hunting |
| **Level 1: Basic** | Scheduled manual hunting | Monthly manual reviews of CloudTrail, VPC Flow Logs; spreadsheets for tracking |
| **Level 2: Structured** | Data-driven hunting hypotheses | Defined hypotheses; scheduled hunts; documented procedures; basic automation |
| **Level 3: Advanced** | Automated and machine learning | Automated hunting pipelines; ML anomaly detection; UEBA integration; threat intel correlation |
| **Level 4: Optimized** | Continuous, adaptive hunting | Real-time automated hunting; self-improving models; threat intel feedback loop; purple team integration |

---

## 61. Infrastructure as Code (IaC) Security Deep Dive

### 61.1 IaC Security Overview

**What IaC Security Covers**:
- Template/Manifest scanning (Terraform, CloudFormation, ARM, Pulumi)
- Secret detection in IaC files
- Compliance validation before deployment
- Drift detection between IaC and actual state
- Policy enforcement via policy as code

**Common IaC Misconfigurations**:
| Misconfiguration | Example | Risk |
|-----------------|---------|------|
| Hardcoded secrets | `db_password = "P@ssw0rd!"` | Credential leak |
| Public resources | `acl = "public-read"` | Data exposure |
| Open ports | `from_port = 0, to_port = 0` | Attack surface |
| No encryption | `encrypted = false` | Data breach |
| Overly permissive IAM | `Action = "*"` | Privilege escalation |
| No logging | `enable_logging = false` | Detection gap |
| Default passwords | `master_password = "admin123"` | Easy compromise |
| Weak TLS | `ssl_policy = "TLSv1"` | Protocol downgrade |

### 61.2 IaC Scanning Tools

**Terraform Security Scanning**:
| Tool | Features | Integration |
|------|----------|-------------|
| Checkov | 1000+ policies; Terraform, CloudFormation, K8s, ARM, CDK | CLI, GitHub Actions, pre-commit |
| tfsec | Static analysis for Terraform | CLI, CI/CD, VS Code |
| Terrascan | Policy-as-code; OPA/Kubernetes support | CLI, CI/CD, pre-commit |
| Snyk IaC | Terraform, CloudFormation, K8s, ARM | CLI, GitHub, GitLab, IDE |
| Bridgecrew (Prisma Cloud IaC) | Checkov cloud platform | CI/CD, PR checks, auto-fix |
| Infracost + security | Cost + security in same workflow | CLI, CI/CD |
| OPA (Open Policy Agent) | Policy engine; Rego language | Any IaC, CI/CD, admission control |

**CloudFormation Security Scanning**:
| Tool | Features | Integration |
|------|----------|-------------|
| cfn-nag | AWS-specific scanning; IAM, security group, encryption checks | CLI, CI/CD |
| cfn-guard | Rule-based; AWS-provided rules; custom rules | CLI, CI/CD, CodePipeline |
| Checkov | CloudFormation support | CLI, CI/CD |
| AWS Config rules | Post-deployment compliance | AWS natively |

### 61.3 Policy as Code (OPA/Rego)

**OPA Architecture for IaC**:
```
IaC File (main.tf) → OPA (Rego Policy) → Pass/Fail Decision
                         ↑
                    Policy Files (.rego)
```

**Example: S3 Bucket Encryption Policy**:
```rego
package terraform.aws

# Deny S3 buckets with server-side encryption disabled
deny[msg] {
    resource := input.resource.aws_s3_bucket[name]
    not resource.server_side_encryption_configuration
    msg := sprintf("S3 bucket %v must have encryption enabled", [name])
}

# Deny S3 buckets with public ACLs
deny[msg] {
    resource := input.resource.aws_s3_bucket[name]
    resource.acl == "public-read" or resource.acl == "public-read-write"
    msg := sprintf("S3 bucket %v has public ACL: %v", [name, resource.acl])
}

# Deny EC2 instances with public IP addresses
deny[msg] {
    resource := input.resource.aws_instance[name]
    resource.associate_public_ip_address == true
    msg := sprintf("EC2 instance %v has public IP address", [name])
}

# Require all resources to have tags
deny[msg] {
    resource := input.resource.aws_instance[name]
    not resource.tags.Environment
    msg := sprintf("EC2 instance %v must have Environment tag", [name])
}
```

**Running OPA against Terraform**:
```bash
# Generate Terraform plan in JSON
terraform plan -out=tfplan.binary
terraform show -json tfplan.binary > tfplan.json

# Inject resource changes into OPA
opa eval --format pretty --data policies/ --input tfplan.json "data.terraform.deny"

# Fail pipeline if any deny rules fire
opa eval --format values --data policies/ --input tfplan.json "data.terraform.deny" | jq '. | length' | grep -q ^0$
```

### 61.4 IaC Security in CI/CD Pipeline

**GitHub Actions Workflow with IaC Security**:
```yaml
name: IaC Security Scan
on:
  pull_request:
    paths:
      - 'terraform/**'
      - 'cloudformation/**'

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      id-token: write

    steps:
      - uses: actions/checkout@v4

      # Secret detection
      - name: Secret Scanning
        uses: trufflesecurity/trufflehog@v3
        with:
          extra_args: --only-verified

      # Terraform formatting
      - name: Terraform Fmt
        run: terraform fmt -check -recursive

      # Static analysis
      - name: Tfsec
        uses: aquasecurity/tfsec-action@v1.0.3
        with:
          soft_fail: false
          additional_args: --concise-output

      # Comprehensive scanning
      - name: Checkov
        uses: bridgecrewio/checkov-action@v12
        with:
          directory: terraform/
          framework: terraform
          soft_fail: false
          extra_args: >-
            --skip-check CKV_AWS_117,CKV_AWS_118
            --compact

      # Policy as code
      - name: OPA Policy Check
        run: |
          terraform init
          terraform plan -out=tfplan.binary
          terraform show -json tfplan.binary > tfplan.json
          opa eval --format values \
            --data policies/ \
            --input tfplan.json \
            "data.terraform.deny"
          echo "All OPA policies passed"

      # Cost estimation
      - name: Infracost
        uses: infracost/actions@v3
        with:
          api_key: ${{ secrets.INFRACOST_API_KEY }}

      # Post comment on PR
      - name: Comment PR
        uses: actions/github-script@v7
        if: failure()
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚫 IaC security scan failed. Review findings before merging.'
            })
```

### 61.5 Drift Detection and Remediation

**Drift Detection Methods**:
| Method | Tool | Detection Type | Remediation |
|--------|------|----------------|-------------|
| AWS Config | Native AWS | Resource configuration drift | Auto-remediate with SSM automations |
| Terraform plan | Terraform | State drift | `terraform apply` to reconcile |
| Azure Policy | Native Azure | Configuration drift | DeployIfNotExists policy |
| GCP Organization Policy | Native GCP | Policy compliance drift | Automated remediation via SCC |
| OPA Gatekeeper | K8s admission | K8s resource drift | Deny non-compliant resources |
| Atlantis + Checkov | PR-driven | IaC drift before apply | Block PR merge |

**Drift Prevention**:
- **Prevent manual changes**: IAM policies to block console/resource creation outside IaC
- **SCP enforcement**: Organization-level SCPs preventing resource creation outside IaC (e.g., `cloudformation:CreateStack` if IaC must use it)
- **GitOps model**: All infrastructure changes must go through Git PR + CI/CD
- **Tagging enforcement**: Tag all resources with `managed-by: terraform` to identify drift sources
- **Approval gates**: Require IaC security scan pass before merge

### 61.6 IaC Security Best Practices Summary

1. **Scan all IaC before deployment**: Use Checkov, tfsec, cfn-nag, cfn-guard in CI/CD pipeline
2. **Never hardcode secrets**: Use Variables + Secrets Manager (references only, no values)
3. **Policy as code**: Enforce security policies with OPA/Rego
4. **Version control everything**: All IaC in Git with reviewed PRs
5. **Immutable infrastructure**: Never modify running resources directly; redeploy via IaC
6. **Module security**: Version-pin modules; scan module registry for vulnerabilities
7. **Least privilege IaC**: Separate deployment roles from administrator roles
8. **Drift detection**: Continuous monitoring for manual changes outside IaC
9. **State file security**: Encrypt Terraform state (S3 + DynamoDB, KMS); restrict state file access
10. **Pipeline security**: Protect CI/CD credentials; use OIDC federation; sign artifacts



---

## 62. Advanced Cryptography and Public Key Infrastructure

### 62.1 Cryptographic Primitives

**Symmetric Encryption**:
| Algorithm | Key Size | Block Size | Mode | Use Case |
|-----------|----------|------------|------|----------|
| AES-256 | 256-bit | 128-bit | GCM (authenticated) | Data at rest (S3, EBS, RDS) |
| AES-256 | 256-bit | 128-bit | CBC (legacy) | Legacy compatibility |
| ChaCha20-Poly1305 | 256-bit | Stream | AEAD | TLS 1.3, mobile, IoT |
| AES-GCM-SIV | 256-bit | 128-bit | Nonce-misuse resistant | High-security storage |

**Key Derivation**:
| Function | Purpose | Cloud Use |
|----------|---------|-----------|
| PBKDF2 | Password-based key derivation | Key encryption keys |
| bcrypt | Slow hashing for passwords | User authentication |
| scrypt | Memory-hard password hashing | Wallet security |
| Argon2id | Modern password hashing (OWASP recommended) | New implementations |
| HKDF | Key derivation from shared secret | KMS key derivation |

**Asymmetric Encryption**:
| Algorithm | Key Size | Purpose | Cloud Service |
|-----------|----------|---------|--------------|
| RSA | 2048-4096 bit | Encryption, signing | ACM, CloudFront signed URLs |
| ECC (P-256/P-384/P-521) | 256-521 bit | Signing, key exchange | KMS, CloudHSM, ACM |
| Ed25519 | 256-bit | Signing (modern) | SSH keys, Sigstore |
| X25519 | 256-bit | Key exchange | TLS 1.3 |

**Hash Functions**:
| Algorithm | Output Size | Security Level | Status |
|-----------|-------------|----------------|--------|
| SHA-256 | 256-bit | 128-bit | Recommended |
| SHA-384 | 384-bit | 192-bit | Recommended |
| SHA-512 | 512-bit | 256-bit | Recommended |
| SHA-3 | Variable | Variable | Recommended (NIST) |
| BLAKE2b | 512-bit | 256-bit | High performance |
| MD5 | 128-bit | Broken | Do not use |
| SHA-1 | 160-bit | Broken (SHAttered) | Do not use |

**Message Authentication Codes (MAC)**:
| Algorithm | Type | Use Case |
|-----------|------|----------|
| HMAC-SHA256 | Hash-based | AWS Signature v4, JWT |
| AES-GCM (GMAC) | Cipher-based | TLS 1.2/1.3 |
| Poly1305 | One-time MAC | TLS 1.3 (ChaCha20-Poly1305) |
| CMAC | Block cipher-based | NIST SP 800-38B |

### 62.2 PKI Architecture

**PKI Hierarchy**:
```
Root CA (offline, HSM-backed)
  └── Intermediate CA (online, restricted)
        ├── Server Certificates (TLS)
        ├── Client Certificates (mTLS)
        ├── Code Signing Certificates (authenticode)
        └── Email Certificates (S/MIME)
```

**Cloud PKI Services**:
| Provider | CA Service | Key Management | Use Case |
|----------|-----------|----------------|----------|
| AWS ACM | Private CA | KMS/CloudHSM | Internal TLS, mTLS, code signing |
| AWS Certificate Manager | Public + Private | KMS | CloudFront, ALB, API Gateway certs |
| Azure Key Vault | Private CA | Managed HSM | Internal certs, app TLS |
| Azure App Service Cert | Public | Key Vault | App Service TLS |
| GCP Certificate Authority Service | Private CA | Cloud HSM | Internal PKI, mTLS, code signing |
| Let's Encrypt / ACME | Public | Automated | Web TLS, free |

**Certificate Management Lifecycle**:
```
Request → Validation → Issuance → Distribution → Monitoring → Renewal → Revocation
   ↑                                                                        │
   └────────────────────────────────────────────────────────────────────────┘
```

**Certificate Validation Methods**:
| Method | Description | Cloud Example |
|--------|-------------|---------------|
| DNS | DNS TXT record verification | ACM email + DNS validation |
| Email | Email to domain admin | ACM email validation |
| API | Automated via ACME protocol | cert-manager + Let's Encrypt |
| Private | Internal CA trust | ACM Private CA |

**Certificate Revocation**:
| Method | Latency | Cloud Support |
|--------|---------|---------------|
| CRL (Certificate Revocation List) | Hours-days | ACM, Private CA, S3 distribution |
| OCSP (Online Certificate Status Protocol) | Seconds-minutes | Private CA OCSP responder |
| OCSP Stapling | Real-time | CloudFront, ALB, NLB |
| Short-lived certs (auto-renewal) | No revocation needed | cert-manager, ACM |

### 62.3 TLS Deep Dive

**TLS Protocol Versions**:
| Version | Status | Key Features |
|---------|--------|-------------|
| TLS 1.0 | Deprecated (PCI DSS prohibited) | CBC modes, RC4 |
| TLS 1.1 | Deprecated (PCI DSS prohibited) | CBC modes |
| TLS 1.2 | Recommended (interop) | AEAD (GCM/CCM), ECDHE, SHA-256 |
| TLS 1.3 | Recommended | 1-RTT handshake, 0-RTT, PFS, only AEAD, HKDF |

**TLS 1.3 Handshake**:
```
Client → ClientHello (key_share, sig_algs, supported_versions)
Server → ServerHello (key_share, cipher_suite)
Server → EncryptedExtensions, Certificate, CertificateVerify, Finished
Client → Finished
[Application Data]  ← 1-RTT (vs 2-RTT for TLS 1.2)
```

**Cloud TLS Configuration Hardening**:
```nginx
# CloudFront: Viewer protocol policy
# Set to: TLSv1.2_2021 or TLSv1.2_2019
# Security headers added at CloudFront:
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload";
# Cipher preference: TLS_AES_128_GCM_SHA256 (TLS 1.3)

# ALB: SSL policy
# Use: ELBSecurityPolicy-TLS13-1-2-2021-06
# Custom policy:
ssl_protocols TLSv1.2 TLSv1.3
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384
ssl_prefer_server_ciphers on

# Azure App Gateway:
# Policy: AppGwSslPolicy20220101 (TLS 1.2+)
# Custom: Front Door WAF policy with TLS termination

# GCP HTTPS Load Balancer:
# TLS 1.2+ enforced; TLS 1.3 enabled by default
# Google-managed certificates auto-renew
```

**mTLS (Mutual TLS)**:
| Component | Certificate | Usage |
|-----------|-------------|-------|
| Server | Server cert (SAN includes hostname) | Authenticates to client |
| Client | Client cert (identity bound to user/service) | Authenticates to server |
| CA | Internal CA in ACM/Key Vault/CA Service | Issues and validates certs |
| Validation | Certificate verification + OCSP/CRL | Ensures certs valid and not revoked |

**Cloud mTLS Implementations**:
- **AWS**: ACM Private CA → ALB mTLS (mutual authentication); API Gateway mTLS; App Mesh mTLS
- **Azure**: Application Gateway mTLS; API Management mTLS; AKS mTLS (Istio, linkerd)
- **GCP**: External HTTP(S) LB mTLS (client TLS); Istio on GKE mTLS; Apigee mTLS

### 62.4 Digital Signatures and Code Signing

**Digital Signature Process**:
```
Signer:
  Hash(Data) → Sign(Hash, PrivateKey) → Signature
Verifier:
  Hash(Data) → Verify(Signature, PublicKey) → Match/No Match
```

**Code Signing in Cloud**:
| Service | Purpose | Key Protection |
|---------|---------|----------------|
| AWS Signer | Code signing for Lambda, IoT | KMS key with usage restrictions |
| Azure Code Signing | Windows app signing (Microsoft partner) | Hardware-backed key |
| GCP Cloud HSM + Cosign | Container image signing | HSM-backed key |
| Sigstore (cosign) | Open-source container signing | Ephemeral keys, transparency log |

**Signed Container Images**:
```bash
# Generate key pair
cosign generate-key-pair

# Sign container image
cosign sign --key cosign.key ghcr.io/myorg/myimage:v1

# Verify container image
cosign verify --key cosign.pub ghcr.io/myorg/myimage:v1

# Sign with KMS
cosign sign --key awskms:///arn:aws:kms:us-east-1:ACCOUNT:key/KEY_ID ghcr.io/myorg/myimage:v1
```

### 62.5 Homomorphic Encryption and Advanced Topics

**Homomorphic Encryption Types**:
| Type | Operations | Performance | Readiness |
|------|-----------|-------------|-----------|
| Partially HE (PHE) | Addition or multiplication | Fast | Production (add-only: cloud voting) |
| Somewhat HE (SWHE) | Limited additions + multiplications | Moderate | Research |
| Fully HE (FHE) | Unlimited operations | Very slow (1000-1Mx) | Experimental |
| Leveled HE | Bounded operations | Slow | Emerging products |

**Cloud Use Cases**:
- **Confidential Computing**: Azure SGX, AWS Nitro, GCP SEV-SNP (hardware-based)
- **HE for Analytics**: Encrypted data queries on third-party cloud
- **Private Set Intersection (PSI)**: Match datasets across orgs without sharing raw data
- **Secure Multi-Party Computation (SMPC)**: Multiple parties compute on shared data

**Post-Quantum Cryptography (PQC)**:
| Algorithm | Type | NIST Standardization |
|-----------|------|---------------------|
| CRYSTALS-Kyber | KEM (Key Encapsulation) | Selected 2022 |
| CRYSTALS-Dilithium | Digital Signature | Selected 2022 |
| SPHINCS+ | Hash-based Signature | Selected 2022 |
| FALCON | Lattice-based Signature | Selected 2022 |

**Cloud PQC Preparedness**:
- NIST anticipates quantum threat within 10-20 years
- Hybrid certificates (classical + PQC) for migration
- Crypto-agility: ability to switch algorithms without redesign
- AWS/PKI providers adding PQC support

---

## 63. Digital Forensics in the Cloud

### 63.1 Cloud Forensics Challenges

| Challenge | Traditional Forensics | Cloud Forensics |
|-----------|----------------------|-----------------|
| Physical Access | Full disk access, forensic workstation | No physical access; API-only |
| Evidence Volatility | RAM, swap, temp files | Shared infrastructure, ephemeral resources |
| Data Ownership | Full ownership | Shared responsibility model |
| Chain of Custody | Physical custody | Digital chain of custody |
| Multi-Tenancy | Single system | Shared physical resources |
| Jurisdiction | Local | Global, data residency issues |
| Preservation | Power off, image disk | Snapshot, CloudTrail freeze |
| Collection Tools | EnCase, FTK, dd | Cloud API, SDK, CLI |
| Data Volume | GB-TB | TB-PB |
| Encryption | Can decrypt with keys | KMS keys held by customer but may expire |
| Ephemeral Resources | Persistent storage | Auto-scaling groups, spot instances, serverless |

### 63.2 Cloud Forensic Evidence Sources

**AWS Forensic Evidence**:
| Evidence Source | Data Obtained | Collection Method |
|----------------|--------------|-------------------|
| CloudTrail | All API calls (who, what, when, from where) | `aws cloudtrail lookup-events` |
| EC2 Snapshot | OS disk, application data | `aws ec2 create-snapshot` |
| EBS Snapshot | Volume-level data | `aws ec2 create-snapshot` + copy to forensics account |
| VPC Flow Logs | Network traffic metadata | S3 query (Athena) |
| GuardDuty Findings | Detected threats | `aws guardduty get-findings` |
| Lambda Logs | Function execution logs | CloudWatch Logs export |
| S3 Access Logs | Object access records | S3 inventory + access logs analysis |
| Instance Metadata | IAM role, instance identity | IMDSv2 query (from instance) |
| Memory Dump | RAM contents (limited support) | Linux `fmems` / Windows `DumpIt` |
| Systems Manager | OS-level data (limited) | SSM Run Command + S3 upload |
| CloudWatch Logs | Application/OS logs | Export to S3 |
| RDS Snapshots | Database state | `aws rds create-db-snapshot` |
| ECR Images | Container images | `docker pull` + save |

**Azure Forensic Evidence**:
| Evidence Source | Collection Method |
|----------------|-------------------|
| Activity Log | `az monitor activity-log list` |
| VM Snapshot | `az vm capture --vhd-name-prefix` |
| Disk Snapshot | `az disk create --source` |
| NSG Flow Logs | `az network watcher flow-log show` |
| Log Analytics | KQL queries, export to storage |
| Key Vault Audit | `az monitor diagnostic-settings create` |
| Defender Alerts | `az security alert list` |
| SQL Audit Logs | Azure SQL auditing + storage |
| AKS Audit | Container insights + K8s audit logs |

**GCP Forensic Evidence**:
| Evidence Source | Collection Method |
|----------------|-------------------|
| Cloud Audit Logs | `gcloud logging read` |
| Persistent Disk Snapshot | `gcloud compute disks snapshot` |
| VM Image | `gcloud compute images create` |
| VPC Flow Logs | BigQuery query on log export |
| SCC Findings | `gcloud scc findings list` |
| Cloud SQL Backup | `gcloud sql backups create` |
| Container Image | `docker pull` + `gcloud container images` |
| Cloud Functions Logs | Cloud Logging + export |
| Secret Access | `gcloud secrets versions access` |

### 63.3 Forensic Collection Methodology

**Collection Order of Volatility**:
```
Highest Volatility
  1. CPU registers, cache
  2. RAM (memory dump)
  3. Network connections
  4. Running processes
  5. Temporary files (/tmp, /var/tmp)
  6. Disk (EBS/PD snapshot)
  7. Remote logs (CloudTrail, CloudWatch)
  8. Archival data (S3, Glacier, backups)
Lowest Volatility
```

**Cloud Forensic Collection Steps**:
```bash
# AWS: Isolate and forensically acquire
# 1. Isolate instance (apply quarantine SG)
aws ec2 modify-instance-attribute --instance-id i-12345 --groups sg-quarantine

# 2. Create forensic snapshot (with description)
aws ec2 create-snapshot --volume-id vol-12345 \
  --description "Forensic-$(date +%Y%m%d_%H%M%S)-incident-12345"

# 3. Copy snapshot to forensics account
aws ec2 copy-snapshot --source-region us-east-1 \
  --source-snapshot-id snap-12345 \
  --destination-region us-east-1 \
  --destination-description "Forensic copy - incident 12345"

# 4. Export CloudTrail for the timeframe
aws cloudtrail lookup-events --start-time "$INCIDENT_START" \
  --end-time "$INCIDENT_END" \
  --max-results 50 > cloudtrail-events.json

# 5. Collect GuardDuty findings
aws guardduty list-findings --detector-id DETECTOR_ID
aws guardduty get-findings --detector-id DETECTOR_ID --finding-ids [...]

# 6. Export VPC Flow Logs to Athena for analysis
# Query flow logs for the affected instance IP

# 7. Collect instance metadata (if accessible)
TOKEN=$(curl -X PUT http://169.254.169.254/latest/api/token \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/dynamic/instance-identity/document
```

**Forensic Analysis of Cloud Snapshots**:
```bash
# Mount EBS snapshot in forensics account
# Launch forensics instance + attach volume
aws ec2 attach-volume --volume-id vol-forensic-12345 \
  --instance-id i-forensic-67890 --device /dev/xvdf

# Mount (read-only)
mkdir /mnt/forensic
mount -o ro,noexec /dev/xvdf1 /mnt/forensic

# Analyze
# Collect timeline (mitre_tools or similar)
# Hash all files (SHA-256)
find /mnt/forensic -type f -exec sha256sum {} \; > /evidence/file_hashes.txt

# Extract logs
cp /mnt/forensic/var/log/* /evidence/logs/

# Check for persistence mechanisms
ls -la /mnt/forensic/etc/cron* /mnt/forensic/etc/systemd/*.service
cat /mnt/forensic/root/.ssh/authorized_keys
cat /mnt/forensic/var/spool/cron/*

# Check for malware (ClamAV)
clamscan -r /mnt/forensic

# Check for rootkits (chkrootkit on mounted fs)
chkrootkit -r /mnt/forensic

# Hash evidence and submit to SIEM/IR platform
```

### 63.4 Chain of Custody in Cloud

**Digital Chain of Custody Documentation**:
```yaml
Evidence ID: EVID-2026-06-001
Collection Timestamp: 2026-06-27T14:30:00Z
Collector: security-team@company.com
Source: AWS EC2 i-12345 / Volume vol-67890
Collection Method: API create-snapshot
Hash (SHA-256): abcdef1234567890...
Copy 1 Location: Forensics Account / snap-forensic-001
Copy 2 Location: Immutable S3 bucket (evidence-bucket)
Chain:
  - 14:30:00 Collected by security-user/Admin (IP: 10.0.1.50)
  - 14:32:00 Copied to forensics account by forensics-role (automated)
  - 14:35:00 Hash verified by forensics-team/Mike (mike@company.com)
  - 15:00:00 Analysis started by forensics-team/Mike
  - 15:30:00 Hash re-verified (no change)
```

**Cloud-Specific Chain of Custody Tools**:
- **AWS**: Config rules for forensic snapshot immutability; CloudTrail for all evidence access
- **Azure**: Activity Log for snapshot operations; Azure Policy for evidence retention
- **GCP**: Cloud Audit Logs; Access Transparency for GCP staff access to evidence
- **General**: Evidence stored in immutable storage (S3 Object Lock / Azure Immutable Blob / GCS retention policy); IAM controls restrict evidence access

### 63.5 Container Forensics

**Container Evidence Collection**:
```bash
# Save container image (from registry or runtime)
docker save compromised-container > compromised.tar

# Export container filesystem (if running)
docker export compromised-container > container-fs.tar

# Inspect container metadata
docker inspect compromised-container > container-inspect.json

# Extract container logs
docker logs compromised-container > container-logs.txt

# Check container environment variables
docker exec compromised-container env > container-env.txt

# Kubernetes: get pod logs
kubectl logs compromised-pod -n production > pod-logs.txt

# Kubernetes: describe pod
kubectl get pod compromised-pod -n production -o yaml > pod-manifest.yaml

# Kubernetes: collect events
kubectl get events -n production --sort-by='.lastTimestamp' > k8s-events.txt

# Get pod definition from etcd backup (if available)
```

### 63.6 Serverless Forensics

**Lambda Forensic Evidence**:
```yaml
# Collection checklist:
- [ ] Lambda function configuration (timeout, memory, role, VPC, env vars)
- [ ] Lambda versions and aliases
- [ ] CloudWatch Logs for function execution
- [ ] X-Ray traces (if enabled)
- [ ] CloudTrail Invoke events
- [ ] Event source mapping (S3, SQS, DynamoDB, API Gateway)
- [ ] Lambda layers (dependencies)
- [ ] Dead Letter Queue contents
- [ ] Reserved concurrency configuration
- [ ] VPC configuration (subnets, security groups)
```

**Serverless Forensic Analysis**:
```bash
# 1. Identify all function invocations during incident
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=Invoke \
  --start-time "$INCIDENT_START" --end-time "$INCIDENT_END"

# 2. Export function logs
aws logs export-task --log-group-name /aws/lambda/function-name \
  --destination bucket --destination-prefix forensics/func-logs

# 3. Check function code version
aws lambda get-function --function-name function-name \
  --query 'Configuration.Version'

# 4. Review environment variables for secrets exposure
aws lambda get-function-configuration --function-name function-name \
  --query 'Environment'

# 5. Check for Lambda layer vulnerabilities
aws lambda list-function-event-invoke-configs --function-name function-name

# 6. Analyze error patterns for exploit attempts
aws logs filter-log-events --log-group-name /aws/lambda/function-name \
  --filter-pattern 'ERROR' --start-time "$INCIDENT_START" --end-time "$INCIDENT_END"
```

---

## 64. Cyber Threat Intelligence (CTI)

### 64.1 CTI Framework

**Threat Intelligence Lifecycle**:
```
Planning & Direction → Collection → Processing → Analysis → Dissemination → Feedback
       ↑                                                                        │
       └────────────────────────────────────────────────────────────────────────┘
```

**Intelligence Types**:
| Type | Description | Shelf Life | Example |
|------|-------------|------------|---------|
| Strategic | High-level trends, threat actor motives, geopolitical context | Years | "Nation-state actors increasing attacks on cloud infrastructure" |
| Operational | Specific campaigns, TTPs, targeting | Months | "APT29 using OAuth token theft to target cloud admins" |
| Tactical | IoCs (IPs, domains, hashes, URLs) | Days-Weeks | "C2 server at 51.15.0.0/24 using Stratum mining protocol" |
| Technical | Specific tools, malware samples, vulnerabilities | Hours-Days | "CVE-2026-1234 PoC in the wild" |

### 64.2 CTI Frameworks and Models

**MITRE ATT&CK Cloud Matrix**:
| Tactic | ID | Technique | Cloud Example |
|--------|----|-----------|---------------|
| Initial Access | T1078.004 | Valid Accounts (Cloud Accounts) | Stolen AWS IAM keys |
| Initial Access | T1199 | Trusted Relationship | Third-party SaaS compromise |
| Persistence | T1098.005 | Account Manipulation (Device Registration) | Unauthorized Azure AD device |
| Privilege Escalation | T1078.004 | Cloud Roles | AssumeRole to admin role |
| Defense Evasion | T1578.002 | Modify Cloud Compute Infrastructure | Create/delete snapshots |
| Credential Access | T1525 | Internal Spearphishing | Impostor cloud portal login |
| Lateral Movement | T1021.007 | Remote Services (Cloud Services) | EC2 Instance Connect |
| Collection | T1530 | Data from Cloud Storage | S3 bucket enumeration |
| Exfiltration | T1537 | Transfer Data to Cloud Account | Copy S3 to attacker account |
| Impact | T1496 | Resource Hijacking | Crypto mining on EC2 |

**Cyber Kill Chain (Lockheed Martin)**:
```
Reconnaissance → Weaponization → Delivery → Exploitation → Installation → C2 → Actions on Objectives
     ↑              ↑               ↑            ↑              ↑        ↑            ↑
    OSINT         Exploit kit    Phishing/    Vulnerability  Backdoor     HTTPS      Data exfil
    Cloud enum    Maldoc         Watering hole   exploit    installation  beacon    Crypto mining
```

**Diamond Model**:
```
           Adversary
              ↑
             / \
            /   \
           /     \
Infrastructure → Capability
          \     /
           \   /
            \ /
             ↓
           Victim
```

### 64.3 Threat Intelligence Sources

**Open Source (OSINT)**:
| Source | Type | Example |
|--------|------|---------|
| AlienVault OTX | IoCs, pulses | `https://otx.alienvault.com` |
| VirusTotal | File/URL/IP analysis | `https://www.virustotal.com` |
| AbuseIPDB | IP reputation | `https://www.abuseipdb.com` |
| Shodan | Internet-connected devices | `https://www.shodan.io` |
| Censys | Internet scanning | `https://censys.io` |
| GreyNoise | Internet noise (ignore background) | `https://www.greynoise.io` |
| MISP | Threat sharing platform | `https://www.misp-project.org` |
| CVE/NVD | Vulnerability database | `https://nvd.nist.gov` |
| Exploit-DB | Exploit details | `https://www.exploit-db.com` |
| HAVE I BEEN PWNED | Credential leaks | `https://haveibeenpwned.com` |
| URLScan.io | Website analysis | `https://urlscan.io` |

**Commercial Threat Intel Feeds**:
| Feed | Coverage | Cloud Integration |
|------|----------|-------------------|
| Recorded Future | All-source CTI | API integration with SIEM |
| Mandiant (Google) | APT tracking | Chronicle integration |
| CrowdStrike Falcon | Adversary intel | CrowdStrike + cloud EDR |
| Anomali | ThreatStream | SIEM integration |
| ThreatConnect | SOAR + TIP | Playbook integration |
| IBM X-Force | Exchange, CVE intel | QRadar integration |

**Cloud-Native Threat Intel**:
| Provider | Service | Description |
|----------|---------|-------------|
| AWS | GuardDuty + Threat Intel | AWS-managed threat intel for cloud |
| AWS | WAF IP Sets | AWS-managed or custom IP reputation |
| Azure | Defender Threat Intel | Microsoft threat intelligence |
| Azure | Sentinel TIP connector | TAXII/MISP to Sentinel |
| GCP | SCC Threat Intel | Google threat intelligence |
| GCP | Chronicle | Google's SIEM with built-in intel |

### 64.4 IoC Management

**IoC Types**:
| Type | Format | Example |
|------|--------|---------|
| IP Address | IPv4/IPv6 | 192.0.2.1 |
| Domain | FQDN | evil.example.com |
| URL | Full URL | https://evil.example.com/malware.exe |
| File Hash | MD5/SHA-1/SHA-256 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| Email | Address | attacker@evil.com |
| Registry | Path | HKLM\Software\Microsoft\Malware |
| YARA Rule | Pattern | `rule BadFile { strings: $a = "malware" condition: $a }` |
| Sigma Rule | SIEM detection | `title: Suspicious PowerShell` |

**IoC Lifecycle**:
```
Create (threat intel) → Publish (feed) → Import (SIEM/TIP) → Match (detection) → Respond (block/hunt) → Archive
```

**Cloud IoC Blocking**:
```bash
# AWS WAF IP set
aws wafv2 create-ip-set --name "ThreatIntelBlocklist" \
  --scope REGIONAL --ip-address-version IPV4 \
  --addresses "192.0.2.0/24" "198.51.100.0/24" "203.0.113.0/24"

# GuardDuty threat intel sets (for custom intel)
aws guardduty create-threat-intel-set --detector-id DETECTOR_ID \
  --name "Custom-Threat-Intel" --location "s3://my-bucket/ioc-list.txt" \
  --activate

# Azure WAF custom rules
az network front-door waf-policy managed-rule-set override add \
  --policy-name "myWAF" --resource-group "myRG" \
  --rule-set-name "DefaultRuleSet" --rule-group-name "IPBlacklist" \
  --action Block --priority 10

# GCP Cloud Armor IP blocklist
gcloud compute security-policies rules create 1000 \
  --security-policy my-policy \
  --src-ip-ranges "192.0.2.0/24" --action "deny-403"
```

### 64.5 Threat Hunting with CTI

**Hunting with IoCs**:
```bash
# AWS: CloudTrail search for IoC IPs
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=ConsoleLogin \
  --query "Events[?contains(UserIdentity, \`$IOC_IP\`)]"

# Azure Sentinel: KQL hunting query
let IOCs = dynamic(["192.0.2.1", "evil.com", "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"]);
union withsource=source_table *
| where * has_any (IOCs)
| extend IoCMatched = extract_all(@"([0-9]{1,3}\.){3}[0-9]{1,3}|([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}|[a-fA-F0-9]{64}", *)

# GCP: Log search by IoC
gcloud logging read "textPayload:(\"192.0.2.1\" OR \"evil.com\")" \
  --freshness=7d --project PROJECT_ID
```

**TTB (Tactics, Techniques, Behaviors) Hunting**:
```python
# Identify suspicious AssumeRole patterns (technique T1078.004)
# Hunt for roles assumed from unexpected accounts
import boto3
from datetime import datetime, timedelta

client = boto3.client('cloudtrail')
events = client.lookup_events(
    LookupAttributes=[{'AttributeKey': 'EventName', 'AttributeValue': 'AssumeRole'}],
    StartTime=datetime.now() - timedelta(days=7)
)

# Filter for cross-account AssumeRole
for event in events['Events']:
    ct = json.loads(event['CloudTrailEvent'])
    if ct.get('userIdentity', {}).get('type') == 'AssumedRole':
        account_from = ct['userIdentity'].get('accountId')
        role_arn = ct.get('requestParameters', {}).get('roleArn', '')
        account_to = role_arn.split(':')[4]
        if account_from != account_to:
            print(f"Cross-account role assumption: {account_from} → {role_arn}")
```

---

## 65. Cloud Security for Healthcare (HIPAA)

### 65.1 HIPAA Overview

**HIPAA Rules**:
| Rule | Purpose | Key Requirements |
|------|---------|-----------------|
| Privacy Rule | Protects individually identifiable health information (PHI) | Use/disclosure restrictions, patient rights, minimum necessary |
| Security Rule | Administrative, physical, technical safeguards | Risk analysis, access control, audit controls, integrity, transmission security |
| Breach Notification Rule | Breach notification requirements | 60-day notification for 500+ records; annual log for <500 |
| Omnibus Rule (2013) | Extended to business associates | BA liability, BA agreements, GDPR-like patient rights |
| Enforcement Rule | Penalties for non-compliance | Tiered civil penalties ($100-$50K per violation) |

**HIPAA Security Rule Safeguards**:
| Category | Standard | Cloud Implementation |
|----------|----------|---------------------|
| Administrative | Security Management Process | Risk assessment, policies, workforce training |
| Administrative | Assigned Security Responsibility | Named security officer |
| Administrative | Workforce Security | Background checks, access termination |
| Administrative | Information Access Management | Authorization, access management |
| Administrative | Security Awareness Training | Training, reminders, password mgmt |
| Administrative | Security Incident Procedures | IR plan, response, reporting |
| Administrative | Contingency Plan | DR/BCP, backups, testing |
| Administrative | Evaluation | Periodic compliance assessment |
| Administrative | BA Contracts & Other Arrangements | BAAs with cloud providers |
| Physical | Facility Access Controls | Data center security (provider-managed) |
| Physical | Workstation Security | Cloud workstation configuration |
| Physical | Device and Media Controls | Disposal, re-use, accountability |
| Technical | Access Control | Unique user IDs, emergency access, auto-logoff, encryption |
| Technical | Audit Controls | Logging, monitoring, audit trails |
| Technical | Integrity Controls | E-signatures, checksums |
| Technical | Person or Entity Authentication | MFA, IAM, RBAC |
| Technical | Transmission Security | TLS 1.2+, VPN, encryption |

### 65.2 Cloud Provider BAA Availability

**AWS HIPAA Eligibility**:
- BAA available for HIPAA-eligible services
- HIPAA-eligible services: EC2 (dedicated or VPC), S3, RDS, DynamoDB, Redshift, KMS, CloudHSM, Lambda, EMR, Kinesis, CloudTrail, CloudWatch, Config, Direct Connect, VPN, WAF, Shield, Route53, SES, SQS, SNS, ElastiCache, WorkDocs, WorkMail, Connect, API Gateway, ECS, EKS, Aurora, DocumentDB, Neptune, QLDB, S3 Glacier
- NOT HIPAA-eligible: CloudFront (unless using OAI/OAC with S3), Route53 public DNS (but private zone is), some newer services
- Architecture must ensure no PHI stored/processed in non-eligible services
- Customer responsible for PHI detection and prevention

**Azure HIPAA Eligibility**:
- BAA available for all Azure services (broad coverage)
- Covered Services: All Azure services under customer's subscription
- Azure HIPAA compliance documentation available
- Additional controls: Azure Policy for HIPAA, Compliance Manager templates
- Azure HIPAA guidance: Microsoft documentation includes architecture patterns

**GCP HIPAA Eligibility**:
- BAA available for covered services
- Covered: Compute Engine, GKE, Cloud Storage, Cloud SQL, BigQuery, Cloud KMS, Cloud HSM, VPC, Cloud Load Balancing, Cloud CDN, Cloud Armor, Cloud Audit Logs, Cloud Functions, Cloud Run, App Engine, Cloud IAM, VPC Service Controls, Access Transparency
- NOT covered: Some GCP services (check BAA list)
- Additional: Assured Workloads for regulated workloads

### 65.3 HIPAA Cloud Architecture

**HIPAA-Compliant Architecture in AWS**:
```yaml
# Architecture components:
# 1. VPC with private subnets (no public IPs for workload instances)
# 2. IAM least privilege (no wildcard actions on PHI resources)
# 3. KMS CMEK for all storage (S3, EBS, RDS)
# 4. CloudTrail enabled (management + data events for S3)
# 5. S3 Block Public Access at account level
# 6. VPC endpoints for all AWS services (no internet egress)
# 7. AWS Config rules for HIPAA compliance
# 8. GuardDuty + Security Hub for threat detection
# 9. CloudWatch Logs with 6-year retention
# 10. Multi-factor authentication for all users

# Config rule: Check S3 bucket encryption
resource "aws_config_config_rule" "s3_bucket_sse_enabled" {
  name = "hipaa-s3-bucket-sse-enabled"
  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED"
  }
}

# Config rule: Check EBS volume encryption
resource "aws_config_config_rule" "ec2_volume_encryption" {
  name = "hipaa-ebs-encryption"
  source {
    owner             = "AWS"
    source_identifier = "ENCRYPTED_VOLUMES"
  }
}
```

**PHI Data Flow Security**:
```
Patient App (HTTPS) → CloudFront (OAC + WAF) → ALB (mTLS) → App (EC2, SG: ALB only) → RDS (KMS encrypted, SG: App only)
                           │                                                        │
                           ▼                                                        ▼
                    S3 access logs                                           CloudWatch Logs
                    (KMS encrypted)                                          (6yr retention, encrypted)
```

### 65.4 BAA Requirements

**Business Associate Agreement (BAA) Key Terms**:
- Definition of permitted uses and disclosures of PHI
- Security safeguards that BA must implement
- BA must report security incidents and breaches
- BA must ensure subcontractors comply (downstream BAAs)
- BA must return/destroy PHI upon termination
- BA must provide access to records for HHS investigation
- Liability for breach (BA responsible for their actions)
- Term and termination clauses

**Cloud BAA Checklist**:
- [ ] Provider signs BAA (check supported services list)
- [ ] Provider lists all subcontractors that process PHI
- [ ] Provider provides audit documentation (SOC 2 Type II, HIPAA report)
- [ ] Provider enables security controls (encryption, logging, access control)
- [ ] Provider supports PHI deletion upon contract termination
- [ ] Provider reports security incidents in timely manner
- [ ] Provider allows customer security assessments
- [ ] Provider restricts data residency (where PHI stored)
- [ ] Provider enables customer control over encryption keys
- [ ] Provider provides incident notification procedures

### 65.5 HIPAA Compliance Automation

**AWS HIPAA Compliance Tools**:
```bash
# Enable HIPAA-eligible Config rules
aws configservice put-config-rule --config-rule file://hipaa-rules.json

# Security Hub with HIPAA standards
aws securityhub enable-security-hub
aws securityhub batch-enable-standards \
  --standards-subscription-requests StandardsArn="arn:aws:securityhub:us-east-1::standards/hipaa/v/1.0.0"

# CloudTrail for HIPAA audit trails
aws cloudtrail create-trail --name hipaa-trail \
  --s3-bucket-name hipaa-audit-logs-prod \
  --is-multi-region-trail --enable-log-file-validation \
  --kms-key-id alias/cloudtrail-key

# AWS Audit Manager: HIPAA assessment
aws auditmanager create-assessment \
  --name "HIPAA-Compliance-Assessment" \
  --framework-id "arn:aws:auditmanager:us-east-1::framework/hipaa"
```

### 65.6 Healthcare IoT and Mobile Security

**HIPAA Mobile Security**:
- Encrypt PHI at rest on device (device-native encryption + app-level)
- TLS 1.2+ for all API calls
- Token-based auth with short expiry (OAuth 2.0)
- No PHI in push notification payloads
- App-level biometric auth
- Remote wipe capability for lost/stolen devices
- Background app refresh disabled when device locked

**Medical IoT Security**:
- Device identity (X.509 certificates in IoT Core)
- Data encryption in transit and at rest
- Device firmware signed and verified
- OTA updates with integrity verification
- Device quarantine on anomalous behavior
- Network segmentation: IoT devices in isolated VLAN/VPC
- HIPAA applies if device stores/transmits PHI

---

## 66. Cloud Security for Financial Services

### 66.1 Regulatory Landscape

| Regulation | Region | Scope | Key Requirements |
|------------|--------|-------|------------------|
| PCI DSS v4.0 | Global | Credit card data | Encryption, access control, logging, segmentation, regular testing |
| SOX | US | Public companies | ITGC controls, change management, access control, audit trails |
| GLBA | US | Financial institutions | Privacy notices, opt-out rights, safeguard rule |
| FFIEC | US | Banking | Risk assessment, vendor management, business continuity, authentication |
| NYDFS 500 | New York | Financial services | CISO, risk assessment, MFA, encryption, testing, 72-hour breach notification |
| PSD2/SCA | EU | Payment services | Strong customer authentication (multi-factor), APIs, secure communication |
| MAS TRM | Singapore | Financial institutions | Risk management, cybersecurity, technology resilience |
| APRA CPS 234 | Australia | Banking/insurance | Security capability, incident management, testing |

### 66.2 PCI DSS Cloud Requirements

**PCI DSS v4.0 Key Requirements**:
| Requirement | Description | Cloud Implementation |
|-------------|-------------|---------------------|
| 1 | Install/configure firewall | Security Groups, NACLs, WAF, Network Firewall |
| 2 | Change vendor defaults | AMI hardening, custom AMIs, CIS benchmarks |
| 3 | Protect stored cardholder data | Encryption (KMS/CloudHSM), tokenization, masking |
| 4 | Encrypt transmission | TLS 1.2+, VPN, Direct Connect |
| 5 | Anti-malware | EDR (CrowdStrike, Defender), CWPP, Inspector |
| 6 | Secure apps | SAST/DAST, WAF, patch management |
| 7 | Restrict access | IAM least privilege, RBAC, JIT |
| 8 | Unique IDs + MFA | IAM, SSO, Conditional Access, MFA for all |
| 9 | Physical security | Data center security (provider responsibility) |
| 10 | Logging | CloudTrail, VPC Flow Logs, SIEM, retention |
| 11 | Testing | Penetration testing, vulnerability scanning, IDS/IPS |
| 12 | Policy | Security policies, risk assessment, vendor management |

**PCI DSS Cloud Scoping**:
```
In Scope (CDE)             Out of Scope (non-CDE)
┌──────────────────────┐  ┌──────────────────────────┐
│ Cardholder Data      │  │ Corporate DNS, DHCP       │
│ + Sensitive Auth Data│  │ Employee workstations     │
│ (CVV, PIN, Track)    │  │ General web servers       │
│                      │  │ Management/backup servers │
│ CDE server, DB, App  │  │ SIEM (logs from CDE)     │
│ Network segment with │  │                           │
│ CDE traffic          │  │                           │
└──────────────────────┘  └──────────────────────────┘
    ↑ All CDE in single VPC, isolated by SGs + NACLs
```

**PCI Cloud Validated Encryption**:
- AES-256 (FIPS 140-2/3 validated) for data at rest
- TLS 1.2+ for data in transit
- KMS/CloudHSM for key management (FIPS 140-2 Level 2/3)
- No storage of CVV/PIN/Track data after authorization (prohibited)
- Tokenization: Replace PAN with token (reduces PCI scope)

### 66.3 SOX ITGC Controls

**SOX ITGC Domains**:
| Domain | Control Objectives | Cloud Evidence |
|--------|-------------------|----------------|
| Change Management | Authorized, tested, approved changes | CloudTrail, IaC PRs, approval gates |
| Logical Access | Least privilege, access reviews, MFA | IAM, Access Analyzer, IAM credential report |
| Computer Operations | Batch jobs, scheduling, monitoring | CloudWatch, Lambda scheduling, job monitoring |
| Program Development | Controlled development lifecycle | SDLC controls, code review, IaC scanning |
| Data Backup/Recovery | Backups verified, DR tested | AWS Backup, DR drills, restore tests |

**SOX Cloud Evidence Collection**:
```bash
# Access review evidence
aws iam generate-credential-report
aws iam get-credential-report

# Change management evidence (CloudTrail for all admin actions)
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=EventName,AttributeValue=CreateStack

# Backup verification evidence
aws backup describe-recovery-point \
  --backup-vault-name Default --recovery-point-arn arn:aws:backup:...

# System monitoring evidence (CloudWatch dashboards + alarms)
# Screen capture of monitoring dashboards

# DR testing evidence (DR test plans + results)
# Screen capture of failover tests
```

### 66.4 Financial Services Cloud Architecture

**Multi-Tier Cardholder Data Environment (CDE)**:
```
┌─────────────────────────────────────────────────────────────────────┐
│ AWS Account: Payment-CDE (PCI DSS scope)                           │
│ VPC: 10.0.0.0/16                                                    │
│                                                                      │
│  DMZ Subnet (10.0.1.0/24)                                           │
│  WAF (block SQLi/XSS) → CloudFront (TLS 1.2+) → ALB (mTLS)         │
│                                                                      │
│  Payment Subnet (10.0.2.0/24)                                       │
│  App EC2 (SG: ALB only; EBS encrypted; IMDSv2; SSM agent)          │
│                                                                      │
│  Transaction Subnet (10.0.3.0/24)                                    │
│  Tokenization Service (isolated: only token→PAN mapping)           │
│  HSM (CloudHSM for PCI HSM requirements)                           │
│                                                                      │
│  Database Subnet (10.0.4.0/24)                                      │
│  RDS (KMS encrypted; IAM auth; audit logging; backup)              │
│  DynamoDB (KMS encrypted; VPC endpoint)                            │
│                                                                      │
│  Logging Subnet (10.0.5.0/24)                                       │
│  CloudTrail (org trail; 7yr retention; S3 Object Lock)              │
│  SIEM Agent → Splunk (VPC endpoint)                                │
└─────────────────────────────────────────────────────────────────────┘
```

**CDE Segmentation Controls**:
- Security Groups: CDE resources only accept traffic from CDE sources
- NACLs: Stateless allow/deny for CDE subnets
- VPC endpoints: CDE traffic stays within AWS network (no internet)
- SCP: Deny IAM actions outside CDE account; deny CDE resource access from non-CDE accounts
- Flow Logs: All CDE network traffic logged (accepted + rejected)
- GuardDuty: CDE-only detector with enhanced monitoring
- Config: CDE-specific rules (encryption, port restrictions, MFA)

### 66.5 FFIEC and Banking Security

**FFIEC Cloud Security Guidance**:
| Domain | Key Controls |
|--------|-------------|
| Risk Management | Cloud risk assessment, vendor due diligence, third-party oversight |
| Data Security | Encryption, key management, data classification, DLP |
| Authentication | Multi-factor, risk-based authentication, session management |
| Business Continuity | Cloud DR planning, testing, failover procedures |
| Vendor Management | Contract review, on-site assessments, performance monitoring |
| Incident Response | Cloud-specific IR plan, testing, coordination with provider |

**NYDFS 500 Compliance Checklist**:
- [ ] CISO designated (written report to board annually)
- [ ] Risk assessment conducted (cybersecurity program based on risk)
- [ ] Policies approved by board (incident response, data governance, vendor)
- [ ] Access controls + MFA (for privileged accounts and external access)
- [ ] Cybersecurity awareness training (annual)
- [ ] Asset inventory + data classification
- [ ] Penetration testing (annual) + vulnerability scanning (continuous)
- [ ] Audit trail (5+ years of logs)
- [ ] Incident response plan (72-hour notification to DFS)
- [ ] Third-party vendor security policy
- [ ] Encryption (at rest + in transit)
- [ ] Business continuity/disaster recovery plan + annual testing
- [ ] Periodic risk assessment (annual minimum)
- [ ] Encryption key management policy

---

## 67. Cloud Security for Government and Public Sector

### 67.1 FedRAMP

**FedRAMP Impact Levels**:
| Level | Impact | Requirements |
|-------|--------|-------------|
| Low | Limited adverse effect | Basic security controls (NIST SP 800-53 low baseline) |
| Moderate | Serious adverse effect | Standard controls (125+ controls) |
| High | Severe/catastrophic effect | Enhanced controls (168+ controls + enhanced monitoring) |

**FedRAMP Authorization Paths**:
| Path | Description | Timeline | Cost |
|------|-------------|----------|------|
| JAD (Joint Authorization Board) | Provisional Authorization by JAB | 12-18 months | $1-6M |
| Agency ATO | Authorization by federal agency | 6-12 months | $500K-2M |
| CSP Supplied | Same as JAD but CSP manages process | 12-24 months | $1-10M |

**FedRAMP Cloud Deployment Requirements**:
- Federal-only datacenters (AWS GovCloud, Azure Government, GCP GovCloud)
- US citizens only for system administration
- Continuous monitoring (automated scanning, SIEM, incident response)
- Annual assessment by independent 3PAO
- Penetration testing
- Incident response within 1 hour (high) / 24 hours (low)
- Data residency: US only
- System boundary documentation

### 67.2 GovCloud and IL Levels

**AWS GovCloud/US Regions**:
| Region | IL Level | Use Case |
|--------|----------|----------|
| us-gov-west-1 | IL2-IL5 | DoD, civilian agencies |
| us-gov-east-1 | IL2-IL5 | DoD, civilian agencies |
| AWS Secret Region | IL6 | Classified workloads (by request) |
| AWS Top Secret Region | TS/SCI | Classified (by request) |

**Azure Government**:
| Region | Compliance | Use Case |
|--------|------------|----------|
| USGov Arizona | FedRAMP High, DoD IL5 | Department of Defense |
| USGov Texas | FedRAMP High, DoD IL5 | Civilian agencies |
| USGov Virginia | FedRAMP High, DoD IL5 | Mixed government |
| Azure Government Secret | Classified | National security |
| Azure Government Top Secret | Classified | Intelligence community |

**GCP Government Regions**:
- Council Bluffs, Iowa | FedRAMP High | Civilian agencies
- Salt Lake City, Utah | FedRAMP High | DoD, IC
- Reston, Virginia | FedRAMP High | Civilian agencies
- Assured Workloads for regulated workloads

### 67.3 CMMC

**CMMC 2.0 Levels**:
| Level | Name | Practices | Assessment |
|-------|------|-----------|------------|
| Level 1 | Foundational | 17 basic practices (FCI protection) | Self-assessment, annual affirmation |
| Level 2 | Advanced | 110 practices (NIST SP 800-171) | Third-party assessment every 3 years |
| Level 3 | Expert | 110+ practices + 20+ enhanced | Government-led assessment every 3 years |

**CMMC Cloud Requirements**:
- CUI data in FedRAMP Moderate/High authorized cloud
- Cloud provider FedRAMP authorization required
- CSP must encrypt CUI at rest and in transit
- Multi-factor authentication for CUI access
- Cloud audit logs retained per CMMC requirements
- Incident reporting to DoD (72 hours)

---

## 68. Cloud Security Metrics, KPIs, and Reporting

### 68.1 Security Metrics Framework

**Metric Categories**:
| Category | Examples | Audience |
|----------|----------|----------|
| Operational | Time to detect, time to respond, tickets by severity | SOC team, IR team |
| Compliance | Control pass rate, overdue remediations, audit findings | Compliance team, auditors |
| Risk | Risk score, open vulnerabilities by severity, CVSS distribution | CISO, risk committee |
| Financial | Cost of incidents, security spend as % of IT, budget utilization | CFO, CISO |
| Performance | Security automation rate, false positive rate, SLA adherence | Security management |
| Coverage | Asset coverage (% monitored), patch coverage, MFA adoption | Architecture team |

**Leading vs Lagging Indicators**:
| Type | Description | Example |
|------|-------------|---------|
| Leading | Predict future state (proactive) | % of IaC scanned before deployment |
| Lagging | Measure past state (reactive) | Number of security incidents |
| Operational | Current state (real-time) | Open critical vulnerabilities |
| Compliance | Pass/fail against standard | PCI DSS control pass rate |

**Security KPIs by Cloud Provider**:

**AWS Security Hub KPIs**:
```python
# Security Hub score
aws securityhub get-findings --filters '{"ComplianceStatus": [{"Value": "PASSED"}]}' 
aws securityhub get-findings --filters '{"ComplianceStatus": [{"Value": "FAILED"}]}'
# KPI: % passed = PASSED / (PASSED + FAILED)

# GuardDuty findings by severity
aws guardduty get-findings-statistics --detector-id DETECTOR_ID \
  --finding-statistic-types FindingStatisticType=COUNT_BY_SEVERITY

# IAM credential age
# KPI: % of access keys >90 days old
# KPI: % of users with MFA enabled

# S3 public bucket count
aws s3api list-buckets --query 'Buckets[*].Name' | xargs -I {} \
  aws s3api get-public-access-block --bucket {} 2>/dev/null
# KPI: # of buckets without Block Public Access

# EC2 EBS encryption % 
# KPI: % of EBS volumes encrypted

# CloudTrail enabled in all regions
# KPI: # of regions with CloudTrail (should equal all)
```

**Azure Secure Score KPIs**:
```powershell
# Get Secure Score
az security secure-scores list --query "[].{name:name, score:current, max:max}"
# KPI: Secure Score %
# KPI: By control category (identity, network, storage, etc.)

# Get regulatory compliance status
az security regulatory-compliance-standards list
# KPI: % of controls passed per standard

# Get Defender for Cloud recommendations
az security recommendation list
# KPI: # of critical recommendations, % remediated
```

**GCP SCC KPI**:
```bash
# Security Command Center findings count
gcloud scc findings list --organization=ORG_ID --category="PUBLIC_BUCKET_ACL"
# KPI: # of public buckets

# CVE count by severity
gcloud scc findings list --organization=ORG_ID --source=SOURCE_ID
# KPI: # of critical/high/medium/low vulnerabilities

# Compliance score
gcloud scc compliance-snapshots list --organization=ORG_ID
# KPI: % compliance against CIS, PCI, NIST
```

### 68.2 Security Dashboard Design

**CISO Dashboard (Executive Level)**:
```
┌─────────────────────────────────────────────────────────────────────┐
│ CLOUD SECURITY DASHBOARD — EXECUTIVE SUMMARY                       │
│ Month: June 2026                                       Score: 82% ↑│
├─────────────────────────────────────────────────────────────────────┤
│ [Score Trend]                        [Open Findings by Severity]    │
│  85% ┤███                                Critical:  12 ↓           │
│  82% ┤██████        ██                  High:       45 ↓           │
│  78% ┤██████████ ████                  Medium:     156 ↑           │
│  75% ┤██████████████                   Low:        423 →           │
│       Jan Feb Mar Apr May Jun                                       │
├─────────────────────────────────────────────────────────────────────┤
│ Security Controls Coverage:                                         │
│  IAM MFA:    95% ██████████▒  │  Encryption:    99% █████████████  │
│  Patching:   88% █████████▒   │  Logging:       92% ██████████▒    │
│  Vuln Scan:  91% █████████▒   │  Backup:        87% █████████▒    │
├─────────────────────────────────────────────────────────────────────┤
│ Top Risks:               │  Compliance Status:                      │
│  • Public S3 buckets: 3  │  SOC 2:    ○ 92%    PCI DSS: ○ 96%     │
│  • Unpatched critical: 5 │  HIPAA:    ● 100%   FedRAMP: ● 100%     │
│  • Open IAM roles: 12   │  ISO 27001:● 100%                         │
└─────────────────────────────────────────────────────────────────────┘
```

**SOC Dashboard (Operational Level)**:
```
┌─────────────────────────────────────────────────────────────────────┐
│ SECURITY OPERATIONS CENTER — REAL-TIME                             │
├─────────────────────────────────────────────────────────────────────┤
│ Incidents Today: 7 (Critical: 1, High: 2, Med: 4)                  │
│ Mean Time to Detect: 4.2 min    Mean Time to Respond: 12.5 min     │
│ Mean Time to Resolve: 1h 23min                                      │
├─────────────────────────────────────────────────────────────────────┤
│ Active Incidents:           │ Alert Volume (24h):                   │
│  • CRI-001: Crypto mining   │ ████████████████████████  1,234      │
│  • HIG-002: Brute force     │ False Positive Rate: 23%              │
│  • HIG-003: Unusual API     │ Automated Response Rate: 67%          │
├─────────────────────────────────────────────────────────────────────┤
│ Cloud Accounts Monitored: 42                                        │
│ AWS: 18 Azure: 14 GCP: 7 Other: 3                                  │
│ Most Active Account: prod-aws-12345678                               │
└─────────────────────────────────────────────────────────────────────┘
```

### 68.3 Security Reporting Cadence

| Report | Audience | Frequency | Content |
|--------|----------|-----------|---------|
| Daily SOC Report | SOC team | Daily | Incidents, alerts, open tickets, threat intel |
| Weekly Security Ops | Security management | Weekly | Trend analysis, incident review, patching status, IoC updates |
| Monthly CISO Report | CISO, Exec team | Monthly | Metrics, risk posture, compliance status, top incidents |
| Quarterly Board Report | Board of Directors | Quarterly | Strategic risk, security investment, incidents, compliance |
| Annual Report | Board, regulators | Annually | Security program effectiveness, risk assessment, audit results |

**Quarterly Board Report Template**:
```yaml
Section 1: Executive Summary
  - Security posture score (current vs prior)
  - Key achievements (projects completed, certifications)
  - Major incidents (summary, impact, remediation)
  
Section 2: Risk Posture
  - Top 5 risks (with trend: ↑↓→)
  - Risk acceptance items
  - Emerging threats relevant to business
  
Section 3: Compliance Status
  - Compliance scores by framework
  - Audit findings (open, closed, overdue)
  - Regulatory changes affecting program
  
Section 4: Security Operations
  - Incident volume (trend)
  - MTD, MTTD, MTTR (trend)
  - False positive rate
  - Automation rate
  
Section 5: Projects and Budget
  - Major security initiatives (status, timeline)
  - Budget vs actual
  - Resource utilization
  
Section 6: Metrics Dashboard
  - Visual dashboards (screenshots)
  - KPI trend graphs
  - Benchmark comparison (peer group)
```

---

## 69. Cloud Security Awareness and Training Programs

### 69.1 Training Needs by Role

**Role-Based Training Matrix**:
| Role | Cloud Security Topics | Frequency |
|------|----------------------|-----------|
| Executives/Board | Cloud risk landscape, shared responsibility, business impact, compliance | Annually |
| Developers | Secure coding, OWASP Top 10, IaC security, API security, secret management | Quarterly |
| DevOps/Engineers | Container security, CI/CD pipeline security, IaC scanning, K8s security | Quarterly |
| Cloud Architects | Cloud security architecture, zero trust, encryption, network segmentation | Bi-annually |
| IT Operations | IAM, patching, logging, incident response, backup/DR | Quarterly |
| SOC Analysts | Cloud threat detection, SIEM queries, incident response, forensics | Monthly |
| Compliance/Risk | Compliance frameworks (PCI, HIPAA, SOC 2), audit evidence, BCP | Bi-annually |
| All Employees | Phishing awareness, password hygiene, data classification, reporting incidents | Quarterly |

### 69.2 Security Awareness Topics

**Core Awareness Modules**:
1. **Phishing and Social Engineering**: Recognizing phishing emails, spear-phishing, vishing, smishing, deepfake voice/video scams; reporting suspicious communications
2. **Password Hygiene**: Password managers (1Password, Bitwarden); no password reuse; MFA for all accounts; recognizing MFA fatigue attacks
3. **Cloud-Specific Risks**: Shared responsibility (what you protect vs provider); public S3 bucket risks; exposed credentials in code; ephemeral resources
4. **Data Classification**: Public, internal, confidential, restricted; handling PHI/PII/PCI data; data labeling; secure data disposal
5. **Physical Security**: Badge access, tailgating prevention; clean desk policy; device locking; visitor management
6. **Insider Threat**: Malicious and accidental; data exfiltration indicators; reporting suspicious behavior; privilege abuse
7. **Remote Work Security**: VPN usage; endpoint security; home network security; personal device risks; video conference security
8. **Incident Reporting**: What to report (phishing, suspicious activity, lost device); how to report; who to contact; no retaliation

**Cloud-Specific Awareness Scenarios**:
```yaml
Scenario 1: Developer pushes AWS key to GitHub
  - Risk: Anyone can use keys to access cloud resources
  - Do: Immediately rotate keys; revoke compromised keys; scan repo history
  - Prevention: Pre-commit hooks (trufflehog/gitleaks); secret scanning in CI/CD

Scenario 2: Employee receives MFA fatigue attack
  - Risk: Attacker spams MFA push until accepted
  - Do: Deny all MFA pushes; contact security; change password immediately
  - Prevention: Number matching MFA; FIDO2 hardware keys; risk-based conditional access

Scenario 3: Contractor leaves with cloud access
  - Risk: Orphaned IAM user or service account
  - Do: Disable/delete account immediately; check recent activity
  - Prevention: SCIM provisioning (auto-deprovisioning); periodic access reviews

Scenario 4: Accidental S3 public bucket
  - Risk: Data exposed to internet (anyone can list/download)
  - Do: Block public access; assess exposure; notify security
  - Prevention: SCP to block public S3; Config rules with auto-remediation
```

### 69.3 Training Program Implementation

**Training Delivery Methods**:
| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| Instructor-led | Interactive, Q&A, customized | Expensive, scheduling | Developers, architects |
| E-learning | Scalable, trackable, consistent | Less engaging, generic | All employees (baseline) |
| Hands-on lab | Practical skills, engaging | Requires environment, time | Engineers, SOC |
| Tabletop exercise | Team building, practical | Time-intensive | IR team, architects |
| Gamification | Fun, competitive, memorable | May trivialize | All employees |
| Phishing simulation | Real-world, measurable | Can create distrust | All employees |

**Annual Training Schedule**:
| Month | Activity | Audience |
|-------|----------|----------|
| January | Annual cloud security awareness training | All employees |
| February | Phishing simulation round 1 | All employees |
| March | Developer secure coding workshop | Engineering |
| April | SOC cloud incident response training | SOC team |
| May | Tabletop exercise: cloud breach | IR team, architects |
| June | Quarterly security newsletter | All employees |
| July | Phishing simulation round 2 | All employees |
| August | Cloud architect security review | Architecture team |
| September | Compliance training (PCI/HIPAA refresher) | Relevant teams |
| October | Cybersecurity Awareness Month events | All employees |
| November | Phishing simulation round 3 | All employees |
| December | Annual review and planning | Security team |

### 69.4 Measuring Training Effectiveness

**Training Metrics**:
| Metric | Target | Measurement |
|--------|--------|-------------|
| Phishing click rate | <5% | Phishing simulation platform |
| Training completion rate | >95% | LMS reports |
| Secure coding pass rate | >80% | Developer assessment |
| Time to report phishing | <5 min | Report tracking |
| Security question score | >85% | Knowledge assessment |
| Incident reporting rate | >90% of confirmed incidents | Incident tracking |
| Behavior change observation | Positive trend | Spot checks, reviews |

**Continuous Improvement**:
- Review phishing simulation results; adjust scenarios
- Update training content based on new threats and incidents
- Analyze incident root causes for training gaps
- Incorporate lessons learned from breaches and audits
- Refresh training materials annually



---

## 70. Malware Analysis and Classification

### 70.1 Malware Classification

**Malware Types**:
| Type | Description | Cloud Relevance |
|------|-------------|-----------------|
| Virus | Self-replicating code that attaches to files | Can spread through shared drives, cloud sync |
| Worm | Self-replicating across networks | Can propagate through VPC peering, VPN |
| Trojan | Disguised as legitimate software | Supply chain attacks on cloud vendors |
| Ransomware | Encrypts files for ransom | Cloud storage sync can amplify damage |
| Spyware | Steals information | Cloud credential theft, session hijacking |
| Rootkit | Hides OS presence | Difficult to detect in cloud VMs |
| Bootkit | Infects boot process | UEFI/Secure Boot in cloud instances |
| RAT (Remote Access Trojan) | Backdoor access | Persistence on cloud workloads |
| Botnet | Network of compromised machines | Cloud instances used for DDoS, mining |
| Cryptominer | Uses CPU/GPU for crypto mining | Most common cloud workload abuse |
| Ransomware-as-a-Service | Commercialized ransomware | Cloud storage and databases targeted |
| Fileless Malware | In-memory, no disk persistence | Detected by memory forensics in cloud |
| Wiper | Destroys data permanently | Cloud backup as mitigation |
| Loader | Downloads additional malware | Initial payload in cloud attacks |
| Dropper | Installs other malware | Common in cloud supply chain |

### 70.2 Malware Analysis Approaches

**Static Analysis**:
```bash
# File identification
file suspicious_file.exe
strings suspicious_file.exe | head -100
# Obfuscation indicators: Base64, XOR encoding, UPX packing

# Hash analysis
sha256sum suspicious_file.exe
# Search hash in VirusTotal

# PE analysis (Windows)
pecheck suspicious_file.exe  # or exiftool
# Import/Export tables, sections, resources

# Linux ELF analysis
readelf -a suspicious_binary
objdump -d suspicious_binary  # Disassemble

# YARA rule matching
yara -s my_rules.yara suspicious_file
```

**Dynamic Analysis**:
```bash
# Run in isolated sandbox (cloud: isolated VPC, no egress)
# Capture network traffic
tcpdump -i eth0 -w malware-traffic.pcap

# Monitor process creation
strace -f -o malware-syscalls.log ./suspicious_binary
ltrace -o malware-libcalls.log ./suspicious_binary

# Monitor file system changes
inotifywait -m -r /tmp /home

# Monitor registry changes (Windows)
# Procmon, Regshot

# Network analysis: DNS, HTTP, TCP connections
# Detect C2 beacons, data exfiltration

# Memory dump and analysis
# Volatility for memory forensics
```

**Cloud Malware Analysis Environment**:
```yaml
Isolated Analysis Environment:
  AWS:
    - Dedicated VPC in security account
    - No internet gateway; VPC endpoints only
    - EC2 with snapshot capability
    - IMDSv2 enforced (prevents escape)
    - CloudTrail + GuardDuty for monitoring
    - S3 for evidence storage (Object Lock)
  
  Azure:
    - Isolated VNet with no egress
    - Azure Firewall denying all outbound
    - VM with disk encryption
    - Log Analytics for VM monitoring
  
  GCP:
    - VPC-SC perimeter with restricted egress
    - Compute Engine with Shielded VM
    - Cloud Audit Logs for all actions
```

**YARA Rule Examples**:
```yara
rule Detect_CryptoMiner_XMRig {
    meta:
        description = "Detects XMRig cryptocurrency miner"
        author = "Security Team"
        date = "2026-06-27"
    strings:
        $s1 = "XMRig" fullword
        $s2 = "donate.vial" fullword
        $s3 = "cryptonight" fullword
        $s4 = "rx/0" fullword  // RandomX variant
        $s5 = "/xmrig" nocase
    condition:
        3 of them
}

rule Detect_Cloud_Key_Stealer {
    meta:
        description = "Detects cloud credential theft tools"
    strings:
        $aws1 = "AWS_ACCESS_KEY_ID" fullword
        $aws2 = "AWS_SECRET_ACCESS_KEY" fullword
        $aws3 = ".aws/credentials" fullword
        $az1 = "AZURE_CLIENT_ID" fullword
        $az2 = "AZURE_TENANT_ID" fullword
        $gcp1 = "google_application_credentials" nocase
        $gcp2 = ".gcp/credentials" fullword
    condition:
        (3 of ($aws*)) or ($az1 and $az2) or ($gcp1 and $gcp2)
}
```

### 70.3 Ransomware in Cloud

**Ransomware Attack Chain**:
```
Initial Access (phishing, VPN, vulnerability)
    → Credential Theft / Session Hijacking
    → Privilege Escalation (cloud admin role)
    → Lateral Movement (cross-account, cross-service)
    → Data Enumeration (S3 buckets, RDS, file shares)
    → Data Exfiltration (copy to attacker account)
    → Encryption (files, EBS volumes, RDS snapshots)
    → Data Deletion (delete backups, CloudTrail logs)
    → Ransom Note
```

**Ransomware Impact on Cloud**:
| Cloud Resource | Ransomware Attack | Mitigation |
|---------------|-------------------|------------|
| S3 Objects | Encrypt or delete objects | Object Lock (compliance mode), versioning, MFA delete |
| EBS Volumes | Encrypt volume | Snapshots in different account, backup vault |
| RDS Databases | Drop tables, encrypt backups | Automated backups, cross-region snapshots |
| File Shares (EFS/FSx) | Encrypt files | File-level backup, ransomware protection |
| Continuous Backups | Delete backup vaults | Immutable backup vaults, MFA for deletion |
| CloudTrail Logs | Delete to hide tracks | S3 Object Lock on log bucket, separate account |
| IAM Roles | Escalate privileges | SCP preventing role modifications |

**Cloud Ransomware Response Playbook**:
```yaml
Step 1: Immediate Containment
  - Isolate affected resources (apply quarantine SG)
  - Disable IAM keys (if compromised)
  - Rotate all credentials
  - Enable MFA delete on S3 (if not already)
  - Block all outbound traffic from affected account (SCP)

Step 2: Preserve Evidence
  - Snapshot all affected EBS volumes
  - Capture CloudTrail for incident timeframe
  - Copy S3 version history
  - Export VPC Flow Logs
  - Memory dump from affected instances (if possible)

Step 3: Recovery
  - Restore from immutable backups (S3 Object Lock)
  - Launch clean instances from AMIs
  - Restore databases from pre-incident snapshots
  - Validate data integrity before recovery

Step 4: Investigation
  - Determine initial access vector
  - Identify all compromised resources
  - Assess data exfiltration
  - Update security controls to prevent recurrence

Step 5: Notification
  - Internal stakeholders
  - Legal/compliance for regulatory notification
  - Law enforcement (if required)
  - Customers (if PII/data breach)
```

### 70.4 Cloud-Specific Malware

**Cloud Malware Examples**:
| Malware | Target | Behavior |
|---------|--------|----------|
| TeamTNT | AWS/Docker | Crypto mining, Docker escape, credential theft |
| BlackMatter | Cloud storage | Ransomware targeting S3, Azure Blob |
| Kinsing | Docker | Crypto mining, container escape |
| LemonDuck | Multi-platform | Crypto mining, cloud credential theft |
| Rocke/Alibaba Cloud | Linux cloud | Crypto mining on unsecured cloud instances |
| Graboid (DDoS) | Docker | Worm spreads across Docker hosts for DDoS |
| XORDDoS | Linux servers | DDoS via compromised cloud instances |

**Cloud Malware Detection Indicators**:
```yaml
Network Indicators:
  - Outbound traffic to known mining pools (pool.minexmr.com, xmrpool.eu)
  - DNS queries to dynamic DNS domains (duckdns, no-ip)
  - HTTP beaconing at regular intervals (C2)
  - Data egress to unusual regions/accounts
  - SSH/RDP brute force traffic

Host Indicators:
  - Unknown SSH keys in authorized_keys
  - Suspicious cron jobs (/tmp/.cache, /dev/shm)
  - High CPU usage (XMRig, miner processes)
  - Unusual kernel modules (rootkits)
  - Modified system binaries (ls, ps, netstat wrappers)

Cloud API Indicators (GuardDuty/Defender):
  - InstanceCredentialExfoliation (EC2 IAM key used externally)
  - UnauthorizedAccess (API calls from unusual source)
  - Recon (PortProbeUnprotected, unusual API enumeration)
  - Behavior (unusual data transfer patterns)
```

---

## 71. Web Application Security (OWASP Top 10 Deep Dive)

### 71.1 OWASP Top 10 (2021)

**OWASP Top 10 Mapping to Cloud**:
| Rank | Risk | Cloud Context | Cloud Defenses |
|------|------|---------------|----------------|
| A01 | Broken Access Control | IAM misconfiguration, unauthenticated API endpoints | IAM policies, API Gateway auth, WAF rules |
| A02 | Cryptographic Failures | Missing encryption, weak keys, expired TLS | KMS enforcement, Config rules, ACM auto-renewal |
| A03 | Injection | SQLi in RDS, NoSQLi in DynamoDB, command injection in Lambda | WAF SQLi/XSS rules, parameterized queries, input validation |
| A04 | Insecure Design | Lack of security requirements in architecture | Cloud security architecture reviews, threat modeling |
| A05 | Security Misconfiguration | Public S3 buckets, open security groups | CSPM, Config rules, SCP guardrails |
| A06 | Vulnerable Components | Unpatched OS, container images, Lambda layers | Inspector/Trivy scanning, patch management, SBOM |
| A07 | Auth Failures | Weak MFA, session timeout, credential stuffing | FIDO2 keys, Conditional Access, IAM conditions |
| A08 | Data Integrity Failures | Unsigned code, compromised CI/CD | Code signing, Cosign, SBOM, supply chain security |
| A09 | Logging Failures | Missing CloudTrail data events, no SIEM | Enable all logging, SIEM, alerting rules |
| A10 | SSRF | Metadata service abuse | IMDSv2, hop limit 1, VPC endpoints, disable metadata |

### 71.2 SQL Injection in Cloud

**Cloud SQLi Attack Paths**:
```
Attack → Web App (WAF bypass) → SQLi → RDS/Aurora → Data exfiltration via S3/UDF
                                            → RDS snapshot export
                                            → Lambda function invocation
                                            → Secrets Manager access
```

**SQLi Defense in Cloud**:
```python
# Parameterized queries (AWS Lambda + RDS)
import psycopg2
from psycopg2.extras import RealDictCursor

def get_user(user_id):
    conn = psycopg2.connect(os.environ['DB_CONNECTION'])
    # Parameterized query - prevents SQL injection
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        return cur.fetchone()

# WAF SQLi prevention
resource "aws_wafv2_web_acl" "sqli_protection" {
  name  = "sqli-protection"
  scope = "REGIONAL"

  rule {
    name     = "AWS-AWSManagedRulesSQLiRuleSet"
    priority = 0
    override_action {
      none {}
    }
    statement {
      managed_rule_group_statement {
        name        = "AWSManagedRulesSQLiRuleSet"
        vendor_name = "AWS"
      }
    }
    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "SQLiRule"
      sampled_requests_enabled   = true
    }
  }
}
```

### 71.3 XSS and Input Validation

**XSS Types and Cloud Defense**:
| XSS Type | Description | Cloud Mitigation |
|----------|-------------|------------------|
| Reflected XSS | Script in URL/request | WAF XSS rules, input validation |
| Stored XSS | Script in database | Output encoding, CSP headers |
| DOM-based XSS | Client-side script | Subresource Integrity (SRI), CSP |
| Blind XSS | Script to admin pages | Input validation, browser isolation |

**CSP (Content Security Policy) for Cloud Apps**:
```nginx
# CloudFront custom headers for CSP
# Strict CSP configuration:
add_header Content-Security-Policy "
  default-src 'self';
  script-src 'self' 'strict-dynamic' 'nonce-{random}';
  style-src 'self' 'nonce-{random}';
  img-src 'self' data: https://*.cloudfront.net;
  connect-src 'self' https://api.example.com;
  font-src 'self';
  frame-src 'none';
  object-src 'none';
  base-uri 'self';
  form-action 'self';
  frame-ancestors 'none';
  block-all-mixed-content;
  upgrade-insecure-requests;
" always;

# CSP reporting endpoint
add_header Reporting-Endpoints "csp-endpoint=\"https://reporting.example.com/csp\";" always;
```

### 71.4 API Security in Cloud

**API Security Controls**:
| Control | AWS | Azure | GCP |
|---------|-----|-------|-----|
| Authentication | IAM auth, Cognito, API Gateway Lambda authorizer | Azure AD, API Management OAuth 2.0 | Firebase Auth, Apigee OAuth |
| Authorization | IAM resource policies, Lambda authorizer | RBAC, managed identities | IAM, service account |
| Rate Limiting | API Gateway usage plans, WAF rate-based rules | API Management rate limits | Apigee rate limiting, Cloud Armor |
| Input Validation | API Gateway request validation, Lambda authorizer | API Management policies | Apigee, Cloud Endpoints |
| Throttling | API Gateway throttling (account-level + method-level) | API Management policies | Apigee, App Engine throttling |
| Logging | CloudWatch Logs, CloudTrail data events | API Management analytics, Azure Monitor | Cloud Audit Logs, Apigee analytics |
| CORS | Configured per API Gateway | API Management CORS policy | Apigee CORS policy |

**API Gateway Security Configuration (AWS)**:
```yaml
REST API:
  - Auth: AWS_IAM or Cognito or Lambda authorizer
  - API Keys: required for usage plans
  - Request Validation: validate parameters, headers, body
  - Throttling: 10,000 req/s burst; 5,000 sustained
  - WAF: AWSManagedRulesCommonRuleSet
  - Logging: full request/response (CloudWatch)
  - TLS: only TLS 1.2+

HTTP API:
  - Auth: JWT (Cognito, OIDC) or Lambda authorizer
  - CORS: defined per route
  - Throttling: account-level
  - WAF: same as REST API
  - Logging: execution logs (CloudWatch)
```

**OpenAPI Security Schemas**:
```yaml
openapi: 3.0.0
info:
  title: Secure API
  version: 1.0.0
paths:
  /users:
    get:
      security:
        - bearerAuth: []
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: OK
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### 71.5 Insecure Deserialization

**Deserialization Attacks**:
| Language | Library | Risk |
|----------|---------|------|
| Python | pickle | Arbitrary code execution (RCE) |
| Java | ObjectInputStream | RCE (commons-collections, gadget chains) |
| JavaScript | JSON.parse | Low (primitive types only) |
| Ruby | Marshal | RCE |
| PHP | unserialize() | RCE |
| .NET | BinaryFormatter | RCE |

**Cloud-Safe Deserialization**:
```python
# AWS Lambda: Never use pickle() for untrusted data
# Use JSON or schema-validated protobuf instead

# Safe deserialization with validation
import json
from jsonschema import validate, ValidationError

USER_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {"type": "integer", "minimum": 1},
        "email": {"type": "string", "pattern": "^[^@]+@[^@]+\.[^@]+$"},
        "role": {"type": "string", "enum": ["user", "admin", "viewer"]}
    },
    "required": ["user_id", "email"],
    "additionalProperties": False
}

def safe_deserialize(event_body):
    try:
        data = json.loads(event_body)
        validate(instance=data, schema=USER_SCHEMA)
        return data
    except (json.JSONDecodeError, ValidationError):
        raise ValueError("Invalid input")
```

---

## 72. Network Protocols and Security Architecture

### 72.1 Core Network Protocols

**OSI Model to Cloud Services Mapping**:
| Layer | Protocols | Cloud Service Mapping |
|-------|-----------|----------------------|
| 7 - Application | HTTP/HTTPS, DNS, SSH, SMTP, RDP, NTP | ALB, CloudFront, API Gateway, Route53 |
| 6 - Presentation | TLS/SSL, mTLS, SOCKS | ACM, CloudHSM |
| 5 - Session | SOCKS5, SMB, NFS | Systems Manager Session Manager, FSx |
| 4 - Transport | TCP, UDP, SCTP | NLB, GWLB, VPC endpoints |
| 3 - Network | IP (IPv4/IPv6), ICMP, IPSec, VXLAN | VPC, subnets, VPN, Transit Gateway |
| 2 - Data Link | Ethernet, VLAN, MPLS, MAC | Direct Connect, VPC, ENI |
| 1 - Physical | Fiber, Copper, Wireless | Data center, Direct Connect locations |

**TCP/IP Protocol Suite**:
```
Application Layer:
  HTTP/HTTPS (80/443)    DNS (53)          SSH (22)          SMTP (25/587)
  FTP (20/21)            NTP (123)          LDAP (389/636)    RDP (3389)
  MQTT (1883/8883)       WebSocket (80/443) gRPC (443)        QUIC (443)

Transport Layer:
  TCP (connection-oriented, reliable, sequenced)
  UDP (connectionless, fast, loss-tolerant)

Network Layer:
  IPv4 (32-bit) / IPv6 (128-bit)
  ICMP (ping, traceroute)
  IPSec (AH: integrity, ESP: encryption, IKE: key exchange)

Internet Layer:
  ARP (IP→MAC)
  DHCP (IP assignment)
  IGMP (multicast)
```

### 72.2 VPN Technologies

**Cloud VPN Types**:
| VPN Type | Description | Cloud Implementation |
|----------|-------------|---------------------|
| Site-to-Site | Connect on-prem to cloud | AWS VPN, Azure VPN Gateway, GCP Cloud VPN |
| Point-to-Site | Connect individual devices | AWS Client VPN, Azure P2S VPN, GCP SSL VPN |
| Remote Access | End-user VPN | AWS Client VPN, Azure VPN Client |
| Cloud-to-Cloud | Inter-cloud connectivity | Equinix, Megaport, IPSec between clouds |
| SD-WAN | Software-defined WAN | VMware SD-WAN, Fortinet, Cisco Meraki |

**IPSec Configuration**:
```bash
# AWS Site-to-Site VPN (automated via Virtual Private Gateway)
aws ec2 create-vpn-connection \
  --customer-gateway-id cgw-1234 \
  --type ipsec.1 \
  --vpn-gateway-id vgw-5678 \
  --options '{"TunnelOptions": [{"IkeVersions": ["ikev2"], "Phase1DHGroupNumbers": [14,16], "Phase2DHGroupNumbers": [14,16]}]}'

# IKEv2 Parameters:
# Phase 1 (ISAKMP):
#   Encryption: AES-256
#   Hash: SHA-256
#   DH Group: 14 (2048-bit MODP) or 16 (4096-bit MODP)
#   Lifetime: 28800 seconds (8 hours)
# Phase 2 (IPSec):
#   Encryption: AES-256
#   Hash: SHA-256
#   PFS: DH Group 14 or 16
#   Lifetime: 3600 seconds (1 hour)
```

**Zero Trust VPN Alternatives**:
| Solution | Architecture | Cloud Integration |
|----------|-------------|-------------------|
| Cloudflare Zero Trust | Cloudflare as ZTNA gateway | All cloud providers |
| Zscaler Private Access | ZPA as ZTNA proxy | AWS, Azure, GCP |
| Netskope Private Access | Netskope edge | Multi-cloud support |
| Twingate | Software-defined perimeter | AWS, Azure, GCP |
| Tailscale | WireGuard-based mesh | All clouds |

### 72.3 Firewall Architectures

**Cloud Firewall Types**:
| Firewall Type | Layer | AWS | Azure | GCP |
|---------------|-------|-----|-------|-----|
| Stateful Firewall | L3-L4 | Security Groups | NSG (stateless), ASG (stateful) | VPC firewall rules (stateful) |
| Stateless Firewall | L3-L4 | NACLs | NSG | - |
| Web Application Firewall | L7 | WAF | WAF (App Gateway/Front Door) | Cloud Armor |
| Network Firewall | L3-L7 | Network Firewall | Azure Firewall | Cloud Firewall (NGFW) |
| DDoS Protection | L3-L4 | Shield | DDoS Protection | Cloud Armor |

**Defense in Depth - Firewall Stack**:
```
Internet
    │
    ▼
[DDoS Protection]  ← Shield / Azure DDoS / Cloud Armor
    │
    ▼
[CDN/WAF]  ← CloudFront + WAF / Azure Front Door + WAF / GCP Cloud CDN + Armor
    │
    ▼
[ALB/NLB]  ← Application/Network Load Balancer
    │
    ▼
[(Optional) NGFW]  ← Palo Alto / Fortinet / Check Point on EC2/GCP/Azure VM
    │
    ▼
[Security Group/ASG]  ← Instance-level stateful firewall
    │
    ▼
[Instance/Container]
```

### 72.4 Network Segmentation Patterns

**VPC Segmentation Strategies**:
```
Single VPC (Simple):
  ┌─────────────────────────────────────────┐
  │ VPC 10.0.0.0/16                         │
  │  Subnets: public (LB), private (app),   │
  │    database (RDS), reserved (mgmt)      │
  └─────────────────────────────────────────┘

Multi-VPC (Transit Gateway):
  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
  │ Prod │  │ Stag │  │ Dev  │  │ Sec  │  │ Data │
  │ VPC  │  │ VPC  │  │ VPC  │  │ VPC  │  │ VPC  │
  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘  └──┬───┘
      └────────┴──────────┴─────────┴──────────┘
                          │
                  Transit Gateway
                  (central routing, inspection)

Multi-Account (AWS Organizations):
  ┌─────────────────────────────────────────────┐
  │ Management Account                           │
  │  (Organizations, billing, consolidated logs) │
  ├─────────────────────────────────────────────┤
  │ Security Account                             │
  │  (CloudTrail, GuardDuty, Security Hub, SIEM) │
  ├─────────────────────────────────────────────┤
  │ Infrastructure Account                       │
  │  (Transit Gateway, firewalls, VPN, DNS)      │
  ├─────────────────────────────────────────────┤
  │ Workload Accounts (Prod/Staging/Dev)         │
  │  (App, DB, data in isolated VPCs)            │
  └─────────────────────────────────────────────┘
```

---

## 73. Social Engineering and Human Attack Vectors

### 73.1 Social Engineering Attacks

**Social Engineering Types**:
| Attack | Description | Cloud-Specific Variation |
|--------|-------------|-------------------------|
| Phishing | Email-based credential theft | Cloud SSO login page clones |
| Spear Phishing | Targeted phishing (specific person) | Impersonating cloud admin/SOC team |
| Whaling | C-suite targeted phishing | CEO fraud for cloud access credentials |
| Smishing | SMS-based phishing | Fake cloud MFA alerts |
| Vishing | Voice call phishing | IT help desk impersonation for password reset |
| Pretexting | Fictional scenario to gain info | "I'm from AWS support, need to verify account" |
| Baiting | Offering something enticing | USB drives labeled "Cloud Security Audit" |
| Tailgating | Following authorized person | Following employee into cloud data center |
| Quid Pro Quo | Offering service for info | "Free cloud security assessment" |
| Watering Hole | Compromise trusted site | Infect cloud console login page |
| MFA Fatigue | Repeated MFA prompts | Push notification spam until accepted |
| Deepfake | AI-generated voice/video | Fake CISO call to reset cloud admin account |

**Real-World Cloud Social Engineering Incidents**:
```yaml
Uber 2022:
  - Contractor's MFA fatigue → Okta session theft → AWS/GCP access
  - Lesson: Number matching MFA, FIDO2 hardware keys

Twitter 2020:
  - Spear phishing of employees → Credential theft → Admin panel access
  - Bitcoin scam from high-profile accounts
  - Lesson: Admin access requires phishing-resistant MFA

MGM Resorts 2023:
  - Vishing to IT help desk → Password reset → Okta admin access
  - Ransomware, $100M+ losses
  - Lesson: Adversary-in-the-middle (AiTM) phishing kit

LastPass 2022:
  - Developer's personal account compromised → Cloud dev environment access
  - Source code + customer vault backups exfiltrated
  - Lesson: PAM for cloud development, separate prod/dev environments
```

### 73.2 Phishing Detection and Prevention

**Phishing Email Indicators**:
```yaml
Sender Analysis:
  - Spoofed display name (verified via SPF/DKIM/DMARC)
  - Lookalike domains (rnicrosoft.com, amaz0n.com, g00gle.com)
  - Free email for business communication
  - Mismatched Reply-To header

Content Analysis:
  - Urgency/threats ("Your account will be suspended in 24 hours")
  - Requests for credentials, MFA codes, PIN
  - Suspicious links (display text ≠ actual URL)
  - Grammar/spelling errors
  - Unexpected attachments (PDF, DOCM, XLSM, ZIP)
  - Generic salutation ("Dear Customer" instead of name)

Technical Indicators:
  - Missing or failed SPF/DKIM/DMARC authentication
  - Suspicious IP origin
  - Newly registered domain (<30 days)
  - URL shorteners (bit.ly, tinyurl, ow.ly)
  - QR codes (QRishing - QR code phishing)
```

**DMARC Configuration**:
```yaml
# Email authentication for cloud email (SES, WorkMail, Google Workspace)
SPF: "v=spf1 include:amazonses.com include:_spf.google.com ~all"
DKIM: Selector with public key in DNS
DMARC: "v=DMARC1; p=reject; rua=mailto:dmarc-reports@example.com; pct=100"
  - p=none (monitor), p=quarantine, p=reject (best)
  - Weekly DMARC report review
```

**Cloud Phishing Defense**:
```bash
# AWS: SES email receiving with spam/phishing detection
aws ses create-receipt-rule --rule-name "phishing-detect" \
  --recipients @example.com \
  --actions '[{"S3Action":{"BucketName":"inbound-phishing","ObjectKeyPrefix":"emails/"}}]'

# GCP: Safe Browsing + Phishing detection
# Enable Chrome Security on Workspace
# Enable phishing detection in Gmail

# Azure: Exchange Online Protection (EOP) + Defender for Office 365
# Enable Safe Links, Safe Attachments, Anti-Phishing policies
```

### 73.3 Security Awareness and Training Against Social Engineering

**Training Program Elements**:
```yaml
Initial Training (Onboarding):
  - Cloud security basics (shared responsibility)
  - Phishing recognition and reporting
  - Password/passkey management
  - MFA importance and MFA fatigue awareness
  
Phishing Simulation Program:
  - Monthly simulated phishing campaigns
  - Quarterly targeted social engineering
  - Varied attack types (email, SMS, phone, QR)
  - Department-specific scenarios (dev, finance, exec)
  
Continuous Awareness:
  - Security newsletter (monthly cloud security tips)
  - Digital signage in office (current threats)
  - Slack/Teams #security-alerts channel
  - Annual mandatory security training
  - Incident post-mortems shared (anonymized)
  
Reporting Culture:
  - One-click phishing report button (email client plugin)
  - No-blame culture for reported incidents
  - Positive reinforcement (recognition, not punishment)
  - Rapid feedback on reported phish (phish or safe?)
```

**Phishing Response Playbook**:
```yaml
User Reports Suspicious Email:
  1. User clicks "Report Phishing" button
  2. Email forwarded to security@company.com automatically
  3. Automated analysis:
     a. Check if other users received same email
     b. Scan URL/attachment in sandbox
     c. Check domain reputation
     d. DMARC/SPF/DKIM verification
  4. If confirmed phishing:
     a. Remove from all inboxes (admin delete)
     b. Block sender domain at email gateway
     c. Block URLs in proxy/WAF
     d. Check if any users clicked/entered credentials
  5. If credentials compromised:
     a. Force password reset
     b. Revoke all sessions/tokens
     c. Check for cloud account access
     d. Monitor for suspicious activity (24h)
  6. Notify affected users + report to management
```

---

## 74. Business Continuity and Disaster Recovery (BCM/DR)

### 74.1 BCM Lifecycle

**BCM Phases**:
```
Program Management → Risk Assessment → Business Impact Analysis → Strategy → Plan → Testing → Maintenance → Culture
```

**Business Impact Analysis (BIA)**:
```yaml
Criticality Scoring:
  - Finance impact ($/hour)
  - Reputation impact (customer trust)
  - Regulatory impact (fines, legal)
  - Operational impact (productivity)

Recovery Objectives:
  - RTO (Recovery Time Objective): Max acceptable downtime
  - RPO (Recovery Point Objective): Max acceptable data loss
  - MTO (Maximum Tolerable Outage): Business survival limit

BIA Output:
  Process Name | Criticality | RTO | RPO | MTO | Dependency | Owner
  Payment Processing | Critical | 15 min | 1 min | 2 hours | RDS, EC2, SQS | Payments Team
  Customer Portal | High | 1 hour | 15 min | 4 hours | ALB, ECS, RDS | Web Team
  Reporting | Medium | 4 hours | 1 hour | 24 hours | Redshift, S3 | Analytics Team
  Internal Email | Low | 24 hours | N/A | 72 hours | WorkMail | IT Team
```

### 74.2 Cloud DR Strategies (Detailed)

**Cloud DR Tiers**:
| Tier | Description | RTO | RPO | Cost (% of Prod) |
|------|-------------|-----|-----|-----------------|
| Tier 0 | No DR (single region, single AZ) | Days-Weeks | Hours | 100% |
| Tier 1 | Backup & Restore (backup + restore in DR) | 4-24 hours | 1-24 hours | 100-110% |
| Tier 2 | Pilot Light (core services in DR, scale on failover) | 15-60 min | 1-5 min | 110-130% |
| Tier 3 | Warm Standby (reduced DR environment) | 5-15 min | 1-5 min | 140-160% |
| Tier 4 | Multi-Site Active-Active (full, both regions live) | Near-zero | <1 sec | 200%+ |

**AWS DR Implementation by Tier**:
```yaml
Tier 1 - Backup & Restore:
  RDS: Automated daily snapshots to DR region
  EC2: AMI replication (cross-region)
  S3: CRR (Cross-Region Replication)
  EFS: EFS Replication
  
Tier 2 - Pilot Light:
  RDS: Cross-region read replica
  Route53: Health check + failover DNS
  Core VPC: Replicated in DR (CloudFormation)
  No app servers running in DR (AMIs ready)
  On failover: Launch EC2 from AMI, point DNS
  
Tier 3 - Warm Standby:
  RDS: Cross-region read replica (promotable)
  EC2: Auto Scaling group, min=1 in DR
  ALB: Deployed in DR with target group
  Route53: Active-passive routing
  On failover: Scale up ASG, fail DNS
  
Tier 4 - Active-Active:
  Aurora Global Database (1 sec RPO)
  DynamoDB Global Tables
  S3 CRR + S3 Batch Replication
  Route53: Latency-based routing
  User sessions: ElastiCache Global Datastore
```

### 74.3 Testing Methodologies

**DR Testing Types**:
| Test Type | Description | Scope | Frequency |
|-----------|-------------|-------|-----------|
| Walkthrough | Review plan verbally | Entire plan | Quarterly |
| Tabletop | Team discussion of scenario | Specific scenario | Semi-annual |
| Component Test | Test individual component | Single service | Monthly |
| Parallel Test | Non-production failover | Full stack in staging | Semi-annual |
| Full Interruption | Production traffic failover | Production | Annual |

**DR Test Report Template**:
```yaml
DR Test Report: June 2026
Test Type: Full Interruption (Production Failover)
Scenario: us-east-1 region failure (complete outage)
Date: 2026-06-15 14:00-18:00 UTC

Objectives:
  - Fail over customer portal from us-east-1 to us-west-2
  - RTO < 15 minutes (actual: 12 min) ✓
  - RPO < 1 minute (actual: 30 sec) ✓
  - Verify all security controls active in DR region ✓

Failover Sequence:
  ┌───────────────┬───────────────────────┬───────────┬──────────┐
  │ Step          │ Action                │ Duration  │ Status   │
  ├───────────────┼───────────────────────┼───────────┼──────────┤
  │ 1             │ Declare DR event      │ 1 minute  │ ✓        │
  │ 2             │ Promote RDS replica   │ 3 minutes │ ✓        │
  │ 3             │ Scale up ASG in DR    │ 5 minutes │ ✓        │
  │ 4             │ Fail Route53 DNS      │ 2 minutes │ ✓        │
  │ 5             │ Verify app function   │ 1 minute  │ ✓        │
  └───────────────┴───────────────────────┴───────────┴──────────┘

Failback Sequence:
  ┌───────────────┬───────────────────────┬───────────┬──────────┐
  │ Step          │ Action                │ Duration  │ Status   │
  ├───────────────┼───────────────────────┼───────────┼──────────┤
  │ 1             │ Establish sync DR→PR  │ 10 min    │ ✓        │
  │ 2             │ Sync data back        │ 15 min    │ ✓        │
  │ 3             │ Fail back Route53     │ 2 min     │ ✓        │
  │ 4             │ Verify app in PR      │ 5 min     │ ✓        │
  │ 5             │ Clean up DR temp      │ 5 min     │ ✓        │
  └───────────────┴───────────────────────┴───────────┴──────────┘

Security Controls Validated in DR:
  - CloudTrail: ✓ (multi-region trail covering DR)
  - GuardDuty: ✓ (activated in DR)
  - Security Hub: ✓ (cross-region aggregator)
  - KMS MRK: ✓ (promoted successfully)
  - WAF Rules: ✓ (deployed via Terraform)
  - SIEM: ✓ (receiving DR logs)
  - IAM: ✓ (global, no changes needed)
  
Issues Found:
  - Secrets Manager replicas not refreshed (expired)
  - IAM role trust policy referenced wrong account ID
  - GuardDuty finding export to SIEM delayed by 5 minutes
  
Remediations:
  - Automate Secrets Manager replication in DR runbook
  - Use IaC for IAM role trust policies (parameterize account ID)
  - Tune GuardDuty → SIEM integration for DR region
```

---

## 75. Cloud Security Labs, CTF, and Practical Exercises

### 75.1 Cloud Security Training Platforms

| Platform | Focus | Cost | Cloud Coverage |
|----------|-------|------|----------------|
| TryHackMe | General cybersecurity + cloud rooms | Free/Paid | AWS, cloud intro rooms |
| HackTheBox | Penetration testing labs | Free/Paid | Cloud challenges, AWS, K8s |
| PwnedLabs | Cloud-specific CTF | Paid | AWS, Azure, GCP challenges |
| Cloud Fox | AWS-focused security labs | Paid | AWS-only |
| AWS Workshop | Official AWS security labs | Free | AWS |
| Azure Labs | Microsoft official labs | Free | Azure |
| GCP Labs | Google Cloud Skills Boost | Free/Paid | GCP |
| Flaws.cloud | AWS CTF (by Scott Piper) | Free | AWS |
| Flaws2 | Advanced AWS CTF | Free | AWS |
| Rhino Security Labs | Cloud penetration testing | Paid | AWS, Azure, GCP |
| Bishop Fox Cloud Labs | Cloud security testing | Free/Paid | Multi-cloud |
| Immersive Labs | Enterprise cyber range | Paid | AWS, Azure |

### 75.2 Cloud CTF Walkthroughs

**Flaws.cloud CTF (Level 1)**:
```bash
# Level 1: Find a public S3 bucket
# Hint: bucket name is flaws.cloud
aws s3 ls s3://flaws.cloud --no-sign-request
# Result: lists files in public bucket
# Download and read the hint file for next level

# Mitigation: Enable S3 Block Public Access
# Lesson: S3 buckets should not be public
```

**CloudFox Lab: IAM Privilege Escalation**:
```bash
# Step 1: Enumerate current permissions
aws sts get-caller-identity
aws iam get-user
aws iam list-attached-user-policies --user-name attacker

# Step 2: Find privilege escalation paths
# Using CloudFox:
cloudfox aws -p TARGET_PROD enum

# Step 3: Exploit IAM passrole + ec2
aws iam list-roles | grep admin
aws ec2 run-instances --image-id ami-12345678 \
  --iam-instance-profile Name=AdminRole \
  --instance-type t2.micro \
  --subnet-id subnet-12345678

# Step 4: Use IMDS to get admin credentials
curl http://169.254.169.254/latest/meta-data/iam/security-credentials/AdminRole

# Mitigation:
# - IMDSv2 with hop limit 1
# - SCP blocking ec2:PassRole unless specific conditions
```

### 75.3 Cloud Security Hands-On Exercises

**Exercise 1: IAM Least Privilege Audit**
```bash
# Task: Identify and remediate over-permissive IAM policies
# 1. Find policies with wildcard actions
aws iam list-policies --scope Local --only-attached \
  --query 'Policies[*].Arn' | xargs -I {} aws iam get-policy-version \
  --policy-arn {} --version-id v1 --query 'PolicyVersion.Document'

# 2. Use IAM Access Analyzer to generate least privilege policy
aws accessanalyzer create-analyzer --analyzer-name "least-privilege"
aws accessanalyzer start-policy-generation \
  --policy-generation-details '{"PrincipalArn":"arn:aws:iam::123456789012:user/test-user"}'

# 3. Apply least privilege policy
aws iam put-user-policy --user-name test-user \
  --policy-name RestrictivePolicy \
  --policy-document file://least-privilege-policy.json
```

**Exercise 2: Build a Secure 3-Tier Architecture**
```hcl
# Terraform: Build and verify a secure 3-tier app
# Implement the following controls:
# 1. VPC with public/private/database subnets
# 2. Security groups per tier (least access)
# 3. RDS encrypted with KMS
# 4. S3 with Block Public Access
# 5. CloudTrail enabled
# 6. GuardDuty enabled

# Verify with:
terraform plan -out=tfplan
terraform show -json tfplan | checkov -f -

# Expected results:
# - No public EC2 instances
# - RDS in private subnet
# - Encryption enabled
# - Logging enabled
# - Backup configured
```

**Exercise 3: Incident Response Simulation**
```bash
# Scenario: GuardDuty alerts on compromised IAM key
# 1. Investigate finding
aws guardduty list-findings --detector-id DETECTOR_ID

# 2. Get finding details
aws guardduty get-findings --detector-id DETECTOR_ID \
  --finding-ids FINDING_ID

# 3. Look up CloudTrail events for the IAM user
aws cloudtrail lookup-events --lookup-attributes \
  AttributeKey=UserName,AttributeValue=compromised-user

# 4. Contain: Disable keys
aws iam update-access-key \
  --access-key-id AKIA1234567890 --status Inactive \
  --user-name compromised-user

# 5. Contain: Detach policies
aws iam detach-user-policy \
  --user-name compromised-user \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess

# 6. Investigate: Check S3 access logs, VPC Flow Logs
# 7. Remediate: Rotate keys, implement IAM conditions, enable MFA
```

**Exercise 4: Container Security Audit**
```bash
# 1. Scan container images
trivy image myapp:latest --severity CRITICAL,HIGH

# 2. Run kube-bench (CIS benchmark)
kubectl apply -f job-bench.yaml
kubectl logs job-bench

# 3. Check K8s RBAC
kubectl auth can-i --list --as=system:serviceaccount:default:mysa

# 4. Review pod security
kubectl get pod mypod -o yaml | grep -A5 securityContext

# 5. Check network policies
kubectl get networkpolicies --all-namespaces

# 6. Verify container runtime security
# Check if seccomp/apparmor profiles applied
# Check if containers run as non-root
```

### 75.4 Cloud Security Certification Study Paths

**CCSP Study Path**:
```yaml
Domain 1: Cloud Concepts, Architecture and Design (17%)
  Focus: Cloud service/deployment models, design principles, cryptography
  Tools: CSA guidance, NIST SP 500-291, CCSP CBK

Domain 2: Cloud Data Security (20%)
  Focus: Data lifecycle, classification, encryption, key management
  Tools: KMS, CloudHSM, Macie, S3 Object Lock

Domain 3: Cloud Platform and Infrastructure Security (17%)
  Focus: Virtualization, container, network, DR/BCP
  Tools: EC2, EKS, VPC, Transit Gateway, Backup

Domain 4: Cloud Application Security (17%)
  Focus: SDLC, secure development, IAM, identity federation
  Tools: CodePipeline, IAM, Cognito, AWS WAF

Domain 5: Cloud Security Operations (16%)
  Focus: Incident response, logging, monitoring, compliance, forensic
  Tools: CloudTrail, GuardDuty, Security Hub, SIEM

Domain 6: Legal, Risk, and Compliance (13%)
  Focus: Regulations, e-discovery, audit, contract, BCP
  Tools: Artifact, Audit Manager, Config

Exam Tips:
  - Understand shared responsibility model (memorize per service model)
  - Know cloud deployment models + differences
  - Data lifecycle stages (create, store, use, share, archive, destroy)
  - Key management differences (CMK, AWS managed, CSEK, etc.)
  - Incident response lifecycle vs cloud IR specifics
  - Legal aspects: eDiscovery, chain of custody, data residency
```

**AWS Security Specialty (SCS-C02) Study Path**:
```yaml
Domain 1: Incident Response (14%)
  - Deep dive: GuardDuty, Security Hub, Detective, Lambda auto-remediation
  - CloudTrail analysis, forensic acquisition
  
Domain 2: Logging and Monitoring (18%)
  - CloudTrail, CloudWatch, Config, VPC Flow Logs
  - SIEM integration, alerting, metric filters
  
Domain 3: Infrastructure Security (20%)
  - VPC design, SG, NACL, WAF, Shield, VPN, Direct Connect
  - Network segmentation, inspection VPC
  
Domain 4: Identity and Access Management (16%)
  - IAM policies, SCP, permissions boundaries, IAM Identity Center
  - SAML/OIDC federation, Cognito, STS
  
Domain 5: Data Protection (18%)
  - S3 security, KMS, CloudHSM, Macie, S3 Object Lock
  - Data classification, DLP, encryption strategies
  
Domain 6: Management and Security Governance (14%)
  - Organizations, Config, Service Catalog, Systems Manager
  - Tag strategy, backup, Trusted Advisor
```



---

## 76. Cloud Security Automation with Python and SDKs

### 76.1 Python Boto3 Security Automation

**IAM Automation**:
```python
import boto3
import json
from datetime import datetime, timedelta

# Auto-rotate IAM access keys older than 90 days
def rotate_old_keys(max_age_days=90):
    iam = boto3.client('iam')
    users = iam.list_users()['Users']
    rotated = []
    
    for user in users:
        keys = iam.list_access_keys(UserName=user['UserName'])['AccessKeyMetadata']
        for key in keys:
            age = (datetime.now() - key['CreateDate'].replace(tzinfo=None)).days
            if age > max_age_days:
                # Create new key
                new_key = iam.create_access_key(UserName=user['UserName'])
                # Disable old key
                iam.update_access_key(
                    UserName=user['UserName'],
                    AccessKeyId=key['AccessKeyId'],
                    Status='Inactive'
                )
                # Note: Store new key in Secrets Manager
                rotated.append({
                    'user': user['UserName'],
                    'old_key': key['AccessKeyId'],
                    'new_key': new_key['AccessKey']['AccessKeyId']
                })
    return rotated

# Identify unattached IAM policies
def cleanup_unused_policies():
    iam = boto3.client('iam')
    policies = iam.list_policies(Scope='Local', OnlyAttached=False)['Policies']
    deleted = []
    
    for policy in policies:
        # Skip if last attached version < 30 days
        versions = iam.list_policy_versions(PolicyArn=policy['Arn'])['Versions']
        if len(versions) > 5:  # Max versions, clean up old
            for v in versions[:-5]:
                iam.delete_policy_version(
                    PolicyArn=policy['Arn'],
                    VersionId=v['VersionId']
                )
                deleted.append(f"Deleted version {v['VersionId']} of {policy['PolicyName']}")
    return deleted

# Enforce MFA on all users
def enforce_mfa_compliance():
    iam = boto3.client('iam')
    users = iam.list_users()['Users']
    non_compliant = []
    
    for user in users:
        # Check if user has virtual MFA device
        mfa_devices = iam.list_virtual_mfa_devices(
            AssignmentStatus='Assigned'
        )['VirtualMFADevices']
        
        user_has_mfa = any(
            mfa['User']['UserName'] == user['UserName'] 
            for mfa in mfa_devices
        )
        
        if not user_has_mfa:
            non_compliant.append(user['UserName'])
    
    return non_compliant
```

**S3 Security Automation**:
```python
# Enforce S3 Block Public Access across all buckets
def enforce_s3_block_public_access(account_id):
    s3 = boto3.client('s3')
    s3control = boto3.client('s3control')
    
    # Account-level Block Public Access
    s3control.put_public_access_block(
        AccountId=account_id,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        }
    )
    
    # Bucket-level: Deny public access via bucket policy
    buckets = s3.list_buckets()['Buckets']
    for bucket in buckets:
        try:
            s3.put_public_access_block(
                Bucket=bucket['Name'],
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                }
            )
        except Exception as e:
            print(f"Failed on {bucket['Name']}: {e}")

# Enforce SSE-KMS on all S3 buckets
def enforce_s3_encryption():
    s3 = boto3.client('s3')
    buckets = s3.list_buckets()['Buckets']
    
    for bucket in buckets:
        try:
            # Get current encryption
            encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
        except:
            # No encryption configured - add default
            s3.put_bucket_encryption(
                Bucket=bucket['Name'],
                ServerSideEncryptionConfiguration={
                    'Rules': [{
                        'ApplyServerSideEncryptionByDefault': {
                            'SSEAlgorithm': 'aws:kms',
                            'KMSMasterKeyID': 'alias/aws/s3'
                        }
                    }]
                }
            )

# Enable S3 versioning and Object Lock on critical buckets
def enable_versioning_and_lock(bucket_name, retention_days=365):
    s3 = boto3.client('s3')
    
    # Enable versioning
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    
    # Enable Object Lock (compliance mode)
    s3.put_object_lock_configuration(
        Bucket=bucket_name,
        ObjectLockConfiguration={
            'ObjectLockEnabled': 'Enabled',
            'Rule': {
                'DefaultRetention': {
                    'Mode': 'COMPLIANCE',
                    'Days': retention_days
                }
            }
        }
    )
```

**Security Group Audit Automation**:
```python
# Find overly permissive security groups (0.0.0.0/0 on sensitive ports)
def find_permissive_sgs():
    ec2 = boto3.client('ec2')
    sgs = ec2.describe_security_groups()['SecurityGroups']
    risky_sgs = []
    
    SENSITIVE_PORTS = [22, 3389, 3306, 5432, 6379, 27017, 9200, 8080]
    
    for sg in sgs:
        for rule in sg['IpPermissions']:
            from_port = rule.get('FromPort', 0)
            to_port = rule.get('ToPort', 65535)
            
            for ip_range in rule.get('IpRanges', []):
                if ip_range['CidrIp'] == '0.0.0.0/0' or ip_range['CidrIp'] == '::/0':
                    # Check if sensitive port is exposed
                    if from_port in SENSITIVE_PORTS or to_port in SENSITIVE_PORTS:
                        risky_sgs.append({
                            'sg_id': sg['GroupId'],
                            'sg_name': sg['GroupName'],
                            'port': f"{from_port}-{to_port}",
                            'protocol': rule['IpProtocol'],
                            'exposed_to': ip_range['CidrIp']
                        })
    return risky_sgs

# Auto-remediate: Remove 0.0.0.0/0 ingress on port 22
def remediate_open_ssh():
    ec2 = boto3.client('ec2')
    sgs = ec2.describe_security_groups()['SecurityGroups']
    remediated = []
    
    for sg in sgs:
        for rule in sg['IpPermissions']:
            if rule.get('FromPort') == 22:
                for ip_range in list(rule.get('IpRanges', [])):
                    if ip_range['CidrIp'] == '0.0.0.0/0':
                        ec2.revoke_security_group_ingress(
                            GroupId=sg['GroupId'],
                            IpPermissions=[{
                                'IpProtocol': rule['IpProtocol'],
                                'FromPort': rule['FromPort'],
                                'ToPort': rule['ToPort'],
                                'IpRanges': [ip_range]
                            }]
                        )
                        remediated.append(sg['GroupId'])
    return remediated
```

### 76.2 Azure Automation (PowerShell/Azure CLI)

**Azure Security Automation**:
```powershell
# Enforce NSG flow logs on all subnets
$subnets = Get-AzVirtualNetwork | Get-AzVirtualNetworkSubnetConfig
foreach ($subnet in $subnets) {
    $nsg = Get-AzNetworkSecurityGroup -ResourceGroupName $subnet.ResourceGroupName
    if (-not $nsg.FlowLog) {
        Set-AzNetworkWatcherConfigFlowLog -NetworkWatcherName "watcher" `
            -ResourceGroupName "NetworkWatcherRG" `
            -TargetResourceId $nsg.Id `
            -Enabled $true `
            -StorageId $storageAccount.Id `
            -RetentionInDays 365
    }
}

# Auto-remediate: Remove public IP from VMs
$vms = Get-AzVM
foreach ($vm in $vms) {
    $nic = Get-AzNetworkInterface -ResourceId $vm.NetworkProfile.NetworkInterfaces[0].Id
    if ($nic.IpConfigurations.PublicIpAddress.Id) {
        Remove-AzNetworkInterfaceIpConfig -NetworkInterface $nic `
            -Name $nic.IpConfigurations[0].Name
        Set-AzNetworkInterface -NetworkInterface $nic
    }
}

# Enforce MFA on all users (Azure AD)
$users = Get-AzureADUser -All $true
foreach ($user in $users) {
    $mfaStatus = Get-MgUserAuthenticationMethod -UserId $user.Id
    if (-not ($mfaStatus | Where-Object {$_.AdditionalProperties.'@odata.type' -eq "#microsoft.graph.microsoftAuthenticatorAuthenticationMethod"})) {
        # Require MFA registration
        Update-MgUser -UserId $user.Id -OtherMails @($user.OtherMails + "REQUIRE_MFA")
    }
}
```

### 76.3 GCP Automation (gcloud + Python)

**GCP Security Automation**:
```python
from google.cloud import storage, compute_v1, iam_admin_v1
from google.cloud import logging as cloud_logging

# Enforce public access prevention on all buckets
def enforce_public_access_prevention():
    storage_client = storage.Client()
    buckets = list(storage_client.list_buckets())
    
    for bucket in buckets:
        # Get current IAM to check for public access
        policy = bucket.get_iam_policy()
        all_users = policy.bindings.get('roles/storage.objectViewer', [])
        
        if 'allUsers' in all_users or 'allAuthenticatedUsers' in all_users:
            # Remove public access
            policy.bindings['roles/storage.objectViewer'] = [
                b for b in all_users 
                if b not in ['allUsers', 'allAuthenticatedUsers']
            ]
            bucket.set_iam_policy(policy)
            
            # Enable public access prevention
            bucket.public_access_prevention = 'enforced'
            bucket.patch()

# Enforce VPC flow logs on all subnets
def enforce_vpc_flow_logs():
    compute = compute_v1.SubnetworksClient()
    project = 'my-project'
    
    # List all regions
    regions = compute_v1.RegionsClient().list(project=project)
    
    for region in regions:
        subnets = compute.list(project=project, region=region.name)
        for subnet in subnets:
            if not subnet.enable_flow_logs:
                # Enable flow logs
                subnet.enable_flow_logs = True
                subnet.aggregation_interval = 'INTERVAL_5_SEC'
                subnet.flow_sampling = 1.0
                compute.patch(
                    project=project,
                    region=region.name,
                    subnetwork=subnet.name,
                    subnetwork_resource=subnet
                )
```

### 76.4 Event-Driven Security Automation

**AWS EventBridge Security Automations**:
```yaml
Rule: Block public S3 buckets
  EventPattern:
    source: ["aws.s3"]
    detail-type: ["AWS API Call via CloudTrail"]
    detail:
      eventSource: ["s3.amazonaws.com"]
      eventName: ["PutBucketPublicAccessBlock", "PutBucketAcl", "PutBucketPolicy"]
  Target: Lambda function to enforce BlockPublicAccess

Rule: Alert on root activity
  EventPattern:
    source: ["aws.signin"]
    detail-type: ["AWS Console Sign In via CloudTrail"]
    detail:
      userIdentity:
        type: ["Root"]
  Target: SNS topic (PagerDuty + Slack + email)

Rule: Auto-remediate non-encrypted EBS volume
  EventPattern:
    source: ["aws.ec2"]
    detail-type: ["EBS Volume Notification"]
    detail:
      event: ["createVolume"]
      requestParameters:
        encrypted: [false]
  Target: SSM Automation to encrypt volume (copy + replace)

Rule: Quarantine compromised instance
  EventPattern:
    source: ["aws.guardduty"]
    detail-type: ["GuardDuty Finding"]
    detail:
      severity: [8, 9]
      type: ["Backdoor:EC2/C2Activity.B!DNS"]
  Target: StepFunctions workflow
    Actions:
      - Apply quarantine security group
      - Snapshot EBS volume (forensic)
      - Disable IAM role (if EC2 profile)
      - CloudTrail event freeze
      - Notify SOC via PagerDuty
```

**Azure Automation Runbook**:
```powershell
# Azure Automation Runbook: Remediate public storage
param(
    [Parameter(Mandatory=$true)]
    [string]$StorageAccountName,
    
    [Parameter(Mandatory=$true)]
    [string]$ResourceGroupName
)

$storageAccount = Get-AzStorageAccount -ResourceGroupName $ResourceGroupName `
    -Name $StorageAccountName

# Block public access
Set-AzStorageAccount -ResourceGroupName $ResourceGroupName `
    -Name $StorageAccountName `
    -AllowBlobPublicAccess $false

# Enable encryption (if not already)
if (-not $storageAccount.Encryption.Services.Blob.Enabled) {
    Set-AzStorageAccount -ResourceGroupName $ResourceGroupName `
        -Name $StorageAccountName `
        -EnableEncryptionService $true
}

# Enable logging
Set-AzStorageServiceLoggingProperty -ServiceType Blob `
    -LoggingOperations All `
    -RetentionDays 365

# Log remediation
$logEntry = @{
    Timestamp = Get-Date
    Action = "Remediated public storage"
    Resource = $StorageAccountName
    Status = "Completed"
}
Write-Output $logEntry
```

---

## 77. Cloud Security for Additional Industries

### 77.1 Education (FERPA)

**FERPA Cloud Requirements**:
| Requirement | Description | Cloud Implementation |
|-------------|-------------|---------------------|
| Student data protection | Educational records must be protected | Encryption at rest + in transit, access controls |
| Directory information opt-out | Parent can restrict directory info | Data classification, restricted access |
| Parental access rights | Parents can review records | API-based access, self-service portal |
| Third-party service restrictions | Cloud vendors must comply | BAA-type agreement with cloud provider |
| Data deletion | Student records on request | S3 lifecycle, secure deletion |

**Cloud Controls for Education**:
- Separate environments for student vs administrative data
- Role-based access (teacher, student, admin, parent)
- No student data in development/testing environments
- Data retention policies for student records (FERPA requires reasonable retention)
- Incident notification to educational institution within 24 hours
- Background checks for cloud admins with student data access
- Cloud provider FedRAMP or equivalent certification

### 77.2 Energy and Utilities (NERC CIP)

**NERC CIP Cloud Requirements**:
| CIP Standard | Description | Cloud Consideration |
|--------------|-------------|---------------------|
| CIP-002 | Bulk Electric System (BES) cyber asset identification | Cloud assets in BES boundary |
| CIP-003 | Security management controls | Cloud service provider management |
| CIP-004 | Personnel and training | Access management, training |
| CIP-005 | Electronic security perimeter | Cloud network segmentation, firewalls |
| CIP-006 | Physical security of BES assets | Data center physical security |
| CIP-007 | Systems security management | Patch management, malware protection |
| CIP-008 | Incident reporting and response | Cloud incident response plan |
| CIP-009 | Recovery plans | Cloud DR, BCP |
| CIP-010 | Configuration change management | IaC, configuration management |
| CIP-011 | Information protection | Encryption, data classification |
| CIP-012 | Communications between control centers | Encrypted communications, secure VPN |
| CIP-013 | Supply chain risk management | Cloud vendor risk management |
| CIP-014 | Physical security | Critical infrastructure, transmission |

**Cloud Security for Energy**:
- Air-gapped cloud environments for OT/SCADA
- No internet access from industrial control systems
- Cloud SCADA with dedicated connections (Direct Connect / ExpressRoute)
- Real-time monitoring with cloud-based analytics
- IoT security for smart grid devices
- Compliance with regional grid operator requirements (ISO, RTO)

### 77.3 Legal and E-Discovery

**Cloud E-Discovery Considerations**:
| Phase | Cloud Consideration |
|-------|---------------------|
| Identification | Know where data is stored (regions, accounts, services) |
| Preservation | Legal hold on cloud resources (S3 Object Lock, Azure Immutable Blob) |
| Collection | API-based collection tools; SPOF for cloud data |
| Processing | Cloud-native format processing (JSON log files, database dumps) |
| Review | Web-based review platforms hosted in cloud |
| Production | Direct cloud-to-cloud production |

**Legal Hold Implementation in Cloud**:
```yaml
AWS:
  - S3 Object Lock (compliance mode) on relevant buckets
  - Cannot be removed or shortened during compliance period
  - Legal hold tag on individual objects
  - CloudTrail to audit any hold changes

Azure:
  - Azure Immutable Blob (legal hold policy)
  - Cannot be deleted, overwritten, or modified
  - Time-based retention or indefinite legal hold

GCP:
  - Retention policies on buckets
  - Bucket Lock (makes retention permanent)
  - Object holds on individual objects
```

### 77.4 Gaming and Media

**Cloud Security for Gaming**:
| Area | Security Controls |
|------|-------------------|
| Game Server Security | Anti-cheat, DDoS protection (Shield/GCP Armor/Azure DDoS), rate limiting |
| Player Accounts | MFA, account takeover prevention, fraud detection |
| In-Game Purchases | PCI DSS for payment processing, fraud detection |
| Digital Rights | DRM integration, content encryption, token-based authorization |
| Real-Time Communications | Encryption, moderation, compliance (COPPA for children) |
| User-Generated Content | Content moderation, copyright detection, abuse reporting |

**Media Security (DRM and Watermarking)**:
| Technology | Description | Cloud Service |
|------------|-------------|---------------|
| DRM (Digital Rights Mgmt) | Encrypt content + license key delivery | AWS Media Services, Azure Media Services |
| Forensic Watermarking | Embed unique identifier in content | AWS Elemental,第三方 watermarking |
| Geo-Blocking | Restrict content by region | CloudFront geo-restriction, WAF geo-match |
| Tokenized Access | Time-limited content access | CloudFront signed URLs/cookies |
| Content Encryption | Encrypt at rest and in transit | KMS, S3 SSE-C |
| CDN Security | Edge authentication | CloudFront, Azure CDN, Cloud CDN |
| Content Verification | Integrity checks | Content hashing, digital signatures |

---

## 78. Cloud Security Reference Architecture Patterns

### 78.1 Microservices Security Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Service Mesh (Istio / App Mesh / Linkerd)                                   │
│  ├── mTLS between all services (mutual authentication)                      │
│  ├── Authorization policies (RBAC per service)                              │
│  ├── Traffic routing (canary, blue/green, fault injection)                   │
│  └── Observability (metrics, tracing, logging)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ API Gateway / Ingress                                                        │
│  ├── Authentication (OIDC / JWT / OAuth 2.0)                                │
│  ├── Rate limiting (per client, per endpoint)                                │
│  ├── Request validation (schema, headers, size)                              │
│  ├── WAF integration (OWASP, bot control, IP reputation)                     │
│  └── API versioning + deprecation                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Service Layer (EKS / ECS / AKS / GKE)                                        │
│  ├── Pod Security Standards (restricted baseline)                            │
│  ├── Security Contexts (non-root, read-only root filesystem)                 │
│  ├── Network Policies (deny-all default, allow-specific)                     │
│  ├── Resource Limits (CPU/memory to prevent DoS)                             │
│  ├── Service Accounts (one per microservice, least privilege)                │
│  └── Image Scanning (vulnerability + secret detection)                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Data Layer                                                                   │
│  ├── Database: Encrypted at rest (KMS/CMEK), audit logging, IAM auth        │
│  ├── Cache: ElastiCache/Memorystore with encryption, VPC, auth token         │
│  ├── Queue: SQS/EventHub/PubSub with KMS, DLQ, access control               │
│  └── Object Store: S3/GCS/Azure Blob with encryption, versioning, lock       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Secrets and Configuration                                                    │
│  ├── Secrets Manager / Key Vault / Secret Manager (auto-rotation)            │
│  ├── Parameter Store / App Config (encrypted parameters)                     │
│  ├── External Secrets Operator (syncs to K8s)                                │
│  └── Vault Agent (sidecar for secret injection)                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Observability                                                                │
│  ├── Distributed Tracing (X-Ray / OpenTelemetry / Jaeger)                   │
│  ├── Metrics (CloudWatch / Prometheus / Datadog)                             │
│  ├── Logging (CloudWatch / ELK / Loki)                                      │
│  └── Alerting (CloudWatch Alarms / PagerDuty / OpsGenie)                     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 78.2 Data Lake Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Data Sources                                                │
│  App Logs    DB CDC    IoT Devices    SaaS APIs   Social     │
└─────────┬──────────┬─────────────┬──────────┬──────────────┘
          │          │             │          │
          ▼          ▼             ▼          ▼
┌─────────────────────────────────────────────────────────────┐
│ Data Ingestion                                              │
│  Kinesis / EventHub / PubSub  (TLS, IAM auth, encrypted)   │
│  → Schema validation → Data classification (PII tagging)    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Raw Zone (S3/GCS/Blob)                                      │
│  - Immutable (Object Lock)                                  │
│  - Encrypted (KMS/CMEK)                                     │
│  - Access: IAM only (no public)                             │
│  - Retention: 7 years (compliance)                           │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Processing Layer (Spark/Glue/EMR/BigQuery)                   │
│  - Encryption in transit (TLS for inter-node)                │
│  - Encryption at rest (KMS for temp storage)                 │
│  - VPC isolation (no internet)                               │
│  - IAM least privilege (per job role)                        │
│  - Data masking (PII/PHI at read time)                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Curated Zone                                                │
│  - Column-level security (S3/Lake Formation)                 │
│  - Row-level security (PII redaction)                        │
│  - Audit logging (all access logged)                         │
│  - Data catalog with classification tags                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Consumption                                                 │
│  Athena / Redshift / BigQuery / Synapse                      │
│  - IAM authentication + VPC endpoints                        │
│  - Query logging + audit                                     │
│  - Result set encryption                                     │
│  - Data masking for sensitive columns                        │
└─────────────────────────────────────────────────────────────┘
```

### 78.3 Multi-Region Active-Active Architecture

```
┌─────────────────────────────┐     ┌─────────────────────────────┐
│ Region: us-east-1           │     │ Region: eu-west-1           │
│                             │     │                             │
│ Route53 (latency-based) ◄───┼─────┼──► Route53 (latency-based)  │
│                             │     │                             │
│ CloudFront + WAF            │     │ CloudFront + WAF            │
│     │                       │     │     │                       │
│     ▼                       │     │     ▼                       │
│ ALB (active)                │     │ ALB (active)                │
│     │                       │     │     │                       │
│     ▼                       │     │     ▼                       │
│ ECS/EKS (app)               │     │ ECS/EKS (app)               │
│     │                       │     │     │                       │
│ ┌───┴──────────┐            │     │ ┌───┴──────────┐            │
│ │ Session Store│            │     │ │ Session Store│            │
│ │ (Global DB)  │◄───────────┼─────┼─┤ (Global DB)  │            │
│ └──────────────┘            │     │ └──────────────┘            │
│ ┌──────────────┐            │     │ ┌──────────────┐            │
│ │ Aurora Global│◄───────────┼─────┼─┤ Aurora Global│            │
│ │ (primary)    │            │     │ │ (secondary)  │            │
│ └──────────────┘            │     │ └──────────────┘            │
│ ┌──────────────┐            │     │ ┌──────────────┐            │
│ │ DynamoDB     │◄───────────┼─────┼─┤ DynamoDB     │            │
│ │ Global Table │            │     │ │ Global Table │            │
│ └──────────────┘            │     │ └──────────────┘            │
│ ┌──────────────┐            │     │ ┌──────────────┐            │
│ │ S3 CRR       ├───────────►┼─────┼─► S3 (replica) │            │
│ └──────────────┘            │     │ └──────────────┘            │
│                             │     │                             │
│ Security (both regions):    │     │ Security (both regions):    │
│ CloudTrail ✓               │     │ CloudTrail ✓               │
│ GuardDuty ✓                │     │ GuardDuty ✓                │
│ KMS MRK ✓                  │     │ KMS MRK ✓                  │
│ WAF ✓                      │     │ WAF ✓                      │
│ Config ✓                   │     │ Config ✓                   │
└─────────────────────────────┘     └─────────────────────────────┘
```

### 78.4 Serverless Data Processing Architecture

```
Event Source (S3 / SQS / API GW / EventBridge / DynamoDB Streams)
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ Event Validation Layer                                          │
│  - Schema validation (JSON Schema, Avro, Protobuf)               │
│  - PII detection and redaction                                   │
│  - Input sanitization (prevent injection)                        │
│  - Rate limiting (reserved concurrency, throttling)              │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    ┌──────┴──────┐
                    ▼             ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Lambda Function │  │ Step Functions   │
          │ (data transform)│  │ (orchestration)  │
          │ - IAM least     │  │ - Error handling │
          │ - KMS env vars  │  │ - DLQ           │
          │ - VPC (if DB)   │  │ - Retry logic   │
          │ - 15 min max    │  │ - Audit trail   │
          └────────┬────────┘  └────────┬────────┘
                   │                    │
                   ▼                    ▼
          ┌──────────────────────────────────────┐
          │ State Store                           │
          │  - S3 (encrypted, versioned)          │
          │  - DynamoDB (KMS encrypted)           │
          │  - RDS Proxy (connection pooling)     │
          └──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────────┐
│ Output / Notification                                           │
│  - SNS / EventBridge → downstream consumers                     │
│  - SQS (DLQ for failures)                                      │
│  - CloudWatch Metrics + Logs                                   │
│  - X-Ray tracing                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 79. Cloud Security FAQ (Comprehensive)

### 79.1 General Cloud Security

**Q: What is the shared responsibility model?**
A: The provider secures security OF the cloud (physical infrastructure, hypervisor, network). The customer secures security IN the cloud (data, IAM, OS, applications, configurations). The exact split varies by service model (IaaS/PaaS/SaaS).

**Q: Most common cloud security mistake?**
A: Misconfiguration — leaving S3/Blob/GCS buckets public, overly permissive IAM policies, default passwords, and missing encryption. ~65% of cloud breaches are from customer misconfiguration, not provider vulnerabilities.

**Q: Does cloud provider handle all security?**
A: No. Even with SaaS, the customer is responsible for user access, data governance, and configuration. The provider handles the infrastructure and application platform.

**Q: Is the cloud more or less secure than on-premises?**
A: Cloud can be more secure if configured correctly (better tooling, automation, expertise). It can be less secure if poorly configured (larger attack surface, internet exposure, complex configuration space). The cloud forces security decisions that on-premises may not require.

### 79.2 IAM and Access Control

**Q: What is the principle of least privilege?**
A: Grant only the minimum permissions needed for a specific task. Never use wildcard `*` permissions, avoid `AdministratorAccess`, scope to specific resource ARNs, use IAM conditions (IP, MFA, time), and regularly review unused permissions.

**Q: Should I use IAM users or IAM roles?**
A: Roles are preferred: temporary credentials, auto-rotation, no long-lived keys. IAM users should only be used for break-glass emergency access. Use IAM Identity Center for human users, IAM roles for workloads.

**Q: What's the difference between security group and NACL?**
A: Security Groups: stateful, instance-level (ENI), allow rules only, evaluate all rules. NACLs: stateless, subnet-level, allow and deny rules, evaluate in order (lowest number first). SGs are simpler and preferred for most scenarios.

**Q: How do I manage cross-account access?**
A: Use cross-account IAM roles (not resource-based policies for anything other than S3). Use IAM conditions (aws:SourceAccount, aws:SourceOrg). Monitor all cross-account AssumeRole events with CloudTrail.

**Q: What is IMDSv2 and why important?**
A: Instance Metadata Service v2 requires a session token (PUT request) with configurable TTL. v1 has no authentication. v2 mitigates SSRF attacks that steal instance credentials. Always use IMDSv2 with hop limit 1.

### 79.3 Data Security and Encryption

**Q: What should I encrypt?**
A: Everything: data at rest (AES-256 via KMS/CloudHSM), data in transit (TLS 1.2+), and data in use (Confidential Computing). Especially: S3 buckets, EBS volumes, RDS databases, secrets, credentials, backups, logs.

**Q: Which encryption type should I use?**
A: SSE-S3 (AES-256, provider-managed) for least effort. SSE-KMS (customer-managed keys) for compliance/control. SSE-C (customer-provided keys) for maximum control. KMS with CMEK is the recommended default for most regulated workloads.

**Q: How do key management and HSM work in cloud?**
A: KMS generates and manages encryption keys (AWS KMS, Azure Key Vault, GCP Cloud KMS). CloudHSM provides FIPS 140-2 Level 3 validated hardware security modules for your exclusive use. KMS for most use cases; HSM for PKI, code signing, and regulatory requirements.

**Q: What is key rotation strategy?**
A: AWS KMS: automatic annual rotation for customer-managed keys (rotate on schedule or on-demand). Imported key material: manual rotation only. Secrets Manager: auto-rotation with Lambda (30-90 day schedule). Best practice: use KMS with automatic rotation and implement envelope encryption.

### 79.4 Monitoring and Incident Response

**Q: What logs should I collect?**
A: CloudTrail (management + data events), VPC Flow Logs, DNS query logs, WAF logs, GuardDuty findings, OS logs (CloudWatch Agent), database audit logs, application logs, load balancer access logs, network firewall logs, Config history.

**Q: What is my first step in cloud incident response?**
A: Isolate. Don't panic — don't delete evidence. Steps: 1) Disable/isolate compromised resources (apply quarantine SG, disable keys, detach policies). 2) Preserve evidence (snapshot, log export, forensic copy). 3) Investigate after containment.

**Q: How do I detect a compromised IAM key?**
A: GuardDuty findings (UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration), CloudTrail anomalous API patterns (new regions, new user agents, unusual times), IAM Access Advisor for unused services suddenly accessed, CloudTrail Lake anomaly detection.

**Q: What is a runbook and do I need one?**
A: A runbook is a documented, step-by-step procedure for responding to specific incidents. Yes — every cloud environment needs runbooks for common scenarios: public S3 bucket, compromised IAM key, crypto mining, DDoS, ransomware, data breach.

### 79.5 Compliance and Audit

**Q: How do I prove compliance to an auditor?**
A: Automate evidence collection: CloudTrail for change management, IAM credential report for access reviews, Config rules for configuration compliance, Backup reports for DR testing, Inspector reports for vulnerability management, Security Hub for continuous compliance.

**Q: What is a BAA and when do I need one?**
A: Business Associate Agreement — required with cloud provider if you store/process PHI (HIPAA). AWS, Azure, and GCP offer BAAs for their HIPAA-eligible services. Must be signed before any PHI is stored in cloud.

**Q: Can my cloud data be accessed by the provider?**
A: Provider employees can access in limited circumstances (maintenance, legal request). Access Transparency (GCP), CloudTrail (AWS), and Customer Lockbox (Azure) log all provider employee access to your resources. Use CMEK/Client-side encryption to prevent provider access.

### 79.6 Cost and Performance

**Q: Does security increase cloud costs?**
A: Initially yes — KMS operations, GuardDuty, WAF, Security Hub, SIEM ingestion, and multi-region DR add costs. But the security cost is typically <5% of total cloud spend. The cost of a breach is much higher (IBM 2024: $4.88M average).

**Q: Does encryption impact performance?**
A: Cloud KMS has negligible latency (<10ms per operation) for key operations. TLS encryption has minimal overhead with modern hardware (AES-NI instructions). EBS/DB encryption has <5% performance impact with modern CPUs. The security benefit far outweighs the minimal performance cost.

**Q: What is free vs paid in cloud security?**
A: Free: IAM, Organizations, Security Groups, NACLs, VPC, CloudTrail management events, Config (limited), Shield Standard, KMS (first key), GuardDuty (trial). Paid: GuardDuty (full), WAF, Shield Advanced, Security Hub, Sentinel, Deputy, Defender for Cloud (paid tier), Inspector, Macie._

### 79.7 Architecture and Design

**Q: Single vs multi-account strategy?**
A: Multi-account is strongly recommended: isolation boundary, blast radius containment, billing separation, environment isolation, compliance boundaries. Use AWS Organizations / Azure Management Groups / GCP Organizations with SCPs for governance.

**Q: How many availability zones do I need?**
A: Minimum 3 for production (multi-AZ deployment). 2 is common but risky (loss of one AZ = 50% capacity). 3+ is best practice. Services like Aurora and DynamoDB benefit from 3+ for quorum-based replication.

**Q: Should I use multi-cloud?**
A: Multi-cloud adds complexity but can be justified for: avoiding vendor lock-in, best-of-breed services, geographic/data residency requirements, M&A scenarios, risk diversification. Most organizations should master one cloud first, then expand.

**Q: What is zero trust and how to implement?**
A: Zero trust means no implicit trust — verify every request. Implementation: IAM with conditions, micro-segmentation (SGs/ACLs), mTLS for service-to-service, continuous authentication (Conditional Access), device trust (Intune/Endpoint Verification), just-in-time access (PIM).

---

## 80. Cloud Security Final Summary and Quick Reference

### 80.1 Top 10 Cloud Security Controls

| Priority | Control | Why | Implementation |
|----------|---------|-----|----------------|
| 1 | Enable MFA for ALL users | Prevents 99% of account compromise | IAM, Conditional Access, FIDO2 |
| 2 | Block Public Access | Prevents data exposure | SCP, S3 Block Public Access, Config |
| 3 | Least Privilege IAM | Limits blast radius | IAM Access Analyzer, permission boundaries |
| 4 | Enable Encryption | Protects data at rest/in transit | KMS, TLS 1.2+, ACM |
| 5 | Enable Logging | Detect and investigate | CloudTrail, VPC Flow Logs, SIEM |
| 6 | Patch Everything | Fix known vulnerabilities | Systems Manager, Inspector, automation |
| 7 | Network Segmentation | Limit lateral movement | VPC, SGs, NACLs, Transit Gateway |
| 8 | Enable Threat Detection | Detect active attacks | GuardDuty, Defender, SCC |
| 9 | Automate Response | Speed up containment | EventBridge, Step Functions, Lambda |
| 10 | Test Incident Plans | Validate readiness | DR drills, tabletop, pen testing |

### 80.2 Quick CLI Security Commands

```bash
# ============ AWS ============

# List all IAM users and check MFA status
aws iam list-users --query 'Users[*].UserName' | xargs -I {} sh -c 'echo "User: {}"; aws iam list-mfa-devices --user-name {}'

# Check S3 Block Public Access (account level)
aws s3control get-public-access-block --account-id ACCOUNT_ID

# List security groups with 0.0.0.0/0 on port 22
aws ec2 describe-security-groups --filters Name=ip-permission.cidr,Values=0.0.0.0/0 --query 'SecurityGroups[?IpPermissions[?FromPort==`22`]].[GroupId,GroupName]'

# Check CloudTrail status
aws cloudtrail describe-trails --query 'trailList[*].[Name,IsMultiRegionTrail,LogFileValidationEnabled,KmsKeyId]'

# Enable GuardDuty in all regions
for region in $(aws ec2 describe-regions --query 'Regions[*].RegionName' --output text); do aws guardduty create-detector --region $region --enable; done

# Check IAM credential report
aws iam generate-credential-report && aws iam get-credential-report --output text | base64 -d > credential-report.csv

# List unused IAM roles
aws iam list-roles --query "Roles[?RoleLastUsed==null].[RoleName,CreateDate]"

# ============ Azure ============

# Check all users MFA status
az rest --method GET --uri "/v1.0/users?`$select=id,displayName,userPrincipalName" | jq '.value[] | {name: .displayName, mfa: .strongAuthenticationRequirements}'

# List VMs with public IPs
az network public-ip list --query "[?ipAddress!=null].[name,ipAddress,resourceGroup]"

# Check NSG flow logs
az network watcher flow-log list --query "[?enabled==false].[name,location]"

# Enable Defender for Cloud on subscription
az security pricing create -n VirtualMachines --tier standard

# ============ GCP ============

# List public buckets
gsutil ls -L | grep -A1 "acl:.*allUsers\|acl:.*allAuthenticatedUsers"

# Check VPC flow logs
gcloud compute networks subnets list --format="json" | jq '.[] | select(.enableFlowLogs!=true) | .name'

# List public IPs on instances
gcloud compute instances list --format="json" | jq '.[] | select(.networkInterfaces[].accessConfigs[]?.natIP != null) | .name'

# Enable Security Command Center
gcloud services enable securitycenter.googleapis.com
```

### 80.3 Cloud Security Pocket Reference

**IAM Quick Reference**:
```
Principal                      ─→ Policy (allow/deny) ─→ Action on Resource
(User/Group/Role/Service)            │                       │
                                     ▼                       ▼
                              Control:                    Control:
                              - aws:SourceIp              - s3:prefix
                              - aws:MultiFactorAuth        - s3:versionid
                              - aws:SourceArn              - ec2:instancetype
                              - aws:CurrentTime            - kms:EncryptionContext
                              - aws:PrincipalOrgPaths
```

**Encryption Quick Reference**:
```
Data at Rest:        AES-256-GCM (KMS/CloudHSM)
Data in Transit:     TLS 1.2+ (ECDHE + AES-GCM + SHA-256)
Data in Use:         Intel SGX / AMD SEV-SNP / AWS Nitro
Key Management:      Envelope encryption (DEK + KEK)
Key Rotation:        Auto (annual) or on-demand (manual)
```

**Logging Quick Reference**:
```
CloudTrail:          Management events (free), Data events (paid), Insights (paid)
VPC Flow Logs:       Accepted traffic, Rejected traffic, All traffic (default)
GuardDuty:           Threat detection, findings export to S3, EventBridge targets
Config:              Configuration history, configuration snapshots, rules
CloudWatch:          Log groups, metric filters, alarms, dashboards
SIEM:                Splunk, Sentinel, ELK, Chronicle, Datadog
```

**Incident Response Quick Reference**:
```
1. ISOLATE → Quarantine SG, disable keys, detach policies
2. PRESERVE → Snapshot EBS, export logs, CloudTrail freeze
3. ANALYZE → CloudTrail timeline, GuardDuty findings, VPC Flow Logs
4. REMEDIATE → Rotate keys, patch vulnerability, update policy
5. RESTORE → Immutable backup, clean AMI, IaC deployment
6. LEARN → Root cause analysis, update playbook, improve controls
```

---

> [!REMINDER] 
> Cloud security is not a destination — it is a continuous journey. The threat landscape evolves, services change, and best practices advance. Regularly review your security posture, stay informed about new threats, and continuously improve your controls.
> **Key takeaway**: The three most important things you can do today to improve your cloud security are:
> 1. **Enable MFA everywhere** (especially for privileged accounts)
> 2. **Block public access to storage** (S3/Blob/GCS)
> 3. **Enable logging and monitoring** (CloudTrail + GuardDuty + SIEM)
