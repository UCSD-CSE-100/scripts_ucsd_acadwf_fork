github-acadwf-scripts
=====================

Scripts for github academic workflow created by Phillip Conrad 

Creating Repos for Students and Pairs
=====================
NOTE: Github Password or oAuth token will need to be entered for each command
      If done remotely, X11 forwarding must be enabled with a local X11 server running

1) run ./addStudentsToTeams.py -u <GITHUBID>
2) run ./createPairTeams.py -u <GITHUBID>
3) run ./createLabRepo.py -u <GITHUBID> <LABNAME>
4) run ./createLabRepoForPairs.py -u <GITHUBID> <LABNAME>
5) run ./pushFilesToRepo.py -u <GITHUBID> <LABNAME>