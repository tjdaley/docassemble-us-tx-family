"""
local_config.py - A function to get a configuration parameter specific to our package.

Copyright (c) 2020 by Thomas J. Daley, J.D. All Rights Reserved
"""
from docassemble.base.functions import get_config

__all__ = ['local_config']

def local_config(param_name: str, default, dev_mode: bool = False):
    if dev_mode:
        return default
    config = get_config('us-tx-family')
    if not config:
        return default
    return config.get(param_name, default)


