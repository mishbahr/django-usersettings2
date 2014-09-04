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



Why would you use usersettings?
-------------------------------

The project structure is heavily inspired by  django 'sites` app, with a one-to-one relationship to site object,
use it to store additional information for your Django-powered sites.

It’s best explained through examples.


Example Usage
-------------

    *TODO

Dependencies
------------

django-usersettings2 requires The `“sites” <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_ framework to be installed.

To enable the sites framework, follow these steps::

1. Add `django.contrib.sites` to your INSTALLED_APPS setting::

    INSTALLED_APPS = (
        ...
        'django.contrib.sites'
        ...
    )

2. Define a SITE_ID setting::

    SITE_ID = 1

3. Run migrate.


Install
-------

1. Install `django-usersettings`::

    pip install django-usersettings2

2. Add `usersettings` to `INSTALLED_APPS`::

    INSTALLED_APPS = (
        ...
        'usersettings',
        ...
    )

4. Specify the custom `UserSettings` model as the default usersettings model for your project using
the `usersettings_model` setting in your settings.py (required)::

    USERSETTINGS_MODEL='config.SiteSettings'

5. Add `usersettings.middleware.CurrentUserSettingsMiddleware` to MIDDLEWARE_CLASSES (optional).

The middleware sets the `usersettings` attribute on every request object, so you can use request.usersettings to get the current usersettings::

    MIDDLEWARE_CLASSES=(
        ...
        'usersettings.middleware.CurrentUserSettingsMiddleware',
        ...
    ),

6. The current usersettings are made available in the template context when your
`TEMPLATE_CONTEXT_PROCESSORS` setting contains `usersettings.context_processors.usersettings`::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'usersettings.context_processors.usersettings',
        ...
    )

DJANGO-CMS >= 3.0 Toolbar
-------------------------
django-usersettings2 works seamlessly with `django-cms>=3.0` with a
custom toolbar. This allows site editor to add/modify all usersettings in the frontend editing mode of django CMS
and provide your users with a streamlined editing experience.

`UserSettingsToolbar` will be automatically loaded as long `CMS_TOOLBARS` is not set (or set to None).

Or you can add `usersettings.cms_toolbar.UserSettingsToolbar` to `CMS_TOOLBARS` settings::

    CMS_TOOLBARS = [
        # CMS Toolbars
        ...

        # django-usersettings2 Toolbar
       'usersettings.cms_toolbar.UserSettingsToolbar',
    ]

Documentation
-------------

The full documentation is at https://django-usersettings2.readthedocs.org.
