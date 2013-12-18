#!/usr/bin/env python

""" Python module for archiving student submissions

    --delete option will also issue a DELETE api call to github
"""

import getpass
import subprocess
import sys

#external installed libraries
try:
    import requests
except ImportError:
    print("Requests not installed on this machine")

#own libraries
sys.path.append("..")
import argparse
import checkrepo
import config
import getclass

ARCHIVE_SOLO = "Could not archive {0}"
ARCHIVE_PAIR = "Could not archive pair {0} {1}"

DELETE_REPO  = "https://api.github.com/repos/{0}/{1}"

SOLO_REPO    = "{0}_{1}"
PAIR_REPO    = "{0}_Pair_{1}_{2}"

def main(del_arg):
    """ Main driver for archiving repos in a github repository """
    students  = getclass.get_students(config.getStudentsFile())
    class_org = config.getOrgName()
    labs      = config.get_labs()

    username = raw_input("Username: ")
    password = getpass.getpass()

    credentials = (username, password)

    for lab in labs:
        for student in students.keys():
            if not checkrepo.check_repo_ghid(class_org, lab, student):
                continue
            repo_name = SOLO_REPO.format(lab, student)
            archive_repo(labno=lab, name=repo_name, ghid=student, ghid2=None)
            if del_arg.delrepo:
                delete_repo(class_org, repo_name, credentials)


def delete_repo(org, repo_url, credentials):
    """ Deletes the specified repo_url from github  """
    request_url = DELETE_REPO.format(org, repo_url)
    try:
        req = requests.delete(request_url, auth=credentials)
        if req.status_code != requests.codes.no_content :
            print("Could not delete {0}".format(repo_url))
    except NameError:
        #TODO use subprocess and curl
        print("Requests not imported, falling back on curl")

def archive_pairs(class_org, labs, credentials, delrepo):
    """ Logic for archiving student pairs  """
     #Currently hardcoded, need a way to put this in the config file for P1
    p1pairsfn = "/Users/arden/Documents/Github/scripts_ucsd_acadwf_fork/\
                 P1Pairs.csv"
    p1pairs   = getclass.get_pairs(p1pairsfn)
    p2pairs   = getclass.get_pairs(config.getPairsFile())

    for lab in labs[0:2]:
        for pair in p1pairs.keys():
            repo_url  = checkrepo.PAIR.format(class_org, lab, pair,
                                              p1pairs[pair])
            repo_name = PAIR_REPO.format(lab, pair, p1pairs[pair])
            if not checkrepo.check_repo_ghid(class_org, lab, pair,
                                             p1pairs[pair]):
                if not checkrepo.check_repo_ghid(class_org, lab,
                                                 p1pairs[pair], pair):
                    continue
                repo_url  = checkrepo.PAIR.format(class_org, lab, pair,
                                                  p1pairs[pair])
                repo_name = PAIR_REPO.format(lab, p1pairs[pair], pair)
            archive_repo(labno=lab, name=repo_url, ghid=pair,
                         ghid2=p1pairs[pair])
            if delrepo:
                delete_repo(class_org, repo_name, credentials)

    for lab in labs[2:]:
        for pair in p2pairs.keys():
            repo_url  = checkrepo.PAIR.format(class_org, lab, pair,
                                              p2pairs[pair])
            repo_name = PAIR_REPO.format(lab, pair, p2pairs[pair])
            if not checkrepo.check_repo_ghid(class_org, lab, pair,
                                             p2pairs[pair]):
                if not checkrepo.check_repo_ghid(class_org, lab,
                                                 p2pairs[pair], pair):
                    continue
                repo_url  = checkrepo.PAIR.format(class_org, lab, pair,
                                                  p2pairs[pair])
                repo_name = PAIR_REPO.format(lab, p2pairs[pair], pair)
            archive_repo(labno=lab, name=repo_url, ghid=pair, ghid2=
                         p2pairs[pair])
            if delrepo:
                delete_repo(class_org, repo_name, credentials)

def archive_repo(**repo):
    """ Archives the specified repo  """
    repo_proc = subprocess.Popen(["./cache_repos.sh", repo['labno'],
                                  repo['name']])
    repo_stat = repo_proc.wait()
    if repo_stat:
        if repo['ghdi2'] == None :
            print ARCHIVE_SOLO.format(repo['ghid'])
        else:
            print ARCHIVE_PAIR.format(repo['ghid'], repo['ghid2'])

if __name__ == '__main__':
    PARSER   = argparse.ArgumentParser(description='Archive repositories')
    PARSER.add_argument('--delete', dest='delrepo', action='store_true',
                        help='Delete repositories after archiving',
                        default=False)
    main(PARSER.parse_args())
    sys.exit(0)
