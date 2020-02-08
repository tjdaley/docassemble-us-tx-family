"""
functions.py - Functions for docassemble interviews.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import json
import os
from .us_tx_counties import UsTxCounties
from .us_tx_courts import UsTxCourts
from .us_tx_court_directory import UsTxCourtDirectory
from .us_tx_jails import UsTxJails
from .us_case_list import UsCaseList

from docassemble.base.functions import get_user_info
from docassemble.base.legal import Case
from docassemble.base.logger import logmessage
from docassemble.base.util import ChildList, DAList, DARedis
from .objects import Attorney, AttorneyList, RepresentedPartyList

TRACE = True
ME_KEY = '{}:me'

def counties():
    # Run us_tx_counties.py to get a new list . . . if Texas ever adds/removes counties.
    if TRACE:
        logmessage("counties(): Started")
    county_db = UsTxCounties()
    return county_db.get_counties()


def courts(county: str, not_filed=True):
    if TRACE:
        logmessage("courts(): Started")
    court_db = UsTxCourts()
    court_list = court_db.get_courts(county)
    if not_filed:
        court_list.insert(0, (None, "(NOT FILED)"))
    return court_list

def court_staff(court: str):
    if TRACE:
        logmessage("court_staff(): Started")
    directory = UsTxCourtDirectory()
    staff_list = directory.get_court(court)
    return staff_list

def clerk_staff(county: str):
    if TRACE:
        logmessage("clerk_staff(): Started")
    directory = UsTxCourtDirectory()
    staff_list = directory.get_clerk(county)
    return staff_list

def jails():
    jail_db = UsTxJails()
    jails = jail_db.get_jails()
    return jails

def jail(short_name: str) -> list:
    jail_db = UsTxJails()
    return jail_db.get_jail(short_name)

def me():
    the_redis = DARedis()
    key = ME_KEY.format(__user_id())
    me = the_redis.get_data(key)
    return me

def my_cases(allow_add:bool = True):
    if TRACE:
        logmessage("my_cases(): Started")
    case_db = UsCaseList(__user_id())
    cases = case_db.get_cases()
    if allow_add:
        cases.insert(0, ('*ADD*', "(ADD NEW CASE)"))
    return cases

def initialize_case(case):
    # Set up a basic family law case.
    case.state = "TEXAS"
    case.country = "US"
    case.court.name = "District Court"
    case.court.jurisdiction = list('Texas')
    try:
        del case.plaintiff
        del case.defendant
    except:
        pass
    case.initializeAttribute('petitioner', RepresentedPartyList)
    case.initializeAttribute('respondent', RepresentedPartyList)
    case.initializeAttribute('intervenor', RepresentedPartyList)
    case.initializeAttribute('client', RepresentedPartyList)
    case.initializeAttribute('child', ChildList)
    case.initializeAttribute('asset', DAList)
    case.initializeAttribute('liability', DAList)
    case.initializeAttribute('attorney', AttorneyList)
    case.initializeAttribute('me', Attorney)
    case.firstParty = case.petitioner
    case.secondParty = case.respondent
    case.me = me()

    # Add our user's attorney profile to the list of attorneys
    # working on this case.
    case.attorney.clear()
    case.attorney.append(me(), set_instance_name=True)

    return case


def get_case(case_key: str):
    if TRACE:
        logmessage("get_case(): Started")
    case_db = UsCaseList(__user_id())
    case = case_db.get_case(case_key)
    return case or '*NONE*'

def del_case(case_key: str):
    if TRACE:
        logmessage("del_case(): Started")
    case_db = UsCaseList(__user_id())
    case_db.del_case(case_key)

def del_cases(confirm: bool = False):
    if TRACE:
        logmessage("del_cases(): Started")
    if not isinstance(confirm, bool) or confirm != True:
        logmessage("del_cases(): Cannot delete all cases unless 2d arg is True")
        return
    case_db = UsCaseList(__user_id())
    case_db.del_cases()

def save_case(case):
    if TRACE:
        logmessage("save_case(): Started")
    case_db = UsCaseList(__user_id())
    return case_db.save(case)

def save_me(about_me):
    if TRACE:
        logmessage("save_me(): Started")
    the_redis = DARedis()
    key = ME_KEY.format(__user_id())
    the_redis.set_data(key, about_me)
    return True

def us_states():
    if TRACE:
        logmessage("retrieving us states")
    return ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

def __user_id() -> str:
    """
    Return a string that we use for indexing users based on
    the current logged in user.

    Args:
        None.
    Returns:
        (str): User-ID for indexing and persisting user data.
    """
    user_info = get_user_info()
    user_id = user_info['id']
    return str(user_id)
