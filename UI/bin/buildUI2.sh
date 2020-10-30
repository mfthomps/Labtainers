#!/bin/bash

javac  -classpath /media/sf_SEED/jars/commons-io-2.8.0/commons-io-2.8.0.jar ../MainUI/src/main/java/labtainers/goalsui/*.java ../MainUI/src/main/java/labtainers/resultsui/*.java ../MainUI/src/main/java/labtainers/mainui/*.java -d . -Xlint:unchecked || exit
jar cmf mainUI.mf ./MainUI.jar labtainers/mainui/*.class labtainers/goalsui/*.class labtainers/resultsui/*.class ../MainUI/src/main/resources/* || exit
java -classpath /media/sf_SEED/jars/commons-io-2.8.0/commons-io-2.8.0.jar -jar MainUI.jar
#java MainWindow
