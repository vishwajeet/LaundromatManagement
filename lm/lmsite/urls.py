from django.conf.urls.defaults import patterns, include, url

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from laundry.views import index

urlpatterns = patterns('',
    url(r'^$', index,name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
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