#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from usersettings.shortcuts import get_usersettings_model
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.sites.models import Site


class CommandsTest(TestCase):
    username = 'superuser'
    email = 'superuser@example.com'
    password = 'pa$sw0Rd'

    usersettings_model = get_usersettings_model()

    def setUp(self):
        Site.objects.get_or_create(id=settings.SITE_ID, domain='example.com', name='example.com')
        self.user = get_user_model().objects.create_superuser(self.username, self.email, self.password)

    def test_usersettings_init(self):
        call_command('usersettings_init')
        self.assertEqual(self.usersettings_model.objects.all().count(), 1)

    def test_usersettings_init_allready_exists(self):
        call_command('usersettings_init')
        call_command('usersettings_init')
        self.assertEqual(self.usersettings_model.objects.all().count(), 1)