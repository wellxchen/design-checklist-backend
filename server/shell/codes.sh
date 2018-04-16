#!/bin/sh

ROOT="../.."
CODE="codes"
TOKEN="$1"
GROUP="$2"
PROJECT="$3"
CACHE="cache"
SHELLDIR="../shell"

cd $SHELLDIR
./makedir.sh $CODE $2

cd $ROOT/$CACHE/$CODE/$GROUP

if [ ! -d $PROJECT ]
then
	git clone https://oauth2:$TOKEN@coursework.cs.duke.edu/$GROUP/$PROJECT.git
else 
	cd $PROJECT
	git pull
fi
