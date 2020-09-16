Here are the instructions to create a new labtainer.master file.
1. Make directory to house files from Git Repo and change dir to that directory. `mkdir foo && cd foo`
2. Git pull the files in this headless-lite folder. `git clone  https://github.com/mfthomps/Labtainers.git`
3. Move to that directory.  `cd Labtainers`
4. Set $LABTAINERDIR to root of Git Repo Files. ``export $LABTAINERDIR=`pwd` ``
5. Copy the motd, docker-entrypoint, and wait-for-it.sh files to $LABTAINERDIR/scripts/designer/workspace_master folder
6. Copy the Dockerfile.labtainer.master to $LABTAINERDIR/scripts/designer/workspace_master
