from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_usersettings_model():
    """
    Returns the ``UserSettings`` model that is active in this project.
    """
    from django.db.models import get_model

    try:
        app_label, model_name = settings.USERSETTINGS_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured('USERSETTINGS_MODEL must be of the '
                                   'form "app_label.model_name"')
    usersettings_model = get_model(app_label, model_name)
    if usersettings_model is None:
        raise ImproperlyConfigured('USERSETTINGS_MODEL refers to model "%s" that has '
                                   'not been installed' % settings.USERSETTINGS_MODEL)
    return usersettings_model


def get_current_usersettings():
    """
    Returns the current ``UserSettings`` based on
    the SITE_ID in the project's settings
    """
    USERSETTINGS_MODEL = get_usersettings_model()
    current_usersettings = USERSETTINGS_MODEL.objects.get_current()
    return current_usersettings
