============
Installation
============

1. Install ``django-usersettings``::

    pip install django-usersettings2

2. Add ``usersettings`` to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'usersettings',
        ...
    )

4. Specify the custom ``UserSettings`` model as the default usersettings model for your project using the ``USERSETTINGS_MODEL`` setting in your settings.py (required)::

    USERSETTINGS_MODEL='config.SiteSettings'

5. Add ``usersettings.middleware.CurrentUserSettingsMiddleware`` to ``MIDDLEWARE_CLASSES`` (optional).

The middleware sets the ``usersettings`` attribute on every request object, so you can use ``request.usersettings`` to get the current usersettings::

    MIDDLEWARE_CLASSES=(
        ...
        'usersettings.middleware.CurrentUserSettingsMiddleware',
        ...
    ),

6. The current usersettings are made available in the template context when your
``TEMPLATE_CONTEXT_PROCESSORS`` setting contains ``usersettings.context_processors.usersettings``::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'usersettings.context_processors.usersettings',
        ...
    )


Dependencies
------------

django-usersettings2 requires The `“sites” <https://docs.djangoproject.com/en/dev/ref/contrib/sites/>`_
framework to be installed.

To enable the sites framework, follow these steps:

1. Add `django.contrib.sites` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'django.contrib.sites'
        ...
    )

2. Define a ``SITE_ID`` setting::

    SITE_ID = 1

3. Run migrate.
