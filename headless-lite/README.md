# Headless Labtainers
Run Labtainers on systems that lack X11 desktops.  This assumes you have installed Docker, e.g., Docker Desktop on a Mac or
Windows machine.  Headless Labtainers are an alternative to the Labtainer VM Appliance.

# Quick Start 
Execute the ./headless-labtainers.sh script.  Or download from 
   https://raw.githubusercontent.com/mfthomps/Labtainers/premaster/headless-lite/headless-labtainers.sh 
and make executable and then run.
On a Mac, this would be done from a terminal.  On Windows, use Powershell.

* Use the -d option to use your modified local docker-compose.yml file rather than the current one in the Labtainers repo.
* Use the -n option to suppress updating of Labtainers on headless container, e.g., if you've created your own labtainer.tar

Open a browser and goto http://localhost:6901/vnc.html?password= (uses blank default password, which is changable in docker-compose.yml).  

In addition to starting the Headless Labtainers, the script will create a ~/headless-labtainers directory.  A student would then run
headless-labtainers.sh from that directory in the future.  That directory will also contain persistent data.

**Warning**: if you run docker-compose directly prior to running headless-labtainers.sh, you may end up with broken file 
permissions (though running it directly after first running headless-labtainers.sh should work fine).

# Security considerations
Please note that Docker runs as a privileged service on your computer, and Labtainers containers run as privileged containers.
If you have sensitive data on your computer, you should understand the isolation provided by Dockers on your system.  An alternative
is to use one of our virtual machine appliances rather than running Docker directly on your computer.

# Developer notes
The following assume you have cloned or otherwise replicated the Labtainers repo.

You can modify the headless containers by editing the yml file and using the "-d" option on headless-labtainers.sh,
running the script from the repo.  To modify the headless container, modify the Dockerfiles and/or the docker-entryentrypoint script.
Rebuild the local container images from the scripts/designer/bin directory using the create\_master\_headless.sh script.
The default will populate the headless container with the latest Labtainers distribution.  Use the "-d" option to force use of your own
labtainers.tar created using distrib/mkdist.sh.  Note however that script assumes you have first created a Labtainers development
environment as described in docs/development/development.pdf

# Labtainers via remote server
Headless Labtainers can be deployed on servers, e.g., on headless VMs upon which Docker Compose is installed.  A notional summary
of such a deployment is provided below.  In this example, each student VM is assumed to be allocated its own IP address.

* Provision one VM per student with an SSH Server, Docker and Docker Compose installed.
* Add a "labtainer" user to the VM.
* Add the headless-labtainers.sh script to the VM, run it, and configure it to run as a service from ~/labtainers-student as user labtainer.
* Allocate at least 2GB and 2 cores to each VM.
* Provide students with SSH access to the VM, e.g., allocate SSH keys or configure the VMs to authenticte via LDAP.
* Direct students to configure their SSH private key (if needed) and to use an SSH command from a PowerShell or Mac terminal such as:
>  ssh -AfN -L 6901:127.0.0.1:6901 -oStrictHostKeyChecking=no -oUserKnownHostsFile=/dev/null -o "ServerAliveInterval 60" labtainer@my\_vm\_ip
   where "my\_vm\_ip" is the IP of their VM, or host witin their SSH config file.
* Students would then access their Labtainers from a browser pointed to http://localhost:6901
* Direct students to retrieve their results zip files from their VM using scp, e.g.,
>  scp labtainer@my\_vm\_ip:~/headless-labtainers/labtainer\_xfer/[lab]/\*.zip .

# Issues and ToDo

The VNC_PW value is in the yml empty, allowing the user to simply click OK.
It would be nice if the password can be suppressed entirely.

The VNC_RESOLTION controls the desktop size.  How best to let the user adjust this, other than editing a file?
Using -resize=scale, let student adjust to taste?

Get a full smoketest running on a headless rig.
Create a user's guide that details headless-specific issues such as changing resolution, running, etc.

X11 applications such as wireshark often start with blank windows, requiring a restart of the application.  The problem
also occurs to some degree on VMs, and frequently on VMWare Horizon hosted VMs.  Or so it seems.  It is likely just an
X11/Docker issue that happens everywhere.

For now, users sit through long downloads as they do labs.  For example, if they've never done a lab that uses the
labtainer.firefox base, and then run one, the are warned of a download of hundreds of MB.  Better to download all
base images on first start?   If added, need an ENV to supress it for testing.

What do we say/know about the security of Windows/Mac Docker containers environments?  We never say people can trust Docker or our 
containers, suggesting instead that the VM provides the isolation from sensitive data and applications that coexist on the student
laptop.  The Windows/Mac Docker environments appear to be some kind of
sandbox or VM.  Can we say anything about that?  I guess we need to at least suggest to not install Labtainers on systems that run other containers
that may handle sensitive data.

Time on the labtainer container is in UTC.  Make localtime?

Lab guides and other references tell students their results are found in ~/labtainer\_xfer/[lab].  How best to avoid confusion since
with Headless Labtainers, that directory on the headless container is mapped to ~/headless-labtainers/labtainer\_xfer on the student's computer?



The following is mostly OBE.  Revise/remove?
# Build the labtainer.master File

Here are the instructions to create a new labtainer.master file.

Prereqs: linux system with git and docker installed.  Note: Labtainer VM is a good place to do this.

1. Make directory to house files from Git Repo and change dir to that directory. `mkdir foo && cd foo`
2. Pull down files from Git repository. `git clone  https://github.com/mfthomps/Labtainers.git`
3. Move to that directory.  `cd Labtainers`
4. Change to the premaster branch `git checkout premaster`
5. Set $LABTAINER_DIR to root of Git Repo Files. ``export LABTAINER_DIR=`pwd` ``
6. Cd to correct directory to update labtainer.tar. `cd distrib`. 
7. Ensure you have latex installed, to build the pdfs for labs. `sudo apt install texlive-full`.  
8. Update the labtainer.tar file `./mkdist.sh`.  Ignore errors.  
9. Cd to correct directory to build image. `cd ../scripts/designer/bin`
10. Run scripts to create the image in two stages: `./create_headless_master_stage_1.sh && ./create_headless_master_stage_2.sh`.  These were separated to make subsequent builds faster, ie. if you only need to update configuration files, you only need to run the second stage.
11. Cd to headless-lite directory (or open new shell tab). `cd $LABTAINER_DIR/headless-lite/`
12. Launch the containers using docker-compose.yml. `docker-compose up`
13. Open browser and goto http://localhost:6901/vnc.html?password= (uses blank default password, which is changable in docker-compose.yml).  

Optionally (push container to hub.docker.com)
a. Create an account on docker hub.  
b. Tag the container created in previous steps (create_headline_master.sh) to match [your docker username]/labtainer.master. `docker tag 259872983749[replace this with your hash shown when running create_headline_master_stage_2.sh] [your docker username]/labtainer.master`.  
c. Push that image to dockerhub. `docker push [your docker username]/labtainer.master`.  
d. Edit the docker-compose.yml file to rename that repo/container above.  
e. Test new docker-compose.yml file. `docker-compose up`.  This command should pull down that image from hub.docker.com.


