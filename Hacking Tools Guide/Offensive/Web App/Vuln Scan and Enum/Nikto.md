# Basic
-dbcheck			scan database check(do it before scanning)
-h or --host			target specify (URL or IP)
--ssl				scan HTTPS enabled website
--port				specify other ports
-o /path/result			output
-Format				give what format you want in one of these                                                                                    valid onces html txt csv xml msf+ 
# Complex Shit
-Cgidirs all			to scan for the presence of CGI directory(web server executables)
-Display			tell nikto what to show
				1: redirects
				2: cookies recieved
				3: 200/OK responce
				4: URL authntication requirements
				D  Debug output
				V  verbose output

-maxtime			time given by you to scan
				(in seconds) 1,2,3....
-nolookup			to tell not to query for names
-no404				to tell not to query for 404 page
-findonly			scan for port without other apps
-timeout			wait time before execution (Default=10seconds)
-Pause				specify delay b/w each test (using seconds)
-id username:password		to specify id and pass for authentication of target
-tuning				specify the test against target
				
				0: fileupload
				1: interesting files in logs
				2: misconfiguration
				3: information disclosure
				4: XSS/HTML/Script injection
				5: remote file retrival (webroot)
				6: DOS
				7: 5 but (server wide)
				8: remote shell
				9: SQLi


				a: authentication bypass
				b: software identification
				c: remote source inclusion
				x: reverse tuning options
	

--list-plugins			inbuilt plugins
-Plugins (plugin name)		use it
-evasion			evading idea by user
				
				1: random url encoding
				2: directory self reference
				3: premature url ending
				4: prepend long random string
				5: fake parameter
				6: TAB as request spacer
				7: change case of url
				8: use windows directoryseperator



can use msf+ to intergrate it with metasploit framework

