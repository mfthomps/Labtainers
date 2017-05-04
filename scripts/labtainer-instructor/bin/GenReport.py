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

# GenReport.py
# Description: Create a report based on <labname>.grades.json

import json
import os
import sys

def ValidateLabGrades(labgrades):
    storedlabname = ""
    storedgoalsline = ""
    storedbarline = ""
    fifteenequal = "="*15
    for emaillabname, keyvalue in labgrades.iteritems():
        email, labname = emaillabname.rsplit('.', 1)
        #print "emaillabname is (%s) email is (%s) labname is (%s)" % (emaillabname, email, labname)
        if storedlabname == "":
            storedlabname = labname
        else:
            # Check to make sure labname is the same throughout
            if storedlabname != labname:
                sys.stderr.write("ERROR: inconsistent labname (%s) vs (%s)\n" % (storedlabname, labname))
                sys.exit(1)

        currentgoalsline = ''
        currentbarline = ''

        #print "keyvalue is (%s)" % keyvalue
        for key, value in keyvalue.iteritems():
            #print "key is (%s)" % key
            if key == 'grades':
                # Do 'grades' portion - skip 'parameter' portion for now
                #print "value is (%s)" % value
                for goalid, goalresult in sorted(value.iteritems()):
                    #print "goalid is (%s)" % goalid
                    #print "goalresult is (%s)" % goalresult
                    currentgoalsline = currentgoalsline + ' %15s' % goalid[:15] + ' |'
                    currentbarline = currentbarline + ' %15s' % fifteenequal + ' |'

        if storedbarline == "":
            storedbarline = currentbarline
        if storedgoalsline == "":
            storedgoalsline = currentgoalsline
        else:
            # Check to make sure each student has the same 'goals'
            if storedgoalsline != currentgoalsline:
                sys.stderr.write("ERROR: inconsistent goals (%s) vs (%s)\n" % (storedgoalsline, currentgoalsline))
                sys.exit(1)

    return storedlabname, storedgoalsline, storedbarline

def PrintHeaderGrades(labgrades, labname, goalsline, barline):
    print "Labname %s" % labname
    headerline = '%20s |%s' % ('Student', goalsline)
    print "\n" + headerline
    twentyequal = "="*20
    barline = '%s |%s' % (twentyequal, barline)
    #barlen = len(headerline)
    #bar = "="*barlen
    #print bar
    print barline

    for emaillabname, keyvalue in labgrades.iteritems():
        email, labname = emaillabname.rsplit('.', 1)
        #print "emaillabname is (%s) email is (%s) labname is (%s)" % (emaillabname, email, labname)
        # Get the first 20 characters of the student's e-mail only
        curline = '%20s' % email[:20] + ' |'

        #print "keyvalue is (%s)" % keyvalue
        for key, value in keyvalue.iteritems():
            #print "key is (%s)" % key
            if key == 'grades':
                # Do 'grades' portion - skip 'parameter' portion for now
                #print "value is (%s)" % value
                for goalid, goalresult in sorted(value.iteritems()):
                    #print "goalid is (%s)" % goalid
                    #print "goalresult is (%s)" % goalresult
                    if goalresult:
                        curline = curline + ' %15s' % 'Y' + ' |'
                    else:
                        curline = curline + ' %15s' % '' + ' |'
        print curline


# Usage: GenReport.py <labgradesjsonfile>
# Arguments:
#     <labgradesjsonfile> - <labname>.grades.json filename
def CreateReport(labgradesjsonfile):
    if not os.path.exists(labgradesjsonfile):
        sys.stderr.write("ERROR: missing grades.json file (%s)\n" % labgradesjsonfile)
        sys.exit(1)
    labgradesjson = open(labgradesjsonfile, "r")
    labgrades = json.load(labgradesjson)
    labgradesjson.close()

    #print "Lab Grades JSON is"
    #print labgrades

    labname, goalsline, barline = ValidateLabGrades(labgrades)

    PrintHeaderGrades(labgrades, labname, goalsline, barline)


# Usage: GenReport.py <labgradesjsonfile>
# Arguments:
#     <labgradesjsonfile> - <labname>.grades.json filename
def main():
    #print "Running GenReport.py"
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: GenReport.py <labgradesjsonfile>\n")
        return 1

    labgradesjsonfile = sys.argv[1]

    CreateReport(labgradesjsonfile)

if __name__ == '__main__':
    sys.exit(main())

