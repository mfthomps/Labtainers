#!/bin/bash
labs=$(ls ../labs)
for l in $labs; do
    echo $l
    ../scripts/labtainer-student/bin/removelab.sh $l
done

