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
    pair_name = "{0}_Pair_{1}_{2}".format(project, gh_id, gh_id2)
    pair_url  = "git@github.com:UCSD-CSE-100/" + pair_name + ".git"
    if check_repo(pair_url):
#        repo_proc = subprocess.Popen(['./pullRepo.sh',
#                                      pair_name,
#                                      pair_url,
#                                      tutor])
        proc_state = 0#repo_proc.wait()
    else:
        pair_name = "{0}_Pair_{1}_{2}.git".format(project, gh_id2, gh_id)
        pair_url = "git@github.com:UCSD-CSE-100/" + pair_name + ".git"
#        repo_proc = subprocess.Popen(['./pullRepo.sh',
#                                      pair_name,
#                                      pair_url,
#                                      tutor])
#        proc_state = repo_proc.wait()
    return False #(proc_state == 0)

def pull_solo(project, gh_id, tutor):
    repo_name = "{0}_{1}".format(project, gh_id)
    repo_url  = "git@github.com:UCSD-CSE-100/" + repo_name + ".git"
    
    repo_proc = subprocess.Popen(['./../Grading/pullRepo.sh',
                                 repo_name,
                                 repo_url,
                                 tutor])
    
    return (repo_proc.wait() == 0)

def check_student(student, pairs, students, csv_str, tutor_csvs, curr_tutor):
    added = [];
    if student in pairs.keys():
        print "Current student is {0} {1}".format(students[pairs[student]][0], students[pairs[student]][1])
        if( pull_pair(lab, student, pairs[student], curr_tutor) ):
            count += 1
            f_name0 = students[student][0]
            l_name0 = students[student][1]
            f_name1 = students[pairs[student]][0]
            l_name1 = students[pairs[student]][1]
            
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student,'YES'))
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name1, l_name1, student,'YES'))
           
            added = [student, pairs[student]]
    # Solo Case
    else:
        if( pull_solo(lab, student, curr_tutor) ):
            count += 1
            f_name0 = students[student][0]
            l_name0 = students[student][1]
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student, 'NO'))
            added = [student]

    return added        

import random
import csv
import sys
sys.path.append("..");
import config
import argparse

parser = argparse.ArgumentParser(description='Pull Students for grading')
parser.add_argument('prefix', help='prefix e.g. PA1')
parser.add_argument('-i','--infileName',
                    help='input file (default: None)',
                    default=None)
parser.add_argument('-p','--pairfileName',
                    help='input file (default: '+config.getPairsFile()+ ')',
                    default=config.getPairsFile())
                    
#Initialize the variables
args      = parser.parse_args()
lab       = args.prefix
tutors    = config.getTutors()
numTutors = len(tutors)
count     = 0

submissions_dir = config.getLabSubmissionsDir()
pairs    = {}
students = {}

#set up pairs
with open(args.pairfileName, 'rb') as pairFile:
    pair_reader = csv.DictReader(pairFile)
    for line in pair_reader:
        pairs[line['Partner1_GithubID'].lower()] = line['Partner2_GithubID'].lower()
        pairs[line['Partner2_GithubID'].lower()] = line['Partner1_GithubID'].lower()

#set up students
with open(config.getStudentsFile(), 'rb') as studentsFile:
    student_reader = csv.DictReader(studentsFile)
    for line in student_reader:
        students[line['github userid'].lower()] = (line['First Name'], line['Last Name'])

#clean out submissions dir
proc = subprocess.Popen(['rm', '-rf', submissions_dir+'*'])
proc.wait()

tutor_csvs = {}
for tutor in tutors:
    tutor_csvs[tutor] = open(submissions_dir + tutor + ".csv", 'wb')
    tutor_csvs[tutor].write("Tutor,Student,Github ID,Pair\n")

completed = []
csv_str   = "{0},{1} {2},{3},{4}\n" #Tutor,Student Name,Github ID,Pair
if(args.infileName != None):
    with open(args.infileName, 'rb') as tb_pulled:
        pull_reader = csv.DictReader(tb_pulled)
        for line in pull_reader:
            if count%8  == 0:
                random.shuffle(tutors)
                count = 0
            curr_tutor = tutors[count]
            student = line['GithubId'].lower()
            if student not in completed:
                added = check_student(student, pairs, students, csv_str, tutor_csvs, curr_tutor)
                if added != None:
                    completed.extends(added)
else:
    for student in students.keys():
        print "Current student is {0} {1}".format(students[student][0], students[student][1])
        if count%8  == 0:
            random.shuffle(tutors)
            count = 0
        curr_tutor = tutors[count]
        if student not in completed:
            added = check_student(student, pairs, students, csv_str, tutor_csvs, curr_tutor)
            if added != None:
                completed.extends(added)
        print
    
#Close all open file handles
for csv in tutor_csvs.values():
    csv.close()

sys.exit(0)
