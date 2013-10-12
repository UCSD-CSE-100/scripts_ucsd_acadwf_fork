#!/bin/bash

if [ $# -ne 3 ]; then
   echo "Usage: pullRepo.sh repoName repoUrl grader"
   exit 1
fi

submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
graderTar="${submissionsDir}${3}.tar"

scratchDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getScratchRepoDir())'`

pair=`echo ${1} | grep "Pair"`

if [ -z "${pair}" ]; then
    student=``
else
    studentOne=``
    studentTwo=``
fi

if [ $? -ne 0 ]; then
   echo "Did not successfully add to archive"
   exit 1
else
   if [ -z "${pair}" ]; then
      echo "${student}" >> pulled
   else
      echo "${studentOne}" >> pulled
      echo "${studentTwo}" >> pulled 
   fi
fi

exit 0
