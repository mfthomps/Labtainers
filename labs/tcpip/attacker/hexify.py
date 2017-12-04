#!/usr/bin/env python
import sys
if len(sys.argv) != 2:
    print('./hexify.py "the string"')
    exit(0)
s = sys.argv[1]
print('The hex encoding of  %s is:\n%s' % (s, s.encode("hex")))
print('Do not forget to add a "0d00" if a newline and null termination is needed')
