# TIES323
Solutions for the JYU TIES323 Sovellusprotokollat-course.

## Mail Protocols:

Extra features:
* POP3 client <-> server communications are secured with SSL. 
* This requires following certs to be created:
* Use TIES323 as the common name.
  * Client-side certs to /MailProtocols/
     ```openssl req -new -newkey rsa:2048 -days 1 -nodes -x509 -keyout client.key -out client.crt```
  * Server-side certs to /MailProtocols/Main/
     ```openssl req -new -newkey rsa:2048 -days 1 -nodes -x509 -keyout server.key -out server.crt```
