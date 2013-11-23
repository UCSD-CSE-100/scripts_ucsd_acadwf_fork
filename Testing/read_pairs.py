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

with open("../" + config.getPairsFile(), 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID']] = line['Partner2_GithubID']
        pairs[line['Partner2_GithubID']] = line['Partner1_GithubID']

count = 0
with open("../" + config.get) as studentsFile:
    student_reader = csv.DictReader(studentsFile)
    for line in student_reader:
        if line['github userid'] in pairs:
            print "{} {} is in a pair!".format(line['First Name'], line['Last Name']) 
            count += 1

print "There were {0} pairs!".format(count/2)