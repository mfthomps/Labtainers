#!/usr/bin/env python
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

def rebuild(labname, labsdir, role, force, logger):
    mycwd = os.getcwd()
    if role == 'student':
        path = '../scripts/labtainer-student'
    elif role == 'instructor':
        path = '../scripts/labtainer-instructor'
    else:
        print('unknown role: %s' % role)
        exit(1)
    os.chdir(path)
    #print('now at %s' % os.getcwd())
    lab_dir = os.path.join(labsdir, labname)
    #print('cwd was %s now %s  lab_dir is %s' % (mycwd, os.getcwd(), lab_dir))
    retval = labutils.DoRebuildLab(lab_dir, role, is_regress_test=False, force_build=force)
    os.chdir(mycwd)
    return retval

def pushIt(lab, docker_dir, role, registry, logger):
    #print('would push to %s' % registry)
    df_list = [f for f in os.listdir(docker_dir) if os.path.isfile(os.path.join(docker_dir, f))]
    for df in df_list:
        if df.endswith('.swp'):
            continue
        logger.DEBUG('tag and push %s' % df)
        try:
            parts = df.split('.')
            image = '%s.%s.%s' % (parts[1], parts[2], role)
        except:
            logger.ERROR('could not get image from %s' % df);
            continue
        image_exists, dumb, dumb1 = labutils.ImageExists(image, None)
        if image_exists:
            dfile_path = os.path.join(docker_dir,df)
            image_base = VersionInfo.getFrom(dfile_path, registry)
            base_id = VersionInfo.getImageId(image_base)
            framework_version = labutils.framework_version
            cmd = './relabel.sh %s %s %s %s %s' % (registry, framework_version , image, image_base, base_id)
            os.system(cmd)
            #cmd = 'docker tag %s %s/%s' % (image, registry, image)
            #os.system(cmd)
            #cmd = 'docker push %s/%s' % (registry, image)
            #os.system(cmd)
            ''' Delete the image. Two reasons: 1) ensure we run authoritative copy,
                which is from the dockerhub.  2) don't push on a rebuild if not rebuilt. '''
            cmd = '../scripts/labtainer-student/bin/removelab.sh %s' % (image)
            os.system(cmd)
        else: 
            logger.DEBUG('Have not built %s, nothing to push' % image)

def DoLab(lab, labsdir, role, force, logger, do_login, test_registry, default_registry):
    logger.DEBUG('DoLab for %s' % lab)
    lab_dir = os.path.join(labsdir, lab)
    if role == 'both':
        registry_set = rebuild(lab, labsdir, 'student', force, logger)
        dumb = rebuild(lab, labsdir, 'instructor', force, logger)
    else:
        registry_set = rebuild(lab, labsdir, role, force, logger)
    if len(registry_set) > 1:
        logger.ERROR('no current support for images from multiple registries')
        exit(1)
    else:
        registry = list(registry_set)[0]
    logger.DEBUG('back from rebuild with registry of %s' % registry)
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
    if role == 'both':
        pushIt(lab, docker_dir, 'student', registry, logger)
        pushIt(lab, docker_dir, 'instructor', registry, logger)
    else:
        pushIt(lab, docker_dir, role, registry, logger)

def main():
    parser = argparse.ArgumentParser(description='Build the images labs and publish to a registry')
    parser.add_argument('role', help='student | instructor | both')
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

    logger = LabtainerLogging.LabtainerLogging("labtainer-publish.log", 'publish', "../config/labtainer.config")
    labutils.logger = logger

    
    src_path = '../'
    skip_labs = 'skip-labs'

    skip = []
    with open(skip_labs) as fh:
        for line in fh:
            f = os.path.basename(line).strip()
            print('adding [%s]' % f)
            skip.append(f) 
    
    labsdir = os.path.abspath(os.path.join(src_path,  'labs'))

    labtainer_config_file = os.path.join(src_path, 'config', 'labtainer.config')
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(labtainer_config_file, logger)
    default_registry = labtainer_config.default_registry

    if args.lab is not None:
        logger.DEBUG('Doing just one lab %s labsdir %s' % (args.lab, labsdir))
        # Do login here and now so we don't wait for lab to build before prompt
        if not args.test_registry:
            os.system('docker login -u %s' % default_registry)
        DoLab(args.lab, labsdir, args.role, args.force, logger, False, args.test_registry, default_registry)
    else:    
        # do them all.  warn of incomplete svn
        mycwd = os.getcwd()
        os.chdir(labsdir)
        command = 'svn status' 
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
        cmd = 'svn ls  https://tor.ern.nps.edu/svn/proj/labtainer/trunk/labs'
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output = child.stdout.read()
        lab_list = output.strip().split()
        for lab in sorted(lab_list):
            lab = lab[:len(lab)-1] 
            if args.start is not None and lab < args.start:
                continue 
            if lab not in skip:
                print('Lab: %s' % lab)
                lab_dir = os.path.join(labsdir, lab)
                os.chdir(lab_dir)
                cmd = 'svn up'
                os.system(cmd)
                os.chdir(mycwd)
                DoLab(lab, labsdir, args.role, args.force, logger, False, args.test_registry, default_registry)

if __name__ == '__main__':
    sys.exit(main())

