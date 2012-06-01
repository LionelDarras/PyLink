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

def init_logger():
    '''Initialize logger.'''
    logger = logging.getLogger('pylink')

    # Default to logging to stderr.
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s ')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)

    return logger

LOGGER = init_logger()
