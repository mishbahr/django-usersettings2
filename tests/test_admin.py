#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
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
    test_sites = ('google.com', 'facebook.com', 'youtube.com', 'yahoo.com', 'wikipedia.org', )
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
    model_opts = get_usersettings_model()._meta

    def create_sites(self):
        for site in self.test_sites:
            Site.objects.create(domain=site, name=site)

    def setUp(self):
        Site.objects.get_or_create(id=settings.SITE_ID, domain='example.com', name='example.com')
        self.obj = get_usersettings_model().objects.create(**self.usersettings_data)
        self.user = get_user_model().objects.create_superuser(
            self.username, self.email, self.password)

        self.assertTrue(self.client.login(
            username=self.username, password=self.password),
            'Failed to login user %s' % self.email)

        factory = RequestFactory()
        request = factory.get('/admin')
        request.user = self.user
        request.session = {}

        self.request = request
        self.settings_admin = SettingsAdmin(get_usersettings_model(), AdminSite())

        # Hack to test this function as it calls 'messages.add'
        # See https://code.djangoproject.com/ticket/17971
        setattr(self.request, 'session', 'session')
        messages = FallbackStorage(self.request)
        setattr(self.request, '_messages', messages)

    def test_has_add_permission(self):
        # now this should return False, as there is only 1 site
        # and we have already created an usersettings
        self.assertFalse(self.settings_admin.has_add_permission(self.request))

    def test_save_model_saves_logged_in_user(self):
        self.settings_admin.save_model(self.request, self.obj, form=None, change=False)
        usersettings = get_usersettings_model().objects.get(site_id=settings.SITE_ID)
        self.assertEqual(usersettings.user, self.user)

    def test_get_site_choices(self):
        self.create_sites()
        # this should return a tuple. +1 as we also create a site during setUp
        self.assertTrue(len(self.settings_admin.get_site_choices()) == len(self.test_sites) + 1)

    @override_settings(MIDDLEWARE_CLASSES=())
    def test_changelist_view(self):
        change_url = reverse('admin:%s_%s_change' % (
            self.model_opts.app_label, self.model_opts.module_name), args=(self.obj.pk,))
        add_url = '%s?site_id=%s' % (
            reverse('admin:%s_%s_add' % (self.model_opts.app_label, self.model_opts.module_name)),
            settings.SITE_ID)

        resp = self.settings_admin.changelist_view(self.request)
        # we already created 1 usersettings required. so changeview should redirect to that
        self.failUnlessEqual(resp.items()[1][1], change_url, 'Should redirect to change view')
        # lets delete the existing usersettings model.
        get_usersettings_model().objects.get(site_id=settings.SITE_ID).delete()
        # now we should redirect to add view
        resp = self.settings_admin.changelist_view(self.request)
        self.failUnlessEqual(resp.items()[1][1], add_url, 'Should redirect to add view')


    def tearDown(self):
        self.client.logout()
