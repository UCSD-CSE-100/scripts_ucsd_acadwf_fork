# sample_config.py contains basic defines for locations of repository 
# information as well as presets for organizations and input files.
# TODO: Make this into a python object, for now just use globals
# TODO: Please copy or rename this file as config.py with your own custom settings
#       for use with the scripts

students          = "test1.csv"
pairs             = "pairs.csv"
org               = "UCSD-CSE-100"
scratchRepoDir    = "/home/linux/ieng6/oce/78/arliao/Github/scratchRepos/"
prototypesDir     = "/home/linux/ieng6/oce/78/arliao/Github/prototypes/"
labSubmissionsDir = "/home/linux/ieng6/oce/78/arliao/Github/labSubmissions"

currQuarter       = "FALL 2013"
currClass         = "CSE 100"
classWebsite      = "https://sites.google.com/a/eng.ucsd.edu/cse-100-fall-2013/"

#see https://github.com/github/gitignore for all possible languages
projLang          = "C++"

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
	