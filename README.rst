==========
PyVPDriver
==========

Universal communication interface using File-Like API.

Examples :
==========

::

  >>> from pylink import TCPLink, link_from_url

  >>> link = TCPLink('localhost', 7) # conntect to echo tcp service
  >>> link.write("Hello")
  >>> link.read() == "Hello"
  True


::

  >>> link = link_from_url("serial:/dev/ttyUSB0:115200:8N1")
  >>> print link
  <SerialLink serial:/dev/ttyUSB0:19200:8N1>
