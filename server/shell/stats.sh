#!/bin/sh

ROOT="../.."
CODE="codes"
TOKEN="$1"
GROUP="$2"
PROJECT="$3"
CACHE="cache"
SHELLDIR="../shell"

cd $SHELLDIR
./codes.sh $TOKEN $GROUP $PROJECT

cd $ROOT/$CACHE/$CODE/$GROUP/$PROJECT

git log  --shortstat  | grep -E "fil(e|es) changed"  -B 5  

#cd ..
#rm -r "$3"

