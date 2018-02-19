#!/bin/bash
if [[ ! -z "$1" ]] && [[ -f "$1" ]]; then
    ls -l $1
    getcap $1
fi
