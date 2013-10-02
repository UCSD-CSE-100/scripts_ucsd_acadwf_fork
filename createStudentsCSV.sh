#!/bin/bash

filename="github_raw.csv"
output="students_list.csv"
pairsP1="P1Pairs.csv"
pairsP2="P2Pairs.csv"

echo "Timestamp,First Name,Last Name,github userid,Umail address,CSIL userid" > ${output}

#exclude any line with emails and special symbols, return only unique lines
cut -d, -f2- ${filename} | sort -u -t, -k3 | grep -v "@" > temp.csv
while read line; do
    TS="10/2/2013 12:00:00"
    FN=`echo ${line} | awk -F',' '{print $1}'`
    LN=`echo ${line} | awk -F',' '{print $2}'`
    GID=`echo ${line} | awk -F',' '{print $4}'`
    PID=`echo ${line} | awk -F',' '{print $3}'`

    echo "${TS},${FN},${LN},${GID},@,${PID}" >> ${output}
done < temp.csv


#exclude any line without a pair (probably no as efficient...)
grep -v ",,," ${filename}  | sort -u -t, -k4 > temp.csv
#while read line; do
#    echo -n
#done < temp.csv

rm temp.csv
