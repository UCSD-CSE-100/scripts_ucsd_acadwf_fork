#!/bin/bash

#usage ./populateStragglers.sh LABNAME

protodir=`python -c 'import config;print(config.getPrototypeDir())'`
protodir=`echo ${protodir}$1`

scratchDir=`python -c 'import config;print(config.getScratchRepoDir())'`

while read line; do
echo "${line}"

done < straglers.txt