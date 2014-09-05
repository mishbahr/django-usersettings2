
def usersettings(request):
    """
    Returns the current ``UserSettings`` based on
    the SITE_ID in the project's settings as context variables

    If there is no 'usersettings' attribute in the request, fetches the
    current UserSettings (from usersettings.shortcuts.get_current_usersettings).
    """
    if hasattr(request, 'usersettings'):
        usersettings = request.usersettings
    else:
        from .shortcuts import get_current_usersettings
        usersettings = get_current_usersettings()

    return {
        'usersettings': usersettings
    }
