#!/bin/sh



DEPENDENCY_ROOT="$1"
GIT_ROOT="$2"

cd $GIT_ROOT

git log --all --numstat --date=short --pretty=format:'--%h--%ad--%aN' --no-renames > logfile.log

mv logfile.log $DEPENDENCY_ROOT

cd $DEPENDENCY_ROOT

java -jar code-maat-1.1-SNAPSHOT-standalone.jar -l logfile.log -c git2 -a summary

