# -*- coding: utf-8 -*-
'''
    pylink
    ------

    The public API to pylink.

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

'''
VERSION = '0.3.1'
__version__ = VERSION

from .link import TCPLink, SerialLink, UDPLink, GSMLink
from .logger import LOGGER, active_logger


def link_from_url(url):
    '''Get link from url'''
    link = None
    bad_url = False
    args = url.split(':')
    try:
        if len(args) > 1:
            mode = args[0].lower()
            if mode == "gsm":
                phone = args[1]
                parent_link = link_from_url(':'.join(args[2:]))
                link = GSMLink(phone, parent_link)
            if mode == "tcp" or mode == "udp":
                host = args[1]
                port = int(args[2])
                if mode == "tcp":
                    link = TCPLink(host, port)
                else:
                    link = UDPLink(host, port)
            elif mode == "serial":
                if len(args) == 2:
                    port = args[1]
                    link = SerialLink(port)
                elif len(args) == 3:
                    port = args[1]
                    baudrate = int(args[2])
                    link = SerialLink(port, baudrate)
                elif len(args) == 4:
                    port = args[1]
                    baudrate = int(args[2])
                    bytesize = int(args[3][0])
                    parity = args[3][1]
                    stopbits = int(args[3][2])
                    link = SerialLink(port, baudrate, bytesize, parity,
                                      stopbits)
    except IndexError:
        bad_url = True
    if link is None or bad_url:
        raise ValueError('Bad url link sepecified')
    return link
