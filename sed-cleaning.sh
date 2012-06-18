#!/bin/bash
#
# uses args $1 $2 $3
# usage:-$ sed-cleaning.sh inputfile temporaryfile outputfile
# file read/write is 1->3->2->3

# Get rid of unicode crap
cat $1 | tr "\r\n" "\n" | tr -s "\n\n" "\n" | tr -s "  " " " > $3 # All hail http://www.unix.com/41858-post5.html

sort -u $3 -o $2

# run this with sed -nf sed-cleaning file.txt

sed -e 's/Mr\. /Mr /g
s/Mrs\. /Mrs /g
s/Dr\. /Dr /g
s/- - -\n//g
s/----------------------------------------------------------\n//g
s/----------------------------------------\n//g
s/-----\n//g
s/--\n//g
s/~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\n//g
s/#\n//g
s/\///g
s/> \n//g
s/\x0A//g
s/\x02//g
s/\x03//g
s/\n\n/\n/g
s/\n \n/\n/g
s/\.\n/\. /g
s/\n/ /g
s/\n /\n/g
s/\n  /\n/g
s/\n   /\n/g
s/\n    /\n/g
s/\.  /\. /g
s/\. \. \./\.\.\./g
s/ \./\./g
s/"//g
s/\. /\.\n/g
s/_//g
s/Dr /Dr\. /g
s/Mrs /Mrs\. /g
s/Mrs\.\. /Mrs\. /g
s/Mr /Mr\. /g
s/Mr\.\. /Mr\. /g' <$2 >$3


