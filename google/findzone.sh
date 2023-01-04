#!/bin/bash
result=$(cat set_defaults.sh | grep -v "#" | awk -F"=" '{print($3)}')
echo $result | awk '{$1=$1};NF'
