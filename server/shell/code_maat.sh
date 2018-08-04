#!/bin/sh



DEPENDENCY_ROOT="$1"
CODE="$2"
LOGS="$3"
GROUP="$4"
PROJECT="$5"
ROOT="$6"
CODEPATH=$CODE/$GROUP/$PROJECT
LOGPATH=$LOGS/$GROUP/$PROJECT

cd $CODEPATH

git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > $LOGPATH/code_maat.log


cd $DEPENDENCY_ROOT

java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l $LOGPATH/code_maat.log -c git2 -a summary

