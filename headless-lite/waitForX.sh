#!/bin/bash
#
# waitForX [<cmd> [<arg> ...]]
#
# Wait for X Server to be ready, then run the given command once X server
# is ready.  (Or simply return if no command is provided.)
#

function LOG {
    echo $(date -R): $0: $*
}

if [ -z "$DISPLAY" ]; then
    LOG "FATAL: No DISPLAY environment variable set.  No X."
    exit 13
fi

LOG "Waiting for X Server $DISPLAY to be available"

MAX=120 # About 60 seconds
CT=0
while ! xterm -e exit >/dev/null 2>&1; do
    sleep 0.50s
    CT=$(( CT + 1 ))
    if [ "$CT" -ge "$MAX" ]; then
        LOG "FATAL: $0: Gave up waiting for X server $DISPLAY"
        exit 11
    fi
done

LOG "X is available"

if [ -n "$1" ]; then
    exec "$@"
fi

#eof
