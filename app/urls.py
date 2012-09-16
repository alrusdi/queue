from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'queue.views.index'),
    (r'^company/(?P<company_id>.*)$', 'queue.views.companies'),
    (r'^services/(?P<company_id>[0-9]+)/(?P<service_id>.*)$', 'queue.views.services'),
    (r'^apply/(?P<company_id>[0-9]+)/(?P<service_id>[0-9]+).*$', 'queue.views.apply'),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
