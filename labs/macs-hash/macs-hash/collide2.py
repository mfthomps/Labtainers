#!/usr/bin/python
# ---------------------------------------------------------------------------
# Filename: collide2.py
# ---------------------------------------------------------------------------
# Description: This Python script generates random messages, hashes them
#     with SHA256 and then truncates the hash to the last byte. These hashes
#     are then saved. With each truncated hash it looks to see if it has
#     been seen before. When it finds a match it stops and displays how
#     many tries it took to find a match.
#
# Created: 2013-03-22 (P. Clark)
#
# Modifications:
#
# 2014-07-17 (P. Clark)
#     Changed the output of the matching text so it is readable hex.
# ---------------------------------------------------------------------------


import sys
import hashlib

# initialize
count = 0
fd = open("/dev/urandom")
hashtable = {}

done = False
while not done:
    msg = fd.read(4)

    digest = hashlib.sha256(msg).hexdigest()
    digest = digest[62:]
    print "message " + str(count) + " hashes to " + digest

    if digest in hashtable:
        print "found after " + str(count) + " tries:"
	output = " ".join(hex(ord(n)) for n in msg) + " = " 
	output = output + " ".join(hex(ord(n)) for n in hashtable[digest]) 
	print output
             
        done = True
    else:
        hashtable[digest] = msg
 
    count += 1

fd.close()
