#!/usr/bin/env python

""" Python module for deleting student teams
    Author: Arden Liao (ardentsoanta)
"""

#Python STL
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

GET_TEAMS   = "https://api.github.com/orgs/{_org}/teams"
DELETE_TEAM = "https://api.github.com/teams/{_id}"

def main():
    return 0


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
    try:
        req = requests.delete(request_url, credentials)
        if (req.status_code != requests.codes.nocontent):
            logging.error("Could not delete team {0} with id {1}".format(
                          team[0], team[1]))
    except NameError
        logging.info("Requests not imported, using subprocess")


if __name__ == "__main__":
    main()
    sys.exit(0)
