'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public domain 
and is not subject to copyright. 
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
import os
'''
Get lists of labs, accounting for lab versions to only get the latest
version of a lab.  Also accounts for the distrib/skip-list.
'''
def getLabVersion(path):
    if os.path.isfile(path):
        with open(path) as fh:
            line = fh.read().strip()
            lname, version = line.split()
        return lname, version
    return None, None

def getVerList(dirs, path):
    vlist = {}
    for lab in sorted(dirs):
        lpath = os.path.join(path, lab, 'config', 'version')
        lname, version = getLabVersion(lpath)
        if lname is not None: 
            if lname not in vlist:
                vlist[lname] = {}
            vlist[lname][lab] = int(version)
    return vlist

def showLabs(dirs, path, versions, skip):
    description = ''
    description += 'Start a Labtainers lab\n'
    description+="List of available labs:\n\n"
    for loc in sorted(dirs):
        if loc in skip: 
            continue
        versionfile = os.path.join(path, loc, "config", "version")
        lname, dumb = getLabVersion(versionfile)
        aboutfile = None
        if lname is None or isLatestVersion(versions[lname], loc):
            description = description+'\n  '+loc
            aboutfile = os.path.join(path, loc, "config", "about.txt")
           
        if aboutfile is not None and os.path.isfile(aboutfile):
            description += ' - '
            with open(aboutfile) as fh:
                for line in fh:
                    description += line
        else:
            description += "\n"
            #sys.stderr.write(description)
    pydoc.pager(description)
    print('Use "-h" for help.')

def isLatestVersion(versions, lab):
    if versions is not None:
        if lab in versions:
            this_version = versions[lab]
            for l in versions:
               if versions[l] > this_version:
                   if not hasLabInstalled(lab):
                       return False
    return True

def hasLabInstalled(lab):
    here = os.getcwd()
    if 'instructor' not in here:
        cmd = 'docker ps -a | grep %s' % lab
        ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[0]) > 0: 
            for line in output[0].decode('utf-8').splitlines():
                print(line)
                name = line.split()[1]
                thislab = os.path.basename(name.split('.')[0])
                if thislab == lab:
                    return True
    return False

def getList(dirs, path, versions, skip):
    retval = []
    for loc in sorted(dirs):
        if loc in skip: 
            continue
        versionfile = os.path.join(path, loc, "config", "version")
        lname, dumb = getLabVersion(versionfile)
        if lname is None or isLatestVersion(versions[lname], loc):
            retval.append(loc)
    return retval

def getLabs():
    labtainer_dir = os.getenv('LABTAINER_DIR')
    lab_path = os.path.join(labtainer_dir, 'labs')
    labdirs = os.listdir(lab_path) 
    versions = getVerList(labdirs, lab_path)
    skip_labs = os.path.join(labtainer_dir, 'distrib', 'skip-labs')
    skip = []
    if os.path.isfile(skip_labs):
        with open(skip_labs) as fh:
            for line in fh:
                f = os.path.basename(line).strip()
                skip.append(f)
    return getList(labdirs, lab_path, versions, skip)
