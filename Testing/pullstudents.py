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

import glob
import logging
import os
import random
import sys
import zipfile

sys.path.append("..")
sys.path.append("../utility")
import argparse
import academicclass
import config
import pullrepo

CSV_STRING   = "{0},{1} {2},{3},{4}\n" #Tutor,Student Name, Github ID, Pair
CURR_STUDENT = "Current student is {name}"

def main():
    """ Main driver for the script  """
    args            = parse_args()
    lab             = args.labno
    due_date_time   = (args.date, args.time)
    chk_date_time   = (args.checkpt_date, args.checkpt_time)

    submissions_dir = config.getLabSubmissionsDir()
    class_tutors    = config.getTutors()
    class_students  = academicclass.Class(args.students_fn, args.pair_fn,
                                          config.getOrgName())
    # class_pairs     = getclass.get_pairs(args.pair_fn)
    # class_students  = getclass.get_students(args.students_fn)

    clean_dir(submissions_dir)
    tutor_csvs = create_csvs(submissions_dir, class_tutors)
    dbg_log    = open_dbglog(args.dbg, submissions_dir)

    if(args.infile_name != None):
        logging.info("Currently not supported")
    else:
        pull_all_students(acad_class=class_students, tutors=class_tutors,
                          csvs=tutor_csvs, labno=lab, due=due_date_time,
                          chk=chk_date_time, log=dbg_log)

    #Close all open file handles
    dbg_log.close()
    for csv_file in tutor_csvs.values():
        csv_file.close()


def pull_all_students(**kwargs):
    """ Pull all student submissions

        Parameters: students, pairs, tutors, csvs, labno
    """
    completed  = []
    count      = 0
    num_tutors = len(kwargs['tutors'])
    acad_class = kwargs['acad_class']
    info = {'labno': kwargs['labno'], 'tutor': None, 'csvs': kwargs['csvs'],
            'due_date': kwargs['due'], 'chkpoint': kwargs['chk'],
            'org': acad_class.org, 'debug': kwargs['log']}

    #Pull pairs first
    for pair in acad_class.pairs:
        if (count == 0):
            random.shuffle(kwargs['tutors'])

        info['tutor'] = kwargs['tutors'][count]
        print CURR_STUDENT.format(pair[0].name)
        print CURR_STUDENT.format(pair[1].name)

        added = check_pair(pair, info)
        if len(added) > 0:
            completed.extend(added)
            count = (count + 1) % num_tutors

    for student in kwargs['students'].students:
        if student not in completed:
            continue
        if (count == 0):
            random.shuffle(kwargs['tutors'])

        info['tutor'] = kwargs['tutors'][count]
        print CURR_STUDENT.format(student.name[0], student.name[1])

        added = check_solo(student, info)
        if len(added) != 0:
            completed.extend(added)
            count = (count + 1) % num_tutors

def check_pair(pair, info):
    """ Pulls a Student pair for grading  """
    added = []
    curr_csv = info['csvs'][info['tutor']]

    # Check if the pair worked separately
    for student in pair:
        if (pullrepo.pull_repo(info, student=student)):
            write_csv(curr_csv, info['tutor'], student, "SOLO-P")
            added.append(student)

    # Pull the pair repository
    if (pullrepo.pull_repo(info, pair=pair)):
        for student in pair:
            write_csv(curr_csv, info['tutor'], student, "PAIR")
        added = [pair[0], pair[1]]

    return added

def check_solo(student, info):
    """ Pulls a Student solo submission for grading  """
    added = []
    curr_csv = info['csvs'][info['tutor']]

    if (pullrepo.pull_repo(info, student=student)):
        write_csv(curr_csv, info['tutor'], student, "SOLO")
        added = [student]

    return added

def write_csv(csv, tutor, student, type_repo):
    """ Writes CSV string to tutor's csv for specified student  """
    csv.write(CSV_STRING.format(tutor, student.name, student.ghid, type_repo))

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
            logging.critical("Could not open csv file for " + tutor)
            sys.exit(1)
    return temp


def open_dbglog(open_log, directory):
    """ Creates a debug log if debug flag is specified  """
    if(open_log):
        try:
            return open(directory + 'git_debug_log', 'wb')
        except IOError:
            logging.critical("Could not open file \'git_debug_log\'")
            sys.exit(1)
    else:
        try:
            return open('/dev/null', 'w')
        except IOError:
            logging.critical("Could not open \'/dev/null\'")
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
    """ Recursively removes all files from a directory """
    for file_name in os.listdir(directory):
        path = directory + file_name
        if (os.path.isdir(path)):
            clean_dir(path)
            os.rmdir(path)
        else:
            os.remove(path)


def zip_csvs(directory):
    """ Zip tutor csvs with their respective zip bundles  """
    os.chdir(directory)
    zipped_csvs = zip(glob.glob("*.zip"), glob.glob ("*.csv"))
    for tutor in zipped_csvs:
        zip_file = zipfile.ZipFile(tutor[0], 'a')
        zip_file.write(tutor[1])
        zip_file.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    main()
    sys.exit(0)

