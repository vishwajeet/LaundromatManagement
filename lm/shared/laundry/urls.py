from django.conf.urls.defaults import patterns, include, url
from django.conf import settings


from laundry.views import add_customer,customer_detail,add_order,compute_bill

urlpatterns = patterns('',
          url(r'^customer/add/$', add_customer,name='add-customer'),
          url(r'^order/add/$', add_order,name='add-order'),
          url(r'^customer/detail/$', customer_detail,name='customer-detail'),
           url(r'^computebill/$', compute_bill,name='compute-bill'),
        )