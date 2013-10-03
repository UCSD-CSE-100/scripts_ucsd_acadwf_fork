#!/bin/bash

if [ $# -ne 3 ] ; then
    echo "Usage: addStudentsCreateRepos.sh <Github Username> <Labnum> <ADD|PAIRS|CREATE|ALL>"
    echo "ex   : ./addStudentsCreateRepos.sh testaccount P1 BOTH"
    exit
fi

#log the latest repo creation
repoLogs=`python -c 'import config; dir = config.getScriptsLogsDir(); print(dir)'`
if [ ! -d "${repoLogs}" ]; then
    mkdir ${repoLogs}
fi

user="${1}"
lab="${2}"

echo -n "Password: "
read -s password
echo

if [ "$3" == "ADD" ] || [ "$3" == "ALL"  ]; then
    echo "Adding Students to teams."
    currTime=`date`
    currLog="${repoLogs}/${lab}_AddingStudentsAndTeams"
    echo -e "Adding students @ ${currTime}" >> ${currLog}
    echo -e "-------------------------" >> ${currLog}
    ./execute.py "addStudentsToTeams.py" "-u ${user}" "${currLog}" "${password}"
    if [ $? -ne 0 ]; then
        echo -e "Did not properly add all students to organization\n"
        exit
    fi
    
fi

if [ "$3" == "PAIRS" ] || [ "$3" == "ALL" ]; then
    echo "Creating Paired teams"
    currTime=`date`
    currLog="${repoLogs}/${lab}_AddingStudentsAndTeams"
    echo >> ${currLog}
    echo -e "\nCreating pair teams @ ${currTime}" >> ${currLog}
    echo -e "-------------------------" >> ${currLog}
    ./execute.py "createPairTeams.py" "-u ${user}" "${currLog}" "${password}"
    if [ $? -ne 0 ]; then
        echo -e "Did not properly create all teams\n"
        exit
    fi
    echo -e "\n\n"  >> ${currLog}

fi

if [ "$3" == "CREATE"  ] || [ "$3" == "ALL"  ]; then
    scratch=`python -c 'import config; print(config.getScratchRepoDir())'`
    rm -rf ${scratch}*

    echo "Creating individual repos"
    currLog="${repoLogs}/${lab}_creatingRepos"
    currTime=`date`
    echo -e "Creating indiv repos @ ${currTime}" >> ${currLog}
    echo -e "-------------------------" >> ${currLog}
    ./execute.py "createLabRepo.py" "-u ${user} ${lab}" "${currLog}" "${password}"
    if [ $? -ne 0 ]; then
        echo -e "Did not create all individual repos\n"
    	exit
    fi
    
    echo "Creating pair repos"
    currTime=`date`
    echo -e "\nCreating pair repos @ ${currTime}" >> ${currLog}
    echo -e "-------------------------" >> ${currLog}
    ./execute.py "createLabRepoForPairs.py" "-u ${user} ${lab}" "${currLog}" "${password}"
    if [ $? -ne 0 ]; then
    	echo -e "Did not create all team repos\n"
    	exit
    fi
	
fi

if [ "$3" == "POPULATE" ] || [ "$3" == "ALL" ]; then
    currLog="${repoLogs}/${lab}_PopulateRepos"
    echo -e "\n\n" >> ${currLog}

    echo "Pushing files to created repos"
    currTime=`date`
    echo -e "Pushing files to repos @ ${currTime}" >> ${currLog}
    echo -e "-------------------------" >> ${currLog}
    ./execute.py "pushFilesToRepo.py" "-u ${user} ${lab}" "${currLog}" "${password}"
    if [ $? -ne 0 ]; then
        echo -e "Could not push files to all repos\n"
        exit
    fi
    
    echo -e "\n\n" >> ${currLog}
fi

echo "All operations return okay. Check ${repoLogs} for detailed status on operations"

#cleanup
rm -f *.pyc
