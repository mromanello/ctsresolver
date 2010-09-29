from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^~56k/ctsresolver/info', 'ctsresolver.resolv.views.list_providers'),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^~56k/ctsresolver/admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^~56k/ctsresolver/admin/', include(admin.site.urls)),
)
