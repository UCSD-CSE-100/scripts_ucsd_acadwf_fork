#!/usr/bin/python

# createPointsReport.py iterates through every comment in every issue in every repo in the 
# specified organization, and generates a .csv file containing the points and users associated
# with each issue

import getpass
import sys
import argparse

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

parser = argparse.ArgumentParser(description='List all repos for an org')
parser.add_argument('orgName',help='github Organization name')

args = parser.parse_args()

username = raw_input("Github Username:")
pw = getpass.getpass()
g = Github(username, pw, user_agent="PyGithub")

print("All repos for organization: ",args.orgName)

org = g.get_organization(args.orgName)

## TODO: Add some error checking code here to see whether
##  the lookup was successful.  Do we try/except or check the return value?

repos = org.get_repos()

# Iterate through all the comments in all the issues in all the repos
for repo in repos:
    issues = repo.get_issues()
    issue_report = {"repository"   : repo.full_name, 
                    "estimated"    : 0,
                    "requested"    : 0,
                    "assigned"     : 0,
                    "assignee_id"  : 0,
                    "esimatee_id"  : 0,
                    "requestee_id" : 0}
    for issue in issues:
        issue_report["issue"] = issue.id
        comments = issue.get_comments()
        for comment in comments:
            comment_text = comment.body
            words = comment_text.split(" ")
            for i in range(0, len(words) - 1):
                if words[i] == "~estimated":
                    issue_report["estimated"] = int(words[i + 1])
                    issue_report["estimatee_id"] = comment.user.id
                elif words[i] == "~assigned":
                    issue_report["assigned"] = int(words[i + 1])
                    issue_report["assignee_id"] = comment.user.id
                elif words[i] == "~requested":
                    issue_report["requested"] = int(words[i + 1])
                    issue_report["requestee_id"] = comment.user.id
        print issue_report