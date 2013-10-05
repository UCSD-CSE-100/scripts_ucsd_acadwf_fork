#!/bin/bash

#usage ./populateStragglers.sh LABNAME

protodir=`python -c 'import config;print(config.getPrototypeDir())'`
protodir=`echo ${protodir}$1`

scratchDir=`python -c 'import config;print(config.getScratchRepoDir())'`

while read line; do
   repoName=`echo ${line} | awk -F',' '{print $1}'`
   repoUrl=`echo ${line} | awk -F',' '{print $2}'`
   ./populateRepo.sh $repoName $repoUrl $protodir $scratchDir
   echo "RepoName: ${repoName} ${repoUrl} ${protodir} ${scratchDir}"

done < straglers.txt
