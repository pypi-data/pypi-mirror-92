======
reiter
======

Wrapper for Python iterators and iterables that implements a list-like random-access interface by caching retrieved items for later reuse.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/reiter.svg
   :target: https://badge.fury.io/py/reiter
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/lapets/reiter.svg?branch=master
   :target: https://travis-ci.com/lapets/reiter

.. |coveralls| image:: https://coveralls.io/repos/github/lapets/reiter/badge.svg?branch=master
   :target: https://coveralls.io/github/lapets/reiter?branch=master

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install reiter

The library can be imported in the usual way::

    import reiter
    from reiter import reiter

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

All unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python reiter/reiter.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint reiter

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
