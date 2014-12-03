#!/usr/bin/python3
"""
cptConfServer.py -- simple program to send a single command (string) to a server.
                    The command ack/reply status is printed out to the user.
"""

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


import socket
import sys
import cyPhyTown

"""
parseArgs -- parse the program's command line arguments
"""
def parseArgs(argv):

    if len(argv) >= 4:      # program name is included in the argument count
        cmd  = argv[1]
        port = cyPhyTown.CMD_PORT_CONF  # use the default port #
        user     = argv[2]
        password = argv[3]
        if len(argv) >= 5:
            host = argv[4]
        else:
            host = "localhost"
    else:
        print("Error: missing command line arguments")
        print("Usage:", argv[0], "command userName password [host]")
        sys.exit(1)

    return host, port, cmd, user, password
   
    
"""
cptConfClient -- send a command to a server & print the reply status
"""
def cptConfClient(argv):

    host, port, cmd, user, password = parseArgs(argv)
    
    # connect to Server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    
    key = cyPhyTown.loadSecretKey()
    
    authCmd = "{0}:{1}:{2}".format(user, password, cmd)
    
    # convert cmd to its integrity variant (format:  len|md|cmd
    pktStr = "{0}|{1}|{2}".format(len(authCmd), cyPhyTown.messageDigest(authCmd), authCmd)
    
    print(" Sending:", pktStr)
    
    cipherPktStr = cyPhyTown.encrypt(pktStr, key)
    print("Encrypted:", cipherPktStr)
    
    sent = s.sendall(cipherPktStr.encode())        # send message string
    if sent == 0:
        raise RuntimeError("Socket connection broken")
    s.shutdown(socket.SHUT_WR)

    cipherAckPacket = s.recv(1024)                 # receive the server's response
    
    cipherAckStr = cipherAckPacket.decode()
    ackStr = cyPhyTown.decrypt(cipherAckStr, key)   # decrypt the response before continuing
    
    try:
        lenStr, mdStr, ackCmd = ackStr.split('|')
        lenCmd = int(lenStr)
        md = int(mdStr)
        if ((lenCmd == len(ackCmd)) and (cyPhyTown.messageDigest(ackCmd) == md)):
            print("Response:", ackCmd)
        else:
            print("Response: -- ERROR --")
    except:
        print("ERROR")
            
    # All done, close the network connection
    s.close()


if __name__ == "__main__":
    cptConfClient(sys.argv)
