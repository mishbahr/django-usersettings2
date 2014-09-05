from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from usersettings.admin import SettingsAdmin

from .models import SiteSettings


class SiteSettingsAdmin(SettingsAdmin):
    fieldsets = (
        (_('Site Title / Tag Line'), {
            'description': 'Enter a Site Title and Tag Line to appear '
                           'on the front of your site. '
                           'Please note, your Site Title and Tag Line\'s '
                           'appearance will be dependent on your template.',
            'fields': ('site_title', 'tag_line',)
        }),
        (_('Site Description'), {
            'classes': ('collapse',),
            'description': 'Enter a Site Description or bio for your site. ',
            'fields': ('site_description', )
        }),
        (_('Physical Location'), {
            'description': 'Enter your address. This is typically for '
                           'businesses with offices or storefronts. '
                           'Depending on your template this can be '
                           'displayed in the header, footer, or '
                           'Info Page of your site.',
            'fields': (
                'street_address', 'address_line_2', 'address_locality',
                'address_region', 'postal_code',
            )
        }),
        (_('Contact Details'), {
            'description': 'Enter a phone/fax number or email,'
                           'where your site visitors can contact you. '
                           'Depending on your template, this may '
                           'display on your site.',
            'fields': ('telephone', 'fax_number', 'email', )
        }),
    )

admin.site.register(SiteSettings, SiteSettingsAdmin)
