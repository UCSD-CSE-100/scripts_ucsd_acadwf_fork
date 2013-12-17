#!/usr/bin/env/python

""" Python module for archiving student submissions

    --delete option will also issue a DELETE api call to github
"""

import getpass
import requests
import subprocess
import sys

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

def main():
    """ Main driver for archiving repos in a github repository """
    parser   = argparse.ArgumentParser(description='Archive repositories')
    parser.add_argument('--delete', dest='delrepo', action='store_true',
                        help='Delete repositories after archiving',
                        default=False)
    del_arg   = parser.parse_args()
    pairs     = getclass.get_pairs(config.getPairsFile())
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
            repo_url = checkrepo.SOLO.format(class_org, lab, student)
            archive_repo(labno=lab, name=repo_url, ghid=student, ghid2=None)
            if del_arg.delrepo:
                repo_name = SOLO_REPO.format(lab, student)
                delete_repo(class_org, repo_name, credentials)
        for pair in pairs.keys():
            repo_url  = checkrepo.PAIR.format(class_org, lab, pair, pairs[pair])
            repo_name = PAIR_REPO.format(lab, pair, pairs[pair])
            if not checkrepo.check_repo_ghid(class_org, lab, pair, pairs[pair]):
                if not checkrepo.check_repo_ghid(class_org, lab,
                                              pairs[pair], pair):
                    continue
                repo_url  = checkrepo.PAIR.format(class_org, lab, pair,
                                                  pairs[pair])
                repo_name = PAIR_REPO.format(lab, pairs[pair], pair)
            archive_repo(labno=lab, name=repo_url, ghid=pair, ghid2=pairs[pair])
            if del_arg.delrepo:
                delete_repo(class_org, repo_name, credentials)


def delete_repo(org, repo_url, credentials):
    """ Deletes the specified repo_url from github  """
    request_url = DELETE_REPO.format(org, repo_url)
    req = requests.delete(request_url, auth=credentials)
    if req.status_code != requests.codes.no_content :
        print "Could not delete {0}".format(repo_url)


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
    main()
    sys.exit(0)
