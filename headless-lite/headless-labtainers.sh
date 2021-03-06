#!/bin/bash
function do_up {
   echo "When you see two 'done's below, open a browser and goto http://localhost:6901/vnc.html?password="
   echo "No password is needed, just click 'submit' if prompted."
   echo "Use ctrl-C to stop Headless Labtainers."
   docker-compose up >> /tmp/headless.log
   echo "Your results are in ~/headless-labtainers/labtainer_xfer"
}

case "$OSTYPE" in
  solaris*) echo "SOLARIS" ;;
  darwin*)  echo "OSX"
            # To work around a persistent problem on docker for mac, test if docker.sock.raw file exists or not, if not, then add symlink, see issue at https://github.com/docker/for-mac/issues/4755

            if [ ! -L "/var/run/docker.sock.raw" ]; then
               echo "Fixing Files for OSX"
               # add link to docker.raw.sock, see issue at https://github.com/docker/for-mac/issues/4755
               sudo ln -s "$HOME/Library/Containers/com.docker.docker/Data/docker.raw.sock" /var/run/docker.sock.raw
               # now fix the docker-compose file to use the docker.sock.raw
               sed -i '' s%/var/run/docker.sock:/var/run/docker.sock%/var/run/docker.sock.raw:/var/run/docker.sock% docker-compose.yml
               echo "Changes complete for OSX"
            fi
            ;;
  linux*)   echo "LINUX" ;;
  bsd*)     echo "BSD" ;;
  msys*)    echo "WINDOWS" ;;
  *)        echo "unknown: $OSTYPE" ;;
esac


while [[ -n "$1" ]]; do
    if [[ "$1" == -h ]]; then
        echo "-d to use your local yml file"
        echo "-n to supress updates on the container, e.g. if you created your own labtainer.tar"
        exit 0
    elif [[ "$1" == -n ]]; then
        export LABTAINER_UPDATE="FALSE"
        shift
    elif [[ "$1" == -d ]]; then
        LABTAINER_DEV="TRUE"
        shift
    elif [[ "$1" == -t ]]; then
        LABTAINER_TEST="TRUE"
        shift
    fi
done

if [[ "$LABTAINER_TEST" == "TRUE" ]];then
   export TEST_REGISTRY=TRUE
fi
if [[ -d ./mystuff ]]; then
    echo "Running Headless Labtainers."
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
    if [[ "$LABTAINER_DEV" == "TRUE" ]];then
        echo "Using local yml"
        cp $LABTAINER_DIR/headless-lite/docker-compose.yml .
    elif [[ "$LABTAINER_TEST" == "TRUE" ]];then
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
    do_up
    HEADLESS_DIR=`pwd`
    echo "Add $HEADLESS_DIR to your PATH environment variable and run headless-labtainers from there in the future."
fi
