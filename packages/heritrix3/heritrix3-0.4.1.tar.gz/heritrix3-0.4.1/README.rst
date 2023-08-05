========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-heritrix3-client/badge/?style=flat
    :target: https://readthedocs.org/projects/python-heritrix3-client
    :alt: Documentation Status

.. |coveralls| image:: https://coveralls.io/repos/Querela/python-heritrix3-client/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/Querela/python-heritrix3-client

.. |codecov| image:: https://codecov.io/gh/Querela/python-heritrix3-client/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/Querela/python-heritrix3-client

.. |version| image:: https://img.shields.io/pypi/v/heritrix3.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/heritrix3

.. |wheel| image:: https://img.shields.io/pypi/wheel/heritrix3.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/heritrix3

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/heritrix3.svg
    :alt: Supported versions
    :target: https://pypi.org/project/heritrix3

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/heritrix3.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/heritrix3

.. |commits-since| image:: https://img.shields.io/github/commits-since/Querela/python-heritrix3-client/v0.4.1.svg
    :alt: Commits since latest release
    :target: https://github.com/Querela/python-heritrix3-client/compare/v0.4.1...master

.. end-badges

A internetarchive/heritrix3 python REST API client.

* Free software: MIT license

Installation
============

::

    pip install heritrix3

You can also install the in-development version with::

    pip install https://github.com/Querela/python-heritrix3-client/archive/master.zip

Documentation
=============

https://python-heritrix3-client.readthedocs.io/

Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
