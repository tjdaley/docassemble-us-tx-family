"""
us_tx_courts.py - Retrieve a list of Courts in Texas.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import date
from lxml import html
import re
import requests
import json

DEV_MODE = False

# Change *VERSION* to force the cached *STORE* file to be refreshed.
VERSION = 'B'

if not DEV_MODE:
    from docassemble.base.core import DAFile
    from .ml_stripper import MLStripper
else:
    from ml_stripper import MLStripper

URL = 'https://statutes.capitol.texas.gov/Docs/GV/htm/GV.24.htm'
STORE = 'us_tx_courts.json'

class UsTxCourts(object):
    """
    Encapsulates the behavior of a datasource for district courts in Texas.
    """
    def __init__(self):
        """
        Initialize and instance.
        """
        self.courts_by_county = {}
        self.courts = None
        self.load()
    
    def load(self):
        """
        Load courts from a local store.
        """
        courts_info = self.read()
        if courts_info is None or courts_info['refresh_key'] != refresh_key():
            self.courts = self.retrieve()
            self.courts_by_county = self.county_list(self.courts)
            self.save(self.courts, self.courts_by_county)
        else:
            self.courts = courts_info['courts']
            self.courts_by_county = courts_info['by_county']

    def get_court(self, court_number: str) -> dict:
        """
        Retrieve a court by court number.

        Args:
            court_number (str): Court number to retrieve, e.g. "1", "416", etc.
        Returns:
            (str): Fields for this court or None if not found.
        """
        court = str(court_number).upper()
        if court in self.courts:
            return self.courts[court]
        return None

    def get_courts(self, county: str, show_jurisdiction: bool = True) -> list:
        """
        Retrieve a list of courts for the given county.

        Args:
            county (str): County to search for.
        Returns:
            (list): List of courts for this county or None if *county* not found.
        """
        county_idx = str(county).strip().upper()
        if county_idx in self.courts_by_county:
            if not show_jurisdiction:
                return self.courts_by_county[county_idx]
            return ["{} - {}".format(court, self.courts[court]['focus'])
                   for court in self.courts_by_county[county_idx]]
        return None

    def retrieve(self) -> dict:
        """
        Retrieve a list of courts for this state from the statute that authorizes them.
        """
        page = requests.get(URL)
        html = page.text
        courts = self.html2dict(html)
        return courts

    def html2dict(self, page_html: str):
        """
        Convert the html we retrieve from *URL_DISTRICT* to a dict.

        Args:
            page_html (str): HTML retrieved from *URL_DISTRICT*.
        Returns:
            (dict): dict indexed by court number.
        """
        result = {}

        stripper = MLStripper()
        stripper.feed(page_html)
        text = stripper.get_data()

        # Extract courts
        for court_number in range(1000):
            court_text = find_court(court_number, text)
            if court_text is not None:
                court_dict = parse_court_text(court_number, court_text)
                result[str(court_number)] = court_dict

        # Extract specializations, which can be funky in Harris County
        tree = html.fromstring(page_html)
        paragraphs = tree.xpath('//p//text()')
        search = r'\)\s*The(.*)[Dd]istrict [Cc]ourt[s]{0,1} shall give preference to ([a-zA-Z0-9,\s]*)\.'
        for paragraph in paragraphs:
            for match in re.finditer(search, paragraph, re.IGNORECASE):
                courts = extract_courts(match.group(1))
                focus = match.group(2)
                for court in courts:
                    result[court]['focus'] = focus
        search = r'The(.*)[Dd]istrict [Cc]ourt[s]{0,1} shall hear ([a-zA-Z0-9,\s]*)\.'
        for paragraph in paragraphs:
            for match in re.finditer(search, paragraph, re.IGNORECASE):
                courts = extract_courts(match.group(1))
                focus = match.group(2)
                for court in courts:
                    result[court]['focus'] = focus

        return result

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

    def prod_save(self, courts, courts_by_county):
        """
        Persist the list of counties to file storage.
        """
        outfile = DAFile()
        outfile.initialize(filename=STORE)
        outfile.set_attributes(persistent=True)
        outfile.write(json.dumps(cache_record(courts, courts_by_county)))

    def dev_save(self, courts, courts_by_county):
        with open(STORE, 'w') as fp:
            json.dump(cache_record(courts, courts_by_county), fp, indent=4)

    def county_list(self, courts: dict) -> dict:
        """
        Given a dict indexed by court number, return a dict indexed by county.

        Args:
            courts (dict): Dict of courts indexed by court number.
        Returns:
            (dict): a dict of lists of court numbers indexed by county name.
        """
        courts_by_county = {}
        for court, record in courts.items():
            for county in record['counties']:
                county_idx = str(county).strip().upper()
                if county_idx not in courts_by_county:
                    courts_by_county[county_idx] = []
                if court not in courts_by_county[county_idx]:
                    courts_by_county[county_idx].append(court)
        return courts_by_county


def cache_record(courts, courts_by_county):
    return {
                'courts': courts,
                'by_county': courts_by_county,
                'refresh_key': refresh_key()
    }


def ordinal(num: int) -> str:
    """
    Given an integer, return an ordinal, e.g. 1st, 2nd, 3rd, 4th, 5th, etc.
    """
    if int(('0'+str(num))[-2:]) in [11, 12, 13]:
        return str(num) + 'th'

    suffixes = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
    s = str(num)[-1]
    d = int(s)
    return str(num) + suffixes[d]


def find_court(court_number: int, text: str) -> str:
    """
    Find the statute that creates the given judicial district.

    Args:
        court_number (int): Judicial district number
        text (str): Text of government code.
    Returns:
        (str): Subset of *text* that relates to this *court_number* or None.
    """
    court_ord = ordinal(court_number)
    search_for = '{} JUDICIAL DISTRICT'.format(court_ord.upper())
    start_pos = text.find(search_for)
    if start_pos == -1:
        return None

    end_pos = text.find(', eff. ', start_pos)
    end_pos - text.find('\n', end_pos)
    return text[start_pos:end_pos-1]


def parse_court_text(court_number: int, text: str) -> dict:
    """
    Parse the statute that creates a court and return a dict
    describing the court.

    Args:
        court_number (int): Judicial district number.
        text (str): The statute that enables a district (from *find_court()*).
    Returns:
        (dict): Having court number, a list of counties, a list of
                specializations, and the year the district was established.
    """
    court = str(court_number)
    return {
        'court': court,
        'counties': court_counties(text),
        'focus': 'general jurisdiction',
        'year_established': court_year(text)
    }


def court_counties(text: str)-> list:
    search = 'Judicial District is composed of '
    start_pos = text.find(search) + len(search)
    end_pos = text.find('.', start_pos+1)
    counties = text[start_pos: end_pos] \
        .replace(', and ', ',') \
        .replace(' and ', ',') \
        .split(',')
    return [x.replace(' and ', '')
            .replace('County', '')
            .replace('Counties', '')
            .replace('county', '')
            .replace('counties', '')
            .strip() for x in counties]


def extract_courts(s: str)-> list:
    my_s = re.sub(r'[^0-9\s]', '', s)
    my_s = re.sub(r'\s{2,}', ' ', my_s)
    courts = my_s.strip().split(' ')
    result = []
    for court in courts:
        if court not in result:
            result.append(court)
    return sorted(result)


def court_jurisdictions(text: str)-> list:
    return []


def court_year(text: str)-> str:
    return ''

def refresh_key()-> str:
    """
    Returns the current year and month as yyyy-mm. The use
    of this refresh key will force the court list to be refreshed
    from the Texas Government code each month. That should be
    frequent enough to catch new courts as they are added by
    the legislature every other year.

    One might think we could get away with checking every month
    during odd-numbered years, but the Legislature is a strange
    operation . . . let's just be safe for now.
    """
    today = date.today()
    return '{}-{}-{}'.format(today.year, today.month, VERSION)


def main():
    o = UsTxCourts()
    print(o.get_court(470))
    print(o.get_courts('Collin'))
    print(refresh_key())


if __name__ == '__main__':
    main()