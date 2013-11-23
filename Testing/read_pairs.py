#!/usr/bin/python

import csv
import os
import sys
import random
import subprocess

sys.path.append("../PyGithub")
sys.path.append("..")

import config
pairs = {}
students = {}

with open("../" + config.getPairsFile(), 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID']] = line['Partner2_GithubID']
        pairs[line['Partner2_GithubID']] = line['Partner1_GithubID']

count = 0
with open("../" + config.getStudentsFile()) as studentsFile:
    student_reader = csv.DictReader(studentsFile)
    for line in student_reader:
        students[line['github userid']] = line['First Name'] + " " + line['Last Name']

print "There are {0} pairs and {1} students".format(len(pairs)/2, len(students))
