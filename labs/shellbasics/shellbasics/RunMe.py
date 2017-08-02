#!/usr/bin/env python
import os
print "Your secret value is SECRET_VALUE . Type 'ls' to see the new file we have created!"
os.rename(".local/config/student_manual.txt", "student_manual.txt")
os.rename("student_manual.txt", "readthis.txt")
