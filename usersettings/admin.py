# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import AdminErrorList, AdminForm
from django.contrib.admin.widgets import AdminRadioSelect
from django.contrib.auth.admin import csrf_protect_m
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class SelectSiteForm(forms.Form):
    site = forms.ChoiceField(
        label=_('Site'), widget=AdminRadioSelect(attrs={'class': 'radiolist'}))


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'modified')

    select_site_form = SelectSiteForm
    select_site_form_template = 'admin/usersettings/select_site_form.html'

    def get_model_info(self):
        # module_name is renamed to model_name in Django 1.8
        app_label = self.model._meta.app_label
        try:
            return app_label, self.model._meta.model_name
        except AttributeError:
            return app_label, self.model._meta.module_name

    def has_add_permission(self, request):
        sites = Site.objects.values_list('id', flat=True).order_by('id')
        settings = self.model.objects.values_list('site', flat=True).order_by('id')
        for site in sites:
            if site not in settings:
                return True
        return False

    def save_model(self, request, obj, form, change):
        if not change and 'site_id' in request.GET:
            obj.site = Site.objects.get(pk=request.GET['site_id'])

        obj.user = request.user
        super(SettingsAdmin, self).save_model(request, obj, form, change)

    @csrf_protect_m
    def add_view(self, request, form_url='', extra_context=None):
        site_id = request.GET.get('site_id', None)

        if not site_id:
            return self.select_site_view(request)
        else:
            try:
                site_id = self.model._meta.pk.to_python(site_id)
                site = Site.objects.get(pk=site_id)
            except (Site.DoesNotExist, ValidationError, ValueError):
                return self.select_site_view(request)
            else:
                try:
                    obj = self.model.objects.get(site=site)
                    change_url = reverse(
                        'admin:%s_%s_change' % self.get_model_info(), args=(obj.pk,),
                        current_app=self.admin_site.name)
                    msg = _('{0} for "{1}" already exists. You may edit it below.')\
                        .format(self.opts.verbose_name, site.domain)
                    self.message_user(request, msg)
                    return HttpResponseRedirect(change_url)
                except self.model.DoesNotExist:
                    pass
        return super(SettingsAdmin, self).add_view(request, form_url, extra_context)

    def get_site_choices(self):
        site_choices = []
        for site in Site.objects.all():
            option_label = '{0} ({1})'.format(site.domain, site.name)
            site_choices.append((site.id, option_label))
        return site_choices

    def select_site_view(self, request, form_url=''):
        """
        Display a choice form to select which site to add settings.
        """
        if not self.has_add_permission(request):
            raise PermissionDenied

        extra_qs = ''
        if request.META['QUERY_STRING']:
            extra_qs = '&' + request.META['QUERY_STRING']

        site_choices = self.get_site_choices()

        if len(site_choices) == 1:
            return HttpResponseRedirect('?site_id={0}{1}'.format(site_choices[0][0], extra_qs))

        # Create form
        form = self.select_site_form(
            data=request.POST if request.method == 'POST' else None,
            initial={'site': site_choices[0][0]}
        )

        form.fields['site'].choices = site_choices

        if form.is_valid():
            return HttpResponseRedirect(
                '?site_id={0}{1}'.format(form.cleaned_data['site'], extra_qs))

        # Wrap in all admin layout
        fieldsets = ((None, {'fields': ('site',)}),)
        adminForm = AdminForm(form, fieldsets, {}, model_admin=self)
        media = self.media + adminForm.media

        context = {
            'title': _('Add %s') % force_text(self.opts.verbose_name),
            'adminform': adminForm,
            'is_popup': '_popup' in request.REQUEST,
            'media': mark_safe(media),
            'errors': AdminErrorList(form, ()),
            'app_label': self.opts.app_label,
        }

        return self.render_select_site_form(request, context, form_url)

    def render_select_site_form(self, request, context, form_url=''):
        """
        Render the site choice form.
        """
        app_label = self.opts.app_label
        context.update({
            'has_change_permission': self.has_change_permission(request),
            'form_url': mark_safe(form_url),
            'opts': self.opts,
            'add': True,
            'save_on_top': self.save_on_top,
        })

        context_instance = RequestContext(request, current_app=self.admin_site.name)

        return render_to_response(self.select_site_form_template or [
            'admin/%s/%s/select_site_form.html' % (app_label, self.opts.object_name.lower()),
            'admin/%s/select_site_form.html' % app_label,
            'admin/usersettings/select_site_form.html',  # added default here
            'admin/select_site_form.html'
        ], context, context_instance=context_instance)

    @csrf_protect_m
    def changelist_view(self, request, extra_context=None):
        sites_count = Site.objects.count()
        if sites_count == 1:
            site = Site.objects.get()
            try:
                obj = self.model.objects.get(site=site)
                change_url = reverse(
                    'admin:%s_%s_change' % self.get_model_info(), args=(obj.pk,),
                    current_app=self.admin_site.name)
                return HttpResponseRedirect(change_url)
            except self.model.DoesNotExist:
                add_url = '%s?site_id=%s' % (
                    reverse('admin:%s_%s_add' % self.get_model_info(),
                            current_app=self.admin_site.name), site.pk)
                return HttpResponseRedirect(add_url)

        else:
            return super(SettingsAdmin, self).changelist_view(request, extra_context)
