
from django.http import HttpResponse, Http404, get_host
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponsePermanentRedirect, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sessions.models import Session
from django.utils import simplejson
from django.utils.cache import patch_vary_headers
from django.views.generic.simple import direct_to_template
from django.views.defaults import page_not_found

from laundry.models import Store



class StoreMiddleware(object):
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        if( settings.DEBUG and request.path.startswith(settings.MEDIA_URL)):
            return
                
        request.store = None
        try:
            slug = view_kwargs.get('store_slug',None)
            if slug:
                request.store = Store.objects.get(code=slug)
        except:
            pass

        return None
        
           
