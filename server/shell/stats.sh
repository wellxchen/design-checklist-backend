#!/bin/sh


CODE="codes"
TOKEN="$1"
GROUP="$2"
PROJECT="$3"
ROOT="$4"
CACHE="cache"
SHELLDIR="$ROOT/server/shell"

cd $SHELLDIR
./codes.sh $TOKEN $GROUP $PROJECT $ROOT

cd $ROOT/$CACHE/$CODE/$GROUP/$PROJECT

git log  --shortstat  | grep -E "fil(e|es) changed"  -B 5  



