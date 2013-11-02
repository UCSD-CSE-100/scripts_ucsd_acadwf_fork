#!/bin/bash

tutors=("victor_alor" "victoria_do" "leta_he" "arden_liao" "ryan_liao" "scott_lin" "michael_luo" "dong_nam")

bundle_dir="../../labSubmissions"

for tutor in "${tutors[@]}"; do
    unzip -l ${bundle_dir}/${tutor}.zip | egrep "*.tar.gz" | awk '{print $4}' > temp
    echo "Tutor,Student,GithubID,PID,Pair,Ontime,Late_One,Late_Two,Comments" > ${bundle_dir}/${tutor}.csv
    echo "${tutor}"
    echo "---------------------------------------------"
    while read student; do
        student1=`echo "${student}" | tr '.' '_' | awk -F'_' '{print $2}'`
        if [[ "${student1}" = "Pair" ]]; then
            student1=`echo "${student}" | tr '.' '_' | awk -F'_' '{print $3}'`
            entry1=`grep -i "${student1}" ../students_list.csv`
            pid1=`echo "${entry1}" | awk -F',' '{print $6}'`
            fName1=`echo "${entry1}" | awk -F',' '{print $2}'`
            lName1=`echo "${entry1}" | awk -F',' '{print $3}'`
            echo "${tutor},${fName1} ${lName1},${student1},${pid1},YES,,,," >> ${bundle_dir}/${tutor}.csv
            
            student2=`echo "${student}" | tr '.' '_' | awk -F'_' '{print $4}'`
            entry2=`grep -i "${student2}" ../students_list.csv`
            pid2=`echo "${entry2}" | awk -F',' '{print $6}'`
            fName2=`echo "${entry2}" | awk -F',' '{print $2}'`
            lName2=`echo "${entry2}" | awk -F',' '{print $3}'`
            echo "${tutor},${fName2} ${lName2},${student2},${pid2},YES,,,," >> ${bundle_dir}/${tutor}.csv
            
        else
            entry1=`grep -i "${student1}" ../students_list.csv`
            pid1=`echo "${entry1}" | awk -F',' '{print $6}'`
            fName1=`echo "${entry1}" | awk -F',' '{print $2}'`
            lName1=`echo "${entry1}" | awk -F',' '{print $3}'`
            echo "${tutor},${fName1} ${lName1},${student1},${pid1},NO,,,," >> ${bundle_dir}/${tutor}.csv
        fi
    done < temp
    zip ${bundle_dir}/${tutor}.zip ${bundle_dir}/${tutor}.csv
    echo "---------------------------------------------"
    rm -f temp
done
