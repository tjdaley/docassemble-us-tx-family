"""
functions.py - Functions for docassemble interviews.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
import os
from .us_tx_counties import UsTxCounties


def counties():
    my_counties = UsTxCounties()
    return my_counties.get_counties
