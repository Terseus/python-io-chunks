io-chunks
#########

Stream chunks compatible with IO standard library

.. image:: https://img.shields.io/github/issues/Terseus/python-io-chunks.svg
  :alt: Issues on Github
  :target: https://github.com/Terseus/python-io-chunks/issues

.. image:: https://img.shields.io/github/issues-pr/Terseus/python-io-chunks.svg
  :alt: Pull Request opened on Github
  :target: https://github.com/Terseus/python-io-chunks/issues

.. image:: https://img.shields.io/github/release/Terseus/python-io-chunks.svg
  :alt: Release version on Github
  :target: https://github.com/Terseus/python-io-chunks/releases/latest

.. image:: https://img.shields.io/github/release-date/Terseus/python-io-chunks.svg
  :alt: Release date on Github
  :target: https://github.com/Terseus/python-io-chunks/releases/latest


CIs status
~~~~~~~~~~

+-------------------+--------------------------+-------------+------------+-------------+
| CI name           |  Travis                  | Appveyor    | CircleCI   | CodeClimate |
+===================+==========================+=============+============+=============+
| CI status badge   |  |img_ci_travis_status|  |  *TODO*     |  *TODO*    |  *TODO*     |
+-------------------+--------------------------+-------------+------------+-------------+


Installing
==========

.. code-block:: bash

    $ pip install io-chunks


Python version
==============

Tested in Python 2.7 and 3.2 to 3.6


Running the tests
=================

Run the tests with ``nose``:

.. code-block:: bash

    $ nosetests


TOX environments
~~~~~~~~~~~~~~~~

*To use tox , need to install first with* (`read more about tox here`_) : ``pip install tox``

+-------------------------------+------------------------------------+
| Env name                      | Env description                    |
+===============================+====================================+
| py27,py32,py33,py34,py35,py36 | Python supported versions          |
+-------------------------------+------------------------------------+
| flake8                        | Exec linter in io_chunks/ tests/   |
+-------------------------------+------------------------------------+


TODO
====

* Write *some* examples and description.
* Write doc for readthedocs.org
* Add tests for concurrency support.


.. _read more about tox here:https://tox.readthedocs.io/en/latest/install.html
.. |img_ci_travis_status| image:: https://travis-ci.org/Terseus/python-io-chunks.svg?branch=master
    :target: https://travis-ci.org/Terseus/python-io-chunks