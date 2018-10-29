#!/bin/sh

CODE="codes"
TOKEN="$1"
GROUP="$2"
PROJECT="$3"
ROOT="$4"
CACHE="cache"
SHELLDIR="$ROOT/server/shell"

cd $SHELLDIR
./codes.sh $TOKEN $GROUP $PROJECT $ROOT

cd $ROOT/$CACHE/$CODE/$GROUP/$PROJECT

echo "meaningless catch: " `grep -R "printStackTrace" --include=*.java .`
echo "abstract:\t" `grep -R "abstract " --include=*.java . | grep "class " | grep "{" | wc -l`
echo "subclasses:\t" `grep -R " extends " --include=*.java . | wc -l`
echo "interfaces:\t" `grep -R "interface " --include=*.java . | grep "{" | wc -l`
echo "interfaces Used:" `grep -R " implements " --include=*.java . | wc -l`