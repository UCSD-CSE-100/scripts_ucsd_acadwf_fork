#!/bin/bash

# Author: Arden Liao

#initialize PyGithub
git submodule update --init

#create the config file
cp sample_config.py config.py

#intialize the config file values to some default values
#makes the scratch, submission, and logs directories if they don't already exist
PWD=`pwd`
sed -i "s,DIRECTORY,$PWD,g" config.py

SCRATCHREPODIR=`python -c 'import config; dir = config.getScratchRepoDir(); print(dir)'`
SUBMISSIONSDIR=`python -c 'import config; dir = config.getLabSubmissionsDir(); print(dir)'`
SCRIPTSLOGSDIR=`python -c 'import config; dir = config.getScriptsLogsDir(); print(dir)'`

echo "Creating directories..."
if [ ! -d "${SCRATCHREPODIR}" ]; then
	mkdir -p ${SCRATCHREPODIR}
fi

if [ ! -d "${SUBMISSIONSDIR}" ]; then
	mkdir -p ${SUBMISSIONSDIR}
fi

if [ ! -d "${SCRIPTSLOGSDIR}" ]; then
	mkdir -p  ${SCRIPTSLOGSDIR}
fi
