README.md
---------
CyPhyTown is a series of programs intended for cyber security education.
Each client/server pair of programs is more secure that the last pair. The
various programs and their high-level specifications are below.

The sequence of programs is starts with a basic client/server application 
and then progressively add new security features, one at a time, with each
new program.  Once a program has been successfully implemented by the
students, the students should then be guided in an assessment of potential
weaknesses of each program and what additions could be added to a "new and 
improved" version of the program.

The intended CyPhyTown sequence of programs, their purpose, and a key 
weakness that motivates the successive CyPhyTown program is as follows:

1) cptClient & cptServer
    Purpose:  Connect two programs running on the same computer
    Weakness: Does not work across a network (ie, on multiple computers)

2) cptRemoteClient & cptRemoteServer
    Purpose:  Connect two programs running on separate computers
    Weakness: Network errors or 'hackers' could corrupt the messages

3) cptIntegClient & cptIntegServer
    Purpose:  Add integrity contrainsts to the network messages, thereby
              detecting network errors and/or changed/hacked messages.
    Weakness: Anyone can send a message, there is no notion of authorized
              users.

4) cptAuthClient & cptAuthServer
    Purpose:  Only allow authorized & authenticated users to sent messages.
    Weakness: Messages are sent in clear/plain text, so they are readable
              by any 'hacker' who can sniff/capture network packets.  This
              means that user names and password are readable by the 
              'hackers'.
              
5) cptConfClient & cptConfServer
    Purpose:  Encrypt messages so that 'hackers' can not read the network
              messages nor discover which users are sending the messages.
    Weakness: Easily breakable algorithms are being used to protect messages.


--------------------------------------------
CyPhyTown Programs and Key File Descriptions
--------------------------------------------

.cptSecretKey
-------------
File in the users home directory that stores the shared, secret key for 
encryption

.cptAuthorizedUsers
------------------
File in the users home directory that stores the user names and passwords of 
authorized users.

cyPhyTown
---------
Python file/module that defines well-known port numbers and the simple message 
digest and encryption functions used.

cptClient & Server
------------------
Basic, starter client/server
Receives simple one-word commands and returns a command acknowledgement
Note:  Server only listens on localhost, won't accept remote connections
Packet format:  <<cmd>>

cptRemoteClient & Server
------------------------
Fairly basic, starter client/server that allows remote connection
Receives simple one-word commands and returns a command acknowledgement
Packet format:  <<cmd>>

cptIntegClient & Server
-----------------------
Remote + packet length and simple error check (parity variant)
Packet format:  <<len|parity|cmd>>

cptAuthClient & Server
----------------------
Integrity + username & password
Packet format:  <<len|parity|user:password:cmd>>
Required file:  .cptAuthorizedUsers

cptConfClient & Server
----------------------
Authorized + simple XOR encryption of username, password, and cmd
Packet format:  <<len|parity|cipherText>>,  
                where cipherText = Encrypt(user:password:cmd)
Required file:  .cptAuthorizedUsers
Required file:  .cptSharedSecretKey
