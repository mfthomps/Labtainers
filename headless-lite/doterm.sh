#
# Start a gnome terminal and update labtainers if not yet done.
#
gnome-terminal --geometry 120x31+150+100 --working-directory=$HOME/labtainer/labtainer-student -e "bash -c \"/bin/cat README; exec bash\"" &
if [[ -f $HOME/labtainer/.doupdate ]]; then
    gnome-terminal --geometry 73x31+100+300 --working-directory=$HOME/labtainer -x ./update-labtainer.sh
    echo "ran update" >/tmp/update.log
fi

