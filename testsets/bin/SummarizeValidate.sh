#!/bin/bash

VALIDATE_DIR="../validate"
VALIDATE_SUMMARY="../validate/summary.txt"

VALIDATE_SETS=`ls $VALIDATE_DIR`

echo "Validate testsets summary: " > $VALIDATE_SUMMARY
for testname in $VALIDATE_SETS
do
    echo "Current test name is ($testname)"
    echo -n "$testname : " >> $VALIDATE_SUMMARY
    cat $VALIDATE_DIR/$testname/about.txt >> $VALIDATE_SUMMARY
done

