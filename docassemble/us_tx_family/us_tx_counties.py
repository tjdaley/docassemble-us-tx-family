"""
us_tx_counties.py - Retrieve a list of Counties in Texas.

The first user invokes an interview that asks for the name of a county,
a list of counties will be retrieved from *URL* and cached. After that,
all requests will use the original cached version. This assumes that
there will be no changes to Texas County names. Ever.

We're retrieving a list of counties from a web-based UX. It's implemented
as an ASP and for both of these reasons, the list may be a little
fragile. Because of the potential fagility, we don't go checking this
list on a regular basis.

Copyright (c) 2019 by Thomas J. Daley, J.D. All Rights Reserved.
"""
from lxml import html
import requests
import json

from docassemble.base.util import DARedis

URL = 'https://card.txcourts.gov/DirectorySearch.aspx'
STORE = 'us_tx_counties.json'

class UsTxCounties(object):
    """
    Encapsulates the behavior of a datasource for counties in Texas.
    """
    def __init__(self):
        """
        Initialize and instance.
        """
        self.counties = self.load()
    
    def load(self) -> list:
        """
        Load courts from a local store. If the local store does not exist,
        then load from the original web source.
        """
        counties = self.read()
        if counties is None:
            counties = self.retrieve()
        return counties

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
        Retrieve a list of counties from the state's search screen and save
        them to file storage.
        """
        page = requests.get(URL)
        counties = self.html2list(page.content)
        self.save(counties)
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

    def read(self) -> dict:
        """
        Read the list of counties from file storage.
        """
        the_redis = DARedis()
        result = the_redis.get_data(STORE)
        return result

    def save(self, counties):
        """
        Persist the list of counties to file storage.
        """
        the_redis = DARedis()
        the_redis.set_data(STORE, counties)


def main():
    counties = UsTxCounties()
    print(counties.get_counties())


if __name__ == '__main__':
    main()
