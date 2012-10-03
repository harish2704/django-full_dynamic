from django.conf.urls.defaults import patterns, include, url
from settings import pdir

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xxx.views.home', name='home'),
    url(r'^bill/', include('billing.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root':pdir +'/static','show_indexes':True}),
    # url(r'^localmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root':pdir +'/media','show_indexes':True}),
)
