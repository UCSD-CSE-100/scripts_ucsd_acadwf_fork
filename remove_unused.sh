#!/bin/bash

awk 'NR>1' ../students_list.csv > temp_students

scratchdir=`python -c 'import config; print(config.getScratchRepoDir())'`

while read line; do

done < temp_students

rm -f temp_students
