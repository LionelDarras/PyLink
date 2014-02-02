# -*- coding: utf-8 -*-
'''
    pylink.test_links
    -----------------------

    The pylink test suite.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD.

'''
from __future__ import unicode_literals
import pytest
from contextlib import contextmanager

from .link import TCPLink, UDPLink
from . import link_from_url
from .logger import active_logger


active_logger()


@contextmanager
def assert_raises(exception_class, message_part):
    """
    Check that an exception is raised and its message contains some string.
    """
    with pytest.raises(exception_class) as exception:
        yield
    message = '%s' % exception
    assert message_part.lower() in message.lower()


class TestUDPLink(object):
    '''Suite test for UDP Link'''

    def setup_class(self):
        '''Setup common data.'''
        # echo service
        self.echo_link = UDPLink('localhost', 7)

    def test_address(self):
        '''Test resolution address.'''
        assert self.echo_link.address == ("127.0.0.1", 7)

    def test_hello_echo(self):
        '''Test echo.'''
        self.echo_link.write("hello")
        assert self.echo_link.read(5) == "hello"
        self.echo_link.write(b'\x06\xFF')
        assert self.echo_link.read(2) == b'\x06\xFF'
        self.echo_link.write(b'\x06\xFF')
        assert self.echo_link.read(2) == b'\x06\xFF'


class TestTCPLink(object):
    '''Suite test for TCP Link'''
    def setup_class(self):
        '''Setup common data.'''
        # echo service
        self.echo_link = TCPLink('localhost', 7)

    def test_address(self):
        '''Test resolution address.'''
        assert self.echo_link.address == ("127.0.0.1", 7)

    def test_hello_echo(self):
        '''Test echo.'''
        self.echo_link.write("hello")
        assert self.echo_link.read(5) == "hello"
        self.echo_link.write(b'\x06\xFF')
        assert self.echo_link.read(2) == b'\x06\xFF'
        self.echo_link.write(b'\x06\xFF')
        assert self.echo_link.read(2) == b'\x06\xFF'

    def test_web_connection(self):
        '''Test internet connection.'''
        link = TCPLink('docs.python.org', 80)
        link.write('GET / HTTP 1.1\n\n')
        data = link.read(4)
        print(link.address)
        assert data == "HTTP"


def test_link_from_url():
    '''Test parssing link from url.'''
    link = link_from_url("tcp:localhost:7")
    link.write("hello")
    assert link.read(5) == "hello"
    with assert_raises(ValueError, 'Bad url link sepecified'):
        assert link_from_url('')
    with assert_raises(ValueError, 'invalid literal for int'):
        assert link_from_url('tcp:localhost:10.3')
    with assert_raises(ValueError, 'Bad url link sepecified'):
        assert link_from_url('unknow:/dev/ttyUSB0')
