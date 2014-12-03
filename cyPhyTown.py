"""
cyPhyTown -- Cy(ber) Phy(sical) Town
             Well-known IP port number assignments and helper functions
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


"""
Define well-known IP port numbers to be used by the various cyPhyTown programs
Define the location of required files
"""
CMD_PORT       = 8400
CMD_PORT_INTEG = 8401
CMD_PORT_AUTH  = 8402
CMD_PORT_CONF  = 8404

AUTHORIZED_USERS_FILE = ".cptAuthorizedUsers"
SHARED_SECRED_KEY_FILE = ".cptSharedSecretKey"

    
"""
messageDigest -- very simple, weak message digest
                 For each charger in a string, its ascii value is summed modulo 256
                 and returned as the message digest.
"""
def messageDigest(str):

    md = 0

    for s in str:
        md += ord(s)
    
    return md % 256
   
   
"""
loadSecretKey -- read the shared secret key from a 'hidden' file
           Note: the key is assumed/constrained to be only one-byte long
"""
def loadSecretKey():

    keyFile = open(SHARED_SECRED_KEY_FILE, "r")
    key = keyFile.read(1)               # use only the first byte in the file as the key
    keyFile.close()
    
    return key

    
"""
encrypt -- simple encryption algorithm
           The cipher text string is created by XOR'ing a one-byte key with each
           character of the plaintext string.
"""
def encrypt(plainText, key):
    
    xorKey = ord(key)                   # XOR needs an integer value
    
    cipherText = plainText
    
    for i in range(len(cipherText)):
        cipherText =  "".join(chr(ord(x) ^ xorKey) for x in plainText)
        
    return cipherText
    
    
"""
decrypt -- simple decryption algorithm
           XOR is symmetrical, a second call to encrypt will decrypt the string
           (i.e., for all strings X and Y, X = (Y ^ key) ^ key
"""
def decrypt(cipherText, key):
    
    return encrypt(cipherText, key)

"""
loadAuthorizedUsers -- read in the "database" of user names and passwords into a 
                       python dictionary
"""
def loadAuthorizedUsers():

    authUsers = {}

    with open(AUTHORIZED_USERS_FILE, "r") as userFile:
        for line in userFile:
            user, password = line.split()
            authUsers[user] = password

    return authUsers
            
