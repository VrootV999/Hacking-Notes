### Syntax
--wordlist=(file)                               Use a wordlist for password cracking
--format=(type)                               Specify hash type (e.g., MD5, SHA256)
--rules                                                Apply word mangling rules
--incremental                                     Perform brute-force attack
--show                                               Display cracked passwords
--session=(name)                           Save and restore session
--single                                             Needs only username.txt  and uses various ways of username  
                            username:hash  

### FIle password Cracking

zip2john file.zip > zip.hashes
john zip.hashes

### Example:
john --wordlist=/usr/share/wordlists/rockyou.txt --format=nt hashes.txt
 
