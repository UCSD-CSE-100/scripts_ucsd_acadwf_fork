#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: pullStragglers.sh labNum"
    exit 1
fi

tutors=("victor_alor" "victoria_do" "leta_he" "arden_liao" "ryan_liao" "scott_lin" "michael_luo" "dong_nam")

declare -i counter
declare -i curr
let counter=0

awk 'NR>1' ../students_list.csv > temp
submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
pulled="${submissionsDir}students_pulled"

echo "${pulled}"
while read line; do
    let curr=counter%8
    githubid=`echo ${line} | awk -F',' '{print $4}'`
    isPulled=`grep "${githubid}" ${pulled}`
    if [ -z "${isPulled}" ]; then
        currTutor="${tutors[$curr]}"
        repoName="$1_${githubid}"
        repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
        
        echo "${repoName}, ${repoUrl}, ${currTutor}"
        
        if [ $? -eq 0 ]; then
            let counter=counter+1
        fi
    fi
    
done < temp

rm -f temp
