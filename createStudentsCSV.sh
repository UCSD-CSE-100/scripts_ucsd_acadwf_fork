#!/bin/bash

filename="github_raw.csv"
output="students_list.csv"
pairsP1="P1Pairs.csv"
pairsP2="P2Pairs.csv"

#exclude any line with emails and special symbols, return only unique lines

if [ "$1" == "students" ]; then

echo "Disambiguating students.."

echo "Timestamp,First Name,Last Name,github userid,Umail address,CSIL userid" > ${output}
cut -d, -f2- ${filename} | grep -v "@" | sort -u -t, -k3  > temp.csv
while read line; do
    TS="10/2/2013 12:00:00"
    FN=`echo ${line} | awk -F',' '{print $1}'`
    LN=`echo ${line} | awk -F',' '{print $2}'`
    GID=`echo ${line} | awk -F',' '{print $4}'`
    PID=`echo ${line} | awk -F',' '{print $3}'`

    echo "${TS},${FN},${LN},${GID},@,${PID}" >> ${output}
done < temp.csv
fi


#exclude any line without a pair (probably no as efficient...)
if [ "$1" == "pairs" ]; then

echo "Creating pairs..."

echo "Partner1_GithubID,Partner2_GithubID,labnumber" > ${pairsP1}
echo "Partner1_GithubID,Partner2_GithubID,labnumber" > ${pairsP2}

cut -d, -f2- ${filename} | grep -v "@" | grep -v ",,," | sort -u -t, -k3 |  tr '[:upper:]' '[:lower:]' > temp.csv
while read line; do
    #FN=`echo ${line} | awk -F',' '{print $5}'`
    #LN=`echo ${line} | awk -F',' '{print $6}'`
    Sec_PID=`echo ${line} | awk -F',' '{print $7}'`
    Fir_GID=`echo ${line} | awk -F',' '{print $4}'`

    searchstr="${Sec_PID},"
    Partner=`grep "${searchstr}" temp.csv`
    echo "Searchstr is \"${searchstr}\""
    echo "Partner is ${Partner}"
    Sec_GID=`echo ${Partner} | awk -F',' '{print $4}'`

    echo "${Fir_GID},${Sec_GID},P1" >> ${pairsP1}
    echo "${Fir_GID},${Sec_GID},P2" >> ${pairsP2}
done < temp.csv
fi

rm -f temp.csv
