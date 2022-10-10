#!/bin/bash
check_docker() {
if [[ -f /usr/local/bin/docker ]]; then
    /usr/local/bin/docker ps
    result=$?
else
    /usr/bin/docker ps
    result=$?
fi
if [ ! $result = 0 ]; then
    echo "Docker Desktop not installed or not running" >>/tmp/lab-preinstall.log

    case "$OSTYPE" in
      solaris*) echo "SOLARIS" ;;
      darwin*)  
        osascript <<'END'
        set theDialogText to "Installation failed.  Docker Desktop is not running.  Make sure it is installed and running. Then open the installation package again."
        display dialog theDialogText buttons {"OK"} default button "OK"
END
            ;;
      linux*)   echo "LINUX" ;;
      bsd*)     echo "BSD" ;;
      msys*)    echo "WINDOWS" ;;
      *)        echo "unknown: $OSTYPE" ;;
    esac
    exit 1
fi

}


do_up() {
   printf "\n\nStarting Labtainers...\n"
   printf "When you see two 'done's below, open a browser and goto\n"
   printf "   http://localhost:6901/vnc.html?password=\n"
   printf "\n"
   printf "No password is needed, just click 'submit' if prompted.\n"
   printf "\n"
   printf "Use 'update-labtainer.sh' to update your Labtainers before the first use.\n"
   printf "\n"
   printf "Use ctrl-C to stop Headless Labtainers.\n"
   docker-compose up --no-recreate >> /tmp/headless.log
   printf "\nYour results are in ~/headless-labtainers/labtainer_xfer\n"
}

fix_it() {
case "$OSTYPE" in
  solaris*) echo "SOLARIS" ;;
  darwin*)  echo "fix up OSX" >> /tmp/headless.log
            # To work around a persistent problem on docker for mac, test if docker.sock.raw file exists or not, if not, then add symlink, see issue at https://github.com/docker/for-mac/issues/4755

            if [ ! -L "/var/run/docker.sock.raw" ]; then
               echo "Fixing Files for OSX" >> /tmp/headless.log
               # add link to docker.raw.sock, see issue at https://github.com/docker/for-mac/issues/4755
               sudo ln -s "$HOME/Library/Containers/com.docker.docker/Data/docker.raw.sock" /var/run/docker.sock.raw
               # now fix the docker-compose file to use the docker.sock.raw
               cd ~/headless-labtainers
               echo "Changes complete for OSX" >> /tmp/headless.log
            fi
            sed -i '' s%/var/run/docker.sock:/var/run/docker.sock%/var/run/docker.sock.raw:/var/run/docker.sock% docker-compose.yml
            ;;
  linux*)   echo "LINUX" ;;
  bsd*)     echo "BSD" ;;
  msys*)    echo "WINDOWS" ;;
  *)        echo "unknown: $OSTYPE" ;;
esac
}

#
#
#

export LABTAINER_UPDATE=""
export LABTAINER_DEV=""
export LABTAINER_TEST=""
export TEST_REGISTRY=""
while [ -n "$1" ]; do
    if [ "$1" = -h ]; then
        echo "-d to use your local yml file"
        echo "-n to supress updates on the container, e.g. if you created your own labtainer.tar"
        exit 0
    elif [ "$1" = -n ]; then
        export LABTAINER_UPDATE="FALSE"
        shift
    elif [ "$1" = -d ]; then
        LABTAINER_DEV="TRUE"
        shift
    elif [ "$1" = -t ]; then
        LABTAINER_TEST="TRUE"
        shift
    fi
done


if [ "$LABTAINER_TEST" = "TRUE" ];then
   export TEST_REGISTRY=TRUE
fi
if [ -d ./mystuff ]; then
    echo "Running Headless Labtainers."
    check_docker
    fix_it
    do_up
else
    echo "Installing and running Headless Labtainers."
    mkdir -p ~/headless-labtainers
    SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
    cp "$SCRIPTPATH/headless-labtainers.sh" ~/headless-labtainers
    cd ~/headless-labtainers
    mkdir -p mystuff
    mkdir -p labtainer_xfer
    mkdir -p labtainers
    if [ "$LABTAINER_DEV" = "TRUE" ];then
        echo "Using local yml"
        cp $LABTAINER_DIR/headless-lite/docker-compose.yml .
    elif [ "$LABTAINER_TEST" = "TRUE" ];then
        echo "Using labtainer.headless.tester"
        curl https://raw.githubusercontent.com/mfthomps/Labtainers/master/headless-lite/docker-compose.yml > docker-compose.yml 
        sed -i s%labtainers/labtainer.master.headless%testregistry:5000/labtainer.headless.tester% docker-compose.yml
        sed -i s%accetto/ubuntu-vnc-xfce%testregistry:5000/ubuntu-vnc-xfce% docker-compose.yml
        echo "frank@beans.com" > /home/labtainer/headless-labtainers/labtainers/email.txt
        labtainer_dns=$(systemd-resolve --status | grep "Current DNS S" | awk '{print $4}')
        sed -i "/TEST_REGISTRY.*/a \ \ \ \ \ \ - LABTAINER_DNS=$labtainer_dns" docker-compose.yml
        #
        #  guess this needs to be constantly changed
        #
        sudo chown root:docker /var/run/docker.sock
    else
        curl https://raw.githubusercontent.com/mfthomps/Labtainers/master/headless-lite/docker-compose.yml > docker-compose.yml 
    fi
    check_docker
    fix_it
    do_up
    HEADLESS_DIR=`pwd`
    echo "In the future, open a terminal, cd to"
    echo " $HEADLESS_DIR and run:"
    echo "./headless-labtainers.sh"
fi
