#
# All non-Ubuntu 18 update logic should go here
#
#
$LABTAINER_DIR/setup_scripts/pull-all.py $test_flag 
grep "^Distribution created:" labtainer/trunk/README.md | awk '{print "Updated to release of: ", $3, $4}'
grep "^Branch:" labtainer/trunk/README.md | awk '{print "branch: ", $2}'
grep "^Revision:" labtainer/trunk/README.md | awk '{print "Revision: ", $2}'
grep "^Commit:" labtainer/trunk/README.md | awk '{print "Commit: ", $2}'
