#!/bin/bash

awk 'NR>1' reregistration_responses.csv > new_pairs

echo -n "Username: "
read username

echo -n "OAuth/Password: "
read -s pwd
echo

echo "Partner1_GithubID,Partner2_GithubID,labnumber" > P2Pairs
rm bad_github_ids

echo "Starting pairing..."
while read line; do
    partner_1=`echo "${line}" | awk -F',' '{print $4}' | tr '[:upper:]' '[:lower:]'`
    partner_2=`echo "${line}" | awk -F',' '{print $7}' | tr '[:upper:]' '[:lower:]'`

    echo "Partner 1 is ${partner_1}, Partner 2 is ${partner_2}"    

    p1_exists=`grep "${partner_1}" P2Pairs`
    p2_exists=`grep "${partner_2}" P2Pairs`
    
    if [ -z "${p1_exists}" ] && [ -z "${p2_exists}" ]; then
        p1_exists=`curl -u ${username}:${pwd} "https://api.github.com/users/${partner_1}" 2>&1 | grep "id"`
        p2_exists=`curl -u ${username}:${pwd} "https://api.github.com/users/${partner_2}" 2>&1 | grep "id"`
        
        if [ ! -z "${p1_exists}" ] && [ ! -z "${p2_exists}" ]; then
            echo "${partner_1},${partner_2},P2" >> P2Pairs;
        else
            echo "${partner_1},${partner_2}" >> bad_github_ids
        fi
    else
        echo "Already exists!"
    fi

done < new_pairs


rm -f new_pairs
