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
'''
Build and publish labtainer images.  Use -h option for help.
'''
def relabel(image, version, base_image, base_id, registry):
    with open('./dfile', 'w') as fh:
        fh.write('FROM %s\n' % image)
        fh.write('ARG version\n')
        fh.write('LABEL version=%s\n' % version)
        fh.write('LABEL base=%s.%s' % (base_image, base_id))

    cmd = 'docker build -f dfile -t %s.tmp .' % image
    os.system(cmd)
    cmd = 'docker tag %s.tmp %s/%s' % (image, registry, image)
    print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s' % (registry, image)
    print cmd
    os.system(cmd)
    cmd = 'docker tag %s.tmp %s/%s:base_image%s' % (image, registry, image, base_id)
    print cmd
    os.system(cmd)
    cmd = 'docker push %s/%s:base_image%s' % (registry, image, base_id)
    print cmd
    os.system(cmd)

def rebuild(labname, labsdir, force, logger):
    mycwd = os.getcwd()
    path = '../scripts/labtainer-student'
    os.chdir(path)
    #print('now at %s' % os.getcwd())
    lab_dir = os.path.join(labsdir, labname)
    #print('cwd was %s now %s  lab_dir is %s' % (mycwd, os.getcwd(), lab_dir))
    retval = labutils.DoRebuildLab(lab_dir, force_build=force)
    os.chdir(mycwd)
    return retval

def pushIt(lab, docker_dir, registry, logger):
    '''
    Set the label and tags on any newly built image and push it to the given registry.
    '''
    df_list = [f for f in os.listdir(docker_dir) if os.path.isfile(os.path.join(docker_dir, f))]
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
            image_base = VersionInfo.getFrom(dfile_path, registry)
            base_id = VersionInfo.getImageId(image_base, True)
            framework_version = labutils.framework_version
            relabel(image, framework_version, image_base, base_id, registry)

        else: 
            logger.debug('Have not built %s, nothing to push' % image)
    ''' Delete the lab images. Two reasons: 1) ensure we run authoritative copy,
    which is from the dockerhub.  2) don't push on a rebuild if not rebuilt. '''
    removelab.removeLab(lab)

def DoLab(lab, labsdir, force, logger, do_login, test_registry, default_registry):
    logger.debug('DoLab for %s' % lab)
    lab_dir = os.path.join(labsdir, lab)
    registry_set = rebuild(lab, labsdir, force, logger)
    if len(registry_set) > 1:
        logger.error('no current support for images from multiple registries')
        exit(1)
    else:
        registry = list(registry_set)[0]
    logger.debug('back from rebuild with registry of %s' % registry)
    ''' should we login?  Never if test registry '''
    if not test_registry:
        if registry is not None and registry != default_registry:
            print('registry %s not equal %s, login' % (registry, default_registry))
            os.system('docker login -u %s' % registry)
        else:
            registry = default_registry
            if do_login:
                os.system('docker login -u %s' % registry)
    docker_dir = os.path.join(labsdir, lab, 'dockerfiles')
    pushIt(lab, docker_dir, registry, logger)

def main():
    parser = argparse.ArgumentParser(description='Build the images labs and publish to a registry')
    parser.add_argument('-l', '--lab', action='store', help='build and publish just this lab')
    parser.add_argument('-s', '--start', action='store', help='all labs starting with this one')
    parser.add_argument('-t', '--test_registry', action='store_true', default=False, help='build and publish with test registry')
    parser.add_argument('-f', '--force', action='store_true', default=False, help='force rebuild of all images')
    args = parser.parse_args()
    if args.test_registry:
        if os.getenv('TEST_REGISTRY') is None:
            print('use putenv to set it')
            os.putenv("TEST_REGISTRY", "TRUE")
            ''' why does putenv not set the value? '''
            os.environ['TEST_REGISTRY'] = 'TRUE'
        else:
            print('exists, set it true')
            os.environ['TEST_REGISTRY'] = 'TRUE'
        print('set TEST REG to %s' % os.getenv('TEST_REGISTRY'))

    src_path = '../'
    labtainer_config_file = os.path.join(src_path, 'config', 'labtainer.config')
    logger = LabtainerLogging.LabtainerLogging("labtainer-publish.log", 'publish', labtainer_config_file)
    labutils.logger = logger

    
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
        # Do login here and now so we don't wait for lab to build before prompt
        if not args.test_registry:
            os.system('docker login -u %s' % default_registry)
        DoLab(args.lab, labsdir, args.force, logger, False, args.test_registry, default_registry)
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
            for line in output[0].splitlines(True):
                print line.strip()
            dumb = raw_input("any key to continue") 
    
        if not args.test_registry:
            os.system('docker login -u %s' % default_registry)
        #cmd = 'svn ls  https://tor.ern.nps.edu/svn/proj/labtainer/trunk/labs'
        cmd = 'git ls-files ./ | cut -d/ -f1 | uniq'
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = child.communicate()
        lab_list = output[0].strip().splitlines(True)
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
                DoLab(lab, labsdir, args.force, logger, False, args.test_registry, default_registry)

if __name__ == '__main__':
    sys.exit(main())

