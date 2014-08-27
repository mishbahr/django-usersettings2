=============================
django-usersettings2
=============================

.. image:: http://img.shields.io/travis/mishbahr/django-usersettings2.svg?style=flat-square
    :target: https://travis-ci.org/mishbahr/django-usersettings2/

.. image:: http://img.shields.io/pypi/v/django-usersettings2.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-usersettings2/
    :alt: Latest Version

.. image:: http://img.shields.io/pypi/dm/django-usersettings2.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-usersettings2/
    :alt: Downloads

.. image:: http://img.shields.io/pypi/l/django-usersettings2.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-usersettings2/
    :alt: License

.. image:: http://img.shields.io/coveralls/mishbahr/django-usersettings2.svg?style=flat-square
  :target: https://coveralls.io/r/mishbahr/django-usersettings2?branch=master


A reusable app for django, provides the ability to configure site settings via the admin interface, rather than by editing settings.py

Features
--------

* TODO


Documentation
-------------

The full documentation is at https://django-usersettings2.readthedocs.org.

Quickstart
----------

1. Install django-usersettings::

    pip install django-usersettings2


2. Add `usersettings` to `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'usersettings',
        ...
    )