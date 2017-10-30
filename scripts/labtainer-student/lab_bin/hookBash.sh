#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
#
# Add preexec hooks to the bash shell to capture stdin & stdout
#
END
if [[ -f $HOME/.profile ]]; then
    target=$HOME/.profile
elif [[ -f $HOME/.bash_profile ]]; then
    target=$HOME/.bash_profile
else
    echo "no profile, use .profile anyway?"
    target=$HOME/.profile
fi
if grep --quiet startup.sh $target/.profile; then
    echo "already hooked" >>/dev/null
else
    #echo "hook not enabled, fix this"
    cat $HOME/.local/bin/profile-add >> $target
    cat $HOME/.local/bin/bashrc-add  |  sed 's@PRECMD_HOME_REPLACE_ME@'"$HOME"'@' >> $HOME/.bashrc
    cat $HOME/.local/bin/bashrc-add  |  sed 's@PRECMD_HOME_REPLACE_ME@'"$HOME"'@' >> /root/.bashrc
fi

