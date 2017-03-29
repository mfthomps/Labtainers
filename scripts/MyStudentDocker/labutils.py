import glob
import json
import md5
import os
import re
import subprocess
import sys
import time
import zipfile
from netaddr import *
import ParseStartConfig
import datetime
import getpass
LABS_ROOT = os.path.abspath("../../labs/")

# Error code returned by docker inspect
SUCCESS=0
FAILURE=1

def isalphadashscore(name):
    # check name - alphanumeric,dash,underscore
    return re.match(r'^[a-zA-Z0-9_-]*$', name)

# get docker0 IP address
def getDocker0IPAddr():
    command="ifconfig docker0 | awk '/inet addr:/ {print $2}' | sed 's/addr://'"
    #print "Command to execute is (%s)" % command
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    result = child.stdout.read().strip()
    #print "Result of subprocess.Popen getDocket0IPAddr is %s" % result
    return result

# Parameterize my_container_name container
def ParameterizeMyContainer(mycontainer_name, container_user, lab_instance_seed, user_email, labname):
    #print "About to call parameterize.sh with LAB_INSTANCE_SEED = (%s)" % lab_instance_seed
    command = 'docker exec -it %s script -q -c "/home/%s/.local/bin/parameterize.sh %s %s %s %s" /dev/null' % (mycontainer_name, container_user, lab_instance_seed, user_email, labname, mycontainer_name)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call ParameterizeMyContainer is %s" % result
    return result

# Start my_container_name container
def StartMyContainer(mycontainer_name):
    command = "docker start %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call StartMyContainer is %s" % result
    return result

# Check to see if my_container_name container has been created or not
def IsContainerCreated(mycontainer_name):
    command = "docker inspect -f {{.Created}} %s 2> /dev/null" % mycontainer_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call IsContainerCreated is %s" % result
    return result

def ConnectNetworkToContainer(mycontainer_name, mysubnet_name, mysubnet_ip):
    #print "Connecting more network subnet to container %s" % mycontainer_name
    command = "docker network connect --ip=%s %s %s 2> /dev/null" % (mysubnet_ip, mysubnet_name, mycontainer_name)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call ConnectNetworkToContainer is %s" % result
    return result

def CreateSingleContainer(mycontainer_name, mycontainer_image_name, mysubnet_name=None, mysubnet_ip=None):
    #print "Create Single Container"
    docker0_IPAddr = getDocker0IPAddr()
    #print "getDockerIPAddr result (%s)" % docker0_IPAddr
    if mysubnet_name:
        createsinglecommand = "docker create -t --network=%s --ip=%s --privileged --add-host my_host:%s --name=%s %s bash" % (mysubnet_name, mysubnet_ip, docker0_IPAddr, mycontainer_name, mycontainer_image_name)
    else:
        createsinglecommand = "docker create -t --privileged --add-host my_host:%s --name=%s %s bash" % (docker0_IPAddr, mycontainer_name, mycontainer_image_name)
    #print "Command to execute is (%s)" % createsinglecommand
    result = subprocess.call(createsinglecommand, shell=True)
    #print "Result of subprocess.call CreateSingleContainer is %s" % result
    return result


# Create SUBNETS
def CreateSubnets(subnets):
    #for (subnet_name, subnet_network_mask) in networklist.iteritems():
    for subnet_name in subnets:
        subnet_network_mask = subnets[subnet_name].mask
        #print "subnet_name is %s" % subnet_name
        #print "subnet_network_mask is %s" % subnet_network_mask

        command = "docker network inspect %s > /dev/null" % subnet_name
        #print "Command to execute is (%s)" % command
        inspect_result = subprocess.call(command, shell=True)
        #print "Result of subprocess.call CreateSubnets docker network inspect is %s" % inspect_result
        if inspect_result == FAILURE:
            # Fail means does not exist - then we can create
            if subnets[subnet_name].gateway != None:
                #print subnets[subnet_name].gateway
                subnet_gateway = subnets[subnet_name].gateway
                command = "docker network create -d bridge --gateway=%s --subnet %s %s 2> /dev/null" % (subnet_gateway, subnet_network_mask, subnet_name)
            else:
                command = "docker network create -d bridge --subnet %s %s 2> /dev/null" % (subnet_network_mask, subnet_name)
            #print "Command to execute is (%s)" % command
            create_result = subprocess.call(command, shell=True)
            #print "Result of subprocess.call CreateSubnets docker network create is %s" % create_result
            if create_result == FAILURE:
                sys.stderr.write("ERROR: Failed to create %s subnet at %s!\n" % (subnet_name, subnet_network_mask))
                sys.exit(1)
        else:
            print "Already exists! Not creating %s subnet at %s!\n" % (subnet_name, subnet_network_mask)
       
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

def ParamForStudent(lab_master_seed, mycontainer_name, container_user, labname):
    done = False
    while not done:
        done = True
        # Prompt user for e-mail address
        eprompt = 'Please enter your e-mail address '
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
    #print mymd5_hex_string

    parameterize_result = ParameterizeMyContainer(mycontainer_name, container_user, mymd5_hex_string,
                                                          user_email, labname)
    if parameterize_result == FAILURE:
        sys.stderr.write("ERROR: Failed to parameterize lab container %s!\n" % mycontainer_name)
        sys.exit(1)

# Copy Students' Artifacts from host to instructor's lab container
def CopyStudentArtifacts(start_config, mycontainer_name, labname, container_user):
    host_home_xfer = start_config.host_home_xfer
    # Set the lab name 
    command = 'docker exec -it %s script -q -c "echo %s > /home/%s/.local/.labname" /dev/null' % (mycontainer_name, labname, container_user)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call CopyStudentArtifacts set labname is %s" % result
    if result == FAILURE:
        sys.stderr.write("ERROR: Failed to set labname in container %s!\n" % mycontainer_name)
        sys.exit(1)

    username = getpass.getuser()
    # Copy zip files from 'Shared' folder to 'home/$CONTAINER_USER'
    zip_filelist = glob.glob('/home/%s/%s/*.zip' % (username, host_home_xfer))
    #print "filenames is (%s)" % zip_filelist
    for fname in zip_filelist:
        #print "name is %s" % fname
        base_fname = os.path.basename(fname)
        # Copy zip file and chown it
        command = 'docker cp %s %s:/home/%s/' % (fname, mycontainer_name, container_user)
        #print "Command to execute is (%s)" % command
        result = subprocess.call(command, shell=True)
        #print "Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s" % (fname, result)
        if result == FAILURE:
            sys.stderr.write("ERROR: Failed to set labname in container %s!\n" % mycontainer_name)
            sys.exit(1)
        command = 'docker exec -it %s sudo chown %s:%s /home/%s/%s' % (mycontainer_name, container_user, container_user, container_user, base_fname)
        #print "Command to execute is (%s)" % command
        result = subprocess.call(command, shell=True)
        #print "Result of subprocess.call CopyStudentArtifacts copy zipfile (%s) is %s" % (fname, result)
        if result == FAILURE:
            sys.stderr.write("ERROR: Failed to set labname in container %s!\n" % mycontainer_name)
            sys.exit(1)

def DoStart(start_config, labname, role):
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    #print "Do: START Multiple Containers and/or multi-home networking"
    docker0_IPAddr = getDocker0IPAddr()
    #print "getDockerIPAddr result (%s)" % docker0_IPAddr

    # Create SUBNETS
    CreateSubnets(start_config.subnets)

    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        container_user         = container.user

        haveContainer = IsContainerCreated(mycontainer_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # Set need_seeds=False first
        need_seeds=False

        # IsContainerCreated returned FAILURE if container does not exists
        if haveContainer == FAILURE:
            # Container does not exist, create the container
            # Use CreateSingleContainer()
            if len(container.container_nets) == 0:
                containerCreated = CreateSingleContainer(mycontainer_name, mycontainer_image_name)
            else:
                mysubnet_name, mysubnet_ip = container.container_nets.popitem()
                containerCreated = CreateSingleContainer(mycontainer_name, mycontainer_image_name,
                                                         mysubnet_name, mysubnet_ip)
                
            #print "CreateSingleContainer result (%s)" % containerCreated
            # Give the container some time -- just in case
            time.sleep(3)
            # If we just create it, then set need_seeds=True
            need_seeds=True

            for mysubnet_name, mysubnet_ip in container.container_nets.items():
                connectNetworkResult = ConnectNetworkToContainer(mycontainer_name, mysubnet_name, mysubnet_ip)

        # Check again - 
        haveContainer = IsContainerCreated(mycontainer_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # IsContainerCreated returned FAILURE if container does not exists
        if haveContainer == FAILURE:
            sys.stderr.write("ERROR: DoStartMultiple Container %s still not created!\n" % mycontainer_name)
            sys.exit(1)
        else:
            # Start the container
            start_result = StartMyContainer(mycontainer_name)
            if start_result == FAILURE:
                sys.stderr.write("ERROR: DoStartMultiple Container %s failed to start!\n" % mycontainer_name)
                sys.exit(1)

        if role == 'instructor':
            '''
            Copy students' artifacts only to the container where 'Instructor.py' supposed
            to be run - where grades.txt will later reside also (i.e., don't copy to all containers)
            Copy to container named start_config.grade_container
            '''
            if mycontainer_name == start_config.grade_container:
                copy_result = CopyStudentArtifacts(start_config, mycontainer_name, labname, container_user)
                if copy_result == FAILURE:
                    sys.stderr.write("ERROR: DoStartMultiple Failed to copy students' artifacts to container %s!\n" % mycontainer_name)
                    sys.exit(1)
        # If the container is just created, prompt user's e-mail
        # then parameterize the container
        elif need_seeds and role == 'student':
            ParamForStudent(lab_master_seed, mycontainer_name, container_user, labname)
    
    # Reach here - Everything is OK - spawn terminal for each container based on num_terminal
    for container in start_config.containers.values():
        num_terminal = container.terminals
        mycontainer_name = container.full_name
        #print "Number of terminal is %d" % num_terminal
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
    #print "host_home_xfer directory (%s)" % host_xfer_dir
    if os.path.exists(host_xfer_dir):
        # exists but is not a directory
        if not os.path.isdir(host_xfer_dir):
            # remove file then create directory
            os.remove(host_xfer_dir)
            os.makedirs(host_xfer_dir)
        #else:
        #    print "host_home_xfer directory (%s) exists" % host_xfer_dir
    else:
        # does not exists, create directory
        os.makedirs(host_xfer_dir)

# CopyChownGradesFile
def CopyChownGradesFile(mycwd, start_config, container_name, container_image, container_user):
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed

    username = getpass.getuser()
    grade_filename = '/home/%s/grades.txt' % container_user
    command = "docker cp %s:%s /home/%s/%s" % (container_name, grade_filename, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec cp grades.txt file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CopyChownGradesFile Container %s fail on executing cp grades.txt file!\n" % container_name)
        sys.exit(1)

    # Change ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/grades.txt" % (username, username, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CopyChownGradesFile: Result of subprocess.Popen exec chown grades.txt file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CopyChownGradesFile Container %s fail on executing chown grades.txt file!\n" % container_name)
        sys.exit(1)

def StartLab(labname, role):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
   
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role)

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, start_config.host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    DoStart(start_config, labname, role)

def FileModLater(ts, fname):
    ''' is the given file later than the timestamp (which is in UTC)? '''
    df_time = os.path.getmtime(fname)
    #print('df ts %s' % df_time)

    df_string = datetime.datetime.fromtimestamp(df_time)
    #print('df_local time is %s' % df_string)

    df_utc_string = str(datetime.datetime.utcfromtimestamp(df_time))
    parts = df_utc_string.split('.')
    df_ts = time.mktime(time.strptime(parts[0], "%Y-%m-%d %H:%M:%S"))

    #print('df_utc time is %s' % df_utc_string)
    #print('df_utc ts is %s' % df_ts)
    if df_ts > ts:
        return True
    else:
        return False

def CheckBuild(labname, image_name, container_name, name):
    '''
    Determine if a container image needs to be rebuilt.
    '''
    retval = False
    print('check build for container %s image %s' % (container_name, image_name))
    cmd = "docker inspect -f '{{.Created}}' %s" % image_name
    child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    result = child.stdout.read().strip()
    if 'Error:' in result or len(result.strip()) == 0:
        return True
    print('result is %s' % result)
    parts = result.strip().split('.')
    time_string = parts[0]
    #print('image time string %s' % time_string)
    ts = time.mktime(time.strptime(time_string, "%Y-%m-%dT%H:%M:%S"))
    #print('image ts %s' % ts)
    lab_path = os.path.join(LABS_ROOT,labname)
    df_name = 'Dockerfile.%s' % container_name
    df = os.path.join(lab_path, 'dockerfiles', df_name)
    if FileModLater(ts, df):
        print('dockerfile changed, would build')
        retval = True
    else:
        container_dir = os.path.join(lab_path, name)
        #print('container dir %s' % container_dir)
        for folder, subs, files in os.walk(container_dir):
            for f in files:
               f_path = os.path.join(folder, f)
               if FileModLater(ts, f_path):
                   print('%s is later, would build' % f_path)
                   retval = True
                   break
    return retval

def RedoLab(labname, role):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role)
    StopLab(labname, role)
    build_student = './buildImage.sh'
    build_instructor = './buildInstructorImage.sh'
    for name, container in start_config.containers.items():
        mycontainer_name       = container.full_name
        mycontainer_image_name = container.image_name
        cmd = 'docker rm %s' % mycontainer_name
        os.system(cmd)
        if CheckBuild(labname, mycontainer_image_name, mycontainer_name, name):
            if os.path.isfile(build_student):
                cmd = '%s %s' % (build_student, labname)
            elif os.path.isfile(build_instructor):
                cmd = '%s %s' % (build_instructor, labname)
            else:
                sys.stderr.write("ERROR: RedoLab, no image rebuild script")
                exit(1)
                 
            os.system(cmd)
    StartLab(labname, role)


# CreateCopyChownZip
def CreateCopyChownZip(mycwd, start_config, container_name, container_image, container_user):
    #TODO: FIX
    host_home_xfer  = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed

    # Run 'Student.py' - This will create zip file of the result
#   print "About to call Student.py"
    bash_command = "'cd ; . .profile ; Student.py'"
#   bash_command = "'cd ; . .bash_profile ; Student.py'"
    command = 'docker exec -it %s script -q -c "/bin/bash -c %s" /dev/null' % (container_name, bash_command)
#   print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
#   print "CreateCopyChownZip: Result of subprocess.call exec Student.py is %s" % result
    if result == FAILURE:
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing Student.py!\n" % container_name)
        sys.exit(1)

    username = getpass.getuser()
    command='docker exec -it %s cat /home/%s/.local/zip.flist' % (container_name, container_user)
#   print "Command to execute is (%s)" % command
    child = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    orig_zipfilenameext = child.stdout.read().strip()
#   print "CreateCopyChownZip: Result of subprocess.Popen exec cat zip.flist is %s" % orig_zipfilenameext
    if orig_zipfilenameext == None:
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing cat zip.flist!\n" % container_name)
        sys.exit(1)

    # The zip filename created by Student.py has the format of e-mail.labname.zip
    orig_zipfilename, orig_zipext = os.path.splitext(orig_zipfilenameext)
    baseZipFilename = os.path.basename(orig_zipfilename)
    #NOTE: Use the '=' to separate e-mail+lab_name from the container_name
    DestZipFilename = '%s=%s.zip' % (baseZipFilename, container_name)
    command = "docker cp %s:%s /home/%s/%s/%s" % (container_name, orig_zipfilenameext, username, host_home_xfer, DestZipFilename)
#   print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CreateCopyChownZip: Result of subprocess.Popen exec cp zip file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing cp zip file!\n" % container_name)
        sys.exit(1)

    # Change ownership to defined user $USER
    command = "sudo chown %s:%s /home/%s/%s/*.zip" % (username, username, username, host_home_xfer)
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "CreateCopyChownZip: Result of subprocess.Popen exec chown zip file is %s" % result
    if result == FAILURE:
        StopMyContainer(mycwd, start_config, container_name)
        sys.stderr.write("ERROR: CreateCopyChownZip Container %s fail on executing chown zip file!\n" % container_name)
        sys.exit(1)


# Stop my_container_name container
def StopMyContainer(mycwd, start_config, container_name):
    command = "docker stop %s 2> /dev/null" % container_name
    #print "Command to execute is (%s)" % command
    result = subprocess.call(command, shell=True)
    #print "Result of subprocess.call StopMyContainer stop is %s" % result
    return result

def IsContainerRunning(mycontainer_name):
    try:
        s = subprocess.check_output('docker ps', shell=True)
    except:
        return False
    if mycontainer_name in s:
        return True
    else:
        return False 


def DoStop(start_config, mycwd, labname, role):
    retval = True
    host_home_xfer = start_config.host_home_xfer
    lab_master_seed = start_config.lab_master_seed
    #print "Do: STOP Multiple Containers and/or multi-home networking"

    for name, container in start_config.containers.items():
        mycontainer_name  = container.full_name
        container_user    = container.user
        mycontainer_image = container.image_name
        haveContainer     = IsContainerCreated(mycontainer_name)
        #print "IsContainerCreated result (%s)" % haveContainer

        # IsContainerCreated returned FAILURE if container does not exists
        # error: can't stop non-existent container
        if haveContainer == FAILURE:
            sys.stderr.write("ERROR: DoStopMultiple Container %s does not exist!\n" % mycontainer_name)
            retval = False
        elif not IsContainerRunning(mycontainer_name):
            sys.stderr.write("container %s not running\n" % (mycontainer_name))
            retval = False
        else:
            if role == 'instructor':
                if mycontainer_name == start_config.grade_container:
                    CopyChownGradesFile(mycwd, start_config, mycontainer_name, mycontainer_image, container_user)
            else:
                # Before stopping a container, run 'Student.py'
                # This will create zip file of the result
                CreateCopyChownZip(mycwd, start_config, mycontainer_name, mycontainer_image, container_user)
            # Stop the container
            StopMyContainer(mycwd, start_config, mycontainer_name)

    return retval

def StopLab(labname, role):
    mycwd = os.getcwd()
    myhomedir = os.environ['HOME']
    #print "current working directory for %s" % mycwd
    #print "current user's home directory for %s" % myhomedir
    #print "ParseStartConfig for %s" % labname
    lab_path          = os.path.join(LABS_ROOT,labname)
    config_path       = os.path.join(lab_path,"config") 
    start_config_path = os.path.join(config_path,"start.config")
   
    start_config = ParseStartConfig.ParseStartConfig(start_config_path, labname, role)

    # Check existence of /home/$USER/$HOST_HOME_XFER directory - create if necessary
    host_xfer_dir = '%s/%s' % (myhomedir, start_config.host_home_xfer)
    CreateHostHomeXfer(host_xfer_dir)

    if DoStop(start_config, mycwd, labname, role):
        # Inform user where results are stored
        print "Results stored in directory: %s" % host_xfer_dir
