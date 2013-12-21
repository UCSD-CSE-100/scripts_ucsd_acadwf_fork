#!/usr/bin/env python

""" Python module for archiving student submissions
    Author: Arden Liao (ardentsonata)

    --delete option will also issue a DELETE api call to github
"""

import getpass
import logging
import subprocess
import sys

#own libraries
sys.path.append("..")
import argparse
import checkrepo
import config
import deleterepo
import getclass

ARCHIVE_SOLO = "Could not archive {0}"
ARCHIVE_PAIR = "Could not archive pair {0} {1}"

SOLO_REPO    = "{0}_{1}"
PAIR_REPO    = "{0}_Pair_{1}_{2}"

def main(del_arg):
    """ Main driver for archiving repos in a github repository """
    class_org = config.getOrgName()
    labs      = config.get_labs()

    username = raw_input("Username: ")
    password = getpass.getpass()

    credentials = (username, password)

    archive_solo(class_org, labs, credentials, del_arg.delrepo)
    archive_pairs(class_org, labs, credentials, del_arg.delrepo)


def archive_solo(org, labs, credentials, delrepo):
    """ Archives all students's solo repository  """
    students  = getclass.get_students(config.getStudentsFile())
    for lab in labs:
        for student in students.keys():
            if not checkrepo.check_repo_ghid(org, lab, student):
                continue
            repo_name = SOLO_REPO.format(lab, student)
            archive_repo(labno=lab, name=repo_name, ghid=student, ghid2=None)
            if delrepo:
                deleterepo.delete_repo(org, repo_name, credentials)

def archive_pairs(org, labs, credentials, delrepo):
    """ Logic for archiving student pairs  """
     #Currently hardcoded, need a way to put this in the config file for P1
    p1pairsfn = "/Users/arden/Documents/Github/scripts_ucsd_acadwf_fork/\
                 P1Pairs.csv"
    p1pairs   = getclass.get_pairs(p1pairsfn)
    p2pairs   = getclass.get_pairs(config.getPairsFile())

    for lab in labs[0:2]:
        archive_pairs_for_lab(org, lab, credentials, p1pairs, delrepo)

    for lab in labs[2:]:
        archive_pairs_for_lab(org, lab, credentials, p2pairs, delrepo)

def archive_pairs_for_lab(org, lab, credentials, pairs, delrepo):
    """ Archives all students for a given lab and pairs  """
    for pair in pairs.items():
        repo_name = PAIR_REPO.format(lab, pair[0], pair[1])
        if not checkrepo.check_repo_ghid(org, lab, pair[0], pair[1]):
            if not checkrepo.check_repo_ghid(org, lab, pair[1], pair[0]):
                continue
            repo_name = PAIR_REPO.format(lab, pairs[pair], pair)

        archive_repo(labno=lab, name=repo_name, ghid=pair, ghid2=pairs[pair])
        if delrepo:
            deleterepo.delete_repo(org, repo_name, credentials)


def archive_repo(**repo):
    """ Archives the specified repo  """
    repo_proc = subprocess.Popen(["./cache_repos.sh", repo['labno'],
                                  repo['name']])
    repo_stat = repo_proc.wait()
    if repo_stat:
        if repo['ghdi2'] == None :
            logging.error(ARCHIVE_SOLO.format(repo['ghid']))
        else:
            logging.error(ARCHIVE_PAIR.format(repo['ghid'], repo['ghid2']))

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Archive repositories')
    PARSER.add_argument('--delete', dest='delrepo', action='store_true',
                        help='Delete repositories after archiving',
                        default=False)
    logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)\
                        - %(message)s')
    main(PARSER.parse_args())
    sys.exit(0)
