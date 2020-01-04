"""
us_tx_court_directory.py - Retrieve a list of court personel in Texas.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import date
import re
import requests
import json

DEV_MODE = False

# Change *VERSION* to force the cached *STORE* file to be refreshed.
VERSION = 'A'

if not DEV_MODE:
    from docassemble.base.core import DAFile, DAList
    from docassemble.base.util import Individual, IndividualName, Address

URL = 'https://card.txcourts.gov/ExcelExportPublic.aspx?type=P&export=E&CommitteeID=0&Court=&SortBy=tblCounty.Sort_ID,%20Last_Name&Active_Flg=true&Last_Name=&First_Name=&Court_Type_CD=55&Court_Sub_Type_CD=0&County_ID=0&City_CD=0&Address_Type_CD=0&Annual_Report_CD=0&PersonnelType1=&PersonnelType2=&DistrictPrimaryLocOnly=1&AdminJudicialRegion=0&COADistrictId=0'
STORE = 'us_tx_court_directory.json'

class UsTxCourtDirectory(object):
    """
    Encapsulates the behavior of a datasource for district court personel in Texas.
    """
    def __init__(self):
        """
        Initialize and instance.
        """
        self.courts = {}  # Indexed by judicial district number
        self.clerks = {}  # Indexed by uppercased county name
        self.load()
    
    def load(self):
        """
        Load courts from a local store.
        """
        directory_info = self.read()
        if directory_info is None or directory_info['refresh_key'] != refresh_key():
            courts, clerks = self.retrieve()
            self.courts = courts
            self.clerks = clerks
            self.save(courts, clerks)
        else:
            self.courts = directory_info['courts']
            self.clerks = directory_info['clerks']

    def get_court(self, court_number: str) -> list:
        """
        Retrieve directory information for a court by court number.

        Args:
            court_number (str): Court number to retrieve, e.g. "1", "416", etc.
        Returns:
            (str): Fields for this court or None if not found.
        """
        court_idx = court_index(court_number)
        if court_idx in self.courts:
            if DEV_MODE:
                return self.courts[court_idx]
            return self.dalist_of_individuals(self.courts[court_idx])
        return None

    def get_clerk(self, county: str) -> list:
        """
        Retrieve directory information for district clerk's office.

        Args:
            county (str): Name of county to search.
        Returns:
            (list): List of district clerk personnel (probably only one)
        """
        county_idx = county_index(county)
        if county_idx in self.clerks:
            if DEV_MODE:
                return self.clerks[county_idx]
            return self.dalist_of_individuals(self.clerks[county_idx])
        return None

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
                country='US')
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

    def retrieve(self) -> dict:
        """
        Retrieve a list of courts for this state from the statute that authorizes them.
        """
        page = requests.get(URL)
        tsv = page.text
        courts, clerks = self.tsv2dict(tsv)
        return courts, clerks

    def tsv2dict(self, tsv: str):
        """
        Convert the html we retrieve from *URL* to a dict.

        Args:
            tsv (str): tab-separated data retrieved from *URL*.
        Returns:
            (dict): courts indexed by court number, clerks indexed by county
        """
        courts = {}
        clerks = {}

        lines = [l.replace('\r', '') for l in tsv.split('\n') if len(l) > 10]
        header = lines[0]
        headers = [h.lower().strip() for h in header.split('\t') if h.strip() != '']
        len_headers = len(headers)
        for line in lines[1:]:
            cols = [c.strip() for c in line.split('\t')]

            # Skip mal-formed records
            if len(cols) != len_headers:
                # print(cols)
                continue

            person = {}
            for idx, header_text in enumerate(headers) :
                person[header_text] = cols[idx]

            court_idx = court_index(person['court'])
            if court_idx:
                # We have a court person
                if court_idx not in courts:
                    courts[court_idx] = []
                courts[court_idx].append(person)
            elif person['court'].lower().strip() == 'district clerk office':
                # We have a district clerk person
                county_idx = county_index(person['county'])
                if county_idx not in clerks:
                    clerks[county_idx] = []
                clerks[county_idx].append(person)
        return courts, clerks
            
    def read(self) -> dict:
        if DEV_MODE:
            return self.dev_read()
        return self.prod_read()

    def save(self, a, b):
        if DEV_MODE:
            return self.dev_save(a, b)
        return self.prod_save(a, b)

    def prod_read(self) -> dict:
        """
        Read the list of counties from file storage.
        """
        infile = DAFile()
        infile.initialize(filename=STORE)
        try:
            json_text = infile.slurp()
            result = json.loads(json_text)
        except:
            result = None
        return result

    def dev_read(self) -> dict:
        try:
            with open (STORE, 'r') as fp:
                return json.load(fp)
        except:
            return None

    def prod_save(self, courts, clerks):
        """
        Persist the directory info to file storage.
        """
        outfile = DAFile()
        outfile.initialize(filename=STORE)
        outfile.set_attributes(persistent=True)
        outfile.write(json.dumps(cache_record(courts, clerks)))

    def dev_save(self, courts, clerks):
        with open(STORE, 'w') as fp:
            json.dump(cache_record(courts, clerks), fp, indent=4)


def county_index(county: str) -> str:
    """
    Transform a string into a form used to index something by county.

    Args:
        county (str): Name of county
    Returns:
        (str): Transformed name to be used as a dict index.
    """
    return str(county).strip().upper().replace(' COUNTY', '')


def court_index(court: str) -> str:
    """
    Transform a string given as a court into the form we use
    to index something by court number.

    Args:
        court (str): Court number
    Returns:
        (str): Transformed name to be used as a dict index.
    """
    court_str = str(court)
    regex = r'^(\d{1,3})'
    matches = re.match(regex, court_str)
    if matches:
        return matches.group(1)
    return None


def cache_record(courts, clerks):
    return {
                'courts': courts,
                'clerks': clerks,
                'refresh_key': refresh_key()
    }


def refresh_key()-> str:
    """
    Returns the current date as yyyy-mm-dd. The use
    of this refresh key will force the directory to be refreshed
    from txcourts.gov each day. That should be
    frequent enough to catch new courts as they are added by
    the legislature every other year and personnel changes that can
    happen on a moment's notice.
    """
    today = date.today()
    return '{}-{}-{}-{}'.format(today.year, today.month, today.day, VERSION)


def main():
    o = UsTxCourtDirectory()
    print("*"*40)
    print(o.get_court(470))
    print("*"*40)
    print(o.get_court('416th District court'))
    print("*"*40)
    print(o.get_clerk('collin'))
    print("*"*40)
    print(refresh_key())
    print("*"*40)


if __name__ == '__main__':
    main()
