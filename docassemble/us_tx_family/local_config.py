"""
local_config.py - A function to get a configuration parameter specific to our
package.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved.
"""
try:
    from docassemble.base.functions import get_config
except Exception:
    # In develpment, we don't have the docassemble api installed.
    # This code mimics the docassemble get_config() function
    # for testing on my local workstation. TJD 2020-02-11
    import os

    class EnvironConfig(object):
        def get(self, param_name: str, default) -> str:
            lookup_name = param_name.replace(' ', '')
            if param_name in os.environ:
                return os.environ[lookup_name]
            print(f"get_config(): Environment variable '{lookup_name}' not found. Returning default of '{default}'")
            return default

    def get_config(environment):
        # environment is ignored
        config = EnvironConfig()
        return config

__all__ = ['local_config']


def local_config(param_name: str, default=None, dev_mode: bool = False):
    if dev_mode:
        return default
    config = get_config('us-tx-family')
    if not config:
        return default
    return config.get(param_name, default)
