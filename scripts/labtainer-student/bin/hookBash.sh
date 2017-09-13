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
if grep --quiet bash-pre-capinout.sh $HOME/.profile; then
    echo "already hooked"
else
    echo "source $HOME/.local/bin/bash-preexec.sh" >> $HOME/.profile
    echo "source $HOME/.local/bin/bash-pre-capinout.sh" >> $HOME/.profile
    echo "cd" >> $HOME/.profile
    echo "source $HOME/.local/bin/startup.sh" >> $HOME/.profile
    echo "trap \"source $HOME/.bash_logout\" SIGTERM SIGKILL" >> $HOME/.profile

    echo "history -a" >> $HOME/.bash_logout
fi

