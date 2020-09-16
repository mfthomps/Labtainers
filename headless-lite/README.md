Here are the instructions to create a new labtainer.master file.
1. Make directory to house files from Git Repo and change dir to that directory. `mkdir foo && cd foo`
2. Set $LABTAINERDIR to root of Git Repo Files. `export $LABTAINERDIR=.`
3. Git pull the files in this headless-lite folder. `git pull 
4. Copy the motd, docker-entrypoint, and wait-for-it.sh files to $LABTAINERDIR/scripts/designer/workspace_master folder
5. Copy the Dockerfile.labtainer.master to $LABTAINERDIR/scripts/designer/workspace_master
