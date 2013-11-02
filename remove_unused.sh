#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Args P1 or P2"
    exit 0
fi

awk 'NR>1' students_list.csv > temp_students
awk 'NR>1' "${1}Pairs.csv" > temp_pairs

scratchdir=`python -c 'import config; print(config.getScratchRepoDir())'`
cd ${scratchdir}

while read line; do
    gitid=`echo ${line} | awk -F',' '{print $4}' | tr '[:upper:]' '[:lower:]' `
    repo="${1}_${gitid}"
    git clone git@github.com:UCSD-CSE-100/${repo}
    cd ${repo}
    
    worked=`diff BST.hpp $PUBLIC/P1/BST.hpp`
    if [ -z "${worked}" ]; then
        echo "${repo}" | tee -a ${scratchdir}not_worked
    fi

    cd ${scratchdir}; rm -rf ${repo}
done < ~/deploy/temp_students

while read line; do

done < ~/deploy/temp_pairs

cd ~/deploy
rm -f temp_students temp_pairs
