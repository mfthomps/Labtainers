#!/bin/bash
labs=$1
function contains() {
    local n=$#
    local value=${!n}
    for ((i=1;i < $#;i++)) {
        if [ "${!i}" == "${value}" ]; then
            echo "y"
            return 0
        fi
    }
    echo "n"
    return 1
}
rootdir=`pwd`
LABPDF=/tmp/labtainer_pdf_$USER
mkdir -p $LABPDF
skip="distrib/skip-labs"
skiplist=""
lines=`cat $skip`
for line in $lines; do
    lab=$(basename $line)
    skiplist+=($lab)
done
llist=$(git ls-files labs | cut -d '/' -f 2 | uniq)
for lab in $llist; do
    if [ $(contains "${skiplist[@]}" $lab) != "y" ]; then
        echo "lab is $lab in dir `pwd`"
        mkdir -p $labs/$lab
        mkdir -p $LABPDF/$lab
        cd $labs/$lab
        if [[ -d docs ]]; then
            echo "lab is $lab"
            cd docs
            cp -p $LABPDF/$lab/*.pdf .
            if [[ -f Makefile ]]; then
                make
            else
                doc=$lab.docx
                if [[ -f $doc ]]; then
                    soffice --convert-to pdf $doc --headless
                fi
            fi
            cp -p *pdf $LABPDF/$lab/
        else
            cp */instructions.txt $LABPDF/$lab/ 2>/dev/null
        fi
        cd $rootdir
    fi
done
