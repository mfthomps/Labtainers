#~/bin/bash
#
# Make distributions of labtainers
#
git status -s | grep -E "^ M|^ D|^ A" | less
./mkdist.sh $@
./mk-devel-dist.sh $@
./mktest.sh $@
echo "Done building Labtainers dist tars"
