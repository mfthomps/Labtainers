#!/bin/bash
#
#  The original /etc/yum.repos.d repo files are in #  /tmp/yum.repos.d
#  If not building from NPS, then restore the repos
#  Otherwise, move the epel repos to the temp.  They were needed to
#  install python-pip.  TBD move that to local mirror.
#
#
if [[ "$APT_SOURCE" != NPS ]]; then
    if [ -d /tmp/yum.repos.d ]; then
        mv /tmp/yum.repos.d/* /etc/yum.repos.d/
        rmdir /tmp/yum.repos.d
    fi
else
    mv /etc/yum.repos.d/epel* /tmp/yum.repos.d/
fi

