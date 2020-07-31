#!/bin/bash

javac ../MainUI/src/main/java/labtainers/mainui/*.java -d . -Xlint:unchecked

java MainWindow
