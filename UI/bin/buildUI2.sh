#!/bin/bash

javac  ../MainUI/src/main/java/labtainers/goalsui/*.java ../MainUI/src/main/java/labtainers/resultsui/*.java ../MainUI/src/main/java/labtainers/mainui/*.java -d . -Xlint:unchecked || exit
jar cmf mainUI.mf ./MainUI.jar labtainers/mainui/*.class labtainers/goalsui/*.class labtainers/resultsui/*.class || exit
java -jar MainUI.jar
#java MainWindow
