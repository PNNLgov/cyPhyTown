cyPhyTown-Readme.txt
--------------------

# Copyright (c) 2014, Battelle Memorial Institute
# All rights reserved.
# 
# 1.	Battelle Memorial Institute (hereinafter Battelle) hereby
# grants permission to any person or entity lawfully obtaining a copy
# of this software and associated documentation files (hereinafter “the
# Software”) to redistribute and use the Software in source and binary
# forms, with or without modification.  Such person or entity may use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and may permit others to do so, subject to
# the following conditions:
# •	Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimers. 
# •	Redistributions in binary form must reproduce the above
#     copyright notice, this list of conditions and the following
#     disclaimer in the documentation and/or other materials provided
#     with the distribution. 
# •	Other than as used herein, neither the name Battelle Memorial
#     Institute or Battelle may be used in any form whatsoever without
#     the express written consent of Battelle.  
# 
# 2.	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL BATTELLE OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# 
# PACIFIC NORTHWEST NATIONAL LABORATORY
# operated by
# BATTELLE
# for the
# UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# 
# -------
# 
# The Software was produced by Battelle under Contract No.
# DE-AC05-76RL01830 with the Department of Energy.  The U.S. Government 
# is granted for itself and others acting on its behalf a nonexclusive,
# paid-up, irrevocable worldwide license in this data to reproduce,
# prepare derivative works, distribute copies to the public, perform
# publicly and display publicly, and to permit others to do so.  The
# specific term of the license can be identified by inquiry made to
# Battelle or DOE.  NEITHER THE UNITED STATES NOR THE UNITED STATES
# DEPARTMENT OF ENERGY, NOR ANY OF THEIR EMPLOYEES, MAKES ANY WARRANTY,
# EXPRESS OR IMPLIED, OR ASSUMES ANY LEGAL LIABILITY OR RESPONSIBILITY FOR
# THE ACCURACY, COMPLETENESS OR USEFULNESS OF ANY DATA, APPARATUS, PRODUCT
# OR PROCESS DISCLOSED, OR REPRESENTS THAT ITS USE WOULD NOT INFRINGE
# PRIVATELY OWNED RIGHTS.

----------------
cyPhyTown-Readme
----------------
cyPhyTown is a series of programs intended for cyber security education.
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
