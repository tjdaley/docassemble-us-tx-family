"""
ml_stripper.py - Strip HTML entities from HTML pages.

From:
https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
https://stackoverflow.com/questions/11061058/using-htmlparser-in-python-3-2

Usage:
```python
stripper = MLStripper()
stripper.feed(html_content)
tag_free_content = stripper.get_data()
```
"""
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)