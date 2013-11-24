#!/usr/bin/python

#needed globally
import subprocess

def check_pairs(students, pairs):
    completed = []
    count = 0
    for student in students.keys():
        if student in pairs and student not in completed:
            print "{0} is in a pair with {1}".format(students[student], students[pairs[student]])
            count+=1
            completed.extend([student, pairs[student]])

    print "There are {0} pairs and {1} students".format(len(pairs)/2, len(students))
    print "Traversal found {0} pairs! Matches actual? {1}".format(count, count==len(pairs)/2)

def repo_exists(project, gh_id, gh_id2=None):
    repo_name = "git@github.com:UCSD-CSE-100/{0}_{1}.git".format(project, gh_id)
    if gh_id2 != None:
        repo_name = "git@github.com:UCSD-CSE-100/{0}_Pair_{1}_{2}.git".format(project, gh_id, gh_id2) 
    repo_proc  = subprocess.Popen(["git", "ls-remote", repo_name, "&> /dev/null"],
                                  stderr = subprocess.PIPE)
    repo_state = repo_proc.wait()
    return (repo_state == 0)
    
def check_pairs(students, pairs):
    completed = []
    for student in students.keys():
        if (student in pairs) and (student not in completed):
            if repo_exists("P4", student, pairs[student]):
                print "Repo name is {0}_Pair_{1}_{2}".format("P4", student, pair[student])
            else
                print "Repo name is {0}_Pair_{1}_{2}".format("P4", pair[student], student)
            completed.extend([student, pairs[student]])

def check_repos(students, pairs):
    completed = [ ]
    count = 0
    for student in students.keys():
        #Pair repository
        if (student in pairs) and (student not in completed):
            student_two = pairs[student]
            if not repo_exists("P4", student):
                print "Error! {0} does not have a repository".format(students[student])
                count+=1
            if not repo_exists("P4", student_two):
                print "Error! {0} does not have a repository".format(students[student_two])
                count+=1
            completed.extend([student, student_two])
        #solo repository
        else:
            if not repo_exists("P4", student):
                print "Error! {0} does not have a repository".format(students[student])
                count +=1
            completed.append(student)
    
    if count == 0:
        print "All repositories accounted for!"
    
import csv
import os
import sys
import random


sys.path.append("../PyGithub")
sys.path.append("..")

import config
pairs = {}
students = {}

#add all pairs to a dict, put in twice to map both ways
with open("../" + config.getPairsFile(), 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID'].lower()] = line['Partner2_GithubID'].lower()
        pairs[line['Partner2_GithubID'].lower()] = line['Partner1_GithubID'].lower()

#add all students to a dict
with open("../" + config.getStudentsFile()) as studentsFile:
    student_reader = csv.DictReader(studentsFile)
    for line in student_reader:
        students[line['github userid'].lower()] = line['First Name'] + " " + line['Last Name']

#check_pairs(students, pairs)
check_repos(students, pairs)

sys.exit(0)
