#!/usr/bin/env python

""" Python module for deleting student teams
    Author: Arden Liao (ardentsoanta)
"""

#Python STL
import getpass
import logging
import re
import subprocess
import sys

#External Libraries
try:
    import requests
except:
    logging.info("\'requests module\' not installed on this system")

#importing user defined libraries
sys.path.append("..")
import argparse
import config

GET_TEAMS   = "https://api.github.com/orgs/{_org}/teams"
DELETE_TEAM = "https://api.github.com/teams/{_id}"

def main():
    class_org = config.getOrgname()

    username = raw_input("Username: ")
    password = getpass.getpass()

    credentials = (username, password)
    teams       = get_teams(class_org, credentials)

    for team in teams:
        if (re.search("\A(Student_)", team[0]) != None) or \
           (re.search("\A(Pair_)", team[0]) != None):
            delete_team(team, credentials)

def get_teams(org, credentials):
    request_url = GET_TEAMS.format(_org=org)
    try:
        req = requests.get(request_url, credentials)
        if (req.status_code != requests.codes.ok):
            logging.error("Could not retrieve teams for {0}".format(org))
            sys.exit(1)i
        teams = req.json()
        return [ (team['name'], team['id']) for team in teams ]
    except NameError:
        logging.info("Requests not installed on this system")
        sys.exit(0)

def delete_team(team, credentials):
    request_url = DELETE_TEAM.format(_id=team[1])
    deleted = False

    try:
        req = requests.delete(request_url, credentials)
        deleted = (req.status_code == requests.codes.nocontent)
    except NameError
        logging.info("Requests not imported, using subprocess")
        repo_proc = subprocess.Popen(["curl", "-X", "DELETE", "-u",
                                      credentials[0]+":"+credentials[1],
                                      request_url])
        deleted = (repo_proc.wait() == 0)

    if not deleted:
        logging.error("Could not delete team {0} with id {1}".format(team[0],
                                                                     team[1]))

if __name__ == "__main__":
    main()
    sys.exit(0)
