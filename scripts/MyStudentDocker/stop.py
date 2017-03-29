#!/usr/bin/env python

# Filename: stop.py
# Description:
# This is the stop script to be run by the student.
# Note:
# 1. It needs 'start.config' file, where
#    <labname> is given as a parameter to the script.
#

import sys
import labutils

# Usage: stop.py <labname>
# Arguments:
#    <labname> - the lab to stop
def main():
    #print "stop.py -- main"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: stop.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.StopLab(labname, "student")

    return 0

if __name__ == '__main__':
    sys.exit(main())

