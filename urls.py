from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # List all the CTS webservices that are being harvested
    (r'^~56k/ctsresolver/info', 'ctsresolver.resolv.views.list_providers'),
    # Ping a CTS repository
    (r'^~56k/ctsresolver/ping/(.*?)$', 'ctsresolver.resolv.views.ping'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^~56k/ctsresolver/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^~56k/ctsresolver/admin/', include(admin.site.urls)),
)
