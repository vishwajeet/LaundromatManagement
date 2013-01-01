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

from .forms import OrderForm, CustomerForm
from .models import Customer

def add_customer(request):
    pass

def customer_detail(request):
    mobile_no = request.GET.get('mobile_no', None)
    try:
        mobile_no = int(mobile_no)
        customer = Customer.objects.get(mobile_number=mobile_no)
        name = customer.name
        email = customer.email
        address = customer.address
        data = {'success':True,'name':name, 'email':email, 'address':address}
    except:
        data = {'success':False}
    

    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype="application/json")
    

def add_order(request):
    if request.POST:
        order_form = OrderForm(request.POST)
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid() and order_form.is_valid():
            customer = None
            try:
                customer = Customer.objects.get(mobile_number=customer_form.cleaned_data['mobile_number'])
            except:
                pass
            if not customer:
                customer = customer_form.save()
                
            order_form.instance.customer = customer
            order = order_form.save()
            template_context = {'customer':customer,'order':order}
            return render_to_response('laundry/order_success.xhtml',template_context,context_instance=RequestContext(request))
        else:
          template_context = {'order_form': order_form,'customer_form':customer_form}
          return render_to_response('laundry/order.xhtml',template_context,context_instance=RequestContext(request))
  
    order_form = OrderForm()
    customer_form = CustomerForm()
    template_context = {'order_form': order_form,'customer_form':customer_form}
    return render_to_response('laundry/order.xhtml',template_context,context_instance=RequestContext(request))

def compute_bill(request):
    '''
    upto 3 kgs 100
    upto 4 kgs 130
    upto 5 150
    upto 6 180
    upto 7 200
    Above 7 200+30*extra kgs
    '''
    rates = {'3':100,'4':130,'5':150,'6':180,'7':200}
    
    wash_load = request.GET.get('wash_load', None)
    iron_load = request.GET.get('iron_load', None)
    
    wash_load_int = int(wash_load)
    iron_load_int = int(iron_load)
    wash_cost = 0
    if wash_load_int > 7:
        excess_load = wash_load_int-7
        wash_cost = rates['7'] + excess_load*30
    else:
        wash_cost = rates[wash_load]
    
    iron_cost = iron_load_int*5
    total = wash_cost+iron_cost
    
    
    data = {'total':total}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype="application/json")
    

