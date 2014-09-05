#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist

from usersettings.shortcuts import get_usersettings_model


class TestUserSettingsModel(TestCase):

    usersettings_model = get_usersettings_model()

    usersettings_data = {
        'site_id': settings.SITE_ID,
        'user_id': 1,
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

    def create_usersettings(self):
        return self.usersettings_model.objects.create(**self.usersettings_data)

    def test_add_user_settings(self):
        self.create_usersettings()
        self.assertEqual(self.usersettings_model.objects.all().count(), 1)

    def test_usersettings_manager(self):
        # Make sure that get_current() does not return a deleted UserSettings object.
        self.create_usersettings()

        current_usersettings = self.usersettings_model.objects.get_current()
        self.assertIsInstance(current_usersettings, self.usersettings_model)

        current_usersettings.delete()
        self.assertRaises(ObjectDoesNotExist, self.usersettings_model.objects.get_current)

    def test_usersettings_cache(self):
        # After updating a UserSettings object (e.g. via the admin), we shouldn't return a
        # bogus value from the USERSETTINGS_CACHE.

        self.create_usersettings()

        current_usersettings = self.usersettings_model.objects.get_current()
        self.assertEqual(self.usersettings_data['site_title'], current_usersettings.site_title)

        usersettings2 = self.usersettings_model.objects.get_current()
        usersettings2.site_title = 'Django is AWESOME'
        usersettings2.save()

        current_usersettings = self.usersettings_model.objects.get_current()
        self.assertEqual('Django is AWESOME', current_usersettings.site_title)

    def test_delete_all_usersettings_clears_cache(self):
        """ When all UserSettings objects are deleted the cache should also
        be cleared and get_current_usersettings() should raise a DoesNotExist."""
        self.create_usersettings()
        self.assertIsInstance(self.usersettings_model.objects.get_current(),
                              self.usersettings_model)
        self.usersettings_model.objects.all().delete()
        self.assertRaises(self.usersettings_model.DoesNotExist,
                          self.usersettings_model.objects.get_current)

    def test_clear_cache(self):
        self.create_usersettings()
        # this will cache the current usersettings as USERSETTINGS_CACHE
        self.usersettings_model.objects.get_current()

        # we clear all USERSETTINGS_CACHE
        self.usersettings_model.objects.clear_cache()

        # test to ensure USERSETTINGS_CACHE is empty
        from usersettings.models import USERSETTINGS_CACHE
        self.assertDictEqual(USERSETTINGS_CACHE, {})
