"""
us_case_list.py - CRUD-provider fro a user's case list

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import date
import json
import pickle
import uuid

DEV_MODE = True

if not DEV_MODE:
    from docassemble.base.core import DAFile, DAList
    from docassemble.base.util import Individual, IndividualName, Address

STORE = 'us_case_list-{}.json'

class UsCaseList(object):
    """
    Encapsulates the behavior of a datasource for district court personel in Texas.
    """
    def __init__(self, user_id: str):
        """
        Initialize and instance.
        """
        self.cases = {}
        self.user_id = user_id
        self.load()
    
    def load(self):
        """
        Load cases from a local store.
        """
        self.cases = self.read() or {}

    def get_cases(self):
        return [(case, 'key') for case in self.cases.items()]

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
            return self.dev_read()
        return self.prod_read()

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
        infile = DAFile()
        store = STORE.format(self.user_id)
        infile.initialize(filename=store)
        try:
            pickle_text = infile.slurp()
            result = pickle.loads(pickle_text)
        except:
            result = None
        return result

    def dev_read(self) -> dict:
        try:
            store = STORE.format(self.user_id)
            with open (store, 'r') as fp:
                return pickle.load(fp)
        except:
            return None

    def prod_save(self, key: str, case):
        """
        Persist the directory info to file storage.
        """
        self.cases[key] = case
        outfile = DAFile()
        store = STORE.format(self.user_id)
        outfile.initialize(filename=store)
        outfile.set_attributes(persistent=True)
        outfile.write(pickle.dumps(self.cases))

    def dev_save(self, key: str, case):
        store = STORE.format(self.user_id)
        self.cases[key] = case
        with open(store, 'w') as fp:
            pickle.dump(self.cases, fp)


def case_key(case):
    """
    Create a unique key for this case.
    """
    if hasattr(case, 'key'):
        return case.key
    case_id = uuid.uuid3(uuid.NAMESPACE_DNS, 'attorney.bot')
    return case_id


def main():
    o = UsCaseList()


if __name__ == '__main__':
    main()
