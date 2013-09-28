#!/bin/bash

if [ $# -ne 2 ] ; then
	echo "Usage: addStudentsCreateRepos.sh <Github Username> <Labnum>"
	echo "ex   : ./addStudentsCreateRepos.sh testaccount P1"
    exit
fi

#log the latest repo creation
repoLogs=`python -c 'import config; dir = config.getScriptsLogsDir(); print(dir)'`
if [ ! -d "${repoLogs}" ]; then
	mkdir ${repoLogs}
fi

user="${1}"
lab="${2}"

echo "Adding Students to teams."
currTime=`date`
echo -e "Adding students @ ${date}" >> ${repoLogs}/${lab}_AddingStudentsAndTeams
echo -e "-------------------------" >> ${repoLogs}/${lab}_AddingStudentsAndTeams
./addStudentsToTeams.py -u ${user} >> ${repoLogs}/${lab}_AddingStudentsAndTeams
if [ $? -ne 0 ]; then
	echo -e "Did not properly add all students to organization\n"
	exit
fi

echo "Creating Paired teams"
currTime=`date`
echo -e "\nCreating pair teams @ ${date}" >> ${repoLogs}/${lab}_AddingStudentsAndTeams
echo -e "-------------------------" >> ${repoLogs}/${lab}_AddingStudentsAndTeams
./createPairTeams.py -u ${user} >> ${repoLogs}/${lab}_AddingStudentsAndTeams
if [ $? -ne 0 ]; then
	echo -e "Did not properly create all teams\n"
	exit
fi

echo "Creating individual repos"
currTime=`date`
echo -e "Creating indiv repos @ ${date}" >> ${repoLogs}/${lab}_CreatingRepos
echo -e "-------------------------" >> ${repoLogs}/${lab}_CreatingRepos
./createLabRepo.py -u ${user} ${lab} >> ${repoLogs}/${lab}_CreatingRepos
if [ $? -ne 0 ]; then
    echo -e "Did not create all individual repos\n"
	exit
fi

echo "Creating pair repos"
currTime=`date`
echo -e "\nCreating pair repos @ ${date}" >> ${repoLogs}/${lab}_CreatingRepos
echo -e "-------------------------" >> ${repoLogs}/${lab}_CreatingRepos
./createLabRepoForPairs.py -u ${user} ${lab} >> ${repoLogs}/${lab}_CreatingRepos
if [ $? -ne 0 ]; then
	echo -e "Did not create all team repos\n"
	exit
fi

echo "Pushing files to created repos"
currTime=`date`
echo -e "Pushing files to repos @ ${date}" >> ${repoLogs}/${lab}_PopulateRepos
echo -e "-------------------------" >> ${repoLogs}/${lab}_PopulateRepos
./pushFilesToRepo.py -u ${user} ${lab} >> ${repoLogs}/${lab}_PopulateRepos
if [ $? -ne 0 ]; then
    echo -e "Could not push files to all repos\n"
	exit
fi

echo "All operations return okay. Check ${repoLogs} for detailed status on operations"

#cleanup
rm -f *.pyc
