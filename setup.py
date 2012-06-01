# coding: utf8
"""
    pylink
    ------

    Universal communication interface using File-Like API.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD.

"""

import sys
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

README = ''
CHANGES = ''
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()
except:
    pass

REQUIREMENTS = [
    'pyserial',
]

setup(
    name='PyLink',
    version='0.1',
    url='https://github.com/SalemHarrache/PyLink',
    license='BSD',
    description='Universal communication interface using File-Like API',
    long_description=README + '\n\n' + CHANGES,
    author='Salem Harrache',
    author_email='contact@salem.harrache.info',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    packages=find_packages(),
    zip_safe=False,
    install_requires=REQUIREMENTS,
    test_suite='pylink.tests',
)
