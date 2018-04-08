#!/bin/sh
cd ../codes/"$2"
git clone https://oauth2:"$1"@coursework.cs.duke.edu/"$2"/"$3".git
cd "$3"
git log --shortstat --author="Andrew Yeung" | grep -E "fil(e|es) changed" | awk '{files+=$1; inserted+=$4; deleted+=$6} END {print "files changed: ", files, "lines inserted: ", inserted, "lines deleted: ", deleted }'
#git log  --shortstat --author="Marcin Olichwirowicz" --since="1 Jan, 2013" | grep...