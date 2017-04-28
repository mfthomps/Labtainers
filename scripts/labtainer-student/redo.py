#!/usr/bin/env python

# Filename: redo.py
# Description:
# For lab development testing workflow.  This will stop containers of a lab, create or update lab images
# and start the containers.
#

import sys
import labutils

# Usage: redo.py <labname>
# Arguments:
#    <labname> - the lab to stop, delete and start
def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: redo.py <labname>\n")
        sys.exit(1)
    
    labname = sys.argv[1]
    labutils.RedoLab(labname, "student", False)

    return 0

if __name__ == '__main__':
    sys.exit(main())

