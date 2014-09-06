from django.apps import AppConfig

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, pre_delete

from .models import clear_usersettings_cache
from .shortcuts import get_usersettings_model


class UserSettingsConfig(AppConfig):
    name = 'usersettings'
    verbose_name = _('User Settings')

    def ready(self):
        usersettings_model = get_usersettings_model()
        pre_save.connect(clear_usersettings_cache, sender=usersettings_model)
        pre_delete.connect(clear_usersettings_cache, sender=usersettings_model)
