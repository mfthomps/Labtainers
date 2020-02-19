#!/usr/bin/env bash
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
END
# parameterize.sh
#
exec &> /tmp/parameterize.sh.log
echo "start parameterize.sh"
date
if [[ -d /var/labtainer/did_param ]]; then
	echo "Already parameterized, exit"
	exit 0
fi
# Configuration variables
LAB_SEEDFILE="$HOME/.local/.seed"
USER_EMAILFILE="$HOME/.local/.email"
LAB_NAMEFILE="$HOME/.local/.labname"
WATERMARK_NAMEFILE="$HOME/.local/.watermark"
LAB_PARAMCONFIGFILE="$HOME/.local/config/parameter.config"

# Do not display instruction during parameterization
LOCKDIR=/tmp/.mylockdir
mkdir "$LOCKDIR" >/dev/null 2>&1

#echo "number of argument is $#"
#echo "argument is $@"

if [ $# -ne 8 ]
then
    echo "Usage: parameterize.sh <CONTAINER_USER> <LAB_INSTANCE_SEED> <USER_EMAIL> <LAB_NAME> <CONTAINER_NAME>"
    echo "       <CONTAINER_USER> -- username of the container"
    echo "       <CONTAINER_PASSWORD> -- password for username of the container"
    echo "       <LAB_INSTANCE_SEED> -- laboratory instance seed"
    echo "       <USER_EMAIL> -- user's e-mail"
    echo "       <LAB_NAME> -- name of the lab"
    echo "       <CONTAINER_NAME> -- name of the container"
    echo "       <version> -- version of container image"
    echo "       <host_display> -- host DISPLAY env variable"
    exit 1
fi

CONTAINER_USER=$1
CONTAINER_PASSWORD=$2
LAB_INSTANCE_SEED=$3
USER_EMAIL=$4
LAB_NAME=$5
CONTAINER_NAME=$6
IMAGE_VERSION=$7
HOST_DISPLAY=$8
echo "email and watermark"
date
# Laboratory instance seed is always stored in $LAB_SEEDFILE
echo "$LAB_INSTANCE_SEED" > $LAB_SEEDFILE
# User's e-mail is always stored in $USER_EMAILFILE
echo "$USER_EMAIL" > $USER_EMAILFILE
echo "$LAB_NAME" > $LAB_NAMEFILE
echo "" > $WATERMARK_NAMEFILE

# fix ownship of system file from _system directory.  Docker!
#previous_match_string=""
while read f;do
    fname=${f:1}
    IFS='/' read -r -a mystring <<< "$fname"
    if [[ ${mystring[1]} == var ]]; then
        continue
    fi
    # chmod on a lot of files, even recursively, takes forever on a container
    #if [[ ${mystring[1]} == var ]] && [[ ${#mystring[@]} -eq 4 ]]; then
    #    previous_match_string=("${mystring[@]}")
    #else
    #    if [[ ${mystring[1]} == var ]] && [[ ${mystring[2]} == ${previous_match_string[2]} ]] && [[ ${mystring[3]} == ${previous_match_string[3]} ]]; then
    #        continue
    #    fi
    #fi
    echo $CONTAINER_PASSWORD | sudo -S chown root:root $fname
done < $HOME/.local/sys_manifest.list
if [[ -f /etc/sudoers.new ]]; then
    # Docker!
    echo $CONTAINER_PASSWORD | sudo -S mv /etc/sudoers.new /etc/sudoers
fi

echo $CONTAINER_PASSWORD | sudo rm -f /run/nologin

# call ParameterParser.py (passing $LAB_INSTANCE_SEED)
echo $CONTAINER_PASSWORD | sudo -S $HOME/.local/bin/ParameterParser.py $CONTAINER_USER $LAB_INSTANCE_SEED $CONTAINER_NAME $LAB_PARAMCONFIGFILE 
echo "back from ParameterParser.py"
date
# If file $HOME/.local/bin/fixlocal.sh exists, run it
if [ -f $HOME/.local/bin/fixlocal.sh ]
then
    if [[ $EUID -ne 0 ]]; then
        $HOME/.local/bin/fixlocal.sh $CONTAINER_PASSWORD $CONTAINER_USER 2>>/tmp/fixlocal.output
    else
        su -c "$HOME/.local/bin/fixlocal.sh $CONTAINER_PASSWORD $CONTAINER_USER 2>>/tmp/fixlocal.output" $CONTAINER_USER
    fi
fi
echo "back from fixlocal.sh"
date
# keep rsyslog from hanging 10 seconds on the xconsole
if [ -f /etc/rsyslog.d/50-default.conf ]; then
   echo $CONTAINER_PASSWORD | sudo -S sed -i '/^daemon...mail/,+3 d' /etc/rsyslog.d/50-default.conf
fi

if [ -f /var/tmp/home.tar ]; then
   cd $HOME
   tar tvf /var/tmp/home.tar > $HOME/.local/config/mytar_list.txt
   tar xf /var/tmp/home.tar 
   echo $CONTAINER_PASSWORD | sudo -S rm /var/tmp/home.tar
   echo "expanded /var/tmp/home.tar to $HOME" >>/tmp/parameterize.out 2>&1
fi
echo "back from expand hometar.sh"
date

export DISPLAY=$HOST_DISPLAY
echo $CONTAINER_PASSWORD | sudo -S $HOME/.local/bin/hookBash.sh $HOME 2>>/tmp/hookBash.output

# restore the apt/yum sources (if not done already)
export APT_SOURCE=NO
if [ -f /usr/bin/yum-source.sh ]; then
    echo $CONTAINER_PASSWORD | sudo -S /usr/bin/yum-source.sh
fi
if [ -f /usr/bin/apt-source.sh ]; then
    echo $CONTAINER_PASSWORD | sudo -S /usr/bin/apt-source.sh
fi

# hack for centos6 gui's
if [ -f /bin/dbus-uuidgen ]; then
    echo $CONTAINER_PASSWORD | sudo -S /bin/dbus-uuidgen > /var/lib/dbus/machine-id
fi

# hack console type for initd
echo $CONTAINER_PASSWORD | sudo touch /sbin/consoletype
echo $CONTAINER_PASSWORD | sudo chmod a+rwx /sbin/consoletype
echo "image version is $IMAGE_VERSION" >/tmp/mft.out
# just for ubuntu, tbd limit to that?
touch ~/.sudo_as_admin_successful

if [ -d $LOCKDIR ]; then
    rmdir $LOCKDIR
fi
# Indicate the container has been parameterized
PERMLOCKDIR=/var/labtainer/did_param
echo $CONTAINER_PASSWORD | sudo -S mkdir -p "$PERMLOCKDIR" 
echo "done with parameterize.sh"
date
echo "do mynotify service"
date
if [[ "$IMAGE_VERSION" -eq -1 ]] || [[ "$IMAGE_VERSION" -gt 2 ]]; then
    systemctl enable mynotify.service
    systemctl start mynotify.service
fi
echo "back from mynotify service"
date

