#!/bin/bash
#
#  The original /etc/yum.repos.d repo files are in #  /tmp/yum.repos.d
#  If not building from NPS, then restore the repos
#  Otherwise, move the epel repos to the temp.  They were needed to
#  install python-pip.  TBD move that to local mirror.
#
#
if [[ "$APT_SOURCE" != NPS ]]; then
    if [ -d /var/tmp/yum.repos.d ]; then
        mv /var/tmp/yum.repos.d/* /etc/yum.repos.d/
        rmdir /var/tmp/yum.repos.d
    fi
else
    mkdir -p /var/tmp/yum.repos.d
    mv /etc/yum.repos.d/epel* /var/tmp/yum.repos.d/
fi

