"""
Parse common arguments for nexpose-py command line programs.
"""

import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    "-u",
    "--user",
    help="""User for authentication to Nexpose.
    Default is to pull from environmental variable NEXPOSE_USER.
    If that variable is not set, prompt.
    """,
    action="store",
)
parser.add_argument(
    "-p",
    "--password",
    help="""Password for authentication to Nexpose.
    Default is to pull from environmental variable NEXPOSE_PASS.
    If that variable is not set, prompt.
    """,
    action="store",
)
parser.add_argument(
    "-i",
    "--baseurl",
    help="""Base url of Nexpose API.
    Default: https://localhost
    """,
    action="store",
    default="https://localhost",
)
parser.add_argument(
    "-P",
    "--port",
    help="""Port the Nexpose API runs on.
    Default is 3780
    """,
    action="store",
    default="3780",
)
parser.add_argument(
    "-k",
    "--insecure",
    help="""Allow operation to proceed even if connection is insecure.
    Do not use this in production.
    """,
    action="store_false",
    default=True,
    dest="verify",
)
