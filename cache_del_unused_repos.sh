#!/bin/bash

echo -n "Username: "
read username

echo -n "OAuth/Password: "
read -s pwd
echo

while read line; do
    echo "Removing REPO ${line}"
    #curl -X DELETE -u ${username}:${pwd} https://api.github.com/repos/UCSD-CSE-100/${line}
done < not_worked

