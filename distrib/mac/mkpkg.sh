#!/bin/bash
#
#  Create a Mac pkg installation file for headless labtainers
#  Only a pre and post install script are included.
#  The pre checks for Docker, the post pulls headless-labtainers.sh,
#  creates the directory and starts a terminal running headless.
#
pkgbuild --identifier labtainers-desktop.pkg --nopayload --scripts ./scripts labtainers-desktop.pkg
