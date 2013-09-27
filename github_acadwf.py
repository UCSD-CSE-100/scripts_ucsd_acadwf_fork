# github-acadwf.py contains utility functions for 
# working with PyGithub objects to set up teams, and repositories
# and other Github objects for academic workflows.

from __future__ import print_function
import sys

def populateRepo(repo,protoDir,scratchDir):
    import subprocess
    callList = ["./populateRepo.sh",repo.name,repo.ssh_url,protoDir,scratchDir]
    print ("Calling " + " ".join(callList))
    subprocess.call(callList)

def pullRepoForGrading(repo,gradingDir):
    import subprocess
    callList = ["./pullRepoForGrading.sh",repo.name,repo.ssh_url,gradingDir]
    print ("Calling " + " ".join(callList))
    subprocess.call(callList)

def pushFilesToRepo(g,org,lab,firstName,scratchDirName):

    addPyGithubToPath()
    from github import GithubException

    import os

    protoDirName = lab + "_prototype"
    
    # check to see if protoDirName exists.  If not, bail
    
    if (not os.path.isdir(protoDirName)):
        raise Exception(protoDirName + " does not exist.")

    if (not os.path.isdir(scratchDirName)):
        raise Exception(scratchDirName + " does not exist.")

    protoDirName = os.path.abspath(protoDirName)
    scratchDirName = os.path.abspath(scratchDirName)

    if (firstName!=""):
        try:
            repoName = (lab + "_" + firstName)
            repo = org.get_repo(repoName)
            populateRepo(repo,protoDirName,scratchDirName)
        except GithubException as ghe:
            print("Could not find repo " + repoName + ":" + str(ghe))
            
    else:
            
        # User wants to update ALL repos that start with labxx_
        
        repos = org.get_repos()
        for repo in repos:
            if (repo.name.startswith(lab+"_")):
                populateRepo(repo,protoDirName,scratchDirName)
            

def pushFilesToPairRepo(g,org,lab,team,scratchDirName):

    addPyGithubToPath()
    from github import GithubException

    import os

    protoDirName = lab + "_prototype"
    
    # check to see if protoDirName exists.  If not, bail
    
    if (not os.path.isdir(protoDirName)):
        raise Exception(protoDirName + " does not exist.")

    if (not os.path.isdir(scratchDirName)):
        raise Exception(scratchDirName + " does not exist.")

    protoDirName = os.path.abspath(protoDirName)
    scratchDirName = os.path.abspath(scratchDirName)

    
    try:
        repoName = (lab + "_" + team.name)
        repo = org.get_repo(repoName)
        populateRepo(repo,protoDirName,scratchDirName)
    except GithubException as ghe:
        print("Could not find repo " + repoName + ":" + str(ghe))
            



def addPyGithubToPath():
    pathToPyGithub="./PyGithub";
    if not pathToPyGithub in sys.path:
        sys.path.append("./PyGithub")


def addStudentsFromFileToTeams(g,org,infileName):
    
    addPyGithubToPath()
    from disambiguateFunctions import getUserList
    
    userList = getUserList(infileName)
   
    allstudents = findTeam(org, "AllStudents")
    if(allstudents is None):
        allstudents = createTeam(org, "AllStudents")
        if(allstudents is None):
           print("Could not create team AllStudents")
     
    for line in userList:
        studentTeam = addStudentToTeams(g,org,
                          line['last'],
                          line['first'],
                          line['github'],
                          line['email'],
                          line['csil'])

def updateStudentsFromFileForLab(g,org,infileName,lab,scratchDirName,firstName=''):

    """
    firstName='' means updateAllStudents
    """

    addPyGithubToPath()
    from disambiguateFunctions import getUserList
    
    userList = getUserList(infileName)

    for line in userList:
        
        if ( firstName=="" or line['first']==firstName ):
        
            studentTeam = addStudentToTeams(g,org,
                                       line['last'],
                                       line['first'],
                                       line['github'],
                                       line['email'],
                                       line['csil'])
            
            result = createLabRepoForThisUser(g,org,lab,
                                              line['last'],line['first'],
                                              line['github'],
                                              line['email'],line['csil'],
                                              studentTeam)
            
            if (result):
                pushFilesToRepo(g,org,lab,line['first'],scratchDirName)
                
        

def updateAllStudentsFromFileForLab(g,org,infileName,lab,scratchDirName):

    
    addPyGithubToPath()
    from disambiguateFunctions import getUserList
    
    userList = getUserList(infileName)

    for line in userList:
        
        studentTeam = addStudentToTeams(g,org,
                                       line['last'],
                          line['first'],
                          line['github'],
                          line['email'],
                          line['csil'])

        result = createLabRepoForThisUser(g,org,lab,
                                 line['last'],line['first'],line['github'],
                                 line['email'],line['csil'],
                                 studentTeam)
        
        if (result):
            pushFilesToRepo(g,org,lab,line['first'],scratchDirName)


def addUserToTeam(team,user,quiet=False):
    "A wrapper for team.add_to_members(user).  Returns true on success"

    addPyGithubToPath()
    from github import GithubException

    try:
       team.add_to_members(user);
       if not quiet:
           print(
           "user {0} added to {1}...".format( user.login, team.name) , end='')
       return True
    except GithubException as e:
       print (e)
       
    return False


def addStudentToTeams(g,org,lastName,firstName,githubUser,umail,csil):
    """
    return the team if it was created or found, and user is member 
    Otherwise False
    Only creates team and adds if wasn't already on the teams
    """

    print("addStudentToTeams: {0} {1} (github: {2})...".format(
            firstName,lastName,githubUser),end='')

    studentTeam = getStudentFirstNameTeam(org, firstName)

    if (not studentTeam is None):
        print("Team {0} exists...".format(studentTeam.name),end='')
    else:
        studentTeam = createTeam(org,
                                 formatStudentTeamName(firstName))
    

    studentGithubUser = findUser(g,githubUser)
    if (studentGithubUser is None):
        print ("github user {0} for {1} {2} does not exist".format(githubUser,firstName,lastName))
        return False       

    result = addUserToTeam(studentTeam,studentGithubUser,quiet=False)

    if (result):
        result = addUserToTeam(
            getAllStudentsTeam(org),studentGithubUser,quiet=False)
        return studentTeam
    else:
        return False
               
def  getStudentFirstNameTeam(org,firstName,refresh=False):
    return findTeam(org,formatStudentTeamName(firstName),refresh)

def  getAllStudentsTeam(org):
    return findTeam(org,"AllStudents")

    


def createStudentFirstNameTeamAndAddStudent(g,org,
                                       lastName,firstName,
                                       githubUser,umail,csil):
    addPyGithubToPath()
    from github import GithubException

    print(firstName + " " + lastName + "...",end='');

    user = findUser(g,githubUser)

    if (user is None):
       return

    team = createTeam(org,
                      formatStudentTeamName(firstName))
    if (team is None):
       return

def addStudentToAllStudentsTeam(g,
                                org,
                                lastName,
                                firstName,
                                githubUser,
                                umail,csil):

    addPyGithubToPath()
    from github import GithubException

    user = findUser(g,githubUser)

    if (user is None):
       return
    
    # TRY ADDING STUDENT TO THE AllStudents team

    try:
        allStudentsTeam = findTeam(org,"AllStudents");
        if (allStudentsTeam != False):
           allStudentsTeam.add_to_members(user);
           print("... {0}({1}) added to AllStudents\n".format(firstName,githubuser))

    except GithubException as e:
       print (e)

def createLabRepo(g,org,infileName,lab):

    from disambiguateFunctions import getUserList

    userList = getUserList(infileName)

    for line in userList:
        createLabRepoForThisUser(g,
                                 org,
                                 lab,
                                 line['last'],
                                 line['first'],
                                 line['github'],
                                 line['email'],
                                 line['csil'])
        

def createLabRepoForThisUser(g,
                             org,
                             lab,
                             lastName,firstName,githubUser,umail,csil,
                             team=None):
   

    print(firstName + "\t" + lastName + "\t" + githubUser);
    
    githubUserObject = findUser(g,githubUser)

    if (githubUserObject is None):
        print("ERROR: could not find github user: " + githubUser);
        return False

    teamName = formatStudentTeamName(firstName)

    if (team is None):
        team = findTeam(org,teamName);

    if (team is None):
        team = findTeam(org,teamName,refresh=True);

    if (team is None):
        print("ERROR: could not find team: " + teamName)
        print("RUN THE addStudentsToTeams script first!")
        return False
    
    return createRepoForOrg(org,lab,
                            githubUserObject,team,firstName,csil)

    

def createRepoForOrg(org,labNumber,githubUserObject,githubTeamObject, firstName,csil):

    addPyGithubToPath()
    from github import GithubException


    desc = "Github repo for " + labNumber + " for " + firstName
    repoName =            labNumber + "_" + firstName  # name -- string
    try:  
        repo = org.create_repo(
            repoName,
            labNumber + " for CS56, S13 for " + firstName, # description 
            "http://www.cs.ucsb.edu/~" + csil, # homepage -- string
            True, # private -- bool
            True, # has_issues -- bool
            True, # has_wiki -- bool
            True, # has_downloads -- bool
            team_id=githubTeamObject,
            auto_init=True,
            gitignore_template="Java")
        print(" Created repo "+repoName)
        return True
    except GithubException as e:
       if 'errors' in e.data and 'message' in e.data['errors'][0] and e.data['errors'][0]['message']=='name already exists on this account':
           print(" repo {0} already exists".format(repoName))
       else:
           print (e)

    return False

def findUser(g,githubUser,quiet=False):
    "wraps the get_user method of the Github object"

    addPyGithubToPath()
    from github import GithubException

    try:
        user = g.get_user(githubUser)
        if (user == None):
            if not quiet:
                print("No such github user: ",githubUser)
            return None
        else:
            if not quiet:
                print(" githubUser: " + user.login + "...",end='');
            return user
    except GithubException as e:
        print(e)
        if not quiet:
            print("No such github user: ",githubUser);
        return None

def formatStudentTeamName(firstName):
       return "Student_" + firstName  # name -- string


def createTeam(org,teamName,quiet=False):
    """
    Only creates the team---doesn't add any members.
    Returns the created team.
    If team already exists, returns reference to that team object.
    Returns False if team can't be created and can't be found.
    """

    addPyGithubToPath()
    from github import GithubException

    # Try to create the team

    team = None   # Sentinel to see if it succeeded or failed
    try:
       team = org.create_team(teamName,
                         [],
                         "push");
       if not team is None:
           if not quiet:
               print(" team {0} created...".format(teamName),end='')
           return team
    except GithubException as e:
       
       if ('errors' in e.data and e.data['errors'][0]['code']=='already_exists'):
          if not quiet:
              print(" team {0} already exists...".format(teamName),
                         end='') 
       else:
          print (e)
       
    # If the create failed, try to find the team by name
    # This is our own function and does NOT throw an exception on failure

    team = findTeam(org,teamName)
    if not team is None:
        return team

    team = findTeam(org,teamName,refresh=True)
    if not team is None:
        return team
     
    if not quiet:
        print(
            "ERROR: team {0} could not be created and was not found".format(
                teamName))
        
    return None
        
    

def findTeam(org,teamName,refresh=False):

    # There isn't a "lookup team by name within an org"
    # function in the API.  So we cache a dictionary of teams
    # on the first call, then use that afterwards to look up the team.
            
    if not hasattr(findTeam, 'cacheTeamList') or refresh:
        findTeam.cacheTeamList = org.get_teams();

    if not hasattr(findTeam, 'cacheTeamDict') or refresh:
        findTeam.cacheTeamDict = {}

        for team in findTeam.cacheTeamList:
            findTeam.cacheTeamDict[team.name]=team

    if teamName in findTeam.cacheTeamDict:
        return findTeam.cacheTeamDict[teamName]
    
    return None


def addTeamsForPairsInFile(g,org,studentFileName,pairFileName):
    
    #addPyGithubToPath()
    from disambiguateFunctions import getUserList
    from disambiguateFunctions import getPairList
    
    userList = getUserList(studentFileName)

    pairList = getPairList(userList,pairFileName)
    
    for pair in pairList:
        print("\nCreating team {0}...".format(pair["teamName"]))
        pairTeam = createTeam(org,pair["teamName"])
        user1 = findUser(g,pair["user1"]["github"])
        if (user1 is None):
            raise Exception("Could not find github user {0}".pair["user1"]["github"])

        addUserToTeam(pairTeam,user1)
        user2 = findUser(g,pair["user2"]["github"])
        if (user2 is None):
            raise Exception("Could not find github user {0}".pair["user2"]["github"])
        addUserToTeam(pairTeam,user2)
        

    

def updatePairsForLab(g,org,lab,scratchDirName,prefix=""):

    """
    go through all Pair_First1_First2 teams and create a repo for each one for this
    lab
    """

    addPyGithubToPath()
    from disambiguateFunctions import getUserList

    allTeams = org.get_teams()

    # If user didn't pass in prefix, then make teams for ALL pairs,
    # that is, every team that starts with Pair_  otherwise,
    # make for every team that starts with prefix

    startsWith =  ("Pair_" if (prefix=="") else prefix)
    
    for team in allTeams:
        
        if team.name.startswith(startsWith):
            print("\nTeam: " + team.name,end='')
            result = createLabRepoForThisPairTeam(g,org,lab,team)
            
            if (result):
                pushFilesToPairRepo(g,org,lab,team,scratchDirName)
                
        


def createLabRepoForThisPairTeam(g,
                             org,
                             lab,
                             team):

    print("Creating repo for " + team.name + "...",end='')
    
    return createRepoForPairTeam(org,lab,team)

def createRepoForPairTeam(org,labNumber,team):

    addPyGithubToPath()
    from github import GithubException


    desc = "Github repo for " + labNumber + " for " + team.name
    repoName = labNumber + "_" + team.name  # name -- string
    try:  
        repo = org.create_repo(
            repoName,
            labNumber + " for CS56, S13 for " + team.name, # description 
            "http://www.cs.ucsb.edu/~pconrad/cs56", # homepage -- string
            True, # private -- bool
            True, # has_issues -- bool
            True, # has_wiki -- bool
            True, # has_downloads -- bool
            team_id=team,
            auto_init=True,
            gitignore_template="Java")
        print(" Created repo "+repoName)
        return True
    except GithubException as e:
       if 'errors' in e.data and 'message' in e.data['errors'][0] and e.data['errors'][0]['message']=='name already exists on this account':
           print(" repo {0} already exists".format(repoName))
       else:
           print (e)

    return False

    
