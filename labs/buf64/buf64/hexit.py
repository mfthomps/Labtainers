#!/usr/bin/env python3
#
#  Read a binary file, and output it as a C string
#
import sys
from pathlib import Path
f = sys.argv[1]
data = Path(f).read_bytes() 
stuff = '\\x'+'\\x'.join(format(x, '02x') for x in data)
print(stuff)
