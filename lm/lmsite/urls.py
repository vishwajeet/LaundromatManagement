from django.conf.urls.defaults import patterns, include, url

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
            (r'^$','direct_to_template', {'template': 'index.xhtml'}),
    # Examples:
    # url(r'^$', 'LBTP.views.home', name='home'),
    # url(r'^LBTP/', include('LBTP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^lm/', include('laundry.urls')),
)


if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns = patterns('',
            (r'^%s(?P<path>.*)$' % _media_url,serve, {'document_root': settings.MEDIA_ROOT})
        )+urlpatterns