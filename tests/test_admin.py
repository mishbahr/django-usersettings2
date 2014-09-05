#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.contrib.sites.models import Site
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage

from usersettings.admin import SettingsAdmin
from usersettings.shortcuts import get_usersettings_model


class AdminTest(TestCase):
    username = 'superuser'
    email = 'superuser@example.com'
    password = 'pa$sw0Rd'

    model_opts = get_usersettings_model()._meta

    usersettings_data = {
        'site_id': settings.SITE_ID,
        'user_id': 2,
        'site_title': 'Site Title',
        'tag_line': 'Friends don\'t let friends use Drupal',
        'street_address': '1600 Amphitheatre Parkway',
        'address_locality': 'Mountain View',
        'address_region': 'CA',
        'postal_code': '94043',
        'telephone': '+1 650-253-0000',
    }

    def setUp(self):
        Site.objects.get_or_create(id=settings.SITE_ID, domain='example.com', name='example.com')
        self.user = get_user_model().objects.create_superuser(
            self.username, self.email, self.password)

        self.assertTrue(self.client.login(
            username=self.username, password=self.password),
            'Failed to login user %s' % self.email)

        factory = RequestFactory()
        self.request = factory.get('/admin')

        self.request.user = self.user

        # Hack to test this function as it calls 'messages.add'
        # See https://code.djangoproject.com/ticket/17971
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

    def test_has_add_permission(self):
        settings_admin = SettingsAdmin(get_usersettings_model(), AdminSite())
        # No usersettings exists, so this should return True
        self.assertTrue(settings_admin.has_add_permission(self.request))
        # we create an usersettings
        get_usersettings_model().objects.create(**self.usersettings_data)
        # now this should return False, as there's only a 1 site
        self.assertFalse(settings_admin.has_add_permission(self.request))

    def test_save_model_saves_logged_in_user(self):
        settings_admin = SettingsAdmin(get_usersettings_model(), AdminSite())
        obj = get_usersettings_model().objects.create(**self.usersettings_data)
        settings_admin.save_model(self.request, obj, form=None, change=False)
        usersettings = get_usersettings_model().objects.get(site_id=1)
        self.assertEqual(usersettings.user, self.user)

    def tearDown(self):
        self.client.logout()
