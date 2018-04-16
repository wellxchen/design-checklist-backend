#!/bin/sh


TARGETCACHE="$1"
GROUP="$2"
ROOT="$3"
CACHE="cache"


cd $ROOT

if [ ! -d $CACHE ]
then
	mkdir $CACHE
fi

cd $CACHE

if [ ! -d $TARGETCACHE ]
then
	mkdir $TARGETCACHE
fi

cd $TARGETCACHE

if [ ! -d $GROUP ]
then
	mkdir $GROUP
fi

