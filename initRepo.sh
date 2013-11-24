#!/bin/bash

#initialize PyGithub, unsure why submodule doesn't work, manually clone for now
git clone git@github.com:jacquev6/PyGithub.git

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
	mkdir ${SCRATCHREPODIR}
fi

if [ ! -d "${SUBMISSIONSDIR}" ]; then
	mkdir ${SUBMISSIONSDIR}
fi

if [ ! -d "${SCRIPTSLOGSDIR}" ]; then
	mkdir ${SCRIPTSLOGSDIR}
fi
