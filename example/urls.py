from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^current-usersettings/$',
        TemplateView.as_view(template_name='example/current-usersettings.html'),
        name='current_usersettings'),
)
