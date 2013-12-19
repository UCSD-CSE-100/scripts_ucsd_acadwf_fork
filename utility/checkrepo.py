#!/usr/bin/env python

""" Python module for checking if a repository exists or not on github
    Author: Arden Liao (ardentsonata)

    Note: User executing the script must have permission to view those
          repositories
"""

import subprocess

SOLO = "git@github.com:{0}/{1}_{2}.git"
PAIR = "git@github.com:{0}/{1}_Pair_{1}_{2}"

def check_repo_ghid(org, project, gh_id, gh_id2=None):
    """ Check if a project exists in github for a specified
        Github ID in an organization
    """
    if gh_id2 == None:
        repo_name = SOLO.format(org, project, gh_id)
    else:
        repo_name = PAIR.format(org, project, gh_id, gh_id2)

    repo_proc = subprocess.Popen(["git", "ls-remote", repo_name,
                                  "&> /dev/null]"],
                                  stderr = subprocess.PIPE)
    return (repo_proc.wait() == 0)

def check_repo_name(repo_name):
    """ Check if a project exists via the git url  """
    repo_proc = subprocess.Popen(["git", "ls-remote", repo_name,
                                  "&> /dev/null]"],
                                  stderr = subprocess.PIPE)
    return (repo_proc.wait() == 0)

