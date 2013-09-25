#!/usr/bin/python

# This script takes a lab number such as lab00 as the command line argument,
# and tries to update all of the lab00_* repos in the 
# UCSB-CS56-S13 organization by deleting all files in the repo currently,
# and replacing them with all files from those under the directory
# lab00_prototype
#

import getpass

import sys

import argparse

import os
import subprocess

PyGitHubLocs = ["./PyGithub"] # list of where to look for PyGithub

#  "/Users/pconrad/github/github-acadwf-scripts/PyGithub"]

from github_acadwf import addPyGithubToPath
addPyGithubToPath()

from github import Github
from github import GithubException

from github_acadwf import pushFilesToRepo







parser = argparse.ArgumentParser(description='push files from labxx_prototype directory to labxx_* repos')

parser.add_argument('lab',metavar='labxx',  
                    help="which lab (e.g. lab00, lab01, etc.)")

parser.add_argument('-f','--firstName', 
                    help="if passed, only update labxx_FirstName",
                    default="")

parser.add_argument('-u','--githubUsername', 
                    help="github username, default is current OS user",
                    default=getpass.getuser())

parser.add_argument('-s','--scratchDirName', 
                    help="scratch directory to clone repos in while doing work",
                    default="./scratchRepos")


args = parser.parse_args()


pw = getpass.getpass()
g = Github(args.githubUsername, pw, user_agent="PyGithub")
org= g.get_organization("UCSB-CS56-S13")

pushFilesToRepo(g,org,args.lab,args.firstName,args.scratchDirName)

