=========
unhashlib
=========

.. image:: https://img.shields.io/pypi/v/unhashlib.svg
   :alt: PyPI


``unhashlib`` is a Python string class enhancement (a mixin).

Installation
------------

The easiest way to install the package is via ``pip``::

    $ pip install unhashlib

Usage
-----

**Checking against a hash to the basic string class**

The hash can be automatically recognized.

.. code:: python

    from unhashlib import unhashlib

    s =  unhashlib('the tragicall historye of romeus and juliet')

    len(s)
    > 43

    s.title()
    > 'The Tragicall Historye Of Romeus And Juliet'

    from hashlib import sha256
    print(s.get_algorithm(sha256(s.encode('utf-8')).hexdigest()))
    > 'sha256'

    print(s.check(sha256(s.encode('utf-8')).hexdigest()))
    > True
