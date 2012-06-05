# coding: utf8
"""
    pylink.logger
    -------------

    Logging setup.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD.

"""

from __future__ import unicode_literals

import logging

def silent_logger():
    '''Initialize a silent logger.'''
    logger = logging.getLogger('pylink')
    try:
        from logging import NullHandler
    except ImportError:
        class NullHandler(logging.Handler):
            def emit(self, record):
                pass
    logger.addHandler(NullHandler())
    return logger

LOGGER = silent_logger()
