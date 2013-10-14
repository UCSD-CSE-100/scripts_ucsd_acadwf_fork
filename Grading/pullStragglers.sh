#!/bin/bash

tutors=("victor_alor" "victoria_do" "leta_he" "arden_liao" "ryan_liao" "scott_lin" "michael_luo" "dong_nam")

declare -i counter
declare -i curr
let counter=0

awk 'NR>1' ../students_list.csv > temp

while read line; do
    let curr=counter%8
    echo "$line"
    echo "${tutors[$curr]}"
    if [ $? -eq 0 ]; then
        let counter=counter+1
    fi
done < temp

rm -f temp
