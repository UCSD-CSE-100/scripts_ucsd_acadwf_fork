#~/usr/bin/python

import disambiguateFunctions

users = disambiguateFunctions.getUserList("students_list.csv")
uniqs = disambiguateFunctions.makeUserLookupDictByGithubId(users)

