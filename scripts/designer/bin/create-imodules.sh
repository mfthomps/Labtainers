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

Create an imodule.tar containing all labs that are within the local
git repository.  NOTE: it is intended that this git repository be distinct
from the Labtainers repos.  The top of the repo should be the labs directory,
and it should only contain changed files.
END
distrib_dir=$LABTAINER_DIR/distrib
cd $LABTAINER_DIR/labs
rootdir=`pwd`
ddir=/tmp/labtainer-distrib
ldir=$ddir/labtainer
ltrunk=$ldir/trunk
scripts=$ltrunk/scripts
labs=$ltrunk/labs
rm -fr /$ddir
mkdir $ddir
mkdir $ldir
mkdir $ltrunk
mkdir $labs
branch=$(git rev-parse --abbrev-ref HEAD)
llist=$(git ls-files . | cut -d '/' -f 1 | uniq)
here=`pwd`
for lab in $llist; do
    echo "lab is $lab"
        config=$(git ls-files $lab | grep config)
        if [[ ! -z "$config" ]]; then
            $distrib_dir/fix-git-dates.py $lab/config $labs $branch
        fi
        instr_config=$(git ls-files $lab | grep instr_config)
        if [[ ! -z "$instr_config" ]]; then
            $distrib_dir/fix-git-dates.py $lab/instr_config $labs $branch
        fi
        docs=$(git ls-files $lab | grep docs)
        if [[ ! -z $docs ]]; then
            echo "Do docs"
            $distrib_dir/fix-git-dates.py $lab/docs $labs $branch
            cd $labs/$lab/docs
	    if [[ ! -f ./Makefile ]]; then
		    # use distrubuted Makefile
		    cp $here/$lab/docs/Makefile . 2>/dev/null 
            fi

	    if [[ -f ./Makefile ]]; then
                make
	    fi
            cd $here
            
        fi
        bin=$(git ls-files $lab | grep /bin)
        if [[ ! -z $bin ]]; then
            $distrib_dir/fix-git-dates.py $lab/bin $labs $branch
        fi
done
cd $labs
tar -cz -f $LABTAINER_DIR/imodule.tar .
echo "*********************************************************"
echo "**  Post $LABTAINER_DIR/imodule.tar to your web server **"
echo "*********************************************************"
