#!/bin/bash
#
# uses args $1 $2 $3
# usage:-$ sed-cleaning.sh inputfile temporaryfile outputfile

# Get rid of unicode crap
cat $1 | tr "\r\n" " " > $2 # All hail http://www.unix.com/41858-post5.html


# run this with sed -nf sed-cleaning file.txt

sed -e 's/Mr\. /Mr /g
s/Mrs\. /Mrs /g
s/- - -\n//g
s/----------------------------------------------------------\n//g
s/----------------------------------------\n//g
s/-----\n//g
s/--\n//g
s/~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-\n//g
s/#\n//g
s/\///g
s/> \n//g
s/\x0A/\n/g
s/\n\n/\n/g
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
s/Mrs /Mrs\. /g
s/Mrs\.\. /Mrs\. /g
s/Mr /Mr\. /g
s/Mr\.\. /Mr\. /g' <$2 >$3 

