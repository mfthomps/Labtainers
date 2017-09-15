#!/usr/bin/env python
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''

# adjusttime.py
# Description: * This is a sample exec file (Python) for 'execute' goals
#              * This script will take two arguments
#              * 'studenttime' - the time associated with the student
#              * 'parameter.PCAPSECOND' - the parameterized PCAPSECOND
#
# Processing:
# This script has a hard-coded time (original time)
# This script will adjust the hard-coded time with the parameterized PCAPSECOND
# If the studenttime equals the adjusted time, the script returns TRUE
# Otherwise, the script returns FALSE

import os
import sys
import datetime

# Usage: adjusttime.py <studenttime> <pcapsecond>
# Arguments:
#     <studenttime> - the time associated with the student
#     <pcapsecond> - the parameterized PCAPSECOND
def main():
    #print "Running adjusttime.py"
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: adjusttime.py <studenttime> <pcapsecond>\n")
        return 0

    ORIG_FRAME = 190

    student_frame = sys.argv[1]
    start_frame = sys.argv[2]
    subframe = int(start_frame)
    #print "adjusttime.py: studenttime is (%s) pcapsecond is (%s)" % (studenttime, pcapsecond)

    if student_frame == "NONE":
        return 0
    else:
        if ORIG_FRAME - subframe == int(student_frame):
            return 1
        else:
            return 0

if __name__ == '__main__':
    sys.exit(main())

