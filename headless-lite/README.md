# Quick Start [temporarily not updated version]
Here is the one liner, to run the headless-lite labtainer master container and web interface, from a linux/mac system with docker installed.  

`curl https://raw.githubusercontent.com/mfthomps/Labtainers/premaster/headless-lite/docker-compose.yml > docker-compose.yml && docker-compose up`

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
9. Run create_master_image.sh. `./create_headless_master.sh`
10. Cd to headless-lite directory (or open new shell tab). `cd $LABTAINER_DIR/headless-lite/`
11. Launch the containers using docker-compose.yml. `docker-compose up`
12. Open browser and goto http://localhost:6901/vnc.html (using pw from $LABTAINER_DIR/headless-lite/Dockerfile.labtainer.master, default: changeme)

Optionally (push container to hub.docker.com)
a. Create an account on docker hub.  
b. Tag the container created in previous steps (create_headline_master.sh) to match [your docker username]/labtainer.master. `docker tag 259872983749[replace this with your hash shown when running create_headline_master.sh] [your docker username]/labtainer.master`.  
c. Push that image to dockerhub. `docker push [your docker username]/labtainer.master`.  
d. Edit the docker-compose.yml file to rename that repo/container above.  
e. Test new docker-compose.yml file. `docker-compose up`.  This command should pull down that image from hub.docker.com.


