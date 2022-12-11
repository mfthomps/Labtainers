#
# Start a gnome terminal and update labtainers if not yet done.
#
exec > >(tee "/tmp/doterm.log") 2>&1
target=~/.bashrc
grep "lab-completion.bash" $target >>/dev/null
result=$?
if [[ result -ne 0 ]];then
   echo 'source $LABTAINER_DIR/setup_scripts/lab-completion.bash' >> $target
fi
source $LABTAINER_DIR/setup_scripts/lab-completion.bash
#
# fix link in README file
#
sed -i '1,/student/{s%student/labtainer%labtainer/labtainer%}' $HOME/labtainer/trunk/scripts/labtainer-student/README
/usr/bin/waitForX.sh 
gnome-terminal --geometry 120x31+150+100 --working-directory=$HOME/labtainer/labtainer-student -- bash -c "exit" 
sleep 2
gnome-terminal --geometry 120x31+150+100 --working-directory=$HOME/labtainer/labtainer-student -- bash -c "/bin/cat README; exec bash" 
if [[ -f $HOME/labtainer/.doupdate ]] && [[ "$LABTAINER_UPDATE" != 'FALSE' ]]; then
    xterm -e  /home/labtainer/.doupdate.sh
    rm $HOME/labtainer/.doupdate
fi

