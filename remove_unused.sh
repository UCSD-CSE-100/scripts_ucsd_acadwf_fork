#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Args P1 or P2"
    exit 0
fi

awk 'NR>1' ../students_list.csv > temp_students

scratchdir=`python -c 'import config; print(config.getScratchRepoDir())'`

while read line; do
    gitid=`echo ${line} | awk -F',' '{print $4}'`
    repo="${1}_gitid"
    git clone git@github.com:UCSD-CSE-100/${repo}
    cd ${repo}
    
    worked=`diff BST.hpp $PUBLIC/P1/BST.hpp`
    if [ ! -z "${worked}" ]; then
        echo "${repo}" | tee -a not_worked
    fi
done < temp_students

rm -f temp_students
