# -*- coding: utf-8 -*-
'''
    pylink.link
    -----------

    :copyright: Copyright 2012 Salem Harrache and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

'''
from __future__ import unicode_literals
import socket
import time
import serial
import binascii

from .logger import LOGGER
from .compat import bytes, str, format_string


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
        hexstr = str(binascii.hexlify(bytes), "utf-8")
        data = []
        for i in range(0, len(hexstr), 2):
            data.append("%s" % hexstr[i:i + 2].upper())
        return ' '.join(data)

    def log(self, message, data):
        if not self.is_text(data):
            LOGGER.info("%s : <%s>" % (message, self.byte_to_hex(data)))
        else:
            LOGGER.info("%s : <%s>" % (message, repr(data)))

    def is_text(self, data):
        return isinstance(data, str)

    def is_bytes(self, data):
        return isinstance(data, bytes)

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
            self.send_to_socket(bytes(data.encode('utf-8')))
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
        if len(data) != 0 :
            self.log("Read", data)
        return data

    def recv_timeout(self, size, timeout):
        '''Uses a non-blocking sockets in order to continue trying to get data
        as long as the client manages to even send a single byte.
        This is useful for moving data which you know very little about
        (like encrypted data), so cannot check for completion in a sane way.
        '''
        begin = time.time()
        data = bytearray()
        total_data = []
        while True:
            #if you got some data, then break after wait sec
            if total_data and time.time() - begin > timeout:
                break
            #if you got no data at all, wait a little longer
            elif time.time() - begin > (timeout * 2):
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
                pass
        # Try to convert into str
        try:
            return str(b"".join(total_data), encoding='utf8')
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
                                         bytesize=self.bytesize,
                                         parity=self.parity,
                                         stopbits=self.stopbits)
            self._serial.reset_output_buffer()
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

    def write(self, data):
        '''Write all `data` to the serial connection.'''
        data = format_string(data)
        self.serial.write(data)
        try:
            self.log("Write", str(data, encoding='utf8'))
        except:
            self.log("Write", data)

    def read(self, size=None, timeout=None):
        '''Read data from the serial connection. The maximum amount of data
        to be received at once is specified by `size`. If `is_byte` is True,
        the data will be convert to byte array.'''
        size = size or self.MAX_STRING_SIZE
        timeout = (timeout or 1) * (self.timeout or 1)
        self.serial.timeout = timeout
        data = self.serial.read(size)
        try:
            data = str(data, encoding='utf8')
        except:
            pass
        if len(data) != 0 :
            self.log("Read", data)
        self.serial.timeout = self.timeout
        return data


class GSMLink(Link):
    '''GSM link class.'''

    def __init__(self, phone, link,timeout=1):      #EGC added timeout (the aplication throws an error if the object doesn't have an attribute when call packbus read method)
        self.link = link
        self.phone = phone
        self.is_open = False
        self.timeout = timeout  #EGC set timeout

    def _call(self):
        LOGGER.info("GSM : Call %s" % self.phone)
        self.link.write("ATD%s\r\n" % self.phone)
        for i in range(100):	#EGC Change While to For (While never ends, in case of error program won't stop, infinite loop)
            response = self.link.read(22)
            if ("BUSY" in response or "NO CARRIER" in response
                    or "ERROR" in response):
                LOGGER.error("GSM : <%s>" % repr(response))
                return False
            if "CONNECT" in response:
                self.log("GSM", "Client is ready (%s)" % response)
                self.link.read()
                return True
            self.log("GSM", "call in progress")
            time.sleep(1)
        return False

    def _hangup(self):      
        #EGC my modem (Citerion (formerly SIEMENS) gprs mc35i) send two additional weird characters before the OK response, something that looks like ᤙᤙOK and it makes the function never ends
        #So I have had to delete the response checking and also the is_open checking because sometimes the modem wasn't able to hang up despite aparently the conexion was closed is_open=false 
        self.link.write("+++")
        self.link.read(6)
        self.link.write("ATH\r\n")
        resp=self.link.read(6)
        LOGGER.info("GSM : Hang-up")
        
    def open(self):
        '''Open the gsm connection.'''
        if not self.is_open:
            self.link.open()
            self.is_open = self._call()
            if not self.is_open:
                self.link.close()   #EGC Close Serial port because sometimes if a error occurrs let the serial port open and busy and it makes impossible  restart a new comunication.
                raise ValueError('no GSM device')
            
    def close(self):
        '''Close the gsm connection.'''
        if self.is_open:
            self._hangup()
            self.link.close()
            self.is_open = False
        else:   
            self.link.close()   #EGC to ensure te correct close of the serial port to avoid futures problems when someone wants to restart a serial com
            
    @property
    def url(self):
        '''Connection url.'''
        return 'gsm:%s:%s' % (self.phone, str(self.link))

    def settimeout(self, timeout):
        self.timeout=timeout #EGC Set GSM timeout
        self.link.settimeout(timeout)    #EGC Also Set the serial port timeout

    def write(self, data):
        '''Write all `data` to the gsm connection.'''
        self.link.write(data)

    def read(self, size=None, timeout=None):
        '''Read data from the serial connection.'''
        return self.link.read(size, timeout)
