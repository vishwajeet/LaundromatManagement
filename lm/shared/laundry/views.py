import os
import datetime
import operator

from django.conf import settings
from django.shortcuts import render,render_to_response
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.template.loader import get_template

from .forms import OrderForm, CustomerForm
from .models import Customer, Order

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
          return render_to_response('laundry/add_order.xhtml',template_context,context_instance=RequestContext(request))
  
    order_form = OrderForm()
    customer_form = CustomerForm()
    template_context = {'order_form': order_form,'customer_form':customer_form}
    return render_to_response('laundry/add_order.xhtml',template_context,context_instance=RequestContext(request))

def order_edit(request,order_id):
    try:
        order = Order.objects.get(id=order_id)
    except:
        raise Http404
    if request.POST:
        order_form = OrderForm(request.POST,instance=order)
        customer_form = CustomerForm(request.POST,instance=order.customer)
        if customer_form.is_valid() and order_form.is_valid():
            customer_form.save()
            order_form.save()
        else:
            template_context = {'order_form': order_form,'customer_form':customer_form, 'order':order}
            return render_to_response('laundry/edit_order.xhtml',template_context,context_instance=RequestContext(request))
        
    order_form = OrderForm(instance=order)
    customer_form = CustomerForm(instance=order.customer)
    template_context = {'order_form': order_form,'customer_form':customer_form, 'order':order}
    return render_to_response('laundry/edit_order.xhtml',template_context,context_instance=RequestContext(request))

    
def compute_bill(request):
    '''
    upto 3 kgs 100
    upto 4 kgs 125
    upto 5 150
    upto 6 175
    upto 7 200
    Above 7 200+30*extra kgs
    '''
    rates = {'0':0,'3':100,'4':125,'5':150,'6':175,'7':200}
    
    wash_load = request.GET.get('wash_load', 0)
    iron_load = request.GET.get('iron_load', 0)
    discount = request.GET.get('discount', 0)
    
    wash_load_int = int(wash_load)
    iron_load_int = int(iron_load)
    discount = int(discount)
    wash_cost = 0
    if wash_load_int > 7:
        excess_load = wash_load_int-7
        wash_cost = rates['7'] + excess_load*30
    else:
        wash_cost = rates[wash_load]
    
    iron_cost = iron_load_int*5
    total = wash_cost+iron_cost - discount
    
    
    data = {'total':total,'wash_cost':wash_cost,'iron_cost':iron_cost}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype="application/json")

def get_orders(request):
    query = request.GET.get("q", 'pending')
    orders = Order.objects.all().order_by('-date')
    if query=='pending':
        orders = orders.exclude(status='DE')
    if query=='delivered':
        orders = orders.filter(status='DE')
    template_context = {'orders':orders}
    return render_to_response('laundry/orders.xhtml',template_context,context_instance=RequestContext(request))

def get_customers(request):
    customers =  list(Customer.objects.all())
    customers.sort(key=lambda x: x.last_visit,reverse=True)
    template_context = {'customers':customers}
    return render_to_response('laundry/customers.xhtml',template_context,context_instance=RequestContext(request))

    
    

