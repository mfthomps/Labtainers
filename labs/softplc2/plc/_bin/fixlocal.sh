#!/bin/bash
#
#  Script will be run after parameterization has completed, e.g., 
#  use this to compile source code that has been parameterized.
#
sudo systemctl enable openplc
cp /var/tmp/mbconfig.cfg $HOME/OpenPLC_v3/webserver
cp /var/tmp/openplc.db $HOME/OpenPLC_v3/webserver
sudo systemctl restart openplc
