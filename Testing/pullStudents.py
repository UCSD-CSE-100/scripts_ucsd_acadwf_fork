#!/usr/bin/env python

import subprocess
import os
import sys
import random
import csv
import zipfile
import re

sys.path.append("..")
import config
import argparse

CSV_STRING   = "{0},{1} {2},{3},{4}\n" #Tutor,Student Name, Github ID, Pair
CURR_STUDENT = "Current student is {0} {1}"

def main():
    """ Main driver for the script  """
    args        = parse_args()
    lab         = args.labno
    due_date    = args.date
    due_time    = args.time
    chk_time    = args.checkpt_date
    chk_time    = args.checkpt_time
    count       = 0

    submissions_dir = config.getLabSubmissionsDir()
    tutors          = config.getTutors()
    pairs           = get_pairs(args.pair_fn)
    students        = get_students(args.students_fn)

    clean_dir(submissions_dir)
    tutor_csvs = create_csvs(submissions_dir, tutors)
    dbg_log    = open_dbglog(args.dbg, submissions_dir)

    if(args.infile_name != None):
        pull_from_file(args.infile_name, pairs, tutors, tutor_csvs)
    else:
        pull_all_students(students, pairs, tutors, tutor_csvs)

    #Close all open file handles
    dbg_log.close()
    for csv_file in tutor_csvs.values():
        csv_file.close()


def pull_from_file(infile, pairs, tutors, csvs):
    """ Pull all student submissions that are in the infile

        Parameters: infile, pairs, tutors, csvs, labo
    """
    completed  = []
    count      = 0
    num_tutors = len(tutors)
    with open(infile, 'rb') as tb_pulled:
        pull_reader = csv.DictReader(tb_pulled)
        for line in pull_reader:
            if count % num_tutors == 0:
                random.shuffle(tutors)
                count = 0
            curr_tutor = tutors[count]
            student = line['GithubId'].lower()
            if student not in completed:
                added = (student, curr_tutor)
                if len(added) != 0:
                    completed.extend(added)
                    count += 1


def pull_all_students(students, pairs, tutors, csvs):
    """ Pull all student submissions

        Parameters: students, pairs, tutors, csvs, labno
    """
    completed  = []
    count      = 0
    num_tutors = len(tutors)
    for student in students.keys():
        if student not in completed:
            continue

        print CURR_STUDENT.format(students[student][0], students[student][1])
        if count % num_tutors == 0:
            random.shuffle(tutors)
            count = 0
        curr_tutor = tutors[count]
        added = (student, curr_tutor)
        if len(added) != 0:
            completed.extend(added)
            count += 1


def get_pairs(infile):
    """ Parses pairs from an infile

        Returns a dictionary of pairs, with the first pair github id
                as the key
    """
    temp = {}
    try:
        with open(infile, 'rb') as pairfile:
            pair_reader = csv.DictReader(pairfile)
            for line in pair_reader:
                temp[line['Partner1_GithubID'].lower()] =\
                line['Partner2_GithubID'].lower()
    except IOError:
        print("Could not open pair file list for reading\n\
               Attempting to continue...")
    return temp

def get_students(infile):
    """ Parses students from an infile

        Returns a dictionary of tuples (First Name, Last Name)
                with the student's github id as the key
    """
    temp = {}
    try:
        with open(infile, 'rb') as studentsfile:
            student_reader = csv.DictReader(studentsfile)
            for line in student_reader:
                temp[line['github userid'].lower()] =\
                (line['First Name'], line['Line Name'])
    except IOError:
        print("Could not open students list for reading\n")
        sys.exit(1)
    return temp


def create_csvs(directory, tutors):
    """ Creates new CSV files for each tutor

        Returns a dictionary of file descriptors with the tutor name as the key
    """
    temp = {}
    for tutor in tutors:
        try:
            temp[tutor] = open (directory + tutor + ".csv", 'wb')
            temp[tutor].write("Tutor,Student,Github ID, Pair\n")
        except IOError:
            print("Could not open csv file for " + tutor)
            sys.exit(1)
    return temp


def open_dbglog(open_log, directory):
    """ Creates a debug log if debug flag is specified  """
    if(open_log):
        try:
            return open(directory + 'git_debug_log', 'wb')
        except IOError:
            print("Could not open file \'git_debug_log\'")
            sys.exit(1)
    else:
        try:
            return open('/dev/null', 'w')
        except IOError:
            print ("Could not open \'/dev/null\'")
            sys.exit(1)


def parse_args():
    """ Parses the system arguments and returns the arguments  """
    parser = argparse.ArgumentParser(description='Pull students for grading')
    parser.add_argument('labno', help='labno e.g. PA1')
    parser.add_argument('date', help='Due date in YYYY-MM-DD format')
    parser.add_argument('time', help='Due Time in 24-Hour HH:MM format')
    parser.add_argument('-d', '--checkpt_date',
                        help='Checkpoint date YYYY-MM-DD format',
                        default=None)
    parser.add_argument('-t', '--checkpt_time',
                        help='Checkpoint date HH:MM format',
                        default=None)
    parser.add_argument('-i', '--infile_name',
                        help='Input file for pulling (default: None)',
                        default=None)
    parser.add_argument('-p', '--pair_fn',
                        help='input file (default: '+config.getPairsFile()+')',
                        default=config.getPairsFile())
    parser.add_argument('-s', '--students_fn',
                        help='input file (default: '+config.getStudentsFile()\
                             +')', default=config.getStudentsFile())
    parser.add_argument('--debug', dest='dbg', action='store_true',
                        help='Enable debug output to a log file',
                        default=False)
    return parser.parse_args()

def clean_dir(directory):
    """ Removes all files from a directory
        Note: Does not work on directories with directories in them
    """
    for file_name in os.listdir(directory):
        os.remove(directory + file_name)


if __name__ == '__main__':
    main()
    sys.exit(0)
