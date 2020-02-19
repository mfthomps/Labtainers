#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
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
#
# Add preexec hooks to the bash shell to capture stdin & stdout
#
END
MYHOME=$1
if [[ -f $MYHOME/.profile ]]; then
    target=$MYHOME/.profile
    root_target=/root/.profile
elif [[ -f $MYHOME/.bash_profile ]]; then
    target=$MYHOME/.bash_profile
    root_target=/root/.bash_profile
else
    echo "no profile, use .profile anyway?"
    target=$MYHOME/.profile
    root_target=/root/.bash_profile
fi
if grep --quiet startup.sh $target; then
    echo "already hooked" >>/dev/null
else
    #echo "hook not enabled, fix this"
    cat $MYHOME/.local/bin/profile-add >> $target
    echo "export DISPLAY=$DISPLAY" >> $target
    echo "export DISPLAY=$DISPLAY" >> $root_target
    if [[ -f /sbin/capinout ]]; then
        cat $MYHOME/.local/bin/bashrc-add  |  sed 's@PRECMD_HOME_REPLACE_ME@'"$MYHOME"'@' >> $MYHOME/.bashrc
        cat $MYHOME/.local/bin/bashrc-add  |  sed 's@PRECMD_HOME_REPLACE_ME@'"$MYHOME"'@' >> /root/.bashrc
    fi
fi

