from django.db import models
from django.utils.translation import ugettext_lazy as _

from usersettings.models import UserSettings


class SiteSettings(UserSettings):
    site_title = models.CharField(_('Site Title'), max_length=255, default='Site Title')
    tag_line = models.CharField(_('Tag Line'), max_length=255, blank=True)
    site_description = models.TextField(_('Site Description'), blank=True)

    street_address = models.CharField(
        _('Street Address'), max_length=150,
        help_text=_('The street address. For example, 1600 Amphitheatre Parkway'))
    address_line_2 = models.CharField(_('Address Line 2'), max_length=150, blank=True)
    address_locality = models.CharField(
        _('Address Locality'), max_length=150,
        help_text=_('The locality. For example, Mountain View.'))
    address_region = models.CharField(
        _('Address Region'), max_length=150,
        help_text=_('The region. For example, CA.'))
    postal_code = models.CharField(
        _('Postal Code'), max_length=50,
        help_text=_('The postal code. For example, 94043.'))

    telephone = models.CharField(_('Telephone'), max_length=100)
    email = models.EmailField(_('Email'), blank=True)
    fax_number = models.CharField(
        _('Fax Number'), max_length=100, blank=True,
        help_text=_('The fax number.'))

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'
