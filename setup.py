import os
import sys
from setuptools import setup, find_packages
from fnmatch import fnmatchcase
from distutils.util import convert_path

standard_exclude = ('*.py', '*.pyc', '*~', '.*', '*.bak', '*.swp*')
standard_exclude_directories = (
    '.*',
    'CVS',
    '_darcs',
    './build',
    './dist',
    'EGG-INFO',
    '*.egg-info'
)

VERSION = "0.0.9"


def find_package_data(
    where='.',
    package='',
    exclude=standard_exclude,
    exclude_directories=standard_exclude_directories
):
    out = {}
    stack = [(convert_path(where), '', package)]
    while stack:
        where, prefix, package = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where, name)
            if os.path.isdir(fn):
                bad_name = False
                for pattern in exclude_directories:
                    if (fnmatchcase(name, pattern)
                       or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                if os.path.isfile(os.path.join(fn, '__init__.py')):
                    if not package:
                        new_package = name
                    else:
                        new_package = package + '.' + name
                        stack.append((fn, '', new_package))
                else:
                    stack.append((fn, prefix + name + '/', package))
            else:
                bad_name = False
                for pattern in exclude:
                    if (fnmatchcase(name, pattern)
                       or fn.lower() == pattern.lower()):
                        bad_name = True
                        break
                if bad_name:
                    continue
                out.setdefault(package, []).append(prefix+name)
    return out


setup(
    name='docassemble.us_tx_family',
    version=VERSION,
    description=('A docassemble extension for Texas Family Law cases by Thomas J. Daley, J.D.'),
    long_description=u"""# docassemble-us-tx-family
    A docassemble extension for Texas Family Law cases by Thomas J. Daley, J.D.

    ## Version History

    * 0.0.1 - Development/Test version.
    * 0.0.2 - Set up basic classes
    * 0.0.3 - Create objects and functions
    * 0.0.4 - First attempt at persistence to file system
    * 0.0.5 - Moved persistence to Redis
    * 0.0.6 - Began case management
    * 0.0.7 - Set up scraping classes to populate counties, courts, etc.
    * 0.0.8 - Persisted scape results to Redis
    * 0.0.9 - First useful version
    """,
    long_description_content_type='text/markdown',
    author='Thomas J. Daley, J.D.',
    author_email='tom@powerdaley.com',
    license='The MIT License (MIT)',
    url='https://github.com/tjdaley/docassemble-us-tx-family',
    packages=find_packages(),
    namespace_packages=['docassemble'],
    install_requires=[],
    zip_safe=False,
    package_data=find_package_data(where='docassemble/us_tx_family/',
                                   package='docassemble.us_tx_family'),
)
