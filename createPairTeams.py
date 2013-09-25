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

addPyGithubToPath()

from github import Github
from github import GithubException
                      
defaultInputFileName =  '../CS56-S13-data/CS56 S13 Github Userids (Responses) - Form Responses.csv'
defaultPairFileName =  '../CS56-S13-data/pairs.csv'

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

org= g.get_organization("UCSB-CS56-S13")

addTeamsForPairsInFile(g,org,args.inFileName,args.pairFileName)








