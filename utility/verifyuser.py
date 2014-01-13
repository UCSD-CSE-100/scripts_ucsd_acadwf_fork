#!/usr/bin/env python

""" Python module for verifying that an input string is a valid
    github userid

    Author: Arden Liao (ardentsonata)
"""

import argparse
import getpass
import sys
import logging

try:
    import requests
except ImportError:
    logging.debug("\'requests\' is not installed on this system")

VERIFY_URL = "https://api.github.com/users/{_user}"

USER_404 = "\'{_ghid}\' not found"

def main():
    """ Main driver that verifies if a passed in string, or list of strings
        are valid github userids, will print out the list of invalid ghids
    """
    args = parse_arguments()
    creds = ()
    if args['cred']:
        username = raw_input("Username: ")
        if not verify_user(username):
            logging.error(USER_404.format(_ghid=username))
        else:
            password = getpass.getpass()
            cred = (username, password)
    ghids = args['list']
    for ghid in ghids:
        if not verify_user(ghid, cred):
            print USER_404.format(_ghid=ghid)
    return 0

def verify_user(user, cred=()):
    """ Verifies is a passed in user string is a valid github user

        Opt Parameters: cred    - tuple of ( "UN", "PW" ) for a valid github
                                  user, usage of cred raises the rate limit
                                  for API requests
    """
    try:
        req = requests.get(VERIFY_URL.format(_user=user), auth=cred)
        return req.status_code == requests.codes.ok
    except NameError:
        logging.debug("Requests not imported, defaulting to alt solution")

    return False

def parse_arguments():
    """ Parses arguments from the command line  """
    parser = argparse.ArgumentParser(description=
                                     'Check github ids for validity')
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', nargs='?',
                       help='verify github ids from a file',
                       dest='file', type=str, default=Non
    group.add_argument('-l', '--list', nargs='*',
                       help='verify github ids from a list',
                       dest='list', default=None)
    group.add_argument('-i', '--id', type=str, default=None,
                       help='verify a github id',
                       dest='ghid')
    parser.add_argument('--cred', dest='cred', action='store_true',
                        help='use credentials to login to Githhub',
                        default=False)
    args = parser.parse_args()

    if args.ghid is not None:
        args.list = [args.ghid]
    elif args.file is not None:
        args.list = []
        try:
            with open(args.file, 'rb') as ghids:
                for line in ghids:
                    args.list.extend(line)
        except IOError:
            logging.error("File does not exist")

    return {'list': args.list, 'cred': args.cred}

if __name__ == "__main__":
    logging.basicConfig(level = logging.ERROR,
                        format="%(asctime)s - %(levelname)s -- %(message)s")
    main()
    sys.exit(0)
