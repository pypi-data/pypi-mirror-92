The Internet Communications Engine (Ice) provides a robust, proven platform for
developing mission-critical networked applications. Let Ice handle all of the
low-level details such as network connections, serialization, and concurrency so
that you can focus on your application logic.

The Ice Python extension makes the full Ice feature set available to Python
developers, including:

* Client and server support
* Synchronous and asynchronous invocations
* Communicate via TCP, SSL, UDP, multicast, and WebSocket transports
* Supports IPv4 and IPv6
* Intuitive mapping from Slice to Python

To give you an idea of what it's like to use Ice in Python, here's a complete
program that tests whether a remote Ice object is available:

::

  import sys, Ice
  with Ice.initialize(sys.argv) as communicator:
      obj = communicator.stringToProxy("hello:tcp -h myhost.mydomain.com -p 10000")
      obj.ice_ping()

With support for Python2 and Python3, you can easily add Ice to your existing
Python infrastructure and discover how easy it is to build distributed
applications with Ice.

Package Contents
----------------

This package includes the Ice extension for Python, the standard Slice
definition files, and the Slice-to-Python compiler. You will need to install a
full Ice distribution if you want to use other Ice language mappings, or Ice
services such as IceGrid, IceStorm and Glacier2.

Installation
------------

We recommend using ``pip`` or ``easy_install`` to install this package. If you
install using ``python setup.py install`` instead, be aware that the Slice-to-
Python compiler (``slice2py``) will not be available.

By default, Ice is built statically with the package. On Linux and macOS, you
can instead build the package with the system-installed Ice shared libraries.
To do so, you can provide the ```--with-installed-ice``` option to
```setup.py``` install. With ```pip```, you should pass the
```--install-option="--with-installed-ice"``` option to pip install.

Home Page
---------

Visit `ZeroC's home page <https://zeroc.com>`_ for the latest news and
information about Ice.

Documentation
-------------

We provide extensive `online documentation
<https://doc.zeroc.com/ice/3.7>`_ for Ice, the Python extension, and the
other Ice language mappings and services.

Support
-------

Join us on our `user forums <https://zeroc.com/forums/forum.php>`_ if you have
questions about Ice.
