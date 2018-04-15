#!/bin/sh

ROOTDIR="student_code"
TOKEN="$1"
GROUP="$2"
PROJECT="$3"

cd ..

if [ ! -d $ROOTDIR ]
then
	mkdir $ROOTDIR
fi

cd $ROOTDIR

if [ ! -d $GROUP ]
then
	mkdir $GROUP
fi

cd $GROUP

if [ ! -d $PROJECT ]
then
	git clone https://oauth2:$TOKEN@coursework.cs.duke.edu/$GROUP/$PROJECT.git
else 
	cd $PROJECT
	git pull
fi

