#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from usersettings.shortcuts import get_usersettings_model
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.contrib.sites.models import Site
from django.core.management.base import CommandError


class CommandsTest(TestCase):
    username = 'superuser'
    email = 'superuser@example.com'
    password = 'pa$sw0Rd'

    def setUp(self):
        Site.objects.get_or_create(id=settings.SITE_ID, domain='example.com', name='example.com')

    def setUpUser(self):
        self.user = get_user_model().objects.create_superuser(self.username, self.email, self.password)

    def test_usersettings_init(self):
        self.setUpUser()

        call_command('usersettings_init')

        self.assertEqual(get_usersettings_model().objects.all().count(), 1)

    def test_usersettings_init_many(self):
        self.setUpUser()

        Site.objects.get_or_create(id=(settings.SITE_ID + 1), domain='example.com', name='example.com')

        call_command('usersettings_init')

        self.assertEqual(get_usersettings_model().objects.all().count(), 2)

    def test_usersettings_init_allready_exists(self):
        self.setUpUser()

        call_command('usersettings_init')
        call_command('usersettings_init')

        self.assertEqual(get_usersettings_model().objects.all().count(), 1)

    def test_usersettings_no_user(self):
        with self.assertRaises(CommandError):
            call_command('usersettings_init')

        self.assertEqual(get_usersettings_model().objects.all().count(), 0)

    def test_usersettings_integrity_constraint(self):
        self.setUpUser()

        # little hack, but don't know another way to test
        get_usersettings_model()._meta.get_field_by_name('tag_line')[0].empty_strings_allowed = False

        with self.assertRaises(CommandError):
            call_command('usersettings_init')

        self.assertEqual(get_usersettings_model().objects.all().count(), 0)

