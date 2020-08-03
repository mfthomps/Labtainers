#!/bin/bash

javac ../MainUI/src/main/java/labtainers/mainui/*.java -d . -Xlint:unchecked || exit
jar cmf mainUI.mf ./MainUI.jar labtainers/mainui/*.class  || exit
java -jar MainUI.jar
#java MainWindow
