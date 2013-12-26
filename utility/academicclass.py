""" Python module for a class
    Author: Arden Liao
"""

import csv
import logging
import sys

class Student(object):
    """ Student class

        Instance Variables:
            name - String = "First Name Last Name"
            ghid - String = "GithubID"
    """

    def __init__(self, name, ghid):
        self.__name = name
        self.__ghid = ghid

    # Getter defines for instance variables
    @property
    def name(self):
        """ Returns name of Student  """
        return self.__name

    @property
    def ghid(self):
        """ Returns Github ID of Student """
        return self.__ghid

    # Setter defines for instance variables
    @name.setter
    def name(self, value):
        """ Sets the name to specified value  """
        self.__name = value

    @ghid.setter
    def ghid(self, value):
        """ Sets the Github ID to the specified value  """
        self.__ghid = value


class Class(object):
    """ Class class

        Instance Variables:
            students - List of Students in a Class
            pairs    - Dict of Student pairs in a Class
    """

    def __init__(self, student_list, pair_list, org):
        self.__students = []
        self.__pairs    = []
        self.__org      = org
        self.__get_students__(student_list)
        self.__get_pairs__(pair_list)

    def __get_students__(self, infile):
        """ Parses CSV and sets the list of students  """
        try:
            with open(infile, 'rb') as students_list:
                student_reader = csv.DictReader(students_list)
                for line in student_reader:
                    ghid = line['github userid'].lower()
                    name = line['First Name'] + " " + line['Last Name']
                    self.__students.append(Student(name, ghid))
        except IOError:
            logging.error("Could not open student list for reading")
            sys.exit(1)

    def __get_pairs__(self, infile):
        """ Parses CSV and sets the dict of pairs  """
        try:
            with open(infile, 'rb') as pairs_list:
                pair_reader = csv.DictReader(pairs_list)
                for line in pair_reader:
                    ghid1 = line['Partner1_GithubID'].lower()
                    ghid2 = line['Partner2_GithubID'].lower()
                    student1 = self.__get_student__(ghid1)
                    student2 = self.__get_student__(ghid2)
                    self.__pairs.append(student1, student2)

        except IOError:
            logging.error("Could not open pair list for reading")
            sys.exit(1)

    def __get_student__(self, ghid):
        """ Finds a Student based on ghid

            Returns: Student found
        """
        for student in self.__students:
            if(student.ghid == ghid):
                return student

    # Getter method for instance variables
    @property
    def students(self):
        """ Returns the list of students in this class """
        return self.__students

    @property
    def pairs(self):
        """ Returns the dictionary of pairs in this class  """
        return self.__pairs

    @property
    def org(self):
        """ Returns the org name string of this class """
        return self.__org

    # Setter methods for instance variables
    @students.setter
    def students(self, value):
        """ Sets the students to specified value  """
        if type(value) is not list:
            raise TypeError
        self.__students = value

    @pairs.setter
    def pairs(self, value):
        """ Sets the pairs to the specified value  """
        if type(value) is not list:
            raise TypeError
        self.__pairs = value

    @org.setter
    def org(self, value):
        """ Sets the org to be the specified value """
        if type(value) is not str:
            raise TypeError
        self.__org = value
