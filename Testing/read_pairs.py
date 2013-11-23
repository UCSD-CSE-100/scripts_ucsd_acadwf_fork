import csv
import os
import sys
import random
import subprocess

sys.path.append("../PyGithub")
sys.path.append("..")

import config

pairFile = config.getPairFile()

pairs = {}

with open(config.getPairFile(), 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID']] = line['Partner2_GithubID']

print pairs

    