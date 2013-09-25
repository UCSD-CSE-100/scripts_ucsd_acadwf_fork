#!/usr/bin/python

# This script looks up every pair team that exists.
# It then,for each pair team
#  (4) creates a repo for the team (if it doesn't already exist)
#  (5) populates it, but only if it was JUST created.

import getpass
import argparse
import os
import sys

from github_acadwf import addPyGithubToPath
from github_acadwf import updatePairsForLab
#from github_acadwf import createLabRepo
#from github_acadwf import findTeam
#from github_acadwf import pushFilesToRepo

addPyGithubToPath()

from github import Github
from github import GithubException
                      
defaultInputFilename =  '../CS56-S13-data/CS56 S13 Github Userids (Responses) - Form Responses.csv'

parser = argparse.ArgumentParser(description='Update for lab only for new users')

parser.add_argument('lab',metavar='labxx',  
                    help="which lab (e.g. lab00, lab01, etc.)")

parser.add_argument('-i','--infileName',
                    help='input file (default: ' + defaultInputFilename+"'",
                    default=defaultInputFilename)

parser.add_argument('-u','--githubUsername', 
                    help="github username, default is current OS user",
                    default=getpass.getuser())

parser.add_argument('-s','--scratchDirName', 
                    help="scratch directory to clone repos in while doing work",
                    default="./scratchRepos")

parser.add_argument('-t','--teamPrefix', 
                    help="prefix of teams to create",
                    default="")


args = parser.parse_args()

if not os.access(args.scratchDirName, os.W_OK):
    print(args.scratchDirName + " is not a writable directory.")
    sys.exit(1)

pw = getpass.getpass()
g = Github(args.githubUsername, pw, user_agent="PyGithub")

org= g.get_organization("UCSB-CS56-S13")

updatePairsForLab(g,org,args.lab,args.scratchDirName, args.teamPrefix)







