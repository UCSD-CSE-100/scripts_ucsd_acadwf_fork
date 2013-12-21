#!/usr/bin/env python

""" Python module for deleting student teams
    Author: Arden Liao (ardentsoanta)
"""

#Python STL
import logging
import subprocess

#External Libraries
try:
    import requests
except:
    logging.info("\'requests module\' not installed on this system")

#importing user defined libraries
sys.path.append("..")
import argparse

GET_TEAMS   = "https://api.github.com/orgs/{_org}/teams"
DELETE_TEAM = "https://api.github.com/teams/{_id}"
