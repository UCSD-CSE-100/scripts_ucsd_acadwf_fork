#!/usr/bin/env python

""" Python module for pulling student submissions and bundling them
    Author: Arden Liao (ardentsonata)
"""

import subprocess
import sys

sys.path.append("..")
import config

SOLO_NAME = "{_lab}_{_ghid}"
PAIR_NAME = "{_lab}_Pair_{_ghid1}_{_ghid2}"

REPO_URL  = "git@github.com/{_org}/{_repo}"

def pull_repo(lab, org, ghid, ghid2=None, tutor, duedate, chkpoint=None,
              dbglog):
    """ Pulls the specified repo with pullRepo.sh  """
    args = ['./pullRepo.sh']

    # Append the repo_name and repo_url to args
    if ghid2 is None :
        args.append(SOLO_NAME.format(_lab=lab, _ghid=ghid))
    else:
        args.append(PAIR_NAME.format(_lab=lab, _ghid=ghid, _ghid2=ghid2))
    args.append(REPO_URL.format(_org=org, _repo=args[1]))

    #Append shared args
    args.extends([tutor, lab, duedate[0], duedate[1]])

    #Append checkpoint date if it exists
    if checkpoint is not None:
       args.extends([chkpoint[0], chekpoint[1]])

    repo_proc = subprocess.Popen(args, stdout=dbglog, stderr=subprocess.PIPE)
    return (repo-proc.wait() == 0)

