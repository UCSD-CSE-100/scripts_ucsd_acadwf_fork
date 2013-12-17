#!/usr/bin/env/python

""" Python module for archiving student submissions

    --delete option will also issue a DELETE api call to github
"""

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

def main():
    """ Main driver for archiving repos in a github repository """
    parser   = argparse.ArgumentParser(description='Archive repositories')
    parser.add_argument('--delete', dest='del', action='store_true',
                        help='Delete repositories after archiving',
                        default=False)

    pairs    = getclass.get_pairs(config.getPairsFile())
    students = getclass.get_students(config.getStudentsFile())
    class_org      = config.getOrgName()
    labs           = config.get_labs()

    for lab in labs:
        for student in students.keys():
            if not checkrepo.check_repo_ghid(class_org, lab, student):
                continue
            repo_name = checkrepo.SOLO.format(class_org, lab, student)
            archive_repo(labno=lab, name=repo_name, ghid=student, ghid2=None)

        for pair in pairs.keys():
            repo_name = checkrepo.PAIR.format(class_org, lab, pair, pairs[pair])
            if not checkrepo.check_repo_ghid(class_org, lab, pair, pairs[pair]):
                if not checkrepo.check_repo_ghid(class_org, lab,
                                              pairs[pair], pair):
                    continue
                repo_name = checkrepo.PAIR.format(class_org, lab, pair,
                                                 pairs[pair])
            archive_repo(labno=lab, name=repo_name, ghid=pair,
                                                    ghid2=pairs[pair])


def delete_repo(repo_url):
    """ Deletes the specified repo_url from github  """
    return repo_url


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
