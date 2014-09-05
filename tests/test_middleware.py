#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase

from django.contrib.sites.models import Site

from usersettings.middleware import CurrentUserSettingsMiddleware
from usersettings.shortcuts import get_usersettings_model


class MiddlewareTest(TestCase):

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

    def test_request(self):
        """ Makes sure that the request has correct `usersettings` attribute. """
        middleware = CurrentUserSettingsMiddleware()
        request = HttpRequest()
        middleware.process_request(request)
        self.assertEqual(request.usersettings.site.id, settings.SITE_ID)
