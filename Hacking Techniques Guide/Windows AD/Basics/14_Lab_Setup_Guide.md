# Active Directory Lab Setup Guide

## What it is

A comprehensive reference for building Active Directory labs tailored to red team practice. Covers automated deployments, manual builds on Hyper‑V/VMware/VirtualBox, cloud options, pre‑made vulnerable labs, adding intentional misconfigurations, tool installation, and a quick‑start minimal lab.

---

## 1. Automated Lab Deployments

### 1.1 GOAD (Game of Active Directory)

The most popular vulnerable AD lab. Provides 5 VMs across 2 domains in 1 forest with ~100 misconfigurations.

**Requirements**

- 64 GB RAM (32 GB minimum)
- 120 GB free disk
- VMware Workstation / VirtualBox / Proxmox

**Installation (Linux host)**

```bash
# Install Vagrant and provider plugin
sudo apt install vagrant
vagrant plugin install vagrant-vmware-desktop   # VMware
# or
vagrant plugin install vagrant-reload            # VirtualBox helper

# Clone the project
git clone https://github.com/Orange-Cyberdefense/GOAD
cd GOAD

# Choose provider (default is VirtualBox)
# For VMware:
cp providers/vmware/vagrant.yml .
# For VirtualBox:
cp providers/virtualbox/vagrant.yml .

# Deploy all VMs
vagrant up
```

**Network layout**

| VM         | Role                  | IP              | Domain          |
|------------|------------------------|-----------------|-----------------|
| DC01       | DC nordcorp.local      | 192.168.10.10   | nordcorp.local  |
| SRV01      | Member server (CA)     | 192.168.10.11   | nordcorp.local  |
| DC02       | DC nwind.local         | 192.168.10.12   | nwind.local     |
| SRV02      | SQL member server      | 192.168.10.13   | nwind.local     |
| DC03       | DC child.nordcorp.local| 192.168.10.14   | child.nordcorp  |

**Post‑deployment**

```bash
# Access via Vagrant
vagrant ssh dc01

# Or plain RDP with credentials:
# Username: vagrant / Password: vagrant
# Local admin: Administrator / Password: Password123!

# Verify forest health (from dc01):
netdom query fsmo
Get-ADForest
Get-ADDomain
```

**Proxmox provider** — Use the `proxmox` branch and configure `proxmox.yml` with your PVE API token.

---

### 1.2 BadBlood

PowerShell script from @davidprowe that fills an existing domain with thousands of insecure objects.

```powershell
# On a domain controller (run as Domain Admin)
Set-ExecutionPolicy Bypass -Scope Process -Force
git clone https://github.com/davidprowe/BadBlood
cd BadBlood
.\BadBlood.ps1 -Domain "lab.local" -UsersLimit 100
```

**What BadBlood creates:**

- 100+ domain users with weak passwords
- Nested groups with privilege escalations
- Misconfigured ACLs (GenericAll / WriteOwner / DCSync on low‑priv users)
- Service accounts with SPNs (Kerberoast targets)
- Users without pre‑auth (AS‑REP roast targets)
- GPOs with insecure settings
- Delegation misconfigurations
- LAPS deployment with readable passwords

Logs are written to `C:\BadBlood\badblood.log`.

---

### 1.3 AutomatedLab

PowerShell module for repeatable lab builds on Hyper‑V and Azure.

```powershell
# Install
Install-Module AutomatedLab -Force
Install-LabDefinition -Name ADLab -DefaultVirtualizationEngine HyperV

# Lab definition example
Add-LabMachineDefinition -Name DC01 -Roles RootDC -OperatingSystem 'Windows Server 2022 Datacenter (Desktop Experience)'
Add-LabMachineDefinition -Name SRV01 -OperatingSystem 'Windows Server 2022 Datacenter (Desktop Experience)'

Install-Lab
```

---

### 1.4 Windows Server Evaluation Copies

Microsoft provides 180‑day eval ISOs — the standard source for all AD lab OS images.

```
https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022
https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2019
https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2016
https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise
https://www.microsoft.com/en-us/evalcenter/evaluate-windows-11-enterprise
```

Re‑arm the 180‑day eval (runs up to 3 times, giving 540 days total):

```powershell
slmgr /rearm
```

---

## 2. Manual Lab with Hyper‑V

Requires Windows 10/11 Pro/Enterprise or Windows Server with the Hyper‑V role.

### 2.1 Enable Hyper‑V

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Hyper-V -All
# Reboot required
Restart-Computer
```

### 2.2 Create Internal Virtual Switch

```powershell
New-VMSwitch -Name "InternalAD" -SwitchType Internal
```

Assign the host an IP on the same subnet (e.g. 172.16.0.1/24) for management access.

### 2.3 Deploy the Domain Controller

**Step 1 — Install OS**

Create a new Gen‑2 VM (Gen‑2 is required for Windows Server 2022; Gen‑1 works for 2016/2019):

```powershell
$VM = @{
    Name             = "DC01"
    MemoryStartupBytes = 4GB
    Generation       = 2
    NewVHDPath       = "D:\VMs\DC01\DC01.vhdx"
    NewVHDSizeBytes  = 60GB
    SwitchName       = "InternalAD"
}
New-VM @VM
Set-VMDvdDrive -VMName DC01 -Path "D:\ISOs\WindowsServer2022.iso"
Start-VM DC01
```

**Step 2 — Configure networking inside the VM**

```powershell
# Inside DC01 — set static IP
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 172.16.0.10 -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 127.0.0.1
Rename-Computer -NewName DC01
Restart-Computer
```

**Step 3 — Install AD DS and promote**

```powershell
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools

# Promote to domain controller (new forest)
Install-ADDSForest `
    -DomainName "lab.local" `
    -DomainNetbiosName "LAB" `
    -DomainMode WinThreshold `
    -ForestMode WinThreshold `
    -InstallDns $true `
    -CreateDnsDelegation $false `
    -Force
```

The server reboots automatically. Log back in as `LAB\Administrator`.

### 2.4 Join Member Servers and Workstations

Repeat for each machine (SRV01, WS01, etc.).

```powershell
# Inside each member machine
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 172.16.0.20 -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 172.16.0.10
Rename-Computer -NewName SRV01
Restart-Computer

# After reboot, join the domain
Add-Computer -DomainName "lab.local" -Credential (Get-Credential "LAB\Administrator")
Restart-Computer
```

### 2.5 Add Additional Domain Controllers

```powershell
# On the new DC VM (e.g. DC02)
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools

Install-ADDSDomainController `
    -DomainName "lab.local" `
    -InstallDns $true `
    -Credential (Get-Credential "LAB\Administrator")
```

### 2.6 Create a Child Domain

```powershell
# Run on any DC in the parent domain
Install-ADDSDomain `
    -NewDomainName "child" `
    -ParentDomainName "lab.local" `
    -DomainMode WinThreshold `
    -Credential (Get-Credential "LAB\Administrator")
```

This produces `child.lab.local`. A new DC is created for the child domain.

### 2.7 Set Up Active Directory Certificate Services (AD CS)

```powershell
# Install the role
Install-WindowsFeature AD-Certificate -IncludeManagementTools

# Configure as Enterprise Root CA
Install-AdcsCertificationAuthority `
    -CAType EnterpriseRootCa `
    -CryptoProviderName "RSA#Microsoft Software Key Storage Provider" `
    -KeyLength 2048 `
    -HashAlgorithmName SHA256 `
    -Force
```

Restart the `CertSvc` service after installation:

```powershell
Restart-Service CertSvc
```

Verify:

```powershell
certutil -config -ping
```

### 2.8 Configure Users, Groups, and OUs

```powershell
# Create OUs
New-ADOrganizationalUnit -Name "Employees" -Path "DC=lab,DC=local"
New-ADOrganizationalUnit -Name "Admins" -Path "DC=lab,DC=local"
New-ADOrganizationalUnit -Name "ServiceAccounts" -Path "DC=lab,DC=local"
New-ADOrganizationalUnit -Name "Servers" -Path "DC=lab,DC=local"
New-ADOrganizationalUnit -Name "Workstations" -Path "DC=lab,DC=local"

# Create groups
New-ADGroup -Name "HelpDesk" -GroupScope Global -Path "OU=Admins,DC=lab,DC=local"
New-ADGroup -Name "ITSupport" -GroupScope Global -Path "OU=Admins,DC=lab,DC=local"
New-ADGroup -Name "SQLAdmins" -GroupScope Global -Path "OU=Admins,DC=lab,DC=local"

# Create users
$Users = @(
    @{Name="jsmith"; GivenName="John"; Surname="Smith"; Password="Password123!"},
    @{Name="jdoe"; GivenName="Jane"; Surname="Doe"; Password="Password123!"},
    @{Name="svc_sql"; GivenName="SQL"; Surname="Service"; Password="P@ssw0rd!"},
    @{Name="svc_oracle"; GivenName="Oracle"; Surname="Service"; Password="P@ssw0rd!"},
    @{Name="svc_web"; GivenName="Web"; Surname="Service"; Password="P@ssw0rd!"},
    @{Name="lowpriv"; GivenName="Low"; Surname="PrivUser"; Password="Summer2024!"},
    @{Name="backup_admin"; GivenName="Backup"; Surname="Admin"; Password="Backup@DM1n!"}
)

foreach ($User in $Users) {
    $SecurePass = ConvertTo-SecureString $User.Password -AsPlainText -Force
    New-ADUser `
        -Name $User.Name `
        -GivenName $User.GivenName `
        -Surname $User.Surname `
        -SamAccountName $User.Name `
        -UserPrincipalName "$($User.Name)@lab.local" `
        -Path "OU=Employees,DC=lab,DC=local" `
        -AccountPassword $SecurePass `
        -Enabled $true
}

# Add users to privileged groups
Add-ADGroupMember -Identity "Domain Admins" -Members "backup_admin"
```

### 2.9 Hyper‑V vs VMware Workstation vs VirtualBox

| Feature               | Hyper‑V                        | VMware Workstation           | VirtualBox                |
|------------------------|--------------------------------|------------------------------|---------------------------|
| Host OS               | Windows only                   | Windows / Linux              | Windows / Linux / macOS   |
| Performance           | Excellent (Type 1)             | Very good                    | Good                      |
| Nested virtualization | Yes (requires PowerShell cmd)  | Yes                          | Yes                       |
| Snapshots             | Yes (checkpoints)              | Yes (snapshots)              | Yes                       |
| Vagrant support       | Yes                            | Yes (plugin)                 | Yes (default)             |
| Licensing             | Free (with Windows)            | Paid                         | Free (OME)                |
| Best for              | Windows‑only red teams         | Cross‑platform teams         | Budget / hobby labs       |

---

## 3. Manual Lab with VMware/VirtualBox

The procedure is nearly identical to Hyper‑V; only the VM creation and network steps differ.

### 3.1 Network Configuration

| Type       | Host‑to‑Guest | Guest‑to‑Guest | Guest‑to‑Internet | Use Case                    |
|------------|---------------|----------------|-------------------|-----------------------------|
| NAT        | Via host IP   | Yes            | Yes (shared)      | Guest needs internet        |
| Host‑Only  | Yes           | Yes            | No                | Isolated lab                |
| Bridged    | Via LAN IP    | Yes            | Yes (direct)      | Not recommended for labs    |

**Recommended:** Host‑only with a static IP range (e.g. 192.168.56.0/24 for VirtualBox, 192.168.136.0/24 for VMware).

### 3.2 Vagrant Alternative

```ruby
# Vagrantfile for a minimal AD lab
Vagrant.configure("2") do |config|
  config.vm.box = "jborean93/WindowsServer2022"

  config.vm.define "dc01" do |dc|
    dc.vm.hostname = "DC01"
    dc.vm.network "private_network", ip: "192.168.56.10"
    dc.vm.provision "shell", path: "provision-dc.ps1"
  end

  config.vm.define "srv01" do |srv|
    srv.vm.hostname = "SRV01"
    srv.vm.network "private_network", ip: "192.168.56.20"
    srv.vm.provision "shell", path: "provision-member.ps1"
  end
end
```

**provision-dc.ps1:**

```powershell
$Password = ConvertTo-SecureString "Password123!" -AsPlainText -Force
New-NetIPAddress -InterfaceAlias "Ethernet2" -IPAddress 192.168.56.10 -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias "Ethernet2" -ServerAddresses 127.0.0.1
Rename-Computer -NewName DC01 -Force
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSForest -DomainName "lab.local" -SafeModeAdministratorPassword $Password -Force
```

**provision-member.ps1:**

```powershell
$Pass = ConvertTo-SecureString "Password123!" -AsPlainText -Force
New-NetIPAddress -InterfaceAlias "Ethernet2" -IPAddress 192.168.56.20 -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias "Ethernet2" -ServerAddresses 192.168.56.10
Rename-Computer -NewName SRV01 -Force
Restart-Computer -Force
```

---

## 4. Cloud-Based Labs

### 4.1 TryHackMe

| Room                   | Description                              | Link                                                                |
|------------------------|------------------------------------------|---------------------------------------------------------------------|
| Attacktive Directory   | Basic Kerberos attacks against a DC      | https://tryhackme.com/room/attacktivedirectory                      |
| Active Directory Basics| AD fundamentals                          | https://tryhackme.com/room/activedirectorybasics                    |
| AD-Exploitation        | Full AD penetration test scenario        | https://tryhackme.com/room/adexploitation                           |
| Breaching AD           | Initial access techniques                | https://tryhackme.com/room/breachingad                              |
| AD Enumeration         | AD recon without tools                   | https://tryhackme.com/room/adenumeration                            |

### 4.2 HackTheBox

Retired AD boxes (accessible with VIP):

| Machine   | Focus                            |
|-----------|----------------------------------|
| Forest    | AS‑REP roasting, Kerberoasting   |
| Sauna     | AS‑REP roasting, DCSync          |
| Cascade   | AD reconnaissance, LAPS          |
| Active    | SMB, Kerberos, GPP passwords     |
| Sizzle     | AD CS (ESC1/ESC8)                |
| Search    | Kerberos delegation              |
| Intelligence| ADIDNS, GPO abuse               |

### 4.3 Pentester Academy

- **Active Directory Exploitation** — Full course with hands-on labs
- **PowerShell for AD** — Scripting against AD targets
- **Certified Red Team Professional (CRTP)** — Exam-focused AD lab

### 4.4 Azure AD / Entra ID

```powershell
# Create a free Azure AD tenant
# https://portal.azure.com -> Azure Active Directory -> Create tenant

# Create test users via PowerShell
Connect-MgGraph -Scopes "User.ReadWrite.All","Group.ReadWrite.All"

New-MgUser `
    -DisplayName "Cloud Admin" `
    -UserPrincipalName "cloudadmin@yourtenant.onmicrosoft.com" `
    -PasswordProfile @{Password="Password123!"; ForceChangePasswordNextSignIn=$false} `
    -AccountEnabled $true `
    -MailNickName "cloudadmin"

# Enable Hybrid AD (Azure AD Connect) for on-prem sync
```

### 4.5 AWS EC2

```bash
# Deploy Windows Server on EC2
aws ec2 run-instances \
    --image-id ami-0abcdef1234567890 \
    --instance-type t3.large \
    --security-group-ids sg-12345678 \
    --key-name my-keypair \
    --block-device-mappings DeviceName=/dev/sda1,Ebs={VolumeSize=60}

# Then RDP in and promote to DC (same steps as manual lab)
```

---

## 5. Pre‑Made Vulnerable AD Labs

### 5.1 DetectionLab (Spartant)

Blue‑team focused but used by many red teams for evasion testing.

```bash
git clone https://github.com/clong/DetectionLab
cd DetectionLab/Vagrant

# Requires VMware + 20 GB RAM
vagrant up --provider vmware_desktop
```

Components: Windows DC, Windows 10 client, Windows Server with Splunk, Kali, SecurityOnion.

### 5.2 Windows Attack & Defense Lab (Malware Archaeology)

```bash
git clone https://github.com/clong/AttackAndDefenseLab
cd AttackAndDefenseLab
vagrant up
```

Includes DC, member server, and a workstation with pre-loaded security tools.

### 5.3 Invoke-ADLabDeployer

PowerShell-based scenario builder — create specific attack scenarios on demand.

```powershell
git clone https://github.com/outflanknl/Invoke-ADLabDeployer
Import-Module .\Invoke-ADLabDeployer.ps1

# Deploy a Kerberoast scenario
Invoke-ADLabDeployer -Scenario Kerberoast -DomainName "lab.local"

# Other scenarios:
# ASREPRoast, ACLAbuse, DCSync, SkeletonKey, GoldenTicket, SilverTicket,
# UnconstrainedDelegation, ConstrainedDelegation, AdminSDHolder
```

### 5.4 SecurityOnion + AD

```bash
# Deploy SecurityOnion alongside your AD lab
git clone https://github.com/Security-Onion-Solutions/securityonion

# Configure SO to monitor the AD subnet
# In so-import / so-rule management, add rules for Kerberos, SMB, LDAP detection
```

### 5.5 Splunk + AD

```bash
# Install Splunk Universal Forwarder on each AD server
# Download from https://www.splunk.com/en_us/download/universal-forwarder.html

# Install and configure
msiexec /i splunkuniversalfowarder.msi AGREETOLICENSE=yes /quiet
& "C:\Program Files\SplunkUniversalForwarder\bin\splunk" add forward-server splunk-indexer.local:9997 -auth admin:changeme
& "C:\Program Files\SplunkUniversalForwarder\bin\splunk" install app C:\WindowsEventLogs.spl -auth admin:changeme
```

Splunk apps for AD monitoring: Splunk Add‑on for Windows, Splunk Security Essentials.

---

## 6. Adding Vulnerabilities for Practice

### 6.1 ACL Misconfigurations

```powershell
# Requires ActiveDirectory and PowerView modules
Import-Module ActiveDirectory
# Load PowerView
. .\PowerView.ps1

# Give lowprivuser DCSync rights on the domain
Add-DomainObjectAcl `
    -TargetIdentity "DC=lab,DC=local" `
    -PrincipalIdentity "lab\lowpriv" `
    -Rights DCSync

# GenericAll on AdminSDHolder (persistence)
Add-DomainObjectAcl `
    -TargetIdentity "CN=AdminSDHolder,CN=System,DC=lab,DC=local" `
    -PrincipalIdentity "lab\lowpriv" `
    -Rights GenericAll

# GenericWrite on a high‑value user
Add-DomainObjectAcl `
    -TargetIdentity "lab\backup_admin" `
    -PrincipalIdentity "lab\lowpriv" `
    -Rights GenericWrite

# WriteOwner on a domain admin group
Add-DomainObjectAcl `
    -TargetIdentity "CN=Domain Admins,CN=Users,DC=lab,DC=local" `
    -PrincipalIdentity "lab\lowpriv" `
    -Rights WriteOwner

# Force set a SecurityDescriptor (alternative method)
$SD = Get-DomainObjectAcl -TargetIdentity "lab\domain admins" -ResolveGUIDs
# Modify SD and apply via Set-DomainObjectAcl
```

### 6.2 Kerberos Delegation Misconfigurations

```powershell
# Unconstrained delegation
Set-ADComputer -Identity "SRV01" -TrustedForDelegation $true

# Constrained delegation
Set-ADUser -Identity "svc_web" -ServicePrincipalNames @{Add="http/web.lab.local"}
Set-ADUser -Identity "svc_web" -PrincipalsAllowedToDelegateToAccount (Get-ADComputer SRV01)

# Resource-based constrained delegation
Set-ADComputer -Identity "SRV01" -PrincipalsAllowedToDelegateToAccount (Get-ADUser svc_web)
```

### 6.3 AS‑REP Roast Targets

```powershell
# Disable pre‑auth and set weak encryption
Set-ADUser -Identity "svc_oracle" -KerberosEncryptionType RC4
Get-ADUser -Identity "svc_oracle" | Set-ADAccountControl -DoesNotRequirePreAuth $true
```

### 6.4 AD CS (ESC1 — Misconfigured Certificate Template)

```powershell
# On the CA server
certutil -setreg CA\EditFlags +EDITF_ATTRIBUTESUBJECTALTNAME2
net stop certsvc && net start certsvc

# Verify the flag was set
certutil -getreg CA\EditFlags
```

Create a certificate template that allows any user to supply a SAN (Subject Alternative Name) — standard ESC1 abuse.

### 6.5 Unconstrained Delegation

Via GUI: Open **Active Directory Users and Computers** → computer object → Properties → Delegation tab → Check "Trust this computer for delegation to any service (Kerberos only)".

Via PowerShell:

```powershell
Set-ADComputer -Identity "SRV01" -TrustedForDelegation $true
```

### 6.6 LAPS with Readable Passwords

```powershell
# Extend schema (requires Schema Admin)
Update-LapsADSchema

# Deploy LAPS GPO (Computer Config → Admin Templates → LAPS)
Set-ADComputer -Identity "SRV01" -Description "LAPS password readable by lowpriv user" 

# Give lowpriv read access
Set-ADObject -Identity "OU=Servers,DC=lab,DC=local" -PrincipalsAllowedToRetrieveManagedPassword "lab\lowpriv"
```

### 6.7 Other Misconfigurations

```powershell
# GPP (Group Policy Preferences) password in SYSVOL
# Create GPO with cpassword
Set-GPPPassword -Domain lab.local -Username "svc_gpp" -NewPassword "P@ssw0rd123" -Guid "12345678-1234-1234-1234-123456789012"

# Add SPNs for Kerberoasting
Set-ADUser -Identity "svc_sql" -ServicePrincipalNames @{Add="MSSQLSvc/SQL01.lab.local:1433"}

# Weak password (likely already in rockyou.txt)
Set-ADAccountPassword -Identity jsmith -Reset -NewPassword (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force)

# SID History injection (simulate trust abuse)
Set-ADUser -Identity "lowpriv" -Add @{SIDHistory="S-1-5-21-<DOMAINID>-512"}   # Domain Admin SID
```

---

## 7. Tool Installation for Attack Machine (Kali / Parrot)

### 7.1 Linux Attack Box

```bash
# Essential AD tools (Kali/Parrot repos)
sudo apt update
sudo apt install -y \
    bloodhound \
    bloodhound.py \
    impacket-scripts \
    crackmapexec \
    responder \
    enum4linux-ng \
    ldapdomaindump \
    kerberoast \
    smbclient \
    nmap \
    libreoffice  # Required for some BloodHound graph rendering

# Python tools via pipx
sudo apt install pipx
pipx ensurepath
pipx install netexec
pipx install certipy-ad
pipx install bloodyad
pipx install targetedKerberoast
pipx install dontkillmymlm

# Kerbrute (Go binary)
git clone https://github.com/ropnop/kerbrute
cd kerbrute
go build
sudo cp kerbrute /usr/local/bin/

# Impacket from source (latest)
git clone https://github.com/fortra/impacket
cd impacket
pipx install .

# PKINITtools
git clone https://github.com/dirkjanm/PKINITtools
cd PKINITtools
pipx install .

# ADExplorer, Sysinternals (run from Linux via wine)
# Or just keep accessible on your host.

# Manually getcert / certipy
certipy find -u jsmith@lab.local -p 'Password123!' -target dc01.lab.local

# ldapsearch
sudo apt install ldapscripts
ldapsearch -x -H ldap://dc01.lab.local -D "LAB\jsmith" -w 'Password123!' -b "DC=lab,DC=local"
```

### 7.2 Windows Tools (transfer to target or run on attack VM)

Keep these binaries available for transfer to Windows targets:

```bash
# Create a tools share on your Kali box
mkdir -p /opt/win-tools
cd /opt/win-tools

# Download common tools (URLs change — check latest releases)
wget https://github.com/gentilkiwi/mimikatz/releases/latest/download/mimikatz_trunk.zip
wget https://github.com/GhostPack/Rubeus/releases/latest/download/Rubeus.exe
wget https://github.com/GhostPack/SharpHound/releases/latest/download/SharpHound.exe
wget https://github.com/GhostPack/Seatbelt/releases/latest/download/Seatbelt.exe
wget https://github.com/rasta-mouse/Sherlock/raw/master/Sherlock.ps1
wget https://github.com/PowerShellMafia/PowerSploit/raw/master/Recon/PowerView.ps1
wget https://github.com/BC-SECURITY/Empire/raw/main/empire/server/data/module_source/credentials/Invoke-Kerberoast.ps1
wget https://github.com/Sic4rio/ADRecon/raw/master/ADRecon.ps1
wget https://github.com/0xthirteenth/Invoke-ZeroLogon/raw/master/Invoke-ZeroLogon.ps1

# Tools to collect at runtime:
# Process Hacker, ProcDump, SysInternals Suite, wireshark, gping, chisel (for tunnels)
```

Serve via Python HTTP:

```bash
cd /opt/win-tools
python3 -m http.server 80
```

On target:

```powershell
Invoke-WebRequest -Uri http://192.168.56.10/Rubeus.exe -OutFile C:\Tools\Rubeus.exe
```

### 7.3 BloodHound Setup

```bash
# Neo4j database
sudo apt install neo4j
sudo systemctl enable neo4j
sudo neo4j start
# Default credentials: neo4j / neo4j (change on first login)

# BloodHound GUI (Electron app)
sudo apt install bloodhound
bloodhound &

# Or use the Python collector
pipx install bloodhound
bloodhound-python -u jsmith -p 'Password123!' -d lab.local -dc dc01.lab.local -c All -ns 172.16.0.10
```

### 7.4 NetExec / CrackMapExec

```bash
# NetExec (successor to CrackMapExec)
netexec smb 172.16.0.10 -u jsmith -p 'Password123!' --shares
netexec ldap 172.16.0.10 -u jsmith -p 'Password123!' --bloodhound -ns 172.16.0.10
netexec smb 172.16.0.10 -u jsmith -p 'Password123!' -M nopac
netexec smb 172.16.0.10 -u jsmith -p 'Password123!' -M coerce_plus
```

---

## 8. Quick Start (Minimal Lab)

The smallest possible AD lab: **1 Domain Controller + 1 Member Server** on any hypervisor with ~8 GB RAM total.

### 8.1 Provision the DC

```powershell
# Paste into PowerShell on the DC after OS install
# Configure IP, rename, install AD, and create objects — all in one script

$DomainName = "lab.local"
$NetBiosName = "LAB"
$SafeModePass = ConvertTo-SecureString "Passw0rd!" -AsPlainText -Force
$AdminPass = ConvertTo-SecureString "Password123!" -AsPlainText -Force

# --- Network ---
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 172.16.0.10 -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 127.0.0.1
Rename-Computer -NewName DC01

# --- AD DS ---
Install-WindowsFeature AD-Domain-Services -IncludeManagementTools
Install-ADDSForest `
    -DomainName $DomainName `
    -DomainNetbiosName $NetBiosName `
    -SafeModeAdministratorPassword $SafeModePass `
    -Force

# --- Post-reboot (run as LAB\Administrator) ---

# Create OUs
New-ADOrganizationalUnit "Employees" -Path "DC=lab,DC=local"
New-ADOrganizationalUnit "Admins" -Path "DC=lab,DC=local"
New-ADOrganizationalUnit "Servers" -Path "DC=lab,DC=local"

# Create groups
New-ADGroup "Domain Admins" -GroupScope Global -Path "OU=Admins,DC=lab,DC=local"
New-ADGroup "SQL Admins" -GroupScope Global -Path "OU=Admins,DC=lab,DC=local"

# Create users with weak passwords
$Users = @(
    @{Name="jsmith"; Pass="Password123!"},
    @{Name="svc_sql"; Pass="P@ssw0rd1"},     # Kerberoast target
    @{Name="svc_oracle"; Pass="P@ssw0rd1"},   # AS-REP target
    @{Name="lowpriv"; Pass="Summer2024!"}     # Low‑priv foothold
)
foreach ($u in $Users) {
    $p = ConvertTo-SecureString $u.Pass -AsPlainText -Force
    New-ADUser -Name $u.Name -SamAccountName $u.Name -UserPrincipalName "$($u.Name)@lab.local" `
        -Path "OU=Employees,DC=lab,DC=local" -AccountPassword $p -Enabled $true
}

# --- Vulnerabilities ---

# 1) Kerberoast target
Set-ADUser -Identity svc_sql -ServicePrincipalNames @{Add="MSSQLSvc/SQL01.lab.local:1433"}

# 2) AS-REP roast target
Set-ADUser -Identity svc_oracle -KerberosEncryptionType RC4
Get-ADUser svc_oracle | Set-ADAccountControl -DoesNotRequirePreAuth $true

# 3) DCSync rights for lowpriv
Add-DomainObjectAcl -TargetIdentity "DC=lab,DC=local" -PrincipalIdentity "lab\lowpriv" -Rights DCSync

# 4) Unconstrained delegation on a nonexistent computer (simulated)
New-ADComputer -Name "SRV01" -Path "OU=Servers,DC=lab,DC=local"
Set-ADComputer -Identity SRV01 -TrustedForDelegation $true

Write-Host "[+] Lab setup complete!"
```

### 8.2 Provision the Member Server

```powershell
# Paste on the member machine after OS install
New-NetIPAddress -InterfaceAlias "Ethernet" -IPAddress 172.16.0.20 -PrefixLength 24
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses 172.16.0.10
Rename-Computer -NewName SRV01 -Force
Restart-Computer -Force

# After reboot, join domain
Add-Computer -DomainName "lab.local" -Credential (Get-Credential "LAB\Administrator")
Restart-Computer -Force
```

### 8.3 Validation Checklist

| Check | Command (run from Kali) |
|-------|--------------------------|
| Domain reachable | `nslookup lab.local 172.16.0.10` |
| LDAP binds | `ldapsearch -x -H ldap://dc01.lab.local -D "LAB\lowpriv" -w 'Summer2024!' -b "DC=lab,DC=local"` |
| SMB accessible | `netexec smb 172.16.0.10 -u lowpriv -p Summer2024!` |
| Kerberos works | `impacket-getTGT lab.local/lowpriv:Summer2024!` |
| AS-REP roast | `impacket-GetNPUsers lab.local/ -dc-ip 172.16.0.10 -usersfile users.txt` |
| Kerberoast | `impacket-GetUserSPNs lab.local/lowpriv:Summer2024! -dc-ip 172.16.0.10 -request` |
| DCSync test | `impacket-secretsdump lab.local/lowpriv:Summer2024!@172.16.0.10 -just-dc` |
| BloodHound | `bloodhound-python -u lowpriv -p Summer2024! -d lab.local -dc dc01.lab.local -c All -ns 172.16.0.10` |

### 8.4 Lab Expansion Roadmap

```
Minimal (2 VMs)     →     Standard (4 VMs)       →     Full (8+ VMs)
  DC01                     DC01                         DC01 (lab.local)
  SRV01                    DC02 (redundancy)             DC02
                           SRV01 (CA + SQL)             DC03 (child.lab.local)
                           WS01 (Win 10)                SRV01 (CA)
                                                         SRV02 (SQL)
                                                         SRV03 (Exchange)
                                                         WS01 (Win 11)
                                                         WS02 (Win 10)
                                                         Kali attack box
```

### 8.5 Common Lab Fixes

```powershell
# Reset KRBTGT password (double reset invalidates all tickets)
Reset-ADAccountPassword -Identity krbtgt -Reset -NewPassword (ConvertTo-SecureString "NewPass!" -AsPlainText -Force)

# Extend evaluation period
slmgr /rearm

# If DNS breaks, re-register
ipconfig /registerdns
Restart-Service DNS

# Force replication
repadmin /syncall /AdeP

# Check FSMO roles
netdom query fsmo

# Rebuild SYSVOL if needed
dcdiag /test:replications /v
```
