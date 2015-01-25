License
=======

* GameQuery is licensed under `Creative Commons Attribution-NonCommercial 3.0 <http://creativecommons.org/licenses/by-nc/3.0/>`__ license.

Requirements
============

* Python 3.4 or better (or maybe python 3.3 [not tested])

Usage
=====

.. code-block:: python

    >>> import query
    >>> 
    >>> info = query.Query()
    >>> info.query('127.0.0.1', 27015, 'gamespy1')
    {'hostname': ' --=[ aX ]=-- (CD and Origin)', 'map': 'iwo jima', 'is_password': False, 'maxplayers': 64, 'players': 42}


TODO
====

* add asyncio module
* add players list
* add rules list
* add install from pip
* adds more docs and samples