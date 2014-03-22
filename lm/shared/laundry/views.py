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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

from .forms import OrderForm, CustomerForm,CustomLoginForm
from .models import Customer, Order,Rates

def add_customer(request):
    pass

@login_required
def index(request,store_slug=None):
    if store_slug==None:
        logout(request)
        return HttpResponseRedirect('/login/')
    template_context = {}
    return render_to_response('index.xhtml',template_context,context_instance=RequestContext(request))


def customer_detail(request,store_slug):
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
    

def add_order(request,store_slug):
    if request.POST:
        order_form = OrderForm(request.POST)
        customer_form = CustomerForm(request.POST)
        customer_form.instance.store = request.store
        if customer_form.is_valid() and order_form.is_valid():
            customer = None
            try:
                customer = Customer.objects.get(mobile_number=customer_form.cleaned_data['mobile_number'])
            except:
                pass
            if not customer:
                customer = customer_form.save()
                
            order_form.instance.customer = customer
            order_form.instance.store = request.store
            order = order_form.save()
            template_context = {'customer':customer,'order':order}
            return render_to_response('laundry/order_success.xhtml',template_context,context_instance=RequestContext(request))
        else:
          template_context = {'order_form': order_form,'customer_form':customer_form}
          return render_to_response('laundry/add_order.xhtml',template_context,context_instance=RequestContext(request))
  
    order_form = OrderForm(initial={'store': request.store.id})
    customer_form = CustomerForm(initial={'store': request.store.id})
    template_context = {'order_form': order_form,'customer_form':customer_form}
    return render_to_response('laundry/add_order.xhtml',template_context,context_instance=RequestContext(request))

def order_edit(request,store_slug,order_id):
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

    
def compute_bill(request,store_slug):
    '''

    '''

    store_rate = Rates.objects.get(store=request.store)
    
    wash_load = request.GET.get('wash_load', 0)
    iron_load = request.GET.get('iron_load', 0)
    discount = request.GET.get('discount', 0)
    is_urgent = request.GET.get('is_urgent', 0)
    
    wash_load_int = int(wash_load)
    iron_load_int = int(iron_load)
    discount = int(discount)
    wash_cost = 0
    if wash_load_int < 4:
        wash_load_int = 4
    if wash_load_int > 7:
        excess_load = wash_load_int-7
        wash_cost = store_rate.wr_upto_7kg + store_rate.wr_per_kg*excess_load
    else:
        wr_var = "wr_upto_" + str(wash_load_int) + "kg"
        wash_cost  = getattr(store_rate, wr_var)
    
    iron_cost = iron_load_int*store_rate.iron_rate
    total = wash_cost+iron_cost - discount
    if is_urgent=='true':
        total = total + store_rate.premium
    
    data = {'total':total,'wash_cost':wash_cost,'iron_cost':iron_cost}
    json = simplejson.dumps(data)
    return HttpResponse(json, mimetype="application/json")

def get_orders(request,store_slug):
    status = request.GET.get("q", None)
    cust = request.GET.get("c", None)
    orders = Order.objects.filter(store=request.store).order_by('-date')
    if status=='pending':
        orders = orders.exclude(status='DE')
    if status=='delivered':
        orders = orders.filter(status='DE')
    if cust:
        orders = orders.filter(customer__id=cust)
    template_context = {'orders':orders}
    return render_to_response('laundry/orders.xhtml',template_context,context_instance=RequestContext(request))

def get_customers(request,store_slug):
    customers =  list(Customer.objects.filter(store=request.store))
    customers.sort(key=lambda x: x.last_visit,reverse=True)
    template_context = {'customers':customers}
    return render_to_response('laundry/customers.xhtml',template_context,context_instance=RequestContext(request))

    

def login_user(request):
    username = password = ''
    form = CustomLoginForm()
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        store    = request.POST['store']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                url = "/"+ store + "/"
                return HttpResponseRedirect(url)
    return render_to_response('registration/login.html', {'form':form},context_instance=RequestContext(request))

