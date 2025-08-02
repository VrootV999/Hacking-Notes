# 🧰 <span style="color:rgb(255, 192, 0)">Common Tools for AD Engagements</span> 
#### <span style="color:rgb(255, 0, 0)">General Enumeration</span>
	1. PowerView
	2. AD Module for PowerShell
	3. BloodHound
	4. SharpHound
	5. Adalanche
	6. ADRecon
	7. LDAPDomainDump
	8. enum4linux-ng

#### <span style="color:rgb(255, 192, 0)">Credential Access and Dumping</span>
	1. Mimikatz
	2. LaZagne
	3. SharpDump
	4. ProcDump
	5. secretsdump.py (Impacket)
	6. Rubeus
	7. CredNinja
#### <span style="color:rgb(146, 208, 80)">Local Priv-Esc</span>
	1. WinPEAS
	2. SeatBelt
	3. PowerUp
	4. AccessChk
#### <span style="color:rgb(0, 32, 96)">Lateral Movement</span>
	1. PsExec (Impacket)
	2. wmiexec (Impacket)
	3. smbexec (Impacket)
	4. CME (CraclMapExec (nxe))
	5. PowerShell Remoting
	6. Invoke-Commands
	7. Impacket (General)
#### <span style="color:rgb(112, 48, 160)">Kerberos Attack</span>
	1. Rubeus
	2. Impacket (GetUserSPNs)
	3. ASPERoast.ps1
	4. john and hashcat
	5. Kerberoast
#### <span style="color:rgb(0, 176, 240)">Persistance</span> And <span style="color:rgb(255, 255, 0)">Post Exploitation</span>
	1. Mimikatz
	2. Kekeo
	3. DCShadow
	4. Certify
	5. ForgeCert
	6. Certipy
	7. DSInternal
#### <span style="color:rgb(94, 18, 18)">ADCS (Certificate System)</span>
	1. Certify
	2. Certipy
	3. ForgeCert
#### <span style="color:rgb(233, 12, 12)">NTLM Relay / MiTM</span>
	1. Responder
	2. Inveigh
	3. mitm6
	4. ntlmrelayx (Impacket)
#### <span style="color:rgb(0, 0, 0)">Vuln Exploits</span>
	1. IDFK why the fuck  i even wrote this shit
# <span style="color:rgb(0, 176, 240)">Attack Overview</span>

## White Box 📦
1. Validate Control over your initial access
2. Enumeration with the initial access to find other access points (for lateral movement)
3. Password Spray or No Auth user or creds lying on the low
4. dump creds if there are
5. lateral movement with rdp rce 
6. privilege escalation
7. persistance (Golden Ticket)
8. Post Exploitation

## <span style="color:rgb(0, 0, 0)">Black Box</span>
1. identify users at first place(by anonymous login or Guest Account)
2. User Enumeration
3. Capture Hashes or Creds lying on the sight
4. use 'em
5. Golden Ticket and Post Exploitation
# <span style="color:rgb(0, 32, 96)">Domain Enumeration</span>

## <span style="color:rgb(255, 0, 0)">PowerView</span> 
- Can be used in the vitcim AD during "Post Exploitation"
```
//first login as a admin
powershell -ep bypass

//all the needed commands

[1] Enumerate users
    Get-NetUser (says em all)
	
	Get-NetUser | select cn //*says only the users*//, objectsid //only               objectsid*//, adspath //*get the adspath*//
    
    Get-NetUser -UserName {User}  //about the user specifically 

	Get-NetGroup //says all the groups
	Get-NetGroup -Domain (domain)
	Get-NetGroup -AdminCount   //lists all the admins
	Get-NetGroup -UserName (user)   //lists the groups where it is present
    Get-NetGroupMember -GroupName (group) //lists the members of the group

	Get-NetComputer  //list the endpoints which have access to the AD
	Get-NetComputer -Ping //shows the alive ones
	Get-NetComputer -fulldata //list data about all of the devices present
								(os version , adspath, objectsid )

	Get-NetDomain    //get the domains info
	Get-DomainSID    //get SID
	Get-DomainPolicy //get policy created and followed in the domain
	Get-NetDomainController  //shows the controller info

	Find-LocalAdminAcess  //list domain which u can get access to domain

	Invoke-EnumerateLocalAdmin //enumerate local admins in the domain directly
	
	Get-NetGPO //get what policies are enabled and disabled (check misconfig)

	Get-NetLoggedon -ComputerName (name) //check who logged in

	Get-LastLoggedOn -ComputerName (name) //last who logged in

	Get-NetRDPSession -ComputerName (name)  //info on rdp

	Invoke-ShareFinder //list all the available shares
```

---

## <span style="color:rgb(255, 192, 0)">BloodHound</span> 
- Always powershell -ep *bypass*
```
Invoke-BloodHound -CollectionMethod All -Domain (Domain) -ZipFileName (zipfile)
				//collects everything thing to enumerate and store it in a zip
```
- upload the data into the bloodhound 
- try whatever takes your eyes

## <span style="color:rgb(146, 208, 80)">Mimikatz</span> 
```

//check privileges
privilege::debug

//list passwords (old windows)
sekurlsa::logonpasswords

//dump sam database
lsadump::sam

//dump lsa database
lsadump::lsa /patch



```