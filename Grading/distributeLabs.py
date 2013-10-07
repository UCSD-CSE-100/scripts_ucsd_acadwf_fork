#!/usr/bin/python
import os

import getpass
import sys
import argparse
from github_acadwf import pullRepoForGrading

import random

sys.path.append("../PyGithub");
sys.path.append("..");

if not os.path.exists("../config.py"):
	print("Unable to find config file, please see sample_config.py")
	sys.exit(1)

import config