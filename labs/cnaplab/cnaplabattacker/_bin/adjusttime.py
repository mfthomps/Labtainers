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

    FIX_DATE = "2017-08-03"
    ORIG_TIME = "22:30:36.245616"

    studenttime = sys.argv[1]
    pcapsecond = sys.argv[2]
    addsecond = int(pcapsecond)
    #print "adjusttime.py: studenttime is (%s) pcapsecond is (%s)" % (studenttime, pcapsecond)

    if studenttime == "NONE":
        return 0
    else:
        full_origtime = "%s %s" % (FIX_DATE, ORIG_TIME)
        # Take up to the first 6 digits of student time nanoseconds portion only
        full_studenttime = "%s %s" % (FIX_DATE, studenttime[0:15])
        #print "adjusttime.py: origtime is (%s) studenttime is (%s)" % (full_origtime, full_studenttime)
        origdatetime = datetime.datetime.strptime(full_origtime, "%Y-%m-%d %H:%M:%S.%f")
        studentdatetime = datetime.datetime.strptime(full_studenttime, "%Y-%m-%d %H:%M:%S.%f")
        newdatetime = origdatetime + datetime.timedelta(seconds=addsecond)
        #print origdatetime
        #print studentdatetime
        #print newdatetime
        if newdatetime == studentdatetime:
            return 1
        else:
            return 0

if __name__ == '__main__':
    sys.exit(main())

