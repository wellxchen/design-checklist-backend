#!/bin/sh

TOKEN="$1"
GROUP="$2"
PROJECT="$3"
ROOT="$4"
FILE="$5"
START="$6"
END="$7"
CACHE="cache"
CODE="codes"
SHELLDIR="$ROOT/server/shell"

cd $SHELLDIR
./codes.sh $TOKEN $GROUP $PROJECT $ROOT

cd $ROOT/$CACHE/$CODE/$GROUP/$PROJECT

git blame -L $START,$END $FILE