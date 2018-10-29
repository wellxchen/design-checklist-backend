#!/bin/sh


LOG="logs"
GROUP="$1"
PROJECT="$2"
ROOT="$3"
CACHE="cache"
SHELLDIR="$ROOT/server/shell"
STATISTICS="statistics"
ISSUES="issues"
QPROFILE="qprofile"
QPROFILEKEY="AV-ylMj9F03llpuaxc9n"
LOGROOT="$ROOT/$CACHE/$LOG"
GENERAL="general"
BYAUTHOER="author"
DUPLICATIONS="duplications"
CODE="code"



cd $SHELLDIR

./makecachedir.sh $LOG $GROUP $ROOT


cd $LOGROOT

if [ ! -d $QPROFILE ]
then
	mkdir $QPROFILE
fi

cd $LOGROOT/$QPROFILE
if [ ! -d $QPROFILEKEY ]
then
	mkdir $QPROFILEKEY
fi


cd $LOGROOT/$GROUP

if [ ! -d $PROJECT ]
then
	mkdir $PROJECT
fi


cd $LOGROOT/$GROUP/$PROJECT

if [ ! -d $STATISTICS ]
then 
	mkdir $STATISTICS
fi


if [ ! -d $ISSUES ]
then 
	mkdir $ISSUES
fi

cd $LOGROOT/$GROUP/$PROJECT/$ISSUES

if [ ! -d $BYAUTHOER ]
then 
	mkdir $BYAUTHOER
fi

if [ ! -d $GENERAL ]
then 
	mkdir $GENERAL
fi

if [ ! -d $DUPLICATIONS ]
then 
	mkdir $DUPLICATIONS
fi

if [ ! -d $CODE ]
then 
	mkdir $CODE
fi


cd $LOGROOT/$GROUP/$PROJECT/$STATISTICS

if [ ! -d $BYAUTHOER ]
then 
	mkdir $BYAUTHOER
fi

if [ ! -d $GENERAL ]
then 
	mkdir $GENERAL
fi
