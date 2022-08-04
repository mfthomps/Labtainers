#!/bin/bash
#
# Rebuild the Labtianers Lab Editor UI
# Use -n to supress running the UI after rebuild.
#
/usr/bin/javac  ../MainUI/src/main/java/labtainers/goalsui/*.java ../MainUI/src/main/java/labtainers/resultsui/*.java ../MainUI/src/main/java/labtainers/paramsui/*.java ../MainUI/src/main/java/labtainers/mainui/*.java -d . -Xlint:unchecked || exit
jar cmf mainUI.mf ./MainUI.jar labtainers/mainui/*.class labtainers/goalsui/*.class labtainers/resultsui/*.class labtainers/paramsui/*.class ../MainUI/src/main/resources/* || exit
if [[ "$1" != "-n" ]]; then
    /usr/bin/java -jar MainUI.jar
fi
