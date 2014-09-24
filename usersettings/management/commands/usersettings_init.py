"""
Init config.
"""
from django.core.management.base import BaseCommand, CommandError
from usersettings.shortcuts import get_usersettings_model
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Init config'
    args = "[user_id]"

    def handle(self, user_id=None, **options):
        user = get_user_model().objects.filter(is_superuser=True)
        if user_id:
            user = user.filter(id=user_id)
        user = user.first()

        if not user:
            raise CommandError("Superuser not found")

        for site in Site.objects.all():
            print "Processing site %s" % site

            config, created = get_usersettings_model().objects.get_or_create(
                site=site,
                user=user
            )

            if not created:
                print "Userconfig for site %s already exists" % Site.objects.get_current()

        print "Done"