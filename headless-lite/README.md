Here are the instructions to create a new labtainer.master file.
1. Make directory to house files from Git Repo and change dir to that directory. `mkdir foo && cd foo`
2. Git pull the files in this headless-lite folder. `git clone  https://github.com/mfthomps/Labtainers.git`
3. Move to that directory.  `cd Labtainers`
4. Change to the premaster branch `git checkout premaster`
5. Set $LABTAINERDIR to root of Git Repo Files. ``export $LABTAINERDIR=`pwd` ``
6. Copy the motd, docker-entrypoint, and wait-for-it.sh files to $LABTAINERDIR/scripts/designer/workspace_master folder 
`cd headless-lite && cp motd docker-entrypoint wait-for-it.sh ../scripts/designer/workspace_master/` 
7. Copy the Dockerfile.labtainer.master to $LABTAINERDIR/scripts/designer/workspace_master. 
`cp Dockerfile.labtainer.master ../scripts/designer/base_dockerfiles/`
8. Cd to correct directory. `cd ../scripts/designer/bin`
9. Run create_master_image.sh. `./create_master_image.sh`
10. Cd to headless-lite directory. `cd $LABTAINERDIR/headless-lite/`
11. Launch the containers using docker-compose.yml. `docker-compose up`
