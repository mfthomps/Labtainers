#!/bin/bash
cd $LABTAINER_DIR/distrib
./mkdist.sh
./mktest.sh
cd $LABTAINER_DIR/scripts/designer/bin
./create_master_headless.sh -d
./create_headless_tester.sh
docker push testregistry:5000/labtainer.headless.tester
cd $LABTAINER_DIR/headless-lite
cp install-headless.sh /media/sf_SEED/multipass/
echo "push any git updates"
echo "reinstall the server and run install_headless.sh -t"
