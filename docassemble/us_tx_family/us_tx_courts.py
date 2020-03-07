"""
us_tx_courts.py - Retrieve a list of Courts in Texas.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from datetime import date
from lxml import html
import re
import requests
import json

# We can get import errors in the test environment when we're doing very
# simple unit tests in an environment where the entire DocAssemble package
# has not been installed.
try:
    from docassemble.base.util import DARedis
    from docassemble.base.logger import logmessage
except ModuleNotFoundError:
    def logmessage(message: str):
        print(message)

from .ml_stripper import MLStripper
from .local_config import local_config

# Change *VERSION* to force the cached *STORE* file to be refreshed.
VERSION = 'B'

# The URL where we retrieve the statute that defines all district courts
URL = 'https://statutes.capitol.texas.gov/Docs/GV/htm/GV.24.htm'

# The file name or redis key where we store the parsed court information.
STORE = 'us_tx_courts.json'

# The highest district court number that we look for.
MAX_COURT_NUMBER = 1000


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
            (dict): Fields for this court or None if not found.
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
            (list): List of courts for this county or None if *county*
            not found.
        """
        county_idx = str(county).strip().upper()
        if county_idx in self.courts_by_county:
            if not show_jurisdiction:
                return self.courts_by_county[county_idx]
            return [(court, "{} - {}".format(ordinal(court), self.courts[court]['focus']).title())
                    for court in self.courts_by_county[county_idx]]
        return None

    def retrieve(self) -> dict:
        """
        Retrieve a list of courts for this state from the statute that
        authorizes them.
        """
        page = requests.get(URL)
        html = page.text
        courts = self.html2dict(html)
        return courts

    def html2dict(self, page_html: str) -> dict:
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
        # There are some gaps in the court numbers and, as of this day,
        # there is a huge gap between the numbers of the last two
        # courts. That's why I'm using a range.
        for court_number in range(max_court_number()):
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
        """
        Read the list of counties from local storage.
        """
        result = None
        try:
            the_redis = DARedis()
            result = the_redis.get_data(STORE)
        except Exception as e:
            logmessage(f"Unable to read cached list of courts: {str(e)}")
        return result

    def save(self, courts: dict, courts_by_county: dict) -> bool:
        """
        Persist the list of courts to local storage.

        Args:
            courts (dict): Dict of courts indexed by court id
            courts_by_county (dict): Dict where index is County and value is list of courts
        Returns:
            (bool): True if successful, otherwise False
        """
        try:
            the_redis = DARedis()
            the_redis.set_data(STORE, cache_record(courts, courts_by_county))
            return True
        except Exception as e:
            logmessage(f"Unable to cache list of courts: {str(e)}")
        return False

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

    Args:
        num (int): The number to convert to an ordinal
    Returns:
        (str): The ordinal of the *num* argument value.
    """
    try:
        court_num = int(num)
    except TypeError:
        return num

    # If the court number is at least two digits and ends in 11, 12, or 13,
    # the ordinal uses 'th'
    if int(('0'+str(num))[-2:]) in [11, 12, 13]:
        return str(num) + 'th'

    # All other ordinals are determined by the last digit of the number
    # which is used as an index into the suffixes[] list.
    suffixes = ['th', 'st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th']
    return str(num) + suffixes[court_num % 10]


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


def max_court_number():
    """
    Returns the maximum court number we will search for.
    """
    return local_config('max court number', MAX_COURT_NUMBER)


def court_counties(text: str) -> list:
    """
    Return a list of county names from the text of the statute.
    NOTE: This is highly dependent upon the writing style of the
    Texas Government Code, which, to date, is fairly consistent.

    Args:
        text (str): Text of statute to parse.
    Returns:
        (list): List of counties mentioned in the statute
    """
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


def extract_courts(s: str) -> list:
    """
    Extract a list of court numbers listed in the statute's text.

    Args:
        s (str): The text of the statute that lists the court numbers.
    Returns:
        (list): A list court numbers, all cleaned up.
    """
    my_s = re.sub(r'[^0-9\s]', '', s)
    my_s = re.sub(r'\s{2,}', ' ', my_s)
    courts = my_s.strip().split(' ')
    result = []
    for court in courts:
        if court not in result:
            result.append(court)
    return sorted(result)


def court_jurisdictions(text: str) -> list:
    return []


def court_year(text: str) -> str:
    """
    TODO: But why?
    """
    return ''


def refresh_key() -> str:
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
    version = local_config('court list version', VERSION)
    return '{}-{}-{}'.format(today.year, today.month, version)


if __name__ == '__main__':
    courtdb = UsTxCourts()
    courts = courtdb.get_courts('COLLIN')
    print(courts)
