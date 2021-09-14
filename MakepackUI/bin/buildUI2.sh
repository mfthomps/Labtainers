#!/bin/bash
#
# Rebuild the Labtianers Lab Editor UI
# Use -n to supress running the UI after rebuild.
#/src/main/java/newpackage
javac -classpath json-simple-1.1.1.jar ../src/main/java/newpackage/NewJFrame.java -d . -Xlint:unchecked || exit
jar cmf makepackui.mf ./makepackui.jar newpackage/*.class ../src/main/resources/* || exit
java -jar makepackui.jar & 
