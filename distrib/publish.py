#!/usr/bin/env python3
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
import sys
import os
import subprocess
import shlex
import argparse
sys.path.append('../scripts/labtainer-student/bin')
import LabtainerLogging
import ParseLabtainerConfig
import labutils
import VersionInfo
import removelab
import registry
import InspectLocalReg
import rebuild
'''
Build and publish labtainer images.  Use -h option for help.
'''
def relabel(image, version, base_image, base_id, registry, logger):
    with open('./dfile', 'w') as fh:
        fh.write('FROM %s\n' % image)
        fh.write('ARG version\n')
        fh.write('LABEL version=%s\n' % version)
        fh.write('LABEL base=%s.%s' % (base_image, base_id))

    cmd = 'docker build -f dfile -t %s.tmp .' % image
    os.system(cmd)
    '''
    Do two pushes, one for the default image, the other with a base image tag for
    retrieval by instances that do not have the appropriate base.
    '''
    cmd = 'docker tag %s.tmp %s/%s' % (image, registry, image)
    #print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s' % (registry, image)
    #print cmd
    os.system(cmd)
    cmd = 'docker tag %s.tmp %s/%s:base_image%s' % (image, registry, image, base_id)
    #print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s:base_image%s' % (registry, image, base_id)
    #print cmd
    os.system(cmd)

def doRebuild(labname, labsdir, force, no_build, logger):
    mycwd = os.getcwd()
    path = '../scripts/labtainer-student'
    os.chdir(path)
    #print('now at %s' % os.getcwd())
    lab_dir = os.path.join(labsdir, labname)
    #print('cwd was %s now %s  lab_dir is %s' % (mycwd, os.getcwd(), lab_dir))
    retval = rebuild.DoRebuildLab(lab_dir, force_build=force, no_build=no_build, no_pull=True, use_cache=False)
    os.chdir(mycwd)
    return retval

def pushImage(lab, docker_dir, registry_info, logger):
    '''
    Set the label and tags on any newly built image and push it to the given registry.
    '''
    did_one = False
    for ri in registry_info:
        df = 'Dockerfile.%s.%s.student' % (lab, ri.name)
        dfile_path = os.path.join(docker_dir,df)
        image_base = VersionInfo.getFrom(dfile_path, ri.base_registry)
        base_id = VersionInfo.getImageId(image_base, True)
        framework_version = labutils.framework_version
        relabel(ri.image_name, framework_version, image_base, base_id, ri.registry, logger)
        logger.debug('Did relabel of %s using base_id %s' % (ri.image_name, base_id))
        did_one = True
            
    ''' Delete the lab images. Two reasons: 1) ensure we run registry or dockerHub copy,
    2) don't push on a rebuild if not rebuilt. '''
    if did_one:
        removelab.removeLab(lab)

def pushIt(lab, docker_dir, registry, base_registry, logger):
    '''
    Set the label and tags on any newly built image and push it to the given registry.
    '''
    df_list = [f for f in os.listdir(docker_dir) if os.path.isfile(os.path.join(docker_dir, f))]
    did_one = False
    for df in df_list:
        if df.endswith('.swp'):
            continue
        logger.debug('tag and push %s' % df)
        try:
            parts = df.split('.')
            image = '%s.%s.student' % (parts[1], parts[2])
        except:
            logger.error('could not get image from %s' % df);
            continue
        image_exists, dumb, dumb1 = labutils.ImageExists(image, None)
        if image_exists:
            dfile_path = os.path.join(docker_dir,df)
            image_base = VersionInfo.getFrom(dfile_path, base_registry)
            base_id = VersionInfo.getImageId(image_base, True)
            framework_version = labutils.framework_version
            relabel(image, framework_version, image_base, base_id, registry, logger)
            logger.debug('Did relabel of %s using base_id %s' % (image, base_id))
            did_one = True
        else: 
            logger.debug('Have not built %s, nothing to push' % image)
    ''' Delete the lab images. Two reasons: 1) ensure we run registry or dockerHub copy,
    2) don't push on a rebuild if not rebuilt. '''
    if did_one:
        removelab.removeLab(lab)

def DoLab(lab, labsdir, force, logger, do_login, use_default_registry, default_registry, no_build=False):
    logger.debug('DoLab for %s' % lab)
    if not no_build:
        removelab.removeLab(lab)
    lab_dir = os.path.join(labsdir, lab)
    registry_info = doRebuild(lab, labsdir, force, no_build, logger)
    registry = None
    for ri in registry_info:
        if registry is not None and ri.registry != registry:
            logger.error('no current support for images from multiple registries, got %s and %s' % (ri.registry, registry))
            exit(1)
        else:
            registry = ri.registry
    logger.debug('Back from rebuild with registry of %s' % registry)
    if not no_build and registry is not None:
        ''' should we login?  Never if test registry '''
        if use_default_registry:
            if registry != default_registry:
                print('registry %s not equal %s, login' % (registry, default_registry))
                os.system('docker login')
            else:
                registry = default_registry
                if do_login:
                    os.system('docker login')
        docker_dir = os.path.join(labsdir, lab, 'dockerfiles')
        #pushIt(lab, docker_dir, registry, base_registry, logger)
        pushImage(lab, docker_dir, registry_info, logger)

def main():
    src_path = '../'
    labtainer_config_file = os.path.join(src_path, 'config', 'labtainer.config')
    logger = LabtainerLogging.LabtainerLogging("/tmp/labtainer-publish.log", 'publish', labtainer_config_file)
    labutils.logger = logger

    parser = argparse.ArgumentParser(description='Build the images labs and publish to a registry')
    parser.add_argument('-l', '--lab', action='store', help='build and publish just this lab')
    parser.add_argument('-s', '--start', action='store', help='all labs starting with this one')
    parser.add_argument('-d', '--default_registry', action='store_true', default=False, help='build and publish with default registry -- instead of the typical test registry')
    parser.add_argument('-f', '--force', action='store_true', default=False, help='force rebuild of all images')
    parser.add_argument('-n', '--no_build', action='store_true', default=False, help='Do not rebuild, just report on what would be built')
    parser.add_argument('-q', '--quiet', action='store_true', default=False, help='Do not prompt user for ok')
    args = parser.parse_args()
    if not args.default_registry:
        if os.getenv('TEST_REGISTRY') is None:
            #print('use putenv to set it')
            os.putenv("TEST_REGISTRY", "TRUE")
            ''' why does putenv not set the value? '''
            os.environ['TEST_REGISTRY'] = 'TRUE'
        else:
            #print('exists, set it true')
            os.environ['TEST_REGISTRY'] = 'TRUE'
        branch, test_registry = registry.getBranchRegistry()
        print('Using test registry %s' % test_registry)
        ok = InspectLocalReg.checkRegistryExists(test_registry, logger)
        if not ok:
            print('Default is to use a test registry, which does not seem to exist.  Use -d option to force publishing directly to Docker Hub')
            exit(1)
    else:
        if os.getenv('TEST_REGISTRY') is not None:
            print('Request to use default registry, but TEST_REGISTRY is set.  Unset that first.')
            exit(1)

    skip_labs = 'skip-labs'

    skip = []
    with open(skip_labs) as fh:
        for line in fh:
            f = os.path.basename(line).strip()
            print('adding [%s]' % f)
            skip.append(f) 
    
    labsdir = os.path.abspath(os.path.join(src_path,  'labs'))

    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_file, logger)
    default_registry = labtainer_config.default_registry

    if args.lab is not None:
        logger.debug('Doing just one lab %s labsdir %s' % (args.lab, labsdir))
        DoLab(args.lab, labsdir, args.force, logger, False, args.default_registry, default_registry, no_build=args.no_build)
    else:    
        # do them all.  warn of incomplete git
        mycwd = os.getcwd()
        os.chdir(labsdir)
        command = 'git status -s' 
        ps = subprocess.Popen(shlex.split(command), True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        grep_command = 'grep -E "^M|^D|^A"'
        ps_grep = subprocess.Popen(shlex.split(grep_command), stdin=ps.stdout,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ps.stdout.close()
        output = ps_grep.communicate()
        if len(output[0]) > 0:
            for line in output[0].decode('utf-8').splitlines():
                print(line.strip())
            if not args.quiet:
                dumb = input("any key to continue") 
    
        # Do login here and now so we don't wait for lab to build before prompt
        if args.default_registry:
            os.system('docker login')
        #cmd = 'svn ls  https://tor.ern.nps.edu/svn/proj/labtainer/trunk/labs'
        cmd = 'git ls-files ./ | cut -d/ -f1 | uniq'
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = child.communicate()
        lab_list = output[0].decode('utf-8').strip().splitlines()
        for lab in sorted(lab_list):
            #lab = lab[:len(lab)-1] 
            lab = lab.strip()
            if args.start is not None and lab < args.start:
                continue 
            if lab not in skip:
                print('Lab: %s' % lab)
                lab_dir = os.path.join(labsdir, lab)
                os.chdir(lab_dir)
                cmd = 'git checkout ./'
                os.system(cmd)
                os.chdir(mycwd)
                DoLab(lab, labsdir, args.force, logger, False, args.default_registry, default_registry, no_build=args.no_build)

if __name__ == '__main__':
    sys.exit(main())

