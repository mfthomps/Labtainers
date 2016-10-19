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
    SaveDirName = studentconfig['savedirectory']
    ZipFileName = 'student%s.%s.zip' % (StudentIndex, LabIDName)

    #print 'The lab name is (%s)' % LabName
    #print 'Output ZipFileName is (%s)' % ZipFileName

    OutputName=os.path.join(HOMELOCAL, ZipFileName)
    zipoutput = zipfile.ZipFile(OutputName, "w")

    flist = os.listdir(StudentHomeDir)

    # Go back to StudentHomeDir
    os.chdir(StudentHomeDir)

    for fname in flist:
        #print "fname is (%s)" % fname
        if fname in SaveDirName:
            savedirlist = os.listdir(fname)
            for sname in savedirlist:
                savefname = fname + '/' + sname
                #print "Savefname is %s" % savefname
                if os.path.isfile(savefname):
                    zipoutput.write(savefname, compress_type=zipfile.ZIP_DEFLATED)
        else:
            #print "skipping (%s)" % fname
            pass
        
    zipoutput.close()

    # Get a list of filenames that ends with '.zip'
    zip_fname = '%szip.flist' % HOMELOCAL
    zip_filenames = glob.glob('%s*.zip' % HOMELOCAL)
    zip_flist = open(zip_fname, "w")
    for zip_file in zip_filenames:
        zip_flist.write('%s ' % zip_file)
    zip_flist.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())

