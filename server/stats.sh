#!/bin/sh

ROOTDIR="student_code"
TOKEN="$1"
GROUP="$2"
PROJECT="$3"

./git.sh $TOKEN $GROUP $PROJECT

cd ../$ROOTDIR/$GROUP/$PROJECT

git log  --shortstat  | grep -E "fil(e|es) changed"  -B 5  

#cd ..
#rm -r "$3"

