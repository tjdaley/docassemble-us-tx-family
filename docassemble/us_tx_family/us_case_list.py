"""
us_case_list.py - CRUD-provider fro a user's case list

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import date
import json
import pickle
import uuid
import sys

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
        self.user_id = user_id  # .replace('@', '_').replace('.', '_', 1)
        self.store = STORE.format(self.user_id)
        self.load()
    
    def load(self):
        """
        Load cases from a local store.
        """
        self.cases = self.read() or {}

    def get_cases(self):
        case_list = [(case['key'], case) for case in self.cases.items()]
        logmessage(str(case_list))
        return case_list

    def get_case(self, key: str):
        return self.cases.get(str, None)

    def dalist_of_individuals(self, directory: list):
        """
        Converts a list of Python dicts into a DAList of Individual instances.

        Args:
            directory (list): List of dicts where each dict defines a person.
        Returns:
            DAList: List of instances of Individual
        """
        individuals = []
        for entry in directory:
            address = Address()
            address.init(
                address=entry.get('address'),
                city=entry.get('city'),
                state='TX',
                zip=entry.get('zip code'),
                country='US'
            )
            name = IndividualName()
            name.init(
                first=entry.get('first name'),
                middle=entry.get('middle name'),
                last=entry.get('last name'),
                suffix=entry.get('suffix')
            )
            individual = Individual()
            individual.init(
                name=name,
                address=address,
                title=entry.get('title'),
                phone=entry.get('phone'),
                email=entry.get('email'),
                ou=entry.get('court')
            )
            individuals.append(individual)
        result = DAList()
        result.init(object_type=Individual, elements=individuals)
        return result

    def read(self) -> dict:
        if DEV_MODE:
            cases = self.dev_read()
        else:
            cases = self.prod_read()
        logmessage("Retrieved {} cases from {}.".format(len(cases or []), self.store))
        return cases

    def save(self, case) -> bool:
        """
        Save a case.
        """
        key = case_key(case)
        case.key = key
        if DEV_MODE:
            return self.dev_save(key, case)
        return self.prod_save(key, case)

    def prod_read(self) -> dict:
        """
        Read the list of cases for this user from file storage.
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
        Persist the directory info to file storage.
        """
        self.cases[key] = case
        the_redis = DARedis()
        the_redis.set_data(self.store, self.cases)

    def dev_save(self, key: str, case):
        self.cases[key] = case
        with open(self.store, 'w') as fp:
            pickle.dump(self.cases, fp)


def case_key(case):
    """
    Create a unique key for this case.
    """
    if hasattr(case, 'key'):
        return case.key
    case_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'attorney.bot'))
    return case_id


def main():
    o = UsCaseList()


if __name__ == '__main__':
    main()
