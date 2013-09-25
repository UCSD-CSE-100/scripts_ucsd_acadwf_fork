#!/usr/bin/python

# createPairPartnersReport.py iterates through every comment in every issue in every repo in the 
# specified organization, and generates markdown output describing what students and moderator are
# assigned to each issue

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
g = Github(username, pw, user_agent="cs56-acadwf-scripts")

print("All repos for organization: ",args.orgName)

org = g.get_organization(args.orgName)

## TODO: Add some error checking code here to see whether
##  the lookup was successful.  Do we try/except or check the return value?

repos = org.get_repos()

partner_mapping = []

# Iterate through all the comments in all the issues in all the repos
for repo in repos:
    issues = repo.get_issues()
    for issue in issues:
        comments = issue.get_comments()
        for comment in comments:
            words = comment.body.split()
            if words[0] == "~claimed":
                pair_issue = dict()
                pair_issue["repo"] = repo.name
                pair_issue["issue"] = issue.number
                pair_issue["students"] = []
                pair_issue["moderator"] = ""

                is_moderator = False
                for word in words:
                    if word.startswith("@") and not is_moderator:
                        pair_issue["students"].append(word[1:])
                    elif word == "~moderator":
                        is_moderator = True
                    elif is_moderator:
                        is_moderator = False
                        pair_issue["moderator"] = word[1:]

                partner_mapping.append(pair_issue)
                break

output = "| Repo                       | Issue | Moderator     | Students                       |\n"
output += "| -------------------------- | ----- | ------------- | ------------------------------ |"
for issue in partner_mapping:
	output += "\n| " + issue["repo"] + " | " + str(issue["issue"]) + " | " + issue["moderator"] + " | "
	for student in issue["students"]:
		output += "@" + student + " "
	output += " |"
print output
