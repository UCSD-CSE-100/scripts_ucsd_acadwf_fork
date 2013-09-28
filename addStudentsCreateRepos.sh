#!/bin/bash

if [ $# -ne 2 ] ; then
	echo "Useage: addStudentsCreateRepos.sh <Github Username> <Labnum>"
	echo "ex    : ./addStudentsCreateRepos.sh testaccount lab01"
fi

#log the latest repo creation
repoLogs='scriptLogs/'
if [ ! -d "${repoLogs}" ]; then
	mkdir ${repoLogs}
fi

user="${1}"
lab="${2}"

./addStudentsToTeams.py -u ${user} >> ${repoLogs}/${lab}_AddingStudentsAndTeams
./createPairTeams.py -u ${user} >> ${repoLogs}/${lab}_AddingStudentsAndTeams
./createLabRepo.py -u ${user} ${lab} >> ${repoLogs}/${lab}_CreatingRepos
./createLabRepoForPairs.py -u ${user} ${lab} >> ${repoLogs}/${lab}_CreatingRepos
./pushFilesToRepo.py -u ${user} ${lab} >> ${repoLogs}/${lab}_PopulateRepos

echo "Check ${repoLogs} for status on operations"