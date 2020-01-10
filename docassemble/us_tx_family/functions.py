"""
functions.py - Functions for docassemble interviews.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
from .us_tx_counties import UsTxCounties
from .us_tx_courts import UsTxCourts
from .us_tx_court_directory import UsTxCourtDirectory
from .us_case_list import UsCaseList

from docassemble.base.logger import logmessage

TRACE = True

def counties():
    # Run us_tx_counties.py to get a new list . . . if Texas ever adds/removes counties.
    if TRACE:
        logmessage("counties(): Started")
    county_db = UsTxCounties()
    return county_db.get_counties()


def courts(county: str):
    if TRACE:
        logmessage("courts(): Started")
    court_db = UsTxCourts()
    court_list = court_db.get_courts(county)
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

def my_cases(user_id: str):
    if TRACE:
        logmessage("my_cases(): Started")
    case_db = UsCaseList(user_id)
    cases = case_db.get_cases()
    cases.insert(0, ('*ADD*', "(ADD NEW CASE)"))
    return cases

def get_case(user_id: str, case_key: str):
    if TRACE:
        logmessage("get_case(): Started")
    case_db = UsCaseList(user_id)
    case = case_db.get_case(case_key)
    return case or '*NONE*'

def del_case(user_id: str, case_key: str):
    if TRACE:
        logmessage("del_case(): Started")
    case_db = UsCaseList(user_id)
    case_db.del_case(case_key)

def del_cases(user_id: str, confirm: bool = False):
    if TRACE:
        logmessage("del_cases(): Started")
    if not isinstance(confirm, bool) or confirm != True:
        logmessage("del_cases(): Cannot delete all cases unless 2d arg is True")
        return
    case_db = UsCaseList(user_id)
    case_db.del_cases()

def save_case(user_id: str, case):
    if TRACE:
        logmessage("save_case(): Started")
    case_db = UsCaseList(user_id)
    case_db.save(case)
