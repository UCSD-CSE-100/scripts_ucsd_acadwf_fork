#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: pullStudents.sh labNum"
    exit 1
fi

submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
tutors=("victor_alor" "victoria_do" "leta_he" "arden_liao" "ryan_liao" "scott_lin" "michael_luo" "dong_nam")

rm -rf ${submissionDir}

declare -i counter
declare -i curr
let counter=0

#Generate grading csv's for the tutors
for tutor in "${tutors[@]}"; do
    echo "Tutor,Student,Pair" > ${submissionsDir}${tutor}.csv
done

#begin reading the students_list.csv
awk 'NR>1' ../students_list.csv > temp_students
pulled="${submissionsDir}students_pulled"
touch ${pulled}

while read line; do
    echo "${line}"
    let curr=counter%8
    currTutor="${tutors[$curr]}"
    githubid=`echo "${line}" | awk -F',' '{print $4}' | tr '[:upper:]' '[:lower:]'`
    isPulled=`grep "${githubid}" ${pulled}`
    if [ -z "${isPulled}" ]; then
        pair=`grep -i "$githubid" ../P1Pairs.csv`
        if [ ! -z "${pair}" ]; then
            githubid_P1=`echo "${pair}" | awk -F',' '{print $1}' | tr '[:upper:]' '[:lower:]'`
            githubid_P2=`echo "${pair}" | awk -F',' '{print $2}' | tr '[:upper:]' '[:lower:]'`
            fName_P1=`grep -i "${githubid_P1}" temp_students | awk -F',' '{print $2}'`
            lName_P1=`grep -i "${githubid_P1}" temp_students | awk -F',' '{print $3}'`
            fName_P2=`grep -i "${githubid_P2}" temp_students | awk -F',' '{print $2}'`
            lName_P2=`grep -i "${githubid_P2}" temp_students | awk -F',' '{print $3}'`
            
            #pull for partner 1 if they worked in it
            repoName="${1}_${githubid_P1}"
            repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
            ./pullRepo.sh "${repoName}" "${repoUrl}" "${currTutor}"
            
            #pull for partner 2 if they worked in it
            repoName="${1}_${githubid_P2}"
            repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
            ./pullRepo.sh "${repoName}" "${repoUrl}" "${currTutor}"
            
            #find what their repo is called
            repoName="${1}_Pair_${githubid_P1}_${githubid_P2}"
            repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
            exists=`git ls-remote ${repoUrl} 2>&1 | grep "ERROR"`
            if [ ! -z "${exists}" ]; then
                repoName="${1}_Pair_${githubid_P2}_${githubid_P1}"
                repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
            fi
            
            ./pullRepo.sh "${repoName}" "${repoUrl}" "${currTutor}"
            if [ $? -eq 0 ]; then
                echo "$currTutor,${fName_P1} ${lName_P1},YES" >> ${submissionsDir}${currTutor}.csv
                echo "$currTutor,${fName_P2} ${lName_P2},YES" >> ${submissionsDir}${currTutor}.csv
                echo "${githubid_P1}" >> ${pulled}
                echo "${githubid_P2}" >> ${pulled}
                let counter=counter+1
            fi
            
        else
            #Pull their repository
            fName=`echo "${line}" | awk -F',' '{print $2}'`
            lName=`echo "${line}" | awk -F',' '{print $3}'`
            repoName="${1}_${githubid}"
            repoUrl="git@github.com:UCSD-CSE-100/${repoName}.git"
            
            ./pullRepo.sh "${repoName}" "${repoUrl}" "${currTutor}"
            if [ $? -eq 0 ]; then
                echo "$currTutor,${fName} ${lName},NO" >> ${submissionsDir}${currTutor}.csv
                let counter=counter+1
                echo "${githubid}" >> ${pulled}
            fi
        fi
    fi
    
done < temp_students

rm -f temp_students

for tutor in "{tutors[@]}"; do
    zip ${tutor}.zip ${tutor}.csv
done

