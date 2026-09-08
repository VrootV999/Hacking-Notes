## sqlmap
-u                               URL
id=5                           parameter for sql injection(1-5)
--random-agent		   for not getting bloacked by waf
-v                               for verbosity 0-6 lvl
-g			                   google dork the target url
--proxy			           use proxy to connect
--tor			               use tor for annonimity
--check-tor		      check tor status
--level			              level of test(1-5)
--risk			              risk of the test(1-5)
-r  

## enumeration

-a				                    all
-b				                    DBMS banner
--current-user			    DBMS current user
--current-db			        DBMS current DB
--passwords			        enumerate user password hashes
--dbs				                enumerate DBMS databases
--tables			                enumerate DBMS tables
--schema			            enumerate DBMS columns
--dump				           dump table entries in database
--dump-all			           dump all entries in database
-T users			              user tables

## access

--os-shell	                  shell of the O.S
--os-pwn	                  OOB shell

## general

--flush session		       flush the session files of target

--wizard		                   if you are a fucking noob

