# sample_config.py contains basic defines for locations of repository 
# information as well as presets for organizations and input files.
# TODO: Make this into a python object, for now just use globals
# TODO: Please copy or rename this file as config.py with your own custom settings
#       for use with the scripts

#Python globals
students          = "test1.csv"
pairs             = "pairs.csv"
org               = "UCSD-CSE-100"
scratchRepoDir    = "/home/linux/ieng6/cs100e/USER/scratchRepos/"
prototypesDir     = "/home/linux/ieng6/cs100e/public/"
labSubmissionsDir = "/home/linux/ieng6/cs100e/USER/labSubmissions/"

currQuarter       = "FALL 2013"
currClass         = "CSE 100"
classWebsite      = "https://sites.google.com/a/eng.ucsd.edu/cse-100-fall-2013/"

#see https://github.com/github/gitignore for all possible languages
projLang          = "C++"

#Shell Script Globals
scriptsLogsDir    = "/home/linux/ieng6/cs100e/USER/scriptLogs/"

#List of current tutors
tutors            = ["tutor_0", "tutor_1", "tutor_2", "tutor_3", "tutor_4", "tutor_5", "tutor_6", "tutor_7"]

''' Python Config calls '''
def getStudentsFile():
    return students

def getPairsFile():
    return pairs

def getOrgName():
    return org

def getScratchRepoDir():
    return scratchRepoDir
	
def getPrototypeDir():
    return prototypesDir
	
def getLabSubmissionsDir():
    return labSubmissionsDir
	
def getCurrentQuarter():
    return currQuarter

def getCurrentClass():
    return currClass
	
def getClassWebsite():
    return classWebsite

def getProjLang():
    return projLang
	
''' Shell Script Config Calls '''
def getScriptsLogsDir():
    return scriptsLogsDir

''' Returns a list of tuples of tutors and their tar files for distribution '''
def getTutors():
    return tutors;

