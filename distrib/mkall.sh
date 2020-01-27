#/bin/bash
#
# Make distributions of labtainers
#
if [[ "$1" != "-q" ]]; then
    git status -s | grep -E "^ M|^ D|^ A" | less
fi
./mkdist.sh $@
result=$?
if [[ $result != 0 ]]; then
    echo "mkdist failed"
    exit 1
fi
./mk-devel-dist.sh $@
result=$?
if [[ $result != 0 ]]; then
    echo "mk-devel-dist failed"
    exit 1
fi
./mktest.sh $@
result=$?
if [[ $result != 0 ]]; then
    echo "mktest failed"
    exit 1
fi
echo "Done building Labtainers dist tars"
