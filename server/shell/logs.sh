#!/bin/sh

ROOT="../.."
LOG="logs"
GROUP="$1"
PROJECT="$2"
CACHE="cache"
SHELLDIR="../shell"

cd $SHELLDIR
./makedir.sh $LOG $1

cd $ROOT/$CACHE/$LOG/$GROUP

if [ ! -d $PROJECT ]
then
	mkdir $PROJECT
fi
