from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    url(r'^manage/', include(admin.site.urls)),
    url(r'^current-usersettings/$',
        TemplateView.as_view(template_name='example/current-usersettings.html'),
        name='current_usersettings'),
]
