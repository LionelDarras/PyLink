PyLink
======

Pylink offers a universal communication interface using File-Like API.
For now, only the *TCP*, *UDP* and *Serial* interfaces are supported.
The USB and GSM interfaces will be added soon.

The aim of this project is to allow any type of communication.
It is best suited for projects that have various ways of communicating
including IP remote or local serial communication.

Installation
------------

You can install, upgrade, uninstall pylink with these commands::

  $ pip install pylink
  $ pip install --upgrade pylink
  $ pip uninstall pylink

Or if you don't have pip::

  $ easy_install pylink

Examples
--------

::

  >>> from pylink import TCPLink, link_from_url
  >>> link = TCPLink('localhost', 7) # conntect to echo tcp service
  >>> link.write('Hello')
  2012-06-05 12:44:06,211 INFO: new <TCPLink udp:127.0.0.1:7> was initialized
  2012-06-05 12:44:06,211 INFO: Write : <b'hello'>
  2012-06-05 12:44:06,312 INFO: Read : <'hello'>
  >>> link.read() == 'Hello'
  True

::

  >>> link = link_from_url("serial:/dev/ttyUSB0:115200")
  >>> print link
  <SerialLink serial:/dev/ttyUSB0:115200:8N1>
