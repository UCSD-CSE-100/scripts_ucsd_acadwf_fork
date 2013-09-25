#!/usr/bin/python3

# This is just a super simple example script of how to process the data
# in the CSV that results from exporting the Google Form.

# It doesn't actually do anything except print out a few fields, just
# as an illustration/proof-of-concept.

import csv

filename =  '../CS56-S13-data/CS56 S13 Github Userids (Responses) - Form Responses.csv'

def processLine(lastName,githubUser):
    print("Last Name: ",lastName,end='');
    print(" github userid:: ",githubUser);
   

with open(filename,'r',newline='') as f:
    csvFile = csv.DictReader(f,delimiter=',', quotechar='"')
    for line in csvFile:
        processLine(line["Last Name"],line["github userid"])

