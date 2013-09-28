#!/bin/bash

#initialize PyGithub, unsure why submodule doesn't work, manually clone for now
git clone git@github.com:jacquev6/PyGithub.git

#create the config file
git cp sample_config.py config.py

#intialize the config file values to some default values
#makes the scratch, submission, and logs directories if they don't already exist
#TODO