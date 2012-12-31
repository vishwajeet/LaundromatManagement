import os
import datetime

from django.conf import settings
from django.shortcuts import render,render_to_response
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.template.loader import get_template

from .forms import OrderForm

def add_customer(request):
    pass

def customer_detail(request,query):
    pass

def add_order(request):
    form = OrderForm()
    template_context = {'form': form}
    return render_to_response('laundry/order.xhtml',template_context,context_instance=RequestContext(request))

