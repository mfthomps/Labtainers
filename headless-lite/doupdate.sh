cd $LABTAINER_DIR/..
#wget -vv -4 https://nps.box.com/shared/static/afz87ok8ezr0vtyo2qtlqbfmc28zk08j.tar -O labtainer.tar
wget -vv -4  https://nps.edu/documents/107523844/117289221/labtainer.tar -O labtainer.tar
sync
cd ..
tar xf labtainer/labtainer.tar --keep-newer-files --warning=none
sleep 10
