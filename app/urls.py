from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'queue.views.index'),
    (r'^company/(?P<company_id>.*)$', 'queue.views.companies'),
    (r'^services/(?P<company_id>[0-9]+)/(?P<service_id>.*)$', 'queue.views.services'),
    (r'^choosedate/(?P<company_id>[0-9]+)/(?P<service_id>[0-9]+).*$', 'queue.views.choosedate'),
    (r'^choosetime/(?P<company_id>[0-9]+)/(?P<service_id>[0-9]+)/(?P<day>[0-9]{4}\-[0-9]{2}\-[0-9]{2}).*$', 'queue.views.choosetime'),
    (r'^apply/(?P<vis_point>[0-9]+).*$', 'queue.views.apply'),
    (r'^login/$', 'queue.views.login'),
    (r'^logout/$', 'queue.views.logout'),
    (r'^operator/$', 'queue.views.operator'),
    (r'^operator/set_request_status/(?P<request_id>[0-9]+)/(?P<status>[a-z]+).*$', 'queue.views.operator_set_request_status'),
    (r'^operator/view_request/(?P<request_id>[0-9]+).*$', 'queue.views.operator_view_request' ),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
