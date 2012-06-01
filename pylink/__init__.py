# -*- coding: utf-8 -*-
'''
    pylink
    ------

    The public API to pylink.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD.

'''

# Make sure the logger is configured early:
from .logger import LOGGER
from .link import TCPLink, SerialLink

VERSION = '0.1dev'
__version__ = VERSION
