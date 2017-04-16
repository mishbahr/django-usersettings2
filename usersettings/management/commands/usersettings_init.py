"""
Init config.
"""
from django.core.management.base import BaseCommand, CommandError
from usersettings.shortcuts import get_usersettings_model
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):
    help = 'Init config'
    args = ""

    def handle(self, **options):
        user = get_user_model().objects.filter(is_superuser=True)[:1]

        if not user:
            raise CommandError('Superuser not found')

        user = user.get()

        for site in Site.objects.all():
            print('Processing site %s' % site)

            try:
                config, created = get_usersettings_model().objects.get_or_create(
                    site=site,
                    user=user
                )

                if not created:
                    print('Userconfig for site %s already exists' % Site.objects.get_current())

            except IntegrityError as e:
                raise CommandError("Couldn't create userconfig record. Please check default values. Error %s" % e)

        print('Done')