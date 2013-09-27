github-acadwf-scripts
=====================

Scripts for github academic workflow

Creating Repos for Students and Pairs
=====================
NOTE: Github Password or oAuth token will need to be entered for each command
      If done remotely, X11 forwarding must be enabled with a local X11 server running

1) run ./addStudentsToTeams.py -i <STUDENTS>.csv -u <GITHUBID>
2) run ./createLabRepo.py -u <GITHUBID> <LABNAME>
3) run ./createPairTeams.py -i <STUDENTS>.csv -p <PAIRS>.csv -u <GITHUBID>