"""
functions.py - Functions for docassemble interviews.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
from .us_tx_counties import UsTxCounties
from .us_tx_courts import UsTxCourts
from .us_tx_court_directory import UsTxCourtDirectory
from .us_case_list import UsCaseList


def counties():
    # Run us_tx_counties.py to get a new list . . . if Texas ever adds/removes counties.
    county_db = UsTxCounties()
    return county_db.get_counties()


def courts(county: str):
    court_db = UsTxCourts()
    court_list = court_db.get_courts(county)
    court_list.insert(0, (None, "(NOT FILED)"))
    return court_list

def court_staff(court: str):
    directory = UsTxCourtDirectory()
    staff_list = directory.get_court(court)
    return staff_list

def clerk_staff(county: str):
    directory = UsTxCourtDirectory()
    staff_list = directory.get_clerk(county)
    return staff_list

def my_cases(user_id: str):
    case_db = UsCaseList(user_id)
    cases = case_db.get_cases()
    cases.insert(0, (None, "(ADD NEW CASE)"))
    return cases

def get_case(user_id: str, case_key: str):
    case_db = UsCaseList(user_id)
    case = case_db.get_case(case_key)
    return case

def save_case(user_id: str, case):
    case_db = UsCaseList(user_id)
    case_db.save(case)
