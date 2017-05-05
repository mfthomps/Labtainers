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

fifteenequal = "="*15
twentyequal = "="*20
goalprintformat = ' %15s |'
emailprintformat = '%20s |'

def ValidateLabGrades(labgrades):
    storedlabname = ""
    storedgoalsline = ""
    storedbarline = ""
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
                    currentgoalsline = currentgoalsline + goalprintformat % goalid[:15]
                    currentbarline = currentbarline + goalprintformat % fifteenequal

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

def PrintHeaderGrades(gradestxtfile, labgrades, labname, goalsline, barline):

    gradestxtouput = open(gradestxtfile, "w")
    headerline = emailprintformat % 'Student' + goalsline
    barline = emailprintformat % twentyequal + barline
    gradestxtouput.write("Labname %s" % labname)
    gradestxtouput.write("\n\n" + headerline + "\n" + barline + "\n")

    for emaillabname, keyvalue in labgrades.iteritems():
        email, labname = emaillabname.rsplit('.', 1)
        #print "emaillabname is (%s) email is (%s) labname is (%s)" % (emaillabname, email, labname)
        # Get the first 20 characters of the student's e-mail only
        curline = emailprintformat % email[:20]

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
                        curline = curline + goalprintformat % 'Y'
                    else:
                        curline = curline + goalprintformat % ''
        gradestxtouput.write(curline + "\n")

    gradestxtouput.close()

# Usage: CreateReport <gradesjsonfile> <gradestxtfile>
# Arguments:
#     <gradesjsonfile> - This is the input file <labname>.grades.json
#     <gradestxtfile> - This is the output file <labname>.grades.txt
def CreateReport(gradesjsonfile, gradestxtfile):
    if not os.path.exists(gradesjsonfile):
        sys.stderr.write("ERROR: missing grades.json file (%s)\n" % gradesjsonfile)
        sys.exit(1)
    labgradesjson = open(gradesjsonfile, "r")
    labgrades = json.load(labgradesjson)
    labgradesjson.close()

    #print "Lab Grades JSON is"
    #print labgrades

    labname, goalsline, barline = ValidateLabGrades(labgrades)

    PrintHeaderGrades(gradestxtfile, labgrades, labname, goalsline, barline)


# Usage: GenReport.py <gradesjsonfile> <gradestxtfile>
# Arguments:
#     <gradesjsonfile> - This is the input file <labname>.grades.json
#     <gradestxtfile> - This is the output file <labname>.grades.txt
def main():
    #print "Running GenReport.py"
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: GenReport.py <gradesjsonfile> <gradestxtfile>\n")
        return 1

    gradesjsonfile = sys.argv[1]
    gradestxtfile = sys.argv[2]
    CreateReport(gradesjsonfile, gradestxtfile)

if __name__ == '__main__':
    sys.exit(main())

