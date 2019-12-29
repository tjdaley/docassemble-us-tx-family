"""
functions.py - Functions for docassemble interviews.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
from .us_tx_counties import UsTxCounties
from .us_tx_courts import UsTxCourts


def counties():
    # Run us_tx_counties.py to get a new list . . . if Texas ever adds/removes counties.
    county_db = UsTxCounties()
    return county_db.get_counties()


def courts(county: str):
    court_db = UsTxCourts()
    court_list = court_db.get_courts(county)
    court_list.append("(NOT FILED)")
    court_list.sorted()
    return court_list
