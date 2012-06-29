PyLink
======

Pylink offers a universal communication interface using File-Like API.
For now, only the **TCP**, **UDP**, **Serial** and GSM interfaces are 
supported.

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
  2012-06-05 12:44:06,211 INFO: new <TCPLink tcp:127.0.0.1:7> was initialized
  2012-06-05 12:44:06,211 INFO: Write : <b'hello'>
  >>> link.read() == 'Hello'
  2012-06-05 12:44:06,312 INFO: Read : <'hello'>
  True

With GSMLink, you shoud specify the modem connection link::


  >>> from pylink import GSMLink, SerialLink
  >>> link = GSMLink("0678986955", SerialLink("/dev/ttyUSB0", 38400))
  >>> link.open()
  2012-06-29 15:13:31,637 INFO: new <SerialLink serial:/dev/ttyUSB0:38400:8N1> was initialized 
  2012-06-29 15:13:31,637 INFO: GSM : Call 0678986955 
  2012-06-29 15:13:31,638 INFO: Write : <u'ATD0678986955\r\n'> 
  2012-06-29 15:13:31,648 INFO: GSM : <u'call in progress'> 
  2012-06-29 15:13:41,649 INFO: GSM : <u'call in progress'> 
  2012-06-29 15:14:08,075 INFO: Read : <u'\r\nCONNECT 9600\r\n\n\r\n\r\n\r'> 
  2012-06-29 15:14:08,076 INFO: GSM : <u'Client is ready (\r\nCONNECT 9600\r\n\n\r\n\r\n\r)'> 
  >>> link.write("TEST\n")
  2012-06-29 15:14:16,193 INFO: Write : <u'TEST\n'> 
  >>> link.read()
  2012-06-29 15:14:24,972 INFO: Read : <u'\n\rTEST\n\r'>
  
  TEST
  
  >>> link.close()
  2012-06-29 15:29:09,295 INFO: Write : <u'+++'> 
  2012-06-29 15:29:10,318 INFO: Read : <u'\r\nOK\r\n'> 
  2012-06-29 15:29:10,318 INFO: Write : <u'ATH\r\n'> 
  2012-06-29 15:29:10,336 INFO: Read : <u'\r\nOK\r\n'> 
  2012-06-29 15:29:10,337 INFO: GSM : Hang-up 
  2012-06-29 15:29:10,437 INFO: Connection <SerialLink serial:/dev/ttyUSB0:38400:8N1> was closed

Contribute
----------

There are several ways to contribute to the project:

#. Post bugs and feature `requests on github`_.
#. Fork `the repository`_ on Github to start making your changes.
#. Write a test which shows that the bug was fixed or that the feature works as expected.
#. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS_.

.. _`requests on github`: https://github.com/SalemHarrache/PyLink/issues
.. _`the repository`: https://github.com/SalemHarrache/PyLink
.. _AUTHORS: https://github.com/SalemHarrache/PyLink/blob/master/AUTHORS.rst
