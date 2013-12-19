#!/usr/bin/env python

""" Module: pullstudents
    Author: Arden Liao (ardentsonata)

    This module is to be used in conjuction with the Professor Conrad's github
    scripts, and is used to pull repositories for grading.

    Arguments:
        labno date time
        -h :    Brings up a help guide for the arguments
        -d :    --checkpt_date set the due date for a checkpoint
        -t :    --checkpt_time set the due time for a checkpoint
        -i :    --infilename pull students from an infile
        -p :    --pairfilename use pairs from a specified file
        --debug: output goes to a debug file
"""

import csv
import glob
import os
import random
import subprocess
import sys
import zipfile

sys.path.append("..")
sys.path.append("../utility")
import argparse
import config
import getclass

CSV_STRING   = "{0},{1} {2},{3},{4}\n" #Tutor,Student Name, Github ID, Pair
CURR_STUDENT = "Current student is {0} {1}" #First Name, Last Name

def main():
    """ Main driver for the script  """
    args            = parse_args()
    lab             = args.labno
    due_date_time   = (args.date, args.time)
    chk_date_time   = (args.checkpt_date, args.chkpt_time)

    submissions_dir = config.getLabSubmissionsDir()
    class_tutors    = config.getTutors()
    class_pairs     = getclass.get_pairs(args.pair_fn)
    class_students  = getclass.get_students(args.students_fn)

    clean_dir(submissions_dir)
    tutor_csvs = create_csvs(submissions_dir, class_tutors)
    dbg_log    = open_dbglog(args.dbg, submissions_dir)

    if(args.infile_name != None):
        pull_from_file(infile=args.infile_name, pairs=class_pairs,
                       tutors=class_tutors, csvs=tutor_csvs, labno=lab,
                       due=due_date_time, chk=chk_date_time)
    else:
        pull_all_students(students=class_students, pairs=class_pairs,
                          tutors=class_tutors, csvs=tutor_csvs, labno=lab,
                          due=due_date_time, chk=chk_date_time)

    #Close all open file handles
    dbg_log.close()
    for csv_file in tutor_csvs.values():
        csv_file.close()


def pull_from_file(**kwargs):
    """ Pull all student submissions that are in the infile

        Parameters: infile, pairs, tutors, csvs, labo
    """
    completed  = []
    count      = 0
    num_tutors = len(kwargs['tutors'])
    with open(kwargs['infile'], 'rb') as tb_pulled:
        pull_reader = csv.DictReader(tb_pulled)
        for line in pull_reader:
            if count % num_tutors == 0:
                random.shuffle(kwargs['tutors'])
                count = 0
            curr_tutor = kwargs['tutors'][count]
            student = line['GithubId'].lower()
            if student not in completed:
                added = (student, curr_tutor)
                if len(added) != 0:
                    completed.extend(added)
                    count += 1


def pull_all_students(**kwargs):
    """ Pull all student submissions

        Parameters: students, pairs, tutors, csvs, labno
    """
    completed  = []
    count      = 0
    num_tutors = len(kwargs['tutors'])
    for student in kwargs['students'].keys():
        if student not in completed:
            continue

        print CURR_STUDENT.format(kwargs['students'][student][0],
                                  kwargs['students'][student][1])
        if count % num_tutors == 0:
            random.shuffle(kwargs['tutors'])
            count = 0
        curr_tutor = kwargs['tutors'][count]
        added = (student, curr_tutor)
        if len(added) != 0:
            completed.extend(added)
            count += 1


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


def zip_csvs(directory):
    """ Zip tutor csvs with their respective zip bundles  """
    os.chdir(directory)
    zipped_csvs = zip(glob.glob("*.zip"), glob.glob ("*.csv"))
    for tutor in zipped_csvs:
        zip_file = zipfile.ZipFile(tutor[0], 'a')
        zip_file.write(tutor[1])
        zip_file.close()

if __name__ == '__main__':
    main()
    sys.exit(0)
