#!/usr/bin/env python

""" Python module for retrieving student information  """

import csv
import sys

def get_pairs(infile):
    """ Retrieves a dictionary of student pairs

        Key   = githubid of student
        Value = githubid of partner
    """
    temp = {}
    try:
        with open(infile, 'rb') as pairfile:
            pair_reader = csv.DictReader(pairfile)
            for line in pair_reader:
                temp[line['Partner1_GithubID'].lower()] =\
                line['Partner2_GithubID'].lower()
    except IOError:
        print("Could not open pair file for reading.\n")
        sys.exit(1)
    return temp

def get_students(infile):
    """ Retrieves a dictionary of students

        Key   = githubid of student
        Value = tuple of (First name, Last name)
    """
    temp = {}
    try:
        with open(infile, 'rb') as studentsfile:
            pair_reader = csv.DictReader(studentsfile)
            for line in pair_reader:
                temp[line['github userid'].lower()] =\
                (line['First Name'], line['Last Name'])
    except IOError:
        print ("Could not open students list for leading.\n")
        sys.exit(1)
    return temp

