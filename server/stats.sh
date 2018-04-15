#!/bin/sh

./git.sh "$1" "$2" "$3"

cd "$3"
git log  --shortstat  | grep -E "fil(e|es) changed"  -B 5  

#cd ..
#rm -r "$3"

#git log --shortstat --author="rcd" | grep -E "fil(e|es) changed" | awk '{files+=$1; inserted+=$4; deleted+=$6} END {print "files changed: ", files, "lines inserted: ", inserted, "lines deleted: ", deleted }'
#git log  --shortstat --author="Marcin Olichwirowicz" --since="1 Jan, 2013" | grep...