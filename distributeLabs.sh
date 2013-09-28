#!/bin/bash

if [ $# -ne 2 ] ; then
	echo "Usage: distributeLabs.sh <Github Username> <Labnum>"
	echo "ex   : ./distributeLabs.sh testaccount P1"
    exit
fi

user="${1}"
lab="${2}"

./getLabSubmissions.py -u ${user} ${lab}

labSubmissionDir=`python -c 'import config; dir = config.getLabSubmissionsDir(); print(dir)'`

#generate file of all repos names
#TODO
cd ${labSubmissionDir};

#zip all bundles
#TODO

#distribute to graders
#TODO
./distributeLabsToGraders.py

