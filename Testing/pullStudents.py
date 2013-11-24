#!/usr/bin/python

import subprocess

#TODO: Come up with a better solution for checking if a repo exists
def repo_exists(project=None, gh_id=None, gh_id2=None, repo=None):
    repo_name = "git@github.com:UCSD-CSE-100/{0}_{1}.git".format(project, gh_id)
    if gh_id2 != None:
        repo_name = "git@github.com:UCSD-CSE-100/{0}_Pair_{1}_{2}.git".format(project, gh_id, gh_id2) 
    repo_proc  = subprocess.Popen(["git", "ls-remote", repo_name, "&> /dev/null"],
                                  stderr = subprocess.PIPE)
    return (repo_proc.wait() == 0)
    
def check_repo(repo_name):
    repo_proc  = subprocess.Popen(["git", "ls-remote", repo_name, "&> /dev/null"],
                                  stderr = subprocess.PIPE)
    return (repo_proc.wait() == 0)

# add repo format strings to config file?
def pull_pair(project, gh_id, gh_id2, tutor):
    proc_state = 0
    pair_name = "{0}_Pair_{1}_{2}.git".format(project, gh_id, gh_id2)
    pair_repo = "git@github.com:UCSD-CSE-100/" + pair_name
    if check_repo(pair_repo):
#        repo_proc = subprocess.Popen(['./pullRepo.sh',
#                                      pair_name,
#                                      pair_repo,
#                                      tutor])
        proc_state = 0#repo_proc.wait()
    else:
        pair_name = "{0}_Pair_{1}_{2}.git".format(project, gh_id2, gh_id)
        pair_repo = "git@github.com:UCSD-CSE-100/" + pair_name
#        repo_proc = subprocess.Popen(['./pullRepo.sh',
#                                      pair_name,
#                                      pair_repo,
#                                      tutor], stdout)
#        proc_state = repo_proc.wait()
    return (proc_state == 0)

def pull_solo(project, gh_id, tutor):
    proc_state = 0
    
    return (proc_state == 0)
    
import random
import csv
import sys
sys.path.append("..");
import config
import argparse

tutors    = config.getTutors()
numTutors = len(tutors)
count     = 0

parser = argparse.ArgumentParser(description='Pull Students for grading')
parser.add_argument('prefix', help='prefix e.g. PA1')

args = parser.parse_args()
lab = args.prefix

submissions_dir = config.getLabSubmissionsDir()
pairs    = {}
students = {}

#set up 
with open(config.getPairsFile(), 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID'].lower()] = line['Partner2_GithubID'].lower()
        pairs[line['Partner2_GithubID'].lower()] = line['Partner1_GithubID'].lower()

with open(config.getStudentsFile(), 'rb') as studentsFile:
    student_reader = csv.DictReader(studentsFile)
    for line in student_reader:
        students[line['github userid'].lower()] = (line['First Name'], line['Last Name'])

proc = subprocess.Popen(['rm', '-rf', submissions_dir+'*'])
proc.wait()

tutor_csvs = {}

for tutor in tutors:
    tutor_csv = open(submissions_dir + tutor, 'ab')
    tutor_csv.write("Tutor,Student,Github ID,Pair")
    tutor_csvs[tutor] = tutor_csv

completed = []
csv_str   = "{0},{1} {2},{3},{4}" #Tutor,Student Name,Github ID,Pair
for student in students.keys():
    print "Current student is {0} {1}".format(students[student][0], students[student][1])
    if count%8  == 0:
        random.shuffle(tutors)
        count = 0
    curr_tutor = tutors[count]
    if student not in completed:
        # Pair Case
        if student in pairs:
            if( pull_pair(lab, student, pairs[student], curr_tutor) ):
                count += 1
                f_name0 = students[student][0]
                l_name0 = students[student][1]
                f_name1 = students[pairs[student]][0]
                l_name1 = students[pairs[student]][1]
                
                tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student, 'YES'))
                tutor_csvs[tutor].write(csv_str.format(tutor, f_name1, l_name1, student,'YES'))
               
                completed.extend([student, pairs[student]])
        # Solo Case
        else:
            if( pull_solo(lab, student, curr_tutor) ):
                count += 1
                f_name0 = students[student][0]
                l_name0 = students[student][1]
                tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student, 'YES'))
                completed.append(student)
    print
    
#Close all open file handles
for csv in tutor_csvs.values():
    csv.close()
