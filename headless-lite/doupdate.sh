cd $LABTAINER_DIR/..
wget --quiet https://github.com/mfthomps/Labtainers/releases/latest/download/labtainer.tar -O labtainer.tar
echo "doing update of labtainer" >/tmp/update.log
sync
cd ..
tar xf labtainer/labtainer.tar --keep-newer-files --warning=none
sleep 1
