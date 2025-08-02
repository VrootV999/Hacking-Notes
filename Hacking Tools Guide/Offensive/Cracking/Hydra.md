
### Syntax
-l (user)                      Specify username
-L (file)                       Use a file for usernames
-p (password)            Specify password
-P (file)                      Use a file for passwords
-s (port)                    Specify port
-t (tasks)                   Number of tasks (default: 16)
-vV                              Verbose output
-R                               Resume interrupted session
-o                               Save File
-c                               Combination attack 
-u                               URL
-d                               Debug mode
-v                               verbose
-S                               SSL Connect
-H                              Hosts

### Example:
hydra -l admin -P /usr/share/wordlists/rockyou.txt 192.168.1.10 ssh
