Here are the instructions to create a new labtainer.master file.

Prereqs: linux system with git and docker installed.  Note: Labtainer VM is a good place to do this.

1. Make directory to house files from Git Repo and change dir to that directory. `mkdir foo && cd foo`
2. Pull down files from Git repository. `git clone  https://github.com/mfthomps/Labtainers.git`
3. Move to that directory.  `cd Labtainers`
4. Change to the premaster branch `git checkout premaster`
5. Set $LABTAINER_DIR to root of Git Repo Files. ``export $LABTAINER_DIR=`pwd` ``
6. Create workspace_master folder. `mkdir -p ../scripts/designer/workspace_master/` 
7. Copy the motd, docker-entrypoint, and wait-for-it.sh files to $LABTAINER_DIR/scripts/designer/workspace_master folder 
`cd headless-lite && cp motd docker-entrypoint wait-for-it.sh ../scripts/designer/workspace_master/` 
8. Copy the Dockerfile.labtainer.master to $LABTAINER_DIR/scripts/designer/workspace_master. 
`cp Dockerfile.labtainer.master ../scripts/designer/base_dockerfiles/`
9. Cd to correct directory. `cd ../scripts/designer/bin`
10. Run create_master_image.sh. `./create_master_image.sh`
11. Cd to headless-lite directory. `cd $LABTAINER_DIR/headless-lite/`
12. Launch the containers using docker-compose.yml. `docker-compose up`
