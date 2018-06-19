#!/bin/sh



WHICHLOG="$1"
ANALYSISID="$2"



cd $WHICHLOG

if [ ! -e $ANALYSISID ]
then
	echo "no"
else
	echo "yes"
fi

