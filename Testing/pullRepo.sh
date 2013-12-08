#!/bin/bash

pull_files() #PARAMS: $1 = FILES,  $2 = NAME, $3 = TYPE
{
    while read line; do
        if [ ! -f ${line} ]; then
            echo "Could not pull file: $file"
            rm -f ${2}_${3}.tar
            return 1;
        fi
        tar -rvf ../${2}_${3}.tar  ${line}
    done < $1    
    return 0
}

if [ $# -lt 6 ]; then
   echo "Usage: pullRepo.sh repoName repoUrl grader lab_num date time"
   exit 1
fi

protoDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getPrototypeDir())'`
FILES="${protoDir}${4}_files"
if [ ! -f "${FILES}" ]; then
    echo "Files to be pulled cannot be found!"
    exit 1
fi

#initial setup
submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
scratchDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getScratchRepoDir())'`
graderZip="${submissionsDir}${3}.zip"

#clone and begin packaging the repository
cd ${scratchDir}

echo "Repo Url is ${2}, reponame is ${1}"

git clone ${2}
cd ${scratchDir}${1}

if [ $? -ne 0  ]; then
    echo "Could not cd to directory ${scratchDir}${1}"
    exit 1
fi

pwd

#If they have less than a certain number of commits, exit
# commits=`git shortlog | grep -E '^[ ]+\w+' | wc -l`
# if [ "${commits}" -le 3 ]; then
    # echo "Did not work in this repository"
    # echo "Commits was ${commits}"
    # cd ..
    # rm -rf ${scratchDir}* #perform cleanup
    # exit 0
# fi

#Check if checkpoint submission exists, pull latest commit before deadline if it does not
#
if [ $# -eq 8  ]; then
    exits=`git rev-list -n 1 --before="$7 $8" --grep="CHECKPOINT" master`
    if [ -z "${exists}" ]; then
        revision=`git rev-list -n 1 --before="$7 $8" master`
        git checkout ${revision} -b checkpoint
    else
        git checkout ${exists} -b checkpoint
    fi
    if [ ! -z ${revision} ] || [ ! -z ${exists} ]; then
        pull_files ${FILES} ${1} "checkpoint"
    fi
    git checkout master
    git branch -d checkpoint
fi
#check if final submission exists, unless we are ignoring final submission
exists=`git rev-list -n 1 --before="12/6/2013 20:15" --grep="final" -i master`
if [ -z "${exists}" ]; then
    revision=`git rev-list -n 1 --before="12/6/2013 20:15" master`
    git checkout ${revision} -b ontime
else
    ontime_check="TRUE"
    git checkout ${exists} -b ontime
fi
if [ ! -z "${ontime_check}" ] || [ ! -z ${revision} ]; then
    pull_files ${FILES} ${1} "ontime"
fi
git checkout master
git branch -d ontime

#check for late submission day one, always get latest commit
unset revision
lateOne=`git rev-list -n 1 --before="12/7/2013 20:15" --after="12/6/2013 20:15" --grep="final" -i master`
if [ ! -z "${lateOne}" ]; then
    revision=${lateOne}
elif [ -z "${ontime_check}" ]; then
    revision=`git rev-list -n 1 --before="12/7/2013 20:15" --after="12/6/2013 20:15" master`
fi

if [ ! -z "${revision}" ]; then
    git checkout ${revision} -b lateone
    pull_files ${FILE} ${1} lateone
    git checkout master
    git branch -d lateone
fi

#check for late submission day two, always get latest commit
lateTwo=`git rev-list -n 1 --before="12/8/2013 20:15" --after="12/9/2013 20:15" --grep="final" -i master`
if [ ! -z "${lateTwo}" ]; then
    revision=${lateTwo}
elif [ -z "${ontime_check}" ]; then
    revision=`git rev-list -n 1 --before="12/8/2013 20:15" --after="12/9/2013 20:15" master`
fi

if [ ! -z "${revision}" ]; then
    git checkout ${revision} -b latetwo
    pull_files ${FILES} ${1} "latetwo"
    git checkout master
    git branch -d latetwo
fi

cd ..
tar_count=`ls -1 *.tar 2>/dev/null | wc -l`
echo "tar_count is ${tar_count}"
if [ "$tar_count" != 0 ]; then
    tar --ignore-failed-read -czvf ${1}.tar.gz *.tar
    zip ${graderZip} ${1}.tar.gz
    status=$?
fi

#Finished with packaging, check if was success
if [ -z "${status}" ] || [ ${status} -ne 0 ]; then
   echo "Did not successfully add to archive"
   rm -rf ${scratchDir}* #perform cleanup
   exit 1
fi

rm -rf ${scratchDir}* #perform cleanup because of possible quota issues
exit 0
