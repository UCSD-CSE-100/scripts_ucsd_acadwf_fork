#!/usr/bin/python

import os
import getpass
import sys
import random
import subprocess

sys.path.append("../PyGithub");
sys.path.append("..");

import argparse
from github_acadwf import pullRepoForGrading
import config #assume exists due to ./initrepo


from github import Github
from github import GithubException

tutors    = config.getTutors()
numTutors = len(tutors)

parser = argparse.ArgumentParser(description='Pull repos for grading that start with a certain prefix')
parser.add_argument('prefix',help='prefix e.g. lab00')
parser.add_argument('-u','--githubUsername',
                    help="github username, default is current OS user",
                    default=getpass.getuser())
parser.add_argument('-o','--orgName',
                    help="organization e.g. UCSD-CSE-100",
                    default=config.getOrgName())
args = parser.parse_args()

username = args.githubUsername
pw       = getpass.getpass()
g        = Github(username, pw, user_agent='PyGithub')
org      = g.get_organization(args.orgName)
repos    = org.get_repos()

random.shuffle(tutors)
currCount=0;

for repo in repos:
    if repo.name.startswith(args.prefix):
        currTutor = tutors[currCount];
        #perform operations here
        callList = ["./pullRepo.sh",repo.name,repo.ssh_url,currTutor]
        check = subprocess.call(callList)
        #check if repo was added
        if(check == 0):
            currCount += 1
            currCount %= 8
            if ( currCount == 0 ):
                random.shuffle(tutors)

# pick up the pair stragglers
#callList = ["./pullPairStragglers.sh", args.prefix]
#check = subprocess.call(callList)

#if (check != 0 ):
#    print("Did not pick up all pairs!")

#pick up the remaining students
#callList = ["./pullStragglers.sh", args.prefix]
#check = subprocess.call(callList)

#if(check == 0):
#    sys.exit(0)

#print("Did not pick up all students!")
sys.exit(1)

