#!/usr/bin/python

def check_pairs(students, pairs):
    completed = []
    count = 0;
    for student in students.keys():
        if student in pairs and student not in completed:
            print "{0} is in a pair with {1}".format(students[student], students[pairs[student]])
            count+=1
            completed.extend([student, pairs[student]])

    print "There are {0} pairs and {1} students".format(len(pairs)/2, len(students))
    print "Traversal found {0} pairs! Matches actual? {1}".format(count, count==len(pairs)/2)




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

#add all pairs to a dict, put in twice to map both ways
with open("../" + config.getPairsFile(), 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID']] = line['Partner2_GithubID']
        pairs[line['Partner2_GithubID']] = line['Partner1_GithubID']

#add all students to a dict
with open("../" + config.getStudentsFile()) as studentsFile:
    student_reader = csv.DictReader(studentsFile)
    for line in student_reader:
        students[line['github userid'].lower()] = line['First Name'] + " " + line['Last Name']

check_pairs(students, pairs)

sys.exit(0)