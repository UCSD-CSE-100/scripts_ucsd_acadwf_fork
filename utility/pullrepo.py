#!/usr/bin/env python

""" Python module for pulling student submissions and bundling them
    Author: Arden Liao (ardentsonata)
"""

import logging
import subprocess

SOLO_NAME = "{_lab}_{_ghid}"
PAIR_NAME = "{_lab}_Pair_{_ghid1}_{_ghid2}"

REPO_URL  = "git@github.com/{_org}/{_repo}"

def pull_repo_depre(lab, org, ghid, tutor, duedate, dbglog, ghid2=None,
                    checkpoint=None):
    """ Pulls the specified repo with pullRepo.sh  """
    args = ['./pullRepo.sh']

    # Append the repo_name and repo_url to args
    if ghid2 is None :
        args.append(SOLO_NAME.format(_lab=lab, _ghid=ghid))
    else:
        args.append(PAIR_NAME.format(_lab=lab, _ghid=ghid, _ghid2=ghid2))
    args.append(REPO_URL.format(_org=org, _repo=args[1]))

    #Append shared args
    args.extend([tutor, lab, duedate[0], duedate[1]])

    #Append checkpoint date if it exists
    if checkpoint is not None:
        args.extend([checkpoint[0], checkpoint[1]])

    repo_proc = subprocess.Popen(args, stdout=dbglog, stderr=subprocess.PIPE)
    return (repo_proc.wait() == 0)

def pull_repo(info, student=None, pair=None):
    """ Pulls the repo specified by student or pair based on
        the provided information
    """
    if student is None and pair is None:
        logging.error("No student or pair arg supplied.")
        return False

    args = ["./pullRepo.sh"]
    if pair is None :
        args.append(SOLO_NAME.format(_lab=info['labno'], _ghid=student.ghid))
    else:
        args.append(PAIR_NAME.format(_lab=info['labno'], _ghid=pair[0].ghid,
                                     _ghid2=pair[1].ghid))
    args.append(REPO_URL.format(_org=info['org'], _repo=args[1]))

    #Append shared args
    args.extend([info['tutor'], info['labno'], info['due_date'][0],
                 info['due_date'][1]])

    if info['chkpoint'] is not None:
        args.extend([info['chkpoint'][0], info['chkpoint'][1]])

    repo_proc = subprocess.Popen(args, stdout=info['debug'],
                                 stderr=subprocess.PIPE)
    return (repo_proc.wait() == 0)

