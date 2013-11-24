#!/usr/bin/python

import subprocess

def repo_exists(project, gh_id, gh_id2=None):
    repo_name = "git@github.com:UCSD-CSE-100/{0}_{1}.git".format(project, gh_id)
    if gh_id2 != None:
        repo_name = "git@github.com:UCSD-CSE-100/{0}_Pair_{1}_{2}.git".format(project, gh_id, gh_id2) 
    repo_proc  = subprocess.Popen(["git", "ls-remote", repo_name, "&> /dev/null"],
                                  stderr = subprocess.PIPE)
    repo_state = repo_proc.wait()
    return (repo_state == 0)

import argparse
import random
import csv
import sys

sys.path.append("..");
import config

tutors    = config.getTutors()
numTutors = len(tutors)

parser = argparse.ArgumentParser(description='Pull Students for grading')
parser.add_argument('prefix', help='prefix e.g. PA1')

args = parser.parse_args()
lab = args.prefix

submissions_dir = config.getLabSubmissionsDir()
pairs    = {}
students = {}

with open(config.getPairsFile(), 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID'].lower()] = line['Partner2_GithubID'].lower()
        pairs[line['Partner2_GithubID'].lower()] = line['Partner1_GithubID'].lower()

with open(config.getStudentsFile(), 'rb') as studentsFile:
    student_reader = csv.DictReader(studentsFile)
    for line in student_reader:
        students[line['github userid'].lower()] = (line['First Name'], line['Last Name'])

