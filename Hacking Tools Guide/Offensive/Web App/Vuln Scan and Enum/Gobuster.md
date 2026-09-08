
## Syntax
- dir                              directory find
- -x                               specific file
- -u                               URL
- -w                              wordlist
- --append-domain    
- vhost                         victim 
## Example
- gobuster -u http://IP -w wordlist -x .php
- gobuster dir -u http://IP -w /usr/share/wordlists/dirb/others/best15.txt 
- gobuster -u http://IP -w /usr/share/SecLists/discovery/DNS/soldomains
