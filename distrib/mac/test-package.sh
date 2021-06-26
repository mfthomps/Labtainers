#!/bin/bash
#open ./labtainers-desktop.pkg
launchctl setenv HEADLESS_PREMASTER TRUE && installer -pkg labtainers-desktop.pkg -target /

