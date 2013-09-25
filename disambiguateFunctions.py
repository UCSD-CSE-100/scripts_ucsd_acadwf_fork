#!/usr/bin/python

import unittest
import csv
from string import maketrans

def containsDuplicates(aList):
    """Does list contain a duplicate
    
    >>> containsDuplicates(['foo','bar','fum'])
    False
    >>> containsDuplicates(['foo','foo','fum'])
    True
    >>> containsDuplicates(['foo','fum','foo'])
    True
    >>> containsDuplicates(['bar','foo','bar'])
    True
    """
    copyList = list(aList)

    copyList.sort()
    
    for i in range(len(copyList)-1):
        if copyList[i]==copyList[i+1]:
            return True
    return False
    
def firstNamesWithNCharsOfLastName(userList, indices, n):
    "return list of new first names"

    names = []
    for i in range(len(indices)):
        names.append(userList[indices[i]]['first'] + "_" + 
                     userList[indices[i]]['last'][0:n])
        
    return names

def disambiguateAllFirstNames(userList):
    newUserList = list(userList)
    firstDuplicateName = nameInFirstMatchingPairOfFirstNames(newUserList)
    while ( firstDuplicateName != False):
       print("Fixing duplicates for ",firstDuplicateName)
       indices = findIndicesOfMatchingFirstNames(newUserList,firstDuplicateName)
       newUserList = disambiguateFirstNamesOfTheseIndices(newUserList,indices)
       firstDuplicateName = nameInFirstMatchingPairOfFirstNames(newUserList)

    return newUserList
        

def disambiguateFirstNamesOfTheseIndices(userList,indices):
    "return a new userList with certain first names disambiguated"
    
    newList = list(userList)
    
    needed = 1;  # Need up through 0 only (i.e. 1 char)
    
    firstNames = firstNamesWithNCharsOfLastName(userList,indices,needed)
    #print("firstNames=",firstNames,"needed=",needed)
    
    while( containsDuplicates(firstNames) ):
        needed = needed + 1
        firstNames = firstNamesWithNCharsOfLastName(userList,indices,needed)
        #print("firstNames=",firstNames,"needed=",needed)

        
    for i in range(len(indices)):
        newList[indices[i]]['first'] = firstNames[i]

    return newList

def nameInFirstMatchingPairOfFirstNames(userList):
    "returns the first name that occurs more than once, or False if no dup first names" 

    for i in range(len(userList)):
        for j in range(i+1,len(userList)):
            if userList[i]['first'] == userList[j]['first']:
               return userList[i]['first']
    return False
           
def findIndicesOfMatchingFirstNames(userList,name):
    "returns list of the indices of the elements in userList who first names match name"

    indices = []
    for i in range(len(userList)):
        if userList[i]['first'] == name:
            indices.append(i)
            
    return indices
                          

def makeUserDict(first,last,github,email,csil):
    return {'first': first, 'last': last, 'github': github.lower(), 'email':email.lower(), 'csil':csil.lower() }


def convertUserList(csvFile):
    userList = []
    for line in csvFile:
        userList.append(makeUserDict(line["First Name"],
                                     line["Last Name"],
                                     line["github userid"],
                                     line["Umail address"],
                                     line["CSIL userid"]))
    

    for user in userList:
        user["first"] = user["first"].strip().translate(maketrans(" ","_"));

    return userList

def makeUserLookupDictByGithubId(userList):
    """
    userList is a list of dictionaries with keys first,last,github,email,csil.
    returned value is a dictionary where the keys are the github ids,
      and the values are the original dictionaries with first,last,github,email,csil
    """

    newDict = {}
    for user in userList:
        if user['github'] in newDict:
            raise Exception("duplicate github user {0}".format(user['github']))
        newDict[user['github']]=user

    return newDict

def convertPairList(userList,csvFile):
    """
    userList is a list of dictionaries with keys first,last,github,email,csil
    csvFile is a list of dictionaries with keys Partner1_GithubID,Partner2_GithubID,labnumber
    
    returned value should be a list of dictionaries with keys teamName,user1,user2, where user1 and user2 are the elements fromn userlist where the github ids match.
    """

    pairList = []
    userLookupDict = makeUserLookupDictByGithubId(userList)
    for line in csvFile:
        line['Partner1_GithubID']=line['Partner1_GithubID'].lower().strip()
        line['Partner2_GithubID']=line['Partner2_GithubID'].lower().strip()
        if not (line['Partner1_GithubID'] in userLookupDict):
            raise Exception("Partner1_GithubID from pair file not found in user list: {0}".format(line['Partner1_GithubID']))
        
        if not (line['Partner2_GithubID'] in userLookupDict):
            raise Exception("Partner2_GithubID from pair file not found in user list: {0}".format(line['Partner2_GithubID']))
        
        team = {}
        user1 = userLookupDict[line['Partner1_GithubID']]
        user2 = userLookupDict[line['Partner2_GithubID']]
        if (user1["first"] > user2["first"]): 
            # Swap if out of order
            temp = user1
            user1 = user2
            user2 = temp
        team["user1"] = user1
        team["user2"] = user2
        team["teamName"]="Pair_" + user1['first'] + "_" + user2['first']
        
        pairList.append(team)
        
    return pairList

def getUserList(csvFilename):

    with open(csvFilename,'r') as f:
        csvFile = csv.DictReader(f,delimiter=',', quotechar='"')
    
        userList = convertUserList(csvFile)
        
        newUserList = disambiguateAllFirstNames(userList)

        return newUserList

def getPairList(userList,csvFilename):

    with open(csvFilename,'r') as f:
        csvFile = csv.DictReader(f,delimiter=',', quotechar='"')
    
        pairList = convertPairList(userList,csvFile)
        
        return pairList

class TestSequenceFunctions(unittest.TestCase):



    def setUp(self):
        self.userList1 = [ makeUserDict('Chris','Jones','cj','cj@example.org','cj'),
                           makeUserDict('Chris','Smith','cs','cs@example.org','cs'),
                           makeUserDict('Mary Kay','Jones','mkj','mkj@example.org','mkj'),
                           makeUserDict('Mary','Kay','mkay','mkay@example.org','mkay') ]

        self.userList1a = [ makeUserDict('Chris_J','Jones','cj','cj@example.org','cj'),
                           makeUserDict('Chris_S','Smith','cs','cs@example.org','cs'),
                           makeUserDict('Mary Kay','Jones','mkj','mkj@example.org','mkj'),
                           makeUserDict('Mary','Kay','mkay','mkay@example.org','mkay') ]

        self.userList2 = [ makeUserDict('Chris_J','Jones','cj','cj@example.org','cj'),
                           makeUserDict('Chris_S','Smith','cs','cs@example.org','cs'),
                           makeUserDict('Mary Kay','Jones','mkj','mkj@example.org','mkj'),
                           makeUserDict('Mary','Kay','mkay','mkay@example.org','mkay') ]

        self.userList3 = [ makeUserDict('Chris','Jones','cj','cj@example.org','cj'),
                           makeUserDict('Chris','Smith','cs','cs@example.org','cs'),
                           makeUserDict('Mary','Jones','mkj','mkj@example.org','mkj'),
                           makeUserDict('Mary','Kay','mkay','mkay@example.org','mkay'),
                           makeUserDict('Dave','Jones','dj','dk@example.org','dj'),
                           makeUserDict('Dave','Kay','dk','dj@example.org','dk') ]

        self.userList3a = [ makeUserDict('Chris_J','Jones','cj','cj@example.org','cj'),
                           makeUserDict('Chris_S','Smith','cs','cs@example.org','cs'),
                           makeUserDict('Mary_J','Jones','mkj','mkj@example.org','mkj'),
                           makeUserDict('Mary_K','Kay','mkay','mkay@example.org','mkay'),
                           makeUserDict('Dave_J','Jones','dj','dk@example.org','dj'),
                           makeUserDict('Dave_K','Kay','dk','dj@example.org','dk') ]



        self.userList4 = [ makeUserDict('Chris','Jones','cj','cj@example.org','cj'),
                           makeUserDict('Mary','Jones','mkj','mkj@example.org','mkj'),
                           makeUserDict('Dave','Kay','dk','dj@example.org','dk') ]

        self.userList5 = [   makeUserDict('Mary','Jones','mkj','mkj@example.org','mkj'),
                             makeUserDict('Chris','Smyth','csmy','cj@example.org','cj'),
                             makeUserDict('Chris','Smith','csmi','cs@example.org','cs'),
                             makeUserDict('Mary','Kay','mkay','mkay@example.org','mkay'),
                             makeUserDict('Dave','Jones','dj','dk@example.org','dj'),
                             makeUserDict('Dave','Kay','dk','dj@example.org','dk') ]

        self.userList5a = [   makeUserDict('Mary_J','Jones','mkj','mkj@example.org','mkj'),
                             makeUserDict('Chris_Smy','Smyth','csmy','cj@example.org','cj'),
                             makeUserDict('Chris_Smi','Smith','csmi','cs@example.org','cs'),
                             makeUserDict('Mary_K','Kay','mkay','mkay@example.org','mkay'),
                             makeUserDict('Dave_J','Jones','dj','dk@example.org','dj'),
                             makeUserDict('Dave_K','Kay','dk','dj@example.org','dk') ]


    def test_firstNamesWithNCharsOfLastName1(self):
        result = firstNamesWithNCharsOfLastName(self.userList1,[0,1,2,3],1)
        self.assertEqual(result, ["Chris_J","Chris_S","Mary Kay_J","Mary_K"])

    def test_firstNamesWithNCharsOfLastName2(self):
        result = firstNamesWithNCharsOfLastName(self.userList1,[0,2],2)
        self.assertEqual(result, ["Chris_Jo","Mary Kay_Jo"])

    def test_disambiguateFirstNamesOfTheseIndices(self):
        result = disambiguateFirstNamesOfTheseIndices(self.userList1,[0,1])
        self.assertEqual(result,self.userList2)


    def test_nameInFirstMatchingPairOfFirstNames1(self):
        result = nameInFirstMatchingPairOfFirstNames(self.userList1);
        self.assertEqual(result,"Chris");

    def test_nameInFirstMatchingPairOfFirstNames3(self):
        result = nameInFirstMatchingPairOfFirstNames(self.userList3);
        self.assertEqual(result,"Chris");

    def test_nameInFirstMatchingPairOfFirstNames4(self):
        result = nameInFirstMatchingPairOfFirstNames(self.userList4);
        self.assertFalse(result);

    def test_nameInFirstMatchingPairOfFirstNames5(self):
        result = nameInFirstMatchingPairOfFirstNames(self.userList5);
        self.assertEqual(result,"Mary");


        

    def test_findIndicesOfMatchingFirstNames1(self):
        result = findIndicesOfMatchingFirstNames(self.userList1,'Chris');
        self.assertEqual(result,[0,1]);

    def test_findIndicesOfMatchingFirstNames3(self):
        result = findIndicesOfMatchingFirstNames(self.userList3,'Mary');
        self.assertEqual(result,[2,3]);

    def test_findIndicesOfMatchingFirstNames4(self):
        result = findIndicesOfMatchingFirstNames(self.userList4,'Dave');
        self.assertEqual(result,[2]);

    def test_findIndicesOfMatchingFirstNames5a(self):
        result = findIndicesOfMatchingFirstNames(self.userList5,'Mary');
        self.assertEqual(result,[0,3]);

    def test_findIndicesOfMatchingFirstNames5b(self):
        result = findIndicesOfMatchingFirstNames(self.userList5,'Chris');
        self.assertEqual(result,[1,2]);

    def test_disambiguateAllFirstNames1(self):
        result = disambiguateAllFirstNames(self.userList1);
        self.assertEqual(result,self.userList1a);

    def test_disambiguateAllFirstNames3(self):
        result = disambiguateAllFirstNames(self.userList3);
        self.assertEqual(result,self.userList3a);

    def test_disambiguateAllFirstNames4(self):
        result = disambiguateAllFirstNames(self.userList4);
        self.assertEqual(result,self.userList4);

    def test_disambiguateAllFirstNames5(self):
        result = disambiguateAllFirstNames(self.userList5);
        self.assertEqual(result,self.userList5a);


if __name__ == '__main__':
    unittest.main()
    import doctest
    doctest.testmod()

