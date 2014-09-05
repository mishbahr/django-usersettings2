from distutils.version import LooseVersion

try:
    import cms
except ImportError:
    DJANGO_CMS_3_0 = False
else:
    DJANGO_CMS_3_0 = LooseVersion(cms.__version__) < LooseVersion('3.1')


if DJANGO_CMS_3_0:

    from django.core.urlresolvers import reverse, NoReverseMatch
    from django.contrib.admin.options import IS_POPUP_VAR

    from cms.toolbar_pool import toolbar_pool
    from cms.toolbar_base import CMSToolbar
    from cms.toolbar.items import Break
    from cms.cms_toolbar import ADMIN_MENU_IDENTIFIER, USER_SETTINGS_BREAK

    from .shortcuts import get_usersettings_model

    @toolbar_pool.register
    class UserSettingsToolbar(CMSToolbar):

        def __init__(self, *args, **kwargs):
            super(UserSettingsToolbar, self).__init__(*args, **kwargs)
            self.model = get_usersettings_model()
            self.opts = self.model._meta

        def populate(self):
            admin_menu = self.toolbar.get_or_create_menu(
                ADMIN_MENU_IDENTIFIER, self.current_site.name)
            position = admin_menu.find_first(
                Break, identifier=USER_SETTINGS_BREAK)

            try:
                usersettings_obj = self.model.objects.get(site_id=self.current_site.pk)
            except self.model.DoesNotExist:
                usersettings_obj = None

            try:
                if usersettings_obj:
                    url = '%s?%s' % (
                        reverse(
                            'admin:%s_%s_change' % (
                                self.opts.app_label, self.opts.module_name),
                            args=(usersettings_obj.pk,)), IS_POPUP_VAR)
                else:
                    url = '%s?site_id=%s&%s' % (
                        reverse('admin:%s_%s_add' % (self.opts.app_label, self.opts.module_name)),
                        self.current_site.pk,
                        IS_POPUP_VAR)
            except NoReverseMatch:
                pass
            else:
                admin_menu.add_modal_item(
                    self.opts.verbose_name, url, position=position+1)
                admin_menu.add_break('usersettings-break', position=position+2)
