#!/bin/bash
"""
cyPhyTown.sh -- Test Script for cyPhyTown programs
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


echo "cyPhyTown Test Script"

echo " "
echo "======= Base Client/Server Case ======="

./cptServer.py 18 &
sPID=$!
sleep 1

./cptClient.py on
sleep 1
kill $sPID &> /dev/null
sleep 1

echo " "
echo "======= Remote Client/Server Case ======="

./cptRemoteServer.py 18 &
rsPID=$!
sleep 1

./cptRemoteClient.py on localhost
sleep 1
kill $rsPID &> /dev/null
sleep 1


echo " "
echo "======= Integrity Client/Server Case ======="

./cptIntegServer.py 18 &
isPID=$!
sleep 1

./cptIntegClient.py on localhost
sleep 1
kill $isPID &> /dev/null
sleep 1


echo " "
echo "======= Authorized Client/Server Case ======="

./cptAuthServer.py 18 &
asPID=$!
sleep 1

./cptAuthClient.py on alice a123 localhost
sleep 1
kill $asPID &> /dev/null
sleep 1


echo " "
echo "======= Confidentiality Client/Server Case ======="

./cptConfServer.py 18 &
csPID=$!
sleep 1

./cptConfClient.py on bob b0b localhost
sleep 1
kill $csPID &> /dev/null
sleep 1



