#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

END
# Assume running from setup_scripts/
#
#  Runs as bash -c argument to gnome-terminal.  unable to get it to inherit bashrc defined env.
#
export TEST_REGISTRY=TRUE
export PATH="${PATH}:./bin:$HOME/labtainer/trunk/scripts/designer/bin:$HOME/labtainer/trunk/testsets/bin"

if [[ ! -f $HOME/.local/share/labtainers/email.txt ]]; then
    echo "frank@beans.com" > $HOME/.local/share/labtainers/email.txt
fi
now=`date +"%s"`
exec > /media/sf_SEED/smokelogs/log-$now.log
exec 2>&1

#Clear out docker.
echo "will destroy docker in 5 seconds"
sleep 5
./destroy-docker.sh -f

# Update baseline and framework
./update-labtainer.sh -t

# Update test sets
./update-testsets.sh
cd ../scripts/labtainer-student
echo "start smoke test"
smoketest.py -r
RESULT=$?
if [ $RESULT !=0 ]; then
    echo "smoke test failed"
    exit 1
fi
build_lab_test.sh
RESULT=$?
if [ $RESULT !=0 ]; then
    echo "build_lab_test failed"
    exit 1
fi
sudo poweroff
