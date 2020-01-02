#!/usr/bin/env python3
'''
This software was created by United States Government employees at 
The Center for Cybersecurity and Cyber Operations (C3O) 
at the Naval Postgraduate School NPS.  Please note that within the 
United States, copyright protection is not available for any works 
created  by United States Government employees, pursuant to Title 17 
United States Code Section 105.   This software is in the public 
domain and is not subject to copyright. 
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.
  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT,
INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
'''

# MyUtil.py
# Description: * Various utilities

import re
import sys

# Strip beginning/ending whitespace from InputTag
# Return True if InputTag consists of alphanumeric, dash or underscore
# Otherwise, return False
def CheckAlphaDashUnder(InputTag):
    InputTagStripped = InputTag.strip()
    if re.match(r'^[a-zA-Z0-9_-]*$', InputTagStripped):
        # Stripped InputTag consists of alphanumeric, dash or underscore
        return True
    else:
        return False
  
def main():
    #print "Testing MyUtil.py"
    t_string = ' This string 123 has spaces in between '
    print('CheckAlphaDashUnder("%s") evaluates to %r' % (t_string, CheckAlphaDashUnder(t_string)))
    t_string = ' This-string-123-does_not-spaces-in-between '
    print('CheckAlphaDashUnder("%s") evaluates to %r' % (t_string, CheckAlphaDashUnder(t_string)))
    t_string = ' This-string-has-&-!-#-special-characters '
    print('CheckAlphaDashUnder("%s") evaluates to %r' % (t_string, CheckAlphaDashUnder(t_string)))

    return 0

if __name__ == '__main__':
    sys.exit(main())

