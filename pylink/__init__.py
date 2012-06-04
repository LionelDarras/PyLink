# -*- coding: utf-8 -*-
'''
    pylink
    ------

    The public API to pylink.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD.

'''
VERSION = '0.1dev'
__version__ = VERSION

from .link import TCPLink, SerialLink, UDPLink
from .logger import LOGGER


def link_from_url(url):
    '''Get link from url'''
    link = None
    args = url.split(':')
    if len(args) > 1:
        mode = args[0].lower()
        if mode == "tcp":
            host = args[1]
            port = int(args[2])
            link = TCPLink(host, port)
        elif mode == "serial":
            if len(args) == 2:
                port = args[1]
                link = SerialLink(port)
            elif len(args) == 3:
                port = args[1]
                baudrate = int(args[2])
                link = SerialLink(port, baudrate)
            elif len(link_args) == 4:
                port = link_args[1]
                baudrate = int(link_args[2])
                bytesize=int(link_args[3][1])
                parity= link_args[3][2]
                stopbits= int(link_args[3][3])
                link = SerialLink(port, baudrate, bytesize, parity,
                                        stopbits, timeout)
    if link is None:
        raise ValueError('Bad url link sepecified')
    else:
        return link
