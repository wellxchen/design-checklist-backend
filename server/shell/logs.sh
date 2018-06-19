#!/bin/sh


LOG="logs"
GROUP="$1"
PROJECT="$2"
ROOT="$3"
CACHE="cache"
SHELLDIR="$ROOT/server/shell"
STATISTICS="statistics"
ISSUES="issues"



cd $SHELLDIR

./makecachedir.sh $LOG $GROUP $ROOT



cd $ROOT/$CACHE/$LOG/$GROUP

if [ ! -d $PROJECT ]
then
	mkdir $PROJECT
fi


cd $ROOT/$CACHE/$LOG/$GROUP/$PROJECT

if [ ! -d $STATISTICS ]
then 
	mkdir $STATISTICS
fi


if [ ! -d $ISSUES ]
then 
	mkdir $ISSUES
fi
