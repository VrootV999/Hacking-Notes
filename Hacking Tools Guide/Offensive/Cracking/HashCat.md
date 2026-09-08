# Syntax
-m (mode)                                 Specify hash type (e.g., -m 0 for MD5, -m 100 for SHA1)
-a (attack)                                  Specify attack mode
                          0   Dictionary Attack
                          1   two wordlist for compound password
                          3  Brute-Force
                        6,7 Hybrid attack (dictionary and mask-based)

--show        Display cracked hashes
--username    Ignore username in hashfile
--increment   Enable incremental brute force
--session     Save/restore session

# Example:
hashcat -m 1000 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
