"""
functions.py - Functions for docassemble interviews.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import datetime
from decimal import Decimal
import json
import os
from .us_fred_data import FredUtil
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

ME_KEY = '{}:me'


def avg_us_mortgage_rate(year: int, month: int, term_in_years: int = 30) -> Decimal:
    """
    Retrieve avg home mortgage interest rate from Federal Reserve Data.
    """
    futil = FredUtil()
    rate = futil.average_fixed_mortgage(year, month, term_in_years)
    return rate


def counties():
    # Run us_tx_counties.py to get a new list if Texas ever
    # adds/removes counties.
    county_db = UsTxCounties()
    return county_db.get_counties()


def courts(county: str, not_filed=True):
    court_db = UsTxCourts()
    court_list = court_db.get_courts(county)
    if not_filed:
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


def estimate_loan_balance(p: int, year: int, month: int, term: int, interest_rate: Decimal):
    """
    Estimate the remaining balance due on a loan.

    From: https://en.wikipedia.org/wiki/Mortgage_calculator#Monthly_payment_formula

    NOTE: This implementation can be off by a few pennies per month,
          which makes the final payment appear to create a very slightly
          negative loan balance.

    TODO: Eliminate "term" argument...it's not needed.

    Args:
      p (int): Original principal value of the loan
      year (int): Year first payment was due
      month (int): Month first payment was due
      term (int): Term of the loan in years
      interest_rate (Decimal): Annual interest rate

    Returns:
      Amount remaining on the loan, assuming timely payments.
    """
    payment = loan_payment(p, term, interest_rate)
    p_d = Decimal(p)
    rate_d = Decimal(interest_rate)
    monthly_rate = Decimal(rate_d / 12)
    start_date = datetime(int(year), int(month), 1)
    N = months_since_date(start_date)

    remaining = (1+monthly_rate)**N*p_d - (((1+monthly_rate)**N-1)/monthly_rate)*payment
    # prevent negative responses
    remaining = max(remaining, 0.00)
    remaining = Decimal(round(remaining, 2))
    return remaining


def last_30_years() -> list:
    """
    Return a list of the last 30 years. Will actually return
    values for the last 31 years.

    Returns:
        (list): List strings representing the last 31 years.
    """
    this_year = datetime.now().year
    return [str(year) for year in range(this_year-31, this_year+1)]


def loan_payment(p: int, term: int, interest_rate: Decimal):
    """
    Compute monthly principal and interest payment on a fixed rate loan.

    From: https://en.wikipedia.org/wiki/Mortgage_calculator#Monthly_payment_formula

    Args:
      p (int): Original principal value of the loan
      term (int): Term of the loan in years
      interest_rate (Decimal): Annual interest rate

    Returns:
      (Decimal): Monthly principal and interest payment
    """
    p_d = Decimal(p)
    term_d = Decimal(term)
    rate_d = Decimal(interest_rate)
    monthly_rate = Decimal(rate_d / 12)
    payment = Decimal(round(((monthly_rate * p_d) / (1-((1+(monthly_rate)) ** (-term_d * 12)))), 2))
    return payment


def months_since_date(start_date) -> int:
    """
    Computes the number of months since a given date.
    My definition of "number of months" relates to the number of times
    you'd flip the calendar page to go to another month, e.g. the
    number of months between Jan 31 and Feb 1 is *1*.
    """
    today = datetime.now()
    return (today.year - start_date.year) * 12 + today.month - start_date.month


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


def my_cases(allow_add: bool = True):
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
    except Exception:
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
    case_db = UsCaseList(__user_id())
    case = case_db.get_case(case_key)
    return case or '*NONE*'


def del_case(case_key: str):
    case_db = UsCaseList(__user_id())
    case_db.del_case(case_key)


def del_cases(confirm: bool = False):
    if not isinstance(confirm, bool) or confirm is not True:
        logmessage("del_cases(): set confirm=True to delete all cases.")
        return
    case_db = UsCaseList(__user_id())
    case_db.del_cases()


def save_case(case):
    case_db = UsCaseList(__user_id())
    return case_db.save(case)


def save_me(about_me):
    the_redis = DARedis()
    key = ME_KEY.format(__user_id())
    the_redis.set_data(key, about_me)
    return True


def set_client_role(case):
    # Make a list of all the parties we represent
    case.client.clear()
    for p in case.petitioner:
        if p.attorney.bar_number == case.me.bar_number:
            case.client.append(p, set_instance_name=True)
            case.client_role = "Petitioner"
    for p in case.respondent:
        if p.attorney.bar_number == case.me.bar_number:
            case.client.append(p, set_instance_name=True)
            case.client_role = "Respondent"
    for p in case.intervenor:
        if p.attorney.bar_number == case.me.bar_number:
            case.client.append(p, set_instance_name=True)
            case.client_role = "Intervenor"
    case.client.gathered = True
    case.client.is_there_another = False
    return True


def us_states():
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
