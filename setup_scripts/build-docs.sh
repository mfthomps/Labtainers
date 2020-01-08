#!/bin/bash
: <<'END'
This software was created by United States Government employees at 
The Center for the Information Systems Studies and Research (CISR) 
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

END
#
# Build the pdf documents for all labs.
# Intended to be run by developers who use SVN to populate their labs/ directory.
# (PDF documents are not kept in svn, and are typically created when a distribution
# is made)
cd ../labs
llist=$(ls)
for lab in $llist; do
    if [[ -d $lab ]]; then
        cd $lab
        if [[ -d docs ]]; then
            cd docs
            if [[ -f Makefile ]]; then
                make
            else
                doc=$lab.docx
                pdf=$lab.pdf
                if [[ -f $doc ]]; then
                    if [[ ! -f $pdf ]] || [[ "$pdf" -ot "$doc" ]]; then
                        soffice --convert-to pdf $doc --headless
                    else
                        echo $pdf is up to date.
                    fi
                fi
            fi
            cd ../
        fi
        cd ../
    fi
done
cd ../docs/labdesigner
make
cd ../student
make
cd ../instructor
make
