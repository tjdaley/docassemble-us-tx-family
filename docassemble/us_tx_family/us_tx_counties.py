"""
us_tx_counties.py - Retrieve a list of Counties in Texas.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from lxml import html
import requests
import json
import os

URL = 'https://card.txcourts.gov/DirectorySearch.aspx'
STORE = '{}/us_tx_counties.json'.format(os.path.dirname(os.path.abspath(__file__)))
STORE = '~/us_tx_counties.json'

class UsTxCounties(object):
    """
    Encapsulates the behavior of a datasource for counties in Texas.
    """
    def __init__(self):
        """
        Initialize and instance.
        """
        self.counties = None
        self.source = None
        self.load()
    
    def load(self):
        """
        Load courts from a local store. If the local store does not exist,
        then load from the original web source.
        """
        try:
            with open(STORE, 'r') as fp:
                self.counties = json.load(fp)['counties']
                self.source = STORE
        except FileNotFoundError:
            self.counties = self.retrieve()
            self.save()
            self.source = URL
        except:
            self.counties = self.retrieve()
            self.save()
            self.source = URL

    def get_counties(self) -> list:
        """
        Retrieve a list of counties.

        Args:
            None.
        Returns:
            (list): List of counties in Texas.
        """
        return self.counties

    def retrieve(self):
        """
        Retrieve a list of courts for this state from the statute that authorizes them.
        """
        page = requests.get(URL)
        counties = self.html2list(page.content)
        return counties

    def html2list(self, page_html: str) -> list:
        """
        Convert the html we retrieve from *URL* to a list of counties.

        Args:
            page_html (str): HTML retrieved from *URL*.
        Returns:
            (list): List of counties
        """
        tree = html.fromstring(page_html)
        counties = tree.xpath('//select[@id="ctlCounty_ddlCounty"]//option//text()')
        # First name in the retrieved list is "All Counties". We don't need that.
        return counties[1:]

    def save(self):
        """
        Persist the list of courts to local storage.
        """
        with open(STORE, 'w') as fp:
            json.dump({'counties': self.counties}, fp)


def main():
    counties = UsTxCounties()
    print(counties.get_counties())
    print("Source:", counties.source)
    print(os.path.dirname(os.path.abspath(__file__)))


if __name__ == '__main__':
    main()
