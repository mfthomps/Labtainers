#!/bin/sh
# -------------------------------------------------------------------------
# Name: collide1.sh
# -------------------------------------------------------------------------
# Description:
#     This script takes as input a file name and a number. The script
#     calculates a hash for the input file. It then tries to find a
#     new file, such that when the new data is hashed, the last input 
#     number of hex digits match the last digits of the original match. The
#     larger the input number, the longer it will take. When (and if) it
#     finds a match, it will display the number of tries it took as well
#     as the data that matches.
#
# Usage:
#     collide1.sh filename numbytes
#
#     Where "numbytes" is a number from 1-to-64 (inclusive), representing
#     whether the hash needs to match on one hex digit or 64 digits (256-bits).
#
# Created: Mar-2013 (P. Clark)
#
# Modifications
# 2014-01-22 (P. Clark)
#     Added some error detection for user input.
# 2014-07-16 (P. Clark)
#     Changed the interface to take a filename and number of bytes to match.
# 2014-09-19 (P. Clark)
#     Fixed a minor bug on the final output.
# -------------------------------------------------------------------------

# Set the number of bytes we get from the urandom device on each call
RAND_BYTES=256

# Verify that the syntax is correct
if [ $# -ne 2 ]
then
    echo "Error: I need two arguments: a filename and a number."
    exit 1
fi

# Verify that the input file exists and is readable
if [ ! -r $1 ]
then
    echo "Error: The input file does not exist."
    exit 1
fi

# Verify that the input is a number greater than 0
if [ $2 -lt 1 ]
then
    echo "Error: the last input must be a number greater than 0."
    exit 1
fi

# Verify that the input number is less than 256
if [ $2 -gt 64 ]
then
    echo "Error: the last input must a number less than or equal to 64"
    exit 1
fi
 
# Assign the value given on the command line
CUT_START=`expr 65 - $2`

# Generate the hash of the input file and only save the hex digits we
# need to match on.
VALUE=`sha256sum $1 | cut -b $CUT_START-64`

# Start a counter to see track how many tries we made
COUNTER=0

# initialize NEW to something not a hex digit
NEW=w

if [ $2 -gt 2 ]
then
    echo The progress will not be shown -- only the final results.
fi


# Keep making new strings and hashing them until truncated hash equals input
while [ $NEW != $VALUE ]
do
    # Get a new string and hash
    NEW=`dd if=/dev/urandom bs=$RAND_BYTES count=1 status=noxfer 2>/dev/null | \
    sha256sum | cut -b $CUT_START-64`

    if [ $2 -lt 3 ]
    then
        # show the truncated hash to the user
        echo $NEW
    fi

    # update the counter
    COUNTER=`expr $COUNTER + 1`
done

if [ $COUNTER -eq 1 ]
then
    echo $COUNTER hash was performed to find a match.
else
    echo $COUNTER hashes were performed before a match was found.
fi
