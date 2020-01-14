cat >>~/.profile <<EOL
if [[ -f $HOME/labtainer/.dosmoke ]]; then
    HOSTNAME=`hostname`
    myscript=/media/sf_SEED/test_vms/$HOSTNAME/dothis.sh
    if [[ -f $myscript ]]; then
        echo "run $myscript" > /tmp/profile.log
        gnome-terminal --geometry 120x31+150+300 -e "bash -c \"exec bash -c $myscript \"" &
    else
        echo "No script at $myscript , just do smoke test" > /tmp/profile.log
        gnome-terminal --geometry 120x31+150+300 --working-directory=$LABTAINER_DIR/setup_scripts -e "bash -c \"exec bash -c ./full-smoke-test.sh \"" &
   fi
fi
EOL
