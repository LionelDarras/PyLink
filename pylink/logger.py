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


def active_logger():
    '''Initialize a speaking logger with stream handler (stderr).'''
    logger = logging.getLogger('pyvpdriver')

    logger.setLevel(logging.INFO)
    logging.getLogger('pylink').setLevel(logging.INFO)

    # Default to logging to stderr.
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s ')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logging.getLogger('pylink').addHandler(stream_handler)

    return logger

LOGGER = silent_logger()
