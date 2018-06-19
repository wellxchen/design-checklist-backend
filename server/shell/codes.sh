#!/bin/sh

CODE="codes"
TOKEN="$1"
GROUP="$2"
PROJECT="$3"
ROOT="$4"
CACHE="cache"
SHELLDIR="$ROOT/server/shell"

cd $SHELLDIR
./makecachedir.sh $CODE $GROUP $ROOT

cd $ROOT/$CACHE/$CODE/$GROUP

if [ ! -d $PROJECT ]
then
	git clone https://oauth2:$TOKEN@coursework.cs.duke.edu/$GROUP/$PROJECT.git
else 
	cd $PROJECT
	git pull
fi
