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
'''
Utilities for managing Labtainer bases
'''
import os
def getBaseList(skip_exempt=True):
    retval = []
    labtainer_dir= os.getenv('LABTAINER_DIR')
    if labtainer_dir is None:
        print('LABTAINER_DIR not defined, exiting')
        exit(1)
    designer_path = os.path.join(labtainer_dir,'scripts','designer')
    dfile = os.path.join(designer_path, 'base_dockerfiles')
    base_list = os.listdir(dfile)

    exempt_file = os.path.join(designer_path, 'bin', 'exempt.txt')
    exempt_list = []
    with open(exempt_file) as fh:
        for line in fh:
            exempt_list.append(line.strip())
    for base in base_list:
        if base.startswith('Dockerfile'):
            full = os.path.join(dfile, base)

            image_name = base.split('.',1)[1]
            image_ext = image_name.split('.',1)[1]
            #print(image_name) 
            if not skip_exempt or image_name not in exempt_list:
                retval.append(image_name)
    return retval

