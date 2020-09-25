# Quick Start [temporarily not updated to latest version of image]
Here is the one liner, to run the headless-lite labtainer master container and web interface, from a linux/mac system with docker installed.  

`curl https://raw.githubusercontent.com/mfthomps/Labtainers/premaster/headless-lite/docker-compose.yml > docker-compose.yml && docker-compose up`

# Options for the yml
UPDATE_LABTAINER=FALSE will prevent an update from the latest distribution.  This is helpful when testing with a modified framework.

The VNC_PW value is empty, allowing the user to simply click OK.
It would be nice if the password can be supressed entirely.

The VNC_RESOLTION controls the desktop size.  How best to let the user adjust this, other than editing a file?

# Other issues
X11 applications such as wireshark often start with blank windows, requiring a restart of the application.  The problem
also occurs to some degree on VMs, and frequently on VMWare Horizon hosted VMs.  Or so it seems.  It is likely just an
X11/Docker issue that happends everywhere.

For now, users sit through long downloads as they do labs.  For example, if they've never done a lab that uses the
labtainer.firefox base, and then run one, the are warned of a download of hundres of MB.  Better to download all
base images on first start?   If added, need an ENV to supress it for testing.

Best way to for users to start headless Labtainers on their own systems?  Assume able to use command line, and just
give them instructions to wget (or save file via browser), etc.?  The Windows curl/wget is MSed and requires special
arguments to just fetch a file without interleaving html fu.  Not sure what those are yet.

Do we want a per-OS script for use in getting the yml and doing the compose?  Same script could have options to
update the headless system (otherwise, user must use docker rmi to remove old headless image).


# Build the labtainer.master File

Here are the instructions to create a new labtainer.master file.

Prereqs: linux system with git and docker installed.  Note: Labtainer VM is a good place to do this.

1. Make directory to house files from Git Repo and change dir to that directory. `mkdir foo && cd foo`
2. Pull down files from Git repository. `git clone  https://github.com/mfthomps/Labtainers.git`
3. Move to that directory.  `cd Labtainers`
4. Change to the premaster branch `git checkout premaster`
5. Set $LABTAINER_DIR to root of Git Repo Files. ``export LABTAINER_DIR=`pwd` ``
6. Cd to correct directory to update labtainer.tar. `cd distrib`.  
7. Update the labtainer.tar file `./mkdist.sh`.  Ignore errors.  
8. Cd to correct directory to build image. `cd ../scripts/designer/bin`
9. Run scripts to create the image in two stages: `./create_headless_master_stage_1.sh && ./create_headless_master_stage_2.sh`.  These were separated to make subsequent builds faster, ie. if you only need to update configuration files, you only need to run the second stage.
10. Cd to headless-lite directory (or open new shell tab). `cd $LABTAINER_DIR/headless-lite/`
11. Launch the containers using docker-compose.yml. `docker-compose up`
12. Open browser and goto http://localhost:6901/vnc.html (using pw from $LABTAINER_DIR/headless-lite/Dockerfile.labtainer.master.stage.2, default is: changeme. Also the sudo password is found in the same file, default is: labtainer)

Optionally (push container to hub.docker.com)
a. Create an account on docker hub.  
b. Tag the container created in previous steps (create_headline_master.sh) to match [your docker username]/labtainer.master. `docker tag 259872983749[replace this with your hash shown when running create_headline_master_stage_2.sh] [your docker username]/labtainer.master`.  
c. Push that image to dockerhub. `docker push [your docker username]/labtainer.master`.  
d. Edit the docker-compose.yml file to rename that repo/container above.  
e. Test new docker-compose.yml file. `docker-compose up`.  This command should pull down that image from hub.docker.com.


