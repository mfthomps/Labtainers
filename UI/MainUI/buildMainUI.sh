#!/bin/bash
#1.4

export ANT_HOME=/PDFdata/library/apache_ant/

export PATH=$ANT_HOME/bin:$PATH

ant -buildfile buildMainUI.xml main
if [ $? -eq 1]; then
        echo "Failed on Build"
        exit 1
fi
