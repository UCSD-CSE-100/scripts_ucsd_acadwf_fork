#!/usr/bin/env python

""" Python module for deleting student submissions
    Author: Arden Liao (ardentsonata)
"""

#python STL
import getpass
import logging
import re
import subprocess
import sys

#importing external libraries
try:
    import requests
except ImportError:
    logging.info("\'requests\' module not installed on this system")

#importing user defined libraries
sys.path.append("..")
#import argparse #defined in python STL, but school python installation old

DELETE_REPO = "https://api.github.com/repos/{_org}/{_repo_name}"
GET_REPO    = "https://api.github.com/orgs/{_org}/repos?page={_pgn}"

def main():
    """ Main driver for deleting all student submissions for
        a github organization
    """
    username = raw_input("Username: ")
    password = getpass.getpass()
    cred = (username, password)
    collect_repos("UCSD-CSE-100", cred)
    return 0

def collect_repos(org, credentials):
    """ Returns a list of all repos for an organization  """
    repos = []
    request_url = GET_REPO.format(_org=org, _pgn="1")

    try:
        req   = requests.get(request_url, auth=credentials)
        pages = req.headers['link']

        # store the repos from the first page
        repos.extend([x['name'] for x in req.json()])

        #determine if there are multiple repos
        if re.search("last", pages):
            lastpg = re.findall("page=[0-9]+", pages)[1]
            lastpg = re.sub(r"\D", "", lastpg)

            for page in range(2, int(lastpg)+1):
                request_url = GET_REPO.format(_org=org, _pgn=page)
                req = requests.get(request_url, auth=credentials)
                repos.extend([x['name'] for x in req.json()])

    except NameError:
        logging.info("Requests not imported, using subprocess")
    return repos

def delete_repo(org, repo_name, credentials):
    """ Deletes the specified repo from a github organization  """
    request_url = DELETE_REPO.format(_org=org, _repo_name=repo_name)
    deleted     = False

    try:
        req = requests.delete(request_url, auth=credentials)
        deleted =  (req.status_code == requests.codes.no_content)
    except NameError:
        logging.info("Requests not imported, using subprocess.")
        repo_proc = subprocess.Popen(["curl", "-X", "DELETE", "-u",
                                      credentials[0]+":"+credentials[1],
                                      request_url])
        deleted = (repo_proc.wait() == 0)

    if not deleted:
        logging.error("Could not delete {0}".format(repo_name))

if __name__ == "__main__":
    main()
    sys.exit(0)
