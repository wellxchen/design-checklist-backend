#!/bin/sh

ROOTDIR="student_code"

cd ..

if [ ! -d $ROOTDIR ]
then
	mkdir $ROOTDIR
fi

cd $ROOTDIR

if [ ! -d "$2" ]
then
	mkdir "$2"
fi

cd "$2"

if [ ! -d "$3" ]
then
	git clone https://oauth2:"$1"@coursework.cs.duke.edu/"$2"/"$3".git
else 
	cd "$3"
	git pull
fi

