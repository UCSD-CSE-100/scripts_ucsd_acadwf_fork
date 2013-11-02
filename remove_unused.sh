#!/bin/bash

checkWork()
{
    git clone git@github.com:UCSD-CSE-100/${2}
    cd ${2}
    
    if [ "${1}" == "P1" ]; then
        worked=`diff BST.hpp $PUBLIC/P1/BST.hpp`
    elif [ "${1}" == "P2" ]; then
        worked=`[ -f "BST.hpp" ] && echo "hello"`
    fi
    
    if [ -z "${worked}" ]; then
        echo "${2}" | tee -a ${scratchdir}not_worked
    fi
}

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
    
    checkWork ${1} ${repo}
    
    cd ${scratchdir}; rm -rf ${repo}
    
done < ~/deploy/temp_students

cd ${scratchdir}

# while read line; do
    # gitid1=`echo "${line}" | awk -F',' '{print $1}' | tr '[:upper:]' '[:lower:]'`
    # gitid2=`echo "${line}" | awk -F',' '{print $2}' | tr '[:upper:]' '[:lower:]'`
    
    # repo="${1}_Pair_${gitid1}_${gitid2}"
    # exists=`git ls-remote git@github.com:UCSD-CSE-100/${repo} 2>&1 | grep "ERROR"`
    # if [ ! -z "${exists}" ]; then
        # repo="${1}_Pair_${gitid2}_${gitid1}"
    # fi
    
    # checkWork ${1} ${repo}
    
    # cd ${scratchdir}; rm -rf ${repo}

# done < ~/deploy/temp_pairs

cd ~/deploy
rm -f temp_students temp_pairs
