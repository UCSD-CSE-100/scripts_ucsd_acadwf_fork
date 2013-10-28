#!/bin/bash

if [ $# -lt 3 ]; then
   echo "Usage: pullRepo.sh repoName repoUrl grader [IGNORE]"
   exit 1
fi

#initial setup
submissionsDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getLabSubmissionsDir())'`
scratchDir=`python -c 'import sys; sys.path.append(".."); import config; print(config.getScratchRepoDir())'`
graderZip="${submissionsDir}${3}.zip"

#clone and begin packaging the repository
cd ${scratchDir}

git clone ${2}
cd ${1}

#If they have less than a certain number of commits, exit
commits=`git shortlog | grep -E '^[ ]+\w+' | wc -l`
if [ "${commits}" -le 3 ]; then
    echo "Did not work in this repository"
    cd ..
    rm -rf ${scratchDir}* #perform cleanup
    exit 0
fi

#Check if checkpoint submission exists, pull latest commit before deadline if it does not
exits=`git rev-list -n 1 --before="10/21/2013 18:30" --grep="CHECKPOINT" master`
if [ -z "${exists}" ]; then
   revision=`git rev-list -n 1 --before="10/21/2013 18:30" master`
   git checkout ${revision} -b checkpoint
else
   git checkout ${exists} -b checkpoint
fi
tar -cvf ../${1}_checkpoint.tar BST*.hpp RST.hpp
git checkout master
git branch -d checkpoint

#check if final submission exists, unless we are ignoring final submission
exists=`git rev-list -n 1 --before="10/25/2013 20:15" --grep="FINAL" master`
if [ -z "${exists}" ]; then
    revision=`git rev-list -n 1 --before="10/25/2013 20:15" master`
    git checkout ${revision} -b ontime
else
    git checkout ${exists} -b ontime
fi
tar -cvf ../${1}_ontime.tar BST*.hpp RST.hpp benchtree.cpp countint.*pp
git checkout master
git branch -d ontime

#check for late submission day one, always get latest commit
lateOne=`git rev-list -n 1 --before="10/26/2013 20:15" --after="10/25/2013 20:15" master`
if [ ! -z "${lateOne}" ]; then
   git checkout ${lateOne} -b lateone
   tar -cvf ../${1}_lateone.tar BST*.hpp RST.hpp benchtree.cpp countint.*pp
   git checkout master
   git branch -d lateone
fi

#check for late submission day two, always get latest commit
lateTwo=`git rev-list -n 1 --before="10/17/2013 20:15" --after="10/16/2013 20:15" master`
if [ ! -z "${lateTwo}" ]; then
   git checkout ${lateTwo} -b latetwo
   tar -cvf ../${1}_latetwo.tar BST*.hpp RST.hpp benchtree.cpp countint.*pp
   git checkout master
   git branch -d latetwo
fi

cp *.pdf ../.

cd ..
tar --ignore-failed-read -czvf ${1}.tar.gz *.tar *.pdf
zip ${graderZip} ${1}.tar.gz

#Finished with packaging, check if was success
if [ $? -ne 0 ]; then
   echo "Did not successfully add to archive"
   rm -rf ${scratchDir}* #perform cleanup
   exit 1
fi

rm -rf ${scratchDir}* #perform cleanup because of possible quota issues
exit 0
