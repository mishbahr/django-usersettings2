#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from django.test import TestCase

from django.contrib.sites.models import Site

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

    def test_context_processors(self):
        """ Test the `usersettings` attribute is available as context in templates """
        resp = self.client.get(reverse('current_usersettings'))
        self.assertEqual(200, resp.status_code)
        self.failUnless(isinstance(resp.context['usersettings'], self.usersettings_model))

    @override_settings(
        MIDDLEWARE_CLASSES=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',)
    )
    def test_context_processors_without_middleware(self):
        """
            Test usersettings context_processors still works without the custom middleware
        """
        resp = self.client.get(reverse('current_usersettings'))
        self.assertEqual(200, resp.status_code)
        self.failUnless(isinstance(resp.context['usersettings'], self.usersettings_model))
