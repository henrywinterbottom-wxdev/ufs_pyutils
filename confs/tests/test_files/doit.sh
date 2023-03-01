#!/bin/sh -f

filenames=`ls *.check *.template *.yaml`

for filename in $filenames; do

    cat $filename | tr -d "\r" > tmp.file
    mv tmp.file $filename

done
