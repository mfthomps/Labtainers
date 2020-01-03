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
import subprocess
import os
import sys
def getFrom(dockerfile, registry):
    ''' given a docker file and registry, get the base image name, qualified by the registry '''
    image_name = None
    with open(dockerfile) as fh:
        for line in fh:
            if line.strip().startswith('FROM'):
                parts = line.strip().split()
                image_name = parts[1]
                image_name = image_name.replace("$registry", registry).strip()
                if image_name.endswith('.xtra'):
                    image_name = image_name[:len(image_name)-5]
                break
    ''' Remove xtra suffix if it exists.  We are only interested in the big base '''
    return image_name

def getImageId(image, quiet):
    ''' given an image name, use docker to determine the image ID present on this installation '''
    #cmd = 'docker images | grep %s' % image
    cmd = 'docker images -f=reference="%s:latest" -q ' % image
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        print(output[1].decode('utf-8'))
        exit(1)
    if len(output[0]) > 0:
        return output[0].decode('utf-8').strip()
    elif quiet:
        cmd = 'docker pull %s' % image
        os.system(cmd)
    else:
        print('VersionInfo, getImageId: no image found for %s' % image)
        print('**************************************************')
        print('*  This lab will require a download of           *')
        print('*  several hundred megabytes.                    *')
        print('**************************************************')
        if sys.version_info >=(3,0):
            confirm = str(input('Continue? (y/n)')).lower().strip()
        else:
            confirm = str(raw_input('Continue? (y/n)')).lower().strip()
        if confirm != 'y':
            print('Exiting lab')
            exit(0)
        else:
            print('Please wait for download to complete...')
            cmd = 'docker pull %s' % image
            os.system(cmd)
            print('Download has completed.  Wait for lab to start.')
            return getImageId(image, quiet)

