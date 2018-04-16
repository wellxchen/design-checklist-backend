#!/bin/sh

ROOT="$3"
LOG="logs"
GROUP="$1"
PROJECT="$2"
CACHE="cache"
SHELLDIR="$ROOT/server/shell"

cd $SHELLDIR
./makedir.sh $LOG $GROUP $ROOT

cd $ROOT/$CACHE/$LOG/$GROUP

if [ ! -d $PROJECT ]
then
	mkdir $PROJECT
fi
