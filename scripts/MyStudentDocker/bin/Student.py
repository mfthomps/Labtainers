#!/usr/bin/env python

# Student.py
# Description: Read studentlab.json and create a zip file
#              containing the student lab work

import glob
import json
import os
import sys
import zipfile

UBUNTUHOME="/home/ubuntu/"
HOMELOCAL="/home/ubuntu/.local/"

# Usage: Student.py
# Arguments:
#     None
def main():
    #print "Running Student.py"
    if len(sys.argv) != 1:
        sys.stderr.write("Usage: Student.py\n")
        return 1

    os.chdir(UBUNTUHOME)

    configjsonfname = '%sconfig/%s' % (HOMELOCAL, "studentlab.json")
    configjson = open(configjsonfname, "r")
    studentconfig = json.load(configjson)
    configjson.close()

    #print "Student JSON config is"
    #print studentconfig
    StudentName = studentconfig['studentname']
    StudentHomeDir = studentconfig['studenthomedir']
    LabName = studentconfig['labname']
    StudentIndex = studentconfig['studentid']
    LabIDName = studentconfig['labid']
    ZipFileName = 'student%s.%s.zip' % (StudentIndex, LabIDName)

    #print 'The lab name is (%s)' % LabName
    #print 'Output ZipFileName is (%s)' % ZipFileName

    OutputName=os.path.join(HOMELOCAL, ZipFileName)
    TempOutputName=os.path.join("/tmp/", ZipFileName)
    # Remove temp zip file and any zip file in HOMELOCAL
    if os.path.exists(TempOutputName):
        os.remove(TempOutputName)
    zip_filenames = glob.glob('%s*.zip' % HOMELOCAL)
    for zip_file in zip_filenames:
        #print "Removing %s" % zip_file
        os.remove(zip_file)

    # Note: Use /tmp to temporary store the zip file first
    # Create temp zip file and zip everything under StudentHomeDir
    zipoutput = zipfile.ZipFile(TempOutputName, "w")
    for rootdir, subdirs, files in os.walk(StudentHomeDir):
        newdir = rootdir.replace("/home/ubuntu", ".")
        for file in files:
            savefname = os.path.join(newdir, file)
            #print "savefname is %s" % savefname
            zipoutput.write(savefname, compress_type=zipfile.ZIP_DEFLATED)
    zipoutput.close()

    # Rename from temp zip file to its proper location
    os.rename(TempOutputName, OutputName)
    # Store 'OutputName' into 'zip.flist' 
    zip_fname = '%szip.flist' % HOMELOCAL
    zip_flist = open(zip_fname, "w")
    zip_flist.write('%s ' % OutputName)
    zip_flist.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())

