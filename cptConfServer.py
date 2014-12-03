#!/usr/bin/python3
"""
cptConfServer -- server that accepts confidential control messages from authorized users
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
try:
    import RPi.GPIO as GPIO         # Using a Raspberry Pi
except:
    import mockRPiGPIO as GPIO      # Not on a Raspberry Pi, make do with mocked stubs
    
    
"""
parseArgs -- parse the program's command line arguments
"""
def parseArgs(argv):

    if len(argv) >= 2:          # include program name in the count of arguments
        port    = cyPhyTown.CMD_PORT_CONF   # use the default port #
        gpioPin = int(argv[1])
    else:
        print("Error: missing command line arguments")
        print("Usage:", argv[0], "gpioPin")
        sys.exit(1)

    return port, gpioPin
   
    
"""
doCmd -- perform the command function
"""
def doCmd(rawPacket):
    global cmdLED
    global authorizedUsers
    global secretKey
    
    cipherPkt = rawPacket.decode()          # client message should be a cipher text string
    print("cipherPkt:", cipherPkt)
    
    pkt = cyPhyTown.decrypt(cipherPkt, secretKey)   # packet is now a simple, plaintext string
    print(" plainPkt:", pkt)                        # status printout, not needed
    
    try:
        lenCmd, mdStr, authCmd = pkt.split('|')
        if ((int(lenCmd) == len(authCmd)) and (cyPhyTown.messageDigest(authCmd) == int(mdStr))):
            print("Received:", authCmd)
        else:
            print("Received: -- ERROR --")
    except:
        print("ERROR -- Bad packet")

    userAuthorized = False
    try:
        user, password, cmd = authCmd.split(':')
        if (user,password) in authorizedUsers.items():
            userAuthorized = True
        else:
            print("ERROR -- Unauthorized User")
    except:
        print("ERROR -- Could not authorized User")
        
    if userAuthorized:
        if cmd in ["on", "On", "ON"]:
            ackMsg = "ACK:" + cmd
            GPIO.output(cmdLED, True)
        elif cmd in ["off", "Off", "OFF"]:
            ackMsg = "ACK:" + cmd
            GPIO.output(cmdLED, False)
        else:
            ackMsg = "NACK"
    else:
        ackMsg = "ERROR -- Unauthorized User"
                
    ackPacket = "{0}|{1}|{2}".format(len(ackMsg), cyPhyTown.messageDigest(ackMsg), ackMsg)
    
    cipherAckPacket = cyPhyTown.encrypt(ackPacket, secretKey)  # need to encrypt the ACK message

    print("ackPacket:", cipherAckPacket)        # status printout, not needed
    return cipherAckPacket


"""
cptConfServer -- receive an encrypted command and return an encrypted reply status
"""
def cptConfServer(argv):
    global cmdLED
    global authorizedUsers
    global secretKey
    
    port, gpioPin = parseArgs(argv)
    
    # read in the authorized users & secret key
    authorizedUsers = cyPhyTown.loadAuthorizedUsers()
    secretKey       = cyPhyTown.loadSecretKey()
    
    # create an inbound socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))  # empty hostname enables binding to localhost and LAN addresses
    
    # configure/setup the Raspberry Pi GPIO hardware
    cmdLED = gpioPin
    GPIO.setmode(GPIO.BOARD)            # BOARD uses Pin numbers, BCM uses GPIO ID#s
    GPIO.setup(cmdLED, GPIO.OUT)
    GPIO.output(cmdLED, False)          # start with the LED off
    
    while 1:
        s.listen(1)                     # listen for potential client connections
        conn, addr = s.accept()         # accept the client's connection
        print("client is at", addr)
    
        rawPacket = conn.recv(1024)     # assume client packet < 1024 characters long
        while (len(rawPacket) > 0):
            ackMsg = doCmd(rawPacket)
            conn.send(ackMsg.encode())
            
            rawPacket = conn.recv(1024) # check for another client message
            
        conn.close()

    # All done, close the network connection
    s.close()


if __name__ == "__main__":
    cptConfServer(sys.argv)
