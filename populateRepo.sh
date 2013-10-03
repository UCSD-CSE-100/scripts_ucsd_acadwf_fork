#!/bin/bash


if [ $# -ne 4 ] ; then
   echo "Usage: populateRepo.sh repoName repoURL protoDir scratchDir" ; 
   echo "Example: populateRepo.sh lab00_Phillip git@github.com:UCSD-CSE-100/lab00_Phillip.git /cs/faculty/pconrad/cs56/lab00_prototype /cs/faculty/pconrad/cs56/scratchRepos" ; exit 0 
fi

export repoName=$1
export repoURL=$2
export protoDir=$3
export scratchDir=$4

printf "Populating repo %s... " $repoName 
 #   " with url " $repoURL  \
 #   " from dir " $protoDir \
 #   " in scratch dir " $scratchDir

mkdir -p $scratchDir; cd $scratchDir

rm -rf *

alreadyPopulated=`grep "${reponame}" ../deploy/alreadyDeployed`

if [ ! -z "${alreadyPopulated}" ]; then
	echo "Already populated!\n"
	exit 0
fi

if [ -d $scratchDir/$repoName ] ; then
   printf " found repo %s ... " $repoName
else
    printf " cloning repo %s... \n" $repoName
    git clone -q $repoURL 
fi

cd $repoName
export cdStatus=$?
if [ $cdStatus -ne 0 ] ; then
    echo "Can't find repo $repoName -- bailing out "; exit 1
fi

git pull origin master

cp -r $protoDir/* .
git add .

#add assignment README url to readme
#can't just use second grep as disambiguation might add
labnum=`echo "${repoName}" | awk -F'_' '{print $1}' | grep -oh "[0-9]"`
url="https://sites.google.com/a/eng.ucsd.edu/cse-100-fall-2013/assignments/assignment-${labnum}-readme"
echo -e "\nAssignment README can be found here: ${url}\n" >> README.md
git add README.md


if [ -f $protoDir/.gitignore ] ; then
   cp $protoDir/.gitignore .
   git add .gitignore
fi
if [ -f $protoDir/.gitmodues ] ; then
   cp $protoDir/.gitmodules .
   git add .gitmodules
fi

git commit -m "Project Files for P${labnum} pushed by populateRepo.sh script"
git push origin master

echo ${repoName} >> alreadyCreated

