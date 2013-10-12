#!/bin/bash

if [ $# -ne 3 ]; then
   echo "Usage: pullRepo.sh repoName repoUrl grader [IGNORE]"
   exit 1
fi

#initial setup
submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
scratchDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getScratchRepoDir())'`
graderTar="${submissionsDir}${3}.tar"

#check if we are currently in a pair
pair=`echo ${1} | grep "Pair"`
if [ -z "${pair}" ]; then
    student=`echo ${1} | awk -F'_' '{print $2}'`
else
    studentOne=`echo ${1} | awk -F'_' '{print $3}'`
    studentTwo=`echo ${1} | awk -F'_' '{print $4}'`
fi

#clone and begin packaging the repository
cd ${scratchDir}
rm -rf *

git clone ${2}
cd ${1}

#check if final submission exists, unless we are ignoring final submission
exists=`git rev-list -n 1 --before="10/11/2013 20:15" --grep="FINAL SUBMISSION" master`
if [ -z "${exists}" ] && [ -z "${4}" ]; then
   echo "No final submission in this repo, excluded from current pass"
   exit 1
else
    if [ ! -z "${exists}" ]; then
       git checkout ${exists} -b ontime
    else
       revision=`git rev-list -n 1 --before="10/11/2013 20:15" master`
       git checkout ${exists} -b ontime
    fi
    tar -cvf ../${1}_ontime.tar BST.hpp BSTNode.hpp BSTIterator.hpp
    git branch -d ontime
fi



#check for late submission day one


#check for late submission day two


#Finished with packaging, check if was success
if [ $? -ne 0 ]; then
   echo "Did not successfully add to archive"
   exit 1
else
   if [ -z "${pair}" ]; then
      echo "${student}" >> students_pulled
   else
      echo "${studentOne}" >> students_pulled
      echo "${studentTwo}" >> students_pulled
   fi
fi

exit 0
