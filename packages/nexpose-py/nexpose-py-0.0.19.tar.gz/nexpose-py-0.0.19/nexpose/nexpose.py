#!/usr/bin/env python3

"""
Python3 bindings for the Nexpose API v3
"""
from collections import namedtuple
from datetime import datetime, timedelta
import re
import urllib3

import requests

import nexpose.get_credentials as get_credentials

urllib3.disable_warnings()

class NexposeException(Exception):
    """
    Base class for exceptions in this module.
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        print(self.status_code)
        print(self.message)


class ResponseNotOK(NexposeException):
    """
    Request did not return 200 (OK)
    """


def _require_response_200_ok(response):
    """
    Accept a requests.response object.
    Raise ResponseNotOK if status code is not 200.
    Otherwise, return True
    """
    if response.status_code != 200:
        raise ResponseNotOK(
            status_code=response.status_code, message=response.text
        )
    return True


def config(args):
    """
    Accept args (argparser Namespace).
    Return nexpose.login
    """
    base_url = ':'.join([args.baseurl, args.port])
    
    user = args.user or get_credentials.user()
    password = args.password or get_credentials.password()
    return login(
        base_url=base_url,
        user=user,
        password=password,
        verify=args.verify,
    )


def login(*, base_url, user, password, verify=True):
    """
    Accept named args base_url, username, password (strings),
    optionally verify (Boolean default True).
    Return a named tuple used for Nexpose login.
    """
    l = namedtuple("Login", ['base_url', 'user', 'password', 'verify'])
    return l(base_url=base_url, user=user, password=password, verify=verify)


def get(*, nlogin, endpoint, params=[]):
    """
    Accept named args nlogin (nexpose.login), endpoint (string), optional params.
    Return get against nexpose.
    """
    url = f"{nlogin.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.get(
        url,
        auth=(nlogin.user, nlogin.password),
        headers=head,
        verify=nlogin.verify,
        params=params
    )
    _require_response_200_ok(response)

    return response.json()


def delete(*, nlogin, endpoint):
    """
    Accept named args nlogin (nexpose.login) and endpoint (string)
    Return delete against nexpose.
    """
    url = f"{nlogin.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.delete(
        url, auth=(nlogin.user, nlogin.password), headers=head, verify=nlogin.verify
    )
    _require_response_200_ok(response)

    return response.json()


def put(*, nlogin, endpoint, data=[]):
    """
    Accept named args nlogin (nexpose.login) and endpoint (string)
    Return put against nexpose.
    """
    url = f"{nlogin.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.put(
        url, auth=(nlogin.user, nlogin.password), headers=head, verify=nlogin.verify, data=data,
    )
    _require_response_200_ok(response)

    return response.json()


def _generator(*, nlogin, endpoint):
    """
    Accept named args nlogin (nexpose.login) and endpoint (str)
    Return generator object of paginated resources.
    """
    pages = get(nlogin=nlogin, endpoint=endpoint)["page"]["totalPages"]
    for page in range(pages):
        for resource in get(
            nlogin=nlogin,
            endpoint=endpoint,
            params={'page': page},
            )["resources"]:
                yield resource


def engines(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return scan engines resources.
    """
    return get(nlogin=nlogin, endpoint="api/3/scan_engines")['resources']


def engine_pools(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return pools resources.
    """
    return get(nlogin=nlogin, endpoint="api/3/scan_engine_pools")['resources']


def reports(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return generator of reports responses.
    """
    return _generator(nlogin=nlogin, endpoint="api/3/reports")


def report_history(*, nlogin, report_id):
    """
    Accept named args nlogin (nexpose.login), report_id (int).
    Return report history reponse.
    """
    return get(nlogin=nlogin, endpoint=f"api/3/reports/{report_id}/history")


def delete_report(*, nlogin, report_id):
    """
    Accept named args nlogin (nexpose.login), report_id (int).
    Return deleted report response.
    """
    return delete(nlogin=nlogin, endpoint=f"api/3/reports/{report_id}")


def users(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return generator of users resources
    """
    return _generator(nlogin=nlogin, endpoint="api/3/users")


def delete_user(*, nlogin, user_id):
    """
    Accept nlogin (nexpose.login), user_id(int).
    Return deleted users response.
    """
    return delete(nlogin=nlogin, endpoint=f"api/3/users/{user_id}")


def scans(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return generator of scans resources.
    """
    return _generator(nlogin=nlogin, endpoint="api/3/scans")


def sites(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return generator of sites resources.
    """
    return _generator(nlogin=nlogin, endpoint="api/3/sites")


def site(*, nlogin, site_id):
    """
    Accept named args nlogin (nexpose.login), site_id (int).
    Return site response.
    """
    return get(nlogin=nlogin, endpoint=f"api/3/sites/{site_id}")


def site_id_older_than(*, nlogin, site_id, days=90):
    """
    Accept named args nlogin (nexpose.login), site_id (int),
    optional days (int, default 90).
    Return True is site is older than days,
    otherwise return False
    """
    now = datetime.now()
    max_age = timedelta(days=days)
    start_dates = [
        schedule['start']
        for schedule in schedules(nlogin=nlogin, site_id=site_id)
    ]
    if len(start_dates) == 0:
        return True
    for date in start_dates:
        # Nexpose date example:
        # '2020-11-01T11:22:27Z'
        start_time = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        if now - start_time < max_age:
            return False
    return True


def delete_site(*, nlogin, site_id):
    """
    Accept named args nlogin (nexpose.login), site_id (int).
    Return deleted site response.
    """
    return delete(nlogin=nlogin, endpoint=f"api/3/sites/{site_id}")


def schedules(*, nlogin, site_id):
    """
    Accept named args nlogin (nexpose.login), site_id (int).
    Return schedules resources.
    """
    return get(
        nlogin=nlogin,
        endpoint=f"api/3/sites/{site_id}/scan_schedules")['resources']


def assets(nlogin):
    """
    Accept nlogin (nexpose.login).
    Return generator of assets responses.
    """
    return _generator(nlogin=nlogin, endpoint="api/3/assets")


def create_role(*, nlogin, role):
    """
    Accept named args nlogin (nexpose.login), role (dict).
    Return created role response.
    """
    return put(nlogin=nlogin, endpoint=f"api/3/roles/{role['id']}", data=role)


def remove_old_reports(*, nlogin):
    """
    Accept named arg nlogin (nexpose.login).
    Remove reports with no history.
    Return a generator of remove report ids.
    """
    report_ids = (report['id'] for report in reports(nlogin))
    for report in report_ids:
        history = report_history(nlogin=nlogin, report_id=report)
        if not history['resources']:
            delete_report(nlogin=nlogin, report_id=report)
            yield report


def remove_old_sites(*, nlogin, days=90, regex=".*"):
    """
    Accept named args nlogin (nexpose.login),
    optionally days (int) and regex (str).
    Remove sites older than days, if it matches regex.
    Return a generator of remove site ids.
    """
    site_ids = (
        site["id"]
        for site in sites(nlogin)
        if re.fullmatch(regex, site['name'])
    )
    for site_id in site_ids:
        if site_id_older_than(nlogin=nlogin, site_id=site_id, days=days):
            try:
                delete_site(nlogin=nlogin, site_id=site_id)
                yield site_id
            except ResponseNotOK as err:
                print(f"something went wrong with {site_id}: {err}")
