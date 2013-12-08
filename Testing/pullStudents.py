#!/usr/bin/env python

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
    if not check_repo(pair_url):
        pair_name = "{0}_Pair_{1}_{2}".format(project, gh_id2, gh_id)
        pair_url = "git@github.com:UCSD-CSE-100/" + pair_name + ".git"
    
    args = []
    if(chk_time is not None):
        args = ['./pullRepo.sh', pair_name, pair_url, tutor, lab,
                due_date, due_time, chk_date, chk_time]
    else:
        args = ['./pullRepo.sh', pair_name, pair_url, tutor, lab,
                due_date, due_time]

    repo_proc = subprocess.Popen(args, stderr=dbg_log)

    return (repo_proc.wait() == 0)

def pull_solo(project, gh_id, tutor):
    repo_name = "{0}_{1}".format(project, gh_id)
    repo_url  = "git@github.com:UCSD-CSE-100/" + repo_name + ".git"
    args = []
    if (chk_time is not None):
        args = ['./pullRepo.sh', repo_name, repo_url, tutor, lab,
                due_date, due_time, chk_date, chk_time]
    else:
        args = ['./pullRepo.sh', repo_name, repo_url, tutor, lab,
                due_date, due_time]

    repo_proc = subprocess.Popen(args, stderr=dbg_log)
    
    return (repo_proc.wait() == 0)

def check_student(student, tutor):
    added = [];
    if student in pairs.keys():
        print "Current student is {0} {1}".format(students[pairs[student]][0], students[pairs[student]][1])
        
        #See if they need to be pulled separately
        if( pull_solo(lab, student, tutor) ):
            f_name0 = students[student][0]
            l_name0 = students[student][1]
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student,'SOLO-P'))
            added.append(student);
        if( pull_solo(lab, pairs[student], tutor) ):
            f_name0 = students[pairs[student]][0]
            l_name0 = students[pairs[student]][1]
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student, 'SOLO-P'))
            added.append(pairs[student]);
        if( pull_pair(lab, student, pairs[student], tutor) ):
            f_name0 = students[student][0]
            l_name0 = students[student][1]
            f_name1 = students[pairs[student]][0]
            l_name1 = students[pairs[student]][1]
            
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student,'PAIR'))
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name1, l_name1, pairs[student],'PAIR'))
           
            added = [student, pairs[student]]
    # Solo Case
    elif student not in pairs.values():
        if( pull_solo(lab, student, tutor) ):
            f_name0 = students[student][0]
            l_name0 = students[student][1]
            tutor_csvs[tutor].write(csv_str.format(tutor, f_name0, l_name0, student, 'SOLO'))
            added = [student]

    return added        

import random, csv, sys, os
import zipfile, re
sys.path.append("..");
import config, argparse

parser = argparse.ArgumentParser(description='Pull Students for grading')
parser.add_argument('prefix', help='prefix e.g. PA1')
parser.add_argument('date', help='Due Date in YYYY-MM-DD format')
parser.add_argument('time', help='Due Time in 24-Hour HH:MM format')
parser.add_argument('-d', '--checkpt_date',
                    help='Checkpoint date YYYY-MM-DD format',
                    default=None)
parser.add_argument('-t', '--checkpt_time',
                    help='Checkpoint date YYYY-MM-DD format',
                    default=None)
parser.add_argument('-i','--infileName',
                    help='input file (default: None)',
                    default=None)
parser.add_argument('-p','--pairfileName',
                    help='input file (default: '+config.getPairsFile()+ ')',
                    default=config.getPairsFile())
parser.add_argument('--debug', dest='dbg', action='store_true', 
                    help='Enables debug output to a log file',
                    default=False)

#Initialize the variables
args      = parser.parse_args()
lab       = args.prefix
tutors    = config.getTutors()
numTutors = len(tutors)
due_date  = args.date
due_time  = args.time
chk_date  = args.checkpt_date
chk_time  = args.checkpt_time
count     = 0
dbg_log   = None

submissions_dir = config.getLabSubmissionsDir()
pairs    = {}
students = {}

#setup debug logs
if(args.dbg):
    try:
        dbg_log = open('git_debug_log', 'wb')
    except IOError:
        print("Could not open file \'git_debug_log\'")
        sys.exit(1)
else:
    try:
        dbg_log = open('/dev/null', 'w')
    except IOError:
        print("Could not open /dev/null")
        sys.exit(1)

#set up pairs
try:
    with open(args.pairfileName, 'rb') as pairFile:
        pair_reader = csv.DictReader(pairFile)
        for line in pair_reader:
            pairs[line['Partner1_GithubID'].lower()] = line['Partner2_GithubID'].lower()
except IOError:
    print("Could not open pair file list for reading\nAttempting to continue...")

#set up students
try:
    with open(config.getStudentsFile(), 'rb') as studentsFile:
        student_reader = csv.DictReader(studentsFile)
        for line in student_reader:
            students[line['github userid'].lower()] = (line['First Name'], line['Last Name'])
except IOError:
    print("Could not open students list for reading")
    sys.exit(1)
    
#clean out submissions dir
for file in os.listdir(submissions_dir):
    os.remove(submissions_dir + file)

#create clean csvs
tutor_csvs = {}
for tutor in tutors:
    try:
        tutor_csvs[tutor] = open(submissions_dir + tutor + ".csv", 'wb')
        tutor_csvs[tutor].write("Tutor,Student,Github ID,Pair\n")
    except IOError:
        print("Could not open csv file for " + tutor)
        sys.exit(0)

completed = []
csv_str   = "{0},{1} {2},{3},{4}\n" #Tutor,Student Name,Github ID,Pair
if(args.infileName != None):
    with open(args.infileName, 'rb') as tb_pulled:
        pull_reader = csv.DictReader(tb_pulled)
        for line in pull_reader:
            if count%numTutors  == 0:
                random.shuffle(tutors)
                count = 0
            curr_tutor = tutors[count]
            student = line['GithubId'].lower()
            if student not in completed:
                added = check_student(student, curr_tutor)
                if len(added) != 0:
                    completed.extend(added)
                    count +=1

else:
    for student in students.keys():
        print "Current student is {0} {1}".format(students[student][0], students[student][1])
        if count%8  == 0:
            random.shuffle(tutors)
            count = 0
        curr_tutor = tutors[count]
        if student not in completed:
            added = check_student(student, curr_tutor)
            if len(added) != 0:
                completed.extend(added)
                count+=1
        print

not_pulled = list(set(completed) ^ set(students.keys()))
with open(submissions_dir+"not_worked", 'wb') as not_worked:
    for student in not_pulled:
        not_worked.write("Not pulled: {name} - {gid}\n".format(
                         name = students[student][0] + students[student][1],
                         gid = student))

#Close all open file handles
dgb_log.close()
for csv in tutor_csvs.values():
    csv.close()

#Zip the CSVs with the zips
os.chdir(submissions_dir)
dir_files = os.listdir(os.getcwd())
zips = sorted([x for x in dir_files if(re.match('.*\.zip', x))])
csvs = sorted([x for x in dir_files if(re.match('.*\.csv', x))])
zip_csvs = zip(zips, csvs)
for tutor in zip_csvs:
    zip_file = zipfile.ZipFile(tutor[0], 'a')
    zip_file.write(tutor[1])
    zip_file.close()

sys.exit(0)
