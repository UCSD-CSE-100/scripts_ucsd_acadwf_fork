#!/usr/local/env python

""" Python module for verifying that an input string is a valid
    github userid

    Author: Arden Liao (ardentsonata)
"""

import sys
import logging

try:
    import requests
except ImportError:
    logging.info("\'requests\' is not installed on this system")

VERIFY_URL = "https://api.github.com/users/{_user}"

def main():
    """ Main driver that verifies if a passed in string, or list of strings
        are valid github userids
    """
    return 0

def verify_user(user, cred=()):
    """ Verifies is a passed in user string is a valid github user

        Opt Parameters: cred    - tuple of ( "UN", "PW" ) for a valid github
                                  user
    """
    try:
        req = requests.get(VERIFY_URL.format(_user=user), auth=cred)
        return req.status_code == requests.codes.ok
    except NameError:
        logging.debug("Requests not imported, defaulting to alt solution")
    return False

if __name__ == "__main__":
    logging.basicConfig(level = logging.error,
                        format="%(asctime)s - %(levelname)s -- %(message)s")
    main()
    sys.exit(0)
