#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: pullStragglers.sh labNum"
    exit 1
fi

submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
tutors=("victor_alor" "victoria_do" "leta_he" "arden_liao" "ryan_liao" "scott_lin" "michael_luo" "dong_nam")

declare -i counter
declare -i curr
let counter=0

#Generate grading csv's for the tutors
for tutor in "${tutors[@]}"
do
    echo "Tutor,Student,Pair,Ontime,Late_One,Late_Two,Comments" > ${submissionsDir}${tutor}.csv
done