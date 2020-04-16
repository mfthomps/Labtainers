#!/bin/bash
echo "If the labtainer.tar is not up to date, you may want to do that first!"
echo ""
echo ""
echo "start 18"
./test-ubuntu18.sh || exit 1
log18=$(./getLog.sh log-ubuntu18) || exit 1

echo "start 16"
./test-ubuntu16.sh || exit 1
log16=$(./getLog.sh log-ubuntu16) || exit 1

echo "log18 is $log18"
echo "log16 is $log16"

echo "wait 18"
./waitLog.py $log18 || exit 1
echo "wait 16"
./waitLog.py $log16 || exit 1
echo "Done"
