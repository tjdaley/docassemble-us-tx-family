"""
us_case_list.py - CRUD-provider fro a user's case list

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import date
import json
import pickle
import sys
import uuid

from docassemble.base.core import DAList
from docassemble.base.util import DARedis, Individual, IndividualName,\
    Address
from docassemble.base.logger import logmessage

CASES_KEY_TEMPLATE = '{}:us_case_list'


class UsCaseList(object):
    """
    Persists  users' case information between sessions and interviews
    """
    def __init__(self, user_id: str):
        """
        Initialize and instance.
        """
        self.cases = {}
        self.user_id = user_id
        self.user_cases_key = CASES_KEY_TEMPLATE.format(self.user_id)
        self.load()

    def load(self):
        """
        Load cases from persistant storage.
        """
        the_redis = DARedis()
        cases = the_redis.get_data(self.user_cases_key) or {}
        self.cases = cases

    def get_cases(self) -> list:
        """
        Return a list of cases sorted by the text that appears in
        a dropdown.

        Args:
            None
        Returns:
            (list): Of Cases
        """
        case_list = [(key, selection_text(case))
                     for key, case in self.cases.items()
                     if hasattr(case, 'case_id')]
        case_list.sort(key=lambda x: x[1])
        return case_list

    def get_case(self, key: str):
        """
        Return a single case based on the case key provided.

        Args:
            key (str): Case.key value
        Returns:
            (Case): Case instance referred to by *key*
        """
        case = self.cases.get(key)
        if not hasattr(case, 'case_id'):
            message = "get_case(): Case key {} does not have a case_id"
            logmessage(message.format(key))
        else:
            logmessage("get_case(): " + "Retrieved case {}".format(str(case)))
        return case

    def del_case(self, key: str):
        if key in self.cases:
            del self.cases[key]
            self.save(None)
        else:
            logmessage(f"del_case(): Could not find case having key={key}")

    def del_cases(self):
        logmessage(f"del_cases(): " +
                   "Deleting all cases for user = {self.user_id}")
        the_redis = DARedis()
        the_redis.set_data(self.user_cases_key, None)
        return

    def save(self, case) -> bool:
        """
        Save the revised case list. If a case is provided, then add it to the
        case list before saving. If no case is provided, then save the case list
        without doing anything else. (This is probably called by a delete operation.)

        Args:
            case (Case): Case to add to list or None
        Returns:
            (bool): True is successful save, otherwise raises exception.
        """
        if case:
            key = case_key(case)
            case.key = key
            self.cases[key] = case
        the_redis = DARedis()
        the_redis.set_data(self.user_cases_key, self.cases)
        return True


def case_key(case):
    """
    Create a unique key for this case.
    """
    if hasattr(case, 'key'):
        return case.key
    key = str(uuid.uuid1())
    return key


def selection_text(case) -> str:
    """
    Create text that is used to populate a dropdown for case selection.
    There is a lot of type, etc., checking here because the representation of
    a 'case' has changed significantly over time and this needs to work for
    all legacy formats so we can delete them during testing.

    Args:
        case (Case): The case to process
    Returns:
        (str): The text to display.
    """
    if hasattr(case, 'client'):
        if isinstance(case.client, DAList) and case.client.number() > 0:
            if hasattr(case.client[0].name, 'last'):
                lname = case.client[0].name.last
                fname = case.client[0].name.first
                client = f"{lname}, {fname}"
            else:
                client = case.client[0].name
        else:
            client = "*{}-{}".format(case.client.number(), str(case.client))
    else:
        client = "(NO CLIENT)"

    if hasattr(case, 'description'):
        description = case.description
    else:
        description = case.footer

    if hasattr(case, 'case_id') and case.case_id:
        case_id = "{}: {}".format(case.county, case.case_id)
    else:
        case_id = "(NOT FILED)"

    return f"{client} - {description} - ({case.county})"
