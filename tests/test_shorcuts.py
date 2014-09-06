#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from django.core.exceptions import ImproperlyConfigured
from django.contrib.sites.models import Site

from usersettings.shortcuts import get_usersettings_model, get_current_usersettings


class TestUserSettingsShotcuts(TestCase):
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
        self.usersettings_model.objects.create(**self.usersettings_data)

    def test_get_current_usersettings(self):
        # Test that the correct UserSettings object is returned
        current_usersettings = get_current_usersettings()
        self.assertIsInstance(current_usersettings, self.usersettings_model)

    @override_settings(USERSETTINGS_MODEL='SiteSettings')
    def test_get_usersettings_model_fails_with_improper_settings(self):
        self.assertRaises(ImproperlyConfigured, get_usersettings_model)
