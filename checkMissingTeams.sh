#!/bin/bash

echo -n "Oauth token: "
read -s oauth
echo

echo -n "Organization: "
read org

curl -u ${oauth}:x-oauth-basic https://api.github.com/orgs/${org}/teams > teams
curl -u ${oauth}:x-oauth-basic https://api.github.com/teams/512752/members > AllStudents


while read line; do
    id=`echo ${line} | awk -F',' '{print $4}'`
    created=`grep "${id}" teams`
    inAllStudents=`grep "${id} AllStudents"`
    
    if [ -z "${created}" ]; then
        echo "${line}" > notFoundStudents
    fi
    
    if [ -z "${inAllStudents}" ]; then
        echo "Not in All Students: ${id}"
    fi
    
done < students_list.csv

while read line; do
    id=`echo ${line} | awk -F',' '{print $1}'`
    created=`grep "${id}" teams`
    
    if [ -z "${created}" ]; then
        echo "${line}" > notFoundPairs
    fi
done < P1Pairs.csv

rm -f teams
rm -f AllStudents
