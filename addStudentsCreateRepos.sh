#!/bin/bash

if [ $# -ne 2 ] ; then
	echo "Useage: addStudentsCreateRepos.sh <Github Username> <Labnum>"
	echo "ex    : ./addStudentsCreateRepos.sh testaccount lab01"
    exit
fi

#log the latest repo creation
repoLogs='scriptLogs/'
if [ ! -d "${repoLogs}" ]; then
	mkdir ${repoLogs}
fi

user="${1}"
lab="${2}"

echo "Adding Students to teams."
./addStudentsToTeams.py -u ${user} >> ${repoLogs}/${lab}_AddingStudentsAndTeams
if [ $? -ne 0 ]; then
	echo -e "Did not properly add all students to organization\n"
	exit
fi

echo "Creating Paired teams"
./createPairTeams.py -u ${user} >> ${repoLogs}/${lab}_AddingStudentsAndTeams
if [ $? -ne 0 ]; then
	echo -e "Did not properly create all teams\n"
	exit
fi

echo "Creating individual repos"
./createLabRepo.py -u ${user} ${lab} >> ${repoLogs}/${lab}_CreatingRepos
if [ $? -ne 0 ]; then
    echo -e "Did not create all individual repos\n"
	exit
fi

echo "Creating pair repos"
./createLabRepoForPairs.py -u ${user} ${lab} >> ${repoLogs}/${lab}_CreatingRepos
if [ $? -ne 0 ]; then
	echo -e "Did not create all team repos\n"
	exit
fi

echo "Pushing files to created repos"
./pushFilesToRepo.py -u ${user} ${lab} >> ${repoLogs}/${lab}_PopulateRepos
if [ $? -ne 0 ]; then
    echo -e "Could not push files to all repos\n"
	exit
fi

echo "All operations return okay. Check ${repoLogs} for detailed status on operations"

#cleanup
rm -f *.pyc
