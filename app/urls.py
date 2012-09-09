from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^info/$', 'defapp.views.index'),
    (r'^$', 'defapp.views.logo'),
    url(r'^admin/', include(admin.site.urls)),
)
