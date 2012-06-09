# -*- coding: utf-8 -*-
'''
    pylink.link
    -----------

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD.

'''

from __future__ import unicode_literals

import sys
import socket
import time
import serial
import binascii

# Type compatibilite between python3 and python2
if sys.version_info[0] >= 3:
    # Python 3
    text_type = str
    byte_type = bytes
else:
    # Python 2
    text_type = unicode
    byte_type = str

from .logger import LOGGER


class Link(object):
    '''Abstract base class for all links.'''
    MAX_STRING_SIZE = 4048

    def open(self):
        '''Open the link.'''
        pass

    def close(self):
        '''Close the link.'''
        pass

    def byte_to_hex(self, bytes):
        '''Convert a byte string to it's hex string representation.'''
        if sys.version_info[0] >= 3:
            hexstr = str(binascii.hexlify(bytes), "utf-8")
        else:
            hexstr = str(binascii.hexlify(bytes))
        data = []
        for i in range(0, len(hexstr), 2):
            data.append("%s" % hexstr[i:i + 2].upper())
        return ' '.join(data)

    def log(self, message, data):
        if self.is_bytes(data):
            LOGGER.info("%s : <%s>" % (message, self.byte_to_hex(data)))
        else:
            LOGGER.info("%s : <%s>" % (message, repr(data)))

    def is_text(self, data):
        return isinstance(data, text_type)

    def is_bytes(self, data):
        return isinstance(data, byte_type)

    def __del__(self):
        '''Close link when object is deleted.'''
        self.close()

    def __unicode__(self):
        name = self.__class__.__name__
        return "<%s %s>" % (name, self.url)

    def __str__(self):
        return str(self.__unicode__())

    def __repr__(self):
        return str(self.__unicode__())


class TCPLink(Link):
    '''TCPLink class allows TCP/IP protocol communication with File-like
    API.'''
    def __init__(self, host, port, timeout=1):
        self.timeout = timeout
        self.host = socket.gethostbyname(host)
        self.port = port
        self._socket = None

    @property
    def address(self):
        '''Return a tuple of (`host`, `port`).'''
        return (self.host, self.port)

    @property
    def url(self):
        '''Make a connection url from `host` and `port`.'''
        return 'tcp:%s:%d' % self.address

    def open(self):
        '''Open the socket.'''
        if self._socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect(self.address)
            self.socket.setblocking(0)
            LOGGER.info('new %s was initialized' % self)

    def settimeout(self, timeout):
        self.timeout = timeout

    def close(self):
        '''Close the socket.'''
        if self._socket is not None:
            LOGGER.info('Close connection %s' % self)
            self.empty_socket()
            self._socket.close()
            LOGGER.info('Connection %s was closed' % self)
            self._socket = None

    @property
    def socket(self):
        '''Return an opened socket object.'''
        self.open()
        return self._socket

    def write(self, data):
        '''Write all `data` to socket.'''
        if self.is_text(data):
            self.send_to_socket(byte_type(data.encode('utf-8')))
        else:
            self.send_to_socket(data)
        self.log("Write", data)

    def read(self, size=None, timeout=None):
        '''Read data from socket. The maximum amount of data to be received at
        once is specified by `size`. If `is_byte` is True, the data will be
        convert to hexadecimal array.'''
        size = size or self.MAX_STRING_SIZE
        timeout = (timeout or 1) * (self.timeout or 1)
        data = self.recv_timeout(size, timeout)
        self.log("Read", data)
        return data

    def recv_timeout(self, size, timeout):
        '''Uses a non-blocking sockets in order to continue trying to get data
        as long as the client manages to even send a single byte.
        This is useful for moving data which you know very little about
        (like encrypted data), so cannot check for completion in a sane way.

        http://code.activestate.com/recipes/408859-socketrecv-three-ways-to-turn-it-into-recvall/
        '''
        begin = time.time()
        data = bytearray()
        total_data = []
        while True:
            #if you got some data, then break after wait sec
            if total_data and time.time() - begin > timeout:
                break
            #if you got no data at all, wait a little longer
            elif time.time() - begin > timeout * 2:
                break
            try:
                data = self.recv_from_socket(size)
                if data:
                    total_data.append(data)
                    size = size - len(data)
                    if size == 0:
                        break
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                # just need to get out of recv form time to time to check if
                # still alive
                time.sleep(0.1)
                pass
        # Try to convert into str
        try:
            return text_type("".join(total_data), encoding='utf8')
        except:
            return b"".join(total_data)

    def send_to_socket(self, data):
        '''Send data to TCP socket.'''
        self.socket.sendall(data)

    def recv_from_socket(self, size):
        '''Read data from TCP socket.'''
        return self.socket.recv(size)

    def empty_socket(self):
        '''Read data from TCP socket.'''
        # empty buffer reception
        self.recv_timeout(self.MAX_STRING_SIZE, timeout=0.1)


class UDPLink(TCPLink):
    '''TCPLink class allows UDP/IP protocol communication with File-like
    API.'''

    @property
    def url(self):
        '''Make a connection url from `host` and `port`.'''
        return 'udp:%s:%d' % self.address

    def open(self):
        '''Open the socket.'''
        if self._socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            LOGGER.info('new %s was initialized' % self)

    def send_to_socket(self, data):
        '''Send data to TCP socket.'''
        self.socket.sendto(data, self.address)

    def recv_from_socket(self, size):
        '''Read data from TCP socket.'''
        data, address = self.socket.recvfrom(size)
        if address == self.address:
            return data


class SerialLink(Link):
    '''SerialLink class allows serial communication with File-like API.
    Possible values for the parameter port:
      - Number: number of device, numbering starts at zero.
      - Device name: depending on operating system.
          e.g. /dev/ttyUSB0 on GNU/Linux or COM3 on Windows.'''
    def __init__(self, port, baudrate=19200, bytesize=8, parity='N',
                                             stopbits=1, timeout=1):
        self.port = port
        self.timeout = timeout
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.parity = parity
        self.stopbits = stopbits
        self._serial = None

    @property
    def url(self):
        '''Make a connection url.'''
        return 'serial:%s:%d:%d%s%d' % (self.port, self.baudrate,
                                          self.bytesize, self.parity,
                                          self.stopbits)

    def open(self):
        '''Open the serial connection.'''
        if self._serial is None:
            self._serial = serial.Serial(self.port, self.baudrate,
                                    timeout=self.timeout,
                                    bytesize=self.bytesize, parity=self.parity,
                                    stopbits=self.stopbits)
            LOGGER.info('new %s was initialized' % self)

    def settimeout(self, timeout):
        self.timeout = timeout
        self.serial.timeout = self.timeout

    def close(self):
        '''Close the serial connection.'''
        if self._serial is not None:
            if self._serial.isOpen():
                self._serial.close()
                LOGGER.info('Connection %s was closed' % self)
            self._serial = None

    @property
    def serial(self):
        '''Return an opened serial object.'''
        self.open()
        return self._serial

    def write(self, data, is_byte=False):
        '''Write all `data` to the serial connection.'''
        self.serial.write(data)
        self.log("Write", data, is_byte)

    def read(self, size=None, is_byte=False):
        '''Read data from the serial connection. The maximum amount of data
        to be received at once is specified by `size`. If `is_byte` is True,
        the data will be convert to byte array.'''
        size = size or self.MAX_STRING_SIZE
        data = self.serial.read(size)
        self.log("Read", data, is_byte)
        return data
