"""
us_tx_courts.py - Retrieve a list of Courts in Texas.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from lxml import html
import requests
import json

URL = 'https://statutes.capitol.texas.gov/Docs/GV/htm/GV.24.htm'
STORE = './data/static/us_tx_courts.json'

class UsTxCourts(object):
    """
    Encapsulates the behavior of a datasource for district courts in Texas.
    """
    def __init__(self):
        """
        Initialize and instance.
        """
        self.courts_by_county = None
        self.courts_by_court = None
        self.load()
    
    def load(self):
        """
        Load courts from a local store.
        """
        with open(STORE, 'r') as court_file:
            courts = json.load(court_file)

        self.courts_by_court = courts
        for court in courts:
            for county in court['counties']:
                if county not in self.courts_by_county:
                    self.courts_by_county[county] = {}
                self.courts_by_county[county].append(court)

    def get_court(self, court_number: str) -> dict:
        """
        Retrieve a court by court number.

        Args:
            court_number (str): Court number to retrieve, e.g. "1", "416", etc.
        Returns:
            (str): Fields for this court or None if not found.
        """
        court = str(court_number).upper()
        if court in self.courts_by_court:
            return self.courts_by_court(court)
        return None

    def get_courts(self, county: str) -> list:
        """
        Retrieve a list of courts for the given county.

        Args:
            county (str): County to search for.
        Returns:
            (list): List of courts for this county or None if *county* not found.
        """
        county_idx = str(county).strip().upper()
        if county_idx in self.courts_by_county:
            return self.courts_by_county[county_idx]
        return None

    def retrieve(self):
        """
        Retrieve a list of courts for this state from the statute that authorizes them.
        """
        page = requests.get(URL)
        html = page.content
        courts = self.html2dict(html)
        self.courts_by_court = courts
        self.courts_by_county = self.county_list(courts)
        self.save()

    def html2dict(self, html: str) -> dict:
        """
        Convert the html we retrieve from *URL_DISTRICT* to a dict.

        Args:
            html (str): HTML retrieved from *URL_DISTRICT*.
        Returns:
            (dict): dict indexed by court number.
        """
        tree = html.fromstring(html)

        return {}

    def save(self):
        """
        Persist the list of courts to local storage.
        """
        with open(STORE, 'w') as court_file:
            json.dump(self.courts_by_court, court_file)

    def county_list(self, courts: dict) -> dict:
        """
        Given a dict indexed by court number, return a dict indexed by county.

        Args:
            courts (dict): Dict of courts indexed by court number.
        Returns:
            (dict): a dict of lists of court numbers indexed by county name.
        """
        result = {}
        for court in courts:
            for county in court['counties']:
                if county not in result:
                    result[county] = []
                result[county].append(court['court_number'])

        return result

                