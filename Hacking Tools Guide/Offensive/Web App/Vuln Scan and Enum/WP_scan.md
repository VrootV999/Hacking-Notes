### Update
- wpscan --update            update the DB
### Enumeration Modes
- `Passive:` scan with a small number of requests => avoid causing DOS server
- `Aggressive:` scan with a large number of requests and continuously to the server
- `Mixed:` Combined both
### Enumeration Options

> [!NOTE] -e flag is used for enumeration.
> -e + enumeration option => -e vp_

- `vp` : Vulnerable plugins
- `ap` : All plugins
- `p` : Popular plugins
- `vt` : Vulnerable themes
- `at` : All themes
- `t` : Popular themes
- `cb` : Config backups (backups file)
- `dbe` : DB exports
- `u` : Grab all the usernames
### Syntax
- --url                     add url 
- - U                       username to try 
-  -P                       passwords to try
- --proxy               scaning proxy server
- --http-auth        scan http auth enabled server
### Examples
- wpscan --url http://192.168.43.12/wordpress/ -e at –e ap –e u
- wpscan --url http://192.168.43.12/wordpress/ -U user.txt -P rockyou.txt
- wpscan --url http://192.168.43.12/wordpress/ --proxy http://192.168.43.12:3333
- wpscan --url http://192.168.43.12/wordpress/ --http-auth robot:123
