#!/usr/bin/env python3

'''
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
'''
# Filename: moreterm.py
# Description:
# This is the script to be run by the student to spawn more terminals.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#
# It will perform the following tasks:
# a. If the lab has only one container, only one terminal for that
#    container will be spawned
# b. If the lab has multiple containers, the number of terminals
#    specified in the start.config will be used, unless
#    the user passed the optional argument specifying the number of
#    terminal

import os
import sys
import ParseStartConfig
import labutils
import LabtainerLogging

LABS_ROOT = os.path.abspath("../../labs/")

def usage():
    sys.stderr.write("Usage: moreterm.py <labname> [<container>] [<clone_number>]\n")
    exit(1)

# Usage: (see usage)
def main():
    num_args = len(sys.argv)
    container = None
    clone_number = None
    if num_args < 2:
        usage()
    elif num_args == 2:
        clone_number = None
        container = sys.argv[1]
    elif num_args == 3:
        if type(sys.argv[2]) is int:
            clone_number = int(sys.argv[2])
            container = sys.argv[1]
        else:
            container = sys.argv[2]
    elif num_args == 4:
        clone_number = int(sys.argv[3])
        container = sys.argv[2]
    else:
        usage()

    labname = sys.argv[1]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.debug("Begin logging moreterm.py for %s lab" % labname)
    lab_path = os.path.join(os.path.abspath('../../labs'), labname)
    labutils.DoMoreterm(lab_path, container, clone_number)

    return 0

if __name__ == '__main__':
    sys.exit(main())

