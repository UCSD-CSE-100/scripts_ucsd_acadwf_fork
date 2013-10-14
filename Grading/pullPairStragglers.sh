#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: pullPairStragglers.sh labNum"
    exit 1
fi

tutors=("victor_alor" "victoria_do" "leta_he" "arden_liao" "ryan_liao" "scott_lin" "michael_luo" "dong_nam")

declare -i counter
declare -i curr
let counter=0

awk 'NR>1' ../P1Pairs.csv > temp
submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
pulled="${submissionsDir}students_pulled"

while read line; do
    student1=`echo ${line} | awk -F',' '{print $1}'`
    student2=`echo ${line} | awk -F',' '{print $2}'`
    isPulled1=`grep "${student1}" ${pulled}`
    isPulled2=`grep "${student2}" ${pulled}`
    
    if [ -z "${isPulled1}" ] && [ -z "${isPulled2}" ]; then
        repoName="P1_Pair_${student1}_${student2}"
        repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
        #check if reponame exists
        git ls-remote ${repoUrl} > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            currTutor="${tutors[$curr]}"
            ./pullRepo.sh ${repoName} ${repoUrl} ${currTutor} "IGNORE"
            fi
        else
            repoName="P1_Pair_${student2}_${student1}"
            repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
            git ls-remote ${repoUrl} > /dev/null 2>&1
            if [ $? -eq 0 ]; then
                currTutor="${tutors[$curr]}"
                ./pullRepo.sh ${repoName} ${repoUrl} ${currTutor} "IGNORE"
            else
                echo "Pair does not have a repository!" >> pullPairsLog
            fi
        fi
    fi

done < temp

rm -f temp
