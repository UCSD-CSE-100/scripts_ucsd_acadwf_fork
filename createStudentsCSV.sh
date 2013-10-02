#!/bin/bash

filename="github_raw.csv"
output="students_list.csv"
pairsP1="P1Pairs.csv"
pairsP2="P2Pairs.csv"

echo "Timestamp,First Name,Last Name,github userid,Umail address,CSIL userid" >> ${output}

#exclude any line with emails and special symbols, return only unique lines
grep -v "@" ${filename}  | uniq -u > temp.csv
while read line; do
    TS=`echo ${line} | awk -F',' '{print $1}'`
    FN=`echo ${line} | awk -F',' '{print $2}'`
    LN=`echo ${line} | awk -F',' '{print $3}'`
    GID=`echo ${line} | awk -F',' '{print $4}'`
    PID=`echo ${line} | awk -F',' '{print $5}'`

    echo "${TS},${FN},${LN},${GID},@,${PID}" >> ${output}
done < temp.csv


#exclude any line without a pair (probably no as efficient...)
grep -v ",,," ${filename}  | uniq -u > temp.csv
#while read line; do
#    echo -n
#done < temp.csv

rm temp.csv
