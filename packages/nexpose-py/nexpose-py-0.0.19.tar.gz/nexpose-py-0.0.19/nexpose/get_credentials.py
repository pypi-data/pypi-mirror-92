"""
Get Nexpose user and password from environment or prompt
"""

import getpass

from os import environ


def user():
    """
    Return user (string), taken from environment or prompt
    """
    try:
        nexpose_user = environ["NEXPOSE_USER"]
    except KeyError:
        nexpose_user = getpass.getpass(prompt="Nexpose user:")
    return nexpose_user


def password():
    """
    Return key (string), taken from environment or prompt
    """
    try:
        nexpose_password = environ["NEXPOSE_PASS"]
    except KeyError:
        nexpose_password = getpass.getpass(prompt="Nexpose password:")
    return nexpose_password
