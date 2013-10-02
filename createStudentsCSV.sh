#!/bin/bash

filename="github_raw.csv"
output="students_list.csv"
pairsP1="P1Pairs.csv"
pairsP2="P2Pairs.csv"

echo "Timestamp,First Name,Last Name,github userid,Umail address,CSIL userid" >> ${output}

#exclude any line with emails and special symbols, return only unique lines
list=`grep -v "@" | uniq -u`

while read line; do
	echo ${line}

done < ${list}
