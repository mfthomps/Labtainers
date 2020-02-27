#!/bin/bash
#
#  The original /etc/apt/srouces.list is in /tmp
#  If not building from NPS, then restore that.
#
#
if [[ "$APT_SOURCE" != NPS ]]; then
    if [ -f /var/tmp/sources.list ]; then
        mv /var/tmp/sources.list /etc/apt/sources.list
    fi
fi

