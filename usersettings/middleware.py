from .shortcuts import get_current_usersettings


class CurrentUserSettingsMiddleware(object):
    """
    Middleware that sets `usersettings` attribute to request object.
    """

    def process_request(self, request):
        request.usersettings = get_current_usersettings()
