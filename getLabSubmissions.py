#!/usr/bin/python
import os

labSubmissionsDir = "labSubmissions"
if not os.access(labSubmissionsDir, os.W_OK):
  os.mkdir(labSubmissionsDir, 0700)

import getpass
import sys
import argparse
from github_acadwf import pullRepoForGrading

# In the main directory of the repo where you are developing with PyGithub,
# type:
#    git submodule add git://github.com/jacquev6/PyGithub.git PyGithub
#    git submodule init
#    git submodule update
#
# That will populate a PyGithub subdirectory with a clone of PyGithub
# Then, to add it to your Python path, you can do:

sys.path.append("./PyGithub");

from github import Github
from github import GithubException

parser = argparse.ArgumentParser(description='Pull repos for grading that start with a certain prefix')
parser.add_argument('prefix',help='prefix e.g. lab00')
parser.add_argument('-u','--githubUsername',
                    help="github username, default is current OS user",
                    default=getpass.getuser())
parser.add_argument('-o','--orgName',
                    help="organization e.g. UCSB-CS56-S13",
                    default='UCSB-CS56-S13')
args = parser.parse_args()

username = args.githubUsername
pw = getpass.getpass()
g = Github(username, pw, user_agent='PyGithub')

print("All repos for organization: ",args.orgName)

org = g.get_organization(args.orgName)

## TODO: Add some error checking code here to see whether
##  the lookup was successful.  Do we try/except or check the return value?

repos = org.get_repos()

for repo in repos:
  if repo.name.startswith(args.prefix):
    print(repo.name)
    pullRepoForGrading(repo,labSubmissionsDir+'/'+args.prefix)
