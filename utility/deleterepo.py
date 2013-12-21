#!/usr/bin/env python

""" Python module for deleting student submissions
    Author: Arden Liao (ardentsonata)
"""

#python STL
import logging
import subprocess

#importing external libraries
try:
    import requests
except ImportError:
    logging.info("\'requests\' module not installed on this system")

#importing user defined libraries
sys.path.append("..")
import argparse #defined in python STL, but school python installation old

DELETE_REPO = "https://api.github.com/repos/{_org}/{_repo_name}"

def delete_repo(org, repo_name, credentials):
    """ Deletes the specified repo from a github organization  """
    request_url = DELETE_REPO.format(_org=org, _repo_name=repo_name)
    try:
        req = requests.delete(request_url, auth=credentials)
        if (req.status_code != requests.codes.no_content):
            logging.error("Could not delete {0}".format(repo_name))
    except NameError:
        logging.info("Requests not imported, using subprocess.")
        repo_proc = subprocess.Popen(["curl", "-X", "DELETE", "-u",
                                      credentials[0]+":"+credentials[1],
                                      request_url])
        if (repo_proc.wait() != 0):
            logging.error("Could not delete {0}".format(repo_name))
