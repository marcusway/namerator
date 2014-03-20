from django.conf.urls import patterns, include, url
from mysite.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^hello/$', hello),
    url(r'^time/$', current_datetime),
    url(r'^fight/(\w+)/(\w+)/(\d+)/$', fight),
    url(r'^namerator/$', input_form),
    url(r'^make-names/.*', make_random_name)
)
