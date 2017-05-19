import filecmp
import glob
import json
import md5
import os
import shutil
import re
import subprocess
import sys
import time
import zipfile
import ParseStartConfig
import ParseLabtainerConfig
import datetime
import getpass
import socket
import fcntl
import struct
import threading
import LabtainerLogging
global logger
'''
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
'''

LABS_ROOT = os.path.abspath("../../labs/")
LABTAINER_CONFIG = os.path.abspath("../../config/labtainer.config")

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

def is_valid_lab(lab_path):
    # Lab path must exist and must be a directory
    if os.path.exists(lab_path) and os.path.isdir(lab_path):
        # Assume it is valid lab then
        logger.DEBUG("lab_path directory (%s) exists" % lab_path)
    else:
        logger.ERROR("Invalid lab! lab_path directory (%s) does not exist!" % lab_path)
        sys.exit(1)

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    return re.match(r'^[a-zA-Z0-9_-]*$', name)

# get docker0 IP address
def getDocker0IPAddr():
    return get_ip_address('docker0')

# Parameterize my_container_name container
def ParameterizeMyContainer(mycontainer_name, container_user, lab_instance_seed, user_email, labname):
    retval = True
    logger.DEBUG("About to call parameterize.sh with LAB_INSTANCE_SEED = (%s)" % lab_instance_seed)
    cmd_path = '/home/%s/.local/bin/parameterize.sh' % (container_user)
    command=['docker', 'exec', '-i',  mycontainer_name, '/usr/bin/sudo', cmd_path, container_user, lab_instance_seed, user_email, labname, mycontainer_name ]
    child = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().strip()
    if len(error_string) > 0:
        logger.ERROR('ParameterizeMyContainer %s' % error_string)
        logger.ERROR('command was %s' % command)
        retval = False
    return retval

# Start my_container_name container
def StartMyContainer(mycontainer_name):
    retval = True
    if IsContainerRunning(mycontainer_name):
        logger.ERROR("Container %s is already running!\n" % (mycontainer_name))
        sys.exit(1)
    command = "docker start %s" % mycontainer_name
    logger.DEBUG("Command to execute is (%s)" % command)
    ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        logger.ERROR('StartMyContainer %s' % output[1])
        logger.ERROR('command was %s' % command)
        retval = False
    return retval

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    retval = True
    command = "docker inspect -f {{.Created}} --type container %s 2> /dev/null" % mycontainer_name
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    if result == FAILURE:
       retval = False
    logger.DEBUG("Result of subprocess.call IsContainerCreated is %s" % result)
    return retval

def ConnectNetworkToContainer(mycontainer_name, mysubnet_name, mysubnet_ip):
    logger.DEBUG("Connecting more network subnet to container %s" % mycontainer_name)
    command = "docker network connect --ip=%s %s %s 2> /dev/null" % (mysubnet_ip, mysubnet_name, mycontainer_name)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.call ConnectNetworkToContainer is %s" % result)
    return result

def DisconnectNetworkFromContainer(mycontainer_name, mysubnet_name):
    logger.DEBUG("Disconnecting more network subnet to container %s" % mycontainer_name)
    command = "docker network disconnect %s %s 2> /dev/null" % (mysubnet_name, mycontainer_name)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.call DisconnectNetworkFromContainer is %s" % result)
    return result

def CreateSingleContainer(mycontainer_name, mycontainer_image_name, hostname, mysubnet_name=None, mysubnet_ip=None):
    logger.DEBUG("Create Single Container")
    retval = True
    cmd = "docker inspect -f '{{.Created}}' --type image %s" % mycontainer_image_name
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1]) > 0:
        logger.DEBUG("Command was (%s)" % cmd)
        logger.ERROR("CreateSingleContainer image %s does not exist!" % mycontainer_image_name)
        retval = False
    else:
        docker0_IPAddr = getDocker0IPAddr()
        logger.DEBUG("getDockerIPAddr result (%s)" % docker0_IPAddr)
        if mysubnet_name:
            createsinglecommand = "docker create -t --network=%s --ip=%s --privileged --add-host my_host:%s --name=%s --hostname %s %s bash" % (mysubnet_name, mysubnet_ip, docker0_IPAddr, mycontainer_name, hostname, mycontainer_image_name)
        else:
            createsinglecommand = "docker create -t --privileged --add-host my_host:%s --name=%s --hostname %s %s bash" % (docker0_IPAddr, 
               mycontainer_name, hostname, mycontainer_image_name)
        logger.DEBUG("Command to execute is (%s)" % createsinglecommand)
        ps = subprocess.Popen(createsinglecommand, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1]) > 0:
            logger.DEBUG('command was %s' % createsinglecommand)
            logger.ERROR('CreateSingleContainer %s' % output[1])
            retval = False
    return retval


# Create SUBNETS
def CreateSubnets(subnets):
    #for (subnet_name, subnet_network_mask) in networklist.iteritems():
    for subnet_name in subnets:
        subnet_network_mask = subnets[subnet_name].mask
        logger.DEBUG("subnet_name is %s" % subnet_name)
        logger.DEBUG("subnet_network_mask is %s" % subnet_network_mask)

        command = "docker network inspect %s > /dev/null" % subnet_name
        logger.DEBUG("Command to execute is (%s)" % command)
        inspect_result = subprocess.call(command, shell=True)
        logger.DEBUG("Result of subprocess.call CreateSubnets docker network inspect is %s" % inspect_result)
        if inspect_result == FAILURE:
            # Fail means does not exist - then we can create
            if subnets[subnet_name].gateway != None:
                logger.DEBUG(subnets[subnet_name].gateway)
                subnet_gateway = subnets[subnet_name].gateway
                command = "docker network create -d bridge --gateway=%s --subnet %s %s" % (subnet_gateway, subnet_network_mask, subnet_name)
            else:
                command = "docker network create -d bridge --subnet %s %s" % (subnet_network_mask, subnet_name)
            logger.DEBUG("Command to execute is (%s)" % command)
            #create_result = subprocess.call(command, shell=True)
            ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            logger.DEBUG("Result of subprocess.call CreateSubnets docker network create is %s" % output[0])
            if len(output[1]) > 0:
                logger.ERROR("Failed to create %s subnet at %s, %s\n" % (subnet_name, subnet_network_mask, output[1]))
                logger.ERROR("command was %s\n" % command)
                sys.exit(1)
        else:
            logger.WARNING("Already exists! Not creating %s subnet at %s!\n" % (subnet_name, subnet_network_mask))

def RemoveSubnets(subnets, ignore_stop_error):
    for subnet_name in subnets:
        command = "docker network rm %s" % subnet_name
        ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output = ps.communicate()
        if len(output[1]) > 0:
            if ignore_stop_error:
                logger.DEBUG('Encountered error removing subnet %s' % subnet_name)
            else:
                logger.ERROR('Encountered error removing subnet %s' % subnet_name)

EMAIL_TMP='./.tmp/email.txt' 
def getLastEmail():
    retval = None
    if os.path.isfile(EMAIL_TMP):
        with open(EMAIL_TMP) as fh:
            retval = fh.read()
    return retval

def putLastEmail(email):
    try:
        os.mkdir('./.tmp')
    except:
        pass
    with open(EMAIL_TMP, 'w') as fh:
            fh.write(email)

def ParamForStudent(lab_master_seed, mycontainer_name, container_user, labname, student_email):
    if student_email is not None:
        user_email = student_email
    else:
        done = False
        while not done and student_email is None:
            done = True
            # Prompt user for e-mail address
            eprompt = 'Please enter your e-mail address: '
            prev_email = getLastEmail()
            if prev_email is not None:
                eprompt = eprompt+" [%s]" % prev_email
            user_email = raw_input(eprompt)
            if len(user_email.strip()) == 0:
                if prev_email is None:
                    done = False
                else:
                    user_email = prev_email
            else:
                putLastEmail(user_email)
    
    # Create hash using LAB_MASTER_SEED concatenated with user's e-mail
    # LAB_MASTER_SEED is per laboratory - specified in start.config
    string_to_be_hashed = '%s:%s' % (lab_master_seed, user_email)
    mymd5 = md5.new()
    mymd5.update(string_to_be_hashed)
    mymd5_hex_string = mymd5.hexdigest()
    logger.DEBUG(mymd5_hex_string)

    if not ParameterizeMyContainer(mycontainer_name, container_user, mymd5_hex_string,
                                                          user_email, labname):
        logger.ERROR("Failed to parameterize lab container %s!\n" % mycontainer_name)
        sys.exit(1)
    return user_email

# Copy Students' Artifacts from host to instructor's lab container
def CopyStudentArtifacts(labtainer_config, mycontainer_name, labname, container_user, is_regress_test):
    # Set the lab name 
    command = 'docker exec -it %s script -q -c "echo %s > /home/%s/.local/.labname" /dev/null' % (mycontainer_name, labname, container_user)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.call CopyStudentArtifacts set labname is %s" % result)
    if result == FAILURE:
        logger.ERROR("Failed to set labname in container %s!\n" % mycontainer_name)
        sys.exit(1)

    # Create is_grade_container
    command = 'docker exec -it %s script -q -c "echo TRUE > /home/%s/.local/.is_grade_container" /dev/null' % (mycontainer_name, container_user)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.call CopyStudentArtifacts create is_grade_container is %s" % result)
    if result == FAILURE:
        logger.ERROR("Failed to create is_grade_container in container %s!\n" % mycontainer_name)
        sys.exit(1)

    username = getpass.getuser()
    if is_regress_test:
        xfer_dir = labtainer_config.testsets_root
        zip_filelist = glob.glob('%s/*.zip' % xfer_dir)
    else:
        xfer_dir = labtainer_config.host_home_xfer
        zip_filelist = glob.glob('/home/%s/%s/*.zip' % (username, xfer_dir))
    logger.DEBUG("filenames is (%s)" % zip_filelist)
    # Copy zip files from 'Shared' folder to 'home/$CONTAINER_USER'
    for fname in zip_filelist:
        logger.DEBUG("name is %s" % fname)
        base_fname = os.path.basename(fname)
        # Copy zip file and chown it
        command = 'docker cp %s %s:/home/%s/' % (fname, mycontainer_name, container_user)
        logger.DEBUG("Command to execute is (%s)" % command)
        result = subprocess.call(command, shell=True)
        logger.DEBUG("Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s" % (fname, result))
        if result == FAILURE:
            logger.ERROR("Failed to set labname in container %s!\n" % mycontainer_name)
            sys.exit(1)
        command = 'docker exec -it %s sudo chown %s:%s /home/%s/%s' % (mycontainer_name, container_user, container_user, container_user, base_fname)
        logger.DEBUG("Command to execute is (%s)" % command)
        result = subprocess.call(command, shell=True)
        logger.DEBUG("Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s" % (fname, result))
        if result == FAILURE:
            logger.ERROR("Failed to set labname in container %s!\n" % mycontainer_name)
            sys.exit(1)

def DoStart(start_config, labtainer_config, labname, role, is_regress_test):
    lab_master_seed = start_config.lab_master_seed
    logger.DEBUG("DoStart Multiple Containers and/or multi-home networking")

    # Create SUBNETS
    CreateSubnets(start_config.subnets)
    student_email = None
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        container_user         = container.user
        container_hostname         = container.hostname

        haveContainer = IsContainerCreated(mycontainer_name)
        logger.DEBUG("DoStart IsContainerCreated result (%s)" % haveContainer)

        # Set need_seeds=False first
        need_seeds=False

        # IsContainerCreated return False if container does not exists
        if not haveContainer:
            # Container does not exist, create the container
            # Use CreateSingleContainer()
            containerCreated = False
            if len(container.container_nets) == 0:
                containerCreated = CreateSingleContainer(mycontainer_name, mycontainer_image_name, container_hostname)
            else:
                mysubnet_name, mysubnet_ip = container.container_nets.popitem()
                containerCreated = CreateSingleContainer(mycontainer_name, mycontainer_image_name, container_hostname,
                                                         mysubnet_name, mysubnet_ip)
                
            logger.DEBUG("CreateSingleContainer result (%s)" % containerCreated)
            if not containerCreated:
                logger.ERROR("CreateSingleContaier fails to create container %s!\n" % mycontainer_name)
                sys.exit(1)

            # Give the container some time -- just in case
            time.sleep(3)
            # If we just create it, then set need_seeds=True
            need_seeds=True

        # Check again - 
        haveContainer = IsContainerCreated(mycontainer_name)
        logger.DEBUG("IsContainerCreated result (%s)" % haveContainer)

        # IsContainerCreated returned False if container does not exists
        if not haveContainer:
            logger.ERROR("Container %s still not created!\n" % mycontainer_name)
            sys.exit(1)
        else:
            for mysubnet_name, mysubnet_ip in container.container_nets.items():
                connectNetworkResult = ConnectNetworkToContainer(mycontainer_name, mysubnet_name, mysubnet_ip)

            # Start the container
            if not StartMyContainer(mycontainer_name):
                logger.ERROR("Container %s failed to start!\n" % mycontainer_name)
                sys.exit(1)

        if role == 'instructor':
            '''
            Copy students' artifacts only to the container where 'Instructor.py' supposed
            to be run - where <labname>.grades.txt will later reside also (i.e., don't copy to all containers)
            Copy to container named start_config.grade_container
            '''
            if mycontainer_name == start_config.grade_container:
                copy_result = CopyStudentArtifacts(labtainer_config, mycontainer_name, labname, container_user, is_regress_test)
                if copy_result == FAILURE:
                    logger.ERROR("Failed to copy students' artifacts to container %s!\n" % mycontainer_name)
                    sys.exit(1)
        # If the container is just created, prompt user's e-mail
        # then parameterize the container
        elif need_seeds and role == 'student':
            student_email = ParamForStudent(lab_master_seed, mycontainer_name, container_user, labname, student_email)
    
    # Reach here - Everything is OK - spawn terminal for each container based on num_terminal
    for container in start_config.containers.values():
        num_terminal = container.terminals
        mycontainer_name = container.full_name
        logger.DEBUG("Number of terminal is %d" % num_terminal)
        # If this is instructor - spawn 2 terminal for 'grader' container otherwise 1 terminal
        if role == 'instructor':
            if mycontainer_name == start_config.grade_container:
                num_terminal = 2
            else:
                num_terminal = 1
        # If the number of terminal is zero -- do not spawn
        if num_terminal != 0:
            for x in range(num_terminal):
                spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % mycontainer_name
                os.system(spawn_command)

    return 0


# Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
def CreateHostHomeXfer(host_xfer_dir):
    # remove trailing '/'
    host_xfer_dir = host_xfer_dir.rstrip('/')
    logger.DEBUG("host_home_xfer directory (%s)" % host_xfer_dir)
    if os.path.exists(host_xfer_dir):
        # exists but is not a directory
        if not os.path.isdir(host_xfer_dir):
            # remove file then create directory
            os.remove(host_xfer_dir)
            os.makedirs(host_xfer_dir)
        #else:
        #    logger.DEBUG("host_home_xfer directory (%s) exists" % host_xfer_dir)
    else:
        # does not exists, create directory
        os.makedirs(host_xfer_dir)

# CopyChownGradesFile
def CopyChownGradesFile(mycwd, start_config, labtainer_config, container_name, container_image, container_user, ignore_stop_error):
    host_home_xfer = labtainer_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    labname = start_config.labname

    username = getpass.getuser()

    # Copy <labname>.grades.txt file
    grade_filename = '/home/%s/%s.grades.txt' % (container_user, labname)
    command = "docker cp %s:%s /home/%s/%s" % (container_name, grade_filename, username, host_home_xfer)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.Popen exec cp %s.grades.txt file is %s" % (labname, result))
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name, ignore_stop_error)
        if ignore_stop_error:
            logger.DEBUG("Container %s fail on executing cp %s.grades.txt file!\n" % (container_name, labname))
        else:
            logger.WARNING("Container %s fail on executing cp %s.grades.txt file!\n" % (container_name, labname))
        return

    # Change <labname>.grades.txt ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/%s.grades.txt" % (username, username, username, host_home_xfer, labname)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.Popen exec chown %s.grades.txt file is %s" % (labname, result))
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name, ignore_stop_error)
        if ignore_stop_error:
            logger.DEBUG("Container %s fail on executing chown %s.grades.txt file!\n" % (container_name, labname))
        else:
            logger.ERROR("Container %s fail on executing chown %s.grades.txt file!\n" % (container_name, labname))
        sys.exit(1)

    # Copy <labname>.grades.json file
    gradejson_filename = '/home/%s/%s.grades.json' % (container_user, labname)
    command = "docker cp %s:%s /home/%s/%s" % (container_name, gradejson_filename, username, host_home_xfer)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.Popen exec cp %s.grades.json file is %s" % (labname, result))
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name, ignore_stop_error)
        if ignore_stop_error:
            logger.DEBUG("Container %s fail on executing cp %s.grades.json file!\n" % (container_name, labname))
        else:
            logger.WARNING("Container %s fail on executing cp %s.grades.json file!\n" % (container_name, labname))
        return

    # Change <labname>.grades.json ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/%s.grades.json" % (username, username, username, host_home_xfer, labname)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.Popen exec chown %s.grades.json file is %s" % (labname, result))
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name, ignore_stop_error)
        if ignore_stop_error:
            logger.DEBUG("Container %s fail on executing chown %s.grades.json file!\n" % (container_name, labname))
        else:
            logger.ERROR("Container %s fail on executing chown %s.grades.json file!\n" % (container_name, labname))
        sys.exit(1)

def StartLab(labname, role, is_regress_test=False, force_build=False, is_redo=False):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    logger.DEBUG("current working directory for %s" % mycwd)
    logger.DEBUG("current user's home directory for %s" % myhomedir)
    logger.DEBUG("ParseStartConfig for %s" % labname)
    lab_path          = os.path.join(LABS_ROOT,labname)
    is_valid_lab(lab_path)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
   
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role, logger)
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(LABTAINER_CONFIG, labname, logger)
    host_home_xfer = labtainer_config.host_home_xfer

    build_student = './buildImage.sh'
    build_instructor = './buildInstructorImage.sh'
    fixresolve='../../setup_scripts/fixresolv.sh'
    didfix = False
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        if force_build:
            cmd = 'docker rm %s' % mycontainer_name
            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            output = ps.communicate()
            logger.DEBUG("Command was (%s)" % cmd)
            if len(output[1]) > 0:
                logger.DEBUG("Error from command = '%s'" % str(output[1]))
        if force_build or CheckBuild(labname, mycontainer_image_name, mycontainer_name, name, role, is_redo):
            if os.path.isfile(fixresolve) and not didfix:
                ''' DNS name resolution from containers (while being built) fails when behind NAT? '''
                os.system(fixresolve)
                didfix=True
            if os.path.isfile(build_student):
                cmd = '%s %s %s' % (build_student, labname, name)
            elif os.path.isfile(build_instructor):
                cmd = '%s %s %s' % (build_instructor, labname, name)
            else:
                logger.ERROR("no image rebuild script\n")
                exit(1)
                 
            if os.system(cmd) != 0:
                logger.ERROR("build of image failed\n")
                exit(1)

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    DoStart(start_config, labtainer_config, labname, role, is_regress_test)

def FileModLater(ts, fname):
    ''' is the given file later than the timestamp (which is in UTC)? '''
    df_time = os.path.getmtime(fname)
    logger.DEBUG('df ts %s' % df_time)

    df_string = datetime.datetime.fromtimestamp(df_time)
    logger.DEBUG('df_local time is %s' % df_string)

    df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
    parts = df_utc_string.split('.')
    df_ts = time.mktime(time.strptime(parts[0], "%Y-%m-%d %H:%M:%S"))

    logger.DEBUG('df_utc time is %s' % df_utc_string)
    logger.DEBUG('df_utc ts is %s given ts is %s' % (df_ts, ts))
    if df_ts > ts:
        return True
    else:
        return False

def CheckBuild(labname, image_name, container_name, name, role, is_redo):
    '''
    Determine if a container image needs to be rebuilt.
    '''
    retval = False
    logger.DEBUG('check build for container %s image %s' % (container_name, image_name))
    cmd = "docker inspect -f '{{.Created}}' --type image %s" % image_name
    ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    result = output[0].strip()
    logger.DEBUG('result is %s' % result)
    if 'Error:' in result or len(result.strip()) == 0:
        if 'Error:' in result:
            logger.DEBUG("Command was (%s)" % cmd)
            logger.DEBUG("Error from command = '%s'" % result)
        return True
    if len(output[1].strip()) > 0:
        logger.DEBUG('No image: error returned %s, do build' % output[1])
        return True
    else:
        if not is_redo:
            logger.DEBUG('Container %s image %s exist, not a redo, just return (no need to check build)' % (container_name, image_name))
            return False
    parts = result.strip().split('.')
    time_string = parts[0]
    logger.DEBUG('image time string %s' % time_string)

    ''' ts is the timestamp of the image '''
    ts = time.mktime(time.strptime(time_string, "%Y-%m-%dT%H:%M:%S"))
    logger.DEBUG('image ts %s' % ts)

    ''' look at dockerfiles '''
    lab_path = os.path.join(LABS_ROOT,labname)
    df_name = 'Dockerfile.%s' % container_name
    df = os.path.join(lab_path, 'dockerfiles', df_name)
    if not os.path.isfile(df):
         df = df.replace('instructor', 'student')
    if FileModLater(ts, df):
        logger.WARNING('dockerfile changed, will build')
        retval = True
    else:
        ''' look for new/deleted files in the container '''
        container_dir = os.path.join(lab_path, name)
        logger.DEBUG('container dir %s' % container_dir)
        if FileModLater(ts, container_dir):
           logger.WARNING('%s is later, will build' % container_dir)
           retval = True
        else:
            ''' look at all files in container '''
            for folder, subs, files in os.walk(container_dir):
                for f in files:
                   f_path = os.path.join(folder, f)
                   logger.DEBUG('check %s' % f_path)
                   if FileModLater(ts, f_path):
                       logger.WARNING('%s is later, will build' % f_path)
                       retval = True
                       break

    if not retval:
        all_bin = './bin' 
        all_bin_files = os.listdir(all_bin)
        for f in all_bin_files:
            f_path = os.path.join(all_bin, f)
            if FileModLater(ts, f_path):
               logger.WARNING('%s is later, will build' % f_path)
               retval = True
               break

    if not retval and role == 'instructor':
        inst_cfg = os.path.join(lab_path,'instr_config')
        inst_cfg_files = os.listdir(inst_cfg)
        for f in inst_cfg_files:
            f_path = os.path.join(inst_cfg, f)
            if FileModLater(ts, f_path):
               logger.WARNING('%s is later, will build' % f_path)
               retval = True
               break
        logger.DEBUG('is instructor')
        if not retval:  
            inst_bin = './bin'
            inst_bin_files = os.listdir(inst_bin)
            for f in inst_bin_files:
                f_path = os.path.join(inst_bin, f)
                if FileModLater(ts, f_path):
                   logger.WARNING('%s is later, will build' % f_path)
                   retval = True
                   break
    return retval

def dumb():
    pass
    '''
    '''
def RedoLab(labname, role, is_regress_test=False, force_build=False):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    logger.DEBUG("current working directory for %s" % mycwd)
    logger.DEBUG("current user's home directory for %s" % myhomedir)
    logger.DEBUG("ParseStartConfig for %s" % labname)
    # Pass 'True' to ignore_stop_error (i.e., ignore certain error encountered during StopLab
    #                                         since it might not even be an error)
    StopLab(labname, role, True)
    is_redo = True
    StartLab(labname, role, is_regress_test, force_build, is_redo=is_redo)

def GatherOtherArtifacts(labname, name, container_name, container_user, ignore_stop_error):
    '''
    Parse the results.config file looking for files named by absolute paths,
    and copy those into the .local/result directory, maintaining the original
    directory structure, e.g., .local/result/var/log/foo.log
    '''
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"instr_config") 
    results_config_path = os.path.join(config_path,"results.config")
    did_file = []
    with open (results_config_path) as fh:
        for line in fh:
            ''' container:filename is between "=" and first " : " '''
            line = line.strip()
            if line.startswith('#') or len(line) == 0:
                continue
            if '=' not in line:
                logger.WARNING('no = in line %s' % line)
                continue
            after_equals = line.split('=', 1)[1]
            fname = after_equals.split(' : ')[0]
            is_mine = False
            if ':' in fname:
                f_container, fname = fname.split(':')
                logger.DEBUG('f_container <%s> container_name %s' % (f_container, name))
                if f_container.strip() == name:
                    is_mine = True 
                fname = fname.strip()
            else: 
                is_mine = True
            if is_mine:
                logger.DEBUG(' is mine %s' % fname )
                if fname.startswith('/') and fname not in did_file:
                    ''' copy from abs path to ~/.local/result ''' 
               
                    command='docker exec -it %s sudo cp --parents %s /home/%s/.local/result' % (container_name, fname, container_user)
                    logger.DEBUG(command)
                    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    error = child.stderr.read().strip()
                    if len(error) > 0:
                        if ignore_stop_error:
                            logger.DEBUG('ERROR: %s' % error)
                            logger.DEBUG('command was %s' % command)
                        else:
                            logger.ERROR('ERROR: %s' % error)
                            logger.ERROR('command was %s' % command)
                    did_file.append(fname)
                    command='docker exec -it %s sudo chmod a+r -R /home/%s/.local/result' % (container_name, container_user)
                    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    error = child.stderr.read().strip()
                    if len(error) > 0:
                        if ignore_stop_error:
                            logger.DEBUG('chmod ERROR: %s' % error)
                            logger.DEBUG('command was %s' % command)
                        else:
                            logger.ERROR('chmod ERROR: %s' % error)
                            logger.ERROR('command was %s' % command)
                        

# RunInstructorCreateGradeFile
def RunInstructorCreateGradeFile(container_name):
    # Run 'instructor.py' - This will create '<labname>.grades.txt' 
    logger.DEBUG("About to call instructor.py")
    bash_command = "'cd ; . .profile ; instructor.py'"
    command = 'docker exec -it %s script -q -c "/bin/bash -c %s" /dev/null' % (container_name, bash_command)
    logger.DEBUG("Command to execute is (%s)" % command)
    result = subprocess.call(command, shell=True)
    logger.DEBUG("Result of subprocess.call exec instructor.py is %s" % result)
    if result == FAILURE:
        logger.ERROR("Container %s fail on executing instructor.py!\n" % container_name)
        sys.exit(1)


def RegressTest(labname, role):
    username = getpass.getuser()
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    logger.DEBUG("current working directory for %s" % mycwd)
    logger.DEBUG("current user's home directory for %s" % myhomedir)
    logger.DEBUG("ParseStartConfig for %s" % labname)
    lab_path          = os.path.join(LABS_ROOT,labname)
    is_valid_lab(lab_path)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role, logger)

    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(LABTAINER_CONFIG, labname, logger)
    regresstest_lab_path = labtainer_config.testsets_root
    host_home_xfer = labtainer_config.host_home_xfer
    logger.DEBUG("Host Xfer directory for labname %s is %s" % (labname, host_home_xfer))
    logger.DEBUG("Regression Test path for labname %s is %s" % (labname, regresstest_lab_path))

    GradesGold = "%s/%s.grades.txt" % (regresstest_lab_path, labname)
    Grades = "/home/%s/%s/%s.grades.txt" % (username, host_home_xfer, labname)
    logger.DEBUG("GradesGold is %s - Grades is %s" % (GradesGold, Grades))

    is_regress_test = True
    RedoLab(labname, role, is_regress_test=is_regress_test)
    RunInstructorCreateGradeFile(start_config.grade_container)
    # Pass 'False' to ignore_stop_error (i.e., do not ignore error)
    StopLab(labname, role, False)

    CompareResult = filecmp.cmp(GradesGold, Grades)
    return CompareResult


def CreateCopyChownZip(mycwd, start_config, labtainer_config, container_name, container_image, container_user, ignore_stop_error):
    '''
    Zip up the student home directory and copy it to the Linux host home directory
    '''
    logger.DEBUG('in CreateCopyChownZip')
    host_home_xfer  = labtainer_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed

    # Run 'Student.py' - This will create zip file of the result
    logger.DEBUG("About to call Student.py")
    cmd_path = '/home/%s/.local/bin/Student.py' % (container_user)
    command=['docker', 'exec', '-i',  container_name, '/usr/bin/sudo', cmd_path, container_user]
    logger.DEBUG('cmd: %s' % str(command))
    child = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().strip()
    if len(error_string) > 0:
        if ignore_stop_error:
            logger.DEBUG("Container %s fail on executing Student.py \n" % (container_name))
        else:
            logger.ERROR("Container %s fail on executing Student.py \n" % (container_name))
        return None, None
    
    #out_string = output[0].strip()
    #if len(out_string) > 0:
    #    logger.DEBUG('output of Student.py is %s' % out_string)
    username = getpass.getuser()

    tmp_dir=os.path.join('/tmp/labtainers', container_name)
    shutil.rmtree(tmp_dir, ignore_errors=True)
    os.makedirs(tmp_dir)
    source_dir = os.path.join('/home', container_user, '.local', 'zip')
    cont_source = '%s:%s' % (container_name, source_dir)
    logger.DEBUG('will copy from %s ' % source_dir)
    command = ['docker', 'cp', cont_source, tmp_dir]
    # The zip filename created by Student.py has the format of e-mail.labname.zip
    logger.DEBUG("Command to execute is (%s)" % command)
    child = subprocess.Popen(command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().strip()
    if len(error_string) > 0:
        if ignore_stop_error:
            logger.DEBUG("Container %s fail on executing cp zip file!\n" % container_name)
            logger.DEBUG("Command was (%s)" % command)
        else:
            logger.ERROR("Container %s fail on executing cp zip file!\n" % container_name)
            logger.ERROR("Command was (%s)" % command)
        StopMyContainer(mycwd, start_config, container_name, ignore_stop_error)
        return None, None
    
    local_tmp_zip = os.path.join(tmp_dir, 'zip')
    try:
        orig_zipfilenameext = os.listdir(local_tmp_zip)[0]
    except:
        if ignore_stop_error:
            logger.DEBUG('no files at %s\n' % local_tmp_zip)
        else:
            logger.ERROR('no files at %s\n' % local_tmp_zip)
        return None, None
    orig_zipfilename, orig_zipext = os.path.splitext(orig_zipfilenameext)
    baseZipFilename = os.path.basename(orig_zipfilename)
    #NOTE: Use the '=' to separate e-mail+labname from the container_name
    DestZipFilename = '%s=%s.zip' % (baseZipFilename, container_name)
    DestZipPath = os.path.join('/home', username, host_home_xfer, DestZipFilename)
    shutil.copyfile(os.path.join(local_tmp_zip, orig_zipfilenameext), DestZipPath)

    # Change ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/*.zip" % (username, username, username, host_home_xfer)
    logger.DEBUG("Command to execute is (%s)" % command)
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    error_string = child.stderr.read().strip()
    if len(error_string) > 0:
        if ignore_stop_error:
            logger.DEBUG("chown failed Command was (%s)" % command)
            logger.DEBUG("Container %s fail on executing chown zip file!\n" % container_name)
        else:
            logger.ERROR("chown failed Command was (%s)" % command)
            logger.ERROR("Container %s fail on executing chown zip file!\n" % container_name)
        StopMyContainer(mycwd, start_config, container_name, ignore_stop_error)
        return None, None

    currentContainerZipFilename = "/home/%s/%s/%s" % (username, host_home_xfer, DestZipFilename)
    return baseZipFilename, currentContainerZipFilename
   
# Stop my_container_name container
def StopMyContainer(mycwd, start_config, container_name, ignore_stop_error):
    command = "docker stop %s" % container_name
    logger.DEBUG("Command to execute is (%s)" % command)
    ps = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    output = ps.communicate()
    if len(output[1].strip()) > 0:
        if ignore_stop_error:
            logger.DEBUG('Fail to stop container, error returned %s' % output[1])
        else:
            logger.ERROR('Fail to stop container, error returned %s' % output[1])
    #if len(output[0].strip()) > 0:
    #    logger.DEBUG('StopMyContainer stdout %s' % output[0])
    #result = subprocess.call(command, shell=True)

def IsContainerRunning(mycontainer_name):
    try:
        s = subprocess.check_output('docker ps', shell=True)
    except:
        return False
    if mycontainer_name in s:
        return True
    else:
        return False 

def DoStopOne(start_config, labtainer_config, mycwd, labname, role, name, container, ZipFileList, ignore_stop_error, results):
        #dumlog = os.path.join('/tmp', name+'.log')
        #sys.stdout = open(dumlog, 'w')
        #sys.stderr = sys.stdout
        retval = True
        mycontainer_name  = container.full_name
        container_user    = container.user
        mycontainer_image = container.image_name
        haveContainer     = IsContainerCreated(mycontainer_name)
        logger.DEBUG("IsContainerCreated result (%s)" % haveContainer)

        # IsContainerCreated returned FAILURE if container does not exists
        # error: can't stop non-existent container
        if not haveContainer:
            if ignore_stop_error:
                logger.DEBUG("Container %s does not exist!\n" % mycontainer_name)
            else:
                logger.ERROR("Container %s does not exist!\n" % mycontainer_name)
            retval = False
        elif not IsContainerRunning(mycontainer_name):
            if ignore_stop_error:
                logger.DEBUG("container %s not running\n" % (mycontainer_name))
            else:
                logger.ERROR("container %s not running\n" % (mycontainer_name))
            retval = False
        else:
            if role == 'instructor':
                if mycontainer_name == start_config.grade_container:
                    CopyChownGradesFile(mycwd, start_config, labtainer_config, mycontainer_name, mycontainer_image, container_user, ignore_stop_error)
            else:
                GatherOtherArtifacts(labname, name, mycontainer_name, container_user, ignore_stop_error)
                # Before stopping a container, run 'Student.py'
                # This will create zip file of the result
    
                baseZipFilename, currentContainerZipFilename = CreateCopyChownZip(mycwd, start_config, labtainer_config, mycontainer_name, mycontainer_image, container_user, ignore_stop_error)
                if baseZipFilename is not None:
                    ZipFileList.append(currentContainerZipFilename)
                logger.DEBUG("baseZipFilename is (%s)" % baseZipFilename)
   

            for mysubnet_name, mysubnet_ip in container.container_nets.items():
                disconnectNetworkResult = DisconnectNetworkFromContainer(mycontainer_name, mysubnet_name)

            # Stop the container
            StopMyContainer(mycwd, start_config, mycontainer_name, ignore_stop_error)

        results.append(retval)

def DoStop(start_config, labtainer_config, mycwd, labname, role, ignore_stop_error):
    retval = True
    host_home_xfer  = labtainer_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    logger.DEBUG("DoStop Multiple Containers and/or multi-home networking")

    username = getpass.getuser()

    baseZipFilename = ""
    ZipFileList = []
    threads = []
    results = []
    for name, container in start_config.containers.items():
        #DoStopOne(start_config, labtainer_config, mycwd, labname, role, name, container, ZipFileList)
        t = threading.Thread(target=DoStopOne, args=(start_config, labtainer_config, mycwd, labname, 
              role, name, container, ZipFileList, ignore_stop_error, results))
        threads.append(t)
        t.setName(name)
        t.start()
      
    logger.DEBUG('started all')
    for t in threads:
        t.join()
        logger.DEBUG('joined %s' % t.getName())

    if not ignore_stop_error:
        if False in results:
            logger.ERROR('DoStopOne has at least one failure!')
            sys.exit(1)

    RemoveSubnets(start_config.subnets, ignore_stop_error)
    if role == 'student':
        if len(ZipFileList) == 0:
            if ignore_stop_error:
                logger.DEBUG('No zip files found')
            else:
                logger.ERROR('No zip files found')
            return None
        base_filename = os.path.basename(ZipFileList[0])
        baseZipFilename = base_filename.split('=')[0]

        # Combine all the zip files
        logger.DEBUG("ZipFileList is ")
        logger.DEBUG(ZipFileList)
        logger.DEBUG("baseZipFilename is (%s)" % baseZipFilename)
        xfer_dir = "/home/%s/%s" % (username, host_home_xfer)
        combinedZipFilename = "%s/%s.zip" % (xfer_dir, baseZipFilename)
        logger.DEBUG("The combined zip filename is %s" % combinedZipFilename)
        zipoutput = zipfile.ZipFile(combinedZipFilename, "w")
        # Go to the xfer_dir
        os.chdir(xfer_dir)
        for fname in ZipFileList:
            basefname = os.path.basename(fname)
            zipoutput.write(basefname, compress_type=zipfile.ZIP_DEFLATED)
            # Remove after the file is zipped
            os.remove(basefname)
        zipoutput.close()

    os.chdir(mycwd)
    return retval

# ignore_stop_error - set to 'False' : do not ignore error
# ignore_stop_error - set to 'True' : ignore certain error encountered since it might not even be an error
#                                     such as error encountered when trying to stop non-existent container
def StopLab(labname, role, ignore_stop_error):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    logger.DEBUG("current working directory for %s" % mycwd)
    logger.DEBUG("current user's home directory for %s" % myhomedir)
    logger.DEBUG("ParseStartConfig for %s" % labname)
    lab_path          = os.path.join(LABS_ROOT,labname)
    is_valid_lab(lab_path)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
   
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role, logger)
    labtainer_config = ParseLabtainerConfig.ParseLabtainerConfig(LABTAINER_CONFIG, labname, logger)
    host_home_xfer = labtainer_config.host_home_xfer

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    if DoStop(start_config, labtainer_config, mycwd, labname, role, ignore_stop_error):
        # Inform user where results are stored
        print "Results stored in directory: %s" % host_xfer_dir

def DoMoreterm(labname, role, container, num_terminal):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    logger.DEBUG("current working directory for %s" % mycwd)
    logger.DEBUG("current user's home directory for %s" % myhomedir)
    logger.DEBUG("ParseStartConfig for %s" % labname)
    lab_path          = os.path.join(LABS_ROOT,labname)
    is_valid_lab(lab_path)
    config_path       = os.path.join(lab_path,"config")
    start_config_path = os.path.join(config_path,"start.config")

    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role, logger)

    mycontainer_name = '%s.%s.%s' % (labname, container, role)
    if not IsContainerCreated(mycontainer_name):
        logger.ERROR('container %s not found' % mycontainer_name)
        sys.exit(1)
    if not IsContainerRunning(mycontainer_name):
        logger.ERROR("Container %s is not running!\n" % (mycontainer_name))
        sys.exit(1)
    for x in range(num_terminal):
        spawn_command = "gnome-terminal -x docker exec -it %s bash -l &" % mycontainer_name
        logger.DEBUG("spawn_command is (%s)" % spawn_command)
        os.system(spawn_command)

