from django.conf.urls.defaults import patterns, include, url

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from laundry.views import index
from laundry.forms import CustomLoginForm

store_slug = '(?P<store_slug>[-\w]+)'

urlpatterns = patterns('',
    url(r'^$', index,name='index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^%s/' % store_slug, include('laundry.urls'))
)

urlpatterns = patterns('',
        url(r'^login/$', 'laundry.views.login_user', name="login_user")
)+urlpatterns

if settings.DEBUG:
    from django.views.static import serve
    _media_url = settings.MEDIA_URL
    if _media_url.startswith('/'):
        _media_url = _media_url[1:]
        urlpatterns = patterns('',
            (r'^%s(?P<path>.*)$' % _media_url,serve, {'document_root': settings.MEDIA_ROOT})
        )+urlpatterns