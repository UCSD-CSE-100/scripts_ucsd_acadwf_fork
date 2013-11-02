#!/bin/bash

if [ $# -ne 1 ]; then
    echo "Usage: cache_del_unused_repos.sh CACHE|DEL"
    exit 0
fi

if [ "$1" == "CACHE" ]; then
    scratchdir=`python -c 'import config; print(config.getScratchRepoDir())'`
    homedir=`pwd`
    
    cd ${scratchdir}
    while read line; do
        bundle=`echo ${line} | awk -F'_' '{print $1}'`
        git clone git@github.com:UCSD-CSE-100/${repo}
        cd ${line}
        
        git bundle create ${line}.bundle master
        zip ${scratchdir}${bundle}_cache.zip ${line}.bundle
        
        cd ${scratchdir}; rm -rf ${line}
    done < ${homedir}/not_worked

elif [ "$1" == "DEL" ]; then
    echo -n "Username: "
    read username

    echo -n "OAuth/Password: "
    read -s pwd
    echo

    while read line; do
        echo "Removing REPO ${line}"
        #curl -X DELETE -u ${username}:${pwd} https://api.github.com/repos/UCSD-CSE-100/${line}
    done < not_worked

fi


