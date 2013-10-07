#!/usr/bin/python

import os
import getpass
import sys
import random

sys.path.append("../PyGithub");
sys.path.append("..");

import argparse
from github_acadwf import pullRepoForGrading
import config #assume exists due to ./initrepo

tutors    = config.getTutors()
numTutors = len(tutors)



sys.exit(0)

