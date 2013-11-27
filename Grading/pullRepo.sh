#!/bin/bash

if [ $# -lt 3 ]; then
   echo "Usage: pullRepo.sh repoName repoUrl grader"
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
exits=`git rev-list -n 1 --before="11/13/2013 20:45" --grep="CHECKPOINT" master`
if [ -z "${exists}" ]; then
   revision=`git rev-list -n 1 --before="11/13/2013 20:45" master`
   git checkout ${revision} -b checkpoint
else
   git checkout ${exists} -b checkpoint
fi
if [ -f "compress.cpp" ] && [ -f "uncompress.cpp"  ]; then
    tar -cvf ../${1}_checkpoint.tar compress.cpp uncompress.cpp HCNode.*pp HCTree.*pp
    if [ -s "BitInputStream.cpp" ] && [ -s "BitOutputStream.cpp" ]; then
        tar -rvf ../${1}_checkpoint.tar BitInputStream.*pp BitOutputStream.*pp
    fi
fi
git checkout master
git branch -d checkpoint

#check if final submission exists, unless we are ignoring final submission
exists=`git rev-list -n 1 --before="11/18/2013 20:15" --grep="final" -i master`
if [ -z "${exists}" ]; then
    revision=`git rev-list -n 1 --before="11/18/2013 20:15" master`
    git checkout ${revision} -b ontime
else
    ontime_check="TRUE"
    git checkout ${exists} -b ontime
fi
if [ -f "compress.cpp" ] && [ -f "uncompress.cpp" ]; then
    tar -cvf ../${1}_ontime.tar *.cpp *.hpp
fi
git checkout master
git branch -d ontime

#check for late submission day one, always get latest commit
unset revision
lateOne=`git rev-list -n 1 --before="11/19/2013 20:15" --after="11/18/2013 20:15" --grep="final" -i master`
if [ ! -z "${lateOne}" ]; then
    revision=${lateOne}
elif [ -z "${ontime_check}" ]; then
    revision=`git rev-list -n 1 --before="11/19/2013 20:15" --after="11/18/2013 20:15" master`
fi

if [ ! -z "${revision}" ]; then
    git checkout ${revision} -b lateone
   if [ -f "compress.cpp" ] && [ -f "uncompress.cpp" ]; then
      tar -cvf ../${1}_lateone.tar *.hpp *.cpp
   fi
   git checkout master
   git branch -d lateone
fi

#check for late submission day two, always get latest commit
lateTwo=`git rev-list -n 1 --before="11/20/2013 20:15" --after="11/19/2013 20:15" --grep="final" -i master`
if [ ! -z "${lateTwo}" ]; then
    revision=${lateTwo}
elif [ -z "${ontime_check}" ]; then
    revision=`git rev-list -n 1 --before="11/20/2013 20:15" --after="11/19/2013 20:15" master`
fi

if [ ! -z "${revision}" ]; then
    git checkout ${revision} -b latetwo
   if [ -f "compress.cpp" ] && [ -f "uncompress.cpp" ]; then
      tar -cvf ../${1}_latetwo.tar *.hpp *.cpp
   fi
   git checkout master
   git branch -d latetwo
fi

cd ..
if [ -f "${1}_checkpoint.tar" ] || [ -f "${1}_lateone.tar" ] || [ -f "${1}_ontime.tar" ] || [ -f "${1}_latetwo.tar" ]; then
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
