"""
us_case_list.py - CRUD-provider fro a user's case list

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import date
import json
import pickle
import sys
import uuid

DEV_MODE = False

if not DEV_MODE:
    from docassemble.base.core import DAList
    from docassemble.base.util import DARedis, Individual, IndividualName, Address
    from docassemble.base.logger import logmessage
else:
    def logmessage(message: str):
        try:
            sys.stderr.write(message + '\n')
        except Exception as e:
            sys.stderr.write('Unable to log: {}'.format(str(e)))

STORE = '{}:us_case_list'

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
        self.store = STORE.format(self.user_id)
        self.load()
    
    def load(self):
        """
        Load cases from a local store.
        """
        self.cases = self.read() or {}

    def get_cases(self):
        case_list = [(key, selection_text(case)) for key, case in self.cases.items() if hasattr(case, 'case_id')]
        return case_list

    def get_case(self, key: str):
        case = self.cases.get(key)
        if not hasattr(case, 'case_id'):
            logmessage("get_case(): " + "Case key {} does not have a case_id".format(key))
        else:
            logmessage("get_case(): " + "Retrieved case {}".format(str(case)))
        return case

    def del_case(self, key: str):
        if key in self.cases:
            del self.cases[key]
            self.save(None)
        else:
            logmessage("del_case(): " + "Could not find case having key={}".format(key))

    def del_cases(self):
        if not DEV_MODE:
            logmessage("del_cases(): " + "Deleting all cases for user = {}".format(self.user_id))
            the_redis = DARedis()
            the_redis.set_data(self.store, None)
            return
        logmessage("del_case(): " + "Cannot delete all cases in DEV_MODE")

    def read(self) -> dict:
        if DEV_MODE:
            cases = self.dev_read()
        else:
            cases = self.prod_read()
        return cases

    def save(self, case) -> bool:
        """
        Save a case.
        """
        if case is not None:
            key = case_key(case)
            case.key = key
        else:
            key = None
        if DEV_MODE:
            return self.dev_save(key, case)
        return self.prod_save(key, case)

    def prod_read(self) -> dict:
        """
        Read the list of cases for this user from cross-session storage.
        """
        the_redis = DARedis()
        return the_redis.get_data(self.store)

    def dev_read(self) -> dict:
        try:
            with open (self.store, 'r') as fp:
                return pickle.load(fp)
        except:
            return None

    def prod_save(self, key: str, case):
        """
        Persist the directory info to cross-session storage.
        """
        if case is not None:
            self.cases[key] = case
        the_redis = DARedis()
        the_redis.set_data(self.store, self.cases)

    def dev_save(self, key: str, case):
        if case is not None:
            self.cases[key] = case
        with open(self.store, 'w') as fp:
            pickle.dump(self.cases, fp)


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

    Args:
        case (Case): The case to process
    Returns:
        (str): The text to display.
    """
    return "{} - {} - {}".format(case.key, case.case_id, case.footer)


def main():
    o = UsCaseList()


if __name__ == '__main__':
    main()
