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

This project is the missing extension to the Django “sites” framework, use it to store additional information for your Django-powered sites. The project structure is heavily inspired by  django ``sites`` app, with a ``one-to-one`` relationship to the ``Site`` model.

It’s best explained through examples.


Example Usage
-------------

For example, suppose you’re developing a multi-site django project i.e. using single Django installation that powers more than one site and you need to differentiate between those sites in some way.

(e.g. Site Title, Physical Location, Contact Details... etc)

Of course, you could hardcode the information in the templates and use different templates
for each site. Alternatively you could configure details in your `settings.py` for each site.

A better solution would be to use ``django-usersettings2``. This project accomplishes several things quite nicely:

* It lets the site producers edit all settings – for multiple sites – in a single interface (the Django admin).
* It lets the site developers use the same Django views/templates for multiple sites.

To get started, create a class that inherits from ``usersettings.models.UserSettings``. Make sure to import the ``UserSettings`` model. Your class should live in one of your apps’ models.py (or module).

Since ``UserSettings`` model inherit from ``django.db.models.Model``, you are free to add any field you want.

Here's a simple example::

    from django.db import models
    from django.utils.translation import ugettext_lazy as _

    from usersettings.models import UserSettings

    class SiteSettings(UserSettings):
        site_title = models.CharField(_('Site Title'), max_length=100)
        tag_line = models.CharField(_('Tag Line'), max_length=150, blank=True)
        site_description = models.TextField(_('Site Description'), blank=True)

        ...

        class Meta:
            verbose_name = 'Site Settings'
            verbose_name_plural = 'Site Settings'

If you followed the Django tutorial, this shouldn’t look too new to you.
The only difference to normal models is that you subclass ``usersettings.models.UserSettings`` rather than ``django.db.models.base.Model``.

Hooking the 'usersettings' to the admin site
--------------------------------------------

To make your new model editable in the admin interface, you must first create an admin class that subclasses ``usersettings.admin.SettingsAdmin``. Continuing with the example model above, here’s a simple corresponding ``SiteSettingsAdmin`` class::

    from django.contrib import admin
    from django.utils.translation import ugettext_lazy as _

    from usersettings.admin import SettingsAdmin

    from .models import SiteSettings


    class SiteSettingsAdmin(SettingsAdmin):

        fieldsets = (
            (_('Site Title / Tag Line'), {
                'description': '...',
                'fields': ('site_title', 'tag_line',)
            }),
            ...
        )

        ...

    admin.site.register(SiteSettings, SiteSettingsAdmin)


Since ``SettingsAdmin`` inherits from ModelAdmin, you’ll be able to use the normal
set of Django ModelAdmin properties, as appropriate to your circumstance.

Once you’ve registered your admin class, a new model will appear in the top-level admin list.


Hooking into the current usersettings from views
------------------------------------------------

You can use the ``usersettings`` in your Django views to do particular things based on the ``usersettings`` for the site.

Here’s an example of what the a view looks like::

    from usersettings.shortcuts import get_current_usersettings

    def home(request):
        ...

        current_usersetting = get_current_usersettings()

        context = {
            'title': current_usersetting.site_title,
        }

        ...

Custom Middleware
-----------------

To avoid the repetitions of having to import ``current_usersetting`` for every view. Add ``usersettings.middleware.CurrentUserSettingsMiddleware`` to ``MIDDLEWARE_CLASSES``
The middleware sets the ``usersettings`` attribute on every request object, so you can use ``request.usersettings`` to get the current usersettings::

    MIDDLEWARE_CLASSES=(
        ...
        'usersettings.middleware.CurrentUserSettingsMiddleware',
        ...
    )

Caching the current ``UserSettings`` object
-------------------------------------------
As the ``usersettings`` are stored in the database, each call to ``UserSettings.objects.get_current()`` could result in a database query.

But just like the Django sites framework, on the first request the current usersettings is cached, and any subsequent call returns the cached data instead of hitting the database.

If for any reason you want to force a database query, you can tell Django to clear the cache using ``UserSettings.objects.clear_cache()``::

    from usersettings.shortcuts import get_usersettings_model
    
    UserSettings = get_usersettings_model()
    
    # First call; current usersettings fetched from database.
    current_usersetting = UserSettings.objects.get_current()

    # Second call; current usersettings fetched from cache.
    current_usersetting = UserSettings.objects.get_current()

    # Force a database query for the third call.
    UserSettings.objects.clear_cache()
    current_usersetting = UserSettings.objects.get_current()

Install
-------

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
    )

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


DJANGO-CMS >= 3.0 Toolbar
--------------------------

`djangocms-usersettings2 <https://github.com/mishbahr/djangocms-usersettings2>`_ integrates ``django-usersettings2`` with `django-cms>=3.0 <https://github.com/divio/django-cms/>`_

This allows a site editor to add/modify all usersettings in the frontend editing mode of django CMS and provide your users with a streamlined editing experience.


Documentation
-------------

The full documentation is at https://django-usersettings2.readthedocs.org.
