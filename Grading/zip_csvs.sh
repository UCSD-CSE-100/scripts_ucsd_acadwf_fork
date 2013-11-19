#!/bin/bash

submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
tutors=("victor_alor" "victoria_do" "leta_he" "arden_liao" "ryan_liao" "scott_lin" "michael_luo" "dong_nam")

for tutor in "${tutors[@]}"; do
    zip ${submissionsDir}${tutor}.zip ${submissionsDir}${tutor}.csv
done