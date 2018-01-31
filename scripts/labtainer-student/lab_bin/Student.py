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

# Student.py
# Description: Create a zip file containing the student's lab work
# Also kill any lingering monitored processes

import glob
import json
import os
import subprocess
import sys
import zipfile


def killMonitoredProcess():
    cmd = "ps x -o \"%r %c\" | grep [c]apinout.sh | awk '{print $1}' | uniq"
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    done = False
    print("cmd was %s" % cmd)
    while not done:
        line = child.stdout.readline().strip()
        print('got line %s' % line)
        if len(line)>0:
            cmd = 'kill -TERM -%s' % line
            print('cmd is %s' % cmd)
            os.system(cmd)
        else:
            done = True

def main():
    #print "Running Student.py"
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: Student.py <username> <image_name>\n")
        return 1

    killMonitoredProcess()

    user_name = sys.argv[1]
    container_image = sys.argv[2].split('.')[1]
    StudentHomeDir = os.path.join('/home',user_name)
    HomeLocal= os.path.join(StudentHomeDir, '.local')
    os.chdir(StudentHomeDir)
    student_email_file=os.path.join(HomeLocal, '.email')
    lab_name_file=os.path.join(HomeLocal, '.labname')
    with open(student_email_file) as fh:
        student_email = fh.read().strip()
    with open(lab_name_file) as fh:
        lab_name = fh.read().strip()
    # NOTE: Always store as e-mail+lab_name.zip
    #       e-mail+lab_name.zip will be renamed by stop.py (add containername)
    ZipFileName = '%s.%s.zip' % (student_email.replace("@","_at_"), lab_name)

    #print 'The lab name is (%s)' % LabName
    #print 'Output ZipFileName is (%s)' % ZipFileName
    HomeLocalZip = os.path.join(HomeLocal, 'zip')
    if not os.path.isdir(HomeLocalZip):
        os.makedirs(HomeLocalZip)
    OutputName=os.path.join(HomeLocalZip, ZipFileName)
    TempOutputName=os.path.join("/tmp/", ZipFileName)
    # Remove temp zip file and any zip file in HomeLocal
    if os.path.exists(TempOutputName):
        os.remove(TempOutputName)
    zip_filenames = glob.glob('%s*.zip' % HomeLocalZip)
    for zip_file in zip_filenames:
        #print "Removing %s" % zip_file
        os.remove(zip_file)
    
    # Note: Use /tmp to temporary store the zip file first
    # Create temp zip file and zip everything under StudentHomeDir
    zipoutput = zipfile.ZipFile(TempOutputName, "w")
    udir = "/home/"+user_name
    skip_list = []
    manifest = '%s-home_tar.list' % container_image
    skip_file = os.path.join(udir,'.local','config', manifest)
    if os.path.isfile(skip_file):
        with open(skip_file) as fh:
            for line in fh:
                skip_list.append(line.strip())
    for rootdir, subdirs, files in os.walk(StudentHomeDir):
        newdir = rootdir.replace(udir, ".")
        for file in files:
            savefname = os.path.join(newdir, file)
            #print "savefname is %s" % savefname
            if savefname[2:] not in skip_list:
                try:
                    zipoutput.write(savefname, compress_type=zipfile.ZIP_DEFLATED)
                except:
                    # do not die if ephemeral files go away
                    pass
    zipoutput.close()
   
    os.chmod(TempOutputName, 0666)

    # Rename from temp zip file to its proper location
    os.rename(TempOutputName, OutputName)
    '''
    # Store 'OutputName' into 'zip.flist' 
    zip_fname = os.path.join(HomeLocal, 'zip.flist')
    zip_flist = open(zip_fname, "w")
    zip_flist.write('%s ' % OutputName)
    zip_flist.close()
    os.chmod(zip_fname, 0666)
    '''
    return 0

if __name__ == '__main__':
    sys.exit(main())

