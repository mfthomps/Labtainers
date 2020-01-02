#!/usr/bin/env python
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
# Filename: transfer.py
# Description:
# This is the script to be run by the student to transfer file
# to/from the container from/to the host.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#
# It will perform the following tasks:
# a. If 'direction' is not specified, then 'direction' is default to 'TOHOST',
#    i.e., default direction is the transfer is from the container to the host.
# b. If 'direction' is 'TOCONTAINER', then transfer is from host to the container.

import glob
import json
import md5
import os
import re
import subprocess
import sys
import time
import zipfile
import ParseStartConfig
import labutils
import logging
import LabtainerLogging

LABS_ROOT = os.path.abspath("../../labs/")

def usage():
    sys.stderr.write("Usage: transfer.py <labname> <filename> [<container>] [TOHOST|TOCONTAINER]\n")
    exit(1)

# Usage: (see usage)
def main():
    num_args = len(sys.argv)
    print "Number of argument is %d" % num_args
    container = None
    requested_direction = "TOHOST"
    if num_args < 3:
        usage()
    elif num_args == 3:
        container = sys.argv[1]
    elif num_args == 4:
        # Assume the third argument is 'TOHOST|TOCONTAINER'
        requested_direction = sys.argv[3]
        if requested_direction == "TOHOST":
            container = sys.argv[1]
        elif requested_direction == "TOCONTAINER":
            container = sys.argv[1]
        else:
            # If third argument is not 'TOHOST|TOCONTAINER' then
            # it must be the container name
            # and requested_direction defaults to 'TOHOST'
            container = sys.argv[3]
    elif num_args == 5:
        requested_direction = sys.argv[4]
        if requested_direction == "TOHOST":
            container = sys.argv[3]
        elif requested_direction == "TOCONTAINER":
            container = sys.argv[3]
        else:
            usage()
    else:
        usage()

    labname = sys.argv[1]
    filename = sys.argv[2]
    labutils.logger = LabtainerLogging.LabtainerLogging("labtainer.log", labname, "../../config/labtainer.config")
    labutils.logger.info("Begin logging transfer.py for %s lab" % labname)
    labutils.DoTransfer(labname, "student", container, filename, requested_direction)

    return 0

if __name__ == '__main__':
    sys.exit(main())

