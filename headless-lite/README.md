# Quick Start
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
6. Create workspace_master folder. `mkdir -p ../scripts/designer/workspace_master/` 
7. Copy the motd, docker-entrypoint, and wait-for-it.sh files to $LABTAINER_DIR/scripts/designer/workspace_master folder.  
`cd headless-lite && cp motd docker-entrypoint wait-for-it.sh ../scripts/designer/workspace_master/` 
8. Copy the Dockerfile.labtainer.master to $LABTAINER_DIR/scripts/designer/workspace_master.   
`cp Dockerfile.labtainer.master ../scripts/designer/base_dockerfiles/`
9. Cd to correct directory. `cd ../scripts/designer/bin`
10. Run create_master_image.sh. `./create_master_image.sh`
11. The below docker-compose.yml leverages a container called harperaa/labtainer.master and may be pulled down from docker hub.  However, you may change that file, to use your own file, created by previous step, stored on your own docker hub.  You would do that as follows.  
a. Create an account on docker hub.  
b. Tag the container created in previous step (create_master_image.sh) to match harperaa/labtainer.master. `docker tag 259872983749[replace this with yours] harperaa/labtainer.master`.  
c. Optionally, use your own name and/or docker hub repository. Look at the ending output of above command (create_master_image.sh), copy and replace hash identifyer from your output in the following command:  
`docker tag 259872983749[replace this with yours] harperaa/labtainer.master[change this to your docker username and container]`.  
d. Optionally, push that image to dockerhub. `docker push harperaa/labtainer.master[change this to your docker username and container]`.  
11. Cd to headless-lite directory. `cd $LABTAINER_DIR/headless-lite/`
12. Optionally (if you changed the container name and container from above optional steps), then edit the docker-compose.yml file to rename that repo/container.  Again, if you choose to leave it as harperaa/labtainer.master, then no need to edit that file.
13. Launch the containers using docker-compose.yml. `docker-compose up`

