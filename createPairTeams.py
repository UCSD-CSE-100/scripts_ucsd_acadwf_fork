#!/usr/bin/python

# This script reads all the users and pairs from the CSV files created
# by the Google Form.

# It first runs all the checks on the CSV file for names, finding duplicates,
# and disambiguating by adding _A _B, etc.

# It then,for each line in the pair spreadsheet
#  (1) creates the Pair_FirstName_SecondName team
#  (2) adds the github users for both student to that team

import getpass
import argparse
import os
import sys

from github_acadwf import addPyGithubToPath
from github_acadwf import addTeamsForPairsInFile

#check if config file exists
if not os.path.exists("config.py"):
	print("Unable to find config file, please see sample_config.py")
	sys.exit()

import config

addPyGithubToPath()

from github import Github
from github import GithubException
                      
defaultInputFileName =  config.getStudentsFile()
defaultPairFileName  =  config.getPairsFile()

parser = argparse.ArgumentParser(description='Setup teams for pairs')

parser.add_argument('-i','--inFileName',
                    help='input file (default: ' + defaultInputFileName+"'",
                    default=defaultInputFileName)

parser.add_argument('-p','--pairFileName',
                    help='pair file (default: ' + defaultPairFileName+"'",
                    default=defaultPairFileName)

parser.add_argument('-u','--githubUsername', 
                    help="github username, default is current OS user",
                    default=getpass.getuser())

args = parser.parse_args()

pw = getpass.getpass()
g = Github(args.githubUsername, pw, user_agent="PyGithub")

org= g.get_organization(config.getOrgName())

addTeamsForPairsInFile(g,org,args.inFileName,args.pairFileName)

sys.exit(0)






